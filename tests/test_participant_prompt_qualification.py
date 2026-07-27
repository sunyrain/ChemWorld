from __future__ import annotations

from pathlib import Path

from chemworld.eval.mechanism_adaptation_execution import load_protocol_object
from chemworld.eval.participant_prompt_qualification import (
    qualify_participant_prompt_envelopes,
)

ROOT = Path(__file__).resolve().parents[1]


def test_worst_legal_prompt_fixtures_derive_unreduced_scaffold_budgets() -> None:
    protocol = load_protocol_object(
        ROOT / "configs/benchmark/mechanism_adaptation_v0.3.0_rc28.json"
    )

    report = qualify_participant_prompt_envelopes(protocol)

    assert report["fixture_count"] == 50
    assert report["provider_calls"] == 0
    assert report["all_rows_passed"] is True
    assert report["same_environment_view_across_scaffolds"] is True
    assert all(
        fixture["reduction_steps"] == []
        for fixture in report["fixtures"]
    )
    budgets = report["suggested_development_budgets"]["by_scaffold"]
    assert budgets["direct_reactive"] == {
        "environment_view_max_estimated_tokens": 2050,
        "agent_memory_max_estimated_tokens": 950,
        "per_decision_max_estimated_tokens": 3600,
    }
    assert budgets["stateful_scientific"] == {
        "environment_view_max_estimated_tokens": 2050,
        "agent_memory_max_estimated_tokens": 1350,
        "per_decision_max_estimated_tokens": 4150,
    }
