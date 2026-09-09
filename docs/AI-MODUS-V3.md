# Analysemodus: zonder AI / met AI

V3.1 houdt de ontwerpregel vast:

> AI mag de analyse later verdiepen, maar is niet nodig om de basiscontrole uit te voeren.

**Zonder AI** is de actieve modus. Parser, contextbevestiging, registers, interne consistentie, bronfilters, bronpoort, review en runstatus draaien deterministisch in Python.

**Met AI** staat zichtbaar in de UI maar is disabled. `app/ai_adapter.py` meldt `available=false`; de API weigert `ai_mode=on` met HTTP 409.

Een latere AI-laag mag nooit bronstatus, `production_approved` of de juridische outputblokkade wijzigen.
