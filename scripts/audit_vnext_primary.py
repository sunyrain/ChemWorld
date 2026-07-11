"""Independently audit and summarize a completed vNext classical primary run."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import statistics
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.run_vnext_primary import build_primary_statistics  # noqa: E402

from chemworld.eval.benchmark_validation import PRIMARY_METRIC_FIELDS  # noqa: E402
from chemworld.eval.confirmatory_freeze import (  # noqa: E402
    audit_confirmatory_freeze,
    load_confirmatory_freeze,
)
from chemworld.eval.result_artifacts import (  # noqa: E402
    validate_verified_evaluation_result,
)

AUDIT_SCHEMA_VERSION = "chemworld-vnext-primary-evidence-0.1"
EXPECTED_RESULT_SCHEMA_VERSION = "chemworld-evaluation-result-0.3"
EXPECTED_RUN_SCHEMA_VERSION = "chemworld-vnext-primary-run-0.1"


def audit_primary_run(
    run_root: str | Path,
    *,
    replay: bool = True,
    workers: int = 4,
) -> dict[str, Any]:
    """Validate a run bundle and return a compact, non-overclaiming evidence record."""

    if workers < 1:
        raise ValueError("workers must be positive")
    root = Path(run_root).resolve()
    manifest_path = root / "manifest.json"
    results_path = root / "primary_results.json"
    statistics_path = root / "primary_statistics.json"
    manifest = _load_json(manifest_path)
    results = _load_json(results_path)
    recorded_statistics = _load_json(statistics_path)
    if not isinstance(results, list):
        raise ValueError("primary_results.json must contain a list")

    protocol = load_confirmatory_freeze()
    protocol_audit = audit_confirmatory_freeze(protocol)
    _validate_manifest(
        manifest,
        result_count=len(results),
        result_digest=_sha256(results_path),
        statistics_digest=_sha256(statistics_path),
        protocol=protocol,
        protocol_digest=str(protocol_audit["protocol_sha256"]),
    )
    expected_keys = _expected_result_keys(protocol)
    actual_keys = [_result_key(row) for row in results]
    if len(set(actual_keys)) != len(actual_keys):
        raise ValueError("primary result matrix contains duplicate task/method/seed rows")
    if set(actual_keys) != expected_keys:
        missing = sorted(expected_keys.difference(actual_keys))
        unexpected = sorted(set(actual_keys).difference(expected_keys))
        raise ValueError(
            f"primary result matrix does not match the freeze; missing={missing}, "
            f"unexpected={unexpected}"
        )

    replay_inputs: list[dict[str, Any]] = []
    for result in results:
        _validate_result_contract(result, manifest=manifest, protocol=protocol)
        rebound = copy.deepcopy(result)
        trajectory = _portable_trajectory_path(root, result)
        rebound["trajectory_path"] = str(trajectory)
        replay_inputs.append(rebound)

    if replay:
        with ProcessPoolExecutor(max_workers=min(workers, len(replay_inputs))) as executor:
            replay_digests = list(executor.map(_replay_one, replay_inputs))
    else:
        replay_digests = [_integrity_one(result) for result in replay_inputs]
    if len(set(replay_digests)) != len(replay_digests):
        raise ValueError("primary result matrix reuses a trajectory digest")

    recomputed_statistics = build_primary_statistics(copy.deepcopy(results), protocol=protocol)
    if not _json_equal(recorded_statistics, recomputed_statistics):
        raise ValueError("primary statistics do not match deterministic recomputation")

    return _build_summary(
        manifest=manifest,
        results=results,
        recorded_statistics=recorded_statistics,
        replay=replay,
        distinct_trajectory_count=len(set(replay_digests)),
    )


def _validate_manifest(
    manifest: dict[str, Any],
    *,
    result_count: int,
    result_digest: str,
    statistics_digest: str,
    protocol: dict[str, Any],
    protocol_digest: str,
) -> None:
    required = {
        "schema_version": EXPECTED_RUN_SCHEMA_VERSION,
        "status": "completed",
        "formal_slice": "primary_classical_only",
        "confirmatory_protocol_id": protocol["protocol_id"],
        "confirmatory_protocol_sha256": protocol_digest,
        "result_count": result_count,
        "expected_result_count": result_count,
        "primary_results_sha256": result_digest,
        "primary_statistics_sha256": statistics_digest,
        "benchmark_claim_allowed": False,
        "publication_ready": False,
    }
    mismatches = {
        key: {"expected": expected, "actual": manifest.get(key)}
        for key, expected in required.items()
        if manifest.get(key) != expected
    }
    if mismatches:
        raise ValueError(f"primary run manifest mismatch: {mismatches}")
    if manifest.get("failures") != []:
        raise ValueError("primary run manifest retains failures")
    source_commit = manifest.get("evaluated_source_commit")
    if not isinstance(source_commit, str) or len(source_commit) != 40:
        raise ValueError("primary run manifest lacks a full evaluated source commit")
    if manifest.get("evaluation_source_tree_dirty") is not False:
        raise ValueError("primary run was not produced from a clean tracked tree")


def _validate_result_contract(
    result: dict[str, Any],
    *,
    manifest: dict[str, Any],
    protocol: dict[str, Any],
) -> None:
    task_id, method_id, seed = _result_key(result)
    if result.get("result_schema_version") != EXPECTED_RESULT_SCHEMA_VERSION:
        raise ValueError(f"{task_id}/{method_id}/seed{seed} uses the wrong result schema")
    if result.get("verified") is not True:
        raise ValueError(f"{task_id}/{method_id}/seed{seed} is not replay verified")
    if result.get("evaluation_policy") != "vnext_risk_cost":
        raise ValueError(f"{task_id}/{method_id}/seed{seed} is not risk-policy bound")
    if result.get("confirmatory_protocol_id") != protocol["protocol_id"]:
        raise ValueError(f"{task_id}/{method_id}/seed{seed} uses the wrong protocol")
    if result.get("confirmatory_protocol_sha256") != manifest["confirmatory_protocol_sha256"]:
        raise ValueError(f"{task_id}/{method_id}/seed{seed} has a protocol digest mismatch")
    if result.get("evaluated_source_commit") != manifest["evaluated_source_commit"]:
        raise ValueError(f"{task_id}/{method_id}/seed{seed} has a source commit mismatch")
    if result.get("evaluation_source_tree_dirty") is not False:
        raise ValueError(f"{task_id}/{method_id}/seed{seed} came from a dirty tree")
    expected_experiments = int(protocol["primary_comparison"]["complete_experiments_per_run"])
    usage = result.get("resource_usage", {})
    ledger = usage.get("method_ledger", {})
    if int(usage.get("complete_experiment_count", -1)) != expected_experiments:
        raise ValueError(f"{task_id}/{method_id}/seed{seed} has an incomplete experiment budget")
    if ledger.get("accounting_complete") is not True:
        raise ValueError(f"{task_id}/{method_id}/seed{seed} has an incomplete resource ledger")
    contract = result.get("score_replay", {}).get("task_evaluation_contract", {})
    if contract.get("risk_limit_semantics") != "benchmark_operational_risk_budget":
        raise ValueError(f"{task_id}/{method_id}/seed{seed} lacks operational-risk semantics")


def _build_summary(
    *,
    manifest: dict[str, Any],
    results: list[dict[str, Any]],
    recorded_statistics: dict[str, Any],
    replay: bool,
    distinct_trajectory_count: int,
) -> dict[str, Any]:
    cells: dict[str, Any] = {}
    for task_id in sorted({str(row["task_id"]) for row in results}):
        metric = PRIMARY_METRIC_FIELDS[task_id]
        cells[task_id] = {}
        for method_id in sorted(
            {str(row["baseline_agent"]) for row in results if row["task_id"] == task_id}
        ):
            rows = [
                row
                for row in results
                if row["task_id"] == task_id and row["baseline_agent"] == method_id
            ]
            values = [float(row[metric]) for row in rows]
            constraints = [row["score_replay"]["layered_evaluation"]["constraints"] for row in rows]
            resources = [row["score_replay"]["layered_evaluation"]["resources"] for row in rows]
            cells[task_id][method_id] = {
                "run_count": len(rows),
                "primary_metric": metric,
                "primary_metric_mean": statistics.fmean(values),
                "primary_metric_sample_sd": (
                    statistics.stdev(values) if len(values) > 1 else None
                ),
                "complete_experiment_count": sum(
                    int(item["complete_experiment_count"]) for item in resources
                ),
                "operation_count": sum(int(item["operation_count"]) for item in resources),
                "campaign_total_cost": sum(
                    float(item["campaign_total_cost"]) for item in resources
                ),
                "risk_budget_exceedance_count": sum(
                    int(item["risk_budget_exceedance_count"]) for item in constraints
                ),
                "risk_budget_exceedance_rate": (
                    sum(int(item["risk_budget_exceedance_count"]) for item in constraints)
                    / sum(int(item["complete_experiment_count"]) for item in resources)
                ),
            }
    tradeoffs = {
        task_id: {
            "candidate_minus_comparator_risk_exceedance_rate": (
                methods["structured_gp_bo"]["risk_budget_exceedance_rate"]
                - methods["random"]["risk_budget_exceedance_rate"]
            ),
            "candidate_minus_comparator_cost_per_experiment": (
                methods["structured_gp_bo"]["campaign_total_cost"]
                / methods["structured_gp_bo"]["complete_experiment_count"]
                - methods["random"]["campaign_total_cost"]
                / methods["random"]["complete_experiment_count"]
            ),
            "candidate_has_higher_observed_risk_exceedance_rate": (
                methods["structured_gp_bo"]["risk_budget_exceedance_rate"]
                > methods["random"]["risk_budget_exceedance_rate"]
            ),
        }
        for task_id, methods in cells.items()
    }
    objective_rule_passed = bool(recorded_statistics["all_task_joint_rule_passed"])
    return {
        "schema_version": AUDIT_SCHEMA_VERSION,
        "status": "audited",
        "evidence_scope": "frozen_primary_classical_slice_only",
        "source": {
            "run_schema_version": manifest["schema_version"],
            "run_generated_at": manifest["generated_at"],
            "evaluated_source_commit": manifest["evaluated_source_commit"],
            "confirmatory_protocol_id": manifest["confirmatory_protocol_id"],
            "confirmatory_protocol_sha256": manifest["confirmatory_protocol_sha256"],
            "primary_results_sha256": manifest["primary_results_sha256"],
            "primary_statistics_sha256": manifest["primary_statistics_sha256"],
        },
        "integrity": {
            "result_count": len(results),
            "distinct_trajectory_count": distinct_trajectory_count,
            "all_results_integrity_checked": True,
            "all_results_replayed": replay,
            "all_resource_ledgers_complete": True,
            "all_runs_complete_experiments": 40,
            "all_runs_risk_policy_bound": True,
            "statistics_deterministically_recomputed": True,
            "job_failures": 0,
        },
        "comparison": {
            "candidate": "structured_gp_bo",
            "comparator": "random",
            "paired_seed_count_per_task": 20,
            "task_decisions": recorded_statistics["task_decisions"],
            "all_task_objective_rule_passed": objective_rule_passed,
            "safety_noninferiority_rule_prespecified": False,
            "cost_noninferiority_rule_prespecified": False,
            "complete_primary_rule_passed": False,
            "cross_task_performance_score": None,
        },
        "diagnostics": {
            "task_method_cells": cells,
            "candidate_comparator_tradeoffs": tradeoffs,
            "higher_candidate_risk_task_count": sum(
                int(card["candidate_has_higher_observed_risk_exceedance_rate"])
                for card in tradeoffs.values()
            ),
        },
        "claim_boundary": {
            "objective_only_slice_supported": bool(replay and objective_rule_passed),
            "primary_classical_slice_supported": False,
            "benchmark_claim_allowed": False,
            "publication_ready": False,
            "independent_reproduction_complete": False,
            "full_cross_family_matrix_complete": False,
            "evaluation_design_issue_detected": True,
            "required_protocol_upgrade": (
                "Pre-register paired task-level safety and cost noninferiority margins, include "
                "them in the joint decision rule, and collect a new untouched seed cohort."
            ),
            "missing_families": [
                "full_budget_ppo",
                "full_budget_sac",
                "live_llm_pro",
                "live_llm_flash",
            ],
            "interpretation": (
                "The frozen structured-GP versus random comparison passes its objective-only "
                "rule, but the protocol omitted pre-specified safety and cost noninferiority "
                "gates. Observed risk-budget exceedance rates are higher for the candidate in "
                "three of four tasks, so this run is diagnostic and cannot support the complete "
                "primary classical claim."
            ),
        },
    }


def _expected_result_keys(protocol: dict[str, Any]) -> set[tuple[str, str, int]]:
    primary = protocol["primary_comparison"]
    return {
        (str(task_id), str(method_id), int(seed))
        for task_id in protocol["task_roles"]["core"]
        for method_id in (primary["candidate_method"], primary["comparator"])
        for seed in primary["paired_confirmatory_seeds"]
    }


def _result_key(result: dict[str, Any]) -> tuple[str, str, int]:
    return (
        str(result.get("task_id")),
        str(result.get("baseline_agent")),
        int(result.get("seed", -1)),
    )


def _portable_trajectory_path(root: Path, result: dict[str, Any]) -> Path:
    task_id, method_id, _ = _result_key(result)
    raw_path = result.get("trajectory_path")
    if not isinstance(raw_path, str) or not raw_path:
        raise ValueError(f"{task_id}/{method_id} result lacks a trajectory path")
    path = root / "runs" / task_id / method_id / "trajectories" / Path(raw_path).name
    if not path.is_file():
        raise ValueError(f"portable trajectory is missing: {path}")
    return path.resolve()


def _replay_one(result: dict[str, Any]) -> str:
    validate_verified_evaluation_result(result, replay=True)
    return str(result["trajectory_sha256"])


def _integrity_one(result: dict[str, Any]) -> str:
    validate_verified_evaluation_result(result, replay=False)
    return str(result["trajectory_sha256"])


def _json_equal(left: Any, right: Any) -> bool:
    return json.dumps(left, sort_keys=True, allow_nan=False) == json.dumps(
        right, sort_keys=True, allow_nan=False
    )


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-root", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--integrity-only", action="store_true")
    args = parser.parse_args()
    summary = audit_primary_run(
        args.run_root,
        replay=not args.integrity_only,
        workers=args.workers,
    )
    if args.output is not None:
        _write_json(args.output, summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
