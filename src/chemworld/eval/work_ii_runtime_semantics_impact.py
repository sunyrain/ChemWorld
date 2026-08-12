"""Outcome-blind static impact audit for Work II runtime-semantics fixes."""

from __future__ import annotations

import json
from collections import Counter
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from chemworld.eval.provenance import canonical_json_sha256, file_sha256

SCHEMA_VERSION = "chemworld-work-ii-runtime-semantics-impact-audit-0.1"
DESTRUCTIVE_INSTRUMENTS = frozenset({"hplc", "gc", "uvvis", "ph_meter", "final_assay"})
REACTION_OPERATIONS = frozenset({"heat", "wait", "run_flow"})
TERMINAL_OPERATIONS = frozenset({"discard_batch", "final_assay"})
COMPLETED_EXECUTION_STATUSES = frozenset(
    {
        "completed",
        "failed",
        "physical_failure",
        "platform_failure",
        "committed",
        "validation_failed",
        "execution_failed",
    }
)
DEFAULT_WORK_II_REPORT_NAMES = frozenset(
    {
        # These current Work II evidence blocks predate the work-ii-* naming convention.
        "static-s0-v1.2-three-arm-information-campaign-summary.json",
        "static-s0-five-task-postqualification-campaign-summary.json",
    }
)


def _json_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def _looks_like_execution_evidence(value: Any) -> bool:
    if not isinstance(value, Mapping):
        return False
    for key, raw in value.items():
        normalized = str(key).lower()
        actual_count = any(
            token in normalized
            for token in (
                "completed",
                "attempted",
                "committed",
                "failed",
                "provider_call",
                "provider_session",
                "model_call",
                "final_assay",
                "exact_replay_checked",
            )
        )
        execution_unit = any(
            token in normalized
            for token in ("experiment", "execution", "operation", "recipe", "run", "call")
        )
        if (
            actual_count
            and execution_unit
            and "planned" not in normalized
            and not isinstance(raw, bool)
            and isinstance(raw, int | float)
            and raw > 0
        ):
            return True
    for collection_key in ("rows", "cells", "cell_records", "executions"):
        collection = value.get(collection_key)
        if isinstance(collection, list):
            for item in collection:
                if not isinstance(item, Mapping):
                    continue
                if isinstance(item.get("action"), Mapping):
                    return True
                status = item.get("status")
                if isinstance(status, str) and status in COMPLETED_EXECUTION_STATUSES:
                    return True
                for key, raw in item.items():
                    normalized = str(key).lower()
                    if (
                        any(token in normalized for token in ("completed", "attempted"))
                        and any(
                            token in normalized
                            for token in ("experiment", "execution", "recipe", "run")
                        )
                        and raw not in (None, False, 0)
                    ):
                        return True
    denominators = value.get("denominators")
    if isinstance(denominators, Mapping):
        for key, raw in denominators.items():
            normalized = str(key).lower()
            if (
                any(
                    token in normalized
                    for token in ("completed", "attempted", "committed", "failed")
                )
                and any(
                    token in normalized
                    for token in ("experiment", "execution", "operation", "recipe", "run")
                )
                and "planned" not in normalized
                and not isinstance(raw, bool)
                and isinstance(raw, int | float)
                and raw > 0
            ):
                return True
    accounting = value.get("accounting")
    if isinstance(accounting, Mapping):
        for key, raw in _flatten_mapping(accounting):
            normalized = key.lower()
            if (
                any(
                    token in normalized
                    for token in (
                        "experiment",
                        "execution",
                        "operation",
                        "participant_world_cell",
                        "participant_cell",
                        "provider_call",
                    )
                )
                and "planned" not in normalized
                and not isinstance(raw, bool)
                and isinstance(raw, int | float)
                and raw > 0
            ):
                return True
    execution = value.get("execution")
    return isinstance(execution, Mapping) and any(
        execution.get(field) is True
        for field in (
            "all_cells_completed",
            "all_three_arms_completed",
            "all_exact_replay_verified",
            "all_sixty_cells_exact_replay_verified",
        )
    )


