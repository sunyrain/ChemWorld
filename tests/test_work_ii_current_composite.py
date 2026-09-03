from __future__ import annotations

import json
from pathlib import Path

import pytest
from scripts.run_work_ii_current_composite_evaluator import _render_markdown

from chemworld.eval.work_ii_current_composite import (
    _compact_checkpoint,
    _terminal_state,
    _validate_checkpoint_schedule,
)

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT_STAGES = (
    "pre_evidence",
    "after_experiment_2",
    "after_experiment_4",
    "after_experiment_6",
    "final",
)


def test_terminal_state_preserves_failure_and_censoring_denominators() -> None:
    assert _terminal_state(
        qualification_passed=True,
        completed_experiments=8,
        scheduled_experiments=8,
        failed_checks=[],
    ) == ("completed", "qualification_passed")
    assert _terminal_state(
        qualification_passed=False,
        completed_experiments=7,
        scheduled_experiments=8,
        failed_checks=["final_recommendation_present"],
    ) == (
        "right_censored",
        "participant_stopped_before_planned_experiment_count",
    )
    assert _terminal_state(
        qualification_passed=False,
        completed_experiments=8,
        scheduled_experiments=8,
        failed_checks=["final_recommendation_present"],
    ) == (
        "failed",
        "qualification_contract_failed_after_planned_experiments:"
        "final_recommendation_present",
    )


def test_right_censored_checkpoint_schedule_accepts_only_an_ordered_prefix() -> None:
    _validate_checkpoint_schedule(
        cell_id="right-censored-cell",
        observed_stages=SNAPSHOT_STAGES[:-1],
        snapshot_stages=SNAPSHOT_STAGES,
        terminal_state="right_censored",
    )

    for observed in (
        (
            "pre_evidence",
            "after_experiment_4",
        ),
        (
            "pre_evidence",
            "after_experiment_4",
            "after_experiment_2",
        ),
        (
            "pre_evidence",
            "after_experiment_2",
            "after_experiment_2",
        ),
    ):
        with pytest.raises(ValueError, match="checkpoint schedule differs from config"):
            _validate_checkpoint_schedule(
                cell_id="right-censored-cell",
                observed_stages=observed,
                snapshot_stages=SNAPSHOT_STAGES,
                terminal_state="right_censored",
            )


def test_non_censored_checkpoint_schedule_requires_the_frozen_final_stage() -> None:
    for terminal_state in ("completed", "failed"):
        with pytest.raises(ValueError, match="checkpoint schedule differs from config"):
            _validate_checkpoint_schedule(
                cell_id=f"{terminal_state}-cell",
                observed_stages=SNAPSHOT_STAGES[:-1],
                snapshot_stages=SNAPSHOT_STAGES,
                terminal_state=terminal_state,
            )


def test_compact_checkpoint_keeps_estimands_but_drops_per_query_terms() -> None:
    compact = _compact_checkpoint(
        {
            "terminal_state": "completed",
            "scheduled_snapshot_count": 5,
            "observed_snapshot_count": 5,
            "scored_snapshot_count": 5,
            "checkpoint_scores": {
                "pre_evidence": {
                    "error": 0.4,
                    "term_count": 16,
                    "terms": [{"query_id": "q-1", "error": 0.2}],
                },
                "final": {
                    "error": 0.1,
                    "term_count": 16,
                    "terms": [{"query_id": "q-1", "error": 0.0}],
                },
            },
            "unscorable_snapshots": [],
            "effective_pre_error": 0.4,
            "effective_final_error": 0.1,
            "effective_final_stage": "final",
            "primary_improvement": 0.3,
            "confirmatory_improvement_bounds": [0.3, 0.3],
            "missing_failure_rule": "observed_final",
        }
    )

    assert compact["primary_improvement"] == 0.3
    assert compact["confirmatory_improvement_bounds"] == [0.3, 0.3]
    assert compact["checkpoint_scores"]["pre_evidence"] == {
        "error": 0.4,
        "term_count": 16,
    }
    assert "terms" not in compact["checkpoint_scores"]["final"]


def test_current_composite_markdown_renderer_binds_all_locus_gate_shapes() -> None:
    report = json.loads(
        (
            ROOT
            / "workstreams/flagship_tasks/reports/"
            "work-ii-deepseek-c2-current-composite-evaluation-v0.2.json"
        ).read_text(encoding="utf-8")
    )

    markdown = _render_markdown(report)

    assert "| A_E | -0.2138 | -0.3592 | 0.990148 |" in markdown
    assert "| A_P | 0.0326 | -0.0063 | 0.079130 |" in markdown
    assert "| A_S | -0.2241 | -0.6286 | 1.000000 |" in markdown
    assert "50/1/84" in markdown
    assert "1/119/1" in markdown
