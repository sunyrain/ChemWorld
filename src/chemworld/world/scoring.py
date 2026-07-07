"""Task-aware scoring helpers for ChemWorld."""

from __future__ import annotations

from typing import Any

import numpy as np


def scalar_observation(observation: dict[str, Any], key: str, default: float = 0.0) -> float:
    value = observation.get(key)
    if value is None:
        return default
    if hasattr(value, "reshape"):
        value = value.reshape(-1)[0]
    return float(value)


def reaction_score(observation: dict[str, Any]) -> float:
    return scalar_observation(observation, "score")


def purification_score(observation: dict[str, Any]) -> float:
    purity = scalar_observation(observation, "purity")
    recovery = scalar_observation(observation, "recovery")
    mass_balance_error = scalar_observation(observation, "process_mass_balance_error")
    return float(np.clip(0.55 * purity + 0.35 * recovery - 0.10 * mass_balance_error, 0.0, 1.0))


def safety_cost_from_flags(flags: dict[str, Any]) -> tuple[float, dict[str, float]]:
    components = {
        "safety_risk": float(bool(flags.get("unsafe", False))),
        "high_cost": float(bool(flags.get("high_cost", False))),
        "precondition_failure": float(bool(flags.get("precondition_failed", False))),
        "constitution_failure": float(bool(flags.get("constitution_failed", False))),
    }
    return min(1.0, sum(components.values())), components


__all__ = ["purification_score", "reaction_score", "safety_cost_from_flags", "scalar_observation"]
