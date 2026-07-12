"""Run the preregistered PPO learning curve and conditional five-seed Dev gate."""

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
from chemworld.rl.environment import RLWorldAllocation, load_rl_protocol  # noqa: E402
from chemworld.rl.evaluation import evaluate_sb3_checkpoint  # noqa: E402
from chemworld.rl.training import train_sb3_baseline  # noqa: E402

PROTOCOL_PATH = ROOT / "configs/foundation/rl_contract_vnext.json"
ALLOCATION_PATH = ROOT / "configs/benchmark/confirmatory_freeze_vnext.json"
REPORT_PATH = ROOT / "workstreams/world_foundation/reports/rl-contract-vnext.json"


def load_protocol(path: str | Path = PROTOCOL_PATH) -> dict[str, Any]:
    protocol = load_rl_protocol(path)
    if protocol.get("schema_version") != "chemworld-foundation-rl-contract-protocol-0.3":
        raise ValueError("unsupported foundation RL contract protocol")
    if protocol.get("benchmark_claim_allowed") is not False:
        raise ValueError("foundation RL learning runs must remain nonclaiming")
    if protocol.get("world_foundation_preconditions", {}).get(
        "formal_training_allowed"
    ) is not True:
        raise RuntimeError(
            "RL training is blocked until shared lite modules, runtime coupling, "
            "maturity truth, and backend freeze all pass"
        )
    gate = protocol["development_gate"]
    seeds = [int(seed) for seed in gate["training_seeds"]]
    checkpoints = [int(step) for step in gate["training_environment_step_checkpoints"]]
    if len(seeds) != 5 or len(set(seeds)) != 5:
        raise ValueError("development gate requires five unique training seeds")
    if seeds[0] != int(gate["preregistered_learning_curve_seed"]):
        raise ValueError("the first training seed must be the preregistered curve seed")
    if checkpoints != sorted(set(checkpoints)) or checkpoints[-1] != int(
        gate["maximum_training_environment_steps"]
    ):
        raise ValueError("learning-curve checkpoints must be unique and end at the maximum")
    if any(step % int(gate["hyperparameters"]["n_steps"]) for step in checkpoints):
        raise ValueError("PPO checkpoints must align with complete rollout batches")
    return protocol


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


def _periodic_checkpoint(root: Path, step: int) -> Path:
    matches = sorted((root / "checkpoints").glob(f"*_{step}_steps.zip"))
    if len(matches) != 1:
        raise RuntimeError(f"expected one checkpoint at {step} steps, found {len(matches)}")
    return matches[0]


def _passes(summary: dict[str, Any], gate: dict[str, Any]) -> bool:
    domain_failures = int(summary["runtime_domain_failure_count"]) + int(
        summary["observation_domain_failure_count"]
    )
    return all(
        (
            float(summary["episode_completion_rate"])
            >= float(gate["minimum_episode_completion_rate"]),
            float(summary["behavior_complete_experiment_rate"])
            >= float(gate["minimum_behavior_complete_experiment_rate"]),
            float(summary["quick_close_rate"]) <= float(gate["quick_close_rate"]),
            domain_failures
            <= int(gate["runtime_domain_failure_count"])
            + int(gate["observation_domain_failure_count"]),
        )
    )


def _evaluation_card(
    *,
    checkpoint: Path,
    model_seed: int,
    training_steps: int,
    protocol: dict[str, Any],
    allocation: RLWorldAllocation,
    seed_index: int,
) -> dict[str, Any]:
    gate = protocol["development_gate"]
    evaluation = evaluate_sb3_checkpoint(
        algorithm="ppo",
        checkpoint=checkpoint,
        task_id=str(protocol["task_id"]),
        allocation=allocation,
        episodes=int(gate["dev_episodes_per_seed"]),
        operation_budget=int(gate["dev_operation_budget"]),
        sampler_seed=int(gate["dev_sampler_seed_base"]) + seed_index,
        policy_seed=int(gate["dev_policy_seed_base"]) + seed_index,
        deterministic=bool(gate["deterministic_policy"]),
    )
    return {
        "model_seed": model_seed,
        "training_environment_steps": training_steps,
        "checkpoint": str(checkpoint),
        "checkpoint_sha256": hashlib.sha256(checkpoint.read_bytes()).hexdigest(),
        "summary": evaluation["summary"],
        "episode_cards": evaluation["episode_cards"],
        "gate_passed": _passes(evaluation["summary"], gate),
    }


