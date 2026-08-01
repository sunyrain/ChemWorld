"""Launch the frozen G2 replication as a durable detached process."""

from __future__ import annotations

import argparse
import ctypes
import json
import os
import subprocess
import sys
from collections.abc import Mapping, Sequence
from copy import deepcopy
from ctypes import wintypes
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from scripts import run_g2_trajectory_replication as replication

from chemworld.eval.provenance import canonical_json_sha256, write_json_atomic

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = replication.DEFAULT_CONFIG
DEFAULT_OUTPUT_ROOT = replication.DEFAULT_OUTPUT_ROOT
DEFAULT_LAUNCH_LOG_ROOT = (
    ROOT
    / "runs/development/"
    "g2-autonomous-material-seed1-seed3-r5-codex-sol-medium-v1-launcher"
)
RECEIPT_SCHEMA_VERSION = "chemworld-g2-detached-launch-receipt-0.1"


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _process_alive(pid: int) -> bool:
    if pid <= 0:
        return False
    if os.name != "nt":
        try:
            os.kill(pid, 0)
        except (OSError, ProcessLookupError):
            return False
        return True
    process_query_limited_information = 0x1000
    still_active = 259
    kernel32 = ctypes.windll.kernel32  # type: ignore[attr-defined]
    kernel32.OpenProcess.argtypes = [
        wintypes.DWORD,
        wintypes.BOOL,
        wintypes.DWORD,
    ]
    kernel32.OpenProcess.restype = wintypes.HANDLE
    kernel32.GetExitCodeProcess.argtypes = [
        wintypes.HANDLE,
        ctypes.POINTER(wintypes.DWORD),
    ]
    kernel32.GetExitCodeProcess.restype = wintypes.BOOL
    kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
    kernel32.CloseHandle.restype = wintypes.BOOL
    handle = kernel32.OpenProcess(
        process_query_limited_information,
        False,
        pid,
    )
    if not handle:
        return False
    try:
        exit_code = wintypes.DWORD()
        if not kernel32.GetExitCodeProcess(handle, ctypes.byref(exit_code)):
            return False
        return int(exit_code.value) == still_active
    finally:
        kernel32.CloseHandle(handle)


