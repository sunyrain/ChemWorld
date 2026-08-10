"""Zero-provider readiness receipts for Work II development campaigns."""

from __future__ import annotations

import json
import subprocess
from collections.abc import Callable, Mapping, Sequence
from datetime import UTC, datetime
from pathlib import Path
from time import perf_counter
from typing import Any

from chemworld.data.logging import load_jsonl
from chemworld.eval.provenance import (
    canonical_json_sha256,
    file_sha256,
    git_source_commit,
    git_worktree_dirty,
)
from chemworld.eval.verify import verify_records
from chemworld.eval.work_ii_process_profile import build_work_ii_execution_artifacts

WORK_II_DEVELOPMENT_READINESS_VERSION = "chemworld-work-ii-development-provider-readiness-0.3"
_PRIOR_ARMS = ("opaque", "aligned_nominal", "misindexed_nominal")


def _self_hash(payload: Mapping[str, Any]) -> str:
    body = dict(payload)
    body.pop("readiness_sha256", None)
    return canonical_json_sha256(body)


def _git_ignored(root: Path, path: Path) -> bool:
    completed = subprocess.run(
        ["git", "check-ignore", "--quiet", str(path.resolve())],
        cwd=root,
        check=False,
    )
    return completed.returncode == 0


def _resolved_config_path(root: Path, config_path: Path) -> Path:
    resolved = config_path.resolve()
    if not resolved.is_relative_to(root.resolve()):
        raise ValueError("campaign config must be inside the repository")
    return resolved


def _config_checks(root: Path, config_path: Path, seeds: Sequence[int]) -> dict[str, bool]:
    config = json.loads(config_path.read_text(encoding="utf-8"))
    provider = config.get("provider", {})
    execution = config.get("execution", {})
    campaign = config.get("campaign", {})
    method = config.get("method_resources", {})
    catalog_value = provider.get("model_catalog_json")
    catalog_path = (root / str(catalog_value)).resolve() if catalog_value else Path()
    catalog: dict[str, Any] = {}
    if catalog_path.is_file():
        loaded = json.loads(catalog_path.read_text(encoding="utf-8"))
        catalog = loaded if isinstance(loaded, dict) else {}
    models = [
        item
        for item in catalog.get("models", [])
        if isinstance(item, Mapping) and item.get("slug") == provider.get("model")
    ]
    api_key_value = provider.get("api_key_file")
    api_key_path = (root / str(api_key_value)).resolve() if api_key_value else Path()
    prior_arms = tuple(config.get("prior_arms", {}))
    checkpoint_experiments = list(campaign.get("checkpoint_complete_experiments", []))
    method_checkpoints = list(method.get("checkpoint_complete_experiments", []))
    return {
        "clean_committed_worktree": not git_worktree_dirty(root),
        "seed_schedule_is_one_pilot_or_five_seed_block": len(seeds) in {1, 5}
        and len(set(seeds)) == len(seeds),
        "three_frozen_prior_arms": prior_arms == _PRIOR_ARMS,
        "three_cell_os_concurrency": execution.get("max_concurrency") == 3
        and execution.get("within_cell_concurrency") == 1
        and execution.get("parallelization_unit") == "same_seed_prior_arm_triplet",
        "retain_cell_failure_continue_schedule_semantics": execution.get("failure_semantics")
        == "retain cell failures and continue every scheduled seed triplet",
        "systemic_triplet_stop_guard": execution.get("systemic_failure_semantics")
        == "stop only when all three arms fail before the first committed operation",
        "four_shared_resource_experiments": campaign.get("complete_experiments") == 4
        and campaign.get("vessel_start_limit") == 4
        and campaign.get("final_assay_limit") == 4
        and method.get("complete_experiment_limit") == 4,
        "four_in_session_checkpoints": list(config.get("snapshot_stages", []))
        == ["pre_evidence", "after_experiment_1", "after_experiment_2", "final"]
        and checkpoint_experiments == [0, 1, 2, 4]
        and method_checkpoints == [1, 2, 4],
        "one_provider_turn_per_campaign_cell": method.get("model_call_limit") == 1,
        "operation_and_wall_envelopes_positive": int(method.get("operation_limit", 0))
        == int(campaign.get("operation_attempt_limit", -1))
        and float(method.get("wall_time_limit_s", 0.0)) > 0.0
        and int(method.get("input_token_limit", 0)) > 0
        and int(method.get("uncached_input_token_limit", 0)) > 0
        and int(method.get("output_token_limit", 0)) > 0,
        "bounded_session_and_recovery_limits": float(provider.get("session_wall_time_limit_s", 0.0))
        > 0.0
        and float(provider.get("session_wall_time_limit_s", 0.0))
        <= float(method.get("wall_time_limit_s", 0.0))
        and isinstance(provider.get("max_recovered_mcp_tool_failures"), int)
        and int(provider.get("max_recovered_mcp_tool_failures", -1)) >= 0
        and isinstance(provider.get("max_consecutive_mcp_tool_failures"), int)
        and int(provider.get("max_consecutive_mcp_tool_failures", -1)) >= 0
        and isinstance(provider.get("max_provider_error_events"), int)
        and int(provider.get("max_provider_error_events", -1)) >= 0
        and 0.0 < float(provider.get("progress_interval_s", 0.0)) <= 60.0
        and float(execution.get("pilot_expansion_headroom_fraction", 0.0)) >= 0.1
        and float(execution.get("pilot_expansion_headroom_fraction", 1.0)) < 1.0,
        "bounded_resource_rejection_policy": isinstance(
            config.get("qualification", {}).get("max_resource_rejections"), int
        )
        and int(config.get("qualification", {}).get("max_resource_rejections", -1)) >= 0,
        "responses_codex_harness_contract": provider.get("wire_api") == "responses"
        and provider.get("model") == "deepseek-v4-flash"
        and provider.get("reasoning_effort") == "high",
        "domain_mcp_routing_catalog_frozen": len(models) == 1
        and models[0].get("supports_search_tool") is False
        and models[0].get("supported_in_api") is True,
        "credential_file_exists_and_is_git_ignored": api_key_path.is_file()
        and _git_ignored(root, api_key_path),
    }


