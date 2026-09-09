# GOVERNANCE.md

**Versie:** 0.1

# 1. Waarom governance nodig is

De tool werkt met wetgeving, jaargebonden examenregels, rechtspraak, handreikingen en AI-modellen.

Daarmee verandert niet alleen de code. Ook de bronset, interpretatie, prompts en modellen veranderen.

Governance bepaalt:

- wie eigenaar is;
- wie bronnen valideert;
- hoe updates actief worden;
- welke wijzigingen getest moeten worden;
- wanneer menselijke beoordeling verplicht is;
- hoe later kan worden gereconstrueerd wat de tool heeft gedaan.

# 2. Rollen

## Functioneel eigenaar

Verantwoordelijk voor:

- scope;
- prioriteiten;
- gebruikersrollen;
- functionele acceptatie.

## Inhoudelijk bronbeheerder

Verantwoordelijk voor:

- bronregistry;
- actualiteitscheck;
- CE-jaargangen;
- metadata;
- bronstatus;
- voorbereiding nieuwe bronversies.

## Juridisch/domeinvalidator

Verantwoordelijk voor:

- rules die tot `MOET` kunnen leiden;
- nieuwe juridische interpretaties;
- regimewissels;
- moeilijke jurisprudentie;
- conflicterende bronnen.

## Technisch eigenaar

Verantwoordelijk voor:

- hosting;
- security;
- software releases;
- modelconfiguratie;
- logging;
- backups;
- incidenten.

## Gebruiker/reviewer

Beoordeelt findings en blijft verantwoordelijk voor het uiteindelijke inhoudelijke besluit.

# 3. Bronlevenscyclus

```text
discovered
pending_review
validated
active
superseded
archived
rejected
```

Een webcrawl maakt een bron nooit automatisch `active`.

# 4. Jaarlijkse cyclus

Minimaal rond de voorbereiding van een nieuw examenreglement:

1. WVO/Uitvoeringsbesluit controleren;
2. nieuwe VO-raad-set controleren;
3. Inspectiekader controleren;
4. CvTE/Examenblad controleren voor volgend examenjaar;
5. protocollen vervangen zodra juiste jaargang beschikbaar is;
6. jurisprudentieset actualiseren;
7. rules herbevestigen;
8. golden set draaien;
9. release vastleggen.

# 5. Tussentijdse bronwijziging

Bij een relevante wijziging:

- nieuwe bronversie registreren;
- affected rules bepalen;
- affected golden tests bepalen;
- validator review;
- release note;
- pas daarna activeren.

# 6. Modelwijziging

Een modelwijziging is een analyserverandering.

Verplicht:

- model-ID vastleggen;
- golden set draaien;
- differences review;
- kritieke regressies blokkeren;
- release registreren.

# 7. Promptwijziging

Prompts staan onder versiebeheer.

Een wijziging die invloed kan hebben op:

- severity;
- legal tagging;
- evidencegebruik;
- human-review-routing;

vereist regressietests.

# 8. Rulewijziging

Een `RuleRecord` dat `must` kan produceren:

- heeft reviewer;
- heeft validatiedatum;
- heeft bron;
- heeft geldigheid;
- is testgedekt.

# 9. Jurisprudentie-update

Nieuwe zaak:

1. vinden;
2. metadata invullen;
3. `holding` vastleggen;
4. `decisive_reasoning` vastleggen;
5. `may_infer` invullen;
6. `must_not_infer` invullen;
7. juridisch regime controleren;
8. relevantietags;
9. reviewstatus;
10. activeren.

# 10. Menselijke beslisgrens

Altijd human review bij:

- nieuwe rechtsvraag;
- primaire bronconflict;
- overgangsrecht;
- mogelijk effect op reeds afgelegde examens;
- mogelijke rechtsongelijkheid;
- onduidelijke bevoegdheidsroute;
- onduidelijke civiele/bestuursrechtelijke route;
- zwaar juridisch oordeel zonder gevalideerde rule.

# 11. Audit

Per run:

- document hash;
- gebruiker;
- tijd;
- schooljaar;
- examenjaar;
- bron-snapshot;
- rule set;
- model;
- prompts;
- parsingstatus;
- fase-uitkomst;
- findings;
- human reviews;
- exports.

# 12. Privacy

De examenreglementmodule heeft geen leerlingdata nodig.

Beleid:

- waarschuw voor persoonsgegevens;
- data minimaliseren;
- bewaartermijn instelbaar;
- geen trainingsgebruik zonder aparte grondslag/toestemming;
- rolgebaseerde toegang;
- exportlogging.

# 13. Security

Minimaal:

- secrets server-side;
- encrypted transport;
- toegangsbeheer;
- auditlogging;
- inputvalidatie;
- bestandstypecontrole;
- prompt-injectiongrens;
- rate limits waar passend;
- dependency updates.

# 14. Release gates

Geen productie wanneer:

- `must` zonder evidence mogelijk is;
- bronversies niet auditbaar zijn;
- verkeerde CE-jaargang niet wordt tegengehouden;
- partial run als complete kan ogen;
- prompt injection uit document agentgedrag kan wijzigen;
- critical golden case faalt;
- oude rechtspraak zonder label actief wordt.

# 15. Incidenten

Voorbeelden:

- foutieve wettelijke regel geactiveerd;
- verkeerde CE-jaargang;
- bronlink naar gewijzigde inhoud;
- model levert structureel verkeerde severity;
- auditdata ontbreekt;
- persoonsgegevens onbedoeld bewaard.

Proces:

1. impact bepalen;
2. rule/source/model zo nodig deactiveren;
3. getroffen runs identificeren;
4. gebruikers informeren waar nodig;
5. fix;
6. regressietest;
7. incidentdocumentatie.

# 16. Eigenaarschap van uitkomst

De tool geeft advies en signalen.

Formele verantwoordelijkheid blijft waar de wet en organisatie die leggen.
