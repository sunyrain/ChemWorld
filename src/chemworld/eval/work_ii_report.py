"""Traceable formal-analysis dataset construction for Work II."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from chemworld.eval.provenance import canonical_json_sha256
from chemworld.eval.work_ii_analysis import (
    WORK_II_ANALYSIS_ARMS,
    build_cluster_correction_record,
    score_cell_checkpoint_errors,
)
from chemworld.eval.work_ii_blind import validate_blind_evaluation_report
from chemworld.eval.work_ii_formal import (
    FORMAL_RECEIPT_VERSION,
    FORMAL_TERMINAL_STATES,
    WorkIIFormalCellStore,
    validate_formal_preflight,
)
from chemworld.eval.work_ii_truth import validate_evaluator_truth_report

WORK_II_FORMAL_ANALYSIS_DATASET_VERSION = (
    "chemworld-work-ii-formal-analysis-dataset-0.1"
)


def _load_object(path: Path) -> dict[str, Any]:
    import json

    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object")
    return value


def _validate_terminal_receipt(
    receipt: Mapping[str, Any],
    expected_cell: Mapping[str, Any],
) -> list[str]:
    errors: list[str] = []
    result = receipt.get("result")
    expected_receipt_hash = canonical_json_sha256(
        {key: value for key, value in receipt.items() if key != "receipt_sha256"}
    )
    if receipt.get("schema_version") != FORMAL_RECEIPT_VERSION:
        errors.append("unexpected terminal receipt schema")
    if receipt.get("cell") != expected_cell:
        errors.append("terminal receipt cell binding mismatch")
    if receipt.get("cell_key_sha256") != expected_cell.get("cell_key_sha256"):
        errors.append("terminal receipt key mismatch")
    if receipt.get("state") not in FORMAL_TERMINAL_STATES:
        errors.append("terminal receipt state is invalid")
    if not isinstance(result, Mapping) or receipt.get(
        "result_sha256"
    ) != canonical_json_sha256(result if isinstance(result, Mapping) else {}):
        errors.append("terminal receipt result binding mismatch")
    if receipt.get("receipt_sha256") != expected_receipt_hash:
        errors.append("terminal receipt self-hash mismatch")
    return errors


def _truth_packs_by_cluster(
    manifest: Mapping[str, Any],
    truth_packs: Mapping[str, Mapping[str, Any]],
) -> tuple[dict[str, Mapping[str, Any]], list[str]]:
    errors: list[str] = []
    expected_clusters: dict[str, dict[str, Any]] = {}
    for cell in manifest["cells"]:
        cluster_id = str(cell["world_cluster_id"])
        expected_clusters.setdefault(
            cluster_id,
            {
                "task_id": cell["task_id"],
                "world_seed": cell["world_seed"],
            },
        )
    if set(truth_packs) != set(expected_clusters):
        errors.append("truth packs do not cover the exact 25-cluster denominator")
    reports: dict[str, Mapping[str, Any]] = {}
    for cluster_id, expected in expected_clusters.items():
        pack = truth_packs.get(cluster_id)
        if not isinstance(pack, Mapping):
            continue
        plan = pack.get("plan")
        report = pack.get("report")
        if not isinstance(plan, Mapping) or not isinstance(report, Mapping):
            errors.append(f"{cluster_id}: malformed evaluator truth pack")
            continue
        validation_errors = validate_evaluator_truth_report(report, plan)
        if validation_errors:
            errors.extend(f"{cluster_id}: {error}" for error in validation_errors)
        if (
            plan.get("world_cluster_id") != cluster_id
            or plan.get("task_id") != expected["task_id"]
            or plan.get("world_seed") != expected["world_seed"]
            or plan.get("formal_preflight_sha256")
            != manifest.get("preflight_sha256")
        ):
            errors.append(f"{cluster_id}: evaluator truth identity binding mismatch")
        reports[cluster_id] = report
    return reports, errors


def _blind_report_record(
    cell: Mapping[str, Any],
    terminal_state: str,
    blind_packs: Mapping[str, Mapping[str, Any]],
    manifest: Mapping[str, Any],
) -> tuple[dict[str, Any], list[str]]:
    key = str(cell["cell_key_sha256"])
    pack = blind_packs.get(key)
    if terminal_state != "completed":
        errors = []
        if pack is not None:
            errors.append(f"{cell['cell_id']}: non-completed cell has a blind pack")
        return (
            {
                "status": "not_started_participant_cell_not_completed",
                "scheduled_execution_count": 6,
                "completed_execution_count": 0,
                "failed_or_unstarted_execution_count": 6,
                "report_sha256": None,
                "recommendation_gain_over_incumbent": None,
            },
            errors,
        )
    if not isinstance(pack, Mapping):
        return (
            {
                "status": "missing_required_blind_pack",
                "scheduled_execution_count": 6,
                "completed_execution_count": 0,
                "failed_or_unstarted_execution_count": 6,
                "report_sha256": None,
                "recommendation_gain_over_incumbent": None,
            },
            [f"{cell['cell_id']}: completed cell lacks a blind pack"],
        )
    plan = pack.get("plan")
    report = pack.get("report")
    receipts = pack.get("receipts")
    if (
        not isinstance(plan, Mapping)
        or not isinstance(report, Mapping)
        or not isinstance(receipts, list)
        or not all(isinstance(item, Mapping) for item in receipts)
    ):
        return (
            {
                "status": "malformed_blind_pack",
                "scheduled_execution_count": 6,
                "completed_execution_count": 0,
                "failed_or_unstarted_execution_count": 6,
                "report_sha256": None,
                "recommendation_gain_over_incumbent": None,
            },
            [f"{cell['cell_id']}: malformed blind pack"],
        )
    errors = [
        f"{cell['cell_id']}: {error}"
        for error in validate_blind_evaluation_report(report, plan, receipts)
    ]
    if (
        plan.get("cell_key_sha256") != key
        or plan.get("formal_preflight_sha256") != manifest.get("preflight_sha256")
    ):
        errors.append(f"{cell['cell_id']}: blind evaluator identity binding mismatch")
    completed = int(report.get("completed_execution_count", 0))
    return (
        {
            "status": report.get("status"),
            "scheduled_execution_count": 6,
            "completed_execution_count": completed,
            "failed_or_unstarted_execution_count": 6 - completed,
            "report_sha256": report.get("report_sha256"),
            "recommendation_gain_over_incumbent": report.get(
                "recommendation_gain_over_incumbent"
            ),
        },
        errors,
    )


def build_formal_analysis_dataset(
    manifest: Mapping[str, Any],
    terminal_receipts: Sequence[Mapping[str, Any]],
    truth_packs: Mapping[str, Mapping[str, Any]],
    blind_packs: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    """Join all immutable formal artifacts into retained cell and cluster rows."""

    manifest_errors = validate_formal_preflight(manifest)
    if manifest_errors:
        raise ValueError("invalid formal manifest: " + "; ".join(manifest_errors))
    if manifest.get("formal_execution_allowed") is not True or manifest.get(
        "blocking_requirements"
    ):
        raise ValueError("formal analysis requires an authorized completed manifest")
    cells = {
        str(cell["cell_key_sha256"]): dict(cell)
        for cell in manifest.get("cells", [])
        if isinstance(cell, Mapping)
    }
    receipts: dict[str, Mapping[str, Any]] = {}
    errors: list[str] = []
    for receipt in terminal_receipts:
        key = str(receipt.get("cell_key_sha256", ""))
        if key not in cells or key in receipts:
            errors.append("terminal receipts contain an unexpected or duplicate cell")
            continue
        receipt_errors = _validate_terminal_receipt(receipt, cells[key])
        errors.extend(f"{cells[key]['cell_id']}: {error}" for error in receipt_errors)
        receipts[key] = receipt
    if set(receipts) != set(cells):
        errors.append("terminal receipts do not cover all 75 formal cells")

    truth_reports, truth_errors = _truth_packs_by_cluster(manifest, truth_packs)
    errors.extend(truth_errors)
    cell_rows: list[dict[str, Any]] = []
    cluster_arm_rows: dict[str, dict[str, dict[str, Any]]] = {}
    for cell in manifest["cells"]:
        key = str(cell["cell_key_sha256"])
        receipt = receipts.get(key)
        if receipt is None:
            continue
        result = receipt.get("result")
        result = result if isinstance(result, Mapping) else {}
        analysis = result.get("analysis")
        analysis = analysis if isinstance(analysis, Mapping) else {}
        truth_report = truth_reports.get(str(cell["world_cluster_id"]), {})
        evaluator_truth = truth_report.get("truth")
        evaluator_truth = evaluator_truth if isinstance(evaluator_truth, Mapping) else {}
        score = score_cell_checkpoint_errors(
            analysis,
            evaluator_truth,
            terminal_state=str(receipt["state"]),
        )
        blind, blind_errors = _blind_report_record(
            cell,
            str(receipt["state"]),
            blind_packs,
            manifest,
        )
        errors.extend(blind_errors)
        trajectory = result.get("trajectory")
        trajectory = trajectory if isinstance(trajectory, Mapping) else None
        row = {
            "schedule_index": cell["schedule_index"],
            "cell_id": cell["cell_id"],
            "cell_key_sha256": key,
            "world_cluster_id": cell["world_cluster_id"],
            "task_id": cell["task_id"],
            "prior_arm": cell["prior_arm"],
            "terminal_state": receipt["state"],
            "terminal_reason_code": receipt["reason_code"],
            "terminal_receipt_sha256": receipt["receipt_sha256"],
            "participant_trajectory": trajectory,
            "evaluator_truth_report_sha256": truth_report.get("report_sha256"),
            "checkpoint_error": score,
            "blind_outcome": blind,
            "provider_receipt_count": result.get("provider_receipt_count", 0),
            "operation_attempt_count": analysis.get("operation_attempt_count", 0),
        }
        cell_rows.append(row)
        cluster_arm_rows.setdefault(str(cell["world_cluster_id"]), {})[
            str(cell["prior_arm"])
        ] = score

    cluster_rows: list[dict[str, Any]] = []
    for cluster_id, arm_rows in cluster_arm_rows.items():
        if set(arm_rows) != set(WORK_II_ANALYSIS_ARMS):
            errors.append(f"{cluster_id}: cluster lacks its exact arm triplet")
            continue
        first = next(row for row in cell_rows if row["world_cluster_id"] == cluster_id)
        contrast = build_cluster_correction_record(arm_rows)
        cluster_rows.append(
            {
                "world_cluster_id": cluster_id,
                "task_id": first["task_id"],
                "evaluator_truth_report_sha256": first[
                    "evaluator_truth_report_sha256"
                ],
                "arm_terminal_receipt_sha256": {
                    row["prior_arm"]: row["terminal_receipt_sha256"]
                    for row in cell_rows
                    if row["world_cluster_id"] == cluster_id
                },
                **contrast,
            }
        )
    cluster_rows.sort(key=lambda row: str(row["world_cluster_id"]))
    state_counts = {
        state: sum(row["terminal_state"] == state for row in cell_rows)
        for state in sorted(FORMAL_TERMINAL_STATES)
    }
    blind_completed = sum(
        int(row["blind_outcome"]["completed_execution_count"]) for row in cell_rows
    )
    report: dict[str, Any] = {
        "schema_version": WORK_II_FORMAL_ANALYSIS_DATASET_VERSION,
        "formal_result": True,
        "status": "passed" if not errors else "failed",
        "formal_preflight_sha256": manifest["preflight_sha256"],
        "expected_cell_count": 75,
        "retained_cell_count": len(cell_rows),
        "expected_cluster_count": 25,
        "cluster_contrast_count": len(cluster_rows),
        "state_counts": state_counts,
        "evaluator_truth_execution_count": sum(
            int(pack["report"].get("truth_query_count", 0))
            for pack in truth_packs.values()
            if isinstance(pack, Mapping) and isinstance(pack.get("report"), Mapping)
        ),
        "evaluator_truth_query_metric_count": sum(
            int(pack["report"].get("truth_query_metric_count", 0))
            for pack in truth_packs.values()
            if isinstance(pack, Mapping) and isinstance(pack.get("report"), Mapping)
        ),
        "blind_scheduled_execution_count": 450,
        "blind_completed_execution_count": blind_completed,
        "blind_failed_or_unstarted_execution_count": 450 - blind_completed,
        "primary_estimand": (
            "(E_misindexed_pre-E_misindexed_final)-"
            "(E_aligned_pre-E_aligned_final)"
        ),
        "statistical_inference_included": False,
        "cell_rows": cell_rows,
        "cluster_rows": cluster_rows,
        "errors": errors,
    }
    report["dataset_sha256"] = canonical_json_sha256(report)
    return report


def load_formal_analysis_dataset(
    manifest: Mapping[str, Any],
    execution_root: Path,
    truth_root: Path,
    blind_root: Path,
) -> dict[str, Any]:
    """Load the frozen filesystem layout and build the formal analysis dataset."""

    store = WorkIIFormalCellStore(execution_root / "store", manifest)
    audit = store.audit()
    if audit.get("complete") is not True:
        raise ValueError("formal participant store is not terminal-complete")
    terminal_receipts = [
        store.load_terminal(str(cell["cell_key_sha256"]))
        for cell in manifest["cells"]
    ]
    cluster_ids = sorted({str(cell["world_cluster_id"]) for cell in manifest["cells"]})
    truth_packs = {
        cluster_id: {
            "plan": _load_object(truth_root / cluster_id / "plan.json"),
            "report": _load_object(truth_root / cluster_id / "report.json"),
        }
        for cluster_id in cluster_ids
    }
    blind_packs: dict[str, dict[str, Any]] = {}
    for receipt in terminal_receipts:
        if receipt["state"] != "completed":
            continue
        key = str(receipt["cell_key_sha256"])
        root = blind_root / key
        report = _load_object(root / "report.json")
        receipt_hashes = report.get("receipt_sha256")
        if not isinstance(receipt_hashes, list):
            raise ValueError(f"{key}: blind report lacks receipt bindings")
        loaded_receipts = [
            _load_object(path) for path in sorted((root / "executions").glob("*/receipt.json"))
        ]
        by_hash = {str(item.get("receipt_sha256")): item for item in loaded_receipts}
        ordered = [by_hash[str(digest)] for digest in receipt_hashes]
        blind_packs[key] = {
            "plan": _load_object(root / "plan.json"),
            "report": report,
            "receipts": ordered,
        }
    return build_formal_analysis_dataset(
        manifest,
        terminal_receipts,
        truth_packs,
        blind_packs,
    )


__all__ = [
    "WORK_II_FORMAL_ANALYSIS_DATASET_VERSION",
    "build_formal_analysis_dataset",
    "load_formal_analysis_dataset",
]
