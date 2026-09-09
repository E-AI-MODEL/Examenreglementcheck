# UI-UX.md

## Status v3.1 / 0.4.1

V3.1 heeft een werkende deterministische runtime zonder AI. PDF/DOCX-extractie, contextbevestiging, vijf rijkere registers, conservatievere interne consistentie, gefilterde bronkandidaten, de bronpoort en menselijke review zijn gebouwd. De AI-modus is alleen een uitgeschakeld geraamte. B/E/F/G/H, OCR en de semantische evidence-validator zijn nog niet gebouwd. Raadpleeg `docs/IMPLEMENTATIESTATUS-V3.1.md` voor de actuele runtime.
> **Status 0.3.0:** De huidige HTML implementeert zes schermen als prototype. Upload en analyse zijn nog niet functioneel gekoppeld.
## Gebruikerservaring en interface van de Examenreglement-checker

**Versie:** 0.1  
**Datum:** 7 september 2026

# 1. Doel van de interface

De interface moet een complexe juridische en inhoudelijke controle begrijpelijk maken zonder de gebruiker een vals gevoel van zekerheid te geven.

De gebruiker moet steeds drie dingen kunnen beantwoorden:

1. **Wat heeft de tool gevonden?**
2. **Waarom vindt de tool dit?**
3. **Wat moet ik ermee doen?**

De UI is geen chatvenster met een juridisch oordeel. Het primaire object is een **reviewbare finding** met bewijs en status.

# 2. UX-principes

## 2.1 Eerst overzicht, daarna bewijs

De gebruiker begint met een overzicht van bevindingen en kan doorklikken naar bewijs.

Geen lange AI-rapportage als eerste scherm.

## 2.2 Severity en zekerheid nooit verwarren

`MOET` zegt iets over ernst/type.

`HIGH CONFIDENCE` zegt iets over zekerheid.

Beide staan apart in de interface.

## 2.3 Geen juridisch stoplicht zonder tekst

Kleur mag ondersteunen, nooit de betekenis dragen.

Gebruik altijd tekstlabels:

- MOET;
- JURIDISCH KWETSBAAR;
- AANBEVOLEN;
- INTERNE TEGENSPRAAK;
- VERGELIJKING;
- REDACTIONEEL;
- MENSELIJKE REVIEW.

## 2.4 Bronstatus zichtbaar

De gebruiker ziet bij iedere bron het type:

- WET / BINDEND;
- AMvB / BINDEND;
- CvTE-REGELING;
- RECHTSPRAAK;
- INSPECTIE;
- VO-RAAD;
- GESCHILUITSPRAAK;
- GELIJKE BEHANDELING;
- VERGELIJKINGSSCHOOL.

Een schoolvoorbeeld mag visueel nooit hetzelfde ogen als een wetsartikel.

## 2.5 Geen totaalscore

Vermijd:

- 87% compliant;
- juridische score 8,4;
- groen = veilig.

Toon aantallen, typen, open status en bronkwaliteit.

## 2.6 Mens houdt besluit

De UI ondersteunt review.

Belangrijke acties zijn:

- akkoord;
- niet overnemen;
- juridische review;
- verwerkt;
- opnieuw controleren.

Niet:

- “AI-besluit uitvoeren”.

# 3. Primaire gebruikers

## 3.1 Examencommissie

Wil weten:

- welke punten formeel of inhoudelijk aandacht vragen;
- welke bronnen daarbij horen;
- welke wijziging zij wil voorstellen;
- welke punten nog niet voldoende onderbouwd zijn.

## 3.2 Examensecretaris

Wil snel kunnen zien:

- procedurele fouten;
- termijnen;
- CE/SE-uitvoering;
- rollen;
- inzage;
- herkansing;
- praktische uitvoerbaarheid.

## 3.3 Schoolleiding / bevoegd gezag

Wil vooral:

- kritieke punten;
- open juridische review;
- vaststellingsgereedheid;
- audittrail;
- verschil met vorige versie.

## 3.4 MR

Heeft geen volledige analysetool nodig, maar wel een heldere export met:

