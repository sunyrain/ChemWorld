#!/usr/bin/env python3
"""Run a long ChemWorld command with structured progress heartbeats."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Any


def _jsonl_count(path: Path) -> int:
    if not path.is_file():
        return 0
    with path.open("r", encoding="utf-8") as handle:
        return sum(1 for line in handle if line.strip())


def _jsonl_rows(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            value = json.loads(line)
            if isinstance(value, dict):
                rows.append(value)
    return rows


def _newest_directory(
    root: Path,
    *,
    prefix: str,
    started_at: float,
) -> Path | None:
    candidates = [
        path
        for path in root.glob(f"{prefix}*")
        if path.is_dir() and path.stat().st_mtime >= started_at - 2.0
    ]
    return max(candidates, key=lambda path: path.stat().st_mtime, default=None)


def _rate_and_eta(
    *,
    completed: int,
    denominator: int,
    elapsed_s: float,
) -> tuple[float, float | None]:
    rate_per_minute = 60.0 * completed / elapsed_s if elapsed_s > 0.0 else 0.0
    eta_minutes = None
    if rate_per_minute > 0.0 and completed < denominator:
        eta_minutes = (denominator - completed) / rate_per_minute
    return rate_per_minute, eta_minutes


def composition_progress(
    *,
    temp_root: Path,
    started_at: float,
    elapsed_s: float,
    output: Path,
) -> dict[str, Any]:
    scratch = _newest_directory(
        temp_root,
        prefix="chemworld-composition-qualification-",
        started_at=started_at,
    )
    if scratch is None:
        return {
            "stage": "startup_or_finalization",
            "output_exists": output.is_file(),
        }

    files = list(scratch.glob("*.jsonl"))
    generated = [path for path in files if path.name.startswith("qualification-")]
    generated_completed = sum(path.stat().st_size > 0 for path in generated)
    reference = [path for path in files if not path.name.startswith("qualification-")]
    reference_completed = sum(path.stat().st_size > 0 for path in reference)
    active = max(files, key=lambda path: path.stat().st_mtime, default=None)

    if reference_completed < 1786:
        completed, denominator = reference_completed, 1786
        stage = "reference_recipes"
    elif generated_completed < 52:
        completed, denominator = generated_completed, 52
        stage = "generated_compositions"
    else:
        completed, denominator = 52, 52
        stage = "mutants_modules_interfaces_and_serialization"
    rate, eta = _rate_and_eta(
        completed=completed,
        denominator=denominator,
        elapsed_s=elapsed_s,
    )
    return {
        "stage": stage,
        "completed": completed,
        "denominator": denominator,
        "percent": round(100.0 * completed / denominator, 1),
        "rate_per_minute": round(rate, 2),
        "eta_minutes": None if eta is None else round(eta, 1),
        "active_unit": active.name if active is not None else None,
        "scratch_bytes": sum(path.stat().st_size for path in files),
        "output_exists": output.is_file(),
    }


def u05_progress(
    *,
    temp_root: Path,
    started_at: float,
    output: Path,
) -> dict[str, Any]:
    scratch = _newest_directory(
        temp_root,
        prefix="chemworld-first-paper-u05-",
        started_at=started_at,
    )
    if scratch is None:
        return {
            "stage": "startup_or_finalization",
            "output_exists": output.is_file(),
        }

    workspace = scratch / "interactive-workspace"
    sessions_root = workspace / ".ipc" / "sessions"
    sessions = [path for path in sessions_root.glob("*") if path.is_dir()]
    session = max(sessions, key=lambda path: path.stat().st_mtime, default=None)
    calls = (
        _jsonl_rows(session / "mcp_tool_calls.jsonl") if session is not None else []
    )
    history_path = workspace / "public" / "history.jsonl"
    history = _jsonl_rows(history_path)
    current_path = workspace / "public" / "current.json"
    current: dict[str, Any] = {}
    if current_path.is_file():
        value = json.loads(current_path.read_text(encoding="utf-8"))
        if isinstance(value, dict):
            current = value

    campaign_state = current.get("campaign_state", {})
    resources = current.get("campaign_resources", {}).get("state", {})
    report_only = resources.get("report_only", {})
    last = history[-1] if history else {}
    return {
        "stage": current.get("stage", "provider_session_startup"),
        "mcp_tool_call_count": len(calls),
        "mcp_step_count": sum(row.get("tool") == "step" for row in calls),
        "submitted_action_count": len(history),
        "committed_action_count": sum(
            row.get("transaction_status") == "committed" for row in history
        ),
        "last_action": last.get("action"),
        "last_transaction_status": last.get("transaction_status"),
        "operation_count": campaign_state.get("operation_count"),
        "remaining_operations": current.get("remaining_operations"),
        "process_time_used_s": report_only.get("process_time_s"),
        "process_time_limit_s": 10440.0,
        "instrument_uses": resources.get("instrument_uses"),
        "final_assays": resources.get("final_assays"),
        "lifecycle_done": campaign_state.get("done"),
        "trajectory_bytes": (
            (scratch / "trajectory.jsonl").stat().st_size
            if (scratch / "trajectory.jsonl").is_file()
            else 0
        ),
        "output_exists": output.is_file(),
    }


def static_s0_progress(
    *,
    progress_file: Path,
    output: Path,
) -> dict[str, Any]:
    if not progress_file.is_file():
        return {
            "stage": "startup",
            "progress_file_exists": False,
            "output_exists": output.is_file(),
        }
    value = json.loads(progress_file.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("static S0 progress file must contain one JSON object")
    return {
        **value,
        "progress_file_exists": True,
        "output_exists": output.is_file(),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--profile",
        choices=("composition", "u05", "static-s0"),
        required=True,
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--progress-file", type=Path)
    parser.add_argument("--interval-s", type=float, default=30.0)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    if args.command and args.command[0] == "--":
        args.command = args.command[1:]
    if not args.command:
        parser.error("a command is required after --")
    if args.interval_s <= 0.0:
        parser.error("--interval-s must be positive")
    if args.profile == "static-s0" and args.progress_file is None:
        parser.error("--progress-file is required for the static-s0 profile")
    return args


def _emit(value: dict[str, Any]) -> None:
    print(json.dumps(value, ensure_ascii=False, sort_keys=True), flush=True)


def main() -> int:
    args = parse_args()
    output = args.output.resolve()
    started_at = time.time()
    temp_root = Path(tempfile.gettempdir())
    with tempfile.TemporaryDirectory(prefix="chemworld-progress-wrapper-") as log_dir:
        log_root = Path(log_dir)
        stdout_path = log_root / "stdout.log"
        stderr_path = log_root / "stderr.log"
        with stdout_path.open("w", encoding="utf-8") as stdout, stderr_path.open(
            "w", encoding="utf-8"
        ) as stderr:
            process = subprocess.Popen(
                args.command,
                cwd=Path.cwd(),
                stdout=stdout,
                stderr=stderr,
                text=True,
                env=os.environ.copy(),
            )
            _emit(
                {
                    "event": "started",
                    "profile": args.profile,
                    "pid": process.pid,
                    "output": str(output),
                }
            )
            while process.poll() is None:
                time.sleep(args.interval_s)
                elapsed_s = time.time() - started_at
                if args.profile == "composition":
                    progress = composition_progress(
                        temp_root=temp_root,
                        started_at=started_at,
                        elapsed_s=elapsed_s,
                        output=output,
                    )
                elif args.profile == "u05":
                    progress = u05_progress(
                        temp_root=temp_root,
                        started_at=started_at,
                        output=output,
                    )
                else:
                    progress = static_s0_progress(
                        progress_file=args.progress_file.resolve(),
                        output=output,
                    )
                _emit(
                    {
                        "event": "progress",
                        "profile": args.profile,
                        "pid": process.pid,
                        "elapsed_s": round(elapsed_s, 1),
                        **progress,
                    }
                )
            return_code = process.wait()

        final = {
            "event": "finished",
            "profile": args.profile,
            "pid": process.pid,
            "return_code": return_code,
            "elapsed_s": round(time.time() - started_at, 1),
            "output_exists": output.is_file(),
        }
        if return_code != 0:
            final["stderr_tail"] = stderr_path.read_text(
                encoding="utf-8", errors="replace"
            ).splitlines()[-20:]
        _emit(final)
        return return_code


if __name__ == "__main__":
    raise SystemExit(main())
