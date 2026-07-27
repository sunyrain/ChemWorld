"""Postrun replay and descriptive audit for S0 static optimization."""

from __future__ import annotations

import copy
import hashlib
import json
import statistics
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from chemworld.agents.electrochemical_single_stage import (
    electrochemical_single_stage_unit_vector_from_parameters,
)
from chemworld.agents.static_optimization import StaticOptimizationPlan
from chemworld.agents.task_recipes import (
    electrochemical_recipe_unit_vector_from_parameters,
)
from chemworld.eval import crystallization_predictive
from chemworld.eval.electrochemical_predictive import (
    PREDICTIVE_PAIRED_REPLICATE_COUNT,
    PREDICTIVE_PHYSICAL_EXPERIMENT_COUNT,
    build_electrochemical_prediction_queries,
    classify_metric_direction,
    metric_value_from_result,
    parse_counterfactual_predictions,
    predictive_measurement_slots,
    predictive_schema_version,
    score_predictive_validation,
)
from chemworld.eval.provenance import canonical_json_sha256 as canonical_sha256
from chemworld.eval.static_optimization_execution import (
    StaticOptimizationExperimentSession,
    static_optimization_workflow_mode,
)
from chemworld.eval.static_optimization_protocol import (
    exploration_experiment_count,
    validate_static_optimization_protocol,
)
from chemworld.eval.static_optimization_seeds import (
    exploration_observation_seed,
    predictive_observation_seed,
)
from chemworld.eval.world_understanding import (
    ReferenceWorldClaim,
    parse_world_understanding_claims,
    score_world_understanding,
)
from chemworld.physchem.electrochemical_task_contract import (
    ELECTROCHEMICAL_WORKFLOW_STATIC_SINGLE_STAGE,
)

STATIC_OPTIMIZATION_POSTRUN_VERSION = "chemworld-static-optimization-postrun-0.4-s0"


def _plan_from_receipt(payload: Mapping[str, Any]) -> StaticOptimizationPlan:
    return StaticOptimizationPlan(
        experiment_intent=str(payload["experiment_intent"]),
        search_vector=tuple(float(item) for item in payload["search_vector"]),
        requested_measurement_slots=tuple(
            str(item) for item in payload["requested_measurement_slots"]
        ),
        measurement_objective=str(payload["measurement_objective"]),
        expected_effect=str(payload["expected_effect"]),
        uncertainty=float(payload["uncertainty"]),
        recipe_parameters=(
            copy.deepcopy(dict(payload["recipe_parameters"]))
            if isinstance(payload.get("recipe_parameters"), Mapping)
            else None
        ),
    )


def _predictive_plan(
    recipe_parameters: Mapping[str, int | float],
    *,
    task_id: str,
    query_id: str,
    arm: str,
    electrochemical_workflow_mode: str,
) -> StaticOptimizationPlan:
    if task_id == "reaction-to-crystallization":
        vector = (
            crystallization_predictive.crystallization_single_stage_unit_vector_from_parameters(
                recipe_parameters
            )
        )
        measurement_slots = crystallization_predictive.PREDICTIVE_MEASUREMENT_SLOTS
    else:
        vector = (
            electrochemical_single_stage_unit_vector_from_parameters(recipe_parameters)
            if electrochemical_workflow_mode
            == ELECTROCHEMICAL_WORKFLOW_STATIC_SINGLE_STAGE
            else electrochemical_recipe_unit_vector_from_parameters(
                dict(recipe_parameters)
            )
        )
        measurement_slots = predictive_measurement_slots(electrochemical_workflow_mode)
    return StaticOptimizationPlan(
        experiment_intent=f"frozen predictive assay for {query_id} {arm}",
        search_vector=tuple(float(value) for value in vector),
        requested_measurement_slots=tuple(measurement_slots),
        measurement_objective="measure the frozen predictive endpoint set",
        expected_effect="held-out result withheld from the model",
        uncertainty=0.0,
        recipe_parameters=copy.deepcopy(dict(recipe_parameters)),
    )