- voorgestelde wijzigingen;
- reden;
- bron;
- verschil met vorige tekst.

# 4. Informatiearchitectuur

Hoofdnavigatie:

```text
Dashboard
Document
Bevindingen
Bronnen
Vergelijken
Wijzigingen
Audit
Instellingen
```

Tijdens een actieve run:

```text
Nieuwe analyse
  ├── Document uploaden
  ├── Documentgegevens bevestigen
  ├── Bronnen bevestigen
  ├── Analyse
  └── Resultaten
```

# 5. Scherm 1: start / analyses

Doel: bestaande analyses zien of een nieuwe starten.

## Inhoud

- knop `Nieuwe controle`;
- recente analyses;
- schooljaar;
- documentstatus;
- datum laatste run;
- status: compleet / gedeeltelijk / mislukt;
- aantal open findings;
- bron-snapshot.

## Voorbeeld

```text
Examenreglement 2026-2027
Havo / vwo
Laatste analyse: 07-09-2026 21:43
Run: compleet

4 MOET
7 juridisch kwetsbaar
11 open reviews

[Open analyse] [Nieuwe run]
```

# 6. Scherm 2: upload en setup

Gebruik een korte wizard, geen technisch formulier van één pagina.

## Stap 1: document

Drag-and-drop:

> Upload het examenreglement  
> DOCX of PDF

Na upload:

- bestandsnaam;
- grootte;
- parserstatus;
- waarschuwing bij scan/OCR;
- mogelijke persoonsgegevens.

## Stap 2: context

Velden:

- schooljaar;
- schoolsoorten;
- status reglement;
- onderwijscontext indien juridisch relevant;
- optioneel PTA.

### Slimme default

Bij `2026-2027` toont de tool:

> Verwacht examenjaar centraal examen: **2027**

De gebruiker bevestigt dit.

## Stap 3: vergelijkingsmateriaal

Optioneel.

De gebruiker kan:

- vaste vergelijkingsset gebruiken;
- eigen documenten toevoegen;
- vergelijking overslaan.

Duidelijke tekst:

> Vergelijkingsreglementen zijn voorbeelden en worden nooit als wettelijke bron gebruikt.

# 7. Scherm 3: documentcheck vóór analyse

Belangrijk vanwege parsingfouten en context compression.

Toon een samenvatting van wat het systeem uit het document heeft gehaald:

```text
Titel                         Examenreglement 2026-2027
Schoolsoorten                 havo, vwo
Hoofdstukken                  17
Artikelen                     68
Definities                    12
Wettelijke verwijzingen       23
Genoemde rollen               8
Vaststellingsdatum            NIET GEVONDEN
Examenjaar CE                 2027
Parserkwaliteit               hoog
```

## Uitklapbaar

- inhoudsopgave;
- gevonden rollen;
- gevonden termijnen;
- gevonden definities;
- onzekere pagina's.

Knop:

`Gegevens kloppen, start analyse`

of

`Corrigeren`

# 8. Scherm 4: analysevoortgang

Toon fases, niet “AI denkt...”.

```text
✓ Documentstructuur
✓ Verplichte onderdelen
✓ Interne consistentie
● Actualiteit
○ SE / CE
○ Jurisprudentie
○ Vergelijking
○ Tegenlezing
○ Evidence-validatie
```

Bij fout:

```text
Jurisprudentiecontrole: gedeeltelijk
2 zoekacties konden niet worden gevalideerd.
De run wordt als PARTIAL gemarkeerd.
```

De gebruiker mag een partial run bekijken, maar ziet permanent dat deze niet compleet is.

# 9. Scherm 5: dashboard

## Bovenste blok

Geen score.

Gebruik:

```text
61 controlepunten onderzocht

4   MOET
7   juridisch kwetsbaar
6   interne tegenspraken
11  aanbevolen
9   redactioneel
24  zonder bevinding
```

## Daarnaast

```text
Reviewstatus

18 nog beoordelen
10 akkoord
4 juridische review
5 verwerkt
```

## Bronstatus

