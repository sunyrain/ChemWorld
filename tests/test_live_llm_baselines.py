from __future__ import annotations

from apps.task_lab.deepseek_client import DeepSeekClient
from scripts.audit_live_llm_baselines import build_report


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


def test_live_llm_controls_do_not_claim_missing_runs() -> None:
    report = build_report()
    assert report["controls_ready"] is True
    assert report["formal_run_matrix_complete"] is False
    assert report["publication_ready"] is False
    assert report["checks"]["two_independent_model_ids"] is True
    assert report["checks"]["private_reasoning_excluded"] is True
