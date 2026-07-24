"""Bounded, decision-first prompt representation for live benchmark agents."""

from __future__ import annotations

import json
import math
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any

from chemworld.data.logging import to_builtin

PROMPT_CONTEXT_VERSION = "chemworld-compact-decision-context-0.2"
DEFAULT_PROMPT_TOKEN_ESTIMATE_CAP = 1500

_TASK_KEYS = (
    "task_id",
    "task_goal",
    "objective",
    "description",
    "budget",
    "episode_mode",
    "safety_limit",
    "success_metrics",
    "termination_policy",
)
_LIFECYCLE_KEYS = (
    "fresh_experiment_precondition",
    "terminate_effect",
    "final_assay_precondition",
    "final_assay_effect",
)
_STATE_KEYS = (
    "experiment_index",
    "remaining_budget",
    "remaining_experiments",
    "remaining_operations",
    "cost",
    "risk",
    "score",
    "leaderboard_score",
    "temperature_K",
    "pressure_Pa",
    "elapsed_time_s",
    "solvent",
    "electrolyte_profile",
    "catalyst",
    "catalyst_amount_mol",
)
_PEAK_FIELDS = (
    "spectrum_id",
    "instrument",
    "kind",
    "assignment",
    "center",
    "retention_time",
    "retention_time_min",
    "chemical_shift",
    "wavelength",
    "wavenumber",
    "area",
    "height",
    "width",
    "fraction",
    "concentration",
    "concentration_mol_L",
)
_SKIPPED_ARRAY_KEYS = frozenset(
    {
        "axis",
        "axes",
        "intensity",
        "intensities",
        "replicate_signals",
        "signal",
        "signals",
        "values",
    }
)


class PromptBudgetExceededError(ValueError):
    """The public decision state cannot fit without dropping required fields."""


@dataclass(frozen=True)
class PromptPacket:
    payload: dict[str, Any]
    text: str
    estimated_tokens: int
    max_estimated_tokens: int


def build_decision_prompt(
    *,
    task_contract: Mapping[str, Any],
    decision_context: Mapping[str, Any],
    tool_json: Mapping[str, Any],
    experiment_memory: Sequence[Mapping[str, Any]],
    recent_decisions: Sequence[Mapping[str, Any]],
    max_estimated_tokens: int = DEFAULT_PROMPT_TOKEN_ESTIMATE_CAP,
) -> PromptPacket:
    """Return one compact prompt without raw arrays or duplicated public views."""

    if max_estimated_tokens < 500:
        raise ValueError("prompt token estimate cap must be at least 500")
    state_raw = decision_context.get("campaign_state", {})
    state = state_raw if isinstance(state_raw, Mapping) else {}
    actions = tool_json.get("available_actions", [])
    payload: dict[str, Any] = {
        "representation_version": PROMPT_CONTEXT_VERSION,
        "instruction": (
            "Choose one legal next operation from the compact public state. Declare "
            "which outcome would support or weaken the diagnostic target. Request a "
            "historical spectrum only when its detail can change the decision. The "
            "harness does not repair, terminate, or assay on your behalf."
        ),
        "task": _compact_task_contract(task_contract),
        "decision_state": {
            "step": decision_context.get("step"),
            "stage": decision_context.get("decision_stage"),
            "remaining_operations": decision_context.get(
                "remaining_operations",
                state.get("remaining_budget"),
            ),
            "current_experiment": _pick_compact(state, _STATE_KEYS),
            "latest_metrics": _compact_scalar_mapping(
                decision_context.get("visible_metrics", {})
            ),
            "latest_measurement": summarize_measurement(
                decision_context.get("latest_spectra", {})
            ),
            "requested_historical_measurement": summarize_measurement(
                decision_context.get("requested_historical_spectrum", {})
            ),
            "active_constraint_flags": _active_flags(
                decision_context.get("constraint_flags", {})
            ),
            "uncertainty": _compact_scalar_mapping(
                decision_context.get("uncertainty", {})
            ),
            "observation_provenance": _pick_compact(
                _mapping(decision_context.get("observation_provenance")),
                (
                    "current_event_type",
                    "current_spectral_packet",
                    "latest_cataloged_spectrum_id",
                    "latest_spectrum_measurement_step",
                    "operations_since_latest_spectrum",
                ),
            ),
        },
        "experiment_memory": compact_experiment_memory(experiment_memory),
        "recent_decisions": [
            compact_decision(item) for item in recent_decisions[-2:]
        ],
        "legal_actions": [
            compact_action(item)
            for item in actions
            if isinstance(item, Mapping) and item.get("operation")
        ]
        if isinstance(actions, list)
        else [],
        "on_demand_detail": {
            "historical_spectrum": (
                "set request_historical_spectrum_id to a supplied public spectrum_id"
            ),
            "historical_spectrum_catalog": _compact_spectrum_catalog(
                decision_context.get("historical_spectrum_catalog", ())
            ),
        },
        "required_json_shape": {
            "action": {"operation": "one legal operation plus required parameters"},
            "expected_effect": "one concise testable expectation",
            "diagnostic_target": "candidate relation or exploitation objective",
            "expected_information_gain": "unitless forecast in [0,1]",
            "belief_update_rule": {
                "if_supported": "belief or next-step change",
                "if_not_supported": "belief or next-step change",
            },
            "uncertainty": "number in [0,1]",
            "request_historical_spectrum_id": (
                "public spectrum_id needed next, or null"
            ),
        },
        "context_manifest": {
            "raw_numeric_arrays": "audit_only_not_supplied",
            "duplicate_observation_views": "not_supplied",
            "provider_repository_and_ledger_metadata": "audit_only_not_supplied",
            "constitution_checks": "audit_only_not_supplied",
            "memory_policy": "historical_best_plus_two_most_recent",
            "recent_decision_count": min(len(recent_decisions), 2),
            "max_estimated_tokens": max_estimated_tokens,
        },
    }
    return serialize_prompt_payload(payload, max_estimated_tokens=max_estimated_tokens)


