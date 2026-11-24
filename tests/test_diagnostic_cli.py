import json
import subprocess
import sys
import unittest


class DiagnosticCliTests(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, "-B", "-m", "dvs", *args],
            capture_output=True,
            text=True,
        )

    def test_explicit_test_mode_marks_result_synthetic(self):
        result = self.run_cli("--local-test", "--scenario", "normal")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(json.loads(result.stdout)["synthetic"])

    def test_default_mode_reports_unavailable_without_substitution(self):
        result = self.run_cli()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            json.loads(result.stdout),
            {"status": "unavailable", "synthetic": False, "conclusion": None},
        )

    def test_scenario_requires_explicit_test_mode(self):
        result = self.run_cli("--scenario", "normal")
        self.assertEqual(result.returncode, 2)
        self.assertIn("--scenario requires --local-test", result.stderr)

    def test_test_mode_requires_explicit_scenario(self):
        result = self.run_cli("--local-test")
        self.assertEqual(result.returncode, 2)
        self.assertIn("--local-test requires --scenario", result.stderr)

    def test_unusable_results_report_distinct_reasons_without_conclusions(self):
        for scenario in ("poor-recording", "unknown-status", "unavailable"):
            with self.subTest(scenario=scenario):
                result = self.run_cli("--local-test", "--scenario", scenario)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(
                    json.loads(result.stdout),
                    {"status": scenario, "synthetic": True, "conclusion": None},
                )
