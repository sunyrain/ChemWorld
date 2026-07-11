from __future__ import annotations

import pytest

from chemworld.agents.base import HistoryRecord
from chemworld.agents.bo import StructuredSafetyConstrainedBOAgent
from chemworld.agents.task_recipes import (
    sample_conservative_task_recipe,
    task_recipe_dimension,
    task_recipe_from_unit_vector,
    task_recipe_to_model_vector,
    task_recipe_to_vector,
)
from chemworld.tasks import get_task


def test_recipe_history_retains_peak_public_risk_not_terminal_risk() -> None:
    task_info = get_task("reaction-to-crystallization").to_dict()
    agent = StructuredSafetyConstrainedBOAgent(n_candidates=16)
    agent.reset(task_info, seed=7)
    recipe = sample_conservative_task_recipe(task_info, agent.rng)
    agent._start_recipe(recipe)
    agent.update(
        {"operation": "heat"},
        {"safety_risk": 0.42},
        reward=0.0,
        info={},
    )
    agent.update(
        {"operation": "measure", "instrument": "final_assay"},
        {"safety_risk": 0.04, "score": 0.5},
        reward=0.5,
        info={},
    )
    retained = agent._recipe_history[0]
    assert retained.observation["safety_risk"] == pytest.approx(0.04)
    assert retained.observation["experiment_peak_safety_risk"] == pytest.approx(0.42)
    assert retained.info["experiment_peak_safety_risk"] == pytest.approx(0.42)


def test_safe_bo_initial_design_is_conservative_and_manifested() -> None:
    task_info = get_task("flow-reaction-optimization").to_dict()
    agent = StructuredSafetyConstrainedBOAgent(n_candidates=16)
    agent.reset(task_info, seed=9)
    agent.act([])
    trace = agent.agent_trace()[-1]
    vector = task_recipe_to_vector(trace["selected_recipe"])
    assert trace["selected_policy"] == "conservative_initial_design"
    assert vector[6] < 0.3  # temperature coordinate
    manifest = agent.manifest()
    assert manifest["risk_observation"] == "experiment_peak_safety_risk"
    assert manifest["risk_confidence_beta"] == 2.0
    assert manifest["initial_design"] == "public_conservative_low_intensity"


def test_safe_bo_acquisition_records_uncertainty_aware_feasibility() -> None:
    task_info = get_task("partition-discovery").to_dict()
    agent = StructuredSafetyConstrainedBOAgent(n_initial=4, n_candidates=32)
    agent.reset(task_info, seed=11)
    agent._recipe_history = [
        HistoryRecord(
            step=index + 1,
            action=sample_conservative_task_recipe(task_info, agent.rng),
            observation={
                "safety_risk": 0.02,
                "experiment_peak_safety_risk": 0.05 + index * 0.01,
            },
            reward=0.2 + index * 0.02,
            info={},
        )
        for index in range(4)
    ]
    agent.act([])
    trace = agent.agent_trace()[-1]
    diagnostics = trace["decision_diagnostics"]
    assert trace["phase"] == "acquisition"
    assert diagnostics["risk_label"] == "experiment_peak_safety_risk"
    assert diagnostics["risk_confidence_beta"] == 2.0
    assert diagnostics["predicted_risk_upper"] == pytest.approx(
        diagnostics["predicted_risk_mean"]
        + 2.0 * diagnostics["predicted_risk_std"]
    )


def test_typed_recipe_encoding_removes_ordinal_material_coordinates() -> None:
    task_info = get_task("flow-reaction-optimization").to_dict()
    dimension = task_recipe_dimension(task_info)
    base = [0.5] * dimension
    vectors = []
    for category_coordinate in (0.01, 0.26, 0.51, 0.76):
        values = list(base)
        values[0] = category_coordinate
        recipe = task_recipe_from_unit_vector(task_info, values)
        vectors.append(task_recipe_to_model_vector(task_info, recipe))
    distances = {
        round(float(((left - right) ** 2).sum() ** 0.5), 12)
        for index, left in enumerate(vectors)
        for right in vectors[index + 1 :]
    }
    assert distances == {round(2.0**0.5, 12)}
    assert vectors[0].size == dimension - 2 + 8
