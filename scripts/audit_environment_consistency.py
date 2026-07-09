"""Run ChemWorld environment self-consistency audits.

The audit is intentionally maintainer-facing: it uses the public Gym interface
for actions and observations, but it also verifies state invariants and replay
metadata so that environment contracts can be checked end to end.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import gymnasium as gym
import numpy as np

import chemworld  # noqa: F401  # registers ChemWorld
from chemworld.agents.base import HistoryRecord
from chemworld.agents.event import ScriptedChemistryAgent
from chemworld.data.logging import TrajectoryLogger, load_jsonl, observation_to_json, to_builtin
from chemworld.eval.verify import verify_records
from chemworld.tasks import get_task, list_tasks
from chemworld.world.scoring import task_score_observation

DEFAULT_OUTPUT_DIR = Path("runs/audit")
SPECTRAL_TASKS = {
    "reaction-to-purification",
    "reaction-to-crystallization",
    "reaction-to-distillation",
}
PROCESS_OPERATION_GROUPS = {
    "crystallization": {"seed_crystals", "cool_crystallize", "filter_crystals"},
    "distillation": {"evaporate", "distill", "collect_fraction"},
    "flow": {"set_flow_rate", "run_flow"},
    "electrochemistry": {"set_potential", "electrolyze"},
}


@dataclass(frozen=True)
class SpectraSummary:
    target_fraction: float = 0.0
    reactant_fraction: float = 0.0
    impurity_fraction: float = 0.0
    target_signal: float = 0.0
    reactant_signal: float = 0.0
    impurity_signal: float = 0.0

    def to_dict(self) -> dict[str, float]:
        return {
            "target_fraction": self.target_fraction,
            "reactant_fraction": self.reactant_fraction,
            "impurity_fraction": self.impurity_fraction,
            "target_signal": self.target_signal,
            "reactant_signal": self.reactant_signal,
            "impurity_signal": self.impurity_signal,
        }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--tasks",
        nargs="+",
        default=["all"],
        help="Task ids to audit, or 'all'.",
    )
    parser.add_argument(
        "--seeds",
        nargs="+",
        type=int,
        default=[0, 1, 2],
        help="Seeds to run for each selected task.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory for audit reports and generated trajectories.",
    )
    parser.add_argument(
        "--max-steps",
        type=int,
        default=24,
        help="Maximum scripted smoke steps per task/seed.",
    )
    parser.add_argument(
        "--agent-probe-rounds",
        type=int,
        default=12,
        help="Rounds for the agent-facing spectra probe; set 0 to disable.",
    )
    return parser.parse_args()


def selected_task_ids(task_args: list[str]) -> list[str]:
    if task_args == ["all"]:
        return [task.task_id for task in list_tasks()]
    return task_args


def scalar(value: Any, default: float = math.nan) -> float:
    if value is None:
        return default
    if hasattr(value, "reshape"):
        value = value.reshape(-1)[0]
    try:
        result = float(value)
    except (TypeError, ValueError):
        return default
    return result if math.isfinite(result) else default


def scalar_observation(observation: dict[str, Any]) -> dict[str, float | None]:
    return observation_to_json(observation)


def spectral_packet(raw_signal: dict[str, Any], instrument_id: str) -> dict[str, Any]:
    if not raw_signal:
        return {}
    kind = str(raw_signal.get("kind", ""))
    if instrument_id == "uvvis" and kind == "uvvis_spectrum":
        return raw_signal
    if instrument_id in {"hplc", "gc"} and kind == f"{instrument_id}_chromatogram":
        return raw_signal
    spectra = raw_signal.get("spectra")
    if isinstance(spectra, dict) and isinstance(spectra.get(instrument_id), dict):
        return spectra[instrument_id]
    return {}


def parse_chromatogram(raw_signal: dict[str, Any], instrument_id: str = "hplc") -> SpectraSummary:
    packet = spectral_packet(raw_signal, instrument_id)
    target = 0.0
    reactant = 0.0
    impurity = 0.0
    for peak in packet.get("peaks", []):
        group = str(peak.get("group", peak.get("assignment", ""))).lower()
        signal = scalar(peak.get("estimated_concentration_mol_L"), default=math.nan)
        if math.isnan(signal) or signal <= 0.0:
            signal = scalar(peak.get("area"), default=0.0)
        if "reactant" in group:
            reactant += signal
        elif "degradation" in group or "impurity" in group or "byproduct" in group:
            impurity += signal
        elif "target" in group or group == "product" or group.endswith("_product"):
            target += signal
    total = max(target + reactant + impurity, 1.0e-12)
    return SpectraSummary(
        target_fraction=target / total,
        reactant_fraction=reactant / total,
        impurity_fraction=impurity / total,
        target_signal=target,
        reactant_signal=reactant,
        impurity_signal=impurity,
    )


def parse_uvvis(raw_signal: dict[str, Any]) -> SpectraSummary:
    packet = spectral_packet(raw_signal, "uvvis")
    wavelength = np.asarray(packet.get("wavelength_nm", []), dtype=float)
    absorbance = np.asarray(packet.get("absorbance", []), dtype=float)
    if wavelength.size == 0 or absorbance.size == 0:
        return SpectraSummary()
    product_mask = (wavelength >= 400.0) & (wavelength <= 470.0)
    impurity_mask = (wavelength >= 500.0) & (wavelength <= 570.0)
    product_signal = float(np.trapezoid(absorbance[product_mask], wavelength[product_mask]))
    impurity_signal = float(np.trapezoid(absorbance[impurity_mask], wavelength[impurity_mask]))
    total = max(product_signal + impurity_signal, 1.0e-12)
    return SpectraSummary(
        target_fraction=product_signal / total,
        impurity_fraction=impurity_signal / total,
        target_signal=product_signal,
        impurity_signal=impurity_signal,
    )


def visible_species_ids(raw_signal: dict[str, Any]) -> list[str]:
    ids: list[str] = []

    def visit(value: Any) -> None:
        if isinstance(value, dict):
            species_id = value.get("species_id")
            if isinstance(species_id, str):
                ids.append(species_id)
            for child in value.values():
                visit(child)
        elif isinstance(value, list):
            for item in value:
                visit(item)

    visit(raw_signal)
    return ids


def score_consistency(
    *,
    env: gym.Env[Any, Any],
    observation: dict[str, Any],
    info: dict[str, Any],
) -> tuple[bool, float]:
    if info.get("leaderboard_score") is None:
        return True, 0.0
    values = {key: scalar(value, default=0.0) for key, value in observation.items()}
    recomputed = task_score_observation(
        contract=env.unwrapped.scoring_contract,
        values=values,
    )
    error = abs(float(info["leaderboard_score"]) - recomputed)
    return error <= 1.0e-6, error


def task_policy_warnings(task_info: dict[str, Any]) -> list[str]:
    task_id = str(task_info.get("task_id"))
    allowed = set(task_info.get("allowed_operations", ()))
    warnings: list[str] = []
    if task_id == "reaction-to-purification":
        unexpected = sorted(
            allowed.intersection(
                PROCESS_OPERATION_GROUPS["crystallization"]
                | PROCESS_OPERATION_GROUPS["distillation"]
                | PROCESS_OPERATION_GROUPS["flow"]
                | PROCESS_OPERATION_GROUPS["electrochemistry"]
            )
        )
        if unexpected:
            warnings.append(
                "task_policy_warning:reaction_to_purification_allows_unrelated_process_ops="
                + ",".join(unexpected)
            )
    if task_id == "reaction-to-crystallization":
        unexpected = sorted(
            allowed.intersection(
                PROCESS_OPERATION_GROUPS["distillation"]
                | PROCESS_OPERATION_GROUPS["flow"]
                | PROCESS_OPERATION_GROUPS["electrochemistry"]
            )
        )
        if unexpected:
            warnings.append(
                "task_policy_warning:crystallization_allows_unrelated_process_ops="
                + ",".join(unexpected)
            )
    if task_id == "reaction-to-distillation":
        unexpected = sorted(
            allowed.intersection(
                PROCESS_OPERATION_GROUPS["crystallization"]
                | PROCESS_OPERATION_GROUPS["flow"]
                | PROCESS_OPERATION_GROUPS["electrochemistry"]
            )
        )
        if unexpected:
            warnings.append(
                "task_policy_warning:distillation_allows_unrelated_process_ops="
                + ",".join(unexpected)
            )
    return warnings


def spectra_metric_consistency(
    *,
    task_id: str,
    observation: dict[str, Any],
    info: dict[str, Any],
) -> tuple[str, list[str], dict[str, Any]]:
    raw_signal = info.get("raw_signal") or {}
    if not raw_signal:
        return "not_applicable", [], {}
    warnings: list[str] = []
    details: dict[str, Any] = {}
    species_ids = visible_species_ids(raw_signal)
    leaked = [
        species_id
        for species_id in species_ids
        if not species_id.endswith("_public")
    ]
    if leaked:
        warnings.append("hidden_species_label_leak")
        details["leaked_species_ids"] = leaked

    hplc = parse_chromatogram(raw_signal, "hplc")
    gc = parse_chromatogram(raw_signal, "gc")
    uvvis = parse_uvvis(raw_signal)
    details["hplc"] = hplc.to_dict()
    details["gc"] = gc.to_dict()
    details["uvvis"] = uvvis.to_dict()

    purity = scalar(observation.get("purity"), default=math.nan)
    distillate_purity = scalar(observation.get("distillate_purity"), default=math.nan)
    crystal_purity = scalar(observation.get("crystal_purity"), default=math.nan)
    if task_id in SPECTRAL_TASKS:
        if not math.isnan(purity) and purity >= 0.70 and hplc.reactant_fraction >= 0.50:
            warnings.append("semantic_alignment_warning:high_purity_with_dominant_reactant_peak")
        if (
            not math.isnan(distillate_purity)
            and distillate_purity >= 0.50
            and gc.target_fraction < 0.20
        ):
            warnings.append("semantic_alignment_warning:distillate_purity_low_gc_target_fraction")
        if (
            not math.isnan(crystal_purity)
            and crystal_purity >= 0.70
            and hplc.target_fraction < 0.10
        ):
            warnings.append("semantic_alignment_warning:crystal_purity_low_hplc_target_fraction")
    if leaked:
        return "fail", warnings, details
    if warnings:
        return "warning", warnings, details
    return "pass", warnings, details


def smoke_action_sequence(task_id: str) -> list[dict[str, Any]] | None:
    """Return a task-aware legal smoke sequence when the generic agent is unsuitable."""
    if task_id != "partition-discovery":
        return None
    return [
        {"operation": "add_solvent", "volume_L": 0.02, "solvent": 1},
        {"operation": "add_reagent", "amount_mol": 0.008},
        {"operation": "add_phase", "phase": "aqueous", "volume_L": 0.015},
        {"operation": "add_extractant", "extractant": "organic", "volume_L": 0.02},
        {"operation": "mix", "duration_s": 240.0, "stirring_speed_rpm": 700.0},
        {"operation": "settle", "duration_s": 420.0},
        {"operation": "measure", "instrument": "hplc"},
        {"operation": "separate_phase", "target_phase": "organic"},
        {"operation": "measure", "instrument": "uvvis"},
        {"operation": "terminate"},
        {"operation": "measure", "instrument": "final_assay"},
    ]


def run_smoke_audit(
    *,
    task_id: str,
    seed: int,
    output_dir: Path,
    max_steps: int,
) -> dict[str, Any]:
    task = get_task(task_id)
    env = gym.make("ChemWorld", task_id=task_id, seed=seed)
    observation, task_info = env.reset(seed=seed)
    agent = ScriptedChemistryAgent()
    agent.reset(task_info, seed)
    trajectory_path = output_dir / "trajectories" / f"{task_id}_seed{seed}.jsonl"
    history: list[HistoryRecord] = []
    invalid_count = 0
    constitution_failure_count = 0
    spectra_statuses: list[str] = []
    warnings: list[str] = task_policy_warnings(task_info)
    last_info: dict[str, Any] = {}
    final_score_error = 0.0
    state_check_failures = 0
    with TrajectoryLogger(trajectory_path) as logger:
        planned_actions = smoke_action_sequence(task_id)
        for step in range(min(task.budget, max_steps)):
            if planned_actions is not None:
                if step >= len(planned_actions):
                    break
                action = planned_actions[step]
            else:
                action = agent.act(history)
            observation, reward, terminated, truncated, info = env.step(action)
            flags = info.get("constraint_flags", {})
            invalid_count += int(bool(flags.get("precondition_failed")))
            constitution_failure_count += int(bool(flags.get("constitution_failed")))
            state_report = env.unwrapped.constitution.check_state(env.unwrapped._state)
            state_check_failures += int(not state_report.passed)
            if not state_report.passed:
                warnings.append("state_constitution_failed")
            score_ok, score_error = score_consistency(
                env=env,
                observation=observation,
                info=info,
            )
            if not score_ok:
                warnings.append("leaderboard_score_recompute_mismatch")
            final_score_error = max(final_score_error, score_error)
            spectra_status, spectra_warnings, _spectra_details = spectra_metric_consistency(
                task_id=task_id,
                observation=observation,
                info=info,
            )
            if spectra_status != "not_applicable":
                spectra_statuses.append(spectra_status)
            warnings.extend(spectra_warnings)
            logger.log(
                task_info=task_info,
                step=step + 1,
                action=action,
                observation=observation,
                reward=float(reward),
                terminated=bool(terminated),
                truncated=bool(truncated),
                info=info,
                agent_metadata=agent.manifest(),
            )
            obs_json = scalar_observation(observation)
            history.append(
                HistoryRecord(
                    step=step,
                    action=action,
                    observation=obs_json,
                    reward=float(reward),
                    info=info,
                )
            )
            agent.update(action, obs_json, float(reward), info)
            last_info = info
            if terminated or truncated:
                break
    records = load_jsonl(trajectory_path)
    verification = verify_records(records)
    env.close()
    if "fail" in spectra_statuses:
        spectra_consistency = "fail"
    elif "warning" in spectra_statuses:
        spectra_consistency = "warning"
    elif "pass" in spectra_statuses:
        spectra_consistency = "pass"
    else:
        spectra_consistency = "not_applicable"
    unique_warnings = sorted(set(warnings))
    return {
        "task_id": task_id,
        "seed": seed,
        "world_law_id": task_info.get("world_law_id"),
        "scenario_id": task_info.get("scenario_id"),
        "initial_state_id": task_info.get("initial_state_id"),
        "task_contract_hash": task_info.get("task_contract_hash"),
        "mechanism_id": task_info.get("mechanism_id"),
        "mechanism_hash": task_info.get("mechanism_hash"),
        "score_contract_hash": task_info.get("scoring_contract_hash"),
        "profile_hash": task_info.get("runtime_profile_hash"),
        "observation_contract_hash": task_info.get("observation_contract_hash"),
        "maturity": task_info.get("physics_maturity"),
        "proxy_allowed": task_info.get("proxy_allowed"),
        "episode_mode": task_info.get("episode_mode"),
        "budget": task_info.get("budget"),
        "steps_run": len(records),
        "invalid_count": invalid_count,
        "constitution_failure_count": constitution_failure_count,
        "state_check_failures": state_check_failures,
        "verify_status": "pass" if verification.verified else "fail",
        "verify_max_abs_error": verification.max_abs_error,
        "verify_mismatch_count": len(verification.mismatches),
        "spectra_metric_consistency": spectra_consistency,
        "score_recompute_max_error": final_score_error,
        "final_leaderboard_score": last_info.get("leaderboard_score"),
        "trajectory_path": str(trajectory_path),
        "warnings": unique_warnings,
        "verify_mismatches": verification.mismatches[:5],
    }


def downstream_actions(strength: int) -> list[dict[str, Any]]:
    volume = (0.006, 0.010, 0.014)[max(0, min(strength, 2))]
    duration = (300.0, 600.0, 900.0)[max(0, min(strength, 2))]
    return [
        {"operation": "add_phase", "phase": "aqueous", "volume_L": 0.012},
        {"operation": "add_extractant", "extractant": "organic", "volume_L": 0.018 + volume},
        {"operation": "mix", "duration_s": 240.0 + 60.0 * strength, "stirring_speed_rpm": 850.0},
        {"operation": "settle", "duration_s": 420.0 + 60.0 * strength},
        {"operation": "separate_phase", "target_phase": "organic"},
        {"operation": "wash", "wash_volume_L": volume},
        {"operation": "dry"},
        {"operation": "concentrate", "duration_s": duration},
    ]


def run_agent_probe_round(
    seed: int,
    round_index: int,
    params: dict[str, float | int],
) -> dict[str, Any]:
    env = gym.make("ChemWorld", task_id="reaction-to-purification", seed=seed)
    observation, _info = env.reset(seed=seed)
    invalid = 0
    spectral_features: dict[str, Any] = {}
    final_info: dict[str, Any] = {}
    try:
        actions: list[dict[str, Any]] = [
            {"operation": "add_solvent", "volume_L": 0.028, "solvent": int(params["solvent"])},
            {"operation": "add_reagent", "amount_mol": float(params["reagent_mol"])},
            {
                "operation": "add_catalyst",
                "catalyst": int(params["catalyst"]),
                "catalyst_amount_mol": float(params["catalyst_mol"]),
            },
            {
                "operation": "heat",
                "target_temperature_K": float(params["temperature_K"]),
                "duration_s": float(params["heat_s"]),
                "stirring_speed_rpm": 720.0,
            },
            {"operation": "measure", "instrument": "hplc"},
        ]
        hplc = SpectraSummary()
        for action in actions:
            observation, _reward, terminated, truncated, info = env.step(action)
            invalid += int(bool(info.get("constraint_flags", {}).get("precondition_failed")))
            final_info = info
            if action.get("instrument") == "hplc":
                hplc = parse_chromatogram(info.get("raw_signal") or {}, "hplc")
            if terminated or truncated:
                break
        spectral_features["mid_hplc"] = hplc.to_dict()
        if hplc.reactant_fraction > 0.62 and hplc.impurity_fraction < 0.30:
            observation, _reward, _terminated, _truncated, info = env.step(
                {"operation": "wait", "duration_s": 900.0, "stirring_speed_rpm": 720.0}
            )
            invalid += int(bool(info.get("constraint_flags", {}).get("precondition_failed")))
            final_info = info
        downstream_strength = int(params["downstream_strength"])
        if hplc.impurity_fraction > 0.22:
            downstream_strength = min(2, downstream_strength + 1)
        if hplc.target_fraction < 0.08:
            downstream_strength = max(0, downstream_strength - 1)
        for action in [
            {"operation": "measure", "instrument": "uvvis"},
            {"operation": "quench"},
            *downstream_actions(downstream_strength),
            {"operation": "measure", "instrument": "hplc"},
            {"operation": "terminate"},
            {"operation": "measure", "instrument": "final_assay"},
        ]:
            observation, _reward, terminated, truncated, info = env.step(action)
            invalid += int(bool(info.get("constraint_flags", {}).get("precondition_failed")))
            final_info = info
            if terminated or truncated:
                break
        final_hplc = parse_chromatogram(final_info.get("raw_signal") or {}, "hplc")
        spectral_features["final_hplc"] = final_hplc.to_dict()
        return {
            "seed": seed,
            "round": round_index,
            "score": scalar(observation.get("score"), default=0.0),
            "leaderboard_score": float(
                final_info.get("leaderboard_score") or scalar(observation.get("score"), default=0.0)
            ),
            "purity": scalar(observation.get("purity")),
            "recovery": scalar(observation.get("recovery")),
            "invalid_count": invalid,
            "params": dict(params),
            "effective_downstream_strength": downstream_strength,
            "spectral_features": spectral_features,
        }
    finally:
        env.close()


def next_probe_params(history: list[dict[str, Any]], round_index: int) -> dict[str, float | int]:
    exploratory = [
        {
            "solvent": 2,
            "reagent_mol": 0.010,
            "catalyst": 1,
            "catalyst_mol": 0.00025,
            "temperature_K": 385.0,
            "heat_s": 1500.0,
            "downstream_strength": 1,
        },
        {
            "solvent": 1,
            "reagent_mol": 0.012,
            "catalyst": 2,
            "catalyst_mol": 0.00040,
            "temperature_K": 360.0,
            "heat_s": 1800.0,
            "downstream_strength": 1,
        },
        {
            "solvent": 2,
            "reagent_mol": 0.009,
            "catalyst": 1,
            "catalyst_mol": 0.00025,
            "temperature_K": 405.0,
            "heat_s": 2400.0,
            "downstream_strength": 2,
        },
    ]
    if round_index < len(exploratory):
        return exploratory[round_index]
    best = max(history, key=lambda row: row["leaderboard_score"])
    params = dict(best["params"])
    features = best["spectral_features"]["mid_hplc"]
    if features["reactant_fraction"] > 0.55:
        params["temperature_K"] = min(405.0, float(params["temperature_K"]) + 8.0)
        params["heat_s"] = min(2700.0, float(params["heat_s"]) + 300.0)
    if features["impurity_fraction"] > 0.28:
        params["temperature_K"] = max(335.0, float(params["temperature_K"]) - 10.0)
        params["heat_s"] = max(600.0, float(params["heat_s"]) - 300.0)
    if float(best["recovery"]) < 0.16:
        params["downstream_strength"] = max(0, int(params["downstream_strength"]) - 1)
    if float(best["purity"]) < 0.70:
        params["downstream_strength"] = min(2, int(params["downstream_strength"]) + 1)
    if round_index % 4 == 0:
        params["solvent"] = 1 if int(params["solvent"]) == 2 else 2
    return params


def run_agent_probe(seeds: list[int], rounds: int) -> dict[str, Any]:
    if rounds <= 0:
        return {"enabled": False}
    details: list[dict[str, Any]] = []
    by_seed: dict[str, Any] = {}
    for seed in seeds:
        history: list[dict[str, Any]] = []
        for round_index in range(rounds):
            params = next_probe_params(history, round_index)
            result = run_agent_probe_round(seed, round_index, params)
            history.append(result)
            details.append(result)
        scores = [float(row["leaderboard_score"]) for row in history]
        best_idx = int(np.argmax(scores))
        best_so_far = np.maximum.accumulate(scores)
        by_seed[str(seed)] = {
            "first_score": scores[0],
            "best_score": scores[best_idx],
            "best_round": best_idx,
            "best_so_far_auc": float(np.mean(best_so_far)),
            "invalid_count": int(sum(row["invalid_count"] for row in history)),
        }
    return {
        "enabled": True,
        "task_id": "reaction-to-purification",
        "rounds": rounds,
        "seeds": seeds,
        "by_seed": by_seed,
        "details": details,
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "task_id",
        "seed",
        "world_law_id",
        "scenario_id",
        "task_contract_hash",
        "mechanism_hash",
        "score_contract_hash",
        "profile_hash",
        "observation_contract_hash",
        "maturity",
        "proxy_allowed",
        "episode_mode",
        "steps_run",
        "invalid_count",
        "constitution_failure_count",
        "state_check_failures",
        "verify_status",
        "verify_mismatch_count",
        "spectra_metric_consistency",
        "score_recompute_max_error",
        "final_leaderboard_score",
        "warnings",
        "trajectory_path",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            payload = {key: row.get(key) for key in fieldnames}
            payload["warnings"] = ";".join(row.get("warnings", []))
            writer.writerow(payload)


def main() -> None:
    args = parse_args()
    output_dir: Path = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    task_ids = selected_task_ids(args.tasks)
    rows: list[dict[str, Any]] = []
    for task_id in task_ids:
        for seed in args.seeds:
            rows.append(
                run_smoke_audit(
                    task_id=task_id,
                    seed=seed,
                    output_dir=output_dir,
                    max_steps=args.max_steps,
                )
            )
    agent_probe = run_agent_probe(args.seeds, int(args.agent_probe_rounds))
    required_hash_keys = (
        "task_contract_hash",
        "mechanism_hash",
        "score_contract_hash",
        "profile_hash",
        "observation_contract_hash",
    )
    summary = {
        "schema_version": "chemworld-environment-consistency-audit-0.1",
        "generated_at": datetime.now(UTC).isoformat(),
        "task_count": len(task_ids),
        "task_ids": task_ids,
        "seeds": args.seeds,
        "rows": rows,
        "agent_probe": agent_probe,
        "aggregate": {
            "row_count": len(rows),
            "covered_task_count": len({row["task_id"] for row in rows}),
            "hash_coverage_complete": all(
                all(row.get(key) for key in required_hash_keys) for row in rows
            ),
            "verify_failures": sum(row["verify_status"] != "pass" for row in rows),
            "spectra_failures": sum(row["spectra_metric_consistency"] == "fail" for row in rows),
            "spectra_warnings": sum(row["spectra_metric_consistency"] == "warning" for row in rows),
            "invalid_steps": sum(int(row["invalid_count"]) for row in rows),
            "constitution_failures": sum(int(row["constitution_failure_count"]) for row in rows),
        },
    }
    json_path = output_dir / "environment_consistency_report.json"
    csv_path = output_dir / "environment_consistency_report.csv"
    json_path.write_text(
        json.dumps(to_builtin(summary), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    write_csv(csv_path, rows)
    print(json.dumps(to_builtin(summary["aggregate"]), indent=2, ensure_ascii=False))
    print(f"Wrote {json_path}")
    print(f"Wrote {csv_path}")


if __name__ == "__main__":
    main()
