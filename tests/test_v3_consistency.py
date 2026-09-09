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
 def test_v31_ui_contains_review_changes_and_audit(self):
  h=(ROOT/'web/index.html').read_text();self.assertIn('Wijzigingen',h);self.assertIn('Audit',h);self.assertIn('Review opslaan',h);self.assertIn('Bronpoort / evidence-validatie',h)
 def test_runtime_dirs_are_release_cleanable(self):
  for rel in ['runtime/uploads','runtime/runs']:
   self.assertTrue((ROOT/rel).is_dir())
if __name__=='__main__':unittest.main()
