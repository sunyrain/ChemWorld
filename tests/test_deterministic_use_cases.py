from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from chemworld.eval.deterministic_use_cases import build_report, write_outputs

ROOT = Path(__file__).resolve().parents[1]

EXPECTED_CASES = {
    "U01": {
        "identity": "reaction-to-crystallization",
        "seed": 0,
        "submitted": 12,
        "action_list_sha256": "928e98b92859afb6968aa07e1021c222403f699baafb10bdd29b3ce9e7b81e95",
    },
    "U02": {
        "identity": "composed-equilibrium-characterization-demo",
        "seed": 0,
        "submitted": 5,
        "action_list_sha256": "cb3446cb33ab3c4e101a6cc2ce96be651958b6e91b49d3b8d223ddffc3de1758",
    },
    "U03/E01": {
        "identity": "composed-reaction-purification-demo",
        "seed": 0,
        "submitted": 19,
        "action_list_sha256": "a0990c28168f348a669ca9db080d095a60a76ab6cb8d31fa7aac995bbe579b4d",
    },
    "U06-flow": {
        "identity": "flow-reaction-optimization",
        "seed": 0,
        "submitted": 8,
        "action_list_sha256": "d3c6776528074b758d7130ecd8cd56f67a9c52a8cf06a2e631f3679b01bea7f0",
    },
    "U06-electro": {
        "identity": "electrochemical-conversion",
        "seed": 0,
        "submitted": 11,
        "action_list_sha256": "d5c0426bb93779aa0c2daf67ccdc1a9274508d82a8f20d5b08eb46f0cea693b6",
    },
    "U06-distillation": {
        "identity": "reaction-to-distillation",
        "seed": 0,
        "submitted": 12,
        "action_list_sha256": "d583f38de8f309f48dfada9c08414795b90c0619328a4bb5898a95a12d8ff3e7",
    },
    "U06-partition": {
        "identity": "partition-discovery",
        "seed": 0,
        "submitted": 10,
        "action_list_sha256": "1dadd67878bfece878e8d8edf76261897577790964cbb5d67a2e30f0ad2cdcba",
    },
    "U06-crystallization": {
        "identity": "reaction-to-crystallization",
        "seed": 1,
        "submitted": 12,
        "action_list_sha256": "928e98b92859afb6968aa07e1021c222403f699baafb10bdd29b3ce9e7b81e95",
    },
}


@pytest.fixture(scope="module")
def report() -> dict[str, Any]:
    return build_report(repository_root=ROOT, require_clean=False)


def test_frozen_case_bindings_and_exact_census(report: dict[str, Any]) -> None:
    assert report["status"] == "passed", report["summary"]["failure_class_counts"]
    assert report["provider_call_count"] == 0
    assert report["summary"] == {
        "cases": {"passed": 8, "denominator": 8},
        "submitted_actions": {"checked": 89, "denominator": 89, "expected": 89},
        "committed_actions": {"observed": 88, "expected": 88},
        "rolled_back_actions": {"observed": 1, "expected": 1},
        "committed_final_assays": {"observed": 8, "expected": 8},
        "public_private_leakage_count": 0,
        "missing_receipt_count": 0,
        "failure_class_counts": {},
        "exact_denominators_passed": True,
    }
    assert report["receipt_completeness"] == {
        "passed": True,
        "error_count": 0,
        "errors": [],
    }

    cases = {case["case_id"]: case for case in report["cases"]}
    assert len(cases) == len(report["cases"]) == 8
    assert set(cases) == set(EXPECTED_CASES)
    for case_id, expected in EXPECTED_CASES.items():
        case = cases[case_id]
        assert case["public_identity"] == expected["identity"]
        assert case["seed"] == expected["seed"]
        assert case["submitted_action_count"] == expected["submitted"]
        assert case["actions_sha256"] == expected["action_list_sha256"]
        assert case["checked_action_count"] == expected["submitted"]
        assert len(case["step_receipts"]) == expected["submitted"]


def test_every_submitted_action_has_complete_receipts(report: dict[str, Any]) -> None:
    steps = [step for case in report["cases"] for step in case["step_receipts"]]
    assert len(steps) == 89
    for case in report["cases"]:
        assert [step["step"] for step in case["step_receipts"]] == list(
            range(1, case["submitted_action_count"] + 1)
        )
        for step in case["step_receipts"]:
            assert step["action"]
            assert len(step["action_sha256"]) == 64
            assert step["schema_validation"]["valid"] is (
                case["case_id"] != "U03/E01" or step["step"] != 1
            )
            assert step["transaction"]["status"] in {"committed", "rolled_back"}
            assert isinstance(step["constitution_checks"], list)
            assert all(check["passed"] for check in step["constitution_checks"])
            assert step["world_events"]
            assert step["event_propagation_matches_operation"] is True
            assert isinstance(step["resource_preflight"], dict)
            assert isinstance(step["resource_outcome_delta"], dict)
            assert step["resource_reconciliation"]["resource_reconciled"] is True
            assert step["resource_reconciliation"]["reconciliation_mismatches"] == []
            assert isinstance(step["public_observation"], dict)
            assert step["leakage_findings"] == []
            assert step["passed"] is True
            assert step["failures"] == []


def test_u02_is_exactly_five_commits(report: dict[str, Any]) -> None:
    u02 = next(case for case in report["cases"] if case["case_id"] == "U02")
    assert [step["transaction"]["status"] for step in u02["step_receipts"]] == [
        "committed"
    ] * 5
    assert u02["committed_action_count"] == 5
    assert u02["rollback_count"] == 0
    assert u02["failures"] == []


