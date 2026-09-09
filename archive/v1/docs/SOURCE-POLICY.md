# SOURCE-POLICY.md

**Versie:** 0.1

# 1. Doel

Dit document bepaalt hoe bronnen worden geclassificeerd en gebruikt.

# 2. Geen simpele ranglijst

Bronnen hebben verschillende functies.

Een rechterlijke uitspraak en een wet zijn niet hetzelfde soort bron.

Gebruik daarom:

- authority class;
- source type;
- binding status;
- context;
- geldigheid;
- onderwerp.

# 3. Bronklassen

## Binding

Voorbeelden:

- WVO 2020;
- Uitvoeringsbesluit WVO 2020;
- formele regelingen;
- relevante beleidsregels binnen hun toepassingsbereik.

Kan directe basis zijn voor `must`.

## Official application / oversight

Voorbeelden:

- rechtspraak;
- Inspectie;
- CvTE / Examenblad.

Gebruik voor toepassing, uitleg, toezicht en procedures.

## Professional guidance

Voorbeeld:

- VO-raad.

Sterke praktische bron, maar niet automatisch bindend.

## Dispute / equality

Voorbeelden:

- Onderwijsgeschillen;
- College voor de Rechten van de Mens.

Eigen bronlabel. Niet presenteren als rechtbank wanneer dat niet zo is.

## Comparison

Andere schoolreglementen.

Alleen voorbeeld.

# 4. Harde regels

- Geen `must` alleen op basis van comparison.
- Geen `must` alleen op basis van een niet-bindende handreiking wanneer bindende grond vereist is.
- Geen oude bron zonder regime- en geldigheidslabel.
- Geen rechtspraak zonder begrenzing van de gevolgtrekking.
- Geen jaargebonden CE-bron zonder correct exam_year.

# 5. URL-beleid

Voorkeur:

1. officiële permanente bron;
2. officiële publicatiepagina;
3. officiële PDF;
4. pas daarna secundaire publicatie.

Bewaar naast URL:

- retrieved_at;
- content hash waar mogelijk;
- publicatiedatum;
- geldig vanaf/tot.

# 6. Bronstatus

```text
discovered
pending_review
validated
active
superseded
archived
rejected
```

Alleen `active` mag standaard in productieretrieval.

# 7. Rechtspraak

Iedere case wordt handmatig of gecontroleerd genormaliseerd.

Verplicht:

- ECLI;
- rechter/instantie;
- datum;
- procedure type;
- legal regime;
- exam type;
- issue;
- holding;
- decisive reasoning;
- may infer;
- must not infer.

# 8. Civiel en bestuursrecht

De tool gaat niet uit van één uniforme rechtsroute.

Een geschil rond examens kan afhankelijk van context, schooltype, besluit en rechtsvraag verschillende routes kennen.

De bronbibliotheek moet die route als metadata opslaan.

# 9. VO-raad

Gebruik de jaarlijkse editie als controlestructuur en professionele handreiking.

De VO-raad geeft zelf aan dat de handreikingen geen verplichtend karakter hebben. Die status moet in UI en bronmetadata zichtbaar blijven.

# 10. CvTE / Examenblad

Gebruik voor jaargebonden centrale-examenregels.

Voor schooljaar 2026-2027:

```text
exam_year = 2027
```

# 11. Vergelijkingsscholen

Leg minimaal vast:

- school;
- schoolsoorten;
- jaar;
- status: concept/vastgesteld/onbekend;
- URL;
- retrieved_at.

Een concept blijft zichtbaar als concept.

# 12. Bronconflict

Bij conflict:

1. bepaal bronsoort;
2. bepaal geldigheid;
3. bepaal toepassingsbereik;
4. zoek hogere/primair bindende norm;
5. hard oordeel blokkeren bij onopgelost conflict.

# 13. Bronclaim

Iedere evidence-link moet kunnen beantwoorden:

> Welke concrete claim ondersteunt deze bron?

Geen algemene bronlijst per finding zonder koppeling.

# 14. Nieuwe webbron

Een crawler mag bronkandidaten vinden.

Proces:

```text
discover
classify
validate
normalize
review
activate
```

Nooit rechtstreeks `discover -> active`.
