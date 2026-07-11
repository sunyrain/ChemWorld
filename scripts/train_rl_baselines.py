"""Train one diagnostic or frozen-budget PPO/SAC checkpoint."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from chemworld.rl.environment import RLWorldAllocation, load_rl_protocol
from chemworld.rl.training import train_sb3_baseline

ROOT = Path(__file__).resolve().parents[1]
RL_PROTOCOL = ROOT / "configs/benchmark/rl_baselines_vnext.json"
FREEZE_PROTOCOL = ROOT / "configs/benchmark/confirmatory_freeze_vnext.json"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--algorithm", choices=("ppo", "sac"), required=True)
    parser.add_argument("--task", required=True)
    parser.add_argument("--timesteps", type=int, required=True)
    parser.add_argument("--model-seed", type=int, default=0)
    parser.add_argument("--operation-budget", type=int)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "runs/rl")
    args = parser.parse_args()

    rl_protocol = load_rl_protocol(RL_PROTOCOL)
    if args.task not in rl_protocol["core_tasks"]:
        raise SystemExit("task is not in the frozen provisional core")
    freeze_protocol = load_rl_protocol(FREEZE_PROTOCOL)
    allocation = RLWorldAllocation.from_protocol(freeze_protocol, task_id=args.task, name="train")
    kwargs = dict(rl_protocol["algorithms"][args.algorithm]["hyperparameters"])
    if args.timesteps < 2048:
        if args.algorithm == "ppo":
            kwargs.update({"n_steps": max(args.timesteps, 8), "batch_size": 8})
        else:
            kwargs.update({"learning_starts": min(8, max(args.timesteps - 1, 0)), "batch_size": 8})
    manifest = train_sb3_baseline(
        algorithm=args.algorithm,
        task_id=args.task,
        allocation=allocation,
        total_timesteps=args.timesteps,
        model_seed=args.model_seed,
        output_dir=args.output_dir,
        algorithm_kwargs=kwargs,
        operation_budget=args.operation_budget,
    )
    print(json.dumps(manifest, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
