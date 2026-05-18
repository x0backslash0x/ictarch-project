# TITEL
006 Automatisaties opgebouwd bovenop scenario's


# STATUS
Accepted


# CONTEXT
De smart-home applicatie moet zowel eenvoudige manuele acties als automatische woninglogica ondersteunen. In bestaande systemen worden deze concepten soms samengevoegd, wat leidt tot meer complexiteit en een minder begrijpelijke gebruikerservaring.

Er is een behoefte aan:
- eenvoudige manuele bediening (bv. "Filmavond")
- automatische uitvoering op vaste momenten of events (bv. elke vrijdag om 20u)


# BESLISSING
Er wordt gekozen voor een model waarbij:
- Scenario's een verzameling van acties vertegenwoordigen die manueel kunnen worden uitgevoerd
- Automatisaties specifiek scenario's automatisch activeren op basis van tijds- of event-gebaseerde triggers


# GEVOLGEN
## Voordelig
+ **[Usability]** Gebruikers kunnen een scenario (bv. Filmavond) zowel manueel activeren als automatisch laten uitvoeren (bv. elke vrijdagavond).
+ **[Configurability]** Gebruikers kunnen zelf instellen wanneer en hoe scenario's verlopen, inclusief tijdstippen, herhalingen en uitzonderingen.
+ **[Maintainability]** Scenario's en tijdsgebonden logica zijn modulair opgebouwd, waardoor functionaliteit herbruikbaar is en aanpassingen eenvoudig kunnen gebeuren zonder impact op andere onderdelen.
+ Scenario-definitie en automatische activatie zijn logisch gescheiden. Dit zorgt voor een duidelijke scheiding van verantwoordelijkheden.

## Nadelig
- **[Reliability]** Automatisaties zijn gekoppeld aan scenario's; indien een scenario foutief geconfigureerd is of faalt, kan dit de automatische uitvoering beïnvloeden.
- Er is bijkomende logica nodig om de relatie tussen scenario's en automatisaties te onderhouden.


# GOVERNANCE
**Eigenaar:** Domeinarchitect / Functioneel architect

**Review moment:**
- bij uitbreiding van automatisatie-types
- bij introductie van complexere afhankelijkheden (bv. geneste scenario's)


# NOTITIES
Deze beslissing sluit aan bij de gekozen karakteristieken usability, configurability, maintainability en reliability, en ondersteunt een event-driven architectuur zonder de gebruikerservaring onnodig complex te maken.