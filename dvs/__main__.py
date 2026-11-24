"""Run a local diagnostic check."""

import argparse
from dataclasses import asdict
import json

from .diagnostics import Scenario, diagnose


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--local-test", action="store_true")
    parser.add_argument("--scenario", choices=[scenario.value for scenario in Scenario])
    args = parser.parse_args()

    if args.local_test and args.scenario is None:
        parser.error("--local-test requires --scenario")
    if args.scenario is not None and not args.local_test:
        parser.error("--scenario requires --local-test")

    scenario = Scenario(args.scenario) if args.scenario is not None else None
    print(json.dumps(asdict(diagnose(scenario, local_test_mode=args.local_test))))


if __name__ == "__main__":
    main()
