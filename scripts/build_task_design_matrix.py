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
from chemworld.eval.task_metric_endpoints import build_task_metric_contract
from chemworld.tasks import CONFIRMATORY_BENCHMARK_TASK_IDS, list_tasks
from chemworld.world.recipes import compile_recipe
from chemworld.world.scoring import (
    CRYSTALLIZATION_S0_BALANCED_PRODUCT_V1,
    DISTILLATION_S0_BALANCED_AUDIT_SAFETY_V2,
    ELECTROCHEMICAL_S0_BALANCED_EFFICIENCY_V2,
    FLOW_S0_BALANCED_PROCESS_V1,
    PARTITION_S0_EXTRACTION_EFFICIENCY_V2,
    TASK_DERIVED_SCORING_CONTRACT,
    TaskScoringContract,
)

FORMAL_EVIDENCE = {
    "electrochemical-conversion": {
        "freeze_manifest": (
            "configs/benchmark/scientific_optimization_s0_v1.0_freeze_manifest.json"
        ),
        "campaign_summary": (
            "workstreams/flagship_tasks/reports/static-s0-v1.0-formal-campaign-summary.json"
        ),
        "participant_campaign_index": (
            "runs/formal/static-s0-v10-codex-subscription-20260729/campaign_execution_index.json"
        ),
        "baseline_campaign_index": (
            "runs/formal/static-s0-v10-baselines-20260729/campaign_execution_index.json"
        ),
    },
    "reaction-to-crystallization": {
        "freeze_manifest": (
            "configs/benchmark/scientific_optimization_s0_v1.0_freeze_manifest.json"
        ),
        "campaign_summary": (
            "workstreams/flagship_tasks/reports/static-s0-v1.0-formal-campaign-summary.json"
        ),
        "participant_campaign_index": (
            "runs/formal/static-s0-v10-codex-subscription-20260729/campaign_execution_index.json"
        ),
        "baseline_campaign_index": (
            "runs/formal/static-s0-v10-baselines-20260729/campaign_execution_index.json"
        ),
    },
}
ROOT = Path(__file__).resolve().parents[1]
_STATIC_S0_SCORING_CONTRACTS = {
    "electrochemical-conversion": ELECTROCHEMICAL_S0_BALANCED_EFFICIENCY_V2,
    "reaction-to-crystallization": CRYSTALLIZATION_S0_BALANCED_PRODUCT_V1,
    "reaction-to-distillation": DISTILLATION_S0_BALANCED_AUDIT_SAFETY_V2,
    "partition-discovery": PARTITION_S0_EXTRACTION_EFFICIENCY_V2,
    "flow-reaction-optimization": FLOW_S0_BALANCED_PROCESS_V1,
}


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


def _execute_recipe_case(
    env: Any,
    task_info: dict[str, Any],
    compiled_recipe: list[dict[str, Any]],
    *,
    case_id: str,
) -> dict[str, Any]:
    failures: list[dict[str, Any]] = []
    env.reset(seed=0)
    for step_index, action in enumerate(compiled_recipe):
        _observation, _reward, _terminated, _truncated, info = env.step(action)
        if (
            info.get("transaction_status") != "committed"
            or info.get("constraint_flags", {}).get("precondition_failed") is True
        ):
            failures.append(
                {
                    "case_id": case_id,
                    "step_index": step_index,
                    "action": action,
                    "transaction_status": info.get("transaction_status"),
                    "preconditions": info.get("preconditions", {}),
                }
            )
            break
    final_assay_present = any(
        action.get("operation") == "measure" and action.get("instrument") == "final_assay"
        for action in compiled_recipe
    )
    within_budget = len(compiled_recipe) <= int(task_info["budget"])
    return {
        "status": "passed" if not failures and final_assay_present and within_budget else "failed",
        "case_id": case_id,
        "world_seed": 0,
        "all_transactions_committed": not failures,
        "final_assay_present": final_assay_present,
        "compiled_operations": len(compiled_recipe),
        "within_environment_operation_budget": within_budget,
        "failures": failures,
        "claim_boundary": "deterministic design smoke; not comparative empirical evidence",
    }


