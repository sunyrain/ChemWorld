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


def test_numeric_probe_rejects_negatives_and_reports_zero_effect_gaps(
    report: dict[str, object],
) -> None:
    assert report["negative_value_acceptances"] == []
    accepted_zero = report["zero_effect_acceptances"]
    defects = {item["defect_id"]: item for item in report["defect_inventory"]}
    if accepted_zero:
        assert defects["state-zero-effect-actions-accepted"]["evidence"] == accepted_zero
    else:
        assert "state-zero-effect-actions-accepted" not in defects


def test_report_is_complete_and_tamper_evident(
    protocol: dict[str, object], report: dict[str, object]
) -> None:
    assert validate_report(report, protocol) == []

    tampered = copy.deepcopy(report)
    tampered["operation_results"].pop("wait")
    errors = validate_report(tampered, protocol)
    assert "operation coverage mismatch" in errors
    assert "report hash mismatch" in errors
