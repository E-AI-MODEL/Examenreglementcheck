# Changelog

## 0.5.0 - v3.3 - 2026-09-10

De afgesproken no-AI-keten is aangevuld met formele volledigheidsscreening, bronactualiteit binnen de snapshot, vergelijking, kritische tegenlezing en evidence-/provenancevalidatie. Dunne PDF-pagina's gebruiken optioneel lokale Tesseract-OCR. De browser kan runs hervatten en verwijderen en rapporten als JSON of Markdown exporteren. Een expliciet lege schoolsoortselectie wordt niet meer stilzwijgend vervangen door eerdere waarden en reviewacties verversen nu direct het auditlog. SE/CE (inclusief PTA/rooster/hulpmiddelen) en jurisprudentie hebben bewust status `out_of_scope`. Alle regels blijven concept; juridische `must` blijft geblokkeerd.

## 0.4.2 - v3.2 - 2026-09-08

Kleine upgrade naar aanleiding van een demo-run met `examples/demo-reglement.docx`. De demo toonde dat `_start_event` in `app/registers.py` te veel tekst extraheren, waardoor twee clausules die semantisch dezelfde stap beschreven (bv. "3 vs 5 schooldagen na publicatie voor herkansing") verschillende start_events kregen en geen `term_conflict` werd gerapporteerd. V3.2 beperkt `_start_event` tot het eerste kern-zelfstandignaamwoord via een stop-lijst van voorzetsels en werkwoorden. Daarnaast zijn `schemas/README.md` en `scripts/README.md` toegevoegd (V3-002), een nieuwe `tests/test_v32_regressions.py` bewaakt de bugfix, en `RELEASE-LOG-V3.2.md` documenteert per bestand wat is gewijzigd. Geen van de runtime-API's is gewijzigd; bestaande v3.1-runs blijven geldig.

## 0.4.1 - v3.1 - 2026-09-08

Deterministische analyzer aangescherpt na technische tegenlezing. Contextbevestiging herberekent het CE-jaar atomair. Artikelherkenning negeert losse jaartallen en datums. Termijn- en procedure-registers bewaren actie, actor en procedurefase, waardoor advisering/besluitvorming en indien-/beslistermijnen niet meer ten onrechte botsen. Externe artikelverwijzingen vereisen een benoemde bron. Bronpoort draait nu in de runtime, terwijl semantische evidence-validatie nog fail-closed ontbreekt. Review, notities, wijzigingsset en eerste auditflow zijn toegevoegd. Bestandsinhoud wordt gecontroleerd. AI blijft volledig uitgeschakeld.


## 0.3.0 - 2026-09-07

Volledige v2 na vergelijking met alle 34 bestanden uit v1. De bronlaag is geconsolideerd, bronstatussen zijn expliciet gemaakt, schema's en golden tests zijn aangescherpt en de huidige standalone HTML is toegevoegd. De oorspronkelijke v1 staat bytegelijk onder `archive/v1/`. Geen bron of regel is voor productie geactiveerd.

## 0.2 - 2026-09-07

Eerste broninhoud en HTML-prototype toegevoegd.

## 0.1

Oorspronkelijk ontwerp- en contractpakket.

## 0.4.0 - v3 - 2026-09-08

Eerste echte analyzer zonder AI. Toegevoegd: FastAPI-runtime, PDF/DOCX-parser, documentcheck, vijf deterministische registers, interne consistentie-engine, bronkandidaten, A-I-fasestatussen, expliciete no-AI/AI-toggle, lege AI-adapter, parser- en runtime-schema's, demo-documenten en nieuwe tests. `active_reviewed` is de actuele bronstatus in de actieve documentatie. Geen bron of rule is voor productie geactiveerd.
