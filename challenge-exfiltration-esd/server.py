#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, HTTPServer

REPONSES_POST = {
    "/api/upload": b'{"status":"init","session":"ok"}\r\n',
    "/message":    b"Message poste sur le forum stagiaire.\r\n",
}

class Serveur(BaseHTTPRequestHandler):

    def repondre(self, corps):
        self.send_response(200)
        self.send_header("Server", "ESD-Intranet/1.0")
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(corps)))
        self.send_header("Connection", "close")
        self.end_headers()
        self.wfile.write(corps)

    def do_GET(self):
        self.repondre(b"<html>ESD Academy - Intranet pedagogique</html>\r\n")

    def do_POST(self):
        taille = int(self.headers.get("Content-Length", 0))
        self.rfile.read(taille)
        if self.path.startswith("/upload"):
            self.repondre(b'{"status":"received"}\r\n')
        else:
            self.repondre(REPONSES_POST.get(self.path, b"OK\r\n"))

    def log_message(self, *args):
        pass

HTTPServer(("127.0.0.1", 8080), Serveur).serve_forever()
