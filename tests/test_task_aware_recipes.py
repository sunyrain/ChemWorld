from __future__ import annotations

import numpy as np
import pytest

from chemworld.agents.task_recipes import (
    task_recipe_dimension,
    task_recipe_from_unit_vector,
    task_recipe_kind,
    task_recipe_to_model_vector,
    task_recipe_to_vector,
)
from chemworld.eval.runner import make_agent, run_agent
from chemworld.tasks import SERIOUS_TASK_IDS, get_task
from chemworld.world.recipes import compile_recipe


@pytest.mark.parametrize("task_id", SERIOUS_TASK_IDS)
def test_task_recipe_compiles_only_allowed_operations(task_id: str) -> None:
    task_info = get_task(task_id).to_dict()
    dimension = task_recipe_dimension(task_info)
    recipe = task_recipe_from_unit_vector(
        task_info,
        np.linspace(0.1, 0.9, dimension),
    )
    steps = compile_recipe(recipe, task_info=task_info)
    assert task_recipe_to_vector(recipe).shape == (dimension,)
    assert all(step["operation"] in task_info["allowed_operations"] for step in steps)
    assert steps[-1] == {"operation": "measure", "instrument": "final_assay"}


@pytest.mark.parametrize(
    ("task_id", "expected_kind"),
    (
        ("partition-discovery", "partition"),
        ("reaction-to-crystallization", "reaction_crystallization"),
        ("reaction-to-distillation", "reaction_distillation"),
        ("flow-reaction-optimization", "flow"),
        ("electrochemical-conversion", "electrochemical"),
        ("equilibrium-characterization", "equilibrium"),
    ),
)
def test_serious_tasks_have_distinct_search_spaces(task_id: str, expected_kind: str) -> None:
    assert task_recipe_kind(get_task(task_id).to_dict()) == expected_kind


def test_model_vector_one_hot_encodes_electrochemical_solvent() -> None:
    task_info = get_task("electrochemical-conversion").to_dict()
    recipe = task_recipe_from_unit_vector(
        task_info,
        np.asarray([0.62, 0.3, 0.4, 0.5, 0.6]),
    )

    encoded = task_recipe_to_model_vector(task_info, recipe)

    assert encoded.shape == (9,)
    assert encoded[-4:].tolist() == [0.0, 0.0, 1.0, 0.0]


@pytest.mark.parametrize("agent_name", ("random", "lhs", "gp_bo", "safe_gp_bo"))
@pytest.mark.parametrize("task_id", SERIOUS_TASK_IDS)
def test_search_baselines_execute_valid_serious_task_actions(
    tmp_path,
    task_id: str,
    agent_name: str,
) -> None:
    task = get_task(task_id)
    history = run_agent(
        env_id=task.env_id,
        agent=make_agent(agent_name),
        world_split=task.world_split,
        budget=task.budget,
        objective=task.objective,
        seed=0,
        task_id=task.task_id,
        output_path=tmp_path / f"{task_id}-{agent_name}.jsonl",
    )
    assert history
    assert not any(
        record.info["constraint_flags"].get("precondition_failed", False)
        for record in history
    )
    assert sum(
        record.action.get("operation") == "measure"
        and record.action.get("instrument") == "final_assay"
        for record in history
    ) >= 1
