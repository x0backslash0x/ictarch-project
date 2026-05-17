# TITEL
001 architecturale stijl


# STATUS
Accepted


# CONTEXT
Deze adr gaat over het kiezen van een architecturale stijl. Volgende vergelijkingen zijn gemaakt:

**Layered**
- Adapters zitten ingebouwd. Vereist update van de app voor nieuwe integraties [interoperability-/maintainability-]
- Aanpassingen businesslogica raken meerdere lagen [maintainability-]

**Modulaire Monoliet**
- Adapters zitten ingebouwd. Vereist update van de app voor nieuwe integraties [interoperability-/maintainability-]
- Latente koppeling die zich voordoet als modulariteit doet op termijn de grenzen vervagen [maintainability-]

**Microservices**
- Moeilijk om consistente UX te garanderen [useability-] (wat wordt hiermee bedoeld?)
- Veel overhead door onderlingen communicatie services [performance-]

# BESLISSING
Er wordt gekozen voor een microkernel architectuur.


# GEVOLGEN
## Voordelig
+ Adapters kunnen als plugins bestaan, los van de kern [interoperability+/maintainability+]
+ Minder code door minimale kern [security+/maintainability+/performance+/reliability+]


# GOVERNANCE
**Eigenaar:** Domeinarchitect / Functioneel architect

**Review moment:**
- bij uitbreidingen of structurele aanpassingen van de kern


# NOTITIES
nvt