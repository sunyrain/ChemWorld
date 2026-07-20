"""Run a bounded PPO learning smoke test on the two flagship tasks.

This is Train/Dev development evidence, not a formal benchmark run.  It retains
training diagnostics and evaluates exact contract-bound checkpoints under both
deterministic and seeded stochastic inference.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from chemworld.rl.environment import RLWorldAllocation, load_rl_protocol
from chemworld.rl.evaluation import evaluate_sb3_checkpoint
from chemworld.rl.training import train_sb3_baseline
from chemworld.tasks import FLAGSHIP_TASK_IDS, get_task

ROOT = Path(__file__).resolve().parents[1]
ALLOCATION_PROTOCOL = ROOT / "configs/benchmark/confirmatory_freeze_vnext.json"
DEFAULT_ARTIFACT_ROOT = ROOT / "runs/flagship-ppo-smoke"
DEFAULT_REPORT = ROOT / "workstreams/flagship_tasks/reports/flagship-ppo-smoke.json"
REPORT_VERSION = "chemworld-flagship-ppo-smoke-0.1"
PRIMARY_METRICS = {
    "reaction-to-crystallization": "crystal_csd_quality",
    "electrochemical-conversion": "faradaic_efficiency",
}
FAILURE_COUNT_KEYS = (
    "runtime_domain_failure_count",
    "observation_domain_failure_count",
    "transaction_rollback_count",
    "constitution_failure_count",
)


def _checkpoint_steps(total_timesteps: int, parallel_environments: int) -> tuple[int, ...]:
    raw = (total_timesteps // 4, total_timesteps // 2, total_timesteps)
    aligned = {
        max(
            parallel_environments,
            (step // parallel_environments) * parallel_environments,
        )
        for step in raw
    }
    return tuple(sorted(step for step in aligned if step <= total_timesteps))


def _evaluation_gates(evaluation: dict[str, Any]) -> dict[str, bool]:
    summary = evaluation["summary"]
    return {
        "checkpoint_contract_exact": all(evaluation["checkpoint_contract_compatibility"].values()),
        "completed_experiment_observed": summary["complete_experiment_count"] > 0,
        "behavior_complete_experiment_observed": (
            summary["behavior_complete_experiment_count"] > 0
        ),
        "clean_behavior_complete_episode_observed": (
            summary["clean_behavior_complete_episode_count"] > 0
        ),
        "primary_metric_observed": summary["primary_metric_observation_count"] > 0,
        "zero_execution_failures": all(summary[key] == 0 for key in FAILURE_COUNT_KEYS),
    }


def _candidate_key(evaluation: dict[str, Any]) -> tuple[float, ...]:
    summary = evaluation["summary"]
    return (
        float(summary["clean_behavior_complete_episode_count"]),
        float(summary["behavior_complete_experiment_count"]),
        float(summary["complete_experiment_count"]),
        float(summary["mean_episode_best_score"]),
    )


def _candidate_is_clean_and_complete(evaluation: dict[str, Any]) -> bool:
    gates = evaluation["gates"]
    return bool(
        gates["checkpoint_contract_exact"]
        and gates["completed_experiment_observed"]
        and gates["behavior_complete_experiment_observed"]
        and gates["clean_behavior_complete_episode_observed"]
        and gates["primary_metric_observed"]
    )


def _clean_behavior_complete_episode_count(evaluation: dict[str, Any]) -> int:
    return sum(
        int(
            card["behavior_complete_experiment_count"] > 0
            and card["complete_experiment_count"] > 0
            and card["best_primary_metric"] is not None
            and all(card[key] == 0 for key in FAILURE_COUNT_KEYS)
        )
        for card in evaluation["episode_cards"]
    )


def _formal_candidate_ready(evaluation: dict[str, Any]) -> bool:
    summary = evaluation["summary"]
    return bool(
        summary["episode_completion_rate"] == 1.0
        and summary["behavior_complete_experiment_rate"] == 1.0
        and summary["primary_metric_missing_count"] == 0
        and all(summary[key] == 0 for key in FAILURE_COUNT_KEYS)
        and all(evaluation["checkpoint_contract_compatibility"].values())
    )


def _run_task(
    task_id: str,
    *,
    protocol: dict[str, Any],
    artifact_root: Path,
    total_timesteps: int,
    episodes: int,
    parallel_environments: int,
) -> dict[str, Any]:
    task = get_task(task_id)
    training = RLWorldAllocation.from_protocol(protocol, task_id=task_id, name="train")
    development = RLWorldAllocation.from_protocol(protocol, task_id=task_id, name="dev")
    checkpoints = _checkpoint_steps(total_timesteps, parallel_environments)
    task_root = artifact_root / f"steps-{total_timesteps}" / task_id
    manifest = train_sb3_baseline(
        algorithm="ppo",
        task_id=task_id,
        allocation=training,
        total_timesteps=total_timesteps,
        model_seed=0,
        output_dir=task_root,
        algorithm_kwargs={
            "learning_rate": 3.0e-4,
            "n_steps": 128,
            "batch_size": 64,
            "gamma": 0.99,
            "gae_lambda": 0.95,
            "ent_coef": 0.01,
        },
        operation_budget=task.budget,
        checkpoint_steps=checkpoints,
        parallel_environments=parallel_environments,
        vectorization_backend="dummy",
        device="cpu",
        torch_num_threads=1,
        progress_interval_steps=max(128, total_timesteps // 4),
    )
    training_diagnostics = manifest["training_diagnostics"]
    training_gates = {
        "exact_training_step_budget": manifest["step_budget_exact"] is True,
        "completed_experiment_observed": (training_diagnostics["completed_experiment_count"] > 0),
        "behavior_complete_experiment_observed": (
            training_diagnostics["behavior_complete_experiment_count"] > 0
        ),
        "execution_failure_counts_retained": all(
            key in training_diagnostics for key in FAILURE_COUNT_KEYS
        ),
        "zero_execution_failures": all(
            training_diagnostics[key] == 0 for key in FAILURE_COUNT_KEYS
        ),
    }
    evaluations: list[dict[str, Any]] = []
    for checkpoint_step in checkpoints:
        checkpoint = task_root / "checkpoints" / f"ppo-{task_id}-seed0_{checkpoint_step}_steps.zip"
        for deterministic in (True, False):
            evaluation = evaluate_sb3_checkpoint(
                algorithm="ppo",
                checkpoint=checkpoint,
                task_id=task_id,
                allocation=development,
                episodes=episodes,
                operation_budget=task.budget,
                sampler_seed=41_000 + checkpoint_step,
                policy_seed=51_000 + checkpoint_step,
                deterministic=deterministic,
                primary_metric=PRIMARY_METRICS[task_id],
            )
            evaluation["summary"]["clean_behavior_complete_episode_count"] = (
                _clean_behavior_complete_episode_count(evaluation)
            )
            evaluations.append(
                {
                    "checkpoint_step": checkpoint_step,
                    "policy_mode": evaluation["policy_mode"],
                    "summary": evaluation["summary"],
                    "checkpoint_contract_compatibility": evaluation[
                        "checkpoint_contract_compatibility"
                    ],
                    "gates": _evaluation_gates(evaluation),
                    "formal_candidate_ready": _formal_candidate_ready(evaluation),
                }
            )
    eligible = [item for item in evaluations if _candidate_is_clean_and_complete(item)]
    selected = max(eligible or evaluations, key=_candidate_key)
    task_gates = {
        "training_contract_ready": bool(
            training_gates["exact_training_step_budget"]
            and training_gates["completed_experiment_observed"]
            and training_gates["execution_failure_counts_retained"]
        ),
        "training_behavior_learning_signal": training_gates[
            "behavior_complete_experiment_observed"
        ],
        "all_checkpoint_contracts_exact": all(
            item["gates"]["checkpoint_contract_exact"] for item in evaluations
        ),
        "at_least_one_clean_behavior_complete_checkpoint": bool(eligible),
    }
    return {
        "task_id": task_id,
        "primary_metric": PRIMARY_METRICS[task_id],
        "task_contract_hash": task.contract_hash,
        "training_manifest": str(
            (task_root / f"ppo-{task_id}-seed0.manifest.json").relative_to(ROOT)
        ).replace("\\", "/"),
        "training_diagnostics": training_diagnostics,
        "training_gates": training_gates,
        "evaluations": evaluations,
        "selected_development_checkpoint": selected,
        "gates": task_gates,
        "smoke_ready": all(task_gates.values()),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--task",
        choices=("all", *FLAGSHIP_TASK_IDS),
        default="all",
    )
    parser.add_argument("--timesteps", type=int, default=4096)
    parser.add_argument("--episodes", type=int, default=8)
    parser.add_argument("--parallel-environments", type=int, default=4)
    parser.add_argument("--artifact-root", type=Path, default=DEFAULT_ARTIFACT_ROOT)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    args = parser.parse_args()
    if args.episodes <= 0 or args.parallel_environments <= 0:
        raise SystemExit("episodes and parallel environments must be positive")
    rollout_size = 128 * args.parallel_environments
    if args.timesteps < rollout_size or args.timesteps % rollout_size:
        raise SystemExit("timesteps must be positive and divisible by 128 * parallel environments")

    protocol = load_rl_protocol(ALLOCATION_PROTOCOL)
    task_ids = FLAGSHIP_TASK_IDS if args.task == "all" else (args.task,)
    tasks = {
        task_id: _run_task(
            task_id,
            protocol=protocol,
            artifact_root=args.artifact_root.resolve(),
            total_timesteps=args.timesteps,
            episodes=args.episodes,
            parallel_environments=args.parallel_environments,
        )
        for task_id in task_ids
    }
    report = {
        "schema_version": REPORT_VERSION,
        "status": (
            "smoke_ready" if all(item["smoke_ready"] for item in tasks.values()) else "smoke_failed"
        ),
        "algorithm": "ppo",
        "formal_evidence": False,
        "benchmark_claim_allowed": False,
        "task_ids": list(task_ids),
        "training_environment_steps_per_task": args.timesteps,
        "development_episodes_per_checkpoint_mode": args.episodes,
        "parallel_environments": args.parallel_environments,
        "tasks": tasks,
        "all_tasks_smoke_ready": all(item["smoke_ready"] for item in tasks.values()),
        "claim_boundary": (
            "Bounded Train/Dev implementation and sample-efficiency smoke test only; "
            "it does not replace the preregistered multi-seed matrix or permit a method ranking."
        ),
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "status": report["status"],
                "report": str(args.report),
                "tasks": {
                    task_id: {
                        "smoke_ready": item["smoke_ready"],
                        "training_behavior_complete": item["training_diagnostics"][
                            "behavior_complete_experiment_count"
                        ],
                        "selected_checkpoint": item["selected_development_checkpoint"],
                    }
                    for task_id, item in tasks.items()
                },
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
