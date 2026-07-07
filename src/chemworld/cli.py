"""Command line interface for ChemWorld-Bench."""

from __future__ import annotations

import argparse
import csv
import glob
import json
import sys
from pathlib import Path
from typing import Any

import gymnasium as gym

import chemworld  # noqa: F401
from chemworld import ENV_ID
from chemworld.data.logging import load_jsonl
from chemworld.data.submission import (
    init_submission_bundle,
    summarize_submission_bundle,
    validate_submission_bundle,
    write_submission_manifest,
)
from chemworld.data.validation import validate_records
from chemworld.eval.leaderboard import aggregate_leaderboard, load_results
from chemworld.eval.metrics import evaluate_records
from chemworld.eval.runner import make_agent, run_agent
from chemworld.eval.suite import run_suite
from chemworld.eval.verify import verify_records
from chemworld.tasks import get_task, get_task_card, list_tasks


def _resolve_run_args(args: argparse.Namespace) -> dict[str, Any]:
    if args.task is None:
        return {
            "env": args.env,
            "world_split": args.world_split,
            "budget": args.budget,
            "objective": args.objective,
            "seed": 42 if args.seed is None else args.seed,
            "threshold": args.threshold,
            "task_id": None,
        }
    task = get_task(args.task)
    return {
        "env": task.env_id,
        "world_split": task.world_split,
        "budget": task.budget,
        "objective": task.objective,
        "seed": task.seeds[0] if args.seed is None else args.seed,
        "threshold": task.threshold,
        "task_id": task.task_id,
    }


def _resolve_suite_args(args: argparse.Namespace) -> dict[str, Any]:
    if args.task is None:
        return {
            "env": args.env,
            "world_splits": args.world_splits,
            "seeds": args.seeds,
            "budget": args.budget,
            "objective": args.objective,
            "threshold": args.threshold,
            "task_id": None,
        }
    task = get_task(args.task)
    return {
        "env": task.env_id,
        "world_splits": [task.world_split],
        "seeds": list(task.seeds),
        "budget": task.budget,
        "objective": task.objective,
        "threshold": task.threshold,
        "task_id": task.task_id,
    }


def _run(args: argparse.Namespace) -> None:
    config = _resolve_run_args(args)
    output = args.output
    if output is None:
        output = (
            f"runs/{args.agent}_{config['env']}_{config['world_split']}_"
            f"{config['objective']}_seed{config['seed']}.jsonl"
        )
    agent = make_agent(args.agent)
    command = args.command_line
    history = run_agent(
        env_id=config["env"],
        agent=agent,
        world_split=config["world_split"],
        budget=config["budget"],
        objective=config["objective"],
        seed=config["seed"],
        task_id=config["task_id"],
        output_path=output,
    )
    manifest_path = args.manifest
    if manifest_path is None:
        manifest_path = str(Path(output).with_suffix(".manifest.json"))
    write_submission_manifest(
        path=manifest_path,
        trajectory_path=output,
        agent_manifest=agent.manifest(),
        command=command,
        notes={
            "task_id": config["task_id"],
            "env_id": config["env"],
            "world_split": config["world_split"],
            "objective": config["objective"],
            "budget": config["budget"],
            "seed": config["seed"],
        },
    )
    print(
        json.dumps(
            {"trajectory": output, "manifest": manifest_path, "steps": len(history)},
            indent=2,
            sort_keys=True,
        )
    )


def _evaluate(args: argparse.Namespace) -> None:
    records = load_jsonl(args.submission)
    validate_records(records)
    result = evaluate_records(records, threshold=args.threshold).to_dict()
    if args.output is None:
        output = Path("results") / (Path(args.submission).stem + ".json")
    else:
        output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2, sort_keys=True)
    print(json.dumps({"result": str(output), **result}, indent=2, sort_keys=True))


def _verify(args: argparse.Namespace) -> None:
    records = load_jsonl(args.submission)
    result = verify_records(records, tolerance=args.tolerance).to_dict()
    if args.constitution:
        failures: list[dict[str, object]] = []
        for record in records:
            checks = record.get("constitution_checks", [])
            if not checks:
                failures.append(
                    {"step": record.get("step"), "message": "missing constitution checks"}
                )
                continue
            for name, passed in record.get("preconditions", {}).items():
                if not passed:
                    failures.append(
                        {
                            "step": record.get("step"),
                            "precondition": name,
                            "message": "failed action precondition",
                        }
                    )
            for check in checks:
                if not check.get("passed", False):
                    failures.append({"step": record.get("step"), "check": check})
        result["constitution_checked"] = True
        result["constitution_passed"] = not failures
        result["constitution_failures"] = failures
    print(json.dumps(result, indent=2, sort_keys=True))
    if not result["verified"] or not result.get("constitution_passed", True):
        raise SystemExit(1)


