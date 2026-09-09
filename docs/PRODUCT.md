# PRODUCT.md

## Status v3.1 / 0.4.1

V3.1 heeft een werkende deterministische runtime zonder AI. PDF/DOCX-extractie, contextbevestiging, vijf rijkere registers, conservatievere interne consistentie, gefilterde bronkandidaten, de bronpoort en menselijke review zijn gebouwd. De AI-modus is alleen een uitgeschakeld geraamte. B/E/F/G/H, OCR en de semantische evidence-validator zijn nog niet gebouwd. Raadpleeg `docs/IMPLEMENTATIESTATUS-V3.1.md` voor de actuele runtime.
> **Status 0.3.0:** Dit document beschrijft het doelproduct. In 0.3.0 zijn alleen de HTML-demo, bronlaag en bronbewaking gebouwd.
## Examenreglement-checker

**Versie:** 0.1  
**Datum:** 7 september 2026

# 1. Waartoe dient de tool?

De Examenreglement-checker helpt scholen om een examenreglement systematisch te controleren voordat het reglement formeel wordt vastgesteld en gebruikt.

De gebruiker levert een examenreglement aan. De tool onderzoekt vervolgens of het document:

- aansluit op actuele wet- en regelgeving;
- verplichte onderdelen bevat;
- intern logisch en consistent is;
- geen verouderde grondslagen of artikelnummers gebruikt;
- functies, rollen en bevoegdheden helder toedeelt;
- termijnen consequent gebruikt;
- procedures uitvoerbaar en begrijpelijk beschrijft;
- regels rond het schoolexamen correct behandelt;
- regels rond het centraal examen correct behandelt;
- op juridisch gevoelige punten steun of waarschuwingen uit relevante rechtspraak oplevert;
- bruikbare vergelijkingen met andere scholen mogelijk maakt.

De tool vervangt geen examencommissie, bevoegd gezag, medezeggenschap, examensecretaris of juridisch adviseur.

De tool verklaart een reglement nooit automatisch juridisch “waterdicht”.

# 2. Voor wie?

Primaire gebruikers:

- examencommissie;
- examensecretaris;
- schoolleiding;
- medewerkers die het examenreglement voorbereiden;
- bestuurder of beleidsmedewerker die de kwaliteit wil controleren.

Secundaire gebruikers:

- MR bij voorbereiding van instemming;
- juridisch adviseur;
- kwaliteitsmedewerker;
- externe reviewer.

# 3. Wat heeft de gebruiker eraan?

Na een analyse moet de gebruiker snel kunnen zien:

- wat vóór vaststelling aandacht nodig heeft;
- waarom iets aandacht nodig heeft;
- hoe zwaar het probleem is;
- hoe zeker de analyse is;
- welke bron de conclusie draagt;
- waar de relevante tekst in het eigen reglement staat;
- welke wijziging kan worden overwogen;
- welke punten menselijke of juridische beoordeling vragen.

De tool vermindert handwerk, maar het belangrijkste voordeel is **controleerbaarheid**.

# 4. Wat krijgt de gebruiker terug?

Iedere bevinding bevat minimaal:

- vindplaats in eigen document;
- korte titel;
- onderwerp;
- type bevinding;
- severity;
- confidence;
- claim;
- bewijs/bronnen;
- uitleg;
- mogelijke actie;
- mogelijke voorsteltekst;
- menselijke reviewstatus.

## 4.1 Bevindingstypen

| Label | Betekenis |
|---|---|
| `MOET` | Directe, herleidbare strijd met bindende norm of verplicht onderdeel ontbreekt |
| `JURIDISCH KWETSBAAR` | Niet eenvoudig strijdig, maar procedure, rechtspraak of context maakt de bepaling risicovol |
| `AANBEVOLEN` | Gezaghebbende handreiking of betere werkwijze, niet automatisch bindend |
| `INTERNE TEGENSPRAAK` | Het eigen document bevat botsende regels |
| `VERGELIJKING` | Andere school geeft bruikbaar voorbeeld |
| `REDACTIONEEL` | Tekst-, nummerings-, verwijzings- of definitieprobleem |
| `MENSELIJKE REVIEW` | Systeem heeft onvoldoende basis voor een harde conclusie |

Severity en confidence blijven aparte velden.

# 5. Primaire scope

Het examenreglement is het primaire onderzoeksobject.

De tool controleert onderwerpen rond:

- organisatie van het eindexamen;
- SE;
- CE;
- onregelmatigheden;
- maatregelen;
- afwezigheid;
- inhalen;
- herkansen;
- examencommissie;
- examensecretaris;
- beroep;
- bezwaarprocedures waar relevant;
- inzage;
- afwijkende wijze van examineren;
- vervroegd examen;
- hoger niveau;
- vrijstellingen;
- afronding;
- uitslagregels voor zover het reglement die behoort te bevatten.

## 5.1 Terminologie CE

Gebruik als algemene term `centraal examen (CE)`.

