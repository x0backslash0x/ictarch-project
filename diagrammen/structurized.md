workspace "Smart Home Systeem" "Architectuur voor een slim woning beheersysteem" {

    model {

        !identifiers hierarchical


        # Personen


        bewoner = person "Bewoner" \
            "Beheert en automatiseert slimme apparaten via de webinterface of mobiele app. \
             Aanvankelijk één gebruiker, later uitbreidbaar naar meerdere."


        # Het systeem — slimme apparaten zitten binnen de systeemgrens


        smartHomeSystem = softwareSystem "Smart Home Systeem" \
            "Beheert en automatiseert slimme apparaten volledig lokaal via een hub. \
             Geen externe afhankelijkheden." {

            # ── Webinterface ─────────────────────────────

            webInterface = container "Webinterface" \
                "Lichtgewichte interface geserveerd door de hub. \
                 Bereikbaar via browser op elk toestel. \
                 Bevat geen eigen logica; alle verwerking gebeurt op de hub." \
                "HTML / CSS / JS" "Interface"

            # ── Mobiele App ──────────────────────────────

            mobieleApp = container "Mobiele App" \
                "Mobiele interface voor smartphones. \
                 Doet dezelfde API-aanroepen als de webinterface maar presenteert \
                 de gegevens in een op mobiel afgestemde weergave." \
                "iOS / Android" "MobieleApp"

            # ── Hub ─────────────────────────────────────

            hub = container "Smart Home Hub" \
                "Microkernel kern met protocol adapters als plugins. \
                 Discovery via probe-scans en announcements. \
                 Lokale opslag via SQLite. Serveert de webinterface. (ADR-001, ADR-004, ADR-006, ADR-007)" \
                "Linux / SQLite"

            # ── Slimme Apparaten ─────────────────────────

            slimmeApparaten = container "Slimme Apparaten" \
                "Fysieke apparaten op het thuisnetwerk: \
                 lampen, schakelaars, sensoren, sloten. \
                 Worden ontdekt via probe-scans en announcements \
                 en aangestuurd via protocol adapters op de hub." \
                "Zigbee / WiFi / Matter" "Apparaat"
        }


        # Relaties — Systeemcontext


        bewoner -> smartHomeSystem \
            "Beheert en automatiseert slimme apparaten via"


        # Relaties — Containers


        bewoner -> smartHomeSystem.webInterface \
            "Bedient apparaten en configureert scenario's via browser" \
            "HTTP / WebSocket"

        bewoner -> smartHomeSystem.mobieleApp \
            "Bedient apparaten en configureert scenario's via mobiele app" \
            "HTTP / WebSocket"

        smartHomeSystem.webInterface -> smartHomeSystem.hub \
            "Stuurt commando's en ontvangt statusupdates" \
            "HTTP / WebSocket"

        smartHomeSystem.mobieleApp -> smartHomeSystem.hub \
            "Stuurt commando's en ontvangt statusupdates" \
            "HTTP / WebSocket"

        smartHomeSystem.hub -> smartHomeSystem.slimmeApparaten \
            "Ontdekt apparaten via probe-scans en announcements; \
             stuurt commando's en leest sensordata via protocol adapters" \
            "Zigbee / MQTT / Matter"


        # Deployment


        deploymentEnvironment "Productie" {

            deploymentNode "Smartphone van de bewoner" \
                "Persoonlijk mobiel toestel van de bewoner. \
                 De app wordt hier apart geïnstalleerd." \
                "iOS / Android" {
                    containerInstance smartHomeSystem.mobieleApp
            }

            deploymentNode "Thuisnetwerk" \
                "Lokaal netwerk in de woning. Alle functionaliteit draait hier. \
                 Geen internetverbinding vereist. (ADR-001)" \
                "LAN" {

                deploymentNode "Smart Home Hub" \
                    "Draait continu. Hub, SQLite en webserver op hetzelfde apparaat." \
                    "Linux / SQLite" {
                        containerInstance smartHomeSystem.hub
                        containerInstance smartHomeSystem.webInterface
                }

                deploymentNode "Slimme Apparaten" \
                    "Fysieke apparaten op het thuisnetwerk." \
                    "Zigbee / WiFi / Matter" {
                        containerInstance smartHomeSystem.slimmeApparaten
                }
            }
        }
    }

    views {

        systemContext smartHomeSystem "SystemContext" \
            "Het systeem als één geheel — slimme apparaten zijn onderdeel van het systeem" {
            include *
            autolayout lr
        }

        container smartHomeSystem "Containers" \
            "Webinterface, mobiele app, hub met ingebouwde SQLite en slimme apparaten" {
            include *
            autolayout lr
        }

        deployment smartHomeSystem "Productie" "Deployment" \
            "Webinterface draait mee op de hub. Mobiele app staat apart op de smartphone." {
            include *
            autolayout lr
        }

        styles {
            element "Person" {
                shape Person
                background #08427b
                color #ffffff
            }
            element "Software System" {
                background #1168bd
                color #ffffff
            }
            element "Container" {
                background #438dd5
                color #ffffff
            }
            element "Interface" {
                background #2ecc71
                color #ffffff
                shape WebBrowser
            }
            element "MobieleApp" {
                background #27ae60
                color #ffffff
                shape MobileDeviceLandscape
            }
            element "Apparaat" {
                background #7f8c8d
                color #ffffff
            }
        }
    }
}