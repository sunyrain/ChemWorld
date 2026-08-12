#!/usr/bin/env python3
"""Plan or execute one provider-free Work II A-E v0.3 development phase."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from chemworld.eval.provenance import write_json_atomic
from chemworld.eval.work_ii_ae_prior_qualification_v03 import (
    AEPriorQualificationV03Error,
    build_development_summary,
    build_phase_plan,
    build_phase_report,
    execute_one,
    select_screen_loci,
    validate_phase_progress,
    validate_plan,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONTRACT = (
    ROOT / "configs/benchmark/work_ii_ae_prior_distinguishability_v0.3_candidate.json"
)


def _load(path: Path | None) -> dict[str, object] | None:
    if path is None:
        return None
    value = json.loads(path.resolve().read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise AEPriorQualificationV03Error(f"{path} must contain one object")
    return value


def _load_receipts(path: Path | None) -> list[dict[str, object]] | None:
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
        payload = json.loads(resolved.read_text(encoding="utf-8"))
        if not isinstance(payload, list):
            raise AEPriorQualificationV03Error(f"{path} must contain one receipt list")
        values = payload
    if any(not isinstance(value, dict) for value in values):
        raise AEPriorQualificationV03Error(f"{path} contains a non-object receipt")
    return values  # type: ignore[return-value]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
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
    parser.add_argument("--output", type=Path, required=True)
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
    parser.add_argument("--plan-only", action="store_true")
    args = parser.parse_args()
    output = args.output.resolve()
    if output.exists():
        raise AEPriorQualificationV03Error("v0.3 output must not already exist")
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
    output.mkdir(parents=True)
    write_json_atomic(output / "plan.json", plan)
    if args.plan_only:
        print(
            json.dumps(
                {
                    "phase": plan["phase"],
                    "primary": plan["denominators"]["primary_executions"],
                    "exact_replay": plan["denominators"]["exact_replays"],
                }
            )
        )
        return 0
    receipts: list[dict[str, object]] = []
    total = len(plan["executions"])
    for row in plan["executions"]:
        receipt = execute_one(ROOT, plan, row, output)
        receipts.append(receipt)
        receipt_path = output / "receipts" / f"{receipt['execution_index']}.json"
        receipt_path.parent.mkdir(parents=True, exist_ok=True)
        write_json_atomic(receipt_path, receipt)
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
                    "throughput_denominator": total,
                    "platform_failures": sum(
                        row["status"] == "platform_failure" for row in receipts
                    ),
                }
            ),
            flush=True,
        )
        # The failing receipt is durable before stopping; no next unit starts.
        if receipt["status"] == "platform_failure":
            write_json_atomic(
                output / "platform-failure.json",
                {
                    "restart_required_from_execution_zero": True,
                    "failed_execution_id": receipt["execution_id"],
                    "failure": receipt["failure"],
                },
            )
            return 2
    contract = _load(args.contract)
    assert contract is not None
    report = build_phase_report(
        contract, plan, receipts, fit_report=fit_report
    )
    write_json_atomic(output / "report.json", report)
    if args.phase == "prospective_screen":
        selection = select_screen_loci(contract, report["locus_results"])
        write_json_atomic(output / "selection.json", selection)
    if args.phase == "confirmation":
        assert fit_report and validation_report and screen_report and selection
        summary = build_development_summary(
            contract,
            fit_report,
            validation_report,
            screen_report,
            selection,
            report,
        )
        write_json_atomic(output / "summary.json", summary)
    print(json.dumps({"status": report["status"], "output": str(output)}), flush=True)
    return 0 if report["status"] in {"completed", "passed", "no_eligible_tasks"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
