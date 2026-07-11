"""Independently replay-audit the frozen Safe-GP confirmatory bundle."""

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

from scripts.run_safe_policy_confirmatory import (  # noqa: E402
    build_confirmatory_statistics,
    load_confirmatory_protocol,
)

from chemworld.data.logging import load_jsonl  # noqa: E402
from chemworld.eval.benchmark_validation import PRIMARY_METRIC_FIELDS  # noqa: E402
from chemworld.eval.result_artifacts import (  # noqa: E402
    validate_verified_evaluation_result,
)

AUDIT_SCHEMA_VERSION = "chemworld-safe-policy-confirmatory-audit-0.1"


def audit_confirmatory_bundle(
    run_root: str | Path,
    *,
    workers: int = 4,
) -> dict[str, Any]:
    if workers < 1:
        raise ValueError("workers must be positive")
    root = Path(run_root).resolve()
    manifest_path = root / "manifest.json"
    results_path = root / "confirmatory_results.json"
    statistics_path = root / "confirmatory_statistics.json"
    manifest = _load_json(manifest_path)
    results = _load_json(results_path)
    saved_statistics = _load_json(statistics_path)
    protocol = load_confirmatory_protocol()
    if not isinstance(results, list):
        raise ValueError("confirmatory_results.json must contain a list")
    _validate_manifest(
        manifest,
        protocol=protocol,
        result_count=len(results),
        results_sha256=_sha256(results_path),
        statistics_sha256=_sha256(statistics_path),
    )

    expected = {
        (str(task), str(method), int(seed))
        for task in protocol["tasks"]
        for method in protocol["methods"]
        for seed in protocol["paired_confirmatory_seeds"]
    }
    actual = [_result_key(row) for row in results]
    if len(set(actual)) != len(actual) or set(actual) != expected:
        raise ValueError("confirmatory result matrix is duplicate, missing, or unexpected")

    rebound: list[dict[str, Any]] = []
    for result in results:
        _validate_result_contract(result, manifest=manifest, protocol=protocol)
        task_id, method_id, _ = _result_key(result)
        trajectory = (
            root
            / "runs"
            / task_id
            / method_id
            / "trajectories"
            / Path(str(result["trajectory_path"])).name
        )
        if not trajectory.is_file():
            raise ValueError(f"portable trajectory is missing: {trajectory}")
        _validate_agent_contract(trajectory, method_id=method_id, protocol=protocol)
        item = copy.deepcopy(result)
        item["trajectory_path"] = str(trajectory.resolve())
        rebound.append(item)

    with ProcessPoolExecutor(max_workers=min(workers, len(rebound))) as executor:
        digests = list(executor.map(_replay_one, rebound))
    if len(set(digests)) != len(digests):
        raise ValueError("confirmatory bundle reuses a trajectory digest")

    recomputed = build_confirmatory_statistics(copy.deepcopy(results), protocol=protocol)
    if _canonical_json(saved_statistics) != _canonical_json(recomputed):
        raise ValueError("confirmatory statistics do not match deterministic recomputation")
    primary_passed = bool(saved_statistics["all_task_joint_rule_passed"])
    return {
        "schema_version": AUDIT_SCHEMA_VERSION,
        "status": "audited",
        "evidence_scope": "untouched_cohort_safe_gp_core_four_slice",
        "source": {
            "protocol_id": protocol["protocol_id"],
            "protocol_sha256": manifest["protocol_sha256"],
            "evaluated_source_commit": manifest["evaluated_source_commit"],
            "run_generated_at": manifest["generated_at"],
            "manifest_sha256": _sha256(manifest_path),
            "confirmatory_results_sha256": _sha256(results_path),
            "confirmatory_statistics_sha256": _sha256(statistics_path),
        },
        "integrity": {
            "result_count": len(results),
            "distinct_trajectory_count": len(set(digests)),
            "all_results_replayed": True,
            "all_resource_ledgers_complete": True,
            "all_runs_complete_experiments": int(protocol["complete_experiments_per_run"]),
            "agent_and_recipe_contracts_verified": True,
            "recipe_space_version_verified": protocol["policy_identity"][
                "recipe_space_version"
            ],
            "statistics_deterministically_recomputed": True,
            "job_failures": 0,
        },
        "primary_comparison": {
            "candidate": protocol["primary_comparison"]["candidate_method"],
            "comparator": protocol["primary_comparison"]["comparator"],
            "paired_seed_count_per_task": len(protocol["paired_confirmatory_seeds"]),
            "task_decisions": saved_statistics["task_decisions"],
            "all_task_objective_rule_passed": saved_statistics[
                "all_task_objective_rule_passed"
            ],
            "all_task_constraint_rule_passed": saved_statistics[
                "all_task_constraint_rule_passed"
            ],
            "complete_primary_rule_passed": primary_passed,
        },
        "secondary_comparison": saved_statistics["secondary_safe_vs_unconstrained_gp"],
        "diagnostics": {"task_method_cells": _task_method_cells(results, protocol=protocol)},
        "claim_boundary": {
            "confirmatory_slice_supported": primary_passed,
            "benchmark_claim_allowed": False,
            "publication_ready": False,
            "independent_external_reproduction_complete": False,
            "full_cross_family_matrix_complete": False,
            "interpretation": (
                "The frozen Safe-GP versus random core-four slice passed every prespecified "
                "objective, safety, and cost rule."
                if primary_passed
                else "The frozen Safe-GP versus random core-four slice failed at least one "
                "prespecified objective, safety, or cost rule."
            ),
        },
    }


