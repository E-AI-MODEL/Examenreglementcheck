# API v3.1

De lokale runtime luistert standaard op `127.0.0.1:8765`.

## `GET /api/health`

Geeft pakketversie, actieve analysemodus en AI-status. `ai.available=false`.

## `POST /api/parse`

Multipart: `file`, `school_year`, `school_types`, `document_status`, `ai_mode=off`.

PDF/DOCX maximaal 20 MB. De extensie alleen is niet genoeg: PDF-signature en DOCX-zipstructuur worden gecontroleerd. Een DOCX die tot meer dan 100 MB uitpakt wordt geweigerd.

## `POST /api/analyze/{run_id}`

Bevestigt de context als één object. Een schooljaar zoals `2026-2027` zet ook `exam_year=2027`. De response bevat registers, documentinterne findings, bronkandidaten, bronpoortresultaten en A-I-fasestatussen.

## `PATCH /api/runs/{run_id}/findings/{finding_id}`

Slaat menselijke review op: `human_status`, `review_notes`, `in_change_set` en optioneel `suggested_text`.

## `GET /api/runs/{run_id}/changes`

Geeft de door de gebruiker geselecteerde wijzigingsset.

## `GET /api/runs/{run_id}`

Leest de lokale run terug.

## `DELETE /api/runs/{run_id}`

Verwijdert run-JSON en het bijbehorende lokale uploadbestand.

## AI-grens

`ai_mode` anders dan `off` geeft HTTP 409. Er is geen verborgen fallback naar een model.
