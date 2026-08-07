from __future__ import annotations

from chemworld.agents.scientific_adaptation import ResourceLedger
from chemworld.providers.wellau import WellAUClient


def test_wellau_request_is_exact_high_reasoning_responses_contract() -> None:
    client = WellAUClient(api_key="test-key", model="gpt-5.6-sol")

    body = client._request_body(
        system_prompt="system",
        user_prompt="user",
        max_tokens=8000,
        retry=False,
    )

    assert body == {
        "model": "gpt-5.6-sol",
        "instructions": "system",
        "input": "user",
        "reasoning": {"effort": "high"},
        "text": {"format": {"type": "json_object"}},
        "max_output_tokens": 8000,
    }
    assert client.wire_api == "responses"


def test_wellau_unknown_pricing_is_not_reported_as_zero_cost_accounting() -> None:
    client = WellAUClient(api_key="test-key", model="gpt-5.6-sol")

    resources = ResourceLedger().snapshot(client)

    assert resources["accounting_complete"] is False
    assert resources["monetary_cost_usd"] == 0.0
    assert resources["usage_source"] == "provider_usage_pricing_unavailable"
    assert resources["model_provenance"]["pricing"]["accounting_complete"] is False


def test_wellau_request_supports_medium_reasoning_without_fallback() -> None:
    client = WellAUClient(
        api_key="test-key",
        model="gpt-5.6-sol",
        reasoning_effort="medium",
    )

    body = client._request_body(
        system_prompt="system",
        user_prompt="user",
        max_tokens=8000,
        retry=False,
    )

    assert body["model"] == "gpt-5.6-sol"
    assert body["reasoning"] == {"effort": "medium"}


def test_wellau_request_supports_strict_json_schema() -> None:
    client = WellAUClient(api_key="test-key", model="gpt-5.6-sol")
    schema = {
        "type": "object",
        "properties": {
            "action": {
                "type": "object",
                "properties": {
                    "operation": {"type": "string", "enum": ["terminate"]}
                },
                "required": ["operation"],
                "additionalProperties": False,
            }
        },
        "required": ["action"],
        "additionalProperties": False,
    }

    body = client._request_body(
        system_prompt="system",
        user_prompt="user",
        max_tokens=512,
        retry=False,
        output_schema=schema,
    )

    assert body["text"]["format"] == {
        "type": "json_schema",
        "name": "chemworld_decision",
        "strict": True,
        "schema": schema,
    }


def test_wellau_responses_envelope_is_adapted_with_cache_usage() -> None:
    from chemworld.providers.wellau import _responses_to_chat_envelope

    raw = """{
      "id": "resp-test",
      "model": "gpt-5.6-sol",
      "status": "completed",
      "output": [{
        "type": "message",
        "content": [{
          "type": "output_text",
          "text": "{\\\"action\\\":{\\\"operation\\\":\\\"terminate\\\"}}"
        }]
      }],
      "usage": {
        "input_tokens": 120,
        "output_tokens": 20,
        "total_tokens": 140,
        "input_tokens_details": {"cached_tokens": 80}
      }
    }"""

    import json

    envelope = json.loads(
        _responses_to_chat_envelope(raw, requested_model="gpt-5.6-sol")
    )

    assert envelope["choices"][0]["message"]["content"] == (
        '{"action":{"operation":"terminate"}}'
    )
    assert envelope["usage"] == {
        "prompt_tokens": 120,
        "completion_tokens": 20,
        "total_tokens": 140,
        "prompt_cache_hit_tokens": 80,
        "prompt_cache_miss_tokens": 40,
    }
