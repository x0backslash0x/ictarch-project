# inleiding
Deze POC is gebaseerd op ADR-004 en gaat over announcement-based device discovery.

Het doel van deze POC is om specifiek volgende vraagstelling te beantwoorden:
> Hoe zou de applicatie gedurende een instelbare tijd announcements van apparaten opvangen, verwerken en tonen in een lijst

## flow
1. gebruiker start zoeken van apparaten
2. applicatie opent een announcement venster
3. listener vangt announcements op
4. parser zet data uit announcements om naar apparaat info.
5. resultaten worden getoond in een lijst.

## acceptance criteria
- discovery start enkel op vraag, niet automatisch
- listener is actief enkel gedurende het announcement venster
- duur announcement venster is instelbaar
- duur announcement venster heeft een default waarde
- meerdere announcements van hetzelfde toestel worden genegeerd. Enkel de eerste telt
- de lijst met resultaten wordt automatisch bijgewerkt wanneer er een nieuw apparaat ontdekt wordt gedurende het announcent venster

Er zijn verschillende services nodig binnen deze POC
- 1 service die periodiek announcements uitzend
- 1 service die luisterd naar de announcements en ze verwerkt
