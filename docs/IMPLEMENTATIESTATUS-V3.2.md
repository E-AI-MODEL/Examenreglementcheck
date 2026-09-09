# Implementatiestatus v3.2 / 0.4.2

V3.2 is een kleine upgrade op v3.1. Eén bugfix in `_start_event` (registers), twee ontbrekende README's, en nieuwe regressietests. Status per onderdeel is ongewijzigd ten opzichte van v3.1, behalve waar expliciet aangegeven.

| Onderdeel | Status | Opmerking |
|---|---|---|
| Analyse zonder AI | **werkend** | Enige actieve modus |
| AI-toggle | **werkend als UI-contract** | `Met AI` disabled |
| DOCX-parser | **werkend** | Koppen, alinea's en tabellen |
| PDF-parser | **werkend voor tekst-PDF** | Pagina-ankers, nog geen OCR |
| Artikelherkenning | **aangescherpt (v3.1)** | Jaartallen/datums niet meer als artikel |
| Contextbevestiging | **werkend** | Schooljaar en CE-jaar atomair herberekend |
| Registers | **werkend, v3.2 verbeterd** | `_start_event` beperkt tot eerste kern-zelfstandignaamwoord |
| Termijnconflicten | **werkend, v3.2 verbeterd** | Herkansing-termijnconflicten worden nu gedetecteerd (was: gemist in v3.1) |
| Rolconflicten | **werkend, conservatiever (v3.1)** | Alleen dezelfde beslisactie; advies ≠ besluit |
| Interne verwijzingen | **werkend, aangescherpt (v3.1)** | Alleen benoemde externe bronnen maken een verwijzing extern |
| Bronretrieval | **eerste versie** | Jaar, schooljaar, scope, regime, schooltype indien beschikbaar, minimumscore |
| Bronpoort | **runtime actief** | Per kandidaat `eligible/reason` |
| Semantische evidence-validator | **niet gebouwd** | Daarom geen juridische `must` |
| Menselijke review | **werkend** | Status, notitie, eigen voorsteltekst |
| Wijzigingsset | **werkend** | Gebruiker selecteert findings |
| Audit | **eerste versie** | Parsing, context, analyse, review |
| OCR | **niet aangesloten** | Lage tekstdekking wordt gemarkeerd |
| Fase A | complete/partial | Extractie |
| Fase B | not_implemented | Formele volledigheid |
| Fase C | complete | Interne consistentie |
| Fase D | partial | Bronselectie, geen volledige actualiteitscontrole |
| Fase E | not_implemented | SE/CE |
| Fase F | not_implemented | Jurisprudentie |
| Fase G | not_implemented | Vergelijking |
| Fase H | not_implemented | Tegenlezing |
| Fase I | partial | Bronpoort wel, semantische evidence-validatie niet |
| Schema-README's | **toegevoegd (v3.2)** | `schemas/README.md` en `scripts/README.md` |
| Tests | **41 slagen (v3.2)** | 37 v3.1-tests + 4 nieuwe v3.2-regressietests |
| Release-log | **toegevoegd (v3.2)** | `RELEASE-LOG-V3.2.md` documenteert per bestand de wijzigingen |

V3.2 blijft een ontwikkelversie. De no-AI-basis is functioneel, de juridische analyzer nog niet.