def _validate_manifest(
    manifest: dict[str, Any],
    *,
    protocol: dict[str, Any],
    result_count: int,
    results_sha256: str,
    statistics_sha256: str,
) -> None:
    required = {
        "schema_version": "chemworld-safe-policy-confirmatory-run-0.1",
        "status": "completed",
        "world_role": "bench_confirmation",
        "protocol_id": protocol["protocol_id"],
        "protocol_sha256": _canonical_sha256(protocol),
        "result_count": result_count,
        "expected_result_count": result_count,
        "failures": [],
        "confirmatory_results_sha256": results_sha256,
        "confirmatory_statistics_sha256": statistics_sha256,
        "benchmark_claim_allowed": False,
        "publication_ready": False,
    }
    mismatches = {
        key: {"expected": expected, "actual": manifest.get(key)}
        for key, expected in required.items()
        if manifest.get(key) != expected
    }
    if mismatches:
        raise ValueError(f"confirmatory manifest mismatch: {mismatches}")
    source_commit = manifest.get("evaluated_source_commit")
    if not isinstance(source_commit, str) or len(source_commit) != 40:
        raise ValueError("confirmatory manifest lacks a source commit")


def _validate_result_contract(
    result: dict[str, Any],
    *,
    manifest: dict[str, Any],
    protocol: dict[str, Any],
) -> None:
    if result.get("result_schema_version") != "chemworld-evaluation-result-0.3":
        raise ValueError("confirmatory result uses the wrong result schema")
    if result.get("verified") is not True:
        raise ValueError("confirmatory result is not replay verified")
    if result.get("safe_policy_confirmatory_protocol_id") != protocol["protocol_id"]:
        raise ValueError("confirmatory result uses the wrong protocol")
    if result.get("safe_policy_confirmatory_protocol_sha256") != manifest["protocol_sha256"]:
        raise ValueError("confirmatory result protocol digest mismatch")
    if result.get("evaluated_source_commit") != manifest["evaluated_source_commit"]:
        raise ValueError("confirmatory result source commit mismatch")
    if result.get("evaluation_source_tree_dirty") is not False:
        raise ValueError("confirmatory result came from a dirty tracked tree")
    usage = result.get("resource_usage", {})
    if int(usage.get("complete_experiment_count", -1)) != int(
        protocol["complete_experiments_per_run"]
    ):
        raise ValueError("confirmatory result has an incomplete experiment budget")
    if usage.get("method_ledger", {}).get("accounting_complete") is not True:
        raise ValueError("confirmatory result has an incomplete resource ledger")


