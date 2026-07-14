"""Agent-facing public views for ChemWorld environments.

The functions in this module are intentionally thin adapters over the existing
task registry, operation validator, observation contracts, and campaign state.
They do not read hidden ledgers or rate constants.
"""

from __future__ import annotations

import math
from typing import Any

import numpy as np

from chemworld.data.logging import to_builtin
from chemworld.envs.spaces import OBSERVATION_KEYS
from chemworld.foundation import equipment_settings
from chemworld.materials import material_choice_labels
from chemworld.world.actions import CATALYSTS, SOLVENTS
from chemworld.world.operations import (
    INSTRUMENTS,
    OPERATION_FIELD_BOUNDS,
    OPERATION_FIELD_CHOICES,
    OPERATION_TYPES,
    operation_contracts,
)

FIELD_UNITS: dict[str, str] = {
    "amount_mol": "mol",
    "volume_L": "L",
    "catalyst_amount_mol": "mol",
    "target_temperature_K": "K",
    "duration_s": "s",
    "stirring_speed_rpm": "rpm",
    "sample_volume_L": "L",
    "wash_volume_L": "L",
    "transfer_fraction": "dimensionless",
    "seed_mass_g": "g",
    "reflux_ratio": "dimensionless",
    "flow_rate_mL_min": "mL/min",
    "residence_time_s": "s",
    "potential_V": "V",
    "current_mA": "mA",
    "instrument": "categorical",
    "catalyst": "categorical",
    "solvent": "categorical",
    "phase": "categorical",
    "target_phase": "categorical",
    "extractant": "categorical",
}

FIELD_RANGES: dict[str, tuple[float, float]] = {
    "amount_mol": (0.0, 0.040),
    "volume_L": (0.0, 0.080),
    "catalyst_amount_mol": (0.0, 0.005),
    "target_temperature_K": (250.0, 520.0),
    "duration_s": (0.0, 14_400.0),
    "stirring_speed_rpm": (100.0, 1200.0),
    "sample_volume_L": (0.0, 0.002),
    "wash_volume_L": (0.0, 0.040),
    "transfer_fraction": (0.0, 1.0),
    "seed_mass_g": (0.0, 1.0),
    "reflux_ratio": (0.0, 10.0),
    "flow_rate_mL_min": (0.01, 20.0),
    "residence_time_s": (1.0, 7200.0),
    "potential_V": (-3.0, 3.0),
    "current_mA": (0.0, 500.0),
}

FIELD_CHOICES: dict[str, list[Any]] = {
    "instrument": list(INSTRUMENTS),
    "catalyst": list(range(len(CATALYSTS))),
    "solvent": list(range(len(SOLVENTS))),
    "phase": ["aqueous", "organic"],
    "target_phase": ["aqueous", "organic"],
    "extractant": list(range(len(SOLVENTS))),
}

OPERATION_GROUPS: dict[str, tuple[str, ...]] = {
    "reaction_setup": ("add_solvent", "add_reagent", "add_catalyst"),
    "reaction_control": ("heat", "wait", "quench", "terminate"),
    "sampling_and_measurement": ("sample", "measure"),
    "phase_setup": ("add_phase", "add_extractant"),
    "phase_partition": ("mix", "settle", "separate_phase"),
    "purification": ("transfer", "wash", "dry", "concentrate"),
    "equilibrium_characterization": ("measure", "terminate"),
}