def _load_receipt(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise RuntimeError(f"invalid detached launch receipt: {path}") from error
    if not isinstance(payload, dict):
        raise RuntimeError(f"detached launch receipt is not an object: {path}")
    unhashed = dict(payload)
    declared = unhashed.pop("receipt_sha256", None)
    if declared != canonical_json_sha256(unhashed):
        raise RuntimeError(f"detached launch receipt hash mismatch: {path}")
    return payload


def _launch_attempt_directories(log_root: Path) -> list[Path]:
    if not log_root.is_dir():
        return []
    attempts: list[tuple[int, Path]] = []
    for path in log_root.iterdir():
        if not path.is_dir():
            continue
        parts = path.name.split("-")
        if len(parts) != 2 or parts[0] != "launch" or not parts[1].isdigit():
            raise RuntimeError(
                f"unexpected directory in detached launch log root: {path.name}"
            )
        attempts.append((int(parts[1]), path))
    attempts.sort()
    expected = list(range(1, len(attempts) + 1))
    observed = [number for number, _ in attempts]
    if observed != expected:
        raise RuntimeError("detached launch attempt numbering is not contiguous")
    return [path for _, path in attempts]


def _guard_no_active_launcher(log_root: Path) -> None:
    attempts = _launch_attempt_directories(log_root)
    if not attempts:
        return
    receipt_path = attempts[-1] / "launch_receipt.json"
    if not receipt_path.is_file():
        raise RuntimeError("latest detached launch attempt lacks its receipt")
    receipt = _load_receipt(receipt_path)
    if _process_alive(int(receipt["process_id"])):
        raise RuntimeError(
            "the latest detached replication launcher is still active: "
            f"PID {receipt['process_id']}"
        )


def _runner_command(
    *,
    config_path: Path,
    output_root: Path,
    resume: bool,
) -> list[str]:
    command = [
        sys.executable,
        "-m",
        "scripts.run_g2_trajectory_replication",
        "--config",
        str(config_path),
        "--output-root",
        str(output_root),
        "--allow-external-provider",
    ]
    if resume:
        command.append("--resume")
    return command


def _launch_receipt(
    *,
    process_id: int,
    command: Sequence[str],
    config_path: Path,
    output_root: Path,
    launch_attempt_root: Path,
    source: Mapping[str, Any],
    schedule_sha256: str,
    resume: bool,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "schema_version": RECEIPT_SCHEMA_VERSION,
        "launched_at": _now(),
        "process_id": process_id,
        "detached": True,
        "resume": resume,
        "command": list(command),
        "working_directory": str(ROOT),
        "config_path": str(config_path),
        "output_root": str(output_root),
        "stdout_path": str(launch_attempt_root / "stdout.log"),
        "stderr_path": str(launch_attempt_root / "stderr.log"),
        "schedule_sha256": schedule_sha256,
        "source": deepcopy(dict(source)),
    }
    payload["receipt_sha256"] = canonical_json_sha256(payload)
    return payload


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument(
        "--launch-log-root",
        type=Path,
        default=DEFAULT_LAUNCH_LOG_ROOT,
    )
    parser.add_argument("--resume", action="store_true")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate source and frozen schedule without starting a process.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    config_path = args.config.resolve()
    output_root = args.output_root.resolve()
    log_root = args.launch_log_root.resolve()
    protocol = replication._load_protocol(config_path)
    schedule = replication._scheduled_cells(protocol)
    source = replication._source_manifest(config_path)
    if source["worktree_dirty"]:
        raise RuntimeError("formal detached launch requires a clean worktree")
    schedule_sha256 = canonical_json_sha256(schedule)
    if args.dry_run:
        report = replication._dry_run_report(protocol=protocol, source=source)
        report["detached_launcher_ready"] = True
        report["command"] = _runner_command(
            config_path=config_path,
            output_root=output_root,
            resume=bool(args.resume),
        )
        print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
        return 0

    if args.resume:
        if not (output_root / "matrix_manifest.json").is_file():
            raise RuntimeError("detached resume requires an existing matrix manifest")
    elif output_root.exists():
        raise FileExistsError(
            f"refusing to overwrite existing formal output root: {output_root}"
        )
    _guard_no_active_launcher(log_root)
    attempts = _launch_attempt_directories(log_root)
    launch_attempt_root = log_root / f"launch-{len(attempts) + 1:02d}"
    launch_attempt_root.mkdir(parents=True, exist_ok=False)
    stdout_path = launch_attempt_root / "stdout.log"
    stderr_path = launch_attempt_root / "stderr.log"
    command = _runner_command(
        config_path=config_path,
        output_root=output_root,
        resume=bool(args.resume),
    )
    creationflags = 0
    popen_kwargs: dict[str, Any] = {}
    if os.name == "nt":
        creationflags = (
            subprocess.CREATE_NEW_PROCESS_GROUP
            | subprocess.CREATE_NO_WINDOW
            | subprocess.DETACHED_PROCESS
        )
    else:
        popen_kwargs["start_new_session"] = True
    with (
        stdout_path.open("xb") as stdout_stream,
        stderr_path.open("xb") as stderr_stream,
    ):
        process = subprocess.Popen(
            command,
            cwd=ROOT,
            stdin=subprocess.DEVNULL,
            stdout=stdout_stream,
            stderr=stderr_stream,
            close_fds=True,
            creationflags=creationflags,
            **popen_kwargs,
        )
    receipt = _launch_receipt(
        process_id=process.pid,
        command=command,
        config_path=config_path,
        output_root=output_root,
        launch_attempt_root=launch_attempt_root,
        source=source,
        schedule_sha256=schedule_sha256,
        resume=bool(args.resume),
    )
    write_json_atomic(launch_attempt_root / "launch_receipt.json", receipt)
    print(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = [
    "DEFAULT_CONFIG",
    "DEFAULT_LAUNCH_LOG_ROOT",
    "DEFAULT_OUTPUT_ROOT",
    "RECEIPT_SCHEMA_VERSION",
    "main",
]