def _parameter_entries(
    parameter_schema: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    if all("coordinate" in value for value in parameter_schema.values()):
        return sorted(
            (dict(value) for value in parameter_schema.values()),
            key=lambda value: int(value["coordinate"]),
        )
    entries: list[dict[str, Any]] = []
    for coordinate, (control_id, value) in enumerate(parameter_schema.items()):
        entry = {"coordinate": coordinate, "control_id": control_id, **value}
        if value.get("type") == "integer":
            entry["kind"] = "categorical"
            entry["category_count"] = int(value["maximum"]) - int(value["minimum"]) + 1
        entries.append(entry)
    return entries


def _design_execution_audit(
    task: Any,
    task_info: dict[str, Any],
    *,
    recipe_builder: Callable[[np.ndarray], dict[str, Any]],
    dimension: int,
    parameter_schema: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    entries = _parameter_entries(parameter_schema)
    if len(entries) != dimension:
        raise RuntimeError(
            f"parameter schema dimension mismatch for {task.task_id}: {len(entries)} != {dimension}"
        )
    vectors: list[tuple[str, np.ndarray]] = [("midpoint", np.full(dimension, 0.5, dtype=float))]
    for coordinate in range(dimension):
        for label, value in (("low", 0.2), ("high", 0.8)):
            vector = np.full(dimension, 0.5, dtype=float)
            vector[coordinate] = value
            vectors.append((f"coordinate-{coordinate}-{label}", vector))
    categorical_coverage: dict[str, dict[str, Any]] = {}
    for entry in entries:
        if entry.get("kind") != "categorical":
            continue
        coordinate = int(entry["coordinate"])
        category_count = int(entry["category_count"])
        control_id = str(entry["control_id"])
        observed: set[int] = set()
        for category in range(category_count):
            vector = np.full(dimension, 0.5, dtype=float)
            vector[coordinate] = (category + 0.5) / category_count
            vectors.append((f"coordinate-{coordinate}-category-{category}", vector))
            recipe = recipe_builder(vector)
            observed.update(
                int(step[control_id])
                for step in recipe["steps"]
                if step.get(control_id) is not None
            )
        categorical_coverage[control_id] = {
            "coordinate": coordinate,
            "declared_category_count": category_count,
            "observed_categories": sorted(observed),
            "all_categories_reachable": len(observed) == category_count,
        }

    cases: list[dict[str, Any]] = []
    env = gym.make(task.env_id, **task.env_kwargs(seed=0))
    try:
        for case_id, vector in vectors:
            recipe = recipe_builder(vector)
            compiled = compile_recipe(recipe, task_info=task_info)
            cases.append(
                _execute_recipe_case(
                    env,
                    task_info,
                    compiled,
                    case_id=case_id,
                )
            )
    finally:
        env.close()
    midpoint = next(case for case in cases if case["case_id"] == "midpoint")
    passed = all(case["status"] == "passed" for case in cases) and all(
        row["all_categories_reachable"] for row in categorical_coverage.values()
    )
    return {
        "status": "passed" if passed else "failed",
        "world_seed": 0,
        "case_count": len(cases),
        "midpoint": midpoint,
        "coordinate_low_high_case_count": 2 * dimension,
        "categorical_case_count": len(cases) - 1 - 2 * dimension,
        "categorical_coverage": categorical_coverage,
        "failed_cases": [case for case in cases if case["status"] != "passed"],
        "claim_boundary": (
            "deterministic coordinate-boundary and categorical reachability audit; "
            "not comparative empirical evidence"
        ),
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
            str(item["coordinate"]): item for item in task_recipe_coordinate_schema(task_info)
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
    execution_audit = _design_execution_audit(
        task,
        task_info,
        recipe_builder=recipe_builder,
        dimension=dimension,
        parameter_schema=parameter_schema,
    )
    if dead_coordinates or execution_audit["status"] != "passed":
        raise RuntimeError(
            f"task design validation failed for {task.task_id}: "
            f"dead_coordinates={dead_coordinates}, execution={execution_audit}"
        )
    scoring = TaskScoringContract.from_success_metrics(
        objective=task.objective,
        success_metrics=task.success_metrics,
        contract_id=_STATIC_S0_SCORING_CONTRACTS.get(
            task.task_id,
            TASK_DERIVED_SCORING_CONTRACT,
        ),
    )
    metric_contract = build_task_metric_contract(task.success_metrics)
    if not metric_contract["all_metrics_bound"]:
        raise RuntimeError(f"task has unbound success metrics: {task.task_id}")
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
            "declared_operation_sequence": [str(step["operation"]) for step in recipe["steps"]],
            "fixed_operation_sequence": [str(step["operation"]) for step in compiled_recipe],
            "compiled_operation_count_at_midpoint": len(compiled_recipe),
            "macro_operations": [
                str(step["operation"])
                for step in recipe["steps"]
                if step["operation"] in {"wash", "dry", "concentrate"}
            ],
            "measurement_slots": list(slots),
            "recipe_space_version": str(
                recipe.get("metadata", {}).get("search_space_version", TASK_RECIPE_SPACE_VERSION)
            ),
            "midpoint_execution_audit": execution_audit["midpoint"],
            "boundary_execution_audit": execution_audit,
        },
        "objective_and_reward": scoring.to_dict(),
        "evaluation_endpoints": metric_contract,
        "safety_and_cost": {
            "safety_limit": task.safety_limit,
            "cost_observed": True,
            "leaderboard_score_source": "final_assay",
            "online_reward_source": "fresh_measurement_score_delta",
            "safety_role": (
                "audit_only_nonoptimizing"
                if task.task_id == "reaction-to-distillation"
                else "task_score_and_constraint"
            ),
        },
        "formal_s0": (
            {
                "status": "completed_ten_worlds_full_classic_baselines",
                "independent_world_count": 10,
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
                "status": "formal_comparative_execution_pending",
                "formal_experiment_run": False,
                "design_and_endpoint_qualification_complete": True,
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
            "formal_campaign_complete_claim_bounded"
            if confirmatory
            else "executable_design_qualified_formal_comparison_pending"
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
        if row["formal_s0"]["status"] == "completed_ten_worlds_full_classic_baselines"
    )
    formal_empirical_comparison_pending_task_ids = sorted(
        row["task_id"]
        for row in tasks
        if row["formal_s0"]["status"] == "formal_comparative_execution_pending"
    )
    payload = {
        "schema_version": "chemworld-task-design-matrix-1.2",
        "source_commit": os.environ.get("CHEMWORLD_EVIDENCE_SOURCE_COMMIT")
        or git_source_commit(ROOT),
        "source_tree_dirty": source_tree_dirty,
        "task_count": len(tasks),
        "confirmatory_task_ids": list(CONFIRMATORY_BENCHMARK_TASK_IDS),
        "design_validation": {
            "status": "all_registered_task_designs_executable_and_metric_bound",
            "executable_midpoint_task_count": sum(
                row["complete_experiment_adapter"]["midpoint_execution_audit"]["status"] == "passed"
                for row in tasks
            ),
            "executable_boundary_task_count": sum(
                row["complete_experiment_adapter"]["boundary_execution_audit"]["status"] == "passed"
                for row in tasks
            ),
            "boundary_recipe_case_count": sum(
                row["complete_experiment_adapter"]["boundary_execution_audit"]["case_count"]
                for row in tasks
            ),
            "dead_recipe_coordinate_count": sum(
                len(row["overprotocol_audit"]["dead_recipe_coordinates"]) for row in tasks
            ),
            "declared_success_metric_count": sum(
                len(row["evaluation_endpoints"]["endpoints"]) for row in tasks
            ),
            "bound_success_metric_count": sum(
                sum(
                    endpoint["implementation_status"] == "executable"
                    for endpoint in row["evaluation_endpoints"]["endpoints"]
                )
                for row in tasks
            ),
            "formalization_blocker_count": sum(
                row["overprotocol_audit"]["formalization_blocker"] is not None for row in tasks
            ),
            "formal_experiment_task_ids": formal_experiment_task_ids,
            "formal_empirical_comparison_pending_task_ids": (
                formal_empirical_comparison_pending_task_ids
            ),
            "nonconfirmatory_formal_experiments_required_for_future_claims": True,
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
