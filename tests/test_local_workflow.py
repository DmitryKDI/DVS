import unittest
from dataclasses import replace

from dvs.diagnostics import Scenario
from dvs.local_workflow import DEMO_EVIDENCE, DEMO_PAGES, DEMO_VEHICLE, LocalReceiptBook, check_vehicle


class LocalWorkflowTests(unittest.TestCase):
    def test_no_draft_without_anomaly(self):
        for scenario in set(Scenario) - {Scenario.ANOMALY}:
            with self.subTest(scenario=scenario):
                check = check_vehicle(DEMO_VEHICLE, scenario, DEMO_EVIDENCE, DEMO_PAGES)
                self.assertEqual(check.vehicle.vehicle_id, "demo-001")
                self.assertIs(check.diagnosis.status, scenario)
                self.assertTrue(check.diagnosis.synthetic)
                if scenario is not Scenario.NORMAL:
                    self.assertIsNone(check.diagnosis.conclusion)
                self.assertIsNone(check.evidence)
                self.assertIsNone(check.draft)

    def test_only_applicable_evidence_with_a_page_can_create_draft(self):
        for candidate in (
            None,
            replace(DEMO_EVIDENCE, engine="other-engine"),
            replace(DEMO_EVIDENCE, modification="other-modification"),
            replace(DEMO_EVIDENCE, pdf_page=0),
            replace(DEMO_EVIDENCE, pdf_page=2),
            replace(DEMO_EVIDENCE, excerpt="Unverified quotation"),
            replace(DEMO_EVIDENCE, excerpt=" "),
            replace(DEMO_EVIDENCE, printed_page="ii"),
            replace(DEMO_EVIDENCE, operation="Unsupported operation"),
        ):
            with self.subTest(candidate=candidate):
                check = check_vehicle(DEMO_VEHICLE, Scenario.ANOMALY, candidate, DEMO_PAGES)
                self.assertIsNone(check.evidence)
                self.assertIsNone(check.draft)
                self.assertEqual(check.evidence_status, "unconfirmed")

        check = check_vehicle(DEMO_VEHICLE, Scenario.ANOMALY, DEMO_EVIDENCE, DEMO_PAGES)
        self.assertIs(check.diagnosis.status, Scenario.ANOMALY)
        self.assertIn("unconfirmed", check.hypothesis)
        self.assertEqual(check.evidence_status, "verified-synthetic")
        self.assertEqual(check.evidence.pdf_page, 1)
        self.assertEqual(check.evidence.printed_page, "i")
        self.assertEqual(check.draft.operation, DEMO_EVIDENCE.operation)

    def test_confirmation_is_required_for_the_current_revision(self):
        check = check_vehicle(DEMO_VEHICLE, Scenario.ANOMALY, DEMO_EVIDENCE, DEMO_PAGES)
        draft = check.draft
        receiver = LocalReceiptBook()
        with self.assertRaises(ValueError):
            receiver.submit(draft)
        draft = draft.confirm(1).edit("Inspect replacement demo component")
        with self.assertRaises(ValueError):
            receiver.submit(draft)
        with self.assertRaises(ValueError):
            draft.confirm(1)
        self.assertEqual(receiver.receipts, [])
        with self.assertRaisesRegex(ValueError, "supported by the verified evidence"):
            receiver.submit(draft.confirm(2))
        self.assertEqual(receiver.receipts, [])
        corrected = draft.edit(DEMO_EVIDENCE.operation)
        receipt = receiver.submit(corrected.confirm(3))
        self.assertEqual(receipt["status"], "accepted-locally")
        self.assertTrue(receipt["synthetic"])
        self.assertEqual(receipt["revision"], 3)
        self.assertEqual(receiver.receipts, [receipt])