TASK_PROMPT_PROFILES: dict[str, dict[str, Any]] = {
    "reaction-to-assay": {
        "task_goal": (
            "Run one complete reaction experiment from charging the reactor to a "
            "valid terminal final assay."
        ),
        "success_criteria": [
            "Reach a valid final_assay after a physically legal operation sequence.",
            "Improve final_assay_score while keeping the trajectory valid.",
            "Use intermediate instruments only when their information is worth the cost.",
        ],
        "constraints": [
            "Single-experiment task: final_assay ends the episode.",
            "Terminate or quench before requesting final_assay.",
            "Heating before adding solvent/reagent/catalyst is invalid.",
        ],
        "measurement_policy": (
            "HPLC, GC, and UV-vis are noisy intermediate tools; final_assay is the "
            "high-cost terminal measurement used for the task result."
        ),
        "recommended_strategy": [
            "Charge solvent and reagent first, then add catalyst if used.",
            "Choose a temperature/time pair, run heat or wait, then inspect with HPLC/UV-vis.",
            "Terminate and run final_assay only after the reaction has meaningful conversion.",
        ],
        "failure_modes": [
            "precondition failure",
            "budget exhaustion before final_assay",
            "unsafe high-temperature or high-risk trajectory",
        ],
    },
    "reaction-to-purification": {
        "task_goal": (
            "Complete a reaction, extract product through phase separation, purify "
            "the material, and submit a final assay."
        ),
        "success_criteria": [
            "Maximize score while balancing purity, recovery, and cost.",
            "Keep process_mass_balance_error small through separation and purification.",
            "Use final_assay after downstream workup to make the result leaderboard eligible.",
        ],
        "constraints": [
            "Single-experiment task: final_assay ends the episode.",
            "Downstream purification should follow a terminated or quenched reaction.",
            "Phase operations require appropriate phase or extractant setup.",
        ],
        "measurement_policy": (
            "Intermediate HPLC/GC/UV-vis can guide reaction and workup choices. "
            "The final_assay should be run on the selected purified material."
        ),
        "recommended_strategy": [
            "First generate product under safe reaction conditions.",
            (
                "Add extractant or phase, mix, settle, and separate the phase "
                "expected to carry product."
            ),
            "Use wash/dry/concentrate to trade recovery against purity before final_assay.",
        ],
        "failure_modes": [
            "poor phase split",
            "low product recovery",
            "high impurity after purification",
            "mass-balance drift",
        ],
    },
    "partition-discovery": {
        "task_goal": (
            "Learn the public behavior of an unknown product/solvent partition system "
            "through repeated finite-budget experiments."
        ),
        "success_criteria": [
            "Estimate phase_ratio from public observations.",
            "Identify when product is enriched in organic versus aqueous phase.",
            "Use measurements efficiently across campaign experiments.",
        ],
        "constraints": [
            (
                "Campaign task: one terminal assay or termination summarizes an "
                "experiment, not the whole campaign."
            ),
            "Partition coefficients and hidden phase amounts are not directly visible.",
            "Phase split actions require a valid phase setup, mixing, and settling sequence.",
        ],
        "measurement_policy": (
            "Use HPLC/GC/UV-vis/final_assay as public instruments to infer partition "
            "trends; do not assume hidden partition coefficients are known."
        ),
        "recommended_strategy": [
            "Vary solvent or extractant choices across experiments.",
            "Use mix and settle before separating phases.",
            (
                "Compare instrument summaries from organic and aqueous outcomes "
                "to build a local model."
            ),
        ],
        "failure_modes": [
            "insufficient phase setup",
            "separating before settling",
            "overusing costly measurements",
            "confusing noisy instrument estimates with hidden truth",
        ],
    },
    "equilibrium-characterization": {
        "task_goal": (
            "Characterize a bounded aqueous-equilibrium slice using pH-meter "
            "and final-assay observations."
        ),
        "success_criteria": [
            "Obtain informative pH-meter observations before final assay.",
            "Maximize equilibrium_confidence while keeping equilibrium_residual low.",
            "Use measurements efficiently under the finite campaign budget.",
        ],
        "constraints": [
            "pH is public only through ph_meter or final_assay observations.",
            "Hidden acidity constants and species amounts are never exposed.",
            "Final assay still requires terminate.",
        ],
        "measurement_policy": (
            "ph_meter is the low-cost primary characterization instrument. "
            "final_assay provides leaderboard-grade equilibrium metrics."
        ),
        "recommended_strategy": [
            "Charge solvent and a moderate reagent amount.",
            "Measure pH, perturb concentration, then measure pH again.",
            "Terminate and request final_assay after enough equilibrium evidence.",
        ],
        "failure_modes": [
            "measuring before material exists",
            "overusing final assay without intermediate evidence",
            "treating pH-normalized Gym scalar as hidden pKa",
        ],
    },
}

HIDDEN_INFORMATION_POLICY = (
    "No hidden species amounts, rate constants, mechanism parameters, partition "
    "coefficients, hidden phase amounts, or private scenario parameters are exposed "
    "through agent-facing views."
)

RL_MISSING_VALUE = -1.0
RL_OBSERVATION_VALUE_BOUNDS = (RL_MISSING_VALUE, 1.0)
RL_MASK_BOUNDS = (0.0, 1.0)
RL_COST_BOUNDS = (0.0, 1.0)

SUBMISSION_REQUIREMENTS = [
    "trajectory JSONL",
    "agent manifest",
    "reproducible command or replay trace",
]


def _base_env(env: Any) -> Any:
    return getattr(env, "unwrapped", env)


def _latest_info(env: Any) -> dict[str, Any]:
    base = _base_env(env)
    info = getattr(base, "_last_info", {})
    return dict(info) if isinstance(info, dict) else {}


def _latest_observation(env: Any) -> dict[str, Any]:
    base = _base_env(env)
    observation = getattr(base, "_last_observation", {})
    return dict(observation) if isinstance(observation, dict) else {}


def _safe_float(value: Any, default: float = 0.0) -> float:
    try:
        scalar = float(value.reshape(-1)[0]) if isinstance(value, np.ndarray) else float(value)
    except (TypeError, ValueError, IndexError):
        return default
    return scalar if math.isfinite(scalar) else default


def _observed_float(value: Any) -> tuple[float, bool]:
    try:
        scalar = float(value.reshape(-1)[0]) if isinstance(value, np.ndarray) else float(value)
    except (TypeError, ValueError, IndexError):
        return -1.0, False
    return (scalar, True) if math.isfinite(scalar) else (-1.0, False)


