"""Recipe validation and compilation for experiment-level planning."""

from __future__ import annotations

from typing import Any

from chemworld.core.batch_reactor import recipe_to_event_sequence
from chemworld.schemas import SchemaValidationResult, validate_action_schema, validate_recipe_schema


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


__all__ = ["compile_recipe", "validate_recipe"]
