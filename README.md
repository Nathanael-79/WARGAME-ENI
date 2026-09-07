# Wargame - Exfiltration sur l'intranet ESD

Module Wargame - ESD Cybersecurity Academy

## Présentation

Challenge CTF de catégorie **Réseau**, difficulté **Difficile (300 pts)**.

Scénario : le SOC de l'ESD Academy intercepte un trafic suspect sur l'intranet
pédagogique. Un stagiaire a exfiltré le corrigé d'un examen blanc vers un
service de dépôt interne. Une capture réseau (`capture.pcap`) est fournie ;
il faut reconstituer le document exfiltré et retrouver la clé qui l'ouvre pour
obtenir le flag.

Le contenu exfiltré n'apparaît jamais en clair : l'archive est **transmise en
deux morceaux** à recoller, puis décodée (Base64 → ZIP), et son **mot de passe
est encodé en Base64** dans un en-tête HTTP d'un autre échange.

## Organisation du dépôt

```
challenge-exfiltration-esd/
├── challenge.yml              fiche de déploiement CTFd (titre, énoncé, flag)
├── WriteUp.md                 solution détaillée, reproductible pas à pas
├── src/public/capture.pcap    capture réseau remise au joueur
└── build.py / server.py       génération de la capture (reproductibilité)
```

Prérequis : `tcpdump`, `zip`, `python3`, `tshark`.

## Conformité à la note de cadrage

- Catégorie Réseau, difficulté Difficile (300 pts), flag au format `ESD{...}`
  sans espace et sensible à la casse.
- Références ESD Academy (intranet pédagogique, dashboard stagiaire, ENT,
  forum, promo NESD_006).
- Pas de guessing : chaque élément nécessaire (bon hôte, ordre des morceaux,
  mot de passe) est présent dans la capture.
- Pas de bruteforce, pas de stéganographie, pas d'OSINT, pas d'IPS/blocage.

## Auteur

Nathanael - ESD Cybersecurity Academy (promo NESD_006)
