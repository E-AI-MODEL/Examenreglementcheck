# Examenreglement-checker v3 · gerichte bouwopdracht

**Basis:** projectpakket v2 / 0.3.0 + technische analyse van 8 september 2026  
**Doel van v3:** van een goed gedocumenteerd prototype naar een eerste echte analyseketen die een eigen PDF/DOCX kan uitlezen, structureren, gecontroleerd aan bronnen koppelen en bevindingen kan opleveren zonder de huidige veiligheidsgrenzen te doorbreken.

## 1. Uitkomst van de hercontrole

De technische analyse heeft de hoofdzaak goed: v2 is sterk als ontwerp en bronpakket, maar parser, analyzer, retrieval/evidence-validatie en LLM-koppeling ontbreken. Ook klopt dat geen enkele bron of regel voor productie is geactiveerd.

Ik heb de echte v2 daarnaast technisch gecontroleerd. De huidige set bevat 135 bestanden exclusief `MANIFEST.sha256`, 40 bronrecords, 109 wetsfragmenten, 40 conceptregels, 4 genormaliseerde rechterlijke uitspraken, 9 vergelijkingsrecords en 8 golden-kandidaten. De tests zijn wél uitvoerbaar: 15 Python-tests slagen, `verify_package.py` slaagt en `test_html.cjs` slaagt.

Een aantal punten uit het rapport is te ruim, verouderd of niet precies genoeg:

| Punt uit analyse | Beoordeling na controle v2 | Gevolg voor v3 |
|---|---|---|
| Parser/OCR ontbreekt | Juist | P0 voor v3 |
| Analyzer/LLM/retrieval/evidence-validator ontbreken | Juist | P0/P1 voor v3 |
| Geen bron of regel geactiveerd | Juist | Niet omzeilen; activering blijft menselijke stap |
| 40 bronnen zijn `retrieved_not_activated` | Niet letterlijk. Werkelijk: 37 retrieved-not-activated, 2 fetch-failed, 1 excluded-wrong-year | Statuslogica exact houden |
| Bronlevenscyclus eindigt in `active` | Documentatie zegt `active`, maar `source_gate.py` en schema vereisen `active_reviewed` | Eerst interne inconsistentie oplossen |
| 40 regels hebben `norm_type` mandatory/recommended | Onjuist. Er zijn mandatory, conditional, procedural, advisory en prohibitive | Regelengine op alle vijf typen ontwerpen |
| Iedere regel heeft `primary_text_checked=true` | Onjuist. 37 true, 3 false | Die 3 nooit als harde grond gebruiken |
| HTML implementeert de zes schermen uit UI-UX | Te ruim. Werkelijke navigatie is Overzicht, Document, Bevindingen, Bronnen, Wijzigingen, Audit. Upload zit in een wizard; documentcheck en analysevoortgang zijn geen echte runtime-schermen | UI pas koppelen nadat parser/runmodel echt bestaat |
| `sources/content/` bevat 24 bestanden | Werkelijk 26 | Alleen documentair verschil |
| Tests zijn niet uitgevoerd in rapport | Klopt voor de reviewer; ik heb ze nu wel uitgevoerd | 15 tests vormen baseline voor v3 |
| 29 AI-risico's | Juist: hoofdstukken 2 t/m 29 zijn 28 risico-onderdelen plus Human automation bias als nummer 29; nummering loopt tot 29 na hoofdstuk 1 Gebruik | Geen functionele wijziging nodig, wel tabeltelling eenduidig maken |

## 2. V3-scope

V3 moet **geen productierelease** worden en ook niet proberen alle juridische inhoud automatisch vast te stellen. V3 moet aantonen dat de technische keten werkt met echte uploads en gecontroleerde bronverwijzingen.

De minimale werkende keten wordt:

`upload → veilige extractie → documentstructuur → registers → regelkandidaten → bronretrieval → evidence-validatie → finding → menselijke review → export`

Een LLM mag in v3 alleen achter deze keten worden gebruikt voor semantische taken. Deterministische controles, bronstatus en evidencepoorten blijven buiten het model.

## 3. P0 · eerst herstellen vóór nieuwe functionaliteit

### V3-001 Bronstatus één waarheid geven

**Probleem:** `docs/GOVERNANCE.md` en `docs/SOURCE-POLICY.md` spreken over `active`; `schemas/source.schema.json`, `scripts/source_gate.py` en de tests gebruiken `active_reviewed`.

