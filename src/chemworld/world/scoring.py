"""Task-aware scoring helpers for ChemWorld."""

from __future__ import annotations

import hashlib
import json
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


@dataclass(frozen=True)
class TaskScoringContract:
    """Serializable score contract compiled from task success metrics."""

    objective: str
    success_metrics: tuple[str, ...]
    score_family: str
    component_weights: dict[str, float]

    @classmethod
    def from_success_metrics(
        cls,
        *,
        objective: str,
        success_metrics: tuple[str, ...] = (),
    ) -> TaskScoringContract:
        metrics = frozenset(success_metrics)
        if metrics.intersection({"crystal_yield", "crystal_purity", "crystal_size"}):
            return cls(
                objective,
                success_metrics,
                "crystallization",
                {
                    "reaction_score": 0.40,
                    "crystal_yield": 0.28,
                    "crystal_purity": 0.24,
                    "crystal_size": 0.08,
                },
            )
        if metrics.intersection({"distillate_purity", "distillate_recovery"}):
            return cls(
                objective,
                success_metrics,
                "distillation",
                {
                    "reaction_score": 0.40,
                    "distillate_purity": 0.34,
                    "distillate_recovery": 0.22,
                    "solvent_loss": -0.10,
                },
            )
        if metrics.intersection({"electrochemical_selectivity", "energy_efficiency"}):
            return cls(
                objective,
                success_metrics,
                "electrochemistry",
                {
                    "reaction_score": 0.35,
                    "electrochemical_selectivity": 0.35,
                    "energy_efficiency": 0.20,
                    "conversion": 0.10,
                },
            )
        if "flow_conversion" in metrics:
            return cls(
                objective,
                success_metrics,
                "continuous_flow",
                {
                    "reaction_score": 0.50,
                    "flow_conversion": 0.35,
                    "yield": 0.15,
                },
            )
        if metrics.intersection({"purity", "recovery", "process_mass_balance_error"}):
            return cls(
                objective,
                success_metrics,
                "purification",
                {
                    "reaction_score": 0.35,
                    "purity": 0.35,
                    "recovery": 0.25,
                    "process_mass_balance_error": -0.10,
                },
            )
        if metrics.intersection({"phase_ratio", "product_in_organic", "product_in_aqueous"}):
            return cls(
                objective,
                success_metrics,
                "partition",
                {
                    "reaction_score": 0.25,
                    "product_in_organic": 0.40,
                    "phase_ratio": 0.25,
                    "product_in_aqueous": -0.10,
                },
            )
        return cls(
            objective,
            success_metrics,
            "reaction",
            {"reaction_score": 1.0},
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "objective": self.objective,
            "success_metrics": list(self.success_metrics),
            "score_family": self.score_family,
            "component_weights": dict(self.component_weights),
            "contract_hash": self.contract_hash,
        }

    @property
    def contract_hash(self) -> str:
        payload = {
            "objective": self.objective,
            "success_metrics": list(self.success_metrics),
            "score_family": self.score_family,
            "component_weights": dict(sorted(self.component_weights.items())),
        }
        digest = hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8"))
        return digest.hexdigest()


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


def task_score_observation(
    *,
    contract: TaskScoringContract,
    values: dict[str, float | None],
) -> float:
    """Compute the task-specific scalar score in [0, 1]."""

    reaction_component = score_observation(
        objective=contract.objective,
        product_yield=scalar_observation(values, "yield"),
        selectivity=scalar_observation(values, "selectivity"),
        conversion=scalar_observation(values, "conversion"),
        cost=scalar_observation(values, "cost"),
        safety_risk=scalar_observation(values, "safety_risk"),
    )
    components = {"reaction_score": reaction_component}
    components.update(
        {
            key: scalar_observation(values, key)
            for key in contract.component_weights
            if key != "reaction_score"
        }
    )
    raw = sum(
        weight * components.get(key, 0.0)
        for key, weight in contract.component_weights.items()
    )
    return float(np.clip(raw, 0.0, 1.0))


__all__ = [
    "OBJECTIVES",
    "ObjectiveWeights",
    "TaskScoringContract",
    "purification_score",
    "reaction_score",
    "safety_cost_from_flags",
    "scalar_observation",
    "score_observation",
    "task_score_observation",
]
