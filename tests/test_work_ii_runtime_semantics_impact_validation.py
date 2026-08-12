from __future__ import annotations

from collections.abc import Callable
from copy import deepcopy
from pathlib import Path
from typing import Any

import pytest

from chemworld.eval.provenance import canonical_json_sha256
from chemworld.eval.work_ii_runtime_semantics_impact import (
    build_runtime_semantics_impact_audit,
)
from chemworld.eval.work_ii_runtime_semantics_impact_validation import (
    validate_runtime_semantics_impact_audit,
)


def _report(tmp_path: Path) -> dict[str, Any]:
    admin = tmp_path / "workstreams/flagship_tasks/reports/work-ii-admin.json"
    admin.parent.mkdir(parents=True)
    admin.write_text('{"status":"planning_only"}', encoding="utf-8")
    return build_runtime_semantics_impact_audit(tmp_path, [admin])


def _rehash(report: dict[str, Any]) -> None:
    report["audit_sha256"] = canonical_json_sha256(
        {key: value for key, value in report.items() if key != "audit_sha256"}
    )


def test_validator_accepts_consistent_audit(tmp_path: Path) -> None:
    result = validate_runtime_semantics_impact_audit(_report(tmp_path))

    assert result == {
        "passed": True,
        "failure_count": 0,
        "failures": [],
        "validated_report_count": 1,
    }


@pytest.mark.parametrize(
    ("mutator", "expected_failure"),
    [
        (lambda report: report.update(audit_sha256="0" * 64), "self_hash_mismatch"),
        (
            lambda report: report["denominators"].update(report_count=99),
            "summary_denominator_mismatch",
        ),
        (
            lambda report: report.update(status="pending_requalification"),
            "summary_status_mismatch",
        ),
        (
            lambda report: report.update(provider_call_count=1),
            "fixed_field_mismatch:provider_call_count",
        ),
        (
            lambda report: report.update(formal_result=True),
            "fixed_field_mismatch:formal_result",
        ),
        (
            lambda report: report.update(formal_execution_authorized=True),
            "fixed_field_mismatch:formal_execution_authorized",
        ),
        (
            lambda report: report.update(
                participant_outcome_values_used_for_classification=True
            ),
            "fixed_field_mismatch:participant_outcome_values_used_for_classification",
        ),
        (
            lambda report: report["reports"][0].update(
                required_action="pending_requalification"
            ),
            "classification_action_mismatch",
        ),
        (
            lambda report: report["reports"][0].update(classification="affected"),
            "classification_basis_mismatch",
        ),
        (
            lambda report: report["reports"][0].update(
                trigger_ids=["zero_dose_catalyst_modifier_fix"]
            ),
            "trigger_finding_mismatch",
        ),
    ],
)
def test_validator_rejects_mutations(
    tmp_path: Path,
    mutator: Callable[[dict[str, Any]], None],
    expected_failure: str,
) -> None:
    report = deepcopy(_report(tmp_path))
    mutator(report)
    if expected_failure != "self_hash_mismatch":
        _rehash(report)

    result = validate_runtime_semantics_impact_audit(report)

    assert result["passed"] is False
    assert any(
        failure == expected_failure or failure.endswith(f":{expected_failure}")
        for failure in result["failures"]
    )
