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
    assert result_payload["verified"] is True
    assert result_payload["verification"]["verified"] is True
    assert len(result_payload["trajectory_sha256"]) == 64
    assert leaderboard.exists()
    assert "sem_total_score" in leaderboard.read_text(encoding="utf-8")


def test_cli_tasks_and_run_task(tmp_path, capsys) -> None:
    trajectory = tmp_path / "task_run.jsonl"
    explicit = tmp_path / "explicit_run.jsonl"
    main(["tasks", "list"])
    main(["tasks", "show", "reaction-to-assay"])
    main(["tasks", "card", "reaction-optimization-standard"])
    output = capsys.readouterr().out
    assert "reaction-optimization-standard" in output
    assert "reaction-to-assay" in output
    assert "baseline_reference_scores" in output

    main(
        [
            "run",
            "--task",
            "reaction-to-assay",
            "--agent",
            "random",
            "--output",
            str(trajectory),
        ]
    )
    first_record = json.loads(trajectory.read_text(encoding="utf-8").splitlines()[0])
    assert first_record["world_split"] == "public-dev"
    assert first_record["objective"] == "balanced"
    assert first_record["seed"] == 0

    main(
        [
            "run",
            "--env",
            "ChemWorld",
            "--world-split",
            "public-dev",
            "--objective",
            "balanced",
            "--budget",
            "18",
            "--seed",
            "0",
            "--agent",
            "random",
            "--output",
            str(explicit),
        ]
    )
    task_records = [
        json.loads(line) for line in trajectory.read_text(encoding="utf-8").splitlines()
    ]
    explicit_records = [
        json.loads(line) for line in explicit.read_text(encoding="utf-8").splitlines()
    ]
    assert len(task_records) == len(explicit_records)
    for task_record, explicit_record in zip(task_records, explicit_records, strict=True):
        assert task_record["action"] == explicit_record["action"]
        assert task_record["observation"] == explicit_record["observation"]
        assert task_record["reward"] == explicit_record["reward"]


def test_cli_seeds_show(capsys) -> None:
    main(["seeds", "show"])
    output = capsys.readouterr().out
    payload = json.loads(output)

    assert payload["schema_version"] == "chemworld-seed-suite-0.1"
    assert "reaction-to-assay" in payload["task_seed_plan"]
    assert payload["private_eval_salt_policy"]["salt_environment_variable"] == (
        "CHEMWORLD_PRIVATE_EVAL_SALT"
    )
