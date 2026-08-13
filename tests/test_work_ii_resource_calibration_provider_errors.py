from __future__ import annotations

from copy import deepcopy

import pytest
from scripts.run_work_ii_resource_calibration import _cell_has_platform_defect

from chemworld.eval.work_ii_resource_calibration_v02 import cell_has_platform_defect


def _zero_failure_taxonomy() -> dict[str, object]:
    counts = {
        "provider_network": 0,
        "transport_ipc_os": 0,
        "agent_invalid": 0,
        "unclassified": 0,
    }
    return {
        "schema_version": "chemworld-mcp-tool-failure-taxonomy-0.1",
        "recovered_mcp_tool_failure_count": 0,
        "current_consecutive_mcp_tool_failure_count": 0,
        "maximum_consecutive_mcp_tool_failure_count": 0,
        "counts_by_category": deepcopy(counts),
        "current_consecutive_counts_by_category": deepcopy(counts),
        "maximum_consecutive_counts_by_category": deepcopy(counts),
        "recovery_episode_taxonomy": {
            "schema_version": "chemworld-mcp-tool-failure-recovery-episode-taxonomy-0.2",
            "recovery_episode_count": 0,
            "current_consecutive_recovery_episode_count": 0,
            "maximum_consecutive_recovery_episode_count": 0,
            "counts_by_category": deepcopy(counts),
            "current_consecutive_counts_by_category": deepcopy(counts),
            "maximum_consecutive_counts_by_category": deepcopy(counts),
        },
    }


def _closed_provider_error_cell() -> dict[str, object]:
    return {
        "completed": False,
        "provider_receipts": [
            {
                "status": "completed",
                "return_code": 0,
                "provider_error_event_count": 1,
                "provider_errors": [{"byte_count": 84, "sha256": "a" * 64}],
                "recovered_mcp_tool_failure_count": 0,
                "current_consecutive_mcp_tool_failure_count": 0,
                "maximum_consecutive_mcp_tool_failure_count": 0,
                "scientific_compliance_mcp_tool_failure_count": 0,
                "current_consecutive_scientific_compliance_mcp_tool_failure_count": 0,
                "maximum_consecutive_scientific_compliance_mcp_tool_failure_count": 0,
                "scientific_compliance_mcp_tool_failure_episode_count": 0,
                "current_consecutive_scientific_compliance_mcp_tool_failure_episode_count": 0,
                "maximum_consecutive_scientific_compliance_mcp_tool_failure_episode_count": 0,
                "mcp_tool_failure_taxonomy": _zero_failure_taxonomy(),
            }
        ],
        "method_resources": {
            "provider_usage_pending": False,
            "provider_usage_accounting_complete": True,
            "in_flight_model_call_count": 0,
        },
        "qualification": {
            "passed": False,
            "failed_checks": ["provider_operational_limits_reconciled"],
            "checks": {
                "one_campaign_session": True,
                "tool_integrity": True,
                "exact_replay": True,
                "execution_audit": True,
                "provider_operational_limits_reconciled": False,
            },
        },
    }


def test_closed_provider_error_remains_a_nonplatform_qualification_failure() -> None:
    row = _closed_provider_error_cell()

    assert _cell_has_platform_defect(row) is False
    assert row["qualification"]["passed"] is False
    assert row["provider_receipts"][0]["provider_error_event_count"] == 1


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("provider_usage_pending", True),
        ("provider_usage_accounting_complete", False),
        ("in_flight_model_call_count", 1),
    ],
)
def test_incomplete_provider_usage_remains_a_platform_defect(
    field: str, value: object
) -> None:
    row = _closed_provider_error_cell()
    row["method_resources"][field] = value

    assert _cell_has_platform_defect(row) is True


@pytest.mark.parametrize("check", ["tool_integrity", "exact_replay", "execution_audit"])
def test_broken_execution_evidence_remains_a_platform_defect(check: str) -> None:
    row = _closed_provider_error_cell()
    row["qualification"]["checks"][check] = False

    assert _cell_has_platform_defect(row) is True


