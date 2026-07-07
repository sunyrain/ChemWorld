"""JSON-friendly schema contracts without a runtime jsonschema dependency."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, cast

from chemworld.world.operations import INSTRUMENTS, OPERATION_TYPES

PHASES = ("reactor_liquid", "aqueous", "organic")
TRAJECTORY_REQUIRED_KEYS = {
    "schema_version",
    "env_version",
    "world_family_version",
    "task_id",
    "env_id",
    "world_split",
    "objective",
    "world_id",
    "seed",
    "step",
    "campaign_id",
    "experiment_index",
    "operation_id",
    "scenario_id",
    "initial_state_id",
    "action",
    "observation",
    "reward",
    "terminated",
    "truncated",
    "constraint_flags",
    "constitution_checks",
    "agent_metadata",
    "instrument",
    "instrument_source",
    "measurement_cost",
    "observed_keys",
    "observed_mask",
    "raw_signal",
    "processed_estimate",
    "uncertainty",
    "observed_reward",
    "operation_type",
    "preconditions",
    "leaderboard_score",
    "reward_source",
    "sample_consumed",
    "state_delta_summary",
    "timestamp",
    "explanation",
}

ACTION_SCHEMA: dict[str, Any] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "ChemWorld event action",
    "type": "object",
    "required": ["operation"],
    "properties": {
        "operation": {
            "oneOf": [
                {"type": "string", "enum": list(OPERATION_TYPES)},
                {"type": "integer", "minimum": 0, "maximum": len(OPERATION_TYPES) - 1},
            ]
        },
        "payload": {"type": "object"},
        "instrument": {
            "oneOf": [
                {"type": "string", "enum": list(INSTRUMENTS)},
                {"type": "integer", "minimum": 0, "maximum": len(INSTRUMENTS) - 1},
            ]
        },
        "phase": {
            "oneOf": [
                {"type": "string", "enum": list(PHASES)},
                {"type": "integer", "minimum": 0, "maximum": len(PHASES) - 1},
            ]
        },
        "target_phase": {
            "oneOf": [
                {"type": "string", "enum": list(PHASES)},
                {"type": "integer", "minimum": 0, "maximum": len(PHASES) - 1},
            ]
        },
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
    "required": sorted(TRAJECTORY_REQUIRED_KEYS),
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


def validate_action_schema(action: object) -> SchemaValidationResult:
    errors: list[str] = []
    if not isinstance(action, dict):
        return SchemaValidationResult(False, ("action must be an object",))
    action = cast(dict[str, Any], action)
    if "operation" not in action:
        errors.append("missing required field: operation")
    operation = action.get("operation")
    if isinstance(operation, str) and operation not in OPERATION_TYPES:
        errors.append(f"unknown operation: {operation}")
    if isinstance(operation, int) and not 0 <= operation < len(OPERATION_TYPES):
        errors.append(f"operation index outside valid range: {operation}")
    if not isinstance(operation, str | int):
        errors.append("operation must be a string name or integer index")
    if "payload" in action and not isinstance(action["payload"], dict):
        errors.append("payload must be an object when provided")
    instrument = action.get("instrument")
    if instrument is not None and not isinstance(instrument, str | int):
        errors.append("instrument must be a string name or integer index")
    if isinstance(instrument, str) and instrument not in INSTRUMENTS:
        errors.append(f"unknown instrument: {instrument}")
    if isinstance(instrument, int) and not 0 <= instrument < len(INSTRUMENTS):
        errors.append(f"instrument index outside valid range: {instrument}")
    for key in ("phase", "target_phase"):
        value = action.get(key)
        if value is None:
            continue
        if isinstance(value, str) and value not in PHASES:
            errors.append(f"unknown {key}: {value}")
        elif isinstance(value, int) and not 0 <= value < len(PHASES):
            errors.append(f"{key} index outside valid range: {value}")
        elif not isinstance(value, str | int):
            errors.append(f"{key} must be a string name or integer index")
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
        "seed_mass_g",
        "reflux_ratio",
        "flow_rate_mL_min",
        "residence_time_s",
        "potential_V",
        "current_mA",
    ):
        if key in action and not _is_number(action[key]):
            errors.append(f"{key} must be numeric")
    return SchemaValidationResult(not errors, tuple(errors))


def validate_recipe_schema(recipe: object) -> SchemaValidationResult:
    errors: list[str] = []
    if not isinstance(recipe, dict):
        return SchemaValidationResult(False, ("recipe must be an object",))
    recipe = cast(dict[str, Any], recipe)
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
    "TRAJECTORY_REQUIRED_KEYS",
    "TRAJECTORY_SCHEMA",
    "SchemaValidationResult",
    "validate_action_schema",
    "validate_manifest_schema",
    "validate_recipe_schema",
]
