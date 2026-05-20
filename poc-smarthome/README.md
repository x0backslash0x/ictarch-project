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

#### Deployment commands

```bash
docker login
docker swarm init --advertise-addr <IP-VAN-DIE-LAPTOP>
docker network create --driver overlay --attachable smarthome
docker stack deploy -c docker-compose.yml smarthome
```

#### Browser openen
1) Hub (Kernel Dashboard): ``http://localhost:5000``
2) App (Gebruikersinterface): ``http://localhost:5001``

#### Stoppen
``docker stack rm smarthome``
