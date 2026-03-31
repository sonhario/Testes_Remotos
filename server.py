#!/usr/bin/env python3
"""Local dev server with save endpoint for region editor."""
import http.server
import json
import os

PORT = 8080
SAVE_PATH = "regioes_eldorado.json"


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/save_regions":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            with open(SAVE_PATH, "w") as f:
                f.write(body.decode("utf-8"))
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"ok": True, "path": SAVE_PATH}).encode())
            print(f"  → Salvo {SAVE_PATH} ({length} bytes)")
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        if "save_regions" in str(args):
            super().log_message(format, *args)


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    server = http.server.HTTPServer(("0.0.0.0", PORT), Handler)
    print(f"Servidor em http://localhost:{PORT}")
    print(f"Regiões serão salvas em: {os.path.abspath(SAVE_PATH)}")
    server.serve_forever()
