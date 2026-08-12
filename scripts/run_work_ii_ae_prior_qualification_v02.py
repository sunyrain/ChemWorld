#!/usr/bin/env python3
"""Run the provider-free Work II A-E v0.2 qualification."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from chemworld.eval.work_ii_ae_prior_qualification_v02 import (
    build_partial_audit,
    execute_qualification,
)
from chemworld.eval.work_ii_execution_mode import ExecutionMode

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONTRACT = (
    ROOT / "configs/benchmark/work_ii_ae_prior_distinguishability_v0.2.json"
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", type=Path, default=DEFAULT_CONTRACT)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--execution-mode",
        choices=[mode.value for mode in ExecutionMode],
        default=ExecutionMode.DEVELOPMENT.value,
        help="development is never formal; release requires one frozen manifest",
    )
    parser.add_argument("--release-manifest", type=Path)
    parser.add_argument(
        "--partial-audit",
        action="store_true",
        help="read and validate an interrupted output without resuming or changing it",
    )
    args = parser.parse_args()
    if args.partial_audit:
        audit = build_partial_audit(
            ROOT, args.output.resolve(), args.contract.resolve()
        )
        print(json.dumps(audit, sort_keys=True), flush=True)
        return 0 if not audit["errors"] else 1
    report = execute_qualification(
        ROOT,
        args.contract.resolve(),
        args.output.resolve(),
        execution_mode=args.execution_mode,
        release_manifest=args.release_manifest,
    )
    print(
        json.dumps(
            {
                "status": report["status"],
                "execution_mode": report["execution_context"]["execution_mode"],
                "development_only": report["development_only"],
                "primary_executions": report["denominators"][
                    "primary_executions_total"
                ],
                "exact_replay_checks": report["denominators"][
                    "tolerance_zero_exact_replay_checks"
                ],
                "failure_count": len(report["failures"]),
                "output": str(args.output),
            },
            sort_keys=True,
        ),
        flush=True,
    )
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
