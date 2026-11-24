"""Offline demonstration of the diagnostic and maintenance workflow."""

import argparse
import json
from collections.abc import Mapping
from dataclasses import asdict, dataclass, field, replace

from .diagnostics import DiagnosticResult, Scenario, diagnose


@dataclass(frozen=True)
class Vehicle:
    vehicle_id: str
    engine: str
    modification: str


@dataclass(frozen=True)
class Evidence:
    document: str
    engine: str
    modification: str
    pdf_page: int
    printed_page: str | None
    excerpt: str
    operation: str


@dataclass(frozen=True)
class ManualPage:
    text: str
    printed_page: str | None
    operation: str


@dataclass(frozen=True)
class Draft:
    vehicle: Vehicle
    evidence: Evidence
    operation: str
    revision: int = 1
    confirmed_revision: int | None = None

    def edit(self, operation: str) -> "Draft":
        if operation == self.operation:
            return self
        return replace(self, operation=operation, revision=self.revision + 1, confirmed_revision=None)

    def confirm(self, revision: int) -> "Draft":
        if revision != self.revision:
            raise ValueError("Confirm the current draft revision.")
        return replace(self, confirmed_revision=revision)


@dataclass
class LocalReceiptBook:
    receipts: list[dict] = field(default_factory=list)

    def submit(self, draft: Draft) -> dict:
        if draft.confirmed_revision != draft.revision:
            raise ValueError("The draft revision must be confirmed before submission.")
        if draft.operation != draft.evidence.operation:
            raise ValueError("The draft operation must be supported by the verified evidence.")
        receipt = {
            "status": "accepted-locally",
            "synthetic": True,
            "vehicle_id": draft.vehicle.vehicle_id,
            "revision": draft.revision,
            "operation": draft.operation,
        }
        self.receipts.append(receipt)
        return receipt


@dataclass
class LocalCheck:
    vehicle: Vehicle
    diagnosis: DiagnosticResult
    evidence: Evidence | None = None
    draft: Draft | None = None
    hypothesis: str | None = None
    evidence_status: str = "not-needed"


DEMO_VEHICLE = Vehicle("demo-001", "demo-engine", "demo-modification")
DEMO_EVIDENCE = Evidence(
    "synthetic-manual",
    "demo-engine",
    "demo-modification",
    1,
    "i",
    "Inspect the demo component.",
    "Inspect demo component",
)
DEMO_PAGES = {
    ("synthetic-manual", "demo-engine", "demo-modification", 1): ManualPage(
        text="Synthetic exercise. Inspect the demo component.",
        printed_page="i",
        operation="Inspect demo component",
    ),
}


def check_vehicle(
    vehicle: Vehicle,
    scenario: Scenario,
    candidate: Evidence | None,
    pages: Mapping[tuple[str, str, str, int], ManualPage],
) -> LocalCheck:
    diagnosis = diagnose(scenario, local_test_mode=True)
    check = LocalCheck(vehicle, diagnosis)
    if diagnosis.status is not Scenario.ANOMALY:
        return check

    check.hypothesis = "The cause of the synthetic anomaly is unconfirmed."
    check.evidence_status = "unconfirmed"
    if candidate is None or candidate.pdf_page < 1:
        return check
    if (candidate.engine, candidate.modification) != (vehicle.engine, vehicle.modification):
        return check

    page_key = (candidate.document, candidate.engine, candidate.modification, candidate.pdf_page)
    page = pages.get(page_key)
    if (
        page is None
        or candidate.printed_page != page.printed_page
        or candidate.operation != page.operation
        or not candidate.excerpt.strip()
        or candidate.excerpt not in page.text
    ):
        return check

    check.evidence_status = "verified-synthetic"
    check.evidence = candidate
    check.draft = Draft(vehicle, candidate, candidate.operation)
    return check


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scenario", required=True, choices=[item.value for item in Scenario])
    parser.add_argument("--submit-local", action="store_true")
    args = parser.parse_args()
    check = check_vehicle(DEMO_VEHICLE, Scenario(args.scenario), DEMO_EVIDENCE, DEMO_PAGES)
    print(json.dumps(asdict(check), indent=2))
    if args.submit_local and check.draft is not None:
        revision = check.draft.revision
        try:
            answer = input(f"Type {revision} to confirm this draft for local submission: ")
        except EOFError:
            return
        if answer.strip() == str(revision):
            confirmed = check.draft.confirm(revision)
            print(json.dumps(LocalReceiptBook().submit(confirmed)))


if __name__ == "__main__":
    main()
