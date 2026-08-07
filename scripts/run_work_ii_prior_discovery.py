"""Run the staged Work II prior-revision discovery pilot.

This runner deliberately keeps the provider-facing scientific decision surface
small: four typed belief snapshots and two autonomous complete-experiment
decisions.  Prefix recipes, held-out queries, and blind replication are bound
by the protocol executor.  The runner writes only redacted, replayable records
under ``runs/``.
"""

from __future__ import annotations

import argparse
import copy
import json
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any, cast

from chemworld.agents.static_optimization import (
    StaticOptimizationPlan,
    StaticOptimizationValidator,
)
from chemworld.eval.provenance import (
    canonical_json_sha256,
    git_source_commit,
    git_worktree_dirty,
    write_json_atomic,
)
from chemworld.eval.static_optimization_execution import StaticOptimizationExperimentSession
from chemworld.eval.static_optimization_protocol import (
    static_optimization_crystallization_material_family_id,
    static_optimization_material_family_id,
    static_optimization_scoring_contract_id,
    static_optimization_workflow_mode,
    validate_static_optimization_protocol,
)
from chemworld.eval.static_optimization_seeds import validation_observation_seed
from chemworld.eval.work_ii_prior_discovery import (
    WORK_II_SNAPSHOT_STAGES,
    WorkIIHeldOutQuery,
    parse_work_ii_belief_snapshot,
    parse_work_ii_discovery_schedule,
    parse_work_ii_held_out_query,
    score_work_ii_snapshot_predictions,
    validate_work_ii_snapshot_sequence,
)
from chemworld.providers.deepseek import JsonCompletion
from chemworld.tasks import get_task

try:
    from scripts.run_static_optimization_s0 import (
        _build_client,
        _DeterministicStaticMockClient,
    )
    from scripts.run_work_ii_prior_pilot import build_pilot_protocol
except ModuleNotFoundError:
    from run_static_optimization_s0 import _build_client, _DeterministicStaticMockClient
    from run_work_ii_prior_pilot import build_pilot_protocol

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PLAN = ROOT / "configs/benchmark/work_ii_prior_discovery_pilot.json"
DEFAULT_OUTPUT = ROOT / "runs/development/work-ii-prior-discovery-pilot"
PROGRESS_SCHEMA_VERSION = "chemworld-work-ii-prior-discovery-progress-0.1"
TRAJECTORY_SCHEMA_VERSION = "chemworld-work-ii-prior-discovery-trajectory-0.1"


def _load_object(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"expected one JSON object: {path}")
    return payload


def _repo_path(value: object) -> Path:
    path = (ROOT / str(value)).resolve()
    path.relative_to(ROOT)
    return path


def _progress(path: Path | None, *, event: str, **payload: Any) -> None:
    if path is None:
        return
    record = {
        "schema_version": PROGRESS_SCHEMA_VERSION,
        "event": event,
        **payload,
    }
    write_json_atomic(path, record)
    print(json.dumps(record, ensure_ascii=False, sort_keys=True), flush=True)


def _task_interface(
    *,
    task_id: str,
    protocol: Mapping[str, Any],
    schedule_experiments: int,
) -> dict[str, Any]:
    from chemworld.agents.static_optimization import StaticOptimizationContextBuilder

    context = StaticOptimizationContextBuilder(
        get_task(task_id).to_dict(),
        total_experiments=schedule_experiments,
        final_synthesis_after_exploration=False,
        material_information=protocol.get("material_information"),
        electrochemical_material_family_id=static_optimization_material_family_id(protocol),
        crystallization_material_family_id=(
            static_optimization_crystallization_material_family_id(protocol)
        ),
        scoring_contract={"contract_id": static_optimization_scoring_contract_id(protocol)},
        electrochemical_workflow_mode=static_optimization_workflow_mode(protocol),
        optimization_scaffold_id="work_ii_direct_fixed_law_prior_discovery",
    ).build([])
    return cast(dict[str, Any], context["experiment_interface"])


def _feature_ids(interface: Mapping[str, Any], task_plan: Mapping[str, Any]) -> tuple[str, ...]:
    configured = tuple(str(item) for item in task_plan["feature_ids"])
    if interface.get("parameterization") == "named_physical_controls":
        actual = tuple(str(item) for item in interface["recipe_parameter_schema"])
    else:
        actual = tuple(
            str(item["control_id"])
            for item in interface["search_vector_coordinate_schema"]
        )
    if configured != actual:
        raise ValueError(f"task feature contract drift for {task_plan}: {configured} != {actual}")
    return configured


def _midpoint(value: Mapping[str, Any], *, category_level: int = 0) -> int | float:
    if value.get("type") == "integer":
        return int(category_level if category_level is not None else value["minimum"])
    return (float(value["minimum"]) + float(value["maximum"])) / 2.0


def _named_parameters(
    interface: Mapping[str, Any], *, target_field: str | None = None, level: int = 0
) -> dict[str, Any]:
    schema = interface["recipe_parameter_schema"]
    parameters: dict[str, Any] = {}
    for field, spec in schema.items():
        parameters[str(field)] = _midpoint(
            spec,
            category_level=(level if field == target_field else 0),
        )
    return parameters


def _unit_vector(
    interface: Mapping[str, Any], *, target_field: str | None = None, level: int = 0
) -> list[float]:
    coordinates = interface["search_vector_coordinate_schema"]
    vector = [0.5] * len(coordinates)
    for coordinate in coordinates:
        if coordinate.get("control_id") != target_field:
            continue
        category_count = int(coordinate["category_count"])
        vector[int(coordinate["coordinate"])] = (level + 0.1) / category_count
    return vector


def _plan(
    *,
    task_id: str,
    protocol: Mapping[str, Any],
    interface: Mapping[str, Any],
    intent: str,
    target_field: str | None = None,
    level: int = 0,
    vector: Sequence[float] | None = None,
) -> StaticOptimizationPlan:
    validator = StaticOptimizationValidator(
        get_task(task_id).to_dict(),
        electrochemical_workflow_mode=static_optimization_workflow_mode(protocol),
    )
    payload: dict[str, Any] = {
        "experiment_intent": intent,
        "requested_measurement_slots": [
            str(slot["slot_id"]) for slot in interface["diagnostic_measurement_slots"]
        ],
        "measurement_objective": "measure the frozen task metrics and safety signals",
        "expected_effect": "the paired condition will provide evidence about the public prior",
        "uncertainty": 0.75,
    }
    if interface.get("parameterization") == "named_physical_controls":
        payload["recipe_parameters"] = _named_parameters(
            interface, target_field=target_field, level=level
        )
    else:
        payload["search_vector"] = list(
            vector
            if vector is not None
            else _unit_vector(interface, target_field=target_field, level=level)
        )
    return validator.validate(payload)


