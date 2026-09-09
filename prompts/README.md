# prompts/
> **Status 0.3.0:** Er is in 0.3.0 nog geen uitvoerbare promptset of modelkoppeling.

Prompts horen onder versiebeheer.

## Geen monolithische prompt

Gebruik losse promptfamilies:

- document extraction;
- semantic completeness;
- conflict explanation;
- issue tagging;
- jurisprudence relevance;
- proposal rewrite;
- adversarial review;
- evidence validation.

## Iedere prompt heeft metadata

Aanbevolen:

```yaml
id:
version:
purpose:
input_contract:
output_contract:
changed_at:
change_reason:
```

## Releasebeleid

Promptwijzigingen die severity, brongebruik of juridische classificatie kunnen veranderen vereisen golden/regressietests.

## Belangrijk

Prompts bevatten geen volledige bronbibliotheek en geen onnodige algemene uitleg. De bronset wordt door retrieval geleverd.
