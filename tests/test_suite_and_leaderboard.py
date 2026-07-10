from __future__ import annotations

import pytest

from chemworld.eval.leaderboard import aggregate_leaderboard
from chemworld.eval.suite import run_suite


def test_suite_runs_and_reports_public_private_gap(tmp_path) -> None:
    results = run_suite(
        agent_name="random",
        env_id="ChemWorld",
        world_splits=["public-test", "private-eval"],
        seeds=[0, 1],
        budget=3,
        objective="balanced",
        output_dir=tmp_path,
    )
    assert len(results) == 4
    rows = aggregate_leaderboard(results)
    assert len(rows) == 2
    assert all("public_private_gap" in row for row in rows)
    assert all("ci95_total_score_low" in row for row in rows)
    assert all("sem_total_score" in row for row in rows)
    assert all(result["verified"] for result in results)


def test_leaderboard_rejects_unverified_result() -> None:
    with pytest.raises(ValueError, match="verified evaluation-result schema"):
        aggregate_leaderboard(
            [
                {
                    "agent_name": "forged",
                    "world_split": "public-test",
                    "total_score": 1.0,
                    "final_best_score": 1.0,
                    "safety_aware_score": 1.0,
                }
            ]
        )


def test_leaderboard_recomputes_metrics_from_verified_trajectory(tmp_path) -> None:
    results = run_suite(
        agent_name="random",
        env_id="ChemWorld",
        world_splits=["public-test"],
        seeds=[0],
        budget=3,
        objective="balanced",
        output_dir=tmp_path,
    )
    results[0]["total_score"] = 1.0

    with pytest.raises(ValueError, match="does not match trajectory evaluation"):
        aggregate_leaderboard(results)
