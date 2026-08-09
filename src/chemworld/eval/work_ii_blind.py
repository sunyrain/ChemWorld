"""Outcome-blind evaluator plans for Work II final recommendations."""

from __future__ import annotations

import hashlib
from collections.abc import Mapping
from copy import deepcopy
from typing import Any

from chemworld.eval.provenance import canonical_json_sha256

BLIND_EVALUATOR_VERSION = "chemworld-work-ii-blind-evaluator-plan-0.1"


def _experiment_rows(summary: Mapping[str, Any]) -> dict[int, dict[str, Any]]:
    analysis = summary.get("analysis")
    if not isinstance(analysis, Mapping):
        raise ValueError("formal cell summary lacks analysis")
    rows = analysis.get("experiments")
    if not isinstance(rows, list):
        raise ValueError("formal cell summary lacks experiment rows")
    experiments: dict[int, dict[str, Any]] = {}
    for row in rows:
        if not isinstance(row, Mapping):
            raise ValueError("formal cell experiment row is malformed")
        index = row.get("experiment_index")
        score = row.get("leaderboard_score")
        actions = row.get("operations")
        if (
            isinstance(index, bool)
            or not isinstance(index, int)
            or isinstance(score, bool)
            or not isinstance(score, int | float)
            or not isinstance(actions, list)
            or not actions
            or not all(isinstance(action, Mapping) for action in actions)
        ):
            raise ValueError("formal cell experiment is not blind-replayable")
        if index in experiments:
            raise ValueError("formal cell experiment indices are not unique")
        final_action = actions[-1]
        if final_action.get("operation") != "measure" or final_action.get("instrument") != (
            "final_assay"
        ):
            raise ValueError("blind-replayable experiment must end in final_assay")
        experiments[index] = {
            "experiment_index": index,
            "leaderboard_score": float(score),
            "operations": [deepcopy(dict(action)) for action in actions],
        }
    if set(experiments) != {1, 2, 3, 4}:
        raise ValueError("blind evaluator requires the exact four completed experiments")
    return experiments


def _paired_noise(cell_key_sha256: str, replicate_index: int) -> dict[str, Any]:
    payload = f"work-ii-blind-v0.1:{cell_key_sha256}:{replicate_index}".encode()
    digest = hashlib.sha256(payload).hexdigest()
    return {
        "paired_noise_id_sha256": digest,
        "observation_seed": int(digest[:8], 16) % 2_147_483_647,
        "observation_noise_namespace": (
            f"work-ii-blind-v0.1-{cell_key_sha256[:16]}-rep-{replicate_index:02d}"
        ),
    }


