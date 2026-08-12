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
    parser.add_argument("--selection-protocol", required=True, type=Path)
    parser.add_argument("--terminal-eligibility", required=True, type=Path)
    parser.add_argument("--selection-slot", required=True, type=int, choices=(1, 2))
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    eligibility = _load(args.terminal_eligibility.resolve())
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
    dispositions = eligibility.get("terminal_eligibility")
    if not isinstance(dispositions, dict):
        raise ValueError("terminal eligibility file lacks terminal_eligibility")
    record = build_c2_outcome_blind_selection_record(
        ROOT,
        locus=args.locus,
        task_id=args.task_id,
        selection_protocol_path=args.selection_protocol.resolve(),
        terminal_eligibility={
            str(task_id): dict(row) if isinstance(row, dict) else {}
            for task_id, row in dispositions.items()
        },
        selection_slot=args.selection_slot,
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
