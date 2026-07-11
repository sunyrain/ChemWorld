from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

import gymnasium as gym
import numpy as np
import pytest

import chemworld  # noqa: F401
from chemworld.agents.task_recipes import (
    task_recipe_dimension,
    task_recipe_from_unit_vector,
)
from chemworld.eval.mechanism_family_audit import (
    audit_mechanism_families,
    load_mechanism_family_protocol,
)
from chemworld.tasks import get_task
from chemworld.world.mechanism_family import MECHANISM_REACHABLE_TASKS
from chemworld.world.scenario import DefaultScenarioGenerator, get_scenario

FROZEN_REPORT = (
    Path(__file__).resolve().parents[1]
    / "workstreams"
    / "benchmark_v1"
    / "reports"
    / "mechanism-family-controls.json"
)


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
        return float(info["leaderboard_score"]), observation
    finally:
        env.close()


@pytest.mark.parametrize("task_id", MECHANISM_REACHABLE_TASKS)
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


@pytest.mark.parametrize(
    "task_id",
    ["partition-discovery", "electrochemical-conversion", "equilibrium-characterization"],
)
def test_mechanism_family_rejects_tasks_without_reaction_network_reachability(
    task_id: str,
) -> None:
    with pytest.raises(ValueError, match="does not causally execute"):
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


def test_protocol_scope_drift_fails_closed() -> None:
    protocol = deepcopy(load_mechanism_family_protocol())
    protocol["reachable_tasks"].append("partition-discovery")
    report = audit_mechanism_families(protocol)
    assert report["checks"]["reachable_task_scope"] is False
    assert report["controls_ready"] is False


def test_protocol_mode_drift_fails_closed_without_skipping_controls() -> None:
    protocol = deepcopy(load_mechanism_family_protocol())
    protocol["modes"] = ["topology_family"]
    report = audit_mechanism_families(protocol)
    assert report["checks"]["mode_scope"] is False
    assert report["controls_ready"] is False
    assert set(report["tasks"]["reaction-to-crystallization"]["modes"]) == {
        "rate_law_family",
        "topology_family",
    }


def test_frozen_mechanism_family_report_is_ready_but_non_claiming() -> None:
    report = json.loads(FROZEN_REPORT.read_text(encoding="utf-8"))
    assert report["controls_ready"] is True
    assert report["checks"]["task_responses_change"] is True
    assert report["benchmark_claim_allowed"] is False
    assert report["publication_ready"] is False