def serialize_prompt_payload(
    payload: Mapping[str, Any],
    *,
    max_estimated_tokens: int,
) -> PromptPacket:
    """Serialize under a hard cap; never silently remove required action fields."""

    mutable = to_builtin(dict(payload))
    text = _canonical_json(mutable)
    estimate = estimate_prompt_tokens(text)
    if estimate > max_estimated_tokens:
        mutable["recent_decisions"] = list(mutable.get("recent_decisions", []))[-1:]
        state = mutable.get("decision_state")
        if isinstance(state, dict):
            state["uncertainty"] = {}
            for measurement_key in (
                "latest_measurement",
                "requested_historical_measurement",
            ):
                measurement = state.get(measurement_key)
                if isinstance(measurement, dict) and isinstance(
                    measurement.get("peaks"), list
                ):
                    measurement["peaks"] = measurement["peaks"][:4]
                    measurement["peak_summary_truncated"] = True
        manifest = mutable.get("context_manifest")
        if isinstance(manifest, dict):
            manifest["fixed_budget_reduction_applied"] = True
        text = _canonical_json(mutable)
        estimate = estimate_prompt_tokens(text)
    if estimate > max_estimated_tokens:
        raise PromptBudgetExceededError(
            f"compact prompt estimate {estimate} exceeds cap "
            f"{max_estimated_tokens}; revise the public representation explicitly"
        )
    return PromptPacket(
        payload=mutable,
        text=text,
        estimated_tokens=estimate,
        max_estimated_tokens=max_estimated_tokens,
    )


def estimate_prompt_tokens(text: str) -> int:
    """Conservative tokenizer-independent estimate for mixed-language JSON."""

    return math.ceil(len(text.encode("utf-8")) / 4)


