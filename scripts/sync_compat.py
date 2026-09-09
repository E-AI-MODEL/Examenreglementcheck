import json,yaml,pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
s=json.loads((ROOT/'sources/registry.json').read_text())
p={'version':'0.3.0','generated_at':'2026-09-07','canonical':'registry.json','notes':['Gegenereerde compatibiliteitskopie.'],'sources':s}
(ROOT/'sources/registry.yaml').write_text(yaml.safe_dump(p,allow_unicode=True,sort_keys=False))
(ROOT/'sources/jurisprudence.seed.json').write_bytes((ROOT/'sources/jurisprudence.normalized.json').read_bytes())
