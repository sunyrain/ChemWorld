#!/usr/bin/env python3
"""Record/check the irreversible, outcome-blind Work II submission-route choice."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from chemworld.eval.provenance import write_json_atomic
from chemworld.eval.work_ii_preregistration import (
    ROUTE_OPTIONS,
    validate_submission_route_decision,
)
from chemworld.eval.work_ii_route_selection import select_submission_route_decision

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DECISION = ROOT / "configs/benchmark/work_ii_submission_route_decision_v0.1.json"


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError("submission-route decision must contain an object")
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--decision", type=Path, default=DEFAULT_DECISION)
    parser.add_argument("--route", choices=ROUTE_OPTIONS)
    parser.add_argument("--selected-at")
    parser.add_argument("--selected-by-user", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    path = args.decision.resolve()
    decision = _load(path)
    if args.check:
        if any((args.route, args.selected_at, args.selected_by_user)):
            raise RuntimeError("route-selection options cannot be used with --check")
        errors = validate_submission_route_decision(decision)
        if errors:
            raise RuntimeError("invalid submission-route decision: " + "; ".join(errors))
        if decision.get("status") != "selected":
            raise RuntimeError("submission route is valid but still awaiting user selection")
    else:
        missing = []
        if args.route is None:
            missing.append("--route")
        if not args.selected_at:
            missing.append("--selected-at")
        if not args.selected_by_user:
            missing.append("--selected-by-user")
        if missing:
            raise RuntimeError(
                "refusing route selection without explicit user inputs: "
                + ", ".join(missing)
            )
        decision = select_submission_route_decision(
            decision,
            selected_option=str(args.route),
            selected_at=str(args.selected_at),
        )
        write_json_atomic(path, decision)

    print(
        json.dumps(
            {
                "status": decision["status"],
                "selected_option": decision["selected_option"],
                "selected_by": decision["selected_by"],
                "selected_at": decision["selected_at"],
                "decision_sha256": decision["decision_sha256"],
                "output": str(path),
                "check": bool(args.check),
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
