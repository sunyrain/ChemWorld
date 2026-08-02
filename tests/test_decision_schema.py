from __future__ import annotations

import json
from typing import Any

import gymnasium as gym
import pytest

import chemworld  # noqa: F401
from chemworld.agents.decision_schema import (
    DecisionSchemaError,
    build_decision_output_schema,
)


def _field(
    name: str,
    *,
    choices: list[Any] | None = None,
    low: float | None = None,
    high: float | None = None,
    lower_inclusive: bool = True,
    upper_inclusive: bool = True,
    unit: str = "unitless",
) -> dict[str, Any]:
    payload: dict[str, Any] = {"field": name, "required": True, "unit": unit}
    if choices is not None:
        payload["choices"] = choices
    if low is not None or high is not None:
        payload["bounds"] = {"low": low, "high": high}
        payload["lower_bound_inclusive"] = lower_inclusive
        payload["upper_bound_inclusive"] = upper_inclusive
    return payload


def _action(
    operation: str,
    fields: list[dict[str, Any]],
    *,
    valid: bool = True,
) -> dict[str, Any]:
    return {
        "operation": operation,
        "valid": valid,
        "schema": {
            "schema_version": "chemworld-public-action-affordance-0.2",
            "operation": operation,
            "valid_operation_type": True,
            "task_allowed": True,
            "required_fields": [field["field"] for field in fields],
            "fields": fields,
        },
    }


def _variant(schema: dict[str, Any], operation: str) -> dict[str, Any]:
    variants = schema["properties"]["action"]["anyOf"]
    return next(item for item in variants if item["properties"]["operation"]["enum"] == [operation])


def _tool_json(actions: list[dict[str, Any]]) -> dict[str, Any]:
    return {"available_actions": actions}


def _assert_all_objects_are_closed_and_required(node: Any) -> None:
    if isinstance(node, dict):
        if node.get("type") == "object":
            assert node["additionalProperties"] is False
            assert set(node["required"]) == set(node["properties"])
        for value in node.values():
            _assert_all_objects_are_closed_and_required(value)
    elif isinstance(node, list):
        for value in node:
            _assert_all_objects_are_closed_and_required(value)


def test_builds_closed_discriminated_decision_schema() -> None:
    schema = build_decision_output_schema(
        _tool_json(
            [
                _action(
                    "add_solvent",
                    [
                        _field(
                            "volume_L",
                            low=0.0,
                            high=0.08,
                            lower_inclusive=False,
                        ),
                        _field("solvent", choices=[0, 1, 2, 3]),
                    ],
                ),
                _action("measure", [_field("instrument", choices=["hplc", "gc"])]),
                _action("terminate", []),
                _action("heat", [], valid=False),
            ]
        )
    )

    assert schema["type"] == "object"
    assert schema["additionalProperties"] is False
    assert schema["required"] == [
        "action",
        "expected_effect",
        "diagnostic_target",
        "expected_information_gain",
        "belief_update_rule",
        "uncertainty",
        "request_historical_spectrum_id",
    ]
    assert len(schema["properties"]["action"]["anyOf"]) == 3

    add_solvent = _variant(schema, "add_solvent")
    assert add_solvent["required"] == ["operation", "volume_L", "solvent"]
    assert add_solvent["additionalProperties"] is False
    assert add_solvent["properties"]["operation"] == {
        "type": "string",
        "enum": ["add_solvent"],
    }
    assert add_solvent["properties"]["volume_L"] == {
        "type": "number",
        "exclusiveMinimum": 0.0,
        "maximum": 0.08,
    }
    assert add_solvent["properties"]["solvent"] == {
        "type": "integer",
        "enum": [0, 1, 2, 3],
    }
    assert _variant(schema, "measure")["properties"]["instrument"] == {
        "type": "string",
        "enum": ["hplc", "gc"],
    }
    assert _variant(schema, "terminate")["required"] == ["operation"]

    properties = schema["properties"]
    assert properties["expected_effect"] == {
        "type": "string",
        "minLength": 1,
        "maxLength": 512,
    }
    assert properties["diagnostic_target"] == {
        "type": "string",
        "minLength": 1,
        "maxLength": 512,
    }
    assert properties["expected_information_gain"] == {
        "type": "number",
        "minimum": 0.0,
        "maximum": 1.0,
    }
    assert properties["uncertainty"] == {
        "type": "number",
        "minimum": 0.0,
        "maximum": 1.0,
    }
    assert properties["belief_update_rule"]["required"] == [
        "if_supported",
        "if_not_supported",
    ]
    assert properties["belief_update_rule"]["additionalProperties"] is False
    assert properties["belief_update_rule"]["properties"]["if_supported"] == {
        "type": "string",
        "minLength": 1,
        "maxLength": 512,
    }
    assert properties["request_historical_spectrum_id"] == {
        "anyOf": [
            {"type": "string", "minLength": 1, "maxLength": 256},
            {"type": "null"},
        ]
    }
    assert "oneOf" not in json.dumps(schema)
    _assert_all_objects_are_closed_and_required(schema)
    json.dumps(schema, allow_nan=False)


