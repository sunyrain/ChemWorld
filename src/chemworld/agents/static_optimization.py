"""Static scientific optimization agent for explicit fixed-world protocols."""

from __future__ import annotations

import copy
import json
import math
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any, ClassVar

import numpy as np

from chemworld.agents.crystallization_single_stage import (
    CRYSTALLIZATION_SINGLE_STAGE_CATEGORICAL_COORDINATES,
    CRYSTALLIZATION_SINGLE_STAGE_DIMENSION,
    CRYSTALLIZATION_SINGLE_STAGE_MEASUREMENT_SLOTS,
    CRYSTALLIZATION_SINGLE_STAGE_RECIPE_VERSION,
    crystallization_single_stage_parameter_schema,
    crystallization_single_stage_parameters_from_unit_vector,
    crystallization_single_stage_recipe_from_unit_vector,
    crystallization_single_stage_unit_vector_from_parameters,
)
from chemworld.agents.electrochemical_single_stage import (
    ELECTROCHEMICAL_SINGLE_STAGE_CATEGORICAL_COORDINATES,
    ELECTROCHEMICAL_SINGLE_STAGE_DIMENSION,
    ELECTROCHEMICAL_SINGLE_STAGE_MEASUREMENT_SLOTS,
    ELECTROCHEMICAL_SINGLE_STAGE_RECIPE_VERSION,
    electrochemical_single_stage_parameter_schema,
    electrochemical_single_stage_parameters_from_unit_vector,
    electrochemical_single_stage_recipe_from_unit_vector,
    electrochemical_single_stage_unit_vector_from_parameters,
)
from chemworld.agents.live_llm import JsonPlannerClientLike
from chemworld.agents.prompt_context import PromptBudgetExceededError, estimate_prompt_tokens
from chemworld.agents.scientific_adaptation import (
    ResourceLedger,
    ScientificPlanValidationError,
    canonical_sha256,
    scientific_measurement_slots,
)
from chemworld.agents.task_recipes import (
    TASK_RECIPE_SPACE_VERSION,
    electrochemical_recipe_parameter_schema,
    electrochemical_recipe_parameters_from_unit_vector,
    electrochemical_recipe_unit_vector_from_parameters,
    task_recipe_categorical_coordinates,
    task_recipe_dimension,
    task_recipe_from_unit_vector,
    task_recipe_kind,
)
from chemworld.data.logging import to_builtin
from chemworld.eval.crystallization_predictive import (
    CrystallizationPredictionQuery,
    build_crystallization_prediction_queries,
)
from chemworld.eval.electrochemical_predictive import (
    ElectrochemicalPredictionQuery,
    build_electrochemical_prediction_queries,
    parse_counterfactual_predictions,
)
from chemworld.eval.world_understanding import (
    parse_world_understanding_claims,
    parse_world_understanding_claims_tolerant,
)
from chemworld.materials import (
    normalize_static_material_information_config,
    static_material_information_dossier,
)
from chemworld.physchem.electrochemical_task_contract import (
    ELECTROCHEMICAL_WORKFLOW_STATIC_SINGLE_STAGE,
    normalize_electrochemical_workflow_mode,
)

STATIC_OPTIMIZATION_INTERFACE_VERSION = "chemworld-static-optimization-interface-0.3-s0-dev"
STATIC_OPTIMIZATION_PROMPT_VERSION = "chemworld-static-optimization-prompt-0.3-s0-dev"
STATIC_FINAL_SYNTHESIS_VERSION = "chemworld-static-final-synthesis-0.3-s0-dev"
STATIC_FINAL_SYNTHESIS_SEPARATE_VERSION = (
    "chemworld-static-final-synthesis-0.4-s0-dev"
)
STATIC_FINAL_SYNTHESIS_TOLERANT_DECLARED_VERSION = (
    "chemworld-static-final-synthesis-0.5-s0-dev"
)
STATIC_PREDICTIVE_SYNTHESIS_VERSION = (
    "chemworld-static-predictive-synthesis-0.1-s0-dev"
)
DECLARED_CLAIM_VALIDATION_STRICT = "strict"
DECLARED_CLAIM_VALIDATION_UNSCORED_UNKNOWN = "unscored_unknown_terms"
DECLARED_CLAIM_VALIDATION_POLICIES = frozenset(
    {
        DECLARED_CLAIM_VALIDATION_STRICT,
        DECLARED_CLAIM_VALIDATION_UNSCORED_UNKNOWN,
    }
)

_ELECTROCHEMICAL_CLAIM_CAUSES = (
    "controlled_potential_V",
    "controlled_current_mA",
    "controlled_duration_s",
    "electrolyte_profile",
    "solvent",
    "reagent_amount_mol",
)
_ELECTROCHEMICAL_SINGLE_STAGE_CLAIM_CAUSES = (
    "potential_V",
    "current_mA",
    "duration_s",
    "electrolyte_profile",
    "solvent",
    "reagent_amount_mol",
)
_ELECTROCHEMICAL_CLAIM_EFFECTS = (
    "selective_product_yield",
    "electrochemical_conversion",
    "electrochemical_selectivity",
    "energy_efficiency",
    "faradaic_efficiency",
    "transport_efficiency",
    "ohmic_efficiency",
    "pH_normalized",
    "precipitation_signal",
    "leaderboard_score",
)
_ELECTROCHEMICAL_MECHANISM_TAGS = (
    "nernst_equilibrium",
    "butler_volmer_kinetics",
    "current_magnitude_cap",
    "faraday_charge",
    "double_layer_charging",
    "mass_transfer_limit",
    "ohmic_loss",
    "overpotential_stress",
    "acid_base_activity",
    "precipitation_equilibrium",
    "categorical_medium_effect",
    "inventory_limit",
    "direction_reversal",
)
_CRYSTALLIZATION_CLAIM_CAUSES = (
    "reaction_temperature_K",
    "reaction_duration_s",
    "reagent_amount_mol",
    "stirring_speed_rpm",
    "catalyst",
    "catalyst_amount_mol",
    "solvent",
    "seed_mass_g",
    "crystallization_temperature_K",
    "crystallization_duration_s",
)
_CRYSTALLIZATION_CLAIM_EFFECTS = (
    "reaction_score",
    "yield",
    "selectivity",
    "crystal_yield",
    "crystal_purity",
    "crystal_size",
    "crystal_csd_quality",
    "crystal_fines_fraction",
    "leaderboard_score",
)
_CRYSTALLIZATION_MECHANISM_TAGS = (
    "arrhenius_kinetics",
    "catalyst_activity",
    "categorical_solvent_effect",
    "inventory_limit",
    "vanthoff_solubility",
    "supersaturation",
    "primary_nucleation",
    "seeded_growth",
    "impurity_occlusion",
    "cooling_rate",
    "filtration_recovery",
    "yield_purity_size_tradeoff",
)

SYSTEM_PROMPT = """You are a static scientific optimization agent in ChemWorld.
The world is fixed for the entire campaign. Optimize the task objective using only the
public task contract and public experiment history. Choose one complete experiment and
return exactly one JSON object without exposing private chain-of-thought. When named
physical recipe parameters are supplied, reason and report in those parameters and units;
do not invent or request hidden normalized coordinates.
"""

FINAL_SYNTHESIS_SYSTEM_PROMPT = """You are completing a fixed-world scientific
optimization campaign in ChemWorld. Exploration is finished. Submit one final experimental
method that represents your overall conclusion from the public evidence. The method may
reuse a tested condition, interpolate between tested conditions, or extrapolate within the
declared public search bounds. Return exactly one JSON object without exposing private
chain-of-thought. Ground the recommendation and working scientific explanation in public
experiment indices and evidence IDs. Separate empirical relations from mechanism claims,
and express structured claims only with the declared public vocabulary.
"""

FINAL_SYNTHESIS_SEPARATE_PREDICTIVE_SYSTEM_PROMPT = """You are completing a
fixed-world scientific optimization campaign in ChemWorld. Exploration is finished.
Submit one final experimental method and a working scientific explanation using only the
public campaign evidence. The final method will be committed before a later, separate
predictive diagnostic. Do not include counterfactual_predictions, predictive queries, or
answers to unseen interventions in this response. Return exactly the declared JSON fields
without exposing private chain-of-thought. Ground the recommendation in public experiment
indices and evidence IDs, and use only the declared public mechanism vocabulary.
"""

PREDICTIVE_SYNTHESIS_SYSTEM_PROMPT = """You are completing a held-out predictive
diagnostic for a fixed-world scientific campaign in ChemWorld. A final experimental method
has already been committed and cannot be changed. Use only the supplied public experiment
history to predict the direction of each pre-registered intervention. Return exactly one
JSON object without exposing private chain-of-thought. Do not recommend, revise, or rank
experimental methods; this call is prediction-only.
"""

_PUBLIC_TASK_KEYS = (
    "task_contract_version",
    "task_id",
    "objective",
    "budget",
    "allowed_operations",
    "allowed_instruments",
    "observation_policy",
    "termination_policy",
    "success_metrics",
    "safety_limit",
    "description",
    "contract_hash",
)
_PUBLIC_TERMINAL_KEYS = ("leaderboard_score", "cost", "safety_risk")


