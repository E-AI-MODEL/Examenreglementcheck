# Vergelijking met ontvangen zip v1

Alle 34 bestanden uit v1 zijn gecontroleerd. 31 actieve bestanden zijn aangepast; 3 konden inhoudelijk ongewijzigd blijven. De oorspronkelijke bytes staan onder `archive/v1/`.

| Bestand | V2 | Beoordeling |
|---|---|---|
| `.env.example` | aangepast | Aangepast: expliciet gemaakt dat de huidige HTML geen backend- of LLM-configuratie gebruikt. |
| `.gitignore` | ongewijzigd | Ongewijzigd: bestaande uitsluitingen blijven bruikbaar. |
| `AGENTS.md` | aangepast | Aangepast: actuele implementatiestatus, leidende bronbestanden en activeringsgrens toegevoegd. |
| `CHANGELOG.md` | aangepast | Aangepast: v0.2 en volledige v0.3-samenvoeging vastgelegd. |
| `FILES.md` | aangepast | Wordt opnieuw gegenereerd op basis van de definitieve inhoud. |
| `README.md` | aangepast | Aangepast: v2 als complete werkbasis en concrete startinstructies. |
| `docs/AI-RISKS.md` | aangepast | Aangepast: onderscheid tussen ontwerpmaatregelen en werkelijk gebouwde blokkades. |
| `docs/ARCHITECTURE.md` | aangepast | Aangepast: doelarchitectuur niet langer als gerealiseerd laten lezen. |
| `docs/DECISIONS.md` | aangepast | Aangepast: samenvoeging, canonieke bronset en golden-status vastgelegd. |
| `docs/GLOSSARY.md` | aangepast | Aangepast: nieuwe bron- en teststatussen toegevoegd. |
| `docs/GOVERNANCE.md` | aangepast | Aangepast: expliciete activering en reviewgrens. |
| `docs/PRODUCT.md` | aangepast | Aangepast: productdoel versus huidige implementatie gemarkeerd. |
| `docs/SOURCE-CATALOG.md` | aangepast | Aangepast: verwijzing naar machineleesbare actuele bronset. |
| `docs/SOURCE-POLICY.md` | aangepast | Aangepast: registry.json leidend en opgehaald is niet goedgekeurd. |
| `docs/UI-UX.md` | aangepast | Aangepast: huidige schermen en ontbrekende documentanalyse gemarkeerd. |
| `prompts/README.md` | aangepast | Aangepast: nog geen model- of promptuitvoering. |
| `schemas/comparison.schema.json` | ongewijzigd | Ongewijzigd: schema is bruikbaar voor de nieuwe vergelijkingrecords. |
| `schemas/finding.schema.json` | aangepast | Aangepast: suggested_action verplicht en must-evidence aangescherpt. |
| `schemas/jurisprudence.schema.json` | aangepast | Aangepast: reviewstatus, bronkoppeling en productiegoedkeuring opgenomen. |
| `schemas/rule.schema.json` | aangepast | Aangepast: evidence, production_approved en fallback naar human_review opgenomen. |
| `schemas/run.schema.json` | ongewijzigd | Ongewijzigd: blijft contract voor de nog te bouwen analyzer-run. |
| `schemas/source.schema.json` | aangepast | Aangepast: fetch-, review-, productie- en contentstatus toegevoegd. |
| `sources/README.md` | aangepast | Aangepast: canonieke bestanden en beperkingen beschreven. |
| `sources/jurisprudence.seed.json` | aangepast | Aangepast: gelijkgetrokken met de genormaliseerde werkrecords. |
| `sources/registry.yaml` | aangepast | Aangepast: gegenereerde compatibiliteitskopie van registry.json; oude active-statussen verwijderd. |
| `tests/README.md` | aangepast | Aangepast: onderscheid structurele tests en nog niet uitvoerbare analyzer-tests. |
| `tests/golden/001_wrong_appeal_term.json` | aangepast | Aangepast: toepasselijke maatregelroute expliciet gemaakt. |
| `tests/golden/002_correct_appeal_term.json` | aangepast | Aangepast: toepasselijke maatregelroute expliciet gemaakt. |
| `tests/golden/003_outdated_legal_basis.json` | aangepast | Aangepast: ongeldige samengestelde severity vervangen door allowed_severities. |
| `tests/golden/004_exam_year_mismatch.json` | aangepast | Aangepast: teststatus toegevoegd; oorspronkelijke verwachting behouden tenzij structureel ongeldig. |
| `tests/golden/005_jurisprudence_overreach.json` | aangepast | Aangepast: human_review als begrensde uitkomst en teststatus toegevoegd. |
| `tests/golden/006_comparison_not_law.json` | aangepast | Aangepast: teststatus toegevoegd; vergelijking blijft nooit juridische norm. |
| `tests/golden/007_internal_role_conflict.json` | aangepast | Aangepast: context toegevoegd om een echte interne rolbotsing te onderscheiden van mandaat/faseverschil. |
| `tests/golden/008_clean_negative_control.json` | aangepast | Aangepast: teststatus toegevoegd; blijft negatieve controle. |
