"""Audit operation-to-model reachability without executing or changing the world."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from chemworld.runtime.model_reachability import (
    audit_model_reachability,
    audit_shared_claim_ownership,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tasks", nargs="+")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("runs/world_foundation/model_reachability_audit.json"),
    )
    parser.add_argument(
        "--strict-alignment",
        action="store_true",
        help="Also fail when task maturity declarations contain known alignment gaps.",
    )
    args = parser.parse_args()
    report = audit_model_reachability(
        None if args.tasks is None else tuple(args.tasks)
    )
    claim_ownership = audit_shared_claim_ownership(Path(__file__).resolve().parents[1])
    report["claim_ownership"] = claim_ownership
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    summary = {
        "output": str(args.output),
        "contract_integrity_passed": report["contract_integrity_passed"],
        "declaration_alignment_status": report["declaration_alignment_status"],
        "declaration_gap_count": report["declaration_gap_count"],
        "task_count": report["task_count"],
        "provider_count": report["provider_count"],
        "route_count": report["route_count"],
        "claim_ownership_passed": claim_ownership["passed"],
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    passed = bool(report["contract_integrity_passed"] and claim_ownership["passed"])
    if args.strict_alignment:
        passed = passed and report["declaration_alignment_status"] == "aligned"
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