def run_learning_gate(
    *, protocol: dict[str, Any], output_dir: Path, source_commit: str
) -> dict[str, Any]:
    gate = protocol["development_gate"]
    task_id = str(protocol["task_id"])
    allocation_protocol = load_rl_protocol(ALLOCATION_PATH)
    train_allocation = RLWorldAllocation.from_protocol(
        allocation_protocol, task_id=task_id, name="train"
    )
    dev_allocation = RLWorldAllocation.from_protocol(
        allocation_protocol, task_id=task_id, name="dev"
    )
    seeds = [int(seed) for seed in gate["training_seeds"]]
    checkpoints = [int(step) for step in gate["training_environment_step_checkpoints"]]
    output_dir.mkdir(parents=True, exist_ok=True)

    curve_root = output_dir / f"seed-{seeds[0]}"
    print(
        f"training preregistered seed {seeds[0]} through {checkpoints[-1]} steps",
        flush=True,
    )
    curve_manifest = train_sb3_baseline(
        algorithm="ppo",
        task_id=task_id,
        allocation=train_allocation,
        total_timesteps=checkpoints[-1],
        model_seed=seeds[0],
        output_dir=curve_root,
        algorithm_kwargs=dict(gate["hyperparameters"]),
        operation_budget=int(gate["training_operation_budget"]),
        checkpoint_interval_steps=checkpoints[0],
    )
    curve: list[dict[str, Any]] = []
    for checkpoint_steps in checkpoints:
        print(f"evaluating seed {seeds[0]} at {checkpoint_steps} steps", flush=True)
        curve.append(
            _evaluation_card(
                checkpoint=_periodic_checkpoint(curve_root, checkpoint_steps),
                model_seed=seeds[0],
                training_steps=checkpoint_steps,
                protocol=protocol,
                allocation=dev_allocation,
                seed_index=0,
            )
        )
    selected = next((item for item in curve if item["gate_passed"]), None)
    multiseed: list[dict[str, Any]] = []
    if selected is not None:
        multiseed.append(selected)
        selected_steps = int(selected["training_environment_steps"])
        for seed_index, model_seed in enumerate(seeds[1:], start=1):
            print(f"training expansion seed {model_seed} for {selected_steps} steps", flush=True)
            seed_root = output_dir / f"seed-{model_seed}"
            manifest = train_sb3_baseline(
                algorithm="ppo",
                task_id=task_id,
                allocation=train_allocation,
                total_timesteps=selected_steps,
                model_seed=model_seed,
                output_dir=seed_root,
                algorithm_kwargs=dict(gate["hyperparameters"]),
                operation_budget=int(gate["training_operation_budget"]),
            )
            checkpoint = seed_root / str(manifest["checkpoint"])
            print(f"evaluating expansion seed {model_seed}", flush=True)
            multiseed.append(
                _evaluation_card(
                    checkpoint=checkpoint,
                    model_seed=model_seed,
                    training_steps=selected_steps,
                    protocol=protocol,
                    allocation=dev_allocation,
                    seed_index=seed_index,
                )
            )

    passed = len(multiseed) == 5 and all(item["gate_passed"] for item in multiseed)
    prior = json.loads(REPORT_PATH.read_text(encoding="utf-8"))
    prior.update(
        {
            "schema_version": "chemworld-foundation-rl-contract-report-0.2",
            "status": "five_seed_learning_gate_passed" if passed else "learning_curve_gate_failed",
            "generated_at": datetime.now(UTC).isoformat(),
            "source_commit": source_commit,
            "source_tree_dirty": False,
            "protocol": {
                "path": str(PROTOCOL_PATH.relative_to(ROOT)).replace("\\", "/"),
                "sha256": _canonical_sha256(protocol),
                "protocol_id": protocol["protocol_id"],
            },
            "preregistered_learning_curve": curve,
            "selected_training_environment_steps": (
                int(selected["training_environment_steps"]) if selected else None
            ),
            "five_seed_development_gate": multiseed,
            "gate_summary": {
                "required_training_seed_count": 5,
                "required_dev_episode_count_per_seed": int(
                    gate["dev_episodes_per_seed"]
                ),
                "learning_curve_checkpoint_passed": selected is not None,
                "evaluated_training_seed_count": len(multiseed),
                "passed_training_seed_count": sum(
                    int(item["gate_passed"]) for item in multiseed
                ),
                "status": "passed" if passed else "failed",
                "reason": (
                    "All five unchanged PPO seeds passed the per-experiment behavior gate."
                    if passed
                    else "The preregistered curve did not justify unchanged five-seed expansion."
                ),
            },
            "benchmark_claim_allowed": False,
            "publication_ready": False,
        }
    )
    prior["checks"]["five_seed_twenty_episode_gate"] = passed
    prior["training_manifest"] = curve_manifest
    return prior


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir", type=Path, default=Path("runs/foundation-rl-learning-curve-0.2")
    )
    parser.add_argument("--report", type=Path, default=REPORT_PATH)
    args = parser.parse_args()
    source_commit = git_commit()
    if source_commit is None or _tracked_tree_dirty():
        raise RuntimeError("foundation RL learning gate requires a clean committed source tree")
    report = run_learning_gate(
        protocol=load_protocol(), output_dir=args.output_dir, source_commit=source_commit
    )
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(report["gate_summary"], indent=2, sort_keys=True), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
