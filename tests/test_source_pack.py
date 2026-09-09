import copy,hashlib,json,pathlib,sys,unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from source_gate import can_support_must
S=json.loads((ROOT/'sources/registry.json').read_text());F=json.loads((ROOT/'sources/fragments.json').read_text());R=json.loads((ROOT/'rules/candidates.json').read_text());C=json.loads((ROOT/'sources/jurisprudence.normalized.json').read_text())
class PackTests(unittest.TestCase):
 def test_schema_contracts(self):
  from jsonschema import Draft202012Validator,FormatChecker
  for file,records in [('source',S),('rule',R),('jurisprudence',C)]:
   validator=Draft202012Validator(json.loads((ROOT/f'schemas/{file}.schema.json').read_text()),format_checker=FormatChecker())
   for r in records:validator.validate(r)
 def test_unique_ids(self):
  for records,key in [(S,'id'),(F,'fragment_id'),(R,'rule_id'),(C,'case_id')]:self.assertEqual(len(records),len({r[key] for r in records}))
 def test_content_integrity(self):
  for f in F:self.assertEqual(f['text_hash'],hashlib.sha256(f['text'].encode()).hexdigest())
  for s in S:
   if s.get('original_path'):self.assertEqual(s['content_hash'],hashlib.sha256((ROOT/s['original_path']).read_bytes()).hexdigest())
   if s.get('content_path'):self.assertTrue((ROOT/s['content_path']).is_file())
 def test_reference_integrity(self):
  idx={f['fragment_id']:f for f in F};si={s['id']:s for s in S}
  for r in R:
   self.assertIn(r['source_id'],si)
   self.assertTrue(r['evidence'])
   for e in r['evidence']:
    if 'fragment_id' in e:self.assertEqual(idx[e['fragment_id']]['source_id'],r['source_id'])
 def test_all_candidates_blocked(self):
  si={s['id']:s for s in S}
  for r in R:self.assertFalse(can_support_must(r,si[r['source_id']],F,as_of='2026-09-07',exam_year=2027)[0])
 def fixture(self):
  r=copy.deepcopy(R[0]);s=copy.deepcopy(next(s for s in S if s['id']==r['source_id']))
  r.update(verification_status='validated',production_approved=True,verified_by='TEST FIXTURE ONLY',verified_at='2026-09-07')
  s.update(production_approved=True,legal_review_status='approved',status='active_reviewed')
  return r,s
 def test_gate_control_and_missing_evidence(self):
  r,s=self.fixture();self.assertTrue(can_support_must(r,s,F,as_of='2026-09-07',exam_year=2027)[0]);r['evidence']=[]
  self.assertFalse(can_support_must(r,s,F,as_of='2026-09-07',exam_year=2027)[0])
 def test_source_year_and_authority(self):
  r,s=self.fixture();s['exam_year']=2026
  self.assertEqual(can_support_must(r,s,F,as_of='2026-09-07',exam_year=2027)[1],'wrong_exam_year')
  s['authority_class']='example';self.assertEqual(can_support_must(r,s,F,as_of='2026-09-07',exam_year=2027)[1],'not_binding')
 def test_expiry_and_hash(self):
  r,s=self.fixture();s['valid_to']='2026-09-07'
  self.assertEqual(can_support_must(r,s,F,as_of='2026-09-07',exam_year=2027)[1],'expired')
  s['valid_to']=None;r['evidence'][0]['text_hash']='changed'
  self.assertEqual(can_support_must(r,s,F,as_of='2026-09-07',exam_year=2027)[1],'fragment_hash_mismatch')
 def test_failed_sources_never_inherit_seed_active(self):
  for s in S:
   self.assertFalse(s['production_approved'])
   if s['fetch_status']=='failed':self.assertEqual(s['status'],'fetch_failed');self.assertIsNone(s['retrieved_at'])
 def test_case_limits(self):
  for c in C:self.assertTrue(c['may_infer']);self.assertTrue(c['must_not_infer']);self.assertFalse(c['production_approved']);self.assertTrue(c['decisive_locations'])
  ams=next(c for c in C if 'RBAMS' in c['case_id']);self.assertIn('fraudevermoeden',ams['topics']);self.assertIn('2020',ams['legal_regime'])
if __name__=='__main__':unittest.main(verbosity=2)
