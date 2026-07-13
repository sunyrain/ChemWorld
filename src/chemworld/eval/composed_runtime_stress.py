"""Stress the composed v0.5 task, operation, provider, and observation runtime."""

from __future__ import annotations

import hashlib
import json
import math
import subprocess
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

import gymnasium as gym
import numpy as np

import chemworld  # noqa: F401
from chemworld.agents.task_recipes import (
    task_recipe_dimension,
    task_recipe_from_unit_vector,
)
from chemworld.data.logging import to_builtin
from chemworld.physchem.mechanism_library import configuration_root
from chemworld.tasks import get_task, list_tasks

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_PROTOCOL_PATH = configuration_root() / "foundation" / "composed_runtime_stress_v0.5.json"
PROTOCOL_VERSION = "chemworld-composed-runtime-stress-protocol-0.1"


class ComposedRuntimeStressError(RuntimeError):
    """Raised when a stress protocol or runtime record is invalid."""


def load_composed_runtime_stress_protocol(path: Path | None = None) -> dict[str, Any]:
    resolved = DEFAULT_PROTOCOL_PATH if path is None else path
    payload = json.loads(resolved.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or payload.get("schema_version") != PROTOCOL_VERSION:
        raise ComposedRuntimeStressError("unsupported composed runtime stress protocol")
    return payload


def run_composed_runtime_stress(
    protocol: Mapping[str, Any], *, workspace: Path = ROOT
) -> dict[str, Any]:
    dependencies = {
        name: _read_object(_resolve_path(workspace, raw_path))
        for name, raw_path in protocol["dependencies"].items()
    }
    runtime = dependencies["runtime_reachability"]
    state = dependencies["state_invariants"]
    tasks = list_tasks()
    task_operation_pairs = [
        (task.task_id, operation) for task in tasks for operation in task.allowed_operations
    ]

    profile_runs: list[dict[str, Any]] = []
    for task in tasks:
        task_payload = task.to_dict()
        for profile_name, raw_value in protocol["profile_values"].items():
            value = float(raw_value)
            vector = np.full(task_recipe_dimension(task_payload), value, dtype=float)
            actions = task_recipe_from_unit_vector(task_payload, vector)["steps"]
            first = _run_actions(task.task_id, int(protocol["stress_seed"]), actions)
            replay = _run_actions(task.task_id, int(protocol["stress_seed"]), actions)
            profile_runs.append(
                {
                    "task_id": task.task_id,
                    "profile": profile_name,
                    "profile_value": value,
                    "action_count": len(actions),
                    "operations": [str(action["operation"]) for action in actions],
                    "trajectory_sha256": first["trajectory_sha256"],
                    "replay_sha256": replay["trajectory_sha256"],
                    "deterministic_replay": first["trajectory_sha256"]
                    == replay["trajectory_sha256"],
                    "all_transactions_committed": first["all_transactions_committed"],
                    "constitution_failure_count": first["constitution_failure_count"],
                    "precondition_failure_count": first["precondition_failure_count"],
                    "nonfinite_observation_count": first["nonfinite_observation_count"],
                    "runtime_failure_count": first["runtime_failure_count"],
                    "final_score": first["final_score"],
                    "task_contract_hash": first["task_contract_hash"],
                    "runtime_profile_hash": first["runtime_profile_hash"],
                    "world_law_id": first["world_law_id"],
                }
            )

    chain_runs: dict[str, dict[str, Any]] = {}
    for task_id, raw_chain in protocol["required_chains"].items():
        chain = dict(raw_chain)
        if "actions" in chain:
            actions = [dict(action) for action in chain["actions"]]
        else:
            task_payload = get_task(task_id).to_dict()
            value = float(chain["profile_value"])
            vector = np.full(task_recipe_dimension(task_payload), value, dtype=float)
            actions = task_recipe_from_unit_vector(task_payload, vector)["steps"]
        result = _run_actions(task_id, int(protocol["stress_seed"]), actions)
        replay = _run_actions(task_id, int(protocol["stress_seed"]), actions)
        observed_operations = {str(action["operation"]) for action in actions}
        reachable_models = runtime["task_paths"][task_id]["reachable_model_ids"]
        observed_modules = {
            runtime["provider_catalog"][model_id]["module_id"]
            for model_id in reachable_models
        }
        chain_runs[task_id] = {
            "action_count": len(actions),
            "operations": sorted(observed_operations),
            "modules": sorted(observed_modules),
            "required_operations_present": set(chain["required_operations"]).issubset(
                observed_operations
            ),
            "required_modules_present": set(chain["required_modules"]).issubset(
                observed_modules
            ),
            "all_transactions_committed": result["all_transactions_committed"],
            "deterministic_replay": result["trajectory_sha256"]
            == replay["trajectory_sha256"],
            "trajectory_sha256": result["trajectory_sha256"],
            "constitution_failure_count": result["constitution_failure_count"],
            "precondition_failure_count": result["precondition_failure_count"],
            "runtime_failure_count": result["runtime_failure_count"],
        }

    expected = protocol["expected_counts"]
    operation_evidence = state["operation_results"]
    runtime_failures = sum(int(item["runtime_failure_count"]) for item in profile_runs)
    executed_steps = sum(int(item["action_count"]) for item in profile_runs)
    controls = {
        "protocol_is_nonclaiming": protocol.get("benchmark_claim_allowed") is False
        and protocol.get("formal_results_present") is False,
        "dependency_controls_are_complete": runtime["controls_ready"] is True
        and state["controls_complete"] is True
        and dependencies["runtime_integration"]["passed"] is True
        and dependencies["contract_coherence"]["controls_ready"] is True,
        "registered_counts_are_exact": len(tasks) == int(expected["tasks"])
        and len(runtime["operation_paths"]) == int(expected["operations"])
        and len(runtime["provider_catalog"]) == int(expected["providers"])
        and len(task_operation_pairs) == int(expected["task_operation_pairs"]),
        "all_task_operation_pairs_are_reachable": all(
            operation
            in {
                item["operation"] for item in runtime["task_paths"][task_id]["operation_paths"]
            }
            for task_id, operation in task_operation_pairs
        ),
        "all_operations_have_transaction_evidence": set(operation_evidence)
        == set(runtime["operation_paths"])
        and all(all(item["checks"].values()) for item in operation_evidence.values()),
        "all_runtime_providers_are_declared_and_clean": not runtime[
            "forbidden_runtime_models"
        ]
        and not runtime["orphan_runtime_providers"]
        and not runtime["incomplete_provider_contracts"]
        and all(
            provider["runtime_reachable"] is True
            for provider in runtime["provider_catalog"].values()
            if provider["role"] == "runtime"
        ),
        "profile_grid_is_complete": len(profile_runs) == int(expected["profile_runs"]),
        "profile_grid_commits_without_failures": all(
            item["all_transactions_committed"]
            and item["constitution_failure_count"] == 0
            and item["precondition_failure_count"] == 0
            and item["runtime_failure_count"] == 0
            and item["nonfinite_observation_count"] == 0
            for item in profile_runs
        ),
        "profile_grid_replays_exactly": all(
            item["deterministic_replay"] for item in profile_runs
        ),
        "required_composed_chains_execute": all(
            item["required_operations_present"]
            and item["required_modules_present"]
            and item["all_transactions_committed"]
            and item["deterministic_replay"]
            and item["constitution_failure_count"] == 0
            and item["precondition_failure_count"] == 0
            and item["runtime_failure_count"] == 0
            for item in chain_runs.values()
        ),
        "reference_failure_domains_are_explicit": dependencies["kinetics_evidence"][
            "maturity"
        ]["implementation_slice"]
        == "reference_validated"
        and dependencies["reactor_reference"]["maturity"]["batch_declared_slice"]
        == "reference_validated"
        and dependencies["instrument_reference"]["maturity_truth"][
            "bounded_contract_verified"
        ]
        is True,
        "invalid_and_boundary_actions_fail_closed": state["control_failures"] == []
        and state["negative_value_acceptances"] == []
        and state["zero_effect_acceptances"] == []
        and state["final_assay_boundary"]["repeated_final_assay_rejected"] is True,
    }
    controls_ready = all(controls.values())
    source_commit, dirty = _git_provenance(workspace)
    return {
        "schema_version": "chemworld-composed-runtime-stress-report-0.1",
        "protocol_id": protocol["protocol_id"],
        "status": "composed_runtime_stress_passed"
        if controls_ready
        else "composed_runtime_stress_failed",
        "controls_ready": controls_ready,
        "formal_results_present": False,
        "benchmark_claim_allowed": False,
        "source_commit": source_commit,
        "source_tree_dirty": dirty,
        "protocol_sha256": _canonical_sha256(protocol),
        "controls": controls,
        "coverage": {
            "task_count": len(tasks),
            "operation_count": len(runtime["operation_paths"]),
            "provider_count": len(runtime["provider_catalog"]),
            "task_operation_pair_count": len(task_operation_pairs),
            "profile_run_count": len(profile_runs),
            "profile_executed_step_count": executed_steps,
            "runtime_failure_count": runtime_failures,
            "runtime_failure_rate": runtime_failures / executed_steps if executed_steps else None,
        },
        "profile_runs": profile_runs,
        "composed_chains": chain_runs,
        "operation_transaction_evidence_sha256": _canonical_sha256(operation_evidence),
        "runtime_graph_sha256": _canonical_sha256(runtime["task_paths"]),
        "limitations": [
            "Cross-process and cross-platform numerical replay belongs to portable-release.",
            (
                "The three unit-vector profiles stress declared recipe bounds, not every "
                "continuous point."
            ),
            "Industrial plant-scale validity remains outside the bounded ChemWorld claim.",
        ],
        "remaining_release_gates": [
            "complete observation identifiability controls",
            "complete task validity and power controls",
            "repeat golden replay in an independent Linux clean-wheel environment",
        ],
    }


def _run_actions(task_id: str, seed: int, actions: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    env = gym.make("ChemWorld", task_id=task_id, seed=seed)
    records: list[dict[str, Any]] = []
    constitution_failures = 0
    precondition_failures = 0
    nonfinite_observations = 0
    runtime_failures = 0
    final_score: float | None = None
    task_contract_hash = ""
    runtime_profile_hash = ""
    world_law_id = ""
    statuses: list[str] = []
    try:
        observation, reset_info = env.reset(seed=seed)
        records.append(
            {
                "reset_observation": to_builtin(observation),
                "reset_identity": {
                    key: reset_info.get(key)
                    for key in (
                        "task_id",
                        "task_contract_hash",
                        "runtime_profile_hash",
                        "world_law_id",
                        "mechanism_hash",
                    )
                },
            }
        )
        for action in actions:
            observation, reward, terminated, truncated, info = env.step(dict(action))
            status = str(info.get("transaction_status"))
            statuses.append(status)
            flags = info.get("constraint_flags", {})
            constitution_failures += int(bool(flags.get("constitution_failed")))
            precondition_failures += int(bool(flags.get("precondition_failed")))
            runtime_failures += int(status not in {"committed", "validation_failed"})
            observed_keys = info.get("observed_keys", ())
            if isinstance(observed_keys, Sequence) and not isinstance(
                observed_keys, (str, bytes, bytearray)
            ):
                nonfinite_observations += sum(
                    _count_nonfinite(observation[key])
                    for key in observed_keys
                    if key in observation
                )
            score = info.get("leaderboard_score")
            if isinstance(score, (int, float)) and not isinstance(score, bool):
                final_score = float(score)
            task_contract_hash = str(info.get("task_contract_hash", task_contract_hash))
            runtime_profile_hash = str(info.get("runtime_profile_hash", runtime_profile_hash))
            world_law_id = str(info.get("world_law_id", world_law_id))
            records.append(
                {
                    "action": to_builtin(action),
                    "observation": to_builtin(observation),
                    "reward": float(reward),
                    "terminated": bool(terminated),
                    "truncated": bool(truncated),
                    "info": {
                        key: to_builtin(info.get(key))
                        for key in (
                            "transaction_status",
                            "rollback_reason",
                            "constraint_flags",
                            "cost",
                            "measurement_cost",
                            "risk_delta",
                            "leaderboard_score",
                            "task_contract_hash",
                            "runtime_profile_hash",
                            "world_law_id",
                            "mechanism_hash",
                            "observation_contract_hash",
                            "scoring_contract_hash",
                            "state_delta_summary",
                        )
                    },
                }
            )
    finally:
        env.close()
    return {
        "trajectory_sha256": _canonical_sha256({"records": records}),
        "all_transactions_committed": all(status == "committed" for status in statuses),
        "constitution_failure_count": constitution_failures,
        "precondition_failure_count": precondition_failures,
        "nonfinite_observation_count": nonfinite_observations,
        "runtime_failure_count": runtime_failures,
        "final_score": final_score,
        "task_contract_hash": task_contract_hash,
        "runtime_profile_hash": runtime_profile_hash,
        "world_law_id": world_law_id,
    }


def _count_nonfinite(value: Any) -> int:
    if isinstance(value, Mapping):
        return sum(_count_nonfinite(item) for item in value.values())
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return sum(_count_nonfinite(item) for item in value)
    if isinstance(value, np.ndarray):
        return int(np.size(value) - np.count_nonzero(np.isfinite(value)))
    if isinstance(value, (int, float, np.number)) and not isinstance(value, bool):
        return int(not math.isfinite(float(value)))
    return 0


def _read_object(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ComposedRuntimeStressError(f"JSON object required: {path}")
    return payload


def _resolve_path(workspace: Path, raw_path: Any) -> Path:
    path = (workspace / str(raw_path)).resolve()
    try:
        path.relative_to(workspace.resolve())
    except ValueError as exc:
        raise ComposedRuntimeStressError("dependency path escapes workspace") from exc
    return path


def _canonical_sha256(payload: Mapping[str, Any]) -> str:
    encoded = json.dumps(
        to_builtin(payload), sort_keys=True, separators=(",", ":"), allow_nan=False
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _git_provenance(workspace: Path) -> tuple[str | None, bool | None]:
    try:
        commit = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=workspace,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        dirty = bool(
            subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=workspace,
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
        )
        return commit, dirty
    except (OSError, subprocess.CalledProcessError):
        return None, None


__all__ = [
    "ComposedRuntimeStressError",
    "load_composed_runtime_stress_protocol",
    "run_composed_runtime_stress",
]
