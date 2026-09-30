import ast
import hashlib
import json
import unittest
from pathlib import Path

from proof.rhythm_excerpt import RhythmAdapter, RhythmConfig

ROOT = Path(__file__).resolve().parents[1]


class LearningProofTests(unittest.TestCase):
    def test_existing_source_method_bodies_are_preserved(self):
        proof = json.loads((ROOT / 'evidence/learning-source-proof.json').read_text())
        tree = ast.parse((ROOT / 'proof/rhythm_excerpt.py').read_text())
        cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == 'RhythmAdapter')
        for node in cls.body:
            if isinstance(node, ast.FunctionDef):
                actual = hashlib.sha256(ast.dump(node, include_attributes=False).encode()).hexdigest()
                self.assertEqual(actual, proof['source_method_ast_sha256'][node.name])

    def test_observations_change_later_pause_policy(self):
        adapter = RhythmAdapter()
        self.assertEqual(adapter.get_next_pause(), 300)
        for observation, expected in [(900, 360), (900, 414), (100, 435.93333333333334)]:
            adapter.record_user_pause(observation)
            self.assertAlmostEqual(adapter.get_next_pause(), expected)
        self.assertEqual(list(adapter.state.recent_pauses), [900, 900, 100])
        self.assertEqual(RhythmAdapter().get_next_pause(), 300)  # no persistence claim

    def test_window_and_bounds(self):
        adapter = RhythmAdapter(RhythmConfig(adaptation_rate=1))
        adapter.record_user_pause(10000)
        self.assertEqual(adapter.get_next_pause(), 2000)
        for _ in range(10):
            adapter.record_user_pause(0)
        self.assertEqual(len(adapter.state.recent_pauses), 10)
        self.assertEqual(adapter.state.avg_user_pause_ms, 0)
        self.assertEqual(adapter.get_next_pause(), 50)

    def test_recorded_human_event_order_and_caveats(self):
        data = json.loads((ROOT / 'evidence/human-validation-timeline.json').read_text())
        events = {e['event']: e['relative_seconds'] for e in data['events']}
        self.assertLess(events['playback_start'], events['speechstarted_detected'])
        self.assertLessEqual(events['speechstarted_detected'], events['tts_stop_triggered'])
        self.assertLess(events['tts_stop_triggered'], events['new_turn_final'])
        self.assertLess(events['new_turn_final'], events['new_response_playback_start'])
        self.assertTrue(any('zero latency' in c for c in data['caveats']))
        self.assertEqual(data['barge_in_record']['marker'], 'LIVE_BARGE_IN_EVIDENCE_EXISTS')


if __name__ == '__main__':
    unittest.main()
