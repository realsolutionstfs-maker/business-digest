#!/usr/bin/env python3
import http.server
import json
import socketserver
from datetime import datetime
from pathlib import Path

PORT = 8080
LANDING = Path(__file__).parent / "templates" / "landing.html"


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            data = {
                "status": "ok",
                "time": datetime.now().isoformat(),
                "project": "Business Digest",
                "version": "1.0",
            }
            self.wfile.write(json.dumps(data).encode())
            return
        if self.path == "/" or self.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(LANDING.read_bytes())
            return
        super().do_GET()


if __name__ == "__main__":
    print(f"Serving at http://localhost:{PORT}")
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        httpd.serve_forever()
