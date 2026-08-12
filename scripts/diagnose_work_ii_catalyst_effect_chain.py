#!/usr/bin/env python3
"""Diagnose the complete reaction-safety catalyst effect chain without a provider."""

from __future__ import annotations

import argparse
import json
import subprocess
import tempfile
from collections.abc import Mapping
from math import isfinite
from pathlib import Path
from time import perf_counter
from typing import Any

import gymnasium as gym
import numpy as np

import chemworld  # noqa: F401
from chemworld.data.logging import load_jsonl
from chemworld.eval.provenance import (
    canonical_json_sha256,
    file_sha256,
    git_source_commit,
    write_json_atomic,
)
from chemworld.eval.runner import run_agent
from chemworld.eval.verify import verify_records
from chemworld.eval.work_ii_catalyst_deactivation_q0 import stable_catalyst_intervention
from chemworld.eval.work_ii_truth import _FrozenTruthReplayAgent
from chemworld.foundation import equipment_settings
from chemworld.tasks import get_task
from chemworld.world.reaction_kernel import _hidden_reaction_modifier

ROOT = Path(__file__).resolve().parents[1]
TASK_ID = "reaction-safety-constrained"
WORLD_SEED = 0
TEMPERATURES_K = (350.0, 410.0, 465.0)
DURATIONS_S = (1_800.0, 7_200.0, 14_400.0)
POSITIVE_DOSES_MOL = (0.000120, 0.000315, 0.000520)
LAW_IDS = ("deactivating_baseline", "stable_catalyst")
SPECIES_IDS = ("A", "P", "B", "D", "Cat_active", "Cat_dead")
DIRECT_METRICS = ("yield", "conversion", "selectivity")
TOTAL_PRIMARY_EXECUTIONS = (
    len(TEMPERATURES_K) * len(DURATIONS_S) * (1 + len(POSITIVE_DOSES_MOL) * len(LAW_IDS))
)
DEFAULT_OUTPUT = (
    ROOT
    / "workstreams/flagship_tasks/reports/"
    / "work-ii-catalyst-effect-chain-diagnostic-20260812.json"
)
SCOPED_RUNTIME_PREFIXES = ("src/", "scripts/", "configs/", "workstreams/flagship_tasks/")


