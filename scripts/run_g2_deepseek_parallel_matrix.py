"""Run the frozen five-pair G2 DeepSeek parallel agent-system matrix."""

from __future__ import annotations

import argparse
import json
import os
from collections.abc import Mapping, Sequence
from concurrent.futures import ThreadPoolExecutor, as_completed
from copy import deepcopy
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from scripts import run_g2_autonomous_material_matrix as matrix

from chemworld.eval.provenance import (
    canonical_json_sha256,
    file_sha256,
    repository_tree_sha256,
    write_json_atomic,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = (
    ROOT / "configs/benchmark/g2_autonomous_electrochemical_material_5x2_deepseek_v0.4_dev.json"
)
DEFAULT_OUTPUT_ROOT = ROOT / "runs/development/g2-autonomous-material-5x2-deepseek-v4-flash-v4"
RUNNER_VERSION = "chemworld-g2-deepseek-parallel-matrix-runner-0.1"
MANIFEST_SCHEMA_VERSION = "chemworld-g2-parallel-agent-matrix-run-0.1"


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _load_protocol(path: Path) -> dict[str, Any]:
    protocol = matrix._load_protocol(path)
    parallel = protocol.get("parallel_execution")
    agent = protocol.get("agent")
    if not isinstance(parallel, Mapping) or not isinstance(agent, Mapping):
        raise ValueError("DeepSeek parallel protocol requires agent and parallel_execution")
    if agent.get("model") != "deepseek-v4-flash":
        raise ValueError("parallel protocol must freeze model=deepseek-v4-flash")
    attempt_limit = int(agent.get("provider_max_attempts", 0))
    if attempt_limit != 3 or agent.get("provider_attempt_limit_per_operation") != 3:
        raise ValueError("three fail-closed provider attempts per operation must be frozen")
    operation_limit = int(protocol["campaign_resource_card"]["operation_attempt_limit"])
    if int(protocol["method_resource_limits_per_cell"]["model_call_limit"]) != (
        operation_limit * attempt_limit
    ):
        raise ValueError("model-call ceiling must bind every allowed provider attempt")
    if parallel.get("unit") != "world_pair":
        raise ValueError("parallel execution unit must be world_pair")
    if int(parallel.get("maximum_concurrent_pairs", 0)) != 5:
        raise ValueError("the five-world matrix freezes five concurrent pairs")
    if parallel.get("conditions_within_pair_are_serial") is not True:
        raise ValueError("conditions within each world pair must remain serial")
    if parallel.get("observed_trajectories_are_never_retried") is not True:
        raise ValueError("observed trajectories must never be retried")
    return protocol


def _source_manifest(config_path: Path) -> dict[str, Any]:
    source = matrix._source_manifest(config_path)
    runner_relative = Path(__file__).resolve().relative_to(ROOT).as_posix()
    roots = list(source["material_source_roots"])
    roots.append(runner_relative)
    roots = list(dict.fromkeys(roots))
    source["material_source_roots"] = roots
    source["material_source_tree_sha256"] = repository_tree_sha256(
        ROOT,
        relative_roots=tuple(roots),
    )
    source["parallel_runner_file"] = runner_relative
    source["parallel_runner_file_sha256"] = file_sha256(Path(__file__).resolve())
    source["parallel_runner_version"] = RUNNER_VERSION
    return source


def _provider_runtime() -> dict[str, Any]:
    return {
        "transport": "direct_deepseek_chat_completions",
        "provider_id": "deepseek",
        "provider_name": "DeepSeek",
        "provider_base_url": "https://api.deepseek.com/beta",
        "provider_env_key": "DEEPSEEK_API_KEY",
        "wire_api": "chat_completions",
        "model_catalog_endpoint": "https://api.deepseek.com/models",
        "structured_output_transport": "beta_strict_forced_tool_call",
    }


def _group_pairs(cells: Sequence[Mapping[str, Any]]) -> list[list[dict[str, Any]]]:
    grouped: dict[int, list[dict[str, Any]]] = {}
    for cell in cells:
        grouped.setdefault(int(cell["world_seed"]), []).append(deepcopy(dict(cell)))
    pairs: list[list[dict[str, Any]]] = []
    for seed in sorted(grouped):
        pair = sorted(grouped[seed], key=lambda item: int(item["within_pair_order"]))
        if len(pair) != 2 or {item["condition_id"] for item in pair} != {
            "opaque_codes",
            "anonymous_nominal_properties",
        }:
            raise ValueError(f"world {seed} does not contain one complete matched pair")
        pairs.append(pair)
    if len(pairs) != 5:
        raise ValueError("DeepSeek matrix must contain five world pairs")
    return pairs


def _attempt_summary(path: Path) -> dict[str, Any]:
    summary_path = path / "run_summary.json"
    if not summary_path.is_file():
        raise RuntimeError(f"provider attempt lacks a summary: {path}")
    payload = json.loads(summary_path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise RuntimeError(f"provider attempt summary is not an object: {path}")
    return payload


def _accepted_operations(summary: Mapping[str, Any]) -> int:
    raw = summary.get("accepted_operation_count")
    if raw is None:
        behavior = summary.get("behavior")
        if isinstance(behavior, Mapping):
            raw = behavior.get("operation_count")
    return int(raw or 0)


def _run_cell_with_pre_action_retries(
    *,
    protocol: Mapping[str, Any],
    source: Mapping[str, Any],
    runtime: Mapping[str, Any],
    cell: Mapping[str, Any],
    output_root: Path,
    card: Any,
    method_limits: Mapping[str, Any],
) -> dict[str, Any]:
    cell_root = output_root / str(cell["cell_id"])
    cell_root.mkdir(parents=True, exist_ok=False)
    maximum_attempts = int(
        protocol["parallel_execution"]["maximum_pre_action_provider_attempts_per_cell"]
    )
    attempts: list[dict[str, Any]] = []
    authoritative: dict[str, Any] | None = None
    for attempt_index in range(1, maximum_attempts + 1):
        attempt_root = cell_root / f"attempt-{attempt_index:02d}"
        error_type: str | None = None
        try:
            result = matrix._run_cell_light(
                protocol=protocol,
                source=source,
                provider_runtime=runtime,
                cell=cell,
                cell_root=attempt_root,
                card=card,
                method_limits=method_limits,
                qualification=False,
            )
        except Exception as error:  # summary is the redacted authoritative failure receipt
            error_type = type(error).__name__
            result = _attempt_summary(attempt_root)
        accepted = _accepted_operations(result)
        status = str(result.get("run_status") or "unknown")
        retryable = status == "provider_infrastructure_failure" and accepted == 0
        entry = {
            "attempt_id": attempt_root.name,
            "attempt_dir": attempt_root.relative_to(output_root).as_posix(),
            "run_status": status,
            "accepted_operation_count": accepted,
            "error_type": error_type,
            "retryable_pre_action_provider_failure": retryable,
            "summary_sha256": file_sha256(attempt_root / "run_summary.json"),
        }
        attempts.append(entry)
        if status == "completed" or not retryable or attempt_index == maximum_attempts:
            authoritative = {
                "cell": deepcopy(dict(cell)),
                "summary": result,
                "attempts": attempts,
                "authoritative_attempt_dir": entry["attempt_dir"],
            }
            break
    if authoritative is None:
        raise RuntimeError(f"cell ended without an authoritative attempt: {cell['cell_id']}")
    return authoritative


def _run_pair(**kwargs: Any) -> list[dict[str, Any]]:
    pair = kwargs.pop("pair")
    results: list[dict[str, Any]] = []
    for cell in pair:
        results.append(_run_cell_with_pre_action_retries(cell=cell, **kwargs))
    return results


def _pair_audits(results: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    by_world: dict[int, list[dict[str, Any]]] = {}
    for record in results:
        summary = record["summary"]
        if summary.get("run_status") == "completed":
            by_world.setdefault(int(record["cell"]["world_seed"]), []).append(dict(summary))
    audits = []
    for seed, pair in sorted(by_world.items()):
        if len(pair) == 2:
            audit = matrix._pair_audit(pair[0], pair[1])
            audit["world_seed"] = seed
            audits.append(audit)
    return audits


def _accounting(results: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    resources = [
        item["summary"].get("method_resources", {})
        for item in results
        if isinstance(item["summary"].get("method_resources"), Mapping)
    ]
    return {
        "provider_model": "deepseek-v4-flash",
        "completed_provider_calls": sum(int(item.get("model_call_count", 0)) for item in resources),
        "input_tokens": sum(int(item.get("input_token_count", 0)) for item in resources),
        "output_tokens": sum(int(item.get("output_token_count", 0)) for item in resources),
        "billed_cost_usd": sum(
            float(item.get("monetary_cost_usd", 0.0) or 0.0) for item in resources
        ),
        "all_materialized_accounting_complete": bool(resources)
        and all(item.get("accounting_complete") is True for item in resources),
    }


def _manifest(
    *,
    protocol: Mapping[str, Any],
    source: Mapping[str, Any],
    runtime: Mapping[str, Any],
    started_at: str,
    planned_cells: Sequence[Mapping[str, Any]],
    results: Sequence[Mapping[str, Any]],
    status: str,
) -> dict[str, Any]:
    audits = _pair_audits(results)
    rows = []
    for item in sorted(results, key=lambda value: int(value["cell"]["cell_id"].split("-")[-1])):
        cell = item["cell"]
        summary = item["summary"]
        behavior = summary.get("behavior", {})
        rows.append(
            {
                "cell_id": cell["cell_id"],
                "world_seed": int(cell["world_seed"]),
                "condition_id": cell["condition_id"],
                "within_pair_order": int(cell["within_pair_order"]),
                "material_information": deepcopy(dict(cell["material_information"])),
                "run_status": summary.get("run_status"),
                "authoritative_attempt_dir": item["authoritative_attempt_dir"],
                "attempts": deepcopy(list(item["attempts"])),
                "accepted_operation_count": _accepted_operations(summary),
                "closed_batch_count": behavior.get("closed_batch_count"),
                "best_final_score": behavior.get("best_final_score"),
                "mean_final_score": behavior.get("mean_final_score"),
                "incumbent_auc_per_operation": behavior.get("incumbent_auc_per_operation"),
                "exact_replay_verified": summary.get("exact_replay_verified"),
                "config_sha256": summary.get("config_sha256"),
                "trajectory_sha256": summary.get("trajectory_sha256"),
                "campaign_resource_ledger_sha256": summary.get("campaign_resource_ledger_sha256"),
                "provider_decision_audit_passed": summary.get("provider_decision_audit", {}).get(
                    "passed"
                ),
            }
        )
    payload: dict[str, Any] = {
        "schema_version": MANIFEST_SCHEMA_VERSION,
        "runner_version": RUNNER_VERSION,
        "protocol_id": protocol["protocol_id"],
        "run_status": status,
        "formal_result": False,
        "confirmatory_claim_allowed": False,
        "comparison_unit": "complete_agent_system",
        "provider_backend_effect_claim_allowed": False,
        "started_at": started_at,
        "updated_at": _now(),
        "source": deepcopy(dict(source)),
        "provider_runtime": deepcopy(dict(runtime)),
        "parallel_execution": deepcopy(dict(protocol["parallel_execution"])),
        "world_seeds": list(protocol["task"]["world_seeds"]),
        "planned_cell_count": len(planned_cells),
        "completed_cell_count": sum(row["run_status"] == "completed" for row in rows),
        "planned_physical_experiment_count": len(planned_cells)
        * int(protocol["campaign_resource_card"]["complete_experiments"]),
        "completed_physical_experiment_count": sum(
            int(row["closed_batch_count"] or 0) for row in rows
        ),
        "cells": rows,
        "pair_audits": audits,
        "all_five_pair_audits_passed": len(audits) == 5 and all(item["passed"] for item in audits),
        "accounting": _accounting(results),
    }
    payload["manifest_sha256"] = canonical_json_sha256(payload)
    return payload


def _dry_run(
    protocol: Mapping[str, Any],
    source: Mapping[str, Any],
) -> dict[str, Any]:
    card = matrix._campaign_card(protocol, qualification=False)
    limits = matrix._method_limits(protocol, qualification=False)
    inspected: list[dict[str, Any]] = []
    for cell in matrix._scheduled_cells(protocol):
        inspected.append(
            {
                "cell": deepcopy(dict(cell)),
                "summary": {
                    "run_status": "completed",
                    "cell": deepcopy(dict(cell)),
                    "environment_contract": matrix._inspect_cell_environment(
                        protocol=protocol,
                        cell=cell,
                        card=card,
                        operation_limit=int(limits["operation_limit"]),
                    ),
                },
            }
        )
    audits = _pair_audits(inspected)
    return {
        "schema_version": "chemworld-g2-deepseek-parallel-dry-run-0.1",
        "protocol_id": protocol["protocol_id"],
        "model": protocol["agent"]["model"],
        "world_pair_count": 5,
        "planned_cells": 10,
        "planned_physical_experiments": 60,
        "maximum_concurrent_pairs": 5,
        "campaign_resource_card_sha256": card.card_sha256,
        "source": deepcopy(dict(source)),
        "pair_audits": audits,
        "passed": len(audits) == 5 and all(item["passed"] for item in audits),
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--allow-external-provider", action="store_true")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    config_path = args.config.resolve()
    protocol = _load_protocol(config_path)
    source = _source_manifest(config_path)
    if args.dry_run:
        report = _dry_run(protocol, source)
        print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
        return 0 if report["passed"] else 2
    if not args.allow_external_provider:
        raise RuntimeError("external execution requires --allow-external-provider")
    if source["worktree_dirty"]:
        raise RuntimeError("DeepSeek matrix requires a clean source worktree")
    runtime = _provider_runtime()
    env_key = str(runtime["provider_env_key"])
    if not os.environ.get(env_key, "").strip():
        raise RuntimeError(f"required provider environment variable is not set: {env_key}")
    output_root = args.output_root.resolve()
    if output_root.exists():
        raise FileExistsError(f"refusing to overwrite existing output root: {output_root}")
    output_root.mkdir(parents=True)
    cells = matrix._scheduled_cells(protocol)
    pairs = _group_pairs(cells)
    card = matrix._campaign_card(protocol, qualification=False)
    limits = matrix._method_limits(protocol, qualification=False)
    started_at = _now()
    initial = _manifest(
        protocol=protocol,
        source=source,
        runtime=runtime,
        started_at=started_at,
        planned_cells=cells,
        results=[],
        status="running",
    )
    write_json_atomic(output_root / "matrix_manifest.json", initial)
    results: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    kwargs = {
        "protocol": protocol,
        "source": source,
        "runtime": runtime,
        "output_root": output_root,
        "card": card,
        "method_limits": limits,
    }
    workers = int(protocol["parallel_execution"]["maximum_concurrent_pairs"])
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(_run_pair, pair=pair, **kwargs): int(pair[0]["world_seed"])
            for pair in pairs
        }
        for future in as_completed(futures):
            seed = futures[future]
            try:
                results.extend(future.result())
            except BaseException as error:
                failures.append({"world_seed": seed, "error_type": type(error).__name__})
            progress = _manifest(
                protocol=protocol,
                source=source,
                runtime=runtime,
                started_at=started_at,
                planned_cells=cells,
                results=results,
                status="running" if len(results) < len(cells) else "auditing",
            )
            progress["pair_worker_failures"] = deepcopy(failures)
            progress["manifest_sha256"] = canonical_json_sha256(
                {key: value for key, value in progress.items() if key != "manifest_sha256"}
            )
            write_json_atomic(output_root / "matrix_manifest.json", progress)
    complete = len(results) == len(cells) and all(
        item["summary"].get("run_status") == "completed" for item in results
    )
    final = _manifest(
        protocol=protocol,
        source=source,
        runtime=runtime,
        started_at=started_at,
        planned_cells=cells,
        results=results,
        status="completed" if complete else "completed_with_right_censoring",
    )
    final["pair_worker_failures"] = failures
    final["manifest_sha256"] = canonical_json_sha256(
        {key: value for key, value in final.items() if key != "manifest_sha256"}
    )
    write_json_atomic(output_root / "matrix_manifest.json", final)
    print(json.dumps(final, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if complete and final["all_five_pair_audits_passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = [
    "DEFAULT_CONFIG",
    "DEFAULT_OUTPUT_ROOT",
    "MANIFEST_SCHEMA_VERSION",
    "RUNNER_VERSION",
    "main",
]
