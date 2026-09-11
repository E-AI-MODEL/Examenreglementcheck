# Examenreglement-checker v3.3

**Pakketversie 0.5.1 · deterministische analyzer zonder AI**

V3.3 leest een PDF of DOCX en voert de afgesproken controleketen lokaal uit. SE/CE-controle en jurisprudentie-analyse zijn bewust buiten scope. De interface toont **Met AI** alleen als uitgeschakelde toekomstige optie; de API weigert modelgebruik.

## Starten

```sh
python -m pip install -r requirements.txt
python run.py
```

Open `http://127.0.0.1:8765`.

Voor een reproduceerbare installatie met werkende OCR:

```sh
docker build -t examenreglement-checker .
docker run --rm -p 8765:8765 examenreglement-checker
```

## Actieve keten

- DOCX- en tekst-PDF-extractie met stabiele vindplaatsen;
- optionele OCR-fallback voor dunne/gescande PDF-pagina's als Tesseract lokaal beschikbaar is;
- bevestiging van schooljaar, examenjaar, schoolsoort en documentstatus;
- formele volledigheidsscreening met menselijke hard stop bij mogelijke afwezigheid;
- vijf registers en documentinterne termijn-, rol-, definitie- en verwijzingscontroles;
- bronselectie en actualiteits-/integriteitscontrole binnen de opgeslagen snapshot;
- evidence-validatie op herkomst, bronpoort, fragmenthash en tekstsignaal;
- vergelijking met beschikbare schooldocumenten, altijd gelabeld als voorbeeld en nooit als juridisch bewijs;
- deterministische kritische tegenlezing die onbewezen `must`-oordelen afwaardeert;
- menselijke review, wijzigingsset en actueel auditlog;
- runs hervatten, verwijderen en als JSON of Markdown exporteren.

Een geslaagde run krijgt `complete` als alle controles **binnen deze productscope** zijn uitgevoerd. Dat is geen juridische goedkeuring. Alle kandidaatregels zijn nog concept en `production_approved=false`; juridische `must` blijft daarom fail-closed geblokkeerd.

## Buiten scope

- inhoudelijke SE/CE-controle (inclusief PTA-, rooster- en hulpmiddelenregels);
- jurisprudentie-analyse;
- live-webactualiteitscontrole;
- AI-analyse.

## Valideren

```sh
python -m unittest discover -s tests -v
node scripts/test_html.cjs
node scripts/test_v3_html.cjs
python scripts/verify_package.py
```

Zie `docs/IMPLEMENTATIESTATUS-V3.3.md`, `docs/API-V3.md` en `docs/RUN-LOCAL.md`. GitHub Actions voert dezelfde validatie automatisch uit. `production_ready=false` zolang de juridische bron- en regelset niet onafhankelijk is goedgekeurd.
