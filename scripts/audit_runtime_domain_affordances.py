"""Generate the deterministic public-affordance/runtime-domain audit report."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

from chemworld.eval.runtime_domain_affordance_audit import (
    audit_runtime_domain_affordances,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = Path(
    "workstreams/benchmark_v1/reports/runtime-domain-affordance-audit-v0.4.json"
)


def _git(*args: str) -> str:
    return subprocess.check_output(
        ["git", *args],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
    ).strip()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--source-commit", default=None)
    parser.add_argument("--seed", type=int, default=0)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source_commit = args.source_commit or _git("rev-parse", "HEAD")
    report = audit_runtime_domain_affordances(
        source_commit=source_commit,
        seed=args.seed,
    )
    output = args.output if args.output.is_absolute() else ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report["summary"], indent=2, sort_keys=True))
    print(json.dumps(report["checks"], indent=2, sort_keys=True))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