def _expand_patterns(patterns: list[str]) -> list[str]:
    expanded: list[str] = []
    for pattern in patterns:
        matches = glob.glob(pattern)
        expanded.extend(matches if matches else [pattern])
    return expanded


def _leaderboard(args: argparse.Namespace) -> None:
    paths = _expand_patterns(args.results)
    rows = aggregate_leaderboard(load_results(paths))
    if args.output:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()) if rows else [])
            writer.writeheader()
            writer.writerows(rows)
    print(json.dumps(rows, indent=2, sort_keys=True))


def _suite(args: argparse.Namespace) -> None:
    config = _resolve_suite_args(args)
    results = run_suite(
        agent_name=args.agent,
        env_id=config["env"],
        world_splits=config["world_splits"],
        seeds=config["seeds"],
        budget=config["budget"],
        objective=config["objective"],
        output_dir=args.output_dir,
        threshold=config["threshold"],
        task_id=config["task_id"],
    )
    print(
        json.dumps(
            {
                "runs": len(results),
                "output_dir": args.output_dir,
                "task_id": config["task_id"],
            },
            indent=2,
            sort_keys=True,
        )
    )


def _tasks_list(args: argparse.Namespace) -> None:
    del args
    print(json.dumps([task.to_dict() for task in list_tasks()], indent=2, sort_keys=True))


def _tasks_show(args: argparse.Namespace) -> None:
    print(json.dumps(get_task(args.task_id).to_dict(), indent=2, sort_keys=True))


def _tasks_card(args: argparse.Namespace) -> None:
    print(json.dumps(get_task_card(args.task_id), indent=2, sort_keys=True))


def _submission_init(args: argparse.Namespace) -> None:
    manifest = init_submission_bundle(
        args.path,
        agent_name=args.agent_name,
        agent_family=args.agent_family,
        task_id=args.task_id,
        seeds=args.seeds,
        command=args.command_text,
        dependency_file=args.dependency_file,
    )
    print(json.dumps({"path": args.path, "manifest": manifest}, indent=2, sort_keys=True))


def _submission_validate(args: argparse.Namespace) -> None:
    result = validate_submission_bundle(args.path).to_dict()
    print(json.dumps(result, indent=2, sort_keys=True))
    if not result["valid"]:
        raise SystemExit(1)


def _submission_summarize(args: argparse.Namespace) -> None:
    print(json.dumps(summarize_submission_bundle(args.path), indent=2, sort_keys=True))


