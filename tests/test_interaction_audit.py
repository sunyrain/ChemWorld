from __future__ import annotations

import pytest

from chemworld.eval.interaction_audit import build_agent_interaction_audit


def _row(task: str, method: str, seed: int, *, risk: float, violations: int = 0) -> dict:
    return {
        "task_id": task,
        "baseline_agent": method,
        "seed": seed,
        "total_score": 0.4 + 0.01 * seed,
        "safety_aware_score": 0.3,
        "mean_safety_risk": risk,
        "safety_violations": violations,
        "invalid_action_count": 0,
        "final_assay_count": 40,
        "bo_initial_recipe_count": 4 if "gp" in method else 0,
        "bo_acquisition_recipe_count": 36 if "gp" in method else 0,
        "bo_entered_acquisition": "gp" in method,
        "observation_use_summary": {
            "instrument_counts": {"final_assay": 40, "uvvis": 40}
        },
        "resource_usage": {"run_wall_time_s": 1.5},
        "verified": True,
    }


def test_interaction_audit_separates_risk_observation_from_active_constraint() -> None:
    tasks = ("task-a", "task-b")
    methods = ("structured_gp_bo", "structured_safe_gp_bo")
    rows = [
        _row(task, method, seed, risk=0.1 + 0.01 * seed)
        for task in tasks
        for method in methods
        for seed in (0, 1)
    ]

    report = build_agent_interaction_audit(
        rows,
        expected_tasks=tasks,
        expected_methods=methods,
    )

    assert report["gates"]["formal_classic_matrix_complete"] is True
    assert report["gates"]["continuous_risk_observed"] is True
    assert report["gates"]["safety_constraint_active"] is False
    assert report["gates"]["safe_method_evaluation_informative"] is False
    assert report["methods"]["structured_gp_bo"]["mean_complete_experiments"] == 40
    assert report["safety_comparison"]["task-a"]["seed_count"] == 2


def test_interaction_audit_requires_canonical_risk_field() -> None:
    row = _row("task-a", "structured_gp_bo", 0, risk=0.2)
    row["mean_risk"] = row.pop("mean_safety_risk")

    with pytest.raises(ValueError, match="mean_safety_risk"):
        build_agent_interaction_audit(
            [row],
            expected_tasks=("task-a",),
            expected_methods=("structured_gp_bo",),
        )


def test_interaction_audit_marks_retained_verified_llm_evidence() -> None:
    rows = [_row("task-a", "random", 0, risk=0.1)]
    report = build_agent_interaction_audit(
        rows,
        task_lab_artifacts=(
            {
                "verified": True,
                "trajectory_retained": True,
                "uses_spectra": True,
                "adapts_within_experiment": True,
            },
        ),
        expected_tasks=("task-a",),
        expected_methods=("random",),
    )

    assert report["gates"]["formal_llm_artifacts_retained"] is True
    assert report["gates"]["spectral_policy_formally_evaluated"] is True
    assert report["gates"]["within_experiment_adaptation_formally_evaluated"] is True
