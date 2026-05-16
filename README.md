# POC – Authenticatie als Plugin (Microkernel Architectuur)

Deze POC toont hoe je authenticatie als losse plugin kunt toevoegen aan een microkernel-architectuur.
De hub zelf blijft heel simpel: hij stuurt apparaten aan.
De login-functionaliteit zit volledig in een aparte plugin die je aan of uit kunt zetten.

De kern hoeft dus nooit aangepast te worden, wat precies het idee is van een microkernel.

## Wat deze POC laat zien
- De hub werkt met authenticatie (login verplicht)
- De hub werkt zonder authenticatie (open systeem)
- De plugin kan runtime aan/uit gezet worden via de loginpagina
- De kern blijft altijd hetzelfde
- Dit past bij ADR-009 (microkernel met uitbreidbare plugins)

## Mapstructuur

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
└── poc.yaml

## Opstarten

Vereisten:
- Docker met Swarm-modus

Stap 1 – images bouwen:

    docker build -t hub:latest ./hub
    docker build -t app:latest ./app

Stap 2 – Swarm initialiseren (eenmalig):

    docker swarm init --advertise-addr <jouw-ip>

Stap 3 – stack deployen:

    docker stack deploy --compose-file poc.yaml poc

Ga naar:
    http://localhost:5000

## Stoppen

    docker stack rm poc

## Controleren

    docker stack services poc
    docker stack ps poc

## Authenticatie plugin

Standaard staat de plugin aan, dus je krijgt een loginpagina.

Je kunt inloggen met:
- admin / admin123
- jan / smarthome

Na de deploy moet je de plugin handmatig in de draaiende container plaatsen:

    docker ps  # zoek de container ID van poc_hub
    docker cp ./hub/plugins/auth_plugin.py <CONTAINER_ID>:/hub/plugins/

## Login aan/uit zetten

Op de loginpagina staat een knop:
- Plugin uitschakelen → login verdwijnt, iedereen mag binnen
- Plugin inschakelen → login wordt weer verplicht

Dit werkt meteen, zonder herstarten.
De status wordt bijgehouden in de sessie.

## Waarom dit microkernel is
- De kern (hub) weet niet hoe authenticatie werkt
- De plugin wordt dynamisch geladen
- De plugin kan verwijderd, vervangen of uitgezet worden
- De kern blijft altijd hetzelfde

## Technologie
- Python 3.11
- Flask
- Docker & Docker Swarm
- Microkernel architectuur met dynamische plugin-loading