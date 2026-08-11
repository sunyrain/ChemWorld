#!/usr/bin/env python3
"""Build a zero-provider hard-gate receipt for one Work II development run."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from chemworld.eval.provenance import write_json_atomic
from chemworld.eval.work_ii_development_readiness import (
    build_development_readiness_receipt,
)

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--historical-run", type=Path, action="append", required=True)
    parser.add_argument("--world-seed", type=int, nargs="+", required=True)
    parser.add_argument("--pilot-run", type=Path)
    parser.add_argument("--continuation-seed0-run", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    def progress(payload: dict[str, object]) -> None:
        print(json.dumps(payload, ensure_ascii=False, sort_keys=True), flush=True)

    receipt = build_development_readiness_receipt(
        ROOT,
        args.config,
        args.world_seed,
        args.historical_run,
        pilot_run=args.pilot_run,
        continuation_seed0_run=args.continuation_seed0_run,
        progress=progress,
    )
    write_json_atomic(args.output.resolve(), receipt)
    print(
        json.dumps(
            {
                "stage": "readiness_completed",
                "ready": receipt["ready"],
                "provider_call_count": receipt["provider_call_count"],
                "historical_passed": receipt["historical_audit"]["passed_trajectory_count"],
                "historical_total": receipt["historical_audit"]["trajectory_count"],
                "direction_stability_applicable": receipt["direction_stability_audit"][
                    "applicable"
                ],
                "direction_stability_passed": receipt["direction_stability_audit"]["passed"],
                "seed0_pilot_passed": (
                    receipt.get("seed0_expansion_pilot", {}).get("passed")
                    if isinstance(receipt.get("seed0_expansion_pilot"), dict)
                    else None
                ),
                "seed0_continuation_bound": (
                    receipt.get("seed0_terminal_continuation", {}).get("passed")
                    if isinstance(receipt.get("seed0_terminal_continuation"), dict)
                    else None
                ),
                "output": str(args.output.resolve()),
            },
            ensure_ascii=False,
            sort_keys=True,
        ),
        flush=True,
    )
    return 0 if receipt["ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
