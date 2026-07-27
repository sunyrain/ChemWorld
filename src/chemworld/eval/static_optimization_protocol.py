"""Shared protocol semantics for fixed-world scientific optimization."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from chemworld.physchem.electrochemical_task_contract import (
    ELECTROCHEMICAL_WORKFLOW_STATIC_SINGLE_STAGE,
    normalize_electrochemical_workflow_mode,
)

STATIC_WORLD_MODE = "static_for_entire_campaign"
ELECTROCHEMICAL_TASK_ID = "electrochemical-conversion"


def exploration_experiment_count(protocol: Mapping[str, Any]) -> int:
    """Return the number of complete experiments in the visible S0 campaign."""

    legacy_horizon = protocol.get("horizon")
    campaign = protocol.get("scientific_campaign_budget")
    if isinstance(campaign, Mapping) and "exploration_experiments" in campaign:
        count = _positive_int(
            campaign["exploration_experiments"],
            "scientific_campaign_budget.exploration_experiments",
        )
        if legacy_horizon is not None and _positive_int(legacy_horizon, "horizon") != count:
            raise ValueError(
                "S0 horizon and scientific campaign exploration budget disagree"
            )
        return count
    return _positive_int(legacy_horizon, "horizon")


def static_optimization_workflow_mode(protocol: Mapping[str, Any]) -> str:
    """Return the explicit electrochemical workflow mode for an S0 protocol.

    Non-electrochemical tasks use the single-stage value as an inert executor
    setting. Electrochemical protocols must state their workflow explicitly so
    an omitted field cannot silently revive the historical two-stage recipe.
    """

    tasks = protocol.get("tasks")
    task_ids = (
        {str(item) for item in tasks}
        if isinstance(tasks, list | tuple)
        else set()
    )
    executor = protocol.get("executor_contract")
    raw_mode = (
        executor.get("electrochemical_workflow_mode")
        if isinstance(executor, Mapping)
        else None
    )
    if ELECTROCHEMICAL_TASK_ID in task_ids and raw_mode is None:
        raise ValueError(
            "electrochemical S0 protocols must explicitly declare "
            "executor_contract.electrochemical_workflow_mode"
        )
    if raw_mode is None:
        return ELECTROCHEMICAL_WORKFLOW_STATIC_SINGLE_STAGE
    return normalize_electrochemical_workflow_mode(str(raw_mode))


def validate_static_optimization_protocol(protocol: Mapping[str, Any]) -> None:
    """Reject ambiguous or non-static protocols before an S0 run starts."""

    tasks = protocol.get("tasks")
    if not isinstance(tasks, list) or not tasks or not all(
        isinstance(item, str) and item for item in tasks
    ):
        raise ValueError("S0 protocol tasks must be a non-empty string list")
    world_policy = protocol.get("world_policy")
    if not isinstance(world_policy, Mapping):
        raise ValueError("S0 protocol lacks world_policy")
    if world_policy.get("mode") != STATIC_WORLD_MODE:
        raise ValueError("S0 runner accepts only a static world policy")
    if list(world_policy.get("interventions", [])):
        raise ValueError("S0 runner rejects world interventions")
    if list(world_policy.get("phase_changes", [])):
        raise ValueError("S0 runner rejects phase changes")
    if world_policy.get("hidden_world_fields_in_public_context") is not False:
        raise ValueError("S0 protocol must hide private world fields")
    exploration_experiment_count(protocol)
    static_optimization_workflow_mode(protocol)

    campaign = protocol.get("scientific_campaign_budget")
    final_synthesis = protocol.get("final_synthesis")
    if isinstance(campaign, Mapping) and "final_synthesis_after_exploration" in campaign:
        expected = bool(campaign["final_synthesis_after_exploration"])
        actual = bool(
            final_synthesis.get("enabled", False)
            if isinstance(final_synthesis, Mapping)
            else False
        )
        if expected != actual:
            raise ValueError(
                "scientific campaign and final synthesis contracts disagree"
            )


def _positive_int(value: object, field: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{field} must be a positive integer")
    if value <= 0:
        raise ValueError(f"{field} must be a positive integer")
    return value


__all__ = [
    "ELECTROCHEMICAL_TASK_ID",
    "STATIC_WORLD_MODE",
    "exploration_experiment_count",
    "static_optimization_workflow_mode",
    "validate_static_optimization_protocol",
]
