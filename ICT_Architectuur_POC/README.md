# Proof of Concept: Smart Home – Eén Gebruiker (Lokale Config)

Dit document bevat de volledige documentatie, architectonische onderbouwing en handleiding voor de Proof of Concept (PoC) binnen de ICT Architectuur. Deze opstelling valideert de functionele kern en de netwerkinfrastructuur in een minimalistische scope.

---

## 1. Waarvoor is deze PoC?
Het doel van deze PoC is het aantonen en valideren van de core-functionaliteit van het Smart Home-platform in zijn meest pure vorm. 

Om de focus volledig te leggen op de stabiliteit van de Docker Swarm-orchestratie en de betrouwbaarheid van de onderlinge service-communicatie, is onnodige complexiteit bewust weggelaten. De PoC simuleert het scenario van **één enkele, reguliere gebruiker met één account zonder administrator-rollen**. Hiermee wordt bewezen dat de lokale configuraties en de app-naar-hub-koppeling robuust werken, zónder dat er in deze fase al overhead van een ingewikkeld Role-Based Access Control (RBAC) of databasebeheer nodig is.

---

## 2. Verband met ons Onderzoek
Deze PoC vormt de tastbare, technische validatie van het hoofd- en deelonderzoek binnen het ICT Architectuurproject:
* **Validatie van de Microkernel-Architectuur:** Het onderzoekt of het fundament van onze architectuur (waarbij de App-interface en de centrale Hub-kernel zijn ontkoppeld) lokaal stabiel en met lage latency kan opereren als basis voor het latere plugin-mechanisme.
* **Security door Eenvoud (Least Privilege):** Het sluit direct aan bij het security-onderzoek. Door in deze fase *geen* admin-functionaliteiten of privileges in de codebase op te nemen, is het systeem inherent veilig tegen privilege-escalation. De focus ligt puur op de minimale rechten die nodig zijn voor een lokale bewoner.
* **Infrastructuur-Keuze:** De PoC dient als benchmark om te onderzoeken hoe Docker Swarm zich gedraagt met betrekking tot service-discovery en netwerkisolatie binnen een IoT/Smart Home-context.

---

## 3. Logische Componenten
De architectuur is opgedeeld in drie heldere, logische componenten om een strikte scheiding van taken (Separation of Concerns) te waarborgen:* **App Service (`/app`):** De Python/Flask frontend waarmee de eindgebruiker interactie heeft. Deze service vangt de HTTP-verzoeken van de gebruiker op en vertaalt deze naar interne API-calls richting de hub.
* **Hub Service (`/hub`):** De centrale, lokale controller (de Kernel) die de status van de slimme apparaten beheert en de logica aanstuurt via een centraal dashboard (`index.html`).
* **Docker Swarm Netwerk:** De infrastructurele lijm. Dit virtuele overlay-netwerk isoleert de interne communicatie tussen de App en de Hub van het publieke netwerk, en regelt de automatische service-discovery.

---

## 4. Architectonische Karakteristieken
Binnen het framework van software-architectuur valideert deze PoC specifiek de zeven vastgestelde kwaliteitsattributen (Quality Attributes) uit ons onderzoek, ingericht volgens de **Microkernel-stijl**:

* **Usability (Gebruiksvriendelijkheid):** Zorgt voor een eenvoudige, consistente UI en een gepersonaliseerde ervaring waarbij instellingen stabiel bewaard blijven voor de bewoner. De UI blijft stabiel doordat de complexiteit naar de kernel/plugins is verplaatst.
* **Interoperability (Interoperabiliteit):** Garandeert dat apparaten van verschillende merken en protocollen (via zowel *probe* als *announcement* gebaseerde discovery) succesvol met elkaar kunnen communiceren via specifieke adapters/plugins.
* **Configurability (Configureerbaarheid):** De kernel is configuratie-gedreven. Dit maakt het voor de gebruiker mogelijk om de status van apparaten, ruimtes en scenario's/automatisaties flexibel en los van de vaste code in te richten.
* **Security (Beveiliging):** Biedt netwerkisolatie op container-niveau en veilige authenticatie via een login, waardoor componenten minder afhankelijk van elkaar zijn en de kans op misbruik minimaal is.
* **Maintainability (Onderhoudbaarheid):** De codebasis is modulair opgebouwd met een duidelijke scheiding tussen UI en de core logica van de kernel, wat leidt tot herbruikbare componenten en eenvoudig onderhoud zonder duplicatie.
* **Reliability (Betrouwbaarheid):** Tijdgestuurde acties en apparaatontdekking zijn redundant opgezet. Mocht een specifieke apparaatintegratie falen, dan blijft de core kernel onafhankelijk en betrouwbaar doorwerken.
* **Performance (Efficiëntie):** Geen onnodige overhead van zware cloud-lookups of te complexe service-structuren. Dit minimaliseert het netwerkverkeer en garandeert een snelle, lokale respons op de hub.

---

## 5. Functionaliteit
- De hub geeft status terug via `/devices`.
- De app kan de hub bereiken en data tonen.
- De webinterface toont devices, status en het laatste commando.
- De oplossing is bewust beperkt tot één gebruiker zonder admin-rollen.

## 6. Deployment
### 6.1. Vereisten
- Docker
- Docker Swarm actief
- Internettoegang om images van Docker Hub te pullen

### 6.2. Stappen
```bash
cd ICT_Architectuur_POC/poc-smarthome
docker swarm init --advertise-addr 172.31.230.19
docker network create --driver overlay --attachable smarthome
docker stack deploy -c docker-compose.yml smarthome
```

### 6.3. Controle
```bash
docker service ls
docker stack ps smarthome
docker service logs smarthome_hub
docker service logs smarthome_app
```

### 6.4. Browser
- Hub: `http://172.31.230.19:5000`
- App: `http://172.31.230.19:5001`
