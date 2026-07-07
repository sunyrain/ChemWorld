"""Task-aware scoring helpers for ChemWorld."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np


@dataclass(frozen=True)
class ObjectiveWeights:
    yield_weight: float
    selectivity_weight: float
    conversion_weight: float
    cost_penalty: float
    risk_penalty: float


OBJECTIVES: dict[str, ObjectiveWeights] = {
    "balanced": ObjectiveWeights(0.50, 0.25, 0.10, 0.15, 0.25),
    "yield": ObjectiveWeights(0.75, 0.10, 0.05, 0.05, 0.10),
    "safe": ObjectiveWeights(0.40, 0.25, 0.10, 0.10, 0.45),
}


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


def score_observation(
    *,
    objective: str,
    product_yield: float,
    selectivity: float,
    conversion: float,
    cost: float,
    safety_risk: float,
) -> float:
    """Compute the benchmark scalar score in [0, 1]."""

    if objective not in OBJECTIVES:
        allowed = ", ".join(sorted(OBJECTIVES))
        raise ValueError(f"Unknown objective {objective!r}. Allowed: {allowed}")

    weights = OBJECTIVES[objective]
    raw = (
        weights.yield_weight * product_yield
        + weights.selectivity_weight * selectivity
        + weights.conversion_weight * conversion
        - weights.cost_penalty * cost
        - weights.risk_penalty * safety_risk
    )
    return float(np.clip(raw, 0.0, 1.0))


__all__ = [
    "OBJECTIVES",
    "ObjectiveWeights",
    "purification_score",
    "reaction_score",
    "safety_cost_from_flags",
    "scalar_observation",
    "score_observation",
]
