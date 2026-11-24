"""Internal diagnostic boundary for local testing."""

from dataclasses import dataclass
from enum import Enum


class Scenario(str, Enum):
    NORMAL = "normal"
    ANOMALY = "anomaly"
    POOR_RECORDING = "poor-recording"
    UNKNOWN_STATUS = "unknown-status"
    UNAVAILABLE = "unavailable"


@dataclass(frozen=True)
class DiagnosticResult:
    status: Scenario
    synthetic: bool
    conclusion: str | None = None


def diagnose(
    scenario: Scenario | None = None, *, local_test_mode: bool = False
) -> DiagnosticResult:
    """Return a synthetic result only when the test source is selected."""
    if not local_test_mode:
        return DiagnosticResult(Scenario.UNAVAILABLE, synthetic=False)
    if scenario is None:
        raise ValueError("A scenario is required in local test mode.")

    conclusions = {
        Scenario.NORMAL: "normal",
        Scenario.ANOMALY: "anomaly",
    }
    return DiagnosticResult(scenario, synthetic=True, conclusion=conclusions.get(scenario))