def _validate_agent_contract(
    trajectory: Path,
    *,
    method_id: str,
    protocol: dict[str, Any],
) -> None:
    if method_id == "random":
        return
    records = load_jsonl(trajectory)
    metadata = records[0].get("agent_metadata", {})
    identity = protocol["policy_identity"]
    common = {
        "recipe_encoding": "continuous_plus_material_one_hot",
        "search_space_version": identity["recipe_space_version"],
    }
    required = dict(common)
    if method_id == "structured_safe_gp_bo":
        required.update(
            {
                "risk_observation": identity["risk_label"],
                "risk_confidence_beta": identity["risk_confidence_beta"],
                "initial_design": identity["initial_design"],
            }
        )
    mismatches = {
        key: {"expected": expected, "actual": metadata.get(key)}
        for key, expected in required.items()
        if metadata.get(key) != expected
    }
    if mismatches:
        raise ValueError(f"agent contract mismatch in {trajectory}: {mismatches}")
    decisions = [
        item
        for item in records[-1].get("agent_trace", [])
        if isinstance(item, dict) and item.get("trace_type") == "surrogate_recipe_decision"
    ]
    if len(decisions) != int(protocol["complete_experiments_per_run"]):
        raise ValueError(f"surrogate decision trace is incomplete in {trajectory}")
    if any(
        item.get("selected_recipe", {}).get("metadata", {}).get("search_space_version")
        != identity["recipe_space_version"]
        for item in decisions
    ):
        raise ValueError(f"recipe-space version mismatch in {trajectory}")
    if method_id == "structured_safe_gp_bo":
        acquisition = [item for item in decisions if item.get("phase") == "acquisition"]
        if not acquisition or any(
            item.get("decision_diagnostics", {}).get("risk_label") != identity["risk_label"]
            for item in acquisition
        ):
            raise ValueError(f"safe acquisition diagnostics are incomplete in {trajectory}")


def _task_method_cells(
    results: list[dict[str, Any]], *, protocol: dict[str, Any]
) -> dict[str, Any]:
    cells: dict[str, Any] = {}
    for task_id in protocol["tasks"]:
        metric = PRIMARY_METRIC_FIELDS[str(task_id)]
        cells[str(task_id)] = {}
        for method_id in protocol["methods"]:
            rows = [
                row
                for row in results
                if row["task_id"] == task_id and row["baseline_agent"] == method_id
            ]
            risks = [
                float(
                    row["score_replay"]["layered_evaluation"]["constraints"][
                        "risk_budget_exceedance_rate"
                    ]
                )
                for row in rows
            ]
            costs = [
                float(row["score_replay"]["layered_evaluation"]["resources"]["campaign_total_cost"])
                / int(
                    row["score_replay"]["layered_evaluation"]["resources"][
                        "complete_experiment_count"
                    ]
                )
                for row in rows
            ]
            values = [float(row[metric]) for row in rows]
            cells[str(task_id)][str(method_id)] = {
                "run_count": len(rows),
                "primary_metric": metric,
                "primary_metric_mean": statistics.fmean(values),
                "primary_metric_sample_sd": statistics.stdev(values),
                "risk_exceedance_rate_mean": statistics.fmean(risks),
                "cost_per_experiment_mean": statistics.fmean(costs),
            }
    return cells


def _result_key(result: dict[str, Any]) -> tuple[str, str, int]:
    return (
        str(result.get("task_id")),
        str(result.get("baseline_agent")),
        int(result.get("seed", -1)),
    )


def _replay_one(result: dict[str, Any]) -> str:
    validate_verified_evaluation_result(result, replay=True)
    return str(result["trajectory_sha256"])


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _canonical_json(payload: Any) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False)


def _canonical_sha256(payload: Any) -> str:
    return hashlib.sha256(_canonical_json(payload).encode()).hexdigest()


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()
    report = audit_confirmatory_bundle(args.run_root, workers=args.workers)
    _write_json(args.output, report)
    print(
        json.dumps(
            {
                "result_count": report["integrity"]["result_count"],
                "all_results_replayed": report["integrity"]["all_results_replayed"],
                "confirmatory_slice_supported": report["claim_boundary"][
                    "confirmatory_slice_supported"
                ],
                "benchmark_claim_allowed": report["claim_boundary"][
                    "benchmark_claim_allowed"
                ],
                "output": str(args.output),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
