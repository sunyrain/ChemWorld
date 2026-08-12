"""Validation contract for the single-task crystallization topology Q0."""

from __future__ import annotations

import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from chemworld.eval.provenance import canonical_json_sha256, file_sha256
from chemworld.eval.work_ii_c2_admission import validate_c2_source_binding
from chemworld.eval.work_ii_static_topology_q0 import (
    LAW_IDS,
    WORLD_SEED,
    analyze_task,
    registered_cells,
)

TASK_ID = "reaction-to-crystallization"
QUALIFICATION_VERSION = "chemworld-work-ii-crystallization-reversible-q0-0.1"
TASK_REPORT_VERSION = (
    "chemworld-work-ii-crystallization-reversible-q0-task-report-0.1"
)
SUMMARY_VERSION = "chemworld-work-ii-crystallization-reversible-q0-summary-0.1"
PLANNED_EXECUTIONS = len(registered_cells(TASK_ID)) * len(LAW_IDS)


def self_hash(payload: Mapping[str, Any], field: str) -> str:
    return canonical_json_sha256(
        {key: value for key, value in payload.items() if key != field}
    )


def validate_task_report(report: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    if report.get("schema_version") != TASK_REPORT_VERSION:
        errors.append("unexpected crystallization reversible Q0 task-report schema")
    if report.get("qualification_schema_version") != QUALIFICATION_VERSION:
        errors.append("crystallization reversible Q0 qualification schema mismatch")
    if report.get("task_id") != TASK_ID or report.get("world_seed") != WORLD_SEED:
        errors.append("crystallization reversible Q0 task/world binding mismatch")
    if report.get("formal_result") is not False:
        errors.append("crystallization reversible Q0 must not be formal")
    if report.get("provider_call_count") != 0 or report.get("participant_session_count") != 0:
        errors.append("crystallization reversible Q0 must remain provider-free")
    if report.get("report_sha256") != self_hash(report, "report_sha256"):
        errors.append("crystallization reversible Q0 task-report self-hash mismatch")
    rows = report.get("rows")
    audit = report.get("mechanism_audit")
    if not isinstance(rows, list) or not isinstance(audit, Mapping):
        errors.append("crystallization reversible Q0 task report lacks rows or audit")
    else:
        try:
            rebuilt = analyze_task(TASK_ID, rows, audit)
        except (KeyError, TypeError, ValueError) as error:
            errors.append(f"crystallization reversible Q0 cannot be rebuilt: {error}")
        else:
            if report.get("analysis") != rebuilt:
                errors.append("crystallization reversible Q0 analysis mismatch")
    return errors


def validate_summary(
    root: Path,
    summary: Mapping[str, Any],
    *,
    expected_source_binding: Mapping[str, Any] | None = None,
) -> list[str]:
    errors: list[str] = []
    if summary.get("schema_version") != SUMMARY_VERSION:
        errors.append("unexpected crystallization reversible Q0 summary schema")
    if summary.get("qualification_schema_version") != QUALIFICATION_VERSION:
        errors.append("crystallization reversible Q0 summary qualification schema mismatch")
    if summary.get("summary_sha256") != self_hash(summary, "summary_sha256"):
        errors.append("crystallization reversible Q0 summary self-hash mismatch")
    if summary.get("task_id") != TASK_ID or summary.get("world_seed") != WORLD_SEED:
        errors.append("crystallization reversible Q0 summary task/world binding mismatch")
    if summary.get("formal_result") is not False:
        errors.append("crystallization reversible Q0 summary must not be formal")
    if summary.get("provider_call_count") != 0 or summary.get("participant_session_count") != 0:
        errors.append("crystallization reversible Q0 summary must remain provider-free")
    coverage = {
        "law_ids": list(LAW_IDS),
        "grid_cell_count": len(registered_cells(TASK_ID)),
        "planned_execution_count": PLANNED_EXECUTIONS,
    }
    if summary.get("coverage") != coverage:
        errors.append("crystallization reversible Q0 coverage mismatch")
    analysis = summary.get("analysis")
    if not isinstance(analysis, Mapping):
        errors.append("crystallization reversible Q0 summary lacks analysis")
    else:
        passed = analysis.get("passed") is True
        if summary.get("five_world_expansion_authorized") is not passed:
            errors.append("crystallization reversible Q0 expansion decision mismatch")
        if summary.get("denominators") != analysis.get("denominators"):
            errors.append("crystallization reversible Q0 denominator mismatch")
    if summary.get("participant_d1_authorized") is not False:
        errors.append("crystallization reversible Q0 must not authorize D1")
    if summary.get("provider_execution_authorized") is not False:
        errors.append("crystallization reversible Q0 must not authorize provider execution")
    binding = summary.get("c2_source_binding")
    errors.extend(validate_c2_source_binding(root, binding))
    if expected_source_binding is not None and binding != expected_source_binding:
        errors.append("crystallization reversible Q0 C2 source binding differs from cohort")
    raw = summary.get("raw_binding")
    if not isinstance(raw, Mapping):
        errors.append("crystallization reversible Q0 raw binding is missing")
    else:
        try:
            path = (root / str(raw["path"])).resolve()
            path.relative_to(root.resolve())
            if not path.is_file():
                raise ValueError("raw task report is missing")
            if raw.get("sha256") != file_sha256(path):
                errors.append("crystallization reversible Q0 raw file hash mismatch")
            payload = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(payload, dict):
                raise ValueError("raw task report is not an object")
            errors.extend(validate_task_report(payload))
            if raw.get("report_sha256") != payload.get("report_sha256"):
                errors.append("crystallization reversible Q0 embedded report hash mismatch")
            if payload.get("c2_source_binding") != binding:
                errors.append("crystallization reversible Q0 raw/source binding mismatch")
            if payload.get("analysis") != analysis:
                errors.append("crystallization reversible Q0 raw/summary analysis mismatch")
        except (KeyError, OSError, TypeError, ValueError, json.JSONDecodeError) as error:
            errors.append(f"crystallization reversible Q0 raw binding cannot be read: {error}")
    return errors


__all__ = [
    "PLANNED_EXECUTIONS",
    "QUALIFICATION_VERSION",
    "SUMMARY_VERSION",
    "TASK_ID",
    "TASK_REPORT_VERSION",
    "self_hash",
    "validate_summary",
    "validate_task_report",
]
