import unittest

from dvs.diagnostics import Scenario, diagnose


class DiagnosticStubTests(unittest.TestCase):
    def test_synthetic_scenarios_are_reproducible(self):
        cases = {
            Scenario.NORMAL: "normal",
            Scenario.ANOMALY: "anomaly",
            Scenario.POOR_RECORDING: None,
            Scenario.UNKNOWN_STATUS: None,
            Scenario.UNAVAILABLE: None,
        }
        self.assertEqual(set(cases), set(Scenario))
        for scenario, conclusion in cases.items():
            with self.subTest(scenario=scenario):
                result = diagnose(scenario, local_test_mode=True)
                self.assertIs(result.status, scenario)
                self.assertEqual(result.conclusion, conclusion)
                self.assertEqual(result, diagnose(scenario, local_test_mode=True))
