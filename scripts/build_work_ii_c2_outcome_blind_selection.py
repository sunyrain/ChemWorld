#!/usr/bin/env python3
"""Build a deterministic Work II C2 outcome-blind task-selection record."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from chemworld.eval.provenance import write_json_atomic
from chemworld.eval.work_ii_c2_admission import (
    C2_DYNAMIC_EVIDENCE_ROOT,
    build_c2_outcome_blind_selection_record,
)

ROOT = Path(__file__).resolve().parents[1]


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("selection specification must contain a JSON object")
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--locus", required=True, choices=("A_P", "A_S"))
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--selection-spec", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    spec = _load(args.selection_spec.resolve())
    output = args.output.resolve()
    try:
        output.relative_to(ROOT.resolve())
    except ValueError as error:
        raise ValueError("C2 selection output must remain inside the repository") from error
    dynamic_root = (ROOT / C2_DYNAMIC_EVIDENCE_ROOT).resolve()
    try:
        output.relative_to(dynamic_root)
    except ValueError as error:
        raise ValueError(
            f"C2 selection output must remain under {C2_DYNAMIC_EVIDENCE_ROOT}"
        ) from error
    roster = spec.get("candidate_roster")
    rule = spec.get("selection_rule")
    if not isinstance(roster, list) or not isinstance(rule, dict):
        raise ValueError("selection specification lacks candidate_roster or selection_rule")
    record = build_c2_outcome_blind_selection_record(
        ROOT,
        locus=args.locus,
        task_id=args.task_id,
        candidate_roster=[dict(row) if isinstance(row, dict) else {} for row in roster],
        selection_rule=rule,
    )
    write_json_atomic(output, record)
    print(
        json.dumps(
            {
                "locus": record["locus"],
                "task_id": record["task_id"],
                "selected_frozen_rank": record["selected_frozen_rank"],
                "selection_sha256": record["selection_sha256"],
                "output": str(output),
            },
            sort_keys=True,
        ),
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