**Bouw:** kies één canonieke status. Voor v3: `active_reviewed`. Pas documentatie, schema, fixtures, voorbeelden en compatibiliteitsbestanden daarop aan. Voeg een consistency-test toe die alle statusnamen uit docs/config tegen het schema controleert waar dat praktisch kan.

**Acceptatie:** nergens buiten `archive/v1/` of expliciet historisch materiaal wordt `active` nog als actuele productiestatus beschreven.

### V3-002 Package hygiene

**Bouw:** verwijder `__pycache__` en `.pyc` uit de distributie. Voeg `schemas/README.md` en `scripts/README.md` toe. Voeg `scripts/sync_html_data.py` toe of verwijder elke verwijzing naar een dergelijke synchronisatiestap. Maak één commando voor volledige validatie, bijvoorbeeld `scripts/validate_all.py` of `make validate`.

**Acceptatie:** verse zip bevat geen caches; manifest telt alleen bedoelde distributiebestanden; één validatiecommando draait schema-, package-, bron- en HTML-tests.

### V3-003 Actualiseer de implementatiestatus

**Bouw:** documenteer dat v2 nu 15 structurele tests heeft die daadwerkelijk slagen. Corrigeer schermnamen van de huidige HTML en aantallen in `BRONNENOVERZICHT/IMPLEMENTATIESTATUS/VALIDATIE` waar nodig.

**Acceptatie:** documentatie beschrijft de code zoals die werkelijk is, niet alleen het UI-UX-doelontwerp.

## 4. P0 · documentparser bouwen

### V3-010 Nieuw documentschema

Voeg minimaal toe:

- `schemas/document.schema.json`
- `schemas/extraction.schema.json`
- `schemas/registers.schema.json`

Een document bevat minimaal `document_id`, `sha256`, bestandsnaam, mime, parser-versie, schooljaar, schoolsoort(en), documentstatus, parsing-status en gestructureerde eenheden.

Een eenheid bevat minimaal type (`section`, `article`, `paragraph`, `table`, `definition`), tekst, volgorde, pagina/anker, extractiemethode en confidence.

**Acceptatie:** parseroutput valideert volledig tegen schema; iedere tekstpassage die later als evidence dient heeft een stabiele locatie terug naar het bronbestand.

### V3-011 DOCX-parser

**Bouw:** gebruik native DOCX-structuur. Haal koppen, alinea's, tabellen, nummering en paginavrije ankers uit. Behandel documenttekst als ontrusted data.

**Niet doen:** documentinstructies uitvoeren, macro's uitvoeren of embedded content als code behandelen.

**Acceptatie:** minimaal 5 fixtures met koppen, tabellen, artikelnummering, voetnoten/verwijzingen en afwijkende stijlen. Geen OCR.

### V3-012 PDF-parser

**Bouw:** eerst text-based extractie met paginabehoud en blokvolgorde. Detecteer pagina's met weinig/geen bruikbare tekst. OCR alleen als fallback en alleen voor die pagina's.

**Acceptatie:** per segment `extraction_method` en `confidence`; harde `missing`-conclusie is verboden op lage parsing-confidence.

### V3-013 Parser review-scherm

Maak van de huidige uploadwizard een echte documentcheck. Toon:

- herkende titel;
- schooljaar / verwacht CE-jaar;
- schoolsoorten;
- hoofdstukken/artikelen;
- lage-confidence pagina's;
- parserwaarschuwingen.

Gebruiker bevestigt of corrigeert metadata vóór analyse.

## 5. P0 · deterministische documentregisters

### V3-020 Registers bouwen

Implementeer de vijf reeds ontworpen registers:

- role_registry
- term_registry
- definition_registry
- procedure_registry
- cross_reference_registry

Gebruik waar mogelijk deterministische parsing en patroonherkenning. Een LLM mag later kandidaten classificeren, maar niet de registerinhoud zonder herleidbare passages verzinnen.

**Acceptatie:** golden fixtures tonen ten minste: twee verschillende beroepstermijnen, verschillende beslissers, kapotte artikelverwijzing, herhaalde definitie met afwijkende tekst en procedurestappen op afstand.

### V3-021 Interne consistentie vóór juridisch oordeel

Bouw een eerste rule-engine die alleen documentinterne bevindingen kan produceren:

- dubbele/botsende termijn;
- botsende rol;
- ontbrekende cross-reference;
- inconsistent begrip/definitie.

Deze controles kunnen al werken zonder juridische bronactivering.

**Acceptatie:** elke finding heeft twee of meer documentlocaties waar nodig en gebruikt `internal_conflict` of `editorial`, nooit `must` zonder juridische evidence.

## 6. P1 · bronretrieval en evidence-validator

