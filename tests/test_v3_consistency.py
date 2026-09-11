import json,re,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class V3ConsistencyTests(unittest.TestCase):
 def test_canonical_active_reviewed_status_in_current_policy_docs(self):
  for rel in ['docs/GOVERNANCE.md','docs/SOURCE-POLICY.md']:
   s=(ROOT/rel).read_text();self.assertIn('active_reviewed',s);self.assertNotRegex(s,r'(?m)^active$')
 def test_no_ai_mode_is_default_and_ai_disabled_in_ui(self):
  h=(ROOT/'web/index.html').read_text();self.assertIn('Zonder AI',h);self.assertRegex(h,r'<button disabled[^>]*>Met AI</button>');self.assertIn("fd.append('ai_mode','off')",h)
  m=json.loads((ROOT/'manifest.json').read_text());self.assertEqual(m['analysis_modes']['without_ai'],'implemented');self.assertEqual(m['analysis_modes']['with_ai'],'skeleton_disabled')
 def test_v33_ui_contains_complete_scoped_workflow(self):
  h=(ROOT/'web/index.html').read_text();
  for label in ('Volledigheid','Vergelijking','Wijzigingen','Audit','Review opslaan','Bronpoort / evidence-validatie','Eerdere controles','Rapport','Verwijder'):self.assertIn(label,h)
  self.assertIn('out_of_scope',h);self.assertIn('loadRuns',h);self.assertIn('downloadExport',h)
 def test_runtime_dirs_are_release_cleanable(self):
  for rel in ['runtime/uploads','runtime/runs']:
   self.assertTrue((ROOT/rel).is_dir())
 def test_ci_and_ocr_container_are_declared(self):
  workflow=(ROOT/'.github/workflows/ci.yml').read_text();docker=(ROOT/'Dockerfile').read_text();ignore=(ROOT/'.dockerignore').read_text()
  self.assertIn('python scripts/validate_all.py',workflow);self.assertIn('python scripts/verify_package.py',workflow);self.assertIn('docker build -t examenreglement-checker:test .',workflow)
  self.assertIn('tesseract-ocr-nld',docker);self.assertIn('USER checker',docker);self.assertIn('HEALTHCHECK',docker)
  self.assertIn('runtime/runs/*',ignore);self.assertIn('runtime/uploads/*',ignore)
if __name__=='__main__':unittest.main()