def _field_schema(field: str, *, operation: str | None = None) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "field": field,
        "unit": FIELD_UNITS.get(field, "unitless"),
        "required": True,
    }
    bounds = OPERATION_FIELD_BOUNDS.get((operation, field)) if operation is not None else None
    if bounds is None:
        bounds = FIELD_RANGES.get(field)
    if bounds is not None:
        low, high = bounds
        payload["bounds"] = {"low": low, "high": high}
        payload["recommended_range"] = {"low": low, "high": high}
    operation_choices = (
        OPERATION_FIELD_CHOICES.get((operation, field)) if operation is not None else None
    )
    choices = list(operation_choices) if operation_choices is not None else FIELD_CHOICES.get(field)
    if choices is not None:
        payload["choices"] = list(choices)
        labels = material_choice_labels(field)
        if labels:
            payload["choice_labels"] = labels
    return payload


def _locked_recipe_choice(base: Any, operation: str, field: str) -> Any | None:
    lock_contract = {
        "add_solvent": ("solvent", "batch_reactor", "solvent_volume_L"),
        "add_catalyst": ("catalyst", "batch_reactor", "catalyst_amount_mol"),
        "add_extractant": (
            "extractant",
            "liquid_liquid_extractor",
            "extractant_volume_L",
        ),
    }.get(operation)
    if lock_contract is None:
        return None
    category_field, equipment_id, charged_key = lock_contract
    if field != category_field:
        return None
    state = getattr(base, "_state", None)
    if state is None:
        return None
    settings = equipment_settings(state.equipment, equipment_id)
    if float(settings.get(charged_key, 0.0)) <= 0.0:
        return None
    return settings.get(field)


def action_schema(env: Any, operation: str) -> dict[str, Any]:
    """Return the public JSON-friendly schema for one operation."""

    base = _base_env(env)
    contracts = operation_contracts()
    if operation not in contracts:
        return {
            "operation": operation,
            "valid_operation_type": False,
            "error": f"Unknown operation {operation!r}",
        }
    contract = contracts[operation]
    fields = [_field_schema(field, operation=operation) for field in contract.required_fields]
    for field in fields:
        field_name = str(field["field"])
        bounds = field.get("bounds")
        state = getattr(base, "_state", None)
        if isinstance(bounds, dict) and state is not None:
            low, high = base.operation_validator.public_field_bounds(
                operation,
                field_name,
                state,
                low=float(bounds["low"]),
                high=float(bounds["high"]),
            )
            if low != float(bounds["low"]) or high != float(bounds["high"]):
                field["bounds"] = {"low": low, "high": high}
                field["recommended_range"] = {"low": low, "high": high}
                field["state_dependent_bounds"] = True
        locked = _locked_recipe_choice(base, operation, field_name)
        if locked is not None:
            field["choices"] = [locked]
            field["locked_for_current_experiment"] = True
    if operation == "measure":
        fields = [
            {
                **_field_schema("instrument", operation=operation),
                "choices": sorted(getattr(base, "allowed_instruments", set(INSTRUMENTS))),
            }
        ]
    return {
        "operation": operation,
        "valid_operation_type": True,
        "module": contract.module,
        "kind": contract.kind,
        "required_fields": list(contract.required_fields),
        "fields": fields,
        "preconditions": list(contract.preconditions),
        "task_allowed": operation in getattr(base, "allowed_operations", set(OPERATION_TYPES)),
        "notes": [
            "Use validate_action(action) before executing.",
            "Payload aliases are canonicalized by the environment action codec.",
        ],
    }


def validate_action(env: Any, action: dict[str, Any]) -> dict[str, Any]:
    """Validate an action against schema, task policy, instrument policy, and state."""

    base = _base_env(env)
    try:
        canonical = base.action_codec.canonicalize(action)
    except (TypeError, ValueError) as exc:
        return {
            "operation_type": str(action.get("operation", "invalid")),
            "valid": False,
            "dispatchable_to_runtime": False,
            "preconditions": {"action_schema_valid": False},
            "invalid_reasons": [str(exc)],
            "valid_operations": list(base.operation_validator.valid_operations(base._state)),
            "action_mask": list(base.operation_validator.action_mask(base._state)),
            "cost_penalty": 0.20,
            "safety_flags": {
                "operation_allowed_by_task": False,
                "precondition_failed": True,
                "action_schema_valid": False,
            },
            "canonical_action": to_builtin(action),
            "will_mutate_state": False,
        }
    validation = base.operation_validator.validate(canonical, base._state)
    payload = validation.to_dict()
    payload["canonical_action"] = to_builtin(canonical)
    payload["will_mutate_state"] = False
    return to_builtin(payload)


def available_actions(env: Any, *, include_invalid: bool = False) -> list[dict[str, Any]]:
    """Return current operation affordances for agents and tool planners."""

    base = _base_env(env)
    valid = set(base.operation_validator.valid_operations(base._state))
    allowed = set(getattr(base, "allowed_operations", set(OPERATION_TYPES)))
    actions: list[dict[str, Any]] = []
    for operation in OPERATION_TYPES:
        if operation not in allowed and not include_invalid:
            continue
        affordance = base.operation_validator.operation_affordance(operation, base._state)
        validation = affordance.to_dict()
        is_valid = operation in valid
        if not is_valid and not include_invalid:
            continue
        actions.append(
            {
                "operation": operation,
                "valid": is_valid,
                "invalid_reasons": validation["invalid_reasons"],
                "preconditions": validation["preconditions"],
                "schema": action_schema(base, operation),
            }
        )
    return actions


