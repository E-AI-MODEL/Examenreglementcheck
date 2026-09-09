# AI-RISKS.md

## Status v3 / 0.4.0

V3 heeft een werkende deterministische runtime zonder AI. PDF/DOCX-extractie, documentcheck, vijf registers, interne consistentie en bronkandidaten zijn gebouwd. De AI-modus is alleen een uitgeschakeld geraamte. B/E/F/G/H, OCR en de volledige juridische evidence-validator zijn nog niet gebouwd. Raadpleeg `docs/IMPLEMENTATIESTATUS.md` voordat je doelarchitectuur als bestaande functionaliteit beschrijft.
> **Status 0.3.0:** In 0.3.0 zijn alleen bronstatus, regelstatus en enkele integriteitsblokkades technisch getest; de analyzermaatregelen zijn nog ontwerp.
## Bekende modelrisico's en verplichte waarborgen

**Versie:** 0.1

# 1. Gebruik

Dit document beschrijft geen interne redeneerinstructies voor een model.

Het beschrijft risico's die gevolgen hebben voor het systeemontwerp.

Vast patroon:

> risico → mogelijk effect → vereiste maatregel → test

# 2. Context compression

## Risico

Lange documenten of lange sessies kunnen worden samengevat of gecomprimeerd. Details uit eerdere delen kunnen minder precies beschikbaar zijn.

## Effect

- uitzondering vergeten;
- definitie missen;
- oude samenvatting als exacte tekst behandelen;
- procedures verwarren.

## Maatregel

- document structureren;
- artikelen apart indexeren;
- relevante passage opnieuw ophalen vóór zware finding;
- finding baseren op evidence, niet op eerdere samenvatting;
- bron- en documentlocatie bewaren.

## Test

Een testcase met uitzondering in vroeg hoofdstuk en hoofdregel ver later.

# 3. Span thinking / long-range reasoning

## Risico

Ver uit elkaar liggende passages worden niet altijd betrouwbaar aan elkaar gekoppeld.

## Effect

Botsende rollen of termijnen blijven onopgemerkt.

## Maatregel

Gebruik expliciete registers:

- role;
- term;
- definition;
- procedure;
- cross-reference.

Laat code mogelijke conflicten produceren.

## Test

Twee artikelen op grote afstand met verschillende beroepstermijn.

# 4. Long-context dilution

## Risico

Te veel bronnen in één context verzwakt de aandacht voor relevante bron.

## Maatregel

- metadatafilter;
- kleine evidence-set;
- topicgerichte retrieval;
- vergelijkingsmateriaal niet meesturen naar wettelijke check zonder reden.

# 5. Authority flattening

## Risico

Wet, handreiking en schoolvoorbeeld klinken in modeltekst even gezaghebbend.

## Maatregel

Verplichte bronmetadata en zichtbaar bronlabel.

## Test

VO-raad-advies mag niet als `must` eindigen zonder bindende grond.

# 6. Citation drift

## Risico

Bron bestaat, maar ondersteunt claim slechts gedeeltelijk.

## Maatregel

Aparte evidence validator.

## Test

Case waarin bron hetzelfde onderwerp noemt maar andere procedure betreft.

# 7. Retrieval miss

## Risico

Geen resultaat wordt geïnterpreteerd als “bestaat niet”.

## Maatregel

Formuleer:

> Binnen de geactiveerde bronset is geen passende bron gevonden.

Niet:

> Er bestaat geen bron.

# 8. Negative evidence

## Risico

Tekst niet gevonden = bepaling ontbreekt.

## Maatregel

Voor “ontbreekt”:

- parser confidence;
- semantische match;
- structurele check;
- human review bij twijfel.

# 9. Recency error

## Risico

Oude regeling wordt actueel gebruikt.

## Maatregel

- valid_from;
- valid_to;
- exam_year;
- status;
- retrieved_at;
- superseded_by.

# 10. Schooljaar versus examenjaar

## Risico

Schooljaar 2026-2027 wordt gekoppeld aan CE 2026.

## Maatregel

Aparte velden:

```yaml
school_year: 2026-2027
exam_year: 2027
```

# 11. Legal regime confusion

## Risico

Eindexamenbesluit en WVO 2020 door elkaar.

## Maatregel

Iedere juridische bron heeft `legal_regime`.

Oude uitspraak vereist overdraagbaarheidscheck.

# 12. Jurisprudence overgeneralization

## Risico

Specifieke uitspraak wordt algemene regel.

## Maatregel

