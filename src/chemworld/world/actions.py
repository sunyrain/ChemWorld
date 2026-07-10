"""Action catalog and terminal recipe-vector helpers for the shared ChemWorld law."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np

CATALYSTS = ("cat_a", "cat_b", "cat_c", "cat_d")
SOLVENTS = ("water", "ethanol", "acetonitrile", "toluene")


@dataclass(frozen=True)
class ContinuousBound:
    low: float
    high: float
    unit: str


ACTION_BOUNDS: dict[str, ContinuousBound] = {
    "temperature": ContinuousBound(40.0, 160.0, "degC"),
    "time": ContinuousBound(0.25, 4.0, "h"),
    "initial_concentration": ContinuousBound(0.10, 2.00, "mol/L"),
    "stirring_speed": ContinuousBound(100.0, 1200.0, "rpm"),
}

ACTION_KEYS = (*ACTION_BOUNDS.keys(), "catalyst", "solvent")


def _scalar(value: Any) -> float:
    if isinstance(value, np.ndarray):
        return float(value.reshape(-1)[0])
    if isinstance(value, np.generic):
        return float(value.item())
    return float(value)


def canonicalize_action(action: dict[str, Any], *, clip: bool = True) -> dict[str, float | int]:
    """Return a normalized terminal-recipe action dictionary."""

    missing = [key for key in ACTION_KEYS if key not in action]
    if missing:
        raise ValueError(f"Action is missing required keys: {missing}")

    normalized: dict[str, float | int] = {}
    for key, bound in ACTION_BOUNDS.items():
        value = _scalar(action[key])
        if clip:
            value = float(np.clip(value, bound.low, bound.high))
        elif not bound.low <= value <= bound.high:
            raise ValueError(f"{key}={value} is outside [{bound.low}, {bound.high}]")
        normalized[key] = value

    catalyst = int(_scalar(action["catalyst"]))
    solvent = int(_scalar(action["solvent"]))
    if clip:
        catalyst = int(np.clip(catalyst, 0, len(CATALYSTS) - 1))
        solvent = int(np.clip(solvent, 0, len(SOLVENTS) - 1))
    elif catalyst not in range(len(CATALYSTS)) or solvent not in range(len(SOLVENTS)):
        raise ValueError("catalyst and solvent must be valid discrete indices")

    normalized["catalyst"] = catalyst
    normalized["solvent"] = solvent
    return normalized


def sample_random_action(rng: np.random.Generator) -> dict[str, float | int]:
    """Sample one uniformly random terminal-recipe action."""

    action: dict[str, float | int] = {
        key: float(rng.uniform(bound.low, bound.high)) for key, bound in ACTION_BOUNDS.items()
    }
    action["catalyst"] = int(rng.integers(0, len(CATALYSTS)))
    action["solvent"] = int(rng.integers(0, len(SOLVENTS)))
    return action


def action_to_vector(action: dict[str, Any]) -> np.ndarray:
    """Map a mixed terminal-recipe action to normalized numeric features."""

    normalized = canonicalize_action(action)
    features: list[float] = []
    for key, bound in ACTION_BOUNDS.items():
        value = float(normalized[key])
        features.append((value - bound.low) / (bound.high - bound.low))

    catalyst = int(normalized["catalyst"])
    solvent = int(normalized["solvent"])
    features.extend(1.0 if catalyst == index else 0.0 for index in range(len(CATALYSTS)))
    features.extend(1.0 if solvent == index else 0.0 for index in range(len(SOLVENTS)))
    return np.asarray(features, dtype=float)


def vector_to_action(vector: np.ndarray) -> dict[str, float | int]:
    """Map a normalized continuous vector to a valid terminal-recipe action."""

    if vector.shape[0] < 6:
        raise ValueError("Expected at least 6 coordinates")

    action: dict[str, float | int] = {}
    for index, (key, bound) in enumerate(ACTION_BOUNDS.items()):
        coordinate = float(np.clip(vector[index], 0.0, 1.0))
        action[key] = bound.low + coordinate * (bound.high - bound.low)
    action["catalyst"] = int(
        np.clip(round(float(vector[4]) * (len(CATALYSTS) - 1)), 0, len(CATALYSTS) - 1)
    )
    action["solvent"] = int(
        np.clip(round(float(vector[5]) * (len(SOLVENTS) - 1)), 0, len(SOLVENTS) - 1)
    )
    return action


__all__ = [
    "ACTION_BOUNDS",
    "ACTION_KEYS",
    "CATALYSTS",
    "SOLVENTS",
    "ContinuousBound",
    "action_to_vector",
    "canonicalize_action",
    "sample_random_action",
    "vector_to_action",
]
