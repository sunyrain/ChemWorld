"""Run the frozen train/dev-only safe-policy comparison."""

from __future__ import annotations

import argparse
import hashlib
import json
import statistics
import subprocess
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import numpy as np

from chemworld.agents.task_recipes import (
    TASK_RECIPE_SPACE_VERSION,
    task_recipe_event_count,
)
from chemworld.data.submission import git_commit
from chemworld.eval.benchmark_validation import PRIMARY_METRIC_FIELDS
from chemworld.eval.confirmatory_freeze import load_confirmatory_freeze
from chemworld.eval.constrained_inference import paired_constraint_decisions
from chemworld.eval.suite import run_suite
from chemworld.physchem.mechanism_library import configuration_root
from chemworld.tasks import get_task

RUN_SCHEMA_VERSION = "chemworld-safe-policy-development-run-0.1"
SUMMARY_SCHEMA_VERSION = "chemworld-safe-policy-development-summary-0.1"
DEFAULT_PROTOCOL = configuration_root() / "benchmark" / "safe_policy_development.json"
LEGACY_PRIMARY_METRIC_FIELDS_0_2 = {
    "partition-discovery": "mean_product_in_organic",
    "reaction-to-crystallization": "mean_crystal_yield",
    "reaction-to-distillation": "mean_distillate_purity",
    "flow-reaction-optimization": "mean_flow_conversion",
}


@dataclass(frozen=True)
class DevelopmentJob:
    task_id: str
    method_id: str
    seeds: tuple[int, ...]
    complete_experiments: int
    operation_budget: int
    output_dir: str
    protocol_id: str
    protocol_sha256: str
    evaluated_source_commit: str


def load_development_protocol(path: str | Path = DEFAULT_PROTOCOL) -> dict[str, Any]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("safe-policy development protocol must be an object")
    _validate_protocol(payload)
    return payload


def build_development_jobs(
    protocol: dict[str, Any],
    *,
    output_dir: str | Path,
    evaluated_source_commit: str,
) -> list[DevelopmentJob]:
    digest = _canonical_sha256(protocol)
    seeds = tuple(int(seed) for seed in protocol["dev_seeds"])
    experiments = int(protocol["complete_experiments_per_run"])
    root = Path(output_dir)
    return [
        DevelopmentJob(
            task_id=str(task_id),
            method_id=str(method_id),
            seeds=seeds,
            complete_experiments=experiments,
            operation_budget=task_recipe_event_count(get_task(str(task_id)).to_dict())
            * experiments,
            output_dir=str(root / "runs" / str(task_id) / str(method_id)),
            protocol_id=str(protocol["protocol_id"]),
            protocol_sha256=digest,
            evaluated_source_commit=evaluated_source_commit,
        )
        for task_id in protocol["tasks"]
        for method_id in protocol["methods"]
    ]


