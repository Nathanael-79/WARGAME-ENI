#!/usr/bin/env python3
# server.py - petit serveur qui imite les services de l'intranet ESD Academy.
# Il sert uniquement a generer la capture reseau (il est appele par build.py).
# Chaque URL demandee renvoie une reponse differente.

from http.server import BaseHTTPRequestHandler, HTTPServer

# Reponse renvoyee selon l'URL demandee en POST
REPONSES_POST = {
    "/api/upload": b'{"status":"init","session":"ok"}\r\n',
    "/message":    b"Message poste sur le forum stagiaire.\r\n",
}

class Serveur(BaseHTTPRequestHandler):

    def repondre(self, corps):
        """Envoie une reponse HTTP 200 avec le corps donne."""
        self.send_response(200)
        self.send_header("Server", "ESD-Intranet/1.0")
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(corps)))
        self.send_header("Connection", "close")
        self.end_headers()
        self.wfile.write(corps)

    def do_GET(self):
        # Toutes les pages consultees renvoient la meme page d'accueil
        self.repondre(b"<html>ESD Academy - Intranet pedagogique</html>\r\n")

    def do_POST(self):
        # On lit (et ignore) le corps envoye par le client
        taille = int(self.headers.get("Content-Length", 0))
        self.rfile.read(taille)

        if self.path.startswith("/upload"):
            # Reception d'un morceau exfiltre
            self.repondre(b'{"status":"received"}\r\n')
        else:
            # /api/upload, /message, ou autre
            self.repondre(REPONSES_POST.get(self.path, b"OK\r\n"))

    def log_message(self, *args):
        pass  # on desactive les logs pour ne pas polluer le terminal

# Demarre le serveur sur le port 8080 (en local)
HTTPServer(("127.0.0.1", 8080), Serveur).serve_forever()
