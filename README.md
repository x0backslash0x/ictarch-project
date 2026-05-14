POC Authenticatie als plugin: 
POC — Authenticatie als Plugin (Microkernel)

Doel

Deze POC test of authenticatie als plugin kan werken binnen een microkernel architectuur in plaats van dat het vast in de kern zit.

De conclusie is dat dit kan. De hub werkt zowel met als zonder auth plugin en de kern hoeft daarvoor niet aangepast te worden.

Structuur

poc-auth-plugin/

* hub (microkernel kern)

  * app.py (laadt plugins dynamisch)
  * plugins/

    * auth_plugin.py
  * templates/

    * index.html
    * login.html
  * Dockerfile
  * requirements.txt
* app (client die een mobiele app simuleert)

  * app.py
  * Dockerfile
  * requirements.txt
* docker-compose.yml

Starten
Vereisten

* Docker en Docker Compose geïnstalleerd op Debian
Met auth plugin (login actief)
docker compose up --build

Ga naar [http://localhost:5000](http://localhost:5000) in je browser
Je krijgt een login scherm met
* admin / admin123
* jan / smarthome

Zonder auth plugin (open modus)

In docker-compose.yml dit stuk uit commentaar zetten:
* ./hub/plugins:/hub/plugins

Daarna opnieuw starten:
docker compose up --build

Ga opnieuw naar [http://localhost:5000](http://localhost:5000)
Nu kom je direct binnen zonder login omdat de plugin niet geladen wordt

Wat dit bewijst
* de kern werkt zonder auth plugin
* de kern werkt met auth plugin
* de kern hoeft niet aangepast te worden
* de auth functionaliteit zit volledig los van de kern

Dit past bij ADR-009 microkernel architectuur waarbij plugins los staan van de kern en je makkelijk functionaliteit kan toevoegen of verwijderen zonder de core te veranderen

Technologie
* Python 3.11 op Debian 12
* Flask
* Docker en Docker Compose
