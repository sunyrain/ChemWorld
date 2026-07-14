"""Audit method-freeze readiness without opening or issuing private Bench data."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from chemworld.eval.method_freeze_v0_4 import (
    DEFAULT_METHOD_FREEZE_PLAN_PATH,
    audit_method_freeze,
    load_method_freeze_plan,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, default=DEFAULT_METHOD_FREEZE_PLAN_PATH)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("workstreams/benchmark_v1/reports/method-freeze-v0.4.json"),
    )
    args = parser.parse_args()
    report = audit_method_freeze(load_method_freeze_plan(args.plan), root=args.repo_root)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "method_freeze_ready": report["method_freeze_ready"],
                "preflight_issuance_allowed": report["preflight_issuance_allowed"],
                "bench_unlock_allowed": report["bench_unlock_allowed"],
                "blocker_count": len(report["blockers"]),
                "output": str(args.output),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if report["method_freeze_ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
