"""Objective functions for reactor optimization tasks."""

from __future__ import annotations

from dataclasses import dataclass

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

