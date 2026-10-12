import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def command(*args):
    return subprocess.run([sys.executable, "-m", "trustelis_benchmark", *args],
                          cwd=ROOT, capture_output=True, text=True, check=False)


class CliTests(unittest.TestCase):
    def test_validation_is_offline(self):
        result = command("validate")
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("zero network calls", result.stdout)

    def test_reference_report_writes_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = command("run", "--output", str(Path(tmp) / "report.json"))
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertTrue((Path(tmp) / "report.json").exists())

    def test_demo_predictions_score_without_api(self):
        result = command("score", "--predictions", "examples/predictions_demo.json")
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("OFFLINE CLASSIFICATION", result.stdout)

    def test_live_calls_require_explicit_consent(self):
        result = command("live-openai", "--model", "YOUR_ELIGIBLE_MODEL", "--max-cases", "1")
        self.assertEqual(2, result.returncode)
        self.assertIn("confirm-paid-api", result.stderr)

    def test_dry_run_never_requests_api(self):
        result = command("live-openai", "--model", "YOUR_ELIGIBLE_MODEL", "--max-cases", "3", "--dry-run")
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("ZERO network calls", result.stdout)

    def test_case_limit_rejects_excessive_calls(self):
        result = command("live-openai", "--model", "YOUR_ELIGIBLE_MODEL", "--max-cases", "101", "--dry-run")
        self.assertEqual(2, result.returncode)


if __name__ == "__main__":
    unittest.main()
