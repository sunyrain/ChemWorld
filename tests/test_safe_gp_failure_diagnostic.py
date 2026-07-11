from __future__ import annotations

from copy import deepcopy

import pytest
from scripts.audit_safe_gp_failure_diagnostic import build_diagnostic_report


def _protocol() -> dict:
    return {
        "protocol_id": "test",
        "benchmark_claim_allowed": False,
        "task_id": "flow-reaction-optimization",
        "dev_seeds": [1, 2],
        "complete_experiments_per_run": 40,
        "comparator": "random",
        "incumbent": "safe_beta_2_0",
        "variants": {
            "safe_beta_2_0": {},
            "safe_beta_1_0": {},
        },
        "joint_revision_rule": {
            "paired_objective_effect_must_be_positive": True,
            "maximum_absolute_risk_rate_regression": 0.05,
            "maximum_relative_cost_regression": 0.05,
        },
        "evidence_boundary": "development only",
    }


def _row(seed: int, score: float, risk: float, cost: float) -> dict:
    return {
        "seed": seed,
        "mean_flow_conversion": score,
        "verified": True,
        "resource_usage": {
            "process_cpu_time_s": 2.0,
            "total_wall_time_s": 3.0,
            "method_ledger": {
                "accounting_complete": True,
                "decision_wall_time_s": 1.0,
            },
        },
        "score_replay": {
            "layered_evaluation": {
                "constraints": {"risk_budget_exceedance_rate": risk},
                "resources": {
                    "campaign_total_cost": cost * 40,
                    "complete_experiment_count": 40,
                },
            }
        },
    }


def test_diagnostic_retains_incumbent_when_lower_beta_is_jointly_worse() -> None:
    results = {
        "random": [_row(1, 0.03, 0.20, 0.50), _row(2, 0.04, 0.20, 0.50)],
        "safe_beta_2_0": [_row(1, 0.06, 0.02, 0.40), _row(2, 0.06, 0.02, 0.40)],
        "safe_beta_1_0": [_row(1, 0.05, 0.08, 0.44), _row(2, 0.05, 0.08, 0.44)],
    }
    report = build_diagnostic_report(results, protocol=_protocol())

    assert report["controls_passed"] is True
    assert report["incumbent_retained"] is True
    assert report["selected_revision"] is None
    assert report["revision_decisions_vs_incumbent"]["safe_beta_1_0"][
        "joint_revision_rule_passed"
    ] is False
    assert report["benchmark_claim_allowed"] is False


def test_diagnostic_selects_only_a_jointly_better_revision() -> None:
    results = {
        "random": [_row(1, 0.03, 0.20, 0.50), _row(2, 0.04, 0.20, 0.50)],
        "safe_beta_2_0": [_row(1, 0.06, 0.02, 0.40), _row(2, 0.06, 0.02, 0.40)],
        "safe_beta_1_0": [_row(1, 0.07, 0.03, 0.41), _row(2, 0.07, 0.03, 0.41)],
    }
    report = build_diagnostic_report(results, protocol=_protocol())

    assert report["selected_revision"] == "safe_beta_1_0"
    assert report["incumbent_retained"] is False


def test_diagnostic_fails_closed_on_seed_or_replay_drift() -> None:
    results = {
        "random": [_row(1, 0.03, 0.20, 0.50), _row(2, 0.04, 0.20, 0.50)],
        "safe_beta_2_0": [_row(1, 0.06, 0.02, 0.40), _row(2, 0.06, 0.02, 0.40)],
        "safe_beta_1_0": [_row(1, 0.05, 0.08, 0.44), _row(2, 0.05, 0.08, 0.44)],
    }
    drifted = deepcopy(results)
    drifted["safe_beta_1_0"][1]["seed"] = 3
    with pytest.raises(ValueError, match="exact frozen Dev seeds"):
        build_diagnostic_report(drifted, protocol=_protocol())

    unverified = deepcopy(results)
    unverified["safe_beta_1_0"][0]["verified"] = False
    report = build_diagnostic_report(unverified, protocol=_protocol())
    assert report["controls_passed"] is False
