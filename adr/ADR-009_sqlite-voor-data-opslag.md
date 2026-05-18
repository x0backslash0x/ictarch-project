# TITEL
009 SQLite voor data opslag


# STATUS
Accepted


# CONTEXT 
De keuze voor een microkernel architectuur vereist dat alle basisfunctionaliteit in 1 kern vervat zit. De nood aan data opslag maakt onderdeel uit van de basisfunctionalteit. Het gebruik van een aparte database dienst of server zou de isolatie tot 1 kern teniet doen. SQLite is kleinschalig genoeg om in te bouwen in de kern van de applicatie.


# BESLISSING
SQlite zal gebruikt worden voor opslag voor data.


# GEVOLGEN
## Voordelig
+ heel weinig overhead. Komt performance ten goede.
+ geen externe database node nodig.


# GOVERNANCE
nvt


# NOTITIES
De redenering in context gaat niet meer op. De microkernel stijl laat toe (fysiek) externe data opslag te hanteren.