def _feature_values(
    *,
    interface: Mapping[str, Any],
    plan: StaticOptimizationPlan,
) -> dict[str, str | int | float]:
    if interface.get("parameterization") == "named_physical_controls":
        if plan.recipe_parameters is None:
            raise ValueError("named plan lacks recipe parameters")
        return {str(key): value for key, value in plan.recipe_parameters.items()}
    vector = list(plan.search_vector)
    values: dict[str, str | int | float] = {}
    for spec in interface["search_vector_coordinate_schema"]:
        coordinate = int(spec["coordinate"])
        control_id = str(spec["control_id"])
        raw = float(vector[coordinate])
        if spec.get("kind") == "categorical":
            category_count = int(spec["category_count"])
            values[control_id] = min(int(raw * category_count), category_count - 1)
        else:
            low, high = spec["physical_bounds"]
            values[control_id] = float(low) + (float(high) - float(low)) * raw
    return values


def _protocol(
    *,
    discovery_plan: Mapping[str, Any],
    source_plan: Mapping[str, Any],
    stage_id: str,
    task_id: str,
    arm_id: str,
    world_seed: int,
    exploration_experiments: int,
) -> dict[str, Any]:
    protocol = build_pilot_protocol(
        source_plan,
        stage_id="real-probe",
        task_id=task_id,
        arm_id=arm_id,
        world_seed=world_seed,
    )
    protocol["schema_version"] = "chemworld-work-ii-prior-discovery-protocol-0.1"
    protocol["protocol_id"] = (
        f"{discovery_plan['pilot_id']}--{stage_id}--{task_id}--{arm_id}--seed{world_seed}"
    )
    protocol["freeze_id"] = protocol["protocol_id"]
    protocol["horizon"] = int(exploration_experiments)
    protocol["scientific_campaign_budget"] = {
        "exploration_experiments": int(exploration_experiments),
        "horizon_visible": True,
        "final_synthesis_after_exploration": False,
    }
    protocol["final_synthesis"] = {
        "enabled": False,
        "calls": 0,
        "mode": "work_ii_typed_snapshot_runner",
        "executes_experiment": False,
        "validation_feedback_returned_to_agent": False,
    }
    protocol["world_understanding"] = {
        "enabled": False,
        "declared_scoring_enabled": False,
        "predictive_score_enabled": False,
        "reason": "Work II snapshots use the independent typed law-summary contract",
    }
    protocol["validation_budget"] = {
        "incumbent_replicates": 0,
        "recommendation_replicates": 0,
        "independent_observation_seeds": True,
        "paired_observation_seeds_across_targets": True,
        "feedback_returned_to_agent": False,
    }
    protocol["work_ii_discovery_contract"] = {
        "schema_version": TRAJECTORY_SCHEMA_VERSION,
        "snapshot_stages": list(WORK_II_SNAPSHOT_STAGES),
        "autonomous_decisions": int(
            discovery_plan["discovery_schedule"]["autonomous_suffix_experiments"]
        ),
        "held_out_query_count": int(discovery_plan["discovery_schedule"]["held_out_query_count"]),
        "blind_recommendation_replicates": int(
            discovery_plan["discovery_schedule"]["blind_recommendation_replicates"]
        ),
    }
    validate_static_optimization_protocol(protocol)
    return protocol


def _build_queries(
    *,
    task_id: str,
    protocol: Mapping[str, Any],
    task_plan: Mapping[str, Any],
    interface: Mapping[str, Any],
    metric_ids: Sequence[str],
) -> tuple[tuple[WorkIIHeldOutQuery, StaticOptimizationPlan], ...]:
    query_plans: list[tuple[WorkIIHeldOutQuery, StaticOptimizationPlan]] = []
    target_field = str(task_plan["discriminating_target_field"])
    levels = [int(item) for item in task_plan["discriminating_levels"]]
    for index in range(4):
        level = levels[index % len(levels)]
        if interface.get("parameterization") == "named_physical_controls":
            query_plan = _plan(
                task_id=task_id,
                protocol=protocol,
                interface=interface,
                intent="held-out counterfactual query",
                target_field=target_field,
                level=level,
            )
        else:
            vector = [0.25 if index % 2 == 0 else 0.75] * int(
                interface["search_vector_dimension"]
            )
            coordinate = next(
                item for item in interface["search_vector_coordinate_schema"]
                if item["control_id"] == target_field
            )
            category_count = int(coordinate["category_count"])
            vector[int(coordinate["coordinate"])] = (level + 0.1) / category_count
            query_plan = _plan(
                task_id=task_id,
                protocol=protocol,
                interface=interface,
                intent="held-out counterfactual query",
                vector=vector,
            )
        query = parse_work_ii_held_out_query(
            {
                "schema_version": "chemworld-work-ii-held-out-query-0.1",
                "query_id": f"held-out-{index + 1:02d}",
                "task_id": task_id,
                "feature_values": _feature_values(interface=interface, plan=query_plan),
                "metric_ids": list(metric_ids),
                "replicate_count": 2,
            },
            expected_task_id=task_id,
            allowed_feature_ids=tuple(str(item) for item in task_plan["feature_ids"]),
            allowed_metric_ids=tuple(metric_ids),
        )
        query_plans.append((query, query_plan))
    return tuple(query_plans)


def _metric_observation(result: Mapping[str, Any], metric_id: str) -> float:
    final_step = result["executed_steps"][-1]
    observation = final_step.get("observation", {})
    if metric_id in observation:
        return float(observation[metric_id])
    terminal = result["terminal_summary"]
    if metric_id == "score":
        return float(terminal["leaderboard_score"])
    if metric_id == "safety_risk":
        return float(terminal["safety_risk"])
    raise ValueError(f"final assay does not expose required metric {metric_id}")


