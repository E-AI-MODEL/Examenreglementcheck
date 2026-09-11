# Lokaal en met Docker draaien

V3 is een kleine lokale webapp. Python 3.11+ wordt aanbevolen.

```sh
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
python run.py
```

Open `http://127.0.0.1:8765`.

Test eerst met `examples/demo-reglement.docx`. Na upload zie je de documentcheck. Na bevestiging hoort de run `complete` te worden binnen de actieve productscope en meerdere bevindingen te tonen. Fasen E en F blijven zichtbaar `out_of_scope`.

## OCR

Voor gescande PDF's gebruikt de lokale installatie Tesseract als dat programma op het systeem staat:

```sh
# macOS met Homebrew
brew install tesseract tesseract-lang

# Debian/Ubuntu
sudo apt-get install tesseract-ocr tesseract-ocr-nld
```

Controleer de beschikbaarheid via `GET /api/health` onder het veld `ocr`. Zonder Tesseract blijven DOCX en tekst-PDF werken; een dunne scan wordt dan zichtbaar `partial`.

## Docker

De container bevat Tesseract en de Nederlandse taaldata:

```sh
docker build -t examenreglement-checker .
docker run --rm -p 8765:8765 examenreglement-checker
```

Open daarna `http://127.0.0.1:8765`.

Runs en uploads worden lokaal onder `runtime/` bewaard. Deze map hoort niet in versiebeheer of een release met gebruikersdata terecht te komen.

Voor validatie:

```sh
python scripts/validate_all.py
```

Dezelfde validatie draait automatisch op iedere push en pull request via GitHub Actions.
