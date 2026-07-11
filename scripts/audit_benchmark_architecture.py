"""Compile all vNext control and formal-evidence gates into one readiness graph."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from chemworld.eval.architecture_audit import (
    audit_benchmark_architecture,
    load_architecture_protocol,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("workstreams/benchmark_v1/reports/architecture-readiness.json"),
    )
    args = parser.parse_args()
    report = audit_benchmark_architecture(load_architecture_protocol())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "status": report["status"],
                "architecture_consistent": report["architecture_consistent"],
                "controls_ready": report["controls_ready"],
                "formal_evidence_ready": report["formal_evidence_ready"],
                "active_issue_count": report["active_issue_count"],
                "critical_path": [item["component"] for item in report["critical_path"]],
                "output": str(args.output),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if report["architecture_consistent"] and report["controls_ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
