"""Run held-out-seed generalization diagnostics for chemworld-serious-v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from chemworld.eval.baseline_report import (
    SERIOUS_BASELINE_AGENTS,
    generate_serious_baseline_report,
)
from chemworld.eval.generalization import compare_public_and_ood_reports


def _read_json(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--public-report",
        type=Path,
        default=Path("runs/benchmark_freeze/release_v1/baseline_report/baseline_report.json"),
    )
    parser.add_argument("--ood-seeds", nargs="+", type=int, default=[101, 102, 103])
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("runs/benchmark_freeze/release_v1/generalization"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("runs/benchmark_freeze/release_v1/generalization_audit.json"),
    )
    args = parser.parse_args()
    public_report = _read_json(args.public_report)
    ood_report = generate_serious_baseline_report(
        agents=list(SERIOUS_BASELINE_AGENTS),
        seeds=list(args.ood_seeds),
        output_dir=args.output_dir,
    )
    audit = compare_public_and_ood_reports(
        public_report,
        ood_report.to_dict(),
        ood_seeds=tuple(args.ood_seeds),
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(audit, indent=2, sort_keys=True))
    return 0 if audit["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
