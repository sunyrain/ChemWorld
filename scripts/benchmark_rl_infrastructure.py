"""Benchmark PPO training infrastructure without consuming research seeds."""

from __future__ import annotations

import argparse
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
from chemworld.rl.training import train_sb3_baseline  # noqa: E402

ALLOCATION_PATH = ROOT / "configs/benchmark/confirmatory_freeze_vnext.json"
TASK_ID = "flow-reaction-optimization"
DIAGNOSTIC_SEED_BASE = 9100
ROLLOUT_ENVIRONMENT_STEPS = 1024


def candidate_matrix(*, cuda_available: bool) -> list[dict[str, Any]]:
    """Return the preregistered infrastructure-only comparison matrix."""

    candidates: list[dict[str, Any]] = []
    devices = ["cpu", *(["cuda"] if cuda_available else [])]
    for device in devices:
        for environments in (1, 4, 8):
            candidates.append(
                {
                    "device": device,
                    "parallel_environments": environments,
                    "vectorization_backend": "dummy",
                }
            )
        for environments in (4, 8):
            candidates.append(
                {
                    "device": device,
                    "parallel_environments": environments,
                    "vectorization_backend": "subprocess",
                }
            )
    return candidates


def _tracked_tree_dirty() -> bool:
    completed = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=no"],
        check=True,
        capture_output=True,
        text=True,
    )
    return bool(completed.stdout.strip())


def run_benchmark(*, output_dir: Path, total_steps: int) -> dict[str, Any]:
    if total_steps <= 0 or total_steps % ROLLOUT_ENVIRONMENT_STEPS:
        raise ValueError("total steps must be a positive multiple of 1024")
    source_commit = git_commit()
    if source_commit is None or _tracked_tree_dirty():
        raise RuntimeError("infrastructure benchmark requires a clean committed source tree")
    if output_dir.exists():
        raise FileExistsError(f"refusing to reuse infrastructure output: {output_dir}")

    try:
        import torch
    except ImportError as exc:  # pragma: no cover - guarded by the RL extra
        raise RuntimeError("install ChemWorld with the 'rl' extra") from exc

    allocation_protocol = load_rl_protocol(ALLOCATION_PATH)
    allocation = RLWorldAllocation.from_protocol(
        allocation_protocol, task_id=TASK_ID, name="train"
    )
    matrix = candidate_matrix(cuda_available=bool(torch.cuda.is_available()))
    results: list[dict[str, Any]] = []
    for index, candidate in enumerate(matrix):
        environments = int(candidate["parallel_environments"])
        candidate_id = (
            f"{candidate['device']}-{candidate['vectorization_backend']}-n{environments}"
        )
        print(f"benchmarking {candidate_id}", flush=True)
        try:
            manifest = train_sb3_baseline(
                algorithm="ppo",
                task_id=TASK_ID,
                allocation=allocation,
                total_timesteps=total_steps,
                model_seed=DIAGNOSTIC_SEED_BASE + index,
                output_dir=output_dir / candidate_id,
                algorithm_kwargs={
                    "learning_rate": 0.0003,
                    "n_steps": ROLLOUT_ENVIRONMENT_STEPS // environments,
                    "batch_size": 64,
                    "gamma": 0.99,
                    "gae_lambda": 0.95,
                    "ent_coef": 0.01,
                },
                operation_budget=60,
                parallel_environments=environments,
                vectorization_backend=str(candidate["vectorization_backend"]),
                device=str(candidate["device"]),
            )
            infrastructure = dict(manifest["training_infrastructure"])
            results.append(
                {
                    "candidate_id": candidate_id,
                    **candidate,
                    "status": "passed",
                    "training_environment_step_count": manifest[
                        "training_environment_step_count"
                    ],
                    "step_budget_exact": manifest["step_budget_exact"],
                    "wall_time_s": manifest["wall_time_s"],
                    "cpu_time_s": manifest["cpu_time_s"],
                    "environment_steps_per_wall_second": infrastructure[
                        "environment_steps_per_wall_second"
                    ],
                    "average_process_cpu_cores": infrastructure[
                        "average_process_cpu_cores"
                    ],
                    "resolved_device": infrastructure["resolved_device"],
                    "torch_num_threads": infrastructure["torch_num_threads"],
                    "cuda_device_name": infrastructure["cuda_device_name"],
                    "training_diagnostics": manifest["training_diagnostics"],
                }
            )
        except Exception as exc:  # retain infrastructure failures as evidence
            results.append(
                {
                    "candidate_id": candidate_id,
                    **candidate,
                    "status": "failed",
                    "error_type": type(exc).__name__,
                    "error": str(exc),
                }
            )
    eligible = [
        item
        for item in results
        if item["status"] == "passed" and item["step_budget_exact"] is True
    ]
    selected = max(
        eligible,
        key=lambda item: float(item["environment_steps_per_wall_second"]),
        default=None,
    )
    return {
        "schema_version": "chemworld-rl-infrastructure-benchmark-0.1",
        "status": "complete" if len(eligible) == len(matrix) else "complete_with_failures",
        "research_result": False,
        "selection_criterion": "maximum_environment_steps_per_wall_second",
        "generated_at": datetime.now(UTC).isoformat(),
        "source_commit": source_commit,
        "task_id": TASK_ID,
        "diagnostic_seed_base": DIAGNOSTIC_SEED_BASE,
        "total_environment_steps_per_candidate": total_steps,
        "aggregate_rollout_environment_steps": ROLLOUT_ENVIRONMENT_STEPS,
        "hardware": {
            "torch": torch.__version__,
            "cuda_available": torch.cuda.is_available(),
            "torch_cuda_version": torch.version.cuda,
            "cuda_device_name": (
                torch.cuda.get_device_name(0) if torch.cuda.is_available() else None
            ),
        },
        "candidates": results,
        "selected_candidate": selected,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--steps", type=int, default=2048)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("runs/rl-infrastructure-benchmark-0.1"),
    )
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    report_path = args.report or args.output_dir / "report.json"
    report = run_benchmark(output_dir=args.output_dir, total_steps=args.steps)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(report["selected_candidate"], indent=2, sort_keys=True), flush=True)
    return 0 if report["selected_candidate"] is not None else 1


if __name__ == "__main__":
    raise SystemExit(main())
