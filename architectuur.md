# Gepersonaliseerde opdracht
Je klant wil een applicatie voor het beheren van slimme woningen, waarbij apparaten van verschillende merken geïntegreerd worden. Automatisaties en scenario’s moeten configureerbaar zijn. Vergelijkbare voorbeelden zijn Google Home en Home Assistant.

> Veronderstel in de eerste plaats dat de afgestudeerde versie van je team deze opdracht productieklaar moet maken op een half jaar tijd. In je ADR's kan je vermelden welke beslissingen anders zouden zijn als je team en je budget groter / kleiner waren.
> Voor de vraag "wat de klant waarschijnlijk belangrijk vindt" kijk je naar de gegeven voorbeelden.

# Requirements
## Expliciet (rechstreeks uit opgave):
*	Apparaten verschillende merken integreren in app
*	App voor beheren van slimme apparaten in woning
*	Automatisaties moeten configureerbaar zijn
* Scenarios moeten configureerbaar zijn

## Impliciet (tussen de lijntjes):
*	Bediening met touch 
*	Aansturing via spraak (uitbereiding)
*	OS-ondersteuning – Android
*	Cross-platform (uitbereiding)

# Karakteristieken
| Karakteristiek | Expliciet? | Top 3? | Toelichtig |
| -------------- | ---------- | ------ | ---------- |
| Useability     | ja         | ja     | Hoe gebruiksvriendelijk is de app. Hoe draagt de app bij aan de gebruikerservaring. |
| Interoperability | ja       | ja     | Hoe gemakkelijk is het om verschillende merken/apparaten te integreren. |
| Configurability  | ja       | ja     | In welke mate het mogelijk is om zaken te configureren in de app.  |
| Security | nee | nee | In welke mate apparaten afgeschermd zijn en de app cyberaanvallen kan weerstaan. |
| Maintainability | nee | nee | Hoe gemakkelijk de app op termijn te onderhouden valt. |
| Reliability | nee | nee | Hoe betrouwbaar de werking van de app is. |
| Performance | nee | nee | In welke mate de prestaties van de app worden beïenvloed door verschillende factoren. |

# Logische componenten
De workflow methode lijkt het meeste aangewezen om logische componenten te kunnen achterhalen. In de werking van de app zijn volgende elementen alvast te onderscheiden

| component | taken |
| --------- | ----- |
| zone beheer | zones aanmaken / verwijderen |
| gebruikers beheer | gebruiker aanmaken / aanpassen / verwijderen |
| authenticator | gebruiker aanmelden / afmelden |
| ontdekker | apparaten vinden op netwerk |
| aparaat beheer | apparaten toevoegen / verwijderen / aansturen |
| protocol adapter | apparaat commando's vertalen |
| scenario beheer | scenario toevoegen / aanpassen / verwijderen / uitvoeren |
| notificatie beheer | berichten tonen ivm app werking |
| status beheer | realtime status van apparaten tonen |