def _task_spec_value(base: Any, name: str, fallback: Any = None) -> Any:
    spec = getattr(base, "task_spec", None)
    if spec is None:
        return fallback
    return getattr(spec, name, fallback)


def _allowed_operation_groups(allowed_operations: list[str]) -> dict[str, list[str]]:
    allowed = set(allowed_operations)
    groups: dict[str, list[str]] = {}
    grouped: set[str] = set()
    for group, operations in OPERATION_GROUPS.items():
        present = [operation for operation in operations if operation in allowed]
        if present:
            groups[group] = present
            grouped.update(present)
    other = sorted(allowed - grouped)
    if other:
        groups["other"] = other
    return groups


def _default_task_prompt_profile(info: dict[str, Any], base: Any) -> dict[str, Any]:
    description = _task_spec_value(
        base,
        "description",
        info.get("description") or "Run the ChemWorld task under the public contract.",
    )
    return {
        "task_goal": description,
        "success_criteria": [
            "Optimize the public task score under the stated budget and constraints.",
            "Use only task-allowed operations and instruments.",
            "Submit a replayable trajectory with public observations and constraint flags.",
        ],
        "constraints": [
            f"Episode mode: {info.get('episode_mode')}.",
            f"Safety limit: {info.get('safety_limit')}.",
            "Measurements are noisy and consume time, sample, or cost.",
        ],
        "measurement_policy": (
            "Use available instruments to obtain public observations. Instrument "
            "outputs are partial, noisy, and cost-aware."
        ),
        "recommended_strategy": [
            "Validate actions before executing them.",
            "Use measurements to update a local world model.",
            "Balance score, cost, risk, and remaining budget.",
        ],
        "failure_modes": [
            "invalid operation",
            "precondition failure",
            "budget exhaustion",
            "unsafe or high-cost trajectory",
        ],
    }


def _task_prompt_profile(info: dict[str, Any], base: Any) -> dict[str, Any]:
    task_id = str(info.get("task_id") or "")
    if task_id in TASK_PROMPT_PROFILES:
        return TASK_PROMPT_PROFILES[task_id]
    return _default_task_prompt_profile(info, base)


def experiment_lifecycle_contract(episode_mode: Any) -> dict[str, str]:
    """Describe experiment completion without prescribing a search strategy."""

    final_effect = (
        "A valid final_assay completes the current experiment and, while campaign "
        "budget remains, resets the environment to a fresh experiment."
        if episode_mode == "campaign"
        else "A valid final_assay completes the experiment and ends the episode."
    )
    return {
        "terminate_effect": (
            "terminate marks the current process as terminated; it does not by itself "
            "complete the experiment."
        ),
        "final_assay_precondition": (
            "measure with instrument=final_assay is valid only after terminate."
        ),
        "final_assay_effect": final_effect,
        "intermediate_measurement_effect": (
            "Measurements with other instruments provide evidence but do not complete "
            "the experiment."
        ),
    }


def _render_task_prompt_text(
    *,
    task_id: str,
    objective: Any,
    budget: Any,
    episode_mode: Any,
    safety_limit: Any,
    profile: dict[str, Any],
    allowed_operations: list[str],
    allowed_instruments: list[str],
    success_metrics: list[str],
    operation_groups: dict[str, list[str]],
    experiment_lifecycle: dict[str, str],
) -> str:
    group_lines = [
        f"  - {group}: {', '.join(operations)}" for group, operations in operation_groups.items()
    ]
    lines = [
        f"Task: {task_id or 'ad-hoc ChemWorld task'}",
        f"Goal: {profile['task_goal']}",
        (
            f"Objective: {objective}; budget: {budget} operations; "
            f"episode_mode: {episode_mode}; safety_limit: {safety_limit}."
        ),
        "Hidden information policy: " + HIDDEN_INFORMATION_POLICY,
        "Success criteria:",
        *[f"  - {item}" for item in profile["success_criteria"]],
        "Constraints:",
        *[f"  - {item}" for item in profile["constraints"]],
        "Experiment lifecycle:",
        *[f"  - {item}" for item in experiment_lifecycle.values()],
        "Allowed tools:",
        f"  - instruments: {', '.join(allowed_instruments)}",
        "  - operation groups:",
        *group_lines,
        f"  - all operations: {', '.join(allowed_operations)}",
        f"Success metrics: {', '.join(success_metrics) if success_metrics else 'task score'}.",
        f"Measurement policy: {profile['measurement_policy']}",
        "Recommended strategy:",
        *[f"  - {item}" for item in profile["recommended_strategy"]],
        "Submission requirements: " + ", ".join(SUBMISSION_REQUIREMENTS) + ".",
    ]
    return "\n".join(lines)


