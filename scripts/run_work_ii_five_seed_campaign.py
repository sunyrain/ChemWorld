#!/usr/bin/env python3
"""Run one configured Work II task for one or five world seeds with heartbeats."""

from __future__ import annotations

import argparse
import contextlib
import json
import os
import queue
import subprocess
import sys
import threading
from pathlib import Path
from time import perf_counter
from typing import Any, TextIO
from uuid import uuid4

from chemworld.data.logging import load_jsonl
from chemworld.eval.provenance import (
    file_sha256,
    git_source_commit,
    git_worktree_dirty,
    write_json_atomic,
)
from chemworld.eval.work_ii_ap_d1_development import (
    build_ap_d1_development_cost_budget,
    validate_ap_d1_development_authorization,
)
from chemworld.eval.work_ii_d1_execution import (
    D1_EXECUTION_CONTRACT,
    D1CellStore,
    validate_d1_qualification_evidence,
)
from chemworld.eval.work_ii_development_readiness import (
    validate_development_readiness_receipt,
)
from chemworld.eval.work_ii_execution_mode import validate_release_d1_config

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "configs/benchmark/work_ii_campaign_pilot.json"
RUNNER = ROOT / "scripts/run_work_ii_campaign_pilot.py"


def _emit(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rendered = json.dumps(payload, ensure_ascii=False, sort_keys=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(rendered + "\n")
    output_encoding = sys.stdout.encoding or "utf-8"
    safe_rendered = rendered.encode(output_encoding, errors="backslashreplace").decode(
        output_encoding
    )
    with contextlib.suppress(BrokenPipeError, OSError, ValueError):
        print(safe_rendered, flush=True)


def _drain(
    stream: TextIO,
    events: queue.Queue[tuple[str, str | None]],
    arm: str,
    log_path: Path,
) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("w", encoding="utf-8") as log:
        for line in stream:
            log.write(line)
            log.flush()
            events.put((arm, line.rstrip("\r\n")))
        events.put((arm, None))


def _terminate_processes(processes: dict[str, subprocess.Popen[str]]) -> None:
    """Boundedly terminate and reap every active cell process after parent failure."""

    for process in processes.values():
        if process.poll() is None:
            process.terminate()
    for process in processes.values():
        try:
            process.wait(timeout=10.0)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=10.0)


def _load_terminal_state(store: D1CellStore, key: str) -> str:
    path = store.terminals / f"{key}.json"
    return str(json.loads(path.read_text(encoding="utf-8"))["state"])


def _materialize_unfinalized_terminal(
    attempt_root: Path,
    *,
    arm: str,
    committed_operation_count: int,
    return_code: int,
) -> dict[str, Any]:
    """Create an evaluator-readable retained failure without replacing trajectory bytes."""

    summary = {
        "arm": arm,
        "completed": False,
        "failure": {
            "type": "UnfinalizedChildAfterCommittedOperation",
            "message": "child ended after a committed operation without a terminal summary",
        },
        "analysis": {
            "operation_attempt_count": len(load_jsonl(attempt_root / "trajectory.jsonl")),
            "committed_operation_count": committed_operation_count,
            "complete_experiment_count": 0,
            "right_censored_open_experiment": True,
        },
        "exact_replay": {"verified": False},
        "qualification": {
            "passed": False,
            "failed_checks": ["unfinalized_child_after_committed_operation"],
        },
    }
    write_json_atomic(attempt_root / "summary.json", summary)
    write_json_atomic(
        attempt_root / "report.json",
        {
            "schema_version": "chemworld-work-ii-d1-unfinalized-cell-report-0.1",
            "completed_cell_count": 0,
            "cell_count": 1,
            "return_code": return_code,
            "results": [summary],
        },
    )
    return summary


def _systemic_preoperation_failure(
    *,
    cell_failures: list[dict[str, Any]],
    results: list[dict[str, Any]],
    arms: list[str],
) -> bool:
    """Stop only when the complete triplet failed before any scientific operation."""

    if len(cell_failures) != len(arms):
        return False
    by_arm = {str(row.get("arm")): row for row in results if isinstance(row, dict)}
    return all(
        int(by_arm.get(arm, {}).get("analysis", {}).get("committed_operation_count", 0)) == 0
        for arm in arms
    )


def _heartbeat(
    *,
    started: float,
    completed_cells: int,
    terminal_cells: int,
    total_cells: int,
    last_event: dict[str, Any],
    active_cells: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    elapsed = perf_counter() - started
    rate = completed_cells / elapsed if elapsed > 0.0 else 0.0
    return {
        "event": "heartbeat",
        "elapsed_s": round(elapsed, 1),
        "completed_cells": completed_cells,
        "terminal_cells": terminal_cells,
        "total_cells": total_cells,
        "throughput_cells_per_hour": round(rate * 3600.0, 3),
        "eta_s": (
            round((total_cells - completed_cells) / rate, 1)
            if rate > 0.0 and completed_cells < total_cells
            else 0.0
            if completed_cells == total_cells
            else None
        ),
        "current_world_seed": last_event.get("world_seed", last_event.get("current_world_seed")),
        "current_arm": last_event.get("arm", last_event.get("current_arm")),
        "current_stage": last_event.get("stage", last_event.get("current_stage")),
        "current_step": last_event.get("step", last_event.get("current_step")),
        "current_complete_experiments": last_event.get(
            "complete_experiments", last_event.get("current_complete_experiments")
        ),
        "active_cells": list(active_cells or last_event.get("active_cells", [])),
        "liveness_counter": int(last_event.get("liveness_counter", 0)) + 1,
    }


def _execution_scope(seeds: list[int]) -> str:
    if len(seeds) == 1:
        return "pilot_seed_triplet"
    if len(seeds) == 5 and len(set(seeds)) == 5:
        return "five_seed_task_block"
    if seeds == [1, 2, 3, 4]:
        return "terminal_seed0_preserving_continuation"
    raise ValueError(
        "execution requires one pilot seed, five distinct world seeds, or "
        "exact continuation seeds 1 2 3 4"
    )


def run(args: argparse.Namespace) -> dict[str, Any]:
    seeds = [int(seed) for seed in args.world_seed]
    config_path = args.config.resolve()
    config = json.loads(config_path.read_text(encoding="utf-8"))
    if not isinstance(config, dict):
        raise ValueError("campaign config must contain an object")
    output = args.output.resolve()
    progress = args.progress_file.resolve()
    ap_development = bool(getattr(args, "ap_development_execution", False))
    ap_authorization: dict[str, Any] | None = None
    if ap_development:
        if len(seeds) != 1:
            raise RuntimeError("A-P development D1 executes exactly one seed triplet")
        if seeds != [int(config.get("world_seed", -1))]:
            raise RuntimeError("A-P development D1 seed differs from its config")
        if getattr(args, "release_manifest", None) is not None or getattr(
            args, "readiness_receipt", None
        ) is not None:
            raise RuntimeError("A-P development D1 cannot also use release gates")
        if getattr(args, "ap_development_authorization", None) is None or getattr(
            args, "ap_development_readiness", None
        ) is None:
            raise RuntimeError(
                "A-P development D1 requires explicit authorization and readiness"
            )
        ap_authorization, ap_errors = validate_ap_d1_development_authorization(
            ROOT,
            args.ap_development_authorization.resolve(),
            config_path=config_path,
            output_root=output,
            readiness_path=args.ap_development_readiness.resolve(),
        )
        if ap_errors:
            raise RuntimeError(
                "A-P development D1 authorization failed: " + "; ".join(ap_errors)
            )
        ap_cost_budget = (
            None
            if ap_authorization.get("spending_limit") == "unlimited"
            else build_ap_d1_development_cost_budget(ROOT, ap_authorization)
        )
    else:
        ap_cost_budget = None
        if git_worktree_dirty(ROOT):
            raise RuntimeError("provider execution requires a clean committed worktree")
        if args.readiness_receipt is None:
            raise RuntimeError("provider execution requires a zero-provider readiness receipt")
        if getattr(args, "release_manifest", None) is None:
            raise RuntimeError("provider execution requires a release manifest")
        release_errors = validate_release_d1_config(
            ROOT,
            config,
            args.release_manifest.resolve(),
            require_provider_authorized=True,
        )
        if release_errors:
            raise RuntimeError(
                "provider release D1 validation failed: " + "; ".join(release_errors)
            )
        evidence_errors = validate_d1_qualification_evidence(ROOT, config)
        if evidence_errors:
            raise RuntimeError(
                "provider D1 qualification evidence failed: "
                + "; ".join(evidence_errors)
            )
        readiness_errors = validate_development_readiness_receipt(
            ROOT,
            args.readiness_receipt.resolve(),
            config_path,
            seeds,
            release_manifest=args.release_manifest.resolve(),
        )
        if readiness_errors:
            raise RuntimeError("provider readiness failed: " + "; ".join(readiness_errors))
    resume = bool(getattr(args, "resume", False))
    if output.exists() and not resume:
        raise FileExistsError(f"refusing to overwrite provider output: {output}")
    if not output.exists() and resume:
        raise FileNotFoundError("D1 missing-only resume requires an existing output root")
    if not isinstance(config, dict) or not isinstance(config.get("prior_arms"), dict):
        raise ValueError("campaign config must define prior_arms")
    provider = config.get("provider")
    if not isinstance(provider, dict):
        raise ValueError("campaign config must define provider")
    env_key = provider.get("env_key")
    if env_key is not None and not os.environ.get(str(env_key)):
        raise RuntimeError(f"{env_key} is not available")
    api_key_file = provider.get("api_key_file")
    if api_key_file is not None:
        key_path = Path(str(api_key_file))
        if not key_path.is_absolute():
            key_path = ROOT / key_path
        if not key_path.is_file():
            raise RuntimeError("configured provider API-key file is not available")
    arms = list(config["prior_arms"])
    if len(arms) != 3:
        raise ValueError("provider execution requires exactly three prior arms")
    configured_concurrency = int(config.get("execution", {}).get("max_concurrency", 0))
    if configured_concurrency != 3:
        raise ValueError("campaign config must freeze execution.max_concurrency=3")
    if int(args.max_concurrency) != 3:
        raise ValueError("the frozen execution requires max_concurrency=3")
    # Do not materialize a run root until every pre-provider gate, including
    # credential availability, has passed.  A rejected launch remains a clean
    # retry rather than an empty output that requires manual repair.
    output.mkdir(parents=True, exist_ok=resume)
    execution_scope = _execution_scope(seeds)
    total_cells = len(seeds) * 3
    store = D1CellStore(
        output / "store",
        config_path=config_path,
        task_id=str(config["task_id"]),
        world_seeds=seeds,
        arms=arms,
    )
    pending = store.pending(resume=resume)
    pending_identities = {
        (int(cell["world_seed"]), str(cell["prior_arm"])) for cell in pending
    }
    initial_audit = store.audit()
    terminal_cells = int(initial_audit["terminal_count"])
    completed_cells = sum(
        _load_terminal_state(store, key) == "completed"
        for key in initial_audit["terminal_cell_key_sha256"]
    )
    started = perf_counter()
    seed_reports: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    last_event: dict[str, Any] = {"stage": "matrix_start", "liveness_counter": 0}
    _emit(
        progress,
        {
            "event": "matrix_resumed" if resume else "matrix_started",
            "world_seeds": seeds,
            "completed_cells": 0,
            "terminal_cells": 0,
            "total_cells": total_cells,
            "source_commit": git_source_commit(ROOT),
            "task_id": config.get("task_id"),
            "provider_id": provider.get("id"),
            "model": provider.get("model"),
        },
    )
    for seed in seeds:
        seed_started = perf_counter()
        seed_output = output / f"seed-{seed}"
        seed_output.mkdir(exist_ok=True)
        events: queue.Queue[tuple[str, str | None]] = queue.Queue()
        processes: dict[str, subprocess.Popen[str]] = {}
        readers: dict[str, threading.Thread] = {}
        process_state: dict[str, dict[str, Any]] = {}
        active_arms = {
            arm for arm in arms if (seed, arm) in pending_identities
        }
        try:
            for arm in sorted(active_arms, key=arms.index):
                key = store.key(seed, arm)
                attempt_id = uuid4().hex
                attempt_root = output / "attempts" / key / attempt_id
                log_path = output / "logs" / key / f"{attempt_id}.log"
                attempt_receipt = store.provider_attempts / key / f"{attempt_id}.json"
                cost_ledger = output / "cost_ledgers" / key / f"{attempt_id}.json"
                if ap_development:
                    audit = store.audit()
                    launched = int(audit["provider_attempt_count"]) + 1
                    if ap_cost_budget is None:
                        ledger_payload = {
                            "state": "user_authorized_unlimited_spend_before_provider_launch",
                            "task_id": config["task_id"],
                            "cell_key_sha256": key,
                            "attempt_id": attempt_id,
                            "provider_attempt_count_for_task": launched,
                            "within_authorized_ceiling": True,
                            "currency": "USD",
                            "currency_ceiling_usd": None,
                        }
                    else:
                        task_budget = ap_cost_budget["per_task"][str(config["task_id"])]
                        per_attempt_cost = float(task_budget["per_attempt_cost_cap_usd"])
                        task_reserved = round(launched * per_attempt_cost, 12)
                        task_ceiling = float(task_budget["all_attempts_cost_cap_usd"])
                        if task_reserved > task_ceiling:
                            raise RuntimeError("A-P development task cost reservation exceeded")
                        ledger_payload = {
                            "state": "full_token_cap_reserved_before_provider_launch",
                            "task_id": config["task_id"],
                            "cell_key_sha256": key,
                            "attempt_id": attempt_id,
                            "provider_attempt_count_for_task": launched,
                            "reserved_cost_usd_for_task": task_reserved,
                            "authorized_cost_cap_usd_for_task": task_ceiling,
                            "within_authorized_ceiling": True,
                        }
                    write_json_atomic(
                        cost_ledger,
                        ledger_payload,
                    )
                store.record_provider_attempt_launch(key, attempt_id=attempt_id)
                child_progress = progress.with_name(f"{progress.stem}-seed-{seed}-{arm}.jsonl")
                command = [
                    sys.executable,
                    str(RUNNER),
                    "--config",
                    str(args.config.resolve()),
                    "--output",
                    str(attempt_root),
                    "--progress-file",
                    str(child_progress),
                    "--world-seed",
                    str(seed),
                    "--prior-arm",
                    arm,
                ]
                if ap_development:
                    command.extend(
                        [
                            "--ap-development-execution",
                            "--ap-development-authorization",
                            str(args.ap_development_authorization.resolve()),
                            "--ap-development-readiness",
                            str(args.ap_development_readiness.resolve()),
                            "--ap-development-authorized-output-root",
                            str(output),
                            "--ap-development-attempt-receipt",
                            str(attempt_receipt),
                            "--ap-development-cost-ledger",
                            str(cost_ledger),
                        ]
                    )
                else:
                    command.extend(
                        [
                            "--release-manifest",
                            str(args.release_manifest.resolve()),
                        ]
                    )
                kwargs: dict[str, Any] = {}
                if os.name == "nt":
                    kwargs["creationflags"] = getattr(subprocess, "CREATE_NO_WINDOW", 0)
                try:
                    process = subprocess.Popen(
                        command,
                        cwd=ROOT,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        text=True,
                        encoding="utf-8",
                        errors="replace",
                        **kwargs,
                    )
                except OSError as error:
                    log_path.parent.mkdir(parents=True, exist_ok=True)
                    log_path.write_text(
                        f"provider process launch failed: {type(error).__name__}: {error}\n",
                        encoding="utf-8",
                    )
                    store.record_infrastructure_failure(
                        key,
                        attempt_id=attempt_id,
                        error_type=type(error).__name__,
                        error_message=str(error),
                        reason_code="provider_process_launch_failed",
                        committed_operation_count=0,
                        log_path=log_path,
                    )
                    active_arms.discard(arm)
                    continue
                if process.stdout is None:
                    process.kill()
                    raise RuntimeError("five-seed cell stdout was not created")
                processes[arm] = process
                process_state[arm] = {
                    "key": key,
                    "attempt_id": attempt_id,
                    "attempt_root": attempt_root,
                    "log_path": log_path,
                }
                reader = threading.Thread(
                    target=_drain,
                    args=(process.stdout, events, arm, log_path),
                    daemon=True,
                )
                readers[arm] = reader
                reader.start()
            _emit(
                progress,
                {
                    "event": "seed_triplet_started",
                    "world_seed": seed,
                    "arms": arms,
                    "max_concurrency": 3,
                    "active_cells": [
                        {"world_seed": seed, "arm": arm, "stage": "process_started"} for arm in arms
                    ],
                    "completed_cells": completed_cells,
                    "total_cells": total_cells,
                },
            )
            while active_arms:
                try:
                    arm, line = events.get(timeout=float(args.heartbeat_interval_s))
                except queue.Empty:
                    last_event = _heartbeat(
                        started=started,
                        completed_cells=completed_cells,
                        terminal_cells=terminal_cells,
                        total_cells=total_cells,
                        last_event=last_event,
                        active_cells=[
                            {"world_seed": seed, "arm": arm, "stage": "provider_session"}
                            for arm in sorted(active_arms)
                        ],
                    )
                    _emit(progress, last_event)
                    continue
                if line is None:
                    active_arms.discard(arm)
                    continue
                try:
                    child_event = json.loads(line)
                except json.JSONDecodeError:
                    _emit(
                        progress,
                        {
                            "event": "child_log",
                            "world_seed": seed,
                            "arm": arm,
                            "message": line[:1000],
                        },
                    )
                    continue
                if not isinstance(child_event, dict):
                    continue
                child_event["event"] = child_event.get("event", "child_progress")
                child_event.setdefault("arm", arm)
                child_event["matrix_completed_cells_before_event"] = completed_cells
                if child_event.get("stage") == "cell_completed" and child_event.get("completed"):
                    completed_cells += 1
                if child_event.get("stage") == "cell_completed":
                    terminal_cells += 1
                child_event["completed_cells"] = completed_cells
                child_event["terminal_cells"] = terminal_cells
                child_event["total_cells"] = total_cells
                child_event["active_cells"] = [
                    {"world_seed": seed, "arm": active, "stage": "provider_session"}
                    for active in sorted(active_arms)
                ]
                child_event["liveness_counter"] = int(last_event.get("liveness_counter", 0)) + 1
                last_event = child_event
                _emit(progress, child_event)
        except BaseException:
            _terminate_processes(processes)
            for reader in readers.values():
                reader.join(timeout=5.0)
            raise
        return_codes = {arm: process.wait() for arm, process in processes.items()}
        for reader in readers.values():
            reader.join(timeout=5.0)
        for arm, state in process_state.items():
            attempt_root = state["attempt_root"]
            summary_path = attempt_root / "summary.json"
            row: dict[str, Any] | None = None
            summary_error: Exception | None = None
            if summary_path.is_file():
                try:
                    candidate = json.loads(summary_path.read_text(encoding="utf-8"))
                    if not isinstance(candidate, dict) or candidate.get("arm") != arm:
                        raise ValueError("summary is not bound to its scheduled arm")
                    row = candidate
                except (OSError, TypeError, ValueError, json.JSONDecodeError) as error:
                    summary_error = error
            if row is not None:
                committed = int(
                    row.get("analysis", {}).get("committed_operation_count", 0)
                )
                state_name = (
                    "completed"
                    if row.get("completed") is True
                    else "right_censored"
                    if committed > 0
                    else "failed"
                )
                store.write_terminal(
                    state["key"],
                    attempt_id=state["attempt_id"],
                    state=state_name,
                    result_root=attempt_root,
                    committed_operation_count=committed,
                )
            else:
                trajectory_path = attempt_root / "trajectory.jsonl"
                records = load_jsonl(trajectory_path) if trajectory_path.is_file() else []
                committed = sum(
                    row.get("transaction_status") == "committed" for row in records
                )
                if committed:
                    _materialize_unfinalized_terminal(
                        attempt_root,
                        arm=arm,
                        committed_operation_count=committed,
                        return_code=return_codes[arm],
                    )
                    store.write_terminal(
                        state["key"],
                        attempt_id=state["attempt_id"],
                        state="right_censored",
                        result_root=attempt_root,
                        committed_operation_count=committed,
                    )
                else:
                    store.record_infrastructure_failure(
                        state["key"],
                        attempt_id=state["attempt_id"],
                        error_type="MissingTerminalSummary",
                        error_message=str(summary_error or "child ended without terminal summary"),
                        reason_code=(
                            "unreadable_terminal_summary_zero_committed_operations"
                            if summary_path.is_file()
                            else "missing_terminal_summary_zero_committed_operations"
                        ),
                        committed_operation_count=0,
                        log_path=state["log_path"],
                    )
        current_audit = store.audit()
        terminal_cells = int(current_audit["terminal_count"])
        completed_cells = sum(
            _load_terminal_state(store, key) == "completed"
            for key in current_audit["terminal_cell_key_sha256"]
        )
        results: list[dict[str, Any]] = []
        cell_failures: list[dict[str, Any]] = []
        for arm in arms:
            summary_path = seed_output / arm / "summary.json"
            row = (
                json.loads(summary_path.read_text(encoding="utf-8"))
                if summary_path.exists()
                else None
            )
            if isinstance(row, dict):
                results.append(row)
            if (
                return_codes.get(arm, 0) != 0
                or not isinstance(row, dict)
                or row.get("completed") is not True
            ):
                cell_failures.append(
                    {
                        "world_seed": seed,
                        "arm": arm,
                        "return_code": return_codes.get(arm),
                        "summary_available": isinstance(row, dict),
                        "qualification_failed_checks": (
                            row.get("qualification", {}).get("failed_checks", [])
                            if isinstance(row, dict)
                            else []
                        ),
                    }
                )
        seed_report = {
            "schema_version": "chemworld-work-ii-campaign-pilot-report-0.2",
            "pilot_id": config.get("pilot_id"),
            "cell_id": f"{config.get('pilot_id')}--seed{seed}",
            "formal_result": False,
            "world_seed": seed,
            "cell_count": len(arms),
            "completed_cell_count": sum(row.get("completed") is True for row in results),
            "terminal_cell_count": len(results),
            "elapsed_s": round(perf_counter() - seed_started, 1),
            "max_concurrency": 3,
            "parallelization_unit": "same_seed_prior_arm_triplet",
            "results": results,
            "failures": cell_failures,
        }
        write_json_atomic(seed_output / "report.json", seed_report)
        seed_reports.append(seed_report)
        if cell_failures:
            failures.extend(cell_failures)
            if _systemic_preoperation_failure(
                cell_failures=cell_failures,
                results=results,
                arms=arms,
            ):
                break
    final_audit = store.audit()
    terminal_record_count = int(final_audit["terminal_count"])
    terminal_receipt_bindings = []
    for key in final_audit["terminal_cell_key_sha256"]:
        path = store.terminals / f"{key}.json"
        receipt = json.loads(path.read_text(encoding="utf-8"))
        terminal_receipt_bindings.append(
            {
                "path": path.relative_to(output).as_posix(),
                "sha256": file_sha256(path),
                "receipt_sha256": receipt["receipt_sha256"],
            }
        )
    report = {
        "schema_version": "chemworld-work-ii-five-seed-campaign-report-0.1",
        "source_commit": git_source_commit(ROOT),
        "execution_context": (
            None if ap_development else dict(config["execution_context"])
        ),
        "legacy_source_evidence": (
            None if ap_development else config.get("legacy_source_evidence")
        ),
        "provider_execution_authorized": True,
        "development_only": ap_development,
        "formal_result": False,
        "formal_r5_authorized": False,
        "ap_development_authorization": (
            {
                "approved_at": ap_authorization.get("approved_at"),
                "authorized_by": "user",
                "currency": ap_authorization.get("currency"),
                "currency_ceiling_usd": ap_authorization.get("currency_ceiling_usd"),
            }
            if ap_authorization is not None
            else None
        ),
        "task_id": config.get("task_id"),
        "provider_id": provider.get("id"),
        "model": provider.get("model"),
        "world_seeds": seeds,
        "execution_scope": execution_scope,
        "expected_cell_count": total_cells,
        "terminal_cell_count": terminal_record_count,
        "completed_cell_count": completed_cells,
        "completed_seed_count": len(seed_reports),
        "max_concurrency": 3,
        "parallelization_unit": "same_seed_prior_arm_triplet",
        "elapsed_s": round(perf_counter() - started, 1),
        "all_cells_completed": completed_cells == total_cells and not failures,
        "all_cells_terminal": terminal_record_count == total_cells,
        "systemic_preoperation_stop_triggered": (
            terminal_record_count < total_cells and bool(failures)
        ),
        "d1_execution_contract": dict(D1_EXECUTION_CONTRACT),
        "terminal_receipt_bindings": terminal_receipt_bindings,
        "store_audit": final_audit,
        "failures": failures,
        "seed_reports": seed_reports,
    }
    write_json_atomic(output / "matrix_report.json", report)
    _emit(
        progress,
        {
            "event": (
                "matrix_completed"
                if report["all_cells_completed"]
                else "matrix_terminal_with_failures"
                if report["all_cells_terminal"]
                else "matrix_failed"
            ),
            "completed_cells": completed_cells,
            "terminal_cells": terminal_record_count,
            "total_cells": total_cells,
            "elapsed_s": report["elapsed_s"],
            "output": str(output),
            "failures": failures,
        },
    )
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--progress-file", type=Path, required=True)
    parser.add_argument(
        "--world-seed",
        type=int,
        nargs="+",
        default=[0, 1, 2, 3, 4],
    )
    parser.add_argument("--heartbeat-interval-s", type=float, default=30.0)
    parser.add_argument("--max-concurrency", type=int, default=3)
    parser.add_argument("--readiness-receipt", type=Path)
    parser.add_argument("--release-manifest", type=Path)
    parser.add_argument("--ap-development-execution", action="store_true")
    parser.add_argument("--ap-development-authorization", type=Path)
    parser.add_argument("--ap-development-readiness", type=Path)
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    report = run(args)
    return 0 if report["all_cells_terminal"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
