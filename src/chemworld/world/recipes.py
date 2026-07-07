"""Recipe validation and compilation for experiment-level planning."""

from __future__ import annotations

from typing import Any

import numpy as np

from chemworld.core.actions import canonicalize_action
from chemworld.schemas import SchemaValidationResult, validate_action_schema, validate_recipe_schema


def recipe_to_event_sequence(action: dict[str, Any]) -> list[dict[str, Any]]:
    """Expand terminal recipe parameters into executable reactor operations."""

    normalized = canonicalize_action(action)
    concentration = float(normalized["initial_concentration"])
    volume = 0.025
    amount = float(np.clip(concentration * volume, 0.0005, 0.040))
    target_temperature = float(normalized["temperature"]) + 273.15
    duration = float(normalized["time"]) * 3600.0
    return [
        {"operation": "add_solvent", "volume_L": volume, "solvent": int(normalized["solvent"])},
        {"operation": "add_reagent", "amount_mol": amount},
        {
            "operation": "add_catalyst",
            "catalyst_amount_mol": 0.00020,
            "catalyst": int(normalized["catalyst"]),
        },
        {
            "operation": "heat",
            "target_temperature_K": target_temperature,
            "duration_s": duration,
            "stirring_speed_rpm": float(normalized["stirring_speed"]),
        },
        {"operation": "terminate"},
        {"operation": "measure", "instrument": "final_assay"},
    ]


def compile_recipe(recipe: dict[str, Any]) -> list[dict[str, Any]]:
    """Compile a recipe object or recipe-style action into event actions."""

    if "steps" in recipe:
        result = validate_recipe_schema(recipe)
        if not result.valid:
            raise ValueError(f"Invalid recipe: {', '.join(result.errors)}")
        return [dict(step) for step in recipe["steps"]]

    if "operation" in recipe:
        result = validate_action_schema(recipe)
        if not result.valid:
            raise ValueError(f"Invalid recipe action: {', '.join(result.errors)}")
        return [dict(recipe)]
    return recipe_to_event_sequence(recipe)


def validate_recipe(recipe: dict[str, Any]) -> SchemaValidationResult:
    """Validate a recipe and ensure it can be compiled."""

    if "steps" in recipe:
        return validate_recipe_schema(recipe)
    if "operation" in recipe:
        result = validate_action_schema(recipe)
        if not result.valid:
            return result
    try:
        compile_recipe(recipe)
    except (KeyError, TypeError, ValueError) as exc:
        return SchemaValidationResult(False, (str(exc),))
    return SchemaValidationResult(True, ())


__all__ = ["compile_recipe", "recipe_to_event_sequence", "validate_recipe"]