def _scoped_dirty_paths() -> list[str]:
    """Return material Work II/runtime paths that are not committed at launch."""

    completed = subprocess.run(
        ["git", "status", "--porcelain=v1", "--untracked-files=all"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    dirty = []
    for line in completed.stdout.splitlines():
        path = line[3:].strip().replace("\\", "/")
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        if path.startswith(SCOPED_RUNTIME_PREFIXES):
            dirty.append(path)
    return sorted(dirty)


def _actions(
    *,
    temperature_K: float,
    duration_s: float,
    catalyst_amount_mol: float,
) -> list[dict[str, Any]]:
    actions = [
        {"operation": "add_solvent", "volume_L": 0.025, "solvent": 0},
        {"operation": "add_reagent", "amount_mol": 0.015},
    ]
    if catalyst_amount_mol > 0.0:
        actions.append(
            {
                "operation": "add_catalyst",
                "catalyst_amount_mol": catalyst_amount_mol,
                "catalyst": 1,
            }
        )
    actions.extend(
        [
            {
                "operation": "heat",
                "target_temperature_K": temperature_K,
                "duration_s": duration_s,
                "stirring_speed_rpm": 675.0,
            },
            {"operation": "quench"},
            {"operation": "measure", "instrument": "hplc"},
            {"operation": "terminate"},
            {"operation": "measure", "instrument": "final_assay"},
        ]
    )
    return actions


def _species(state: Any) -> dict[str, float]:
    return {
        species_id: float(state.species_amounts.get(species_id, 0.0))
        for species_id in SPECIES_IDS
    }


def _truth(base_env: Any, state: Any) -> dict[str, float]:
    values = base_env.observation_kernel._truth_values(state)
    return {str(key): float(value) for key, value in values.items()}


def _adjusted_rates(base_env: Any, state: Any, *, stirring_speed_rpm: float) -> dict[str, float]:
    network = base_env.scenario_instance.compiled_mechanism.network
    rates = network.reaction_rates(
        state.species_amounts,
        volume_L=state.volume_L,
        temperature_K=state.temperature_K,
    )
    settings = equipment_settings(state.equipment, "batch_reactor")
    catalyst = int(settings.get("catalyst", 0))
    solvent = int(settings.get("solvent", 0))
    stirring_factor = 0.70 + 0.30 * (1.0 - np.exp(-stirring_speed_rpm / 420.0))
    return {
        reaction.reaction_id: float(
            rates[reaction.reaction_id]
            * _hidden_reaction_modifier(
                base_env.world,
                catalyst=catalyst,
                solvent=solvent,
                reaction_index=index,
                stirring_factor=float(stirring_factor),
                state=state,
            )
        )
        for index, reaction in enumerate(network.reactions)
    }


def _public_observation(observation: Mapping[str, Any]) -> dict[str, float | None]:
    result: dict[str, float | None] = {}
    for key, value in observation.items():
        array = np.asarray(value)
        numeric = None if array.size == 0 else float(array.reshape(-1)[0])
        result[str(key)] = numeric if numeric is not None and isfinite(numeric) else None
    return result


def _sampling_audit(before: Any, after: Any) -> dict[str, Any]:
    volume_factor = float(after.volume_L / before.volume_L)
    amount_residuals = {
        species_id: float(
            after.species_amounts.get(species_id, 0.0)
            - before.species_amounts.get(species_id, 0.0) * volume_factor
        )
        for species_id in SPECIES_IDS
    }
    return {
        "volume_factor": volume_factor,
        "maximum_amount_scaling_residual_mol": max(
            (abs(value) for value in amount_residuals.values()),
            default=0.0,
        ),
        "amount_scaling_residuals_mol": amount_residuals,
        "pre_withdrawal_truth": _truth_values_for_state(before),
        "post_withdrawal_truth": _truth_values_for_state(after),
    }


def _truth_values_for_state(state: Any) -> dict[str, float]:
    initial = max(float(state.species.initial_amounts_mol.get("A", 0.0)), 1.0e-12)
    target = float(state.species_amounts.get("P", 0.0))
    remaining = float(state.species_amounts.get("A", 0.0))
    impurity = sum(
        float(state.species_amounts.get(species_id, 0.0))
        for species_id in ("B", "D", "Cat_dead")
    )
    consumed = max(initial - remaining, 1.0e-12)
    return {
        "yield": float(np.clip(target / initial, 0.0, 1.0)),
        "conversion": float(np.clip(consumed / initial, 0.0, 1.0)),
        "selectivity": float(np.clip(target / consumed, 0.0, 1.0)),
        "impurity_fraction": float(np.clip(impurity / initial, 0.0, 1.0)),
    }


def _execute_once(
    *,
    temperature_K: float,
    duration_s: float,
    catalyst_amount_mol: float,
    law_id: str,
    namespace: str,
) -> dict[str, Any]:
    task = get_task(TASK_ID)
    interventions = () if law_id == "deactivating_baseline" else (stable_catalyst_intervention(),)
    actions = _actions(
        temperature_K=temperature_K,
        duration_s=duration_s,
        catalyst_amount_mol=catalyst_amount_mol,
    )
    env = gym.make(
        task.env_id,
        task_id=TASK_ID,
        seed=WORLD_SEED,
        budget_override=len(actions) + 1,
        episode_mode_override="single_experiment",
        world_interventions=interventions,
        observation_seed_override=0,
        observation_noise_mode="keyed",
        observation_noise_namespace=namespace,
        debug_truth=True,
    )
    try:
        env.reset(seed=WORLD_SEED)
        base = env.unwrapped
        snapshots: dict[str, dict[str, Any]] = {}
        measurement_payloads: dict[str, dict[str, Any]] = {}
        final_info: dict[str, Any] = {}
        for action in actions:
            state_before_action = base._state
            observation, _, terminated, truncated, info = env.step(action)
            if info.get("transaction_status") != "committed":
                raise RuntimeError(
                    f"noncommitted {action['operation']}: "
                    f"status={info.get('transaction_status')} reason={info.get('rollback_reason')}"
                )
            operation = str(action["operation"])
            if operation == "add_catalyst" or (
                operation == "add_reagent" and catalyst_amount_mol == 0.0
            ):
                state = base._state
                snapshots["charged"] = {
                    "species_amounts_mol": _species(state),
                    "temperature_K": float(state.temperature_K),
                    "volume_L": float(state.volume_L),
                    "truth": _truth(base, state),
                    "adjusted_rates_mol_L_s": _adjusted_rates(
                        base,
                        state,
                        stirring_speed_rpm=675.0,
                    ),
                }
            elif operation == "heat":
                state = base._state
                snapshots["post_heat"] = {
                    "species_amounts_mol": _species(state),
                    "temperature_K": float(state.temperature_K),
                    "volume_L": float(state.volume_L),
                    "truth": _truth(base, state),
                    "adjusted_rates_mol_L_s": _adjusted_rates(
                        base,
                        state,
                        stirring_speed_rpm=675.0,
                    ),
                }
            elif operation == "quench":
                state = base._state
                snapshots["post_quench"] = {
                    "species_amounts_mol": _species(state),
                    "temperature_K": float(state.temperature_K),
                    "volume_L": float(state.volume_L),
                    "truth": _truth(base, state),
                }
            elif operation == "measure":
                instrument = str(action["instrument"])
                state_after_action = base._state
                snapshots[f"pre_{instrument}"] = {
                    "species_amounts_mol": _species(state_before_action),
                    "temperature_K": float(state_before_action.temperature_K),
                    "volume_L": float(state_before_action.volume_L),
                    "truth": _truth(base, state_before_action),
                }
                measurement_payloads[instrument] = {
                    "observation": _public_observation(observation),
                    "observed_mask": {
                        str(key): bool(value)
                        for key, value in info.get("observed_mask", {}).items()
                    },
                    "processed_estimate": {
                        str(key): (
                            float(value)
                            if value is not None and isfinite(float(value))
                            else None
                        )
                        for key, value in info.get("processed_estimate", {}).items()
                    },
                    "uncertainty": {
                        str(key): float(value)
                        for key, value in info.get("uncertainty", {}).items()
                    },
                    "sampling_audit": _sampling_audit(
                        state_before_action,
                        state_after_action,
                    ),
                }
                if instrument == "final_assay":
                    final_info = dict(info)
            if truncated:
                raise RuntimeError(f"execution truncated at {operation}")
            if terminated and operation != "measure":
                raise RuntimeError(f"execution terminated before final assay at {operation}")

        final_state = base._state
        snapshots["post_final_assay"] = {
            "species_amounts_mol": _species(final_state),
            "temperature_K": float(final_state.temperature_K),
            "volume_L": float(final_state.volume_L),
            "truth": _truth(base, final_state),
        }
        post_heat_species = snapshots["post_heat"]["species_amounts_mol"]
        initial_reactant = 0.015
        derived = {
            "active_catalyst_fraction_post_heat": (
                None
                if catalyst_amount_mol == 0.0
                else post_heat_species["Cat_active"] / catalyst_amount_mol
            ),
            "dead_catalyst_fraction_post_heat": (
                None
                if catalyst_amount_mol == 0.0
                else post_heat_species["Cat_dead"] / catalyst_amount_mol
            ),
            "catalyst_inventory_error_mol_post_heat": (
                post_heat_species["Cat_active"]
                + post_heat_species["Cat_dead"]
                - catalyst_amount_mol
            ),
            "target_formation_fraction_post_heat": (
                post_heat_species["P"] + post_heat_species["D"]
            )
            / initial_reactant,
            "side_formation_fraction_post_heat": post_heat_species["B"] / initial_reactant,
            "final_leaderboard_score": float(final_info["leaderboard_score"]),
            "final_safety_risk": float(
                measurement_payloads["final_assay"]["observation"]["safety_risk"]
            ),
        }
        payload = {
            "temperature_K": temperature_K,
            "duration_s": duration_s,
            "catalyst_amount_mol": catalyst_amount_mol,
            "law_id": law_id,
            "mechanism_hash": base.scenario_instance.compiled_mechanism.mechanism_hash,
            "mechanism_metadata": dict(
                base.scenario_instance.compiled_mechanism.network.metadata
            ),
            "reaction_ids": [
                reaction.reaction_id
                for reaction in base.scenario_instance.compiled_mechanism.network.reactions
            ],
            "snapshots": snapshots,
            "measurements": measurement_payloads,
            "derived": derived,
        }
        payload["execution_sha256"] = canonical_json_sha256(payload)
        return payload
    finally:
        env.close()


def _official_exact_replay(
    *,
    temperature_K: float,
    duration_s: float,
    catalyst_amount_mol: float,
    law_id: str,
    namespace: str,
) -> dict[str, Any]:
    task = get_task(TASK_ID)
    actions = _actions(
        temperature_K=temperature_K,
        duration_s=duration_s,
        catalyst_amount_mol=catalyst_amount_mol,
    )
    interventions = () if law_id == "deactivating_baseline" else (stable_catalyst_intervention(),)
    with tempfile.TemporaryDirectory(prefix="chemworld-catalyst-effect-chain-") as directory:
        trajectory = Path(directory) / "trajectory.jsonl"
        run_agent(
            env_id=task.env_id,
            agent=_FrozenTruthReplayAgent(actions),
            world_split=task.world_split,
            budget=len(actions) + 1,
            objective=task.objective,
            seed=WORLD_SEED,
            agent_seed=0,
            observation_seed=0,
            task_id=TASK_ID,
            output_path=trajectory,
            budget_override=len(actions) + 1,
            episode_mode_override="single_experiment",
            observation_noise_mode="keyed",
            observation_noise_namespace=namespace,
            world_interventions=interventions,
        )
        records = load_jsonl(trajectory)
        verification = verify_records(
            records,
            tolerance=0.0,
            world_interventions=interventions,
        ).to_dict()
    return {
        "verified": verification.get("verified") is True,
        "record_count": len(records),
        "committed_record_count": sum(
            row.get("transaction_status") == "committed" for row in records
        ),
        "all_records_committed": all(
            row.get("transaction_status") == "committed" for row in records
        ),
        "verification": verification,
    }


def _max_abs_delta(rows: list[dict[str, Any]], field: str) -> float:
    return max((abs(float(row[field])) for row in rows), default=0.0)


def _campaign_reset_check() -> dict[str, Any]:
    task = get_task(TASK_ID)
    actions = _actions(
        temperature_K=410.0,
        duration_s=1_800.0,
        catalyst_amount_mol=0.000315,
    )
    env = gym.make(
        task.env_id,
        task_id=TASK_ID,
        seed=WORLD_SEED,
        budget_override=len(actions) + 1,
        episode_mode_override="campaign",
        debug_truth=True,
    )
    try:
        env.reset(seed=WORLD_SEED)
        base = env.unwrapped
        final_info: dict[str, Any] = {}
        for action in actions:
            _, _, _, truncated, final_info = env.step(action)
            if truncated or final_info.get("transaction_status") != "committed":
                raise RuntimeError("campaign reset check did not complete its first experiment")
        fresh = base._state
        return {
            "experiment_completed": final_info.get("experiment_completed") is True,
            "next_experiment_ready": final_info.get("next_experiment_ready") is True,
            "fresh_volume_L": float(fresh.volume_L),
            "fresh_time_s": float(fresh.ledger.time_s),
            "fresh_species_amounts_mol": _species(fresh),
            "all_physical_species_reset": all(
                abs(float(value)) <= 1.0e-15 for value in fresh.species_amounts.values()
            ),
            "fresh_batch_confirmed": (
                final_info.get("experiment_completed") is True
                and final_info.get("next_experiment_ready") is True
                and abs(float(fresh.volume_L)) <= 1.0e-15
                and abs(float(fresh.ledger.time_s)) <= 1.0e-15
                and all(abs(float(value)) <= 1.0e-15 for value in fresh.species_amounts.values())
            ),
        }
    finally:
        env.close()


def _analyze(rows: list[dict[str, Any]], campaign_reset: Mapping[str, Any]) -> dict[str, Any]:
    failures = [row for row in rows if row.get("status") != "completed"]
    primary = [row for row in rows if row.get("status") == "completed"]
    expected_keys = {
        (temperature_K, duration_s, 0.0, "deactivating_baseline")
        for temperature_K in TEMPERATURES_K
        for duration_s in DURATIONS_S
    }
    expected_keys.update(
        (temperature_K, duration_s, dose, law_id)
        for temperature_K in TEMPERATURES_K
        for duration_s in DURATIONS_S
        for dose in POSITIVE_DOSES_MOL
        for law_id in LAW_IDS
    )
    by_key = {
        (
            float(row["temperature_K"]),
            float(row["duration_s"]),
            float(row["catalyst_amount_mol"]),
            str(row["law_id"]),
        ): row
        for row in primary
    }
    completed_keys = set(by_key)
    denominators = {
        "primary_executions": len(rows),
        "completed": len(primary),
        "failed": len(failures),
        "official_replay_attempts": sum(
            row.get("official_replay_attempted") is True for row in rows
        ),
        "official_exact_replays": sum(
            row.get("official_exact_replay") is True for row in rows
        ),
        "projection_replays": sum(
            row.get("projection_replay_equal") is True for row in rows
        ),
    }
    completeness_checks = {
        "fixed_63_execution_denominator": len(rows) == TOTAL_PRIMARY_EXECUTIONS,
        "all_expected_cells_present": completed_keys == expected_keys,
        "zero_execution_failures": not failures,
        "all_official_exact_replays": denominators["official_exact_replays"]
        == TOTAL_PRIMARY_EXECUTIONS,
        "all_projection_replays_equal": denominators["projection_replays"]
        == TOTAL_PRIMARY_EXECUTIONS,
    }
    if not all(completeness_checks.values()):
        return {
            "denominators": denominators,
            "completeness_checks": completeness_checks,
            "runtime_checks": {},
            "mechanism_activation": {},
            "catalyst_vs_no_catalyst_truth": [],
            "stable_vs_deactivating_truth": [],
            "stable_vs_deactivating_public_hplc": [],
            "dose_summary": {},
            "high_temperature_tradeoff": [],
            "findings": {"analysis_complete": False},
            "classification": ["execution_or_replay_failure"],
            "failures": failures,
        }
    catalyst_vs_none: list[dict[str, Any]] = []
    stable_vs_deactivating_truth: list[dict[str, Any]] = []
    stable_vs_deactivating_public: list[dict[str, Any]] = []
    dose_summary: dict[str, dict[str, float]] = {}

    for temperature_K in TEMPERATURES_K:
        for duration_s in DURATIONS_S:
            no_catalyst = by_key[(temperature_K, duration_s, 0.0, "deactivating_baseline")]
            no_truth = no_catalyst["execution"]["snapshots"]["post_heat"]["truth"]
            no_target_fraction = no_catalyst["execution"]["derived"][
                "target_formation_fraction_post_heat"
            ]
            for dose in POSITIVE_DOSES_MOL:
                deactivating = by_key[(temperature_K, duration_s, dose, "deactivating_baseline")]
                stable = by_key[(temperature_K, duration_s, dose, "stable_catalyst")]
                for law_id, treatment in (
                    ("deactivating_baseline", deactivating),
                    ("stable_catalyst", stable),
                ):
                    execution = treatment["execution"]
                    truth = execution["snapshots"]["post_heat"]["truth"]
                    catalyst_vs_none.append(
                        {
                            "temperature_K": temperature_K,
                            "duration_s": duration_s,
                            "catalyst_amount_mol": dose,
                            "law_id": law_id,
                            "yield_delta": truth["yield"] - no_truth["yield"],
                            "conversion_delta": truth["conversion"] - no_truth["conversion"],
                            "selectivity_delta": truth["selectivity"] - no_truth["selectivity"],
                            "target_formation_fraction_delta": (
                                execution["derived"]["target_formation_fraction_post_heat"]
                                - no_target_fraction
                            ),
                            "charged_target_rate_mol_L_s": execution["snapshots"][
                                "charged"
                            ]["adjusted_rates_mol_L_s"]["catalytic_target"],
                            "no_catalyst_target_rate_mol_L_s": no_catalyst["execution"][
                                "snapshots"
                            ]["charged"]["adjusted_rates_mol_L_s"]["catalytic_target"],
                            "post_heat_target_product_delta_mol": (
                                execution["snapshots"]["post_heat"]["species_amounts_mol"]["P"]
                                - no_catalyst["execution"]["snapshots"]["post_heat"][
                                    "species_amounts_mol"
                                ]["P"]
                            ),
                        }
                    )
                deact_execution = deactivating["execution"]
                stable_execution = stable["execution"]
                deact_truth = deact_execution["snapshots"]["post_heat"]["truth"]
                stable_truth = stable_execution["snapshots"]["post_heat"]["truth"]
                stable_vs_deactivating_truth.append(
                    {
                        "temperature_K": temperature_K,
                        "duration_s": duration_s,
                        "catalyst_amount_mol": dose,
                        "yield_delta": stable_truth["yield"] - deact_truth["yield"],
                        "conversion_delta": stable_truth["conversion"] - deact_truth["conversion"],
                        "selectivity_delta": (
                            stable_truth["selectivity"] - deact_truth["selectivity"]
                        ),
                        "target_formation_fraction_delta": (
                            stable_execution["derived"]["target_formation_fraction_post_heat"]
                            - deact_execution["derived"]["target_formation_fraction_post_heat"]
                        ),
                        "product_degradation_fraction_delta": (
                            stable_execution["snapshots"]["post_heat"]["species_amounts_mol"]["D"]
                            - deact_execution["snapshots"]["post_heat"]["species_amounts_mol"]["D"]
                        )
                        / 0.015,
                        "active_fraction_deactivating": deact_execution["derived"][
                            "active_catalyst_fraction_post_heat"
                        ],
                    }
                )
                deact_hplc = deact_execution["measurements"]["hplc"]
                stable_hplc = stable_execution["measurements"]["hplc"]
                public_row: dict[str, Any] = {
                    "temperature_K": temperature_K,
                    "duration_s": duration_s,
                    "catalyst_amount_mol": dose,
                    "all_direct_metrics_observed": all(
                        deact_hplc["observed_mask"].get(metric) is True
                        and stable_hplc["observed_mask"].get(metric) is True
                        and deact_hplc["processed_estimate"].get(metric) is not None
                        and stable_hplc["processed_estimate"].get(metric) is not None
                        for metric in DIRECT_METRICS
                    ),
                }
                for metric in DIRECT_METRICS:
                    public_row[f"{metric}_delta"] = float(
                        stable_hplc["processed_estimate"][metric]
                        - deact_hplc["processed_estimate"][metric]
                    )
                public_row["metrics_above_w2_33_gate"] = sum(
                    abs(float(public_row[f"{metric}_delta"])) >= gate
                    for metric, gate in (
                        ("yield", 0.050),
                        ("conversion", 0.050),
                        ("selectivity", 0.054),
                    )
                )
                stable_vs_deactivating_public.append(public_row)

    for dose in POSITIVE_DOSES_MOL:
        selected = [
            row
            for row in stable_vs_deactivating_truth
            if row["catalyst_amount_mol"] == dose
        ]
        dose_summary[f"{dose:.6f}"] = {
            "mean_yield_delta": float(np.mean([row["yield_delta"] for row in selected])),
            "max_yield_delta": max(row["yield_delta"] for row in selected),
            "mean_target_formation_fraction_delta": float(
                np.mean([row["target_formation_fraction_delta"] for row in selected])
            ),
            "minimum_active_fraction_deactivating": min(
                row["active_fraction_deactivating"] for row in selected
            ),
        }

    high_temperature_tradeoff: list[dict[str, Any]] = []
    for duration_s in DURATIONS_S:
        for dose in POSITIVE_DOSES_MOL:
            row_410 = by_key[(410.0, duration_s, dose, "deactivating_baseline")]
            row_465 = by_key[(465.0, duration_s, dose, "deactivating_baseline")]
            stable_410 = by_key[(410.0, duration_s, dose, "stable_catalyst")]
            stable_465 = by_key[(465.0, duration_s, dose, "stable_catalyst")]
            deact_yield_change = (
                row_465["execution"]["snapshots"]["post_heat"]["truth"]["yield"]
                - row_410["execution"]["snapshots"]["post_heat"]["truth"]["yield"]
            )
            stable_yield_change = (
                stable_465["execution"]["snapshots"]["post_heat"]["truth"]["yield"]
                - stable_410["execution"]["snapshots"]["post_heat"]["truth"]["yield"]
            )
            high_temperature_tradeoff.append(
                {
                    "duration_s": duration_s,
                    "catalyst_amount_mol": dose,
                    "deactivating_yield_change_465_minus_410": deact_yield_change,
                    "stable_yield_change_465_minus_410": stable_yield_change,
                    "deactivation_specific_difference_in_difference": (
                        stable_yield_change - deact_yield_change
                    ),
                }
            )

    charged_dose_errors = [
        abs(
            row["execution"]["snapshots"]["charged"]["species_amounts_mol"]["Cat_active"]
            - float(row["catalyst_amount_mol"])
        )
        for row in primary
    ]
    inventory_errors = [
        abs(
            row["execution"]["derived"]["catalyst_inventory_error_mol_post_heat"]
        )
        for row in primary
    ]
    no_catalyst_rows = [row for row in primary if float(row["catalyst_amount_mol"]) == 0.0]
    no_catalyst_target_rates = [
        abs(
            row["execution"]["snapshots"]["charged"]["adjusted_rates_mol_L_s"][
                "catalytic_target"
            ]
        )
        for row in no_catalyst_rows
    ]
    no_catalyst_products = [
        abs(row["execution"]["snapshots"]["post_heat"]["species_amounts_mol"]["P"])
        for row in no_catalyst_rows
    ]
    stable_reaction_sets = {
        tuple(row["execution"]["reaction_ids"])
        for row in primary
        if row["law_id"] == "stable_catalyst"
    }
    deactivating_reaction_sets = {
        tuple(row["execution"]["reaction_ids"])
        for row in primary
        if row["law_id"] == "deactivating_baseline"
    }
    stable_hashes = {
        row["execution"]["mechanism_hash"]
        for row in primary
        if row["law_id"] == "stable_catalyst"
    }
    deactivating_hashes = {
        row["execution"]["mechanism_hash"]
        for row in primary
        if row["law_id"] == "deactivating_baseline"
    }
    stable_metadata = {
        canonical_json_sha256(row["execution"]["mechanism_metadata"])
        for row in primary
        if row["law_id"] == "stable_catalyst"
    }
    sampling_audits = [
        execution["measurements"][instrument]["sampling_audit"]
        for row in primary
        for execution in (row["execution"],)
        for instrument in ("hplc", "final_assay")
    ]
    observation_binding_residuals = []
    for row in primary:
        execution = row["execution"]
        hplc = execution["measurements"]["hplc"]
        pre_truth = execution["snapshots"]["pre_hplc"]["truth"]
        for metric in DIRECT_METRICS:
            observed = hplc["processed_estimate"].get(metric)
            sigma = float(hplc["uncertainty"].get(f"{metric}_std", 0.0))
            if observed is not None:
                observation_binding_residuals.append(
                    {
                        "absolute_residual": abs(float(observed) - float(pre_truth[metric])),
                        "five_sigma_bound": 5.0 * sigma + 1.0e-12,
                    }
                )
    max_catalyst_yield_effect = max(row["yield_delta"] for row in catalyst_vs_none)
    max_stable_yield_effect = max(
        row["yield_delta"] for row in stable_vs_deactivating_truth
    )
    max_stable_integrated_effect = max(
        row["target_formation_fraction_delta"]
        for row in stable_vs_deactivating_truth
    )
    high_dose = dose_summary[f"{max(POSITIVE_DOSES_MOL):.6f}"]
    middle_dose = dose_summary[f"{POSITIVE_DOSES_MOL[1]:.6f}"]
    stable_set = set(next(iter(stable_reaction_sets)))
    deactivating_set = set(next(iter(deactivating_reaction_sets)))
    stable_metadata_rows = [
        row["execution"]["mechanism_metadata"]
        for row in primary
        if row["law_id"] == "stable_catalyst"
    ]
    runtime_checks = {
        **completeness_checks,
        "charged_dose_written_exactly": max(charged_dose_errors, default=0.0) <= 1.0e-15,
        "catalyst_inventory_conserved": max(inventory_errors, default=0.0) <= 1.0e-10,
        "no_catalyst_target_rate_is_zero": max(no_catalyst_target_rates, default=0.0)
        <= 1.0e-15,
        "no_catalyst_target_product_is_zero": max(no_catalyst_products, default=0.0) <= 1.0e-12,
        "stable_topology_removes_only_deactivation": (
            len(stable_reaction_sets) == 1
            and len(deactivating_reaction_sets) == 1
            and stable_set == deactivating_set - {"catalyst_deactivation"}
            and not (stable_set - deactivating_set)
            and len(stable_hashes) == 1
            and len(deactivating_hashes) == 1
            and stable_hashes != deactivating_hashes
            and len(stable_metadata) == 1
            and all(
                metadata.get("derived_family_transform_id")
                == "stable_catalyst_topology_v1"
                and metadata.get("derived_family_target_reaction_id")
                == "catalyst_deactivation"
                for metadata in stable_metadata_rows
            )
        ),
        "destructive_sampling_is_exactly_proportional": max(
            audit["maximum_amount_scaling_residual_mol"] for audit in sampling_audits
        )
        <= 1.0e-12,
        "hplc_observation_binds_pre_withdrawal_state": all(
            item["absolute_residual"] <= item["five_sigma_bound"]
            for item in observation_binding_residuals
        ),
        "all_public_hplc_direct_metrics_observed": all(
            row["all_direct_metrics_observed"]
            for row in stable_vs_deactivating_public
        ),
        "campaign_final_assay_starts_fresh_physical_batch": campaign_reset.get(
            "fresh_batch_confirmed"
        )
        is True,
    }
    mechanism_activation = {
        "max_active_catalyst_loss_fraction": max(
            1.0 - float(row["active_fraction_deactivating"])
            for row in stable_vs_deactivating_truth
        ),
        "max_stable_minus_deactivating_yield": max_stable_yield_effect,
        "max_stable_minus_deactivating_conversion": max(
            row["conversion_delta"] for row in stable_vs_deactivating_truth
        ),
        "max_stable_minus_deactivating_selectivity": max(
            row["selectivity_delta"] for row in stable_vs_deactivating_truth
        ),
        "max_stable_minus_deactivating_target_formation_fraction": (
            max_stable_integrated_effect
        ),
    }
    catalyst_functionality_supported = (
        all(row["charged_target_rate_mol_L_s"] > 0.0 for row in catalyst_vs_none)
        and all(
            abs(row["no_catalyst_target_rate_mol_L_s"]) <= 1.0e-15
            for row in catalyst_vs_none
        )
        and all(row["post_heat_target_product_delta_mol"] > 0.0 for row in catalyst_vs_none)
        and max_catalyst_yield_effect >= 0.10
    )
    public_supporting_cells = sum(
        row["metrics_above_w2_33_gate"] >= 2
        for row in stable_vs_deactivating_public
    )
    endpoint_compression_cells = sum(
        row["target_formation_fraction_delta"] - row["yield_delta"] >= 0.003
        for row in stable_vs_deactivating_truth
    )
    robust_high_temperature_cells = sum(
        row["deactivating_yield_change_465_minus_410"] <= -0.03
        and row["deactivation_specific_difference_in_difference"] >= 0.01
        for row in high_temperature_tradeoff
    )
    findings = {
        "analysis_complete": True,
        "runtime_implementation_defect_detected": not all(runtime_checks.values()),
        "catalyst_functionality_supported": catalyst_functionality_supported,
        "catalyst_functionality_max_yield_effect_vs_no_catalyst": max_catalyst_yield_effect,
        "deactivation_publicly_identifiable_at_w2_33_gate": public_supporting_cells > 0,
        "public_effect_supporting_cells": public_supporting_cells,
        "dose_masking_supported": (
            middle_dose["mean_yield_delta"] - high_dose["mean_yield_delta"] >= 0.003
            and high_dose["minimum_active_fraction_deactivating"] > 0.50
        ),
        "endpoint_compression_supported": endpoint_compression_cells >= 2,
        "endpoint_compression_cells": endpoint_compression_cells,
        "fresh_batch_partial_ageing_masks_campaign_accumulation": (
            catalyst_functionality_supported
            and campaign_reset.get("fresh_batch_confirmed") is True
            and mechanism_activation["max_active_catalyst_loss_fraction"] < 0.50
            and public_supporting_cells == 0
        ),
        "robust_high_temperature_deactivation_tradeoff_cells": (
            robust_high_temperature_cells
        ),
        "high_temperature_tradeoff_cell_denominator": len(high_temperature_tradeoff),
        "scenario_qualitative_calibration_supported": (
            catalyst_functionality_supported and robust_high_temperature_cells >= 2
        ),
    }
    classifications = []
    if findings["runtime_implementation_defect_detected"]:
        classifications.append("runtime_implementation_defect")
    if findings["fresh_batch_partial_ageing_masks_campaign_accumulation"]:
        classifications.append("experiment_design_masking")
    if findings["catalyst_functionality_supported"] and not findings[
        "deactivation_publicly_identifiable_at_w2_33_gate"
    ]:
        classifications.append("task_mechanism_identifiability_gap")
    if findings["endpoint_compression_supported"]:
        classifications.append("endpoint_compression")
    if not findings["scenario_qualitative_calibration_supported"]:
        classifications.append("scenario_parameter_calibration_gap")
    return {
        "denominators": denominators,
        "completeness_checks": completeness_checks,
        "runtime_checks": runtime_checks,
        "mechanism_activation": mechanism_activation,
        "catalyst_vs_no_catalyst_truth": catalyst_vs_none,
        "stable_vs_deactivating_truth": stable_vs_deactivating_truth,
        "stable_vs_deactivating_public_hplc": stable_vs_deactivating_public,
        "dose_summary": dose_summary,
        "high_temperature_tradeoff": high_temperature_tradeoff,
        "findings": findings,
        "classification": list(dict.fromkeys(classifications)),
        "failures": failures,
    }


def run(output: Path) -> dict[str, Any]:
    if output.exists():
        raise FileExistsError(f"refusing to overwrite existing diagnostic: {output}")
    dirty = _scoped_dirty_paths()
    if dirty:
        raise RuntimeError(
            "catalyst-effect diagnostic requires clean Work II/runtime sources: "
            + ", ".join(dirty)
        )
    started = perf_counter()
    rows: list[dict[str, Any]] = []
    completed = 0
    failures = 0
    for temperature_K in TEMPERATURES_K:
        for duration_s in DURATIONS_S:
            arms = [(0.0, "deactivating_baseline")]
            arms.extend(
                (dose, law_id) for dose in POSITIVE_DOSES_MOL for law_id in LAW_IDS
            )
            for dose, law_id in arms:
                cell_id = (
                    f"T{temperature_K:.0f}-t{duration_s:.0f}-dose{dose:.6f}-{law_id}"
                )
                noise_pair_id = (
                    f"T{temperature_K:.0f}-t{duration_s:.0f}-dose{dose:.6f}"
                )
                namespace = f"work-ii-catalyst-effect-chain:{noise_pair_id}"
                row: dict[str, Any] = {
                    "cell_id": cell_id,
                    "temperature_K": temperature_K,
                    "duration_s": duration_s,
                    "catalyst_amount_mol": dose,
                    "law_id": law_id,
                    "official_replay_attempted": False,
                }
                try:
                    primary = _execute_once(
                        temperature_K=temperature_K,
                        duration_s=duration_s,
                        catalyst_amount_mol=dose,
                        law_id=law_id,
                        namespace=namespace,
                    )
                    replay = _execute_once(
                        temperature_K=temperature_K,
                        duration_s=duration_s,
                        catalyst_amount_mol=dose,
                        law_id=law_id,
                        namespace=namespace,
                    )
                    projection_equal = (
                        primary["execution_sha256"] == replay["execution_sha256"]
                    )
                    row["official_replay_attempted"] = True
                    official_replay = _official_exact_replay(
                        temperature_K=temperature_K,
                        duration_s=duration_s,
                        catalyst_amount_mol=dose,
                        law_id=law_id,
                        namespace=namespace,
                    )
                    row.update(
                        {
                            "status": "completed",
                            "projection_replay_equal": projection_equal,
                            "official_exact_replay": official_replay["verified"],
                            "official_replay": official_replay,
                            "execution": primary,
                            "replay_execution_sha256": replay["execution_sha256"],
                        }
                    )
                    if not projection_equal:
                        raise RuntimeError("deterministic projection replay payload differs")
                    if not official_replay["verified"]:
                        raise RuntimeError("official trajectory exact replay failed")
                except Exception as error:
                    failures += 1
                    row.update(
                        {
                            "status": "failed",
                            "exact_replay": False,
                            "failure": {
                                "type": type(error).__name__,
                                "message": str(error)[:1000],
                            },
                        }
                    )
                rows.append(row)
                completed += 1
                elapsed = perf_counter() - started
                throughput = completed / elapsed if elapsed else 0.0
                progress = {
                    "stage": "paired_deterministic_diagnostic",
                    "completed": completed,
                    "total": TOTAL_PRIMARY_EXECUTIONS,
                    "throughput_primary_units_per_minute": round(throughput * 60.0, 2),
                    "eta_s": round((TOTAL_PRIMARY_EXECUTIONS - completed) / throughput, 1)
                    if throughput
                    else None,
                    "failure_count": failures,
                    "current_cell": cell_id,
                }
                print(json.dumps(progress, sort_keys=True), flush=True)
    campaign_reset = _campaign_reset_check()
    analysis = _analyze(rows, campaign_reset)
    summary = {
        "schema_version": "chemworld-work-ii-catalyst-effect-chain-diagnostic-0.1",
        "date": "2026-08-12",
        "source_commit": git_source_commit(ROOT),
        "scoped_runtime_clean": True,
        "diagnostic_script_sha256": file_sha256(Path(__file__).resolve()),
        "task_id": TASK_ID,
        "world_seed": WORLD_SEED,
        "provider_call_count": 0,
        "participant_session_count": 0,
        "formal_result": False,
        "design": {
            "temperatures_K": list(TEMPERATURES_K),
            "durations_s": list(DURATIONS_S),
            "positive_catalyst_doses_mol": list(POSITIVE_DOSES_MOL),
            "no_catalyst_control_dose_mol": 0.0,
            "reagent_amount_mol": 0.015,
            "solvent_volume_L": 0.025,
            "solvent": 0,
            "catalyst": 1,
            "stirring_speed_rpm": 675.0,
            "primary_execution_count": TOTAL_PRIMARY_EXECUTIONS,
            "deterministic_replay_count": TOTAL_PRIMARY_EXECUTIONS,
        },
        "campaign_reset_check": campaign_reset,
        "analysis": analysis,
        "executions": rows,
        "elapsed_s": perf_counter() - started,
    }
    summary["summary_sha256"] = canonical_json_sha256(summary)
    write_json_atomic(output, summary)
    print(
        json.dumps(
            {
                "stage": "completed",
                "completed": len(rows),
                "total": TOTAL_PRIMARY_EXECUTIONS,
                "failure_count": failures,
                "classification": analysis["classification"],
                "output": str(output),
                "elapsed_s": round(float(summary["elapsed_s"]), 2),
            },
            sort_keys=True,
        ),
        flush=True,
    )
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


if __name__ == "__main__":
    arguments = parse_args()
    run(arguments.output.resolve())
