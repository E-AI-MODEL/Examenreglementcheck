# Implementatiestatus v3.1 / 0.4.1

| Onderdeel | Status | Opmerking |
|---|---|---|
| Analyse zonder AI | **werkend** | Enige actieve modus |
| AI-toggle | **werkend als UI-contract** | `Met AI` disabled |
| DOCX-parser | **werkend** | Koppen, alinea's en tabellen |
| PDF-parser | **werkend voor tekst-PDF** | Pagina-ankers, nog geen OCR |
| Artikelherkenning | **aangescherpt** | Jaartallen/datums niet meer als artikel |
| Contextbevestiging | **werkend** | Schooljaar en CE-jaar atomair herberekend |
| Registers | **werkend, v2-model** | Actie, actor, procedurefase en start_event toegevoegd |
| Termijnconflicten | **werkend, conservatiever** | Alleen dezelfde herkenbare procedurestap |
| Rolconflicten | **werkend, conservatiever** | Alleen dezelfde beslisactie; advies ≠ besluit |
| Interne verwijzingen | **werkend, aangescherpt** | Alleen benoemde externe bronnen maken een verwijzing extern |
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

V3.1 blijft een ontwikkelversie. De no-AI-basis is functioneel, de juridische analyzer nog niet.
