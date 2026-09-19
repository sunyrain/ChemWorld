"""Resume failed RX-P Q/K2 posttests without rerunning source experiments."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sqlite3
import tempfile
import time
from pathlib import Path

import scripts.run_work_ii_ec_dual_goal_trial as shared
import scripts.run_work_ii_rx_p_opaque_dual_goal_canary as canary


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def copy_sqlite_database(source: Path, destination: Path) -> None:
    with sqlite3.connect(source) as source_db, sqlite3.connect(destination) as target_db:
        source_db.backup(target_db)


def restore_session_index(agent, source_sessions: Path, thread_id: str) -> None:
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
                str(meta.get("model_provider", canary.PROVIDER["id"])),
                str(agent.workspace.agent_directory),
                f"RX posttest continuation {thread_id}",
                json.dumps({"type": "workspaceWrite"}),
                "never",
                0,
                1,
                0,
                str(meta.get("cli_version", "")),
                "RX sealed posttest continuation",
                "enabled",
                canary.PROVIDER["model"],
                canary.PROVIDER["reasoning_effort"],
                now_ms,
                now_ms,
                str(meta.get("thread_source", "user")),
                "RX sealed posttest continuation",
                now_ms // 1000,
                now_ms,
                str(meta.get("history_mode", "paginated")),
                str(meta.get("originator", "codex_exec")),
            ),
        )


def repair_cell(root: Path, goal: str, truth: dict) -> dict:
    cell = root / f"{goal}-{canary.LOCUS}-{canary.ARM}"
    original = read(cell / "result.json")
    repair = cell / "posttest-repair-v3"
    result_path = repair / "result.json"
    if result_path.exists():
        return read(result_path)
    repair.mkdir(parents=True, exist_ok=False)
    q_original = original.get("posttests", {}).get("Q", {})
    receipts = read(cell / "source-receipts.json")
    thread_id = q_original.get("thread_id") or receipts[-1].get("thread_id")
    if not thread_id:
        raise RuntimeError(f"{cell.name} has no resumable thread id")
    output = {
        "schema_version": "work-ii-rx-p-opaque-posttest-repair-0.1",
        "cell_id": cell.name,
        "original_status": original.get("status"),
        "original_failure": original.get("failure"),
        "source_operations_reused": original.get("operations"),
        "source_batches_reused": len(original.get("batches", [])),
        "source_experiments_rerun": False,
        "question_changed": False,
        "truth_revealed_to_agent": False,
        "posttests": {},
        "status": "failed",
    }
    with tempfile.TemporaryDirectory(prefix="chemworld-rx-posttest-repair-") as temporary:
        temporary_root = Path(temporary)
        agent = canary.RxFreeResearchAgent(
            goal=goal,
            home_root=temporary_root,
            output=repair,
            workspace=temporary_root / "laboratory",
            initial_world_model=None,
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
        agent.followup_environment = shared._prepare_codex_home(
            agent.home_root,
            canary.PROVIDER,
        )
        agent._session_process_environment = agent.followup_environment
        source_sessions = cell / "provider-rollouts"
        restore_session_index(agent, source_sessions, thread_id)
        progress = {
            "stage": cell.name,
            "phase": "Q-repair",
            "operations": original.get("operations", 0),
            "batches": len(original.get("batches", [])),
            "repair": True,
        }
        try:
            q_turn = shared.posttest(agent, repair, "Q", thread_id, progress)
            output["posttests"]["Q"] = q_turn
            output["prediction_evaluation"] = shared.evaluate_predictions(
                q_turn.get("payload"), truth
            )
            next_thread = q_turn.get("thread_id") or thread_id
            if not q_turn.get("failure") and output["prediction_evaluation"].get("valid"):
                progress["phase"] = "K2-repair"
                output["posttests"]["K2"] = shared.posttest(
                    agent,
                    repair,
                    "K2",
                    next_thread,
                    progress,
                )
        finally:
            agent.close()
        sessions = agent.home_root / "codex-home" / "sessions"
        if sessions.exists():
            shutil.copytree(sessions, repair / "provider-rollouts")
    output["status"] = (
        "completed"
        if (
            not output["posttests"].get("Q", {}).get("failure")
            and output.get("prediction_evaluation", {}).get("valid") is True
            and not output["posttests"].get("K2", {}).get("failure")
            and output["posttests"].get("K2", {}).get("payload")
        )
        else "failed"
    )
    shared.write(result_path, output)
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()
    canary.configure_shared_helpers()
    truth = read(args.root / "truth.json")
    results = [repair_cell(args.root, goal, truth) for goal in canary.GOALS]
    summary = {
        "schema_version": "work-ii-rx-p-opaque-posttest-repair-summary-0.1",
        "planned_repairs": 2,
        "completed_repairs": sum(row["status"] == "completed" for row in results),
        "results": results,
    }
    shared.write(args.root / "posttest-repair-v3-summary.json", summary)
    print(
        json.dumps(
            {
                "completed_repairs": summary["completed_repairs"],
                "planned_repairs": summary["planned_repairs"],
            }
        ),
        flush=True,
    )


if __name__ == "__main__":
    main()
