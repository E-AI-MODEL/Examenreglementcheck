# ARCHITECTURE.md

## Status v3.1 / 0.4.1

V3.1 heeft een werkende deterministische runtime zonder AI. PDF/DOCX-extractie, contextbevestiging, vijf rijkere registers, conservatievere interne consistentie, gefilterde bronkandidaten, de bronpoort en menselijke review zijn gebouwd. De AI-modus is alleen een uitgeschakeld geraamte. B/E/F/G/H, OCR en de semantische evidence-validator zijn nog niet gebouwd. Raadpleeg `docs/IMPLEMENTATIESTATUS-V3.1.md` voor de actuele runtime.
> **Status 0.3.0:** De beschreven services zijn doelarchitectuur. De huidige levering is lokaal en bevat geen API, parser, retrievalservice of LLM-workers.

**Versie:** 0.1

# 1. Doel

De architectuur moet voorkomen dat een taalmodel zelfstandig een examenreglement “juridisch beoordeelt” vanuit één grote context.

De applicatie combineert:

- deterministische documentextractie;
- gestructureerde bronrecords;
- regelgestuurde controles;
- gerichte LLM-analyse;
- evidence-validatie;
- menselijke review;
- audit.

# 2. Componenten

```text
Browser
  |
  v
Application API
  |
  +--> Document service
  |      +--> parser
  |      +--> OCR fallback
  |      +--> structure extractor
  |
  +--> Analysis orchestrator
  |      +--> deterministic rule engine
  |      +--> LLM analysis workers
  |      +--> retrieval service
  |      +--> evidence validator
  |
  +--> Source service
  |      +--> source registry
  |      +--> rule records
  |      +--> jurisprudence
  |      +--> comparison material
  |
  +--> Review service
  |
  +--> Export service
  |
  +--> Audit service
```

# 3. Documentmodel

Na parsing wordt het document niet alleen als tekstblob opgeslagen.

Minimaal:

```text
Document
Section
Article
Paragraph
Table
Definition
Reference
RoleMention
TermMention
ProcedureStep
PageAnchor
```

Iedere eenheid bewaart een link naar de originele vindplaats.

# 4. Registers

Voor long-range analyse:

```text
role_registry
term_registry
definition_registry
procedure_registry
cross_reference_registry
```

Voorbeeld `term_registry`:

```json
{
  "beroep": [
    {
      "article": "N.5",
      "value": 2,
      "unit": "dagen",
      "start_event": "beslissing rector"
    },
    {
      "article": "N.6",
      "value": 5,
      "unit": "dagen",
      "start_event": "beslissing rector"
    }
  ]
}
```

Daarna kan deterministisch een mogelijk conflict worden aangemaakt. Het LLM helpt vervolgens met context en uitleg.

# 5. Bronnen

Bronnen bestaan uit meer dan embeddings.

Minimaal metadata:

- source ID;
- title;
- source type;
- authority class;
- binding status;
- URL;
- valid from;
- valid to;
- exam year;
- legal regime;
- retrieved at;
- reviewed at;
- status;
- content hash.

# 6. Rule records

Bindende en gecontroleerde normen worden vertaald naar een regelrecord.

Niet alle wetgeving hoeft in één keer te worden genormaliseerd.

Start met regels die rechtstreeks nodig zijn voor de examenreglement-checklist.

# 7. Retrieval

Retrievalvolgorde:

1. bepaal topic;
2. bepaal SE/CE/algemeen;
3. bepaal schooljaar/examenjaar;
4. filter geldige bronnen;
5. filter bronsoort;
6. filter juridisch regime;
7. pas semantische ranking toe;
8. lever kleine, relevante evidence-set.

Geen globale vectorsearch over alle bronnen zonder filters.

# 8. Analysefasen

## A. Extractie

Output:
- documentstructuur;
- parsing confidence;
- registers.

## B. Completeness

Output:
- checklist control records;
- aanwezig / gedeeltelijk / ontbreekt / onzeker.

## C. Interne consistentie

Output:
- conflicts tussen rollen, termijnen, definities en procedures.

## D. Actualiteit

Output:
- verouderde bronnen;
- verkeerde jaargangen;
- ingetrokken of vervangen begrippen.

## E. SE/CE

Output:
- onderwerp-specifieke findings.