```text
Bron-snapshot 2026.09.07-1
42 actieve bronnen
5 bindende bronsets
7 jurisprudentierecords
3 vergelijkingsscholen
```

# 10. Scherm 6: lijst met bevindingen

Een finding is de belangrijkste UI-eenheid.

## Standaardrij

```text
[MOET] [HIGH]
N.5  Beroepstermijn mogelijk onjuist
Beroep · wettelijke conformiteit

Eigen tekst noemt 2 dagen. Voor deze beroepsroute is
een andere termijn als wettelijke norm gekoppeld.

Bron: WVO 2020 · art. ...
Status: Nog beoordelen

[Open]
```

## Filters

- severity;
- confidence;
- onderwerp;
- SE / CE / algemeen;
- bronsoort;
- reviewstatus;
- artikel/hoofdstuk;
- alleen findings met juridische review;
- alleen unresolved.

## Sortering

Default:

1. MOET;
2. legally vulnerable;
3. internal conflict;
4. human review;
5. recommended;
6. editorial.

Binnen severity: confidence en documentvolgorde.

# 11. Scherm 7: finding detail

Gebruik bij voorkeur een split view.

```text
┌────────────────────────────────┬────────────────────────────────┐
│ EIGEN DOCUMENT                 │ BEVINDING                      │
│                                │                                │
│ Artikel N.5                    │ MOET                           │
│ ...binnen twee dagen...        │ Confidence: HIGH               │
│                                │                                │
│ [toon context ervoor/erna]     │ Uitleg                         │
│                                │ ...                            │
│                                │                                │
│                                │ Evidence                       │
│                                │ WVO 2020 ...                   │
│                                │                                │
│                                │ Voorstel                       │
│                                │ ...                            │
└────────────────────────────────┴────────────────────────────────┘
```

## Finding-detail bevat

- finding-ID;
- documentlocatie;
- exacte relevante passage;
- contextknop;
- severity;
- confidence;
- type;
- uitleg;
- evidence;
- bronstatus;
- voorstelactie;
- voorsteltekst;
- eventuele rechtspraak;
- `wat deze uitspraak niet bewijst`;
- menselijke notities;
- reviewactie.

# 12. Bronnenpaneel

Open een bron in een drawer of rechterpaneel.

Toon:

```text
Wet voortgezet onderwijs 2020
Type: WET / BINDEND
Status: actief
Geldig voor run: ja
Geraadpleegd: 07-09-2026

Artikel: ...
Relevant fragment: ...

[Open officiële bron]
[Waarom gebruikt de tool deze bron?]
```

Voor VO-raad:

```text
Type: PROFESSIONELE HANDREIKING
Bindend: nee
Gebruik: checklist / interpretatiehulp
```

Voor vergelijkingsschool:

```text
Type: VERGELIJKING
Juridische autoriteit: geen
```

# 13. Rechtspraakweergave

Rechtspraak moet anders worden getoond dan gewone bronnen.

## Case card

```text
ECLI:NL:RBMNE:2025:4637
Rechtbank Midden-Nederland
22 augustus 2025
Civiel kort geding

Thema:
CE-score · inzage · herbeoordeling

Waarom relevant:
...

Wat de uitspraak ondersteunt:
...

Niet uit deze uitspraak afleiden:
...
```

De sectie `Niet uit deze uitspraak afleiden` is standaard zichtbaar.

# 14. Vergelijkingsscherm

Vergelijk per onderwerp, niet per volledig document.

Voorbeeld:

| Onderwerp | Eigen school | Regius | RSG Ter Apel | STC |
|---|---|---|---|---|
| Beroep | tekst | tekst | tekst | tekst |
| Herkansing | tekst | tekst | tekst | tekst |
| AI/plagiaat | tekst | tekst | tekst | tekst |

Bovenaan:

> Deze vergelijking laat zien hoe andere scholen onderwerpen formuleren. Dit is geen juridische norm.

# 15. Wijzigingsscherm

Hier werkt de gebruiker van finding naar voorstel.

Per item:

```text
N.5 Beroepstermijn
Status finding: akkoord

Huidig:
...

Voorstel:
...

Reden:
...

Bron:
...

[Voorstel aanpassen]
[Toevoegen aan wijzigingsset]
```

