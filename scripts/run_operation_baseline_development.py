"""Run frozen operation controls on public Train/Dev without opening Bench."""

from __future__ import annotations

import argparse
import json

from chemworld.agents.operation_baselines import OPERATION_BASELINE_IDS
from chemworld.eval.operation_baseline_development import (
    run_operation_baseline_development_audit,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workers", type=int, default=None)
    parser.add_argument("--train-seeds", type=int, default=4)
    parser.add_argument("--dev-seeds", type=int, default=20)
    parser.add_argument("--complete-experiments", type=int, default=40)
    parser.add_argument(
        "--methods",
        nargs="+",
        choices=OPERATION_BASELINE_IDS,
        default=None,
        help="Run a frozen method subset for a resumable diagnostic screen.",
    )
    args = parser.parse_args()
    if args.workers is not None and args.workers < 1:
        parser.error("--workers must be positive")
    if not 1 <= args.train_seeds <= 100:
        parser.error("--train-seeds must be in 1..100")
    if not 1 <= args.dev_seeds <= 20:
        parser.error("--dev-seeds must be in 1..20")
    if not 2 <= args.complete_experiments <= 40:
        parser.error("--complete-experiments must be in 2..40")
    report = run_operation_baseline_development_audit(
        train_seeds=tuple(range(10_000, 10_000 + args.train_seeds)),
        dev_seeds=tuple(range(11_000, 11_000 + args.dev_seeds)),
        complete_experiments=args.complete_experiments,
        methods=None if args.methods is None else tuple(args.methods),
        workers=args.workers,
    )
    print(
        json.dumps(
            {
                "status": report["status"],
                "cell_count": report["cell_count"],
                "all_method_controls_pass": report["acceptance"]["all_method_controls_pass"],
                "operation_random_invalid_operation_count": report["acceptance"][
                    "operation_random_invalid_operation_count"
                ],
                "report": ("workstreams/benchmark_v1/reports/operation-baselines-dev-v0.4.json"),
            },
            indent=2,
        )
    )
    return 0 if report["acceptance"]["all_method_controls_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
