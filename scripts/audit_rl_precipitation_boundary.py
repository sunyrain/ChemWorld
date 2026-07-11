"""Re-evaluate the RL-triggered precipitation boundary after the kernel repair."""

from __future__ import annotations

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
from chemworld.physchem.equilibrium_chemistry import (  # noqa: E402
    SolubilityProductSpec,
    precipitate_if_supersaturated,
)
from chemworld.rl.environment import (  # noqa: E402
    RLWorldAllocation,
    load_rl_protocol,
)
from chemworld.rl.evaluation import evaluate_sb3_checkpoint  # noqa: E402

FREEZE = ROOT / "configs/benchmark/confirmatory_freeze_vnext.json"
STAGED_REPORT = ROOT / "workstreams/benchmark_v1/reports/rl-staged-development.json"
CHECKPOINT = (
    ROOT
    / "runs/rl-staged-development-0.1/sac/sac-flow-reaction-optimization-seed0.zip"
)
OUTPUT = (
    ROOT / "workstreams/benchmark_v1/reports/rl-precipitation-boundary-audit.json"
)


def build_report(*, source_commit: str) -> dict[str, Any]:
    staged = load_rl_protocol(STAGED_REPORT)
    before = staged["algorithm_cards"]["sac"]["world_family_dev_evaluation"]["summary"]
    freeze = load_rl_protocol(FREEZE)
    allocation = RLWorldAllocation.from_protocol(
        freeze,
        task_id="flow-reaction-optimization",
        name="dev",
    )
    after = evaluate_sb3_checkpoint(
        algorithm="sac",
        checkpoint=CHECKPOINT,
        task_id="flow-reaction-optimization",
        allocation=allocation,
        episodes=20,
        operation_budget=40,
        sampler_seed=199,
        policy_seed=223,
        deterministic=False,
    )
    extreme = precipitate_if_supersaturated(
        {"X+": 1.0, "Y-": 1.0e-6},
        SolubilityProductSpec("XY(s)", "X+", "Y-", ksp=1.0e-30),
        volume_L=1.0,
    )
    after_summary = after["summary"]
    checks = {
        "same_checkpoint": _sha256(CHECKPOINT)
        == staged["algorithm_cards"]["sac"]["checkpoint_sha256"],
        "same_dev_sampling_contract": after["sampler_seed"] == 199
        and after["policy_seed"] == 223
        and after["episodes"] == 20,
        "pre_fix_failure_reproduced_in_bound_report": int(
            before["observation_domain_failure_count"]
        )
        == 31,
        "post_fix_observation_domain_failures_zero": int(
            after_summary["observation_domain_failure_count"]
        )
        == 0,
        "post_fix_runtime_domain_failures_zero": int(
            after_summary["runtime_domain_failure_count"]
        )
        == 0,
        "extreme_stoichiometric_boundary_solved": extreme.ion_product <= 1.0e-30,
        "extreme_material_balance_preserved": extreme.material_balance_error_mol
        < 1.0e-12,
    }
    return {
        "schema_version": "chemworld-rl-precipitation-boundary-audit-0.1",
        "status": "passed" if all(checks.values()) else "failed",
        "generated_at": datetime.now(UTC).isoformat(),
        "evaluated_source_commit": source_commit,
        "evaluation_source_tree_dirty": False,
        "checkpoint_sha256": _sha256(CHECKPOINT),
        "checks": checks,
        "before_fix": _summary(before),
        "after_fix": _summary(after_summary),
        "extreme_boundary_case": {
            "ksp": 1.0e-30,
            "initial_cation_mol": 1.0,
            "initial_anion_mol": 1.0e-6,
            "precipitated_mol": extreme.precipitated_mol,
            "final_ion_product": extreme.ion_product,
            "material_balance_error_mol": extreme.material_balance_error_mol,
            "solver_status": extreme.metadata.get("solver_status"),
        },
        "claim_boundary": (
            "Fixed-source Dev diagnostic using a pre-fix 20k checkpoint; this validates "
            "the numerical repair but does not restore the checkpoint as formal evidence."
        ),
        "training_policy": (
            "Any 100k or formal checkpoint must be trained from scratch on the repaired source."
        ),
    }


def _summary(payload: dict[str, Any]) -> dict[str, Any]:
    keys = (
        "operation_count",
        "complete_experiment_count",
        "episode_completion_rate",
        "invalid_action_rate",
        "mean_final_score",
        "mean_episode_best_score",
        "runtime_domain_failure_count",
        "observation_domain_failure_count",
    )
    return {key: payload[key] for key in keys}


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
    source_commit = git_commit()
    if source_commit is None or _tracked_tree_dirty():
        raise RuntimeError("RL precipitation boundary audit requires a clean committed tree")
    report = build_report(source_commit=source_commit)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "status": report["status"],
                "before_failures": report["before_fix"][
                    "observation_domain_failure_count"
                ],
                "after_failures": report["after_fix"][
                    "observation_domain_failure_count"
                ],
                "report": str(OUTPUT.relative_to(ROOT)),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
