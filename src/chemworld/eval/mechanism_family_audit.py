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
    MECHANISM_TASK_MODES,
)
from chemworld.world.scenario import DefaultScenarioGenerator, get_scenario

MECHANISM_FAMILY_AUDIT_VERSION = "chemworld-mechanism-family-control-audit-0.2"
MECHANISM_FAMILY_PROTOCOL_VERSION = "chemworld-mechanism-family-protocol-0.2"
MECHANISM_FAMILY_MODES = (
    "rate_law_family",
    "topology_family",
    "constitutive_law_family",
)
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
        base_run = _run_midpoint(task_id, None)
        mode_reports: dict[str, Any] = {}
        for mode in MECHANISM_TASK_MODES[task_id]:
            payload = (_intervention(mode),)
            first = DefaultScenarioGenerator().generate(scenario, 0, payload)
            second = DefaultScenarioGenerator().generate(scenario, 0, payload)
            shifted_run = _run_midpoint(task_id, mode)
            first_hash = first.initial_state.metadata.get("mechanism_family_intervention_hash")
            second_hash = second.initial_state.metadata.get("mechanism_family_intervention_hash")
            base_exponent = base.parameters.domain_parameter("partition_coefficient_exponent")
            shifted_exponent = first.parameters.domain_parameter("partition_coefficient_exponent")
            mode_reports[mode] = {
                "deterministic": bool(first_hash) and first_hash == second_hash,
                "intervention_hash": first_hash,
                "network_hash_changed": first.compiled_mechanism.mechanism_hash
                != base.compiled_mechanism.mechanism_hash,
                "opaque_public_id": ":mechanism-" in first.parameters.world_id
                and mode not in first.parameters.world_id,
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
                "partition_coefficient_exponent": shifted_exponent,
                "constitutive_exponent_changed": shifted_exponent != base_exponent,
                "score_delta": shifted_run["score"] - base_run["score"],
                "task_response_changed": abs(shifted_run["score"] - base_run["score"]) > 1.0e-8,
                "process_mass_balance_error": shifted_run["mass_balance_error"],
                "mass_balance_preserved": shifted_run["mass_balance_error"] <= 1.0e-8,
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
        "task_mode_scope": protocol.get("task_modes")
        == {task_id: list(modes) for task_id, modes in MECHANISM_TASK_MODES.items()},
        "candidate_is_non_claiming": protocol.get("benchmark_claim_allowed") is False,
        "reachable_task_scope": tuple(protocol.get("reachable_tasks", ()))
        == MECHANISM_REACHABLE_TASKS,
        "excluded_task_scope_explicit": set(protocol.get("excluded_tasks", {}))
        == {"electrochemical-conversion", "equilibrium-characterization"},
        "all_intervention_hashes_deterministic": all(
            report["deterministic"]
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
            for task_id, task in task_reports.items()
            if "topology_family" in MECHANISM_TASK_MODES[task_id]
        ),
        "rate_law_family_changes": all(
            task["modes"]["rate_law_family"]["rate_law_families_changed"]
            for task_id, task in task_reports.items()
            if "rate_law_family" in MECHANISM_TASK_MODES[task_id]
        ),
        "reaction_network_hashes_change": all(
            report["network_hash_changed"]
            for task_id, task in task_reports.items()
            if task_id != "partition-discovery"
            for report in task["modes"].values()
        ),
        "partition_constitutive_family_changes": (
            task_reports["partition-discovery"]["modes"]["constitutive_law_family"][
                "constitutive_exponent_changed"
            ]
        ),
        "partition_preserves_reaction_network_identity": not (
            task_reports["partition-discovery"]["modes"]["constitutive_law_family"][
                "network_hash_changed"
            ]
        ),
        "task_responses_change": all(
            report["task_response_changed"]
            for task in task_reports.values()
            for report in task["modes"].values()
        ),
        "mass_balance_preserved": all(
            report["mass_balance_preserved"]
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
            "Core coverage now includes reaction-network and partition constitutive-law families.",
            "Electrochemistry and equilibrium still lack dedicated constitutive-law families.",
            "Multi-seed severity calibration and method comparisons remain pending.",
        ],
        "remaining_release_gates": list(protocol.get("remaining_release_gates", ())),
    }


def _intervention(mode: str) -> dict[str, Any]:
    return {"kind": "mechanism_family", "mode": mode, "severity": 0.8}


def _run_midpoint(task_id: str, mode: str | None) -> dict[str, float]:
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
        raw_signal = info.get("raw_signal", {})
        mass_balance = raw_signal.get("mass_balance", {}) if isinstance(raw_signal, dict) else {}
        raw_balance_error = (
            mass_balance.get("process_mass_balance_error")
            if isinstance(mass_balance, dict)
            else None
        )
        mass_balance_error = (
            abs(float(np.asarray(raw_balance_error).reshape(-1)[0]))
            if raw_balance_error is not None
            else float("inf")
        )
        return {
            "score": float(info["leaderboard_score"]),
            "mass_balance_error": mass_balance_error,
        }
    finally:
        env.close()


__all__ = [
    "DEFAULT_MECHANISM_FAMILY_PROTOCOL_PATH",
    "MECHANISM_FAMILY_AUDIT_VERSION",
    "audit_mechanism_families",
    "load_mechanism_family_protocol",
]
