"""Offline host adapter for a writable notebook and a read-only experiment record.

The host owns this object and exposes only read_notebook/write_notebook to an agent.
This API separation is not an OS sandbox for arbitrary code running on the same host.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, cast

import gymnasium as gym

import chemworld  # noqa: F401
from chemworld.agents.experiment_documents import ExperimentDocumentWorkspace
from chemworld.data.logging import TrajectoryLogger, load_jsonl, observation_to_json
from chemworld.envs.chemworld_env import ChemWorldEnv
from chemworld.eval.verify import verify_records


def run(output: Path) -> dict[str, Any]:
    output.mkdir(parents=True, exist_ok=False)
    documents = ExperimentDocumentWorkspace(output)
    documents.initialize()
    documents.write_notebook(
        "# Research notebook\n\n"
        "## Question and hypothesis\nCan an assay distinguish material from an empty vessel?\n\n"
        "## Prediction before execution\nAn empty-vessel HPLC should be rejected.\n\n"
        "## Fixed design\nAttempt HPLC, charge solvent and reagent, HPLC, terminate, final assay.\n"
    )
    actions: list[dict[str, Any]] = [
        {"operation": "measure", "instrument": "hplc"},
        {"operation": "add_solvent", "volume_L": 0.025, "solvent": 0},
        {"operation": "add_reagent", "amount_mol": 0.012},
        {"operation": "measure", "instrument": "hplc"},
        {"operation": "terminate"},
        {"operation": "measure", "instrument": "final_assay"},
    ]
    env = gym.make(
        "ChemWorld", task_id="reaction-to-assay", seed=0, episode_mode_override="single_experiment"
    )
    try:
        env.reset(seed=0)
        core = cast(ChemWorldEnv, env.unwrapped)
        task_info = {**core.task_info(), **core.evaluator_provenance()}
        with TrajectoryLogger(output / "trajectory.jsonl") as logger:
            for step, action in enumerate(actions, 1):
                observation, reward, terminated, truncated, info = env.step(action)
                logger.log(
                    task_info=task_info,
                    step=step,
                    action=action,
                    observation=observation,
                    reward=float(reward),
                    terminated=terminated,
                    truncated=truncated,
                    info=info,
                    agent_metadata={"agent_id": "offline-document-example"},
                )
                documents.append_operation(
                    {
                        "event_id": f"operation-{step:04d}",
                        "action": action,
                        "transaction_status": info["transaction_status"],
                        "observation": observation_to_json(observation),
                        "trajectory_reference": {"path": "trajectory.jsonl", "step": step},
                    }
                )
        before = documents.manifest()["authoritative_ledger"]
        documents.write_notebook(
            documents.read_notebook() + "\n## Observation and evidence\n"
            "operation-0001 was rejected; operation-0006 completed "
            "the final assay. See trajectory.jsonl at those steps.\n\n"
            "## Interpretation and uncertainty\nThis tests the lifecycle, not a chemical law.\n\n"
            "## Next step\nChoose a scientific question before starting another batch.\n"
        )
        assert documents.manifest()["authoritative_ledger"] == before
        records = load_jsonl(output / "trajectory.jsonl")
        summary = {
            "formal_result": False,
            "operation_count": len(records),
            "committed_count": sum(r["transaction_status"] == "committed" for r in records),
            "failed_count": sum(r["transaction_status"] != "committed" for r in records),
            "final_assay": records[-1]["instrument"] == "final_assay" and records[-1]["terminated"],
            "replay": verify_records(records, tolerance=0.0).to_dict(),
            "documents": documents.manifest(),
        }
        (output / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
        return summary
    finally:
        env.close()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.output), indent=2))


if __name__ == "__main__":
    main()
