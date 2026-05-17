# POC – Authenticatie als Plugin (Microkernel Architectuur)

Deze POC toont hoe je authenticatie als losse plugin kunt toevoegen aan een microkernel‑architectuur.  
De hub zelf blijft heel simpel: hij stuurt apparaten aan.  
De login‑functionaliteit zit volledig in een aparte plugin die je aan of uit kunt zetten.

De kern hoeft dus nooit aangepast te worden, wat precies het idee is van een microkernel.

## Wat deze POC laat zien
- De hub werkt met authenticatie (login verplicht)
- De hub werkt zonder authenticatie (open systeem)
- De plugin kan runtime aan/uit gezet worden via de loginpagina
- De kern blijft altijd hetzelfde
- De stack draait via Docker Swarm met 3 hub-replica's en 2 app-replica's
- Dit past bij ADR‑009 (microkernel met uitbreidbare plugins)

## Projectstructuur
poc-auth-plugin/
│
├── hub/
│   ├── app.py
│   ├── plugins/
│   │   └── auth_plugin.py
│   ├── templates/
│   │   ├── index.html
│   │   └── login.html
│   ├── Dockerfile
│   └── requirements.txt
│
├── app/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
│
└── poc.yml

## Starten

**Vereisten:**
- Docker
- Docker Swarm (ingebouwd in Docker Desktop)

**Images staan klaar op Docker Hub:**
- `quinxa/smarthome-hub:latest`
- `quinxa/smarthome-app:latest`

**Start de swarm en deploy de stack:**
docker swarm init
docker stack deploy -c poc.yml smarthome

**Ga naar:**  
http://localhost:5000

**Status controleren:**

docker stack ps smarthome   # welke containers draaien waar
docker service ls           # overzicht replica's per service

**Stack verwijderen:**
docker stack rm smarthome

## Authenticatie plugin
Standaard staat de plugin aan, dus je krijgt een loginpagina.

Je kunt inloggen met:
- `admin` / `admin123`
- `jan` / `smarthome`

## Login aan/uit zetten

Op de loginpagina staat een knop:

- **Plugin uitschakelen** → login verdwijnt, iedereen mag binnen
- **Plugin inschakelen** → login wordt weer verplicht

Dit werkt meteen, zonder herstarten en zonder de stack aan te passen.  
De status wordt bijgehouden in de sessie.

## Docker Swarm topologie

De stack bestaat uit 5 containers verdeeld over de swarm:
- `smarthome_hub` – 3 replica's – Flask-kern met auth-plugin
- `smarthome_app` – 2 replica's – Client die de hub periodiek bevraagt

Bij een echte multi-node setup (3 managers + 2 workers) kun je in `poc.yml` de placement constraints terugzetten:
# Hub → alleen op managers
placement:
  constraints:
    - node.role == manager

# App → alleen op workers
placement:
  constraints:
    - node.role == worker

## Waarom dit microkernel is
- De kern (hub) weet niet hoe authenticatie werkt
- De plugin wordt dynamisch geladen
- De plugin kan verwijderd, vervangen of uitgezet worden
- De kern blijft altijd hetzelfde

## Technologie
- Python 3.11
- Flask
- Docker & Docker Swarm
- Microkernel architectuur met dynamische plugin‑loading
