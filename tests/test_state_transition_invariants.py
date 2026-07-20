from __future__ import annotations

import copy

import pytest
from scripts.audit_state_transition_invariants import (
    build_report,
    load_protocol,
    validate_report,
)

from chemworld.world.operations import OPERATION_TYPES


@pytest.fixture(scope="module")
def protocol() -> dict[str, object]:
    return load_protocol()


@pytest.fixture(scope="module")
def report(protocol: dict[str, object]) -> dict[str, object]:
    return build_report(protocol)


def test_protocol_declares_every_operation_and_semantic_once(
    protocol: dict[str, object],
) -> None:
    operations = protocol["operations"]
    assert isinstance(operations, dict)
    assert set(operations) == set(OPERATION_TYPES)
    assert len(operations) == protocol["expected_operation_count"] == 28
    assert {case["semantic"] for case in operations.values()} <= set(protocol["allowed_semantics"])


def test_all_operations_have_positive_repeat_replay_and_atomic_failure_evidence(
    report: dict[str, object],
) -> None:
    results = report["operation_results"]
    assert isinstance(results, dict)
    assert report["control_failures"] == []
    for operation, result in results.items():
        assert operation in OPERATION_TYPES
        checks = result["checks"]
        assert all(checks.values())
        assert result["positive_probe"]["transaction_status"] == "committed"
        assert result["invalid_probe"]["atomic"] is True
        assert result["invalid_probe"]["attempt_consumed"] is True


def test_terminal_and_final_assay_boundaries_fail_closed(
    report: dict[str, object],
) -> None:
    assert report["final_assay_boundary"] == {
        "runtime_guard": True,
        "episode_guard": True,
        "repeated_final_assay_rejected": True,
    }
    terminal = report["post_terminal_boundary"]
    assert terminal["all_process_operations_rejected"] is True
    assert terminal["measurement_remains_available_for_terminal_assay"] is True
    assert all(terminal["operations"].values())
    rollback = report["rolled_back_final_assay_boundary"]
    assert rollback["passed"] is True
    assert all(rollback["checks"].values())
    assert rollback["transaction_status"] == "rolled_back"
    assert rollback["rollback_reason"] == "constitution_failed"
    assert rollback["reward"] == 0.0
    assert rollback["measurement_cost"] == 0.0
    assert rollback["sample_consumed"] == 0.0


def test_numeric_probe_rejects_negative_and_zero_effect_payloads(
    report: dict[str, object],
) -> None:
    assert report["negative_value_acceptances"] == []
    assert report["zero_effect_acceptances"] == []
    assert report["defect_inventory"] == []


def test_malformed_action_boundary_is_atomic_and_non_crashing(
    report: dict[str, object],
) -> None:
    boundary = report["malformed_action_boundary"]
    assert boundary["case_count"] == 8
    assert boundary["passed"] is True
    assert set(boundary["cases"]) == {
        "infinite_operation",
        "empty_operation",
        "fractional_operation",
        "infinite_material_choice",
        "infinite_phase_choice",
        "none_action",
        "list_action",
        "scalar_action",
    }
    assert all(case["passed"] for case in boundary["cases"].values())


def test_observation_integrity_boundary_rolls_back_state_and_rng(
    report: dict[str, object],
) -> None:
    boundary = report["observation_integrity_boundary"]
    assert boundary["case_count"] == 3
    assert boundary["infinity_rejected_by_observation_space"] is True
    assert boundary["passed"] is True
    assert set(boundary["cases"]) == {
        "nonfinite_value",
        "private_payload",
        "nonfinite_uncertainty",
    }
    assert all(case["passed"] for case in boundary["cases"].values())


def test_report_is_complete_and_tamper_evident(
    protocol: dict[str, object], report: dict[str, object]
) -> None:
    assert validate_report(report, protocol) == []

    tampered = copy.deepcopy(report)
    tampered["operation_results"].pop("wait")
    errors = validate_report(tampered, protocol)
    assert "operation coverage mismatch" in errors
    assert "report hash mismatch" in errors
