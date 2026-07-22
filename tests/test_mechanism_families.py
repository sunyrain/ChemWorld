from __future__ import annotations

import gymnasium as gym
import numpy as np
import pytest

import chemworld  # noqa: F401
from chemworld.agents.task_recipes import (
    task_recipe_dimension,
    task_recipe_from_unit_vector,
)
from chemworld.tasks import get_task
from chemworld.world.mechanism_family import (
    CONSTITUTIVE_MECHANISM_TASKS,
    REACTION_MECHANISM_TASKS,
)
from chemworld.world.scenario import DefaultScenarioGenerator, get_scenario


def _intervention(mode: str, severity: float = 0.8) -> dict:
    return {"kind": "mechanism_family", "mode": mode, "severity": severity}


def _run_midpoint(task_id: str, mode: str | None) -> tuple[float, dict]:
    kwargs = get_task(task_id).env_kwargs(seed=0)
    if mode is not None:
        kwargs["world_interventions"] = [_intervention(mode)]
    env = gym.make("ChemWorld", **kwargs)
    try:
        env.reset(seed=0)
        task_info = env.unwrapped.task_info()
        recipe = task_recipe_from_unit_vector(
            task_info,
            np.full(task_recipe_dimension(task_info), 0.5),
        )
        observation: dict = {}
        info: dict = {}
        for action in recipe["steps"]:
            observation, _, _, _, info = env.step(action)
        observation["_audit_mass_balance_error"] = np.asarray(
            [info["raw_signal"]["mass_balance"]["process_mass_balance_error"]]
        )
        return float(info["leaderboard_score"]), observation
    finally:
        env.close()


@pytest.mark.parametrize("task_id", REACTION_MECHANISM_TASKS)
@pytest.mark.parametrize("mode", ["rate_law_family", "topology_family"])
def test_mechanism_family_changes_hash_structure_and_task_response(
    task_id: str,
    mode: str,
) -> None:
    generator = DefaultScenarioGenerator()
    scenario = get_scenario(task_id)
    base = generator.generate(scenario, 0)
    shifted = generator.generate(scenario, 0, (_intervention(mode),))
    repeated = generator.generate(scenario, 0, (_intervention(mode),))
    assert shifted.compiled_mechanism.mechanism_hash != base.compiled_mechanism.mechanism_hash
    assert shifted.compiled_mechanism.mechanism_hash == repeated.compiled_mechanism.mechanism_hash
    assert shifted.parameters.world_id != base.parameters.world_id
    assert shifted.compiled_mechanism.mechanism_id.startswith("mechanism-family-")
    if mode == "topology_family":
        assert (
            len(shifted.compiled_mechanism.network.reactions)
            == len(base.compiled_mechanism.network.reactions) + 1
        )
    else:
        base_laws = [r.rate_law.equation_id for r in base.compiled_mechanism.network.reactions]
        shifted_laws = [
            r.rate_law.equation_id for r in shifted.compiled_mechanism.network.reactions
        ]
        assert shifted_laws != base_laws
    base_score, base_observation = _run_midpoint(task_id, None)
    shifted_score, shifted_observation = _run_midpoint(task_id, mode)
    task = get_task(task_id)
    deltas = [abs(shifted_score - base_score)]
    deltas.extend(
        abs(float(shifted_observation[key][0]) - float(base_observation[key][0]))
        for key in task.success_metrics
        if shifted_observation.get(key) is not None and base_observation.get(key) is not None
    )
    assert max(deltas) > 1.0e-8


def test_partition_constitutive_family_changes_executed_law_not_reaction_network() -> None:
    generator = DefaultScenarioGenerator()
    scenario = get_scenario("partition-discovery")
    base = generator.generate(scenario, 0)
    intervention = (_intervention("constitutive_law_family"),)
    shifted = generator.generate(scenario, 0, intervention)
    repeated = generator.generate(scenario, 0, intervention)
    assert shifted.compiled_mechanism.mechanism_hash == base.compiled_mechanism.mechanism_hash
    assert shifted.parameters.domain_parameter(
        "partition_coefficient_exponent"
    ) > base.parameters.domain_parameter("partition_coefficient_exponent")
    assert (
        shifted.initial_state.metadata["mechanism_family_intervention_hash"]
        == (repeated.initial_state.metadata["mechanism_family_intervention_hash"])
    )
    assert ":mechanism-" in shifted.parameters.world_id
    base_score, _ = _run_midpoint("partition-discovery", None)
    shifted_score, shifted_observation = _run_midpoint(
        "partition-discovery",
        "constitutive_law_family",
    )
    assert abs(shifted_score - base_score) > 1.0e-8
    assert float(shifted_observation["_audit_mass_balance_error"][0]) <= 1.0e-8


@pytest.mark.parametrize("task_id", CONSTITUTIVE_MECHANISM_TASKS)
def test_constitutive_family_changes_executed_provider_without_network_rewrite(
    task_id: str,
) -> None:
    generator = DefaultScenarioGenerator()
    scenario = get_scenario(task_id)
    base = generator.generate(scenario, 0)
    shifted = generator.generate(
        scenario,
        0,
        (_intervention("constitutive_law_family"),),
    )
    assert shifted.compiled_mechanism.mechanism_hash == base.compiled_mechanism.mechanism_hash
    assert shifted.initial_state.metadata["mechanism_family_intervention_hash"]
    base_score, _ = _run_midpoint(task_id, None)
    shifted_score, shifted_observation = _run_midpoint(
        task_id,
        "constitutive_law_family",
    )
    assert abs(shifted_score - base_score) > 1.0e-8
    assert float(shifted_observation["_audit_mass_balance_error"][0]) <= 1.0e-8


@pytest.mark.parametrize(
    "task_id",
    ["electrochemical-conversion", "equilibrium-characterization"],
)
def test_nonreaction_tasks_reject_reaction_network_modes(task_id: str) -> None:
    with pytest.raises(ValueError, match="not causally reachable"):
        DefaultScenarioGenerator().generate(
            get_scenario(task_id),
            0,
            (_intervention("topology_family"),),
        )


def test_zero_intervention_preserves_frozen_mechanism() -> None:
    scenario = get_scenario("reaction-to-crystallization")
    generator = DefaultScenarioGenerator()
    base = generator.generate(scenario, 0)
    empty = generator.generate(scenario, 0, ())
    assert empty.compiled_mechanism.mechanism_hash == base.compiled_mechanism.mechanism_hash
    assert empty.parameters.world_id == base.parameters.world_id
    assert empty.parameters.domain_parameter("partition_coefficient_exponent") == 1.0
