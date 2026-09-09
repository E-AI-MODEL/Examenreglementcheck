# sources/

Deze map bevat de machineleesbare bronlaag.

## Bestanden

- `registry.yaml`: startregister van bronnen.
- `jurisprudence.seed.json`: eerste genormaliseerde jurisprudentierecords.

## Later

Aanbevolen structuur:

```text
sources/
├── registry.yaml
├── jurisprudence.seed.json
├── raw/
├── snapshots/
├── rules/
├── jurisprudence/
└── comparison/
```

## Belangrijk

- `raw/` is geen automatische ground truth.
- Een gevonden PDF wordt pas productief na metadata, validatie en status `active`.
- Vergelijkingsmateriaal blijft gescheiden van bindende bronnen.
- Jaargebonden CE-bronnen krijgen `exam_year`.
