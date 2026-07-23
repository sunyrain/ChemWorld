from __future__ import annotations

import copy
from pathlib import Path

from scripts.audit_runtime_reachability_vnext import (
    ROOT,
    build_report,
    load_protocol,
    validate_report,
)

from chemworld.world.operations import OPERATION_TYPES


def test_protocol_freezes_all_registered_tasks_and_operations() -> None:
    protocol = load_protocol()
    assert protocol["expected_task_count"] == 15
    assert protocol["expected_operation_count"] == len(OPERATION_TYPES) == 28
    assert len(protocol["expected_task_ids"]) == len(set(protocol["expected_task_ids"]))


def test_report_maps_every_task_operation_service_kernel_and_provider() -> None:
    protocol = load_protocol()
    report = build_report(protocol)

    assert report["task_count"] == 15
    assert report["operation_count"] == 28
    assert report["provider_count"] == 20
    assert set(report["operation_paths"]) == set(OPERATION_TYPES)
    for task_id, task_path in report["task_paths"].items():
        assert task_id in protocol["expected_task_ids"]
        assert task_path["operation_paths"]
        for path in task_path["operation_paths"]:
            assert path["service_id"]
            assert path["kernel_id"].startswith("chemworld.operation.")
            assert path["affected_ledgers"]


def test_report_identifies_only_the_current_shared_lite_upgrade_targets() -> None:
    report = build_report(load_protocol())
    assert report["lite_upgrade_targets"] == {}
    assert report["remaining_gates"] == []
    assert report["orphan_runtime_providers"] == []
    assert report["reference_providers_routed"] == []
    assert report["forbidden_runtime_models"] == []


def test_report_uses_transactional_provider_execution_as_dynamic_evidence() -> None:
    report = build_report(load_protocol(), repository_root=ROOT)
    evidence = report["dynamic_integration_evidence"]
    assert evidence["available"] is True
    assert evidence["passed"] is True
    assert evidence["provider_model_ids"]["mix"] == "chemworld_stability_aware_lle_vnext"
    assert evidence["provider_model_ids"]["distill"] == (
        "chemworld_duty_limited_distillation_vnext"
    )
    assert evidence["provider_model_ids"]["measure"] == (
        "chemworld_validated_synthetic_instruments_v1"
    )


def test_report_is_self_validating_and_tamper_evident() -> None:
    protocol = load_protocol()
    report = build_report(protocol)
    assert validate_report(report, protocol) == []

    tampered = copy.deepcopy(report)
    tampered["task_paths"].pop("partition-discovery")
    errors = validate_report(tampered, protocol)
    assert "task coverage mismatch" in errors
    assert "report hash mismatch" in errors


def test_dynamic_evidence_path_is_repository_local() -> None:
    protocol = load_protocol()
    path = ROOT / protocol["dynamic_integration_evidence"]
    assert path.is_file()
    assert Path(protocol["dynamic_integration_evidence"]).parts[0] == "workstreams"
