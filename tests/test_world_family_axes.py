from __future__ import annotations

from dataclasses import replace

import gymnasium as gym
import numpy as np
import pytest

import chemworld  # noqa: F401
from chemworld.agents.task_recipes import (
    task_recipe_dimension,
    task_recipe_from_unit_vector,
)
from chemworld.tasks import SERIOUS_TASK_IDS, get_task
from chemworld.world.scenario import DefaultScenarioGenerator, get_scenario
from chemworld.world.world_family import WORLD_AXIS_REGISTRY, AxisIntervention, axes_for_task


def _intervention(axis_id: str, mode: str = "extrapolation", severity: float = 1.0) -> dict:
    return {"axis_id": axis_id, "mode": mode, "severity": severity}


def _run_midpoint_recipe(
    task_id: str,
    axis_id: str | None,
    *,
    mode: str = "extrapolation",
) -> tuple[float, dict]:
    kwargs = get_task(task_id).env_kwargs(seed=0)
    if axis_id is not None:
        severity = -1.0 if axis_id == "electrochem.redox-kinetics" else 1.0
        kwargs["world_interventions"] = [_intervention(axis_id, mode=mode, severity=severity)]
    env = gym.make("ChemWorld", **kwargs)
    try:
        env.reset(seed=0)
        base = env.unwrapped
        task_info = base.task_info()
        vector = np.full(task_recipe_dimension(task_info), 0.5, dtype=float)
        recipe = task_recipe_from_unit_vector(task_info, vector)
        observation: dict = {}
        info: dict = {}
        for action in recipe["steps"]:
            observation, _, _, _, info = env.step(action)
        return float(info["leaderboard_score"]), observation
    finally:
        env.close()


def test_serious_tasks_declare_two_executable_world_axes() -> None:
    assert len(WORLD_AXIS_REGISTRY) == 12
    for task_id in SERIOUS_TASK_IDS:
        axes = axes_for_task(task_id)
        assert len(axes) == 2
        assert all(len(axis.modes) == 4 for axis in axes)


@pytest.mark.parametrize(
    "mode", ["interpolation", "extrapolation", "composition", "observation_noise"]
)
def test_each_axis_mode_builds_a_hashed_deterministic_world(mode: str) -> None:
    generator = DefaultScenarioGenerator()
    for axis in WORLD_AXIS_REGISTRY.values():
        scenario = get_scenario(axis.task_id)
        payload = (_intervention(axis.axis_id, mode=mode, severity=0.7),)
        first = generator.generate(scenario, 5, payload)
        second = generator.generate(scenario, 5, payload)
        assert first.parameters.world_id == second.parameters.world_id
        assert first.parameters.world_id != generator.generate(scenario, 5).parameters.world_id
        assert first.initial_state.metadata["world_family_intervention_hash"]
        assert (
            first.initial_state.metadata["world_family_intervention_hash"]
            == second.initial_state.metadata["world_family_intervention_hash"]
        )


@pytest.mark.parametrize(
    ("task_id", "axis_id"),
    [(axis.task_id, axis.axis_id) for axis in WORLD_AXIS_REGISTRY.values()],
)
def test_each_axis_changes_a_real_task_response(task_id: str, axis_id: str) -> None:
    base_score, base_observation = _run_midpoint_recipe(task_id, None)
    shifted_score, shifted_observation = _run_midpoint_recipe(task_id, axis_id)
    task = get_task(task_id)
    compared_fields = [
        field
        for field in task.success_metrics
        if field in shifted_observation and shifted_observation[field] is not None
    ]
    changes = [abs(shifted_score - base_score)]
    changes.extend(
        abs(
            float(np.asarray(shifted_observation[field]).reshape(-1)[0])
            - float(np.asarray(base_observation[field]).reshape(-1)[0])
        )
        for field in compared_fields
        if base_observation.get(field) is not None
    )
    assert max(changes) > 1.0e-8, (task_id, axis_id, base_score, shifted_score)


def test_axis_cannot_be_applied_to_another_task() -> None:
    scenario = get_scenario("partition-discovery")
    with pytest.raises(ValueError, match="belongs to"):
        DefaultScenarioGenerator().generate(
            scenario,
            0,
            (_intervention("electrochem.redox-kinetics"),),
        )


@pytest.mark.parametrize(
    ("task_id", "axis_id"),
    [(axis.task_id, axis.axis_id) for axis in WORLD_AXIS_REGISTRY.values()],
)
def test_composition_interventions_execute_complete_task_recipes(
    task_id: str,
    axis_id: str,
) -> None:
    score, _ = _run_midpoint_recipe(task_id, axis_id, mode="composition")
    assert np.isfinite(score)


def test_intervention_set_is_order_invariant() -> None:
    scenario = get_scenario("partition-discovery")
    first = _intervention("partition.distribution-coefficient", severity=0.5)
    second = _intervention("partition.phase-volume-ratio", severity=-0.5)
    generator = DefaultScenarioGenerator()
    forward = generator.generate(scenario, 9, (first, second))
    reverse = generator.generate(scenario, 9, (second, first))
    assert forward.parameters.world_id == reverse.parameters.world_id
    assert forward.parameters.domain_parameters == reverse.parameters.domain_parameters
    assert forward.initial_state.species_amounts == reverse.initial_state.species_amounts


def test_observation_noise_mode_keeps_the_selected_physical_axis_active() -> None:
    scenario = get_scenario("partition-discovery")
    shifted = DefaultScenarioGenerator().generate(
        scenario,
        0,
        (_intervention("partition.distribution-coefficient", mode="observation_noise"),),
    )
    assert shifted.parameters.domain_parameter("observation_noise_multiplier") > 1.0
    assert shifted.parameters.domain_parameter("partition_coefficient_multiplier") > 1.0


def test_interventions_and_domain_parameters_fail_closed() -> None:
    with pytest.raises(ValueError, match="non-zero"):
        AxisIntervention(
            axis_id="partition.distribution-coefficient",
            mode="interpolation",
            severity=0.0,
        )
    parameters = (
        DefaultScenarioGenerator().generate(get_scenario("partition-discovery"), 0).parameters
    )
    invalid = dict(parameters.domain_parameters)
    invalid.pop("partition_coefficient_multiplier")
    with pytest.raises(ValueError, match="invalid domain parameters"):
        replace(parameters, domain_parameters=invalid)
