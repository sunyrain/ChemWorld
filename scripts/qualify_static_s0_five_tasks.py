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
    observation_noise_namespace_base = str(
        plan.get("observation_noise_namespace_base", plan["qualification_id"])
    )
    if not observation_noise_namespace_base.strip():
        raise ValueError("observation_noise_namespace_base must be non-empty")
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
            "final_selection": campaign.get(
                "baseline_final_selection", campaign.get("final_selection")
            ),
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
        "observation_noise_namespace": (
            f"{observation_noise_namespace_base}--{task_id}"
        ),
    }


def _participant_protocol(plan: Mapping[str, Any], task_id: str) -> dict[str, Any]:
    if not isinstance(plan.get("participant"), Mapping):
        raise ValueError("strengthened qualification lacks a participant binding")
    protocol = _task_protocol(plan, task_id)
    qualification_version = (
        "0.3"
        if str(plan.get("schema_version", "")).endswith("0.3-dev")
        else "0.2"
    )
    protocol["schema_version"] = (
        "chemworld-static-scientific-optimization-protocol-five-task-"
        f"qualification-{qualification_version}-s0-dev"
    )
    protocol["protocol_id"] = f"{plan['qualification_id']}--participant--{task_id}"
    protocol["freeze_id"] = f"{plan['qualification_id']}--participant--{task_id}--seed0"
    protocol["status"] = "development_single_seed_participant_qualification"
    protocol["candidate_order_seed"] = int(plan["seed_policy"]["algorithm_seeds"][0])
    protocol["method_config_path"] = str(plan["participant"]["method_config_path"])
    protocol["method_ids"] = [str(plan["participant"]["method_id"])]
    protocol["final_synthesis"] = {
        "enabled": True,
        "calls": 1,
        "executes_experiment": False,
        "allow_tested_recommendation": True,
        "allow_interpolated_recommendation": True,
        "allow_extrapolated_recommendation_within_bounds": True,
        "requires_structured_world_claims": False,
        "validation_feedback_returned_to_agent": False,
        "list_item_limit": 16,
        "list_item_limit_visible_to_model": True,
    }
    protocol["reward_contract"]["final_selection"] = str(
        plan["campaign"]["participant_final_selection"]
    )
    protocol["world_understanding"] = {
        "enabled": False,
        "declared_scoring_enabled": False,
        "predictive_score_enabled": False,
        "reason": "seed-0 qualification isolates optimization readiness",
    }
    validate_static_optimization_protocol(protocol)
    return protocol


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
    empirical_score_component_ranges = {}
    for component in scoring.component_weights:
        if component == "reaction_score":
            continue
        values = [
            float(
                experiment["result"]["measurement_evidence"][-1]["observation"][
                    component
                ]
            )
            for receipt in receipts
            for experiment in receipt["experiments"]
        ]
        empirical_score_component_ranges[component] = max(values) - min(values)
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
        "empirical_score_component_ranges": empirical_score_component_ranges,
        "threshold": task.threshold,
        "validated_scores": {
            receipt["method_id"]: float(receipt["primary_score"]) for receipt in receipts
        },
        "validated_scores_by_algorithm": {
            str(receipt["method"]["algorithm_id"]): float(receipt["primary_score"])
            for receipt in receipts
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


def _participant_task_report(
    *,
    plan: Mapping[str, Any],
    task_id: str,
    protocol: Mapping[str, Any],
    report_path: Path,
    baseline_report: Mapping[str, Any],
    method_config: Mapping[str, Any],
    source_commit: str,
) -> dict[str, Any]:
    report = _load_object(report_path)
    protocol_hash = canonical_json_sha256(protocol)
    method_hash = canonical_json_sha256(method_config)
    method_id = str(plan["participant"]["method_id"])
    if report.get("protocol_sha256") != protocol_hash:
        raise RuntimeError(f"stale participant protocol binding: {report_path}")
    if report.get("method_config_sha256") != method_hash:
        raise RuntimeError(f"stale participant method binding: {report_path}")
    if report.get("source_commit") != source_commit:
        raise RuntimeError(f"participant source commit mismatch: {report_path}")
    if report.get("source_tree_dirty") is not False:
        raise RuntimeError(f"participant was not executed on a clean source tree: {report_path}")
    if report.get("method_ids") != [method_id] or report.get("task_ids") != [task_id]:
        raise RuntimeError(f"participant cell scope mismatch: {report_path}")
    if report.get("execution_seed") != 0:
        raise RuntimeError(f"participant cell is not world seed 0: {report_path}")
    if report.get("completed_cell_count") != report.get("cell_count") or report.get(
        "method_failure_cell_count"
    ):
        raise RuntimeError(f"participant cell did not complete: {report_path}")
    cell = report["cells"][0]
    exploration_replay = replay_static_optimization_receipt(cell, protocol)
    validation_replay = replay_static_optimization_validation(cell)
    method = method_config["methods"][method_id]
    scoring = TaskScoringContract.from_success_metrics(
        objective=get_task(task_id).objective,
        success_metrics=get_task(task_id).success_metrics,
        contract_id=plan["tasks"][task_id]["scoring_contract_id"],
    )
    context_agent = StaticOptimizationAgent(
        object(),
        role_id="five-task-strengthened-qualification-context-audit",
        response_max_tokens=1,
        history_limit=20,
        prompt_token_estimate_cap=100_000,
        experiment_horizon=20,
        horizon_visible=True,
        final_synthesis_enabled=True,
        declared_claim_validation_policy=str(
            method["declared_claim_validation_policy"]
        ),
        scoring_contract=scoring.to_dict(),
        optimization_scaffold_id=str(method["static_optimization_scaffold_id"]),
    )
    context_agent.reset(get_task(task_id).to_dict(), 0)
    initial_context = context_agent.public_context(cell["public_history"][:8])
    scaffold = initial_context.get("campaign_scaffold")
    if not isinstance(scaffold, Mapping):
        raise RuntimeError(f"participant lacks the strengthened campaign scaffold: {report_path}")
    coverage = scaffold["coverage_audit"]
    decision_audits = [
        experiment["decision_audit"] for experiment in cell["experiments"]
    ]
    participant_score = float(
        cell["validation"]["primary_validated_recommendation_score_mean"]
    )
    incumbent_score = float(cell["validation"]["validated_incumbent_score_mean"])
    best_baseline = max(
        float(value) for value in baseline_report["validated_scores"].values()
    )
    task = get_task(task_id)
    checks = {
        "single_seed_only": int(cell["cell"]["world_seed"]) == 0,
        "twenty_completed_experiments": int(cell["completed_experiment_count"]) == 20,
        "three_validation_replicates_per_target": all(
            len(cell["validation"][target]["replicates"]) == 3
            for target in ("incumbent", "recommendation")
        ),
        "final_synthesis_completed": int(cell["completed_synthesis_call_count"]) == 1,
        "initial_continuous_extremes_covered": bool(
            coverage["all_continuous_extremes_seen"]
        ),
        "initial_nominal_categories_covered": bool(
            coverage["all_nominal_categories_seen"]
        ),
        "initial_nominal_pairs_maximally_distinct": bool(
            coverage["all_nominal_pairs_maximally_distinct"]
        ),
        "first_eight_recipes_committed_by_protocol_executor": all(
            audit.get("coverage_design_enforced") is True
            and audit.get("recipe_selection_authority") == "protocol_executor"
            and audit.get("coverage_design_experiment_index") == experiment_index
            for experiment_index, audit in enumerate(decision_audits[:8])
        ),
        "remaining_twelve_recipes_selected_by_model": all(
            audit.get("coverage_design_enforced") is False
            and audit.get("recipe_selection_authority") == "model"
            for audit in decision_audits[8:]
        ),
        "validated_threshold_reached": participant_score >= task.threshold,
        "regret_to_best_baseline_within_limit": (
            best_baseline - participant_score
            <= float(
                plan["qualification_gates"][
                    "participant_regret_to_best_baseline_at_most"
                ]
            )
        ),
        "recommendation_not_materially_worse_than_incumbent": (
            participant_score - incumbent_score
            >= -float(
                plan["qualification_gates"][
                    "participant_recommendation_not_worse_than_incumbent_by_more_than"
                ]
            )
        ),
        "exploration_replay": bool(exploration_replay["verified"]),
        "validation_replay": bool(validation_replay["verified"]),
        "unknown_declared_terms_are_unscored_not_fatal": (
            cell["agent_manifest"]["declared_claim_validation_policy"]
            == "unscored_unknown_terms"
        ),
    }
    if (
        "participant_experiments_9_through_17_selected_by_model_from_public_history_portfolio"
        in plan["qualification_gates"]
    ):
        checks.update(
            {
                "experiments_9_through_17_selected_by_model_from_public_history_portfolio": all(
                    audit.get("coverage_design_enforced") is False
                    and audit.get("recipe_selection_authority") == "model"
                    and audit.get("portfolio_selection_enforced") is True
                    and isinstance(audit.get("portfolio_candidate_id"), str)
                    and audit.get("portfolio_candidate_generation_authority")
                    == "protocol_executor_using_public_history_only"
                    and audit.get("portfolio_candidate_selection_authority") == "model"
                    for audit in decision_audits[8:17]
                ),
                "experiments_18_through_20_freely_selected_by_model": all(
                    audit.get("coverage_design_enforced") is False
                    and audit.get("recipe_selection_authority") == "model"
                    and audit.get("portfolio_selection_enforced") is False
                    for audit in decision_audits[17:20]
                ),
                "candidate_generation_uses_no_hidden_world_fields": all(
                    audit.get("portfolio_hidden_world_fields_used") is False
                    for audit in decision_audits[8:17]
                ),
            }
        )
    return {
        "method_id": method_id,
        "provider": str(report["provider_mode"]),
        "report_path": str(report_path),
        "report_sha256": canonical_json_sha256(report),
        "protocol_sha256": protocol_hash,
        "method_config_sha256": method_hash,
        "source_commit": str(report["source_commit"]),
        "participant_score": participant_score,
        "validated_incumbent_score": incumbent_score,
        "recommendation_gain_over_incumbent": participant_score - incumbent_score,
        "best_baseline_score": best_baseline,
        "regret_to_best_baseline": best_baseline - participant_score,
        "threshold": task.threshold,
        "coverage_audit_after_eight_experiments": copy.deepcopy(coverage),
        "checks": checks,
        "qualified": all(checks.values()),
    }


def _strengthened_baseline_readiness(
    *,
    plan: Mapping[str, Any],
    task_id: str,
    task_report: Mapping[str, Any],
) -> dict[str, Any]:
    policy = plan.get("baseline_readiness_policy")
    if not isinstance(policy, Mapping):
        raise ValueError("strengthened qualification lacks a baseline readiness policy")
    adaptive_algorithm_ids = tuple(str(item) for item in policy["adaptive_algorithm_ids"])
    if len(adaptive_algorithm_ids) != len(set(adaptive_algorithm_ids)):
        raise ValueError("adaptive baseline algorithm IDs must be distinct")
    missing = sorted(set(adaptive_algorithm_ids) - set(plan["algorithms"]))
    if missing:
        raise ValueError(f"unknown adaptive baseline algorithms: {missing}")
    adaptive_families = {
        algorithm_id: str(plan["algorithms"][algorithm_id]["family"])
        for algorithm_id in adaptive_algorithm_ids
    }
    if len(set(adaptive_families.values())) != len(adaptive_families):
        raise ValueError("adaptive baseline algorithms must represent distinct families")
    scores = {
        str(key): float(value)
        for key, value in task_report["validated_scores_by_algorithm"].items()
    }
    threshold = float(get_task(task_id).threshold)
    passing_adaptive_ids = [
        algorithm_id
        for algorithm_id in adaptive_algorithm_ids
        if scores[algorithm_id] >= threshold
    ]
    best_algorithm_id = max(scores, key=scores.__getitem__)
    best_score = scores[best_algorithm_id]
    minimum_passing = int(policy["minimum_passing_adaptive_families"])
    minimum_margin = float(policy["minimum_best_validated_threshold_margin"])
    return {
        "adaptive_algorithm_ids": list(adaptive_algorithm_ids),
        "adaptive_families": adaptive_families,
        "passing_adaptive_algorithm_ids": passing_adaptive_ids,
        "passing_adaptive_family_count": len(passing_adaptive_ids),
        "minimum_passing_adaptive_families": minimum_passing,
        "best_algorithm_id": best_algorithm_id,
        "best_validated_score": best_score,
        "best_validated_threshold_margin": best_score - threshold,
        "minimum_best_validated_threshold_margin": minimum_margin,
        "checks": {
            "two_adaptive_baseline_families_reach_validated_threshold": (
                len(passing_adaptive_ids) >= minimum_passing
            ),
            "best_baseline_has_nontrivial_threshold_margin": (
                best_score - threshold >= minimum_margin
            ),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, default=DEFAULT_PLAN)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--resume-missing", action="store_true")
    parser.add_argument(
        "--participant-run-root",
        type=Path,
        help=(
            "Root containing one externally executed participant report per task; "
            "required before a strengthened plan can release multi-seed execution."
        ),
    )
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
    plan_schema_version = str(plan.get("schema_version", ""))
    strengthened = plan_schema_version.endswith(("0.2-dev", "0.3-dev"))
    participant_protocols = (
        {task_id: _participant_protocol(plan, task_id) for task_id in task_ids}
        if strengthened
        else {}
    )
    for task_id, protocol in participant_protocols.items():
        write_json_atomic(
            args.output / "participant_protocols" / f"{task_id}.json",
            protocol,
        )
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
                    "participant_protocol_sha256": {
                        task_id: canonical_json_sha256(protocol)
                        for task_id, protocol in participant_protocols.items()
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
    source_commit = git_source_commit(ROOT)
    if strengthened:
        participant_root = (
            args.participant_run_root.resolve()
            if args.participant_run_root is not None
            else None
        )
        method_config = _load_object(ROOT / str(plan["participant"]["method_config_path"]))
        for task_id, task_report in task_reports.items():
            baseline_readiness = _strengthened_baseline_readiness(
                plan=plan,
                task_id=task_id,
                task_report=task_report,
            )
            task_report["baseline_readiness"] = baseline_readiness
            task_report["checks"].update(baseline_readiness["checks"])
            minimum_component_range = float(
                plan["qualification_gates"][
                    "minimum_empirical_score_component_range"
                ]
            )
            task_report["checks"]["empirically_active_score_components"] = all(
                float(value) >= minimum_component_range
                for value in task_report[
                    "empirical_score_component_ranges"
                ].values()
            )
            task_report["baseline_qualified"] = all(task_report["checks"].values())
            participant_path = (
                participant_root / task_id / "report.json"
                if participant_root is not None
                else None
            )
            task_report["participant"] = (
                _participant_task_report(
                    plan=plan,
                    task_id=task_id,
                    protocol=participant_protocols[task_id],
                    report_path=participant_path,
                    baseline_report=task_report,
                    method_config=method_config,
                    source_commit=source_commit,
                )
                if participant_path is not None and participant_path.is_file()
                else {
                    "status": "pending",
                    "qualified": False,
                    "expected_report_path": (
                        str(participant_path) if participant_path is not None else None
                    ),
                }
            )
            task_report["qualified"] = bool(
                task_report["baseline_qualified"]
                and task_report["participant"]["qualified"]
            )
    report = {
        "schema_version": (
            "chemworld-static-s0-five-task-qualification-report-0.3-dev"
            if plan_schema_version.endswith("0.3-dev")
            else "chemworld-static-s0-five-task-qualification-report-0.2-dev"
            if strengthened
            else "chemworld-static-s0-five-task-qualification-report-0.1-dev"
        ),
        "qualification_id": plan["qualification_id"],
        "qualification_plan_sha256": canonical_json_sha256(plan),
        "source_commit": source_commit,
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
        "participant_qualification_required": strengthened,
        "participant_reports_complete": bool(
            strengthened
            and all(
                report["participant"].get("status") != "pending"
                for report in task_reports.values()
            )
        ),
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
