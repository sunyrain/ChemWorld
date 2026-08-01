"""Run one development-only strict G2 operation-level smoke trajectory."""

from __future__ import annotations

import argparse
import os
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from chemworld.agents.base import HistoryRecord
from chemworld.agents.live_llm import LiveLLMAgent
from chemworld.eval.provenance import (
    canonical_json_sha256,
    file_sha256,
    git_source_commit,
    git_worktree_dirty,
    write_json_atomic,
)
from chemworld.eval.runner import run_agent
from chemworld.providers.wellau import WellAUClient
from chemworld.tasks import get_task

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_ROOT = (
    ROOT / "runs/development/g2-reaction-to-assay-w0-a0-wellau-sol-high-v1"
)
RUN_SCHEMA_VERSION = "chemworld-g2-development-smoke-0.1"


def _utc_now() -> str:
    return datetime.now(UTC).isoformat()


def _resource_limits(
    *, operation_limit: int, max_attempts: int, max_tokens: int
) -> dict[str, Any]:
    return {
        "operation_limit": operation_limit,
        "complete_experiment_limit": 1,
        "wall_time_limit_s": 3_600.0,
        "model_call_limit": operation_limit * max_attempts,
        "input_token_limit": operation_limit * 12_000,
        "output_token_limit": operation_limit * max_tokens,
        # WellAU has no verifiable price schedule. A monetary cap would falsely
        # turn an unknown billed cost into a measured zero, so it is omitted.
        "training_environment_step_limit": 0,
        "checkpoint_complete_experiments": (1,),
    }


def _redacted_failure(error: Exception) -> dict[str, Any]:
    return {
        "error_type": type(error).__name__,
        "provider_status_code": getattr(error, "status_code", None),
        "retryable": bool(getattr(error, "retryable", False)),
        "reported_attempts": getattr(error, "attempts", None),
        "error_text_retained": False,
    }


def _history_summary(history: list[HistoryRecord]) -> dict[str, Any]:
    action_counts = Counter(str(record.action.get("operation")) for record in history)
    measurement_counts = Counter(
        str(record.action.get("instrument"))
        for record in history
        if record.action.get("operation") == "measure"
    )
    invalid_steps = [
        {
            "step": record.step,
            "action": record.action,
            "transaction_status": record.info.get("transaction_status"),
            "error_message": record.info.get("error_message"),
            "constraint_flags": {
                str(key): bool(value)
                for key, value in record.info.get("constraint_flags", {}).items()
                if value
            },
        }
        for record in history
        if record.info.get("transaction_status") != "committed"
    ]
    completed = [record for record in history if record.event_type == "experiment_end"]
    scores = [
        float(score)
        for record in history
        if isinstance((score := record.info.get("leaderboard_score")), int | float)
        and not isinstance(score, bool)
    ]
    return {
        "operation_count": len(history),
        "complete_experiment_count": len(completed),
        "action_counts": dict(sorted(action_counts.items())),
        "measurement_counts": dict(sorted(measurement_counts.items())),
        "invalid_operation_count": len(invalid_steps),
        "invalid_steps": invalid_steps,
        "terminate_steps": [
            record.step
            for record in history
            if record.action.get("operation") == "terminate"
        ],
        "final_assay_steps": [
            record.step
            for record in history
            if record.action.get("operation") == "measure"
            and record.action.get("instrument") == "final_assay"
        ],
        "experiment_end_steps": [record.step for record in completed],
        "best_leaderboard_score": max(scores) if scores else None,
        "terminal_leaderboard_score": (
            completed[-1].info.get("leaderboard_score") if completed else None
        ),
        "terminal_observation": completed[-1].observation if completed else None,
        "last_action": history[-1].action if history else None,
        "last_event_type": history[-1].event_type if history else None,
    }


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--task", default="reaction-to-assay")
    parser.add_argument("--world-seed", type=int, default=0)
    parser.add_argument("--agent-seed", type=int, default=0)
    parser.add_argument("--model", default="gpt-5.6-sol")
    parser.add_argument(
        "--reasoning-effort", choices=("medium", "high"), default="high"
    )
    parser.add_argument("--max-tokens", type=int, default=4_000)
    parser.add_argument("--max-attempts", type=int, default=2)
    parser.add_argument("--timeout-s", type=float, default=180.0)
    parser.add_argument(
        "--allow-external-provider",
        action="store_true",
        help="Required opt-in because the run makes billable external model requests.",
    )
    return parser


