from __future__ import annotations

import importlib.util
import json
from argparse import Namespace
from pathlib import Path
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/run_work_ii_ae_v03_shard_group.py"
CONTRACT = ROOT / "configs/benchmark/work_ii_ae_prior_distinguishability_v0.3_candidate.json"


def _script_module():
    spec = importlib.util.spec_from_file_location("ae_v03_shard_group_script", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _args(tmp_path: Path, phase: str = "classifier_validation") -> Namespace:
    return Namespace(
        contract=CONTRACT,
        phase=phase,
        output=tmp_path / "output",
        shard_root=tmp_path / "shards",
        shard_count=4,
        import_prefix=None,
        import_prefix_count=0,
        progress_interval=60.0,
        fit_report=tmp_path / "fit/report.json",
        fit_plan=tmp_path / "fit/plan.json",
        fit_receipts=tmp_path / "fit/receipts",
        validation_report=None,
        validation_plan=None,
        validation_receipts=None,
        screen_report=None,
        screen_plan=None,
        screen_receipts=None,
        selection=None,
    )


class _FakeProcess:
    def __init__(self, code: int | None, pid: int) -> None:
        self.code = code
        self.pid = pid
        self.terminated = False
        self.killed = False

    def poll(self) -> int | None:
        return self.code

    def terminate(self) -> None:
        self.terminated = True
        self.code = -15

    def kill(self) -> None:
        self.killed = True
        self.code = -9

    def wait(self, timeout: float | None = None) -> int:
        assert timeout is None or timeout > 0
        assert self.code is not None
        return self.code


def test_classifier_fit_group_keeps_full_denominator_and_starts_from_zero(
    tmp_path: Path,
) -> None:
    module = _script_module()
    args = _args(tmp_path, "classifier_fit")
    args.fit_report = None
    args.fit_plan = None
    args.fit_receipts = None

    assert module._expected_receipts(args) == 14_400
    workers, merge = module.build_group_commands(args)
    assert len(workers) == 4
    for command in (*workers, merge):
        assert command[command.index("--import-prefix-count") + 1] == "0"
        assert "--import-prefix" not in command


def test_group_commands_pass_every_upstream_binding_to_workers_and_merge(
    tmp_path: Path,
) -> None:
    module = _script_module()
    args = _args(tmp_path, "confirmation")
    args.validation_report = tmp_path / "validation/report.json"
    args.validation_plan = tmp_path / "validation/plan.json"
    args.validation_receipts = tmp_path / "validation/receipts"
    args.screen_report = tmp_path / "screen/report.json"
    args.screen_plan = tmp_path / "screen/plan.json"
    args.screen_receipts = tmp_path / "screen/receipts"
    args.selection = tmp_path / "screen/selection.json"
    workers, merge = module.build_group_commands(args)
    assert len(workers) == 4
    assert [command[command.index("--shard-index") + 1] for command in workers] == [
        "0",
        "1",
        "2",
        "3",
    ]
    for option in (
        "--fit-report",
        "--fit-plan",
        "--fit-receipts",
        "--validation-report",
        "--validation-plan",
        "--validation-receipts",
        "--screen-report",
        "--screen-plan",
        "--screen-receipts",
        "--selection",
    ):
        assert option in merge
        assert all(option in command for command in workers)
    assert "--merge" in merge
    assert merge[merge.index("--output") + 1] == str(args.output.resolve())


def test_worker_failure_terminates_peers_and_never_starts_merge(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    module = _script_module()
    args = _args(tmp_path)
    commands = [("worker", str(index)) for index in range(4)]
    peers = [_FakeProcess(3, 100), *[_FakeProcess(None, 101 + i) for i in range(3)]]
    spawned: list[tuple[str, ...]] = []
    monkeypatch.setattr(module, "_expected_receipts", lambda _args: 48)
    monkeypatch.setattr(
        module, "build_group_commands", lambda _args: (commands, ("merge",))
    )

    def fake_spawn(command: tuple[str, ...], _log: Path) -> _FakeProcess:
        spawned.append(command)
        return peers[len(spawned) - 1]

    monkeypatch.setattr(module, "_spawn", fake_spawn)
    assert module.run_group(args) == 3
    assert spawned == commands
    assert all(process.terminated for process in peers[1:])
    failure = json.loads(
        (args.shard_root / "group-failure.json").read_text(encoding="utf-8")
    )
    assert failure["status"] == "failed"
    assert failure["stage"] == "execute"
    assert failure["restart_required_from_execution_zero"] is True
    assert not args.output.exists()


def test_all_workers_exit_zero_then_merge_runs_exactly_once(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    module = _script_module()
    args = _args(tmp_path)
    commands = [("worker", str(index)) for index in range(4)]
    merge = ("merge",)
    spawned: list[tuple[str, ...]] = []
    monkeypatch.setattr(module, "_expected_receipts", lambda _args: 0)
    monkeypatch.setattr(module, "_receipt_count", lambda _root: 0)
    monkeypatch.setattr(
        module, "build_group_commands", lambda _args: (commands, merge)
    )

    def fake_spawn(command: tuple[str, ...], _log: Path) -> _FakeProcess:
        spawned.append(command)
        if command == merge:
            args.output.mkdir()
            (args.output / "report.json").write_text("{}\n", encoding="utf-8")
        return _FakeProcess(0, 200 + len(spawned))

    monkeypatch.setattr(module, "_spawn", fake_spawn)
    assert module.run_group(args) == 0
    assert spawned == [*commands, merge]
    completion = json.loads(
        (args.shard_root / "group-completed.json").read_text(encoding="utf-8")
    )
    assert completion["worker_return_codes"] == [0, 0, 0, 0]
    assert completion["merge_return_code"] == 0
    assert not (args.shard_root / "group-failure.json").exists()


def test_progress_reports_completed_total_throughput_and_eta(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    module = _script_module()
    args = _args(tmp_path)
    args.shard_root.mkdir()
    for shard_index in range(2):
        receipts = args.shard_root / f"shard-{shard_index:05d}-of-00004/receipts"
        receipts.mkdir(parents=True)
        for index in range(6):
            (receipts / f"{index}.json").write_text("{}\n", encoding="utf-8")
    monkeypatch.setattr(module.time, "monotonic", lambda: 120.0)
    module._emit_progress(
        args=args,
        started=60.0,
        total=24,
        processes=[_FakeProcess(None, 1), _FakeProcess(0, 2)],
        stage="execute",
    )
    payload: dict[str, Any] = json.loads(capsys.readouterr().out)
    assert payload["completed"] == 12
    assert payload["total"] == 24
    assert payload["throughput_receipts_per_min"] == 12.0
    assert payload["eta_s"] == 60.0
