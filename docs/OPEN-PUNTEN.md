# Open punten vóór productie

- Alle 40 controlepunten staan op concept. Leg een menselijke beoordelaar, goedkeuringsdatum en gemotiveerd activeringsbesluit vast. Zet `production_approved` niet automatisch aan.
- Controleer de wijzigingshistorie van de twee CE-regelingen. De basispublicaties voor 2027 zijn opgehaald; een complete search naar wijzigingsbesluiten is nog niet afgerond.
- Voeg de relevante artikelen van de Awb, Algemene termijnenwet, WMS, AVG en WGBH/CZ toe. Voeg voor inzage ook de primaire Europese rechtspraak toe, waaronder de in de VO-raad-handreiking genoemde zaak C-434/16. Zonder die aanvulling geen automatische einddatum, algemene rechtsroute of volledige inzage-/aanpassingsconclusie.
- WVO 2.60 lid 4 bevat in de opgehaalde officiële HTML de formulering met “hoeft”. De tekst is letterlijk behouden. Verifieer de formulering en de instemmingsgrondslag ook aan WMS artikel 10 voordat dit als tekstregel wordt geactiveerd. Het pakket trekt hieruit geen conclusie dat instemming niet nodig zou zijn.
- De vier uitspraken zijn inhoudelijk genormaliseerd. Eventueel hoger beroep en latere uitspraken over dezelfde kwestie zijn niet systematisch onderzocht.
- LKC 101642: alleen de publicatiesamenvatting was toegankelijk; de PDF gaf 403. Het volledige advies is nodig vóór normalisatie. De publicatiedatum op de pagina is niet automatisch de datum waarop het advies is vastgesteld.
- Het aanvullende LKC-advies uit 2021 was niet op te halen. Het startdocument noemt nummer 6346, maar de PDF-URL bevat 2021006436. Identiteit en datum blijven onbevestigd; het record is niet bruikbaar voor conclusies.
- Gelijkebehandelingsoordeel 2018-44 is gelezen en samengevat, maar de actuele WGBH/CZ en toepasselijkheid op een nieuwe casus moeten apart worden beoordeeld.
- VO-raad-documenten blijven handreikingen. Hun samenvattingen zijn geen complete overname van alle checklistitems. Normatieve controles in deze versie zijn rechtstreeks gekoppeld aan wetsartikelen. Volledige dekking van elk checklistitem vraagt een volgende inhoudelijke uitwerking.
- De beschikbare VO-raad-ingang verwees naar CE-protocollen 2026. Die zijn niet als bron voor examenjaar 2027 geactiveerd. Dit is geen bewijs dat een document voor 2027 nergens bestaat.
- Vergelijkingsdocumenten zijn nog niet per onderwerp naast het eigen reglement gezet. Regius havo/vwo is een concept; STC 2026-2027 is gepubliceerd onder voorbehoud. Een meegevonden STC-document uit 2025-2026 is uitgesloten voor de jaargang 2026-2027.
- De oorspronkelijke bronregistratie bevatte ongedekte active- en retrieved_at-labels. Deze blijven uitsluitend in `registry-original-unverified.yaml` voor herkomstonderzoek. De nieuwe checker moet uitsluitend `registry.json` gebruiken.
- Volledige artikelteksten zijn behouden. Een artikel kan een plicht voor de uitvoering bevatten zonder dat elke zin verplicht in het examenreglement moet staan. Gebruik procesbewijs waar dat nodig is.

## Technische open punten na v3.1

- OCR-fallback is nog niet aangesloten. Lage tekstdekking wordt nu wel herkend en zichtbaar gemarkeerd.
- De deterministische PDF-parser gebruikt tekstblokken; complexe kolommen, voetnoten en tabellen vragen extra layouttests.
- De procedure-registry bewaart nu actie, actor, fase en start_event, maar kent nog geen volledig proceduremodel met object, appeal_body en formele procesrelaties.
- Bronretrieval gebruikt jaar-, scope- en regimefilters plus deterministische tokenoverlap. Dit blijft kandidaatselectie, geen semantische gelijkwaardigheid.
- De bronpoort wordt nu per bronkandidaat in de runtime uitgevoerd. De volledige evidence-validator die een concrete schoolclaim inhoudelijk tegen een bronfragment toetst ontbreekt nog; `must` blijft geblokkeerd.
- Fasen B, E, F, G en H zijn zichtbaar `not_implemented`. Een v3-run is om die reden `partial`.
- De AI-modus is alleen een uitgeschakeld contract. Er is geen provider, model, promptset of API-call in de runtime.
