from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

import pytest
from scripts.qualify_work_i_latent_terminal_analysis import (
    build_markdown,
    build_qualification_report,
    build_synthetic_receipts,
)

from chemworld.eval.latent_terminal_analysis import (
    LatentTerminalAnalysisError,
    analyze_latent_terminal_population,
    finite_population_fraction,
    latent_terminal_analysis_sha256,
    validate_latent_terminal_analysis,
)
from chemworld.eval.latent_terminal_contract import latent_terminal_contract_sha256

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "configs/benchmark/work_i_latent_terminal_contract_v0.1.json"
REPORT_PATH = (
    ROOT
    / "workstreams/arxiv_v1/reports/"
    "work-i-latent-terminal-analysis-qualification-v0.1.json"
)
MARKDOWN_PATH = (
    ROOT
    / "workstreams/arxiv_v1/reports/"
    "work-i-latent-terminal-analysis-qualification-v0.1.md"
)


@pytest.fixture
def contract() -> dict[str, object]:
    payload = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def _receipts(contract: dict[str, object], score: float = 0.5) -> list[dict[str, object]]:
    receipts = build_synthetic_receipts(contract)
    for receipt in receipts:
        receipt["score"] = score
    return receipts


def _analyze(
    contract: dict[str, object], receipts: list[dict[str, object]]
) -> dict[str, object]:
    return analyze_latent_terminal_population(
        contract,
        receipts,
        mode="synthetic_qualification",
    )


def _primary(analysis: dict[str, object]) -> dict[str, object]:
    rows = analysis["selection_and_threshold_sensitivity"]
    assert isinstance(rows, list)
    return next(row for row in rows if row["primary"] is True)


def test_complete_population_implements_all_estimands_and_aggregation(
    contract: dict[str, object],
) -> None:
    analysis = _analyze(contract, _receipts(contract))
    assert validate_latent_terminal_analysis(analysis) == []
    assert analysis["status"] == "complete"
    assert analysis["census"] == {
        "campaign_cells": 10,
        "closed_lifecycles": 60,
        "observed_assays": 24,
        "observed_discards": 36,
        "resolved_shadow_receipts": 36,
        "unresolved_shadow_receipts": 0,
    }
    estimands = analysis["estimands"]
    assert set(estimands) == {
        "latent_terminal_score",
        "discard_to_observed_best_delta",
        "positive_discard_regret",
        "campaign_oracle_regret",
        "false_discard_fraction",
        "assay_commitment_precision",
        "assay_commitment_recall",
        "decision_time_discard_regret",
    }
    latent = estimands["latent_terminal_score"]
    overall = latent["aggregation"]["finite_population_micro"]["overall"]
    assert overall["fixed_denominator"] == 36
    assert overall["point_summary"]["mean"] == pytest.approx(0.5)
    assert latent["aggregation"]["cell_macro_average"]["defined_cell_count"] == 9
    assert len(latent["aggregation"]["paired_arm_contrasts"]) == 5
    assert analysis["missingness_and_censoring"]["complete_case_primary_used"] is False


def test_selection_table_uses_all_60_lifecycles_and_threshold_sensitivities(
    contract: dict[str, object],
) -> None:
    analysis = _analyze(contract, _receipts(contract))
    rows = analysis["selection_and_threshold_sensitivity"]
    assert [row["threshold_id"] for row in rows] == [
        "relative_0.80",
        "relative_0.90",
        "relative_1.00",
        "absolute_0.58",
    ]
    primary = _primary(analysis)
    overall = primary["strata"]["overall"]
    assert overall["fixed_lifecycle_denominator"] == 60
    assert sum(overall["point_table"].values()) == 60
    assert overall["point_table"]["FN"] == 36
    assert overall["point_metrics"]["false_discard_fraction"] == (
        finite_population_fraction(36, 36)
    )


def test_equality_is_near_best(contract: dict[str, object]) -> None:
    receipts = _receipts(contract, score=0.0)
    population = contract["population"]
    first = receipts[0]
    cell = next(
        item for item in population["cells"] if item["cell_id"] == first["cell_id"]
    )
    first["score"] = 0.90 * cell["campaign_best_assayed_score"]
    analysis = _analyze(contract, receipts)
    row = next(
        item
        for item in analysis["unit_rows"]
        if item["discard_id"] == first["discard_id"]
    )
    assert row["score"] == row["primary_threshold"]
    assert row["primary_classification"] == "FN"
    assert _primary(analysis)["positive_comparator"] == ">="