def build_development_summary(
    results: list[dict[str, Any]],
    *,
    protocol: dict[str, Any],
) -> dict[str, Any]:
    tasks = tuple(str(task_id) for task_id in protocol["tasks"])
    methods = tuple(str(method_id) for method_id in protocol["methods"])
    seeds = tuple(int(seed) for seed in protocol["dev_seeds"])
    selection = protocol["selection_rule"]
    safe_method = "structured_safe_gp_bo"
    comparator = str(selection["comparator"])
    bootstrap_samples = int(selection["bootstrap_samples"])

    cells: dict[str, Any] = {}
    objective_retention: dict[str, Any] = {}
    metric_fields = _primary_metric_fields(protocol)
    for task_id in tasks:
        metric = metric_fields[task_id]
        cells[task_id] = {}
        indexed: dict[tuple[str, int], dict[str, Any]] = {}
        for row in results:
            if row["task_id"] == task_id:
                indexed[(str(row["baseline_agent"]), int(row["seed"]))] = row
        for method_id in methods:
            rows = [indexed[(method_id, seed)] for seed in seeds]
            values = [float(row[metric]) for row in rows]
            risks = [_risk_rate(row) for row in rows]
            costs = [_cost_per_experiment(row) for row in rows]
            cells[task_id][method_id] = {
                "run_count": len(rows),
                "primary_metric": metric,
                "primary_metric_mean": statistics.fmean(values),
                "primary_metric_sample_sd": statistics.stdev(values),
                "risk_exceedance_rate_mean": statistics.fmean(risks),
                "cost_per_experiment_mean": statistics.fmean(costs),
            }
        effects = [
            (
                float(indexed[(safe_method, seed)][metric])
                - float(indexed[(comparator, seed)][metric])
            )
            for seed in seeds
        ]
        lower_bound = _bootstrap_mean_bound(
            effects,
            task_id=task_id,
            label="objective_retention",
            samples=bootstrap_samples,
            quantile=float(selection["objective_lower_quantile"]),
        )
        sesoi = float(load_confirmatory_freeze()["sesoi"]["tasks"][task_id]["sesoi"])
        margin = -float(selection["objective_retention_margin_sesoi_multiple"]) * sesoi
        objective_retention[task_id] = {
            "primary_metric": metric,
            "mean_paired_effect": statistics.fmean(effects),
            "simultaneous_lower_confidence_bound": lower_bound,
            "minimum_retention_margin": margin,
            "retention_passed": lower_bound >= margin,
        }

    constraint_comparisons = {
        comparison: paired_constraint_decisions(
            results,
            task_ids=tasks,
            candidate=safe_method,
            comparator=comparison,
            paired_seeds=seeds,
            bootstrap_samples=bootstrap_samples,
            upper_quantile=float(selection["constraint_upper_quantile"]),
            safety_margin=float(selection["safety_absolute_noninferiority_margin"]),
            cost_margin=float(selection["cost_relative_noninferiority_margin"]),
        )
        for comparison in (comparator, "structured_gp_bo")
    }
    objective_retention_passed = all(
        card["retention_passed"] for card in objective_retention.values()
    )
    random_constraints_passed = bool(
        constraint_comparisons[comparator]["all_task_constraints_passed"]
    )
    selected_for_future_freeze = objective_retention_passed and random_constraints_passed
    return {
        "schema_version": SUMMARY_SCHEMA_VERSION,
        "status": "development_complete",
        "world_role": "dev",
        "protocol_id": protocol["protocol_id"],
        "protocol_sha256": _canonical_sha256(protocol),
        "result_count": len(results),
        "task_method_cells": cells,
        "objective_retention_vs_random": objective_retention,
        "constraint_comparisons": constraint_comparisons,
        "objective_retention_all_tasks_passed": objective_retention_passed,
        "constraints_vs_random_all_tasks_passed": random_constraints_passed,
        "selected_for_future_freeze": selected_for_future_freeze,
        "benchmark_claim_allowed": False,
        "publication_ready": False,
        "interpretation": (
            "Development evidence may select a method for a future untouched-cohort freeze; "
            "it cannot support a benchmark or method-superiority claim."
        ),
    }


def _run_job(job: DevelopmentJob) -> list[dict[str, Any]]:
    task = get_task(job.task_id)
    results = run_suite(
        agent_name=job.method_id,
        env_id=task.env_id,
        world_splits=[task.world_split],
        seeds=list(job.seeds),
        budget=task.budget,
        budget_override=job.operation_budget,
        objective=task.objective,
        output_dir=job.output_dir,
        threshold=task.threshold,
        task_id=job.task_id,
        evaluation_policy="vnext_risk_cost",
    )
    for result in results:
        result.update(
            {
                "task_id": job.task_id,
                "baseline_agent": job.method_id,
                "safe_policy_development_protocol_id": job.protocol_id,
                "safe_policy_development_protocol_sha256": job.protocol_sha256,
                "evaluated_source_commit": job.evaluated_source_commit,
                "evaluation_source_tree_dirty": False,
            }
        )
        usage = result.get("resource_usage", {})
        if result.get("verified") is not True:
            raise RuntimeError(f"{job.task_id}/{job.method_id} failed replay verification")
        if int(usage.get("complete_experiment_count", -1)) != job.complete_experiments:
            raise RuntimeError(f"{job.task_id}/{job.method_id} incomplete experiment budget")
        if usage.get("method_ledger", {}).get("accounting_complete") is not True:
            raise RuntimeError(f"{job.task_id}/{job.method_id} incomplete resource ledger")
    return results


def _validate_protocol(protocol: dict[str, Any]) -> None:
    if protocol.get("schema_version") != "chemworld-safe-policy-development-0.1":
        raise ValueError("unsupported safe-policy development protocol")
    if protocol.get("benchmark_claim_allowed") is not False:
        raise ValueError("development protocol must remain nonclaiming")
    dev_seeds = {int(seed) for seed in protocol.get("dev_seeds", ())}
    forbidden = {int(seed) for seed in protocol.get("bench_seeds_forbidden", ())}
    if len(dev_seeds) != 20 or dev_seeds & forbidden:
        raise ValueError("dev seeds must contain 20 unique non-bench values")
    if protocol.get("recipe_space_version") != "chemworld-task-recipe-space-0.2":
        raise ValueError("development protocol must use decoupled recipe space 0.2")
    contract = protocol.get("safe_policy_contract", {})
    if contract.get("risk_label") != "experiment_peak_safety_risk":
        raise ValueError("safe policy must learn experiment peak risk")


