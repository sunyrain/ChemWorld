#!/usr/bin/env python3
"""Repair and resume the frozen RX P/S five-world dual-goal block without overwrites."""
# ruff: noqa: E501

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import threading
import time
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import scripts.run_work_ii_final_diagnostic as diagnostic  # noqa: E402
import scripts.run_work_ii_rx_ps_five_world_dual_goal as campaign  # noqa: E402

RECOVERY_VERSION = "recovery-v3"
NUMERICS_LIMIT = 256
POSTTEST_TOOL_ATTEMPT_LIMIT = 256
POSTTEST_REPAIRS = {
    "RX-W01--S--mechanism_discovery--Opaque": ("Q", "K2"),
    "RX-W01--S--safety_constrained_optimization--MisIndexed": ("Q", "K2"),
    "RX-W02--P--mechanism_discovery--MisIndexed": ("K1", "Q", "K2"),
}
SOURCE_RERUN_CELL = "RX-W02--P--safety_constrained_optimization--Opaque"
_BASE_BUILD_COMMAND = campaign.rx_canary.build_command


def read(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def high_budget_build_command(provider: Any, schema_path: Path, workspace: Path, **kwargs: Any) -> list[str]:
    command = _BASE_BUILD_COMMAND(provider, schema_path, workspace, **kwargs)
    prefix = "mcp_servers.public_numerics.args="
    for index, argument in enumerate(command):
        if not argument.startswith(prefix):
            continue
        values = json.loads(argument.removeprefix(prefix))
        limit_index = values.index("--limit")
        values[limit_index + 1] = str(NUMERICS_LIMIT)
        command[index] = prefix + json.dumps(values)
    return command


def configure_recovery_helpers() -> None:
    campaign.configure_shared_helpers()
    campaign.rx_canary.build_command = high_budget_build_command
    campaign.shared.build_command = high_budget_build_command
    campaign.shared.launch = recovery_launch


def recovery_launch(
    command: list[str],
    message: str,
    workspace: Path,
    environment: dict[str, str],
    output: Path,
    timeout: float,
    enabled: bool,
    audit: Path,
    progress: dict[str, Any],
) -> dict[str, Any]:
    """Launch one posttest with the recovery-specific, recorded tool allowance."""
    output.mkdir(parents=True, exist_ok=False)
    (output / "prompt.txt").write_text(message, encoding="utf-8")
    started = time.monotonic()
    state = diagnostic._EventState()
    forbidden = threading.Event()
    provider_failure_kinds: set[str] = set()
    options = (
        {"creationflags": subprocess.CREATE_NO_WINDOW}
        if os.name == "nt"
        else {"start_new_session": True}
    )
    process = subprocess.Popen(
        command,
        cwd=workspace,
        env=environment,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        errors="replace",
        text=True,
        **options,
    )

    def consume_stdout() -> None:
        assert process.stdout is not None
        with (output / "stdout.jsonl").open("w", encoding="utf-8") as handle:
            for line in process.stdout:
                handle.write(line)
                handle.flush()
                state.consume_stdout([line])
                try:
                    event = json.loads(line)
                    if event.get("type") in {"error", "turn.failed"}:
                        error = event.get("message") or event.get("error", {}).get("message", "")
                        for term in ("max_output_tokens", "context_length", "Reconnecting"):
                            if term in str(error):
                                provider_failure_kinds.add(term)
                    if event.get("type") in {"item.started", "item.completed"} and not diagnostic.tool_allowed(
                        event.get("item", {}), enabled
                    ):
                        forbidden.set()
                except (ValueError, AttributeError):
                    pass

    def consume_stderr() -> None:
        assert process.stderr is not None
        with (output / "stderr.txt").open("w", encoding="utf-8") as handle:
            for line in process.stderr:
                handle.write(line)
                handle.flush()

    threads = [threading.Thread(target=target, daemon=True) for target in (consume_stdout, consume_stderr)]
    for thread in threads:
        thread.start()
    failure = None
    try:
        assert process.stdin is not None
        process.stdin.write(message)
        process.stdin.close()
        last = started
        while process.poll() is None:
            elapsed = time.monotonic() - started
            attempts = len(audit.read_text(encoding="utf-8").splitlines()) if audit.exists() else 0
            if forbidden.is_set():
                failure = "forbidden_tool"
            elif attempts > POSTTEST_TOOL_ATTEMPT_LIMIT:
                failure = "tool_budget_exceeded"
            elif elapsed >= timeout:
                failure = "turn_timeout"
            if failure:
                diagnostic.stop_process(process)
                break
            if time.monotonic() - last >= 30:
                snapshot = state.snapshot()
                print(
                    json.dumps(
                        {
                            **progress,
                            "turn_elapsed_s": round(elapsed),
                            "events": sum(snapshot["event_counts"].values()),
                            "tool_attempts": attempts,
                        }
                    ),
                    flush=True,
                )
                last = time.monotonic()
            time.sleep(0.2)
    except (KeyboardInterrupt, SystemExit):
        failure = "platform_interrupted"
    finally:
        if process.poll() is None:
            diagnostic.stop_process(process)
        for thread in threads:
            thread.join(timeout=15)
    receipt = state.snapshot()
    receipt["provider_failure_kinds"] = sorted(provider_failure_kinds)
    receipt["payload"] = diagnostic._parse_payload(receipt.pop("final_message"))
    if forbidden.is_set():
        failure = "forbidden_tool"
    receipt.update(
        exit_code=process.returncode,
        elapsed_s=time.monotonic() - started,
        failure=failure,
        stderr_byte_count=(output / "stderr.txt").stat().st_size,
        stderr_sha256=diagnostic.digest(output / "stderr.txt"),
    )
    if not failure and (process.returncode or receipt["provider_errors"]):
        receipt["failure"] = "provider_failure"
    write(output / "receipt.json", receipt)
    return receipt


def copy_sqlite_database(source: Path, destination: Path) -> None:
    with sqlite3.connect(source) as source_db, sqlite3.connect(destination) as target_db:
        source_db.backup(target_db)


def restore_session_index(agent: Any, source_sessions: Path, thread_id: str) -> None:
    target_home = agent.home_root / "codex-home"
    target_sessions = target_home / "sessions"
    if target_sessions.exists():
        shutil.rmtree(target_sessions)
    shutil.copytree(source_sessions, target_sessions)
    source_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
    copy_sqlite_database(source_home / "state_5.sqlite", target_home / "state_5.sqlite")
    history_db = source_home / "thread_history_1.sqlite"
    if history_db.exists():
        copy_sqlite_database(history_db, target_home / "thread_history_1.sqlite")
    rollouts = list(target_sessions.rglob(f"*{thread_id}.jsonl"))
    if len(rollouts) != 1:
        raise RuntimeError(f"expected one archived rollout for {thread_id}, found {len(rollouts)}")
    rollout = rollouts[0].resolve()
    first = json.loads(rollout.read_text(encoding="utf-8").splitlines()[0])
    meta = first["payload"]
    now_ms = int(time.time() * 1000)
    with sqlite3.connect(target_home / "state_5.sqlite") as database:
        database.execute(
            """
            INSERT OR REPLACE INTO threads (
                id, rollout_path, created_at, updated_at, source, model_provider, cwd,
                title, sandbox_policy, approval_mode, tokens_used, has_user_event,
                archived, cli_version, first_user_message, memory_mode, model,
                reasoning_effort, created_at_ms, updated_at_ms, thread_source, preview,
                recency_at, recency_at_ms, history_mode, originator
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                thread_id,
                str(rollout),
                now_ms // 1000,
                now_ms // 1000,
                str(meta.get("source", "exec")),
                str(meta.get("model_provider", campaign.PROVIDER["id"])),
                str(agent.workspace.agent_directory),
                f"RX P/S recovery {thread_id}",
                json.dumps({"type": "workspaceWrite"}),
                "never",
                0,
                1,
                0,
                str(meta.get("cli_version", "")),
                "RX P/S sealed posttest recovery",
                "enabled",
                campaign.PROVIDER["model"],
                campaign.PROVIDER["reasoning_effort"],
                now_ms,
                now_ms,
                str(meta.get("thread_source", "user")),
                "RX P/S sealed posttest recovery",
                now_ms // 1000,
                now_ms,
                str(meta.get("history_mode", "paginated")),
                str(meta.get("originator", "codex_exec")),
            ),
        )


def merge_posttest_repair(
    original: Mapping[str, Any],
    repaired: Mapping[str, Mapping[str, Any]],
    query_rows: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    effective = copy.deepcopy(dict(original))
    effective.setdefault("posttests", {})
    effective.setdefault("posttest_validation", {})
    for stage, turn in repaired.items():
        effective["posttests"][stage] = copy.deepcopy(dict(turn))
        effective["posttest_validation"][stage] = campaign.validate_posttest_payload(
            stage, turn.get("payload"), query_rows
        )
    stages = ("K1", "Q", "K2")
    effective["posttest_chain_sealed"] = all(
        effective["posttests"].get(stage, {}).get("payload")
        and effective["posttest_validation"].get(stage, {}).get("valid") is True
        for stage in stages
    )
    effective["status"] = (
        "completed"
        if effective.get("source_status") == "completed"
        and effective["posttest_chain_sealed"]
        and not effective.get("failure")
        else "retained_nonconforming"
    )
    return effective


def _repair_agent(original_folder: Path, original: Mapping[str, Any], repair: Path) -> Any:
    prior = read(original_folder / "public-prior-binding.json").get("initial_world_model")
    temporary = tempfile.TemporaryDirectory(prefix="chemworld-rx-ps-posttest-recovery-")
    agent = campaign.rx_canary.RxFreeResearchAgent(
        goal=original["goal"],
        home_root=Path(temporary.name),
        output=repair,
        workspace=Path(temporary.name) / "laboratory",
        initial_world_model=prior,
        request_timeout_s=1200,
        finalization_timeout_s=300,
        session_wall_time_limit_s=5400,
        max_recovered_mcp_tool_failures=12,
        max_consecutive_mcp_tool_failures=6,
        max_provider_error_events=0,
        pre_action_restart_limit=0,
        accepted_turn_continuation_limit=0,
        provider_process_attempt_limit=1,
        max_initial_prompt_bytes=262144,
        max_tool_output_bytes=131072,
        history_event_limit=360,
        history_byte_limit=524288,
    )
    agent._recovery_temporary_directory = temporary
    agent.followup_environment = campaign.shared._prepare_codex_home(
        agent.home_root, campaign.PROVIDER
    )
    agent._session_process_environment = agent.followup_environment
    return agent


def repair_posttests(
    root: Path,
    cell: Mapping[str, Any],
    config: Mapping[str, Any],
    progress: dict[str, Any],
) -> dict[str, Any]:
    original_folder = root / "sources" / cell["cell_id"]
    original_path = original_folder / "result.json"
    original = read(original_path)
    repair = original_folder / "posttest-repair-v3"
    effective_path = repair / "effective-result.json"
    if effective_path.exists():
        return read(effective_path)
    if repair.exists():
        raise RuntimeError(f"incomplete write-once posttest repair requires inspection: {cell['cell_id']}")
    repair.mkdir(parents=True)
    stages = POSTTEST_REPAIRS[cell["cell_id"]]
    receipts = read(original_folder / "source-receipts.json")
    thread_id = receipts[-1].get("thread_id") if receipts else None
    if not thread_id:
        raise RuntimeError(f"{cell['cell_id']} has no resumable source thread")
    manifest = {
        "schema_version": "work-ii-rx-ps-posttest-repair-1.0",
        "cell_id": cell["cell_id"],
        "started_epoch": time.time(),
        "original_result_sha256": file_sha256(original_path),
        "source_experiments_rerun": False,
        "truth_revealed_to_agent": False,
        "question_changed": False,
        "model_changed": False,
        "thread_reused": True,
        "repair_stages": list(stages),
        "public_numerics_limit_original": 128,
        "public_numerics_limit_recovery": NUMERICS_LIMIT,
    }
    write(repair / "manifest.json", manifest)
    query_rows = campaign.queries(config, cell["locus"])
    repaired: dict[str, dict[str, Any]] = {}
    agent = _repair_agent(original_folder, original, repair)
    try:
        restore_session_index(agent, original_folder / "provider-rollouts", thread_id)
        for stage in stages:
            progress.update(stage=cell["cell_id"], phase=f"{stage}-repair", repair=True)
            turn = campaign.run_posttest(agent, repair, stage, thread_id, progress, query_rows)
            repaired[stage] = turn
            validation = campaign.validate_posttest_payload(stage, turn.get("payload"), query_rows)
            write(repair / f"{stage}-validation.json", validation)
            if validation.get("valid") is not True:
                break
            thread_id = turn.get("thread_id") or thread_id
    finally:
        agent.close()
        sessions = agent.home_root / "codex-home" / "sessions"
        if sessions.exists():
            shutil.copytree(sessions, repair / "provider-rollouts")
        agent._recovery_temporary_directory.cleanup()
    effective = merge_posttest_repair(original, repaired, query_rows)
    effective["recovery"] = manifest
    write(repair / "turns.json", repaired)
    write(effective_path, effective)
    if effective["status"] != "completed":
        raise RuntimeError(f"posttest repair did not seal: {cell['cell_id']}")
    return effective


def rerun_zero_action_source(
    root: Path,
    cell: Mapping[str, Any],
    *,
    validated: Mapping[str, Any],
    config: Mapping[str, Any],
    progress: dict[str, Any],
) -> dict[str, Any]:
    original_folder = root / "sources" / cell["cell_id"]
    original_path = original_folder / "result.json"
    original = read(original_path)
    if original.get("operations") != 0 or original.get("batches"):
        raise RuntimeError("source repair is restricted to the retained zero-action failure")
    repair_root = original_folder / "source-repair-v3"
    result_path = repair_root / "sources" / cell["cell_id"] / "result.json"
    if result_path.exists():
        result = read(result_path)
    else:
        manifest_path = repair_root / "manifest.json"
        if repair_root.exists() and not manifest_path.exists():
            raise RuntimeError("incomplete source repair directory requires inspection")
        write(
            manifest_path,
            {
                "schema_version": "work-ii-rx-ps-zero-action-source-repair-1.0",
                "cell_id": cell["cell_id"],
                "started_epoch": time.time(),
                "original_result_sha256": file_sha256(original_path),
                "original_operations": 0,
                "original_batches": 0,
                "frozen_cell_reused": True,
                "deterministic_seeds_reused": True,
                "truth_revealed_to_agent": False,
            },
        )
        result = campaign.run_cell(
            repair_root,
            cell,
            p_package=validated["p_package"],
            s_contract=validated["s_contract"],
            config=config,
            progress=progress,
        )
    result = copy.deepcopy(result)
    result["recovery"] = {
        "kind": "zero_action_source_rerun",
        "original_result_sha256": file_sha256(original_path),
        "original_preserved": True,
    }
    if result.get("status") != "completed":
        raise RuntimeError(f"zero-action source rerun did not seal: {cell['cell_id']}")
    write(repair_root / "effective-result.json", result)
    return result


def write_recovery_summary(
    root: Path,
    results: Sequence[Mapping[str, Any]],
    phase: str,
) -> None:
    write(
        root / RECOVERY_VERSION / "summary.json",
        {
            "schema_version": "work-ii-rx-ps-five-world-dual-goal-recovery-summary-1.0",
            "phase": phase,
            "planned_sources": 60,
            "planned_source_batches": 720,
            "planned_posttests": 180,
            "effective_sources": len(results),
            "completed_sources": sum(row.get("status") == "completed" for row in results),
            "sealed_posttest_chains": sum(
                row.get("posttest_chain_sealed") is True for row in results
            ),
            "posttest_repair_cells": list(POSTTEST_REPAIRS),
            "zero_action_source_rerun_cell": SOURCE_RERUN_CELL,
            "public_numerics_limit": NUMERICS_LIMIT,
            "posttest_tool_attempt_limit": POSTTEST_TOOL_ATTEMPT_LIMIT,
            "truth_embargo_active": phase != "complete",
            "results": [
                {
                    "cell_id": row["cell_id"],
                    "status": row.get("status"),
                    "source_status": row.get("source_status"),
                    "operations": row.get("operations"),
                    "batches": len(row.get("batches", [])),
                    "posttest_chain_sealed": row.get("posttest_chain_sealed"),
                    "failure": row.get("failure"),
                    "recovered": bool(row.get("recovery")),
                }
                for row in results
            ],
        },
    )


def load_or_run_cell(
    root: Path,
    cell: Mapping[str, Any],
    *,
    validated: Mapping[str, Any],
    config: Mapping[str, Any],
    progress: dict[str, Any],
) -> dict[str, Any]:
    cell_id = cell["cell_id"]
    if cell_id in POSTTEST_REPAIRS:
        return repair_posttests(root, cell, config, progress)
    if cell_id == SOURCE_RERUN_CELL:
        return rerun_zero_action_source(
            root, cell, validated=validated, config=config, progress=progress
        )
    original_path = root / "sources" / cell_id / "result.json"
    if original_path.exists():
        result = read(original_path)
        if result.get("status") != "completed":
            raise RuntimeError(f"unexpected nonconforming cell without repair plan: {cell_id}")
        return result
    return campaign.run_cell(
        root,
        cell,
        p_package=validated["p_package"],
        s_contract=validated["s_contract"],
        config=config,
        progress=progress,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()
    configure_recovery_helpers()
    root = args.root.resolve()
    config = read(campaign.CONFIG)
    validated = campaign.validate_design(config)
    existing_design = read(root / "design.json")
    if existing_design.get("frozen_config_sha256") != campaign.digest(config):
        raise RuntimeError("existing run is not bound to the frozen recovery config")
    recovery_root = root / RECOVERY_VERSION
    recovery_root.mkdir(parents=True, exist_ok=True)
    write(
        recovery_root / "manifest.json",
        {
            "schema_version": "work-ii-rx-ps-five-world-dual-goal-recovery-1.0",
            "started_epoch": time.time(),
            "original_summary_sha256": file_sha256(root / "summary.json"),
            "posttest_repairs": {key: list(value) for key, value in POSTTEST_REPAIRS.items()},
            "source_rerun": SOURCE_RERUN_CELL,
            "remaining_never_started_cells": 44,
            "public_numerics_limit": NUMERICS_LIMIT,
            "posttest_tool_attempt_limit": POSTTEST_TOOL_ATTEMPT_LIMIT,
            "truth_revealed_before_all_cells_sealed": False,
        },
    )
    progress: dict[str, Any] = {
        "completed": 0,
        "total": 60,
        "stage": "recovery-starting",
        "phase": "repair",
    }
    stop = threading.Event()
    started = time.monotonic()

    def heartbeat() -> None:
        while not stop.wait(30):
            elapsed = time.monotonic() - started
            done = progress["completed"]
            print(
                json.dumps(
                    {
                        **progress,
                        "elapsed_s": round(elapsed),
                        "eta_s": round(elapsed / done * (60 - done)) if done else None,
                    },
                    default=str,
                ),
                flush=True,
            )

    heartbeat_thread = threading.Thread(target=heartbeat, daemon=True)
    heartbeat_thread.start()
    results: list[dict[str, Any]] = []
    try:
        for cell in validated["schedule"]:
            result = load_or_run_cell(
                root,
                cell,
                validated=validated,
                config=config,
                progress=progress,
            )
            results.append(result)
            progress["completed"] = len(results)
            write_recovery_summary(root, results, "sources_and_posttests")
            print(
                json.dumps(
                    {
                        "cell": result["cell_id"],
                        "status": result["status"],
                        "completed": len(results),
                        "total": 60,
                        "recovered": bool(result.get("recovery")),
                    }
                ),
                flush=True,
            )
            if result.get("status") != "completed":
                raise RuntimeError(f"effective cell is not complete: {result['cell_id']}")
        if not all(row.get("posttest_chain_sealed") is True for row in results):
            write_recovery_summary(root, results, "truth_embargoed_incomplete_posttest_chain")
            raise RuntimeError("not all posttest chains are sealed; reference truth remains embargoed")
        progress.update(stage="reference_truth", phase="provider_free", repair=False)
        truth = campaign.generate_truth(root, config)
        for result in results:
            query_rows = campaign.queries(config, result["locus"])
            evaluation = campaign.evaluate_predictions(
                result["posttests"]["Q"].get("payload"),
                query_rows,
                truth[result["world_id"]][result["locus"]],
            )
            write(root / "evaluations" / f"{result['cell_id']}.json", evaluation)
            retest = campaign.run_recommendation_retest(root, result)
            if retest is not None and (
                retest["failure"]
                or len(retest["batches"]) != 1
                or retest["rollbacks"]
                or retest["exact_replay"].get("verified") is not True
            ):
                raise RuntimeError(f"recommendation retest failed: {result['cell_id']}")
        write_recovery_summary(root, results, "complete")
        write(
            recovery_root / "completion.json",
            {
                "completed_epoch": time.time(),
                "source_sessions": len(results),
                "source_batches": sum(len(row.get("batches", [])) for row in results),
                "posttests": sum(len(row.get("posttests", {})) for row in results),
                "reference_executions": 600,
                "recommendation_retests": sum(
                    (root / "recommendation-retests" / row["cell_id"] / "result.json").exists()
                    for row in results
                ),
                "original_failures_preserved": True,
            },
        )
    finally:
        stop.set()
        heartbeat_thread.join(timeout=2)


if __name__ == "__main__":
    main()
