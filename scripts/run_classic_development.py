"""Run the frozen classic Train/Dev audit without accessing Bench or reference-search."""

from __future__ import annotations

import argparse
import json

from chemworld.eval.classic_development import run_classic_development_audit


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workers", type=int, default=None)
    parser.add_argument("--train-seeds", type=int, default=4)
    parser.add_argument("--dev-seeds", type=int, default=20)
    parser.add_argument("--complete-experiments", type=int, default=40)
    args = parser.parse_args()
    if not 1 <= args.train_seeds <= 100:
        parser.error("--train-seeds must be in 1..100")
    if not 1 <= args.dev_seeds <= 20:
        parser.error("--dev-seeds must be in 1..20")
    report = run_classic_development_audit(
        train_seeds=tuple(range(10_000, 10_000 + args.train_seeds)),
        dev_seeds=tuple(range(11_000, 11_000 + args.dev_seeds)),
        complete_experiments=args.complete_experiments,
        workers=args.workers,
    )
    print(
        json.dumps(
            {
                "status": report["status"],
                "cell_count": report["cell_count"],
                "family_champions": report["family_champions"],
                "report": "workstreams/benchmark_v1/reports/classic-dev-v0.4.json",
            },
            indent=2,
        )
    )
    return 0 if report["acceptance"]["all_method_controls_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
