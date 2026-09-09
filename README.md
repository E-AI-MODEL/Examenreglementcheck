# Examenreglement-checker v3.1

**Pakketversie 0.4.1 · deterministische analyzer zonder AI**

V3.1 leest een eigen PDF of DOCX uit en voert een echte lokale analyse uit. De actieve keten gebruikt geen AI. De UI toont wel **Zonder AI / Met AI**, maar `Met AI` blijft uitgeschakeld en de API weigert modelgebruik.

## Meteen starten

```sh
python -m pip install -r requirements.txt
python run.py
```

Open daarna `http://127.0.0.1:8765`. Op macOS kan ook `start-v3.1.command` worden gebruikt.

## Wat v3.1 nu doet

- PDF en DOCX uitlezen, met inhoudscontrole van het bestand;
- documentcheck met bevestiging van schooljaar, CE-jaar, schoolsoort en documentstatus;
- vijf registers voor rollen, termijnen, definities, procedures en verwijzingen;
- termijnen koppelen aan actie en procedurefase;
- rollen onderscheiden als actor, adviseur of andere betrokkene waar dit deterministisch herkenbaar is;
- interne termijn-, rol- en definitieconflicten vinden;
- kapotte interne artikelverwijzingen vinden;
- bronkandidaten selecteren op jaar, scope, regime en tekstoverlap;
- de echte bronpoort uitvoeren voor iedere bronkandidaat;
- juridische `must` blokkeren zolang semantische evidence-validatie ontbreekt;
- findings menselijk beoordelen, notities bewaren en een wijzigingsset opbouwen;
- auditregels voor parsing, contextbevestiging, analyse en review bewaren;
- runs lokaal verwijderen via de API.

## Belangrijkste v3.1-reparaties

V3.1 is gebouwd naar aanleiding van een technische tegenlezing van v3. Vier aantoonbare fouten zijn nu regressietests:

- `2026-2027` en `1 januari 2027` worden niet meer als artikelnummer gezien;
- `de examencommissie adviseert` en `de rector besluit` geeft geen rolconflict;
- `5 dagen om beroep in te stellen` en `2 weken om erop te beslissen` geeft geen termijnconflict;
- wijziging van schooljaar bij de documentcheck herberekent het CE-jaar atomair vóór retrieval.

Daarnaast wordt een generiek woord als `wet` niet meer genoeg geacht om een artikelverwijzing als extern te behandelen.

## Wat nog niet is gebouwd

OCR, volledige formele volledigheid, volledige SE/CE-controle, jurisprudentie-analyse, inhoudelijke vergelijking, tegenlezing en semantische evidence-validatie ontbreken nog. Fasen B, E, F, G en H blijven zichtbaar `not_implemented`. Fasen D en I zijn `partial` omdat daar slechts kandidaatselectie respectievelijk de bronpoort draait.

Geen bron of regel staat op `production_approved=true`. De tool geeft geen juridische conformiteitsverklaring.

## Architectuur

`upload → extractie → contextbevestiging → registers → interne consistentie → bronkandidaten → bronpoort → findings → menselijke review`

AI kan later alleen als optionele laag achter deze keten worden toegevoegd. De no-AI-route blijft zelfstandig.

## Valideren

```sh
python scripts/validate_all.py
python scripts/verify_package.py
```

De huidige release bevat **37 Python-tests** plus twee JavaScript/HTML-controles. Zie `docs/VALIDATIE-V3.1.md`.

## Productiestatus

`production_ready=false`.
