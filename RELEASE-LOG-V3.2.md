# RELEASE-LOG-V3.2

**Versie:** 0.4.2 (v3.2)
**Datum:** 8 september 2026
**Aanleiding:** Demo-run met `examples/demo-reglement.docx` toonde dat `_start_event` in `app/registers.py` te veel tekst extraheren, waardoor termijnconflicten voor dezelfde stap niet werden gedetecteerd.
**Aard:** Kleine upgrade. Eén bugfix, twee ontbrekende README's, nieuwe regressietests. Geen API-wijzigingen. Geen schema-wijzigingen. Volledig backward-compatibel met v3.1.

---

## Samenvatting wijzigingen

| Categorie | Aantal | Effect |
|---|---|---|
| Bugfix in broncode | 1 | `app/registers.py` — `_start_event` |
| Nieuwe broncode-tests | 1 bestand (4 tests) | `tests/test_v32_regressions.py` |
| Nieuwe documentatie | 2 | `schemas/README.md`, `scripts/README.md` |
| Bijgewerkte documentatie | 3 | `CHANGELOG.md`, `docs/V3.1-NAAR-V3.2.md`, `docs/IMPLEMENTATIESTATUS-V3.2.md` |
| Metadata bijgewerkt | 1 | `manifest.json` |
| Release-log | 1 | dit bestand |
| MANIFEST.sha256 | 1 | hergegenereerd |
| **Totaal gewijzigde of nieuwe bestanden** | **8** (plus `MANIFEST.sha256` en dit log) | |

**Verwijderde bestanden:** geen.
**Hernoemde bestanden:** geen.

---

## Per bestand

### 1. `app/registers.py` — bugfix

**Type:** bugfix in runtime-code
**Regels beïnvloed:** 77–94 (functie `_start_event`)
**Compatibiliteit:** geen API-wijziging; output-schema ongewijzigd; bestaande runs blijven geldig.

**Reden:**
De demo-run met `examples/demo-reglement.docx` leverde deze twee clausules:

1. `De kandidaat meldt zich binnen 3 schooldagen na publicatie aan voor de herkansing.`
2. `Aanmelden voor dezelfde herkansing kan tot 5 schooldagen na publicatie.`

V3.1 extraheren `start_event`:
- Clause 1 → `"publicatie aan voor de herkansing"`
- Clause 2 → `"publicatie"`

Daardoor verschillen `_term_key`-sleutels en wordt geen `term_conflict` gerapporteerd. De gebruiker ziet geen melding dat er 3 vs 5 schooldagen voor dezelfde stap staan.

**Wijziging:**
- `_start_event` beperkt nu tot het eerste kern-zelfstandignaamwoord via een stop-lijst van voorzetsels, werkwoorden en voegwoorden.
- Beide clausules krijgen nu `start_event = "publicatie"` → zelfde `_term_key` → `term_conflict` gerapporteerd.

**SHA-256:**
- v3.1 (voor): `68b0a3e76f1749edaa69b3d9847b5ad9a84ad0a0182a3f7ccf82950fd107e042`
- v3.2 (na):  `d9f98381c9d9f55101fd797a09a2245c72f9d36dde92a36a6a19a27107c0b041`

**Regressiebewaking:**
`tests/test_v32_regressions.py` — 4 nieuwe tests.

---

### 2. `tests/test_v32_regressions.py` — nieuw

**Type:** nieuw testbestand
**Aantal tests:** 4

| Test | Doel |
|---|---|
| `test_start_event_stops_at_function_word` | Verifieert dat "publicatie" wordt geëxtraheerd, niet "publicatie aan voor de herkansing" |
| `test_herkansing_term_conflict_with_different_values_is_detected` | Verifieert dat het demo-document nu een `term_conflict` finding oplevert |
| `test_start_event_handles_multiline_clause` | Edge-case met samengesteld zelfstandignaamwoord ("beslissing van de rector") |
| `test_start_event_returns_none_without_preposition` | Geen "na|vanaf|volgend op" → `None` |

**SHA-256 (v3.2):** `ff7b0971d95e66ca28be84d4aa25965add455ca02488a47366854e2e465f362a`

---

### 3. `schemas/README.md` — nieuw

**Type:** nieuwe documentatie
**Reden:** V3-bouwopdracht V3-002 noemde expliciet dat deze README ontbrak.

**Inhoud:** Overzicht van 11 JSON-schema's (document, extraction, registers, finding, rule, source, jurisprudence, comparison, run, fragment, golden) met per schema: doel, status, en gebruiksinstructie.

**SHA-256 (v3.2):** `ef6dff3fe8cb523e3fc01c19b73e7ad45437007434ef7bce3d628dfe51e01808`

---

### 4. `scripts/README.md` — nieuw

**Type:** nieuwe documentatie
**Reden:** V3-bouwopdracht V3-002 noemde expliciet dat deze README ontbrak.

**Inhoud:** Overzicht van 6 scripts (validate_all.py, verify_package.py, source_gate.py, sync_compat.py, test_html.cjs, test_v3_html.cjs) met per script: doel, aanroep, en opmerkingen. Beschrijft tevens de stappen die `validate_all.py` uitvoert.

**SHA-256 (v3.2):** `7fcfe6419dee1da4bda451e3e27ae8b575da8f3617e7693edaf25a87310a25fd`

---

### 5. `CHANGELOG.md` — bijgewerkt