def _load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object")
    return value


def audit_seed0_expansion_pilot(
    config: Mapping[str, Any],
    pilot_root: Path | None,
) -> dict[str, Any] | None:
    """Audit the exact three-arm pilot that authorizes a five-seed expansion."""

    if pilot_root is None:
        return None
    root = pilot_root.resolve()
    matrix_path = root / "matrix_report.json"
    failures: list[str] = []
    bindings: list[dict[str, Any]] = []
    try:
        matrix = _load_object(matrix_path)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        return {
            "root": root.as_posix(),
            "passed": False,
            "failures": [f"pilot matrix is unreadable: {error}"],
            "bindings": [],
            "cells": [],
        }
    bindings.append({"path": matrix_path.as_posix(), "sha256": file_sha256(matrix_path)})
    if matrix.get("all_cells_completed") is not True:
        failures.append("pilot matrix did not complete all cells")
    if matrix.get("world_seeds") != [0] or matrix.get("expected_cell_count") != 3:
        failures.append("pilot matrix is not exactly seed 0 x three prior arms")
    if matrix.get("task_id") != config.get("task_id"):
        failures.append("pilot task differs from the campaign config")
    provider = config.get("provider", {})
    if matrix.get("provider_id") != provider.get("id") or matrix.get("model") != provider.get(
        "model"
    ):
        failures.append("pilot provider/model differs from the campaign config")
    method = config.get("method_resources", {})
    execution = config.get("execution", {})
    headroom = float(execution.get("pilot_expansion_headroom_fraction", 0.0))
    accepted_fraction = 1.0 - headroom
    cells: list[dict[str, Any]] = []
    for arm in _PRIOR_ARMS:
        cell_root = root / "seed-0" / arm
        summary_path = cell_root / "summary.json"
        trajectory_path = cell_root / "trajectory.jsonl"
        cell_failures: list[str] = []
        try:
            summary = _load_object(summary_path)
        except (OSError, ValueError, json.JSONDecodeError) as error:
            failures.append(f"{arm}: summary is unreadable: {error}")
            continue
        for path in (summary_path, trajectory_path):
            if path.is_file():
                bindings.append({"path": path.as_posix(), "sha256": file_sha256(path)})
            else:
                cell_failures.append(f"missing {path.name}")
        analysis = summary.get("analysis", {})
        usage = summary.get("method_resources", {})
        qualification = summary.get("qualification", {})
        receipts = summary.get("provider_receipts", [])
        receipt = receipts[0] if isinstance(receipts, list) and len(receipts) == 1 else {}
        records = load_jsonl(trajectory_path) if trajectory_path.is_file() else []
        replay = verify_records(records, tolerance=0.0).to_dict() if records else {}
        artifacts = (
            build_work_ii_execution_artifacts(
                records,
                replay,
                planned_experiment_count=4,
                terminal_state="completed",
                hidden_identity={"prior_arm": arm, "world_seed": 0},
            )
            if records
            else None
        )
        failed_mcp_calls = [
            item
            for item in receipt.get("mcp_tool_calls", [])
            if isinstance(item, Mapping) and item.get("status") != "completed"
        ]
        raw_max_consecutive = receipt.get(
            "maximum_consecutive_mcp_tool_failure_count"
        )
        max_consecutive = (
            raw_max_consecutive
            if isinstance(raw_max_consecutive, int)
            and not isinstance(raw_max_consecutive, bool)
            else -1
        )
        provider_errors = receipt.get("provider_errors", [])
        provider_error_count = receipt.get("provider_error_event_count")
        if not isinstance(provider_error_count, int) or isinstance(provider_error_count, bool):
            provider_error_count = (
                len(provider_errors) if isinstance(provider_errors, list) else -1
            )
        elapsed_s = float(summary.get("elapsed_s", float("inf")))
        observed = {
            "input_tokens": int(usage.get("input_token_count", -1)),
            "uncached_input_tokens": int(usage.get("uncached_input_token_count", -1)),
            "output_tokens": int(usage.get("output_token_count", -1)),
            "elapsed_s": elapsed_s,
            "recovered_mcp_tool_failures": len(failed_mcp_calls),
            "maximum_consecutive_mcp_tool_failures": max_consecutive,
            "provider_error_events": provider_error_count,
        }
        caps = {
            "input_tokens": int(int(method.get("input_token_limit", 0)) * accepted_fraction),
            "uncached_input_tokens": int(
                int(method.get("uncached_input_token_limit", 0)) * accepted_fraction
            ),
            "output_tokens": int(int(method.get("output_token_limit", 0)) * accepted_fraction),
            "elapsed_s": float(provider.get("session_wall_time_limit_s", 0.0)) * accepted_fraction,
            "recovered_mcp_tool_failures": int(provider.get("max_recovered_mcp_tool_failures", -1)),
            "maximum_consecutive_mcp_tool_failures": int(
                provider.get("max_consecutive_mcp_tool_failures", -1)
            ),
            "provider_error_events": int(provider.get("max_provider_error_events", -1)),
        }
        if summary.get("completed") is not True or qualification.get("passed") is not True:
            cell_failures.append("cell or qualification did not pass")
        if analysis.get("complete_experiment_count") != 4:
            cell_failures.append("cell did not complete four experiments")
        max_resource_rejections = int(
            config.get("qualification", {}).get("max_resource_rejections", 0)
        )
        if int(analysis.get("resource_rejection_count", 0)) > max_resource_rejections:
            cell_failures.append("cell exceeds the frozen resource-rejection allowance")
        if replay.get("verified") is not True:
            cell_failures.append("physical replay failed")
        if artifacts is None or artifacts.get("execution_audit", {}).get("passed") is not True:
            cell_failures.append("current-code execution audit failed")
        if usage.get("provider_usage_accounting_complete") is not True:
            cell_failures.append("provider usage accounting is incomplete")
        for name, value in observed.items():
            if value < 0 or value > caps[name]:
                cell_failures.append(f"{name} lacks the frozen pilot headroom")
        if cell_failures:
            failures.extend(f"{arm}: {failure}" for failure in cell_failures)
        cells.append(
            {
                "arm": arm,
                "passed": not cell_failures,
                "failures": cell_failures,
                "observed": observed,
                "expansion_caps": caps,
                "record_count": len(records),
            }
        )
    return {
        "root": root.as_posix(),
        "source_commit": matrix.get("source_commit"),
        "headroom_fraction": headroom,
        "passed": len(cells) == 3 and not failures,
        "failures": failures,
        "bindings": bindings,
        "cells": cells,
    }