def _execute(
    *,
    protocol: Mapping[str, Any],
    task_id: str,
    world_seed: int,
    plan: StaticOptimizationPlan,
    experiment_index: int,
    namespace_suffix: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    with StaticOptimizationExperimentSession(
        task_id=task_id,
        seed=world_seed,
        experiment_horizon=1,
        experiment_index_offset=experiment_index,
        observation_seed=validation_observation_seed(
            task_id, world_seed, "work-ii-discovery", experiment_index
        ),
        observation_noise_namespace=(
            f"{protocol['observation_noise_namespace']}-{namespace_suffix}"
        ),
        electrochemical_workflow_mode=static_optimization_workflow_mode(protocol),
        electrochemical_material_family_id=static_optimization_material_family_id(protocol),
        crystallization_material_family_id=(
            static_optimization_crystallization_material_family_id(protocol)
        ),
        scoring_contract_id=static_optimization_scoring_contract_id(protocol),
    ) as session:
        result = session.execute(plan)
    return result.public_record(), result.to_dict()


def _snapshot_payload_from_mock(request: Mapping[str, Any]) -> dict[str, Any]:
    metrics = [str(item) for item in request["metric_ids"]]
    bounds = request["metric_bounds"]
    laws = []
    for metric_id in metrics:
        lower, upper = bounds[metric_id]
        laws.append(
            {
                "metric_id": metric_id,
                "intercept": (float(lower) + float(upper)) / 2.0,
                "link": "identity",
                "lower_bound": float(lower),
                "upper_bound": float(upper),
                "terms": [],
            }
        )
    evidence = [str(item) for item in request["evidence_ids"]]
    return {
        "schema_version": "chemworld-work-ii-belief-snapshot-0.1",
        "snapshot_id": f"mock-{request['snapshot_stage']}",
        "stage": request["snapshot_stage"],
        "prior_assessment": {
            "nominal_information_available": bool(request["nominal_information_available"]),
            "reliability_probability": 0.5 if request["nominal_information_available"] else None,
            "suspected_misindexed_fields": [],
            "rationale": (
                "The typed mock keeps prior reliability at an explicitly uncertain baseline."
            ),
        },
        "predictions": [
            {
                "query_id": str(query["query_id"]),
                "metrics": [
                    {
                        "metric_id": metric_id,
                        "mean": float(bounds[metric_id][0] + bounds[metric_id][1]) / 2.0,
                        "interval_lower": float(bounds[metric_id][0]),
                        "interval_upper": float(bounds[metric_id][1]),
                        "confidence": 0.5,
                    }
                    for metric_id in query["metric_ids"]
                ],
            }
            for query in request["queries"]
        ],
        "law_summary": {
            "schema_version": "chemworld-work-ii-law-summary-0.1",
            "summary_id": f"mock-law-{request['snapshot_stage']}",
            "feature_ids": list(request["feature_ids"]),
            "metric_laws": laws,
            "evidence_ids": evidence,
            "applicability": "the declared public feature domain",
            "limitations": ["typed mock has no fitted interactions"],
            "confidence": 0.5,
        },
        "evidence_ids": evidence,
        "next_experiment_intent": "Follow the frozen Work II phase schedule.",
        "overall_confidence": 0.5,
    }


def _snapshot_output_schema() -> dict[str, Any]:
    metric_prediction = {
        "type": "object",
        "additionalProperties": False,
        "required": [
            "metric_id",
            "mean",
            "interval_lower",
            "interval_upper",
            "confidence",
        ],
        "properties": {
            "metric_id": {"type": "string"},
            "mean": {"type": "number"},
            "interval_lower": {"type": "number"},
            "interval_upper": {"type": "number"},
            "confidence": {"type": "number"},
        },
    }
    law_term = {
        "type": "object",
        "required": ["term_id", "basis", "input_ids", "coefficient"],
        "properties": {
            "term_id": {"type": "string"},
            "basis": {"type": "string"},
            "input_ids": {"type": "array", "items": {"type": "string"}},
            "coefficient": {"type": "number"},
            "category_value": {},
        },
    }
    metric_law = {
        "type": "object",
        "additionalProperties": False,
        "required": [
            "metric_id",
            "intercept",
            "link",
            "lower_bound",
            "upper_bound",
            "terms",
        ],
        "properties": {
            "metric_id": {"type": "string"},
            "intercept": {"type": "number"},
            "link": {"type": "string"},
            "lower_bound": {"type": "number"},
            "upper_bound": {"type": "number"},
            "terms": {"type": "array", "items": law_term},
        },
    }
    law_summary = {
        "type": "object",
        "additionalProperties": False,
        "required": [
            "schema_version",
            "summary_id",
            "feature_ids",
            "metric_laws",
            "evidence_ids",
            "applicability",
            "limitations",
            "confidence",
        ],
        "properties": {
            "schema_version": {"type": "string"},
            "summary_id": {"type": "string"},
            "feature_ids": {"type": "array", "items": {"type": "string"}},
            "metric_laws": {"type": "array", "items": metric_law},
            "evidence_ids": {"type": "array", "items": {"type": "string"}},
            "applicability": {"type": "string"},
            "limitations": {"type": "array", "items": {"type": "string"}},
            "confidence": {"type": "number"},
        },
    }
    query_metric = {
        "type": "object",
        "additionalProperties": False,
        "required": ["query_id", "metrics"],
        "properties": {
            "query_id": {"type": "string"},
            "metrics": {"type": "array", "items": metric_prediction},
        },
    }
    return {
        "type": "object",
        "additionalProperties": False,
        "required": [
            "schema_version",
            "snapshot_id",
            "stage",
            "prior_assessment",
            "predictions",
            "law_summary",
            "evidence_ids",
            "next_experiment_intent",
            "overall_confidence",
        ],
        "properties": {
            "schema_version": {"type": "string"},
            "snapshot_id": {"type": "string"},
            "stage": {"type": "string"},
            "prior_assessment": {
                "type": "object",
                "additionalProperties": False,
                "required": [
                    "nominal_information_available",
                    "reliability_probability",
                    "suspected_misindexed_fields",
                    "rationale",
                ],
                "properties": {
                    "nominal_information_available": {"type": "boolean"},
                    "reliability_probability": {"type": ["number", "null"]},
                    "suspected_misindexed_fields": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "rationale": {"type": "string"},
                },
            },
            "predictions": {"type": "array", "items": query_metric},
            "law_summary": law_summary,
            "evidence_ids": {"type": "array", "items": {"type": "string"}},
            "next_experiment_intent": {"type": "string"},
            "overall_confidence": {"type": "number"},
        },
    }


def _compact_snapshot_output_schema() -> dict[str, Any]:
    metric_prediction = {
        "type": "object",
        "additionalProperties": False,
        "required": [
            "metric_id",
            "mean",
            "interval_lower",
            "interval_upper",
            "confidence",
        ],
        "properties": {
            "metric_id": {"type": "string"},
            "mean": {"type": "number"},
            "interval_lower": {"type": "number"},
            "interval_upper": {"type": "number"},
            "confidence": {"type": "number"},
        },
    }
    return {
        "type": "object",
        "additionalProperties": False,
        "required": [
            "snapshot_stage",
            "belief_status",
            "prior_reliability",
            "feature_beliefs",
            "metric_beliefs",
            "query_predictions",
            "evidence_ids",
            "next_experiment_intent",
        ],
        "properties": {
            "snapshot_stage": {"type": "string"},
            "belief_status": {"type": "string"},
            "prior_reliability": {"type": ["number", "null"]},
            "feature_beliefs": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["feature_id", "role", "confidence"],
                    "properties": {
                        "feature_id": {"type": "string"},
                        "role": {"type": "string"},
                        "confidence": {"type": "number"},
                    },
                },
            },
            "metric_beliefs": {"type": "array", "items": metric_prediction},
            "query_predictions": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["query_id", "metric_predictions"],
                    "properties": {
                        "query_id": {"type": "string"},
                        "metric_predictions": {
                            "type": "array",
                            "items": metric_prediction,
                        },
                    },
                },
            },
            "evidence_ids": {"type": "array", "items": {"type": "string"}},
            "next_experiment_intent": {"type": "string"},
        },
    }


