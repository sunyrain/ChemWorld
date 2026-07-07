from __future__ import annotations

import json

from chemworld.cli import main


def test_cli_run_writes_manifest(tmp_path) -> None:
    trajectory = tmp_path / "run.jsonl"
    manifest = tmp_path / "run.manifest.json"
    main(
        [
            "run",
            "--agent",
            "random",
            "--budget",
            "3",
            "--seed",
            "9",
            "--output",
            str(trajectory),
            "--manifest",
            str(manifest),
        ]
    )

    assert trajectory.exists()
    payload = json.loads(manifest.read_text(encoding="utf-8"))
    assert payload["schema_version"] == "chemworld-submission-0.1"
    assert payload["trajectory_path"] == str(trajectory)
    assert payload["agent_manifest"]["agent_name"] == "random"
    assert payload["command"][0] == "chemworld"
    assert payload["source_digest"]
    assert "numpy" in payload["dependency_versions"]


def test_cli_evaluate_and_leaderboard(tmp_path) -> None:
    trajectory = tmp_path / "run.jsonl"
    result = tmp_path / "result.json"
    leaderboard = tmp_path / "leaderboard.csv"
    main(["run", "--agent", "lhs", "--budget", "4", "--seed", "10", "--output", str(trajectory)])
    main(["evaluate", "--submission", str(trajectory), "--output", str(result)])
    main(["leaderboard", "--results", str(result), "--output", str(leaderboard)])

    assert result.exists()
    result_payload = json.loads(result.read_text(encoding="utf-8"))
    assert 0.0 <= result_payload["total_score"] <= 1.0
    assert leaderboard.exists()
    assert "sem_total_score" in leaderboard.read_text(encoding="utf-8")
