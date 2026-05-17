# POC — Smart Home: Eén Gebruiker (Lokale Config)

## Beschrijving
Deze Proof of Concept (POC) demonstreert de core-functionaliteit van ons Smart Home-platform in zijn meest pure vorm. 
Het doel is om te laten zien hoe de applicatie lokaal werkt voor **één enkele, reguliere gebruiker met één account, zonder de complexiteit van admin-rollen, rechtenbeheer of zware database-overhead**. De focus ligt puur op een stabiele, betrouwbare basisconfiguratie.

## Functionaliteiten
* **Lokale Status:** De Hub beheert en serveert de apparaatstatus via `/devices`.
* **Ontkoppelde Communicatie:** De App kan de Hub feilloos bereiken en data ophalen over het netwerk.
* **Webinterface:** Overzichtelijk dashboard dat actieve apparaten, live status en het laatst uitgevoerte commando toont.
* **Security door Eenvoud:** Inherent veilig tegen privilege-escalation omdat admin-endpoints en rollen bewust ontbreken.

## ADR002 (Account verplicht)
* **Usability & Security:** Toont aan hoe de app functioneert wanneer deze gekoppeld is aan één vast gebruikersaccount zonder extra admin-rechten.
* **Microkernel-stijl:** De UI (App) en de core-logica (Hub/Kernel) zijn strikt gescheiden, waardoor de hub stabiel blijft draaien als de interface herstart.

## Architectuur
Web Browser ---> App Service (`/app` - Python/Flask Frontend) ---> (Interne API-calls over Docker Swarm Netwerk) ---> Hub Service (`/hub` - Centrale Kernel)  

## Starten

### Handleiding en Commando's

#### Stap 1: Navigeer naar de juiste directory
``cd ICT_Architectuur_POC/poc-smarthome``

#### Stap 2: Initialiseer Docker Swarm (indien nog niet actief)
``docker swarm init --advertise-addr 172.31.230.19``

#### Stap 3: Maak het overlay netwerk aan
``docker network create --driver overlay --attachable smarthome``

#### Stap 4: Deploy de applicatiestack binnen het Swarm-cluster
``docker stack deploy -c docker-compose.yml smarthome``

#### Stap 5: Controleer de status van de opgestarte services
``docker service ls``

#### Browser openen
1) Hub (Kernel Dashboard): ``http://172.31.230.19:5000``
2) App (Gebruikersinterface): ``http://172.31.230.19:5001``

#### Stoppen
``docker stack rm smarthome``
