from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from chemworld.eval.static_optimization_baselines import (
    BaselineObservation,
    make_optimizer,
    plan_from_baseline_decision,
    run_baseline_cell,
)
from chemworld.eval.static_optimization_execution import (
    static_optimization_workflow_mode,
)
from chemworld.tasks import get_task

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = (
    ROOT
    / "configs/benchmark/scientific_optimization_s0_v0.3_classic_baselines_20_dev.json"
)


def test_baseline_protocol_uses_terminal_score_not_reward_delta() -> None:
    protocol = json.loads(PROTOCOL.read_text(encoding="utf-8"))
    reward = protocol["reward_contract"]
    assert reward["optimization_feedback"] == "terminal_summary.leaderboard_score"
    assert reward["fresh_measurement_score_delta_used"] is False
    assert reward["safety_is_separate_from_primary_reward"] is True


def test_all_baseline_optimizers_emit_bounded_complete_recipe_vectors() -> None:
    protocol = json.loads(PROTOCOL.read_text(encoding="utf-8"))
    task_info = get_task("electrochemical-conversion").to_dict()
    workflow_mode = static_optimization_workflow_mode(protocol)
    for algorithm_id, configuration in protocol["algorithms"].items():
        optimizer = make_optimizer(
            algorithm_id=algorithm_id,
            task_info=task_info,
            horizon=20,
            seed=0,
            configuration=configuration,
            electrochemical_workflow_mode=workflow_mode,
        )
        decision = optimizer.propose()
        vector = np.asarray(decision.vector, dtype=float)
        assert vector.shape == (9,)
        assert np.all(vector >= 0.0)
        assert np.all(vector <= 1.0)


def test_optimizer_feedback_is_terminal_score() -> None:
    protocol = json.loads(PROTOCOL.read_text(encoding="utf-8"))
    task_info = get_task("electrochemical-conversion").to_dict()
    workflow_mode = static_optimization_workflow_mode(protocol)
    optimizer = make_optimizer(
        algorithm_id="random",
        task_info=task_info,
        horizon=2,
        seed=0,
        configuration=protocol["algorithms"]["random"],
        electrochemical_workflow_mode=workflow_mode,
    )
    decision = optimizer.propose()
    plan = plan_from_baseline_decision(
        decision,
        algorithm_id="random",
        task_info=task_info,
        electrochemical_workflow_mode=workflow_mode,
    )
    optimizer.observe(
        BaselineObservation(
            experiment_index=0,
            vector=decision.vector,
            score=0.42,
            peak_safety_risk=0.11,
            plan=plan,
        )
    )
    assert optimizer.best_observation().score == 0.42
    assert optimizer.resource_usage()["model_call_count"] == 0


def test_short_random_baseline_cell_completes_and_validates() -> None:
    protocol = json.loads(PROTOCOL.read_text(encoding="utf-8"))
    protocol["horizon"] = 2
    protocol["scientific_campaign_budget"]["exploration_experiments"] = 2
    protocol["validation_budget"]["incumbent_replicates"] = 1
    protocol["validation_budget"]["recommendation_replicates"] = 1
    cell = run_baseline_cell(
        protocol=protocol,
        algorithm_id="random",
        algorithm_seed=0,
    )
    assert cell["cell_status"] == "completed"
    assert cell["completed_experiment_count"] == 2
    assert cell["completed_validation_experiment_count"] == 2
    assert cell["resources"]["model_call_count"] == 0
    assert cell["final_synthesis"]["recommendation"]["recommendation_type"] == "tested"