def test_u03_expected_rollback_is_atomic_reconciled_then_recovers(
    report: dict[str, Any],
) -> None:
    u03 = next(case for case in report["cases"] if case["case_id"] == "U03/E01")
    first, *recovery = u03["step_receipts"]
    assert first["step"] == 1
    assert first["action"]["operation"] == "separate_phase"
    assert first["schema_validation"]["valid"] is False
    assert first["transaction"]["status"] == "rolled_back"
    assert first["transaction"]["rollback_reason"] == "precondition_failed"
    assert first["transaction"]["operation_committed"] is False
    ghost = first["rollback_recovery_receipt"]
    assert ghost["ghost_state_preserved"] is True
    assert ghost["physical"]["preserved"] is True
    assert ghost["observation_rng"]["preserved"] is True
    assert ghost["ledger"]["declared_penalty_reconciled"] is True
    assert ghost["ledger"]["ghost_state_preserved"] is True
    assert ghost["process"]["declared_penalty_reconciled"] is True
    assert ghost["process"]["ghost_state_preserved"] is True
    assert ghost["events"]["reconciled"] is True
    assert ghost["resource"]["resource_reconciled"] is True
    assert ghost["resource"]["reconciliation_mismatches"] == []

    assert len(recovery) == 18
    assert all(step["schema_validation"]["valid"] for step in recovery)
    assert all(step["transaction"]["status"] == "committed" for step in recovery)
    assert u03["committed_action_count"] == 18
    assert u03["rollback_count"] == 1
    assert u03["recovery_receipt"]["passed"] is True
    assert u03["recovery_receipt"]["observed_rollback_count"] == 1
    assert u03["recovery_receipt"]["subsequent_expected_commit_count"] == 18
    assert u03["recovery_receipt"]["subsequent_observed_commit_count"] == 18
    assert u03["failures"] == []


def test_all_cases_close_once_with_resource_boundary_and_replay_receipts(
    report: dict[str, Any],
) -> None:
    final_assays = 0
    for case in report["cases"]:
        final_steps = [
            step
            for step in case["step_receipts"]
            if step["action"].get("operation") == "measure"
            and step["action"].get("instrument") == "final_assay"
        ]
        assert len(final_steps) == 1
        final = final_steps[0]
        assert final["transaction"]["status"] == "committed"
        assert case["committed_final_assay_count"] == 1
        assert case["termination_receipt"]["closed"] is True
        assert case["termination_receipt"]["committed_terminate_count"] == 1
        assert case["termination_receipt"]["committed_final_assay_count"] == 1
        assert case["termination_receipt"]["final_terminated"] is True
        assert case["termination_receipt"]["final_truncated"] is False
        assert case["termination_receipt"]["right_censored_open_batch"] is False
        assert case["termination_receipt"]["post_termination_validation"]["passed"] is True
        assert case["resource_receipt"]["resource_reconciled"] is True
        assert case["resource_receipt"]["reconciliation_mismatches"] == []
        assert (
            case["resource_receipt"]["preflight"]["receipt_count"]
            == case["submitted_action_count"]
        )
        assert (
            case["resource_receipt"]["outcome_delta"]["operations_committed"]
            == case["committed_action_count"]
        )
        assert case["leakage_findings"] == []
        assert case["public_private_leakage_count"] == 0
        assert case["exact_replay"]["verified"] is True
        assert case["exact_replay"]["checked_steps"] == case["submitted_action_count"]
        assert case["exact_replay"]["max_abs_error"] == 0.0
        assert case["exact_replay"]["mismatches"] == []
        assert case["provider_call_count"] == 0
        assert case["trajectory_bytes"] > 0
        assert case["passed"] is True
        assert case["failures"] == []
        final_assays += 1
    assert final_assays == 8


def test_failure_accounting_is_complete_not_sampled(report: dict[str, Any]) -> None:
    case_failures = [failure for case in report["cases"] for failure in case["failures"]]
    step_failures = [
        failure
        for case in report["cases"]
        for step in case["step_receipts"]
        for failure in step["failures"]
    ]
    assert case_failures == []
    assert step_failures == []
    assert report["summary"]["failure_class_counts"] == {}
    assert report["receipt_completeness"]["errors"] == []
    unexpected = [
        {"case_id": case["case_id"], **step}
        for case in report["cases"]
        for step in case["step_receipts"]
        if step["transaction"]["status"] != "committed"
        and not (case["case_id"] == "U03/E01" and step["step"] == 1)
    ]
    assert unexpected == []


def test_output_writer_refuses_to_overwrite_either_artifact(
    report: dict[str, Any], tmp_path: Path
) -> None:
    output_json = tmp_path / "report.json"
    output_markdown = tmp_path / "report.md"
    write_outputs(
        report,
        output_path=output_json,
        markdown_path=output_markdown,
        allow_existing=False,
    )
    json_before = output_json.read_bytes()
    markdown_before = output_markdown.read_bytes()

    with pytest.raises(FileExistsError, match="refusing to"):
        write_outputs(
            report,
            output_path=output_json,
            markdown_path=tmp_path / "new.md",
            allow_existing=False,
        )
    with pytest.raises(FileExistsError, match="refusing to"):
        write_outputs(
            report,
            output_path=tmp_path / "new.json",
            markdown_path=output_markdown,
            allow_existing=False,
        )
    assert output_json.read_bytes() == json_before
    assert output_markdown.read_bytes() == markdown_before
