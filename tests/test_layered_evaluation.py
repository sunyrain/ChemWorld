from __future__ import annotations

import json
from pathlib import Path

import pytest

from chemworld.eval.layered_evaluation import (
    TaskEvaluationContract,
    evaluate_layered_records,
)

FROZEN_REPORT = (
    Path(__file__).resolve().parents[1]
    / "workstreams"
    / "benchmark_v1"
    / "reports"
    / "evaluation-identifiability-controls.json"
)


def _record(
    *,
    score: float | None,
    primary: float | None,
    cost: float | None,
    reward: float,
    risk: float | None = 0.2,
    unsafe: bool = False,
) -> dict:
    return {
        "leaderboard_score": score,
        "observation": {
            "product_in_organic": primary,
            "cost": cost,
            "safety_risk": risk,
        },
        "reward": reward,
        "measurement_cost": 0.03 if score is not None else 0.0,
        "constraint_flags": {"unsafe": unsafe},
    }


def test_layered_evaluator_keeps_endpoints_shaping_constraints_and_cost_separate() -> None:
    contract = TaskEvaluationContract.for_task("partition-discovery")
    records = [
        _record(score=None, primary=0.99, cost=None, reward=0.7),
        _record(score=0.4, primary=0.5, cost=0.2, reward=0.4),
        _record(score=None, primary=0.01, cost=None, reward=0.9, unsafe=True),
        _record(score=0.6, primary=0.7, cost=0.3, reward=0.6),
    ]
    result = evaluate_layered_records(records, contract=contract)
    assert result["objective"]["best"] == pytest.approx(0.6)
    assert result["task_primary"]["terminal_values"] == pytest.approx([0.5, 0.7])
    assert result["online_shaping"]["eligible_as_primary_endpoint"] is False
    assert result["constraints"]["unsafe_operation_count"] == 1
    assert result["resources"]["campaign_process_cost"] == pytest.approx(0.5)
    assert result["resources"]["measurement_cost"] == pytest.approx(0.06)


def test_layered_evaluator_fails_on_missing_terminal_primary() -> None:
    contract = TaskEvaluationContract.for_task("partition-discovery")
    with pytest.raises(ValueError, match="product_in_organic"):
        evaluate_layered_records(
            [_record(score=0.4, primary=None, cost=0.2, reward=0.4)],
            contract=contract,
        )


def test_frozen_evaluation_report_keeps_signal_blocker_visible() -> None:
    report = json.loads(FROZEN_REPORT.read_text(encoding="utf-8"))
    assert report["controls_ready"] is True
    assert report["evaluation_identifiable"] is False
    assert report["checks"]["formal_safety_constraint_active"] is False
    assert report["benchmark_claim_allowed"] is False
