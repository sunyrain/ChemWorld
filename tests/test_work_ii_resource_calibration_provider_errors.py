from __future__ import annotations

from copy import deepcopy

import pytest
from scripts.run_work_ii_resource_calibration import _cell_has_platform_defect


def _closed_provider_error_cell() -> dict[str, object]:
    return {
        "completed": False,
        "provider_receipts": [
            {
                "status": "completed",
                "return_code": 0,
                "provider_error_event_count": 1,
                "provider_errors": [{"byte_count": 84, "sha256": "a" * 64}],
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