def _compile_snapshot_draft(
    payload: Mapping[str, Any],
    *,
    stage: str,
    task_plan: Mapping[str, Any],
    queries: Sequence[Any],
    nominal_information_available: bool,
) -> dict[str, Any]:
    if "schema_version" in payload:
        return dict(payload)
    expected = {
        "snapshot_stage",
        "belief_status",
        "prior_reliability",
        "feature_beliefs",
        "metric_beliefs",
        "query_predictions",
        "evidence_ids",
        "next_experiment_intent",
    }
    if set(payload) != expected:
        raise ValueError(
            "compact belief draft fields do not match the contract: "
            f"missing={sorted(expected - set(payload))}, "
            f"extra={sorted(set(payload) - expected)}"
        )
    if str(payload["snapshot_stage"]) != stage:
        raise ValueError("compact belief draft stage does not match the requested snapshot")
    feature_ids = [str(item) for item in task_plan["feature_ids"]]
    metric_ids = [str(item) for item in task_plan["prediction_metrics"]]
    raw_features = payload["feature_beliefs"]
    if not isinstance(raw_features, list):
        raise ValueError("compact feature_beliefs must be a list")
    feature_belief_ids = [str(item["feature_id"]) for item in raw_features]
    if not set(feature_belief_ids).issubset(set(feature_ids)):
        raise ValueError("compact feature_beliefs contains an unknown feature")
    raw_metrics = payload["metric_beliefs"]
    if not isinstance(raw_metrics, list):
        raise ValueError("compact metric_beliefs must be a list")
    metric_map = {str(item["metric_id"]): item for item in raw_metrics}
    if set(metric_map) != set(metric_ids):
        raise ValueError("compact metric_beliefs do not cover the exact task metrics")
    bounds = task_plan["prediction_metrics"]

    def normalize_prediction(item: Mapping[str, Any]) -> dict[str, Any]:
        metric_id = str(item["metric_id"])
        if metric_id not in metric_ids:
            raise ValueError("compact query prediction contains an unknown metric")
        mean = float(item["mean"])
        lower = float(item["interval_lower"])
        upper = float(item["interval_upper"])
        confidence = float(item["confidence"])
        if not lower <= mean <= upper or not 0.0 <= confidence <= 1.0:
            raise ValueError("compact query prediction has invalid interval or confidence")
        return {
            "metric_id": metric_id,
            "mean": mean,
            "interval_lower": lower,
            "interval_upper": upper,
            "confidence": confidence,
        }

    metric_laws = []
    for metric_id in metric_ids:
        metric = metric_map[metric_id]
        lower, upper = bounds[metric_id]
        metric_laws.append(
            {
                "metric_id": metric_id,
                "intercept": float(metric["mean"]),
                "link": "identity",
                "lower_bound": float(lower),
                "upper_bound": float(upper),
                "terms": [],
            }
        )
    raw_queries = payload["query_predictions"]
    if not isinstance(raw_queries, list):
        raise ValueError("compact query_predictions must be a list")
    query_map = {str(item["query_id"]): item for item in raw_queries}
    expected_query_ids = {str(query.query_id) for query in queries}
    if set(query_map) != expected_query_ids:
        raise ValueError("compact query_predictions do not cover the exact query set")
    predictions = []
    for query in queries:
        raw_query = query_map[query.query_id]
        raw_query_metrics = raw_query["metric_predictions"]
        metric_prediction_map = {
            str(item["metric_id"]): item for item in raw_query_metrics
        }
        if set(metric_prediction_map) != set(query.metric_ids):
            raise ValueError("compact query prediction metrics drifted from the query contract")
        predictions.append(
            {
                "query_id": query.query_id,
                "metrics": [
                    normalize_prediction(metric_prediction_map[metric_id])
                    for metric_id in query.metric_ids
                ],
            }
        )
    reliability = None if not nominal_information_available else payload["prior_reliability"]
    if reliability is not None:
        reliability = float(reliability)
        if not 0.0 <= reliability <= 1.0:
            raise ValueError("compact prior_reliability must be in [0,1]")
    mean_confidence = sum(float(item["confidence"]) for item in raw_metrics) / len(raw_metrics)
    return {
        "schema_version": "chemworld-work-ii-belief-snapshot-0.1",
        "snapshot_id": f"wellau-{stage}",
        "stage": stage,
        "prior_assessment": {
            "nominal_information_available": nominal_information_available,
            "reliability_probability": reliability,
            "suspected_misindexed_fields": [],
            "rationale": str(payload["belief_status"]),
        },
        "predictions": predictions,
        "law_summary": {
            "schema_version": "chemworld-work-ii-law-summary-0.1",
            "summary_id": f"wellau-law-{stage}",
            "feature_ids": feature_ids,
            "metric_laws": metric_laws,
            "evidence_ids": [str(item) for item in payload["evidence_ids"]],
            "applicability": "the declared public feature domain",
            "limitations": [
                "provider-facing compact draft compiled to constant metric laws",
                "interaction terms require a later formal law-summary scaffold",
            ],
            "confidence": mean_confidence,
        },
        "evidence_ids": [str(item) for item in payload["evidence_ids"]],
        "next_experiment_intent": str(payload["next_experiment_intent"]),
        "overall_confidence": mean_confidence,
    }


