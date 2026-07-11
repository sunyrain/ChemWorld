"""Run the preregistered 20k RL screening stage without Bench access."""

from __future__ import annotations

import argparse
import hashlib
import json
import statistics
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
from chemworld.rl.evaluation import (  # noqa: E402
    evaluate_replay_verified_sb3_checkpoint,
    evaluate_sb3_checkpoint,
)
from chemworld.rl.training import train_sb3_baseline  # noqa: E402

PROTOCOL_PATH = ROOT / "configs/benchmark/rl_staged_development.json"
RL_PROTOCOL_PATH = ROOT / "configs/benchmark/rl_baselines_vnext.json"
FREEZE_PATH = ROOT / "configs/benchmark/confirmatory_freeze_vnext.json"


def load_staged_protocol(path: str | Path = PROTOCOL_PATH) -> dict[str, Any]:
    payload = load_rl_protocol(path)
    if payload.get("schema_version") != "chemworld-rl-staged-development-0.1":
        raise ValueError("unsupported staged RL development protocol")
    if payload.get("benchmark_claim_allowed") is not False:
        raise ValueError("staged RL development must remain nonclaiming")
    if payload["training"]["allocation"] != "train":
        raise ValueError("staged RL training must use Train")
    if payload["world_family_dev_evaluation"]["allocation"] != "dev":
        raise ValueError("staged RL selection must use Dev")
    if payload["replay_evaluation"].get("world_family_allocation") is not None:
        raise ValueError("standard replay evaluation cannot claim world-family cells")
    return payload


def run_staged_development(
    *,
    protocol: dict[str, Any],
    output_dir: str | Path,
    source_commit: str,
) -> dict[str, Any]:
    task_id = str(protocol["task_id"])
    training = protocol["training"]
    dev_spec = protocol["world_family_dev_evaluation"]
    replay_spec = protocol["replay_evaluation"]
    rl_protocol = load_rl_protocol(RL_PROTOCOL_PATH)
    freeze = load_rl_protocol(FREEZE_PATH)
    train_allocation = RLWorldAllocation.from_protocol(
        freeze, task_id=task_id, name="train"
    )
    dev_allocation = RLWorldAllocation.from_protocol(
        freeze, task_id=task_id, name="dev"
    )
    root = Path(output_dir)
    cards: dict[str, Any] = {}
    for algorithm in protocol["algorithms"]:
        algorithm_dir = root / str(algorithm)
        kwargs = dict(rl_protocol["algorithms"][algorithm]["hyperparameters"])
        kwargs.update(training["development_overrides"].get(algorithm, {}))
        manifest = train_sb3_baseline(
            algorithm=algorithm,
            task_id=task_id,
            allocation=train_allocation,
            total_timesteps=int(training["timesteps"]),
            model_seed=int(training["model_seed"]),
            output_dir=algorithm_dir,
            algorithm_kwargs=kwargs,
            operation_budget=int(training["operation_budget"]),
        )
        checkpoint = algorithm_dir / str(manifest["checkpoint"])
        checkpoint_manifest = checkpoint.with_suffix(".manifest.json")
        dev = evaluate_sb3_checkpoint(
            algorithm=algorithm,
            checkpoint=checkpoint,
            task_id=task_id,
            allocation=dev_allocation,
            episodes=int(dev_spec["episodes"]),
            operation_budget=int(dev_spec["operation_budget"]),
            sampler_seed=int(dev_spec["sampler_seed"]),
            policy_seed=int(dev_spec["policy_seed"]),
            deterministic=False,
        )
        replay = evaluate_replay_verified_sb3_checkpoint(
            algorithm=algorithm,
            checkpoint=checkpoint,
            checkpoint_manifest=checkpoint_manifest,
            task_id=task_id,
            seeds=[int(seed) for seed in replay_spec["standard_registered_task_seeds"]],
            operation_budget=int(replay_spec["operation_budget"]),
            output_dir=algorithm_dir / "standard-replay",
            policy_seed=int(replay_spec["policy_seed_base"]),
            deterministic=False,
        )
        replay_summary = _summarize_replay(replay)
        gate_passed = _gate_passed(
            dev["summary"], replay_summary, gate=protocol["escalation_gate"]
        )
        cards[str(algorithm)] = {
            "training_manifest": manifest,
            "checkpoint_sha256": _sha256(checkpoint),
            "world_family_dev_evaluation": dev,
            "standard_replay_evaluation": replay_summary,
            "eligible_for_100k_train_dev_scaling": gate_passed,
        }
    eligible = [
        name for name, card in cards.items() if card["eligible_for_100k_train_dev_scaling"]
    ]
    return {
        "schema_version": "chemworld-rl-staged-development-report-0.1",
        "status": "development_complete",
        "generated_at": datetime.now(UTC).isoformat(),
        "protocol_id": protocol["protocol_id"],
        "protocol_sha256": _canonical_sha256(protocol),
        "evaluated_source_commit": source_commit,
        "evaluation_source_tree_dirty": False,
        "task_id": task_id,
        "algorithm_cards": cards,
        "eligible_algorithms_for_100k": eligible,
        "at_least_one_algorithm_eligible": bool(eligible),
        "benchmark_claim_allowed": False,
        "publication_ready": False,
        "formal_training_complete": False,
        "formal_bench_evaluation_complete": False,
        "claim_boundary": protocol["claim_boundary"],
    }


