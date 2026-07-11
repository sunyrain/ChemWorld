"""Machine-executable generalization and exploit-resistance publication gates."""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import gymnasium as gym
import numpy as np

import chemworld  # noqa: F401
from chemworld.agents.task_recipes import sample_task_recipe
from chemworld.data.logging import observation_to_json
from chemworld.eval.publication_protocol import (
    canonical_protocol_sha256,
    load_publication_protocol,
)
from chemworld.physchem.mechanism_library import configuration_root
from chemworld.task_design import SERIOUS_GENERALIZATION_CONTRACTS
from chemworld.tasks import SERIOUS_TASK_IDS, get_task

GENERALIZATION_SECURITY_SCHEMA_VERSION = (
    "chemworld-generalization-security-protocol-0.1"
)
DEFAULT_GENERALIZATION_SECURITY_PATH = (
    configuration_root() / "benchmark" / "generalization_security_v0.1.json"
)


def load_generalization_security_protocol(
    path: str | Path = DEFAULT_GENERALIZATION_SECURITY_PATH,
) -> dict[str, Any]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("generalization-security protocol must be a JSON object")
    return payload


def audit_generalization_controls(protocol: dict[str, Any]) -> dict[str, Any]:
    publication_protocol = load_publication_protocol()
    checks = {
        "schema": protocol.get("schema_version")
        == GENERALIZATION_SECURITY_SCHEMA_VERSION,
        "publication_protocol_binding": protocol.get("publication_protocol_sha256")
        == canonical_protocol_sha256(publication_protocol),
        "task_scope": list(protocol.get("axis_control_status", {}))
        == list(SERIOUS_TASK_IDS),
        "paired_seed_modes": _paired_seed_modes_valid(protocol),
        "method_scope": protocol.get("methods") == ["random", "structured_gp_bo"],
        "learning_horizon": protocol.get("complete_experiments_per_task_seed") == 40,
    }
    required_modes = set(protocol.get("required_generalization_modes", ()))
    task_reports: dict[str, dict[str, Any]] = {}
    for task_id in SERIOUS_TASK_IDS:
        declared_axes = [
            str(item["label"]) for item in SERIOUS_GENERALIZATION_CONTRACTS[task_id]
        ]
        configured = protocol.get("axis_control_status", {}).get(task_id, {})
        axis_reports: dict[str, dict[str, Any]] = {}
        for axis in declared_axes:
            implemented = set(configured.get(axis, ())) if isinstance(configured, dict) else set()
            missing = sorted(required_modes - implemented)
            axis_reports[axis] = {
                "implemented_modes": sorted(implemented),
                "missing_modes": missing,
                "ready": not missing,
            }
        task_reports[task_id] = {
            "declared_axes": declared_axes,
            "configured_axes_match": list(configured) == declared_axes,
            "axes": axis_reports,
            "ready": list(configured) == declared_axes
            and all(item["ready"] for item in axis_reports.values()),
        }
    invariance = protocol.get("invariance_probes", {})
    invariance_ready = all(value == "executable" for value in invariance.values())
    protocol_valid = all(checks.values()) and all(
        task["configured_axes_match"] for task in task_reports.values()
    )
    axis_ready = all(task["ready"] for task in task_reports.values())
    return {
        "schema_version": GENERALIZATION_SECURITY_SCHEMA_VERSION,
        "protocol_id": protocol.get("protocol_id"),
        "protocol_valid": protocol_valid,
        "axis_generalization_ready": axis_ready,
        "invariance_ready": invariance_ready,
        "generalization_ready": protocol_valid and axis_ready and invariance_ready,
        "checks": checks,
        "tasks": task_reports,
        "invariance_probes": invariance,
        "known_scope": {
            "public_seed_ood": "tests new seeds but does not isolate a declared axis",
            "salted_private_eval": "shifts the hidden world jointly but does not isolate an axis",
        },
    }


