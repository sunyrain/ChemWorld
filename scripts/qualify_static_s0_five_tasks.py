"""Run the seed-0 readiness gate for the five selected S0 task families."""

from __future__ import annotations

import argparse
import copy
import json
from collections.abc import Callable, Mapping
from pathlib import Path
from typing import Any

import numpy as np

from chemworld.agents.crystallization_single_stage import (
    crystallization_single_stage_recipe_from_unit_vector,
)
from chemworld.agents.electrochemical_single_stage import (
    ELECTROCHEMICAL_SINGLE_STAGE_CATEGORICAL_COORDINATES,
    electrochemical_single_stage_recipe_from_unit_vector,
)
from chemworld.agents.static_optimization import StaticOptimizationAgent
from chemworld.agents.task_recipes import (
    task_recipe_categorical_coordinates,
    task_recipe_dimension,
    task_recipe_from_unit_vector,
)
from chemworld.eval.provenance import (
    canonical_json_sha256,
    git_source_commit,
    git_worktree_dirty,
    write_json_atomic,
)
from chemworld.eval.static_optimization_baselines import run_baseline_cell
from chemworld.eval.static_optimization_postrun import (
    replay_static_optimization_receipt,
    replay_static_optimization_validation,
)
from chemworld.eval.static_optimization_protocol import (
    validate_static_optimization_protocol,
)
from chemworld.tasks import get_task
from chemworld.world.scoring import TaskScoringContract

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PLAN = (
    ROOT / "configs/benchmark/static_s0_five_task_single_seed_qualification_v0.1_dev.json"
)
DEFAULT_OUTPUT = ROOT / "runs/dev/static-s0-five-task-single-seed-qualification-v0.1"


