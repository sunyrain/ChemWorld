from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import analyze_work_ii_w261_cross_model_completion as combined  # noqa: E402


def _row(
    index: int,
    condition: str,
    *,
    admitted: bool = True,
    status: str = "completed",
    regret: float = 0.2,
) -> dict[str, object]:
    task = "task-a" if index < 24 else "task-b"
    return {
        "stratum_id": f"stratum-{index:02d}",
        "cluster_id": f"{task}-world-{index // 3:02d}",
        "task_id": task,
        "world_seed": index // 3,
        "prior_arm": ("opaque", "aligned_nominal", "misindexed_nominal")[index % 3],
        "condition": condition,
        "source": "original",
        "status": status,
        "admitted_stratum": admitted,
        "analysis_eligible": admitted,
        "scheduled_for_execution": True,
        "provider_call_count": 1,
        "failure_aware_normalized_regret": regret,
        "selected_rank": 1 if status == "completed" else None,
        "top1": 1 if status == "completed" else 0,
        "within_0_01_of_best": 1 if status == "completed" else 0,
        "pairwise_ranking_agreement_excluding_truth_gaps_below_0_01": (
            0.8 if status == "completed" else None
        ),
    }


def test_full_condition_recovery_replaces_only_admitted_yoked_rows() -> None:
    original_rows = [
        _row(index, condition, admitted=index < 2)
        for index in range(45)
        for condition in combined.CONDITIONS
    ]
    recovery_rows = [
        _row(index, "yoked_evidence", regret=0.05 + index * 0.01)
        for index in range(2)
    ]
    merged, incident = combined._merge_model_rows(
        participant="synthetic",
        original={"condition_rows": original_rows},
        recovery={
            "condition_rows": recovery_rows,
            "denominators": {"admitted_yoked_recovery_sessions": 2},
        },
    )

    assert len(merged) == 180
    assert len(incident) == 45
    recovered = [
        row
        for row in merged
        if row["condition"] == "yoked_evidence"
        and row["source"] == "new_w2_61_yoked_recovery_primary"
    ]
    assert len(recovered) == 2
    assert {row["stratum_id"] for row in recovered} == {"stratum-00", "stratum-01"}
    assert all(row["superseded_platform_incident_status"] == "completed" for row in recovered)


def test_failure_aware_contrast_keeps_failed_rows(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(combined, "BOOTSTRAP_REPLICATES", 100)
    rows = [
        _row(0, "no_evidence", status="failed_retained", regret=1.0),
        _row(0, "yoked_evidence", status="completed", regret=0.2),
        _row(1, "no_evidence", status="completed", regret=0.1),
        _row(1, "yoked_evidence", status="failed_retained", regret=1.0),
    ]

    result = combined._paired_condition_contrast(
        rows,
        treatment="yoked_evidence",
        control="no_evidence",
        population="synthetic",
    )

    assert result["paired_stratum_count"] == 2
    assert result["mean_failure_aware_normalized_regret_difference"] == pytest.approx(
        0.05
    )
    assert result["wins_ties_losses_on_regret"] == {
        "wins": 1,
        "ties": 0,
        "losses": 1,
    }
