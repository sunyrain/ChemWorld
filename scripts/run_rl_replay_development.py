"""Generate replay-verified development trajectories for frozen PPO/SAC policies."""

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
from chemworld.rl.evaluation import (  # noqa: E402
    evaluate_replay_verified_sb3_checkpoint,
)

PROTOCOL_PATH = ROOT / "configs/benchmark/rl_replay_development.json"


def load_protocol(path: str | Path = PROTOCOL_PATH) -> dict[str, Any]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if payload.get("schema_version") != "chemworld-rl-replay-development-0.1":
        raise ValueError("unsupported RL replay development protocol")
    if payload.get("benchmark_claim_allowed") is not False:
        raise ValueError("RL replay development must remain nonclaiming")
    evaluation = payload["evaluation"]
    if evaluation.get("world_family_allocation") is not None:
        raise ValueError("standard replay development cannot claim a world-family allocation")
    seeds = evaluation.get("seeds", [])
    if not seeds or len(set(seeds)) != len(seeds):
        raise ValueError("RL replay development seeds must be non-empty and unique")
    return payload


def run_protocol(
    *,
    protocol: dict[str, Any],
    output_dir: str | Path,
    source_commit: str,
) -> dict[str, Any]:
    task_id = str(protocol["task_id"])
    evaluation = protocol["evaluation"]
    root = Path(output_dir)
    algorithms: dict[str, Any] = {}
    for algorithm, paths in protocol["algorithms"].items():
        checkpoint = ROOT / str(paths["checkpoint"])
        manifest = ROOT / str(paths["manifest"])
        result = evaluate_replay_verified_sb3_checkpoint(
            algorithm=algorithm,
            checkpoint=checkpoint,
            checkpoint_manifest=manifest,
            task_id=task_id,
            seeds=[int(seed) for seed in evaluation["seeds"]],
            operation_budget=int(evaluation["operation_budget"]),
            output_dir=root / algorithm,
            policy_seed=int(evaluation["policy_seed_base"]),
            deterministic=False,
        )
        algorithms[str(algorithm)] = _summarize(result, checkpoint=checkpoint)
    return {
        "schema_version": "chemworld-rl-replay-development-report-0.1",
        "status": "development_complete",
        "generated_at": datetime.now(UTC).isoformat(),
        "protocol_id": protocol["protocol_id"],
        "protocol_sha256": _canonical_sha256(protocol),
        "evaluated_source_commit": source_commit,
        "evaluation_source_tree_dirty": False,
        "task_id": task_id,
        "algorithms": algorithms,
        "trajectory_count": sum(card["trajectory_count"] for card in algorithms.values()),
        "all_replay_verified": all(card["all_replay_verified"] for card in algorithms.values()),
        "benchmark_claim_allowed": False,
        "publication_ready": False,
        "formal_training_complete": False,
        "formal_bench_evaluation_complete": False,
        "claim_boundary": protocol["claim_boundary"],
        "interpretation": (
            "The official checkpoint-to-trajectory bridge works, but these 2048-step "
            "policies remain weak and the standard-seed runs are not a world-family result."
        ),
    }


def _summarize(report: dict[str, Any], *, checkpoint: Path) -> dict[str, Any]:
    results = list(report["results"])
    final_scores = [float(item["final_best_score"]) for item in results]
    completed = [int(item["final_assay_count"] > 0) for item in results]
    invalid_counts = [
        int(
            item["score_replay"]["layered_evaluation"]["validity"][
                "invalid_operation_count"
            ]
        )
        for item in results
    ]
    steps = [int(item["steps"]) for item in results]
    return {
        "checkpoint_sha256": hashlib.sha256(checkpoint.read_bytes()).hexdigest(),
        "trajectory_count": len(results),
        "all_replay_verified": bool(report["all_replay_verified"]),
        "completed_run_count": sum(completed),
        "episode_completion_rate": sum(completed) / len(completed),
        "complete_experiment_count": sum(int(item["final_assay_count"]) for item in results),
        "mean_final_best_score_including_failures": statistics.fmean(final_scores),
        "final_best_scores": final_scores,
        "invalid_operation_rate": sum(invalid_counts) / sum(steps),
        "operation_count": sum(steps),
        "training_environment_step_count": int(
            results[0]["resource_usage"]["training_environment_step_count"]
        ),
        "formal_evidence": False,
    }


def _canonical_sha256(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return hashlib.sha256(encoded.encode()).hexdigest()


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
        "--output-dir",
        type=Path,
        default=Path("runs/rl-replay-development-0.1"),
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("workstreams/benchmark_v1/reports/rl-replay-development.json"),
    )
    args = parser.parse_args()
    source_commit = git_commit()
    if source_commit is None or _tracked_tree_dirty():
        raise RuntimeError("RL replay development requires a clean committed source tree")
    report = run_protocol(
        protocol=load_protocol(),
        output_dir=args.output_dir,
        source_commit=source_commit,
    )
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "all_replay_verified": report["all_replay_verified"],
                "trajectory_count": report["trajectory_count"],
                "report": str(args.report),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