Gebruik `centraal schriftelijk examen` alleen wanneer werkelijk die specifieke examenvorm wordt bedoeld.

# 6. PTA

Het PTA is geen tweede primair onderzoeksobject in MVP.

Optionele kruiscontrole kan bijvoorbeeld onderzoeken:

- sluiten herkansingsregels aan;
- verwijst het reglement correct naar het PTA;
- zijn regels rond SE-afronding niet onderling strijdig.

Een volledige PTA-checker wordt een aparte module.

# 7. Niet binnen MVP

De tool:

- beoordeelt geen individuele leerlingcasus;
- corrigeert geen CE-werk;
- bepaalt geen cijfer;
- stelt geen fraude vast;
- bepaalt niet of een leerling slaagt;
- neemt geen formeel besluit;
- publiceert geen nieuw reglement zonder menselijke actie;
- beoordeelt niet de vakinhoudelijke kwaliteit van iedere concrete SE-toets;
- voert niet automatisch een volledige PTA-audit uit.

# 8. Analyseprincipe

De tool gebruikt geen enkele allesomvattende prompt.

De analyse bestaat uit afzonderlijke stappen:

1. documentextractie;
2. formele volledigheid;
3. interne consistentie;
4. actualiteit;
5. SE/CE-specifieke controle;
6. juridisch gevoelige punten en rechtspraak;
7. optionele vergelijking;
8. kritische tegenlezing;
9. evidence-validatie.

De norm komt uit de bronbibliotheek. Het taalmodel helpt bij semantische interpretatie en uitleg.

# 9. Happy flow

## Stap 1: nieuwe controle

De gebruiker start een analyse en kiest:

- schooljaar;
- schoolsoorten;
- status document: concept, vastgesteld of historisch;
- optioneel: openbaar/bijzonder onderwijs voor juridische routering.

Daarna uploadt de gebruiker het examenreglement.

Optioneel:

- PTA;
- vorig reglement;
- eigen beleidsdocument;
- gewenste vergelijkingsset.

## Stap 2: documentcheck

De tool toont wat is herkend:

> Examenreglement 2026-2027  
> havo en vwo  
> 68 artikelen  
> 12 definities  
> vaststellingsdatum niet gevonden  
> schooljaar: 2026-2027  
> examenjaar CE: 2027

De gebruiker bevestigt of corrigeert deze gegevens.

## Stap 3: bron-snapshot

De run krijgt een vaste bronset.

Bijvoorbeeld:

> bronnen gecontroleerd op: 7 september 2026  
> VO-raad checklist: 2026-2027  
> CE-bronnen: examenjaar 2027  
> jurisprudentieset: 2026.09.1

De bronset verandert niet ongemerkt tijdens dezelfde run.

## Stap 4: analyse

De gebruiker ziet voortgang per fase.

## Stap 5: dashboard

Voorbeeld:

> 61 controlepunten  
> 4 MOET  
> 7 juridisch kwetsbaar  
> 6 interne tegenstrijdigheden  
> 11 aanbevelingen  
> 9 redactioneel  
> 24 zonder bevinding

Geen totaalscore zoals “82% juridisch correct”.

## Stap 6: review

Per finding kan de gebruiker:

- de eigen tekst openen;
- de bron openen;
- de juridische status van de bron zien;
- de uitleg bekijken;
- voorsteltekst bekijken;
- notities maken;
- akkoord, afwijzen, escaleren of verwerkt kiezen.

## Stap 7: wijzigingsset

De tool maakt op verzoek:

- wijzigingslijst per artikel;
- voorstelteksten;
- open beslissingen;
- wijzigingslog.

## Stap 8: hercontrole

Na aanpassing wordt het document opnieuw geanalyseerd.

De tool toont:

- opgelost;
- gedeeltelijk opgelost;
- nog open;
- nieuw conflict ontstaan.

## Stap 9: export

Minimale exports:

- volledig bevindingenrapport;
- korte beslisnotitie;
- wijzigingslijst;
- bronverantwoording;
- auditoverzicht.

# 10. Niet-happy flow

## Slechte PDF

De tool benoemt welke pagina's onzeker zijn uitgelezen. Een harde “ontbreekt”-finding wordt geblokkeerd wanneer parsing te onzeker is.

## Schooljaar ontbreekt

De gebruiker moet het jaar bevestigen. De tool kiest niet stilzwijgend een examenseizoen.

## Bronconflict

De tool laat het conflict zien en verlaagt de zekerheid.

## Primaire bron ontbreekt

Een secundaire bron mag een aandachtspunt opleveren, maar geen hard `MOET`-label zonder passende primaire grond.

## Oude jurisprudentie

De uitspraak wordt zichtbaar als oud regime gelabeld.

# 11. Belangrijke kwaliteitsgrens

De tool ondersteunt een juridisch en organisatorisch proces. Hij neemt het proces niet over.

Formele stappen rond voorstel, vaststelling, instemming, publicatie en uitvoering blijven bij de bevoegde personen en organen.
