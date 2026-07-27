from __future__ import annotations

from chemworld.agents.scientific_adaptation import ResourceLedger
from chemworld.providers.wellau import WellAUClient


def test_wellau_request_is_exact_high_reasoning_json_contract() -> None:
    client = WellAUClient(api_key="test-key", model="gpt-5.6-sol")

    body = client._request_body(
        system_prompt="system",
        user_prompt="user",
        max_tokens=8000,
        retry=False,
    )

    assert body == {
        "model": "gpt-5.6-sol",
        "messages": [
            {"role": "system", "content": "system"},
            {"role": "user", "content": "user"},
        ],
        "response_format": {"type": "json_object"},
        "reasoning_effort": "high",
        "stream": False,
        "max_tokens": 8000,
    }
    assert "thinking" not in body


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
    assert body["reasoning_effort"] == "medium"
