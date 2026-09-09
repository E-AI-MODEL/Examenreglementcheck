# schemas/ — JSON-schema's voor datacontracten

Dit dossier bevat alle JSON-schema's die de datacontracten tussen parser, analyzer, evidence validator en UI vastleggen. Iedere schema valideert met `jsonschema` Draft 2020-12.

## Overzicht

| Schema | Doel | Status |
|---|---|---|
| `document.schema.json` | Output van `app/parser.py` (document, units, warnings) | werkend sinds v3 |
| `extraction.schema.json` | Eenheid (unit) in een document | werkend sinds v3 |
| `registers.schema.json` | De vijf deterministische registers | werkend sinds v3 |
| `finding.schema.json` | Bevinding (finding) van de analyzer; dwingt must+evidence af via allOf | sinds v1 |
| `rule.schema.json` | Controleerbare norm uit `rules/candidates.json` | sinds v1 |
| `source.schema.json` | Bronrecord uit `sources/registry.json` | sinds v1 |
| `jurisprudence.schema.json` | Genormaliseerde rechtszaak | sinds v1 |
| `comparison.schema.json` | Vergelijkingsschool-record | sinds v1 |
| `run.schema.json` | Volledige analyserun-JSON | sinds v1 |
| `fragment.schema.json` | Artikelpassage uit `sources/fragments.json` | sinds v2 |
| `golden.schema.json` | Testverwachting uit `tests/golden/` | sinds v2 |

## Gebruik

Schema's worden in tests geladen en gevalideerd met:

```python
from jsonschema import Draft202012Validator, RefResolver
schema = json.loads((ROOT / 'schemas/document.schema.json').read_text())
resolver = RefResolver(base_uri=(ROOT / 'schemas/').as_uri() + '/', referrer=schema)
Draft202012Validator(schema, resolver=resolver).validate(document)
```

## Toevoegen of wijzigen

- Bump de pakketversie in `manifest.json` en `CHANGELOG.md`.
- Voeg een regressietest toe in `tests/test_*_consistency.py` als een veld wordt toegevoegd of een enum wordt aangescherpt.
- Houd `additionalProperties: true` alleen waar runtime-velden vrij mogen meekomen; elders `false`.