**Type:** documentatie-update
**Wijziging:** Nieuwe 0.4.2-entry bovenaan toegevoegd. Oorspronkelijke 0.4.1-, 0.4.0-, 0.3.0-, 0.2- en 0.1-entries ongewijzigd.

**SHA-256:**
- v3.1 (voor): `dcab43875f1c319c61551d1d06601a24244166775aafcd94393c2df1b4f84d81`
- v3.2 (na):  `de1f4a72e3c233bb776a0edf87cdde2fc3cb97b025ff6045d708968a18e8fed1`

---

### 6. `manifest.json` — bijgewerkt

**Type:** metadata-update
**Wijzigingen:**

| Veld | v3.1 | v3.2 |
|---|---|---|
| `version` | `0.4.1` | `0.4.2` |
| `delivery` | `functional-v3.1-no-ai` | `functional-v3.2-no-ai` |
| `notes` | (5 entries over v3.1-reparaties) | (5 entries over v3.2-reparaties) |
| `distribution_files_excluding_manifest_sha256` | `175` | `178` |
| `tests_passed` | `37` | `41` |

**SHA-256:**
- v3.1 (voor): `59e3eea8ace39fb33b1a10cfcd2a68793a50194f06c493bc054024a676500aa8`
- v3.2 (na):  `a24d6daa9f468ad1248ad3c74c16423f787a02e79871af27cf759766537fa3e8`

---

### 7. `docs/V3.1-NAAR-V3.2.md` — nieuw

**Type:** nieuwe documentatie
**Inhoud:** Beschrijft de overgang van v3.1 naar v3.2: de demo-run die de bug aan het licht bracht, de `_start_event`-fix, de nieuwe README's, de nieuwe regressietests, compatibiliteit en validatie.

**SHA-256 (v3.2):** `9d47e1c59989f4368dab412da5ff0443926ec6a2b1e15e5fd8a643ef11bd4729`

---

### 8. `docs/IMPLEMENTATIESTATUS-V3.2.md` — nieuw

**Type:** nieuwe documentatie
**Inhoud:** Actuele implementatiestatus per onderdeel. Vervangt `IMPLEMENTATIESTATUS-V3.1.md` niet (dat bestand blijft als archief), maar is het leidende statusdocument voor v3.2. Belangrijkste wijzigingen ten opzichte van v3.1: termijnconflicten zijn nu werkend-verbeterd, schema-README's zijn toegevoegd, 41 tests slagen.

**SHA-256 (v3.2):** `563db9bde07c86bf751ac4a043a33dbbc8e870ee4952332c1aece54a62ad9ccc`

---

### 9. `RELEASE-LOG-V3.2.md` — nieuw (dit bestand)

**Type:** release-log
**Reden:** Gebruiker vroeg expliciet om een duidelijke log bij de levering.
**SHA-256 (v3.2):** wordt berekend na finalisatie.

---

### 10. `MANIFEST.sha256` — hergegenereerd

**Type:** package-integriteitsbestand
**Reden:** Bevat SHA-256-hashes van alle distributiebestanden. Moet worden hergegenereerd bij elke wijziging.
**Wijziging:** Alle hashes voor de 8 gewijzigde of nieuwe bestanden zijn bijgewerkt.

**SHA-256:**
- v3.1 (voor): `341393f9f248f70a17a4f1b70ee46336547a0c5dc90d054314182a08be162267`
- v3.2 (na):  wordt berekend na finalisatie.

---

## Validatie

```
$ python scripts/validate_all.py
[...]
----------------------------------------------------------------------
Ran 41 tests in 0.967s

OK
+ node scripts/test_html.cjs
PASS HTML logic and embedded source pack
+ node scripts/test_v3_html.cjs
PASS v3.1 HTML syntax, no-AI toggle, reviewflow and required views
PASS package hygiene and manifest
```

- **41 Python-tests slagen** (37 v3.1-tests + 4 nieuwe v3.2-regressietests)
- **2 JavaScript-tests slagen** (HTML-syntaxis v2 + v3.1)
- **Package-hygiëne OK** (geen caches in distributie, runtime leeg)
- **Manifest OK** (`production_ready=false`, no-AI geïmplementeerd, AI uitgeschakeld)

## Compatibiliteit

- API-endpoints ongewijzigd
- JSON-schema's ongewijzigd
- Manifest-structuur ongewijzigd (alleen versie en tellingen bijgewerkt)
- Bestaande v3.1-runs blijven leesbaar
- Bestaande v3.1-tests blijven slagen

## Wat niet is veranderd

- `app/server.py`, `app/parser.py`, `app/analyzer.py`, `app/retrieval.py`, `app/source_gate.py`, `app/ai_adapter.py`, `app/run_store.py`, `app/__init__.py`, `run.py` — ongewijzigd
- `web/index.html`, `examenreglement-checker*.html` — ongewijzigd
- `sources/`, `rules/`, `prompts/`, `examples/`, `archive/v1/` — ongewijzigd
- Alle 11 `schemas/*.json` — ongewijzigd
- Alle 8 `tests/golden/*.json` — ongewijzigd
- Overige `tests/*.py`, `scripts/*.py`, `scripts/*.cjs` — ongewijzigd
- Overige `docs/*.md` — ongewijzigd

## Productiestatus

`production_ready = false`
`analysis_modes.without_ai = implemented`
`analysis_modes.with_ai = skeleton_disabled`

V3.2 is nog steeds niet productierijp — bewust. De juridische MOET blijft geblokkeerd totdat de semantische evidence-validator is gebouwd en bron- en regelactivering door een juridisch domeinvalidator is uitgevoerd.
