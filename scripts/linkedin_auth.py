#!/usr/bin/env python3
"""LinkedIn OAuth — server locale cattura codice e scambia per token."""
import json
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from agents.social_publisher import exchange_code

CLIENT_ID = __import__("os").getenv("LINKEDIN_CLIENT_ID", "") or "863hwbrm55axm1"
PORT = 8888
REDIRECT = f"http://localhost:{PORT}"

AUTH_URL = (
    "https://www.linkedin.com/oauth/v2/authorization"
    f"?response_type=code&client_id={CLIENT_ID}"
    f"&redirect_uri={REDIRECT}"
    "&scope=w_member_social%20openid%20profile%20email"
)

received_code = None


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        global received_code
        params = parse_qs(urlparse(self.path).query)
        err = params.get("error", [None])[0]
        code = params.get("code", [None])[0]

        if err:
            self.send_response(400)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(f"<h1>Errore</h1><p>{err}</p>".encode())
            print(f"ERRORE: {err}")
            return

        if code:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<html><body><h1>Autorizzato!</h1><p>Puoi chiudere.</p></body></html>")
            global received_code
            received_code = code
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"<h1>Nessun codice</h1>")

    def log_message(self, format, *args):
        pass


print("=" * 60)
print("LINKEDIN AUTH — SERVER LOCALE")
print("=" * 60)
print()
print(f"Server su http://localhost:{PORT}")
print()
print("APRI NEL BROWSER (clicca o copia):")
print()
print(AUTH_URL)
print()
print("Autorizza l'app. Il codice verra' catturato automaticamente.")
print()

server = HTTPServer(("0.0.0.0", PORT), Handler)
server.timeout = 180

while received_code is None:
    server.handle_request()

print()
print("Codice ricevuto! Scambio per token...")
token = exchange_code(received_code)
if token:
    print("OK! Token salvato — LinkedIn publishing attivo.")
else:
    print("ERRORE: scambio token fallito")
    sys.exit(1)
