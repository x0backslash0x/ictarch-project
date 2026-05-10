# ADR-004: Strategie voor het ontdekken van apparaten op het netwerk

## Status

Accepted

---

## Context

Om apparaten van verschillende merken te kunnen beheren, moet de applicatie eerst weten welke
apparaten beschikbaar zijn op het thuisnetwerk. Dit is een fundamentele stap — zonder een
goede discovery strategie kan de applicatie haar kernbelofte van **interoperability** niet
waarmaken.

Er zijn twee gangbare manieren waarop apparaten ontdekt kunnen worden:

**Probe-based discovery**
De applicatie neemt zelf het initiatief en stuurt een vraag uit op het netwerk. Apparaten die
deze vraag ontvangen, antwoorden met hun aanwezigheid. De applicatie heeft volledige controle
over wanneer dit gebeurt.

**Announcement-based discovery**
De applicatie opent een tijdvenster en wacht. Apparaten die zichzelf willen kenbaar maken,
sturen uit zichzelf een bericht. De applicatie vangt deze berichten op.

Het probleem is dat niet elk merk of protocol dezelfde methode ondersteunt. Sommige apparaten
reageren enkel op een actieve vraag, andere kondigen zichzelf enkel zelf aan. Een keuze voor
slechts één methode sluit dus automatisch een deel van de markt uit — wat rechtstreeks ingaat
tegen onze karakteristiek **interoperability**.

---

## Decision

**We kiezen ervoor om beide methodes te ondersteunen, uitgevoerd na elkaar op expliciete
vraag van de gebruiker.**

Discovery start pas wanneer de gebruiker actief aangeeft een apparaat te willen toevoegen.
Er is geen achtergrondproces dat continu meeluistert. Het systeem voert eerst een probe uit,
opent daarna een venster voor announcements, en toont uiteindelijk één gecombineerde lijst
van gevonden apparaten. Apparaten die via beide methodes gevonden worden, verschijnen slechts
één keer in die lijst.

Welke technische methode gebruikt werd om een apparaat te vinden is een intern detail dat niet
zichtbaar is voor de gebruiker.

---

## Consequences

### Positief

- **(+) Interoperability:** Geen enkel apparaat wordt uitgesloten op basis van welke discovery
  methode het ondersteunt. Beide gevallen worden gedekt.
- **(+) Security:** Omdat de applicatie enkel actief scant op vraag van de gebruiker, is ze
  buiten dat moment niet vatbaar voor apparaten of aanvallers die berichten uitsturen op het
  netwerk. Een continu luisterende applicatie zou een groter aanvalsoppervlak hebben.
- **(+) Usability:** De gebruiker ziet één duidelijke lijst van beschikbare apparaten, zonder
  technische details over hoe ze gevonden werden.
- **(+) Performance:** Er is geen continu achtergrondverkeer op het netwerk. Netwerkbelasting
  beperkt zich tot de momenten waarop de gebruiker actief apparaten zoekt.

### Negatief

- **(-) Maintainability:** Twee discovery methodes ondersteunen is complexer dan één. Beide
  moeten correct geïmplementeerd en onderhouden worden.
- **(-) Gebruikerservaring:** De gebruiker wacht op twee opeenvolgende scanvensters voordat
  het volledige resultaat zichtbaar is.

---

## Governance

- Alle discovery logica wordt ondergebracht in de **Apparaat-discovery** component zodat
  toekomstige wijzigingen aan één methode geen impact hebben op de rest van het systeem.
- De duur van elk scanvenster wordt instelbaar gemaakt zodat dit later bijgesteld kan worden
  zonder aanpassingen aan de code.

---

## Notes

- **Als team groter / budget groter:** beide methodes zouden gelijktijdig kunnen draaien in
  plaats van na elkaar, wat de wachttijd voor de gebruiker halveert.
- **Als team kleiner / budget kleiner:** enkel probe-based discovery zou volstaan als
  vereenvoudigde aanpak. Dit dekt de meeste moderne apparaten en is eenvoudiger te beveiligen.
- Deze ADR beslist over de **strategie** van discovery. Er kunnen aparte ADR's gemaakt worden
  over welke specifieke protocollen gebruikt worden voor probe en announcement — denk aan keuzes
  zoals mDNS, SSDP, Zigbee permit join of Matter commissioner discovery. Omwille van de scope
  van dit project worden die beslissingen hier niet verder uitgewerkt, maar het is een bewuste
  keuze om dit op te merken.

### Referenties

- [mDNS — RFC 6762](https://www.rfc-editor.org/rfc/rfc6762)
- [Matter — Wat is Matter? (Homey)](https://homey.app/nl-be/wiki/wat-is-matter/)
- [Zigbee — Connectivity Standards Alliance](https://csa-iot.org/all-solutions/zigbee/)
- [SSDP/UPnP — Tutorial en gebruikersgids (Macchina)](https://docs.macchina.io/edge/00200-UPnPSSDPTutorialAndUserGuide.html)
- [SSDP — Protocol uitleg (StormWall)](https://stormwall.network/resources/terms/protocols/ssdp)
- [Bonjour — Apple developer documentatie](https://developer.apple.com/bonjour/)