def replay_static_optimization_receipt(
    receipt: Mapping[str, Any],
    protocol: Mapping[str, Any],
) -> dict[str, Any]:
    """Replay all completed experiments in one static receipt exactly."""

    pair = receipt["cell"]
    task_id = str(pair["task_id"])
    seed = int(pair["world_seed"])
    mismatches: list[dict[str, Any]] = []
    for recorded in receipt["experiments"]:
        recorded_result = recorded["result"]
        experiment_index = int(recorded_result["experiment_index"])
        plan = _plan_from_receipt(recorded_result["plan"])
        with StaticOptimizationExperimentSession(
            task_id=task_id,
            seed=seed,
            experiment_horizon=1,
            experiment_index_offset=experiment_index,
            observation_seed=exploration_observation_seed(task_id, seed),
            observation_noise_namespace=(
                f"{protocol['observation_noise_namespace']}-{task_id}-"
                f"experiment-{experiment_index:03d}"
            ),
            electrochemical_workflow_mode=static_optimization_workflow_mode(
                protocol
            ),
        ) as session:
            replayed_result = session.execute(plan).to_dict()
        base_fields = (
            "schema_version",
            "interface_version",
            "task_id",
            "experiment_index",
            "plan",
            "executed_steps",
            "measurement_evidence",
            "terminal_summary",
            "completed",
            "operation_count",
            "peak_safety_risk",
        )
        optional_fields = (
            "compiled_operation_count",
            "runtime_operation_cap",
            "runtime_margin_used",
        )
        fields = base_fields + tuple(
            field for field in optional_fields if field in recorded_result
        )
        mismatch_fields = [
            field
            for field in fields
            if replayed_result.get(field) != recorded_result.get(field)
        ]
        if mismatch_fields:
            mismatches.append(
                {
                    "experiment_index": experiment_index,
                    "mismatch_fields": mismatch_fields,
                    "recorded_result_sha256": canonical_sha256(recorded_result),
                    "replayed_result_sha256": canonical_sha256(replayed_result),
                }
            )
    return {
        "cell_id": str(pair["cell_id"]),
        "task_id": task_id,
        "method_id": str(receipt["method_id"]),
        "cell_status": str(receipt["cell_status"]),
        "completed_prefix_only": receipt["cell_status"] != "completed",
        "replayed_experiment_count": len(receipt["experiments"]),
        "verified": not mismatches,
        "mismatches": mismatches,
    }


def replay_static_optimization_validation(
    receipt: Mapping[str, Any],
) -> dict[str, Any]:
    """Replay blind incumbent and recommendation validation replicates exactly."""

    validation = receipt.get("validation")
    if not isinstance(validation, Mapping):
        return {
            "cell_id": str(receipt["cell"]["cell_id"]),
            "present": False,
            "replayed_experiment_count": 0,
            "verified": True,
            "targets": [],
        }
    task_id = str(receipt["cell"]["task_id"])
    world_seed = int(receipt["cell"]["world_seed"])
    target_rows: list[dict[str, Any]] = []
    for target_name in ("incumbent", "recommendation"):
        target = validation[target_name]
        plan = _plan_from_receipt(target["plan"])
        mismatches: list[dict[str, Any]] = []
        for replicate in target["replicates"]:
            recorded_result = replicate["result"]
            experiment_index = int(recorded_result["experiment_index"])
            with StaticOptimizationExperimentSession(
                task_id=task_id,
                seed=world_seed,
                experiment_horizon=1,
                experiment_index_offset=experiment_index,
                observation_seed=int(replicate["observation_seed"]),
                observation_noise_namespace=str(
                    replicate["observation_noise_namespace"]
                ),
                electrochemical_workflow_mode=static_optimization_workflow_mode(
                    receipt
                ),
            ) as session:
                replayed_result = session.execute(plan).to_dict()
            fields = tuple(recorded_result)
            mismatch_fields = [
                field
                for field in fields
                if replayed_result.get(field) != recorded_result.get(field)
            ]
            if mismatch_fields:
                mismatches.append(
                    {
                        "replicate_index": int(replicate["replicate_index"]),
                        "experiment_index": experiment_index,
                        "mismatch_fields": mismatch_fields,
                        "recorded_result_sha256": canonical_sha256(recorded_result),
                        "replayed_result_sha256": canonical_sha256(replayed_result),
                    }
                )
        target_rows.append(
            {
                "target": target_name,
                "replayed_experiment_count": len(target["replicates"]),
                "verified": not mismatches,
                "mismatches": mismatches,
            }
        )
    return {
        "cell_id": str(receipt["cell"]["cell_id"]),
        "present": True,
        "replayed_experiment_count": sum(
            item["replayed_experiment_count"] for item in target_rows
        ),
        "verified": all(item["verified"] for item in target_rows),
        "targets": target_rows,
    }


