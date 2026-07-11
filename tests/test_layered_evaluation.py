from __future__ import annotations

import json
from pathlib import Path

import pytest

from chemworld.eval.layered_evaluation import (
    TaskEvaluationContract,
    evaluate_layered_records,
)

FROZEN_REPORT = (
    Path(__file__).resolve().parents[1]
    / "workstreams"
    / "benchmark_v1"
    / "reports"
    / "evaluation-identifiability-controls.json"
)


def _record(
    *,
    score: float | None,
    primary: float | None,
    cost: float | None,
    reward: float,
    risk: float | None = 0.2,
    unsafe: bool = False,
) -> dict:
    return {
        "leaderboard_score": score,
        "observation": {
            "product_in_organic": primary,
            "cost": cost,
            "safety_risk": risk,
        },
        "reward": reward,
        "measurement_cost": 0.03 if score is not None else 0.0,
        "constraint_flags": {"unsafe": unsafe},
    }


def test_layered_evaluator_keeps_endpoints_shaping_constraints_and_cost_separate() -> None:
    contract = TaskEvaluationContract.for_task("partition-discovery")
    records = [
        _record(score=None, primary=0.99, cost=None, reward=0.7),
        _record(score=0.4, primary=0.5, cost=0.2, reward=0.4),
        _record(score=None, primary=0.01, cost=None, reward=0.9, unsafe=True),
        _record(score=0.6, primary=0.7, cost=0.3, reward=0.6),
    ]
    result = evaluate_layered_records(records, contract=contract)
    assert result["objective"]["best"] == pytest.approx(0.6)
    assert result["task_primary"]["terminal_values"] == pytest.approx([0.5, 0.7])
    assert result["online_shaping"]["eligible_as_primary_endpoint"] is False
    assert result["constraints"]["legacy_unsafe_operation_count"] == 1
    assert result["constraints"]["experiment_max_risks"] == pytest.approx([0.2, 0.2])
    assert result["resources"]["campaign_total_cost"] == pytest.approx(0.5)
    assert result["resources"]["campaign_process_cost"] == pytest.approx(0.44)
    assert result["resources"]["measurement_cost"] == pytest.approx(0.06)


def test_layered_evaluator_uses_peak_experiment_risk_for_constraint() -> None:
    contract = TaskEvaluationContract.for_task("partition-discovery", risk_limit=0.3)
    records = [
        _record(score=None, primary=0.2, cost=0.1, reward=0.1, risk=0.4),
        _record(score=0.5, primary=0.6, cost=0.2, reward=0.5, risk=0.1),
    ]
    result = evaluate_layered_records(records, contract=contract)
    assert result["constraints"]["max_observed_safety_risk"] == pytest.approx(0.4)
    assert result["constraints"]["risk_budget_exceedance_count"] == 1
    assert result["constraints"]["constraint_activated"] is True


def test_layered_evaluator_fails_on_missing_terminal_primary() -> None:
    contract = TaskEvaluationContract.for_task("partition-discovery")
    with pytest.raises(ValueError, match="product_in_organic"):
        evaluate_layered_records(
            [_record(score=0.4, primary=None, cost=0.2, reward=0.4)],
            contract=contract,
        )


def test_layered_evaluator_accepts_costless_incomplete_tail() -> None:
    contract = TaskEvaluationContract.for_task("partition-discovery")
    records = [
        _record(score=0.4, primary=0.5, cost=0.2, reward=0.4),
        _record(score=None, primary=None, cost=None, reward=0.0),
    ]
    records[-1]["constraint_flags"]["precondition_failed"] = True

    result = evaluate_layered_records(records, contract=contract)

    assert result["resources"]["campaign_total_cost"] == pytest.approx(0.2)
    assert result["resources"]["incomplete_experiment_count"] == 1
    assert result["validity"]["invalid_operation_count"] == 1


def test_layered_evaluator_reports_interaction_stratum_and_resources_without_scalarizing() -> None:
    contract = TaskEvaluationContract.for_task("partition-discovery")
    records = [
        _record(score=None, primary=0.3, cost=0.1, reward=0.1),
        _record(score=0.6, primary=0.7, cost=0.2, reward=0.6),
    ]
    metadata = {
        "interaction_capabilities": {
            "decision_scope": "operation",
            "consumes_intermediate_observations": True,
            "consumes_spectra": True,
            "adapts_within_experiment": True,
            "adapts_across_experiments": True,
            "emits_structured_decision_audit": True,
        },
        "official_runner_policy": {
            "one_agent_decision_per_operation": True,
            "automatic_action_repair": False,
            "automatic_terminate": False,
            "automatic_final_assay": False,
            "failed_or_invalid_actions_retained": True,
        },
    }
    for index, record in enumerate(records):
        record["agent_metadata"] = metadata
        record["explanation"] = {
            "decision_audit": {
                "status": "provided",
                "adaptation_source": "spectrum" if index else "none",
            },
            "outcome": {"has_spectral_packet": index == 1},
        }
    records[-1]["method_resources"] = {
        "accounting_complete": True,
        "agent_usage": {"model_call_count": 2},
    }

    result = evaluate_layered_records(records, contract=contract)

    assert result["interaction"]["capability_stratum"] == "operation_closed_loop"
    assert result["interaction"]["observed_within_experiment_adaptation"] is True
    assert result["interaction"]["harness_assistance_absent"] is True
    assert result["interaction"]["interaction_diagnostics_scalarized_into_endpoint"] is False
    assert result["resources"]["method_resource_accounting_complete"] is True
    assert result["resources"]["resource_axes_scalarized_into_endpoint"] is False


def test_frozen_evaluation_report_keeps_signal_blocker_visible() -> None:
    report = json.loads(FROZEN_REPORT.read_text(encoding="utf-8"))
    assert report["controls_ready"] is True
    assert report["evaluation_identifiable"] is False
    assert report["checks"]["formal_safety_constraint_active"] is False
    assert report["benchmark_claim_allowed"] is False