def task_prompt(env: Any) -> dict[str, Any]:
    """Build a natural-language task prompt plus structured task facts."""

    base = _base_env(env)
    info = base.task_info()
    allowed_operations = list(info.get("allowed_operations", []))
    allowed_instruments = list(info.get("allowed_instruments", []))
    success_metrics = list(
        info.get("scoring_contract", {}).get("success_metrics")
        or _task_spec_value(base, "success_metrics", ())
        or []
    )
    operation_groups = _allowed_operation_groups(allowed_operations)
    profile = _task_prompt_profile(info, base)
    experiment_lifecycle = experiment_lifecycle_contract(info.get("episode_mode"))
    task_id = str(info.get("task_id") or "")
    text = _render_task_prompt_text(
        task_id=task_id,
        objective=info.get("objective"),
        budget=info.get("budget"),
        episode_mode=info.get("episode_mode"),
        safety_limit=info.get("safety_limit"),
        profile=profile,
        allowed_operations=allowed_operations,
        allowed_instruments=allowed_instruments,
        success_metrics=success_metrics,
        operation_groups=operation_groups,
        experiment_lifecycle=experiment_lifecycle,
    )
    return {
        "text": text,
        "task_id": info.get("task_id"),
        "objective": info.get("objective"),
        "budget": info.get("budget"),
        "episode_mode": info.get("episode_mode"),
        "description": _task_spec_value(base, "description", info.get("description")),
        "world_law_id": info.get("world_law_id"),
        "scenario_id": info.get("scenario_id"),
        "allowed_operations": info.get("allowed_operations", []),
        "allowed_instruments": info.get("allowed_instruments", []),
        "success_metrics": success_metrics,
        "safety_limit": info.get("safety_limit"),
        "threshold": _task_spec_value(base, "threshold", info.get("threshold")),
        "termination_policy": _task_spec_value(
            base,
            "termination_policy",
            info.get("termination_policy"),
        ),
        "observation_policy": _task_spec_value(
            base,
            "observation_policy",
            info.get("observation_policy"),
        ),
        "task_goal": profile["task_goal"],
        "constraints": list(profile["constraints"]),
        "success_criteria": list(profile["success_criteria"]),
        "allowed_tools": {
            "operations": allowed_operations,
            "operation_groups": operation_groups,
            "instruments": allowed_instruments,
        },
        "material_catalog": info.get("material_catalog", {}),
        "measurement_policy": profile["measurement_policy"],
        "experiment_lifecycle": experiment_lifecycle,
        "recommended_strategy": list(profile["recommended_strategy"]),
        "failure_modes": list(profile["failure_modes"]),
        "hidden_information_policy": HIDDEN_INFORMATION_POLICY,
        "submission_requirements": list(SUBMISSION_REQUIREMENTS),
        "prompt_version": "chemworld-agent-task-prompt-0.3",
    }


def campaign_state(env: Any) -> dict[str, Any]:
    """Return visible campaign progress and best-so-far state."""

    base = _base_env(env)
    summaries = list(getattr(base, "_experiment_summaries", []))
    scored = [
        _safe_float(summary.get("leaderboard_score"), default=-1.0)
        for summary in summaries
        if summary.get("leaderboard_score") is not None
    ]
    info = _latest_info(base)
    current_score = info.get("leaderboard_score")
    current_score_already_summarized = bool(
        info.get("experiment_ended") and getattr(base, "episode_mode", None) == "campaign"
    )
    if current_score is not None and not current_score_already_summarized:
        scored.append(_safe_float(current_score, default=-1.0))
    best_score = max(scored) if scored else None
    remaining_budget = max(
        int(getattr(base, "budget", 0)) - int(getattr(base, "_step_count", 0)),
        0,
    )
    return {
        "campaign_id": getattr(base, "_campaign_id", None),
        "task_id": getattr(base, "task_id", None),
        "scenario_id": getattr(getattr(base, "scenario_spec", None), "scenario_id", None),
        "episode_mode": getattr(base, "episode_mode", None),
        "experiment_index": int(getattr(base, "_experiment_index", 0)),
        "operation_count": int(getattr(base, "_step_count", 0)),
        "remaining_budget": remaining_budget,
        "budget": int(getattr(base, "budget", 0)),
        "final_assay_count": len(summaries)
        + (1 if current_score is not None and not current_score_already_summarized else 0),
        "best_score": best_score,
        "last_terminal_summary": summaries[-1] if summaries else None,
        "experiment_summaries": to_builtin(summaries),
        "done": bool(getattr(base, "_done", False)),
    }


def rl_observation_view(
    observation: dict[str, Any],
    info: dict[str, Any] | None = None,
    *,
    include_cost: bool = True,
) -> dict[str, Any]:
    """Return a NaN-safe vector observation and binary observed mask."""

    values: list[float] = []
    mask: list[float] = []
    for key in OBSERVATION_KEYS:
        value, observed = _observed_float(observation.get(key))
        values.append(value if observed else RL_MISSING_VALUE)
        mask.append(1.0 if observed else 0.0)
    if include_cost:
        values.append(_safe_float((info or {}).get("cost"), default=0.0))
        mask.append(1.0)
    spec = rl_observation_spec(include_cost=include_cost)
    return {
        "mode": "rl",
        "schema_version": "chemworld-rl-view-0.2",
        "keys": spec["keys"],
        "vector": values,
        "mask": mask,
        "cost": _safe_float((info or {}).get("cost"), default=0.0),
        "bounds": spec["value_bounds"],
        "mask_bounds": spec["mask_bounds"],
        "missing_value": RL_MISSING_VALUE,
        "dtype": "float32",
        "nan_safe": True,
        "constraint_flags": to_builtin((info or {}).get("constraint_flags", {})),
    }