def replay_static_optimization_predictive(
    receipt: Mapping[str, Any],
    protocol: Mapping[str, Any],
) -> dict[str, Any]:
    """Regenerate, replay, and rescore the frozen predictive validation layer."""

    contract = protocol.get("world_understanding")
    enabled = bool(
        isinstance(contract, Mapping)
        and contract.get("predictive_score_enabled", False)
    )
    recorded = receipt.get("predictive_validation")
    cell_id = str(receipt["cell"]["cell_id"])
    if not enabled:
        return {
            "cell_id": cell_id,
            "present": recorded is not None,
            "enabled": False,
            "replayed_experiment_count": 0,
            "verified": recorded is None,
            "mismatches": (
                [] if recorded is None else ["unexpected_predictive_validation"]
            ),
        }
    if not isinstance(recorded, Mapping):
        return {
            "cell_id": cell_id,
            "present": False,
            "enabled": True,
            "replayed_experiment_count": 0,
            "verified": False,
            "mismatches": ["missing_predictive_validation"],
        }
    task_id = str(receipt["cell"]["task_id"])
    world_seed = int(receipt["cell"]["world_seed"])
    history = receipt["public_history"]
    workflow_mode = static_optimization_workflow_mode(protocol)
    queries = (
        crystallization_predictive.build_crystallization_prediction_queries(history)
        if task_id == "reaction-to-crystallization"
        else build_electrochemical_prediction_queries(
            history,
            electrochemical_workflow_mode=workflow_mode,
        )
    )
    public_queries = [query.to_public_dict() for query in queries]
    predictions = parse_counterfactual_predictions(
        recorded["predictions"],
        queries=queries,
    )
    normalized_predictions = [prediction.to_dict() for prediction in predictions]
    mismatches: list[str] = []
    expected_schema_version = (
        crystallization_predictive.CRYSTALLIZATION_PREDICTIVE_VERSION
        if task_id == "reaction-to-crystallization"
        else predictive_schema_version(workflow_mode)
    )
    if recorded.get("schema_version") != expected_schema_version:
        mismatches.append("schema_version")
    if recorded.get("frozen_before_model_prediction") is not True:
        mismatches.append("frozen_before_model_prediction")
    if recorded.get("executed_after_model_prediction") is not True:
        mismatches.append("executed_after_model_prediction")
    if recorded.get("feedback_returned_to_agent") is not False:
        mismatches.append("feedback_returned_to_agent")
    if int(recorded.get("query_count", -1)) != len(queries):
        mismatches.append("query_count")
    if int(recorded.get("paired_replicates_per_query", -1)) != (
        PREDICTIVE_PAIRED_REPLICATE_COUNT
    ):
        mismatches.append("paired_replicates_per_query")
    if int(recorded.get("planned_physical_experiment_count", -1)) != (
        PREDICTIVE_PHYSICAL_EXPERIMENT_COUNT
    ):
        mismatches.append("planned_physical_experiment_count")
    if int(recorded.get("completed_physical_experiment_count", -1)) != (
        PREDICTIVE_PHYSICAL_EXPERIMENT_COUNT
    ):
        mismatches.append("completed_physical_experiment_count")
    if recorded.get("query_set_sha256") != canonical_sha256(public_queries):
        mismatches.append("query_set_sha256")
    if recorded.get("query_sha256") != [query.query_sha256 for query in queries]:
        mismatches.append("query_sha256")
    if recorded.get("predictions_sha256") != canonical_sha256(
        normalized_predictions
    ):
        mismatches.append("predictions_sha256")
    if recorded.get("predictions") != normalized_predictions:
        mismatches.append("predictions")
    if recorded.get("model_call_count_before_execution") != recorded.get(
        "model_call_count_after_execution"
    ):
        mismatches.append("additional_model_calls")
    recommendation = receipt["final_synthesis"]["recommendation"]
    if recommendation.get("counterfactual_predictions") != normalized_predictions:
        mismatches.append("recommendation_predictions")
    synthesis_audit = receipt["final_synthesis"]["synthesis_audit"]
    if synthesis_audit.get("predictive_query_sha256") != [
        query.query_sha256 for query in queries
    ]:
        mismatches.append("synthesis_query_sha256")
    if synthesis_audit.get("predictive_query_set_sha256") != canonical_sha256(
        public_queries
    ):
        mismatches.append("synthesis_query_set_sha256")
    recorded_query_rows = recorded.get("queries")
    if not isinstance(recorded_query_rows, list) or len(recorded_query_rows) != len(
        queries
    ):
        raise ValueError("predictive receipt query rows do not match the frozen count")
    recomputed_query_results: list[dict[str, Any]] = []
    replayed_count = 0
    horizon = int(protocol["horizon"])
    for query_index, (query, row) in enumerate(
        zip(queries, recorded_query_rows, strict=True)
    ):
        if not isinstance(row, Mapping):
            raise ValueError("predictive receipt query row must be an object")
        if row.get("query_id") != query.query_id:
            mismatches.append(f"{query.query_id}:query_id")
        if row.get("query_sha256") != query.query_sha256:
            mismatches.append(f"{query.query_id}:query_sha256")
        if row.get("query") != query.to_public_dict():
            mismatches.append(f"{query.query_id}:query")
        reference_plan = _predictive_plan(
            query.reference_recipe_parameters,
            task_id=task_id,
            query_id=query.query_id,
            arm="reference",
            electrochemical_workflow_mode=workflow_mode,
        )
        intervention_plan = _predictive_plan(
            query.intervention_recipe_parameters,
            task_id=task_id,
            query_id=query.query_id,
            arm="intervention",
            electrochemical_workflow_mode=workflow_mode,
        )
        if row.get("reference_plan_sha256") != canonical_sha256(
            reference_plan.to_dict()
        ):
            mismatches.append(f"{query.query_id}:reference_plan_sha256")
        if row.get("intervention_plan_sha256") != canonical_sha256(
            intervention_plan.to_dict()
        ):
            mismatches.append(f"{query.query_id}:intervention_plan_sha256")
        pairs = row.get("paired_replicates")
        if not isinstance(pairs, list) or len(pairs) != (
            PREDICTIVE_PAIRED_REPLICATE_COUNT
        ):
            raise ValueError("predictive receipt paired replicate count mismatch")
        normalized_pairs: list[dict[str, Any]] = []
        for replicate_index, pair in enumerate(pairs):
            if int(pair["replicate_index"]) != replicate_index:
                mismatches.append(f"{query.query_id}:replicate_index")
            reference = pair["reference"]
            intervention = pair["intervention"]
            expected_seed = predictive_observation_seed(
                task_id,
                world_seed,
                query.query_id,
                replicate_index,
            )
            expected_namespace = (
                f"{protocol['observation_noise_namespace']}-{task_id}-predictive-"
                f"{query.query_id}-{replicate_index:03d}"
            )
            for arm_name, arm in (
                ("reference", reference),
                ("intervention", intervention),
            ):
                if int(arm["observation_seed"]) != expected_seed:
                    mismatches.append(
                        f"{query.query_id}:{replicate_index}:{arm_name}:observation_seed"
                    )
                if arm["observation_noise_namespace"] != expected_namespace:
                    mismatches.append(
                        f"{query.query_id}:{replicate_index}:{arm_name}:noise_namespace"
                    )
            if reference["observation_seed"] != intervention["observation_seed"]:
                mismatches.append(f"{query.query_id}:{replicate_index}:paired_seed")
            if reference["observation_noise_namespace"] != intervention[
                "observation_noise_namespace"
            ]:
                mismatches.append(f"{query.query_id}:{replicate_index}:paired_namespace")
            pair_offset = (
                horizon
                + query_index * PREDICTIVE_PAIRED_REPLICATE_COUNT * 2
                + replicate_index * 2
            )
            replayed_results: dict[str, dict[str, Any]] = {}
            for arm_name, arm, expected_plan, experiment_index in (
                ("reference", reference, reference_plan, pair_offset),
                (
                    "intervention",
                    intervention,
                    intervention_plan,
                    pair_offset + 1,
                ),
            ):
                recorded_result = arm["result"]
                if recorded_result["plan"] != expected_plan.to_dict():
                    mismatches.append(
                        f"{query.query_id}:{replicate_index}:{arm_name}:plan"
                    )
                if int(recorded_result["experiment_index"]) != experiment_index:
                    mismatches.append(
                        f"{query.query_id}:{replicate_index}:{arm_name}:experiment_index"
                    )
                with StaticOptimizationExperimentSession(
                    task_id=task_id,
                    seed=world_seed,
                    experiment_horizon=1,
                    experiment_index_offset=experiment_index,
                    observation_seed=int(arm["observation_seed"]),
                    observation_noise_namespace=str(
                        arm["observation_noise_namespace"]
                    ),
                    electrochemical_workflow_mode=workflow_mode,
                ) as session:
                    replayed = session.execute(expected_plan).to_dict()
                replayed_count += 1
                replayed_results[arm_name] = replayed
                if replayed != recorded_result:
                    mismatches.append(
                        f"{query.query_id}:{replicate_index}:{arm_name}:result"
                    )
            normalized_pairs.append(
                {
                    "reference": replayed_results["reference"],
                    "intervention": replayed_results["intervention"],
                }
            )
        metric_results: list[dict[str, Any]] = []
        for metric_id in query.metric_ids:
            reference_mean = statistics.fmean(
                metric_value_from_result(item["reference"], metric_id)
                for item in normalized_pairs
            )
            intervention_mean = statistics.fmean(
                metric_value_from_result(item["intervention"], metric_id)
                for item in normalized_pairs
            )
            delta = intervention_mean - reference_mean
            threshold = query.direction_thresholds[metric_id]
            metric_results.append(
                {
                    "metric_id": metric_id,
                    "reference_mean": reference_mean,
                    "intervention_mean": intervention_mean,
                    "delta": delta,
                    "direction_threshold": threshold,
                    "metric_source": query.metric_sources[metric_id],
                    "actual_direction": classify_metric_direction(delta, threshold),
                }
            )
        if row.get("metric_results") != metric_results:
            mismatches.append(f"{query.query_id}:metric_results")
        recomputed_query_results.append(
            {
                "query_id": query.query_id,
                "query_sha256": query.query_sha256,
                "metric_results": metric_results,
            }
        )
    recomputed_score = score_predictive_validation(
        predictions,
        recomputed_query_results,
        queries=queries,
    )
    if recorded.get("score") != recomputed_score:
        mismatches.append("score")
    return {
        "cell_id": cell_id,
        "present": True,
        "enabled": True,
        "replayed_experiment_count": replayed_count,
        "verified": not mismatches,
        "mismatches": mismatches,
        "score": recomputed_score,
    }


