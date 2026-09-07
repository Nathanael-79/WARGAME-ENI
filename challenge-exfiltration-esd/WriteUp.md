# Challenge
Exfiltration sur l'intranet ESD (Difficile - Réseau - 300 pts)

## Énoncé
Le SOC de l'ESD Academy a intercepté un trafic suspect sur l'intranet pédagogique. Un stagiaire semble avoir exfiltré le corrigé d'un examen blanc vers un service de dépôt interne, en deux envois, dans une archive protégée. Reconstituez le document et retrouvez la clé pour l'ouvrir.

Flag : `ESD{Antis3ch3_Du_S0C_ESD}`

## Solution
1. Ouvrir `capture.pcap` dans Wireshark, filtre `http.request`. On observe :
```
dashboard.esdacademy.eu   GET   /                  (anodin : dashboard stagiaire)
forum.esdacademy.eu       POST  /message           (leurre : message forum)
depot.esdacademy.eu       POST  /api/upload         (porte l'en-tete de clef)
ent.esdacademy.eu         GET   /                  (anodin : ENT)
depot.esdacademy.eu       POST  /upload/1          (1er morceau exfiltre)
depot.esdacademy.eu       POST  /upload/2          (2e morceau exfiltre)
```
Les deux POST vers `depot.esdacademy.eu/upload/1` et `/upload/2` portent la charge fractionnée.

2. `Follow` > `HTTP Stream` sur chacun des deux POST `/upload/*` (ou `File > Export Objects > HTTP`). Chaque corps est un fragment de Base64. **Concaténer les deux fragments dans l'ordre de capture** (`/upload/1` puis `/upload/2`) pour reconstituer le bloc Base64 complet.

3. Décoder ce bloc Base64. Ce n'est pas du texte : il commence par `UEsD` = octets `PK` = archive ZIP. On enregistre :
```
cat part1.b64 part2.b64 | base64 -d > corrige.zip
file corrige.zip      # Zip archive data
```

4. L'archive est protégée par mot de passe (`unzip` le demande). Inspecter le POST `/api/upload` : il porte un en-tête `X-Upload-Key`, mais sa valeur ressemble à du Base64 plutôt qu'à un mot de passe lisible. La décoder d'abord :
```
echo 'RXhhbTNuX0JsYW5jX05FU0RfMDA2' | base64 -d      # -> Exam3n_Blanc_NESD_006
```

5. Ouvrir l'archive avec le mot de passe décodé :
```
unzip -P 'Exam3n_Blanc_NESD_006' corrige.zip && cat corrige_examen.txt
```

Le document exfiltré contient le flag.

Flag : `ESD{Antis3ch3_Du_S0C_ESD}`

## Hints
- L'exfiltration est fractionnée en deux requêtes vers le service de dépôt (`/upload/1`, `/upload/2`) : recollez les deux corps (dans l'ordre de capture) avant de décoder le Base64.
- La charge recollée n'est pas du texte : décodez le Base64 et regardez les premiers octets (`UEsD` / `PK`) = archive ZIP.
- L'archive est protégée par mot de passe.
- La clé n'est pas écrite en clair : elle est en Base64 dans l'en-tête `X-Upload-Key` du POST `/api/upload`. Décodez-la avant de vous en servir.

## Clins d'œil de la consigne (pour le helper)
- "deux envois séparés, dans l'ordre" -> les deux morceaux `/upload/1` et `/upload/2` à concaténer dans l'ordre de capture.
- "deux petites lettres trahissent l'archive, même déguisée" -> après Base64, octets `PK` = archive ZIP.
- "la clé maquillée dans un en-tête, à faire passer par le même décodeur" -> en-tête `X-Upload-Key` encodé en Base64 (à décoder comme le reste).
- "service de dépôt" -> hôte `depot.esdacademy.eu` (les autres hôtes `dashboard`, `ent`, `forum` sont anodins/leurres).

## Notes de conception (conformité note de cadrage)
- Catégorie Réseau, difficulté Difficile (300 pts). Références ESD Academy (intranet, dashboard stagiaire, ENT, forum, promo NESD_006).
- Pas de guessing : chaque élément (bon hôte, ordre des morceaux, mot de passe) est présent dans la capture.
- Pas de bruteforce, pas de stéganographie, pas d'OSINT, pas d'IPS/blocage.
- Flag au format `ESD{...}`, sans espace, sensible à la casse.

## Régénérer la capture
Prérequis : `tcpdump zip python3 tshark`. Dans ce dossier, 3 terminaux :
1. `python3 server.py`
2. `sudo tcpdump -i lo -w capture.pcap port 8080`
3. `python3 build.py`
Puis Ctrl+C sur le terminal 2, et `mv capture.pcap src/public/capture.pcap`.
