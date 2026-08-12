#!/usr/bin/env python3
"""Build or execute the provider-free Work II A-E v0.3 development phases."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from chemworld.eval.provenance import write_json_atomic
from chemworld.eval.work_ii_ae_prior_qualification_v03 import (
    AEPriorQualificationV03Error,
    build_confirmation_plan,
    build_phase_report,
    build_screen_plan,
    execute_one,
    select_screen_candidates,
    validate_phase_progress,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONTRACT = (
    ROOT / "configs/benchmark/work_ii_ae_prior_distinguishability_v0.3_candidate.json"
)


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise AEPriorQualificationV03Error(f"{path} must contain an object")
    return value


def _write_receipt(output: Path, receipt: dict[str, object]) -> None:
    receipt_path = output / "receipts" / f"{receipt['execution_index']}.json"
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    write_json_atomic(receipt_path, receipt)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", type=Path, default=DEFAULT_CONTRACT)
    parser.add_argument("--phase", choices=("screen", "confirmation"), required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--selection", type=Path)
    parser.add_argument("--screen-report", type=Path)
    parser.add_argument(
        "--plan-only",
        action="store_true",
        help="validate and write the plan without producing experimental data",
    )
    args = parser.parse_args()
    output = args.output.resolve()
    if output.exists():
        raise AEPriorQualificationV03Error("v0.3 output must not already exist")
    contract_path = args.contract.resolve()
    contract = _load(contract_path)
    if args.phase == "screen":
        if args.selection is not None or args.screen_report is not None:
            raise AEPriorQualificationV03Error(
                "screen phase does not accept selection or prior report"
            )
        plan = build_screen_plan(ROOT, contract_path)
    else:
        if args.selection is None or args.screen_report is None:
            raise AEPriorQualificationV03Error(
                "confirmation phase requires the screen report and frozen selection"
            )
        selection = _load(args.selection.resolve())
        screen_report = _load(args.screen_report.resolve())
        plan = build_confirmation_plan(
            ROOT, contract_path, selection, screen_report
        )
    output.mkdir(parents=True)
    write_json_atomic(output / "plan.json", plan)
    if args.plan_only:
        print(json.dumps({"phase": plan["phase"], "primary": len(plan["executions"])}))
        return 0
    receipts: list[dict[str, object]] = []
    total = len(plan["executions"])
    for row in plan["executions"]:
        receipt = execute_one(ROOT, plan, row, output)
        receipts.append(receipt)
        _write_receipt(output, receipt)
        progress_errors = validate_phase_progress(plan, receipts)
        if progress_errors:
            raise AEPriorQualificationV03Error(
                "invalid write-once progress: " + "; ".join(progress_errors)
            )
        completed = len(receipts)
        print(
            json.dumps(
                {
                    "stage": plan["phase"],
                    "completed": completed,
                    "total": total,
                    "failures": sum(
                        1 for item in receipts if item.get("status") != "completed"
                    ),
                }
            ),
            flush=True,
        )
    report = build_phase_report(contract, plan, receipts)
    write_json_atomic(output / "report.json", report)
    if args.phase == "screen":
        selection = select_screen_candidates(contract, report["world_results"])
        write_json_atomic(output / "selection.json", selection)
    print(json.dumps({"status": report["status"], "output": str(output)}), flush=True)
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
