#!/usr/bin/env python3
"""Recover the full admitted W2-61 yoked condition after a local consumer defect."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from collections.abc import Mapping
from copy import deepcopy
from pathlib import Path
from typing import Any

from run_work_ii_w250_action_aligned_causal_extension import (
    _condition_row,
    _condition_summary,
    _load,
    _result_path,
    _sha256_file,
    _write_once_or_match,
    build_inputs,
    execute,
    provider_free_canary,
)
from work_ii_longitudinal_runtime import Progress

from chemworld.eval.provenance import canonical_json_sha256, write_json_atomic

ROOT = Path(__file__).resolve().parents[1]
NOTE_PATH = (
    "workstreams/flagship_tasks/"
    "WORK_II_W250_ACTION_ALIGNED_CAUSAL_EXTENSION_EXPERIMENT_NOTE.md"
)
SOURCE_ROOTS = {
    "deepseek": ROOT
    / "runs/development/"
    "work-ii-w2-61-deepseek-action-aligned-recipients-v0.1-20260902",
    "codex": ROOT
    / "runs/development/"
    "work-ii-w2-61-codex-action-aligned-recipients-v0.1-20260902-restart2",
}
DEFAULT_OUTPUTS = {
    participant: ROOT
    / "runs/development/"
    / f"work-ii-w2-61-{participant}-yoked-recovery-v0.1-20260902"
    for participant in ("deepseek", "codex")
}
DEFAULT_REPORTS = {
    participant: ROOT
    / "workstreams/flagship_tasks/reports/"
    / f"work-ii-w2-61-{participant}-yoked-recovery-v0.1.json"
    for participant in ("deepseek", "codex")
}
EXPECTED_INCIDENT_KEY_ERRORS = {"deepseek": 39, "codex": 22}
RECOVERY_CONDITION = "yoked_evidence"


def _source_incident(participant: str, base_inputs: Mapping[str, Any]) -> dict[str, Any]:
    source_root = SOURCE_ROOTS[participant]
    input_path = source_root / "input_bundle.json"
    summary_path = source_root / "summary.json"
    if not input_path.is_file() or not summary_path.is_file():
        raise FileNotFoundError(f"retained W2-61 source root is incomplete: {source_root}")
    source_inputs = _load(input_path)
    source_summary = _load(summary_path)
    if source_summary.get("status") != "terminal_complete":
        raise ValueError("retained W2-61 source cohort is not terminal")
    if source_inputs.get("participant") != participant:
        raise ValueError("retained W2-61 source participant drifted")
    if source_inputs.get("input_sha256") != base_inputs.get("input_sha256"):
        raise ValueError("current W2-61 materialization differs from the retained source cohort")

    statuses: Counter[str] = Counter()
    failures: Counter[str] = Counter()
    admitted_results = 0
    for stratum in base_inputs["strata"]:
        if not stratum["admitted"]:
            continue
        path = _result_path(source_root, str(stratum["stratum_id"]), RECOVERY_CONDITION)
        if not path.is_file():
            raise FileNotFoundError(f"retained yoked result is missing: {path}")
        result = _load(path)
        admitted_results += 1
        statuses[str(result.get("status", "missing"))] += 1
        failure_key = f"{result.get('failure_type')}:{result.get('failure_message')}"
        if result.get("status") != "completed":
            failures[failure_key] += 1
    key_errors = failures["KeyError:'category_value'"]
    if key_errors != EXPECTED_INCIDENT_KEY_ERRORS[participant]:
        raise ValueError("retained category-value incident denominator drifted")
    if admitted_results != int(base_inputs["admitted_stratum_count"]):
        raise ValueError("retained admitted yoked denominator drifted")
    return {
        "root": str(source_root.relative_to(ROOT)).replace("\\", "/"),
        "input_bundle": str(input_path.relative_to(ROOT)).replace("\\", "/"),
        "input_bundle_sha256": _sha256_file(input_path),
        "summary": str(summary_path.relative_to(ROOT)).replace("\\", "/"),
        "summary_sha256": _sha256_file(summary_path),
        "source_input_sha256": str(source_inputs["input_sha256"]),
        "admitted_yoked_result_count": admitted_results,
        "status_counts": dict(sorted(statuses.items())),
        "failure_counts": dict(sorted(failures.items())),
        "category_value_key_error_count": key_errors,
        "disposition": "retained_platform_incident_not_overwritten",
    }


def build_recovery_inputs(*, participant: str) -> dict[str, Any]:
    base = build_inputs(participant=participant)
    source_incident = _source_incident(participant, base)
    recovery = deepcopy(base)
    recovery["schema_version"] = "chemworld-work-ii-w2-61-yoked-recovery-input-0.1"
    recovery["study_id"] = f"work-ii-w2-61-{participant}-yoked-recovery-v0.1"
    recovery["experiment_note"] = NOTE_PATH
    recovery["execution_scope"] = "full_admitted_yoked_condition"
    recovery["recovery_condition"] = RECOVERY_CONDITION
    recovery["recipient_execution_order"] = [RECOVERY_CONDITION]
    recovery["original_four_condition_slot_count"] = int(
        base["scheduled_condition_slot_count"]
    )
    recovery["new_recipient_session_count"] = int(base["admitted_stratum_count"])
    recovery["source_incident"] = source_incident
    for stratum in recovery["strata"]:
        stratum["recipient_conditions"] = (
            [RECOVERY_CONDITION] if stratum["admitted"] else []
        )
    recovery.pop("input_sha256", None)
    recovery["input_sha256"] = canonical_json_sha256(recovery)
    return recovery


def recovery_provider_free_canary(inputs: Mapping[str, Any]) -> dict[str, Any]:
    canary = provider_free_canary(inputs)
    return {
        "schema_version": "chemworld-work-ii-w2-61-yoked-recovery-canary-0.1",
        "status": "passed",
        "participant": inputs["participant"],
        "recovery_sessions": inputs["new_recipient_session_count"],
        "checked_admitted_strata": canary["checked_admitted_strata"],
        "checked_yoked_snapshot_schemas": canary["checked_yoked_snapshot_schemas"],
        "candidate_preterminal_reveal_count": canary[
            "candidate_preterminal_reveal_count"
        ],
        "provider_calls": 0,
        "tools": 0,
        "truth_executions": 0,
        "physical_experiments": 0,
        "source_incident_summary_sha256": inputs["source_incident"]["summary_sha256"],
    }


def _provider_ledger(output_root: Path) -> dict[str, Any]:
    usage: Counter[str] = Counter()
    provider_errors = 0
    tool_events = 0
    thread_ids: set[str] = set()
    threads_by_stratum: dict[str, set[str]] = defaultdict(set)
    turn_files = sorted(
        (output_root / "provider-turns").glob(
            f"**/{RECOVERY_CONDITION}/turn-*.json"
        )
    )
    for path in turn_files:
        payload = _load(path)
        receipt = payload.get("receipt")
        receipt = receipt if isinstance(receipt, Mapping) else {}
        tool_events += int(receipt.get("tool_event_count", 0) or 0)
        errors = receipt.get("provider_errors")
        provider_errors += len(errors) if isinstance(errors, list) else 0
        thread_id = receipt.get("thread_id")
        if isinstance(thread_id, str):
            thread_ids.add(thread_id)
            stratum_id = path.parents[1].name
            threads_by_stratum[stratum_id].add(thread_id)
        turn_usage = receipt.get("usage")
        if isinstance(turn_usage, Mapping):
            for key, value in turn_usage.items():
                if isinstance(value, int) and not isinstance(value, bool):
                    usage[str(key)] += value
    continuity_issues = {
        stratum_id: sorted(ids)
        for stratum_id, ids in threads_by_stratum.items()
        if len(ids) != 1
    }
    return {
        "provider_turn_record_count": len(turn_files),
        "unique_thread_count": len(thread_ids),
        "thread_continuity_issue_count": len(continuity_issues),
        "thread_continuity_issues": continuity_issues,
        "tool_event_count": tool_events,
        "provider_error_event_count": provider_errors,
        "usage": dict(sorted(usage.items())),
    }


def analyze_recovery(
    *, inputs: Mapping[str, Any], output_root: Path
) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    terminal_count = 0
    for stratum in inputs["strata"]:
        if not stratum["admitted"]:
            continue
        stratum_id = str(stratum["stratum_id"])
        path = _result_path(output_root, stratum_id, RECOVERY_CONDITION)
        result = (
            _load(path)
            if path.is_file()
            else {
                "condition": RECOVERY_CONDITION,
                "status": "not_started",
                "provider_call_count": 0,
            }
        )
        row = _condition_row(
            stratum=stratum,
            condition=RECOVERY_CONDITION,
            result=result,
        )
        row["source"] = "new_w2_61_yoked_recovery"
        rows.append(row)
        if result.get("status") != "not_started":
            terminal_count += 1
        if result.get("status") != "completed":
            failures.append(
                {
                    "stratum_id": stratum_id,
                    "task_id": str(stratum["task_id"]),
                    "world_seed": int(stratum["world_seed"]),
                    "prior_arm": str(stratum["prior_arm"]),
                    "status": str(result.get("status", "not_started")),
                    "failure_type": result.get("failure_type"),
                    "failure_classification": result.get("failure_classification"),
                    "failure_message": result.get("failure_message"),
                    "provider_call_count": int(
                        result.get("provider_call_count", 0) or 0
                    ),
                }
            )
    expected = int(inputs["new_recipient_session_count"])
    if len(rows) != expected:
        raise ValueError("recovery admitted yoked denominator drifted")
    ledger = _provider_ledger(output_root)
    result_provider_calls = sum(int(row["provider_call_count"]) for row in rows)
    payload = {
        "schema_version": "chemworld-work-ii-w2-61-yoked-recovery-summary-0.1",
        "study_id": inputs["study_id"],
        "formal_result": False,
        "prospective_development_experiment": True,
        "experiment_note": NOTE_PATH,
        "participant": inputs["participant"],
        "model": inputs["model"],
        "reasoning_effort": inputs["reasoning_effort"],
        "status": "terminal_complete" if terminal_count == expected else "partial_retained",
        "input_sha256": inputs["input_sha256"],
        "execution_scope": inputs["execution_scope"],
        "source_incident": deepcopy(dict(inputs["source_incident"])),
        "denominators": {
            "original_scheduled_strata": int(inputs["scheduled_stratum_count"]),
            "original_four_condition_slots": int(
                inputs["original_four_condition_slot_count"]
            ),
            "admitted_yoked_recovery_sessions": expected,
            "terminal_yoked_recovery_sessions": terminal_count,
            "completed_yoked_recovery_sessions": sum(
                row["status"] == "completed" for row in rows
            ),
            "failed_or_interrupted_yoked_recovery_sessions": sum(
                row["status"] not in {"completed", "not_started"} for row in rows
            ),
            "not_started_yoked_recovery_sessions": sum(
                row["status"] == "not_started" for row in rows
            ),
            "provider_calls_from_results": result_provider_calls,
            "provider_turn_records": ledger["provider_turn_record_count"],
            "new_truth_executions": 0,
            "new_physical_experiments": 0,
        },
        "condition_summary": _condition_summary(rows),
        "provider_ledger": ledger,
        "failures": failures,
        "condition_rows": rows,
    }
    payload["summary_sha256"] = canonical_json_sha256(payload)
    return payload


def _first_admitted_inputs(inputs: Mapping[str, Any]) -> dict[str, Any]:
    first = next(row for row in inputs["strata"] if row["admitted"])
    canary_inputs = deepcopy(dict(inputs))
    canary_inputs["strata"] = [deepcopy(first)]
    return canary_inputs


def execute_with_operational_canary(
    *, inputs: Mapping[str, Any], output_root: Path, progress: Progress
) -> None:
    existing = sum(
        _result_path(output_root, str(row["stratum_id"]), RECOVERY_CONDITION).is_file()
        for row in inputs["strata"]
        if row["admitted"]
    )
    if existing == 0:
        canary_inputs = _first_admitted_inputs(inputs)
        execute(inputs=canary_inputs, output_root=output_root, progress=progress)
        canary_stratum = str(canary_inputs["strata"][0]["stratum_id"])
        canary_result = _load(
            _result_path(output_root, canary_stratum, RECOVERY_CONDITION)
        )
        if (
            canary_result.get("failure_type") == "KeyError"
            and "category_value" in str(canary_result.get("failure_message"))
        ):
            halt = {
                "status": "halted_on_recurrent_category_value_platform_defect",
                "stratum_id": canary_stratum,
                "condition": RECOVERY_CONDITION,
            }
            _write_once_or_match(output_root / "halt.json", halt)
            raise RuntimeError("yoked recovery canary reproduced the repaired platform defect")
    execute(inputs=inputs, output_root=output_root, progress=progress)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--participant", choices=("deepseek", "codex"), required=True)
    parser.add_argument("--output-root", type=Path)
    parser.add_argument("--report-output", type=Path)
    parser.add_argument("--materialize", action="store_true")
    parser.add_argument("--provider-free-canary", action="store_true")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--analyze", action="store_true")
    parser.add_argument("--allow-provider-execution", action="store_true")
    args = parser.parse_args()
    if not (args.materialize or args.provider_free_canary or args.execute or args.analyze):
        parser.error("select at least one action")
    if args.execute and not args.allow_provider_execution:
        parser.error("provider execution requires --allow-provider-execution")

    selected_output = args.output_root or DEFAULT_OUTPUTS[args.participant]
    selected_report = args.report_output or DEFAULT_REPORTS[args.participant]
    output_root = selected_output if selected_output.is_absolute() else ROOT / selected_output
    report_output = selected_report if selected_report.is_absolute() else ROOT / selected_report
    output_root.mkdir(parents=True, exist_ok=True)
    progress = Progress(output_root / "progress.jsonl")
    inputs = build_recovery_inputs(participant=args.participant)
    _write_once_or_match(output_root / "input_bundle.json", inputs)
    progress.emit(
        {
            "stage": "w2_61_yoked_recovery_materialized",
            "participant": args.participant,
            "completed_sessions": 0,
            "total_sessions": inputs["new_recipient_session_count"],
            "provider_calls": 0,
            "truth_executions": 0,
            "physical_experiments": 0,
        }
    )
    if args.provider_free_canary:
        canary = recovery_provider_free_canary(inputs)
        _write_once_or_match(output_root / "provider_free_canary.json", canary)
        progress.emit({"stage": "w2_61_yoked_recovery_canary_passed", **canary})
    if args.execute:
        execute_with_operational_canary(
            inputs=inputs,
            output_root=output_root,
            progress=progress,
        )
    if args.execute or args.analyze:
        summary = analyze_recovery(inputs=inputs, output_root=output_root)
        write_json_atomic(output_root / "summary.json", summary)
        if summary["status"] == "terminal_complete":
            write_json_atomic(report_output, summary)
        progress.emit(
            {
                "stage": "w2_61_yoked_recovery_analysis_complete",
                "status": summary["status"],
                **summary["denominators"],
            }
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