def audit_world_understanding_receipts(
    receipts: list[Mapping[str, Any]], protocol: Mapping[str, Any]
) -> dict[str, Any]:
    """Score declared claims when a frozen hidden reference is configured."""

    contract = protocol.get("world_understanding")
    if not isinstance(contract, Mapping) or not contract.get("enabled"):
        return {"enabled": False, "scored_cell_count": 0, "cells": []}
    reference_path = Path(str(contract["reference_path"]))
    if not reference_path.is_absolute():
        reference_path = Path(__file__).resolve().parents[3] / reference_path
    reference_payload = json.loads(reference_path.read_text(encoding="utf-8"))
    vocabulary = reference_payload["public_vocabulary"]
    references = tuple(
        ReferenceWorldClaim.from_dict(item)
        for item in reference_payload["reference_claims"]
    )
    rows: list[dict[str, Any]] = []
    scored: list[dict[str, Any]] = []
    for receipt in receipts:
        final = receipt.get("final_synthesis")
        recommendation = final.get("recommendation") if isinstance(final, Mapping) else None
        explanation = (
            recommendation.get("working_explanation")
            if isinstance(recommendation, Mapping)
            else None
        )
        claims_payload = (
            explanation.get("structured_claims")
            if isinstance(explanation, Mapping)
            else None
        )
        base = {
            "cell_id": str(receipt["cell"]["cell_id"]),
            "task_id": str(receipt["cell"]["task_id"]),
            "method_id": str(receipt["method_id"]),
        }
        if not isinstance(claims_payload, list):
            rows.append(
                {
                    **base,
                    "status": "not_scored_missing_structured_claims",
                    "score": None,
                }
            )
            continue
        claims = parse_world_understanding_claims(
            claims_payload,
            evidence_catalog=[
                str(entry["evidence_id"])
                for experiment in receipt["experiments"]
                for entry in experiment["result"]["measurement_evidence"]
            ],
            allowed_cause_variables=vocabulary["cause_variables"],
            allowed_effect_variables=vocabulary["effect_variables"],
            allowed_mechanism_tags=vocabulary["mechanism_tags"],
        )
        score = score_world_understanding(claims, references).to_dict()
        scored.append(score)
        rows.append({**base, "status": "scored", "score": score})
    metric_names = tuple(scored[0]) if scored else ()
    return {
        "enabled": True,
        "reference_id": reference_payload["reference_id"],
        "reference_sha256": canonical_sha256(reference_payload),
        "layer": "declared_secondary_diagnostic",
        "predictive_score_enabled": bool(contract.get("predictive_score_enabled", False)),
        "scored_cell_count": len(scored),
        "mean_scores": {
            metric: statistics.fmean(float(item[metric]) for item in scored)
            for metric in metric_names
            if metric not in {"predicted_claim_count", "reference_claim_count"}
        },
        "cells": rows,
    }


