from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from analyze_work_ii_w263_b3_failure_aware_cross_model import (  # noqa: E402
    _metric_block,
    _paired_block,
)


def _row(
    *,
    cluster: str,
    completed: bool,
    regret: float,
    top1: bool,
    post_error: float | None,
) -> dict:
    return {
        "cluster_id": cluster,
        "arm": "opaque",
        "replicate_index": 1,
        "completed": completed,
        "failure_classification": None if completed else "participant_schema",
        "post_error": post_error,
        "joint_family_exponent_recovery": completed,
        "top1_selected": top1,
        "selected_true_rank": 1.0 if completed else None,
        "normalized_regret": regret,
        "action_opportunity_eligible": completed,
        "selected_action_gain": 0.03 if completed else None,
    }


def test_metric_block_keeps_failures_in_action_denominator() -> None:
    rows = [
        _row(cluster="w1", completed=True, regret=0.0, top1=True, post_error=0.1),
        _row(cluster="w2", completed=False, regret=1.0, top1=False, post_error=None),
    ]
    summary = _metric_block(rows)
    assert summary["scheduled_cell_count"] == 2
    assert summary["completed_cell_count"] == 1
    assert summary["failure_aware_mean_regret"] == 0.5
    assert summary["failure_aware_top1_rate"] == 0.5
    assert summary["completed_mean_post_mae"] == 0.1


def test_paired_block_uses_codex_minus_deepseek_orientation() -> None:
    deepseek = [
        _row(cluster="w1", completed=False, regret=1.0, top1=False, post_error=None),
        _row(cluster="w2", completed=True, regret=0.4, top1=False, post_error=0.2),
    ]
    codex = [
        _row(cluster="w1", completed=True, regret=0.2, top1=True, post_error=0.1),
        _row(cluster="w2", completed=True, regret=0.2, top1=True, post_error=0.1),
    ]
    summary = _paired_block(deepseek, codex)
    assert summary["orientation"] == "codex_minus_deepseek"
    assert summary["paired_scheduled_cell_count"] == 2
    assert summary["paired_common_completed_cell_count"] == 1
    assert summary["failure_aware_mean_regret_difference"] == -0.5
    assert summary["failure_aware_top1_rate_difference"] == 1.0
