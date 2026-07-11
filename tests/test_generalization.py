from __future__ import annotations

from chemworld.agents.task_recipes import task_recipe_event_count
from chemworld.eval.benchmark_validation import PRIMARY_METRIC_FIELDS
from chemworld.eval.generalization import compare_publication_distribution_shift
from chemworld.tasks import SERIOUS_TASK_IDS, get_task


def _matrix(*, seed_offset: int, adaptive_effect: float) -> list[dict]:
    rows = []
    for task_id in SERIOUS_TASK_IDS:
        task = get_task(task_id)
        budget = task_recipe_event_count(task.to_dict()) * 40
        primary = PRIMARY_METRIC_FIELDS[task_id]
        for seed in range(seed_offset, seed_offset + 20):
            for method in ("random", "structured_gp_bo"):
                effect = adaptive_effect if method == "structured_gp_bo" else 0.0
                score = 0.4 + 0.001 * (seed - seed_offset) + effect
                rows.append(
                    {
                        "task_id": task_id,
                        "baseline_agent": method,
                        "seed": seed,
                        "total_score": score,
                        primary: score,
                        "final_best_score": score,
                        "area_under_best_score": score,
                        "safety_aware_score": score,
                        "cost_aware_score": score,
                        "invalid_action_rate": 0.0,
                        "bo_initial_recipe_count": 4 if method != "random" else 0,
                        "bo_acquisition_recipe_count": 36 if method != "random" else 0,
                        "sample_efficiency_step": None,
                        "evaluation_budget_steps": budget,
                        "resource_usage": {"complete_experiment_count": 40},
                    }
                )
    return rows


def test_publication_shift_audit_tracks_adaptive_effect_persistence() -> None:
    report = compare_publication_distribution_shift(
        _matrix(seed_offset=0, adaptive_effect=0.08),
        _matrix(seed_offset=100, adaptive_effect=0.06),
        shift_id="test-shift",
        bootstrap_samples=500,
    )

    assert report["passed"] is True
    assert report["ready_task_count"] == len(SERIOUS_TASK_IDS)
    for task in report["tasks"].values():
        assert task["total_score_effect_shift"] < 0.0
        assert task["checks"]["total_effect_direction_preserved"] is True
        assert task["checks"]["primary_effect_direction_preserved"] is True
