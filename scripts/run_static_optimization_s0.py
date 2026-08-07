"""Run an explicitly selected fixed-world S0 optimization protocol."""

from __future__ import annotations

import argparse
import copy
import json
import statistics
from collections.abc import Mapping
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, cast

from chemworld.agents.electrochemical_single_stage import (
    electrochemical_single_stage_unit_vector_from_parameters,
)
from chemworld.agents.prompt_context import PromptBudgetExceededError
from chemworld.agents.static_optimization import StaticOptimizationPlan
from chemworld.agents.task_recipes import (
    electrochemical_recipe_unit_vector_from_parameters,
)
from chemworld.eval import crystallization_predictive
from chemworld.eval.electrochemical_predictive import (
    PREDICTIVE_DIRECTION_THRESHOLD,
    PREDICTIVE_METRIC_SOURCES,
    PREDICTIVE_PAIRED_REPLICATE_COUNT,
    PREDICTIVE_PHYSICAL_EXPERIMENT_COUNT,
    PREDICTIVE_QUERY_COUNT,
    build_electrochemical_prediction_queries,
    build_standardized_electrochemical_prediction_queries,
    classify_metric_direction,
    metric_value_from_result,
    parse_counterfactual_predictions,
    predictive_measurement_slots,
    predictive_query_metrics,
    score_predictive_validation,
)
from chemworld.eval.provenance import (
    canonical_json_sha256 as canonical_sha256,
)
from chemworld.eval.provenance import (
    git_source_commit,
    git_worktree_dirty,
    write_json_atomic,
)
from chemworld.eval.static_optimization_execution import (
    StaticOptimizationExperimentSession,
    build_static_optimization_agent,
    static_optimization_workflow_mode,
)
from chemworld.eval.static_optimization_protocol import (
    PREDICTIVE_CALL_INTEGRATED,
    PREDICTIVE_CALL_SEPARATE,
    PREDICTIVE_QUERY_HISTORY_LOCAL,
    PREDICTIVE_QUERY_STANDARDIZED,
    exploration_experiment_count,
    static_optimization_crystallization_material_family_id,
    static_optimization_material_family_id,
    static_optimization_predictive_call_policy,
    static_optimization_predictive_query_policy,
    static_optimization_scoring_contract_id,
    validate_static_optimization_protocol,
)
from chemworld.eval.static_optimization_seeds import (
    exploration_observation_seed,
    predictive_observation_seed,
    validation_observation_seed,
)
from chemworld.physchem.electrochemical_task_contract import (
    ELECTROCHEMICAL_WORKFLOW_STATIC_SINGLE_STAGE,
)
from chemworld.providers.codex_subscription import CodexSubscriptionClient
from chemworld.providers.deepseek import DeepSeekAPIError, DeepSeekClient, JsonCompletion
from chemworld.providers.wellau import ReasoningEffort, WellAUClient

ROOT = Path(__file__).resolve().parents[1]
DEVELOPMENT_TEST_PROTOCOL = ROOT / "configs/benchmark/scientific_optimization_s0_v0.1_dev.json"
DEVELOPMENT_TEST_METHODS = (
    ROOT / "configs/methods/llm_v0.4/participant_methods_s0_static_development.json"
)
REPORT_SCHEMA_VERSION = "chemworld-static-scientific-optimization-report-0.1-s0-dev"
INTEGRATED_REPORT_SCHEMA_VERSION = "chemworld-static-scientific-optimization-report-0.3-s0-dev"
PROGRESS_SCHEMA_VERSION = "chemworld-static-scientific-optimization-progress-0.1"


def _record_progress(
    progress_file: Path | None,
    *,
    event: str,
    **payload: Any,
) -> None:
    if progress_file is None:
        return
    record = {
        "schema_version": PROGRESS_SCHEMA_VERSION,
        "updated_at_utc": datetime.now(UTC).isoformat(),
        "event": event,
        **payload,
    }
    write_json_atomic(progress_file, record)
    print(json.dumps(record, ensure_ascii=False, sort_keys=True), flush=True)


