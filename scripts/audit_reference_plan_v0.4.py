"""Audit the exact independent reference plan without opening private Bench values."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from chemworld.eval.reference_plan_v0_4 import (
    audit_reference_plan,
    load_reference_portfolio_v0_4,
    load_reference_regret_v0_4,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--portfolio",
        type=Path,
        default=Path("configs/benchmark/reference_portfolio_v0.4.json"),
    )
    parser.add_argument(
        "--regret",
        type=Path,
        default=Path("configs/benchmark/reference_regret_v0.4.json"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("workstreams/benchmark_v1/reports/reference-plan-v0.4.json"),
    )
    args = parser.parse_args()
    report = audit_reference_plan(
        load_reference_portfolio_v0_4(args.portfolio),
        load_reference_regret_v0_4(args.regret),
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "controls_ready": report["controls_ready"],
                "reference_cell_count": report["run_counts"]["reference_cell_count"],
                "source_run_count": report["run_counts"]["source_run_count"],
                "complete_experiment_count": report["run_counts"][
                    "complete_experiment_count"
                ],
                "output": str(args.output),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if report["controls_ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
