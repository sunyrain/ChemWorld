#!/usr/bin/env python3
"""Execute or merge external whole-cluster shards for Work II A-E v0.3."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from chemworld.eval.work_ii_ae_prior_qualification_v03 import (
    AEPriorQualificationV03Error,
    build_phase_plan,
    validate_plan,
)
from chemworld.eval.work_ii_ae_v03_shards import (
    execute_shard,
    materialize_merged_output,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONTRACT = (
    ROOT / "configs/benchmark/work_ii_ae_prior_distinguishability_v0.3_candidate.json"
)
SERIAL_OUTPUT_MARKERS = {
    ".runner.lock",
    "executions",
    "plan.json",
    "receipts",
    "report.json",
}
MERGED_TERMINAL_STATUSES = {
    "completed",
    "passed",
    "scientifically_rejected",
    "no_eligible_tasks",
}


def _load(path: Path | None) -> dict[str, Any] | None:
    if path is None:
        return None
    value = json.loads(path.resolve().read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise AEPriorQualificationV03Error(f"{path} must contain one object")
    return value


def _load_receipts(path: Path | None) -> list[dict[str, Any]] | None:
    if path is None:
        return None
    resolved = path.resolve()
    if resolved.is_dir():
        try:
            files = sorted(resolved.glob("*.json"), key=lambda item: int(item.stem))
        except ValueError as error:
            raise AEPriorQualificationV03Error(
                f"{path} receipt filenames must be numeric execution indexes"
            ) from error
        if [int(item.stem) for item in files] != list(range(len(files))):
            raise AEPriorQualificationV03Error(
                f"{path} receipt indexes must be complete from zero"
            )
        values = [_load(item) for item in files]
    else:
        values = json.loads(resolved.read_text(encoding="utf-8"))
    if not isinstance(values, list) or any(
        not isinstance(value, dict) for value in values
    ):
        raise AEPriorQualificationV03Error(f"{path} must contain a receipt list")
    return values


def _external_path(path: Path, *, role: str) -> Path:
    resolved = path.resolve()
    if resolved == ROOT or resolved.is_relative_to(ROOT):
        raise AEPriorQualificationV03Error(
            f"{role} must be outside the code worktree: {resolved}"
        )
    return resolved


def _reject_serial_output_root(path: Path) -> None:
    if not path.exists():
        return
    collisions = sorted(name for name in SERIAL_OUTPUT_MARKERS if (path / name).exists())
    if collisions:
        raise AEPriorQualificationV03Error(
            "shard root resembles an existing serial phase output; refusing to touch it: "
            + ", ".join(collisions)
        )


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--execute-shard", action="store_true")
    mode.add_argument("--merge", action="store_true")
    parser.add_argument("--contract", type=Path, default=DEFAULT_CONTRACT)
    parser.add_argument(
        "--phase",
        choices=(
            "classifier_fit",
            "classifier_validation",
            "prospective_screen",
            "confirmation",
        ),
        required=True,
    )
    parser.add_argument("--shard-root", type=Path, required=True)
    parser.add_argument("--shard-count", type=int, required=True)
    parser.add_argument("--shard-index", type=int)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--import-prefix", type=Path)
    parser.add_argument("--import-prefix-count", type=int, default=0)
    parser.add_argument("--fit-report", type=Path)
    parser.add_argument("--fit-plan", type=Path)
    parser.add_argument("--fit-receipts", type=Path)
    parser.add_argument("--validation-report", type=Path)
    parser.add_argument("--validation-plan", type=Path)
    parser.add_argument("--validation-receipts", type=Path)
    parser.add_argument("--screen-report", type=Path)
    parser.add_argument("--screen-plan", type=Path)
    parser.add_argument("--screen-receipts", type=Path)
    parser.add_argument("--selection", type=Path)
    return parser


def main() -> int:
    args = _parser().parse_args()
    shard_root = _external_path(args.shard_root, role="shard root")
    _reject_serial_output_root(shard_root)
    if args.shard_count < 1:
        raise AEPriorQualificationV03Error("--shard-count must be positive")
    if args.execute_shard and args.shard_index is None:
        raise AEPriorQualificationV03Error("--execute-shard requires --shard-index")
    if args.execute_shard and args.output is not None:
        raise AEPriorQualificationV03Error("--output belongs only to --merge")
    if args.merge and args.output is None:
        raise AEPriorQualificationV03Error("--merge requires --output")
    if args.merge and args.shard_index is not None:
        raise AEPriorQualificationV03Error("--shard-index belongs only to --execute-shard")
    if (args.import_prefix is None) != (args.import_prefix_count == 0):
        raise AEPriorQualificationV03Error(
            "--import-prefix and a positive --import-prefix-count are required together"
        )
    imported_prefix = (
        _external_path(args.import_prefix, role="imported prefix")
        if args.import_prefix is not None
        else None
    )

    contract = _load(args.contract)
    assert contract is not None
    fit_report = _load(args.fit_report)
    fit_plan = _load(args.fit_plan)
    fit_receipts = _load_receipts(args.fit_receipts)
    validation_report = _load(args.validation_report)
    validation_plan = _load(args.validation_plan)
    validation_receipts = _load_receipts(args.validation_receipts)
    screen_report = _load(args.screen_report)
    screen_plan = _load(args.screen_plan)
    screen_receipts = _load_receipts(args.screen_receipts)
    selection = _load(args.selection)
    plan = build_phase_plan(
        ROOT,
        args.contract.resolve(),
        args.phase,
        fit_report=fit_report,
        fit_plan=fit_plan,
        fit_receipts=fit_receipts,
        validation_report=validation_report,
        validation_plan=validation_plan,
        validation_receipts=validation_receipts,
        screen_report=screen_report,
        screen_plan=screen_plan,
        screen_receipts=screen_receipts,
        selection=selection,
    )
    errors = validate_plan(plan)
    if errors:
        raise AEPriorQualificationV03Error("invalid plan: " + "; ".join(errors))

    if args.execute_shard:
        summary = execute_shard(
            ROOT,
            plan,
            shard_root,
            shard_index=args.shard_index,
            shard_count=args.shard_count,
            start_execution_index=args.import_prefix_count,
        )
        print(json.dumps(summary, ensure_ascii=False, sort_keys=True), flush=True)
        return 0 if summary["status"] == "completed" else 2

    assert args.output is not None
    output = _external_path(args.output, role="merged output")
    if (
        output == shard_root
        or output.is_relative_to(shard_root)
        or shard_root.is_relative_to(output)
    ):
        raise AEPriorQualificationV03Error(
            "merged output and shard root must be disjoint external directories"
        )
    result = materialize_merged_output(
        contract,
        plan,
        shard_root,
        output,
        shard_count=args.shard_count,
        imported_prefix=imported_prefix,
        imported_prefix_count=args.import_prefix_count,
        fit_report=fit_report,
        validation_report=validation_report,
        screen_report=screen_report,
        selection=selection,
    )
    print(json.dumps(result, ensure_ascii=False, sort_keys=True), flush=True)
    return 0 if result["status"] in MERGED_TERMINAL_STATUSES else 1


if __name__ == "__main__":
    raise SystemExit(main())
