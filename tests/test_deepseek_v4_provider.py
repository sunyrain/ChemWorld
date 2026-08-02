from __future__ import annotations

import json

import pytest

from chemworld.providers.deepseek import DeepSeekClient

SCHEMA = {
    "type": "object",
    "properties": {
        "status": {"type": "string", "enum": ["ok"], "minLength": 1},
        "value": {"type": "integer", "minimum": 1, "maximum": 1},
    },
    "required": ["status", "value"],
    "additionalProperties": False,
}


class _StrictResponseClient(DeepSeekClient):
    def _send(self, body):  # type: ignore[no-untyped-def]
        assert "response_format" not in body
        return (
            json.dumps(
                {
                    "id": "request-1",
                    "model": "deepseek-v4-flash",
                    "choices": [
                        {
                            "finish_reason": "tool_calls",
                            "message": {
                                "content": None,
                                "reasoning_content": "private",
                                "tool_calls": [
                                    {
                                        "type": "function",
                                        "function": {
                                            "name": "chemworld_decision",
                                            "arguments": '{"status":"ok","value":1}',
                                        },
                                    }
                                ],
                            },
                        }
                    ],
                    "usage": {
                        "prompt_tokens": 10,
                        "completion_tokens": 5,
                        "total_tokens": 15,
                        "prompt_cache_hit_tokens": 4,
                        "prompt_cache_miss_tokens": 6,
                    },
                }
            ),
            "request-1",
        )


def test_strict_tool_transport_requires_beta_endpoint() -> None:
    with pytest.raises(ValueError, match="/beta"):
        DeepSeekClient(
            api_key="test",
            base_url="https://api.deepseek.com",
            model="deepseek-v4-flash",
            strict_tool_calls=True,
        )


def test_strict_tool_transport_projects_schema_to_supported_keywords() -> None:
    client = DeepSeekClient(
        api_key="test",
        base_url="https://api.deepseek.com/beta",
        model="deepseek-v4-flash",
        thinking=True,
        reasoning_effort="high",
        strict_tool_calls=True,
    )
    body = client._request_body(
        system_prompt="system",
        user_prompt="user",
        max_tokens=100,
        retry=False,
        output_schema=SCHEMA,
    )
    function = body["tools"][0]["function"]
    assert "tool_choice" not in body
    assert function["strict"] is True
    assert function["parameters"]["properties"]["status"] == {
        "type": "string",
        "enum": ["ok"],
    }
    assert "response_format" not in body


def test_strict_tool_response_is_parsed_and_accounted() -> None:
    client = _StrictResponseClient(
        api_key="test",
        base_url="https://api.deepseek.com/beta",
        model="deepseek-v4-flash",
        thinking=True,
        reasoning_effort="high",
        strict_tool_calls=True,
        max_attempts=1,
    )
    completion = client.complete_json(
        system_prompt="Return JSON.",
        user_prompt="Submit the decision.",
        output_schema=SCHEMA,
    )
    assert completion.payload == {"status": "ok", "value": 1}
    assert completion.finish_reason == "tool_calls"
    assert completion.reasoning_content_present is True
    assert completion.attempt_records[0]["usage_complete"] is True


def test_non_strict_schema_falls_back_to_json_object_with_schema_in_prompt() -> None:
    client = DeepSeekClient(api_key="test", model="deepseek-v4-flash")
    body = client._request_body(
        system_prompt="system",
        user_prompt="Return JSON.",
        max_tokens=100,
        retry=False,
        output_schema=SCHEMA,
    )
    assert body["response_format"] == {"type": "json_object"}
    assert "Return a JSON object conforming to this schema" in body["messages"][1]["content"]