def rl_observation_spec(*, include_cost: bool = True) -> dict[str, Any]:
    """Return the stable RL vector contract used by views and wrappers."""

    keys = [*OBSERVATION_KEYS, *(["cost_signal"] if include_cost else [])]
    low = [RL_OBSERVATION_VALUE_BOUNDS[0] for _ in OBSERVATION_KEYS]
    high = [RL_OBSERVATION_VALUE_BOUNDS[1] for _ in OBSERVATION_KEYS]
    if include_cost:
        low.append(RL_COST_BOUNDS[0])
        high.append(RL_COST_BOUNDS[1])
    return {
        "schema_version": "chemworld-rl-view-0.2",
        "keys": list(keys),
        "value_bounds": {
            "low": low,
            "high": high,
        },
        "mask_bounds": {
            "low": [RL_MASK_BOUNDS[0] for _ in keys],
            "high": [RL_MASK_BOUNDS[1] for _ in keys],
        },
        "missing_value": RL_MISSING_VALUE,
        "dtype": "float32",
        "nan_safe": True,
    }


def _peak_group(peak: dict[str, Any]) -> str:
    for key in ("public_role", "role", "group", "species_role", "species_id"):
        value = str(peak.get(key, "")).lower()
        if value:
            if "reactant" in value:
                return "reactant"
            if "byproduct" in value or "impurity" in value:
                return "impurity"
            if "degradation" in value:
                return "degradation"
            if "target" in value or "product" in value:
                return "target"
    return "unknown"


def _find_peak_tables(payload: Any) -> list[list[dict[str, Any]]]:
    if isinstance(payload, dict):
        tables: list[list[dict[str, Any]]] = []
        for key, value in payload.items():
            if key in {"peaks", "peak_table", "chromatogram"} and isinstance(value, list):
                dict_rows = [row for row in value if isinstance(row, dict)]
                if dict_rows:
                    tables.append(dict_rows)
            else:
                tables.extend(_find_peak_tables(value))
        return tables
    if isinstance(payload, list):
        tables = []
        for item in payload:
            tables.extend(_find_peak_tables(item))
        return tables
    return []


def _area_value(peak: dict[str, Any]) -> float:
    for key in ("area_fraction", "peak_fraction", "area", "height", "intensity"):
        if key in peak:
            return max(_safe_float(peak[key], default=0.0), 0.0)
    return 0.0


def spectra_summary(info: dict[str, Any]) -> dict[str, Any]:
    """Summarize public raw signals without exposing hidden mechanism identities."""

    raw_signal = info.get("raw_signal", {})
    raw_signal_dict = raw_signal if isinstance(raw_signal, dict) else {}
    spectra = raw_signal_dict.get("spectra", {})
    channels = raw_signal_dict.get("channels", [])
    if not isinstance(channels, list):
        channels = []
    if isinstance(spectra, dict) and not channels:
        channels = sorted(str(key) for key in spectra)
    peak_tables = _find_peak_tables(raw_signal)
    grouped: dict[str, float] = {
        "target": 0.0,
        "reactant": 0.0,
        "impurity": 0.0,
        "degradation": 0.0,
        "unknown": 0.0,
    }
    dominant_group: str | None = None
    dominant_fraction = 0.0
    total_area = 0.0
    for table in peak_tables:
        for peak in table:
            area = _area_value(peak)
            group = _peak_group(peak)
            grouped[group] = grouped.get(group, 0.0) + area
            total_area += area
    if total_area > 0.0:
        for group, value in list(grouped.items()):
            grouped[group] = value / total_area
        top_group, top_fraction = max(grouped.items(), key=lambda item: item[1])
        dominant_group = top_group
        dominant_fraction = top_fraction

    processed = info.get("processed_estimate", {})
    observed = info.get("observed_keys", [])
    warnings: list[str] = []
    if grouped["reactant"] > grouped["target"] and any(
        key in observed for key in ("yield", "purity", "recovery")
    ):
        warnings.append("reactant_peak_dominates_public_spectrum")
    if grouped["impurity"] + grouped["degradation"] > 0.35:
        warnings.append("impurity_or_degradation_peaks_are_large")

    return {
        "instrument": info.get("instrument_source") or info.get("instrument"),
        "packet_kind": raw_signal_dict.get("kind"),
        "has_spectral_packet": bool(
            peak_tables or spectra or channels or raw_signal_dict.get("kind") == "ph_meter_signal"
        ),
        "channels": [str(channel) for channel in channels],
        "channel_count": len(channels),
        "peak_table_count": len(peak_tables),
        "observed_keys": list(observed),
        "peak_group_fractions": grouped,
        "dominant_peak": {"group": dominant_group, "fraction": dominant_fraction},
        "processed_estimate": to_builtin(processed),
        "uncertainty": to_builtin(info.get("uncertainty", {})),
        "warnings": warnings,
    }


