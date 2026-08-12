#!/usr/bin/env python3
"""Run the development-only provider-free Work II A-E v0.2 qualification."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from chemworld.eval.work_ii_ae_prior_qualification_v02 import execute_qualification

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONTRACT = (
    ROOT / "configs/benchmark/work_ii_ae_prior_distinguishability_v0.2.json"
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", type=Path, default=DEFAULT_CONTRACT)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = execute_qualification(
        ROOT, args.contract.resolve(), args.output.resolve()
    )
    print(
        json.dumps(
            {
                "status": report["status"],
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
