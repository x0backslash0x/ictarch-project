POC — Automatisaties opgebouwd bovenop scenario's

## Beschrijving

Deze Proof of Concept (POC) demonstreert hoe een smart-home applicatie scenario’s zowel manueel als automatisch kan uitvoeren.

Het systeem bevat een scenario “Filmavond” dat bestaat uit meerdere acties zoals:
- verlichting dimmen
- TV opstarten
- thermostaat aanpassen
- deur vergrendelen

Het scenario kan:

- manueel gestart worden via een knop
- automatisch uitgevoerd worden via een timer

## Functionaliteiten

- Manuele activatie van scenario
- Automatische activatie via timer (elke 30 seconden)
- Toggle switch om automatisatie aan/uit te zetten
- Logging van uitgevoerde acties
- Webinterface om alles te bedienen

## ADR (Automatisaties opgebouwd bovenop scenario's)

- Scenario's bevatten een set acties
- Automatisaties activeren scenario’s
- Scheiding tussen:
  - scenario (wat gebeurt er)
  - automatisatie (wanneer gebeurt het)

## Relevantie voor de ADR

- Usability: één druk op de knop voert het scenario direct uit.
- Configurability: de toggle simuleert het instellen van wanneer het scenario automatisch loopt.
- Maintainability: scenario-definitie en automatisatie-logica zijn volledig gescheiden; `runScenario()` kent geen timers, de `setInterval` kent geen acties.

## Architectuur

```
┌────────────────────────────────────────────────────┐
│                  Express app                       │
│                                                    │
│  SCENARIO = { name, actions[] }                    │
│  └─ definitie, geen kennis van timers              │
│                                                    │
│  POST /trigger ──────────────────────────┐         │
│                                          ▼         │
│  setInterval (elke 30 s) ────────── runScenario()  │
│  (enkel als automationEnabled = true)              │
│                                                    │
│  POST /automation/toggle                           │
│  └─ zet automationEnabled aan/uit                  │
└────────────────────────────────────────────────────┘
```

## Bestandsstructuur

```
.
├── app/
│   ├── app.js           ← Express server + scenario-logica + automatisatie
│   ├── Dockerfile
│   ├── package.json
│   └── public/
│       └── index.html   ← UI met manuele knop en automatisatie-toggle
├── poc.yaml             ← Docker stack configuratie
└── README.md
```

## Starten

Stap 1 — image bouwen (éénmalig, vanuit de `app/` map)

```bash
cd app
docker build -t scenario-poc:latest .
cd ..
```

Stap 2 — Swarm initialiseren (indien nog niet gedaan)

```bash
docker swarm init --advertise-addr <jouw-ip>
```

Stap 3 — stack deployen

```bash
docker stack deploy --compose-file poc.yaml poc
```

Stap 4 — controleren of de service draait

```bash
docker service ls
```

Je zou `1/1` moeten zien onder REPLICAS.

Stap 5 — UI openen

http://localhost:5000

## Stoppen

```bash
docker stack rm poc
```
