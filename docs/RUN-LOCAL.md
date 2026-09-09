# Lokaal draaien

V3 is een kleine lokale webapp. Python 3.11+ wordt aanbevolen.

```sh
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
python run.py
```

Open `http://127.0.0.1:8765`.

Test eerst met `examples/demo-reglement.docx`. Na upload zie je de documentcheck. Na bevestiging hoort de run `partial` te worden en meerdere documentinterne bevindingen te tonen.

Runs en uploads worden lokaal onder `runtime/` bewaard. Deze map hoort niet in versiebeheer of een release met gebruikersdata terecht te komen.

Voor validatie:

```sh
python scripts/validate_all.py
```
