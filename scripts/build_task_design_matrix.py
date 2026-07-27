"""Build the machine-readable design and evidence matrix for all registered tasks."""

from __future__ import annotations

import argparse
import json
import os
from collections.abc import Callable
from functools import partial
from pathlib import Path
from typing import Any
from uuid import uuid4

import gymnasium as gym
import numpy as np

import chemworld  # noqa: F401
from chemworld.agents.crystallization_single_stage import (
    CRYSTALLIZATION_SINGLE_STAGE_MEASUREMENT_SLOTS,
    crystallization_single_stage_parameter_schema,
    crystallization_single_stage_recipe_from_unit_vector,
)
from chemworld.agents.electrochemical_single_stage import (
    ELECTROCHEMICAL_SINGLE_STAGE_MEASUREMENT_SLOTS,
    electrochemical_single_stage_parameter_schema,
    electrochemical_single_stage_recipe_from_unit_vector,
)
from chemworld.agents.scientific_adaptation import scientific_measurement_slots
from chemworld.agents.task_recipes import (
    TASK_RECIPE_SPACE_VERSION,
    task_recipe_coordinate_schema,
    task_recipe_dimension,
    task_recipe_from_unit_vector,
    task_recipe_kind,
)
from chemworld.eval.provenance import git_source_commit, git_worktree_dirty
from chemworld.tasks import CONFIRMATORY_BENCHMARK_TASK_IDS, list_tasks
from chemworld.world.recipes import compile_recipe
from chemworld.world.scoring import TaskScoringContract

FORMAL_EVIDENCE = {
    "electrochemical-conversion": {
        "protocol": (
            "configs/benchmark/"
            "scientific_optimization_s0_v0.4.1_single_stage_high_20_formal.json"
        ),
        "aggregate": (
            "runs/formal/"
            "static_scientific_optimization_s0_v041_single_stage_high_20_5seed_20260727/"
            "multiseed_report.json"
        ),
    },
    "reaction-to-crystallization": {
        "protocol": (
            "configs/benchmark/"
            "scientific_optimization_s0_v0.5_crystallization_high_20_formal.json"
        ),
        "aggregate": (
            "runs/formal/"
            "static_scientific_optimization_s0_v05_crystallization_high_20_5seed_20260727/"
            "multiseed_report.json"
        ),
        "classic_baselines": (
            "runs/development/"
            "static_scientific_optimization_s0_v05_crystallization_"
            "classic_baselines_20_5worlds_20260727/multiseed_report.json"
        ),
    },
}
ROOT = Path(__file__).resolve().parents[1]


