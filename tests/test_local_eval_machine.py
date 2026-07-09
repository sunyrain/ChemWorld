from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

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
