"""Development integration demo: Core experiment, explicit carrier transport, exact replay log."""

from __future__ import annotations

import argparse
import time
import uuid
from pathlib import Path
from typing import Any

import gymnasium as gym

import chemworld  # noqa: F401
from chemworld.data.logging import TrajectoryLogger
from chemworld.interfaces.blender import BlenderClient, BlenderObserver


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--blender-url", default="http://127.0.0.1:8877")
    parser.add_argument("--skip-transport", action="store_true")
    parser.add_argument("--pause", type=float, default=1)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    path = args.output or Path("runs/blender_lab") / uuid.uuid4().hex / "trajectory.jsonl"
    if path.exists():
        parser.error("--output already exists; choose a new trajectory path")
    client = BlenderClient(args.blender_url)
    env = BlenderObserver(gym.make("ChemWorld", task_id="reaction-to-assay", seed=7), client=client)
    actions = [
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
    try:
        env.reset(seed=7)
        base: Any = env.unwrapped
        task_info = {**base.task_info(), **base.evaluator_provenance()}
        with TrajectoryLogger(path) as logger:
            for index, action in enumerate(actions, 1):
                observation, reward, terminated, truncated, info = env.step(action)
                logger.log(
                    task_info=task_info,
                    step=index,
                    action=action,
                    observation=observation,
                    reward=reward,
                    terminated=terminated,
                    truncated=truncated,
                    info=info,
                    agent_metadata={
                        "agent_id": "blender-integration-demo",
                        "development_only": True,
                    },
                )
                print(
                    f"Core {index}/{len(actions)}: {action['operation']}"
                    f" / {info.get('transaction_status')}",
                    flush=True,
                )
                if env.projection_error:
                    raise RuntimeError(
                        "Core step was executed and logged; presentation failed: "
                        + env.projection_error
                    )
                if info.get("transaction_status") != "committed":
                    raise RuntimeError(f"Core operation failed; original result kept in {path}")
                if action["operation"] == "sample" and not args.skip_transport:
                    task = client.transport()
                    print("Demonstration carrier moving; Core experiment is waiting", flush=True)
                    deadline = time.monotonic() + 180
                    while time.monotonic() < deadline:
                        result = client.request("/api/v1/environment/tasks/" + task["id"])
                        print(f"Logistics: {result['status']} {result['step_index']}/5", flush=True)
                        if result["status"] in {"succeeded", "failed", "cancelled", "interrupted"}:
                            if result["status"] != "succeeded":
                                raise RuntimeError(f"Logistics stopped: {result}")
                            break
                        time.sleep(5)
                    else:
                        raise TimeoutError(
                            f"Logistics outcome unknown; query task {task['id']} before retrying"
                        )
                time.sleep(max(0, args.pause))
                if terminated or truncated:
                    break
        print(f"Trajectory: {path}", flush=True)
    finally:
        env.close()


if __name__ == "__main__":
    main()
