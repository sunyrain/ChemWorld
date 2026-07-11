"""Train and evaluate the frozen nonclaiming RL interaction development slice."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from chemworld.data.submission import git_commit  # noqa: E402
from chemworld.rl.environment import (  # noqa: E402
    RLWorldAllocation,
    load_rl_protocol,
)
from chemworld.rl.evaluation import evaluate_sb3_checkpoint  # noqa: E402
from chemworld.rl.training import train_sb3_baseline  # noqa: E402

DEVELOPMENT_PROTOCOL = ROOT / "configs/benchmark/rl_interaction_development.json"
RL_PROTOCOL = ROOT / "configs/benchmark/rl_baselines_vnext.json"
FREEZE_PROTOCOL = ROOT / "configs/benchmark/confirmatory_freeze_vnext.json"


def load_development_protocol(path: str | Path = DEVELOPMENT_PROTOCOL) -> dict[str, Any]:
    protocol = load_rl_protocol(path)
    if protocol.get("schema_version") != "chemworld-rl-interaction-development-0.1":
        raise ValueError("unsupported RL interaction development protocol")
    if protocol.get("benchmark_claim_allowed") is not False:
        raise ValueError("RL interaction development protocol must remain nonclaiming")
    if protocol["training"]["allocation"] != "train":
        raise ValueError("RL development training must use Train")
    if protocol["evaluation"]["allocation"] != "dev":
        raise ValueError("RL development evaluation must use Dev")
    return protocol


def run_development(
    *,
    output_dir: str | Path,
    protocol: dict[str, Any],
    source_commit: str,
) -> dict[str, Any]:
    task_id = str(protocol["task_id"])
    training = protocol["training"]
    evaluation = protocol["evaluation"]
    rl_protocol = load_rl_protocol(RL_PROTOCOL)
    freeze = load_rl_protocol(FREEZE_PROTOCOL)
    train_allocation = RLWorldAllocation.from_protocol(
        freeze, task_id=task_id, name="train"
    )
    dev_allocation = RLWorldAllocation.from_protocol(freeze, task_id=task_id, name="dev")
    root = Path(output_dir)
    algorithm_cards: dict[str, Any] = {}
    gate = protocol["development_gate"]
    for algorithm in protocol["algorithms"]:
        kwargs = dict(rl_protocol["algorithms"][algorithm]["hyperparameters"])
        timesteps = int(training["timesteps"])
        if algorithm == "ppo" and timesteps <= int(kwargs["n_steps"]):
            kwargs.update({"n_steps": max(timesteps, 8), "batch_size": 8})
        if algorithm == "sac":
            kwargs.update(
                {
                    "learning_starts": min(8, max(timesteps - 1, 0)),
                    "batch_size": 8,
                }
            )
        algorithm_dir = root / algorithm
        manifest = train_sb3_baseline(
            algorithm=algorithm,
            task_id=task_id,
            allocation=train_allocation,
            total_timesteps=timesteps,
            model_seed=int(training["model_seed"]),
            output_dir=algorithm_dir,
            algorithm_kwargs=kwargs,
            operation_budget=int(training["operation_budget"]),
        )
        checkpoint = algorithm_dir / str(manifest["checkpoint"])
        primary = evaluate_sb3_checkpoint(
            algorithm=algorithm,
            checkpoint=checkpoint,
            task_id=task_id,
            allocation=dev_allocation,
            episodes=int(evaluation["episodes"]),
            operation_budget=int(evaluation["operation_budget"]),
            sampler_seed=int(evaluation["sampler_seed"]),
            policy_seed=int(evaluation["policy_seed"]),
            deterministic=False,
        )
        deterministic = evaluate_sb3_checkpoint(
            algorithm=algorithm,
            checkpoint=checkpoint,
            task_id=task_id,
            allocation=dev_allocation,
            episodes=int(evaluation["episodes"]),
            operation_budget=int(evaluation["operation_budget"]),
            sampler_seed=int(evaluation["sampler_seed"]),
            policy_seed=int(evaluation["policy_seed"]),
            deterministic=True,
        )
        summary = primary["summary"]
        eligible = development_gate_passed(summary, gate=gate)
        algorithm_cards[str(algorithm)] = {
            "training_manifest": manifest,
            "checkpoint_path": str(checkpoint.relative_to(root)),
            "checkpoint_sha256": _sha256(checkpoint),
            "stochastic_dev_evaluation": primary,
            "deterministic_dev_diagnostic": deterministic,
            "eligible_for_larger_train_dev_scaling": eligible,
        }
    eligible_algorithms = [
        algorithm
        for algorithm, card in algorithm_cards.items()
        if card["eligible_for_larger_train_dev_scaling"]
    ]
    return {
        "schema_version": "chemworld-rl-interaction-development-report-0.1",
        "status": "development_complete",
        "generated_at": datetime.now(UTC).isoformat(),
        "protocol_id": protocol["protocol_id"],
        "protocol_sha256": _canonical_sha256(protocol),
        "evaluated_source_commit": source_commit,
        "evaluation_source_tree_dirty": False,
        "task_id": task_id,
        "algorithm_cards": algorithm_cards,
        "eligible_algorithms": eligible_algorithms,
        "at_least_one_algorithm_eligible": bool(eligible_algorithms),
        "all_algorithms_eligible": len(eligible_algorithms) == len(algorithm_cards),
        "benchmark_claim_allowed": False,
        "publication_ready": False,
        "formal_training_complete": False,
        "formal_bench_evaluation_complete": False,
        "interpretation": (
            "This Train/Dev slice can select an interaction contract for larger scaling. "
            "It has no replay-verified Bench trajectories and cannot support an RL ranking."
        ),
    }


def development_gate_passed(
    summary: dict[str, Any], *, gate: dict[str, Any]
) -> bool:
    return bool(
        float(summary["invalid_action_rate"])
        <= float(gate["maximum_invalid_action_rate"])
        and float(summary["episode_completion_rate"])
        >= float(gate["minimum_episode_completion_rate"])
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("runs/rl-interaction-development-0.1"),
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("workstreams/benchmark_v1/reports/rl-interaction-development.json"),
    )
    args = parser.parse_args()
    protocol = load_development_protocol()
    source_commit = git_commit()
    if source_commit is None:
        raise RuntimeError("RL development requires a Git commit")
    if _tracked_tree_dirty():
        raise RuntimeError("RL development requires a clean tracked tree")
    report = run_development(
        output_dir=args.output_dir,
        protocol=protocol,
        source_commit=source_commit,
    )
    _write_json(args.report, report)
    print(
        json.dumps(
            {
                "eligible_algorithms": report["eligible_algorithms"],
                "all_algorithms_eligible": report["all_algorithms_eligible"],
                "benchmark_claim_allowed": report["benchmark_claim_allowed"],
                "report": str(args.report),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


def _tracked_tree_dirty() -> bool:
    completed = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=no"],
        check=True,
        capture_output=True,
        text=True,
    )
    return bool(completed.stdout.strip())


def _canonical_sha256(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return hashlib.sha256(encoded.encode()).hexdigest()


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
