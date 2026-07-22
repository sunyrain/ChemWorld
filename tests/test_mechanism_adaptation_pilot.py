from __future__ import annotations

import json
from pathlib import Path

import pytest

from chemworld.eval.mechanism_adaptation_pilot import (
    build_agent_pilot_report,
    distribution_after_experiments,
    load_campaigns_from_index,
)


def _record(
    complete_experiments: int,
    *,
    status: str | None = None,
    distribution: dict[str, float] | None = None,
) -> dict[str, object]:
    trace = []
    if status is not None:
        trace.append(
            {
                "status": status,
                "mechanism_distribution": distribution,
            }
        )
    return {
        "method_resources": {
            "complete_experiment_count": complete_experiments,
        },
        "agent_trace": trace,
    }


def test_distribution_uses_first_valid_decision_after_feedback() -> None:
    expected = {
        "no_change": 0.2,
        "rate_law_family": 0.8,
    }
    records = [
        _record(
            0,
            status="model_decision",
            distribution={"no_change": 0.9, "rate_law_family": 0.1},
        ),
        _record(1, status="lifecycle_guardrail"),
        _record(1, status="model_failure"),
        _record(1, status="model_decision", distribution=expected),
        _record(
            1,
            status="model_decision",
            distribution={"no_change": 0.7, "rate_law_family": 0.3},
        ),
    ]

    assert distribution_after_experiments(records, 1) == expected


def test_distribution_rejects_missing_post_feedback_decision() -> None:
    with pytest.raises(ValueError, match="no valid decision"):
        distribution_after_experiments([_record(1)], 1)


def test_campaign_index_must_name_campaigns(tmp_path: Path) -> None:
    index = tmp_path / "campaign-index.json"
    index.write_text(json.dumps({"campaign_paths": []}), encoding="utf-8")

    with pytest.raises(ValueError, match="at least one campaign"):
        load_campaigns_from_index(index, root=tmp_path)


def test_pilot_report_rejects_split_pair_before_analysis(tmp_path: Path) -> None:
    campaigns = [
        {"matrix_row": {"arm": "changed", "pair_id": "pair-a"}},
        {"matrix_row": {"arm": "no_change_twin", "pair_id": "pair-b"}},
    ]

    with pytest.raises(ValueError, match="do not share"):
        build_agent_pilot_report({}, campaigns, root=tmp_path, replay=False)
