"""Run a DeepSeek or classical active-learning evaluation on ChemWorld tasks."""

from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from apps.task_lab.classic_runner import CLASSIC_AGENT_IDS, run_classic_task
from apps.task_lab.deepseek_client import DeepSeekClient
from apps.task_lab.runner import run_task
from chemworld.tasks import list_tasks

DEFAULT_TASKS = ("reaction-to-assay", "equilibrium-characterization")


def _event_printer(event: dict[str, Any]) -> None:
    event_type = event.get("type")
    task_id = event.get("task_id", "-")
    if event_type == "task_started":
        print(f"\n[{task_id}] 开始：{event['background']['title']}", flush=True)
    elif event_type == "plan_ready":
        print(
            f"[{task_id}] 计划 {event['planned_action_count']} 步："
            f"{event.get('strategy_summary', '')}",
            flush=True,
        )
    elif event_type == "action_rejected":
        print(f"[{task_id}] 计划动作被拒绝：{event.get('reasons', [])}", flush=True)
    elif event_type == "surrogate_decision":
        print(
            f"[{task_id}] {event['phase']} | trained={event['trained_recipe_count']} | "
            f"policy={event['selected_policy']} | acquisition={event.get('acquisition_value')}",
            flush=True,
        )
    elif event_type == "step_completed":
        score = event.get("leaderboard_score")
        score_text = "-" if score is None else f"{float(score):.4f}"
        print(
            f"[{task_id}] {event['step']:02d}/{event['step_limit']} "
            f"{event['action'].get('operation')} | final={score_text} | "
            f"best={event.get('best_score')} | remaining={event.get('remaining_budget')}",
            flush=True,
        )
    elif event_type == "task_completed":
        print(
            f"[{task_id}] 完成：status={event['status']}, "
            f"score={event.get('official_score') or event.get('research_score')}, "
            f"experiments={event.get('experiment_count')}, steps={event['steps']}",
            flush=True,
        )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tasks", nargs="+")
    parser.add_argument(
        "--all-tasks",
        action="store_true",
        help="Run every registered task instead of the two quick-start tasks.",
    )
    parser.add_argument("--seed", type=int)
    parser.add_argument(
        "--agent",
        choices=("deepseek", *CLASSIC_AGENT_IDS),
        default="deepseek",
        help="Decision backend. Classical agents do not require an API key.",
    )
    parser.add_argument("--mode", choices=("plan", "adaptive"), default="adaptive")
    parser.add_argument("--max-steps", type=int, default=18)
    parser.add_argument(
        "--budget-multiplier",
        type=float,
        default=1.0,
        help="Extended-research budget multiplier from 1 to 4.",
    )
    parser.add_argument(
        "--campaign-override",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Run a single-experiment contract as a repeated research campaign.",
    )
    parser.add_argument("--model")
    parser.add_argument("--base-url")
    parser.add_argument(
        "--thinking",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Use model-side thinking while returning only structured audit summaries.",
    )
    parser.add_argument(
        "--reasoning-effort",
        choices=("high", "max"),
        default="max",
        help="DeepSeek V4 thinking effort.",
    )
    parser.add_argument(
        "--spectrum-disclosure",
        choices=("raw", "unassigned", "assigned"),
        default="unassigned",
        help=(
            "Instrument evidence supplied to the agent: raw curves, unassigned peaks, "
            "or assigned peaks."
        ),
    )
    parser.add_argument("--output-dir")
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Merge rerun task results into an existing summary in --output-dir.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    output_dir = Path(args.output_dir or f"runs/task_lab/{stamp}")
    output_dir.mkdir(parents=True, exist_ok=True)
    client = (
        DeepSeekClient(
            model=args.model,
            base_url=args.base_url,
            thinking=args.thinking,
            reasoning_effort=args.reasoning_effort,
        )
        if args.agent == "deepseek"
        else None
    )
    task_ids = (
        [task.task_id for task in list_tasks()]
        if args.all_tasks
        else (args.tasks or list(DEFAULT_TASKS))
    )
    summary_path = output_dir / "evaluation_summary.json"
    result_map: dict[str, dict[str, Any]] = {}
    if args.resume and summary_path.is_file():
        previous = json.loads(summary_path.read_text(encoding="utf-8"))
        result_map = {
            str(item["task_id"]): item
            for item in previous.get("results", [])
            if isinstance(item, dict) and item.get("task_id")
        }
    for task_id in task_ids:
        try:
            if args.agent == "deepseek":
                if client is None:
                    raise RuntimeError("DeepSeek client was not initialized")
                result = run_task(
                    client=client,
                    task_id=task_id,
                    output_dir=output_dir,
                    seed=args.seed,
                    mode=args.mode,
                    max_steps=args.max_steps,
                    budget_multiplier=args.budget_multiplier,
                    campaign_override=args.campaign_override,
                    spectrum_disclosure=args.spectrum_disclosure,
                    event_callback=_event_printer,
                )
            else:
                result = run_classic_task(
                    agent_id=args.agent,
                    task_id=task_id,
                    output_dir=output_dir,
                    seed=args.seed,
                    max_steps=args.max_steps,
                    budget_multiplier=args.budget_multiplier,
                    campaign_override=args.campaign_override,
                    spectrum_disclosure=args.spectrum_disclosure,
                    event_callback=_event_printer,
                )
            result_map[task_id] = result.to_dict()
        except Exception as exc:
            failure = {"task_id": task_id, "status": "error", "error": str(exc)}
            result_map[task_id] = failure
            print(f"[{task_id}] ERROR: {exc}", flush=True)
    ordered_task_ids = [task.task_id for task in list_tasks()]
    results = [result_map[task_id] for task_id in ordered_task_ids if task_id in result_map]
    summary = {
        "schema_version": "chemworld-task-lab-evaluation-0.2",
        "generated_at": datetime.now(UTC).isoformat(),
        "agent_backend": args.agent,
        "model": client.model if client is not None else args.agent,
        "mode": args.mode,
        "thinking": args.thinking if client is not None else False,
        "reasoning_effort": args.reasoning_effort if client is not None else None,
        "budget_multiplier": args.budget_multiplier,
        "campaign_override": args.campaign_override,
        "spectrum_disclosure": args.spectrum_disclosure,
        "results": results,
    }
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"\n汇总：{summary_path.resolve()}")
    print(json.dumps(results, ensure_ascii=False, indent=2))
    return 0 if all(item.get("status") != "error" for item in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
