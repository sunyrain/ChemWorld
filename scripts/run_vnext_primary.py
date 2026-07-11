"""Run the frozen vNext core-four structured-GP versus random comparison."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from chemworld.agents.task_recipes import task_recipe_event_count
from chemworld.data.submission import git_commit
from chemworld.eval.benchmark_validation import PRIMARY_METRIC_FIELDS
from chemworld.eval.confirmatory_freeze import (
    audit_confirmatory_freeze,
    load_confirmatory_freeze,
)
from chemworld.eval.constrained_inference import paired_constraint_decisions
from chemworld.eval.suite import run_suite
from chemworld.eval.validity_power import audit_validity_power
from chemworld.tasks import get_task

PRIMARY_RESULT_SCHEMA_VERSION = "chemworld-vnext-primary-run-0.2"


@dataclass(frozen=True)
class PrimaryJob:
    task_id: str
    method_id: str
    seeds: tuple[int, ...]
    complete_experiments: int
    operation_budget: int
    output_dir: str
    protocol_id: str
    protocol_sha256: str
    evaluated_source_commit: str


def build_primary_jobs(
    *,
    protocol: dict[str, Any],
    output_dir: str | Path,
    evaluated_source_commit: str,
) -> list[PrimaryJob]:
    audit = audit_confirmatory_freeze(protocol)
    if audit.get("primary_classical_rerun_ready") is not True:
        raise ValueError("frozen primary classical comparison is not ready")
    primary = protocol["primary_comparison"]
    methods = (str(primary["candidate_method"]), str(primary["comparator"]))
    seeds = tuple(int(seed) for seed in primary["paired_confirmatory_seeds"])
    complete_experiments = int(primary["complete_experiments_per_run"])
    root = Path(output_dir)
    jobs: list[PrimaryJob] = []
    for task_id in protocol["task_roles"]["core"]:
        task = get_task(str(task_id))
        operation_budget = task_recipe_event_count(task.to_dict()) * complete_experiments
        for method_id in methods:
            jobs.append(
                PrimaryJob(
                    task_id=str(task_id),
                    method_id=method_id,
                    seeds=seeds,
                    complete_experiments=complete_experiments,
                    operation_budget=operation_budget,
                    output_dir=str(root / "runs" / str(task_id) / method_id),
                    protocol_id=str(protocol["protocol_id"]),
                    protocol_sha256=str(audit["protocol_sha256"]),
                    evaluated_source_commit=evaluated_source_commit,
                )
            )
    return jobs


def _run_job(job: PrimaryJob) -> list[dict[str, Any]]:
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
                "evaluation_budget_steps": job.operation_budget,
                "evaluated_complete_experiments": job.complete_experiments,
                "confirmatory_protocol_id": job.protocol_id,
                "confirmatory_protocol_sha256": job.protocol_sha256,
                "evaluated_source_commit": job.evaluated_source_commit,
                "evaluation_source_tree_dirty": False,
                "evaluation_policy": "vnext_risk_cost",
            }
        )
        _validate_result(result, job)
    return results


def _validate_result(result: dict[str, Any], job: PrimaryJob) -> None:
    usage = result.get("resource_usage", {})
    if result.get("result_schema_version") != "chemworld-evaluation-result-0.3":
        raise RuntimeError(f"{job.task_id}/{job.method_id} did not emit result schema 0.3")
    if result.get("verified") is not True:
        raise RuntimeError(f"{job.task_id}/{job.method_id} result did not replay-verify")
    if int(usage.get("complete_experiment_count", -1)) != job.complete_experiments:
        raise RuntimeError(
            f"{job.task_id}/{job.method_id}/seed{result.get('seed')} completed "
            f"{usage.get('complete_experiment_count')} experiments; expected "
            f"{job.complete_experiments}"
        )
    if usage.get("method_ledger", {}).get("accounting_complete") is not True:
        raise RuntimeError(f"{job.task_id}/{job.method_id} resource ledger is incomplete")


def build_primary_statistics(
    results: list[dict[str, Any]],
    *,
    protocol: dict[str, Any],
) -> dict[str, Any]:
    primary = protocol["primary_comparison"]
    candidate = str(primary["candidate_method"])
    comparator = str(primary["comparator"])
    task_ids = tuple(str(task_id) for task_id in protocol["task_roles"]["core"])
    for result in results:
        task_id = str(result["task_id"])
        field = PRIMARY_METRIC_FIELDS[task_id]
        sesoi = float(protocol["sesoi"]["tasks"][task_id]["sesoi"])
        result["primary_metric_field"] = field
        result["primary_metric_sesoi"] = sesoi
        result["primary_metric_normalized_by_sesoi"] = float(result[field]) / sesoi
    bootstrap_samples = int(primary["decision_rule"]["deterministic_bootstrap_samples"])
    audit = audit_validity_power(
        results,
        task_ids=task_ids,
        method_pairs=((candidate, comparator),),
        adaptive_method_pairs=((candidate, comparator),),
        metric="primary_metric_normalized_by_sesoi",
        practical_effect=1.0,
        alpha=float(primary["decision_rule"]["holm_adjusted_alpha"]),
        planned_seed_count=len(primary["paired_confirmatory_seeds"]),
        bootstrap_samples=bootstrap_samples,
    )
    comparison_key = f"{candidate}__minus__{comparator}"
    constraint_rule = primary["decision_rule"]["constraint_noninferiority"]
    constraint_audit = paired_constraint_decisions(
        results,
        task_ids=task_ids,
        candidate=candidate,
        comparator=comparator,
        paired_seeds=tuple(int(seed) for seed in primary["paired_confirmatory_seeds"]),
        bootstrap_samples=bootstrap_samples,
        upper_quantile=float(constraint_rule["upper_quantile"]),
        safety_margin=float(constraint_rule["safety"]["maximum_noninferiority_margin"]),
        cost_margin=float(constraint_rule["cost"]["maximum_noninferiority_margin"]),
    )
    decisions: dict[str, Any] = {}
    for task_id in task_ids:
        sesoi = float(protocol["sesoi"]["tasks"][task_id]["sesoi"])
        comparison = audit["tasks"][task_id]["comparisons"][comparison_key]
        ci = comparison["paired_bootstrap_ci"]
        mean_effect = float(comparison["mean_paired_effect"]) * sesoi
        raw_ci = [float(bound) * sesoi for bound in ci]
        decisions[task_id] = {
            "primary_metric": protocol["sesoi"]["tasks"][task_id]["primary_metric"],
            "sesoi": sesoi,
            "mean_paired_effect": mean_effect,
            "paired_bootstrap_ci": raw_ci,
            "holm_adjusted_p_value": comparison["holm_adjusted_p_value"],
            "direction_passed": raw_ci[0] > 0.0,
            "multiplicity_passed": comparison["significant_after_holm"],
            "sesoi_passed": mean_effect >= sesoi,
        }
        decisions[task_id]["joint_rule_passed"] = all(
            decisions[task_id][key]
            for key in ("direction_passed", "multiplicity_passed", "sesoi_passed")
        )
        decisions[task_id]["objective_rule_passed"] = decisions[task_id].pop(
            "joint_rule_passed"
        )
        decisions[task_id]["constraints"] = constraint_audit["task_decisions"][task_id]
        decisions[task_id]["complete_joint_rule_passed"] = bool(
            decisions[task_id]["objective_rule_passed"]
            and decisions[task_id]["constraints"]["constraints_passed"]
        )
    all_objectives_passed = all(card["objective_rule_passed"] for card in decisions.values())
    all_constraints_passed = bool(constraint_audit["all_task_constraints_passed"])
    return {
        "schema_version": "chemworld-vnext-primary-statistics-0.2",
        "metric_policy": "per_task_primary_metric_normalized_only_for_joint_inference",
        "cross_task_performance_score": None,
        "comparison": comparison_key,
        "bootstrap_samples": bootstrap_samples,
        "task_decisions": decisions,
        "all_task_objective_rule_passed": all_objectives_passed,
        "all_task_constraint_rule_passed": all_constraints_passed,
        "all_task_joint_rule_passed": all(
            card["complete_joint_rule_passed"] for card in decisions.values()
        ),
        "constraint_inference": constraint_audit,
        "validity_power_audit": audit,
        "benchmark_claim_allowed": False,
        "publication_ready": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("runs/benchmark-vnext/primary-0.1"),
    )
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.workers < 1:
        raise ValueError("workers must be positive")
    protocol = load_confirmatory_freeze()
    evaluated_commit = git_commit()
    if evaluated_commit is None:
        raise RuntimeError("vNext primary runs require a Git commit")
    jobs = build_primary_jobs(
        protocol=protocol,
        output_dir=args.output_dir,
        evaluated_source_commit=evaluated_commit,
    )
    if args.dry_run:
        print(json.dumps([asdict(job) for job in jobs], indent=2, sort_keys=True))
        return 0
    if _tracked_tree_dirty():
        raise RuntimeError("vNext primary runs require a clean tracked tree")

    args.output_dir.mkdir(parents=True, exist_ok=True)
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
                        "seeds": list(job.seeds),
                        "error_type": type(exc).__name__,
                        "error": str(exc),
                    }
                )

    all_results.sort(
        key=lambda row: (
            str(row["task_id"]),
            str(row["baseline_agent"]),
            int(row["seed"]),
        )
    )
    _write_json(args.output_dir / "primary_results.json", all_results)
    statistics = None
    if not failures:
        statistics = build_primary_statistics(all_results, protocol=protocol)
        _write_json(args.output_dir / "primary_statistics.json", statistics)
    manifest = {
        "schema_version": PRIMARY_RESULT_SCHEMA_VERSION,
        "status": "completed" if not failures else "failed_with_retained_failures",
        "generated_at": datetime.now(UTC).isoformat(),
        "formal_slice": "primary_classical_only",
        "confirmatory_protocol_id": protocol["protocol_id"],
        "confirmatory_protocol_sha256": jobs[0].protocol_sha256,
        "evaluated_source_commit": evaluated_commit,
        "evaluation_source_tree_dirty": False,
        "jobs": [asdict(job) for job in jobs],
        "result_count": len(all_results),
        "expected_result_count": sum(len(job.seeds) for job in jobs),
        "failures": failures,
        "primary_results_sha256": _sha256(args.output_dir / "primary_results.json"),
        "primary_statistics_sha256": (
            _sha256(args.output_dir / "primary_statistics.json") if statistics is not None else None
        ),
        "benchmark_claim_allowed": False,
        "publication_ready": False,
        "remaining_gate": (
            "complete constrained primary rule, full cross-family matrix, private "
            "generalization, and independent reproduction"
        ),
    }
    _write_json(args.output_dir / "manifest.json", manifest)
    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0 if not failures else 1


def _tracked_tree_dirty() -> bool:
    completed = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=no"],
        check=True,
        capture_output=True,
        text=True,
    )
    return bool(completed.stdout.strip())


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


if __name__ == "__main__":
    raise SystemExit(main())
