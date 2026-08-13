#!/usr/bin/env python3
"""Run the frozen provider-free crystallization reversible-topology Q0."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from time import perf_counter
from typing import Any

try:
    from scripts.run_work_ii_static_topology_q0 import _execute, _mechanism_audit
except ModuleNotFoundError:
    from run_work_ii_static_topology_q0 import (  # type: ignore[no-redef]
        _execute,
        _mechanism_audit,
    )

from chemworld.eval.provenance import file_sha256, write_json_atomic
from chemworld.eval.work_ii_crystallization_reversible_q0 import (
    PLANNED_EXECUTIONS,
    QUALIFICATION_VERSION,
    SUMMARY_VERSION,
    TASK_ID,
    TASK_REPORT_VERSION,
    self_hash,
    validate_summary,
    validate_task_report,
)
from chemworld.eval.work_ii_execution_mode import (
    ExecutionMode,
    build_execution_envelope,
    prepare_execution_context,
)
from chemworld.eval.work_ii_static_topology_q0 import (
    LAW_IDS,
    WORLD_SEED,
    analyze_task,
    registered_cells,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_ROOT = (
    ROOT / "runs/development/work-ii-crystallization-reversible-q0-seed0-20260812"
)
RELEASE_OUTPUT_ROOT = ROOT / "runs/release/work-ii-crystallization-reversible-q0"
DEFAULT_SUMMARY = (
    ROOT
    / "workstreams/flagship_tasks/reports/"
    "work-ii-crystallization-reversible-topology-q0-seed0-20260812.json"
)
RELEASE_SUMMARY = (
    ROOT
    / "workstreams/flagship_tasks/reports/"
    "work-ii-crystallization-release-reversible-topology-q0.json"
)


def _emit(*, completed: int, started: float, row: dict[str, Any]) -> None:
    elapsed = perf_counter() - started
    rate = completed / max(elapsed, 1.0e-9)
    print(
        json.dumps(
            {
                "stage": "paired_execution",
                "completed": completed,
                "total": PLANNED_EXECUTIONS,
                "throughput_executions_per_minute": round(rate * 60.0, 2),
                "eta_s": round((PLANNED_EXECUTIONS - completed) / rate, 1),
                "cell_id": row["cell_id"],
                "law_id": row["law_id"],
                "status": row["status"],
            },
            sort_keys=True,
        ),
        flush=True,
    )


def run(args: argparse.Namespace) -> dict[str, Any]:
    execution_context = prepare_execution_context(
        ROOT,
        mode=args.execution_mode,
        release_manifest=args.release_manifest,
    )
    if args.output_root.exists() or args.summary.exists():
        raise FileExistsError("refusing to overwrite crystallization reversible Q0 outputs")
    args.output_root.mkdir(parents=True)
    started = perf_counter()
    mechanism = _mechanism_audit(TASK_ID)
    rows: list[dict[str, Any]] = []
    platform_stop = False
    for cell in registered_cells(TASK_ID):
        for law_id in LAW_IDS:
            row = _execute(
                task_id=TASK_ID,
                cell=cell,
                law_id=law_id,
                output_root=args.output_root,
            )
            rows.append(row)
            _emit(completed=len(rows), started=started, row=row)
            if row["status"] == "platform_failure":
                platform_stop = True
                break
        if platform_stop:
            break
    baseline_hashes = {row["mechanism_hash"] for row in rows if row["law_id"] == "baseline"}
    altered_hashes = {
        row["mechanism_hash"]
        for row in rows
        if row["law_id"] == "reversible_target_pathway"
    }
    mechanism["execution_mechanism_binding_matches"] = (
        len(rows) == PLANNED_EXECUTIONS
        and baseline_hashes == {mechanism["baseline_mechanism_hash"]}
        and altered_hashes == {mechanism["reversible_mechanism_hash"]}
    )
    analysis = analyze_task(TASK_ID, rows, mechanism)
    report: dict[str, Any] = {
        "schema_version": TASK_REPORT_VERSION,
        "qualification_schema_version": QUALIFICATION_VERSION,
        "formal_result": False,
        "provider_call_count": 0,
        "participant_session_count": 0,
        "execution_context": build_execution_envelope(execution_context),
        "task_id": TASK_ID,
        "world_seed": WORLD_SEED,
        "mechanism_audit": mechanism,
        "rows": rows,
        "analysis": analysis,
    }
    report["report_sha256"] = self_hash(report, "report_sha256")
    report_path = args.output_root / "task-report.json"
    write_json_atomic(report_path, report)
    report_errors = validate_task_report(
        report,
        root=ROOT,
        expected_execution_context=execution_context,
    )
    if report_errors:
        raise RuntimeError(
            "invalid crystallization reversible Q0 report: "
            + "; ".join(report_errors)
        )
    passed = analysis["passed"] is True
    summary: dict[str, Any] = {
        "schema_version": SUMMARY_VERSION,
        "qualification_schema_version": QUALIFICATION_VERSION,
        "formal_result": False,
        "provider_call_count": 0,
        "participant_session_count": 0,
        "execution_context": build_execution_envelope(execution_context),
        "task_id": TASK_ID,
        "world_seed": WORLD_SEED,
        "coverage": {
            "law_ids": list(LAW_IDS),
            "grid_cell_count": len(registered_cells(TASK_ID)),
            "planned_execution_count": PLANNED_EXECUTIONS,
        },
        "denominators": analysis["denominators"],
        "analysis": analysis,
        "platform_stop_triggered": platform_stop,
        "five_world_expansion_authorized": passed,
        "participant_d1_authorized": False,
        "provider_execution_authorized": False,
        "decision": (
            "proceed_to_unchanged_five_world_provider_free_qualification"
            if passed
            else "fix_platform_and_rerun_whole_block_from_start"
            if platform_stop
            else "retain_q0_scientific_rejection_and_do_not_expand"
        ),
        "raw_binding": {
            "path": report_path.relative_to(ROOT).as_posix(),
            "sha256": file_sha256(report_path),
            "report_sha256": report["report_sha256"],
        },
        "elapsed_s": round(perf_counter() - started, 3),
    }
    summary["summary_sha256"] = self_hash(summary, "summary_sha256")
    write_json_atomic(args.summary, summary)
    errors = validate_summary(
        ROOT,
        summary,
        expected_execution_context=execution_context,
    )
    if errors:
        raise RuntimeError("invalid crystallization reversible Q0 summary: " + "; ".join(errors))
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--summary", type=Path)
    parser.add_argument(
        "--execution-mode",
        choices=[mode.value for mode in ExecutionMode],
        default=ExecutionMode.DEVELOPMENT.value,
    )
    parser.add_argument("--release-manifest", type=Path)
    args = parser.parse_args()
    if (
        args.execution_mode == ExecutionMode.RELEASE.value
        and args.output_root.resolve() == DEFAULT_OUTPUT_ROOT.resolve()
    ):
        args.output_root = RELEASE_OUTPUT_ROOT
    args.output_root = args.output_root.resolve()
    args.summary = (
        args.summary.resolve()
        if args.summary is not None
        else (
            RELEASE_SUMMARY
            if args.execution_mode == ExecutionMode.RELEASE.value
            else args.output_root / "summary.json"
        ).resolve()
    )
    if args.release_manifest is not None:
        args.release_manifest = args.release_manifest.resolve()
    result = run(args)
    return 0 if result["analysis"]["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