def audit_historical_trajectories(
    historical_roots: Sequence[Path],
    *,
    progress: Callable[[dict[str, Any]], None] | None = None,
) -> dict[str, Any]:
    """Rebuild every retained trajectory without making a provider call."""

    trajectories = sorted(
        {
            trajectory.resolve()
            for root in historical_roots
            for trajectory in root.resolve().glob("seed-*/**/trajectory.jsonl")
        }
    )
    started = perf_counter()
    rows: list[dict[str, Any]] = []
    for index, trajectory in enumerate(trajectories, start=1):
        records = load_jsonl(trajectory)
        replay = (
            verify_records(records, tolerance=0.0).to_dict()
            if records
            else {
                "verified": False,
                "checked_steps": 0,
                "max_abs_error": None,
                "mismatches": ["empty trajectory"],
            }
        )
        arm = trajectory.parent.name
        seed_name = trajectory.parent.parent.name
        seed = int(seed_name.removeprefix("seed-"))
        artifacts = (
            build_work_ii_execution_artifacts(
                records,
                replay,
                planned_experiment_count=4,
                terminal_state="completed",
                hidden_identity={"prior_arm": arm, "world_seed": seed},
            )
            if records
            else None
        )
        execution = artifacts["execution_audit"] if artifacts is not None else {}
        passed = execution.get("passed") is True
        row = {
            "path": trajectory.as_posix(),
            "sha256": file_sha256(trajectory),
            "world_seed": seed,
            "arm": arm,
            "record_count": len(records),
            "physical_exact_replay": replay.get("verified") is True,
            "resource_exact_replay": (
                artifacts is not None and artifacts["resource_replay"].get("status") == "passed"
            ),
            "hidden_boundary": (
                artifacts is not None
                and artifacts["hidden_boundary_audit"].get("status") == "passed"
            ),
            "process_profile_constructed": (
                artifacts is not None and artifacts.get("process_profile") is not None
            ),
            "execution_audit_passed": passed,
            "failed_checks": list(execution.get("failed_checks", [])),
        }
        rows.append(row)
        if progress is not None:
            elapsed = perf_counter() - started
            rate = index / elapsed if elapsed > 0.0 else 0.0
            progress(
                {
                    "stage": "historical_trajectory_audit",
                    "completed": index,
                    "total": len(trajectories),
                    "passed": sum(item["execution_audit_passed"] for item in rows),
                    "throughput_trajectories_per_minute": round(rate * 60.0, 2),
                    "eta_s": (round((len(trajectories) - index) / rate, 1) if rate > 0.0 else None),
                    "current": trajectory.as_posix(),
                }
            )
    return {
        "historical_root_count": len(historical_roots),
        "trajectory_count": len(rows),
        "passed_trajectory_count": sum(item["execution_audit_passed"] for item in rows),
        "all_trajectories_passed": bool(rows)
        and all(item["execution_audit_passed"] for item in rows),
        "provider_call_count": 0,
        "trajectories": rows,
    }