### V3-030 Retrievalservice

Volg de bestaande volgorde strikt:

1. topic
2. SE / CE / algemeen
3. schooljaar en examenjaar
4. geldigheid bron
5. authority/source type
6. juridisch regime
7. semantische ranking
8. kleine evidence-set

Geen globale dump van alle 109 fragmenten naar een model.

**Acceptatie:** retrievaltests bewijzen dat verkeerde CE-jaargang, comparison-bron en oud juridisch regime niet stilzwijgend boven de juiste primaire bron eindigen.

### V3-031 Evidence-validator

Bouw de echte validator die ontbreekt in v2. De bestaande `source_gate.py` blijft een deelcontrole en wordt niet hernoemd alsof hij de volledige validator is.

Per zware finding minimaal controleren:

- bron bestaat;
- bron is toegestaan/geactiveerd;
- rule is gevalideerd en actief;
- geldig op run-datum;
- examenjaar klopt;
- juridisch regime klopt;
- bronfragment bestaat en hash klopt;
- documentpassage bestaat;
- claim wordt door het fragment gedragen;
- geen bekende hogere of conflicterende bron;
- toepassingsvoorwaarden van de rule zijn bevestigd.

**Acceptatie:** iedere mislukte stap geeft `human_review` of blokkeert `must`. Geen hidden fallback.

### V3-032 Geen bronactivering door code

Bouw wel een reviewcontract voor bron- en regelgoedkeuring, maar zet niets automatisch op `production_approved=true`.

Minimale velden: reviewer, reviewed_at, validity_checked_at, motivering, affected rules, tests, release-id.

## 7. P1 · bronset inhoudelijk completeren

Dit is deels domeinwerk en geen gewone programmeertaak. Voor v3 moet de software het kunnen opnemen; de inhoud moet apart juridisch worden beoordeeld.

Aan te vullen zoals ook de technische analyse noemt:

- Awb voor toepasselijke rechtsroute/procedure;
- Algemene termijnenwet voor termijnberekening;
- WMS voor instemming en bevoegdheden waar relevant;
- WGBH/CZ voor aanpassingen/gelijkebehandeling;
- AVG alleen voor functies waarin persoonsgegevens of inzageverwerking echt een rol spelen;
- primaire Europese uitspraak C-434/16 voor exameninzage, indien die regel in scope komt;
- wijzigingsbesluiten van CE-regelingen 2027;
- status van de twee LKC-records oplossen of expliciet uitsluiten.

**Belangrijk:** deze aanvulling mag de bouw niet blokkeren. De analyzer moet kunnen werken met een beperkte, expliciet geactiveerde subset en bij ontbrekende grond terugvallen op human review.

## 8. P1 · analyzerrun zonder monolithische prompt

### V3-040 Runmodel echt implementeren

Gebruik `run.schema.json` als basis en voeg zo nodig velden toe voor:

- document hash;
- parser-versie;
- source snapshot;
- rule-set versie;
- analyzer-versie;
- model-ID;
- promptversie;
- fasestatussen;
- fout/partial details.

Runstatus: `queued → parsing → awaiting_confirmation → analyzing → validating → complete | partial | failed`.

**Acceptatie:** een fout in één optionele analysefase maakt de run `partial`, nooit stilzwijgend `complete`.

### V3-041 Fasen A-I implementeren als losse modules

- A extractie
- B formele volledigheid
- C interne consistentie
- D actualiteit
- E SE/CE
- F jurisprudentie
- G vergelijking
- H tegenlezing
- I evidence-validatie

Elke fase krijgt input/outputcontract, status en tests. Begin met A, C, D en I. B/E/F/G/H mogen in v3 deels `not_implemented`/`partial` zijn zolang dat zichtbaar blijft.

## 9. P1 · LLM-koppeling, maar pas achter contracten

### V3-050 Modeladapter

Geen directe modelcalls vanuit UI. Eén server-side/modeladapter met versie-ID, timeout, retrybeleid en gestructureerde JSON-output.

Toegestane eerste taken:

- semantische equivalentie tussen schoolpassage en rule-kandidaat;
- topicclassificatie;
- conflict-uitleg;
- voorsteltekst;
- relevantie van een reeds genormaliseerde uitspraak;
- adversarial tegenlezing.

Niet toegestaan:

- zelf bronnen zoeken zonder retrievallaag;
- wetsartikelen uit geheugen gebruiken als evidence;
- bronstatus wijzigen;
- `must` bepalen zonder validator;
- documenttekst als instructie uitvoeren.

