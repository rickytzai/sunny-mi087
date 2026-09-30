import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_json(relative_path):
    return json.loads((ROOT / relative_path).read_text(encoding="utf-8"))


def walk_keys(value):
    if isinstance(value, dict):
        for key, child in value.items():
            yield key.lower()
            yield from walk_keys(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk_keys(child)


class PublicEvidenceContractTests(unittest.TestCase):
    def test_evidence_is_functional_without_published_metrics(self):
        for path, expected_id in [
            ("evidence/human-e2e-redacted.json", "20260928_184302"),
            ("evidence/barge-in-redacted.json", "20260928_184855"),
        ]:
            artifact = load_json(path)
            self.assertEqual(artifact["verification_status"], "VERIFIED_FUNCTIONAL")
            self.assertEqual(artifact["evidence_id"], expected_id)
            self.assertEqual(artifact["published_measurements"], [])

    def test_public_artifacts_have_no_raw_content_fields(self):
        forbidden = {
            "api_key",
            "audio",
            "audio_path",
            "credential",
            "password",
            "token",
            "transcript",
            "transcript_text",
            "user_email",
            "user_name",
        }
        for path in [
            "evidence/human-e2e-redacted.json",
            "evidence/barge-in-redacted.json",
            "examples/assemblyai_events.json",
            "examples/turn_policy_cases.json",
        ]:
            keys = set(walk_keys(load_json(path)))
            self.assertFalse(keys & forbidden, f"{path} contains forbidden keys")

    def test_barge_in_event_responsibilities_and_order(self):
        fixture = load_json("examples/assemblyai_events.json")
        self.assertFalse(fixture["recorded_telemetry"])
        events = fixture["events"]
        by_name = {event["event"]: event for event in events}
        self.assertEqual(by_name["SpeechStarted"]["source"], "assemblyai")
        self.assertEqual(by_name["PlaybackStopOrDuck"]["source"], "sunny")
        self.assertLess(
            by_name["SpeechStarted"]["sequence"],
            by_name["PlaybackStopOrDuck"]["sequence"],
        )
        self.assertLess(
            by_name["PlaybackStopOrDuck"]["sequence"],
            by_name["ResponseToNewTurn"]["sequence"],
        )

    def test_policy_cases_are_bounded_and_deterministic(self):
        fixture = load_json("examples/turn_policy_cases.json")
        self.assertFalse(fixture["recorded_telemetry"])
        cases = {case["id"]: case for case in fixture["cases"]}
        self.assertEqual(
            cases["thinking_pause"]["expected_policy_action"],
            "keep_listening",
        )
        self.assertEqual(
            cases["human_barge_in"]["expected_policy_action"],
            "stop_playback_before_new_response",
        )
        self.assertTrue(all(case["route"] == "deterministic_fast_path" for case in cases.values()))


if __name__ == "__main__":
    unittest.main()
