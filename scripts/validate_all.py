from __future__ import annotations
import subprocess,sys,pathlib,json
ROOT=pathlib.Path(__file__).resolve().parents[1]
def run(cmd):
 print('+',' '.join(map(str,cmd)));subprocess.run(cmd,cwd=ROOT,check=True)
def main():
 run([sys.executable,'-m','unittest','discover','-s','tests','-p','test_*.py','-v'])
 run(['node','scripts/test_html.cjs'])
 run(['node','scripts/test_v3_html.cjs'])
 # Clean test caches, then enforce release hygiene.
 import shutil
 for d in list(ROOT.rglob('__pycache__')): shutil.rmtree(d,ignore_errors=True)
 for f in list(ROOT.rglob('*.pyc')): f.unlink(missing_ok=True)
 for d in [ROOT/'runtime/uploads',ROOT/'runtime/runs']:
  for f in d.glob('*'):
   if f.name != '.gitkeep' and f.is_file(): f.unlink()
 bad=[p for p in ROOT.rglob('*') if p.is_file() and (p.suffix=='.pyc' or '__pycache__' in p.parts)]
 if bad:raise SystemExit('Caches in distributie: '+', '.join(str(p.relative_to(ROOT)) for p in bad))
 m=json.loads((ROOT/'manifest.json').read_text())
 assert m['production_ready'] is False and m['analysis_modes']['without_ai']=='implemented' and m['analysis_modes']['with_ai']=='skeleton_disabled'
 print('PASS package hygiene and manifest')
if __name__=='__main__':main()
