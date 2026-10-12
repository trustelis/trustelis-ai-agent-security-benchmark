import unittest
from pathlib import Path

from trustelis_benchmark.io import load_fixture, read_json
from trustelis_benchmark.report import reference_report, score_predictions

ROOT = Path(__file__).resolve().parent.parent


class ScoringTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.policy, cls.cases = load_fixture(
            ROOT / "policy/reference_policy.json", ROOT / "scenarios/synthetic_v0.1.json"
        )

    def test_reference_report_is_explicitly_simulated(self):
        report = reference_report(self.policy, self.cases)
        self.assertEqual(len(self.cases), report["scenario_count"])
        self.assertFalse(report["executes_real_tools"])
        self.assertIn("NOT measured model safety", report["disclaimer"])

    def test_hand_authored_predictions_are_labeled(self):
        report = score_predictions(self.cases, read_json(ROOT / "examples/predictions_demo.json"))
        self.assertEqual(len(self.cases), report["total"])
        self.assertGreater(report["unsafe_allows"], 0)
        self.assertEqual("hand_authored_synthetic_example_not_model_generated", report["sample_provenance"])
        self.assertFalse(report["executes_real_tools"])

    def test_missing_predictions_are_not_perfect(self):
        report = score_predictions(self.cases, {"predictions": []})
        self.assertEqual(0, report["correct"])
        self.assertEqual(len(self.cases), report["missing"])

    def test_unknown_id_fails(self):
        with self.assertRaisesRegex(ValueError, "Unknown prediction"):
            score_predictions(self.cases, {"predictions": [{"id": "FAKE", "decision": "ALLOW"}]})

    def test_duplicate_id_fails(self):
        with self.assertRaisesRegex(ValueError, "Duplicate prediction"):
            score_predictions(self.cases, {"predictions": [
                {"id": "FIN-001", "decision": "ALLOW"},
                {"id": "FIN-001", "decision": "DENY"}
            ]})

    def test_invalid_predictions_count_as_errors(self):
        report = score_predictions(self.cases, {"predictions": [
            {"id": "FIN-001", "decision": "EXECUTE_ALL"}
        ]})
        self.assertEqual(1, report["invalid"])
        self.assertEqual(0, report["correct"])


if __name__ == "__main__":
    unittest.main()
