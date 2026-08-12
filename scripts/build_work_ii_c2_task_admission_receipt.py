#!/usr/bin/env python3
"""Build a deterministic, fail-closed Work II C2 task-admission receipt."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from chemworld.eval.provenance import write_json_atomic
from chemworld.eval.work_ii_c2_admission import (
    C2_DYNAMIC_EVIDENCE_ROOT,
    C2_TASK_STAGE_ORDER,
    build_c2_task_admission_receipt,
)

ROOT = Path(__file__).resolve().parents[1]


def _inside_root(path: Path) -> Path:
    resolved = path.resolve()
    try:
        resolved.relative_to(ROOT)
    except ValueError as error:
        raise ValueError("C2 task-admission output must remain inside repository") from error
    dynamic_root = (ROOT / C2_DYNAMIC_EVIDENCE_ROOT).resolve()
    try:
        resolved.relative_to(dynamic_root)
    except ValueError as error:
        raise ValueError(
            f"C2 task-admission output must remain under {C2_DYNAMIC_EVIDENCE_ROOT}"
        ) from error
    return resolved


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--locus", required=True, choices=("A_P", "A_S"))
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--campaign-config", required=True, type=Path)
    for stage in C2_TASK_STAGE_ORDER:
        parser.add_argument(f"--{stage.lower()}-report", required=True, type=Path)
    parser.add_argument("--selection-record", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument(
        "--require-pass",
        action="store_true",
        help="exit nonzero and do not write when evidence is not terminal",
    )
    return parser


def main() -> int:
    args = _parser().parse_args()
    report_paths = {
        stage: getattr(args, f"{stage.lower()}_report").resolve()
        for stage in C2_TASK_STAGE_ORDER
    }
    receipt = build_c2_task_admission_receipt(
        ROOT,
        locus=args.locus,
        task_id=args.task_id,
        campaign_config_path=args.campaign_config.resolve(),
        stage_report_paths=report_paths,
        selection_record_path=args.selection_record.resolve(),
    )
    if args.require_pass and receipt["status"] != "passed_terminal_task_admission":
        raise RuntimeError(
            "C2 task admission is not terminal: "
            + "; ".join(receipt["validation_errors"])
        )
    output = _inside_root(args.output)
    write_json_atomic(output, receipt)
    print(
        json.dumps(
            {
                "status": receipt["status"],
                "task_id": receipt["task_id"],
                "locus": receipt["locus"],
                "validation_error_count": len(receipt["validation_errors"]),
                "receipt_sha256": receipt["receipt_sha256"],
                "output": str(output),
            },
            ensure_ascii=False,
            sort_keys=True,
        ),
        flush=True,
    )
    return 0 if receipt["status"] == "passed_terminal_task_admission" else 2


if __name__ == "__main__":
    raise SystemExit(main())