def _recovery_suggestion(env: Any, info: dict[str, Any]) -> str | None:
    flags = info.get("constraint_flags", {})
    if not flags.get("precondition_failed") and not info.get("error_message"):
        return None
    options = [entry["operation"] for entry in available_actions(env)]
    if options:
        return "Retry with a currently valid operation such as " + ", ".join(options[:4]) + "."
    return (
        "No valid operation is currently available; reset the environment or inspect task policy."
    )


def _visible_metrics(observation: dict[str, Any]) -> dict[str, float]:
    metrics: dict[str, float] = {}
    for key in OBSERVATION_KEYS:
        value, observed = _observed_float(observation.get(key))
        if observed:
            metrics[key] = value
    return metrics


def _format_metric_map(metrics: dict[str, float], keys: tuple[str, ...]) -> str:
    parts = [f"{key}={metrics[key]:.3f}" for key in keys if key in metrics]
    return ", ".join(parts) if parts else "none"


def _instrument_summary(info: dict[str, Any]) -> dict[str, Any]:
    instrument = info.get("instrument_source") or info.get("instrument")
    return {
        "operation_type": info.get("operation_type"),
        "instrument": instrument,
        "is_measurement": info.get("operation_type") == "measure",
        "observed_keys": to_builtin(info.get("observed_keys", [])),
        "measurement_cost": _safe_float(info.get("measurement_cost"), default=0.0),
        "sample_consumed": _safe_float(info.get("sample_consumed"), default=0.0),
        "reward_source": info.get("reward_source"),
    }


def _final_assay_summary(info: dict[str, Any], campaign: dict[str, Any]) -> dict[str, Any]:
    instrument = info.get("instrument_source") or info.get("instrument")
    is_final_assay = info.get("operation_type") == "measure" and instrument == "final_assay"
    leaderboard_score = info.get("leaderboard_score")
    return {
        "is_final_assay": is_final_assay,
        "leaderboard_score": (
            None if leaderboard_score is None else _safe_float(leaderboard_score)
        ),
        "leaderboard_eligible": bool(is_final_assay and leaderboard_score is not None),
        "experiment_ended": bool(info.get("experiment_ended", False)),
        "episode_done": bool(campaign.get("done", False)),
        "final_assay_count": campaign.get("final_assay_count", 0),
        "last_terminal_summary": to_builtin(campaign.get("last_terminal_summary")),
    }


def _campaign_progress(campaign: dict[str, Any]) -> dict[str, Any]:
    budget = max(int(campaign.get("budget") or 0), 0)
    operation_count = max(int(campaign.get("operation_count") or 0), 0)
    remaining = max(int(campaign.get("remaining_budget") or 0), 0)
    progress_fraction = operation_count / budget if budget > 0 else 0.0
    best_score = campaign.get("best_score")
    return {
        "campaign_id": campaign.get("campaign_id"),
        "task_id": campaign.get("task_id"),
        "episode_mode": campaign.get("episode_mode"),
        "experiment_index": campaign.get("experiment_index"),
        "operation_count": operation_count,
        "budget": budget,
        "remaining_budget": remaining,
        "progress_fraction": progress_fraction,
        "final_assay_count": campaign.get("final_assay_count", 0),
        "best_score": None if best_score is None else _safe_float(best_score),
        "done": bool(campaign.get("done", False)),
    }


def _failure_summary(info: dict[str, Any]) -> dict[str, Any]:
    flags = info.get("constraint_flags", {})
    preconditions = info.get("preconditions", {})
    failed_preconditions = [
        str(key) for key, passed in preconditions.items() if isinstance(passed, bool) and not passed
    ]
    return {
        "precondition_failed": bool(flags.get("precondition_failed", False)),
        "constitution_failed": bool(flags.get("constitution_failed", False)),
        "transaction_status": info.get("transaction_status"),
        "rollback_reason": info.get("rollback_reason"),
        "error_message": info.get("error_message"),
        "failed_preconditions": failed_preconditions,
    }


def _next_action_hints(env: Any, *, limit: int = 5) -> list[str]:
    return [entry["operation"] for entry in available_actions(env)[:limit]]