class _WorkIIDiscoveryMockClient:
    model = "work-ii-discovery-mock"
    thinking = False
    reasoning_effort = None

    def __init__(self) -> None:
        self._static = _DeterministicStaticMockClient()

    def complete_json(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int = 4096,
        output_schema: Mapping[str, Any] | None = None,
    ) -> JsonCompletion:
        del system_prompt, output_schema
        request = json.loads(user_prompt)
        if "work_ii_snapshot_request" in request:
            return JsonCompletion(
                payload=_snapshot_payload_from_mock(request),
                model=self.model,
                usage={"prompt_tokens": 220, "completion_tokens": 240, "total_tokens": 460},
                attempts=1,
            )
        if "work_ii_autonomous_request" in request:
            interface = request["experiment_interface"]
            history_count = len(request["history"])
            if interface.get("parameterization") == "named_physical_controls":
                schema = interface["recipe_parameter_schema"]
                parameters = {
                    field: _midpoint(spec, category_level=history_count % 4)
                    for field, spec in schema.items()
                }
                selection = {"recipe_parameters": parameters}
            else:
                vector = [0.5] * int(interface["search_vector_dimension"])
                if vector:
                    vector[history_count % len(vector)] = 0.25 if history_count % 2 else 0.75
                selection = {"search_vector": vector}
            return JsonCompletion(
                payload={
                    **selection,
                    "experiment_intent": (
                        "use the latest typed evidence to choose a safe autonomous experiment"
                    ),
                    "requested_measurement_slots": [
                        str(item["slot_id"])
                        for item in interface["diagnostic_measurement_slots"]
                    ],
                    "measurement_objective": "measure the public task metrics",
                    "expected_effect": (
                        "the selected condition will improve or clarify the fixed law"
                    ),
                    "uncertainty": 0.6,
                },
                model=self.model,
                usage={"prompt_tokens": 240, "completion_tokens": 140, "total_tokens": 380},
                attempts=1,
            )
        return self._static.complete_json(
            system_prompt="",
            user_prompt=user_prompt,
            max_tokens=max_tokens,
        )

    def pricing_snapshot(self) -> dict[str, Any]:
        return {
            "provider": "mock",
            "model_id": self.model,
            "accounting_complete": True,
            "input_per_million_usd": 0.0,
            "output_per_million_usd": 0.0,
        }

    def estimate_cost_usd(self, usage: Mapping[str, Any]) -> float:
        del usage
        return 0.0


def _call_snapshot(
    *,
    client: Any,
    stage: str,
    protocol: Mapping[str, Any],
    task_plan: Mapping[str, Any],
    interface: Mapping[str, Any],
    queries: Sequence[WorkIIHeldOutQuery],
    history: Sequence[Mapping[str, Any]],
    evidence_ids: Sequence[str],
    max_tokens: int,
) -> tuple[dict[str, Any], JsonCompletion]:
    metric_ids = [str(item) for item in task_plan["prediction_metrics"]]
    request = {
        "work_ii_snapshot_request": True,
        "schema_version": "chemworld-work-ii-belief-snapshot-0.1",
        "snapshot_stage": stage,
        "nominal_information_available": protocol["material_information"]["mode"] != "opaque_codes",
        "public_material_information": protocol.get("material_information"),
        "feature_ids": list(task_plan["feature_ids"]),
        "metric_ids": metric_ids,
        "metric_bounds": task_plan["prediction_metrics"],
        "queries": [query.to_dict() for query in queries],
        "history": list(history[-8:]),
        "evidence_ids": list(evidence_ids),
        "instructions": (
            "Return only the typed Work II belief snapshot. Do not name the prior arm. "
            "Treat measured evidence as authoritative, expose uncertainty, and provide an "
            "executable law summary whose metric predictions cover every held-out query."
        ),
    }
    completion = client.complete_json(
        system_prompt=(
            "You are a scientific discovery participant. You must return a strict JSON "
            "belief snapshot; do not claim hidden world fields."
        ),
        user_prompt=json.dumps(request, ensure_ascii=False, sort_keys=True),
        max_tokens=max_tokens,
        output_schema=_compact_snapshot_output_schema(),
    )
    compiled = _compile_snapshot_draft(
        completion.payload,
        stage=stage,
        task_plan=task_plan,
        queries=queries,
        nominal_information_available=(
            protocol["material_information"]["mode"] != "opaque_codes"
        ),
    )
    return compiled, completion


def _call_autonomous(
    *,
    client: Any,
    protocol: Mapping[str, Any],
    task_id: str,
    task_plan: Mapping[str, Any],
    interface: Mapping[str, Any],
    history: Sequence[Mapping[str, Any]],
    snapshot: Mapping[str, Any],
    max_tokens: int,
) -> tuple[StaticOptimizationPlan, JsonCompletion]:
    request = {
        "work_ii_autonomous_request": True,
        "task_id": task_id,
        "feature_ids": list(task_plan["feature_ids"]),
        "experiment_interface": copy.deepcopy(dict(interface)),
        "public_material_information": protocol.get("material_information"),
        "history": list(history[-8:]),
        "latest_belief_snapshot": snapshot,
        "instructions": (
            "Choose exactly one complete experiment using only public history and the latest "
            "typed snapshot. Return the task-native plan fields and no hidden world fields."
        ),
    }
    completion = client.complete_json(
        system_prompt=(
            "You are an autonomous scientific experiment planner. Return one complete "
            "experiment JSON object with no commentary outside the object."
        ),
        user_prompt=json.dumps(request, ensure_ascii=False, sort_keys=True),
        max_tokens=max_tokens,
    )
    validator = StaticOptimizationValidator(
        get_task(task_id).to_dict(),
        electrochemical_workflow_mode=static_optimization_workflow_mode(protocol),
    )
    plan_payload = dict(completion.payload)
    plan = validator.validate(plan_payload)
    return plan, completion


