"""Leakage-resistant training reward and behavioral-completion contracts."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Iterable
from typing import Any

REWARD_SCHEMA_VERSION = "chemworld-rl-training-reward-0.3"

REWARD_COMPONENTS = {
    "raw_environment_reward": 1.0,
    "valid_nonterminal_operation": 0.0,
    "invalid_precondition": -0.25,
    "newly_unlocked_operation": 0.02,
    # A small, one-shot progress signal prevents sparse-reward policies from
    # learning to repeat a legal operation forever. Requirements are derived
    # solely from the published task operation contract, never hidden world
    # state or the benchmark objective, and repeated operations earn nothing.
    "newly_satisfied_core_requirement": 0.10,
    "behavioral_core_completion": 1.0,
    "measurement": 0.0,
    "experiment_ended": 0.0,
    "quick_close_incomplete": -0.50,
    "unsafe_step": -0.10,
    "high_cost_step": -0.05,
}


def core_operation_requirements(
    allowed_operations: Iterable[str],
) -> tuple[tuple[str, ...], ...]:
    """Derive observable behavior requirements from the task operation slice.

    Each inner tuple is an alternatives group; every group must be satisfied.
    This is deliberately based on the public task contract, not hidden state.
    """

    allowed = set(allowed_operations)
    groups: list[tuple[str, ...]] = []
    if "run_flow" in allowed:
        groups.extend((("set_flow_rate",), ("run_flow",)))
    elif "electrolyze" in allowed:
        groups.extend((("set_potential",), ("electrolyze",)))
    elif {"heat", "wait"}.intersection(allowed):
        groups.append(tuple(item for item in ("heat", "wait") if item in allowed))

    if "cool_crystallize" in allowed:
        groups.extend((("cool_crystallize",), ("filter_crystals",)))
    if "distill" in allowed:
        groups.extend((("distill",), ("collect_fraction",)))
    if "mix" in allowed:
        groups.extend((("mix",), ("settle",), ("separate_phase",)))
    return tuple(groups)


def satisfied_requirement_count(
    requirements: tuple[tuple[str, ...], ...],
    executed_operations: set[str],
) -> int:
    return sum(bool(set(group).intersection(executed_operations)) for group in requirements)


def reward_contract(allowed_operations: Iterable[str]) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "schema_version": REWARD_SCHEMA_VERSION,
        "public_signals_only": True,
        "benchmark_evaluation_uses_shaped_reward": False,
        "components": dict(REWARD_COMPONENTS),
        "behavioral_completion": {
            "requirements": [
                list(group) for group in core_operation_requirements(allowed_operations)
            ],
            "all_requirements_must_be_satisfied": True,
            "experiment_end_without_core_behavior": "quick_close_incomplete",
        },
        "leakage_controls": {
            "terminal_bonus": False,
            "measurement_bonus": False,
            "core_progress_uses_public_operation_history_only": True,
            "repeated_core_operation_bonus": False,
            "raw_benchmark_reward_preserved": True,
        },
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    payload["contract_hash"] = hashlib.sha256(encoded).hexdigest()
    return payload


__all__ = [
    "REWARD_COMPONENTS",
    "REWARD_SCHEMA_VERSION",
    "core_operation_requirements",
    "reward_contract",
    "satisfied_requirement_count",
]
