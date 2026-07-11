"""Build a paired-seed validity and prospective-power report."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

from chemworld.data.submission import git_commit
from chemworld.eval.validity_power import audit_validity_power
from chemworld.tasks import SERIOUS_TASK_IDS, get_task
from chemworld.world.parameters import WORLD_FAMILY_VERSION


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
    parser.add_argument("--baseline-results", type=Path, required=True)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("workstreams/benchmark_v1/reports/validity-power-pilot.json"),
    )
    parser.add_argument("--practical-effect", type=float, default=0.05)
    parser.add_argument("--planned-seeds", type=int, default=20)
    parser.add_argument(
        "--adaptive-methods",
        nargs="+",
        help="Compare these diagnostic methods against random.",
    )
    parser.add_argument(
        "--evaluated-source-commit",
        help="Commit that exactly produced the input results; omit for a dirty diagnostic run.",
    )
    args = parser.parse_args()

    results = json.loads(args.baseline_results.read_text(encoding="utf-8"))
    if not isinstance(results, list):
        raise ValueError("baseline results must be a JSON list")
    audit_kwargs = {
        "practical_effect": args.practical_effect,
        "planned_seed_count": args.planned_seeds,
    }
    if args.adaptive_methods:
        adaptive_pairs = tuple((method, "random") for method in args.adaptive_methods)
        audit_kwargs.update(
            {
                "method_pairs": adaptive_pairs,
                "adaptive_method_pairs": adaptive_pairs,
            }
        )
    report = audit_validity_power(results, **audit_kwargs)
    report["provenance"] = {
        "report_source_commit": git_commit(),
        "report_source_tree_dirty": _tracked_tree_dirty(),
        "evaluated_source_commit": args.evaluated_source_commit,
        "evaluation_source_tree_dirty": args.evaluated_source_commit is None,
        "world_law_id": WORLD_FAMILY_VERSION,
        "baseline_results_sha256": _sha256(args.baseline_results),
        "baseline_result_count": len(results),
        "task_contract_hashes": {
            task_id: get_task(task_id).contract_hash for task_id in SERIOUS_TASK_IDS
        },
        "diagnostic_only": True,
        "paper_claim_allowed": False,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(
        (json.dumps(report, indent=2, sort_keys=True) + "\n").encode("utf-8")
    )
    summary = {
        "output": str(args.output),
        "status": report["status"],
        "task_count": report["task_count"],
        "adaptive_value_task_count": report["adaptive_value_task_count"],
        "learning_capacity_task_count": report["learning_capacity_task_count"],
        "planned_seed_count": report["planned_seed_count"],
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
