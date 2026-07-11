from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from chemworld.agents.greedy import GreedyLocalAgent
from chemworld.agents.task_recipes import (
    TASK_RECIPE_SPACE_VERSION,
    task_recipe_dimension,
    task_recipe_event_count,
    task_recipe_to_vector,
)
from chemworld.eval.runner import run_agent
from chemworld.tasks import SERIOUS_TASK_IDS, get_task
from chemworld.world.recipes import compile_recipe


@pytest.mark.parametrize("task_id", SERIOUS_TASK_IDS)
def test_greedy_executes_legal_campaign_on_every_serious_task(
    tmp_path: Path,
    task_id: str,
) -> None:
    task = get_task(task_id)
    operation_budget = 2 * task_recipe_event_count(task.to_dict())
    history = run_agent(
        env_id=task.env_id,
        agent=GreedyLocalAgent(warmup=1),
        world_split=task.world_split,
        budget=task.budget,
        objective=task.objective,
        seed=0,
        task_id=task.task_id,
        output_path=tmp_path / f"{task_id}.jsonl",
        budget_override=operation_budget,
    )

    assert history
    assert not any(
        record.info["constraint_flags"].get("precondition_failed", False) for record in history
    )
    assert (
        sum(
            record.action.get("operation") == "measure"
            and record.action.get("instrument") == "final_assay"
            for record in history
        )
        >= 1
    )


def test_greedy_local_candidate_stays_in_task_recipe_space() -> None:
    task_info = get_task("partition-discovery").to_dict()
    agent = GreedyLocalAgent(warmup=1, perturbation_scale=0.10)
    agent.reset(task_info, seed=7)

    agent.act([])
    initial_recipe = dict(agent._active_recipe or {})
    agent.update(
        {"operation": "measure", "instrument": "final_assay"},
        {"product_in_organic": 0.5},
        0.5,
        {},
    )
    agent._pending_events.clear()
    agent.act([])
    candidate_recipe = dict(agent._active_recipe or {})

    initial = task_recipe_to_vector(initial_recipe)
    candidate = task_recipe_to_vector(candidate_recipe)
    assert initial.shape == candidate.shape == (task_recipe_dimension(task_info),)
    assert np.all((candidate >= 0.0) & (candidate <= 1.0))
    assert not np.array_equal(initial, candidate)
    assert all(
        step["operation"] in task_info["allowed_operations"]
        for step in compile_recipe(candidate_recipe, task_info=task_info)
    )


def test_greedy_is_deterministic_for_fixed_task_and_seed(tmp_path: Path) -> None:
    task = get_task("partition-discovery")
    operation_budget = 2 * task_recipe_event_count(task.to_dict())
    actions = []
    for suffix in ("left", "right"):
        history = run_agent(
            env_id=task.env_id,
            agent=GreedyLocalAgent(warmup=1),
            world_split=task.world_split,
            budget=task.budget,
            objective=task.objective,
            seed=11,
            task_id=task.task_id,
            output_path=tmp_path / f"{suffix}.jsonl",
            budget_override=operation_budget,
        )
        actions.append([record.action for record in history])

    assert actions[0] == actions[1]


def test_greedy_manifest_declares_task_recipe_local_search() -> None:
    agent = GreedyLocalAgent(warmup=3, perturbation_scale=0.12)
    agent.reset(get_task("flow-reaction-optimization").to_dict(), seed=0)

    manifest = agent.manifest()

    assert manifest["search_policy"] == "task_recipe_local_perturbation"
    assert manifest["search_space_version"] == TASK_RECIPE_SPACE_VERSION
    assert manifest["recipe_encoding"] == "task_specific_unit_hypercube"
    assert manifest["warmup"] == 3
    assert manifest["perturbation_scale"] == 0.12
    assert manifest["interaction_capabilities"]["adapts_across_experiments"] is True
