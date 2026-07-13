from __future__ import annotations

import json
from typing import Any

import pytest
from scripts.audit_live_llm_baselines import build_report

from chemworld.providers.deepseek import DeepSeekAPIError, DeepSeekClient


class _ResponseClient(DeepSeekClient):
    def __init__(self, responses: list[str | Exception], **kwargs: Any) -> None:
        super().__init__(
            api_key="test-only",
            model="deepseek-v4-pro",
            retry_backoff_s=0.0,
            sleep=lambda _: None,
            **kwargs,
        )
        self.responses = list(responses)

    def _send(self, body: dict[str, Any]) -> tuple[str, str | None]:
        del body
        item = self.responses.pop(0)
        if isinstance(item, Exception):
            raise item
        return item, "request-header-id"


def _envelope(*, model: str = "deepseek-v4-pro") -> str:
    return json.dumps(
        {
            "id": "request-body-id",
            "model": model,
            "system_fingerprint": "fp-test",
            "choices": [
                {
                    "finish_reason": "stop",
                    "message": {
                        "content": '{"status":"ok"}',
                        "reasoning_content": "private reasoning is not retained",
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
    )


def test_deepseek_cost_uses_cache_breakdown_and_conservative_fallback() -> None:
    client = DeepSeekClient(api_key="test-only", model="deepseek-v4-pro")
    split = client.estimate_cost_usd(
        {
            "prompt_tokens": 1000,
            "prompt_cache_hit_tokens": 400,
            "prompt_cache_miss_tokens": 600,
            "completion_tokens": 200,
        }
    )
    expected = (400 * 0.003625 + 600 * 0.435 + 200 * 0.87) / 1_000_000
    assert split == expected
    fallback = client.estimate_cost_usd({"prompt_tokens": 1000, "completion_tokens": 200})
    assert fallback == (1000 * 0.435 + 200 * 0.87) / 1_000_000
    assert fallback > split


def test_deepseek_rejects_legacy_alias_and_returned_model_replacement() -> None:
    alias = DeepSeekClient(api_key="test-only", model="deepseek-chat")
    with pytest.raises(DeepSeekAPIError, match="No frozen pricing or formal identity"):
        alias.pricing_snapshot()

    client = _ResponseClient([_envelope(model="deepseek-v4-flash")])
    with pytest.raises(DeepSeekAPIError, match="model identity"):
        client.complete_json(system_prompt="system", user_prompt="user")


def test_deepseek_retries_transient_failure_and_retains_only_reasoning_metadata() -> None:
    client = _ResponseClient(
        [
            DeepSeekAPIError("temporary", retryable=True, status_code=429),
            _envelope(),
        ]
    )

    completion = client.complete_json(system_prompt="system", user_prompt="user")

    assert completion.attempts == 2
    assert completion.request_id == "request-header-id"
    assert completion.system_fingerprint == "fp-test"
    assert completion.reasoning_content_present is True
    assert completion.reasoning_character_count > 0
    assert "reasoning_content" not in completion.__dict__
    assert len(completion.attempt_records) == 2
    assert completion.attempt_records[0]["status"] == "failed"
    assert completion.attempt_records[0]["usage_complete"] is False
    assert completion.attempt_records[1]["status"] == "succeeded"
    assert completion.attempt_records[1]["usage_complete"] is True
    assert "reasoning_content" not in json.dumps(completion.attempt_records)


def test_live_llm_controls_do_not_claim_missing_runs() -> None:
    report = build_report()
    assert report["controls_ready"] is True
    assert report["formal_run_matrix_complete"] is False
    assert report["publication_ready"] is False
    assert report["checks"]["two_independent_model_ids"] is True
    assert report["checks"]["private_reasoning_excluded"] is True
    assert all(
        manifest["formal_unbillable_provider_failure_policy"]
        == "raise_resumable_infrastructure_interruption"
        for manifest in report["official_adapter_manifests"].values()
    )