def audit_exploit_resistance() -> dict[str, Any]:
    task_reports: dict[str, dict[str, Any]] = {}
    for task_id in SERIOUS_TASK_IDS:
        unknown = _single_step(task_id, {"operation": "unknown_operation"})
        premature_assay = _single_step(
            task_id,
            {"operation": "measure", "instrument": "final_assay"},
        )
        premature_terminate = _single_step(task_id, {"operation": "terminate"})
        nonfinite = _single_step(
            task_id,
            {"operation": "add_reagent", "amount_mol": float("nan")},
        )
        ordered_trace, repeated_assay = _recipe_trace(task_id, reverse_keys=False)
        reordered_trace, _ = _recipe_trace(task_id, reverse_keys=True)
        probes = {
            "unknown_operation": _rejected_without_score(unknown),
            "premature_final_assay": _rejected_without_score(premature_assay),
            "premature_terminate": _rejected_without_score(premature_terminate),
            "nonfinite_amount": _rejected_without_score(nonfinite),
            "repeated_final_assay": _rejected_without_score(repeated_assay),
            "action_key_order": ordered_trace == reordered_trace,
        }
        task_reports[task_id] = {
            "task_contract_hash": get_task(task_id).contract_hash,
            "probes": probes,
            "passed": all(probes.values()),
        }
    passed = all(task["passed"] for task in task_reports.values())
    return {
        "schema_version": "chemworld-exploit-resistance-audit-0.1",
        "passed": passed,
        "task_count": len(task_reports),
        "tasks": task_reports,
    }


def _paired_seed_modes_valid(protocol: dict[str, Any]) -> bool:
    modes = protocol.get("evaluation_modes", {})
    public = modes.get("public_seed_ood", {})
    private = modes.get("salted_private_eval", {})
    public_seeds = public.get("seeds")
    private_seeds = private.get("seeds")
    return all(
        (
            public.get("world_split") == "public-test",
            private.get("world_split") == "private-eval",
            public_seeds == list(range(100, 120)),
            private_seeds == list(range(200, 220)),
            not (set(public_seeds or ()) & set(private_seeds or ())),
            private.get("publish_raw_salt") is False,
        )
    )


def _single_step(task_id: str, action: dict[str, Any]) -> dict[str, Any]:
    task = get_task(task_id)
    env = gym.make(
        task.env_id,
        task_id=task_id,
        world_split=task.world_split,
        budget=task.budget,
        objective=task.objective,
        seed=991,
    )
    try:
        env.reset(seed=991)
        _, reward, terminated, truncated, info = env.step(action)
        return {
            "reward": float(reward),
            "terminated": bool(terminated),
            "truncated": bool(truncated),
            "leaderboard_score": info.get("leaderboard_score"),
            "constraint_flags": info.get("constraint_flags", {}),
        }
    except (ValueError, RuntimeError, TypeError, KeyError) as error:
        return {"exception": type(error).__name__}
    finally:
        env.close()


def _recipe_trace(
    task_id: str,
    *,
    reverse_keys: bool,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    task = get_task(task_id)
    recipe = sample_task_recipe(task.to_dict(), np.random.default_rng(991))
    actions = recipe["steps"]
    env = gym.make(
        task.env_id,
        task_id=task_id,
        world_split=task.world_split,
        budget=len(actions) + 1,
        budget_override=len(actions) + 1,
        objective=task.objective,
        seed=991,
    )
    trace: list[dict[str, Any]] = []
    try:
        env.reset(seed=991)
        for raw_action in actions:
            action = (
                dict(reversed(list(raw_action.items())))
                if reverse_keys
                else dict(raw_action)
            )
            observation, reward, terminated, truncated, info = env.step(action)
            trace.append(
                {
                    "observation": observation_to_json(observation),
                    "reward": float(reward),
                    "terminated": bool(terminated),
                    "truncated": bool(truncated),
                    "leaderboard_score": info.get("leaderboard_score"),
                    "constraint_flags": info.get("constraint_flags", {}),
                }
            )
        repeated_action = {"operation": "measure", "instrument": "final_assay"}
        try:
            _, reward, terminated, truncated, info = env.step(repeated_action)
            repeated = {
                "reward": float(reward),
                "terminated": bool(terminated),
                "truncated": bool(truncated),
                "leaderboard_score": info.get("leaderboard_score"),
                "constraint_flags": info.get("constraint_flags", {}),
            }
        except (ValueError, RuntimeError, TypeError, KeyError) as error:
            repeated = {"exception": type(error).__name__}
        return trace, repeated
    finally:
        env.close()


def _rejected_without_score(result: dict[str, Any]) -> bool:
    if "exception" in result:
        return True
    reward = float(result.get("reward", 0.0))
    return (
        math.isfinite(reward)
        and reward <= 0.0
        and result.get("leaderboard_score") is None
    )


__all__ = [
    "DEFAULT_GENERALIZATION_SECURITY_PATH",
    "GENERALIZATION_SECURITY_SCHEMA_VERSION",
    "audit_exploit_resistance",
    "audit_generalization_controls",
    "load_generalization_security_protocol",
]
