# ADR 002: Account verplicht voor gebruik van de applicatie

## Status
Accepted

## Context
De applicatie wordt gebruikt voor het beheren van slimme woningen met apparaten van verschillende merken. Gebruikers moeten apparaten kunnen bedienen, scenario’s configureren en later mogelijk rechten of zones beheren.

De groep heeft besproken of de applicatie ook zonder account bruikbaar zou moeten zijn. Dat zou het echter moeilijker maken om gebruikers te onderscheiden, instellingen op te slaan en toegang goed te beveiligen.

## Decision
We kiezen ervoor dat een account verplicht is om de applicatie te gebruiken.

Elke gebruiker moet zich aanmelden met een persoonlijk account voordat hij of zij toegang krijgt tot de woning, apparaten en configuraties. Dit account vormt de basis voor authenticatie, persoonlijke instellingen en toegangscontrole.

## Alternatives Considered

### 1. Geen account
De app zou volledig zonder login werken.

Voordelen:
- Lage instapdrempel.

Nadelen:
- Gebruikers zijn moeilijk te onderscheiden.
- Instellingen kunnen niet per persoon worden opgeslagen.
- Beveiliging wordt zwakker, omdat men vooral op netwerkbeveiliging moet vertrouwen.

### 2. Meerdere accounts vanaf het begin
Elke gebruiker zou meteen een eigen account krijgen met mogelijke rollen en rechten.

Voordelen:
- Veel flexibiliteit.
- Goede basis voor uitgebreide toegangscontrole.

Nadelen:
- Hogere complexiteit.
- Meer werk voor implementatie, testen en onderhoud.
- Waarschijnlijk te zwaar voor een tweedejaars eindproject.

### 3. Eén verplicht account
Elke gebruiker heeft één persoonlijk account nodig om de app te gebruiken.

Voordelen:
- Goede balans tussen eenvoud en functionaliteit.
- Ondersteunt security en personalisatie.
- Makkelijker uitbreidbaar naar meerdere gebruikers later.

## Consequences

### Positive consequences
- Gebruikersinstellingen kunnen per account worden opgeslagen.
- Toegangscontrole wordt duidelijker en veiliger.
- De app kan later makkelijker worden uitgebreid naar meerdere gebruikers of rollen.
- Acties kunnen beter gelogd of gekoppeld worden aan een specifieke gebruiker.

### Negative consequences
- Extra werk voor login, accountbeheer en validatie.
- Gebruikers moeten zich registreren en aanmelden.
- Er moet rekening gehouden worden met privacy en beveiliging van gebruikersgegevens.

## Rationale
Voor een smart-home applicatie is een account belangrijk omdat de app niet alleen apparaten moet bedienen, maar ook moet weten wie welke actie uitvoert.

Dat is nuttig voor beveiliging, personalisatie en toekomstige uitbreiding naar meerdere gebruikers of rechten per zone. Een verplicht account geeft de beste combinatie van controle, uitbreidbaarheid en duidelijkheid voor deze projectscope.

## Impact on Quality Attributes
- **Security**: verbeterd door authenticatie en toegangscontrole.
- **Usability**: iets meer instapwerk, maar een gepersonaliseerde ervaring na login.
- **Configurability**: instellingen kunnen per gebruiker worden bewaard.
- **Maintainability**: de structuur is overzichtelijker dan een volledig accountloos systeem.

## Future Considerations
Als de scope later uitbreidt, kan deze beslissing worden verfijnd met extra ADR’s voor:
- gastaccounts,
- meerdere gebruikers per woning,
- rollen en rechten per zone,
- een hybride loginmodel.
