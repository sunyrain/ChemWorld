"""JSON-friendly schema contracts without a runtime jsonschema dependency."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from chemworld.core.batch_reactor import INSTRUMENTS, OPERATION_TYPES

ACTION_SCHEMA: dict[str, Any] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "ChemWorld event action",
    "type": "object",
    "required": ["operation"],
    "properties": {
        "operation": {"type": ["string", "integer"], "enum": list(OPERATION_TYPES)},
        "payload": {"type": "object"},
        "instrument": {"type": ["string", "integer"], "enum": list(INSTRUMENTS)},
    },
    "additionalProperties": True,
}

OBSERVATION_SCHEMA: dict[str, Any] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "ChemWorld observation",
    "type": "object",
    "additionalProperties": {"type": ["number", "null"]},
}

RECIPE_SCHEMA: dict[str, Any] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "ChemWorld recipe",
    "type": "object",
    "required": ["steps"],
    "properties": {
        "steps": {"type": "array", "items": ACTION_SCHEMA, "minItems": 1},
        "metadata": {"type": "object"},
    },
    "additionalProperties": True,
}

TRAJECTORY_SCHEMA: dict[str, Any] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "ChemWorld trajectory record",
    "type": "object",
    "required": ["schema_version", "campaign_id", "experiment_index", "operation_id"],
}

MANIFEST_SCHEMA: dict[str, Any] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "ChemWorld submission manifest",
    "type": "object",
    "required": ["schema_version", "agent_name", "agent_family", "task_id", "seeds"],
}

TASK_SCHEMA: dict[str, Any] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "ChemWorld task spec",
    "type": "object",
    "required": ["task_id", "world_law_id", "scenario_id", "budget"],
}

SCENARIO_SCHEMA: dict[str, Any] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "ChemWorld scenario spec",
    "type": "object",
    "required": ["scenario_id", "world_law_id", "family", "split"],
}


@dataclass(frozen=True)
class SchemaValidationResult:
    valid: bool
    errors: tuple[str, ...]
    warnings: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "valid": self.valid,
            "errors": list(self.errors),
            "warnings": list(self.warnings),
        }


def _is_number(value: Any) -> bool:
    return isinstance(value, int | float) and not isinstance(value, bool)


def validate_action_schema(action: dict[str, Any]) -> SchemaValidationResult:
    errors: list[str] = []
    if not isinstance(action, dict):
        return SchemaValidationResult(False, ("action must be an object",))
    if "operation" not in action:
        errors.append("missing required field: operation")
    operation = action.get("operation")
    if isinstance(operation, str) and operation not in OPERATION_TYPES:
        errors.append(f"unknown operation: {operation}")
    if not isinstance(operation, str | int):
        errors.append("operation must be a string name or integer index")
    if "payload" in action and not isinstance(action["payload"], dict):
        errors.append("payload must be an object when provided")
    instrument = action.get("instrument")
    if instrument is not None and not isinstance(instrument, str | int):
        errors.append("instrument must be a string name or integer index")
    for key in (
        "amount_mol",
        "volume_L",
        "catalyst_amount_mol",
        "target_temperature_K",
        "duration_s",
        "stirring_speed_rpm",
        "sample_volume_L",
        "wash_volume_L",
        "transfer_fraction",
    ):
        if key in action and not _is_number(action[key]):
            errors.append(f"{key} must be numeric")
    return SchemaValidationResult(not errors, tuple(errors))


def validate_recipe_schema(recipe: dict[str, Any]) -> SchemaValidationResult:
    errors: list[str] = []
    if not isinstance(recipe, dict):
        return SchemaValidationResult(False, ("recipe must be an object",))
    steps = recipe.get("steps")
    if not isinstance(steps, list) or not steps:
        errors.append("recipe.steps must be a non-empty list")
        return SchemaValidationResult(False, tuple(errors))
    for index, step in enumerate(steps):
        result = validate_action_schema(step)
        errors.extend(f"steps[{index}]: {error}" for error in result.errors)
    return SchemaValidationResult(not errors, tuple(errors))


def validate_manifest_schema(manifest: dict[str, Any]) -> SchemaValidationResult:
    required = {"schema_version", "agent_name", "agent_family", "task_id", "seeds"}
    missing = sorted(required - manifest.keys())
    errors = [f"missing required field: {key}" for key in missing]
    if "seeds" in manifest and not isinstance(manifest["seeds"], list):
        errors.append("seeds must be a list")
    return SchemaValidationResult(not errors, tuple(errors))


__all__ = [
    "ACTION_SCHEMA",
    "MANIFEST_SCHEMA",
    "OBSERVATION_SCHEMA",
    "RECIPE_SCHEMA",
    "SCENARIO_SCHEMA",
    "TASK_SCHEMA",
    "TRAJECTORY_SCHEMA",
    "SchemaValidationResult",
    "validate_action_schema",
    "validate_manifest_schema",
    "validate_recipe_schema",
]
