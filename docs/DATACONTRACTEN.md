# Datacontracten 0.3.0

De schema's beschrijven de transportvorm. Juridische juistheid volgt niet uit schema-validatie.

## Bronstatus

`retrieved_not_activated` betekent dat de bron in de werkset staat. Voor een toekomstige harde conclusie zijn minimaal nodig: `legal_review_status: approved`, `production_approved: true`, een actuele geldigheidscontrole en een passende regel.

## Regelstatus

Alle regels in `rules/candidates.json` staan op `draft`. Evidence verwijst naar fragment-ID's. Ontbrekende of niet-gevalideerde evidence leidt naar `human_review`.

## Finding

`severity` en `confidence` blijven apart. Een `must` vraagt bron- en rule-ID plus gevalideerde evidence. `suggested_action` is verplicht.

## Golden cases

Een testcase kan meerdere toegestane severity-uitkomsten bevatten via `allowed_severities`. Dat is geen geldige waarde voor een echte finding.