class _DeterministicStaticMockClient:
    model = "static-optimization-mock"
    thinking = False
    reasoning_effort = None

    def __init__(self) -> None:
        self.call_count = 0

    def complete_json(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int = 4096,
    ) -> JsonCompletion:
        del system_prompt, max_tokens
        prompt = json.loads(user_prompt)
        if "public_predictive_context" in prompt:
            predictive_context = prompt["public_predictive_context"]
            queries = predictive_context["held_out_prediction_queries"]
            self.call_count += 1
            return JsonCompletion(
                payload={
                    "schema_version": prompt["schema_version"],
                    "counterfactual_predictions": [
                        {
                            "query_id": str(query["query_id"]),
                            "metric_predictions": [
                                {
                                    "metric_id": str(metric_id),
                                    "direction": "no_material_change",
                                    "confidence": 0.5,
                                }
                                for metric_id in query["metric_ids"]
                            ],
                        }
                        for query in queries
                    ],
                },
                model=self.model,
                usage={
                    "prompt_tokens": 110,
                    "completion_tokens": 70,
                    "total_tokens": 180,
                },
                attempts=1,
            )
        if "public_final_synthesis_context" in prompt:
            context = prompt["public_final_synthesis_context"]
            history = context["experiment_history"]
            if not history:
                raise ValueError("mock final synthesis requires experiment history")
            best = max(
                history,
                key=lambda item: float(item["terminal_summary"].get("leaderboard_score", 0.0)),
            )
            evidence = list(context["evidence_catalog"])
            self.call_count += 1
            named_controls = (
                context["experiment_interface"].get("parameterization") == "named_physical_controls"
            )
            recommendation = (
                {"recommended_recipe_parameters": dict(best["plan"]["recipe_parameters"])}
                if named_controls
                else {"recommended_search_vector": list(best["plan"]["search_vector"])}
            )
            working_explanation = {
                "empirical_relationships": [
                    "the selected tested region produced the strongest public score"
                ],
                "mechanistic_hypothesis": (
                    "the selected process conditions jointly favor the task objective"
                ),
                "supporting_evidence_ids": evidence[:3],
                "contradicting_evidence_ids": [],
                "uncertainty": 0.38,
            }
            if named_controls:
                parameter_schema = context["experiment_interface"]["recipe_parameter_schema"]
                if "reaction_temperature_K" in parameter_schema:
                    working_explanation["structured_claims"] = [
                        {
                            "claim_id": "mock-cooling-yield",
                            "cause_variables": ["crystallization_temperature_K"],
                            "effect_variable": "crystal_yield",
                            "relation": "negative",
                            "mechanism_tags": ["vanthoff_solubility", "supersaturation"],
                            "scope": "within the declared cooling range",
                            "evidence_ids": evidence[:2],
                            "confidence": 0.6,
                        }
                    ]
                else:
                    potential_variable = (
                        "potential_V"
                        if "potential_V" in parameter_schema
                        else "controlled_potential_V"
                    )
                    working_explanation["structured_claims"] = [
                        {
                            "claim_id": "mock-potential-selective-product-yield",
                            "cause_variables": [potential_variable],
                            "effect_variable": "selective_product_yield",
                            "relation": "nonmonotonic",
                            "mechanism_tags": [
                                "nernst_equilibrium",
                                "butler_volmer_kinetics",
                            ],
                            "scope": "within the declared S0 potential range",
                            "evidence_ids": evidence[:2],
                            "confidence": 0.6,
                        }
                    ]
            held_out_queries = context.get("held_out_prediction_queries", [])
            counterfactual_predictions = (
                {
                    "counterfactual_predictions": [
                        {
                            "query_id": str(query["query_id"]),
                            "metric_predictions": [
                                {
                                    "metric_id": str(metric_id),
                                    "direction": "no_material_change",
                                    "confidence": 0.5,
                                }
                                for metric_id in query["metric_ids"]
                            ],
                        }
                        for query in held_out_queries
                    ]
                }
                if held_out_queries
                else {}
            )
            return JsonCompletion(
                payload={
                    "schema_version": prompt["schema_version"],
                    **recommendation,
                    "recommended_measurement_slots": list(
                        best["plan"]["requested_measurement_slots"]
                    ),
                    "recommendation_type": "tested",
                    "source_experiment_indices": [int(best["experiment_index"])],
                    "predicted_score": float(
                        best["terminal_summary"].get("leaderboard_score", 0.0)
                    ),
                    "confidence": 0.72,
                    "method_summary": (
                        "submit the best tested fixed-world method from the campaign"
                    ),
                    "evidence_refs": evidence[:4],
                    "working_explanation": working_explanation,
                    "remaining_risks": ["independent assay variation"],
                    "recommended_followup": (
                        "repeat the submitted method under independent observation noise"
                    ),
                    **counterfactual_predictions,
                },
                model=self.model,
                usage={"prompt_tokens": 120, "completion_tokens": 90, "total_tokens": 210},
                attempts=1,
            )
        context = prompt["public_experiment_context"]
        history = context["experiment_history"]
        named_controls = (
            context["experiment_interface"].get("parameterization") == "named_physical_controls"
        )
        campaign_scaffold = context.get("campaign_scaffold", {})
        candidate_portfolio = campaign_scaffold.get("model_candidate_portfolio", [])
        selected_candidate = (
            candidate_portfolio[0]
            if isinstance(candidate_portfolio, list) and candidate_portfolio
            else None
        )
        if isinstance(selected_candidate, dict):
            recipe_selection = (
                {
                    "candidate_id": str(selected_candidate["candidate_id"]),
                    "recipe_parameters": dict(
                        selected_candidate["recipe_parameters"]
                    ),
                }
                if named_controls
                else {
                    "candidate_id": str(selected_candidate["candidate_id"]),
                    "search_vector": list(selected_candidate["search_vector"]),
                }
            )
        elif named_controls:
            parameter_schema = context["experiment_interface"]["recipe_parameter_schema"]
            recipe_parameters = (
                {
                    "reaction_temperature_K": 378.15,
                    "reaction_duration_s": 3000.0,
                    "reagent_amount_mol": 0.012,
                    "stirring_speed_rpm": 700.0,
                    "catalyst": len(history) % 4,
                    "catalyst_amount_mol": 0.00030,
                    "solvent": (len(history) // 2) % 4,
                    "seed_mass_g": 0.006,
                    "crystallization_temperature_K": 278.15,
                    "crystallization_duration_s": 3600.0,
                }
                if "reaction_temperature_K" in parameter_schema
                else {
                    "electrolyte_profile": len(history) % 4,
                    "solvent": (len(history) // 2) % 4,
                    "reagent_amount_mol": 0.010,
                    "potential_V": 1.10,
                    "current_mA": 65.0,
                    "duration_s": 1500.0,
                }
                if "potential_V" in parameter_schema
                else {
                    "electrolyte_profile": len(history) % 4,
                    "solvent": (len(history) // 2) % 4,
                    "reagent_amount_mol": 0.010,
                    "probe_potential_V": 0.90,
                    "probe_current_mA": 45.0,
                    "probe_duration_s": 420.0,
                    "controlled_potential_V": 1.10,
                    "controlled_current_mA": 65.0,
                    "controlled_duration_s": 1500.0,
                }
            )
            recipe_selection = {"recipe_parameters": recipe_parameters}
        else:
            dimension = int(context["experiment_interface"]["search_vector_dimension"])
            vector = [0.5] * dimension
            if history:
                coordinate = (len(history) - 1) % dimension
                vector[coordinate] = 0.2 if len(history) % 2 else 0.8
            recipe_selection = {"search_vector": vector}
        self.call_count += 1
        payload = {
            **recipe_selection,
            "experiment_intent": (
                "establish a fixed-world reference"
                if not history
                else "probe one recipe coordinate"
            ),
            "requested_measurement_slots": [
                item["slot_id"]
                for item in context["experiment_interface"]["diagnostic_measurement_slots"]
            ],
            "measurement_objective": (
                "compare public yield, purity, selectivity, and safety signals"
            ),
            "expected_effect": (
                "the selected condition will improve or clarify the fixed task objective"
            ),
            "uncertainty": 0.7 if not history else max(0.2, 0.7 - 0.05 * len(history)),
        }
        return JsonCompletion(
            payload=payload,
            model=self.model,
            usage={"prompt_tokens": 100, "completion_tokens": 60, "total_tokens": 160},
            attempts=1,
        )

    def pricing_snapshot(self) -> dict[str, Any]:
        return {
            "provider": "mock",
            "model_id": self.model,
            "accounting_complete": True,
            "input_per_million_usd": 0.0,
            "output_per_million_usd": 0.0,
        }

    def estimate_cost_usd(self, usage: dict[str, int]) -> float:
        del usage
        return 0.0


def _exploration_horizon(protocol: Mapping[str, Any]) -> int:
    return exploration_experiment_count(protocol)


def _plan_from_payload(payload: Mapping[str, Any]) -> StaticOptimizationPlan:
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


def _score_summary(values: list[float]) -> dict[str, Any]:
    return {
        "replicate_count": len(values),
        "mean": statistics.fmean(values) if values else None,
        "median": statistics.median(values) if values else None,
        "sample_standard_deviation": (statistics.stdev(values) if len(values) > 1 else None),
        "minimum": min(values) if values else None,
        "maximum": max(values) if values else None,
    }


def _execute_validation_target(
    *,
    protocol: Mapping[str, Any],
    task_id: str,
    world_seed: int,
    target: str,
    plan: StaticOptimizationPlan,
    replicate_count: int,
    experiment_index_offset: int,
) -> dict[str, Any]:
    if replicate_count <= 0:
        raise ValueError("validation replicate count must be positive")
    replicates: list[dict[str, Any]] = []
    for replicate_index in range(replicate_count):
        observation_seed = validation_observation_seed(
            task_id,
            world_seed,
            "paired-replicate",
            replicate_index,
        )
        validation_key = "paired-replicate"
        namespace = (
            f"{protocol['observation_noise_namespace']}-{task_id}-validation-"
            f"{validation_key}-{replicate_index:03d}"
        )
        experiment_index = experiment_index_offset + replicate_index
        with StaticOptimizationExperimentSession(
            task_id=task_id,
            seed=world_seed,
            experiment_horizon=1,
            experiment_index_offset=experiment_index,
            observation_seed=observation_seed,
            observation_noise_namespace=namespace,
            electrochemical_workflow_mode=static_optimization_workflow_mode(protocol),
            electrochemical_material_family_id=(static_optimization_material_family_id(protocol)),
            crystallization_material_family_id=(
                static_optimization_crystallization_material_family_id(protocol)
            ),
            scoring_contract_id=static_optimization_scoring_contract_id(protocol),
        ) as session:
            result = session.execute(plan)
        replicates.append(
            {
                "replicate_index": replicate_index,
                "observation_seed": observation_seed,
                "observation_noise_namespace": namespace,
                "result": result.to_dict(),
            }
        )
    scores = [float(item["result"]["terminal_summary"]["leaderboard_score"]) for item in replicates]
    return {
        "target": target,
        "plan": plan.to_dict(),
        "plan_sha256": canonical_sha256(plan.to_dict()),
        "score_summary": _score_summary(scores),
        "scores": scores,
        "replicates": replicates,
    }


def _predictive_contract(protocol: Mapping[str, Any]) -> Mapping[str, Any] | None:
    world_understanding = protocol.get("world_understanding")
    if not isinstance(world_understanding, Mapping) or not bool(
        world_understanding.get("predictive_score_enabled", False)
    ):
        return None
    contract = world_understanding.get("predictive_validation")
    if not isinstance(contract, Mapping):
        raise ValueError("predictive world understanding lacks a frozen validation contract")
    task_id = str(protocol["tasks"][0])
    workflow_mode = static_optimization_workflow_mode(protocol)
    crystallization = task_id == "reaction-to-crystallization"
    query_metrics = (
        crystallization_predictive.PREDICTIVE_QUERY_METRICS
        if crystallization
        else predictive_query_metrics(workflow_mode)
    )
    metric_sources = (
        crystallization_predictive.PREDICTIVE_METRIC_SOURCES
        if crystallization
        else PREDICTIVE_METRIC_SOURCES
    )
    measurement_slots = (
        crystallization_predictive.PREDICTIVE_MEASUREMENT_SLOTS
        if crystallization
        else predictive_measurement_slots(workflow_mode)
    )
    expected = {
        "query_count": PREDICTIVE_QUERY_COUNT,
        "paired_replicates_per_query": PREDICTIVE_PAIRED_REPLICATE_COUNT,
        "simulations_per_pair": 2,
        "total_physical_experiments_per_seed": PREDICTIVE_PHYSICAL_EXPERIMENT_COUNT,
        "intervention_variables": list(query_metrics),
        "metric_ids_by_intervention": {key: list(value) for key, value in query_metrics.items()},
        "metric_source_by_metric": dict(metric_sources),
        "direction_labels": [
            "increase",
            "decrease",
            "no_material_change",
        ],
        "direction_threshold": PREDICTIVE_DIRECTION_THRESHOLD,
        "standardized_measurement_slots": list(measurement_slots),
        "paired_observation_seed": True,
        "paired_observation_noise_namespace": True,
        "feedback_returned_to_agent": False,
    }
    call_policy = static_optimization_predictive_call_policy(protocol)
    query_policy = static_optimization_predictive_query_policy(protocol)
    if call_policy == PREDICTIVE_CALL_INTEGRATED:
        expected["additional_model_calls"] = 0
        if "reference_selection_policy" in contract:
            expected["reference_selection_policy"] = PREDICTIVE_QUERY_HISTORY_LOCAL
        if "call_policy" in contract:
            expected["call_policy"] = PREDICTIVE_CALL_INTEGRATED
    elif call_policy == PREDICTIVE_CALL_SEPARATE:
        expected.update(
            {
                "reference_selection_policy": PREDICTIVE_QUERY_STANDARDIZED,
                "call_policy": PREDICTIVE_CALL_SEPARATE,
                "recommendation_committed_before_query_visibility": True,
                "prediction_call_can_modify_recommendation": False,
                "additional_model_calls": 1,
            }
        )
    else:
        raise ValueError("predictive validation call policy is disabled unexpectedly")
    if expected.get("reference_selection_policy", query_policy) != query_policy:
        raise ValueError("predictive validation query policy changed")
    if dict(contract) != expected:
        raise ValueError("predictive validation protocol does not match the frozen contract")
    return contract


def _build_prediction_queries(
    *,
    protocol: Mapping[str, Any],
    task_id: str,
    history: list[dict[str, Any]],
) -> tuple[Any, ...]:
    query_policy = static_optimization_predictive_query_policy(protocol)
    workflow_mode = static_optimization_workflow_mode(protocol)
    if query_policy == PREDICTIVE_QUERY_STANDARDIZED:
        if task_id != "electrochemical-conversion":
            raise ValueError("standardized predictive anchor is electrochemical-only")
        return build_standardized_electrochemical_prediction_queries()
    if query_policy != PREDICTIVE_QUERY_HISTORY_LOCAL:
        raise ValueError("unsupported predictive query policy")
    if task_id == "reaction-to-crystallization":
        return crystallization_predictive.build_crystallization_prediction_queries(history)
    return build_electrochemical_prediction_queries(
        history,
        electrochemical_workflow_mode=workflow_mode,
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
            if electrochemical_workflow_mode == ELECTROCHEMICAL_WORKFLOW_STATIC_SINGLE_STAGE
            else electrochemical_recipe_unit_vector_from_parameters(dict(recipe_parameters))
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


def _execute_predictive_validation(
    *,
    protocol: Mapping[str, Any],
    task_id: str,
    world_seed: int,
    history: list[dict[str, Any]],
    predictions_payload: object,
    experiment_index_offset: int,
    model_call_count_before_execution: int,
) -> dict[str, Any]:
    _predictive_contract(protocol)
    workflow_mode = static_optimization_workflow_mode(protocol)
    queries = _build_prediction_queries(
        protocol=protocol,
        task_id=task_id,
        history=history,
    )
    predictions = parse_counterfactual_predictions(
        predictions_payload,
        queries=queries,
    )
    query_results: list[dict[str, Any]] = []
    for query_index, query in enumerate(queries):
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
        paired_replicates: list[dict[str, Any]] = []
        for replicate_index in range(PREDICTIVE_PAIRED_REPLICATE_COUNT):
            observation_seed = predictive_observation_seed(
                task_id,
                world_seed,
                query.query_id,
                replicate_index,
            )
            namespace = (
                f"{protocol['observation_noise_namespace']}-{task_id}-predictive-"
                f"{query.query_id}-{replicate_index:03d}"
            )
            pair_offset = (
                experiment_index_offset
                + query_index * PREDICTIVE_PAIRED_REPLICATE_COUNT * 2
                + replicate_index * 2
            )
            with StaticOptimizationExperimentSession(
                task_id=task_id,
                seed=world_seed,
                experiment_horizon=1,
                experiment_index_offset=pair_offset,
                observation_seed=observation_seed,
                observation_noise_namespace=namespace,
                electrochemical_workflow_mode=workflow_mode,
                electrochemical_material_family_id=(
                    static_optimization_material_family_id(protocol)
                ),
                crystallization_material_family_id=(
                    static_optimization_crystallization_material_family_id(protocol)
                ),
                scoring_contract_id=static_optimization_scoring_contract_id(protocol),
            ) as session:
                reference_result = session.execute(reference_plan).to_dict()
            with StaticOptimizationExperimentSession(
                task_id=task_id,
                seed=world_seed,
                experiment_horizon=1,
                experiment_index_offset=pair_offset + 1,
                observation_seed=observation_seed,
                observation_noise_namespace=namespace,
                electrochemical_workflow_mode=workflow_mode,
                electrochemical_material_family_id=(
                    static_optimization_material_family_id(protocol)
                ),
                crystallization_material_family_id=(
                    static_optimization_crystallization_material_family_id(protocol)
                ),
                scoring_contract_id=static_optimization_scoring_contract_id(protocol),
            ) as session:
                intervention_result = session.execute(intervention_plan).to_dict()
            paired_replicates.append(
                {
                    "replicate_index": replicate_index,
                    "reference": {
                        "observation_seed": observation_seed,
                        "observation_noise_namespace": namespace,
                        "result": reference_result,
                    },
                    "intervention": {
                        "observation_seed": observation_seed,
                        "observation_noise_namespace": namespace,
                        "result": intervention_result,
                    },
                }
            )
        metric_results: list[dict[str, Any]] = []
        for metric_id in query.metric_ids:
            reference_mean = statistics.fmean(
                metric_value_from_result(item["reference"]["result"], metric_id)
                for item in paired_replicates
            )
            intervention_mean = statistics.fmean(
                metric_value_from_result(item["intervention"]["result"], metric_id)
                for item in paired_replicates
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
        query_results.append(
            {
                "query_id": query.query_id,
                "query_sha256": query.query_sha256,
                "query": query.to_public_dict(),
                "reference_plan_sha256": canonical_sha256(reference_plan.to_dict()),
                "intervention_plan_sha256": canonical_sha256(intervention_plan.to_dict()),
                "paired_replicates": paired_replicates,
                "metric_results": metric_results,
            }
        )
    score = score_predictive_validation(
        predictions,
        query_results,
        queries=queries,
    )
    public_queries = [query.to_public_dict() for query in queries]
    normalized_predictions = [prediction.to_dict() for prediction in predictions]
    return {
        "schema_version": queries[0].schema_version,
        "call_policy": static_optimization_predictive_call_policy(protocol),
        "query_policy": static_optimization_predictive_query_policy(protocol),
        "enabled": True,
        "frozen_before_model_prediction": True,
        "executed_after_model_prediction": True,
        "feedback_returned_to_agent": False,
        "query_count": len(queries),
        "paired_replicates_per_query": PREDICTIVE_PAIRED_REPLICATE_COUNT,
        "planned_physical_experiment_count": PREDICTIVE_PHYSICAL_EXPERIMENT_COUNT,
        "completed_physical_experiment_count": sum(
            len(item["paired_replicates"]) * 2 for item in query_results
        ),
        "model_call_count_before_execution": model_call_count_before_execution,
        "model_call_count_after_execution": model_call_count_before_execution,
        "query_set_sha256": canonical_sha256(public_queries),
        "query_sha256": [query.query_sha256 for query in queries],
        "predictions_sha256": canonical_sha256(normalized_predictions),
        "predictions": normalized_predictions,
        "queries": query_results,
        "score": score,
    }


def _load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"expected JSON object: {path}")
    return payload


def _build_client(method: Mapping[str, Any], provider: str, allow_external: bool) -> Any:
    if provider == "mock":
        return _DeterministicStaticMockClient()
    if not allow_external:
        raise RuntimeError("external provider execution requires --allow-external-provider")
    request = method["request_configuration"]
    if provider == "deepseek":
        return DeepSeekClient(
            model=str(method["model_id"]),
            thinking=bool(request["thinking"]),
            reasoning_effort=cast(Any, str(request.get("reasoning_effort") or "max")),
            timeout_s=float(request["timeout_s"]),
            max_attempts=int(request["max_attempts"]),
            retry_backoff_s=float(request["retry_backoff_s"]),
        )
    if provider == "wellau":
        return WellAUClient(
            model=str(method["model_id"]),
            reasoning_effort=cast(ReasoningEffort, str(request["reasoning_effort"])),
            timeout_s=float(request["timeout_s"]),
            max_attempts=int(request["max_attempts"]),
            retry_backoff_s=float(request["retry_backoff_s"]),
        )
    if provider == "codex_subscription":
        return CodexSubscriptionClient(
            model=str(method["model_id"]),
            reasoning_effort=cast(Any, str(request["reasoning_effort"])),
            timeout_s=float(request["timeout_s"]),
            max_attempts=int(request["max_attempts"]),
            retry_backoff_s=float(request["retry_backoff_s"]),
        )
    raise ValueError("unsupported S0 provider")


def _failure_reason_code(error: Exception) -> str:
    if isinstance(error, PromptBudgetExceededError):
        return "prompt_budget_contract_failure"
    if isinstance(error, DeepSeekAPIError):
        return "provider_infrastructure_failure"
    if isinstance(error, ValueError):
        return "invalid_model_response"
    if isinstance(error, RuntimeError):
        return "experiment_execution_failure"
    if isinstance(error, OSError):
        return "provider_infrastructure_failure"
    return "unexpected_cell_failure"


def _run_cell(
    *,
    protocol: Mapping[str, Any],
    methods: Mapping[str, Any],
    method_id: str,
    task_id: str,
    provider: str,
    allow_external_provider: bool,
    progress_file: Path | None = None,
    cell_index: int = 0,
    cell_count: int = 1,
) -> dict[str, Any]:
    method = methods["methods"][method_id]
    predictive_contract = _predictive_contract(protocol)
    if predictive_contract is not None and task_id not in {
        "electrochemical-conversion",
        "reaction-to-crystallization",
    }:
        raise ValueError("predictive validation is frozen only for the two confirmatory tasks")
    client = _build_client(method, provider, allow_external_provider)
    agent = build_static_optimization_agent(
        protocol,
        task_id,
        llm_methods=methods,
        method_id=method_id,
        client=client,
    )
    history: list[dict[str, Any]] = []
    experiments: list[dict[str, Any]] = []
    failure: dict[str, Any] | None = None
    horizon = _exploration_horizon(protocol)
    seed = int(protocol["world_policy"]["world_seed"])
    observation_seed = exploration_observation_seed(task_id, seed)
    final_synthesis: dict[str, Any] | None = None
    validation: dict[str, Any] | None = None
    predictive_validation: dict[str, Any] | None = None
    progress_base = {
        "cell_index": int(cell_index),
        "cell_count": int(cell_count),
        "task_id": task_id,
        "method_id": method_id,
        "world_seed": seed,
        "provider": provider,
    }
    _record_progress(
        progress_file,
        event="cell_started",
        stage="exploration",
        completed_experiments=0,
        total_experiments=horizon,
        **progress_base,
    )
    try:
        for experiment_index in range(horizon):
            with StaticOptimizationExperimentSession(
                task_id=task_id,
                seed=seed,
                experiment_horizon=1,
                experiment_index_offset=experiment_index,
                observation_seed=observation_seed,
                observation_noise_namespace=(
                    f"{protocol['observation_noise_namespace']}-{task_id}-"
                    f"experiment-{experiment_index:03d}"
                ),
                electrochemical_workflow_mode=static_optimization_workflow_mode(protocol),
                electrochemical_material_family_id=(
                    static_optimization_material_family_id(protocol)
                ),
                crystallization_material_family_id=(
                    static_optimization_crystallization_material_family_id(protocol)
                ),
                scoring_contract_id=static_optimization_scoring_contract_id(protocol),
            ) as session:
                _record_progress(
                    progress_file,
                    event="provider_call_inflight",
                    stage="exploration",
                    completed_experiments=experiment_index,
                    total_experiments=horizon,
                    current_experiment_index=experiment_index,
                    **progress_base,
                )
                plan = agent.plan_next(history)
                decision_audit = agent.decision_audit()
                result = session.execute(plan)
                public_record = result.public_record()
                history.append(public_record)
                experiments.append(
                    {
                        "result": result.to_dict(),
                        "decision_audit": decision_audit,
                    }
                )
                _record_progress(
                    progress_file,
                    event="experiment_completed",
                    stage="exploration",
                    completed_experiments=experiment_index + 1,
                    total_experiments=horizon,
                    current_experiment_index=experiment_index,
                    **progress_base,
                )
        final_config = protocol.get("final_synthesis", {})
        if bool(final_config.get("enabled", False)):
            _record_progress(
                progress_file,
                event="provider_call_inflight",
                stage="final_synthesis",
                completed_experiments=horizon,
                total_experiments=horizon,
                **progress_base,
            )
            recommendation = agent.synthesize_final(history)
            recommendation_sha256 = canonical_sha256(recommendation.to_dict())
            final_synthesis = {
                "recommendation": recommendation.to_dict(),
                "synthesis_audit": agent.synthesis_audit(),
                "recommendation_commit_sha256": recommendation_sha256,
                "executes_experiment": False,
                "validation_feedback_returned_to_agent": False,
            }
            if predictive_contract is not None:
                call_policy = static_optimization_predictive_call_policy(protocol)
                queries = _build_prediction_queries(
                    protocol=protocol,
                    task_id=task_id,
                    history=history,
                )
                model_calls_before_prediction = int(
                    agent.method_resource_usage()["model_call_count"]
                )
                if call_policy == PREDICTIVE_CALL_SEPARATE:
                    if recommendation.counterfactual_predictions:
                        raise RuntimeError(
                            "separate final recommendation contains predictive output"
                        )
                    _record_progress(
                        progress_file,
                        event="provider_call_inflight",
                        stage="predictive_synthesis",
                        completed_experiments=horizon,
                        total_experiments=horizon,
                        **progress_base,
                    )
                    predictions_payload: object = list(
                        agent.predict_counterfactuals(
                            history,
                            prediction_queries=queries,
                            committed_recommendation_sha256=recommendation_sha256,
                        )
                    )
                    model_calls_before_execution = int(
                        agent.method_resource_usage()["model_call_count"]
                    )
                    if model_calls_before_execution != model_calls_before_prediction + 1:
                        raise RuntimeError(
                            "predictive-only stage must consume exactly one model call"
                        )
                elif call_policy == PREDICTIVE_CALL_INTEGRATED:
                    predictions_payload = list(recommendation.counterfactual_predictions)
                    model_calls_before_execution = model_calls_before_prediction
                else:
                    raise RuntimeError("predictive call policy is not executable")
                predictive_validation = _execute_predictive_validation(
                    protocol=protocol,
                    task_id=task_id,
                    world_seed=seed,
                    history=history,
                    predictions_payload=predictions_payload,
                    experiment_index_offset=horizon,
                    model_call_count_before_execution=model_calls_before_execution,
                )
                model_calls_after_execution = int(agent.method_resource_usage()["model_call_count"])
                if model_calls_after_execution != model_calls_before_execution:
                    raise RuntimeError(
                        "predictive validation unexpectedly changed the model call count"
                    )
                predictive_validation["model_call_count_after_execution"] = (
                    model_calls_after_execution
                )
                predictive_validation["model_call_count_before_prediction"] = (
                    model_calls_before_prediction
                )
                predictive_validation["recommendation_commit_sha256"] = recommendation_sha256
                predictive_validation["recommendation_committed_before_query_visibility"] = (
                    call_policy == PREDICTIVE_CALL_SEPARATE
                )
                predictive_validation["query_visible_during_final_synthesis"] = (
                    call_policy == PREDICTIVE_CALL_INTEGRATED
                )
                predictive_validation["prediction_call_audit"] = (
                    agent.predictive_audit() if call_policy == PREDICTIVE_CALL_SEPARATE else None
                )
            scores = [float(item["terminal_summary"]["leaderboard_score"]) for item in history]
            incumbent_index = max(range(len(scores)), key=scores.__getitem__)
            incumbent_plan = _plan_from_payload(history[incumbent_index]["plan"])
            validation_config = protocol.get("validation_budget", {})
            incumbent_replicates = int(validation_config.get("incumbent_replicates", 0))
            recommendation_replicates = int(validation_config.get("recommendation_replicates", 0))
            incumbent_validation = _execute_validation_target(
                protocol=protocol,
                task_id=task_id,
                world_seed=seed,
                target="incumbent",
                plan=incumbent_plan,
                replicate_count=incumbent_replicates,
                experiment_index_offset=(
                    horizon
                    + (
                        PREDICTIVE_PHYSICAL_EXPERIMENT_COUNT
                        if predictive_contract is not None
                        else 0
                    )
                ),
            )
            recommendation_validation = _execute_validation_target(
                protocol=protocol,
                task_id=task_id,
                world_seed=seed,
                target="recommendation",
                plan=recommendation.execution_plan(),
                replicate_count=recommendation_replicates,
                experiment_index_offset=(
                    horizon
                    + (
                        PREDICTIVE_PHYSICAL_EXPERIMENT_COUNT
                        if predictive_contract is not None
                        else 0
                    )
                    + incumbent_replicates
                ),
            )
            recommendation_mean = float(recommendation_validation["score_summary"]["mean"])
            incumbent_mean = float(incumbent_validation["score_summary"]["mean"])
            validation = {
                "blind": True,
                "feedback_returned_to_agent": False,
                "incumbent_source_experiment_index": incumbent_index,
                "incumbent_observed_score": scores[incumbent_index],
                "incumbent": incumbent_validation,
                "recommendation": recommendation_validation,
                "primary_validated_recommendation_score_mean": recommendation_mean,
                "validated_incumbent_score_mean": incumbent_mean,
                "recommendation_gain_over_incumbent_mean": (recommendation_mean - incumbent_mean),
            }
    except Exception as error:
        failure = {
            "reason_code": _failure_reason_code(error),
            "error_type": type(error).__name__,
            "message": " ".join(str(error).split())[:500],
            "scientific_retry_allowed": False,
        }
        diagnostics = getattr(error, "validation_diagnostics", None)
        if isinstance(diagnostics, Mapping):
            failure["validation_diagnostics"] = copy.deepcopy(dict(diagnostics))
        _record_progress(
            progress_file,
            event="cell_failed",
            stage="failed",
            completed_experiments=len(history),
            total_experiments=horizon,
            failure_reason_code=failure["reason_code"],
            **progress_base,
        )
    resources = agent.method_resource_usage()
    integrated = bool(protocol.get("final_synthesis", {}).get("enabled", False))
    planned_incumbent_replicates = int(
        protocol.get("validation_budget", {}).get("incumbent_replicates", 0)
    )
    planned_recommendation_replicates = int(
        protocol.get("validation_budget", {}).get("recommendation_replicates", 0)
    )
    completed_validation_count = (
        sum(len(validation[target]["replicates"]) for target in ("incumbent", "recommendation"))
        if validation is not None
        else 0
    )
    planned_predictive_count = (
        PREDICTIVE_PHYSICAL_EXPERIMENT_COUNT if predictive_contract is not None else 0
    )
    planned_predictive_model_call_count = int(
        predictive_contract is not None
        and static_optimization_predictive_call_policy(protocol) == PREDICTIVE_CALL_SEPARATE
    )
    completed_predictive_model_call_count = int(
        predictive_validation is not None
        and predictive_validation.get("prediction_call_audit") is not None
    )
    completed_predictive_count = (
        int(predictive_validation["completed_physical_experiment_count"])
        if predictive_validation is not None
        else 0
    )
    formal_result = bool(protocol.get("formal_result", False)) and bool(
        methods.get("formal_result", False)
    )
    benchmark_claim_allowed = bool(protocol.get("benchmark_claim_allowed", False)) and bool(
        methods.get("benchmark_claim_allowed", False)
    )
    cell = {
        "schema_version": (
            INTEGRATED_REPORT_SCHEMA_VERSION if integrated else REPORT_SCHEMA_VERSION
        ),
        "formal_result": formal_result,
        "benchmark_claim_allowed": benchmark_claim_allowed,
        "protocol_id": protocol["protocol_id"],
        "protocol_sha256": canonical_sha256(protocol),
        "method_config_freeze_id": methods["freeze_id"],
        "method_config_sha256": canonical_sha256(methods),
        "method_id": method_id,
        "provider_mode": provider,
        "method": {
            "model_id": method["model_id"],
            "scaffold_id": method["static_optimization_scaffold_id"],
        },
        "cell": {
            "cell_id": f"{method_id}:{task_id}",
            "task_id": task_id,
            "world_seed": seed,
            "world_policy": "static_for_entire_campaign",
        },
        "world_policy": copy.deepcopy(protocol["world_policy"]),
        "reward_contract": copy.deepcopy(protocol.get("reward_contract", {})),
        "scientific_campaign_budget": copy.deepcopy(protocol.get("scientific_campaign_budget", {})),
        "measurement_budget": copy.deepcopy(protocol.get("measurement_budget", {})),
        "executor_contract": copy.deepcopy(protocol.get("executor_contract", {})),
        "recommendation_stage_present": integrated,
        "cell_status": "completed" if failure is None else "method_failure",
        "failure": failure,
        "agent_manifest": agent.manifest(),
        "resources": resources,
        "planned_experiment_count": horizon,
        "planned_exploration_model_call_count": horizon,
        "completed_exploration_model_call_count": sum(
            bool(item["decision_audit"].get("model_call_consumed", True)) for item in experiments
        ),
        "experiment_count": len(experiments),
        "completed_experiment_count": sum(int(item["result"]["completed"]) for item in experiments),
        "scores": [item["result"]["terminal_summary"]["leaderboard_score"] for item in experiments],
        "experiments": experiments,
        "public_history": history,
        "planned_synthesis_call_count": int(integrated),
        "completed_synthesis_call_count": int(final_synthesis is not None),
        "planned_predictive_model_call_count": planned_predictive_model_call_count,
        "completed_predictive_model_call_count": (completed_predictive_model_call_count),
        "final_synthesis": final_synthesis,
        "planned_validation_experiment_count": (
            planned_incumbent_replicates + planned_recommendation_replicates
        ),
        "completed_validation_experiment_count": completed_validation_count,
        "planned_predictive_validation_experiment_count": planned_predictive_count,
        "completed_predictive_validation_experiment_count": (completed_predictive_count),
        "total_physical_experiment_count": len(experiments)
        + completed_validation_count
        + completed_predictive_count,
        "validation": validation,
        "predictive_validation": predictive_validation,
        "primary_score": (
            validation["primary_validated_recommendation_score_mean"]
            if validation is not None
            else None
        ),
    }
    _record_progress(
        progress_file,
        event="cell_completed" if failure is None else "cell_finalized_after_failure",
        stage="completed" if failure is None else "failed",
        completed_experiments=len(history),
        total_experiments=horizon,
        provider_calls=int(resources["model_call_count"]),
        provider_attempts=int(resources["provider_attempt_count"]),
        **progress_base,
    )
    return cell


def _require_external_execution_confirmation(
    *,
    protocol: Mapping[str, Any],
    methods: Mapping[str, Any],
    provider: str,
    allow_external_provider: bool,
    confirmed_protocol_sha256: str | None,
    confirmed_method_sha256: str | None,
) -> None:
    if provider == "mock":
        return
    if not allow_external_provider:
        raise RuntimeError("external provider execution requires --allow-external-provider")
    expected_protocol = canonical_sha256(protocol)
    expected_methods = canonical_sha256(methods)
    if confirmed_protocol_sha256 != expected_protocol:
        raise RuntimeError(
            "paid execution requires an exact --confirm-protocol-sha256 "
            "matching the loaded protocol"
        )
    if confirmed_method_sha256 != expected_methods:
        raise RuntimeError(
            "paid execution requires an exact --confirm-method-sha256 "
            "matching the loaded method config"
        )


def run_s0(args: argparse.Namespace) -> dict[str, Any]:
    protocol = _load_json(args.protocol)
    if args.world_seed is not None:
        protocol = copy.deepcopy(protocol)
        protocol["world_policy"] = copy.deepcopy(protocol["world_policy"])
        protocol["world_policy"]["world_seed"] = int(args.world_seed)
    validate_static_optimization_protocol(protocol)
    methods = _load_json(args.llm_methods)
    _require_external_execution_confirmation(
        protocol=protocol,
        methods=methods,
        provider=str(args.provider),
        allow_external_provider=bool(args.allow_external_provider),
        confirmed_protocol_sha256=getattr(args, "confirm_protocol_sha256", None),
        confirmed_method_sha256=getattr(args, "confirm_method_sha256", None),
    )
    configured_method_ids = [
        str(item) for item in protocol.get("method_ids", []) if item in methods["methods"]
    ]
    method_ids = list(args.method_id or configured_method_ids or methods["methods"])
    task_ids = list(args.task or protocol["tasks"])
    progress_file = getattr(args, "progress_file", None)
    progress_path = Path(progress_file) if progress_file is not None else None
    requested_cells = [
        (method_id, task_id) for method_id in method_ids for task_id in task_ids
    ]
    cells = []
    for cell_index, (method_id, task_id) in enumerate(requested_cells, start=1):
        cells.append(
            _run_cell(
                protocol=protocol,
                methods=methods,
                method_id=method_id,
                task_id=task_id,
                provider=args.provider,
                allow_external_provider=bool(args.allow_external_provider),
                progress_file=progress_path,
                cell_index=cell_index,
                cell_count=len(requested_cells),
            )
        )
    for cell in cells:
        filename = f"{cell['method_id']}--{cell['cell']['task_id']}.json"
        write_json_atomic(args.output / "receipts" / filename, cell)
    integrated = bool(protocol.get("final_synthesis", {}).get("enabled", False))
    formal_result = bool(protocol.get("formal_result", False)) and bool(
        methods.get("formal_result", False)
    )
    benchmark_claim_allowed = bool(protocol.get("benchmark_claim_allowed", False)) and bool(
        methods.get("benchmark_claim_allowed", False)
    )
    report = {
        "schema_version": (
            INTEGRATED_REPORT_SCHEMA_VERSION if integrated else REPORT_SCHEMA_VERSION
        ),
        "formal_result": formal_result,
        "benchmark_claim_allowed": benchmark_claim_allowed,
        "protocol_id": protocol["protocol_id"],
        "protocol_sha256": canonical_sha256(protocol),
        "source_commit": git_source_commit(ROOT),
        "source_tree_dirty": git_worktree_dirty(ROOT),
        "method_config_freeze_id": methods["freeze_id"],
        "method_config_sha256": canonical_sha256(methods),
        "provider_mode": args.provider,
        "execution_seed": int(protocol["world_policy"]["world_seed"]),
        "world_policy": protocol["world_policy"],
        "reward_contract": copy.deepcopy(protocol.get("reward_contract", {})),
        "static_world": True,
        "hidden_world_fields_supplied": False,
        "recommendation_stage_present": integrated,
        "predictive_validation_present": bool(
            protocol.get("world_understanding", {}).get("predictive_score_enabled", False)
        ),
        "last_score_is_final_recommendation": False,
        "primary_metric": (
            "validated_final_recommendation_score_mean"
            if integrated
            else "development_descriptive_scores"
        ),
        "method_ids": method_ids,
        "task_ids": task_ids,
        "cell_count": len(cells),
        "completed_cell_count": sum(item["cell_status"] == "completed" for item in cells),
        "method_failure_cell_count": sum(item["cell_status"] == "method_failure" for item in cells),
        "planned_experiment_count": sum(item["planned_experiment_count"] for item in cells),
        "completed_experiment_count": sum(item["completed_experiment_count"] for item in cells),
        "planned_exploration_model_call_count": sum(
            item["planned_exploration_model_call_count"] for item in cells
        ),
        "completed_exploration_model_call_count": sum(
            item["completed_exploration_model_call_count"] for item in cells
        ),
        "planned_synthesis_call_count": sum(item["planned_synthesis_call_count"] for item in cells),
        "completed_synthesis_call_count": sum(
            item["completed_synthesis_call_count"] for item in cells
        ),
        "planned_predictive_model_call_count": sum(
            item["planned_predictive_model_call_count"] for item in cells
        ),
        "completed_predictive_model_call_count": sum(
            item["completed_predictive_model_call_count"] for item in cells
        ),
        "planned_validation_experiment_count": sum(
            item["planned_validation_experiment_count"] for item in cells
        ),
        "completed_validation_experiment_count": sum(
            item["completed_validation_experiment_count"] for item in cells
        ),
        "planned_predictive_validation_experiment_count": sum(
            item["planned_predictive_validation_experiment_count"] for item in cells
        ),
        "completed_predictive_validation_experiment_count": sum(
            item["completed_predictive_validation_experiment_count"] for item in cells
        ),
        "total_physical_experiment_count": sum(
            item["total_physical_experiment_count"] for item in cells
        ),
        "provider_call_count": sum(item["resources"]["model_call_count"] for item in cells),
        "provider_attempt_count": sum(
            item["resources"]["provider_attempt_count"] for item in cells
        ),
        "provider_reported_total_tokens": sum(
            item["resources"]["provider_usage"]["total_tokens"] for item in cells
        ),
        "accounting_complete": all(item["resources"]["accounting_complete"] for item in cells),
        "known_billed_cost_usd": sum(
            item["resources"]["monetary_cost_usd"]
            for item in cells
            if item["resources"]["accounting_complete"]
        ),
        "receipt_sha256": {
            f"{item['method_id']}:{item['cell']['task_id']}": canonical_sha256(item)
            for item in cells
        },
        "cells": cells,
        "interpretation": (
            f"S0 fixed-world protocol with {_exploration_horizon(protocol)} complete "
            "exploration experiments and a separate final synthesis. Its primary "
            "endpoint is blind validation of the submitted method; declared claims and "
            "frozen held-out predictive directions are separate secondary diagnostics."
            if integrated
            else (
                "S0 static optimization development baseline. It measures fixed-world "
                "optimization and feedback use only; it does not estimate change detection, "
                "mechanism attribution, recovery after a change, or method effects."
            )
        ),
    }
    write_json_atomic(args.output / "report.json", report)
    _record_progress(
        progress_path,
        event="run_completed",
        stage="completed",
        completed_cells=report["completed_cell_count"],
        failed_cells=report["method_failure_cell_count"],
        total_cells=report["cell_count"],
        provider_calls=report["provider_call_count"],
        provider_attempts=report["provider_attempt_count"],
        output=str(args.output),
    )
    return report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--protocol", type=Path, required=True)
    parser.add_argument("--llm-methods", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--provider",
        choices=("mock", "deepseek", "wellau", "codex_subscription"),
        default="mock",
    )
    parser.add_argument("--allow-external-provider", action="store_true")
    parser.add_argument(
        "--confirm-protocol-sha256",
        help="Required exact protocol hash before any external-provider execution.",
    )
    parser.add_argument(
        "--confirm-method-sha256",
        help="Required exact method-config hash before any external-provider execution.",
    )
    parser.add_argument(
        "--world-seed",
        type=int,
        default=None,
        help="Override the static world seed for this execution.",
    )
    parser.add_argument("--task", action="append")
    parser.add_argument("--method-id", action="append")
    parser.add_argument(
        "--progress-file",
        type=Path,
        help="Optional machine-readable progress file; keep it outside the repository.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    parsed = parse_args()
    result = run_s0(parsed)
    print(
        json.dumps(
            {
                "output": str(parsed.output),
                "cells": result["cell_count"],
                "completed_experiments": result["completed_experiment_count"],
                "provider": result["provider_mode"],
            },
            sort_keys=True,
        )
    )
