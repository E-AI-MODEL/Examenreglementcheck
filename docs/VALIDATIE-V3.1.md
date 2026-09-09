# Validatie v3.1

De release is gecontroleerd met **37 Python-tests** en twee JavaScript-tests.

Nieuwe regressietests bewaken expliciet:

- geen artikelherkenning van schooljaar of datum;
- geen rolconflict tussen adviseren en beslissen;
- geen termijnconflict tussen indien- en beslistermijn;
- wél conflict bij twee verschillende termijnen voor dezelfde herkende indieningsstap;
- generiek `wet` maakt een interne artikelverwijzing niet extern;
- benoemde WVO-verwijzing wordt wel extern;
- bevestigd schooljaar herberekent het CE-jaar in run, document en confirmed context;
- bronpoort wordt in de runtime uitgevoerd;
- semantische evidence-validator blijft uit en `must` blijft geblokkeerd;
- nep-DOCX en nep-PDF worden op inhoud geweigerd;
- reviewstatus, notitie en wijzigingsset worden opgeslagen;
- een lokale run kan worden verwijderd.

De bestaande bron-, schema-, parser-, API- en no-AI-regressietests blijven eveneens draaien.

Uitvoeren:

```sh
python scripts/validate_all.py
```

Deze tests zijn geen juridisch keurmerk. Ze bewijzen ook niet dat iedere mogelijke PDF- of DOCX-layout goed wordt gelezen.