def _uses_single_stage_electrochemistry(
    task_info: Mapping[str, Any], workflow_mode: str
) -> bool:
    return (
        task_recipe_kind(dict(task_info)) == "electrochemical"
        and workflow_mode == ELECTROCHEMICAL_WORKFLOW_STATIC_SINGLE_STAGE
    )


def _uses_named_physical_controls(task_info: Mapping[str, Any]) -> bool:
    return task_recipe_kind(dict(task_info)) in {
        "electrochemical",
        "reaction_crystallization",
    }


def _recipe_parameter_schema(
    task_info: Mapping[str, Any], workflow_mode: str
) -> dict[str, dict[str, Any]]:
    if _uses_single_stage_electrochemistry(task_info, workflow_mode):
        return electrochemical_single_stage_parameter_schema()
    if task_recipe_kind(dict(task_info)) == "reaction_crystallization":
        return crystallization_single_stage_parameter_schema()
    return electrochemical_recipe_parameter_schema()


def _recipe_dimension(task_info: Mapping[str, Any], workflow_mode: str) -> int:
    if _uses_single_stage_electrochemistry(task_info, workflow_mode):
        return ELECTROCHEMICAL_SINGLE_STAGE_DIMENSION
    if task_recipe_kind(dict(task_info)) == "reaction_crystallization":
        return CRYSTALLIZATION_SINGLE_STAGE_DIMENSION
    return task_recipe_dimension(dict(task_info))


def _recipe_categorical_coordinates(
    task_info: Mapping[str, Any], workflow_mode: str
) -> tuple[tuple[int, int], ...]:
    if _uses_single_stage_electrochemistry(task_info, workflow_mode):
        return ELECTROCHEMICAL_SINGLE_STAGE_CATEGORICAL_COORDINATES
    if task_recipe_kind(dict(task_info)) == "reaction_crystallization":
        return CRYSTALLIZATION_SINGLE_STAGE_CATEGORICAL_COORDINATES
    return task_recipe_categorical_coordinates(dict(task_info))


def _measurement_slots(
    task_info: Mapping[str, Any], workflow_mode: str
) -> tuple[dict[str, Any], ...]:
    if _uses_single_stage_electrochemistry(task_info, workflow_mode):
        return tuple(copy.deepcopy(item) for item in ELECTROCHEMICAL_SINGLE_STAGE_MEASUREMENT_SLOTS)
    if task_recipe_kind(dict(task_info)) == "reaction_crystallization":
        return tuple(
            copy.deepcopy(item) for item in CRYSTALLIZATION_SINGLE_STAGE_MEASUREMENT_SLOTS
        )
    return scientific_measurement_slots(task_info)


def _parameters_from_vector(
    task_info: Mapping[str, Any], workflow_mode: str, vector: np.ndarray
) -> dict[str, int | float]:
    if _uses_single_stage_electrochemistry(task_info, workflow_mode):
        return electrochemical_single_stage_parameters_from_unit_vector(vector)
    if task_recipe_kind(dict(task_info)) == "reaction_crystallization":
        return crystallization_single_stage_parameters_from_unit_vector(vector)
    return electrochemical_recipe_parameters_from_unit_vector(vector)


def _vector_from_parameters(
    task_info: Mapping[str, Any], workflow_mode: str, payload: object
) -> np.ndarray:
    if _uses_single_stage_electrochemistry(task_info, workflow_mode):
        return electrochemical_single_stage_unit_vector_from_parameters(payload)
    if task_recipe_kind(dict(task_info)) == "reaction_crystallization":
        return crystallization_single_stage_unit_vector_from_parameters(payload)
    return electrochemical_recipe_unit_vector_from_parameters(payload)


def _recipe_from_vector(
    task_info: Mapping[str, Any], workflow_mode: str, vector: np.ndarray
) -> dict[str, Any]:
    if _uses_single_stage_electrochemistry(task_info, workflow_mode):
        return electrochemical_single_stage_recipe_from_unit_vector(task_info, vector)
    if task_recipe_kind(dict(task_info)) == "reaction_crystallization":
        return crystallization_single_stage_recipe_from_unit_vector(task_info, vector)
    return task_recipe_from_unit_vector(dict(task_info), vector)


def _compact(value: Any) -> Any:
    normalized = to_builtin(value)
    if isinstance(normalized, float):
        return round(normalized, 6)
    if isinstance(normalized, dict):
        return {str(key): _compact(item) for key, item in normalized.items()}
    if isinstance(normalized, list):
        return [_compact(item) for item in normalized]
    return copy.deepcopy(normalized)


@dataclass(frozen=True)
class StaticOptimizationPlan:
    """Validated Agent-authored selection for one experiment in a fixed world."""

    experiment_intent: str
    search_vector: tuple[float, ...]
    requested_measurement_slots: tuple[str, ...]
    measurement_objective: str
    expected_effect: str
    uncertainty: float
    recipe_parameters: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        payload = {
            "experiment_intent": self.experiment_intent,
            "search_vector": list(self.search_vector),
            "requested_measurement_slots": list(self.requested_measurement_slots),
            "measurement_objective": self.measurement_objective,
            "expected_effect": self.expected_effect,
            "uncertainty": self.uncertainty,
        }
        if self.recipe_parameters is not None:
            payload["recipe_parameters"] = copy.deepcopy(self.recipe_parameters)
        return payload


@dataclass(frozen=True)
class StaticFinalRecommendation:
    """One terminal scientific recommendation after the exploration budget is exhausted."""

    recommended_search_vector: tuple[float, ...]
    recommended_measurement_slots: tuple[str, ...]
    recommendation_type: str
    source_experiment_indices: tuple[int, ...]
    predicted_score: float
    confidence: float
    method_summary: str
    evidence_refs: tuple[str, ...]
    working_explanation: dict[str, Any]
    remaining_risks: tuple[str, ...]
    recommended_followup: str
    recommended_recipe_parameters: dict[str, Any] | None = None
    counterfactual_predictions: tuple[dict[str, Any], ...] = ()
    schema_version: str = STATIC_FINAL_SYNTHESIS_VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = {
            "schema_version": self.schema_version,
            "recommended_search_vector": list(self.recommended_search_vector),
            "recommended_measurement_slots": list(self.recommended_measurement_slots),
            "recommendation_type": self.recommendation_type,
            "source_experiment_indices": list(self.source_experiment_indices),
            "predicted_score": self.predicted_score,
            "confidence": self.confidence,
            "method_summary": self.method_summary,
            "evidence_refs": list(self.evidence_refs),
            "working_explanation": copy.deepcopy(self.working_explanation),
            "remaining_risks": list(self.remaining_risks),
            "recommended_followup": self.recommended_followup,
        }
        if self.recommended_recipe_parameters is not None:
            payload["recommended_recipe_parameters"] = copy.deepcopy(
                self.recommended_recipe_parameters
            )
        if self.counterfactual_predictions:
            payload["counterfactual_predictions"] = copy.deepcopy(
                list(self.counterfactual_predictions)
            )
        return payload

    def execution_plan(self) -> StaticOptimizationPlan:
        return StaticOptimizationPlan(
            experiment_intent="blind validation of the final campaign recommendation",
            search_vector=self.recommended_search_vector,
            requested_measurement_slots=self.recommended_measurement_slots,
            measurement_objective="validate the submitted method under independent noise",
            expected_effect=self.method_summary,
            uncertainty=1.0 - self.confidence,
            recipe_parameters=(
                None
                if self.recommended_recipe_parameters is None
                else copy.deepcopy(self.recommended_recipe_parameters)
            ),
        )