De tool schrijft nooit direct over het bronbestand heen zonder expliciete opdracht.

# 16. Diff-weergave

Na een gewijzigde versie:

```diff
- binnen twee dagen
+ binnen vijf dagen
```

Toon daarbij:

- oude finding;
- nieuwe analyse;
- opgelost / deels opgelost / nog open;
- nieuwe conflictscan.

# 17. Audit-scherm

Voor transparantie:

```text
Run ID
Document hash
Starttijd
Eindtijd
Gebruiker
Parserversie
Regelsetversie
Bron-snapshot
Modelversie
Promptversies
Fases compleet/partial/failed
Aantal findings
Menselijke wijzigingen
Exports
```

Niet alles hoeft standaard zichtbaar. Gebruik een eenvoudige samenvatting met `Technische details`.

# 18. Empty states

Goede empty states voorkomen dat nul findings als juridische garantie wordt gelezen.

Niet:

> Geen problemen gevonden. Alles is in orde.

Wel:

> Binnen de uitgevoerde controles zijn geen bevindingen gevonden.  
> Dit is geen juridische garantie. Bekijk de dekking van deze run.

Link:

`Bekijk welke controles zijn uitgevoerd`

# 19. Error states

## Parsing error

> Pagina 14 kon niet betrouwbaar worden gelezen.  
> Bevindingen die van deze pagina afhangen krijgen geen harde classificatie.

## Bron niet bereikbaar

> De primaire bron kon niet worden gevalideerd.  
> De finding is teruggezet naar `MENSELIJKE REVIEW`.

## Evidence conflict

> De beschikbare bronnen geven geen eenduidige basis voor een harde conclusie.

# 20. Partial run

Een partial run krijgt permanent een banner:

> **Analyse onvolledig**  
> Eén of meer controlefases zijn niet volledig uitgevoerd. Gebruik deze run niet als eindcontrole.

Nooit alleen een klein icoon.

# 21. Accessibility

Minimaal WCAG 2.2 AA als ontwerpniveau.

Concreet:

- kleur nooit als enige informatiedrager;
- toetsenbordnavigatie;
- zichtbare focus;
- goede heading-structuur;
- labels bij iconen;
- tabellen hebben kolomkoppen;
- voldoende contrast;
- tooltips niet als enige plek voor belangrijke informatie;
- foutmeldingen tekstueel;
- screenreader-vriendelijke statusupdates tijdens analyse.

# 22. Taalgebruik

Schrijf gewoon en precies.

Wel:

> Het reglement noemt hier twee verschillende termijnen.

Niet:

> Er is sprake van een discrepantie binnen het normatieve kader.

Wel:

> Deze bron is een VO-raad-handreiking en is niet bindend.

Niet:

> De bron heeft een lagere autoriteitsclassificatie.

Technische termen mogen in de auditweergave.

# 23. Progressive disclosure

Niet alles tegelijk tonen.

### Niveau 1
Wat moet ik weten?

### Niveau 2
Waarom?

### Niveau 3
Welke bron en passage?

### Niveau 4
Technische provenance en analysemethode.

Dit beperkt cognitieve belasting zonder bewijs te verbergen.

# 24. Mobiel en desktop

De primaire werkervaring is desktop/laptop vanwege documentvergelijking.

Mobiel ondersteunt:

- dashboard;
- findings lezen;
- reviewstatus;
- opmerkingen;
- bron openen.

Complexe diff, documentvergelijking en bulkreview krijgen op mobiel een vereenvoudigde weergave.

# 25. Rollen in de UI

Mogelijke rollen:

## Reviewer
- findings bekijken;
- status en notities aanpassen.

## Beheerder examenproces
- analyses starten;
- wijzigingssets maken;
- exports genereren.

## Bronbeheerder
- bronrecords beheren;
- versie activeren/deactiveren.

## Technisch beheerder
- modellen, prompts, releases en audit.

Niet iedere gebruiker ziet bronbeheer of modelinformatie.

