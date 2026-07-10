"""Replay-derived audits of controlled comparisons in experiment campaigns."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from chemworld.data.logging import to_builtin

AUDIT_SCHEMA_VERSION = "chemworld-experiment-design-audit-0.1"
_CONDITION_OPERATIONS = {
    "add_solvent",
    "add_reagent",
    "add_catalyst",
    "heat",
    "wait",
}
_FACTOR_FIELDS: dict[str, tuple[str, tuple[str, ...]]] = {
    "solvent_charge": ("add_solvent", ("solvent", "volume_L")),
    "reagent_charge": ("add_reagent", ("amount_mol",)),
    "catalyst_charge": (
        "add_catalyst",
        ("catalyst", "catalyst_amount_mol"),
    ),
    "thermal_program": (
        "heat",
        ("target_temperature_K", "duration_s", "stirring_speed_rpm"),
    ),
    "wait_program": ("wait", ("duration_s", "stirring_speed_rpm")),
}


def audit_experiment_design(experiments: Iterable[dict[str, Any]]) -> dict[str, Any]:
    """Classify each completed experiment against its nearest prior condition set."""

    normalized = [_normalize_experiment(item, index) for index, item in enumerate(experiments)]
    comparisons: list[dict[str, Any]] = []
    for position, experiment in enumerate(normalized):
        if position == 0:
            comparisons.append(
                {
                    "experiment_index": experiment["experiment_index"],
                    "classification": "baseline",
                    "reference_experiment_index": None,
                    "changed_factor_count": 0,
                    "changed_factors": [],
                    "score_delta": None,
                }
            )
            continue
        reference, changes = _nearest_reference(experiment, normalized[:position])
        changed_count = len(changes)
        classification = (
            "replication"
            if changed_count == 0
            else "controlled_single_factor"
            if changed_count == 1
            else "multi_factor_change"
        )
        score_delta = None
        if experiment["final_score"] is not None and reference["final_score"] is not None:
            score_delta = float(experiment["final_score"]) - float(reference["final_score"])
        comparisons.append(
            {
                "experiment_index": experiment["experiment_index"],
                "classification": classification,
                "reference_experiment_index": reference["experiment_index"],
                "changed_factor_count": changed_count,
                "changed_factors": changes,
                "score_delta": score_delta,
            }
        )

    nonbaseline = comparisons[1:]
    controlled = sum(item["classification"] == "controlled_single_factor" for item in nonbaseline)
    multi_factor = sum(item["classification"] == "multi_factor_change" for item in nonbaseline)
    replications = sum(item["classification"] == "replication" for item in nonbaseline)
    denominator = len(nonbaseline)
    unique_conditions = {_freeze(item["condition_signature"]) for item in normalized}
    return {
        "schema_version": AUDIT_SCHEMA_VERSION,
        "experiment_count": len(normalized),
        "comparison_count": denominator,
        "controlled_single_factor_count": controlled,
        "multi_factor_change_count": multi_factor,
        "replication_count": replications,
        "unique_condition_count": len(unique_conditions),
        "controlled_comparison_rate": controlled / denominator if denominator else None,
        "multi_factor_change_rate": multi_factor / denominator if denominator else None,
        "comparisons": to_builtin(comparisons),
    }


def experiments_from_trajectory(records: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    """Recover completed experiment condition sets from replayable trajectory rows."""

    experiments: list[dict[str, Any]] = []
    conditions: list[dict[str, Any]] = []
    for record in records:
        action = dict(record.get("action") or {})
        if action.get("operation") in _CONDITION_OPERATIONS:
            conditions.append(action)
        score = record.get("leaderboard_score")
        if score is None:
            continue
        experiments.append(
            {
                "experiment_index": int(record.get("experiment_index", len(experiments))),
                "final_score": float(score),
                "conditions": list(conditions),
            }
        )
        conditions = []
    return experiments


def _normalize_experiment(item: dict[str, Any], fallback_index: int) -> dict[str, Any]:
    conditions = [
        dict(action)
        for action in item.get("conditions", [])
        if isinstance(action, dict) and action.get("operation") in _CONDITION_OPERATIONS
    ]
    return {
        "experiment_index": int(item.get("experiment_index", fallback_index)),
        "final_score": (
            float(item["final_score"]) if item.get("final_score") is not None else None
        ),
        "condition_signature": _condition_signature(conditions),
    }


def _condition_signature(conditions: list[dict[str, Any]]) -> dict[str, Any]:
    signature: dict[str, Any] = {}
    for factor, (operation, fields) in _FACTOR_FIELDS.items():
        steps = []
        for action in conditions:
            if action.get("operation") != operation:
                continue
            steps.append(
                {field: _normalized_value(action.get(field)) for field in fields if field in action}
            )
        signature[factor] = steps
    return signature


def _nearest_reference(
    experiment: dict[str, Any],
    priors: list[dict[str, Any]],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    ranked: list[tuple[int, int, dict[str, Any], list[dict[str, Any]]]] = []
    for recency, prior in enumerate(priors):
        changes = _factor_changes(
            prior["condition_signature"],
            experiment["condition_signature"],
        )
        ranked.append((len(changes), -recency, prior, changes))
    _, _, reference, changes = min(ranked, key=lambda item: (item[0], item[1]))
    return reference, changes


def _factor_changes(previous: dict[str, Any], current: dict[str, Any]) -> list[dict[str, Any]]:
    changes = []
    for factor in _FACTOR_FIELDS:
        if previous.get(factor) == current.get(factor):
            continue
        changes.append(
            {
                "factor": factor,
                "previous": previous.get(factor),
                "current": current.get(factor),
            }
        )
    return changes


def _normalized_value(value: Any) -> Any:
    if isinstance(value, float):
        return round(value, 10)
    return value


def _freeze(value: Any) -> Any:
    if isinstance(value, dict):
        return tuple((key, _freeze(item)) for key, item in sorted(value.items()))
    if isinstance(value, list):
        return tuple(_freeze(item) for item in value)
    return value


__all__ = [
    "AUDIT_SCHEMA_VERSION",
    "audit_experiment_design",
    "experiments_from_trajectory",
]
