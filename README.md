POC – Authenticatie als Plugin (Microkernel Architectuur)

Deze POC toont hoe je authenticatie als losse plugin kunt toevoegen aan een microkernel‑architectuur.  
De hub zelf blijft heel simpel: hij stuurt apparaten aan.  
De login‑functionaliteit zit volledig in een aparte plugin die je aan of uit kunt zetten.

De kern hoeft dus nooit aangepast te worden, wat precies het idee is van een microkernel.

Wat deze POC laat zien
- De hub werkt met authenticatie (login verplicht)
- De hub werkt zonder authenticatie (open systeem)
- De plugin kan runtime aan/uit gezet worden via de loginpagina
- De kern blijft altijd hetzelfde
- Dit past bij ADR‑009 (microkernel met uitbreidbare plugins)

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
└── docker-compose.yml

Starten
Vereisten:
- Docker
- Docker Compose

Start alles:
docker compose up --build

Ga naar:
http://localhost:5000

Authenticatie plugin

Standaard staat de plugin aan, dus je krijgt een loginpagina.

Je kunt inloggen met:
- admin / admin123
- jan / smarthome

login aan/uit zetten (NIEUW)
Op de loginpagina staat een knop:

- Plugin uitschakelen → login verdwijnt, iedereen mag binnen  
- Plugin inschakelen → login wordt weer verplicht  

Dit werkt meteen, zonder herstarten en zonder docker‑compose aan te passen.
De status wordt bijgehouden in de sessie.

Waarom dit microkernel is
- De kern (hub) weet niet hoe authenticatie werkt  
- De plugin wordt dynamisch geladen  
- De plugin kan verwijderd, vervangen of uitgezet worden  
- De kern blijft altijd hetzelfde  


Technologie
- Python 3.11
- Flask
- Docker & Docker Compose
- Microkernel architectuur met dynamische plugin‑loading