def build_development_readiness_receipt(
    root: Path,
    config_path: Path,
    seeds: Sequence[int],
    historical_roots: Sequence[Path],
    *,
    pilot_run: Path | None = None,
    progress: Callable[[dict[str, Any]], None] | None = None,
) -> dict[str, Any]:
    resolved_config = _resolved_config_path(root, config_path)
    config = json.loads(resolved_config.read_text(encoding="utf-8"))
    checks = _config_checks(root, resolved_config, seeds)
    historical = audit_historical_trajectories(historical_roots, progress=progress)
    pilot = audit_seed0_expansion_pilot(config, pilot_run)
    checks["historical_current_code_audits_passed"] = historical["all_trajectories_passed"]
    checks["five_seed_expansion_has_passing_seed0_pilot"] = len(seeds) == 1 or (
        pilot is not None and pilot.get("passed") is True
    )
    receipt: dict[str, Any] = {
        "schema_version": WORK_II_DEVELOPMENT_READINESS_VERSION,
        "generated_at": datetime.now(UTC).isoformat(),
        "source_commit": git_source_commit(root),
        "config": {
            "path": resolved_config.relative_to(root.resolve()).as_posix(),
            "sha256": file_sha256(resolved_config),
            "task_id": config.get("task_id"),
        },
        "schedule": {
            "world_seeds": [int(seed) for seed in seeds],
            "prior_arms": list(config.get("prior_arms", {})),
            "expected_cell_count": len(seeds) * 3,
            "max_concurrency": 3,
        },
        "provider": {
            "provider_id": config.get("provider", {}).get("id"),
            "model": config.get("provider", {}).get("model"),
            "wire_api": config.get("provider", {}).get("wire_api"),
            "reasoning_effort": config.get("provider", {}).get("reasoning_effort"),
        },
        "checks": checks,
        "historical_audit": historical,
        "seed0_expansion_pilot": pilot,
        "provider_call_count": 0,
        "ready": all(checks.values()) and historical["provider_call_count"] == 0,
    }
    receipt["readiness_sha256"] = _self_hash(receipt)
    return receipt


