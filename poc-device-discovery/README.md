# POC — Probe-based Device Discovery

## Doel van deze POC

Deze POC beantwoordt de technische vraag uit **ADR-004**:

> *"Hoe ontdekt de hub actief apparaten op het netwerk via probe-based discovery?"*

### Wat wordt aangetoond?

In een echt smart home systeem weet de hub niet op voorhand welke apparaten
aanwezig zijn op het netwerk. Via probe-based discovery stuurt de hub actief
een verzoek uit en wacht op antwoorden van aanwezige apparaten.

Deze POC toont drie concrete zaken:

**1. Probe-based discovery werkt**
De hub stuurt een UDP probe naar elk apparaat op het netwerk.
Elk aanwezig apparaat antwoordt met zijn naam, type en MAC-adres.
Het resultaat is een lijst van alle gevonden apparaten.

**2. Enkel aanwezige apparaten worden gevonden**
Als een apparaat offline is gehaald verschijnt het niet in de lijst.
Dit toont aan dat de scan effectief kijkt naar de actuele netwerktoestand
en geen gecachte of vaste lijst gebruikt.

**3. De scan start alleen op gebruikersvraag**
Dit sluit aan bij de beslissing in ADR-004 dat discovery enkel actief
gestart wordt wanneer de gebruiker een apparaat wil toevoegen — nooit
automatisch op de achtergrond.

---

## Wat wordt gesimuleerd?

Vijf slimme apparaten van verschillende merken worden gesimuleerd als
Docker containers. Elk apparaat luistert op UDP poort 5000 en antwoordt
op probe requests van de hub.

| Service                | Apparaat              | Type        |
|------------------------|-----------------------|-------------|
| `poc_device_lamp`      | Philips Hue Lamp      | lamp        |
| `poc_device_sensor`    | IKEA Bewegingssensor  | sensor      |
| `poc_device_lock`      | Nuki Slim Slot        | slot        |
| `poc_device_thermostat`| Nest Thermostaat      | thermostaat |
| `poc_device_speaker`   | Sonos Speaker         | speaker     |

De hub is een aparte container die actief blijft maar pas scant
wanneer het script manueel uitgevoerd wordt.

---

## Vereisten

- Docker met Swarm mode actief (`docker swarm init`)
- Internetverbinding om images van Docker Hub te pullen

De images staan publiek op Docker Hub en worden automatisch
opgehaald bij het deployen. Bouwen is niet nodig.

---

## Opstarten

### Stap 1 — Swarm initialiseren (indien nog niet gedaan)

```bash
docker swarm init
```

Heb je al een swarm? Sla deze stap over.

### Stap 2 — Stack deployen

Navigeer naar de map met `poc.yaml` en voer uit:

```bash
docker stack deploy -c poc.yaml poc
```

### Stap 3 — Wachten tot alle services actief zijn

```bash
docker service ls
```

Wacht tot alle services `1/1` tonen onder REPLICAS.
Dit duurt ongeveer 30 seconden terwijl Docker de images pullt.

```
ID             NAME                    REPLICAS   IMAGE
...            poc_hub                 1/1        xandropalomo03/poc-hub:latest
...            poc_device_lamp         1/1        xandropalomo03/poc-device:latest
...            poc_device_sensor       1/1        xandropalomo03/poc-device:latest
...            poc_device_lock         1/1        xandropalomo03/poc-device:latest
...            poc_device_thermostat   1/1        xandropalomo03/poc-device:latest
...            poc_device_speaker      1/1        xandropalomo03/poc-device:latest
```

---

## Scan uitvoeren

Start de scan door het script manueel uit te voeren in de hub container:

```bash
docker exec -it $(docker ps -qf name=poc_hub) python hub_discovery.py
```

---

## Aantonen dat enkel aanwezige apparaten gevonden worden

Dit is het kernpunt van de POC. Voer de volgende stappen uit:

```bash
# Stap 1 — Eerste scan: alle 5 apparaten aanwezig
docker exec -it $(docker ps -qf name=poc_hub) python hub_discovery.py

# Stap 2 — Lamp offline halen
docker service scale poc_device_lamp=0

# Stap 3 — Tweede scan: lamp verschijnt niet meer in de lijst
docker exec -it $(docker ps -qf name=poc_hub) python hub_discovery.py

# Stap 4 — Lamp terug online brengen
docker service scale poc_device_lamp=1

# Stap 5 — Derde scan: lamp is terug zichtbaar
docker exec -it $(docker ps -qf name=poc_hub) python hub_discovery.py
```

---

## Verwacht resultaat

**Scan 1 — alle apparaten aanwezig:**

```
[HUB]   PROBE SCAN GESTART
[HUB]   5 apparaten te scannen

[HUB] → Probe verstuurd naar device_lamp...
[HUB] ✓ Gevonden: Philips Hue Lamp      | lamp        | AA:BB:CC:11:22:01
[HUB] → Probe verstuurd naar device_sensor...
[HUB] ✓ Gevonden: IKEA Bewegingssensor  | sensor      | AA:BB:CC:11:22:02
[HUB] → Probe verstuurd naar device_lock...
[HUB] ✓ Gevonden: Nuki Slim Slot        | slot        | AA:BB:CC:11:22:03
[HUB] → Probe verstuurd naar device_thermostat...
[HUB] ✓ Gevonden: Nest Thermostaat      | thermostaat | AA:BB:CC:11:22:04
[HUB] → Probe verstuurd naar device_speaker...
[HUB] ✓ Gevonden: Sonos Speaker         | speaker     | AA:BB:CC:11:22:05

[HUB]   GEVONDEN APPARATEN (5 totaal)

  Naam                      Type            MAC                    IP
  ───────────────────────────────────────────────────────────────────
  Philips Hue Lamp          lamp            AA:BB:CC:11:22:01      10.0.x.x
  IKEA Bewegingssensor      sensor          AA:BB:CC:11:22:02      10.0.x.x
  Nuki Slim Slot            slot            AA:BB:CC:11:22:03      10.0.x.x
  Nest Thermostaat          thermostaat     AA:BB:CC:11:22:04      10.0.x.x
  Sonos Speaker             speaker         AA:BB:CC:11:22:05      10.0.x.x
```

**Scan 2 — na `docker service scale poc_device_lamp=0`:**

```
[HUB] → Probe verstuurd naar device_lamp...
[HUB] ✗ Geen antwoord van device_lamp — niet aanwezig op netwerk

[HUB]   GEVONDEN APPARATEN (4 totaal)

  Naam                      Type            MAC                    IP
  ───────────────────────────────────────────────────────────────────
  IKEA Bewegingssensor      sensor          AA:BB:CC:11:22:02      10.0.x.x
  Nuki Slim Slot            slot            AA:BB:CC:11:22:03      10.0.x.x
  Nest Thermostaat          thermostaat     AA:BB:CC:11:22:04      10.0.x.x
  Sonos Speaker             speaker         AA:BB:CC:11:22:05      10.0.x.x
```

---

## Stack verwijderen

```bash
docker stack rm poc
```

---

## Verband met ADR-004

| Concept uit ADR-004             | Implementatie in POC                              |
|---------------------------------|---------------------------------------------------|
| Actieve scan op gebruikersvraag | Scan start pas bij `docker exec`                  |
| Probe-based discovery           | Hub stuurt UDP pakket, apparaat antwoordt         |
| Enkel aanwezige apparaten       | Offline apparaten geven geen antwoord             |
| Geen passief luisteren          | Hub doet niets op de achtergrond                  |
| Verschillende merken            | Elk apparaat heeft andere naam, type en MAC       |