def summarize_measurement(value: Any) -> dict[str, Any]:
    if not isinstance(value, Mapping) or not value:
        return {"available": False}
    if value.get("has_spectral_packet") is False:
        return {"available": False}
    masked = value.get("spectrum_condition") == "masked"
    summary: dict[str, Any] = {
        "available": False
        if masked
        else bool(value.get("has_spectral_packet", True)),
    }
    for key in (
        "spectrum_id",
        "instrument",
        "kind",
        "measurement_step",
        "spectrum_condition",
    ):
        if _is_compact_value(value.get(key)):
            summary[key] = to_builtin(value[key])
    peaks: list[dict[str, Any]] = []
    _collect_peaks(value, peaks)
    if peaks:
        summary["peaks"] = peaks[:8]
        summary["peak_count_supplied"] = min(len(peaks), 8)
    processed = value.get("processed_estimate")
    if isinstance(processed, Mapping):
        summary["processed_estimate"] = _compact_scalar_mapping(
            processed,
            limit=16,
        )
    raw = value.get("raw_signal")
    if isinstance(raw, Mapping):
        for key in ("spectrum_id", "instrument", "kind"):
            if key not in summary and _is_compact_value(raw.get(key)):
                summary[key] = to_builtin(raw[key])
        non_spectral = _compact_nested_scalars(raw)
        if non_spectral:
            summary["non_spectral_estimate"] = non_spectral
    if summary["available"]:
        summary["raw_signal"] = "available_by_public_spectrum_id_not_in_prompt"
    return summary


