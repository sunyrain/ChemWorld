"""Audit exposed cohorts and the v0.5 formal-evidence quarantine guard."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from chemworld.eval.evidence_quarantine import (
    audit_evidence_quarantine,
    load_evidence_quarantine_policy,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("workstreams/benchmark_v1/reports/evidence-quarantine-v0.5.json"),
    )
    args = parser.parse_args()
    report = audit_evidence_quarantine(load_evidence_quarantine_policy())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "controls_ready": report["controls_ready"],
                "exposed_seed_count": report["inventory"]["exposed_seed_count"],
                "legacy_result_count": report["legacy_primary_0_3"]["result_count"],
                "output": str(args.output),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if report["controls_ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
