"""V3.2 regressietests — bewaken de bugfix in _start_event.

De v3.1-demo-run toonde dat twee clausules die semantisch dezelfde stap beschrijven
(hier: zich aanmelden voor een herkansing binnen N schooldagen na publicatie)
verschillende _start_event waarden kregen, waardoor _term_key verschilde en
geen term_conflict werd gerapporteerd. V3.2 beperkt _start_event tot het eerste
kern-zelfstandignaamwoord zodat beide clausules dezelfde sleutel krijgen.
"""
import tempfile, unittest, sys
from pathlib import Path
from docx import Document
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT))
from app.parser import parse_document
from app.registers import build_registers, _start_event
from app.analyzer import analyze_document


class V32RegressionTests(unittest.TestCase):
    def doc(self, td, paras, year='2026-2027'):
        p = Path(td) / 'x.docx'
        d = Document()
        for x in paras:
            d.add_paragraph(x)
        d.save(p)
        return parse_document(p, school_year=year, school_types=['vwo'])

    def test_start_event_stops_at_function_word(self):
        # V3.1 bug: _start_event pakte alles tot leesteken — gaf "publicatie aan voor de herkansing"
        # V3.2 fix: stopt bij het eerste voorzetsel/werkwoord — geeft "publicatie"
        self.assertEqual(_start_event('De kandidaat meldt zich binnen 3 schooldagen na publicatie aan voor de herkansing.'), 'publicatie')
        self.assertEqual(_start_event('Aanmelden voor dezelfde herkansing kan tot 5 schooldagen na publicatie.'), 'publicatie')

    def test_herkansing_term_conflict_with_different_values_is_detected(self):
        # Het demo-document bevat deze twee clausules; v3.1 vond dit niet als conflict.
        with tempfile.TemporaryDirectory() as td:
            doc = self.doc(td, [
                'Artikel 1 Herkansing',
                'De kandidaat meldt zich binnen 3 schooldagen na publicatie aan voor de herkansing.',
                'Aanmelden voor dezelfde herkansing kan tot 5 schooldagen na publicatie.',
            ])
            result = analyze_document(doc, root=ROOT, run_id='v32-test')
            term_conflicts = [f for f in result['findings'] if 'term_conflict' in f['finding_type']]
            self.assertTrue(term_conflicts,
                'V3.2 moet een term_conflict rapporteren voor verschillende waarden bij dezelfde stap '
                f'(gevonden findings: {[f["finding_type"] for f in result["findings"]]})')

    def test_start_event_handles_multiline_clause(self):
        # Edge-case: een start_event met een samengesteld zelfstandignaamwoord
        self.assertEqual(_start_event('De kandidaat kan binnen 5 dagen na de beslissing van de rector beroep instellen.'), 'beslissing')

    def test_start_event_returns_none_without_preposition(self):
        # Geen "na|vanaf|volgend op" → geen start_event
        self.assertIsNone(_start_event('De kandidaat meldt zich binnen 3 schooldagen aan.'))


if __name__ == '__main__':
    unittest.main(verbosity=2)
