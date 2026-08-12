#!/usr/bin/env python3
"""Independently validate a Work II runtime-semantics impact audit."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from chemworld.eval.work_ii_runtime_semantics_impact_validation import (
    validate_runtime_semantics_impact_audit,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPORT = (
    ROOT
    / "workstreams/flagship_tasks/reports/"
    / "work-ii-runtime-semantics-impact-audit-20260812.json"
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    args = parser.parse_args()
    report = json.loads(args.report.read_text(encoding="utf-8"))
    result = validate_runtime_semantics_impact_audit(report)
    print(json.dumps(result, sort_keys=True))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