@pytest.mark.parametrize("receipts", [[], [{}, {}]])
def test_missing_or_ambiguous_receipt_remains_a_platform_defect(
    receipts: list[dict[str, object]],
) -> None:
    row = deepcopy(_closed_provider_error_cell())
    row["provider_receipts"] = receipts

    assert _cell_has_platform_defect(row) is True


def _typed_closed_cell() -> dict[str, object]:
    row = _closed_provider_error_cell()
    receipt = row["provider_receipts"][0]
    receipt.update(
        {
            "pre_action_retry_classification": "terminal_accepted",
            "recovered_mcp_tool_failure_count": 0,
            "current_consecutive_mcp_tool_failure_count": 0,
            "maximum_consecutive_mcp_tool_failure_count": 0,
            "scientific_compliance_mcp_tool_failure_count": 0,
            "current_consecutive_scientific_compliance_mcp_tool_failure_count": 0,
            "maximum_consecutive_scientific_compliance_mcp_tool_failure_count": 0,
            "scientific_compliance_mcp_tool_failure_episode_count": 0,
            "current_consecutive_scientific_compliance_mcp_tool_failure_episode_count": 0,
            "maximum_consecutive_scientific_compliance_mcp_tool_failure_episode_count": 0,
        }
    )
    zeros = dict.fromkeys(
        ("provider_network", "transport_ipc_os", "agent_invalid", "unclassified"),
        0,
    )
    receipt["mcp_tool_failure_taxonomy"] = {
        "schema_version": "chemworld-mcp-tool-failure-taxonomy-0.1",
        "recovered_mcp_tool_failure_count": 0,
        "current_consecutive_mcp_tool_failure_count": 0,
        "maximum_consecutive_mcp_tool_failure_count": 0,
        "counts_by_category": deepcopy(zeros),
        "current_consecutive_counts_by_category": deepcopy(zeros),
        "maximum_consecutive_counts_by_category": deepcopy(zeros),
        "recovery_episode_taxonomy": {
            "schema_version": "chemworld-mcp-tool-failure-recovery-episode-taxonomy-0.2",
            "recovery_episode_count": 0,
            "current_consecutive_recovery_episode_count": 0,
            "maximum_consecutive_recovery_episode_count": 0,
            "counts_by_category": deepcopy(zeros),
            "current_consecutive_counts_by_category": deepcopy(zeros),
            "maximum_consecutive_counts_by_category": deepcopy(zeros),
        },
    }
    return row


def test_shared_classifier_keeps_resource_rejection_as_method_failure() -> None:
    row = _typed_closed_cell()
    row["qualification"]["checks"]["no_resource_rejection"] = False

    assert cell_has_platform_defect(row) is False


def test_shared_classifier_rejects_nonterminal_cell_without_legal_action() -> None:
    row = _typed_closed_cell()
    row["analysis"] = {
        "right_censored_open_experiment": True,
        "last_legal_action_count": 0,
        "nonterminal_no_legal_actions": True,
    }

    assert cell_has_platform_defect(row) is True


def test_shared_classifier_keeps_early_method_exit_with_legal_action() -> None:
    row = _typed_closed_cell()
    row["analysis"] = {
        "right_censored_open_experiment": True,
        "last_legal_action_count": 3,
        "nonterminal_no_legal_actions": False,
    }

    assert cell_has_platform_defect(row) is False


@pytest.mark.parametrize("category", ["transport_ipc_os", "unclassified"])
def test_shared_classifier_rejects_platform_taxonomy(category: str) -> None:
    row = _typed_closed_cell()
    receipt = row["provider_receipts"][0]
    receipt["recovered_mcp_tool_failure_count"] = 1
    receipt["maximum_consecutive_mcp_tool_failure_count"] = 1
    taxonomy = receipt["mcp_tool_failure_taxonomy"]
    taxonomy["recovered_mcp_tool_failure_count"] = 1
    taxonomy["maximum_consecutive_mcp_tool_failure_count"] = 1
    taxonomy["counts_by_category"][category] = 1
    taxonomy["maximum_consecutive_counts_by_category"][category] = 1

    assert cell_has_platform_defect(row) is True
