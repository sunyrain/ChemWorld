"""Capture the fixed eight-action development example through public frames only."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import gymnasium as gym

import chemworld  # noqa: F401
from chemworld.data.logging import TrajectoryLogger
from chemworld.interfaces.blender import BlenderObserver

ROOT = Path(__file__).resolve().parent
ACTIONS = [
    {"operation": "add_solvent", "volume_L": 0.03, "solvent": 0},
    {"operation": "add_reagent", "amount_mol": 0.01},
    {"operation": "add_catalyst", "catalyst_amount_mol": 0.00025, "catalyst": 1},
    {
        "operation": "heat",
        "target_temperature_K": 370.0,
        "duration_s": 300.0,
        "stirring_speed_rpm": 400.0,
    },
    {"operation": "sample", "sample_volume_L": 0.0005},
    {"operation": "measure", "instrument": "uvvis"},
    {"operation": "terminate"},
    {"operation": "measure", "instrument": "final_assay"},
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--trajectory", type=Path, required=True)
    args = parser.parse_args()
    if args.trajectory.exists():
        parser.error("Preserve the original trajectory; select a new output path")
    frames = []
    env = BlenderObserver(
        gym.make("ChemWorld", task_id="reaction-to-assay", seed=7), sink=frames.append
    )
    statuses = []
    try:
        env.reset(seed=7)
        base = env.unwrapped
        with TrajectoryLogger(args.trajectory) as logger:
            for index, action in enumerate(ACTIONS, 1):
                observation, reward, terminated, truncated, info = env.step(action)
                logger.log(
                    task_info={**base.task_info(), **base.evaluator_provenance()},
                    step=index,
                    action=action,
                    observation=observation,
                    reward=reward,
                    terminated=terminated,
                    truncated=truncated,
                    info=info,
                    agent_metadata={"agent_id": "explorer-demo", "development_only": True},
                )
                statuses.append(info.get("transaction_status"))
                print(f"Public demo {index}/8: {action['operation']} / {statuses[-1]}", flush=True)
                if statuses[-1] != "committed":
                    raise RuntimeError("Core failure preserved in trajectory")
        for frame in frames:
            frame["session_id"] = "recorded-development-example"
        payload = {
            "source": "recorded_core_development",
            "research_evidence": False,
            "title": "从配液到终检",
            "frames": frames,
            "actions": ACTIONS,
            "scheduled": 8,
            "completed": len(statuses),
            "statuses": statuses,
        }
        (ROOT / "static/demo.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        print(f"Completed 8/8; public frames {len(frames)}; ETA 0s", flush=True)
    finally:
        env.close()


if __name__ == "__main__":
    main()