# 26. Governance zichtbaar maken in UX

Voor de gebruiker moet zichtbaar zijn:

- wanneer bronnen voor het laatst zijn gecontroleerd;
- of de run compleet is;
- welke versie van de regels is gebruikt;
- welke findings menselijke review vragen;
- welke findings na wijziging opnieuw zijn gecontroleerd.

# 27. Geen chat als hoofdinterface

Een chat kan later ondersteunend zijn, bijvoorbeeld:

> “Waarom is deze finding juridisch kwetsbaar?”

Maar chat mag niet de primaire plaats worden waar bevindingen leven.

De finding, evidence en reviewstatus blijven gestructureerde data.

# 28. Eventuele assistentfunctie

Een beperkte assistent kan contextueel vragen beantwoorden over de geopende finding.

Regels:

- antwoordt alleen vanuit de actieve finding en bronset;
- noemt gebruikte bron;
- mag severity niet stil wijzigen;
- kan een nieuwe finding voorstellen maar niet zonder validatie opslaan;
- kan geen formele beslissing nemen.

# 29. Belangrijkste UX-metrieken

Niet alleen snelheid meten.

Meet bijvoorbeeld:

- percentage findings met geopende evidence;
- percentage MOET-findings dat menselijk is beoordeeld;
- aantal findings dat na review wordt afgewezen;
- tijd van finding naar besluit;
- aantal partial runs dat ten onrechte als eindcontrole wordt gebruikt;
- aantal bronklikken;
- verschillen tussen analyzer-versies.

# 30. Prototypevolgorde

Voor de eerste UI-prototype:

1. startscherm;
2. uploadwizard;
3. documentcheck;
4. analysevoortgang;
5. dashboard;
6. findingslijst;
7. finding detail + bronpaneel;
8. reviewstatus;
9. wijzigingsset;
10. audit.

Vergelijking en geïntegreerde assistent kunnen daarna.

# 31. Wireframe: dashboard

```text
┌───────────────────────────────────────────────────────────────┐
│ Examenreglement 2026-2027                    Run COMPLEET    │
│ havo / vwo · bronset 2026.09.07-1                            │
├───────────────────────────────────────────────────────────────┤
│ 4 MOET   7 KWETSBAAR   6 CONFLICT   11 AANBEVOLEN           │
├───────────────────────────────────────────────────────────────┤
│ Review                                                        │
│ 18 nog beoordelen · 10 akkoord · 4 juridisch · 5 verwerkt   │
├───────────────────────────────────────────────────────────────┤
│ Topbevindingen                                                │
│ [MOET] N.5 Beroepstermijn ...                    [Open]      │
│ [MOET] A.1 Verouderde wettelijke grondslag ...    [Open]      │
│ [CONFLICT] P.3 Rollen examencommissie ...         [Open]      │
└───────────────────────────────────────────────────────────────┘
```

# 32. Wireframe: finding

```text
┌──────────────────────────────┬────────────────────────────────┐
│ DOCUMENT                     │ FINDING                        │
│                              │                                │
│ Artikel N.5                  │ MOET · confidence HIGH         │
│                              │                                │
│ "... binnen twee dagen ..."  │ Wat is er aan de hand?        │
│                              │ ...                            │
│ [Meer context]               │                                │
│                              │ Evidence                       │
│                              │ [WET] WVO 2020 ...             │
│                              │                                │
│                              │ Voorstel                       │
│                              │ ...                            │
│                              │                                │
│                              │ [Akkoord] [Afwijzen]           │
│                              │ [Juridische review]            │
└──────────────────────────────┴────────────────────────────────┘
```

# 33. Definition of done voor UI-features

Een scherm is pas klaar wanneer:

- loading, empty, error en partial states zijn ontworpen;
- severity én confidence zichtbaar zijn waar relevant;
- bronstatus toegankelijk is;
- acties auditbaar zijn;
- toetsenbordgebruik werkt;
- mobiele fallback is bepaald;
- geen juridisch oordeel alleen uit kleur of icoon blijkt;
- tekst begrijpelijk is voor een examensecretaris zonder technische kennis.
