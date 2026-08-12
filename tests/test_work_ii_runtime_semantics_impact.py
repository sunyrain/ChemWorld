from __future__ import annotations

import json
from pathlib import Path

from chemworld.eval.provenance import canonical_json_sha256, file_sha256
from chemworld.eval.work_ii_runtime_semantics_impact import (
    audit_evidence_report,
    build_runtime_semantics_impact_audit,
)


def _write(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value), encoding="utf-8")


def test_static_audit_marks_bound_destructive_measurement_affected(tmp_path: Path) -> None:
    trajectory = tmp_path / "runs/trajectory.jsonl"
    trajectory.parent.mkdir(parents=True)
    trajectory.write_text(
        json.dumps(
            {
                "task_id": "reaction-to-assay",
                "action": {"operation": "measure", "instrument": "hplc"},
                "transaction_status": "committed",
            }
        )
        + "\n",
        encoding="utf-8",
    )
    report = tmp_path / "workstreams/flagship_tasks/reports/work-ii-example.json"
    _write(
        report,
        {
            "denominators": {"execution_count": 1},
            "trajectory": {
                "path": "runs/trajectory.jsonl",
                "sha256": file_sha256(trajectory),
                "hash_kind": "file_sha256",
            },
        },
    )

    row = audit_evidence_report(tmp_path, report)

    assert row["classification"] == "affected"
    assert row["required_action"] == "pending_requalification"
    assert row["findings"]["destructive_measurement_count"] == 1


def test_static_audit_detects_reaction_without_positive_catalyst_charge(tmp_path: Path) -> None:
    report = tmp_path / "workstreams/flagship_tasks/reports/work-ii-example.json"
    _write(
        report,
        {
            "rows": [
                {"action": {"operation": "add_reagent", "amount_mol": 0.01}},
                {"action": {"operation": "heat", "duration_s": 10.0}},
            ]
        },
    )

    row = audit_evidence_report(tmp_path, report)

    assert row["classification"] == "affected"
    assert row["findings"]["uncharged_reaction_operation_count"] == 1


def test_static_audit_marks_missing_bound_actions_unknown(tmp_path: Path) -> None:
    report = tmp_path / "workstreams/flagship_tasks/reports/work-ii-example.json"
    _write(
        report,
        {
            "denominators": {"experiment_count": 3},
            "trajectory": {
                "path": "runs/missing.jsonl",
                "sha256": "0" * 64,
                "hash_kind": "file_sha256",
            },
        },
    )

    row = audit_evidence_report(tmp_path, report)

    assert row["classification"] == "unknown"
    assert row["binding_audit"]["missing_paths"] == ["runs/missing.jsonl"]


def test_positive_catalyst_charge_and_non_execution_admin_are_unaffected(
    tmp_path: Path,
) -> None:
    action_report = tmp_path / "workstreams/flagship_tasks/reports/work-ii-action.json"
    admin_report = tmp_path / "workstreams/flagship_tasks/reports/work-ii-admin.json"
    _write(
        action_report,
        {
            "rows": [
                {
                    "action": {
                        "operation": "add_catalyst",
                        "catalyst_amount_mol": 0.001,
                    }
                },
                {"action": {"operation": "heat", "duration_s": 10.0}},
            ]
        },
    )
    _write(admin_report, {"status": "planning_only", "formal_result": False})

    report = build_runtime_semantics_impact_audit(
        tmp_path, [action_report, admin_report]
    )

    assert report["status"] == "passed"
    assert report["participant_outcome_values_used_for_classification"] is False
    assert report["formal_execution_authorized"] is False
    assert report["denominators"]["unaffected_report_count"] == 2
    embedded_hash = report["audit_sha256"]
    assert embedded_hash == canonical_json_sha256(
        {key: value for key, value in report.items() if key != "audit_sha256"}
    )


def test_rejected_trigger_actions_do_not_create_affected_classification(tmp_path: Path) -> None:
    report = tmp_path / "workstreams/flagship_tasks/reports/work-ii-rejected.json"
    _write(
        report,
        {
            "rows": [
                {
                    "action": {"operation": "measure", "instrument": "hplc"},
                    "transaction_status": "validation_failed",
                },
                {
                    "action": {"operation": "heat", "duration_s": 10.0},
                    "transaction_status": "validation_failed",
                },
            ]
        },
    )

    row = audit_evidence_report(tmp_path, report)

    assert row["classification"] == "unaffected"
    assert row["findings"]["destructive_measurement_count"] == 0
    assert row["findings"]["uncharged_reaction_operation_count"] == 0


def test_final_assay_resets_catalyst_charge_before_next_batch(tmp_path: Path) -> None:
    report = tmp_path / "workstreams/flagship_tasks/reports/work-ii-two-batches.json"
    _write(
        report,
        {
            "rows": [
                {
                    "action": {
                        "operation": "add_catalyst",
                        "catalyst_amount_mol": 0.001,
                    },
                    "experiment_index": 0,
                },
                {
                    "action": {"operation": "heat", "duration_s": 10.0},
                    "experiment_index": 0,
                },
                {
                    "action": {"operation": "measure", "instrument": "final_assay"},
                    "transaction_status": "validation_failed",
                    "experiment_index": 0,
                },
                {
                    "action": {"operation": "heat", "duration_s": 10.0},
                    "experiment_index": 1,
                },
            ]
        },
    )

    row = audit_evidence_report(tmp_path, report)

    assert row["classification"] == "affected"
    assert row["findings"]["destructive_measurement_count"] == 0
    assert row["findings"]["uncharged_reaction_operation_count"] == 1