def compact_experiment_memory(
    memory: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    if not memory:
        return {"historical_best": None, "recent": []}
    scored = [
        item
        for item in memory
        if _numeric_score(item) is not None
    ]
    best = (
        max(scored, key=lambda item: float(_numeric_score(item) or 0.0))
        if scored
        else memory[-1]
    )
    return {
        "historical_best": _compact_experiment(best),
        "recent": [_compact_experiment(item) for item in memory[-2:]],
    }


def compact_decision(item: Mapping[str, Any]) -> dict[str, Any]:
    action = item.get("action")
    compact = {
        "action": to_builtin(dict(action)) if isinstance(action, Mapping) else {},
    }
    compact.update(
        _pick_compact(
            item,
            (
                "expected_effect",
                "diagnostic_target",
                "observed_effect",
                "uncertainty",
                "request_historical_spectrum_id",
                "status",
            ),
        )
    )
    return compact


def compact_action(item: Mapping[str, Any]) -> dict[str, Any]:
    compact: dict[str, Any] = {"operation": item.get("operation")}
    if item.get("valid") is False:
        compact["currently_valid"] = False
        reasons = item.get("invalid_reasons")
        if isinstance(reasons, list):
            compact["invalid_reasons"] = [
                str(reason) for reason in reasons[:4]
            ]
    schema = item.get("schema")
    if not isinstance(schema, Mapping):
        return compact
    required_raw = schema.get("required_fields", [])
    required = set(required_raw) if isinstance(required_raw, list) else set()
    fields = schema.get("fields")
    parameters: list[dict[str, Any]] = []
    if isinstance(fields, list):
        for field in fields:
            if not isinstance(field, Mapping):
                continue
            name = field.get("field", field.get("name"))
            if not isinstance(name, str) or not name:
                continue
            parameter = {"field": name, "required": name in required}
            parameter.update(
                _pick_compact(
                    field,
                    (
                        "minimum",
                        "maximum",
                        "min",
                        "max",
                        "unit",
                        "choices",
                        "default",
                    ),
                )
            )
            parameters.append(parameter)
    if parameters:
        compact["parameters"] = parameters
    return compact


def _compact_task_contract(task_contract: Mapping[str, Any]) -> dict[str, Any]:
    compact = _pick_compact(task_contract, _TASK_KEYS)
    method_budget = task_contract.get("method_budget_contract")
    if isinstance(method_budget, Mapping):
        compact["method_budget_contract"] = _compact_scalar_mapping(
            method_budget,
            limit=8,
        )
    lifecycle = task_contract.get("experiment_lifecycle")
    if isinstance(lifecycle, Mapping):
        compact["experiment_lifecycle"] = _pick_compact(
            lifecycle,
            _LIFECYCLE_KEYS,
        )
    return compact


def _compact_spectrum_catalog(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list | tuple):
        return []
    result: list[dict[str, Any]] = []
    for item in value[-8:]:
        if not isinstance(item, Mapping):
            continue
        compact = _pick_compact(
            item,
            (
                "spectrum_id",
                "instrument",
                "kind",
                "measurement_step",
                "experiment_index",
            ),
        )
        if compact.get("spectrum_id"):
            result.append(compact)
    return result


def _compact_experiment(item: Mapping[str, Any]) -> dict[str, Any]:
    compact = _pick_compact(
        item,
        (
            "experiment_index",
            "score",
            "leaderboard_score",
            "yield",
            "selectivity",
            "cost",
            "risk",
            "outcome",
        ),
    )
    visible = item.get("visible_metrics")
    if isinstance(visible, Mapping):
        compact["visible_metrics"] = _compact_scalar_mapping(visible, limit=12)
    flags = item.get("constraint_flags")
    if isinstance(flags, Mapping):
        compact["active_constraint_flags"] = _active_flags(flags)
    operations = item.get("operation_sequence", item.get("actions", []))
    if isinstance(operations, list):
        compact["operations"] = [
            str(operation.get("operation"))
            for operation in operations[-8:]
            if isinstance(operation, Mapping) and operation.get("operation")
        ]
    return compact


def _numeric_score(item: Mapping[str, Any]) -> float | None:
    for key in ("score", "leaderboard_score"):
        value = item.get(key)
        if isinstance(value, int | float) and not isinstance(value, bool):
            return float(value)
    return None


def _collect_peaks(value: Any, output: list[dict[str, Any]]) -> None:
    if len(output) >= 16:
        return
    if isinstance(value, Mapping):
        for key, item in value.items():
            if str(key).lower() in _SKIPPED_ARRAY_KEYS:
                continue
            if key == "peaks" and isinstance(item, list):
                for peak in item:
                    if isinstance(peak, Mapping):
                        row = _pick_compact(peak, _PEAK_FIELDS)
                        if row:
                            output.append(row)
                continue
            _collect_peaks(item, output)
    elif isinstance(value, list) and len(value) <= 16:
        for item in value:
            _collect_peaks(item, output)


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _pick_compact(
    source: Mapping[str, Any],
    keys: Sequence[str],
) -> dict[str, Any]:
    return {
        key: to_builtin(source[key])
        for key in keys
        if key in source and _is_compact_value(source[key])
    }


def _compact_scalar_mapping(value: Any, *, limit: int = 20) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        return {}
    compact: dict[str, Any] = {}
    for key in sorted(value):
        item = value[key]
        if _is_compact_value(item):
            compact[str(key)] = to_builtin(item)
        if len(compact) >= limit:
            break
    return compact


def _compact_nested_scalars(
    value: Mapping[str, Any],
    *,
    depth: int = 0,
    limit: int = 12,
) -> dict[str, Any]:
    if depth > 1:
        return {}
    compact: dict[str, Any] = {}
    for key in sorted(value):
        if str(key).lower() in _SKIPPED_ARRAY_KEYS or key == "peaks":
            continue
        item = value[key]
        if _is_compact_value(item):
            compact[str(key)] = to_builtin(item)
        elif isinstance(item, Mapping):
            nested = _compact_nested_scalars(item, depth=depth + 1, limit=limit)
            if nested:
                compact[str(key)] = nested
        if len(compact) >= limit:
            break
    return compact


def _active_flags(value: Any) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        return {}
    return {
        str(key): to_builtin(item)
        for key, item in value.items()
        if item not in (None, False, 0, "", [], {}) and _is_compact_value(item)
    }


def _is_compact_value(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, bool | int | float):
        return True
    if isinstance(value, str):
        return len(value) <= 400
    if isinstance(value, list | tuple):
        return len(value) <= 12 and all(_is_compact_value(item) for item in value)
    return False


def _canonical_json(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


__all__ = [
    "DEFAULT_PROMPT_TOKEN_ESTIMATE_CAP",
    "PROMPT_CONTEXT_VERSION",
    "PromptBudgetExceededError",
    "PromptPacket",
    "build_decision_prompt",
    "compact_action",
    "compact_decision",
    "compact_experiment_memory",
    "estimate_prompt_tokens",
    "serialize_prompt_payload",
    "summarize_measurement",
]
