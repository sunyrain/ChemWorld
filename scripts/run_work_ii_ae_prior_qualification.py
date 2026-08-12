#!/usr/bin/env python3
"""Run the frozen provider-free Work II A-E prior-distinguishability qualification."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from chemworld.eval.work_ii_ae_prior_qualification import execute_qualification

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DESIGN = ROOT / "configs/benchmark/work_ii_formal_design_v0.1.json"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--design", type=Path, default=DEFAULT_DESIGN)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = execute_qualification(ROOT, args.design.resolve(), args.output.resolve())
    print(
        json.dumps(
            {
                "status": report["status"],
                "tasks": report["denominators"]["tasks"],
                "task_worlds": report["denominators"]["task_worlds"],
                "executions": report["denominators"]["evaluator_executions"],
                "failure_count": len(report["failures"]),
                "report_sha256": report["report_sha256"],
                "output": str(args.output),
            },
            sort_keys=True,
        ),
        flush=True,
    )
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())

