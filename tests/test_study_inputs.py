import json
import unittest
from pathlib import Path


class StudyInputTests(unittest.TestCase):
    def test_domain_references_and_units(self):
        data=json.loads((Path(__file__).resolve().parents[1]/'fixtures/study-input.json').read_text())
        from network.contracts import Study
        from catchments.pairs import build
        snapshots={s['id']:Study(s['document']) for s in data['snapshots']}
        eligible={key:{(r['community'],r['facility']) for r in build(s)['pairs']} for key,s in snapshots.items()}
        for r in data['choices']:
            self.assertIn(r['snapshot'],snapshots)
            self.assertIn(r['community'],snapshots[r['snapshot']].communities)
            if r['chosen'] is not None:
                self.assertIn((r['community'],r['chosen']),eligible[r['snapshot']])