def _summarize_replay(report: dict[str, Any]) -> dict[str, Any]:
    results = list(report["results"])
    scores = [float(item["final_best_score"]) for item in results]
    complete = [int(item["final_assay_count"] > 0) for item in results]
    invalid = [
        int(
            item["score_replay"]["layered_evaluation"]["validity"][
                "invalid_operation_count"
            ]
        )
        for item in results
    ]
    steps = [int(item["steps"]) for item in results]
    return {
        "trajectory_count": len(results),
        "all_replay_verified": bool(report["all_replay_verified"]),
        "episode_completion_rate": sum(complete) / len(complete),
        "complete_experiment_count": sum(int(item["final_assay_count"]) for item in results),
        "invalid_action_rate": sum(invalid) / sum(steps),
        "mean_final_best_score_including_failures": statistics.fmean(scores),
        "final_best_scores": scores,
        "formal_evidence": False,
    }


def _gate_passed(
    dev: dict[str, Any],
    replay: dict[str, Any],
    *,
    gate: dict[str, Any],
) -> bool:
    return bool(
        float(dev["episode_completion_rate"])
        >= float(gate["world_family_dev_minimum_episode_completion_rate"])
        and float(dev["invalid_action_rate"])
        <= float(gate["world_family_dev_maximum_invalid_action_rate"])
        and replay["all_replay_verified"] is True
        and float(replay["episode_completion_rate"])
        >= float(gate["standard_replay_minimum_episode_completion_rate"])
        and float(replay["invalid_action_rate"])
        <= float(gate["standard_replay_maximum_invalid_action_rate"])
        and float(replay["mean_final_best_score_including_failures"])
        >= float(gate["standard_replay_minimum_mean_final_best_score_including_failures"])
    )


def _canonical_sha256(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return hashlib.sha256(encoded.encode()).hexdigest()


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _tracked_tree_dirty() -> bool:
    completed = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=no"],
        check=True,
        capture_output=True,
        text=True,
    )
    return bool(completed.stdout.strip())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir", type=Path, default=Path("runs/rl-staged-development-0.1")
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("workstreams/benchmark_v1/reports/rl-staged-development.json"),
    )
    args = parser.parse_args()
    source_commit = git_commit()
    if source_commit is None or _tracked_tree_dirty():
        raise RuntimeError("staged RL development requires a clean committed source tree")
    report = run_staged_development(
        protocol=load_staged_protocol(),
        output_dir=args.output_dir,
        source_commit=source_commit,
    )
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "eligible_algorithms_for_100k": report["eligible_algorithms_for_100k"],
                "report": str(args.report),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