def _load_object(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain one JSON object")
    return payload


def _task_protocol(plan: Mapping[str, Any], task_id: str) -> dict[str, Any]:
    task_plan = plan["tasks"][task_id]
    seed_policy = plan["seed_policy"]
    campaign = plan["campaign"]
    world_policy: dict[str, Any] = {
        "mode": "static_for_entire_campaign",
        "world_seed": int(seed_policy["world_seeds"][0]),
        "interventions": [],
        "phase_changes": [],
        "hidden_world_fields_in_public_context": False,
    }
    material_family = task_plan.get("material_family_id")
    if task_id == "electrochemical-conversion":
        world_policy["electrochemical_material_family_id"] = material_family
    elif task_id == "reaction-to-crystallization":
        world_policy["crystallization_material_family_id"] = material_family
    executor_contract: dict[str, Any] = {
        "atomic_complete_experiment": True,
        "runtime_guard_margin_operations": 1,
        "runtime_margin_available_to_agent": False,
        "mandatory_terminate": True,
        "mandatory_final_assay": True,
        "show_task_operation_budget_to_agent": False,
    }
    if task_id == "electrochemical-conversion":
        executor_contract["electrochemical_workflow_mode"] = task_plan["workflow_mode"]
    return {
        "schema_version": (
            "chemworld-static-scientific-optimization-baseline-protocol-"
            "five-task-qualification-0.1-dev"
        ),
        "protocol_id": f"{plan['qualification_id']}--{task_id}",
        "freeze_id": f"{plan['qualification_id']}--{task_id}--seed0",
        "status": "development_single_seed_qualification",
        "formal_result": False,
        "benchmark_claim_allowed": False,
        "world_policy": world_policy,
        "tasks": [task_id],
        "horizon": int(campaign["exploration_experiments"]),
        "scientific_campaign_budget": {
            "exploration_experiments": int(campaign["exploration_experiments"]),
            "horizon_visible": bool(campaign["horizon_visible"]),
            "final_synthesis_after_exploration": True,
        },
        "material_information": {"mode": "opaque_codes"},
        "reward_contract": {
            "scoring_contract_id": task_plan["scoring_contract_id"],
            "optimization_feedback": "terminal_summary.leaderboard_score",
            "feedback_timing": "after_completed_final_assay_only",
            "intermediate_measurement_reward_used": False,
            "fresh_measurement_score_delta_used": False,
            "failed_experiment_score": 0.0,
            "final_selection": campaign["final_selection"],
            "primary_endpoint": ("blind_validated_final_recommendation_score_mean"),
        },
        "executor_contract": executor_contract,
        "final_synthesis": {
            "enabled": True,
            "calls": 0,
            "mode": "deterministic_best_observed_selection",
            "executes_experiment": False,
            "allow_tested_recommendation": True,
            "allow_interpolated_recommendation": False,
            "allow_extrapolated_recommendation_within_bounds": False,
            "validation_feedback_returned_to_agent": False,
        },
        "world_understanding": {
            "enabled": False,
            "declared_scoring_enabled": False,
            "predictive_score_enabled": False,
            "reason": "classic optimizers are readiness controls",
        },
        "validation_budget": {
            "incumbent_replicates": int(campaign["incumbent_validation_replicates"]),
            "recommendation_replicates": int(campaign["recommendation_validation_replicates"]),
            "independent_observation_seeds": True,
            "paired_observation_seeds_across_targets": True,
            "feedback_returned_to_agent": False,
        },
        "development_seed_policy": {
            "world_seeds": list(seed_policy["world_seeds"]),
            "algorithm_seeds": list(seed_policy["algorithm_seeds"]),
            "multi_seed_execution_allowed": False,
            "release_condition": seed_policy["release_condition"],
        },
        "algorithm_seeds": list(seed_policy["algorithm_seeds"]),
        "algorithms": copy.deepcopy(plan["algorithms"]),
        "observation_noise_namespace": (f"{plan['qualification_id']}--{task_id}"),
    }


def _recipe_builder(
    task_id: str,
    task_info: Mapping[str, Any],
) -> tuple[
    int,
    Callable[[np.ndarray], dict[str, Any]],
    tuple[tuple[int, int], ...],
]:
    if task_id == "electrochemical-conversion":
        return (
            6,
            lambda vector: electrochemical_single_stage_recipe_from_unit_vector(
                dict(task_info), vector
            ),
            ELECTROCHEMICAL_SINGLE_STAGE_CATEGORICAL_COORDINATES,
        )
    if task_id == "reaction-to-crystallization":
        return (
            10,
            lambda vector: crystallization_single_stage_recipe_from_unit_vector(
                dict(task_info), vector
            ),
            task_recipe_categorical_coordinates(dict(task_info)),
        )
    dimension = task_recipe_dimension(dict(task_info))
    return (
        dimension,
        lambda vector: task_recipe_from_unit_vector(dict(task_info), vector),
        task_recipe_categorical_coordinates(dict(task_info)),
    )


def _recipe_design_checks(
    task_id: str,
    task_info: Mapping[str, Any],
    expected_dimension: int,
) -> dict[str, Any]:
    dimension, builder, categorical = _recipe_builder(task_id, task_info)
    if dimension != expected_dimension:
        raise ValueError(f"{task_id} qualification dimension is stale")
    dead_coordinates: list[int] = []
    for coordinate in range(dimension):
        low = np.full(dimension, 0.5)
        high = np.full(dimension, 0.5)
        low[coordinate] = 0.2
        high[coordinate] = 0.8
        if canonical_json_sha256(builder(low)) == canonical_json_sha256(builder(high)):
            dead_coordinates.append(coordinate)
    categorical_coverage: dict[str, Any] = {}
    for coordinate, category_count in categorical:
        recipe_values = []
        for category in range(category_count):
            vector = np.full(dimension, 0.5)
            vector[coordinate] = (category + 0.5) / category_count
            recipe_values.append(canonical_json_sha256(builder(vector)))
        categorical_coverage[str(coordinate)] = {
            "category_count": category_count,
            "distinct_recipe_count": len(set(recipe_values)),
            "all_categories_reachable": len(set(recipe_values)) == category_count,
        }
    return {
        "dimension": dimension,
        "dead_recipe_coordinates": dead_coordinates,
        "categorical_coverage": categorical_coverage,
        "passed": not dead_coordinates
        and all(item["all_categories_reachable"] for item in categorical_coverage.values()),
    }


def _evidence_contract_check(
    task_id: str,
    protocol: Mapping[str, Any],
    receipt: Mapping[str, Any],
) -> dict[str, Any]:
    task_info = get_task(task_id).to_dict()
    scoring = TaskScoringContract.from_success_metrics(
        objective=task_info["objective"],
        success_metrics=tuple(task_info["success_metrics"]),
        contract_id=protocol["reward_contract"]["scoring_contract_id"],
    )
    agent = StaticOptimizationAgent(
        object(),
        role_id="five-task-qualification-context-audit",
        response_max_tokens=1,
        history_limit=8,
        prompt_token_estimate_cap=20_000,
        scoring_contract=scoring.to_dict(),
    )
    agent.reset(task_info, 0)
    first = receipt["experiments"][0]["result"]
    public_context = agent.public_context(
        [
            {
                "experiment_index": first["experiment_index"],
                "plan": first["plan"],
                "measurement_evidence": first["measurement_evidence"],
                "terminal_summary": first["terminal_summary"],
            }
        ]
    )
    slots = public_context["experiment_interface"]["diagnostic_measurement_slots"]
    compact_evidence = public_context["experiment_history"][0]["measurement_evidence"]
    stage_checks = []
    for slot_index, slot in enumerate(slots):
        allowed = set(slot.get("model_facing_metric_ids", ()))
        observed = set(compact_evidence[slot_index]["processed_estimate"])
        stage_checks.append(
            {
                "slot_id": slot["slot_id"],
                "observed_metric_ids": sorted(observed),
                "allowed_metric_ids": sorted(allowed),
                "passed": not allowed or observed.issubset(allowed),
            }
        )
    semantics = public_context["experiment_interface"].get("categorical_semantics", {})
    nominal_semantics_passed = bool(
        semantics.get("unordered_nominal")
        or semantics.get("categories_are_unordered_nominal_choices")
    )
    required = set(public_context["experiment_interface"]["required_measurement_slots"])
    requested = set(first["plan"]["requested_measurement_slots"])
    return {
        "stage_checks": stage_checks,
        "stage_valid_model_facing_evidence": all(item["passed"] for item in stage_checks),
        "nominal_categorical_semantics": nominal_semantics_passed,
        "required_measurements_present": required.issubset(requested),
    }


def _run_task(
    plan: Mapping[str, Any],
    task_id: str,
    output: Path,
    *,
    resume_missing: bool,
) -> dict[str, Any]:
    protocol = _task_protocol(plan, task_id)
    validate_static_optimization_protocol(protocol)
    task_output = output / task_id
    write_json_atomic(task_output / "protocol.json", protocol)
    protocol_hash = canonical_json_sha256(protocol)
    receipts = []
    for algorithm_id in plan["algorithms"]:
        receipt_path = task_output / "receipts" / f"{algorithm_id}_seed0.json"
        if resume_missing and receipt_path.is_file():
            receipt = _load_object(receipt_path)
            if receipt.get("protocol_sha256") != protocol_hash:
                raise RuntimeError(f"stale qualification receipt: {receipt_path}")
        else:
            receipt = run_baseline_cell(
                protocol=protocol,
                algorithm_id=algorithm_id,
                algorithm_seed=0,
            )
            write_json_atomic(receipt_path, receipt)
        receipts.append(receipt)
        print(
            json.dumps(
                {
                    "task_id": task_id,
                    "algorithm_id": algorithm_id,
                    "best_score": max(receipt["scores"]),
                    "validated_score": receipt["primary_score"],
                },
                sort_keys=True,
            ),
            flush=True,
        )
    exploration_replays = [
        replay_static_optimization_receipt(receipt, protocol) for receipt in receipts
    ]
    validation_replays = [replay_static_optimization_validation(receipt) for receipt in receipts]
    task = get_task(task_id)
    primary_scores = [float(receipt["primary_score"]) for receipt in receipts]
    first_receipt = receipts[0]
    design = _recipe_design_checks(
        task_id,
        task.to_dict(),
        int(plan["tasks"][task_id]["dimension"]),
    )
    evidence = _evidence_contract_check(
        task_id,
        protocol,
        first_receipt,
    )
    expected_operations = int(plan["tasks"][task_id]["compiled_operation_count"])
    atomic = all(
        result["completed"] is True
        and result["compiled_operation_count"] == expected_operations
        and result["operation_count"] == expected_operations
        and result["runtime_margin_used"] is False
        for receipt in receipts
        for result in (
            [item["result"] for item in receipt["experiments"]]
            + [
                replicate["result"]
                for target in ("incumbent", "recommendation")
                for replicate in receipt["validation"][target]["replicates"]
            ]
        )
    )
    scoring = TaskScoringContract.from_success_metrics(
        objective=task.objective,
        success_metrics=task.success_metrics,
        contract_id=plan["tasks"][task_id]["scoring_contract_id"],
    )
    first_assay = first_receipt["experiments"][0]["result"]["measurement_evidence"][-1][
        "observation"
    ]
    active_score_components = all(
        component == "reaction_score" or component in first_assay
        for component in scoring.component_weights
    )
    distinct_scores = len({round(value, 5) for value in primary_scores})
    checks = {
        "single_seed_only": all(
            receipt["cell"]["world_seed"] == 0 and receipt["method"]["algorithm_seed"] == 0
            for receipt in receipts
        ),
        "recipe_design": design["passed"],
        "atomic_complete_experiments": atomic,
        "stage_valid_model_facing_evidence": evidence["stage_valid_model_facing_evidence"],
        "explicit_nominal_categorical_semantics": evidence["nominal_categorical_semantics"],
        "required_measurements_present": evidence["required_measurements_present"],
        "active_score_components": active_score_components,
        "twenty_completed_experiments_per_method": all(
            receipt["completed_experiment_count"] == 20 for receipt in receipts
        ),
        "three_validation_replicates_per_target": all(
            len(receipt["validation"][target]["replicates"]) == 3
            for receipt in receipts
            for target in ("incumbent", "recommendation")
        ),
        "exploration_replay": all(replay["verified"] for replay in exploration_replays),
        "validation_replay": all(replay["verified"] for replay in validation_replays),
        "three_distinct_validated_scores": distinct_scores >= 3,
        "validated_threshold_reached": max(primary_scores) >= task.threshold,
    }
    return {
        "task_id": task_id,
        "task_contract_hash": task.contract_hash,
        "protocol_sha256": protocol_hash,
        "scoring_contract": scoring.to_dict(),
        "threshold": task.threshold,
        "validated_scores": {
            receipt["method_id"]: float(receipt["primary_score"]) for receipt in receipts
        },
        "validated_score_spread": max(primary_scores) - min(primary_scores),
        "distinct_validated_score_count": distinct_scores,
        "recipe_design": design,
        "evidence_contract": evidence,
        "exploration_replays": exploration_replays,
        "validation_replays": validation_replays,
        "checks": checks,
        "qualified": all(checks.values()),
        "receipt_sha256": {
            receipt["method_id"]: canonical_json_sha256(receipt) for receipt in receipts
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, default=DEFAULT_PLAN)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--resume-missing", action="store_true")
    parser.add_argument(
        "--check-plan",
        action="store_true",
        help="Validate and expand all task protocols without executing experiments.",
    )
    args = parser.parse_args()
    plan = _load_object(args.plan)
    task_ids = list(plan["task_ids"])
    if set(task_ids) != set(plan["tasks"]):
        raise ValueError("qualification task_ids and task contracts differ")
    protocols = {task_id: _task_protocol(plan, task_id) for task_id in task_ids}
    for protocol in protocols.values():
        validate_static_optimization_protocol(protocol)
    if args.check_plan:
        print(
            json.dumps(
                {
                    "qualification_id": plan["qualification_id"],
                    "task_ids": task_ids,
                    "protocol_sha256": {
                        task_id: canonical_json_sha256(protocol)
                        for task_id, protocol in protocols.items()
                    },
                    "single_seed_only": True,
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 0
    task_reports = {
        task_id: _run_task(
            plan,
            task_id,
            args.output,
            resume_missing=args.resume_missing,
        )
        for task_id in task_ids
    }
    report = {
        "schema_version": ("chemworld-static-s0-five-task-qualification-report-0.1-dev"),
        "qualification_id": plan["qualification_id"],
        "qualification_plan_sha256": canonical_json_sha256(plan),
        "source_commit": git_source_commit(ROOT),
        "source_tree_dirty": git_worktree_dirty(ROOT),
        "formal_result": False,
        "benchmark_claim_allowed": False,
        "world_seeds": [0],
        "algorithm_seeds": [0],
        "task_ids": task_ids,
        "tasks": task_reports,
        "qualified_task_count": sum(report["qualified"] for report in task_reports.values()),
        "qualified": all(report["qualified"] for report in task_reports.values()),
        "multi_seed_release_allowed": all(report["qualified"] for report in task_reports.values()),
        "claim_boundary": plan["claim_boundary"],
    }
    report["report_sha256"] = canonical_json_sha256(report)
    write_json_atomic(args.output / "qualification_report.json", report)
    print(
        json.dumps(
            {
                "output": str(args.output / "qualification_report.json"),
                "qualified": report["qualified"],
                "qualified_task_count": report["qualified_task_count"],
                "task_count": len(task_ids),
            },
            sort_keys=True,
        ),
        flush=True,
    )
    return 0 if report["qualified"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
