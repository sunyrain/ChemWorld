"""Audit exact failure causes for trained flagship PPO checkpoints.

The output is development-only diagnostic evidence.  It deliberately reuses
the frozen Dev allocation and does not inspect Bench worlds.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from chemworld.rl.environment import RLWorldAllocation, load_rl_protocol
from chemworld.rl.evaluation import evaluate_sb3_checkpoint
from chemworld.tasks import FLAGSHIP_TASK_IDS, get_task

ROOT = Path(__file__).resolve().parents[1]
ALLOCATION_PROTOCOL = ROOT / "configs/benchmark/confirmatory_freeze_vnext.json"
DEFAULT_ARTIFACT_ROOT = ROOT / "runs/flagship-ppo-smoke-v07"
DEFAULT_REPORT = (
    ROOT / "workstreams/flagship_tasks/reports/flagship-ppo-failure-audit.json"
)
PRIMARY_METRICS = {
    "reaction-to-crystallization": "crystal_csd_quality",
    "electrochemical-conversion": "faradaic_efficiency",
}


def _failing_episode_cards(evaluation: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            key: card[key]
            for key in (
                "episode_index",
                "operation_count",
                "complete_experiment_count",
                "behavior_complete_experiment_count",
                "transaction_rollback_count",
                "constitution_failure_count",
                "failure_reason_counts",
                "failure_operation_counts",
                "failed_precondition_counts",
                "failed_constitution_check_counts",
            )
        }
        for card in evaluation["episode_cards"]
        if card["failure_reason_counts"]
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint-step", type=int, default=4096)
    parser.add_argument("--training-steps", type=int, default=4096)
    parser.add_argument("--episodes", type=int, default=8)
    parser.add_argument("--allocation", choices=("train", "dev"), default="dev")
    parser.add_argument("--artifact-root", type=Path, default=DEFAULT_ARTIFACT_ROOT)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    args = parser.parse_args()

    protocol = load_rl_protocol(ALLOCATION_PROTOCOL)
    tasks: dict[str, Any] = {}
    for task_id in FLAGSHIP_TASK_IDS:
        allocation = RLWorldAllocation.from_protocol(
            protocol,
            task_id=task_id,
            name=args.allocation,
        )
        checkpoint = (
            args.artifact_root.resolve()
            / f"steps-{args.training_steps}"
            / task_id
            / "checkpoints"
            / f"ppo-{task_id}-seed0_{args.checkpoint_step}_steps.zip"
        )
        evaluation = evaluate_sb3_checkpoint(
            algorithm="ppo",
            checkpoint=checkpoint,
            task_id=task_id,
            allocation=allocation,
            episodes=args.episodes,
            operation_budget=get_task(task_id).budget,
            sampler_seed=41_000 + args.checkpoint_step,
            policy_seed=51_000 + args.checkpoint_step,
            deterministic=False,
            primary_metric=PRIMARY_METRICS[task_id],
        )
        tasks[task_id] = {
            "checkpoint": str(checkpoint.relative_to(ROOT)).replace("\\", "/"),
            "checkpoint_contract_compatibility": evaluation[
                "checkpoint_contract_compatibility"
            ],
            "summary": evaluation["summary"],
            "failing_episode_cards": _failing_episode_cards(evaluation),
        }

    payload = {
        "schema_version": "chemworld-flagship-ppo-failure-audit-0.1",
        "formal_evidence": False,
        "allocation": args.allocation,
        "policy_mode": "stochastic_frozen_seed",
        "checkpoint_step": args.checkpoint_step,
        "episodes_per_task": args.episodes,
        "tasks": tasks,
        "claim_boundary": (
            "Failure diagnosis for a bounded Train/Dev smoke run; not formal benchmark evidence."
        ),
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