def _flatten_mapping(
    value: Mapping[str, Any], prefix: str = ""
) -> list[tuple[str, Any]]:
    rows: list[tuple[str, Any]] = []
    for key, raw in value.items():
        path = f"{prefix}.{key}" if prefix else str(key)
        if isinstance(raw, Mapping):
            rows.extend(_flatten_mapping(raw, path))
        else:
            rows.append((path, raw))
    return rows


def _task_ids(value: Any) -> set[str]:
    found: set[str] = set()
    if isinstance(value, Mapping):
        for key, item in value.items():
            if key == "task_id" and isinstance(item, str):
                found.add(item)
            else:
                found.update(_task_ids(item))
    elif isinstance(value, list):
        for item in value:
            found.update(_task_ids(item))
    return found


def _actions(value: Any) -> list[dict[str, Any]]:
    found: list[dict[str, Any]] = []
    if isinstance(value, Mapping):
        action = value.get("action")
        if isinstance(action, Mapping) and isinstance(action.get("operation"), str):
            return [
                {
                    **dict(action),
                    "transaction_status": value.get("transaction_status"),
                    "experiment_index": value.get("experiment_index"),
                }
            ]
        elif isinstance(value.get("operation"), str):
            return [dict(value)]
        elif isinstance(value.get("operation_type"), str):
            return [
                {
                    "operation": value.get("operation_type"),
                    "instrument": value.get("instrument"),
                    "transaction_status": value.get("transaction_status"),
                    "experiment_index": value.get("experiment_index"),
                }
            ]
        for key, item in value.items():
            if key not in {"action", "agent_view", "agent_trace", "tool_json"}:
                found.extend(_actions(item))
    elif isinstance(value, list):
        for item in value:
            found.extend(_actions(item))
    return found


def _bindings(value: Any) -> list[tuple[str, str | None, str | None]]:
    found: list[tuple[str, str | None, str | None]] = []
    if isinstance(value, Mapping):
        path = value.get("path")
        if isinstance(path, str) and Path(path).suffix.lower() in {".json", ".jsonl"}:
            digest = value.get("sha256")
            hash_kind = value.get("hash_kind")
            found.append(
                (
                    path,
                    digest if isinstance(digest, str) else None,
                    hash_kind if isinstance(hash_kind, str) else None,
                )
            )
        for item in value.values():
            found.extend(_bindings(item))
    elif isinstance(value, list):
        for item in value:
            found.extend(_bindings(item))
    return found


