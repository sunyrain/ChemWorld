"""Independently replay-audit a safe-policy development bundle."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.run_safe_policy_development import (  # noqa: E402
    build_development_summary,
    load_development_protocol,
)

from chemworld.data.logging import load_jsonl  # noqa: E402
from chemworld.eval.result_artifacts import (  # noqa: E402
    validate_verified_evaluation_result,
)

AUDIT_VERSION = "chemworld-safe-policy-development-audit-0.1"


def audit_development_bundle(
    run_root: str | Path,
    *,
    workers: int = 4,
) -> dict[str, Any]:
    if workers < 1:
        raise ValueError("workers must be positive")
    root = Path(run_root).resolve()
    manifest_path = root / "manifest.json"
    results_path = root / "development_results.json"
    summary_path = root / "development_summary.json"
    manifest = _load_json(manifest_path)
    results = _load_json(results_path)
    saved_summary = _load_json(summary_path)
    protocol = load_development_protocol()
    if not isinstance(results, list):
        raise ValueError("development_results.json must contain a list")
    _validate_manifest(manifest, protocol=protocol, result_count=len(results))

    expected = {
        (str(task), str(method), int(seed))
        for task in protocol["tasks"]
        for method in protocol["methods"]
        for seed in protocol["dev_seeds"]
    }
    actual = [
        (str(row.get("task_id")), str(row.get("baseline_agent")), int(row.get("seed", -1)))
        for row in results
    ]
    if len(set(actual)) != len(actual) or set(actual) != expected:
        raise ValueError("development result matrix is duplicate, missing, or unexpected")

    rebound: list[dict[str, Any]] = []
    for result in results:
        _validate_result_contract(result, manifest=manifest, protocol=protocol)
        item = copy.deepcopy(result)
        task_id = str(result["task_id"])
        method_id = str(result["baseline_agent"])
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
        _validate_agent_contract(
            trajectory,
            method_id=method_id,
            protocol=protocol,
        )
        item["trajectory_path"] = str(trajectory.resolve())
        rebound.append(item)

    with ProcessPoolExecutor(max_workers=min(workers, len(rebound))) as executor:
        digests = list(executor.map(_replay_one, rebound))
    if len(set(digests)) != len(digests):
        raise ValueError("development bundle reuses a trajectory digest")

    recomputed = build_development_summary(copy.deepcopy(results), protocol=protocol)
    if _canonical_json(saved_summary) != _canonical_json(recomputed):
        raise ValueError("development summary does not match deterministic recomputation")
    audited = copy.deepcopy(saved_summary)
    audited["integrity"] = {
        "schema_version": AUDIT_VERSION,
        "result_count": len(results),
        "distinct_trajectory_count": len(set(digests)),
        "all_results_replayed": True,
        "all_resource_ledgers_complete": True,
        "all_runs_complete_experiments": int(protocol["complete_experiments_per_run"]),
        "job_failures": 0,
        "statistics_deterministically_recomputed": True,
        "safe_agent_contract_verified": True,
        "recipe_space_version_verified": protocol["recipe_space_version"],
        "evaluated_source_commit": manifest["evaluated_source_commit"],
        "manifest_sha256": _sha256(manifest_path),
        "development_results_sha256": _sha256(results_path),
        "development_summary_sha256": _sha256(summary_path),
    }
    return audited


def _validate_manifest(
    manifest: dict[str, Any],
    *,
    protocol: dict[str, Any],
    result_count: int,
) -> None:
    required = {
        "schema_version": "chemworld-safe-policy-development-run-0.1",
        "status": "completed",
        "protocol_id": protocol["protocol_id"],
        "protocol_sha256": _canonical_sha256(protocol),
        "world_role": "dev",
        "result_count": result_count,
        "expected_result_count": result_count,
        "failures": [],
        "benchmark_claim_allowed": False,
        "publication_ready": False,
    }
    mismatches = {
        key: {"expected": expected, "actual": manifest.get(key)}
        for key, expected in required.items()
        if manifest.get(key) != expected
    }
    if mismatches:
        raise ValueError(f"development manifest mismatch: {mismatches}")
    source_commit = manifest.get("evaluated_source_commit")
    if not isinstance(source_commit, str) or len(source_commit) != 40:
        raise ValueError("development manifest lacks a source commit")


def _validate_result_contract(
    result: dict[str, Any],
    *,
    manifest: dict[str, Any],
    protocol: dict[str, Any],
) -> None:
    if result.get("result_schema_version") != "chemworld-evaluation-result-0.3":
        raise ValueError("development result uses the wrong result schema")
    if result.get("verified") is not True:
        raise ValueError("development result is not replay verified")
    if result.get("safe_policy_development_protocol_id") != protocol["protocol_id"]:
        raise ValueError("development result uses the wrong protocol")
    if result.get("safe_policy_development_protocol_sha256") != manifest["protocol_sha256"]:
        raise ValueError("development result protocol digest mismatch")
    if result.get("evaluated_source_commit") != manifest["evaluated_source_commit"]:
        raise ValueError("development result source commit mismatch")
    if result.get("evaluation_source_tree_dirty") is not False:
        raise ValueError("development result came from a dirty tracked tree")
    usage = result.get("resource_usage", {})
    if int(usage.get("complete_experiment_count", -1)) != int(
        protocol["complete_experiments_per_run"]
    ):
        raise ValueError("development result has an incomplete experiment budget")
    if usage.get("method_ledger", {}).get("accounting_complete") is not True:
        raise ValueError("development result has an incomplete resource ledger")


def _replay_one(result: dict[str, Any]) -> str:
    validate_verified_evaluation_result(result, replay=True)
    return str(result["trajectory_sha256"])


def _validate_agent_contract(
    trajectory: Path,
    *,
    method_id: str,
    protocol: dict[str, Any],
) -> None:
    records = load_jsonl(trajectory)
    metadata = records[0].get("agent_metadata", {})
    if method_id == "structured_safe_gp_bo":
        contract = protocol["safe_policy_contract"]
        required = {
            "risk_observation": contract["risk_label"],
            "risk_confidence_beta": contract["risk_confidence_beta"],
            "initial_design": contract["initial_design"],
            "recipe_encoding": "continuous_plus_material_one_hot",
        }
        mismatches = {
            key: {"expected": expected, "actual": metadata.get(key)}
            for key, expected in required.items()
            if metadata.get(key) != expected
        }
        if mismatches:
            raise ValueError(f"safe-agent contract mismatch in {trajectory}: {mismatches}")
    if method_id not in {"structured_safe_gp_bo", "structured_gp_bo"}:
        return
    trace = records[-1].get("agent_trace", [])
    decisions = [
        item
        for item in trace
        if isinstance(item, dict) and item.get("trace_type") == "surrogate_recipe_decision"
    ]
    if len(decisions) != int(protocol["complete_experiments_per_run"]):
        raise ValueError(f"surrogate decision trace is incomplete in {trajectory}")
    if any(
        item.get("selected_recipe", {}).get("metadata", {}).get("search_space_version")
        != protocol["recipe_space_version"]
        for item in decisions
    ):
        raise ValueError(f"recipe-space version mismatch in {trajectory}")
    if method_id == "structured_safe_gp_bo":
        acquisition = [item for item in decisions if item.get("phase") == "acquisition"]
        if not acquisition or any(
            item.get("decision_diagnostics", {}).get("risk_label")
            != protocol["safe_policy_contract"]["risk_label"]
            for item in acquisition
        ):
            raise ValueError(f"safe acquisition diagnostics are incomplete in {trajectory}")


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
    report = audit_development_bundle(args.run_root, workers=args.workers)
    _write_json(args.output, report)
    print(
        json.dumps(
            {
                "result_count": report["integrity"]["result_count"],
                "all_results_replayed": report["integrity"]["all_results_replayed"],
                "selected_for_future_freeze": report["selected_for_future_freeze"],
                "benchmark_claim_allowed": report["benchmark_claim_allowed"],
                "output": str(args.output),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
