#!/usr/bin/env python3
"""Audit Work II estimands, power and formal resource topology."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from scipy.optimize import brentq
from scipy.stats import nct, t

from chemworld.campaign_resources import CampaignResourceCard
from chemworld.eval.provenance import canonical_json_sha256, write_json_atomic
from chemworld.eval.work_ii_formal import (
    EXPECTED_LAW_SUMMARY_EVALUATION_CONTRACT,
    EXPECTED_PARTICIPANT_EXECUTION_CONTRACT,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PLAN = ROOT / "configs/benchmark/work_ii_analysis_plan_v0.1.json"
DEFAULT_OUTPUT = ROOT / "workstreams/flagship_tasks/reports/work-ii-analysis-power-audit.json"


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object")
    return value


def _power(*, effect: float, clusters: int, df: int, alpha: float) -> float:
    critical = t.ppf(1.0 - alpha, df)
    return float(1.0 - nct.cdf(critical, df, effect * clusters**0.5))


def _campaign_card(config: dict[str, Any]) -> CampaignResourceCard:
    campaign = config["campaign"]
    return CampaignResourceCard(
        card_id=str(campaign["card_id"]),
        operation_attempt_limit=int(campaign["operation_attempt_limit"]),
        vessel_start_limit=int(campaign["vessel_start_limit"]),
        final_assay_limit=int(campaign["final_assay_limit"]),
        nonfinal_instrument_use_limit=int(campaign["nonfinal_instrument_use_limit"]),
        stock_limits=dict(campaign["stock_limits"]),
        process_time_limit_s=float(campaign["process_time_limit_s"]),
        implicit_operation_time_s=dict(campaign.get("implicit_operation_time_s", {})),
        operation_repeat_limits=dict(campaign["operation_repeat_limits"]),
        metadata={
            "pilot_id": config["pilot_id"],
            "task_id": config["task_id"],
            "process_time_policy": dict(campaign["process_time_policy"]),
            "closeout_policy": dict(campaign["closeout_policy"]),
            "scope": "one_task_prior_world_cell",
        },
    )


def _expected_closeout_policy(complete_experiments: int) -> dict[str, Any]:
    return {
        "planned_batches": complete_experiments,
        "final_assay_path_operations_per_batch": 2,
        "discard_path_operations_per_batch": 1,
        "final_assay_path_total_operation_reserve": complete_experiments * 2,
        "discard_path_total_operation_reserve": complete_experiments,
        "policy": "participant_controlled_advisory_no_hidden_allocation",
        "automatic_action_repair": False,
        "automatic_closeout": False,
    }


def audit(plan_path: Path, output_path: Path) -> dict[str, Any]:
    plan = _load(plan_path)
    failures: list[dict[str, Any]] = []
    binding = plan["design_binding"]
    design_path = ROOT / str(binding["path"])
    design = _load(design_path)
    design_hash = canonical_json_sha256(design)
    if design_hash != binding["sha256"]:
        failures.append({"check": "design_binding_current"})

    public = design["world_cohort"]["public_formal"]
    public_worlds = sum(len(seeds) for seeds in public["task_world_seeds"].values())
    prior_arm_count = len(design["prior_arms"])
    scheduled_cells = public_worlds * prior_arm_count
    attempt_contract = design["provider_attempt_contract"]
    planned_provider_attempts = scheduled_cells * int(attempt_contract["initial_attempts_per_cell"])
    provider_attempt_hard_cap = scheduled_cells * int(
        attempt_contract["maximum_total_provider_attempts_per_cell"]
    )
    if planned_provider_attempts != int(attempt_contract["public_matrix_initial_attempt_count"]):
        failures.append({"check": "provider_attempt_initial_denominator"})
    if provider_attempt_hard_cap != int(
        attempt_contract["public_matrix_provider_attempt_hard_cap"]
    ):
        failures.append({"check": "provider_attempt_hard_cap"})
    blind_contract = design["blind_evaluator_contract"]
    final_recommendations = scheduled_cells * int(
        blind_contract["participant_final_recommendations_per_cell"]
    )
    blind_targets = scheduled_cells * len(blind_contract["blind_targets_per_cell"])
    blind_executions = blind_targets * int(blind_contract["blind_replicates_per_target"])
    if final_recommendations != int(blind_contract["public_matrix_final_recommendation_count"]):
        failures.append({"check": "final_recommendation_denominator"})
    if blind_targets != int(blind_contract["public_matrix_blind_target_count"]):
        failures.append({"check": "blind_target_denominator"})
    if blind_executions != int(blind_contract["public_matrix_blind_execution_count"]):
        failures.append({"check": "blind_execution_denominator"})
    population = plan["analysis_population"]
    if public_worlds != population["independent_task_world_clusters"]:
        failures.append({"check": "independent_cluster_denominator"})
    if scheduled_cells != population["scheduled_public_cells"]:
        failures.append({"check": "scheduled_cell_denominator"})

    participant_contract = design.get("participant_execution_contract")
    if participant_contract != EXPECTED_PARTICIPANT_EXECUTION_CONTRACT:
        failures.append({"check": "participant_execution_contract"})
    law_summary_contract = plan.get("law_summary_evaluation_contract")
    if law_summary_contract != EXPECTED_LAW_SUMMARY_EVALUATION_CONTRACT:
        failures.append({"check": "law_summary_evaluation_contract"})
    variance_contract = plan.get("variance_component_contract")
    expected_variance_keys = {
        "world_cluster",
        "task_mechanism_family",
        "prior_arm",
        "participant_model_and_scaffold",
        "provider_session",
        "provider_repeat",
        "task_by_prior_interaction",
        "model_by_session_interaction",
        "operations_experiments_and_checkpoints",
    }
    if not isinstance(variance_contract, dict) or set(variance_contract) != expected_variance_keys:
        failures.append({"check": "variance_component_contract"})

    resource_rows: list[dict[str, Any]] = []
    total_sessions = 0
    total_model_calls = 0
    total_experiments = 0
    total_operations = 0
    total_vessel_starts = 0
    total_final_assays = 0
    total_nonfinal_instruments = 0
    total_process_time_s = 0.0
    total_input = 0
    total_uncached = 0
    total_output = 0
    topology_wall = 0.0
    provider_ids: set[str] = set()
    expected_stages = plan["checkpoint_contract"]["stage_ids"]
    for task in design["tasks"]:
        config = _load(ROOT / str(task["campaign_config"]))
        task_id = str(task["task_id"])
        task_worlds = len(public["task_world_seeds"][task_id])
        cells = task_worlds * prior_arm_count
        campaign = config["campaign"]
        resources = config["method_resources"]
        provider = config["provider"]
        provider_ids.add(str(provider["id"]))
        execution = config["execution"]
        complete_experiments = int(campaign["complete_experiments"])
        operation_limit = int(campaign["operation_attempt_limit"])
        card = _campaign_card(config)
        closeout_policy = dict(campaign["closeout_policy"])
        process_time_policy = dict(campaign["process_time_policy"])
        if config.get("snapshot_stages") != expected_stages:
            failures.append({"check": "neutral_snapshot_stages", "task_id": task_id})
        if complete_experiments != int(
            design["campaign_contract"]["complete_experiments_per_cell"]
        ):
            failures.append({"check": "complete_experiment_limit", "task_id": task_id})
        if (
            campaign["checkpoint_complete_experiments"]
            != design["campaign_contract"]["checkpoint_complete_experiments"]
        ):
            failures.append({"check": "campaign_checkpoint_schedule", "task_id": task_id})
        if (
            int(resources["operation_limit"]) != operation_limit
            or int(resources["complete_experiment_limit"]) != complete_experiments
            or resources["checkpoint_complete_experiments"] != [1, 2, 4]
        ):
            failures.append({"check": "method_campaign_resource_alignment", "task_id": task_id})
        if int(resources["model_call_limit"]) != 1:
            failures.append({"check": "model_call_limit", "task_id": task_id})
        if closeout_policy != _expected_closeout_policy(complete_experiments):
            failures.append({"check": "closeout_policy", "task_id": task_id})
        process_time_envelope = sum(
            float(process_time_policy.get(key, 0.0))
            for key in (
                "required_stage_max_s",
                "repeat_allowance_s",
                "quench_transfer_allowance_s",
            )
        )
        if abs(process_time_envelope - float(campaign["process_time_limit_s"])) > 1.0e-9:
            failures.append({"check": "process_time_envelope", "task_id": task_id})
        timeout_contract = EXPECTED_PARTICIPANT_EXECUTION_CONTRACT["timeout_contract_s"]
        if float(provider["request_timeout_s"]) != float(timeout_contract["request"]) or float(
            provider["finalization_timeout_s"]
        ) != float(timeout_contract["finalization"]):
            failures.append({"check": "provider_timeout_contract", "task_id": task_id})
        if (
            int(execution["max_concurrency"]) != 3
            or int(execution["within_cell_concurrency"]) != 1
            or execution["parallelization_unit"] != "same_seed_prior_arm_triplet"
        ):
            failures.append({"check": "execution_concurrency", "task_id": task_id})
        total_sessions += cells
        total_model_calls += cells * int(resources["model_call_limit"])
        total_experiments += cells * complete_experiments
        total_operations += cells * operation_limit
        total_vessel_starts += cells * int(campaign["vessel_start_limit"])
        total_final_assays += cells * int(campaign["final_assay_limit"])
        total_nonfinal_instruments += cells * int(campaign["nonfinal_instrument_use_limit"])
        total_process_time_s += cells * float(campaign["process_time_limit_s"])
        total_input += cells * int(resources["input_token_limit"])
        total_uncached += cells * int(resources["uncached_input_token_limit"])
        total_output += cells * int(resources["output_token_limit"])
        task_wall = task_worlds * float(resources["wall_time_limit_s"])
        topology_wall += task_wall
        resource_rows.append(
            {
                "task_id": task_id,
                "worlds": task_worlds,
                "cells": cells,
                "campaign_resource_card": card.to_dict(),
                "per_cell_method_limits": dict(resources),
                "per_cell_provider_timeouts_s": {
                    "request": float(provider["request_timeout_s"]),
                    "finalization": float(provider["finalization_timeout_s"]),
                },
                "matrix_upper_bounds": {
                    "complete_experiments": cells * complete_experiments,
                    "operation_attempts": cells * operation_limit,
                    "vessel_starts": cells * int(campaign["vessel_start_limit"]),
                    "final_assays": cells * int(campaign["final_assay_limit"]),
                    "nonfinal_instrument_uses": cells
                    * int(campaign["nonfinal_instrument_use_limit"]),
                    "stock_limits": {
                        stock_id: cells * float(limit)
                        for stock_id, limit in campaign["stock_limits"].items()
                    },
                    "process_time_s": cells * float(campaign["process_time_limit_s"]),
                    "model_calls": cells * int(resources["model_call_limit"]),
                    "input_tokens": cells * int(resources["input_token_limit"]),
                    "uncached_input_tokens": cells * int(resources["uncached_input_token_limit"]),
                    "output_tokens": cells * int(resources["output_token_limit"]),
                    "serial_seed_triplet_wall_time_s": task_wall,
                },
            }
        )

    power = plan["power_design"]
    clusters = int(power["independent_clusters"])
    df = int(power["residual_degrees_of_freedom"])
    alpha = float(power["alpha"])
    planning_effect = float(power["planning_standardized_effect"])
    planning_power = _power(effect=planning_effect, clusters=clusters, df=df, alpha=alpha)
    mde_80 = float(
        brentq(
            lambda effect: (
                _power(
                    effect=effect,
                    clusters=clusters,
                    df=df,
                    alpha=alpha,
                )
                - 0.80
            ),
            1.0e-6,
            5.0,
        )
    )
    if planning_power < float(power["minimum_required_power_at_planning_effect"]):
        failures.append({"check": "planning_power"})

    maximum_attempts_per_cell = int(attempt_contract["maximum_total_provider_attempts_per_cell"])
    report = {
        "schema_version": "chemworld-work-ii-analysis-power-audit-0.2",
        "analysis_plan_path": str(plan_path.relative_to(ROOT)).replace("\\", "/"),
        "analysis_plan_sha256": canonical_json_sha256(plan),
        "design_sha256": design_hash,
        "status": "passed" if not failures else "failed",
        "formal_result": False,
        "participant_provider_calls": 0,
        "participant_execution_contract_audit": {
            "status": "passed" if not failures else "failed",
            "contract_sha256": canonical_json_sha256(participant_contract),
            "same_session_operation_experiment_checkpoint_receipt": True,
            "automatic_action_repair": False,
            "automatic_closeout": False,
            "checkpoint_provider_calls": 0,
            "final_method_qualification_is_separate_w2_10": True,
        },
        "denominators": {
            "tasks": len(design["tasks"]),
            "independent_task_world_clusters": public_worlds,
            "prior_arms": prior_arm_count,
            "scheduled_participant_cells": scheduled_cells,
            "provider_repeats_per_cell": population["provider_repeats_per_cell"],
            "provider_attempts_initial_planned": planned_provider_attempts,
            "provider_attempts_hard_cap": provider_attempt_hard_cap,
            "participant_final_recommendations": final_recommendations,
            "blind_validation_targets": blind_targets,
            "blind_validation_executions": blind_executions,
        },
        "denominator_ledger": {
            "host_provider_process_attempt": {
                "initial_planned": planned_provider_attempts,
                "hard_cap": provider_attempt_hard_cap,
            },
            "accepted_participant_provider_session": {
                "scheduled": total_sessions,
                "actual_source": "per_session_provider_receipts",
            },
            "mcp_tool_call": {
                "hard_cap": None,
                "actual_source": "per_session_mcp_tool_call_receipts",
                "note": "separate from physical operation attempts",
            },
            "operation_attempt": {"hard_cap": total_operations},
            "committed_operation": {
                "hard_cap": total_operations,
                "actual_source": "participant_trajectory_transaction_status",
            },
            "complete_experiment": {"scheduled": total_experiments},
            "participant_cell": {"scheduled": scheduled_cells},
            "blind_evaluator_execution": {"scheduled": blind_executions},
        },
        "power": {
            "alpha_one_sided": alpha,
            "clusters": clusters,
            "residual_degrees_of_freedom": df,
            "planning_standardized_effect": planning_effect,
            "power_at_planning_effect": planning_power,
            "minimum_detectable_standardized_effect_80pct": mde_80,
            "sensitivity_table": [
                {
                    "standardized_effect": effect,
                    "power": _power(effect=effect, clusters=clusters, df=df, alpha=alpha),
                }
                for effect in (0.3, 0.4, 0.5, 0.6, 0.7, 0.8)
            ],
            "interpretation": (
                "The frozen 25-cluster design is powered for moderate-to-large effects, "
                "not small effects."
            ),
        },
        "resource_topology": {
            "task_rows": resource_rows,
            "scheduled_accepted_provider_sessions": total_sessions,
            "scheduled_model_calls": total_model_calls,
            "provider_attempt_hard_model_call_cap": total_model_calls * maximum_attempts_per_cell,
            "provider_attempts_initial_planned": planned_provider_attempts,
            "provider_attempts_hard_cap": provider_attempt_hard_cap,
            "maximum_provider_attempts_per_cell": maximum_attempts_per_cell,
            "complete_experiments": total_experiments,
            "operation_attempt_limit": total_operations,
            "vessel_start_limit": total_vessel_starts,
            "final_assay_limit": total_final_assays,
            "nonfinal_instrument_use_limit": total_nonfinal_instruments,
            "process_time_limit_s": total_process_time_s,
            "accepted_cell_input_token_limit": total_input,
            "accepted_cell_uncached_input_token_limit": total_uncached,
            "accepted_cell_output_token_limit": total_output,
            "provider_attempt_hard_input_token_limit": total_input * maximum_attempts_per_cell,
            "provider_attempt_hard_uncached_input_token_limit": total_uncached
            * maximum_attempts_per_cell,
            "provider_attempt_hard_output_token_limit": total_output * maximum_attempts_per_cell,
        },
        "execution_budget_and_eta": {
            "same_world_prior_arm_triplet_concurrency": 3,
            "within_cell_concurrency": 1,
            "serial_seed_triplet_count": public_worlds,
            "initial_schedule_wall_limit_s": topology_wall,
            "initial_schedule_wall_limit_h": topology_wall / 3600.0,
            "all_infrastructure_resumes_wall_hard_cap_s": topology_wall * maximum_attempts_per_cell,
            "all_infrastructure_resumes_wall_hard_cap_h": topology_wall
            * maximum_attempts_per_cell
            / 3600.0,
            "qualified_expected_wall_time_s": None,
            "qualified_expected_wall_time_status": (
                "pending_final_current_method_w2_10_qualification"
            ),
            "result_direction_early_stopping_allowed": False,
        },
        "currency_budget": {
            "formal_provider_ids": sorted(provider_ids),
            "provider_currency_pricing_verified": False,
            "approved_currency_ceiling": None,
            "formal_currency_ceiling_approved": False,
            "unknown_cost_must_not_be_reported_as_zero": True,
        },
        "variance_component_contract": variance_contract,
        "law_summary_evaluation_contract": law_summary_contract,
        "w2_06_contract_complete": not failures,
        "w2_10_final_method_qualification_complete": False,
        "w2_07_completed_components": {
            "power": not failures,
            "variance_and_confounding_boundary": not failures,
            "campaign_resource_cards": not failures,
            "token_wall_concurrency_and_retry_bounds": not failures,
            "currency_ceiling": False,
            "qualified_expected_eta": False,
        },
        "w2_05_complete": not failures,
        "w2_07_complete": False,
        "w2_07_remaining_blockers": [
            "user-approved formal currency ceiling",
            "qualified formal runner ETA calibration",
        ],
        "failures": failures,
    }
    write_json_atomic(output_path, report)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, default=DEFAULT_PLAN)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    report = audit(args.plan.resolve(), args.output.resolve())
    print(
        json.dumps(
            {
                "status": report["status"],
                "clusters": report["denominators"]["independent_task_world_clusters"],
                "cells": report["denominators"]["scheduled_participant_cells"],
                "power_at_d_0_6": report["power"]["power_at_planning_effect"],
                "mde_80": report["power"]["minimum_detectable_standardized_effect_80pct"],
                "failure_count": len(report["failures"]),
                "output": str(args.output),
            },
            sort_keys=True,
        ),
        flush=True,
    )
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
