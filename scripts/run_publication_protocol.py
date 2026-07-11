"""Run the clean, replay-verified experiment matrix frozen by the publication protocol."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from chemworld.agents.task_recipes import task_recipe_event_count
from chemworld.data.submission import git_commit
from chemworld.eval.benchmark_validation import PRIMARY_METRIC_FIELDS
from chemworld.eval.publication_protocol import (
    DEFAULT_PUBLICATION_PROTOCOL_PATH,
    assert_valid_publication_protocol,
    canonical_protocol_sha256,
    load_publication_protocol,
)
from chemworld.eval.suite import run_suite
from chemworld.eval.validity_power import audit_validity_power
from chemworld.tasks import get_task


def _tracked_tree_dirty() -> bool:
    completed = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=no"],
        check=True,
        capture_output=True,
        text=True,
    )
    return bool(completed.stdout.strip())


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes((json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--protocol",
        type=Path,
        default=DEFAULT_PUBLICATION_PROTOCOL_PATH,
    )
    parser.add_argument(
        "--stage",
        choices=("confirmatory", "full"),
        default="confirmatory",
        help="Run the primary contrast or every pre-registered classical method.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("runs/publication/protocol-v0.1"),
    )
    args = parser.parse_args()

    protocol = load_publication_protocol(args.protocol)
    assert_valid_publication_protocol(protocol)
    if _tracked_tree_dirty():
        raise RuntimeError(
            "Formal publication runs require a clean tracked tree; commit protocol changes first"
        )
    evaluated_commit = git_commit()
    if evaluated_commit is None:
        raise RuntimeError("Formal publication runs require a Git commit")

    protocol_sha256 = canonical_protocol_sha256(protocol)
    task_ids = [str(item["task_id"]) for item in protocol["tasks"]]
    seeds = [int(seed) for seed in protocol["experimental_design"]["seeds"]]
    complete_experiments = int(
        protocol["experimental_design"]["complete_experiments_per_task_seed"]
    )
    if args.stage == "confirmatory":
        contrasts = protocol["confirmatory_contrasts"]
        methods = sorted(
            {
                str(item[key])
                for item in contrasts
                for key in ("method", "comparator")
            }
        )
    else:
        methods = [str(item["method_id"]) for item in protocol["methods"]]

    root = args.output_dir / args.stage
    root.mkdir(parents=True, exist_ok=True)
    all_results: list[dict[str, Any]] = []
    budgets: dict[str, int] = {}
    for task_id in task_ids:
        task = get_task(task_id)
        budget = task_recipe_event_count(task.to_dict()) * complete_experiments
        budgets[task_id] = budget
        for method in methods:
            results = run_suite(
                agent_name=method,
                env_id=task.env_id,
                world_splits=[task.world_split],
                seeds=seeds,
                budget=task.budget,
                budget_override=budget,
                objective=task.objective,
                output_dir=root / "runs" / task_id / method,
                threshold=task.threshold,
                task_id=task_id,
            )
            for result in results:
                result.update(
                    {
                        "task_id": task_id,
                        "baseline_agent": method,
                        "evaluation_budget_steps": budget,
                        "evaluated_complete_experiments": complete_experiments,
                        "publication_protocol_id": protocol["protocol_id"],
                        "publication_protocol_sha256": protocol_sha256,
                        "evaluated_source_commit": evaluated_commit,
                        "evaluation_source_tree_dirty": False,
                    }
                )
                usage = result["resource_usage"]
                if int(usage["complete_experiment_count"]) != complete_experiments:
                    raise RuntimeError(
                        f"{task_id}/{method}/seed{result['seed']} completed "
                        f"{usage['complete_experiment_count']} experiments; expected "
                        f"{complete_experiments}"
                    )
            all_results.extend(results)

    results_path = root / "baseline_results.json"
    _write_json(results_path, all_results)
    contrast_pairs = tuple(
        (str(item["method"]), str(item["comparator"]))
        for item in protocol["confirmatory_contrasts"]
        if item["method"] in methods and item["comparator"] in methods
    )
    validity = audit_validity_power(
        all_results,
        task_ids=tuple(task_ids),
        method_pairs=contrast_pairs,
        adaptive_method_pairs=contrast_pairs,
        practical_effect=float(protocol["statistics"]["sesoi_total_score"]),
        alpha=float(protocol["statistics"]["alpha"]),
        planned_seed_count=len(seeds),
        bootstrap_samples=int(protocol["statistics"]["bootstrap_samples"]),
    )
    validity["provenance"] = {
        "publication_protocol_id": protocol["protocol_id"],
        "publication_protocol_sha256": protocol_sha256,
        "evaluated_source_commit": evaluated_commit,
        "evaluation_source_tree_dirty": False,
        "baseline_results_sha256": _sha256(results_path),
        "baseline_result_count": len(all_results),
        "formal_stage": args.stage,
        "paper_claim_allowed": False,
        "paper_claim_blocker": "generalization, exploit, and reproducibility gates remain",
    }
    validity["primary_task_metric_audits"] = {
        task_id: audit_validity_power(
            [row for row in all_results if row["task_id"] == task_id],
            task_ids=(task_id,),
            method_pairs=contrast_pairs,
            adaptive_method_pairs=contrast_pairs,
            metric=PRIMARY_METRIC_FIELDS[task_id],
            practical_effect=float(
                protocol["statistics"]["sesoi_primary_normalized_metric"]
            ),
            alpha=float(protocol["statistics"]["alpha"]),
            planned_seed_count=len(seeds),
            bootstrap_samples=int(protocol["statistics"]["bootstrap_samples"]),
        )
        for task_id in task_ids
    }
    validity_path = root / "validity_power.json"
    _write_json(validity_path, validity)

    manifest = {
        "schema_version": "chemworld-publication-run-0.1",
        "status": "completed",
        "formal_stage": args.stage,
        "generated_at": datetime.now(UTC).isoformat(),
        "publication_protocol_id": protocol["protocol_id"],
        "publication_protocol_sha256": protocol_sha256,
        "evaluated_source_commit": evaluated_commit,
        "evaluation_source_tree_dirty": False,
        "tasks": task_ids,
        "methods": methods,
        "seeds": seeds,
        "complete_experiments_per_task_seed": complete_experiments,
        "evaluation_budgets": budgets,
        "result_count": len(all_results),
        "baseline_results": str(results_path),
        "baseline_results_sha256": _sha256(results_path),
        "validity_power": str(validity_path),
        "validity_power_sha256": _sha256(validity_path),
        "paper_claim_allowed": False,
    }
    _write_json(root / "manifest.json", manifest)
    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
