"""Executable controls for candidate vNext world-family interventions."""

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
from chemworld.tasks import SERIOUS_TASK_IDS, get_task
from chemworld.world.scenario import DefaultScenarioGenerator, get_scenario
from chemworld.world.world_family import (
    WORLD_AXIS_REGISTRY,
    WORLD_FAMILY_INTERVENTION_VERSION,
    axes_for_task,
)

WORLD_FAMILY_AUDIT_VERSION = "chemworld-world-family-control-audit-0.1"
WORLD_FAMILY_PROTOCOL_VERSION = "chemworld-generalization-security-protocol-0.2"
DEFAULT_WORLD_FAMILY_PROTOCOL_PATH = (
    configuration_root() / "benchmark" / "generalization_security_vnext.json"
)


def load_world_family_protocol(
    path: str | Path = DEFAULT_WORLD_FAMILY_PROTOCOL_PATH,
) -> dict[str, Any]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("world-family protocol must be a JSON object")
    return payload


def audit_world_family_controls(
    protocol: dict[str, Any],
    *,
    run_response_probes: bool = True,
) -> dict[str, Any]:
    """Check registry, determinism, behavior, and public-information controls."""

    configured_tasks = protocol.get("tasks", {})
    required_modes = tuple(str(item) for item in protocol.get("required_modes", ()))
    registry_task_ids = tuple(SERIOUS_TASK_IDS)
    protocol_task_ids = tuple(configured_tasks) if isinstance(configured_tasks, dict) else ()
    task_scope_matches = protocol_task_ids == registry_task_ids
    task_reports: dict[str, dict[str, Any]] = {}
    deterministic = True
    mode_worlds_unique = True
    base_contract_preserved = True
    public_identity_hidden = True
    every_axis_changes_response = True

    for task_id in SERIOUS_TASK_IDS:
        registry_axes = axes_for_task(task_id)
        configured = configured_tasks.get(task_id, {}) if isinstance(configured_tasks, dict) else {}
        configured_axes = tuple(configured.get("axes", ())) if isinstance(configured, dict) else ()
        registered_axis_ids = tuple(axis.axis_id for axis in registry_axes)
        axis_reports: dict[str, dict[str, Any]] = {}
        base = DefaultScenarioGenerator().generate(get_scenario(task_id), 0)
        base_again = DefaultScenarioGenerator().generate(get_scenario(task_id), 0, ())
        task_base_preserved = _base_fingerprint(base) == _base_fingerprint(base_again)
        base_contract_preserved = base_contract_preserved and task_base_preserved

        for axis in registry_axes:
            mode_world_ids: list[str] = []
            mode_hashes: list[str] = []
            axis_deterministic = True
            for mode in required_modes:
                intervention = ({"axis_id": axis.axis_id, "mode": mode, "severity": 0.7},)
                first = DefaultScenarioGenerator().generate(get_scenario(task_id), 5, intervention)
                second = DefaultScenarioGenerator().generate(get_scenario(task_id), 5, intervention)
                first_hash = str(
                    first.initial_state.metadata.get("world_family_intervention_hash", "")
                )
                second_hash = str(
                    second.initial_state.metadata.get("world_family_intervention_hash", "")
                )
                mode_world_ids.append(first.parameters.world_id)
                mode_hashes.append(first_hash)
                axis_deterministic = (
                    axis_deterministic
                    and bool(first_hash)
                    and (
                        _intervention_fingerprint(first) == _intervention_fingerprint(second)
                        and first_hash == second_hash
                    )
                )
            axis_modes_unique = len(set(mode_world_ids)) == len(required_modes) and len(
                set(mode_hashes)
            ) == len(required_modes)
            deterministic = deterministic and axis_deterministic
            mode_worlds_unique = mode_worlds_unique and axis_modes_unique
            public_probe = _public_identity_probe(task_id, axis.axis_id)
            public_identity_hidden = public_identity_hidden and public_probe["passed"]
            response_probe = (
                _response_probe(task_id, axis.axis_id)
                if run_response_probes
                else {"executed": False, "changed": None}
            )
            if run_response_probes:
                every_axis_changes_response = every_axis_changes_response and bool(
                    response_probe["changed"]
                )
            axis_reports[axis.axis_id] = {
                "spec": axis.to_dict(),
                "registered_modes_match": tuple(axis.modes) == required_modes,
                "deterministic": axis_deterministic,
                "mode_worlds_unique": axis_modes_unique,
                "public_identity_probe": public_probe,
                "response_probe": response_probe,
            }

        task_reports[task_id] = {
            "configured_axes_match_registry": configured_axes == registered_axis_ids,
            "two_independent_axes_registered": len(registry_axes) == 2
            and len(set(registered_axis_ids)) == 2,
            "base_contract_preserved": task_base_preserved,
            "axes": axis_reports,
        }

    checks = {
        "schema": protocol.get("schema_version") == WORLD_FAMILY_PROTOCOL_VERSION,
        "intervention_contract": protocol.get("intervention_contract_version")
        == WORLD_FAMILY_INTERVENTION_VERSION,
        "candidate_is_non_claiming": protocol.get("benchmark_claim_allowed") is False,
        "task_scope_matches": task_scope_matches,
        "two_axes_per_task": all(
            report["two_independent_axes_registered"] for report in task_reports.values()
        ),
        "configured_axes_match_registry": all(
            report["configured_axes_match_registry"] for report in task_reports.values()
        ),
        "required_modes_registered": all(
            axis_report["registered_modes_match"]
            for task_report in task_reports.values()
            for axis_report in task_report["axes"].values()
        ),
        "deterministic_given_seed_and_intervention": deterministic,
        "mode_worlds_unique": mode_worlds_unique,
        "zero_intervention_preserves_base_contract": base_contract_preserved,
        "agent_facing_axis_identity_hidden": public_identity_hidden,
        "single_axis_probe_changes_task_response": (
            every_axis_changes_response if run_response_probes else None
        ),
    }
    controls_ready = all(value is True for value in checks.values())
    return {
        "schema_version": WORLD_FAMILY_AUDIT_VERSION,
        "protocol_id": protocol.get("protocol_id"),
        "status": "controls_ready_experiments_pending" if controls_ready else "controls_failed",
        "controls_ready": controls_ready,
        "benchmark_claim_allowed": False,
        "publication_ready": False,
        "checks": checks,
        "tasks": task_reports,
        "remaining_release_gates": list(protocol.get("remaining_release_gates", ())),
        "limitations": [
            "Control probes establish executable shifts, not method generalization.",
            "Severity grids and disjoint Train/Dev/Bench intervention allocations remain unfrozen.",
            "No paired multi-seed method comparison is attached to this control audit.",
        ],
    }


