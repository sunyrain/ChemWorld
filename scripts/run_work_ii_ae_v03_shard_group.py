#!/usr/bin/env python3
"""Manage one four-worker external shard group and its deterministic merge."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from collections.abc import Sequence
from contextlib import suppress
from pathlib import Path
from typing import Any

from chemworld.eval.provenance import write_json_atomic
from chemworld.eval.work_ii_ae_prior_qualification_v03 import (
    AEPriorQualificationV03Error,
)

ROOT = Path(__file__).resolve().parents[1]
SHARD_RUNNER = ROOT / "scripts/run_work_ii_ae_v03_shards.py"
DEFAULT_CONTRACT = (
    ROOT / "configs/benchmark/work_ii_ae_prior_distinguishability_v0.3_candidate.json"
)
GROUP_VERSION = "chemworld-work-ii-ae-v03-shard-group-0.1"
UPSTREAM_OPTIONS = (
    ("fit_report", "--fit-report"),
    ("fit_plan", "--fit-plan"),
    ("fit_receipts", "--fit-receipts"),
    ("validation_report", "--validation-report"),
    ("validation_plan", "--validation-plan"),
    ("validation_receipts", "--validation-receipts"),
    ("screen_report", "--screen-report"),
    ("screen_plan", "--screen-plan"),
    ("screen_receipts", "--screen-receipts"),
    ("selection", "--selection"),
)


def _load_object(path: Path, label: str) -> dict[str, Any]:
    value = json.loads(path.resolve().read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise AEPriorQualificationV03Error(f"{label} must contain one object")
    return value


def _external_path(path: Path, *, role: str) -> Path:
    resolved = path.resolve()
    if resolved == ROOT or resolved.is_relative_to(ROOT):
        raise AEPriorQualificationV03Error(
            f"{role} must be outside the code worktree: {resolved}"
        )
    return resolved


def _expected_receipts(args: argparse.Namespace) -> int:
    contract = _load_object(args.contract, "A-E v0.3 contract")
    if args.phase == "confirmation":
        if args.selection is None:
            raise AEPriorQualificationV03Error("confirmation requires --selection")
        selection = _load_object(args.selection, "screen selection")
        selected = selection.get("selected_locus_ids")
        if not isinstance(selected, dict):
            raise AEPriorQualificationV03Error(
                "screen selection lacks selected_locus_ids"
            )
        locus_count = len(selected)
    else:
        tasks = contract.get("tasks")
        if not isinstance(tasks, list):
            raise AEPriorQualificationV03Error("contract tasks are malformed")
        locus_count = sum(
            len(task.get("loci", [])) for task in tasks if isinstance(task, dict)
        )
    cohorts = contract.get("cohorts")
    cohort = cohorts.get(args.phase) if isinstance(cohorts, dict) else None
    if not isinstance(cohort, dict):
        raise AEPriorQualificationV03Error(f"contract lacks {args.phase} cohort")
    worlds = cohort.get("worlds_per_locus")
    if isinstance(worlds, bool) or not isinstance(worlds, int) or worlds < 0:
        raise AEPriorQualificationV03Error("cohort worlds_per_locus is malformed")
    total = locus_count * worlds * 24
    if args.import_prefix_count > total:
        raise AEPriorQualificationV03Error(
            "imported prefix count exceeds the phase denominator"
        )
    return total - args.import_prefix_count


def _upstream_arguments(args: argparse.Namespace) -> list[str]:
    arguments: list[str] = []
    for attribute, option in UPSTREAM_OPTIONS:
        value = getattr(args, attribute, None)
        if value is not None:
            arguments.extend([option, str(Path(value).resolve())])
    return arguments


def build_group_commands(
    args: argparse.Namespace,
) -> tuple[list[tuple[str, ...]], tuple[str, ...]]:
    """Build four execution commands and the one post-success merge command."""

    common = [
        sys.executable,
        str(SHARD_RUNNER),
        "--contract",
        str(args.contract.resolve()),
        "--phase",
        args.phase,
        "--shard-root",
        str(args.shard_root.resolve()),
        "--shard-count",
        str(args.shard_count),
        "--import-prefix-count",
        str(args.import_prefix_count),
        *_upstream_arguments(args),
    ]
    if args.import_prefix is not None:
        common.extend(["--import-prefix", str(args.import_prefix.resolve())])
    workers = [
        (*common, "--execute-shard", "--shard-index", str(index))
        for index in range(args.shard_count)
    ]
    merge = (*common, "--merge", "--output", str(args.output.resolve()))
    return workers, merge


def _write_once(path: Path, payload: dict[str, Any]) -> None:
    if path.exists():
        return
    write_json_atomic(path, payload)


def _emit(event: dict[str, Any]) -> None:
    print(
        json.dumps({"unix_time": time.time(), **event}, ensure_ascii=False, sort_keys=True),
        flush=True,
    )


def _receipt_count(shard_root: Path) -> int:
    return sum(
        1
        for shard in shard_root.glob("shard-*")
        if shard.is_dir()
        for path in (shard / "receipts").glob("*.json")
        if path.is_file()
    )


def _emit_progress(
    *,
    args: argparse.Namespace,
    started: float,
    total: int,
    processes: Sequence[subprocess.Popen[str]],
    stage: str,
) -> None:
    completed = _receipt_count(args.shard_root)
    elapsed = max(0.0, time.monotonic() - started)
    throughput = 60.0 * completed / elapsed if elapsed > 0 else 0.0
    remaining = max(0, total - completed)
    eta = 60.0 * remaining / throughput if throughput > 0 else None
    return_codes = [process.poll() for process in processes]
    _emit(
        {
            "event": "shard_group_progress",
            "stage": stage,
            "phase": args.phase,
            "completed": completed,
            "total": total,
            "throughput_receipts_per_min": round(throughput, 3),
            "eta_s": round(eta, 1) if eta is not None else None,
            "elapsed_s": round(elapsed, 1),
            "active_workers": sum(code is None for code in return_codes),
            "finished_workers": sum(code is not None for code in return_codes),
        }
    )


def _monitor(
    args: argparse.Namespace,
    processes: Sequence[subprocess.Popen[str]],
    *,
    started: float,
    total: int,
    stage: str,
    progress_interval: float,
) -> list[int]:
    next_progress = 0.0
    while True:
        now = time.monotonic()
        if now >= next_progress:
            _emit_progress(
                args=args,
                started=started,
                total=total,
                processes=processes,
                stage=stage,
            )
            next_progress = now + progress_interval
        return_codes = [process.poll() for process in processes]
        if any(code not in (None, 0) for code in return_codes):
            return [int(code) if code is not None else -1 for code in return_codes]
        if all(code == 0 for code in return_codes):
            return [0 for _process in processes]
        time.sleep(min(1.0, progress_interval))


def _terminate_running(processes: Sequence[subprocess.Popen[str]]) -> None:
    for process in processes:
        if process.poll() is not None:
            continue
        with suppress(OSError):
            process.terminate()
    for process in processes:
        if process.poll() is not None:
            continue
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=5)


def _spawn(command: tuple[str, ...], log: Path) -> subprocess.Popen[str]:
    log.parent.mkdir(parents=True, exist_ok=True)
    with log.open("a", encoding="utf-8", newline="\n") as handle:
        return subprocess.Popen(
            command,
            cwd=ROOT,
            stdout=handle,
            stderr=subprocess.STDOUT,
            text=True,
        )


def _failure(
    args: argparse.Namespace,
    *,
    stage: str,
    message: str,
    return_codes: Sequence[int] = (),
) -> None:
    payload = {
        "schema_version": GROUP_VERSION,
        "status": "failed",
        "phase": args.phase,
        "stage": stage,
        "message": message,
        "worker_return_codes": list(return_codes),
        "restart_required_from_execution_zero": True,
    }
    _write_once(args.shard_root / "group-failure.json", payload)
    _emit({"event": "shard_group_failed", **payload})


def run_group(args: argparse.Namespace) -> int:
    args.contract = args.contract.resolve()
    args.shard_root = _external_path(args.shard_root, role="shard root")
    args.output = _external_path(args.output, role="merged output")
    if args.shard_count != 4:
        raise AEPriorQualificationV03Error("the A-E v0.3 shard group requires 4 workers")
    if (
        args.output == args.shard_root
        or args.output.is_relative_to(args.shard_root)
        or args.shard_root.is_relative_to(args.output)
    ):
        raise AEPriorQualificationV03Error(
            "merged output and shard root must be disjoint"
        )
    if args.output.exists():
        raise AEPriorQualificationV03Error("merged output must not already exist")
    args.shard_root.parent.mkdir(parents=True, exist_ok=True)
    args.shard_root.mkdir()
    processes: list[subprocess.Popen[str]] = []
    stage = "execute"
    try:
        total = _expected_receipts(args)
        workers, merge = build_group_commands(args)
        write_json_atomic(
            args.shard_root / "group-manifest.json",
            {
                "schema_version": GROUP_VERSION,
                "status": "running",
                "phase": args.phase,
                "worker_count": args.shard_count,
                "expected_receipts": total,
                "imported_prefix_count": args.import_prefix_count,
                "merged_output": str(args.output),
                "orchestrator_pid": os.getpid(),
            },
        )
        started = time.monotonic()
        for index, command in enumerate(workers):
            processes.append(
                _spawn(command, args.shard_root / "logs" / f"worker-{index}.log")
            )
        _emit(
            {
                "event": "shard_group_started",
                "phase": args.phase,
                "worker_pids": [process.pid for process in processes],
                "total": total,
            }
        )
        return_codes = _monitor(
            args,
            processes,
            started=started,
            total=total,
            stage=stage,
            progress_interval=args.progress_interval,
        )
        if any(code != 0 for code in return_codes):
            _terminate_running(processes)
            _failure(
                args,
                stage=stage,
                message="at least one execute-shard process exited nonzero",
                return_codes=return_codes,
            )
            return next((code for code in return_codes if code > 0), 1)

        stage = "merge"
        merge_process = _spawn(merge, args.shard_root / "logs" / "merge.log")
        processes.append(merge_process)
        merge_codes = _monitor(
            args,
            [merge_process],
            started=started,
            total=total,
            stage=stage,
            progress_interval=args.progress_interval,
        )
        if merge_codes != [0]:
            _failure(
                args,
                stage=stage,
                message="deterministic merge exited nonzero",
                return_codes=merge_codes,
            )
            return merge_codes[0] if merge_codes[0] > 0 else 1
        required = [args.output / "report.json"]
        if args.phase == "prospective_screen":
            required.append(args.output / "selection.json")
        elif args.phase == "confirmation":
            required.append(args.output / "summary.json")
        if any(not path.is_file() for path in required):
            _failure(
                args,
                stage=stage,
                message="merge exited zero without the complete standard output",
            )
            return 1
        completion = {
            "schema_version": GROUP_VERSION,
            "status": "completed",
            "phase": args.phase,
            "worker_return_codes": return_codes,
            "merge_return_code": 0,
            "completed_receipts": _receipt_count(args.shard_root),
            "expected_receipts": total,
            "merged_output": str(args.output),
        }
        write_json_atomic(args.shard_root / "group-completed.json", completion)
        _emit({"event": "shard_group_completed", **completion})
        return 0
    except BaseException as error:
        _terminate_running(processes)
        _failure(args, stage=stage, message=f"{type(error).__name__}: {error}")
        raise


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", type=Path, default=DEFAULT_CONTRACT)
    parser.add_argument(
        "--phase",
        choices=(
            "classifier_fit",
            "classifier_validation",
            "prospective_screen",
            "confirmation",
        ),
        required=True,
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--shard-root", type=Path, required=True)
    parser.add_argument("--shard-count", type=int, default=4)
    parser.add_argument("--import-prefix", type=Path)
    parser.add_argument("--import-prefix-count", type=int, default=0)
    parser.add_argument("--progress-interval", type=float, default=60.0)
    parser.add_argument("--fit-report", type=Path)
    parser.add_argument("--fit-plan", type=Path)
    parser.add_argument("--fit-receipts", type=Path)
    parser.add_argument("--validation-report", type=Path)
    parser.add_argument("--validation-plan", type=Path)
    parser.add_argument("--validation-receipts", type=Path)
    parser.add_argument("--screen-report", type=Path)
    parser.add_argument("--screen-plan", type=Path)
    parser.add_argument("--screen-receipts", type=Path)
    parser.add_argument("--selection", type=Path)
    return parser


def main() -> int:
    args = _parser().parse_args()
    if args.progress_interval <= 0:
        raise AEPriorQualificationV03Error("--progress-interval must be positive")
    if (args.import_prefix is None) != (args.import_prefix_count == 0):
        raise AEPriorQualificationV03Error(
            "--import-prefix and a positive --import-prefix-count are required together"
        )
    return run_group(args)


if __name__ == "__main__":
    raise SystemExit(main())