class StaticOptimizationContextBuilder:
    """Public context with no mechanism candidates or hidden-world fields."""

    def __init__(
        self,
        task_info: Mapping[str, Any],
        *,
        history_limit: int = 8,
        total_experiments: int | None = None,
        final_synthesis_after_exploration: bool = False,
        include_task_operation_budget: bool = True,
        predictive_world_understanding_enabled: bool = False,
        material_information: Mapping[str, Any] | None = None,
        electrochemical_material_family_id: str | None = None,
        crystallization_material_family_id: str | None = None,
        scoring_contract: Mapping[str, Any] | None = None,
        electrochemical_workflow_mode: str = (
            ELECTROCHEMICAL_WORKFLOW_STATIC_SINGLE_STAGE
        ),
    ) -> None:
        if history_limit <= 0:
            raise ValueError("history_limit must be positive")
        self.task_info = dict(task_info)
        self.history_limit = int(history_limit)
        self.total_experiments = (
            int(total_experiments) if total_experiments is not None else None
        )
        if self.total_experiments is not None and self.total_experiments <= 0:
            raise ValueError("total_experiments must be positive")
        self.final_synthesis_after_exploration = bool(
            final_synthesis_after_exploration
        )
        self.include_task_operation_budget = bool(include_task_operation_budget)
        self.predictive_world_understanding_enabled = bool(
            predictive_world_understanding_enabled
        )
        active_material_family_id = (
            crystallization_material_family_id
            if str(self.task_info.get("task_id", "")) == "reaction-to-crystallization"
            else electrochemical_material_family_id
        )
        self.material_information_config = normalize_static_material_information_config(
            material_information,
            task_ids=(str(self.task_info.get("task_id", "")),),
            material_family_id=active_material_family_id,
        )
        self.material_information_condition = str(
            self.material_information_config["mode"]
        )
        self.material_information = static_material_information_dossier(
            self.material_information_config,
            task_id=str(self.task_info.get("task_id", "")),
            material_family_id=active_material_family_id,
        )
        self.material_information_sha256 = (
            canonical_sha256(self.material_information)
            if self.material_information is not None
            else None
        )
        self.scoring_contract = (
            None if scoring_contract is None else copy.deepcopy(dict(scoring_contract))
        )
        self.electrochemical_workflow_mode = normalize_electrochemical_workflow_mode(
            electrochemical_workflow_mode
        )
        self.measurement_slots = _measurement_slots(
            self.task_info, self.electrochemical_workflow_mode
        )

    def build(
        self,
        experiment_history: Sequence[Mapping[str, Any]],
        *,
        decision_stage: str = "experiment_design",
        include_prediction_queries: bool | None = None,
    ) -> dict[str, Any]:
        if decision_stage not in {"experiment_design", "final_synthesis"}:
            raise ValueError("unsupported static optimization decision stage")
        if include_prediction_queries is None:
            include_prediction_queries = (
                self.predictive_world_understanding_enabled
                and decision_stage == "final_synthesis"
            )
        if include_prediction_queries and decision_stage != "final_synthesis":
            raise ValueError("prediction queries are only valid after exploration")
        selected = self._select_history(experiment_history)
        history = [self._compact_history_record(item) for item in selected]
        evidence_catalog = [
            str(entry["evidence_id"])
            for record in history
            for entry in record["measurement_evidence"]
        ]
        optimization_contract: dict[str, Any] = {
            "world_policy": "static_for_entire_campaign",
            "objective": "maximize_fixed_task_success_metrics",
            "feedback_policy": "public_processed_estimate_uncertainty_reward",
            "decision_stage": decision_stage,
        }
        if self.scoring_contract is not None:
            optimization_contract["scoring_contract"] = copy.deepcopy(
                self.scoring_contract
            )
        if self.total_experiments is not None:
            completed = len(experiment_history)
            current = min(completed + 1, self.total_experiments)
            remaining_after_current = max(self.total_experiments - current, 0)
            if decision_stage == "final_synthesis":
                current = self.total_experiments
                remaining_after_current = 0
            optimization_contract["scientific_campaign_budget"] = {
                "total_exploration_experiments": self.total_experiments,
                "completed_experiments": completed,
                "current_experiment_number": current,
                "remaining_experiments_after_current": remaining_after_current,
                "final_synthesis_after_exploration": (
                    self.final_synthesis_after_exploration
                ),
                "validation_feedback_returned_to_agent": False,
            }
        experiment_interface: dict[str, Any] = {
            "decision_scope": "complete_experiment",
            "recipe_space_version": (
                ELECTROCHEMICAL_SINGLE_STAGE_RECIPE_VERSION
                if _uses_single_stage_electrochemistry(
                    self.task_info, self.electrochemical_workflow_mode
                )
                else CRYSTALLIZATION_SINGLE_STAGE_RECIPE_VERSION
                if task_recipe_kind(self.task_info) == "reaction_crystallization"
                else TASK_RECIPE_SPACE_VERSION
            ),
            "recipe_space_kind": task_recipe_kind(self.task_info),
            "diagnostic_measurement_slots": [
                copy.deepcopy(item) for item in self.measurement_slots
            ],
            "closeout": [
                {"operation": "terminate"},
                {"operation": "measure", "instrument": "final_assay"},
            ],
        }
        recipe_kind = task_recipe_kind(self.task_info)
        if _uses_named_physical_controls(self.task_info):
            experiment_interface.update(
                {
                    "parameterization": "named_physical_controls",
                    "recipe_parameter_schema": _recipe_parameter_schema(
                        self.task_info, self.electrochemical_workflow_mode
                    ),
                    "internal_unit_vector_visible_to_agent": False,
                    "world_understanding_claim_contract": {
                        "cause_variables": list(
                            _ELECTROCHEMICAL_SINGLE_STAGE_CLAIM_CAUSES
                            if _uses_single_stage_electrochemistry(
                                self.task_info, self.electrochemical_workflow_mode
                            )
                            else _ELECTROCHEMICAL_CLAIM_CAUSES
                            if recipe_kind == "electrochemical"
                            else _CRYSTALLIZATION_CLAIM_CAUSES
                        ),
                        "effect_variables": list(
                            _ELECTROCHEMICAL_CLAIM_EFFECTS
                            if recipe_kind == "electrochemical"
                            else _CRYSTALLIZATION_CLAIM_EFFECTS
                        ),
                        "relations": [
                            "positive",
                            "negative",
                            "nonmonotonic",
                            "conditional",
                            "no_direct_effect",
                        ],
                        "mechanism_tags": list(
                            _ELECTROCHEMICAL_MECHANISM_TAGS
                            if recipe_kind == "electrochemical"
                            else _CRYSTALLIZATION_MECHANISM_TAGS
                        ),
                        "claim_target": (
                            "observable causal equivalence classes; do not guess hidden species IDs"
                        ),
                    },
                }
            )
            if recipe_kind == "electrochemical":
                experiment_interface["electrochemical_workflow_mode"] = (
                    self.electrochemical_workflow_mode
                )
            if self.material_information is not None:
                experiment_interface["material_information"] = copy.deepcopy(
                    self.material_information
                )
        else:
            experiment_interface.update(
                {
                    "parameterization": "unit_vector",
                    "search_vector_dimension": _recipe_dimension(
                        self.task_info, self.electrochemical_workflow_mode
                    ),
                    "search_vector_bounds": [0.0, 1.0],
                    "categorical_coordinates": [
                        {"coordinate": coordinate, "category_count": count}
                        for coordinate, count in _recipe_categorical_coordinates(
                            self.task_info, self.electrochemical_workflow_mode
                        )
                    ],
                }
            )
        payload = {
            "schema_version": STATIC_OPTIMIZATION_INTERFACE_VERSION,
            "optimization_contract": optimization_contract,
            "task": {
                key: copy.deepcopy(self.task_info[key])
                for key in _PUBLIC_TASK_KEYS
                if key in self.task_info
                and (key != "budget" or self.include_task_operation_budget)
            },
            "experiment_interface": experiment_interface,
            "history_window": {
                "selection_policy": "oldest_reference_half_plus_most_recent_half",
                "total_experiment_count": len(experiment_history),
                "included_experiment_indices": [record["experiment_index"] for record in history],
            },
            "experiment_history": history,
            "evidence_catalog": evidence_catalog,
        }
        if (
            decision_stage == "final_synthesis"
            and include_prediction_queries
        ):
            queries = (
                build_electrochemical_prediction_queries(
                    experiment_history,
                    electrochemical_workflow_mode=self.electrochemical_workflow_mode,
                )
                if recipe_kind == "electrochemical"
                else build_crystallization_prediction_queries(experiment_history)
            )
            payload["held_out_prediction_queries"] = [
                query.to_public_dict() for query in queries
            ]
            optimization_contract["predictive_validation"] = {
                "query_count": len(queries),
                "executed_before_prediction": False,
                "feedback_returned_to_agent": False,
                "one_factor_interventions": True,
            }
        return payload

    def _select_history(self, history: Sequence[Mapping[str, Any]]) -> list[Mapping[str, Any]]:
        records = list(history)
        if len(records) <= self.history_limit:
            return records
        reference_count = max(self.history_limit // 2, 1)
        return records[:reference_count] + records[-(self.history_limit - reference_count) :]

    def _compact_history_record(self, item: Mapping[str, Any]) -> dict[str, Any]:
        plan = item.get("plan")
        evidence = item.get("measurement_evidence")
        terminal = item.get("terminal_summary")
        if not isinstance(plan, Mapping):
            raise ValueError("static history record is missing plan")
        if not isinstance(evidence, list) or not all(
            isinstance(entry, Mapping) for entry in evidence
        ):
            raise ValueError("static history measurement_evidence must be a list")
        if not isinstance(terminal, Mapping):
            raise ValueError("static history record is missing terminal_summary")
        compact_plan = {
            key: _compact(plan[key])
            for key in (
                "requested_measurement_slots",
                "measurement_objective",
                "expected_effect",
                "uncertainty",
            )
            if key in plan
        }
        if _uses_named_physical_controls(self.task_info):
            vector = np.asarray(plan["search_vector"], dtype=float)
            compact_plan["recipe_parameters"] = _compact(
                plan.get(
                    "recipe_parameters",
                    _parameters_from_vector(
                        self.task_info,
                        self.electrochemical_workflow_mode,
                        vector,
                    ),
                )
            )
        else:
            compact_plan["search_vector"] = _compact(plan["search_vector"])
        return {
            "experiment_index": int(item["experiment_index"]),
            "plan": compact_plan,
            "measurement_evidence": [
                {
                    key: _compact(entry[key])
                    for key in ("evidence_id", "processed_estimate", "uncertainty", "reward")
                    if key in entry
                }
                for entry in evidence
            ],
            "terminal_summary": {
                key: _compact(terminal[key]) for key in _PUBLIC_TERMINAL_KEYS if key in terminal
            },
        }


class StaticOptimizationValidator:
    def __init__(
        self,
        task_info: Mapping[str, Any],
        *,
        electrochemical_workflow_mode: str = (
            ELECTROCHEMICAL_WORKFLOW_STATIC_SINGLE_STAGE
        ),
    ) -> None:
        self.task_info = dict(task_info)
        self.recipe_kind = task_recipe_kind(self.task_info)
        self.electrochemical_workflow_mode = normalize_electrochemical_workflow_mode(
            electrochemical_workflow_mode
        )
        self.dimension = _recipe_dimension(
            self.task_info, self.electrochemical_workflow_mode
        )
        self.measurement_slot_ids = tuple(
            str(item["slot_id"])
            for item in _measurement_slots(
                self.task_info, self.electrochemical_workflow_mode
            )
        )

    @staticmethod
    def _text(value: Any, *, field: str, maximum: int) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ScientificPlanValidationError(
                f"{field} must be a non-empty string",
                field_path=field,
                constraint="non_empty_string",
                observed=0 if isinstance(value, str) else type(value).__name__,
                limit=1,
            )
        normalized = value.strip()
        if len(normalized) > maximum:
            raise ScientificPlanValidationError(
                f"{field} exceeds its character limit",
                field_path=field,
                constraint="max_characters",
                observed=len(normalized),
                limit=maximum,
            )
        return normalized

    def validate(self, payload: Any) -> StaticOptimizationPlan:
        if not isinstance(payload, Mapping):
            raise ScientificPlanValidationError(
                "static optimization response must be an object",
                field_path="static_optimization_response",
                constraint="object",
                observed=type(payload).__name__,
            )
        required = {
            "experiment_intent",
            "requested_measurement_slots",
            "measurement_objective",
            "expected_effect",
            "uncertainty",
        }
        required.add(
            "recipe_parameters"
            if _uses_named_physical_controls(self.task_info)
            else "search_vector"
        )
        if set(payload) != required:
            raise ScientificPlanValidationError(
                "static optimization response fields do not match its contract",
                field_path="static_optimization_response",
                constraint="exact_declared_fields",
                observed=len(set(payload) - required),
                limit=0,
            )
        normalized_recipe_parameters: dict[str, Any] | None = None
        if _uses_named_physical_controls(self.task_info):
            try:
                encoded = _vector_from_parameters(
                    self.task_info,
                    self.electrochemical_workflow_mode,
                    payload["recipe_parameters"],
                )
            except ValueError as error:
                raise ScientificPlanValidationError(
                    str(error),
                    field_path="recipe_parameters",
                    constraint="physical_recipe_contract",
                ) from error
            normalized_vector = [float(value) for value in encoded]
            normalized_recipe_parameters = (
                _parameters_from_vector(
                    self.task_info,
                    self.electrochemical_workflow_mode,
                    encoded,
                )
            )
        else:
            vector = payload["search_vector"]
            if not isinstance(vector, list) or len(vector) != self.dimension:
                raise ScientificPlanValidationError(
                    "search_vector has the wrong dimension",
                    field_path="search_vector",
                    constraint="exact_items",
                    observed=(
                        len(vector) if isinstance(vector, list) else type(vector).__name__
                    ),
                    limit=self.dimension,
                )
            normalized_vector = []
            for value in vector:
                if isinstance(value, bool) or not isinstance(value, int | float):
                    raise ScientificPlanValidationError(
                        "search_vector values must be numeric",
                        field_path="search_vector",
                        constraint="numeric_items",
                        observed=type(value).__name__,
                    )
                coordinate = float(value)
                if not math.isfinite(coordinate) or not 0.0 <= coordinate <= 1.0:
                    raise ScientificPlanValidationError(
                        "search_vector values must be finite and in [0, 1]",
                        field_path="search_vector",
                        constraint="finite_unit_interval_items",
                    )
                normalized_vector.append(coordinate)
        requested = payload["requested_measurement_slots"]
        if not isinstance(requested, list) or not all(isinstance(item, str) for item in requested):
            raise ScientificPlanValidationError(
                "requested_measurement_slots must be a string list",
                field_path="requested_measurement_slots",
                constraint="string_list",
                observed=type(requested).__name__,
            )
        normalized_requested = [str(item) for item in requested]
        if len(set(normalized_requested)) != len(normalized_requested):
            raise ScientificPlanValidationError(
                "requested_measurement_slots must be unique",
                field_path="requested_measurement_slots",
                constraint="unique_items",
                observed=len(normalized_requested),
                limit=len(set(normalized_requested)),
            )
        if not set(normalized_requested).issubset(self.measurement_slot_ids):
            raise ScientificPlanValidationError(
                "requested_measurement_slots contains an unknown slot",
                field_path="requested_measurement_slots",
                constraint="known_measurement_slot_ids",
            )
        normalized_requested.sort(key=self.measurement_slot_ids.index)
        uncertainty = payload["uncertainty"]
        if isinstance(uncertainty, bool) or not isinstance(uncertainty, int | float):
            raise ScientificPlanValidationError(
                "uncertainty must be numeric",
                field_path="uncertainty",
                constraint="numeric",
                observed=type(uncertainty).__name__,
            )
        uncertainty_float = float(uncertainty)
        if not math.isfinite(uncertainty_float) or not 0.0 <= uncertainty_float <= 1.0:
            raise ScientificPlanValidationError(
                "uncertainty must be finite and in [0, 1]",
                field_path="uncertainty",
                constraint="finite_unit_interval",
            )
        return StaticOptimizationPlan(
            experiment_intent=self._text(
                payload["experiment_intent"], field="experiment_intent", maximum=1000
            ),
            search_vector=tuple(normalized_vector),
            requested_measurement_slots=tuple(normalized_requested),
            measurement_objective=self._text(
                payload["measurement_objective"],
                field="measurement_objective",
                maximum=1000,
            ),
            expected_effect=self._text(
                payload["expected_effect"], field="expected_effect", maximum=1200
            ),
            uncertainty=uncertainty_float,
            recipe_parameters=normalized_recipe_parameters,
        )


class StaticFinalRecommendationValidator:
    _RECOMMENDATION_TYPES: ClassVar[frozenset[str]] = frozenset(
        {"tested", "interpolated", "extrapolated"}
    )

    def __init__(
        self,
        task_info: Mapping[str, Any],
        *,
        predictive_world_understanding_enabled: bool = False,
        final_synthesis_version: str = STATIC_FINAL_SYNTHESIS_VERSION,
        declared_claim_validation_policy: str = DECLARED_CLAIM_VALIDATION_STRICT,
        electrochemical_workflow_mode: str = (
            ELECTROCHEMICAL_WORKFLOW_STATIC_SINGLE_STAGE
        ),
    ) -> None:
        self.electrochemical_workflow_mode = normalize_electrochemical_workflow_mode(
            electrochemical_workflow_mode
        )
        self.plan_validator = StaticOptimizationValidator(
            task_info,
            electrochemical_workflow_mode=self.electrochemical_workflow_mode,
        )
        self.recipe_kind = self.plan_validator.recipe_kind
        self.predictive_world_understanding_enabled = bool(
            predictive_world_understanding_enabled
        )
        self.final_synthesis_version = str(final_synthesis_version)
        if declared_claim_validation_policy not in DECLARED_CLAIM_VALIDATION_POLICIES:
            raise ValueError("unknown Declared claim validation policy")
        self.declared_claim_validation_policy = declared_claim_validation_policy

    @staticmethod
    def _string_list(value: Any, *, field: str, maximum_items: int = 16) -> list[str]:
        if not isinstance(value, list) or not all(
            isinstance(item, str) and item.strip() for item in value
        ):
            raise ScientificPlanValidationError(
                f"{field} must be a list of non-empty strings",
                field_path=field,
                constraint="non_empty_string_list",
            )
        if len(value) > maximum_items:
            raise ScientificPlanValidationError(
                f"{field} exceeds its item limit",
                field_path=field,
                constraint="max_items",
                observed=len(value),
                limit=maximum_items,
            )
        return [str(item).strip() for item in value]

    @staticmethod
    def _probability(value: Any, *, field: str) -> float:
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise ScientificPlanValidationError(
                f"{field} must be numeric",
                field_path=field,
                constraint="numeric",
            )
        normalized = float(value)
        if not math.isfinite(normalized) or not 0.0 <= normalized <= 1.0:
            raise ScientificPlanValidationError(
                f"{field} must be in [0, 1]",
                field_path=field,
                constraint="finite_unit_interval",
            )
        return normalized

    def validate(
        self,
        payload: Any,
        *,
        history: Sequence[Mapping[str, Any]],
        evidence_catalog: Sequence[str],
        prediction_queries: Sequence[
            ElectrochemicalPredictionQuery | CrystallizationPredictionQuery
        ] = (),
    ) -> StaticFinalRecommendation:
        if not isinstance(payload, Mapping):
            raise ScientificPlanValidationError(
                "final synthesis response must be an object",
                field_path="final_synthesis_response",
                constraint="object",
            )
        required = {
            "schema_version",
            "recommended_measurement_slots",
            "recommendation_type",
            "source_experiment_indices",
            "predicted_score",
            "confidence",
            "method_summary",
            "evidence_refs",
            "working_explanation",
            "remaining_risks",
            "recommended_followup",
        }
        required.add(
            "recommended_recipe_parameters"
            if _uses_named_physical_controls(self.plan_validator.task_info)
            else "recommended_search_vector"
        )
        if prediction_queries:
            required.add("counterfactual_predictions")
        missing = required - set(payload)
        if missing:
            raise ScientificPlanValidationError(
                "final synthesis response is missing required fields",
                field_path="final_synthesis_response",
                constraint="required_fields_present",
                observed=",".join(sorted(str(item) for item in missing)),
            )
        if set(payload) != required:
            raise ScientificPlanValidationError(
                "final synthesis response fields do not match its contract",
                field_path="final_synthesis_response",
                constraint="exact_declared_fields",
                observed=",".join(sorted(str(item) for item in set(payload) - required)),
            )
        if payload["schema_version"] != self.final_synthesis_version:
            raise ScientificPlanValidationError(
                "final synthesis schema_version does not match the frozen contract",
                field_path="schema_version",
                constraint="exact_schema_version",
                observed=str(payload["schema_version"]),
                limit=self.final_synthesis_version,
            )
        confidence = self._probability(payload["confidence"], field="confidence")
        plan_payload = {
                "experiment_intent": "validate the final recommendation",
                "requested_measurement_slots": payload[
                    "recommended_measurement_slots"
                ],
                "measurement_objective": "blind independent validation",
                "expected_effect": "evaluate the submitted fixed-world method",
                "uncertainty": 1.0 - confidence,
            }
        if _uses_named_physical_controls(self.plan_validator.task_info):
            plan_payload["recipe_parameters"] = payload[
                "recommended_recipe_parameters"
            ]
        else:
            plan_payload["search_vector"] = payload["recommended_search_vector"]
        plan = self.plan_validator.validate(plan_payload)
        recommendation_type = str(payload["recommendation_type"])
        if recommendation_type not in self._RECOMMENDATION_TYPES:
            raise ScientificPlanValidationError(
                "recommendation_type is unsupported",
                field_path="recommendation_type",
                constraint="declared_enum",
            )
        raw_indices = payload["source_experiment_indices"]
        if not isinstance(raw_indices, list) or not raw_indices or not all(
            isinstance(item, int) and not isinstance(item, bool) for item in raw_indices
        ):
            raise ScientificPlanValidationError(
                "source_experiment_indices must be a non-empty integer list",
                field_path="source_experiment_indices",
                constraint="non_empty_integer_list",
            )
        source_indices = tuple(int(item) for item in raw_indices)
        available_indices = {int(item["experiment_index"]) for item in history}
        if not set(source_indices).issubset(available_indices):
            raise ScientificPlanValidationError(
                "source_experiment_indices contains an unknown experiment",
                field_path="source_experiment_indices",
                constraint="known_experiment_indices",
            )
        if recommendation_type == "tested":
            matching_source_exists = any(
                list(plan.search_vector)
                == [float(value) for value in item["plan"]["search_vector"]]
                and list(plan.requested_measurement_slots)
                == [
                    str(value)
                    for value in item["plan"]["requested_measurement_slots"]
                ]
                for item in history
                if int(item["experiment_index"]) in source_indices
            )
            if not matching_source_exists:
                raise ScientificPlanValidationError(
                    "tested recommendation must reproduce at least one cited source method",
                    field_path=(
                        "recommended_recipe_parameters"
                        if _uses_named_physical_controls(self.plan_validator.task_info)
                        else "recommended_search_vector"
                    ),
                    constraint="matches_tested_source",
                )
        evidence_refs = self._string_list(
            payload["evidence_refs"], field="evidence_refs"
        )
        if not set(evidence_refs).issubset(set(evidence_catalog)):
            raise ScientificPlanValidationError(
                "evidence_refs contains an unknown evidence ID",
                field_path="evidence_refs",
                constraint="known_evidence_ids",
            )
        explanation = payload["working_explanation"]
        explanation_fields = {
            "empirical_relationships",
            "mechanistic_hypothesis",
            "supporting_evidence_ids",
            "contradicting_evidence_ids",
            "uncertainty",
        }
        if _uses_named_physical_controls(self.plan_validator.task_info):
            explanation_fields.add("structured_claims")
        missing_explanation_fields = (
            explanation_fields - set(explanation)
            if isinstance(explanation, Mapping)
            else explanation_fields
        )
        if not isinstance(explanation, Mapping) or missing_explanation_fields:
            raise ScientificPlanValidationError(
                "working_explanation is missing required fields",
                field_path="working_explanation",
                constraint="required_fields_present",
                observed=",".join(sorted(missing_explanation_fields)),
            )
        if set(explanation) != explanation_fields:
            raise ScientificPlanValidationError(
                "working_explanation fields do not match its contract",
                field_path="working_explanation",
                constraint="exact_declared_fields",
                observed=",".join(
                    sorted(str(item) for item in set(explanation) - explanation_fields)
                ),
            )
        supporting = self._string_list(
            explanation["supporting_evidence_ids"],
            field="working_explanation.supporting_evidence_ids",
        )
        contradicting = self._string_list(
            explanation["contradicting_evidence_ids"],
            field="working_explanation.contradicting_evidence_ids",
        )
        if not set(supporting + contradicting).issubset(set(evidence_catalog)):
            raise ScientificPlanValidationError(
                "working explanation cites an unknown evidence ID",
                field_path="working_explanation",
                constraint="known_evidence_ids",
            )
        normalized_explanation = {
            "empirical_relationships": self._string_list(
                explanation["empirical_relationships"],
                field="working_explanation.empirical_relationships",
            ),
            "mechanistic_hypothesis": StaticOptimizationValidator._text(
                explanation["mechanistic_hypothesis"],
                field="working_explanation.mechanistic_hypothesis",
                maximum=1200,
            ),
            "supporting_evidence_ids": supporting,
            "contradicting_evidence_ids": contradicting,
            "uncertainty": self._probability(
                explanation["uncertainty"],
                field="working_explanation.uncertainty",
            ),
        }
        if _uses_named_physical_controls(self.plan_validator.task_info):
            claim_arguments = {
                "evidence_catalog": evidence_catalog,
                "allowed_cause_variables": (
                    _ELECTROCHEMICAL_SINGLE_STAGE_CLAIM_CAUSES
                    if self.electrochemical_workflow_mode
                    == ELECTROCHEMICAL_WORKFLOW_STATIC_SINGLE_STAGE
                    and self.recipe_kind == "electrochemical"
                    else _ELECTROCHEMICAL_CLAIM_CAUSES
                    if self.recipe_kind == "electrochemical"
                    else _CRYSTALLIZATION_CLAIM_CAUSES
                ),
                "allowed_effect_variables": (
                    _ELECTROCHEMICAL_CLAIM_EFFECTS
                    if self.recipe_kind == "electrochemical"
                    else _CRYSTALLIZATION_CLAIM_EFFECTS
                ),
                "allowed_mechanism_tags": (
                    _ELECTROCHEMICAL_MECHANISM_TAGS
                    if self.recipe_kind == "electrochemical"
                    else _CRYSTALLIZATION_MECHANISM_TAGS
                ),
            }
            if (
                self.declared_claim_validation_policy
                == DECLARED_CLAIM_VALIDATION_UNSCORED_UNKNOWN
            ):
                claims, claim_diagnostics = (
                    parse_world_understanding_claims_tolerant(
                        explanation["structured_claims"],
                        **claim_arguments,
                    )
                )
                normalized_explanation["structured_claim_diagnostics"] = (
                    claim_diagnostics
                )
            else:
                try:
                    claims = parse_world_understanding_claims(
                        explanation["structured_claims"],
                        **claim_arguments,
                    )
                except ValueError as error:
                    raise ScientificPlanValidationError(
                        str(error),
                        field_path="working_explanation.structured_claims",
                        constraint="world_understanding_claim_contract",
                    ) from error
            normalized_explanation["structured_claims"] = [
                claim.to_dict() for claim in claims
            ]
        counterfactual_predictions: tuple[dict[str, Any], ...] = ()
        if prediction_queries:
            try:
                parsed_predictions = parse_counterfactual_predictions(
                    payload["counterfactual_predictions"],
                    queries=prediction_queries,
                )
            except ValueError as error:
                raise ScientificPlanValidationError(
                    str(error),
                    field_path="counterfactual_predictions",
                    constraint="frozen_predictive_contract",
                ) from error
            counterfactual_predictions = tuple(
                prediction.to_dict() for prediction in parsed_predictions
            )
        return StaticFinalRecommendation(
            recommended_search_vector=plan.search_vector,
            recommended_measurement_slots=plan.requested_measurement_slots,
            recommendation_type=recommendation_type,
            source_experiment_indices=source_indices,
            predicted_score=self._probability(
                payload["predicted_score"], field="predicted_score"
            ),
            confidence=confidence,
            method_summary=StaticOptimizationValidator._text(
                payload["method_summary"], field="method_summary", maximum=1000
            ),
            evidence_refs=tuple(evidence_refs),
            working_explanation=normalized_explanation,
            remaining_risks=tuple(
                self._string_list(payload["remaining_risks"], field="remaining_risks")
            ),
            recommended_followup=StaticOptimizationValidator._text(
                payload["recommended_followup"],
                field="recommended_followup",
                maximum=1000,
            ),
            recommended_recipe_parameters=plan.recipe_parameters,
            counterfactual_predictions=counterfactual_predictions,
            schema_version=self.final_synthesis_version,
        )


class StaticOptimizationAgent:
    name = "static_optimization_agent"

    def __init__(
        self,
        client: JsonPlannerClientLike,
        *,
        role_id: str,
        response_max_tokens: int,
        history_limit: int,
        prompt_token_estimate_cap: int,
        experiment_horizon: int | None = None,
        horizon_visible: bool = False,
        final_synthesis_enabled: bool = False,
        final_synthesis_prompt_token_estimate_cap: int | None = None,
        predictive_synthesis_prompt_token_estimate_cap: int | None = None,
        include_task_operation_budget: bool = True,
        predictive_world_understanding_enabled: bool = False,
        predictive_queries_in_final_synthesis: bool = True,
        declared_claim_validation_policy: str = DECLARED_CLAIM_VALIDATION_STRICT,
        material_information: Mapping[str, Any] | None = None,
        electrochemical_material_family_id: str | None = None,
        crystallization_material_family_id: str | None = None,
        scoring_contract: Mapping[str, Any] | None = None,
        electrochemical_workflow_mode: str = (
            ELECTROCHEMICAL_WORKFLOW_STATIC_SINGLE_STAGE
        ),
    ) -> None:
        self.client = client
        self.role_id = role_id
        self.response_max_tokens = int(response_max_tokens)
        self.history_limit = int(history_limit)
        self.prompt_token_estimate_cap = int(prompt_token_estimate_cap)
        self.experiment_horizon = (
            int(experiment_horizon) if experiment_horizon is not None else None
        )
        self.horizon_visible = bool(horizon_visible)
        self.final_synthesis_enabled = bool(final_synthesis_enabled)
        self.final_synthesis_prompt_token_estimate_cap = int(
            final_synthesis_prompt_token_estimate_cap
            if final_synthesis_prompt_token_estimate_cap is not None
            else prompt_token_estimate_cap
        )
        self.predictive_synthesis_prompt_token_estimate_cap = int(
            predictive_synthesis_prompt_token_estimate_cap
            if predictive_synthesis_prompt_token_estimate_cap is not None
            else self.final_synthesis_prompt_token_estimate_cap
        )
        self.include_task_operation_budget = bool(include_task_operation_budget)
        self.predictive_world_understanding_enabled = bool(
            predictive_world_understanding_enabled
        )
        self.predictive_queries_in_final_synthesis = bool(
            predictive_queries_in_final_synthesis
        )
        if declared_claim_validation_policy not in DECLARED_CLAIM_VALIDATION_POLICIES:
            raise ValueError("unknown Declared claim validation policy")
        self.declared_claim_validation_policy = declared_claim_validation_policy
        if (
            self.declared_claim_validation_policy
            == DECLARED_CLAIM_VALIDATION_UNSCORED_UNKNOWN
        ):
            self.final_synthesis_version = (
                STATIC_FINAL_SYNTHESIS_TOLERANT_DECLARED_VERSION
            )
        else:
            self.final_synthesis_version = (
                STATIC_FINAL_SYNTHESIS_SEPARATE_VERSION
                if self.predictive_world_understanding_enabled
                and not self.predictive_queries_in_final_synthesis
                else STATIC_FINAL_SYNTHESIS_VERSION
            )
        self.material_information_config = (
            None
            if material_information is None
            else copy.deepcopy(dict(material_information))
        )
        self.electrochemical_material_family_id = electrochemical_material_family_id
        self.crystallization_material_family_id = crystallization_material_family_id
        self.scoring_contract = (
            None if scoring_contract is None else copy.deepcopy(dict(scoring_contract))
        )
        self.electrochemical_workflow_mode = normalize_electrochemical_workflow_mode(
            electrochemical_workflow_mode
        )
        self.resource_ledger = ResourceLedger()
        self._last_audit: dict[str, Any] | None = None
        self._last_synthesis_audit: dict[str, Any] | None = None
        self._last_predictive_audit: dict[str, Any] | None = None

    def reset(self, task_info: Mapping[str, Any], seed: int) -> None:
        self.task_info = dict(task_info)
        self.seed = int(seed)
        if self.predictive_world_understanding_enabled and task_recipe_kind(
            self.task_info
        ) not in {"electrochemical", "reaction_crystallization"}:
            raise ValueError(
                "predictive world understanding is frozen only for the two confirmatory tasks"
            )
        self.context_builder = StaticOptimizationContextBuilder(
            self.task_info,
            history_limit=self.history_limit,
            total_experiments=(
                self.experiment_horizon if self.horizon_visible else None
            ),
            final_synthesis_after_exploration=self.final_synthesis_enabled,
            include_task_operation_budget=self.include_task_operation_budget,
            predictive_world_understanding_enabled=(
                self.predictive_world_understanding_enabled
            ),
            material_information=self.material_information_config,
            electrochemical_material_family_id=(
                self.electrochemical_material_family_id
            ),
            crystallization_material_family_id=(
                self.crystallization_material_family_id
            ),
            scoring_contract=self.scoring_contract,
            electrochemical_workflow_mode=self.electrochemical_workflow_mode,
        )
        self.validator = StaticOptimizationValidator(
            self.task_info,
            electrochemical_workflow_mode=self.electrochemical_workflow_mode,
        )
        self.final_validator = StaticFinalRecommendationValidator(
            self.task_info,
            predictive_world_understanding_enabled=(
                self.predictive_world_understanding_enabled
            ),
            final_synthesis_version=self.final_synthesis_version,
            declared_claim_validation_policy=(
                self.declared_claim_validation_policy
            ),
            electrochemical_workflow_mode=self.electrochemical_workflow_mode,
        )
        self.resource_ledger.reset()
        self._last_audit = None
        self._last_synthesis_audit = None
        self._last_predictive_audit = None

    def public_context(self, history: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
        if not hasattr(self, "context_builder"):
            raise RuntimeError("StaticOptimizationAgent must be reset before use")
        return self.context_builder.build(history)

    def final_synthesis_context(
        self,
        history: Sequence[Mapping[str, Any]],
        *,
        include_prediction_queries: bool | None = None,
    ) -> dict[str, Any]:
        if not self.final_synthesis_enabled:
            raise RuntimeError("final synthesis is not enabled for this S0 method")
        if self.experiment_horizon is not None and len(history) != self.experiment_horizon:
            raise RuntimeError("final synthesis requires the complete exploration history")
        if include_prediction_queries is None:
            include_prediction_queries = (
                self.predictive_world_understanding_enabled
                and self.predictive_queries_in_final_synthesis
            )
        return self.context_builder.build(
            history,
            decision_stage="final_synthesis",
            include_prediction_queries=include_prediction_queries,
        )

    def plan_next(self, history: Sequence[Mapping[str, Any]]) -> StaticOptimizationPlan:
        context = self.public_context(history)
        context_sha256 = canonical_sha256(context)
        recipe_field = (
            {
                "recipe_parameters": {
                    key: copy.deepcopy(value)
                    for key, value in _recipe_parameter_schema(
                        self.task_info, self.electrochemical_workflow_mode
                    ).items()
                }
            }
            if _uses_named_physical_controls(self.task_info)
            else {
                "search_vector": [
                    "number in [0,1]"
                    for _ in range(
                        _recipe_dimension(
                            self.task_info, self.electrochemical_workflow_mode
                        )
                    )
                ]
            }
        )
        prompt_payload = {
            "schema_version": STATIC_OPTIMIZATION_PROMPT_VERSION,
            "public_experiment_context": context,
            "public_context_sha256": context_sha256,
            "required_json_shape": {
                "experiment_intent": "string",
                **recipe_field,
                "requested_measurement_slots": ["public diagnostic slot ID"],
                "measurement_objective": "string",
                "expected_effect": "string",
                "uncertainty": "number in [0,1]",
            },
        }
        prompt = json.dumps(
            prompt_payload,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        prompt_estimated_tokens = estimate_prompt_tokens(prompt)
        if prompt_estimated_tokens > self.prompt_token_estimate_cap:
            raise PromptBudgetExceededError(
                f"static optimization prompt estimate {prompt_estimated_tokens} exceeds cap "
                f"{self.prompt_token_estimate_cap}"
            )
        try:
            completion = self.client.complete_json(
                system_prompt=SYSTEM_PROMPT,
                user_prompt=prompt,
                max_tokens=self.response_max_tokens,
            )
        except Exception as error:
            self.resource_ledger.record_failure(error)
            raise
        self.resource_ledger.record_completion(completion)
        plan = self.validator.validate(completion.payload)
        self._last_audit = {
            "schema_version": STATIC_OPTIMIZATION_INTERFACE_VERSION,
            "role_id": self.role_id,
            "public_context_sha256": context_sha256,
            "plan_sha256": canonical_sha256(plan.to_dict()),
            "provider_model": str(completion.model),
            "provider_attempts": int(completion.attempts),
            "provider_usage": copy.deepcopy(to_builtin(completion.usage)),
            "model_call_consumed": True,
            "prompt_estimated_tokens": prompt_estimated_tokens,
            "prompt_token_estimate_cap": self.prompt_token_estimate_cap,
            "static_world_assumed": True,
            "hidden_world_fields_supplied": False,
            "material_information_condition": (
                self.context_builder.material_information_condition
            ),
            "material_information_sha256": (
                self.context_builder.material_information_sha256
            ),
            "scoring_contract": copy.deepcopy(self.scoring_contract),
        }
        return plan

    def synthesize_final(
        self,
        history: Sequence[Mapping[str, Any]],
        *,
        include_prediction_queries: bool | None = None,
    ) -> StaticFinalRecommendation:
        if include_prediction_queries is None:
            include_prediction_queries = (
                self.predictive_world_understanding_enabled
                and self.predictive_queries_in_final_synthesis
            )
        context = self.final_synthesis_context(
            history,
            include_prediction_queries=include_prediction_queries,
        )
        context_sha256 = canonical_sha256(context)
        dimension = _recipe_dimension(
            self.task_info, self.electrochemical_workflow_mode
        )
        recipe_kind = task_recipe_kind(self.task_info)
        electrochemical = recipe_kind == "electrochemical"
        named_controls = _uses_named_physical_controls(self.task_info)
        prediction_queries = (
            (
                build_electrochemical_prediction_queries(
                    history,
                    electrochemical_workflow_mode=self.electrochemical_workflow_mode,
                )
                if electrochemical
                else build_crystallization_prediction_queries(history)
            )
            if include_prediction_queries
            else ()
        )
        if prediction_queries:
            public_queries = [query.to_public_dict() for query in prediction_queries]
            if context.get("held_out_prediction_queries") != public_queries:
                raise RuntimeError("predictive query regeneration does not match final context")
        recommendation_field = (
            {
                "recommended_recipe_parameters": {
                    key: copy.deepcopy(value)
                    for key, value in _recipe_parameter_schema(
                        self.task_info, self.electrochemical_workflow_mode
                    ).items()
                }
            }
            if named_controls
            else {
                "recommended_search_vector": [
                    "number in [0,1]" for _ in range(dimension)
                ]
            }
        )
        structured_claim_shape = {
            "structured_claims": [
                {
                    "claim_id": "string",
                    "cause_variables": ["declared public cause variable"],
                    "effect_variable": "declared public effect variable",
                    "relation": (
                        "positive|negative|nonmonotonic|conditional|no_direct_effect"
                    ),
                    "mechanism_tags": ["declared public mechanism tag"],
                    "scope": "string",
                    "evidence_ids": ["public evidence ID"],
                    "confidence": "number in [0,1]",
                }
            ]
        }
        counterfactual_prediction_shape = (
            {
                "counterfactual_predictions": [
                    {
                        "query_id": query.query_id,
                        "metric_predictions": [
                            {
                                "metric_id": metric_id,
                                "direction": "increase|decrease|no_material_change",
                                "confidence": "number in [0,1]",
                            }
                            for metric_id in query.metric_ids
                        ],
                    }
                    for query in prediction_queries
                ]
            }
            if prediction_queries
            else {}
        )
        prompt_payload = {
            "schema_version": self.final_synthesis_version,
            "public_final_synthesis_context": context,
            "public_context_sha256": context_sha256,
            **(
                {"forbidden_json_fields": ["counterfactual_predictions"]}
                if self.predictive_world_understanding_enabled
                and not include_prediction_queries
                else {}
            ),
            "required_json_shape": {
                "schema_version": self.final_synthesis_version,
                **recommendation_field,
                "recommended_measurement_slots": ["public diagnostic slot ID"],
                "recommendation_type": "tested|interpolated|extrapolated",
                "source_experiment_indices": ["integer experiment index"],
                "predicted_score": "number in [0,1]",
                "confidence": "number in [0,1]",
                "method_summary": "string",
                "evidence_refs": [
                    "at most 16 public evidence IDs"
                ],
                "working_explanation": {
                    "empirical_relationships": ["at most 16 strings"],
                    "mechanistic_hypothesis": "string",
                    "supporting_evidence_ids": [
                        "at most 16 public evidence IDs"
                    ],
                    "contradicting_evidence_ids": [
                        "at most 16 public evidence IDs"
                    ],
                    "uncertainty": "number in [0,1]",
                    **(structured_claim_shape if named_controls else {}),
                },
                "remaining_risks": ["at most 16 strings"],
                "recommended_followup": "string",
                **counterfactual_prediction_shape,
            },
        }
        prompt = json.dumps(
            prompt_payload,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        prompt_estimated_tokens = estimate_prompt_tokens(prompt)
        if prompt_estimated_tokens > self.final_synthesis_prompt_token_estimate_cap:
            raise PromptBudgetExceededError(
                "static final synthesis prompt estimate "
                f"{prompt_estimated_tokens} exceeds cap "
                f"{self.final_synthesis_prompt_token_estimate_cap}"
            )
        try:
            completion = self.client.complete_json(
                system_prompt=(
                    FINAL_SYNTHESIS_SEPARATE_PREDICTIVE_SYSTEM_PROMPT
                    if self.predictive_world_understanding_enabled
                    and not include_prediction_queries
                    else FINAL_SYNTHESIS_SYSTEM_PROMPT
                ),
                user_prompt=prompt,
                max_tokens=self.response_max_tokens,
            )
        except Exception as error:
            self.resource_ledger.record_failure(error)
            raise
        self.resource_ledger.record_completion(completion)
        evidence_catalog = [
            str(entry["evidence_id"])
            for record in history
            for entry in record["measurement_evidence"]
        ]
        recommendation = self.final_validator.validate(
            completion.payload,
            history=history,
            evidence_catalog=evidence_catalog,
            prediction_queries=prediction_queries,
        )
        self._last_synthesis_audit = {
            "schema_version": self.final_synthesis_version,
            "role_id": self.role_id,
            "public_context_sha256": context_sha256,
            "recommendation_sha256": canonical_sha256(recommendation.to_dict()),
            "provider_model": str(completion.model),
            "provider_attempts": int(completion.attempts),
            "provider_usage": copy.deepcopy(to_builtin(completion.usage)),
            "prompt_estimated_tokens": prompt_estimated_tokens,
            "prompt_token_estimate_cap": (
                self.final_synthesis_prompt_token_estimate_cap
            ),
            "static_world_assumed": True,
            "validation_feedback_returned_to_agent": False,
            "predictive_world_understanding_enabled": bool(prediction_queries),
            "predictive_queries_visible": bool(prediction_queries),
            "forbidden_json_fields": (
                ["counterfactual_predictions"]
                if self.predictive_world_understanding_enabled
                and not bool(prediction_queries)
                else []
            ),
            "recommendation_committed_before_predictive_query_visibility": (
                self.predictive_world_understanding_enabled
                and not bool(prediction_queries)
            ),
            "predictive_query_sha256": [
                query.query_sha256 for query in prediction_queries
            ],
            "predictive_query_set_sha256": (
                canonical_sha256(
                    [query.to_public_dict() for query in prediction_queries]
                )
                if prediction_queries
                else None
            ),
            "material_information_condition": (
                self.context_builder.material_information_condition
            ),
            "material_information_sha256": (
                self.context_builder.material_information_sha256
            ),
        }
        return recommendation

    def predict_counterfactuals(
        self,
        history: Sequence[Mapping[str, Any]],
        *,
        prediction_queries: Sequence[
            ElectrochemicalPredictionQuery | CrystallizationPredictionQuery
        ],
        committed_recommendation_sha256: str,
    ) -> tuple[dict[str, Any], ...]:
        if not self.predictive_world_understanding_enabled:
            raise RuntimeError("predictive world understanding is not enabled")
        if self.predictive_queries_in_final_synthesis:
            raise RuntimeError("predictive-only call is disabled for the integrated policy")
        if not prediction_queries:
            raise ValueError("predictive-only call requires a frozen query set")
        if not isinstance(committed_recommendation_sha256, str) or len(
            committed_recommendation_sha256
        ) != 64:
            raise ValueError("committed recommendation requires a SHA256 digest")
        context = self.final_synthesis_context(
            history,
            include_prediction_queries=False,
        )
        if "held_out_prediction_queries" in context:
            raise RuntimeError("final recommendation context leaked predictive queries")
        public_queries = [query.to_public_dict() for query in prediction_queries]
        predictive_context = {
            "public_campaign_context": context,
            "held_out_prediction_queries": public_queries,
            "prediction_contract": {
                "recommendation_committed_before_query_visibility": True,
                "prediction_call_can_modify_recommendation": False,
                "feedback_returned_to_agent": False,
            },
        }
        prompt_payload = {
            "schema_version": STATIC_PREDICTIVE_SYNTHESIS_VERSION,
            "public_predictive_context": predictive_context,
            "public_context_sha256": canonical_sha256(predictive_context),
            "required_json_shape": {
                "schema_version": STATIC_PREDICTIVE_SYNTHESIS_VERSION,
                "counterfactual_predictions": [
                    {
                        "query_id": query.query_id,
                        "metric_predictions": [
                            {
                                "metric_id": metric_id,
                                "direction": "increase|decrease|no_material_change",
                                "confidence": "number in [0,1]",
                            }
                            for metric_id in query.metric_ids
                        ],
                    }
                    for query in prediction_queries
                ],
            },
        }
        prompt = json.dumps(
            prompt_payload,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        prompt_estimated_tokens = estimate_prompt_tokens(prompt)
        if prompt_estimated_tokens > self.predictive_synthesis_prompt_token_estimate_cap:
            raise PromptBudgetExceededError(
                "static predictive synthesis prompt estimate "
                f"{prompt_estimated_tokens} exceeds cap "
                f"{self.predictive_synthesis_prompt_token_estimate_cap}"
            )
        try:
            completion = self.client.complete_json(
                system_prompt=PREDICTIVE_SYNTHESIS_SYSTEM_PROMPT,
                user_prompt=prompt,
                max_tokens=self.response_max_tokens,
            )
        except Exception as error:
            self.resource_ledger.record_failure(error)
            raise
        self.resource_ledger.record_completion(completion)
        payload = completion.payload
        required_fields = {"schema_version", "counterfactual_predictions"}
        if not isinstance(payload, Mapping) or set(payload) != required_fields:
            raise ScientificPlanValidationError(
                "predictive-only response fields do not match its contract",
                field_path="predictive_synthesis_response",
                constraint="exact_declared_fields",
            )
        if payload["schema_version"] != STATIC_PREDICTIVE_SYNTHESIS_VERSION:
            raise ScientificPlanValidationError(
                "predictive-only schema_version does not match the frozen contract",
                field_path="schema_version",
                constraint="exact_schema_version",
                observed=str(payload["schema_version"]),
                limit=STATIC_PREDICTIVE_SYNTHESIS_VERSION,
            )
        try:
            parsed = parse_counterfactual_predictions(
                payload["counterfactual_predictions"],
                queries=prediction_queries,
            )
        except ValueError as error:
            raise ScientificPlanValidationError(
                str(error),
                field_path="counterfactual_predictions",
                constraint="frozen_predictive_contract",
            ) from error
        normalized = tuple(prediction.to_dict() for prediction in parsed)
        self._last_predictive_audit = {
            "schema_version": STATIC_PREDICTIVE_SYNTHESIS_VERSION,
            "role_id": self.role_id,
            "public_context_sha256": canonical_sha256(predictive_context),
            "query_sha256": [query.query_sha256 for query in prediction_queries],
            "query_set_sha256": canonical_sha256(public_queries),
            "predictions_sha256": canonical_sha256(list(normalized)),
            "committed_recommendation_sha256": committed_recommendation_sha256,
            "recommendation_visible_to_prediction_call": False,
            "recommendation_committed_before_query_visibility": True,
            "prediction_call_can_modify_recommendation": False,
            "provider_model": str(completion.model),
            "provider_attempts": int(completion.attempts),
            "provider_usage": copy.deepcopy(to_builtin(completion.usage)),
            "prompt_estimated_tokens": prompt_estimated_tokens,
            "prompt_token_estimate_cap": (
                self.predictive_synthesis_prompt_token_estimate_cap
            ),
        }
        return normalized

    def decision_audit(self) -> dict[str, Any] | None:
        return copy.deepcopy(self._last_audit)

    def synthesis_audit(self) -> dict[str, Any] | None:
        return copy.deepcopy(self._last_synthesis_audit)

    def predictive_audit(self) -> dict[str, Any] | None:
        return copy.deepcopy(self._last_predictive_audit)

    def manifest(self) -> dict[str, Any]:
        return {
            "agent_name": self.name,
            "agent_family": type(self).__name__,
            "role_id": self.role_id,
            "seed": self.seed,
            "provider_model": self.client.model,
            "decision_scope": "complete_experiment",
            "interface_version": STATIC_OPTIMIZATION_INTERFACE_VERSION,
            "prompt_version": STATIC_OPTIMIZATION_PROMPT_VERSION,
            "history_limit": self.history_limit,
            "prompt_token_estimate_cap": self.prompt_token_estimate_cap,
            "experiment_horizon": self.experiment_horizon,
            "horizon_visible": self.horizon_visible,
            "final_synthesis_enabled": self.final_synthesis_enabled,
            "final_synthesis_version": self.final_synthesis_version,
            "declared_claim_validation_policy": (
                self.declared_claim_validation_policy
            ),
            "final_synthesis_prompt_token_estimate_cap": (
                self.final_synthesis_prompt_token_estimate_cap
            ),
            "predictive_synthesis_prompt_token_estimate_cap": (
                self.predictive_synthesis_prompt_token_estimate_cap
            ),
            "predictive_world_understanding_enabled": (
                self.predictive_world_understanding_enabled
            ),
            "predictive_queries_in_final_synthesis": (
                self.predictive_queries_in_final_synthesis
            ),
            "electrochemical_workflow_mode": self.electrochemical_workflow_mode,
            "material_information_condition": (
                self.context_builder.material_information_condition
            ),
            "material_information_sha256": (
                self.context_builder.material_information_sha256
            ),
            "scoring_contract": copy.deepcopy(self.scoring_contract),
            "mechanical_closeout": True,
            "static_world": True,
            "hidden_world_fields_supplied": False,
        }

    def method_resource_usage(self) -> dict[str, Any]:
        return self.resource_ledger.snapshot(self.client)


def compile_static_optimization_plan(
    task_info: Mapping[str, Any],
    plan: StaticOptimizationPlan,
    *,
    electrochemical_workflow_mode: str = (
        ELECTROCHEMICAL_WORKFLOW_STATIC_SINGLE_STAGE
    ),
) -> dict[str, Any]:
    workflow_mode = normalize_electrochemical_workflow_mode(
        electrochemical_workflow_mode
    )
    recipe = _recipe_from_vector(
        task_info,
        workflow_mode,
        np.asarray(plan.search_vector, dtype=float),
    )
    available = {
        str(item["slot_id"])
        for item in _measurement_slots(task_info, workflow_mode)
    }
    requested = set(plan.requested_measurement_slots)
    if not requested.issubset(available):
        raise ValueError("static plan requests an unknown diagnostic slot")
    steps: list[dict[str, Any]] = []
    slots_by_step: dict[str, str] = {}
    diagnostic_index = 0
    for action in recipe["steps"]:
        operation = action.get("operation")
        instrument = action.get("instrument")
        if operation == "measure" and instrument != "final_assay":
            diagnostic_index += 1
            slot_id = f"diagnostic-{diagnostic_index:02d}-{instrument}"
            if slot_id not in requested:
                continue
            slots_by_step[str(len(steps))] = slot_id
        elif operation == "measure" and instrument == "final_assay":
            slots_by_step[str(len(steps))] = "closeout-final-assay"
        steps.append(copy.deepcopy(action))
    metadata = copy.deepcopy(recipe["metadata"])
    metadata.update(
        {
            "static_optimization_interface_version": STATIC_OPTIMIZATION_INTERFACE_VERSION,
            "requested_measurement_slots": list(plan.requested_measurement_slots),
            "measurement_slots_by_step": slots_by_step,
            "plan_sha256": canonical_sha256(plan.to_dict()),
            "closeout_policy": "recipe_compiler_terminate_then_final_assay",
            "static_world": True,
            "electrochemical_workflow_mode": workflow_mode,
        }
    )
    return {"steps": steps, "metadata": metadata}


__all__ = [
    "DECLARED_CLAIM_VALIDATION_STRICT",
    "DECLARED_CLAIM_VALIDATION_UNSCORED_UNKNOWN",
    "FINAL_SYNTHESIS_SEPARATE_PREDICTIVE_SYSTEM_PROMPT",
    "FINAL_SYNTHESIS_SYSTEM_PROMPT",
    "PREDICTIVE_SYNTHESIS_SYSTEM_PROMPT",
    "STATIC_FINAL_SYNTHESIS_SEPARATE_VERSION",
    "STATIC_FINAL_SYNTHESIS_TOLERANT_DECLARED_VERSION",
    "STATIC_FINAL_SYNTHESIS_VERSION",
    "STATIC_OPTIMIZATION_INTERFACE_VERSION",
    "STATIC_OPTIMIZATION_PROMPT_VERSION",
    "STATIC_PREDICTIVE_SYNTHESIS_VERSION",
    "StaticFinalRecommendation",
    "StaticFinalRecommendationValidator",
    "StaticOptimizationAgent",
    "StaticOptimizationContextBuilder",
    "StaticOptimizationPlan",
    "StaticOptimizationValidator",
    "compile_static_optimization_plan",
]
