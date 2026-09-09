# Examenreglement-checker

Een controleerbare webtool voor het analyseren van examenreglementen in het voortgezet onderwijs.

## Wat dit project bouwt

De applicatie helpt een school om een examenreglement te controleren op:

- actuele wet- en regelgeving;
- verplichte onderdelen;
- interne tegenstrijdigheden;
- rollen en bevoegdheden;
- termijnen en procedures;
- regels voor het schoolexamen (SE);
- regels voor het centraal examen (CE);
- relevante rechtspraak en officiële uitleg;
- bruikbare vergelijking met examenreglementen van andere scholen;
- concrete wijzigingsvoorstellen met herleidbare onderbouwing.

De tool geeft geen juridisch keurmerk. De uitkomst bestaat uit controleerbare bevindingen met bron, vindplaats, zekerheid, voorgestelde actie en menselijke reviewstatus.

## Primaire scope

Het **examenreglement** is het primaire onderzoeksobject.

Een PTA kan later als aparte module worden toegevoegd. In de eerste versie kan een PTA alleen als aanvullend document dienen voor gerichte kruiscontroles, bijvoorbeeld rond herkansingen of de inrichting van het schoolexamen.

De tool bestrijkt zowel SE als CE voor zover die onderwerpen in een examenreglement horen.

## Belangrijkste ontwerpregel

> Geen harde juridische conclusie zonder passende, actuele en herleidbare evidence.

## Projectstructuur

```text
.
├── README.md
├── AGENTS.md
├── CHANGELOG.md
├── .env.example
├── .gitignore
├── docs/
│   ├── PRODUCT.md
│   ├── UI-UX.md
│   ├── ARCHITECTURE.md
│   ├── GOVERNANCE.md
│   ├── AI-RISKS.md
│   ├── SOURCE-POLICY.md
│   ├── SOURCE-CATALOG.md
│   ├── GLOSSARY.md
│   └── DECISIONS.md
├── sources/
│   ├── README.md
│   ├── registry.yaml
│   └── jurisprudence.seed.json
├── schemas/
│   ├── source.schema.json
│   ├── rule.schema.json
│   ├── jurisprudence.schema.json
│   ├── comparison.schema.json
│   ├── finding.schema.json
│   └── run.schema.json
├── prompts/
│   └── README.md
└── tests/
    ├── README.md
    └── golden/
        ├── 001_wrong_appeal_term.json
        ├── 002_correct_appeal_term.json
        ├── 003_outdated_legal_basis.json
        ├── 004_exam_year_mismatch.json
        ├── 005_jurisprudence_overreach.json
        ├── 006_comparison_not_law.json
        ├── 007_internal_role_conflict.json
        └── 008_clean_negative_control.json
```

## Documenten lezen

Voor een nieuwe ontwikkelsessie:

1. Lees `AGENTS.md`.
2. Lees `docs/PRODUCT.md` voor doel, gebruiker en scope.
3. Lees `docs/DECISIONS.md` voor reeds genomen ontwerpbesluiten.
4. Lees alleen de aanvullende documentatie die voor de taak nodig is.
5. Wijzig analysegedrag niet zonder passende golden/regressietests.

## Waar staat wat?

| Bestand | Functie |
|---|---|
| `AGENTS.md` | Korte, leidende bouwinstructies voor AI-agents |
| `docs/PRODUCT.md` | Waartoe, doelgroep, output, happy flow en afbakening |
| `docs/UI-UX.md` | Informatiearchitectuur, schermen, interacties, states en UX-regels |
| `docs/ARCHITECTURE.md` | Technische opzet en dataflow |
| `docs/GOVERNANCE.md` | Eigenaarschap, releases, bron- en modelbeheer |
| `docs/AI-RISKS.md` | Bekende AI-risico's en verplichte technische tegenmaatregelen |
| `docs/SOURCE-POLICY.md` | Bronsoorten, autoriteit, geldigheid en jurisprudentiegebruik |
| `docs/SOURCE-CATALOG.md` | Menselijk leesbare startlijst met bronnen, URL's en gebruik |
| `docs/GLOSSARY.md` | Vaste terminologie |
| `docs/DECISIONS.md` | Vastgelegde ontwerpbesluiten |
| `sources/registry.yaml` | Machineleesbare startset van bronnen |
| `schemas/` | Contracten voor bronnen, regels, uitspraken, findings en runs |
| `tests/golden/` | Bekende positieve en negatieve testgevallen |

## Bouwvolgorde

1. bronbibliotheek en metadata;
2. schema's en validators;
3. golden set;
4. documentparser;
5. regelengine;
6. retrieval;
7. LLM-analyserondes;
8. evidence validator;
9. reviewinterface;
10. exports en audit;
11. release- en updateproces.

Begin niet met een generieke chatinterface.

## MVP

De eerste versie ondersteunt minimaal:

- upload van DOCX en PDF;
- herkenning van hoofdstukken en artikelen;
- vaste controle op noodzakelijke onderdelen;
- WVO 2020 en Uitvoeringsbesluit WVO 2020 als primaire normlaag;
- controle op verouderde verwijzingen;
- interne consistentie;
- rol-, termijn- en procedurecontrole;
- SE/CE-classificatie;
- een kleine gevalideerde jurisprudentieset;
- evidence per relevante finding;
- menselijke reviewstatus;
- rapport- en auditexport.

## Geen SKILL.md in deze projectversie

Dit project is in eerste instantie een webapplicatie die met AI wordt gebouwd en AI gebruikt.

Een ChatGPT Skill is een mogelijke latere distributielaag, maar geen vereiste voor de applicatie. Er wordt daarom bewust nog geen `SKILL.md` opgenomen. Zie `docs/DECISIONS.md`.

## Status

Conceptbasis voor bouw en validatie. Juridische bronrecords en rules moeten vóór productie inhoudelijk worden gevalideerd.
