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
from chemworld.world.actions import CATALYSTS, SOLVENTS
from chemworld.world.operations import INSTRUMENTS, OPERATION_TYPES, operation_contracts

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
    "phase": ["aqueous", "organic", "solid"],
    "target_phase": ["aqueous", "organic", "solid"],
    "extractant": ["organic", "aqueous", "toluene", "ethyl_acetate"],
}


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


def _field_schema(field: str) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "field": field,
        "unit": FIELD_UNITS.get(field, "unitless"),
        "required": True,
    }
    if field in FIELD_RANGES:
        low, high = FIELD_RANGES[field]
        payload["bounds"] = {"low": low, "high": high}
        payload["recommended_range"] = {"low": low, "high": high}
    if field in FIELD_CHOICES:
        payload["choices"] = FIELD_CHOICES[field]
    return payload


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
    fields = [_field_schema(field) for field in contract.required_fields]
    if operation == "measure":
        fields = [
            {
                **_field_schema("instrument"),
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


def task_prompt(env: Any) -> dict[str, Any]:
    """Build a natural-language task prompt plus structured task facts."""

    base = _base_env(env)
    info = base.task_info()
    success_metrics = list(info.get("scoring_contract", {}).get("success_metrics", []))
    lines = [
        f"Task: {info.get('task_id') or 'ad-hoc ChemWorld task'}",
        f"Objective: {info.get('objective')} under a budget of {info.get('budget')} operations.",
        (
            "You control a partially observable virtual physical-chemical world. "
            "Hidden species amounts, kinetic parameters, partition coefficients, "
            "and mechanism internals are not directly observable."
        ),
        (
            "Use only the listed operations and instruments. Measurements are noisy, "
            "cost time/sample, and final_assay is the leaderboard scoring source."
        ),
        f"Allowed operations: {', '.join(info.get('allowed_operations', []))}.",
        f"Allowed instruments: {', '.join(info.get('allowed_instruments', []))}.",
        f"Success metrics: {', '.join(success_metrics) if success_metrics else 'task score'}.",
        (
            "Submit a valid trajectory with actions, observations, constraint flags, "
            "and any hypothesis or explanation fields required by the task."
        ),
    ]
    return {
        "text": "\n".join(lines),
        "task_id": info.get("task_id"),
        "objective": info.get("objective"),
        "budget": info.get("budget"),
        "episode_mode": info.get("episode_mode"),
        "allowed_operations": info.get("allowed_operations", []),
        "allowed_instruments": info.get("allowed_instruments", []),
        "success_metrics": success_metrics,
        "safety_limit": info.get("safety_limit"),
        "hidden_information_policy": (
            "No hidden species amounts, rate constants, mechanism parameters, or "
            "private scenario parameters are exposed through agent-facing views."
        ),
        "submission_requirements": [
            "trajectory JSONL",
            "agent manifest",
            "reproducible command or replay trace",
        ],
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
        values.append(value)
        mask.append(1.0 if observed else 0.0)
    if include_cost:
        values.append(_safe_float((info or {}).get("cost"), default=0.0))
        mask.append(1.0)
    return {
        "mode": "rl",
        "keys": [*OBSERVATION_KEYS, *(["cost_signal"] if include_cost else [])],
        "vector": values,
        "mask": mask,
        "cost": _safe_float((info or {}).get("cost"), default=0.0),
        "constraint_flags": to_builtin((info or {}).get("constraint_flags", {})),
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
        "No valid operation is currently available; reset the environment "
        "or inspect task policy."
    )


def lab_report_view(env: Any, observation: dict[str, Any], info: dict[str, Any]) -> dict[str, Any]:
    """Return a compact public lab report for LLMs and students."""

    summary = spectra_summary(info)
    campaign = campaign_state(env)
    score = _safe_float(observation.get("score"), default=0.0)
    cost = _safe_float(observation.get("cost"), default=0.0)
    risk = _safe_float(observation.get("safety_risk"), default=0.0)
    failed = bool(info.get("constraint_flags", {}).get("precondition_failed", False))
    status = "failed_precondition" if failed else "accepted"
    lines = [
        f"Operation {info.get('operation_type') or 'none'} was {status}.",
        f"Visible score={score:.3f}, cost={cost:.3f}, safety_risk={risk:.3f}.",
        f"Observed keys: {', '.join(summary['observed_keys']) or 'none'}.",
    ]
    dominant = summary["dominant_peak"]
    if dominant["group"] is not None:
        lines.append(
            f"Dominant public spectral group: {dominant['group']} "
            f"({float(dominant['fraction']):.2f})."
        )
    recovery = _recovery_suggestion(env, info)
    if recovery is not None:
        lines.append(f"Recovery suggestion: {recovery}")
    if campaign["best_score"] is not None:
        lines.append(f"Best campaign score so far: {float(campaign['best_score']):.3f}.")
    return {
        "mode": "lab_report",
        "text": "\n".join(lines),
        "status": status,
        "operation_type": info.get("operation_type"),
        "spectra_summary": summary,
        "campaign_state": campaign,
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
    "rl_observation_view",
    "spectra_summary",
    "task_prompt",
    "tool_json_view",
    "validate_action",
]
