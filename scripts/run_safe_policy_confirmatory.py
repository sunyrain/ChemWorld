"""Run the frozen untouched-cohort Safe-GP confirmatory comparison."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import statistics
import subprocess
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.run_vnext_primary import build_primary_statistics  # noqa: E402

from chemworld.agents.task_recipes import task_recipe_event_count  # noqa: E402
from chemworld.data.submission import git_commit  # noqa: E402
from chemworld.eval.benchmark_validation import PRIMARY_METRIC_FIELDS  # noqa: E402
from chemworld.eval.constrained_inference import (  # noqa: E402
    paired_constraint_decisions,
)
from chemworld.eval.suite import run_suite  # noqa: E402
from chemworld.physchem.mechanism_library import configuration_root  # noqa: E402
from chemworld.tasks import get_task  # noqa: E402

RUN_SCHEMA_VERSION = "chemworld-safe-policy-confirmatory-run-0.1"
STATISTICS_SCHEMA_VERSION = "chemworld-safe-policy-confirmatory-statistics-0.1"
DEFAULT_PROTOCOL = configuration_root() / "benchmark" / "safe_policy_confirmatory_freeze.json"


@dataclass(frozen=True)
class ConfirmatoryJob:
    task_id: str
    method_id: str
    seeds: tuple[int, ...]
    complete_experiments: int
    operation_budget: int
    output_dir: str
    protocol_id: str
    protocol_sha256: str
    evaluated_source_commit: str


def load_confirmatory_protocol(path: str | Path = DEFAULT_PROTOCOL) -> dict[str, Any]:
    protocol = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(protocol, dict):
        raise ValueError("safe-policy confirmatory protocol must be an object")
    _validate_protocol(protocol)
    return protocol


def build_confirmatory_jobs(
    protocol: dict[str, Any],
    *,
    output_dir: str | Path,
    evaluated_source_commit: str,
) -> list[ConfirmatoryJob]:
    digest = _canonical_sha256(protocol)
    seeds = tuple(int(seed) for seed in protocol["paired_confirmatory_seeds"])
    experiments = int(protocol["complete_experiments_per_run"])
    root = Path(output_dir)
    return [
        ConfirmatoryJob(
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


def build_confirmatory_statistics(
    results: list[dict[str, Any]],
    *,
    protocol: dict[str, Any],
) -> dict[str, Any]:
    primary_protocol = _primary_statistics_protocol(protocol)
    primary = build_primary_statistics(copy.deepcopy(results), protocol=primary_protocol)
    primary["schema_version"] = STATISTICS_SCHEMA_VERSION
    primary["evidence_scope"] = "untouched_cohort_safe_gp_core_four_slice"
    primary["confirmatory_protocol_id"] = protocol["protocol_id"]

    rule = protocol["primary_comparison"]["constraint_rule"]
    secondary = protocol["secondary_comparison"]
    secondary_constraints = paired_constraint_decisions(
        results,
        task_ids=tuple(str(task) for task in protocol["tasks"]),
        candidate=str(secondary["candidate_method"]),
        comparator=str(secondary["comparator"]),
        paired_seeds=tuple(int(seed) for seed in protocol["paired_confirmatory_seeds"]),
        bootstrap_samples=int(rule["bootstrap_samples"]),
        upper_quantile=float(rule["simultaneous_upper_quantile"]),
        safety_margin=float(rule["safety_absolute_noninferiority_margin"]),
        cost_margin=float(rule["cost_relative_noninferiority_margin"]),
    )
    primary["secondary_safe_vs_unconstrained_gp"] = {
        "confirmatory_claim": False,
        "purpose": secondary["purpose"],
        "objective_effects": _descriptive_objective_effects(
            results,
            protocol=protocol,
            candidate=str(secondary["candidate_method"]),
            comparator=str(secondary["comparator"]),
        ),
        "constraint_effects": secondary_constraints,
    }
    primary["benchmark_claim_allowed"] = False
    primary["publication_ready"] = False
    return primary


def _run_job(job: ConfirmatoryJob) -> list[dict[str, Any]]:
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
                "safe_policy_confirmatory_protocol_id": job.protocol_id,
                "safe_policy_confirmatory_protocol_sha256": job.protocol_sha256,
                "evaluated_source_commit": job.evaluated_source_commit,
                "evaluation_source_tree_dirty": False,
                "evaluated_complete_experiments": job.complete_experiments,
                "evaluation_budget_steps": job.operation_budget,
                "evaluation_policy": "vnext_risk_cost",
            }
        )
        _validate_result(result, job)
    return results


def _validate_result(result: dict[str, Any], job: ConfirmatoryJob) -> None:
    if result.get("result_schema_version") != "chemworld-evaluation-result-0.3":
        raise RuntimeError(f"{job.task_id}/{job.method_id} emitted the wrong result schema")
    if result.get("verified") is not True:
        raise RuntimeError(f"{job.task_id}/{job.method_id} failed replay verification")
    usage = result.get("resource_usage", {})
    if int(usage.get("complete_experiment_count", -1)) != job.complete_experiments:
        raise RuntimeError(f"{job.task_id}/{job.method_id} has an incomplete experiment budget")
    if usage.get("method_ledger", {}).get("accounting_complete") is not True:
        raise RuntimeError(f"{job.task_id}/{job.method_id} has an incomplete resource ledger")


def _primary_statistics_protocol(protocol: dict[str, Any]) -> dict[str, Any]:
    primary = protocol["primary_comparison"]
    objective = primary["objective_rule"]
    constraints = primary["constraint_rule"]
    return {
        "task_roles": {"core": protocol["tasks"]},
        "primary_comparison": {
            "candidate_method": primary["candidate_method"],
            "comparator": primary["comparator"],
            "paired_confirmatory_seeds": protocol["paired_confirmatory_seeds"],
            "complete_experiments_per_run": protocol["complete_experiments_per_run"],
            "decision_rule": {
                "deterministic_bootstrap_samples": objective["deterministic_bootstrap_samples"],
                "holm_adjusted_alpha": objective["holm_familywise_alpha"],
                "constraint_noninferiority": {
                    "upper_quantile": constraints["simultaneous_upper_quantile"],
                    "safety": {
                        "maximum_noninferiority_margin": constraints[
                            "safety_absolute_noninferiority_margin"
                        ]
                    },
                    "cost": {
                        "maximum_noninferiority_margin": constraints[
                            "cost_relative_noninferiority_margin"
                        ]
                    },
                },
            },
        },
        "sesoi": protocol["sesoi"],
    }


def _descriptive_objective_effects(
    results: list[dict[str, Any]],
    *,
    protocol: dict[str, Any],
    candidate: str,
    comparator: str,
) -> dict[str, Any]:
    cards: dict[str, Any] = {}
    for task_id in protocol["tasks"]:
        metric = PRIMARY_METRIC_FIELDS[str(task_id)]
        indexed = {
            (str(row["baseline_agent"]), int(row["seed"])): row
            for row in results
            if row["task_id"] == task_id
        }
        effects = [
            float(indexed[(candidate, int(seed))][metric])
            - float(indexed[(comparator, int(seed))][metric])
            for seed in protocol["paired_confirmatory_seeds"]
        ]
        cards[str(task_id)] = {
            "primary_metric": metric,
            "paired_effects": effects,
            "mean_paired_effect": statistics.fmean(effects),
            "sample_sd": statistics.stdev(effects),
        }
    return cards


def _validate_protocol(protocol: dict[str, Any]) -> None:
    if protocol.get("schema_version") != "chemworld-safe-policy-confirmatory-freeze-0.1":
        raise ValueError("unsupported safe-policy confirmatory protocol")
    if protocol.get("status") != "frozen_before_evaluation":
        raise ValueError("confirmatory protocol must be frozen before evaluation")
    if protocol.get("benchmark_claim_allowed") is not False:
        raise ValueError("the slice protocol cannot claim full benchmark completion")
    seeds = {int(seed) for seed in protocol.get("paired_confirmatory_seeds", ())}
    used = {
        int(seed)
        for cohort in protocol.get("previously_used_seeds", {}).values()
        for seed in cohort
    }
    if len(seeds) != 20 or seeds & used:
        raise ValueError("confirmatory seeds must be 20 unique untouched values")
    if protocol.get("methods") != [
        "structured_safe_gp_bo",
        "structured_gp_bo",
        "random",
    ]:
        raise ValueError("confirmatory method order or membership changed")
    if protocol["policy_identity"].get("recipe_space_version") != (
        "chemworld-task-recipe-space-0.2"
    ):
        raise ValueError("confirmatory policy must use recipe space 0.2")
    for relative, expected in protocol["policy_identity"]["source_sha256"].items():
        actual = hashlib.sha256((configuration_root().parent / relative).read_bytes()).hexdigest()
        if actual != expected:
            raise ValueError(f"frozen policy source changed: {relative}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("runs/benchmark-vnext/safe-policy-confirmatory-0.1"),
    )
    parser.add_argument("--protocol", type=Path, default=DEFAULT_PROTOCOL)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.workers < 1:
        raise ValueError("workers must be positive")
    protocol = load_confirmatory_protocol(args.protocol)
    evaluated_commit = git_commit()
    if evaluated_commit is None:
        raise RuntimeError("confirmatory runs require a Git commit")
    jobs = build_confirmatory_jobs(
        protocol,
        output_dir=args.output_dir,
        evaluated_source_commit=evaluated_commit,
    )
    if args.dry_run:
        print(json.dumps([asdict(job) for job in jobs], indent=2, sort_keys=True))
        return 0
    if _tracked_tree_dirty():
        raise RuntimeError("confirmatory runs require a clean tracked tree")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    all_results: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    with ProcessPoolExecutor(max_workers=min(args.workers, len(jobs))) as executor:
        future_jobs = {executor.submit(_run_job, job): job for job in jobs}
        for future in as_completed(future_jobs):
            job = future_jobs[future]
            try:
                all_results.extend(future.result())
            except Exception as exc:  # pragma: no cover - real runtime failure capture
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
        key=lambda row: (str(row["task_id"]), str(row["baseline_agent"]), int(row["seed"]))
    )
    _write_json(args.output_dir / "confirmatory_results.json", all_results)
    statistics_payload = None
    if not failures:
        statistics_payload = build_confirmatory_statistics(all_results, protocol=protocol)
        _write_json(args.output_dir / "confirmatory_statistics.json", statistics_payload)
    manifest = {
        "schema_version": RUN_SCHEMA_VERSION,
        "status": "completed" if not failures else "failed_with_retained_failures",
        "generated_at": datetime.now(UTC).isoformat(),
        "world_role": protocol["world_role"],
        "protocol_id": protocol["protocol_id"],
        "protocol_sha256": _canonical_sha256(protocol),
        "evaluated_source_commit": evaluated_commit,
        "evaluation_source_tree_dirty": False,
        "jobs": [asdict(job) for job in jobs],
        "result_count": len(all_results),
        "expected_result_count": sum(len(job.seeds) for job in jobs),
        "failures": failures,
        "confirmatory_results_sha256": _sha256(args.output_dir / "confirmatory_results.json"),
        "confirmatory_statistics_sha256": (
            _sha256(args.output_dir / "confirmatory_statistics.json")
            if statistics_payload is not None
            else None
        ),
        "benchmark_claim_allowed": False,
        "publication_ready": False,
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


def _canonical_sha256(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return hashlib.sha256(encoded.encode()).hexdigest()


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


if __name__ == "__main__":
    raise SystemExit(main())
