"""Run the repaired-source 100k SAC development stage with checkpoint provenance."""

from __future__ import annotations

import argparse
import hashlib
import json
import statistics
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Literal

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

PROTOCOL_PATH = ROOT / "configs/benchmark/rl_100k_development.json"
RL_PROTOCOL_PATH = ROOT / "configs/benchmark/rl_baselines_vnext.json"
FREEZE_PATH = ROOT / "configs/benchmark/confirmatory_freeze_vnext.json"


def load_100k_protocol(path: str | Path = PROTOCOL_PATH) -> dict[str, Any]:
    protocol = load_rl_protocol(path)
    if protocol.get("schema_version") != "chemworld-rl-100k-development-0.1":
        raise ValueError("unsupported RL 100k development protocol")
    if protocol.get("benchmark_claim_allowed") is not False:
        raise ValueError("RL 100k development must remain nonclaiming")
    if protocol.get("algorithm") != "sac":
        raise ValueError("RL 100k development is frozen to SAC")
    if protocol["training"]["allocation"] != "train":
        raise ValueError("RL 100k training must use Train")
    if protocol["final_dev"]["allocation"] != "dev":
        raise ValueError("RL 100k selection must use Dev")
    if protocol["standard_replay"].get("world_family_allocation") is not None:
        raise ValueError("standard replay cannot claim world-family allocation")
    checkpoints = protocol["learning_curve_dev"]["checkpoint_steps"]
    requested = int(protocol["training"]["requested_environment_steps"])
    if checkpoints[-1] != requested or checkpoints != sorted(set(checkpoints)):
        raise ValueError("learning-curve checkpoints must be unique and end at 100k")
    return protocol


def run_100k_development(
    *,
    protocol: dict[str, Any],
    output_dir: str | Path,
    source_commit: str,
) -> dict[str, Any]:
    _validate_prerequisites(protocol)
    task_id = str(protocol["task_id"])
    algorithm: Literal["sac"] = "sac"
    training = protocol["training"]
    rl_protocol = load_rl_protocol(RL_PROTOCOL_PATH)
    freeze = load_rl_protocol(FREEZE_PATH)
    train_allocation = RLWorldAllocation.from_protocol(
        freeze, task_id=task_id, name="train"
    )
    dev_allocation = RLWorldAllocation.from_protocol(
        freeze, task_id=task_id, name="dev"
    )
    root = Path(output_dir)
    kwargs = dict(rl_protocol["algorithms"][algorithm]["hyperparameters"])
    kwargs.update(training["hyperparameter_overrides"])
    manifest = train_sb3_baseline(
        algorithm=algorithm,
        task_id=task_id,
        allocation=train_allocation,
        total_timesteps=int(training["requested_environment_steps"]),
        model_seed=int(training["model_seed"]),
        output_dir=root,
        algorithm_kwargs=kwargs,
        operation_budget=int(training["operation_budget"]),
        checkpoint_interval_steps=int(training["checkpoint_interval_steps"]),
        save_replay_buffer=bool(training["save_replay_buffer"]),
    )
    if training["actual_environment_steps_must_equal_requested"] and not manifest[
        "step_budget_exact"
    ]:
        raise RuntimeError("100k training exceeded its requested environment-step budget")
    final_checkpoint = root / str(manifest["checkpoint"])
    final_manifest = final_checkpoint.with_suffix(".manifest.json")
    curve_spec = protocol["learning_curve_dev"]
    curve: list[dict[str, Any]] = []
    for step in curve_spec["checkpoint_steps"]:
        checkpoint = _periodic_checkpoint(root, int(step))
        evaluation = evaluate_sb3_checkpoint(
            algorithm="sac",
            checkpoint=checkpoint,
            task_id=task_id,
            allocation=dev_allocation,
            episodes=int(curve_spec["episodes_per_checkpoint"]),
            operation_budget=int(curve_spec["operation_budget"]),
            sampler_seed=int(curve_spec["sampler_seed"]),
            policy_seed=int(curve_spec["policy_seed"]),
            deterministic=False,
        )
        curve.append(
            {
                "training_environment_steps": int(step),
                "checkpoint_sha256": _sha256(checkpoint),
                "summary": evaluation["summary"],
            }
        )
    final_spec = protocol["final_dev"]
    final_dev = evaluate_sb3_checkpoint(
        algorithm="sac",
        checkpoint=final_checkpoint,
        task_id=task_id,
        allocation=dev_allocation,
        episodes=int(final_spec["episodes"]),
        operation_budget=int(final_spec["operation_budget"]),
        sampler_seed=int(final_spec["sampler_seed"]),
        policy_seed=int(final_spec["policy_seed"]),
        deterministic=False,
    )
    replay_spec = protocol["standard_replay"]
    replay = evaluate_replay_verified_sb3_checkpoint(
        algorithm="sac",
        checkpoint=final_checkpoint,
        checkpoint_manifest=final_manifest,
        task_id=task_id,
        seeds=[int(seed) for seed in replay_spec["seeds"]],
        operation_budget=int(replay_spec["operation_budget"]),
        output_dir=root / "standard-replay",
        policy_seed=int(replay_spec["policy_seed_base"]),
        deterministic=False,
    )
    replay_summary = _summarize_replay(replay)
    gate = _evidence_gate(
        final_dev["summary"],
        replay_summary,
        protocol["evidence_gate"],
    )
    return {
        "schema_version": "chemworld-rl-100k-development-report-0.1",
        "status": "development_complete",
        "generated_at": datetime.now(UTC).isoformat(),
        "protocol_id": protocol["protocol_id"],
        "protocol_sha256": _canonical_sha256(protocol),
        "evaluated_source_commit": source_commit,
        "evaluation_source_tree_dirty": False,
        "task_id": task_id,
        "algorithm": algorithm,
        "training_manifest": manifest,
        "learning_curve_dev": curve,
        "final_world_family_dev": final_dev,
        "standard_replay": replay_summary,
        "evidence_gate": gate,
        "eligible_for_multiseed_development": all(gate.values()),
        "benchmark_claim_allowed": False,
        "publication_ready": False,
        "formal_training_complete": False,
        "formal_bench_evaluation_complete": False,
        "claim_boundary": protocol["claim_boundary"],
    }