def main() -> int:
    args = _build_parser().parse_args()
    if not args.allow_external_provider:
        raise RuntimeError("external execution requires --allow-external-provider")
    if not os.environ.get("WELLAU_API_KEY", "").strip():
        raise RuntimeError("WELLAU_API_KEY is not available in the process environment")
    if args.max_tokens <= 0 or args.max_attempts <= 0 or args.timeout_s <= 0:
        raise ValueError("provider limits must be positive")

    task = get_task(args.task)
    if args.world_seed not in task.seeds:
        raise ValueError(
            f"world seed {args.world_seed} is outside the registered task seeds"
        )
    if task.episode_mode != "single_experiment":
        raise ValueError("this smoke launcher requires a single_experiment task")

    output_root = args.output_root.resolve()
    trajectory_path = output_root / "trajectory.jsonl"
    config_path = output_root / "run_config.json"
    summary_path = output_root / "run_summary.json"
    if output_root.exists():
        raise FileExistsError(
            f"refusing to overwrite existing output root: {output_root}"
        )
    output_root.mkdir(parents=True)

    resource_limits = _resource_limits(
        operation_limit=task.budget,
        max_attempts=args.max_attempts,
        max_tokens=args.max_tokens,
    )
    run_config: dict[str, Any] = {
        "schema_version": RUN_SCHEMA_VERSION,
        "formal_result": False,
        "benchmark_claim_allowed": False,
        "purpose": "development-only strict G2 lifecycle and autonomy smoke",
        "frozen_at": _utc_now(),
        "source": {
            "git_commit": git_source_commit(ROOT),
            "worktree_dirty": git_worktree_dirty(
                ROOT,
                excluded_prefixes=("runs/development/",),
            ),
        },
        "task": {
            "task_id": task.task_id,
            "task_contract_hash": task.contract_hash,
            "world_split": task.world_split,
            "world_seed": args.world_seed,
            "agent_seed": args.agent_seed,
            "budget": task.budget,
            "episode_mode": task.episode_mode,
            "objective": task.objective,
        },
        "method": {
            "method_id": "g2_direct_live_llm_v1",
            "decision_scope": "operation",
            "provider": "WellAU",
            "model": args.model,
            "reasoning_effort": args.reasoning_effort,
            "response_max_tokens": args.max_tokens,
            "timeout_s": args.timeout_s,
            "max_attempts": args.max_attempts,
            "retry_backoff_s": 0.25,
            "spectrum_disclosure": "assigned",
            "automatic_action_repair": False,
            "automatic_terminate": False,
            "automatic_final_assay": False,
            "failed_or_invalid_actions_retained": True,
            "complete_current_experiment_ledger_in_prompt": False,
            "current_prompt_memory_note": (
                "The existing direct controller stores the full current operation "
                "ledger internally but supplies only compact recent decisions to its prompt."
            ),
        },
        "resource_contract": {
            **resource_limits,
            "checkpoint_complete_experiments": list(
                resource_limits["checkpoint_complete_experiments"]
            ),
            "monetary_cost_usd_limit": None,
            "monetary_accounting": "unknown_provider_price",
        },
        "artifacts": {
            "trajectory": trajectory_path.name,
            "summary": summary_path.name,
        },
    }
    run_config["config_sha256"] = canonical_json_sha256(run_config)
    write_json_atomic(config_path, run_config)

    client = WellAUClient(
        model=args.model,
        reasoning_effort=args.reasoning_effort,
        timeout_s=args.timeout_s,
        max_attempts=args.max_attempts,
        retry_backoff_s=0.25,
    )
    agent = LiveLLMAgent(
        client,
        role_id="g2_direct_smoke_v1",
        spectrum_disclosure="assigned",
        response_max_tokens=args.max_tokens,
        fail_fast_on_unbillable_provider_failure=True,
    )
    started_at = _utc_now()
    try:
        history = run_agent(
            env_id=task.env_id,
            agent=agent,
            world_split=task.world_split,
            budget=task.budget,
            objective=task.objective,
            seed=args.world_seed,
            agent_seed=args.agent_seed,
            task_id=task.task_id,
            output_path=trajectory_path,
            budget_override=task.budget,
            episode_mode_override=task.episode_mode,
            method_resource_limits=resource_limits,
            evaluation_policy="task_contract",
        )
    except Exception as error:
        failure_summary = {
            "schema_version": RUN_SCHEMA_VERSION,
            "formal_result": False,
            "run_status": "infrastructure_or_execution_failure",
            "started_at": started_at,
            "finished_at": _utc_now(),
            "config_sha256": run_config["config_sha256"],
            "failure": _redacted_failure(error),
            "trajectory_materialized": trajectory_path.exists(),
            "trajectory_sha256": (
                file_sha256(trajectory_path) if trajectory_path.exists() else None
            ),
        }
        write_json_atomic(summary_path, failure_summary)
        raise

    method_resources = agent.method_resource_usage()
    receipts = agent.provider_receipts()
    receipt_status_counts = Counter(str(item.get("status")) for item in receipts)
    behavior = _history_summary(history)
    completed = behavior["complete_experiment_count"] == 1
    summary = {
        "schema_version": RUN_SCHEMA_VERSION,
        "formal_result": False,
        "benchmark_claim_allowed": False,
        "run_status": "completed"
        if completed
        else "operation_budget_exhausted_incomplete",
        "started_at": started_at,
        "finished_at": _utc_now(),
        "config_sha256": run_config["config_sha256"],
        "trajectory_sha256": file_sha256(trajectory_path),
        "strict_g2_contract_satisfied": {
            "one_agent_decision_per_operation": True,
            "automatic_action_repair": False,
            "automatic_terminate": False,
            "automatic_final_assay": False,
            "invalid_actions_retained": True,
        },
        "behavior": behavior,
        "method_resources": method_resources,
        "provider_receipts": receipts,
        "provider_receipt_status_counts": dict(sorted(receipt_status_counts.items())),
        "accounting_note": (
            "Provider calls and reported tokens are retained; billed USD is unknown "
            "because WellAU has no verifiable frozen price schedule."
        ),
        "limitations": [
            "one public development world and one agent seed",
            "lifecycle smoke rather than an optimization or mechanism-discovery claim",
            "existing direct prompt omits the complete current-experiment operation ledger",
            "no hard material-portion or per-instrument quota is implemented in this run",
            "provider billed USD cost is unknown",
        ],
    }
    write_json_atomic(summary_path, summary)
    print(
        {
            "output_root": str(output_root),
            "run_status": summary["run_status"],
            "operations": behavior["operation_count"],
            "complete_experiments": behavior["complete_experiment_count"],
            "invalid_operations": behavior["invalid_operation_count"],
            "terminal_score": behavior["terminal_leaderboard_score"],
            "model_calls": method_resources["model_call_count"],
            "input_tokens": method_resources["input_token_count"],
            "output_tokens": method_resources["output_token_count"],
            "billed_usd": "unknown",
        }
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
