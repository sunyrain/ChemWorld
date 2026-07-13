from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

import pytest

from chemworld.eval.formal_statistics import (
    FormalStatisticsError,
    analyze_paired_contrast,
    audit_statistical_analysis_plan,
    holm_adjusted_p_values,
    load_statistical_analysis_plan,
    paired_percentile_interval,
    paired_sign_flip_p_value,
)

ROOT = Path(__file__).resolve().parents[1]
REPORT = (
    ROOT
    / "workstreams"
    / "benchmark_v1"
    / "reports"
    / "statistical-analysis-plan-v0.4.json"
)
TASKS = (
    "partition-discovery",
    "reaction-to-crystallization",
    "reaction-to-distillation",
    "flow-reaction-optimization",
)
PAIR_IDS = tuple(f"pair-{index:03d}" for index in range(100))


def _rows(
    protocol: dict[str, Any],
    *,
    objective_multiplier: float,
    risk_delta: float = 0.0,
    cost_multiplier: float = 1.0,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for task_id in TASKS:
        sesoi = float(protocol["objective_inference"]["task_sesoi"][task_id])
        for pair_id in PAIR_IDS:
            for method_id, primary, risk, cost in (
                ("operation_random", 0.4, 0.2, 100.0),
                (
                    "candidate",
                    0.4 + objective_multiplier * sesoi,
                    0.2 + risk_delta,
                    100.0 * cost_multiplier,
                ),
            ):
                rows.append(
                    {
                        "task_id": task_id,
                        "method_id": method_id,
                        "pair_id": pair_id,
                        "status": "success",
                        "failure_class": None,
                        "primary_value": primary,
                        "risk_exceedance_rate": risk,
                        "process_cost": cost,
                        "replay_verified": True,
                        "accounting_complete": True,
                    }
                )
    return rows


def _analyze(protocol: dict[str, Any], rows: list[dict[str, Any]]) -> dict[str, Any]:
    return analyze_paired_contrast(
        rows,
        protocol=protocol,
        candidate="candidate",
        comparator="operation_random",
        pair_ids=PAIR_IDS,
    )


def test_paired_interval_and_sign_flip_are_deterministic() -> None:
    effects = [0.01 + index * 0.001 for index in range(100)]
    first = paired_percentile_interval(
        effects,
        confidence_level=0.95,
        bootstrap_samples=1_000,
        seed_material="fixture",
    )
    second = paired_percentile_interval(
        effects,
        confidence_level=0.95,
        bootstrap_samples=1_000,
        seed_material="fixture",
    )
    assert first == second
    assert first[0] > 0.0
    assert paired_sign_flip_p_value(
        [0.1] * 100,
        randomization_samples=10_000,
        seed_material="fixture",
    ) < 0.001
    assert paired_sign_flip_p_value(
        [0.0] * 100,
        randomization_samples=10_000,
        seed_material="fixture",
    ) == 1.0


def test_holm_adjustment_is_monotone_and_familywise() -> None:
    adjusted = holm_adjusted_p_values({"a": 0.01, "b": 0.02, "c": 0.50, "d": 0.04})
    assert adjusted == {"a": 0.04, "b": 0.06, "d": 0.08, "c": 0.5}


def test_positive_fixture_passes_complete_joint_rule() -> None:
    protocol = load_statistical_analysis_plan()
    result = _analyze(protocol, _rows(protocol, objective_multiplier=1.5))
    assert result["benchmark_wide_joint_rule_passed"] is True
    assert result["task_pass_count"] == 4
    assert result["cross_task_primary_scalar"] is None
    assert all(
        card["mean_effect_reaches_task_sesoi"]
        and card["positive_objective_interval"]
        and card["holm_adjusted_p_at_or_below_alpha"]
        and card["safety"]["noninferiority_passed"]
        and card["cost"]["noninferiority_passed"]
        for card in result["task_decisions"].values()
    )


def test_null_unsafe_and_cost_regression_cannot_be_labeled_success() -> None:
    protocol = load_statistical_analysis_plan()
    null = _analyze(protocol, _rows(protocol, objective_multiplier=0.0))
    unsafe = _analyze(
        protocol,
        _rows(protocol, objective_multiplier=1.5, risk_delta=0.2),
    )
    expensive = _analyze(
        protocol,
        _rows(protocol, objective_multiplier=1.5, cost_multiplier=1.2),
    )
    assert null["benchmark_wide_joint_rule_passed"] is False
    assert unsafe["benchmark_wide_joint_rule_passed"] is False
    assert expensive["benchmark_wide_joint_rule_passed"] is False
    assert all(
        card["positive_objective_interval"] for card in unsafe["task_decisions"].values()
    )
    assert all(
        not card["safety"]["noninferiority_passed"]
        for card in unsafe["task_decisions"].values()
    )
    assert all(
        not card["cost"]["noninferiority_passed"]
        for card in expensive["task_decisions"].values()
    )


def test_failure_remains_in_all_100_denominators_and_fails_joint_rule() -> None:
    protocol = load_statistical_analysis_plan()
    rows = _rows(protocol, objective_multiplier=1.5)
    for row in rows:
        if row["method_id"] == "candidate" and row["pair_id"] == "pair-000":
            row.update(
                {
                    "status": "failure",
                    "failure_class": "runtime_failure",
                    "primary_value": None,
                    "risk_exceedance_rate": None,
                    "replay_verified": False,
                    "accounting_complete": False,
                }
            )
    result = _analyze(protocol, rows)
    assert result["benchmark_wide_joint_rule_passed"] is False
    for card in result["task_decisions"].values():
        assert card["observed_pair_count"] == 100
        assert card["candidate_success_count"] == 99
        assert card["failure_counts"]["candidate"] == {"runtime_failure": 1}
        assert card["all_trajectories_replay_verified"] is False
        assert card["all_required_resource_accounting_complete"] is False


def test_missing_pair_yields_incomplete_no_claim_and_duplicate_is_rejected() -> None:
    protocol = load_statistical_analysis_plan()
    rows = _rows(protocol, objective_multiplier=1.5)
    incomplete = _analyze(protocol, rows[1:])
    assert incomplete["benchmark_wide_joint_rule_passed"] is False
    assert incomplete["task_decisions"][TASKS[0]]["matrix_complete"] is False
    with pytest.raises(FormalStatisticsError, match="duplicate"):
        _analyze(protocol, [*rows, dict(rows[0])])


def test_malformed_failure_or_nonfinite_success_is_rejected() -> None:
    protocol = load_statistical_analysis_plan()
    rows = _rows(protocol, objective_multiplier=1.5)
    rows[0]["primary_value"] = float("nan")
    with pytest.raises(FormalStatisticsError, match="finite"):
        _analyze(protocol, rows)
    rows = _rows(protocol, objective_multiplier=1.5)
    rows[0].update({"status": "failure", "failure_class": "mystery"})
    with pytest.raises(FormalStatisticsError, match="unknown failure class"):
        _analyze(protocol, rows)


@pytest.mark.parametrize(
    ("mutator", "control"),
    [
        (
            lambda payload: payload["objective_inference"].update(
                {"familywise_alpha": 0.1}
            ),
            "objective_inference_and_holm_are_frozen",
        ),
        (
            lambda payload: payload["constraint_inference"].update(
                {"simultaneous_comparison_count": 4}
            ),
            "constraint_noninferiority_matches_power_design",
        ),
        (
            lambda payload: payload["joint_primary_rule"].update(
                {"total_score_can_replace_joint_rule": True}
            ),
            "joint_rule_cannot_be_replaced_by_total_score",
        ),
        (
            lambda payload: payload["family_champion_selection"].update(
                {"selection_split": "bench"}
            ),
            "family_champions_use_dev_only_and_freeze_before_bench",
        ),
    ],
)
def test_plan_tampering_fails_closed(mutator: Any, control: str) -> None:
    protocol = copy.deepcopy(load_statistical_analysis_plan())
    mutator(protocol)
    report = audit_statistical_analysis_plan(protocol, run_synthetic=False)
    assert report["controls_ready"] is False
    assert report["controls"][control] is False


def test_checked_in_statistical_plan_report_is_ready_and_nonclaiming() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    assert report["controls_ready"] is True
    assert report["formal_results_present"] is False
    assert report["benchmark_claim_allowed"] is False
    assert report["paired_identity_count"] == 100
    assert report["primary_contrast"] == "operation_champion_vs_operation_random_masked"
    assert report["synthetic_fixtures"]["null"][
        "benchmark_wide_joint_rule_passed"
    ] is False
    assert report["synthetic_fixtures"]["positive"][
        "benchmark_wide_joint_rule_passed"
    ] is True
    assert report["synthetic_fixtures"]["unsafe"][
        "benchmark_wide_joint_rule_passed"
    ] is False
    assert report["synthetic_fixtures"]["cost_regressing"][
        "benchmark_wide_joint_rule_passed"
    ] is False