def _validate_prerequisites(protocol: dict[str, Any]) -> None:
    selection = load_rl_protocol(ROOT / str(protocol["selection_source"]))
    if "sac" not in selection.get("eligible_algorithms_for_100k", []):
        raise ValueError("SAC did not pass the frozen 20k escalation gate")
    repair = load_rl_protocol(ROOT / str(protocol["required_backend_repair_audit"]))
    if repair.get("status") != "passed" or repair.get("checks", {}).get(
        "post_fix_observation_domain_failures_zero"
    ) is not True:
        raise ValueError("precipitation boundary repair audit has not passed")


def _periodic_checkpoint(root: Path, step: int) -> Path:
    matches = sorted((root / "checkpoints").glob(f"*_{step}_steps.zip"))
    if len(matches) != 1:
        raise RuntimeError(f"expected one checkpoint at {step} steps, found {len(matches)}")
    return matches[0]


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


def _evidence_gate(
    dev: dict[str, Any],
    replay: dict[str, Any],
    spec: dict[str, Any],
) -> dict[str, bool]:
    domain_failures = int(dev["runtime_domain_failure_count"]) + int(
        dev["observation_domain_failure_count"]
    )
    return {
        "final_dev_completion": float(dev["episode_completion_rate"])
        >= float(spec["final_dev_minimum_episode_completion_rate"]),
        "final_dev_validity": float(dev["invalid_action_rate"])
        <= float(spec["final_dev_maximum_invalid_action_rate"]),
        "final_dev_domain_stability": domain_failures
        <= int(spec["final_dev_maximum_domain_failure_count"]),
        "standard_replay_integrity": replay["all_replay_verified"] is True,
        "standard_replay_completion": float(replay["episode_completion_rate"])
        >= float(spec["standard_replay_minimum_episode_completion_rate"]),
        "standard_replay_validity": float(replay["invalid_action_rate"])
        <= float(spec["standard_replay_maximum_invalid_action_rate"]),
        "standard_replay_score": float(
            replay["mean_final_best_score_including_failures"]
        )
        >= float(spec["standard_replay_minimum_mean_final_best_score_including_failures"]),
    }


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
        "--output-dir", type=Path, default=Path("runs/rl-100k-development-0.1")
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("workstreams/benchmark_v1/reports/rl-100k-development.json"),
    )
    args = parser.parse_args()
    source_commit = git_commit()
    if source_commit is None or _tracked_tree_dirty():
        raise RuntimeError("RL 100k development requires a clean committed source tree")
    report = run_100k_development(
        protocol=load_100k_protocol(),
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
                "eligible_for_multiseed_development": report[
                    "eligible_for_multiseed_development"
                ],
                "evidence_gate": report["evidence_gate"],
                "report": str(args.report),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