def test_campaign_oracle_has_nine_cells_and_no_opportunity_is_null(
    contract: dict[str, object],
) -> None:
    analysis = _analyze(contract, _receipts(contract))
    oracle = analysis["estimands"]["campaign_oracle_regret"]
    assert oracle["denominator"] == 9
    assert oracle["bounds"]["fixed_denominator"] == 9
    assert sum(row["opportunity"] for row in oracle["cells"]) == 9
    cell_02 = next(row for row in oracle["cells"] if row["cell_id"] == "cell-02")
    assert cell_02["opportunity"] is False
    assert cell_02["point_estimate"] is None
    assert cell_02["bounds"] is None
    assert "never assigned zero" in cell_02["null_rule"]


def test_decision_time_uses_only_strictly_prior_assays(
    contract: dict[str, object],
) -> None:
    analysis = _analyze(contract, _receipts(contract))
    decision = analysis["estimands"]["decision_time_discard_regret"]
    assert decision["denominator"] == 34
    assert decision["null_count"] == 2
    assert decision["null_discard_ids"] == [
        "cell-07:lifecycle-00:terminal-step-021",
        "cell-08:lifecycle-00:terminal-step-013",
    ]
    assert decision["future_assay_imputed"] is False


def test_missing_receipt_withholds_primary_and_preserves_sharp_fixed_bounds(
    contract: dict[str, object],
) -> None:
    receipts = _receipts(contract)
    analysis = _analyze(contract, receipts[1:])
    assert analysis["status"] == "incomplete_full_report_required"
    assert analysis["census"]["unresolved_shadow_receipts"] == 1
    latent = analysis["estimands"]["latent_terminal_score"]
    assert latent["point_estimate_status"] == "withheld"
    overall = latent["aggregation"]["finite_population_micro"]["overall"]
    assert overall["point_summary"] is None
    assert overall["fixed_denominator"] == 36
    mean_bound = overall["bounds"]["mean_and_order_statistic_bounds"]["mean"]
    assert mean_bound["lower"] == pytest.approx(17.5 / 36)
    assert mean_bound["upper"] == pytest.approx(18.5 / 36)
    assert overall["observed_only_diagnostic"]["count"] == 35
    assert overall["observed_only_is_primary"] is False
    assert _primary(analysis)["strata"]["overall"]["point_table"] is None
    assert analysis["missingness_and_censoring"]["complete_case_primary_used"] is False


def test_unresolved_receipt_emits_every_registered_bound_surface(
    contract: dict[str, object],
) -> None:
    analysis = _analyze(contract, _receipts(contract)[1:])
    estimands = analysis["estimands"]
    for estimand_id in (
        "latent_terminal_score",
        "discard_to_observed_best_delta",
        "positive_discard_regret",
    ):
        overall = estimands[estimand_id]["aggregation"]["finite_population_micro"][
            "overall"
        ]
        assert overall["point_summary"] is None
        assert overall["bounds"]["fixed_denominator"] == 36
        assert set(overall["bounds"]["mean_and_order_statistic_bounds"]) == {
            "mean",
            "minimum",
            "25th_percentile_linear",
            "median_linear",
            "75th_percentile_linear",
            "maximum",
        }
        assert overall["bounds"]["empirical_cdf_band"]
    assert estimands["campaign_oracle_regret"]["point_estimate_status"] == "withheld"
    assert estimands["campaign_oracle_regret"]["bounds"]["fixed_denominator"] == 9
    assert estimands["false_discard_fraction"]["point_estimate"] is None
    assert estimands["false_discard_fraction"]["bounds"]
    assert estimands["assay_commitment_precision"][
        "point_estimate_status"
    ] == "available_observed_exact"
    assert estimands["assay_commitment_precision"]["bounds"]
    assert estimands["assay_commitment_recall"]["point_estimate"] is None
    assert estimands["assay_commitment_recall"]["bounds"]
    assert estimands["decision_time_discard_regret"][
        "point_estimate_status"
    ] == "withheld"
    decision_overall = estimands["decision_time_discard_regret"]["aggregation"][
        "finite_population_micro"
    ]["overall"]
    assert decision_overall["bounds"]["fixed_denominator"] == 34
    for threshold in analysis["selection_and_threshold_sensitivity"]:
        overall = threshold["strata"]["overall"]
        assert overall["all_unresolved_score_zero_table"]
        assert overall["all_unresolved_score_one_table"]
        assert set(overall["bounds"]) == {
            "false_discard_fraction",
            "assay_commitment_precision",
            "assay_commitment_recall",
        }
    missingness = analysis["missingness_and_censoring"]
    assert set(missingness["by_registered_reason"]) == {
        "prefix",
        "identity",
        "evaluator",
        "resource",
        "nonfinite_score",
    }
    assert missingness["by_registered_reason"]["identity"] == 1
    assert len(missingness["by_information_arm"]) == 2
    assert len(missingness["by_campaign_cell"]) == 10
    assert missingness["by_campaign_cell"]["cell-02"] == {
        "unresolved_count": 0,
        "fixed_denominator": 0,
        "unresolved_fraction": {"numerator": 0, "denominator": 0, "value": None},
    }
    assert all(
        row["unresolved_fraction"]["denominator"] == row["fixed_denominator"]
        for row in missingness["by_campaign_cell"].values()
    )