def _action_findings(actions: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    destructive: Counter[str] = Counter()
    uncharged_reaction: Counter[str] = Counter()
    first_destructive_index: int | None = None
    first_uncharged_index: int | None = None
    positive_catalyst_charge = False
    previous_experiment_index: object = None
    for index, action in enumerate(actions):
        operation = str(action.get("operation", ""))
        status = action.get("transaction_status")
        committed_or_planned = status in {None, "committed"}
        experiment_index = action.get("experiment_index")
        if (
            experiment_index is not None
            and previous_experiment_index is not None
            and experiment_index != previous_experiment_index
        ):
            positive_catalyst_charge = False
        if experiment_index is not None:
            previous_experiment_index = experiment_index
        if operation == "add_catalyst" and committed_or_planned:
            amount = action.get("catalyst_amount_mol")
            positive_catalyst_charge = (
                not isinstance(amount, bool)
                and isinstance(amount, int | float)
                and float(amount) > 0.0
            )
        if (
            operation in REACTION_OPERATIONS
            and committed_or_planned
            and not positive_catalyst_charge
        ):
            uncharged_reaction[operation] += 1
            if first_uncharged_index is None:
                first_uncharged_index = index
        instrument = str(action.get("instrument", ""))
        if (
            operation == "measure"
            and instrument in DESTRUCTIVE_INSTRUMENTS
            and committed_or_planned
        ):
            destructive[instrument] += 1
            if first_destructive_index is None:
                first_destructive_index = index
        if operation in TERMINAL_OPERATIONS or (
            operation == "measure" and action.get("instrument") == "final_assay"
        ):
            positive_catalyst_charge = False
    return {
        "action_count": len(actions),
        "destructive_measurement_count": sum(destructive.values()),
        "uncharged_reaction_operation_count": sum(uncharged_reaction.values()),
        "destructive_measurements_by_instrument": dict(sorted(destructive.items())),
        "uncharged_reaction_operations_by_operation": dict(
            sorted(uncharged_reaction.items())
        ),
        "first_destructive_measurement_action_index": first_destructive_index,
        "first_uncharged_reaction_action_index": first_uncharged_index,
    }


def audit_evidence_report(root: Path, report_path: Path) -> dict[str, Any]:
    root = root.resolve()
    report_path = report_path.resolve()
    report = _json_object(report_path)
    inspected: list[dict[str, Any]] = []
    missing: list[str] = []
    hash_drift: list[str] = []
    artifact_findings: list[dict[str, Any]] = []
    execution_evidence_sources: list[str] = []
    task_ids = _task_ids(report)
    execution_evidence = _looks_like_execution_evidence(report)
    queue: list[tuple[Path, str | None, str | None, Any]] = [
        (report_path, None, "file_sha256", report)
    ]
    queued = {report_path}
    while queue:
        path, expected_sha, hash_kind, value = queue.pop(0)
        actual_sha = file_sha256(path)
        declared_sha = (
            canonical_json_sha256(value)
            if hash_kind == "canonical_json_sha256"
            else actual_sha
        )
        if expected_sha is not None and declared_sha != expected_sha:
            hash_drift.append(path.relative_to(root).as_posix())
        actions = _actions(value)
        findings = _action_findings(actions)
        artifact_findings.append(findings)
        artifact_execution_evidence = bool(actions) or _looks_like_execution_evidence(value)
        execution_evidence = execution_evidence or artifact_execution_evidence
        if artifact_execution_evidence:
            execution_evidence_sources.append(path.relative_to(root).as_posix())
        task_ids.update(_task_ids(value))
        inspected.append(
            {
                "path": path.relative_to(root).as_posix(),
                "sha256": actual_sha,
                "action_count": len(actions),
                "findings": findings,
            }
        )
        for relative, digest, child_hash_kind in _bindings(value):
            candidate = (root / relative).resolve()
            if not candidate.is_relative_to(root):
                missing.append(relative)
                continue
            if candidate in queued:
                continue
            queued.add(candidate)
            if not candidate.is_file():
                missing.append(relative)
                continue
            try:
                child = (
                    [
                        json.loads(line)
                        for line in candidate.read_text(encoding="utf-8").splitlines()
                        if line.strip()
                    ]
                    if candidate.suffix == ".jsonl"
                    else _json_object(candidate)
                )
            except (OSError, UnicodeError, json.JSONDecodeError, ValueError):
                missing.append(relative)
                continue
            if digest is not None and child_hash_kind is None:
                missing.append(f"{relative}#missing_hash_kind")
            queue.append((candidate, digest, child_hash_kind, child))
    destructive_by_instrument: Counter[str] = Counter()
    uncharged_by_operation: Counter[str] = Counter()
    for item in artifact_findings:
        destructive_by_instrument.update(item["destructive_measurements_by_instrument"])
        uncharged_by_operation.update(
            item["uncharged_reaction_operations_by_operation"]
        )
    findings = {
        "action_count": sum(item["action_count"] for item in artifact_findings),
        "destructive_measurement_count": sum(
            item["destructive_measurement_count"] for item in artifact_findings
        ),
        "uncharged_reaction_operation_count": sum(
            item["uncharged_reaction_operation_count"] for item in artifact_findings
        ),
        "destructive_measurements_by_instrument": dict(
            sorted(destructive_by_instrument.items())
        ),
        "uncharged_reaction_operations_by_operation": dict(
            sorted(uncharged_by_operation.items())
        ),
    }
    trigger_ids = []
    if findings["destructive_measurement_count"]:
        trigger_ids.append("destructive_measurement_pre_withdrawal_observation_fix")
    if findings["uncharged_reaction_operation_count"]:
        trigger_ids.append("zero_dose_catalyst_modifier_fix")
    if trigger_ids:
        classification = "affected"
        required_action = "pending_requalification"
    elif missing or hash_drift or (execution_evidence and not findings["action_count"]):
        classification = "unknown"
        required_action = "recover_bound_actions_then_reclassify"
    else:
        classification = "unaffected"
        required_action = "no_runtime_semantics_requalification_required"
    root_findings = artifact_findings[0]
    direct_trigger = bool(
        root_findings["destructive_measurement_count"]
        or root_findings["uncharged_reaction_operation_count"]
    )
    binding_failure = bool(missing or hash_drift)
    execution_without_actions = execution_evidence and not findings["action_count"]
    return {
        "report_path": report_path.relative_to(root).as_posix(),
        "report_sha256": file_sha256(report_path),
        "classification": classification,
        "required_action": required_action,
        "task_ids": sorted(task_ids),
        "execution_evidence_detected": execution_evidence,
        "execution_evidence_sources": sorted(set(execution_evidence_sources)),
        "trigger_ids": trigger_ids,
        "classification_basis": {
            "direct_action_trigger": direct_trigger,
            "bound_action_trigger": bool(trigger_ids) and not direct_trigger,
            "binding_failure": binding_failure,
            "execution_summary_without_actions": execution_without_actions,
            "fail_closed_propagation": (
                classification in {"affected", "unknown"} and not direct_trigger
            ),
        },
        "findings": findings,
        "binding_audit": {
            "inspected_artifact_count": len(inspected),
            "missing_paths": sorted(set(missing)),
            "hash_drift_paths": sorted(set(hash_drift)),
            "artifacts": inspected,
        },
    }


def build_runtime_semantics_impact_audit(
    root: Path,
    report_paths: Sequence[Path] | None = None,
) -> dict[str, Any]:
    root = root.resolve()
    if report_paths is None:
        reports_root = root / "workstreams/flagship_tasks/reports"
        report_paths = sorted(
            path
            for path in reports_root.glob("*.json")
            if (
                path.name.startswith("work-ii-")
                or path.name in DEFAULT_WORK_II_REPORT_NAMES
            )
            and not path.name.startswith("work-ii-runtime-semantics-impact-audit-")
        )
    rows = [audit_evidence_report(root, path) for path in report_paths]
    counts = Counter(row["classification"] for row in rows)
    summary: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "status": (
            "pending_requalification"
            if counts["affected"] or counts["unknown"]
            else "passed"
        ),
        "formal_result": False,
        "provider_call_count": 0,
        "participant_outcome_values_used_for_classification": False,
        "classification_contract": {
            "affected": "a bound action trace statically contains a fixed-semantics trigger",
            "unknown": "execution evidence lacks complete readable hash-consistent action bindings",
            "unaffected": (
                "all readable bindings lack triggers, or the artifact is "
                "non-execution administration"
            ),
            "precedence": ["affected", "unknown", "unaffected"],
        },
        "fixes_audited": [
            "destructive_measurement_pre_withdrawal_observation_fix",
            "zero_dose_catalyst_modifier_fix",
        ],
        "denominators": {
            "report_count": len(rows),
            "affected_report_count": counts["affected"],
            "unknown_report_count": counts["unknown"],
            "unaffected_report_count": counts["unaffected"],
        },
        "formal_execution_authorized": False,
        "requalification_complete": False,
        "reports": rows,
    }
    summary["audit_sha256"] = canonical_json_sha256(summary)
    return summary


__all__ = [
    "SCHEMA_VERSION",
    "audit_evidence_report",
    "build_runtime_semantics_impact_audit",
]
