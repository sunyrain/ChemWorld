"""Audit ChemWorld transactional runtime source boundaries."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from chemworld.runtime.boundary_audit import audit_runtime_boundaries


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("runs/audit/runtime_boundary_report.json"),
        help="Path for the JSON boundary audit report.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = audit_runtime_boundaries()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(json.dumps(
        {
            "passed": report["passed"],
            "finding_count": report["finding_count"],
            "output": str(args.output),
        },
        indent=2,
        ensure_ascii=False,
    ))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