## F. Jurisprudentie

Output:
- relevante cases met begrensde gevolgtrekking.

## G. Vergelijking

Output:
- voorbeeldverschillen, nooit bindende findings.

## H. Tegenlezing

Output:
- procedurele kwetsbaarheden.

## I. Evidence validation

Output:
- confirmed;
- downgraded;
- blocked;
- human review.

# 9. Evidence validator

Voor ieder zwaar oordeel:

- bestaat bron;
- is bron actief;
- juiste datum;
- juiste exam year;
- juiste context;
- ondersteunt passage claim;
- hogere bronconflicten;
- juridische status voldoende.

Een `must` finding wordt geblokkeerd wanneer validatie faalt.

# 10. Runmodel

Een analyse-run heeft eigen immutable context:

- input document hash;
- input metadata;
- source snapshot;
- rule set;
- modelversion;
- promptversion;
- parserversion;
- analyzer version.

Nieuwe bronversies veranderen een bestaande run niet.

# 11. Statussen

Run:

```text
queued
parsing
awaiting_confirmation
analyzing
validating
complete
partial
failed
```

Fase:

```text
not_started
running
complete
partial
failed
```

# 12. Finding lifecycle

```text
unreviewed
accepted
rejected
needs_legal_review
implemented
resolved
```

Analyse-severity staat los van menselijke lifecycle.

# 13. Securitygrens

Documentinhoud:

- is untrusted data;
- mag promptinstructies bevatten;
- krijgt nooit systeemstatus.

System/developer instructions blijven buiten user-controlled content.

# 14. Parsing

Voorkeur:

1. native DOCX-structuur;
2. text-based PDF;
3. layout extraction;
4. OCR alleen als fallback.

Bewaar parsing confidence per segment.

# 15. OCR-regel

Geen harde afwezigheidsconclusie op lage OCR-confidence.

Bij kritieke tekst:

- tweede extractiemethode;
- page image check;
- eventueel human review.

# 16. LLM-taken

LLM mag:

- bepalingen classificeren;
- semantische equivalentie herkennen;
- conflicten uitleggen;
- voorsteltekst maken;
- cases samenvatten binnen normalized case records.

LLM mag niet autonoom:

- juridisch gezag bepalen zonder metadata;
- geldigheidsdata verzinnen;
- wetstekst uit geheugen als primaire bron gebruiken;
- severity verhogen zonder evidence.

# 17. Promptarchitectuur

Geen monolithische prompt.

Aanbevolen promptmodules:

```text
document_classification
article_extraction
completeness_semantic_match
conflict_explanation
legal_issue_tagging
jurisprudence_relevance
proposal_rewrite
adversarial_review
evidence_check
```

Prompts worden versioned.

# 18. Provenance

Finding bewaart:

- document location;
- source IDs;
- rule IDs;
- case IDs;
- retrieval query metadata;
- model/prompt version;
- validator outcome;
- timestamps.

# 19. Opslag

Scheid:

- gebruikersdocumenten;
- source library;
- normalized records;
- run data;
- audit log.

Een bronupdate mag geen userdocument wijzigen.

# 20. API-grenzen

Nog geen definitieve endpointcontracten vastleggen.

Waarschijnlijke domeinen:

```text
/analyses
/documents
/findings
/sources
/reviews
/exports
/admin/sources
/admin/prompts
```

# 21. Export

Export wordt gegenereerd vanuit gestructureerde findings, niet uit chatgeschiedenis.

# 22. Teststrategie

Lagen:

- schema tests;
- parser tests;
- rule tests;
- retrieval tests;
- golden analyzer tests;
- evidence validator tests;
- end-to-end run tests;
- UI state tests.

# 23. MVP-techniek

Technologiekeuze is nog vrij.

Belangrijker dan frameworkkeuze:

- server-side secrets;
- betrouwbare documentparsing;
- gestructureerde database;
- source versioning;
- audit;
- testbare analyserondes.

# 24. Latere uitbreidingen

Mogelijk:

- volledige PTA-module;
- bron-update crawler;
- automatische diff tussen schooljaren;
- aparte casusmodule;
- ChatGPT Skill als alternatieve interface;
- koppeling aan documentmanagement.

Deze uitbreidingen mogen de bron- en findingcontracten niet doorbreken.
