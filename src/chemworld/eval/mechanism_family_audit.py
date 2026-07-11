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

MECHANISM_FAMILY_AUDIT_VERSION = "chemworld-mechanism-family-control-audit-0.3"
MECHANISM_FAMILY_PROTOCOL_VERSION = "chemworld-mechanism-family-protocol-0.3"
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
    calibration = protocol["behavioral_calibration"]
    severity = float(calibration["severity"])
    seeds = tuple(int(item) for item in calibration["seeds"])
    probe_ids = tuple(str(item) for item in calibration["recipe_probes"])
    minimum_shift = float(calibration["minimum_abs_score_shift"])
    minimum_fraction = float(calibration["minimum_detectable_fraction"])
    maximum_p90 = float(calibration["maximum_p90_abs_score_shift"])
    balance_tolerance = float(calibration["mass_balance_tolerance"])
    task_reports: dict[str, Any] = {}
    for task_id in MECHANISM_REACHABLE_TASKS:
        scenario = get_scenario(task_id)
        base = DefaultScenarioGenerator().generate(scenario, 0)
        base_runs = {
            (seed, probe_id): _run_probe(task_id, seed, probe_id, None, severity)
            for seed in seeds
            for probe_id in probe_ids
        }
        mode_reports: dict[str, Any] = {}
        for mode in MECHANISM_TASK_MODES[task_id]:
            payload = (_intervention(mode, severity),)
            first = DefaultScenarioGenerator().generate(scenario, 0, payload)
            second = DefaultScenarioGenerator().generate(scenario, 0, payload)
            shifted_runs = {
                (seed, probe_id): _run_probe(task_id, seed, probe_id, mode, severity)
                for seed in seeds
                for probe_id in probe_ids
            }
            signed_deltas = [
                shifted_runs[key]["score"] - base_runs[key]["score"]
                for key in base_runs
            ]
            absolute_deltas = np.abs(np.asarray(signed_deltas, dtype=float))
            balance_errors = np.asarray(
                [item["mass_balance_error"] for item in shifted_runs.values()],
                dtype=float,
            )
            detectable_fraction = float(np.mean(absolute_deltas >= minimum_shift))
            median_abs_delta = float(np.median(absolute_deltas))
            p90_abs_delta = float(np.quantile(absolute_deltas, 0.9))
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
                "calibration": {
                    "severity": severity,
                    "seed_count": len(seeds),
                    "recipe_probe_count": len(probe_ids),
                    "paired_response_count": len(signed_deltas),
                    "minimum_abs_score_shift": minimum_shift,
                    "detectable_fraction": detectable_fraction,
                    "median_abs_score_delta": median_abs_delta,
                    "p90_abs_score_delta": p90_abs_delta,
                    "maximum_abs_score_delta": float(np.max(absolute_deltas)),
                    "mean_signed_score_delta": float(np.mean(signed_deltas)),
                    "behaviorally_distinguishable": median_abs_delta >= minimum_shift
                    and detectable_fraction >= minimum_fraction,
                    "noncatastrophic": p90_abs_delta <= maximum_p90,
                },
                "process_mass_balance_error_max": float(np.max(balance_errors)),
                "mass_balance_preserved": bool(
                    np.all(balance_errors <= balance_tolerance)
                ),
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
        "mechanism_families_behaviorally_distinguishable": all(
            report["calibration"]["behaviorally_distinguishable"]
            for task in task_reports.values()
            for report in task["modes"].values()
        ),
        "mechanism_shifts_are_noncatastrophic": all(
            report["calibration"]["noncatastrophic"]
            for task in task_reports.values()
            for report in task["modes"].values()
        ),
        "mass_balance_preserved": all(
            report["mass_balance_preserved"]
            for task in task_reports.values()
            for report in task["modes"].values()
        ),
        "calibration_design_is_multiseed_multiprobe": len(seeds) >= 5
        and len(probe_ids) >= 5,
        "replay_requires_separate_exact_intervention_context": protocol.get(
            "replay_binding", {}
        ).get("exact_intervention_payload_required")
        is True,
        "public_trajectory_retains_only_opaque_hash": protocol.get(
            "replay_binding", {}
        ).get("public_trajectory_payload_policy")
        == "opaque_intervention_version_and_hash_only",
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
        "behavioral_calibration": calibration,
        "limitations": [
            "The controls prove causal execution, not agent adaptation or scientific realism.",
            (
                "Effect-size calibration targets benchmark identifiability, "
                "not real chemical constants."
            ),
            "Core coverage includes reaction-network and partition constitutive-law families.",
            "Electrochemistry and equilibrium still lack dedicated constitutive-law families.",
            "Disjoint Train/Dev/Bench allocation and agent adaptation comparisons remain pending.",
        ],
        "remaining_release_gates": list(protocol.get("remaining_release_gates", ())),
    }


def _intervention(mode: str, severity: float) -> dict[str, Any]:
    return {"kind": "mechanism_family", "mode": mode, "severity": severity}


def _run_probe(
    task_id: str,
    seed: int,
    probe_id: str,
    mode: str | None,
    severity: float,
) -> dict[str, float]:
    kwargs = get_task(task_id).env_kwargs(seed=seed)
    if mode is not None:
        kwargs["world_interventions"] = [_intervention(mode, severity)]
    env = gym.make("ChemWorld", **kwargs)
    try:
        env.reset(seed=seed)
        task_info = cast(Any, env.unwrapped).task_info()
        dimension = task_recipe_dimension(task_info)
        recipe = task_recipe_from_unit_vector(
            task_info,
            _probe_vector(probe_id, dimension),
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


def _probe_vector(probe_id: str, dimension: int) -> np.ndarray:
    if probe_id == "low":
        return np.full(dimension, 0.2)
    if probe_id == "midpoint":
        return np.full(dimension, 0.5)
    if probe_id == "high":
        return np.full(dimension, 0.8)
    if probe_id == "ascending":
        return np.linspace(0.1, 0.9, dimension)
    if probe_id == "descending":
        return np.linspace(0.9, 0.1, dimension)
    raise ValueError(f"unknown mechanism calibration probe: {probe_id}")


__all__ = [
    "DEFAULT_MECHANISM_FAMILY_PROTOCOL_PATH",
    "MECHANISM_FAMILY_AUDIT_VERSION",
    "audit_mechanism_families",
    "load_mechanism_family_protocol",
]