def test_preserves_inclusive_and_exclusive_numeric_bounds() -> None:
    schema = build_decision_output_schema(
        _tool_json(
            [
                _action(
                    "heat",
                    [
                        _field(
                            "target_temperature_K",
                            low=250.0,
                            high=470.0,
                            upper_inclusive=False,
                        )
                    ],
                )
            ]
        )
    )

    parameter = _variant(schema, "heat")["properties"]["target_temperature_K"]
    assert parameter == {
        "type": "number",
        "minimum": 250.0,
        "exclusiveMaximum": 470.0,
    }


def test_accepts_bounded_text_reason_without_enum() -> None:
    schema = build_decision_output_schema(
        _tool_json([_action("discard_batch", [_field("reason", unit="text")])])
    )

    reason = _variant(schema, "discard_batch")["properties"]["reason"]
    assert reason == {
        "type": "string",
        "minLength": 1,
        "maxLength": 256,
    }


def test_accepts_current_public_environment_affordances() -> None:
    env = gym.make("ChemWorld", task_id="reaction-to-crystallization", seed=0)
    try:
        env.reset(seed=0)
        actions = env.unwrapped.available_actions()
        schema = build_decision_output_schema({"available_actions": actions})
    finally:
        env.close()

    expected_operations = {item["operation"] for item in actions}
    generated_operations = {
        item["properties"]["operation"]["enum"][0]
        for item in schema["properties"]["action"]["anyOf"]
    }
    assert generated_operations == expected_operations


@pytest.mark.parametrize(
    ("actions", "message"),
    [
        ([], "at least one entry"),
        ([{"operation": "terminate"}], "valid must be boolean"),
        ([_action("terminate", [], valid=False)], "no explicitly valid action"),
        (
            [
                {
                    **_action("terminate", []),
                    "schema": {
                        **_action("terminate", [])["schema"],
                        "schema_version": "unknown",
                    },
                }
            ],
            "schema_version",
        ),
        (
            [
                {
                    **_action("terminate", []),
                    "schema": {
                        **_action("terminate", [])["schema"],
                        "operation": "measure",
                    },
                }
            ],
            "must match",
        ),
        (
            [
                {
                    **_action("terminate", []),
                    "schema": {
                        **_action("terminate", [])["schema"],
                        "task_allowed": False,
                    },
                }
            ],
            "task_allowed must be true",
        ),
        (
            [
                {
                    **_action("add_reagent", [_field("amount_mol", low=0.0, high=1.0)]),
                    "schema": {
                        **_action(
                            "add_reagent",
                            [_field("amount_mol", low=0.0, high=1.0)],
                        )["schema"],
                        "fields": [],
                    },
                }
            ],
            "exactly match required_fields",
        ),
        (
            [_action("measure", [_field("instrument")])],
            "non-empty choices or finite numeric bounds",
        ),
        (
            [_action("measure", [_field("instrument", choices=["hplc", 1])])],
            "one compatible JSON scalar type",
        ),
        (
            [
                _action("terminate", []),
                _action("terminate", []),
            ],
            "duplicate legal operation",
        ),
    ],
)
def test_incomplete_or_ambiguous_affordances_fail_closed(
    actions: list[dict[str, Any]],
    message: str,
) -> None:
    with pytest.raises(DecisionSchemaError, match=message):
        build_decision_output_schema(_tool_json(actions))


def test_rejects_non_finite_or_empty_numeric_domain() -> None:
    with pytest.raises(DecisionSchemaError, match="must be finite"):
        build_decision_output_schema(
            _tool_json([_action("heat", [_field("duration_s", low=1.0, high=float("inf"))])])
        )
    with pytest.raises(DecisionSchemaError, match="empty interval"):
        build_decision_output_schema(
            _tool_json(
                [
                    _action(
                        "sample",
                        [
                            _field(
                                "sample_volume_L",
                                low=0.0,
                                high=0.0,
                                lower_inclusive=False,
                            )
                        ],
                    )
                ]
            )
        )