@pytest.mark.parametrize("bad_score", [float("nan"), float("inf"), -1.0, 1.1, True, None])
def test_invalid_scores_become_unresolved_without_clamping_or_imputation(
    contract: dict[str, object], bad_score: object
) -> None:
    receipts = _receipts(contract)
    target_id = receipts[0]["discard_id"]
    receipts[0]["score"] = bad_score
    analysis = _analyze(contract, receipts)
    row = next(
        item for item in analysis["unit_rows"] if item["discard_id"] == target_id
    )
    assert row["outcome_status"] == "unresolved"
    assert row["score"] is None
    assert row["unresolved_category"] == "nonfinite_score"
    assert analysis["estimands"]["positive_discard_regret"][
        "point_estimate_status"
    ] == "withheld"


def test_tampered_receipt_binding_fails_closed(contract: dict[str, object]) -> None:
    receipts = _receipts(contract)
    target_id = receipts[0]["discard_id"]
    receipts[0]["terminal_action_sha256"] = "0" * 64
    analysis = _analyze(contract, receipts)
    row = next(
        item for item in analysis["unit_rows"] if item["discard_id"] == target_id
    )
    assert row["outcome_status"] == "unresolved"
    assert row["score"] is None
    assert row["unresolved_category"] == "identity"
    assert row["binding_errors"] == ["terminal_action_sha256_mismatch"]


def test_unresolved_receipt_cannot_smuggle_an_imputed_score(
    contract: dict[str, object],
) -> None:
    receipts = _receipts(contract)
    target_id = receipts[0]["discard_id"]
    receipts[0].update(
        {
            "outcome_status": "unresolved",
            "failure_category": "resource",
            "failure_reason": "synthetic_failure",
            "score": 1.0,
        }
    )
    analysis = _analyze(contract, receipts)
    row = next(
        item for item in analysis["unit_rows"] if item["discard_id"] == target_id
    )
    assert row["score"] is None
    assert row["unresolved_reason"] == "forbidden_score_on_unresolved_receipt"
    assert "forbidden_unresolved_score" in row["binding_errors"]
    assert analysis["missingness_and_censoring"]["complete_case_primary_used"] is False


def test_zero_denominator_is_explicit_null(contract: dict[str, object]) -> None:
    analysis = _analyze(contract, _receipts(contract, score=0.0))
    absolute = next(
        row
        for row in analysis["selection_and_threshold_sensitivity"]
        if row["threshold_id"] == "absolute_0.58"
    )
    recall = absolute["strata"]["overall"]["point_metrics"][
        "assay_commitment_recall"
    ]
    assert recall == {"numerator": 0, "denominator": 0, "value": None}
    assert finite_population_fraction(0, 0) == recall


def test_tampered_contract_and_ambiguous_receipts_are_rejected(
    contract: dict[str, object],
) -> None:
    tampered = deepcopy(contract)
    tampered["quality_reference"]["primary_near_best_fraction"] = 0.95
    tampered["contract_sha256"] = latent_terminal_contract_sha256(tampered)
    with pytest.raises(LatentTerminalAnalysisError, match="frozen L01 binding"):
        _analyze(tampered, _receipts(contract))

    receipts = _receipts(contract)
    with pytest.raises(LatentTerminalAnalysisError, match="duplicate receipt"):
        _analyze(contract, [*receipts, deepcopy(receipts[0])])


def test_analysis_self_hash_detects_tampering(contract: dict[str, object]) -> None:
    analysis = _analyze(contract, _receipts(contract))
    assert analysis["analysis_sha256"] == latent_terminal_analysis_sha256(analysis)
    altered = deepcopy(analysis)
    altered["census"]["observed_discards"] = 35
    errors = validate_latent_terminal_analysis(altered)
    assert "analysis self-hash mismatch" in errors
    assert "fixed terminal census mismatch" in errors


def test_synthetic_qualification_is_deterministic_and_outcome_blind() -> None:
    report = build_qualification_report()
    assert report["status"] == "qualified"
    assert all(case["passed"] for case in report["qualification_cases"])
    assert report["synthetic_fixture"] == {
        "receipt_count": 36,
        "score_rule": "((cell_number*17 + lifecycle_index*23 + 11) mod 101)/100",
        "formal_shadow_outcomes_accessed": False,
        "formal_shadow_evaluations_executed": 0,
        "agent_provider_calls": 0,
    }
    assert report["scientific_boundary"]["formal_analysis_authorized"] is False


def test_committed_qualification_reports_match_rebuild() -> None:
    report = build_qualification_report()
    assert json.loads(REPORT_PATH.read_text(encoding="utf-8")) == report
    assert MARKDOWN_PATH.read_text(encoding="utf-8") == build_markdown(report)
