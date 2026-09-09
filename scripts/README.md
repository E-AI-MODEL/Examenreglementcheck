# scripts/ — Hulp- en validatiescripts

Dit dossier bevat scripts voor bronsynchronisatie, package-hygiëne en validatie. Geen van deze scripts hoort in de runtime-route van de FastAPI-server.

## Overzicht

| Script | Doel | Aanroep |
|---|---|---|
| `validate_all.py` | Eén commando voor volledige validatie: unittests, HTML-tests, cache-cleanup, manifest-assert | `python scripts/validate_all.py` |
| `verify_package.py` | Package-integriteitscontrole (MANIFEST.sha256) | `python scripts/verify_package.py` |
| `source_gate.py` | Compatibiliteitsimport voor de canonieke runtime-poort in `app.source_gate` | wordt niet direct aangeroepen; bestaat voor legacy |
| `sync_compat.py` | Genereert `sources/registry.yaml` uit `sources/registry.json` (compatibiliteitskopie) | `python scripts/sync_compat.py` |
| `test_html.cjs` | JavaScript-syntaxischeck op `examenreglement-checker-met-bronnen.html` | `node scripts/test_html.cjs` |
| `test_v3_html.cjs` | JavaScript-syntaxischeck op `web/index.html` (v3-runtime-UI) | `node scripts/test_v3_html.cjs` |

## validate_all.py

Draait in volgorde:

1. `python -m unittest discover -s tests -p 'test_*.py' -v`
2. `node scripts/test_html.cjs`
3. `node scripts/test_v3_html.cjs`
4. Schoont `__pycache__`, `*.pyc` en runtime/uploads/runs weg
5. Controleert dat de distributie geen caches bevat
6. Asserteert manifest-waarden: `production_ready=false`, `analysis_modes.without_ai='implemented'`, `analysis_modes.with_ai='skeleton_disabled'`

## Toevoegen van een nieuw script

- Plaats het script in dit dossier.
- Voeg een regel toe aan deze README.
- Als het script in `validate_all.py` moet worden opgenomen, voeg dan een `run([...])`-call toe aan `scripts/validate_all.py`.
