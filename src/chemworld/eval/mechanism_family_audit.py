"""Executable audit for causally reachable mechanism-family controls."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

import gymnasium as gym
import numpy as np

import chemworld  # noqa: F401
from chemworld.agents.task_recipes import (
    task_recipe_dimension,
    task_recipe_from_unit_vector,
)
from chemworld.physchem.mechanism_library import configuration_root
from chemworld.tasks import get_task
from chemworld.world.mechanism_family import (
    MECHANISM_FAMILY_INTERVENTION_VERSION,
    MECHANISM_REACHABLE_TASKS,
)
from chemworld.world.scenario import DefaultScenarioGenerator, get_scenario

MECHANISM_FAMILY_AUDIT_VERSION = "chemworld-mechanism-family-control-audit-0.1"
MECHANISM_FAMILY_PROTOCOL_VERSION = "chemworld-mechanism-family-protocol-0.1"
MECHANISM_FAMILY_MODES = ("rate_law_family", "topology_family")
DEFAULT_MECHANISM_FAMILY_PROTOCOL_PATH = (
    configuration_root() / "benchmark" / "mechanism_families_vnext.json"
)


def load_mechanism_family_protocol(
    path: str | Path = DEFAULT_MECHANISM_FAMILY_PROTOCOL_PATH,
) -> dict[str, Any]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("mechanism-family protocol must be a JSON object")
    return payload


def audit_mechanism_families(protocol: dict[str, Any]) -> dict[str, Any]:
    declared_modes = tuple(str(item) for item in protocol.get("modes", ()))
    task_reports: dict[str, Any] = {}
    for task_id in MECHANISM_REACHABLE_TASKS:
        scenario = get_scenario(task_id)
        base = DefaultScenarioGenerator().generate(scenario, 0)
        mode_reports: dict[str, Any] = {}
        for mode in MECHANISM_FAMILY_MODES:
            payload = (_intervention(mode),)
            first = DefaultScenarioGenerator().generate(scenario, 0, payload)
            second = DefaultScenarioGenerator().generate(scenario, 0, payload)
            base_score = _run_midpoint(task_id, None)
            shifted_score = _run_midpoint(task_id, mode)
            mode_reports[mode] = {
                "deterministic": first.compiled_mechanism.mechanism_hash
                == second.compiled_mechanism.mechanism_hash,
                "hash_changed": first.compiled_mechanism.mechanism_hash
                != base.compiled_mechanism.mechanism_hash,
                "opaque_public_id": first.compiled_mechanism.mechanism_id.startswith(
                    "mechanism-family-"
                )
                and mode not in first.compiled_mechanism.mechanism_id,
                "reaction_count_delta": len(first.compiled_mechanism.network.reactions)
                - len(base.compiled_mechanism.network.reactions),
                "rate_law_families_changed": [
                    reaction.rate_law.equation_id
                    for reaction in first.compiled_mechanism.network.reactions
                ]
                != [
                    reaction.rate_law.equation_id
                    for reaction in base.compiled_mechanism.network.reactions
                ],
                "score_delta": shifted_score - base_score,
                "task_response_changed": abs(shifted_score - base_score) > 1.0e-8,
            }
        task_reports[task_id] = {
            "base_mechanism_hash": base.compiled_mechanism.mechanism_hash,
            "modes": mode_reports,
        }
    checks = {
        "schema": protocol.get("schema_version") == MECHANISM_FAMILY_PROTOCOL_VERSION,
        "contract_version": protocol.get("intervention_contract_version")
        == MECHANISM_FAMILY_INTERVENTION_VERSION,
        "mode_scope": declared_modes == MECHANISM_FAMILY_MODES,
        "candidate_is_non_claiming": protocol.get("benchmark_claim_allowed") is False,
        "reachable_task_scope": tuple(protocol.get("reachable_tasks", ()))
        == MECHANISM_REACHABLE_TASKS,
        "excluded_task_scope_explicit": set(protocol.get("excluded_tasks", {}))
        == {
            "partition-discovery",
            "electrochemical-conversion",
            "equilibrium-characterization",
        },
        "all_hashes_deterministic_and_changed": all(
            report["deterministic"] and report["hash_changed"]
            for task in task_reports.values()
            for report in task["modes"].values()
        ),
        "public_ids_opaque": all(
            report["opaque_public_id"]
            for task in task_reports.values()
            for report in task["modes"].values()
        ),
        "topology_graph_changes": all(
            task["modes"]["topology_family"]["reaction_count_delta"] == 1
            for task in task_reports.values()
        ),
        "rate_law_family_changes": all(
            task["modes"]["rate_law_family"]["rate_law_families_changed"]
            for task in task_reports.values()
        ),
        "task_responses_change": all(
            report["task_response_changed"]
            for task in task_reports.values()
            for report in task["modes"].values()
        ),
    }
    controls_ready = all(checks.values())
    return {
        "schema_version": MECHANISM_FAMILY_AUDIT_VERSION,
        "protocol_id": protocol.get("protocol_id"),
        "status": "controls_ready_experiments_pending" if controls_ready else "controls_failed",
        "controls_ready": controls_ready,
        "benchmark_claim_allowed": False,
        "publication_ready": False,
        "checks": checks,
        "tasks": task_reports,
        "excluded_tasks": protocol.get("excluded_tasks", {}),
        "limitations": [
            "The controls prove causal execution, not agent adaptation or scientific realism.",
            "Mechanism families currently cover only tasks that execute ReactionNetworkSpec.",
            "Multi-seed severity calibration and method comparisons remain pending.",
        ],
        "remaining_release_gates": list(protocol.get("remaining_release_gates", ())),
    }


def _intervention(mode: str) -> dict[str, Any]:
    return {"kind": "mechanism_family", "mode": mode, "severity": 0.8}


def _run_midpoint(task_id: str, mode: str | None) -> float:
    kwargs = get_task(task_id).env_kwargs(seed=0)
    if mode is not None:
        kwargs["world_interventions"] = [_intervention(mode)]
    env = gym.make("ChemWorld", **kwargs)
    try:
        env.reset(seed=0)
        task_info = cast(Any, env.unwrapped).task_info()
        recipe = task_recipe_from_unit_vector(
            task_info,
            np.full(task_recipe_dimension(task_info), 0.5),
        )
        info: dict[str, Any] = {}
        for action in recipe["steps"]:
            _, _, _, _, info = env.step(action)
        return float(info["leaderboard_score"])
    finally:
        env.close()


__all__ = [
    "DEFAULT_MECHANISM_FAMILY_PROTOCOL_PATH",
    "MECHANISM_FAMILY_AUDIT_VERSION",
    "audit_mechanism_families",
    "load_mechanism_family_protocol",
]