def test_canonical_json_binding_uses_declared_hash_kind(tmp_path: Path) -> None:
    child = tmp_path / "runs/child.json"
    child_value = {"rows": [{"action": {"operation": "add_reagent"}}]}
    _write(child, child_value)
    report = tmp_path / "workstreams/flagship_tasks/reports/work-ii-canonical.json"
    _write(
        report,
        {
            "denominators": {"execution_count": 1},
            "binding": {
                "path": "runs/child.json",
                "sha256": canonical_json_sha256(child_value),
                "hash_kind": "canonical_json_sha256",
            },
        },
    )

    row = audit_evidence_report(tmp_path, report)

    assert row["classification"] == "unaffected"
    assert row["binding_audit"]["hash_drift_paths"] == []


def test_digest_without_hash_kind_remains_unknown(tmp_path: Path) -> None:
    child = tmp_path / "runs/child.json"
    child_value = {"rows": [{"action": {"operation": "add_reagent"}}]}
    _write(child, child_value)
    report = tmp_path / "workstreams/flagship_tasks/reports/work-ii-ambiguous.json"
    _write(
        report,
        {
            "denominators": {"execution_count": 1},
            "binding": {
                "path": "runs/child.json",
                "sha256": file_sha256(child),
            },
        },
    )

    row = audit_evidence_report(tmp_path, report)

    assert row["classification"] == "unknown"
    assert row["binding_audit"]["missing_paths"] == [
        "runs/child.json#missing_hash_kind"
    ]


def test_default_discovery_excludes_prior_impact_audit(tmp_path: Path) -> None:
    reports = tmp_path / "workstreams/flagship_tasks/reports"
    _write(reports / "work-ii-admin.json", {"status": "planning_only"})
    _write(
        reports / "work-ii-runtime-semantics-impact-audit-old.json",
        {"denominators": {"execution_count": 999}},
    )

    result = build_runtime_semantics_impact_audit(tmp_path)

    assert result["denominators"]["report_count"] == 1


def test_default_discovery_includes_current_pre_work_ii_named_evidence(
    tmp_path: Path,
) -> None:
    reports = tmp_path / "workstreams/flagship_tasks/reports"
    _write(
        reports / "static-s0-v1.2-three-arm-information-campaign-summary.json",
        {"status": "completed", "formal_result": True},
    )
    _write(
        reports / "static-s0-five-task-postqualification-campaign-summary.json",
        {"status": "completed", "formal_result": False},
    )
    _write(reports / "unrelated-static-report.json", {"status": "completed"})

    result = build_runtime_semantics_impact_audit(tmp_path)

    assert result["denominators"]["report_count"] == 2
    assert {row["report_path"] for row in result["reports"]} == {
        "workstreams/flagship_tasks/reports/"
        "static-s0-v1.2-three-arm-information-campaign-summary.json",
        "workstreams/flagship_tasks/reports/"
        "static-s0-five-task-postqualification-campaign-summary.json",
    }


def test_legacy_accounting_without_bound_actions_fails_closed_unknown(
    tmp_path: Path,
) -> None:
    report = tmp_path / "workstreams/flagship_tasks/reports/static-s0-example.json"
    _write(
        report,
        {
            "status": "completed_audited_formal_three_arm_result",
            "execution": {"all_cells_completed": True},
            "accounting": {"total_physical_experiments": 2280},
        },
    )

    row = audit_evidence_report(tmp_path, report)

    assert row["execution_evidence_detected"] is True
    assert row["classification"] == "unknown"
    assert row["required_action"] == "recover_bound_actions_then_reclassify"


def test_planned_denominator_alone_is_not_execution_evidence(tmp_path: Path) -> None:
    report = tmp_path / "workstreams/flagship_tasks/reports/work-ii-plan.json"
    _write(
        report,
        {
            "status": "planning_only",
            "denominators": {"planned_executions": 75},
            "cells": [{"cell_id": "planned-cell", "status": "planned"}],
        },
    )

    row = audit_evidence_report(tmp_path, report)

    assert row["classification"] == "unaffected"
    assert row["execution_evidence_detected"] is False
    assert row["classification_basis"]["fail_closed_propagation"] is False


def test_admin_binding_propagates_affected_execution_fail_closed(tmp_path: Path) -> None:
    trajectory = tmp_path / "runs/trajectory.jsonl"
    trajectory.parent.mkdir(parents=True)
    trajectory.write_text(
        json.dumps(
            {
                "action": {"operation": "measure", "instrument": "hplc"},
                "transaction_status": "committed",
            }
        )
        + "\n",
        encoding="utf-8",
    )
    report = tmp_path / "workstreams/flagship_tasks/reports/work-ii-admin.json"
    _write(
        report,
        {
            "status": "administrative_receipt",
            "trajectory": {
                "path": "runs/trajectory.jsonl",
                "sha256": file_sha256(trajectory),
                "hash_kind": "file_sha256",
            },
        },
    )

    row = audit_evidence_report(tmp_path, report)

    assert row["classification"] == "affected"
    assert row["classification_basis"] == {
        "direct_action_trigger": False,
        "bound_action_trigger": True,
        "binding_failure": False,
        "execution_summary_without_actions": False,
        "fail_closed_propagation": True,
    }


def test_actual_execution_denominator_without_actions_is_unknown(tmp_path: Path) -> None:
    report = tmp_path / "workstreams/flagship_tasks/reports/work-ii-summary.json"
    _write(
        report,
        {
            "status": "operational_pilot",
            "denominators": {
                "complete_experiments": 12,
                "committed_operations": 72,
            },
        },
    )

    row = audit_evidence_report(tmp_path, report)

    assert row["classification"] == "unknown"
    assert row["execution_evidence_detected"] is True
    assert row["classification_basis"]["execution_summary_without_actions"] is True
    assert row["classification_basis"]["fail_closed_propagation"] is True
