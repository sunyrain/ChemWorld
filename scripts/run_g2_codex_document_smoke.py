"""Run one direct Codex G2 smoke with file-backed experiment memory."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from chemworld.agents.documented_codex_g2 import DocumentedCodexG2Agent
from chemworld.agents.experiment_documents import ExperimentDocumentWorkspace
from chemworld.eval.provenance import (
    canonical_json_sha256,
    file_sha256,
    git_source_commit,
    git_worktree_dirty,
    write_json_atomic,
)
from chemworld.eval.runner import run_agent
from chemworld.providers.codex_subscription import CodexSubscriptionClient
from chemworld.tasks import get_task

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_ROOT = (
    ROOT / "runs/development/g2-reaction-to-assay-w0-a0-codex-sol-high-doc-v1"
)


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _slope(values: list[int]) -> float | None:
    if len(values) < 2:
        return None
    center = (len(values) + 1) / 2
    denominator = sum((index - center) ** 2 for index in range(1, len(values) + 1))
    return sum(
        (index - center) * (value - sum(values) / len(values))
        for index, value in enumerate(values, start=1)
    ) / denominator


def _series(values: list[int]) -> dict[str, Any]:
    return {
        "count": len(values),
        "first": values[0] if values else None,
        "last": values[-1] if values else None,
        "minimum": min(values) if values else None,
        "maximum": max(values) if values else None,
        "mean": sum(values) / len(values) if values else None,
        "ols_slope_per_decision": _slope(values),
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--world-seed", type=int, default=0)
    parser.add_argument("--agent-seed", type=int, default=0)
    parser.add_argument("--model", default="gpt-5.6-sol")
    parser.add_argument("--reasoning-effort", default="high")
    parser.add_argument("--timeout-s", type=float, default=600.0)
    parser.add_argument("--max-attempts", type=int, default=1)
    return parser


def main() -> int:
    args = _parser().parse_args()
    task = get_task("reaction-to-assay")
    output_root = args.output_root.resolve()
    if output_root.exists():
        raise FileExistsError(f"refusing to overwrite {output_root}")
    output_root.mkdir(parents=True)
    trajectory_path = output_root / "trajectory.jsonl"
    summary_path = output_root / "run_summary.json"
    config_path = output_root / "run_config.json"

    documents = ExperimentDocumentWorkspace(output_root / "codex_workspace")
    initial_documents = documents.initialize()
    client = CodexSubscriptionClient(
        model=args.model,
        reasoning_effort=args.reasoning_effort,
        timeout_s=args.timeout_s,
        max_attempts=args.max_attempts,
        persistent_workspace=documents.run_directory,
        allow_document_tools=True,
    )
    agent = DocumentedCodexG2Agent(
        client,
        documents=documents,
        role_id="g2_direct_codex_document_smoke_v1",
        spectrum_disclosure="assigned",
        response_max_tokens=8_000,
        prompt_token_estimate_cap=2_500,
        fail_fast_on_unbillable_provider_failure=True,
    )
    resource_limits = {
        "operation_limit": task.budget,
        "complete_experiment_limit": 1,
        "wall_time_limit_s": 7_200.0,
        "model_call_limit": task.budget * args.max_attempts,
        "input_token_limit": task.budget * 30_000,
        "output_token_limit": task.budget * 12_000,
        "training_environment_step_limit": 0,
        "checkpoint_complete_experiments": (1,),
    }
    config: dict[str, Any] = {
        "schema_version": "chemworld-g2-direct-codex-document-smoke-0.1",
        "formal_result": False,
        "purpose": "one-world one-seed direct Codex operation-level smoke",
        "created_at": _now(),
        "source": {
            "git_commit": git_source_commit(ROOT),
            "worktree_dirty": git_worktree_dirty(
                ROOT, excluded_prefixes=("runs/development/",)
            ),
        },
        "task": {
            "task_id": task.task_id,
            "world_seed": args.world_seed,
            "agent_seed": args.agent_seed,
            "budget": task.budget,
            "episode_mode": task.episode_mode,
        },
        "method": {
            "provider": "OpenAI Codex CLI with ChatGPT subscription",
            "model": args.model,
            "reasoning_effort": args.reasoning_effort,
            "one_codex_exec_per_operation": True,
            "automatic_action_repair": False,
            "automatic_closeout": False,
            "ledger_contents_in_prompt": False,
            "environment_ledger_agent_writable": False,
            "model_notebook_agent_writable": True,
            "codex_workspace": "codex_workspace",
        },
        "initial_document_manifest": initial_documents,
        "resource_limits": {
            key: list(value) if isinstance(value, tuple) else value
            for key, value in resource_limits.items()
        },
    }
    config["config_sha256"] = canonical_json_sha256(config)
    write_json_atomic(config_path, config)

    step_metrics: list[dict[str, Any]] = []

    def progress(record: Any, trace: list[dict[str, Any]]) -> None:
        decision = trace[0] if trace else {}
        provider_usage = decision.get("provider_usage", {})
        manifest = agent.document_manifest()
        row = {
            "step": record.step,
            "operation": record.action.get("operation"),
            "instrument": record.action.get("instrument"),
            "transaction_status": record.info.get("transaction_status"),
            "event_type": record.event_type,
            "prompt_estimated_tokens": decision.get("prompt_estimated_tokens"),
            "provider_input_tokens": provider_usage.get("prompt_tokens"),
            "provider_output_tokens": provider_usage.get("completion_tokens"),
            "ledger_lines": manifest["authoritative_ledger"]["line_count"],
            "ledger_bytes": manifest["authoritative_ledger"]["byte_count"],
            "notebook_bytes": manifest["model_notebook"]["byte_count"],
            "notebook_updated": decision.get("document_memory", {}).get(
                "model_notebook_updated"
            ),
        }
        step_metrics.append(row)
        print(json.dumps(row, ensure_ascii=False), flush=True)

    started_at = _now()
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
            step_callback=progress,
            method_resource_limits=resource_limits,
            evaluation_policy="task_contract",
        )
    except Exception as error:
        write_json_atomic(
            summary_path,
            {
                "schema_version": config["schema_version"],
                "run_status": "failed",
                "started_at": started_at,
                "finished_at": _now(),
                "config_sha256": config["config_sha256"],
                "failure": {
                    "error_type": type(error).__name__,
                    "error_text_retained": False,
                },
                "completed_step_metrics": step_metrics,
                "final_document_manifest": agent.document_manifest(),
                "trajectory_sha256": (
                    file_sha256(trajectory_path) if trajectory_path.exists() else None
                ),
            },
        )
        raise

    action_counts = Counter(str(item.action.get("operation")) for item in history)
    invalid = [
        item.step
        for item in history
        if item.info.get("transaction_status") != "committed"
    ]
    completed = [item for item in history if item.event_type == "experiment_end"]
    prompt_values = [
        int(row["prompt_estimated_tokens"])
        for row in step_metrics
        if isinstance(row["prompt_estimated_tokens"], int)
    ]
    input_values = [
        int(row["provider_input_tokens"])
        for row in step_metrics
        if isinstance(row["provider_input_tokens"], int)
    ]
    ledger_values = [int(row["ledger_bytes"]) for row in step_metrics]
    final_documents = agent.document_manifest()
    method_resources = agent.method_resource_usage()
    summary = {
        "schema_version": config["schema_version"],
        "run_status": "completed" if completed else "budget_exhausted_incomplete",
        "started_at": started_at,
        "finished_at": _now(),
        "config_sha256": config["config_sha256"],
        "trajectory_sha256": file_sha256(trajectory_path),
        "behavior": {
            "operation_count": len(history),
            "complete_experiment_count": len(completed),
            "action_counts": dict(sorted(action_counts.items())),
            "invalid_operation_count": len(invalid),
            "invalid_steps": invalid,
            "terminal_score": (
                completed[-1].info.get("leaderboard_score") if completed else None
            ),
            "terminal_action": completed[-1].action if completed else None,
        },
        "prompt_growth_audit": {
            "ledger_contents_directly_in_prompt": False,
            "prompt_estimated_tokens": _series(prompt_values),
            "provider_input_tokens": _series(input_values),
            "authoritative_ledger_bytes": _series(ledger_values),
            "notebook_update_steps": [
                row["step"] for row in step_metrics if row["notebook_updated"]
            ],
            "interpretation_limit": (
                "Codex input tokens include fixed instructions, output schema, tool "
                "context, and any on-demand document reads; they are not prompt-only."
            ),
        },
        "step_metrics": step_metrics,
        "initial_document_manifest": initial_documents,
        "final_document_manifest": final_documents,
        "method_resources": method_resources,
        "provider_receipts": agent.provider_receipts(),
    }
    write_json_atomic(summary_path, summary)
    print(
        json.dumps(
            {
                "output_root": str(output_root),
                "run_status": summary["run_status"],
                **summary["behavior"],
            },
            ensure_ascii=False,
        ),
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