def _base_fingerprint(instance: Any) -> str:
    payload = {
        "world_id": instance.parameters.world_id,
        "provider": instance.parameters.provider,
        "domain": instance.parameters.domain_parameters,
        "species": instance.initial_state.species_amounts,
        "temperature_K": instance.initial_state.temperature_K,
        "pressure_Pa": instance.initial_state.pressure_Pa,
        "mechanism_hash": instance.compiled_mechanism.mechanism_hash,
        "intervention_hash": instance.initial_state.metadata.get("world_family_intervention_hash"),
    }
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), default=float)


def _intervention_fingerprint(instance: Any) -> str:
    payload = {
        "card": instance.to_card(),
        "domain": instance.parameters.domain_parameters,
        "catalyst_effects": instance.parameters.catalyst_effects.tolist(),
        "solvent_effects": instance.parameters.solvent_effects.tolist(),
        "species": instance.initial_state.species_amounts,
        "metadata": {
            key: value
            for key, value in instance.initial_state.metadata.items()
            if key.startswith("world_family_") or key.startswith("hidden_equilibrium_")
        },
    }
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), default=float)


def _response_probe(task_id: str, axis_id: str) -> dict[str, Any]:
    base_score, base_metrics = _run_midpoint_recipe(task_id, None)
    severity = -1.0 if axis_id == "electrochem.redox-kinetics" else 1.0
    shifted_score, shifted_metrics = _run_midpoint_recipe(task_id, axis_id, severity)
    metric_deltas = {
        key: shifted_metrics[key] - base_metrics[key]
        for key in sorted(set(base_metrics) & set(shifted_metrics))
    }
    score_delta = shifted_score - base_score
    max_absolute_delta = max([abs(score_delta), *(abs(value) for value in metric_deltas.values())])
    return {
        "executed": True,
        "changed": max_absolute_delta > 1.0e-8,
        "score_delta": score_delta,
        "success_metric_deltas": metric_deltas,
        "max_absolute_delta": max_absolute_delta,
    }


def _run_midpoint_recipe(
    task_id: str,
    axis_id: str | None,
    severity: float = 1.0,
) -> tuple[float, dict[str, float]]:
    kwargs = get_task(task_id).env_kwargs(seed=0)
    if axis_id is not None:
        kwargs["world_interventions"] = [
            {"axis_id": axis_id, "mode": "extrapolation", "severity": severity}
        ]
    env = gym.make("ChemWorld", **kwargs)
    try:
        env.reset(seed=0)
        base = cast(Any, env.unwrapped)
        task_info = base.task_info()
        vector = np.full(task_recipe_dimension(task_info), 0.5, dtype=float)
        recipe = task_recipe_from_unit_vector(task_info, vector)
        observation: dict[str, Any] = {}
        info: dict[str, Any] = {}
        for action in recipe["steps"]:
            observation, _, _, _, info = env.step(action)
        metrics = {
            field: float(np.asarray(observation[field]).reshape(-1)[0])
            for field in get_task(task_id).success_metrics
            if observation.get(field) is not None
        }
        return float(info["leaderboard_score"]), metrics
    finally:
        env.close()


def _public_identity_probe(task_id: str, axis_id: str) -> dict[str, Any]:
    kwargs = get_task(task_id).env_kwargs(seed=0)
    kwargs["world_interventions"] = [{"axis_id": axis_id, "mode": "interpolation", "severity": 0.7}]
    env = gym.make("ChemWorld", **kwargs)
    try:
        observation, info = env.reset(seed=0)
        public_payload = {
            "observation": observation,
            "reset_info": info,
            "task_info": cast(Any, env.unwrapped).task_info(),
        }
        rendered = json.dumps(public_payload, sort_keys=True, default=_json_default)
        forbidden = [
            axis_id,
            WORLD_AXIS_REGISTRY[axis_id].rationale,
        ]
        leaked = [item for item in forbidden if item and item in rendered]
        return {"passed": not leaked, "leaked_identifiers": leaked}
    finally:
        env.close()


def _json_default(value: Any) -> Any:
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.generic):
        return value.item()
    return str(value)


__all__ = [
    "DEFAULT_WORLD_FAMILY_PROTOCOL_PATH",
    "WORLD_FAMILY_AUDIT_VERSION",
    "audit_world_family_controls",
    "load_world_family_protocol",
]
