# 003 Automatisaties opgebouwd bovenop scenario's

## Status
Accepted

## Context

De smart-home applicatie moet zowel eenvoudige manuele acties als automatische woninglogica ondersteunen. In bestaande systemen worden deze concepten soms samengevoegd, wat leidt tot meer complexiteit en een minder begrijpelijke gebruikerservaring.

Er is een behoefte aan:

- eenvoudige manuele bediening (bv. "Filmavond")
- automatische uitvoering op vaste momenten of events (bv. elke vrijdag om 20u)

## Decision

Er wordt gekozen voor een model waarbij:

- Scenario's een verzameling van acties vertegenwoordigen die manueel kunnen worden uitgevoerd
- Automatisaties specifiek scenario's automatisch activeren op basis van tijds- of event-gebaseerde triggers

## Consequences

### Positief

- **Usability:**
  Gebruikers kunnen een scenario (bv. Filmavond) zowel manueel activeren als automatisch laten uitvoeren (bv. elke vrijdagavond).
- **Configurability:**
  Gebruikers kunnen zelf instellen wanneer en hoe scenario's verlopen, inclusief tijdstippen, herhalingen en uitzonderingen.
- **Maintainability:**
  Scenario's en tijdsgebonden logica zijn modulair opgebouwd, waardoor functionaliteit herbruikbaar is en aanpassingen eenvoudig kunnen gebeuren zonder impact op andere onderdelen.
- **Duidelijke scheiding van verantwoordelijkheden:**
  Scenario-definitie en automatische activatie zijn logisch gescheiden.

### Negatief / trade-offs

- **Reliability-afhankelijkheid:**
  Automatisaties zijn gekoppeld aan scenario's; indien een scenario foutief geconfigureerd is of faalt, kan dit de automatische uitvoering beïnvloeden.
- **Extra beheerlaag:**
  Er is bijkomende logica nodig om de relatie tussen scenario's en automatisaties te onderhouden.

## Governance

- **Eigenaar:** Domeinarchitect / Functioneel architect
- **Reviewmoment:**
  - bij uitbreiding van automatisatie-types
  - bij introductie van complexere afhankelijkheden (bv. geneste scenario's)

## Notes

Deze beslissing sluit aan bij de gekozen karakteristieken usability, configurability, maintainability en reliability, en ondersteunt een event-driven architectuur zonder de gebruikerservaring onnodig complex te maken.