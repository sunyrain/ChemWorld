from __future__ import annotations

from chemworld.eval.leaderboard import aggregate_leaderboard
from chemworld.eval.suite import run_suite


def test_suite_runs_and_reports_public_private_gap(tmp_path) -> None:
    results = run_suite(
        agent_name="random",
        env_id="BatchReactorWorld",
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

