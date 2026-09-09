# Implementatiestatus v3 / 0.4.0

| Onderdeel | Status | Opmerking |
|---|---|---|
| Analyse zonder AI | **werkend** | Standaard en enige actieve modus |
| AI-toggle | **werkend als UI-contract** | `Met AI` zichtbaar maar disabled |
| AI-adapter | **geraamte** | Geen provider, model of API-call |
| DOCX-parser | **werkend** | Koppen, alinea's, tabellen, stabiele ankers |
| PDF-parser | **werkend voor tekst-PDF** | Pagina-ankers en confidence |
| OCR | **niet aangesloten** | Lage tekstdekking wordt zichtbaar gemarkeerd |
| Documentcheck | **werkend** | Metadata en waarschuwingen vóór analyse |
| Role registry | **werkend** | Deterministische rolvermeldingen |
| Term registry | **werkend** | Termijnen met onderwerp en vindplaats |
| Definition registry | **werkend** | Expliciete definitiepatronen |
| Procedure registry | **eerste versie** | Besluit- en procedurezinnen |
| Cross-reference registry | **werkend** | Interne artikelverwijzingen; wetsverwijzingen apart behandeld |
| Interne termijnconflicten | **werkend** | `internal_conflict` |
| Interne rolconflicten | **werkend** | Met waarschuwing dat fase/mandaat kan verschillen |
| Definitiestrijd | **werkend** | `internal_conflict` |
| Kapotte interne verwijzing | **werkend** | `editorial` |
| Bronretrieval | **eerste deterministische versie** | Tokenoverlap + jaar/autoriteit/statusfilters |
| Volledige evidence-validator | **nog niet** | Bronpoort bestaat; semantische claimvalidatie niet |
| Juridische `must` | **geblokkeerd** | 0 bronnen/rules production-approved |
| Fase A | **complete/partial** | Extractie |
| Fase B | **not_implemented** | Formele volledigheid |
| Fase C | **complete** | Interne consistentie |
| Fase D | **complete** | Bronselectie / actualiteit |
| Fase E | **not_implemented** | SE/CE |
| Fase F | **not_implemented** | Jurisprudentie |
| Fase G | **not_implemented** | Vergelijking |
| Fase H | **not_implemented** | Tegenlezing |
| Fase I | **complete als blokkade** | Geen harde juridische finding zonder geactiveerde basis |

De runtime geeft een `partial` run wanneer niet alle A-I-fasen zijn geïmplementeerd. Dat voorkomt dat de UI een onvolledige controle als eindcontrole presenteert.