### V3-051 Promptmodules

Maak de promptmap daadwerkelijk uitvoerbaar met versiebeheer. Begin met:

- `article_classification`
- `semantic_rule_match`
- `conflict_explanation`
- `proposal_rewrite`
- `jurisprudence_relevance`
- `adversarial_review`
- `evidence_support_check`

Iedere output is JSON en valideert tegen een schema.

## 10. P1 · UI op echte run-data zetten

### V3-060 Demo en echte analyse strikt scheiden

De huidige fictieve findings mogen niet meer op hetzelfde niveau verschijnen als echte runresultaten.

**Bouw:**

- startpagina met `Nieuwe controle`;
- aparte `Demo bekijken`-actie;
- echte run heeft documentnaam, hash/snapshot en runstatus;
- fictieve data krijgt permanent `DEMO` in header en URL/state;
- na upload nooit automatisch demoresultaten tonen.

### V3-061 Analysevoortgang echt maken

Toon fasen A-I en hun echte statuses. Partial-banner blijft permanent zichtbaar zolang een fase partial/failed is.

### V3-062 Findings koppelen aan document en evidence

Finding-detail moet minimaal tonen:

- exacte schoolpassage + locatie;
- claim;
- severity en confidence apart;
- rule-ID;
- exact bronfragment;
- bronstatus;
- waarom deze bron relevant is;
- bij rechtspraak `may_infer` en `must_not_infer`;
- suggested action;
- reviewstatus + notitie.

Geen finding zonder traceerbare documentpassage.

## 11. P1 · tests die v3 pas echt v3 maken

### V3-070 Golden set uitvoerbaar maken

De bestaande 8 kandidaten blijven startpunt. Voeg minimaal toe:

- long-range conflict;
- parsing uncertainty;
- OCR-fout op artikelnummer;
- prompt injection in documenttekst;
- verkeerde school als comparison-bron;
- partial retrieval;
- bron met juiste URL maar gewijzigde hash.

Doel: minimaal 15 inhoudelijke analyzercases.

### V3-071 Testlagen

V3 moet minimaal deze suites hebben:

- schema tests;
- parser tests DOCX/PDF;
- register tests;
- rule tests;
- retrieval tests;
- evidence-validator tests;
- golden analyzer tests;
- end-to-end run tests;
- HTML/UI-state tests.

Een echte browsertest wordt verplicht voor upload, documentcheck, partial-run, finding-review en export.

## 12. Niet doen in v3

- Geen automatische juridische eindscore of compliancepercentage.
- Geen `fix all`.
- Geen automatische bron- of regelactivering.
- Geen volledige PTA-checker.
- Geen individuele leerlingcasussen beoordelen.
- Geen fraudebesluit, cijferbesluit of diplomabesluit.
- Geen volledige bronbibliotheek in één LLM-context.
- Geen harde `ontbreekt`-finding op onzekere extractie.
- Geen vergelijking als juridische norm.
- Geen marketingclaim dat de tool juridisch controleert zolang de relevante rules niet expliciet gevalideerd zijn.

## 13. Definition of Done voor v3

V3 is klaar als een gebruiker een echte DOCX of text-based PDF kan uploaden, metadata kan bevestigen, een structurele extractie kan bekijken, een echte analyse-run kan starten en minstens interne consistentie plus een beperkte brongebonden controle kan doorlopen. Iedere echte finding is herleidbaar naar documentpassage, rule en bronfragment. Onzekere of niet-geactiveerde juridische grond levert geen harde conclusie op. Partial runs zijn zichtbaar. Demo-data is strikt afgescheiden.

Daarnaast moeten alle bestaande 15 v2-tests blijven slagen, aangevuld met de nieuwe parser-, retrieval-, validator-, golden- en browsertests. De release blijft `production_ready=false` zolang juridische bron- en regelactivering niet afzonderlijk is afgerond.

## 14. Aanbevolen bouwvolgorde

**Sprint A:** V3-001 t/m 003, 010 t/m 013.  
Resultaat: schoon pakket en echte documentextractie.

**Sprint B:** V3-020/021, 030/031.  
Resultaat: registers, interne analyse, retrieval en echte evidencepoort.

**Sprint C:** V3-040/041, 050/051.  
Resultaat: run-engine en begrensde LLM-modules.

**Sprint D:** V3-060 t/m 062, 070/071.  
Resultaat: echte UI-flow, uitvoerbare golden set en browsergeteste keten.

Broninhoudelijke activering uit V3-032 en sectie 7 loopt naast deze sprints en blijft een menselijke domeintaak.