def _inspect_constitution(args: argparse.Namespace) -> None:
    kwargs: dict[str, Any] = {
        "world_split": args.world_split,
        "budget": args.budget,
        "objective": args.objective,
        "seed": args.seed,
    }
    env = gym.make(args.env, **kwargs)
    try:
        env.reset(seed=args.seed)
        if not hasattr(env.unwrapped, "constitution_summary"):
            raise SystemExit(f"{args.env} does not expose a foundation constitution")
        print(json.dumps(env.unwrapped.constitution_summary(), indent=2, sort_keys=True))
    finally:
        env.close()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="chemworld")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Run an agent and write a trajectory JSONL.")
    run_parser.add_argument("--env", default=ENV_ID)
    run_parser.add_argument("--task")
    run_parser.add_argument("--agent", default="random")
    run_parser.add_argument("--world-split", default="public-dev")
    run_parser.add_argument("--budget", type=int, default=30)
    run_parser.add_argument("--objective", default="balanced")
    run_parser.add_argument("--seed", type=int)
    run_parser.add_argument("--threshold", type=float, default=0.75)
    run_parser.add_argument("--output")
    run_parser.add_argument("--manifest")
    run_parser.set_defaults(func=_run)

    eval_parser = subparsers.add_parser("evaluate", help="Evaluate one trajectory JSONL.")
    eval_parser.add_argument("--submission", required=True)
    eval_parser.add_argument("--threshold", type=float, default=0.75)
    eval_parser.add_argument("--output")
    eval_parser.set_defaults(func=_evaluate)

    verify_parser = subparsers.add_parser("verify", help="Replay and verify one trajectory JSONL.")
    verify_parser.add_argument("--submission", required=True)
    verify_parser.add_argument("--tolerance", type=float, default=1.0e-5)
    verify_parser.add_argument("--constitution", action="store_true")
    verify_parser.set_defaults(func=_verify)

    leaderboard_parser = subparsers.add_parser("leaderboard", help="Aggregate result JSON files.")
    leaderboard_parser.add_argument("--results", nargs="+", required=True)
    leaderboard_parser.add_argument("--output")
    leaderboard_parser.set_defaults(func=_leaderboard)

    suite_parser = subparsers.add_parser("suite", help="Run an agent across splits and seeds.")
    suite_parser.add_argument("--env", default=ENV_ID)
    suite_parser.add_argument("--task")
    suite_parser.add_argument("--agent", default="random")
    suite_parser.add_argument(
        "--world-splits",
        nargs="+",
        default=["public-test", "private-eval"],
    )
    suite_parser.add_argument("--seeds", nargs="+", type=int, default=[0, 1, 2, 3, 4])
    suite_parser.add_argument("--budget", type=int, default=30)
    suite_parser.add_argument("--objective", default="balanced")
    suite_parser.add_argument("--threshold", type=float, default=0.75)
    suite_parser.add_argument("--output-dir", default="runs/suite")
    suite_parser.set_defaults(func=_suite)

    tasks_parser = subparsers.add_parser("tasks", help="Inspect benchmark task specs.")
    tasks_subparsers = tasks_parser.add_subparsers(dest="tasks_command", required=True)
    tasks_list_parser = tasks_subparsers.add_parser("list", help="List registered tasks.")
    tasks_list_parser.set_defaults(func=_tasks_list)
    tasks_show_parser = tasks_subparsers.add_parser("show", help="Show one registered task.")
    tasks_show_parser.add_argument("task_id")
    tasks_show_parser.set_defaults(func=_tasks_show)
    tasks_card_parser = tasks_subparsers.add_parser("card", help="Show one task card.")
    tasks_card_parser.add_argument("task_id")
    tasks_card_parser.set_defaults(func=_tasks_card)

    submission_parser = subparsers.add_parser("submission", help="Manage submission bundles.")
    submission_subparsers = submission_parser.add_subparsers(
        dest="submission_command",
        required=True,
    )
    submission_init_parser = submission_subparsers.add_parser(
        "init",
        help="Create a local submission bundle skeleton.",
    )
    submission_init_parser.add_argument("path")
    submission_init_parser.add_argument("--agent-name", default="unknown")
    submission_init_parser.add_argument("--agent-family", default="unknown")
    submission_init_parser.add_argument("--task-id", default="reaction-optimization-standard")
    submission_init_parser.add_argument("--seeds", nargs="+", type=int, default=[0])
    submission_init_parser.add_argument("--command-text", nargs="*", default=[])
    submission_init_parser.add_argument("--dependency-file", default="pyproject.toml")
    submission_init_parser.set_defaults(func=_submission_init)
    submission_validate_parser = submission_subparsers.add_parser(
        "validate",
        help="Validate a submission bundle.",
    )
    submission_validate_parser.add_argument("path")
    submission_validate_parser.set_defaults(func=_submission_validate)
    submission_summarize_parser = submission_subparsers.add_parser(
        "summarize",
        help="Summarize a submission bundle.",
    )
    submission_summarize_parser.add_argument("path")
    submission_summarize_parser.set_defaults(func=_submission_summarize)

    constitution_parser = subparsers.add_parser(
        "inspect-constitution",
        help="Inspect an environment's physical constitution checklist.",
    )
    constitution_parser.add_argument("--env", default=ENV_ID)
    constitution_parser.add_argument("--world-split", default="public-dev")
    constitution_parser.add_argument("--budget", type=int, default=30)
    constitution_parser.add_argument("--objective", default="balanced")
    constitution_parser.add_argument("--seed", type=int, default=42)
    constitution_parser.set_defaults(func=_inspect_constitution)
    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.command_line = ["chemworld", *(argv if argv is not None else sys.argv[1:])]
    args.func(args)


if __name__ == "__main__":
    main()
