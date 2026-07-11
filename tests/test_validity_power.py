from __future__ import annotations

import pytest

from chemworld.eval.runner import make_agent, run_agent
from chemworld.eval.validity_power import (
    audit_validity_power,
    calibrated_validity_budget,
    campaign_record_prefix,
    minimum_learning_capacity,
)
from chemworld.tasks import get_task


def _result(method: str, seed: int, score: float) -> dict[str, object]:
    return {
        "task_id": "partition-discovery",
        "baseline_agent": method,
        "seed": seed,
        "total_score": score,
        "final_best_score": score,
        "area_under_best_score": score - 0.02,
        "safety_aware_score": score - 0.01,
        "cost_aware_score": score - 0.01,
        "invalid_action_rate": 0.0,
        "bo_initial_recipe_count": 2 if method == "gp_bo" else 0,
        "bo_acquisition_recipe_count": 2 if method == "gp_bo" else 0,
        "sample_efficiency_step": 10 if score >= 0.6 else None,
    }


def test_validity_power_uses_paired_effects_and_non_oracle_reference() -> None:
    results = []
    for seed in range(8):
        results.append(_result("random", seed, 0.45 + 0.01 * seed))
        results.append(_result("gp_bo", seed, 0.55 + 0.01 * seed))

    report = audit_validity_power(
        results,
        task_ids=("partition-discovery",),
        method_pairs=(("gp_bo", "random"),),
        planned_seed_count=20,
        bootstrap_samples=500,
    )

    task = report["tasks"]["partition-discovery"]
    effect = task["comparisons"]["gp_bo__minus__random"]
    assert effect["mean_paired_effect"] == pytest.approx(0.10)
    assert effect["wins"] == 8
    assert effect["sign_flip_p_value"] == pytest.approx(2 / 256)
    assert task["best_known_reference"]["is_oracle"] is False
    assert task["best_known_reference"]["mean_gap_by_method"]["gp_bo"] == pytest.approx(0.0)
    assert report["oracle_policy"]["random_sample_maximum_is_oracle"] is False


def test_validity_power_rejects_unpaired_seed_coverage() -> None:
    results = [
        _result("random", 0, 0.4),
        _result("random", 1, 0.5),
        _result("gp_bo", 0, 0.6),
    ]
    with pytest.raises(ValueError, match="fewer than two paired seeds"):
        audit_validity_power(
            results,
            task_ids=("partition-discovery",),
            method_pairs=(("gp_bo", "random"),),
            bootstrap_samples=500,
        )


def test_calibrated_budget_provides_dimension_aware_learning_opportunity() -> None:
    task_info = get_task("partition-discovery").to_dict()

    assert minimum_learning_capacity(task_info) == 8
    assert calibrated_validity_budget(task_info) == 80


def test_runner_budget_override_reaches_agent_and_execution_loop(tmp_path) -> None:
    history = run_agent(
        env_id="ChemWorld",
        agent=make_agent("gp_bo"),
        world_split="public-test",
        budget=24,
        budget_override=64,
        objective="balanced",
        seed=0,
        task_id="equilibrium-characterization",
        output_path=tmp_path / "override.jsonl",
    )

    assert len(history) == 64
    assert history[-1].info["budget"] == 64


def test_campaign_record_prefix_stops_at_requested_final_assay() -> None:
    records = [
        {"step": 1, "leaderboard_score": None},
        {"step": 2, "leaderboard_score": 0.4},
        {"step": 3, "leaderboard_score": None},
        {"step": 4, "leaderboard_score": 0.6},
        {"step": 5, "leaderboard_score": None},
    ]

    prefix = campaign_record_prefix(records, 2)

    assert [record["step"] for record in prefix] == [1, 2, 3, 4]
    with pytest.raises(ValueError, match="has 2 complete experiments"):
        campaign_record_prefix(records, 3)
