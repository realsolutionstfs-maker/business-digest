#!/usr/bin/env python3
"""Simple landing page server for Business Digest."""
import http.server
import socketserver
from pathlib import Path

PORT = 8080
LANDING = Path(__file__).parent / "templates" / "landing.html"


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(LANDING.read_bytes())
        else:
            super().do_GET()


if __name__ == "__main__":
    print(f"Serving landing page at http://localhost:{PORT}")
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        httpd.serve_forever()