def validate_development_runtime_compatibility(protocol: dict[str, Any]) -> None:
    """Refuse to execute a frozen historical protocol with a newer agent space."""

    frozen_version = str(protocol.get("recipe_space_version", ""))
    if frozen_version != TASK_RECIPE_SPACE_VERSION:
        raise RuntimeError(
            "safe-policy development protocol is superseded: frozen recipe space "
            f"{frozen_version!r} does not match runtime {TASK_RECIPE_SPACE_VERSION!r}"
        )


def _primary_metric_fields(protocol: dict[str, Any]) -> dict[str, str]:
    version = str(protocol.get("recipe_space_version", ""))
    if version == "chemworld-task-recipe-space-0.2":
        return dict(LEGACY_PRIMARY_METRIC_FIELDS_0_2)
    return dict(PRIMARY_METRIC_FIELDS)


def _risk_rate(result: dict[str, Any]) -> float:
    return float(
        result["score_replay"]["layered_evaluation"]["constraints"][
            "risk_budget_exceedance_rate"
        ]
    )


def _cost_per_experiment(result: dict[str, Any]) -> float:
    resources = result["score_replay"]["layered_evaluation"]["resources"]
    return float(resources["campaign_total_cost"]) / int(resources["complete_experiment_count"])


def _bootstrap_mean_bound(
    effects: list[float],
    *,
    task_id: str,
    label: str,
    samples: int,
    quantile: float,
) -> float:
    values = np.asarray(effects, dtype=float)
    seed = int.from_bytes(hashlib.sha256(f"{task_id}|{label}".encode()).digest()[:8], "big")
    rng = np.random.default_rng(seed)
    indices = rng.integers(0, values.size, size=(samples, values.size))
    means = values[indices].mean(axis=1)
    return float(np.quantile(means, quantile, method="lower"))


def _canonical_sha256(payload: dict[str, Any]) -> str:
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _tracked_tree_dirty() -> bool:
    status = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=no"],
        check=True,
        capture_output=True,
        text=True,
    )
    return bool(status.stdout.strip())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--protocol", type=Path, default=DEFAULT_PROTOCOL)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--report", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.workers < 1:
        raise ValueError("workers must be positive")
    protocol = load_development_protocol(args.protocol)
    validate_development_runtime_compatibility(protocol)
    source_commit = git_commit()
    if source_commit is None:
        raise RuntimeError("safe-policy development requires a Git source commit")
    jobs = build_development_jobs(
        protocol,
        output_dir=args.output_dir,
        evaluated_source_commit=source_commit,
    )
    if args.dry_run:
        print(json.dumps([asdict(job) for job in jobs], indent=2, sort_keys=True))
        return 0
    if _tracked_tree_dirty():
        raise RuntimeError("safe-policy development requires a clean tracked tree")

    all_results: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    with ProcessPoolExecutor(max_workers=min(args.workers, len(jobs))) as executor:
        future_jobs = {executor.submit(_run_job, job): job for job in jobs}
        for future in as_completed(future_jobs):
            job = future_jobs[future]
            try:
                all_results.extend(future.result())
            except Exception as exc:  # pragma: no cover - real runtime failures
                failures.append(
                    {
                        "task_id": job.task_id,
                        "method_id": job.method_id,
                        "error_type": type(exc).__name__,
                        "error": str(exc),
                    }
                )
    all_results.sort(
        key=lambda row: (str(row["task_id"]), str(row["baseline_agent"]), int(row["seed"]))
    )
    args.output_dir.mkdir(parents=True, exist_ok=True)
    _write_json(args.output_dir / "development_results.json", all_results)
    summary = build_development_summary(all_results, protocol=protocol) if not failures else None
    if summary is not None:
        _write_json(args.output_dir / "development_summary.json", summary)
        if args.report is not None:
            _write_json(args.report, summary)
    manifest = {
        "schema_version": RUN_SCHEMA_VERSION,
        "status": "completed" if not failures else "failed_with_retained_failures",
        "generated_at": datetime.now(UTC).isoformat(),
        "protocol_id": protocol["protocol_id"],
        "protocol_sha256": _canonical_sha256(protocol),
        "evaluated_source_commit": source_commit,
        "world_role": "dev",
        "jobs": [asdict(job) for job in jobs],
        "result_count": len(all_results),
        "expected_result_count": sum(len(job.seeds) for job in jobs),
        "failures": failures,
        "benchmark_claim_allowed": False,
        "publication_ready": False,
    }
    _write_json(args.output_dir / "manifest.json", manifest)
    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
