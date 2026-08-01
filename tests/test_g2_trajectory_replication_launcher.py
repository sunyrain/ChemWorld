from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest
from scripts import launch_g2_trajectory_replication as launcher

from chemworld.eval.provenance import canonical_json_sha256


def _source(*, dirty: bool = False) -> dict[str, Any]:
    return {
        "git_commit": "test-commit",
        "worktree_dirty": dirty,
        "material_source_tree_sha256": "test-tree",
        "protocol_file_sha256": "test-protocol",
    }


def test_runner_command_binds_config_output_and_resume() -> None:
    command = launcher._runner_command(
        config_path=Path("C:/repo/protocol.json"),
        output_root=Path("C:/repo/formal-run"),
        resume=True,
    )

    assert command[1:3] == ["-m", "scripts.run_g2_trajectory_replication"]
    assert command[-2:] == ["--allow-external-provider", "--resume"]
    assert command[command.index("--config") + 1] == "C:\\repo\\protocol.json"
    assert command[command.index("--output-root") + 1] == "C:\\repo\\formal-run"


def test_launch_receipt_is_content_hashed(tmp_path: Path) -> None:
    receipt = launcher._launch_receipt(
        process_id=123,
        command=["python", "-m", "runner"],
        config_path=tmp_path / "protocol.json",
        output_root=tmp_path / "formal-run",
        launch_attempt_root=tmp_path / "launch-01",
        source=_source(),
        schedule_sha256="schedule",
        resume=False,
    )

    unhashed = dict(receipt)
    declared = unhashed.pop("receipt_sha256")
    assert declared == canonical_json_sha256(unhashed)
    assert receipt["detached"] is True
    assert receipt["process_id"] == 123


def test_guard_rejects_an_active_previous_launcher(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    attempt = tmp_path / "launch-01"
    attempt.mkdir()
    receipt = launcher._launch_receipt(
        process_id=456,
        command=["python"],
        config_path=tmp_path / "protocol.json",
        output_root=tmp_path / "formal-run",
        launch_attempt_root=attempt,
        source=_source(),
        schedule_sha256="schedule",
        resume=False,
    )
    (attempt / "launch_receipt.json").write_text(
        json.dumps(receipt),
        encoding="utf-8",
    )
    monkeypatch.setattr(launcher, "_process_alive", lambda pid: pid == 456)

    with pytest.raises(RuntimeError, match="still active"):
        launcher._guard_no_active_launcher(tmp_path)


def _patch_protocol(
    monkeypatch: pytest.MonkeyPatch,
    *,
    dirty: bool = False,
) -> None:
    monkeypatch.setattr(
        launcher.replication,
        "_load_protocol",
        lambda path: {"protocol_id": "test-protocol"},
    )
    monkeypatch.setattr(
        launcher.replication,
        "_scheduled_cells",
        lambda protocol: [{"cell_id": "cell-001"}],
    )
    monkeypatch.setattr(
        launcher.replication,
        "_source_manifest",
        lambda path: _source(dirty=dirty),
    )


def test_dry_run_requires_a_clean_source_and_never_launches(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    _patch_protocol(monkeypatch)
    monkeypatch.setattr(
        launcher.replication,
        "_dry_run_report",
        lambda **kwargs: {"passed": True, "planned_cells": 20},
    )
    monkeypatch.setattr(
        launcher.subprocess,
        "Popen",
        lambda *args, **kwargs: pytest.fail("dry run started a process"),
    )

    assert launcher.main(
        [
            "--config",
            str(tmp_path / "protocol.json"),
            "--output-root",
            str(tmp_path / "formal-run"),
            "--launch-log-root",
            str(tmp_path / "logs"),
            "--dry-run",
        ]
    ) == 0
    report = json.loads(capsys.readouterr().out)
    assert report["passed"] is True
    assert report["detached_launcher_ready"] is True
    assert report["command"][-1] == "--allow-external-provider"

    _patch_protocol(monkeypatch, dirty=True)
    with pytest.raises(RuntimeError, match="clean worktree"):
        launcher.main(
            [
                "--config",
                str(tmp_path / "protocol.json"),
                "--dry-run",
            ]
        )


def test_launch_writes_immutable_logs_and_receipt(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    _patch_protocol(monkeypatch)
    observed: dict[str, Any] = {}

    class FakeProcess:
        pid = 789

    def popen(command: list[str], **kwargs: Any) -> FakeProcess:
        observed["command"] = command
        observed["kwargs"] = kwargs
        return FakeProcess()

    monkeypatch.setattr(launcher.subprocess, "Popen", popen)
    output_root = tmp_path / "formal-run"
    log_root = tmp_path / "logs"
    assert launcher.main(
        [
            "--config",
            str(tmp_path / "protocol.json"),
            "--output-root",
            str(output_root),
            "--launch-log-root",
            str(log_root),
        ]
    ) == 0

    receipt_path = log_root / "launch-01" / "launch_receipt.json"
    receipt = launcher._load_receipt(receipt_path)
    assert receipt["process_id"] == 789
    assert receipt["output_root"] == str(output_root.resolve())
    assert Path(receipt["stdout_path"]).is_file()
    assert Path(receipt["stderr_path"]).is_file()
    assert observed["command"][-1] == "--allow-external-provider"
    assert observed["kwargs"]["stdin"] is launcher.subprocess.DEVNULL
    assert json.loads(capsys.readouterr().out)["receipt_sha256"] == (
        receipt["receipt_sha256"]
    )