def validate_development_readiness_receipt(
    root: Path,
    receipt_path: Path,
    config_path: Path,
    seeds: Sequence[int],
) -> list[str]:
    errors: list[str] = []
    try:
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        return [f"readiness receipt is unreadable: {error}"]
    if not isinstance(receipt, dict):
        return ["readiness receipt must contain an object"]
    if receipt.get("schema_version") != WORK_II_DEVELOPMENT_READINESS_VERSION:
        errors.append("readiness receipt schema mismatch")
    if receipt.get("readiness_sha256") != _self_hash(receipt):
        errors.append("readiness receipt self-hash mismatch")
    if receipt.get("ready") is not True:
        errors.append("readiness receipt is not passing")
    checks = receipt.get("checks")
    if (
        not isinstance(checks, Mapping)
        or not checks
        or not all(value is True for value in checks.values())
    ):
        errors.append("readiness receipt checks are incomplete or failing")
    if receipt.get("provider_call_count") != 0:
        errors.append("readiness receipt was not produced by a zero-provider audit")
    if receipt.get("source_commit") != git_source_commit(root):
        errors.append("readiness receipt source commit is stale")
    resolved_config = _resolved_config_path(root, config_path)
    config_binding = receipt.get("config", {})
    if not isinstance(config_binding, Mapping):
        errors.append("readiness receipt lacks config binding")
    elif config_binding.get("path") != resolved_config.relative_to(
        root.resolve()
    ).as_posix() or config_binding.get("sha256") != file_sha256(resolved_config):
        errors.append("readiness receipt config binding mismatch")
    schedule = receipt.get("schedule", {})
    if not isinstance(schedule, Mapping) or schedule.get("world_seeds") != [
        int(seed) for seed in seeds
    ]:
        errors.append("readiness receipt seed schedule mismatch")
    historical = receipt.get("historical_audit", {})
    if not isinstance(historical, Mapping) or historical.get("all_trajectories_passed") is not True:
        errors.append("readiness receipt historical audit is not passing")
    else:
        for row in historical.get("trajectories", []):
            if not isinstance(row, Mapping):
                errors.append("readiness receipt trajectory binding is malformed")
                continue
            path = Path(str(row.get("path", "")))
            if not path.is_file() or row.get("sha256") != file_sha256(path):
                errors.append(f"readiness trajectory binding changed: {path}")
    pilot = receipt.get("seed0_expansion_pilot")
    if len(seeds) == 5:
        if not isinstance(pilot, Mapping) or pilot.get("passed") is not True:
            errors.append("five-seed readiness lacks a passing seed-0 expansion pilot")
        else:
            for row in pilot.get("bindings", []):
                if not isinstance(row, Mapping):
                    errors.append("seed-0 pilot binding is malformed")
                    continue
                path = Path(str(row.get("path", "")))
                if not path.is_file() or row.get("sha256") != file_sha256(path):
                    errors.append(f"seed-0 pilot binding changed: {path}")
    return errors


__all__ = [
    "WORK_II_DEVELOPMENT_READINESS_VERSION",
    "audit_historical_trajectories",
    "audit_seed0_expansion_pilot",
    "build_development_readiness_receipt",
    "validate_development_readiness_receipt",
]
