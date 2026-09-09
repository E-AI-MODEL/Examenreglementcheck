# DECISIONS.md
## Vastgelegde ontwerpbesluiten

**Versie:** 0.1

# D001 - Examenreglement is primair object

**Besluit:** MVP controleert het examenreglement.

**Gevolg:** PTA alleen optioneel voor kruiscontrole.

# D002 - SE én CE binnen scope

**Besluit:** De tool beperkt zich niet tot schoolexaminering.

**Gevolg:** CE-jaargangen, inzage, hulpmiddelen, zittingen en relevante rechtspraak kunnen onderdeel van controle zijn.

# D003 - Gebruik term CE

**Besluit:** Gebruik `centraal examen` als algemene term.

**Reden:** `CSE` is smaller en kan onbedoeld scope beperken.

# D004 - Geen juridisch totaalcijfer

**Besluit:** Geen percentage of compliance-score.

**Reden:** Wekt schijnprecisie en kan zware bevindingen maskeren.

# D005 - Severity en confidence apart

**Besluit:** Twee velden.

# D006 - Geen MOET zonder evidence

**Besluit:** `must` is schematechnisch alleen geldig met evidence.

# D007 - Andere scholen zijn alleen vergelijking

**Besluit:** Geen juridische norm op basis van meerderheid of voorbeeld.

# D008 - Rechtspraak genormaliseerd

**Besluit:** Iedere zaak krijgt `may_infer` en `must_not_infer`.

# D009 - Bron-snapshot per run

**Besluit:** Een run bevriest de bronset.

# D010 - Geen monolithische analyseprompt

**Besluit:** Analyse in fases.

# D011 - Registers tegen long-range fouten

**Besluit:** rollen, termijnen, definities, procedures en verwijzingen expliciet structureren.

# D012 - Geen SKILL.md nu

**Besluit:** Nog geen ChatGPT Skill bouwen.

**Reden:** De webapp is het primaire product. Eerst één bronmodel, regelmodel en analysemethode stabiliseren. Daarna kan een Skill dezelfde bestanden hergebruiken.

**Herbeoordelen wanneer:**
- analyzer werkt;
- bronbibliotheek stabiel is;
- golden set volwassen is;
- de workflow ook rechtstreeks in ChatGPT waarde heeft.

# D013 - UI is finding-first, niet chat-first

**Besluit:** Bevindingen, evidence en review zijn de hoofdinterface.

**Gevolg:** Chat kan later ondersteunend zijn.

# D014 - Schooljaar en examenjaar apart

**Besluit:** aparte velden.

Voorbeeld:

```yaml
school_year: 2026-2027
exam_year: 2027
```

# D015 - Civiel toetsingsmateriaal hoort in bronbibliotheek

**Besluit:** Niet alleen SE- en bestuursrechtelijke bronnen opnemen.

**Gevolg:** Civiele rechtspraak rond CE-score, inzage en rechtsbescherming krijgt eigen tags en proceduretype.

# D016 - Geen automatische update van juridische bronnen

**Besluit:** Crawlers mogen ontdekken, niet activeren.

# D017 - Griftland-analyse is geen ground truth

**Besluit:** Eerdere AI-analyse levert kandidaat-testcases.

**Voor golden set:** onafhankelijk verifiëren tegen origineel + primaire bron.

# D018 - Partial run is zichtbaar onvolledig

**Besluit:** De UI mag een mislukte fase nooit verbergen.


## D019 - Eén volledige v2

De bronaanvulling en HTML worden samengevoegd met alle bestanden uit v1. V1 blijft bytegelijk onder `archive/v1/`.

## D020 - Eén leidende bronregistratie

`registry.json` is leidend. YAML is alleen compatibiliteit.

## D021 - Ophalen is geen goedkeuring

Bron- en regelstatus blijven gescheiden. Alle huidige regels zijn `draft` en `production_approved: false`.

## D022 - Golden cases zijn kandidaten

Golden cases mogen geen ongeldige severity-waarde gebruiken en mogen de toepasselijke beroepsroute niet stilzwijgend aannemen.

## D023 - HTML blijft prototype

De standalone HTML mag broninhoud tonen, maar niet suggereren dat een gekozen schooldocument werkelijk is geanalyseerd.
