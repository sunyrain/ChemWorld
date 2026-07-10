from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest
from local_eval_server.teacher_side.eval_machine import (
    accept_submissions,
    student_process_environment,
    validate_submission,
    workspace_paths,
)

SCRIPT = Path("local_eval_server") / "teacher_side" / "eval_machine.py"


def _run_eval_machine(workspace: Path, *args: str) -> dict:
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--workspace",
            str(workspace),
            *args,
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)


def _write_submission(
    path: Path,
    *,
    team_id: str = "team_safe",
    entrypoint: str = "agent:make_agent",
    dependency_file: str = "requirements.txt",
) -> None:
    path.mkdir(parents=True)
    (path / "agent.py").write_text("def make_agent(): return object()\n", encoding="utf-8")
    (path / "requirements.txt").write_text("", encoding="utf-8")
    (path / "manifest.json").write_text(
        json.dumps(
            {
                "team_id": team_id,
                "agent_name": "safe test",
                "agent_family": "test",
                "entrypoint": entrypoint,
                "dependency_file": dependency_file,
                "llm_used": False,
                "allowed_network": False,
            }
        ),
        encoding="utf-8",
    )


def test_local_eval_machine_demo(tmp_path: Path) -> None:
    workspace = tmp_path / "eval_machine"
    payload = _run_eval_machine(
        workspace,
        "demo",
        "--tasks",
        "reaction-to-assay",
        "--seeds",
        "0",
    )

    assert payload["result_count"] == 1
    leaderboard = workspace / "published" / "demo_eval_leaderboard.json"
    summary = workspace / "published" / "demo_eval_summary.json"
    trajectory = (
        workspace
        / "runs"
        / "demo_eval"
        / "team_alpha"
        / "trajectories"
        / "reaction-to-assay_seed0.jsonl"
    )
    verification = (
        workspace
        / "runs"
        / "demo_eval"
        / "team_alpha"
        / "verify"
        / "reaction-to-assay_seed0.json"
    )
    assert leaderboard.exists()
    assert summary.exists()
    assert trajectory.exists()
    assert payload["summary"]["verified_count"] == 1
    assert payload["summary"]["failed_verifications"] == []
    assert json.loads(verification.read_text(encoding="utf-8"))["verified"]


def test_local_eval_machine_manual_validate_run_summarize(tmp_path: Path) -> None:
    workspace = tmp_path / "manual_eval_machine"

    init_payload = _run_eval_machine(workspace, "init-demo")
    validate_payload = _run_eval_machine(workspace, "validate")
    run_payload = _run_eval_machine(
        workspace,
        "run",
        "--tasks",
        "reaction-to-assay",
        "--seeds",
        "0",
    )
    summary_payload = _run_eval_machine(workspace, "summarize", "--run-id", "demo_eval")

    assert init_payload["initialized"]
    assert validate_payload["accepted"] == ["team_alpha"]
    assert run_payload["result_count"] == 1
    assert summary_payload["result_count"] == 1
    assert summary_payload["team_count"] == 1
    assert summary_payload["task_count"] == 1
    assert summary_payload["verification_count"] == 1
    assert summary_payload["verified_count"] == 1
    assert summary_payload["failed_verifications"] == []
    assert Path(summary_payload["leaderboard_json"]).exists()
    assert Path(summary_payload["leaderboard_csv"]).exists()
    assert Path(summary_payload["summary_json"]).exists()


@pytest.mark.parametrize(
    "team_id",
    ("../teacher_private", "team.with.dot", "team with space", "/absolute", "x" * 65),
)
def test_submission_validation_rejects_unsafe_team_ids(
    tmp_path: Path,
    team_id: str,
) -> None:
    submission = tmp_path / "submission"
    _write_submission(submission, team_id=team_id)

    with pytest.raises(ValueError, match="team_id"):
        validate_submission(submission)


@pytest.mark.parametrize(
    ("entrypoint", "dependency_file", "message"),
    (
        ("../agent:make_agent", "requirements.txt", "entrypoint"),
        ("agent", "requirements.txt", "entrypoint"),
        ("agent:make-agent", "requirements.txt", "entrypoint"),
        ("agent:make_agent", "../outside.txt", "dependency_file"),
    ),
)
def test_submission_validation_rejects_paths_outside_submission(
    tmp_path: Path,
    entrypoint: str,
    dependency_file: str,
    message: str,
) -> None:
    submission = tmp_path / "submission"
    _write_submission(
        submission,
        entrypoint=entrypoint,
        dependency_file=dependency_file,
    )
    (tmp_path / "outside.txt").write_text("outside", encoding="utf-8")

    with pytest.raises(ValueError, match=message):
        validate_submission(submission)


def test_malicious_manifest_cannot_escape_accepted_directory(tmp_path: Path) -> None:
    workspace = tmp_path / "workspace"
    paths = workspace_paths(workspace)
    for path in paths.values():
        path.mkdir(parents=True, exist_ok=True)
    protected = workspace / "protected"
    protected.mkdir()
    marker = protected / "marker.txt"
    marker.write_text("preserve", encoding="utf-8")
    _write_submission(paths["incoming"] / "malicious", team_id="../../protected")

    accepted = accept_submissions(workspace)

    assert accepted == []
    assert marker.read_text(encoding="utf-8") == "preserve"
    assert (paths["rejected"] / "malicious" / "rejection_reason.txt").exists()


def test_student_process_uses_environment_allowlist(tmp_path: Path, monkeypatch) -> None:
    submission_path = tmp_path / "submission"
    _write_submission(submission_path)
    submission = validate_submission(submission_path)
    monkeypatch.setenv("CHEMWORLD_PRIVATE_EVAL_SALT", "do-not-leak")
    monkeypatch.setenv("UNRELATED_HOST_SECRET", "do-not-leak")
    monkeypatch.setenv("PYTHONPATH", "untrusted-inherited-path")

    env = student_process_environment(submission)

    assert "CHEMWORLD_PRIVATE_EVAL_SALT" not in env
    assert "UNRELATED_HOST_SECRET" not in env
    assert "untrusted-inherited-path" not in env["PYTHONPATH"]
    assert str(submission.path) in env["PYTHONPATH"]
    assert env["PYTHONNOUSERSITE"] == "1"
