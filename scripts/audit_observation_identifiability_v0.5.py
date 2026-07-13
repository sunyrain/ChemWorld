"""Audit v0.5 public instrument identifiability and spectrum disclosure."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from chemworld.eval.observation_identifiability import (
    audit_observation_identifiability,
    load_observation_identifiability_protocol,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "workstreams/world_foundation/reports/observation-identifiability-v0.5.json"
        ),
    )
    args = parser.parse_args()
    report = audit_observation_identifiability(load_observation_identifiability_protocol())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "controls_ready": report["controls_ready"],
                "instrument_count": len(report["instruments"]) + 1,
                "leakage_match_count": len(report["leakage_matches"]),
                "output": str(args.output),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if report["controls_ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
