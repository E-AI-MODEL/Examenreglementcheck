# Implementatiestatus v3.3 / 0.5.0

| Onderdeel | Status | Begrenzing |
|---|---|---|
| No-AI-analyse | **werkend** | Enige actieve modus |
| DOCX / tekst-PDF | **werkend** | Lokale extractie met ankers |
| OCR-fallback | **werkend indien beschikbaar** | Vereist lokale `tesseract`; anders zichtbare partial parsing |
| A Extractie | **complete/partial** | Afhankelijk van extractiedekking |
| B Formele volledigheid | **complete** | Token-screening; mogelijk ontbreken blijft `human_review` |
| C Interne consistentie | **complete** | Registers, termijnen, rollen, definities, verwijzingen |
| D Actualiteit | **complete** | Geldigheid, jaar, fetchstatus en hash binnen snapshot; geen live web |
| E SE/CE | **out_of_scope** | Ook PTA-, rooster- en hulpmiddelenregels uitgesloten |
| F Jurisprudentie | **out_of_scope** | Geen rechtspraakselectie of -duiding |
| G Vergelijking | **complete** | Alleen lokale bronnotities; nooit juridisch bewijs |
| H Tegenlezing | **complete** | Duplicaten/evidence/partial-parsing/vergelijkingsveiligheid |
| I Evidence-validatie | **complete** | Herkomst, fragmenthash, bronpoort en conservatief tekstsignaal |
| Juridische `must` | **geblokkeerd** | Alle bron- en kandidaatregels zijn nog niet productiegoedgekeurd |
| Review/audit | **werkend** | UI herlaadt na opslaan zodat audit direct actueel is |
| Runbeheer | **werkend** | Lijst, hervatten en verwijderen in UI/API |
| Export | **werkend** | JSON en Markdown |
| Tests | **46 Python + 2 HTML** | Inclusief scope-, OCR-, export- en hard-stopregressies |

`complete` betekent uitsluitend dat alle controles binnen de gekozen productscope technisch zijn uitgevoerd. De tool geeft geen juridisch keurmerk. `production_ready=false` blijft gelden totdat bronnen en regels onafhankelijk zijn beoordeeld en geactiveerd.