def _run_cell(
    *,
    discovery_plan: Mapping[str, Any],
    source_plan: Mapping[str, Any],
    method: Mapping[str, Any],
    method_id: str,
    stage_id: str,
    task_id: str,
    arm_id: str,
    world_seed: int,
    output: Path,
    progress_file: Path | None,
    provider: str,
    allow_external_provider: bool,
    cell_index: int,
    cell_count: int,
) -> dict[str, Any]:
    schedule = parse_work_ii_discovery_schedule(discovery_plan["discovery_schedule"])
    task_plan = discovery_plan["tasks"][task_id]
    protocol = _protocol(
        discovery_plan=discovery_plan,
        source_plan=source_plan,
        stage_id=stage_id,
        task_id=task_id,
        arm_id=arm_id,
        world_seed=world_seed,
        exploration_experiments=schedule.exploration_experiments,
    )
    interface = _task_interface(
        task_id=task_id,
        protocol=protocol,
        schedule_experiments=schedule.exploration_experiments,
    )
    feature_ids = _feature_ids(interface, task_plan)
    metric_ids = tuple(str(item) for item in task_plan["prediction_metrics"])
    query_pairs = _build_queries(
        task_id=task_id,
        protocol=protocol,
        task_plan=task_plan,
        interface=interface,
        metric_ids=metric_ids,
    )
    queries = tuple(query for query, _ in query_pairs)
    query_contract = {
        query.query_id: tuple(query.metric_ids) for query in queries
    }
    if provider == "mock":
        client: Any = _WorkIIDiscoveryMockClient()
    else:
        client = _build_client(method, provider, allow_external_provider)
    cell_id = f"{cell_index:02d}--{task_id}--{arm_id}--seed{world_seed}"
    cell_root = output / "cells" / cell_id
    protocol_path = output / "protocols" / f"{cell_id}.json"
    write_json_atomic(protocol_path, protocol)
    history: list[dict[str, Any]] = []
    raw_results: list[dict[str, Any]] = []
    decisions: list[dict[str, Any]] = []
    snapshots: list[Any] = []
    usages: list[dict[str, int]] = []
    _progress(
        progress_file,
        event="cell_started",
        stage=stage_id,
        cell_index=cell_index,
        cell_count=cell_count,
        task_id=task_id,
        prior_arm=arm_id,
        world_seed=world_seed,
        completed_physical_experiments=0,
        total_physical_experiments=schedule.physical_experiments_per_cell,
    )
    try:
        evidence_ids: list[str] = []
        _progress(
            progress_file,
            event="snapshot_provider_call_inflight",
            snapshot_stage="pre_evidence",
            stage=stage_id,
            cell_index=cell_index,
            task_id=task_id,
            prior_arm=arm_id,
            completed_provider_decisions=0,
            total_provider_decisions=schedule.provider_decisions_per_cell,
        )
        payload, completion = _call_snapshot(
            client=client,
            stage="pre_evidence",
            protocol=protocol,
            task_plan=task_plan,
            interface=interface,
            queries=queries,
            history=history,
            evidence_ids=evidence_ids,
            max_tokens=int(method["request_configuration"].get("snapshot_max_tokens", 4500)),
        )
        usages.append(dict(completion.usage))
        snapshot = parse_work_ii_belief_snapshot(
            payload,
            expected_stage="pre_evidence",
            query_metric_contract=query_contract,
            allowed_feature_ids=feature_ids,
            allowed_metric_ids=metric_ids,
            allowed_prior_fields=tuple(task_plan["prior_fields"]),
            evidence_catalog=tuple(evidence_ids),
            nominal_information_available=arm_id != "opaque",
        )
        snapshots.append(snapshot)
        neutral = _plan(
            task_id=task_id,
            protocol=protocol,
            interface=interface,
            intent="frozen neutral-prefix evidence acquisition",
        )
        public, raw = _execute(
            protocol=protocol,
            task_id=task_id,
            world_seed=world_seed,
            plan=neutral,
            experiment_index=0,
            namespace_suffix="neutral-prefix-000",
        )
        history.append(public)
        raw_results.append(raw)
        evidence_ids.extend(
            str(item["evidence_id"])
            for item in public.get("measurement_evidence", [])
        )
        _progress(
            progress_file,
            event="neutral_prefix_completed",
            stage=stage_id,
            cell_index=cell_index,
            task_id=task_id,
            prior_arm=arm_id,
            completed_physical_experiments=1,
            total_physical_experiments=schedule.physical_experiments_per_cell,
        )
        _progress(
            progress_file,
            event="snapshot_provider_call_inflight",
            snapshot_stage="post_neutral",
            stage=stage_id,
            cell_index=cell_index,
            task_id=task_id,
            prior_arm=arm_id,
            completed_provider_decisions=1,
            total_provider_decisions=schedule.provider_decisions_per_cell,
        )
        payload, completion = _call_snapshot(
            client=client,
            stage="post_neutral",
            protocol=protocol,
            task_plan=task_plan,
            interface=interface,
            queries=queries,
            history=history,
            evidence_ids=evidence_ids,
            max_tokens=int(method["request_configuration"].get("snapshot_max_tokens", 4500)),
        )
        usages.append(dict(completion.usage))
        snapshots.append(
            parse_work_ii_belief_snapshot(
                payload,
                expected_stage="post_neutral",
                query_metric_contract=query_contract,
                allowed_feature_ids=feature_ids,
                allowed_metric_ids=metric_ids,
                allowed_prior_fields=tuple(task_plan["prior_fields"]),
                evidence_catalog=tuple(evidence_ids),
                nominal_information_available=arm_id != "opaque",
            )
        )
        for index, level in enumerate(task_plan["discriminating_levels"]):
            discriminating = _plan(
                task_id=task_id,
                protocol=protocol,
                interface=interface,
                intent="frozen discriminating-prefix paired evidence acquisition",
                target_field=str(task_plan["discriminating_target_field"]),
                level=int(level),
            )
            public, raw = _execute(
                protocol=protocol,
                task_id=task_id,
                world_seed=world_seed,
                plan=discriminating,
                experiment_index=index + 1,
                namespace_suffix=f"discriminating-prefix-{index:03d}",
            )
            history.append(public)
            raw_results.append(raw)
            evidence_ids.extend(
                str(item["evidence_id"])
                for item in public.get("measurement_evidence", [])
            )
        _progress(
            progress_file,
            event="snapshot_provider_call_inflight",
            snapshot_stage="post_discriminating",
            stage=stage_id,
            cell_index=cell_index,
            task_id=task_id,
            prior_arm=arm_id,
            completed_provider_decisions=2,
            total_provider_decisions=schedule.provider_decisions_per_cell,
        )
        payload, completion = _call_snapshot(
            client=client,
            stage="post_discriminating",
            protocol=protocol,
            task_plan=task_plan,
            interface=interface,
            queries=queries,
            history=history,
            evidence_ids=evidence_ids,
            max_tokens=int(method["request_configuration"].get("snapshot_max_tokens", 4500)),
        )
        usages.append(dict(completion.usage))
        snapshots.append(
            parse_work_ii_belief_snapshot(
                payload,
                expected_stage="post_discriminating",
                query_metric_contract=query_contract,
                allowed_feature_ids=feature_ids,
                allowed_metric_ids=metric_ids,
                allowed_prior_fields=tuple(task_plan["prior_fields"]),
                evidence_catalog=tuple(evidence_ids),
                nominal_information_available=arm_id != "opaque",
            )
        )
        for autonomous_index in range(schedule.autonomous_suffix_experiments):
            _progress(
                progress_file,
                event="autonomous_provider_call_inflight",
                stage=stage_id,
                cell_index=cell_index,
                task_id=task_id,
                prior_arm=arm_id,
                completed_physical_experiments=len(raw_results),
                total_physical_experiments=schedule.physical_experiments_per_cell,
            )
            plan, completion = _call_autonomous(
                client=client,
                protocol=protocol,
                task_id=task_id,
                task_plan=task_plan,
                interface=interface,
                history=history,
                snapshot=snapshots[-1].to_dict(),
                max_tokens=int(method["request_configuration"]["max_tokens"]),
            )
            usages.append(dict(completion.usage))
            public, raw = _execute(
                protocol=protocol,
                task_id=task_id,
                world_seed=world_seed,
                plan=plan,
                experiment_index=len(raw_results),
                namespace_suffix=f"autonomous-suffix-{autonomous_index:03d}",
            )
            history.append(public)
            raw_results.append(raw)
            decisions.append(
                {
                    "stage": "autonomous_suffix",
                    "experiment_index": len(raw_results) - 1,
                    "plan": plan.to_dict(),
                    "plan_sha256": canonical_json_sha256(plan.to_dict()),
                }
            )
        _progress(
            progress_file,
            event="snapshot_provider_call_inflight",
            snapshot_stage="final",
            stage=stage_id,
            cell_index=cell_index,
            task_id=task_id,
            prior_arm=arm_id,
            completed_provider_decisions=5,
            total_provider_decisions=schedule.provider_decisions_per_cell,
        )
        payload, completion = _call_snapshot(
            client=client,
            stage="final",
            protocol=protocol,
            task_plan=task_plan,
            interface=interface,
            queries=queries,
            history=history,
            evidence_ids=evidence_ids,
            max_tokens=int(method["request_configuration"].get("snapshot_max_tokens", 4500)),
        )
        usages.append(dict(completion.usage))
        snapshots.append(
            parse_work_ii_belief_snapshot(
                payload,
                expected_stage="final",
                query_metric_contract=query_contract,
                allowed_feature_ids=feature_ids,
                allowed_metric_ids=metric_ids,
                allowed_prior_fields=tuple(task_plan["prior_fields"]),
                evidence_catalog=tuple(evidence_ids),
                nominal_information_available=arm_id != "opaque",
            )
        )
        validate_work_ii_snapshot_sequence(snapshots)
        held_out_observed: dict[str, dict[str, float]] = {}
        held_out_records: list[dict[str, Any]] = []
        experiment_offset = len(raw_results)
        for query_index, (query, query_plan) in enumerate(query_pairs):
            replicate_values: dict[str, list[float]] = {metric_id: [] for metric_id in metric_ids}
            for replicate_index in range(query.replicate_count):
                public, raw = _execute(
                    protocol=protocol,
                    task_id=task_id,
                    world_seed=world_seed,
                    plan=query_plan,
                    experiment_index=experiment_offset,
                    namespace_suffix=f"held-out-{query_index:02d}-{replicate_index:02d}",
                )
                experiment_offset += 1
                for metric_id in metric_ids:
                    replicate_values[metric_id].append(_metric_observation(raw, metric_id))
            held_out_observed[query.query_id] = {
                metric_id: sum(values) / len(values)
                for metric_id, values in replicate_values.items()
            }
            held_out_records.append(
                {
                    "query": query.to_dict(),
                    "plan_sha256": canonical_json_sha256(query_plan.to_dict()),
                    "replicate_values": replicate_values,
                }
            )
        prediction_scores = [
            score_work_ii_snapshot_predictions(snapshot, held_out_observed)
            for snapshot in snapshots
        ]
        scores = [float(item["terminal_summary"]["leaderboard_score"]) for item in raw_results]
        incumbent_index = max(range(len(scores)), key=scores.__getitem__)
        incumbent_plan = StaticOptimizationPlan(
            **dict(raw_results[incumbent_index]["plan"])
        )
        blind_values: list[float] = []
        for replicate_index in range(schedule.blind_recommendation_replicates):
            _, raw = _execute(
                protocol=protocol,
                task_id=task_id,
                world_seed=world_seed,
                plan=incumbent_plan,
                experiment_index=experiment_offset,
                namespace_suffix=f"blind-recommendation-{replicate_index:02d}",
            )
            experiment_offset += 1
            blind_values.append(float(raw["terminal_summary"]["leaderboard_score"]))
        trajectory = {
            "schema_version": TRAJECTORY_SCHEMA_VERSION,
            "formal_result": False,
            "benchmark_claim_allowed": False,
            "scientific_result": False,
            "cell": {
                "cell_id": f"{method_id}:{task_id}:{arm_id}:seed{world_seed}",
                "task_id": task_id,
                "prior_arm": arm_id,
                "world_seed": world_seed,
            },
            "protocol_sha256": canonical_json_sha256(protocol),
            "method_id": method_id,
            "provider": provider,
            "provider_wire_api": "responses" if provider == "wellau" else "mock",
            "feature_ids": list(feature_ids),
            "prediction_metric_bounds": copy.deepcopy(task_plan["prediction_metrics"]),
            "query_set": [query.to_dict() for query in queries],
            "snapshots": [snapshot.to_dict() for snapshot in snapshots],
            "autonomous_decisions": decisions,
            "exploration_experiment_count": len(raw_results),
            "held_out_validation": held_out_records,
            "prediction_scores_by_snapshot": prediction_scores,
            "blind_validation": {
                "recommendation_rule": "best_observed_completed_experiment",
                "source_experiment_index": incumbent_index,
                "replicate_scores": blind_values,
                "mean_score": sum(blind_values) / len(blind_values),
            },
            "resource_accounting": {
                "provider_call_count": len(usages),
                "provider_attempt_count": sum(
                    int(completion.get("attempts", 1)) for completion in []
                ),
                "input_tokens": sum(int(usage.get("prompt_tokens", 0)) for usage in usages),
                "output_tokens": sum(int(usage.get("completion_tokens", 0)) for usage in usages),
                "total_tokens": sum(int(usage.get("total_tokens", 0)) for usage in usages),
                "cache_hit_tokens": sum(
                    int(usage.get("prompt_cache_hit_tokens", 0)) for usage in usages
                ),
            },
        }
        trajectory["resource_accounting"]["provider_attempt_count"] = len(usages)
        write_json_atomic(cell_root / "trajectory.json", trajectory)
        return {
            "cell_index": cell_index,
            "task_id": task_id,
            "prior_arm": arm_id,
            "world_seed": world_seed,
            "completed": True,
            "trajectory_path": str((cell_root / "trajectory.json").relative_to(output)),
            "trajectory_sha256": canonical_json_sha256(trajectory),
            "provider_call_count": len(usages),
            "provider_attempt_count": len(usages),
            "provider_reported_total_tokens": trajectory["resource_accounting"]["total_tokens"],
            "completed_exploration_experiments": len(raw_results),
            "completed_held_out_experiments": sum(
                query.replicate_count for query in queries
            ),
            "completed_blind_experiments": len(blind_values),
            "failure": None,
        }
    except Exception as error:
        failure = {
            "reason_code": (
                "invalid_model_response"
                if isinstance(error, ValueError)
                else "cell_execution_failure"
            ),
            "error_type": type(error).__name__,
            "message": " ".join(str(error).split())[:500],
            "scientific_retry_allowed": False,
        }
        _progress(
            progress_file,
            event="cell_failed",
            stage=stage_id,
            cell_index=cell_index,
            task_id=task_id,
            prior_arm=arm_id,
            completed_physical_experiments=len(raw_results),
            total_physical_experiments=schedule.physical_experiments_per_cell,
            failure_reason_code=failure["reason_code"],
        )
        return {
            "cell_index": cell_index,
            "task_id": task_id,
            "prior_arm": arm_id,
            "world_seed": world_seed,
            "completed": False,
            "provider_call_count": len(usages),
            "provider_attempt_count": len(usages),
            "provider_reported_total_tokens": sum(
                int(usage.get("total_tokens", 0)) for usage in usages
            ),
            "completed_exploration_experiments": len(raw_results),
            "completed_held_out_experiments": 0,
            "completed_blind_experiments": 0,
            "failure": failure,
        }


