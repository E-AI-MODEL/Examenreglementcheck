# Bronnenpakket examenreglement-checker

Versie 0.2 · peildatum 7 september 2026 · schooljaar 2026-2027 · examenjaar CE 2027.

Er is nu inhoud beschikbaar om de checker verder te bouwen: volledige relevante wetsartikelen, officiële CE-publicaties, vier volledige uitspraken met afgebakende gevolgtrekkingen, en samenvattingen van professionele handreikingen en schoolvoorbeelden. Het pakket bevat 40 bronrecords. Daarvan zijn 38 opgehaald; twee volledige LKC-adviezen waren niet bereikbaar. De 38 omvatten ook verwijspagina’s en aanvullende versies, dus geen 38 zelfstandige normdocumenten.

Er zijn 109 volledige artikelpassages en 40 conceptcontrolepunten opgenomen. De bronrecords staan nog niet op actief voor productie. Ophalen, technische controle, inhoudelijke vergelijking en onafhankelijke juridische goedkeuring zijn afzonderlijke stappen.

## Bestanden gebruiken

- `examenreglement-checker-met-bronnen.html`: zelfstandig bestand. Open het in een browser. Onder Bronnen staan de echte broninhoud en conceptcontroles. Bevindingen en documentanalyse blijven een afzonderlijke demo.
- `sources/registry.json`: bronsoort, URL, datum, status, samenvatting, bestandspad en controlehash per bron.
- `sources/fragments.json`: 109 relevante volledige wetsartikelen, met anker, bron-URL en teksthash.
- `sources/content/`: wetsartikelen, uitspraakteksten, officiële publicaties en korte inhoudelijke bronbeschrijvingen.
- `sources/originals/`: opgehaalde officiële wetsteksten, uitspraken en andere overheidsdocumenten. De originele VO-raad- en schooldocumenten zijn via hun directe bronlinks te openen; ze zijn niet integraal heruitgegeven.
- `rules/candidates.json`: 40 conceptcontrolepunten met toepasselijkheid, beperkingen en bronkoppelingen.
- `sources/jurisprudence.normalized.json`: vier zaken met beslissing, vindplaatsen, toegestane en niet-toegestane gevolgtrekkingen.
- `docs/BRONNENOVERZICHT.md`: dekking per bronrecord.
- `docs/OPEN-PUNTEN.md`: wat nog ontbreekt of aanvullende beoordeling vraagt.
- `scripts/source_gate.py`: blokkeert gebruik van niet-goedgekeurde of niet-onderbouwde regels voor harde conclusies.
- `tests/test_source_pack.py`: controles op schema’s, hashes, bronverwijzingen en blokkades.

## Inhoudelijke aanvullingen

**Inhalen bij ziekte of overmacht.** WVO 2.60 lid 1 onder c noemt in de opgehaalde versie uitdrukkelijk een inhaalmogelijkheid voor een kandidaat die wegens ziekte of een bijzondere onafhankelijke omstandigheid een SE-toets niet kon maken. Een bepaling over een gemiste herkansing moet worden beoordeeld met onderscheid tussen eerste afname en herkansing. Het LKC-advies uit 2025 mag deze actuele wetsbepaling niet vervangen.

**Afsluiting schoolexamen.** De actuele WVO 2.55 lid 2 spreekt over het schoolexamen, zonder beperking tot vakken met een CE. Lid 3 en 4 en Uitvoeringsbesluit 3.12 bevatten relevante uitzonderingen. Het pakket bevat de huidige tekst. De precieze historische ingangsdatum van deze afzonderlijke wetswijziging is niet onafhankelijk gereconstrueerd.

**Rechtsroute.** WVO 2.63 en 2.64 zijn afzonderlijk opgenomen. Beide noemen vijf dagen, maar het type beslissing en de procedure verschillen. Een gewone cijferdiscussie krijgt niet automatisch de beroepstermijn voor een maatregel.

**Fraudevermoeden.** RBAMS 2020:3552 bespreekt in overwegingen 23-30 wél de onderbouwing van fraudebeschuldigingen. De voorzieningenrechter had twijfels, maar wees de voorziening om andere redenen af. De oude beschrijving in het startpakket was op dit punt te beperkt. De zaak speelt onder het oude regime en de bijzondere examenregels van 2020.

**AI in een uitspraak.** In RBOVE 2026:2055 staat een AI-bepaling in de geciteerde reglementsbijlage. De rechter beoordeelde medische onderbouwing, verzuim en afronding. Die uitspraak is geen inhoudelijke goedkeuring van een AI-frauderegel.

**Status schoolvoorbeelden.** Het Regius-document voor havo/vwo staat als concept gepubliceerd. STC vermeldt een voorbehoud van instemming en bevat lege datumvelden. RSG Ter Apel havo/vwo noemt vaststelling op 27 augustus en MR-instemming op 2 september 2026. Deze statussen zijn vastgelegd zoals de bronnen ze vermelden, zonder de besluitvorming onafhankelijk te controleren.

## Grenzen van deze versie

De tool kan met deze inhoud nog niet zelfstandig een volledige controle uitvoeren. De documentparser, volledige analyse-engine en bewijsvalidatie bij een concrete schooltekst ontbreken. De bestaande golden cases uit het startpakket zijn behouden als specificaties; er is geen werkende analyzer die daarop een inhoudelijke regressietest kan draaien. De nieuwe tests valideren het bronnenpakket en de blokkades, niet de uitkomst van een juridische analyse.
