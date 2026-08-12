from __future__ import annotations

from pathlib import Path

from scripts.audit_work_ii_analysis_plan import audit

from chemworld.eval.work_ii_formal import EXPECTED_LAW_SUMMARY_EVALUATION_CONTRACT

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "configs/benchmark/work_ii_analysis_plan_v0.1.json"


def test_analysis_audit_freezes_resource_cards_denominators_and_hard_bounds(
    tmp_path: Path,
) -> None:
    report = audit(PLAN, tmp_path / "audit.json")

    assert report["status"] == "passed"
    assert report["w2_06_contract_complete"] is True
    assert report["w2_10_final_method_qualification_complete"] is False
    assert report["w2_07_complete"] is False
    assert len(report["resource_topology"]["task_rows"]) == 5
    assert report["resource_topology"]["operation_attempt_limit"] == 6_840
    assert report["resource_topology"]["vessel_start_limit"] == 600
    assert report["resource_topology"]["final_assay_limit"] == 600
    assert report["resource_topology"]["accepted_cell_input_token_limit"] == 324_000_000
    assert report["resource_topology"]["provider_attempt_hard_input_token_limit"] == 648_000_000
    assert report["execution_budget_and_eta"]["initial_schedule_wall_limit_h"] == 47.5
    assert report["execution_budget_and_eta"]["all_infrastructure_resumes_wall_hard_cap_h"] == 95.0
    assert report["denominator_ledger"]["mcp_tool_call"]["hard_cap"] is None
    assert (
        report["law_summary_evaluation_contract"]
        == EXPECTED_LAW_SUMMARY_EVALUATION_CONTRACT
    )
    assert report["currency_budget"]["formal_currency_ceiling_approved"] is False


def test_analysis_plan_is_bounded_failure_aware_and_h4_is_not_confirmatory(
    tmp_path: Path,
) -> None:
    report = audit(PLAN, tmp_path / "audit.json")
    assert report["status"] == "passed"
    assert not {
        "bounded_primary_prediction_error",
        "symmetric_failure_aware_estimand",
        "H4_excluded_from_confirmatory_family",
    } & {row["check"] for row in report["failures"]}
