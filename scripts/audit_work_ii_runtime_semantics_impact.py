#!/usr/bin/env python3
"""Build an outcome-blind Work II runtime-semantics impact report."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from chemworld.eval.provenance import write_json_atomic
from chemworld.eval.work_ii_runtime_semantics_impact import (
    build_runtime_semantics_impact_audit,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = (
    ROOT
    / "workstreams/flagship_tasks/reports/"
    / "work-ii-runtime-semantics-impact-audit-20260812.json"
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    report = build_runtime_semantics_impact_audit(ROOT)
    write_json_atomic(args.output.resolve(), report)
    print(json.dumps({"status": report["status"], **report["denominators"]}, sort_keys=True))
    return 0 if report["status"] == "passed" else 2


if __name__ == "__main__":
    raise SystemExit(main())