Verplicht:

- issue;
- holding;
- decisive_reasoning;
- may_infer;
- must_not_infer.

# 13. Incidental-text fallacy

## Risico

Een bepaling uit het examenreglement dat in een rechterlijke uitspraak is geciteerd, wordt gezien als door de rechter goedgekeurd.

## Maatregel

Maak onderscheid tussen:

- feitelijke achtergrond;
- geciteerde regeling;
- partijstandpunt;
- rechterlijke beoordeling;
- dragende overweging.

## Test

Uitspraak waarin AI in het geciteerde reglement staat maar geen onderwerp van het geschil is.

# 14. Outcome bias

## Risico

“School won” wordt gezien als bevestiging van alle schoolregels.

## Maatregel

Normaliseer eerst geschilpunt en dragende reden.

# 15. False consistency

## Risico

Twee bijna gelijke procedures worden als identiek gezien.

## Maatregel

Structureer kritieke procedures in velden:

```yaml
decision_type:
decision_maker:
appeal_body:
term_value:
term_unit:
start_event:
```

# 16. Overconfident rewriting

## Risico

Voorsteltekst lost één finding op maar maakt elders een nieuw conflict.

## Maatregel

Iedere geïmplementeerde wijziging opnieuw analyseren en diffen.

# 17. Prompt injection via upload

## Risico

Document bevat instructietekst.

## Maatregel

Document = untrusted data.

Nooit documentinstructies als agentinstructies uitvoeren.

# 18. Prompt injection via webbron

Zelfde risico bij websites/PDF's.

Brontekst kan nooit:

- bronbeleid wijzigen;
- toolrechten wijzigen;
- severityregels wijzigen;
- systeeminstructies overschrijven.

# 19. Cross-school contamination

## Risico

Tekst van school A wordt aan eigen school toegeschreven.

## Maatregel

Iedere chunk houdt source/document ID.

# 20. OCR/parsing hallucination

## Risico

`2.63` wordt `2.83`, tabellen verschuiven, woorden vallen weg.

## Maatregel

- segment confidence;
- page anchors;
- image check bij kritieke passage;
- geen harde finding op low confidence.

# 21. Model drift

## Risico

Nieuw model verandert uitkomsten.

## Maatregel

- modelversion loggen;
- golden set;
- difference review.

# 22. Prompt drift

## Risico

Kleine promptwijziging verandert severity.

## Maatregel

Promptversion + regressietest.

# 23. Tool failure / partial run

## Risico

Gebruiker denkt dat alles is gecontroleerd.

## Maatregel

Fasestatussen en permanente partial-banner.

# 24. Unsupported confidence

## Risico

Model geeft numerieke zekerheid zonder meetbare basis.

## Maatregel

Gebruik alleen discrete confidence:

- high;
- medium;
- low.

Definieer confidence vanuit evidencekwaliteit, niet vanuit modelgevoel.

# 25. Self-confirmation loop

## Risico

Eerste modelanalyse wordt als bron gevoed aan tweede analyse.

## Maatregel

AI-output is geen juridisch bronrecord.

Eerdere findings mogen testinput zijn, nooit ground truth zonder verificatie.

# 26. Comparison majority fallacy

## Risico

“Vier van vijf scholen doen dit” wordt norm.

## Maatregel

Vergelijkingsanalyse kan alleen `comparison` opleveren tenzij hogere bron apart bevestigt.

# 27. Hidden fallback

## Risico

Primaire bron faalt, systeem gebruikt blog of schoolpagina zonder melding.

## Maatregel

Fallbackstatus zichtbaar en severity blokkeren waar nodig.

# 28. Stale source by URL

## Risico

Zelfde URL krijgt later nieuwe inhoud.

## Maatregel

Bij ingest:

- retrieved_at;
- content hash;
- source version;
- snapshot/reference waar toegestaan.

# 29. Human automation bias

## Risico

Gebruiker neemt AI-voorstel over omdat het overtuigend oogt.

## Maatregel

- bewijs naast voorstel;
- expliciete review;
- geen éénknops “fix alles” voor juridische wijzigingen;
- audit wie goedkeurde.

# 30. Testmatrix

Iedere release moet minimaal cases hebben voor:

- contextafstand;
- correcte negative control;
- verkeerde jaargang;
- oude wet;
- zwakke bron;
- irrelevante rechtspraak;
- geciteerde maar niet beoordeelde bepaling;
- parsing uncertainty;
- partial run;
- prompt injection;
- cross-school bronverwisseling.
