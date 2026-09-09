import hashlib,json,pathlib,re,unittest,yaml
ROOT=pathlib.Path(__file__).resolve().parents[1]
class T(unittest.TestCase):
 def j(self,p):return json.loads((ROOT/p).read_text())
 def test_v1_archive(self):
  r=self.j('docs/v1-file-review.json');self.assertEqual(len(r),34)
  for x in r:
   p=ROOT/'archive/v1'/x['file'];self.assertTrue(p.is_file());self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),x['v1_sha256']);self.assertTrue((ROOT/x['file']).is_file())
 def test_compat(self):
  self.assertEqual(yaml.safe_load((ROOT/'sources/registry.yaml').read_text())['sources'],self.j('sources/registry.json'));self.assertEqual(self.j('sources/jurisprudence.seed.json'),self.j('sources/jurisprudence.normalized.json'))
 def test_html_embeds_full_prior_pack(self):
  h=(ROOT/'examenreglement-checker-met-bronnen.html').read_text();m=re.search(r'const sourceLibrary=(.*?);\nconst seed=',h,re.S);self.assertIsNotNone(m);d=json.loads(m.group(1));self.assertEqual(d['sources'],self.j('sources/registry.json'));self.assertEqual(d['fragments'],self.j('sources/fragments.json'));self.assertEqual(d['rules'],self.j('rules/candidates.json'));self.assertEqual(d['cases'],self.j('sources/jurisprudence.normalized.json'))
 def test_counts_and_blocked(self):
  self.assertEqual(len(self.j('sources/registry.json')),40);self.assertEqual(len(self.j('sources/fragments.json')),109);self.assertEqual(len(self.j('rules/candidates.json')),40);self.assertFalse(any(s.get('production_approved') for s in self.j('sources/registry.json')));self.assertFalse(any(r.get('production_approved') for r in self.j('rules/candidates.json')))
 def test_golden_status(self):
  for p in (ROOT/'tests/golden').glob('*.json'):
   x=json.loads(p.read_text());self.assertEqual(x['validation_status'],'candidate_needs_independent_review');self.assertEqual(x['execution_status'],'not_run_analyzer_missing')
if __name__=='__main__':unittest.main(verbosity=2)
