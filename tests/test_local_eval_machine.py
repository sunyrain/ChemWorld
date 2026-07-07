from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def test_local_eval_machine_demo(tmp_path: Path) -> None:
    workspace = tmp_path / "eval_machine"
    script = Path("local_eval_server") / "teacher_side" / "eval_machine.py"
    result = subprocess.run(
        [
            sys.executable,
            str(script),
            "--workspace",
            str(workspace),
            "demo",
            "--tasks",
            "reaction-to-assay",
            "--seeds",
            "0",
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    payload = json.loads(result.stdout)
    assert payload["result_count"] == 1
    leaderboard = workspace / "published" / "demo_eval_leaderboard.json"
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
    assert trajectory.exists()
    assert json.loads(verification.read_text(encoding="utf-8"))["verified"]
