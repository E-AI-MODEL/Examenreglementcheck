# API v3.3

De lokale runtime luistert standaard op `127.0.0.1:8765`.

## `GET /api/health`

Geeft pakketversie, analysemodus, AI-status, OCR-beschikbaarheid en de actieve/uitgesloten productscope.

## `POST /api/parse`

Multipart: `file`, `school_year`, `school_types`, `document_status`, `ai_mode=off`.

PDF/DOCX maximaal 20 MB. PDF-signature en DOCX-zipstructuur worden gecontroleerd. Een DOCX die tot meer dan 100 MB uitpakt wordt geweigerd. Dunne PDF-pagina's gaan door de optionele Tesseract-fallback; zonder lokale Tesseract wordt de parsing `partial` gemarkeerd.

## `POST /api/analyze/{run_id}`

Bevestigt de context als één object en voert fasen A, B, C, D, G, H en I uit. Een expliciete lege `school_types`-lijst geeft HTTP 422 en hergebruikt niet stilzwijgend een eerdere selectie. Fasen E (SE/CE) en F (jurisprudentie) hebben status `out_of_scope`.

## `GET /api/runs`

Geeft samenvattingen van lokaal opgeslagen runs, nieuwste eerst. Hiermee kan de browser een eerdere controle hervatten.

## `GET /api/runs/{run_id}`

Leest een volledige lokale run terug.

## `PATCH /api/runs/{run_id}/findings/{finding_id}`

Slaat `human_status`, `review_notes`, `in_change_set` en optioneel `suggested_text` op en voegt een auditregel toe.

## `GET /api/runs/{run_id}/changes`

Geeft de door de gebruiker geselecteerde wijzigingsset.

## `GET /api/runs/{run_id}/export`

Geeft een gestructureerde JSON-export met beslisnotitie, bevindingen, wijzigingslijst, bronverantwoording, scope en audit.

## `GET /api/runs/{run_id}/export.md`

Geeft hetzelfde controlerapport als downloadbaar Markdown-bestand.

## `DELETE /api/runs/{run_id}`

Verwijdert de run-JSON en het bijbehorende lokale uploadbestand.

## Veiligheidsgrens

`ai_mode` anders dan `off` geeft HTTP 409. Vergelijkingsmateriaal is geen evidence. Een regel kan alleen `must` ondersteunen als bronpoort, herkomst en inhoudelijk signaal slagen én bron/regel vooraf productiegoedgekeurd zijn; in de meegeleverde snapshot is dat laatste nergens het geval.
