# ADR-004: Actieve Device Discovery via Probe en Announcement

## Status

Draft

---

## Context

De applicatie moet apparaten van verschillende merken en protocollen kunnen ontdekken op het
lokale netwerk. Dit is rechtstreeks gekoppeld aan onze belangrijkste karakteristiek
**interoperability** — zonder een robuust discovery mechanisme kunnen apparaten van
verschillende merken niet geïntegreerd worden.

Er zijn twee gangbare methodes om apparaten te ontdekken op een netwerk:

**Probe-based discovery**
Het systeem stuurt actief een broadcast uit en wacht op reacties van beschikbare apparaten.
Het systeem heeft volledige controle over wanneer dit gebeurt. Voorbeelden:

- **ARP scanning:** stuurt een broadcast op het netwerk en verzamelt MAC-adressen van
  aanwezige apparaten
- **Zigbee permit join broadcast:** opent het Zigbee netwerk tijdelijk zodat nieuwe apparaten
  kunnen joinen
- **Matter commissioner discovery:** stuurt een DNS-SD query waarop Matter-compatibele
  apparaten antwoorden

**Announcement-based discovery**
Het systeem opent een tijdvenster waarin het wacht op apparaten die zichzelf actief aankondigen
op het netwerk. Voorbeelden:

- **mDNS/Bonjour:** apparaten kondigen zichzelf aan op het lokale netwerk via multicast DNS
  zonder centrale DNS-server
- **SSDP:** apparaten sturen periodiek een multicast bericht met hun aanwezigheid en services,
  onderdeel van het UPnP protocol
- **Zigbee device announcements:** een Zigbee apparaat stuurt automatisch een bericht op het
  Zigbee netwerk wanneer het opstart of terug online komt

Niet alle apparaten ondersteunen beide methodes. Sommige apparaten reageren enkel op een probe,
andere kondigen zichzelf enkel aan. Aangezien **interoperability** een van de drie meest
kritische karakteristieken is, mag de keuze van discovery methode geen apparaten uitsluiten op
basis van hun ondersteunde methode.

De keuze heeft gevolgen voor:

- Welke apparaten en merken ondersteund worden
- De hoeveelheid en timing van netwerkverkeer
- De beveiliging van het netwerk
- De implementatiecomplexiteit

### Relevante karakteristieken

| Karakteristiek | Prioriteit | Relevantie |
|---|---|---|
| Interoperability | Top 3 | Verschillende merken en protocollen moeten ondersteund worden |
| Reliability | — | Discovery moet werken ongeacht welke methode een apparaat ondersteunt |
| Security | — | Discovery gebeurt alleen op expliciete gebruikersactie |
| Usability | Top 3 | De gebruiker ziet één duidelijke lijst zonder technische details |

---

## Decision

**We kiezen voor volledig actieve, sequentiële discovery waarbij zowel probe als announcement
sequentieel worden uitgevoerd op expliciete gebruikersactie.**

Discovery wordt enkel gestart wanneer de gebruiker actief een apparaat wil toevoegen. Er is
geen passief achtergrondproces dat continu meeluistert.

Het proces verloopt als volgt:

1. Gebruiker start discovery via de interface
2. Systeem voert een **probe scan** uit — stuurt een broadcast en verzamelt reacties gedurende
   een vast tijdvenster
3. Systeem opent een **announcement venster** — wacht gedurende een vast tijdvenster op
   apparaten die zichzelf aankondigen
4. Beide resultaten worden samengevoegd en **gededupliceerd op basis van het MAC-adres** van
   elk apparaat
5. De gebruiker ziet één gecombineerde lijst van gevonden apparaten

De gebruikte discovery methode is een intern implementatiedetail en wordt niet getoond in de
interface. De gebruiker ziet enkel het gevonden apparaat en zijn eigenschappen.

---

## Consequences

### Positief

- **(+) Interoperability:** Apparaten die enkel probe of enkel announcement ondersteunen worden
  beiden gevonden. Geen enkel apparaat wordt uitgesloten op basis van zijn discovery methode.
- **(+) Security:** Doordat discovery enkel actief gestart wordt op gebruikersactie, verwerkt
  de hub buiten dat venster geen discovery packets. Dit minimaliseert het aanvalsoppervlak —
  een aanvaller die crafted announcement packets stuurt naar de hub wordt genegeerd zolang er
  geen actieve scan loopt. Bij passief luisteren zou de hub continu packets verwerken, wat bij
  een vulnerability in de parser misbruikt kan worden.
- **(+) Usability:** De gebruiker ziet één overzichtelijke lijst zonder technische details over
  hoe een apparaat gevonden werd.
- **(+) Performance:** Geen continu achtergrondverkeer — netwerkbelasting is beperkt tot het
  moment van actieve discovery.
- **(+) Deduplicatie:** Apparaten die beide methodes ondersteunen verschijnen slechts één keer
  in de lijst dankzij MAC-adres matching.

### Negatief

- **(-) Maintainability:** Beide methodes moeten geïmplementeerd en onderhouden worden, wat de
  complexiteit van de discovery component verhoogt.
- **(-) Gebruikerservaring:** De gebruiker moet wachten op twee opeenvolgende scanvensters
  voordat de volledige lijst beschikbaar is.
- **(-) Tijdsbestek:** Twee discovery methodes implementeren kost meer tijd dan één. Dit is een
  bewuste afweging ten voordele van interoperability.

---

## Governance

- De volledige discovery logica wordt gecentraliseerd in de **Apparaat-discovery** component.
  Wijzigingen aan één methode hebben geen impact op andere componenten.
- Deduplicatie gebeurt intern op basis van MAC-adres voordat resultaten aan de gebruiker getoond
  worden.
- De duur van elk scanvenster wordt configureerbaar gemaakt zodat dit later afgestemd kan worden
  op de praktijk zonder code te wijzigen.
- Bij uitbreiding naar nieuwe protocollen wordt per protocol gedocumenteerd welke discovery
  methode ondersteund wordt.

---

## Notes

- **Als team groter / budget groter:** beide methodes zouden parallel kunnen draaien in plaats
  van sequentieel, wat de totale discovery tijd halveert.
- **Als team kleiner / budget kleiner:** enkel probe-based discovery zou geïmplementeerd worden
  als fallback. Dit dekt de meeste moderne apparaten en is eenvoudiger te implementeren en te
  beveiligen.
- **Mogelijke POC:** een proof of concept die aantoont hoe het systeem sequentieel een probe
  broadcast verstuurt en daarna een announcement venster opent, de resultaten samenvoegt en
  duplicaten filtert op MAC-adres.

### Referenties

- [mDNS — RFC 6762](https://www.rfc-editor.org/rfc/rfc6762)
- [Matter — Wat is Matter? (Homey)](https://homey.app/nl-be/wiki/wat-is-matter/)
- [Zigbee — Connectivity Standards Alliance](https://csa-iot.org/all-solutions/zigbee/)
- [SSDP/UPnP — Tutorial en gebruikersgids (Macchina)](https://docs.macchina.io/edge/00200-UPnPSSDPTutorialAndUserGuide.html)
- [SSDP — Protocol uitleg (StormWall)](https://stormwall.network/resources/terms/protocols/ssdp)
- [Bonjour — Apple developer documentatie](https://developer.apple.com/bonjour/)
