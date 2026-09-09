import hashlib,json,pathlib,sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
manifest=ROOT/'MANIFEST.sha256'
if not manifest.exists(): print('MANIFEST ontbreekt'); sys.exit(1)
for line in manifest.read_text().splitlines():
 if not line.strip(): continue
 h,rel=line.split('  ',1); p=ROOT/rel
 if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=h:
  print('FOUT',rel); sys.exit(1)
print('PASS manifest',sum(1 for _ in manifest.read_text().splitlines()))