def run_discovery(args: argparse.Namespace) -> dict[str, Any]:
    discovery_plan = _load_object(args.plan)
    source_plan = _load_object(_repo_path(discovery_plan["source_prior_contract_plan"]))
    stage = discovery_plan["stages"][args.stage]
    provider = str(stage["provider"])
    if provider not in {"mock", "wellau"}:
        raise ValueError("Work II discovery supports only mock or WellAU")
    if provider == "wellau" and not args.allow_external_provider:
        raise RuntimeError("real Work II discovery requires --allow-external-provider")
    if provider == "wellau" and git_worktree_dirty(ROOT):
        raise RuntimeError("real Work II discovery requires a clean committed worktree")
    task_ids = (
        [str(item) for item in discovery_plan["task_ids"]]
        if stage["task_ids"] == "all"
        else [str(item) for item in stage["task_ids"]]
    )
    arm_ids = (
        list(discovery_plan["prior_arms"])
        if stage["prior_arms"] == "all"
        else [str(item) for item in stage["prior_arms"]]
    )
    world_seeds = [int(item) for item in stage["world_seeds"]]
    cells = [
        (task_id, arm_id, world_seed)
        for world_seed in world_seeds
        for task_id in task_ids
        for arm_id in arm_ids
    ]
    if len(cells) != int(stage["expected_cells"]):
        raise ValueError("discovery stage denominator differs from expected_cells")
    method_path = _repo_path(
        "configs/methods/work_ii/participant_methods_work_ii_wellau_sol_medium_prior_discovery.json"
    )
    methods = _load_object(method_path)
    method_id = "work_ii_wellau_sol_medium_prior_discovery"
    method = methods["methods"][method_id]
    output = args.output.resolve()
    progress_file = args.progress_file.resolve() if args.progress_file else None
    results: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    for cell_index, (task_id, arm_id, world_seed) in enumerate(cells, start=1):
        result = _run_cell(
            discovery_plan=discovery_plan,
            source_plan=source_plan,
            method=method,
            method_id=method_id,
            stage_id=args.stage,
            task_id=task_id,
            arm_id=arm_id,
            world_seed=world_seed,
            output=output,
            progress_file=progress_file,
            provider=provider,
            allow_external_provider=args.allow_external_provider,
            cell_index=cell_index,
            cell_count=len(cells),
        )
        results.append(result)
        if not result["completed"]:
            failures.append(result)
        _progress(
            progress_file,
            event="cell_completed" if result["completed"] else "cell_failed",
            stage=args.stage,
            completed_cells=sum(bool(item["completed"]) for item in results),
            failed_cells=len(failures),
            total_cells=len(cells),
            current_cell_index=cell_index,
            task_id=task_id,
            prior_arm=arm_id,
            world_seed=world_seed,
        )
        if failures:
            break
    summary = {
        "schema_version": "chemworld-work-ii-prior-discovery-execution-index-0.1",
        "pilot_id": discovery_plan["pilot_id"],
        "stage": args.stage,
        "formal_result": False,
        "benchmark_claim_allowed": False,
        "scientific_result": False,
        "source_commit": git_source_commit(ROOT),
        "source_tree_dirty": git_worktree_dirty(ROOT),
        "provider": provider,
        "wire_api": "responses" if provider == "wellau" else "mock",
        "model_id": discovery_plan["participant"]["model_id"],
        "reasoning_effort": discovery_plan["participant"]["reasoning_effort"],
        "expected_cell_count": len(cells),
        "attempted_cell_count": len(results),
        "completed_cell_count": sum(bool(item["completed"]) for item in results),
        "failed_cell_count": len(failures),
        "all_requested_cells_completed": len(results) == len(cells) and not failures,
        "provider_call_count": sum(int(item["provider_call_count"]) for item in results),
        "provider_attempt_count": sum(int(item["provider_attempt_count"]) for item in results),
        "provider_reported_total_tokens": sum(
            int(item["provider_reported_total_tokens"]) for item in results
        ),
        "results": results,
        "failures": failures,
    }
    write_json_atomic(output / "execution_index.json", summary)
    _progress(
        progress_file,
        event="run_completed" if summary["all_requested_cells_completed"] else "run_failed",
        stage=args.stage,
        completed_cells=summary["completed_cell_count"],
        failed_cells=summary["failed_cell_count"],
        total_cells=summary["expected_cell_count"],
    )
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, default=DEFAULT_PLAN)
    parser.add_argument(
        "--stage",
        choices=("mock-discovery-preflight", "real-discovery-probe", "one-seed-breadth"),
        required=True,
    )
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--progress-file", type=Path)
    parser.add_argument("--allow-external-provider", action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    parsed = parse_args()
    result = run_discovery(parsed)
    print(
        json.dumps(
            {
                "output": str(parsed.output),
                "stage": result["stage"],
                "completed_cells": result["completed_cell_count"],
                "failed_cells": result["failed_cell_count"],
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    raise SystemExit(0 if result["all_requested_cells_completed"] else 1)
