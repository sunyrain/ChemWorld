from __future__ import annotations

import json
import subprocess
import sys


def test_release_gate_dry_run_lists_required_commands(tmp_path) -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "scripts/run_release_gate.py",
            "--dry-run",
            "--output-dir",
            str(tmp_path / "gate"),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    plan = json.loads(completed.stdout)
    names = [item["name"] for item in plan]
    assert names == [
        "lint",
        "type_check",
        "tests",
        "docs",
        "runtime_boundary_audit",
        "environment_audit",
        "baseline_smoke",
    ]
    flat_commands = [" ".join(item["command"]) for item in plan]
    assert any("ruff check ." in command for command in flat_commands)
    assert any("mypy src/chemworld" in command for command in flat_commands)
    assert any("pytest" in command for command in flat_commands)
    assert any("mkdocs build --strict" in command for command in flat_commands)
    assert any("audit_environment_consistency.py" in command for command in flat_commands)
    assert any("baselines report" in command for command in flat_commands)
