# Validatie v3

De v3-runtime is getest met echte, lokaal gegenereerde DOCX- en PDF-bestanden.

De tests controleren onder meer:

- parseroutput tegen het documentschema;
- stabiele DOCX- en PDF-ankers;
- pagina-informatie voor PDF;
- vijf registers;
- termijnconflict;
- rolconflict;
- kapotte interne artikelverwijzing;
- onderscheid tussen interne verwijzing en verwijzing naar WVO;
- geen `must` uit de deterministische analyzer zolang bron/rules niet zijn geactiveerd;
- AI-adapter staat uit en weigert calls;
- API weigert `ai_mode=on`;
- alle 15 v2-regressietests blijven slagen.

Gebruik `python scripts/validate_all.py`. Een geslaagde testset is geen juridisch keurmerk en geen bewijs dat alle examenreglementen correct worden geparsed.