def _write_json_atomic(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{uuid4().hex}.tmp")
    temporary.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    temporary.replace(path)


def _dead_recipe_coordinates(
    recipe_builder: Callable[[np.ndarray], dict[str, Any]],
    dimension: int,
) -> list[int]:
    dead: list[int] = []
    for coordinate in range(dimension):
        low = np.full(dimension, 0.5, dtype=float)
        high = np.full(dimension, 0.5, dtype=float)
        low[coordinate] = 0.2
        high[coordinate] = 0.8
        low_steps = recipe_builder(low)["steps"]
        high_steps = recipe_builder(high)["steps"]
        if low_steps == high_steps:
            dead.append(coordinate)
    return dead


def _midpoint_execution_audit(
    task: Any,
    task_info: dict[str, Any],
    compiled_recipe: list[dict[str, Any]],
) -> dict[str, Any]:
    failures: list[dict[str, Any]] = []
    env = gym.make(task.env_id, **task.env_kwargs(seed=0))
    try:
        env.reset(seed=0)
        for step_index, action in enumerate(compiled_recipe):
            _observation, _reward, _terminated, _truncated, info = env.step(action)
            if (
                info.get("transaction_status") != "committed"
                or info.get("constraint_flags", {}).get("precondition_failed") is True
            ):
                failures.append(
                    {
                        "step_index": step_index,
                        "action": action,
                        "transaction_status": info.get("transaction_status"),
                        "preconditions": info.get("preconditions", {}),
                    }
                )
                break
    finally:
        env.close()
    final_assay_present = any(
        action.get("operation") == "measure"
        and action.get("instrument") == "final_assay"
        for action in compiled_recipe
    )
    within_budget = len(compiled_recipe) <= int(task_info["budget"])
    return {
        "status": "passed" if not failures and final_assay_present and within_budget else "failed",
        "world_seed": 0,
        "all_transactions_committed": not failures,
        "final_assay_present": final_assay_present,
        "compiled_operations": len(compiled_recipe),
        "within_environment_operation_budget": within_budget,
        "failures": failures,
        "claim_boundary": "deterministic design smoke; not comparative empirical evidence",
    }


def _task_row(task: Any) -> dict[str, Any]:
    task_info = task.to_dict()
    kind = task_recipe_kind(task_info)
    dimension = task_recipe_dimension(task_info)
    midpoint = np.full(dimension, 0.5, dtype=float)
    if task.task_id == "electrochemical-conversion":
        parameterization = "named_physical_controls"
        parameter_schema = electrochemical_single_stage_parameter_schema()
        recipe = electrochemical_single_stage_recipe_from_unit_vector(task_info, np.full(6, 0.5))
        slots = ELECTROCHEMICAL_SINGLE_STAGE_MEASUREMENT_SLOTS
        workflow = "static_single_stage_electrochemical"
        dimension = 6
        recipe_builder = partial(
            electrochemical_single_stage_recipe_from_unit_vector,
            task_info,
        )
    elif task.task_id == "reaction-to-crystallization":
        parameterization = "named_physical_controls"
        parameter_schema = crystallization_single_stage_parameter_schema()
        recipe = crystallization_single_stage_recipe_from_unit_vector(task_info, midpoint)
        slots = CRYSTALLIZATION_SINGLE_STAGE_MEASUREMENT_SLOTS
        workflow = "static_single_stage_complete_reaction_crystallization"
        recipe_builder = partial(
            crystallization_single_stage_recipe_from_unit_vector,
            task_info,
        )
    else:
        parameterization = "unit_vector_with_public_physical_coordinate_schema"
        parameter_schema = {
            str(item["coordinate"]): item
            for item in task_recipe_coordinate_schema(task_info)
        }
        recipe = task_recipe_from_unit_vector(task_info, midpoint)
        slots = scientific_measurement_slots(task_info)
        workflow = f"registered_complete_{kind}_recipe"
        recipe_builder = partial(task_recipe_from_unit_vector, task_info)
    coupled_controls = [
        value["control_id"]
        for value in parameter_schema.values()
        if value.get("kind") == "coupled_linear" or "coupled_minimum" in value
    ]
    compiled_recipe = compile_recipe(recipe, task_info=task_info)
    dead_coordinates = _dead_recipe_coordinates(recipe_builder, dimension)
    execution_audit = _midpoint_execution_audit(task, task_info, compiled_recipe)
    if dead_coordinates or execution_audit["status"] != "passed":
        raise RuntimeError(
            f"task design validation failed for {task.task_id}: "
            f"dead_coordinates={dead_coordinates}, execution={execution_audit}"
        )
    scoring = TaskScoringContract.from_success_metrics(
        objective=task.objective,
        success_metrics=task.success_metrics,
    )
    confirmatory = task.task_id in CONFIRMATORY_BENCHMARK_TASK_IDS
    return {
        "task_id": task.task_id,
        "role": "confirmatory" if confirmatory else "registered_extended",
        "world_split": task.world_split,
        "episode_mode": task.episode_mode,
        "environment_operation_budget": task.budget,
        "environment_decision_unit": "one_validated_operation",
        "complete_experiment_adapter": {
            "workflow": workflow,
            "recipe_kind": kind,
            "parameterization": parameterization,
            "dimension": dimension,
            "parameter_schema": parameter_schema,
            "declared_operation_sequence": [
                str(step["operation"]) for step in recipe["steps"]
            ],
            "fixed_operation_sequence": [
                str(step["operation"]) for step in compiled_recipe
            ],
            "compiled_operation_count_at_midpoint": len(compiled_recipe),
            "macro_operations": [
                str(step["operation"])
                for step in recipe["steps"]
                if step["operation"] in {"wash", "dry", "concentrate"}
            ],
            "measurement_slots": list(slots),
            "recipe_space_version": str(
                recipe.get("metadata", {}).get(
                    "search_space_version", TASK_RECIPE_SPACE_VERSION
                )
            ),
            "midpoint_execution_audit": execution_audit,
        },
        "objective_and_reward": scoring.to_dict(),
        "safety_and_cost": {
            "safety_limit": task.safety_limit,
            "cost_observed": True,
            "leaderboard_score_source": "final_assay",
            "online_reward_source": "fresh_measurement_score_delta",
        },
        "formal_s0": (
            {
                "status": "completed_five_static_world_seeds",
                "exploration_horizon": 20,
                "horizon_visible": True,
                "final_synthesis": True,
                "blind_validation_replicates_per_target": 3,
                "declared_world_understanding": True,
                "predictive_world_understanding": True,
                "evidence": FORMAL_EVIDENCE[task.task_id],
            }
            if confirmatory
            else {
                "status": "not_required_for_current_confirmatory_release",
                "formal_experiment_run": False,
            }
        ),
        "overprotocol_audit": {
            "dead_recipe_coordinates": dead_coordinates,
            "coupled_internal_controls": coupled_controls,
            "formalization_blocker": None,
        },
        "physics_maturity": task.kernel_maturity.lowest_level.value,
        "proxy_allowed": task.kernel_maturity.proxy_allowed,
        "design_status": (
            "formal_design_and_empirical_execution_complete"
            if confirmatory
            else "registered_design_complete_formal_empirical_execution_not_required"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    tasks = [_task_row(task) for task in list_tasks()]
    source_tree_dirty_value = os.environ.get("CHEMWORLD_EVIDENCE_SOURCE_TREE_DIRTY")
    source_tree_dirty = (
        source_tree_dirty_value.lower() == "true"
        if source_tree_dirty_value is not None
        else git_worktree_dirty(ROOT)
    )
    formal_experiment_task_ids = sorted(
        row["task_id"]
        for row in tasks
        if row["formal_s0"]["status"] == "completed_five_static_world_seeds"
    )
    payload = {
        "schema_version": "chemworld-task-design-matrix-1.1",
        "source_commit": os.environ.get("CHEMWORLD_EVIDENCE_SOURCE_COMMIT")
        or git_source_commit(ROOT),
        "source_tree_dirty": source_tree_dirty,
        "task_count": len(tasks),
        "confirmatory_task_ids": list(CONFIRMATORY_BENCHMARK_TASK_IDS),
        "design_validation": {
            "status": "all_registered_task_designs_executable",
            "executable_midpoint_task_count": sum(
                row["complete_experiment_adapter"]["midpoint_execution_audit"][
                    "status"
                ]
                == "passed"
                for row in tasks
            ),
            "dead_recipe_coordinate_count": sum(
                len(row["overprotocol_audit"]["dead_recipe_coordinates"])
                for row in tasks
            ),
            "formalization_blocker_count": sum(
                row["overprotocol_audit"]["formalization_blocker"] is not None
                for row in tasks
            ),
            "formal_experiment_task_ids": formal_experiment_task_ids,
            "nonconfirmatory_formal_experiments_required": False,
        },
        "design_principles": {
            "one_environment_step": "one validated operation",
            "one_s0_decision": "one complete experiment",
            "optimizer_feedback": "terminal final-assay leaderboard score",
            "final_submission": "separate synthesis after the visible horizon",
            "hidden_world_fields_supplied_to_agent": False,
        },
        "tasks": tasks,
    }
    if len(tasks) != 15:
        raise RuntimeError(f"expected 15 registered tasks, found {len(tasks)}")
    _write_json_atomic(args.output, payload)
    print(json.dumps({"output": str(args.output), "task_count": len(tasks)}, sort_keys=True))


if __name__ == "__main__":
    main()
