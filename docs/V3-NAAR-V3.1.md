# Van v3 naar v3.1

V3 bewees dat de checker zonder AI kan draaien. De technische tegenlezing liet daarna vooral zien dat de deterministische registers nog te snel betekenis aan tekst gaven.

V3.1 verandert daarom niet de productrichting. De basis wordt preciezer.

## Aangepast

1. **Context als één bevestigd object**  
   Een aangepast schooljaar herberekent direct het examenjaar. Retrieval gebruikt daarna alleen de bevestigde context.

2. **Termijnregister met procedurebetekenis**  
   Naast getal en eenheid worden actie, actor, deadline-type en start-event bewaard. De analyzer vergelijkt alleen termijnen die aantoonbaar dezelfde stap beschrijven.

3. **Procedure- en rolregister**  
   Tekst wordt per clausule bekeken. `adviseert` en `besluit` zijn verschillende acties. Voor rolconflicten telt alleen dezelfde beslisactie.

4. **Conservatievere artikelherkenning**  
   Jaartallen en datums worden niet meer door een los begincijfer als artikel geclassificeerd.

5. **Expliciete verwijzingsscope**  
   Alleen benoemde bronnen als WVO, Uitvoeringsbesluit, Awb of WMS maken een verwijzing extern. Een los woord `wet` is onvoldoende.

6. **Bronpoort in de runtime**  
   Iedere geselecteerde bronkandidaat krijgt een echte `source_gate`-uitkomst. Fase I blijft `partial`, omdat nog niet wordt vastgesteld of het bronfragment de concrete schoolclaim inhoudelijk draagt.

7. **Review terug in de werkende runtime**  
   Reviewstatus, notities, eigen voorsteltekst, wijzigingsset en eerste auditregels zijn weer beschikbaar.

## Bewust niet gedaan

Geen AI toegevoegd. Geen conceptregel geactiveerd. Geen OCR, semantische evidence-validator of nieuwe juridische bronclaim toegevoegd.