def lab_report_view(env: Any, observation: dict[str, Any], info: dict[str, Any]) -> dict[str, Any]:
    """Return a compact public lab report for LLMs and students."""

    summary = spectra_summary(info)
    campaign = campaign_state(env)
    progress = _campaign_progress(campaign)
    metrics = _visible_metrics(observation)
    instrument = _instrument_summary(info)
    final_assay = _final_assay_summary(info, campaign)
    failure = _failure_summary(info)
    score = _safe_float(observation.get("score"), default=0.0)
    cost = _safe_float(observation.get("cost"), default=0.0)
    risk = _safe_float(observation.get("safety_risk"), default=0.0)
    failed = failure["precondition_failed"]
    status = "failed_precondition" if failed else "accepted"
    lines = [
        f"Operation {info.get('operation_type') or 'none'} was {status}.",
        f"Visible score={score:.3f}, cost={cost:.3f}, safety_risk={risk:.3f}.",
        (
            "Key public metrics: "
            + _format_metric_map(
                metrics,
                (
                    "yield",
                    "selectivity",
                    "conversion",
                    "purity",
                    "recovery",
                    "phase_ratio",
                    "pH_normalized",
                    "acid_dissociation_fraction",
                    "precipitation_signal",
                    "equilibrium_residual",
                    "equilibrium_confidence",
                    "score",
                ),
            )
            + "."
        ),
        f"Observed keys: {', '.join(summary['observed_keys']) or 'none'}.",
        (
            f"Campaign progress: step {progress['operation_count']}/{progress['budget']}, "
            f"experiment {progress['experiment_index']}, "
            f"remaining {progress['remaining_budget']}, "
            f"final_assays {progress['final_assay_count']}."
        ),
    ]
    if instrument["instrument"] is not None:
        lines.append(
            f"Instrument: {instrument['instrument']} "
            f"(measurement_cost={instrument['measurement_cost']:.3f}, "
            f"sample={instrument['sample_consumed']:.6f})."
        )
    if final_assay["is_final_assay"]:
        score_text = (
            "none"
            if final_assay["leaderboard_score"] is None
            else f"{float(final_assay['leaderboard_score']):.3f}"
        )
        lines.append(
            "Final assay: leaderboard_eligible="
            f"{final_assay['leaderboard_eligible']}, score={score_text}."
        )
    if summary["has_spectral_packet"]:
        channels = ", ".join(summary["channels"]) or "public peaks"
        lines.append(
            f"Spectra packet: {summary['packet_kind'] or 'instrument_signal'} "
            f"with {summary['channel_count']} channels ({channels})."
        )
    dominant = summary["dominant_peak"]
    if dominant["group"] is not None:
        lines.append(
            f"Dominant public spectral group: {dominant['group']} "
            f"({float(dominant['fraction']):.2f})."
        )
    if summary["warnings"]:
        lines.append("Spectral warnings: " + ", ".join(summary["warnings"]) + ".")
    recovery = _recovery_suggestion(env, info)
    if recovery is not None:
        lines.append(f"Recovery suggestion: {recovery}")
    if campaign["best_score"] is not None:
        lines.append(f"Best score so far: {float(campaign['best_score']):.3f}.")
    return {
        "mode": "lab_report",
        "report_version": "chemworld-lab-report-0.2",
        "text": "\n".join(lines),
        "status": status,
        "operation_type": info.get("operation_type"),
        "visible_metrics": metrics,
        "instrument_summary": instrument,
        "final_assay_summary": final_assay,
        "spectra_summary": summary,
        "campaign_state": campaign,
        "campaign_progress": progress,
        "failure_summary": failure,
        "next_action_hints": _next_action_hints(env),
        "recovery_suggestion": recovery,
        "constraint_flags": to_builtin(info.get("constraint_flags", {})),
    }


def tool_json_view(env: Any, observation: dict[str, Any], info: dict[str, Any]) -> dict[str, Any]:
    """Return a structured public observation bundle for tool agents."""

    return {
        "mode": "tool_json",
        "task": {
            "task_id": getattr(_base_env(env), "task_id", None),
            "objective": getattr(_base_env(env), "objective", None),
        },
        "observation": to_builtin(observation),
        "raw_signal": to_builtin(info.get("raw_signal", {})),
        "processed_estimate": to_builtin(info.get("processed_estimate", {})),
        "uncertainty": to_builtin(info.get("uncertainty", {})),
        "observed_keys": to_builtin(info.get("observed_keys", [])),
        "observed_mask": to_builtin(info.get("observed_mask", {})),
        "cost": _safe_float(info.get("cost"), default=0.0),
        "cost_components": to_builtin(info.get("cost_components", {})),
        "constraints": to_builtin(info.get("constraint_flags", {})),
        "campaign_state": campaign_state(env),
        "available_actions": available_actions(env),
        "lab_report": lab_report_view(env, observation, info),
    }


def observation_view(
    env: Any,
    mode: str = "tool_json",
    observation: dict[str, Any] | None = None,
    info: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Return an agent-facing observation view."""

    base = _base_env(env)
    obs = _latest_observation(base) if observation is None else observation
    step_info = _latest_info(base) if info is None else info
    if mode == "rl":
        return rl_observation_view(obs, step_info)
    if mode == "tool_json":
        return tool_json_view(base, obs, step_info)
    if mode == "lab_report":
        return lab_report_view(base, obs, step_info)
    raise ValueError("mode must be one of 'rl', 'tool_json', or 'lab_report'")


def agent_view_bundle(
    env: Any,
    observation: dict[str, Any],
    info: dict[str, Any],
) -> dict[str, Any]:
    """Return all standard agent-facing views for trajectory export."""

    return {
        "rl": observation_view(env, "rl", observation, info),
        "tool_json": observation_view(env, "tool_json", observation, info),
        "lab_report": observation_view(env, "lab_report", observation, info),
    }


__all__ = [
    "action_schema",
    "agent_view_bundle",
    "available_actions",
    "campaign_state",
    "lab_report_view",
    "observation_view",
    "rl_observation_spec",
    "rl_observation_view",
    "spectra_summary",
    "task_prompt",
    "tool_json_view",
    "validate_action",
]