def _predictive_results(receipt: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    predictive = receipt.get("predictive_validation")
    if not isinstance(predictive, Mapping):
        return []
    return [
        arm["result"]
        for query in predictive.get("queries", [])
        for pair in query.get("paired_replicates", [])
        for arm in (pair["reference"], pair["intervention"])
    ]


def audit_static_optimization_run(
    *,
    protocol: Mapping[str, Any],
    run_root: str | Path,
) -> dict[str, Any]:
    validate_static_optimization_protocol(protocol)
    root = Path(run_root)
    report = json.loads((root / "report.json").read_text(encoding="utf-8"))
    formal_result = bool(protocol.get("formal_result", False)) and bool(
        report.get("formal_result", False)
    )
    benchmark_claim_allowed = bool(
        protocol.get("benchmark_claim_allowed", False)
    ) and bool(report.get("benchmark_claim_allowed", False))
    receipt_paths = sorted((root / "receipts").glob("*.json"))
    receipts = [json.loads(path.read_text(encoding="utf-8")) for path in receipt_paths]
    protocol_hash = canonical_sha256(protocol)
    if any(item["protocol_sha256"] != protocol_hash for item in receipts):
        raise ValueError("S0 receipt protocol hash mismatch")
    replay = [replay_static_optimization_receipt(item, protocol) for item in receipts]
    validation_replay = [
        replay_static_optimization_validation(item) for item in receipts
    ]
    predictive_replay = [
        replay_static_optimization_predictive(item, protocol) for item in receipts
    ]
    scores = [
        [float(value) for value in item["scores"]]
        for item in receipts
        if item["scores"]
    ]
    cell_descriptives = []
    for item in receipts:
        values = [float(value) for value in item["scores"]]
        cell_descriptives.append(
            {
                "cell_id": item["cell"]["cell_id"],
                "method_id": item["method_id"],
                "task_id": item["cell"]["task_id"],
                "cell_status": item["cell_status"],
                "completed_experiment_count": item["completed_experiment_count"],
                "first_score": values[0] if values else None,
                "last_score": values[-1] if values else None,
                "best_score": max(values) if values else None,
                "last_minus_first_score": values[-1] - values[0] if values else None,
                "validated_recommendation_score_mean": (
                    item["validation"][
                        "primary_validated_recommendation_score_mean"
                    ]
                    if item.get("validation") is not None
                    else None
                ),
                "validated_incumbent_score_mean": (
                    item["validation"]["validated_incumbent_score_mean"]
                    if item.get("validation") is not None
                    else None
                ),
                "recommendation_gain_over_incumbent_mean": (
                    item["validation"][
                        "recommendation_gain_over_incumbent_mean"
                    ]
                    if item.get("validation") is not None
                    else None
                ),
                "predictive_directional_accuracy": (
                    item["predictive_validation"]["score"]["directional_accuracy"]
                    if item.get("predictive_validation") is not None
                    else None
                ),
                "predictive_confidence_brier_score": (
                    item["predictive_validation"]["score"][
                        "confidence_brier_score"
                    ]
                    if item.get("predictive_validation") is not None
                    else None
                ),
            }
        )
    integrated_receipts = [
        item for item in receipts if item.get("recommendation_stage_present") is True
    ]
    validated_recommendation_scores = [
        float(
            item["validation"]["primary_validated_recommendation_score_mean"]
        )
        for item in integrated_receipts
        if item.get("validation") is not None
    ]
    validated_incumbent_scores = [
        float(item["validation"]["validated_incumbent_score_mean"])
        for item in integrated_receipts
        if item.get("validation") is not None
    ]
    world_understanding = audit_world_understanding_receipts(receipts, protocol)
    predictive_scores = [
        item["predictive_validation"]["score"]
        for item in receipts
        if item.get("predictive_validation") is not None
    ]
    predictive_world_understanding = {
        "enabled": bool(
            protocol.get("world_understanding", {}).get(
                "predictive_score_enabled", False
            )
        ),
        "layer": "held_out_predictive_secondary_diagnostic",
        "scored_cell_count": len(predictive_scores),
        "mean_directional_accuracy": (
            statistics.fmean(
                float(item["directional_accuracy"]) for item in predictive_scores
            )
            if predictive_scores
            else None
        ),
        "mean_confidence_brier_score": (
            statistics.fmean(
                float(item["confidence_brier_score"])
                for item in predictive_scores
            )
            if predictive_scores
            else None
        ),
        "mean_nontrivial_actual_effect_rate": (
            statistics.fmean(
                float(item["nontrivial_actual_effect_rate"])
                for item in predictive_scores
            )
            if predictive_scores
            else None
        ),
        "cells": [
            {
                "cell_id": replay_item["cell_id"],
                "verified": replay_item["verified"],
                "score": replay_item.get("score"),
                "mismatches": replay_item["mismatches"],
            }
            for replay_item in predictive_replay
        ],
    }
    return {
        "schema_version": STATIC_OPTIMIZATION_POSTRUN_VERSION,
        "formal_result": formal_result,
        "benchmark_claim_allowed": benchmark_claim_allowed,
        "protocol_id": protocol["protocol_id"],
        "protocol_sha256": protocol_hash,
        "static_world_verified": all(
            item["world_policy"]["mode"] == "static_for_entire_campaign"
            and item["world_policy"]["interventions"] == []
            and item["agent_manifest"]["static_world"]
            and not item["agent_manifest"]["hidden_world_fields_supplied"]
            for item in receipts
        ),
        "no_mechanism_fields_in_plans": all(
            set(experiment["result"]["plan"]).issubset(
                {
                "experiment_intent",
                "search_vector",
                "recipe_parameters",
                "requested_measurement_slots",
                "measurement_objective",
                "expected_effect",
                "uncertainty",
                }
            )
            and "search_vector" in experiment["result"]["plan"]
            for item in receipts
            for experiment in item["experiments"]
        ),
        "known_horizon_visible": all(
            item["agent_manifest"].get("horizon_visible") is True
            and int(item["agent_manifest"].get("experiment_horizon", 0))
            == exploration_experiment_count(protocol)
            for item in integrated_receipts
        )
        if integrated_receipts
        else False,
        "final_synthesis_present": all(
            item.get("final_synthesis") is not None for item in integrated_receipts
        )
        if integrated_receipts
        else False,
        "final_recommendation_validation_matches": all(
            item["validation"]["recommendation"]["plan"]["search_vector"]
            == item["final_synthesis"]["recommendation"][
                "recommended_search_vector"
            ]
            and item["validation"]["recommendation"]["plan"][
                "requested_measurement_slots"
            ]
            == item["final_synthesis"]["recommendation"][
                "recommended_measurement_slots"
            ]
            for item in integrated_receipts
            if item.get("validation") is not None
        )
        if integrated_receipts
        else False,
        "atomic_executor_verified": all(
            result["operation_count"] == result["compiled_operation_count"]
            and result["runtime_margin_used"] is False
            for item in receipts
            for result in (
                [experiment["result"] for experiment in item["experiments"]]
                + [
                    replicate["result"]
                    for target in ("incumbent", "recommendation")
                    for replicate in (
                        (item.get("validation") or {}).get(target, {}).get(
                            "replicates", []
                        )
                    )
                ]
                + _predictive_results(item)
            )
            if "compiled_operation_count" in result
        ),
        "report_receipt_hashes_match": all(
            report["receipt_sha256"].get(
                f"{item['method_id']}:{item['cell']['task_id']}"
            )
            == canonical_sha256(item)
            for item in receipts
        ),
        "report_predictive_counts_match": (
            int(report.get("planned_predictive_validation_experiment_count", -1))
            == sum(
                int(item["planned_predictive_validation_experiment_count"])
                for item in receipts
            )
            and int(
                report.get("completed_predictive_validation_experiment_count", -1)
            )
            == sum(
                int(item["completed_predictive_validation_experiment_count"])
                for item in receipts
            )
        ),
        "report_total_physical_experiment_count_matches": int(
            report.get("total_physical_experiment_count", -1)
        )
        == sum(int(item["total_physical_experiment_count"]) for item in receipts),
        "replay": {
            "receipt_count": len(replay),
            "replayed_experiment_count": sum(
                item["replayed_experiment_count"] for item in replay
            ),
            "verified_receipt_count": sum(item["verified"] for item in replay),
            "replayed_validation_experiment_count": sum(
                item["replayed_experiment_count"] for item in validation_replay
            ),
            "verified_validation_receipt_count": sum(
                item["verified"] for item in validation_replay
            ),
            "replayed_predictive_experiment_count": sum(
                item["replayed_experiment_count"] for item in predictive_replay
            ),
            "verified_predictive_receipt_count": sum(
                item["verified"] for item in predictive_replay
            ),
            "all_exploration_verified": all(item["verified"] for item in replay),
            "all_validation_verified": all(
                item["verified"] for item in validation_replay
            ),
            "all_predictive_verified": all(
                item["verified"] for item in predictive_replay
            ),
            "all_verified": all(item["verified"] for item in replay)
            and all(item["verified"] for item in validation_replay)
            and all(item["verified"] for item in predictive_replay),
            "receipts": replay,
            "validation_receipts": validation_replay,
            "predictive_receipts": predictive_replay,
        },
        "descriptive_scores": {
            "cell_count": len(scores),
            "mean_first_score": (
                statistics.fmean(values[0] for values in scores) if scores else None
            ),
            "mean_last_score": (
                statistics.fmean(values[-1] for values in scores) if scores else None
            ),
            "mean_best_score": (
                statistics.fmean(max(values) for values in scores) if scores else None
            ),
            "mean_validated_recommendation_score": (
                statistics.fmean(validated_recommendation_scores)
                if validated_recommendation_scores
                else None
            ),
            "mean_validated_incumbent_score": (
                statistics.fmean(validated_incumbent_scores)
                if validated_incumbent_scores
                else None
            ),
            "cell_descriptives": cell_descriptives,
            "formal_optimization_estimand": formal_result,
        },
        "world_understanding": world_understanding,
        "predictive_world_understanding": predictive_world_understanding,
        "source_report": {
            "run_root": str(root),
            "report_sha256": hashlib.sha256((root / "report.json").read_bytes()).hexdigest(),
            "audit_source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        },
        "interpretation": (
            "Formal S0 fixed-world optimization replay audit. Blind validation of the "
            "terminal recommendation is the primary endpoint; exploration curves and "
            "working explanations remain secondary diagnostics. The result characterizes "
            "the frozen sampled worlds and does not establish broad generalization."
            if formal_result
            else (
                "Development S0 fixed-world optimization replay audit. Integrated runs "
                "use blind validation of a terminal recommendation as the primary "
                "endpoint; exploration curves and working explanations remain secondary "
                "diagnostics."
            )
        ),
    }


__all__ = [
    "STATIC_OPTIMIZATION_POSTRUN_VERSION",
    "audit_static_optimization_run",
    "audit_world_understanding_receipts",
    "replay_static_optimization_predictive",
    "replay_static_optimization_receipt",
    "replay_static_optimization_validation",
]