def build_blind_evaluation_plan(
    cell: Mapping[str, Any],
    summary: Mapping[str, Any],
    contract: Mapping[str, Any],
) -> dict[str, Any]:
    """Bind a qualified cell's committed choice to six evaluator-owned replays."""

    if summary.get("completed") is not True:
        raise ValueError("blind evaluator plan requires a qualified completed cell")
    if int(contract.get("participant_final_recommendations_per_cell", -1)) != 1:
        raise ValueError("blind evaluator final-recommendation denominator drifted")
    targets = contract.get("blind_targets_per_cell")
    if targets != ["observed_incumbent", "participant_final_recommendation"]:
        raise ValueError("blind evaluator target contract drifted")
    replicates = int(contract.get("blind_replicates_per_target", -1))
    if replicates != 3:
        raise ValueError("blind evaluator replicate contract drifted")
    if (
        contract.get("paired_noise_within_replicate") is not True
        or contract.get("participant_feedback_from_blind_evaluator") is not False
        or int(contract.get("evaluator_provider_calls", -1)) != 0
        or contract.get("evaluator_trajectory_separate_from_participant") is not True
        or contract.get("evaluator_resources_excluded_from_participant_ledger") is not True
    ):
        raise ValueError("blind evaluator isolation contract drifted")

    experiments = _experiment_rows(summary)
    analysis = summary["analysis"]
    recommendation = analysis.get("final_recommendation")
    if not isinstance(recommendation, Mapping):
        raise ValueError("formal cell lacks a committed final recommendation")
    recommendation_digest = canonical_json_sha256(recommendation)
    if recommendation_digest != analysis.get("final_recommendation_sha256"):
        raise ValueError("final recommendation digest differs from participant receipt")
    selected_index = recommendation.get("selected_experiment_index")
    if isinstance(selected_index, bool) or selected_index not in experiments:
        raise ValueError("final recommendation does not select a completed experiment")
    incumbent_index = min(
        experiments,
        key=lambda index: (-experiments[index]["leaderboard_score"], index),
    )
    if incumbent_index != analysis.get("observed_incumbent_experiment_index"):
        raise ValueError("observed incumbent differs from the frozen tie rule")

    execution_rows: list[dict[str, Any]] = []
    target_rows: list[dict[str, Any]] = []
    target_indices = {
        "observed_incumbent": incumbent_index,
        "participant_final_recommendation": int(selected_index),
    }
    for target in targets:
        experiment = experiments[target_indices[target]]
        action_plan = experiment["operations"]
        action_plan_sha256 = canonical_json_sha256(action_plan)
        target_rows.append(
            {
                "target": target,
                "source_experiment_index": experiment["experiment_index"],
                "participant_observed_leaderboard_score": experiment[
                    "leaderboard_score"
                ],
                "action_plan": action_plan,
                "action_plan_sha256": action_plan_sha256,
            }
        )
        for replicate_index in range(1, replicates + 1):
            execution_rows.append(
                {
                    "execution_index": len(execution_rows) + 1,
                    "execution_id": (
                        f"{cell['cell_id']}--blind-{target}--rep-{replicate_index:02d}"
                    ),
                    "target": target,
                    "replicate_index": replicate_index,
                    "source_experiment_index": experiment["experiment_index"],
                    "action_plan_sha256": action_plan_sha256,
                    **_paired_noise(str(cell["cell_key_sha256"]), replicate_index),
                }
            )
    plan: dict[str, Any] = {
        "schema_version": BLIND_EVALUATOR_VERSION,
        "formal_result": False,
        "cell_id": cell["cell_id"],
        "cell_key_sha256": cell["cell_key_sha256"],
        "task_id": cell["task_id"],
        "world_seed": cell["world_seed"],
        "recommendation_sha256": recommendation_digest,
        "participant_final_recommendation_count": 1,
        "blind_target_count": len(target_rows),
        "blind_execution_count": len(execution_rows),
        "evaluator_provider_call_count": 0,
        "participant_operation_denominator_impact": 0,
        "participant_feedback_allowed": False,
        "targets": target_rows,
        "executions": execution_rows,
    }
    plan["plan_sha256"] = canonical_json_sha256(plan)
    return plan


def validate_blind_evaluation_plan(plan: Mapping[str, Any]) -> list[str]:
    """Check plan self-binding, paired noise and frozen denominators."""

    errors: list[str] = []
    if plan.get("schema_version") != BLIND_EVALUATOR_VERSION:
        errors.append("unexpected blind evaluator plan schema")
    expected_hash = canonical_json_sha256(
        {key: value for key, value in plan.items() if key != "plan_sha256"}
    )
    if plan.get("plan_sha256") != expected_hash:
        errors.append("blind evaluator plan self-hash mismatch")
    targets = plan.get("targets")
    executions = plan.get("executions")
    if not isinstance(targets, list) or len(targets) != 2:
        errors.append("blind evaluator plan does not contain two targets")
        targets = []
    if not isinstance(executions, list) or len(executions) != 6:
        errors.append("blind evaluator plan does not contain six executions")
        executions = []
    target_digests = {
        str(target.get("target")): target.get("action_plan_sha256")
        for target in targets
        if isinstance(target, Mapping)
    }
    for execution in executions:
        if not isinstance(execution, Mapping):
            errors.append("blind evaluator execution row is malformed")
            continue
        if target_digests.get(str(execution.get("target"))) != execution.get(
            "action_plan_sha256"
        ):
            errors.append("blind evaluator action plan binding mismatch")
    for replicate_index in range(1, 4):
        rows = [
            row
            for row in executions
            if isinstance(row, Mapping) and row.get("replicate_index") == replicate_index
        ]
        paired_ids = {row.get("paired_noise_id_sha256") for row in rows}
        seeds = {row.get("observation_seed") for row in rows}
        namespaces = {row.get("observation_noise_namespace") for row in rows}
        if len(rows) != 2 or len(paired_ids) != 1 or len(seeds) != 1 or len(namespaces) != 1:
            errors.append(f"blind evaluator replicate {replicate_index} is not paired")
    if (
        plan.get("evaluator_provider_call_count") != 0
        or plan.get("participant_operation_denominator_impact") != 0
        or plan.get("participant_feedback_allowed") is not False
    ):
        errors.append("blind evaluator isolation invariant failed")
    return errors


__all__ = [
    "BLIND_EVALUATOR_VERSION",
    "build_blind_evaluation_plan",
    "validate_blind_evaluation_plan",
]
