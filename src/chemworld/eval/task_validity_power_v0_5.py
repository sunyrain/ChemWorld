"""Validate v0.5 core-task surfaces, controls, SESOI, and prospective power."""

from __future__ import annotations

import hashlib
import json
import math
import subprocess
from collections.abc import Mapping, Sequence
from pathlib import Path
from statistics import NormalDist
from typing import Any

import gymnasium as gym
import numpy as np

import chemworld  # noqa: F401
from chemworld.agents.task_recipes import sample_task_recipe
from chemworld.physchem.mechanism_library import configuration_root
from chemworld.tasks import get_task
from chemworld.world.recipes import compile_recipe

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_PROTOCOL_PATH = configuration_root() / "foundation" / "task_validity_power_v0.5.json"
PROTOCOL_VERSION = "chemworld-task-validity-power-protocol-0.1"


class TaskValidityPowerError(RuntimeError):
    """Raised when a validity protocol or runtime sample is invalid."""


def load_task_validity_power_protocol(path: Path | None = None) -> dict[str, Any]:
    resolved = DEFAULT_PROTOCOL_PATH if path is None else path
    payload = json.loads(resolved.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or payload.get("schema_version") != PROTOCOL_VERSION:
        raise TaskValidityPowerError("unsupported task validity power protocol")
    return payload


def run_task_validity_power(
    protocol: Mapping[str, Any], *, workspace: Path = ROOT
) -> dict[str, Any]:
    dependencies = {
        name: _read_object(_resolve_path(workspace, raw_path))
        for name, raw_path in protocol["dependencies"].items()
    }
    legacy_risk_path = protocol["risk_cost_calibration"]["legacy_protocol_path"]
    legacy_risk = _read_object(_resolve_path(workspace, legacy_risk_path))
    task_reports: dict[str, dict[str, Any]] = {}
    global_recommended = int(protocol["power"]["candidate_paired_seed_count"])
    for task_index, (task_id, primary_metric) in enumerate(protocol["core_tasks"].items()):
        task = get_task(task_id)
        rows = _sample_task_surface(
            task_id,
            primary_metric,
            samples_per_seed=int(protocol["surface"]["samples_per_seed"]),
            rng_namespace=int(protocol["surface"]["rng_namespace"]),
            task_index=task_index,
        )
        primary = np.asarray([row["primary"] for row in rows], dtype=float)
        score = np.asarray([row["score"] for row in rows], dtype=float)
        risk = np.asarray([row["risk"] for row in rows], dtype=float)
        process_cost = np.asarray([row["process_cost"] for row in rows], dtype=float)
        spread = float(np.ptp(primary))
        sesoi = round(
            max(
                float(protocol["sesoi"]["absolute_floor"]),
                float(protocol["sesoi"]["response_surface_fraction"]) * spread,
            ),
            int(protocol["sesoi"]["round_decimal_places"]),
        )
        proposed_risk_limit = float(
            np.quantile(risk, float(protocol["risk_cost_calibration"]["risk_quantile"]))
        )
        proposed_cost_limit = float(
            np.quantile(
                process_cost,
                float(protocol["risk_cost_calibration"]["process_cost_quantile"]),
            )
        )
        risk_activation = float(np.mean(risk > proposed_risk_limit))
        cost_activation = float(np.mean(process_cost > proposed_cost_limit))
        legacy_limits = legacy_risk["tasks"][task_id]
        legacy_risk_activation = float(np.mean(risk > float(legacy_limits["risk_limit"])))
        legacy_cost_activation = float(
            np.mean(process_cost > float(legacy_limits["process_cost_limit"]))
        )
        near_optimal_fraction = float(np.mean(primary >= float(np.max(primary)) - sesoi))
        probes = _behavior_probe_report(
            rows,
            proposed_risk_limit=proposed_risk_limit,
            proposed_cost_limit=proposed_cost_limit,
            selected_count=int(protocol["behavior_probes"]["selected_recipes_per_seed"]),
        )
        power = _power_report(
            rows,
            sesoi=sesoi,
            selected_count=int(protocol["behavior_probes"]["selected_recipes_per_seed"]),
            protocol=protocol,
        )
        global_recommended = max(global_recommended, int(power["recommended_paired_seed_count"]))
        risk_bounds = protocol["risk_cost_calibration"]["risk_activation_rate_bounds"]
        cost_bounds = protocol["risk_cost_calibration"][
            "process_cost_activation_rate_bounds"
        ]
        near_bounds = protocol["surface"]["near_optimal_fraction_bounds"]
        behavior_primary_spread = max(
            item["mean_primary"] for item in probes.values()
        ) - min(item["mean_primary"] for item in probes.values())
        checks = {
            "complete_surface": len(rows)
            == len(task.seeds) * int(protocol["surface"]["samples_per_seed"]),
            "no_invalid_or_nonfinite_runs": all(
                row["invalid_action_count"] == 0
                and all(
                    math.isfinite(float(row[field]))
                    for field in ("primary", "score", "risk", "process_cost")
                )
                for row in rows
            ),
            "primary_dynamic_range": spread
            >= float(protocol["surface"]["minimum_primary_spread"]),
            "primary_direction_aligns_with_score": _spearman(primary, score) > 0.2,
            "near_optimal_region_is_nontrivial": float(near_bounds[0])
            <= near_optimal_fraction
            <= float(near_bounds[1]),
            "risk_activation_is_identifiable": float(risk_bounds[0])
            <= risk_activation
            <= float(risk_bounds[1]),
            "cost_activation_is_identifiable": float(cost_bounds[0])
            <= cost_activation
            <= float(cost_bounds[1]),
            "behavior_probes_are_distinguishable": behavior_primary_spread >= sesoi
            and len(
                {
                    (
                        round(float(item["risk_exceedance_rate"]), 6),
                        round(float(item["cost_exceedance_rate"]), 6),
                    )
                    for item in probes.values()
                }
            )
            >= 2,
            "prospective_sample_size_is_frozen": int(
                power["recommended_paired_seed_count"]
            )
            >= int(protocol["power"]["candidate_paired_seed_count"]),
        }
        task_reports[task_id] = {
            "role": "formal_core_candidate",
            "task_contract_hash": task.contract_hash,
            "primary_metric": primary_metric,
            "sample_count": len(rows),
            "seed_count": len(task.seeds),
            "surface": {
                **_distribution(primary),
                "sesoi": sesoi,
                "near_optimal_fraction": near_optimal_fraction,
                "primary_score_spearman": _spearman(primary, score),
                "primary_risk_spearman": _spearman(primary, risk),
                "primary_process_cost_spearman": _spearman(primary, process_cost),
            },
            "risk_cost": {
                "proposed_risk_limit": proposed_risk_limit,
                "proposed_process_cost_limit": proposed_cost_limit,
                "risk_activation_rate": risk_activation,
                "process_cost_activation_rate": cost_activation,
                "legacy_risk_limit": legacy_limits["risk_limit"],
                "legacy_process_cost_limit": legacy_limits["process_cost_limit"],
                "legacy_risk_activation_rate": legacy_risk_activation,
                "legacy_process_cost_activation_rate": legacy_cost_activation,
                "risk_semantics": protocol["risk_cost_calibration"]["risk_semantics"],
            },
            "behavior_probes": probes,
            "power": power,
            "checks": checks,
            "validity_ready": all(checks.values()),
            "surface_rows_sha256": _canonical_sha256({"rows": rows}),
        }

    rounding = int(protocol["power"]["round_recommendation_to_multiple"])
    global_recommended = int(math.ceil(global_recommended / rounding) * rounding)
    controls = {
        "protocol_is_nonclaiming": protocol.get("benchmark_claim_allowed") is False
        and protocol.get("formal_results_present") is False,
        "dependencies_are_ready": all(
            report["controls_ready"] is True for report in dependencies.values()
        ),
        "core_task_scope_is_exact": set(task_reports) == set(protocol["core_tasks"]),
        "all_core_tasks_are_validity_ready": all(
            report["validity_ready"] for report in task_reports.values()
        ),
        "legacy_threshold_failures_are_not_reused": any(
            report["risk_cost"]["legacy_risk_activation_rate"] == 0.0
            or report["risk_cost"]["legacy_process_cost_activation_rate"] in {0.0, 1.0}
            for report in task_reports.values()
        )
        and protocol["risk_cost_calibration"]["supersedes_protocol_id"]
        == legacy_risk["protocol_id"],
        "sample_size_adjusted_before_bench": global_recommended
        > int(protocol["power"]["candidate_paired_seed_count"]),
    }
    controls_ready = all(controls.values())
    source_commit, dirty = _git_provenance(workspace)
    return {
        "schema_version": "chemworld-task-validity-power-report-0.1",
        "protocol_id": protocol["protocol_id"],
        "status": "core4_validity_ready_protocol_0_4_freeze_pending"
        if controls_ready
        else "task_validity_or_power_failed",
        "controls_ready": controls_ready,
        "formal_results_present": False,
        "benchmark_claim_allowed": False,
        "source_commit": source_commit,
        "source_tree_dirty": dirty,
        "protocol_sha256": _canonical_sha256(protocol),
        "controls": controls,
        "core_tasks": task_reports,
        "exploratory_tasks": list(protocol["exploratory_tasks"]),
        "formal_design_recommendation": {
            "candidate_paired_seed_count": protocol["power"]["candidate_paired_seed_count"],
            "recommended_paired_seed_count": global_recommended,
            "twenty_paired_seeds_adequate": global_recommended <= 20,
            "reason": (
                "Simultaneous five-percent safety/cost noninferiority cannot be resolved "
                "with twenty pairs even under zero adverse discordance."
            ),
            "risk_cost_protocol_superseded": legacy_risk["protocol_id"],
        },
        "limitations": [
            "Behavior probes diagnose endpoint distinguishability; they are not method rankings.",
            "Calibration uses public development seeds and must not be repeated on Bench.",
            "Operational risk is a benchmark budget, not a real-world safety threshold.",
        ],
        "remaining_release_gates": [
            "freeze the proposed task-specific thresholds in protocol 0.4",
            "allocate the recommended untouched private paired cohort",
            "run formal methods only after reference and method manifests are frozen",
        ],
    }


def _sample_task_surface(
    task_id: str,
    primary_metric: str,
    *,
    samples_per_seed: int,
    rng_namespace: int,
    task_index: int,
) -> list[dict[str, Any]]:
    task = get_task(task_id)
    rows: list[dict[str, Any]] = []
    for seed in task.seeds:
        rng = np.random.default_rng(rng_namespace + task_index * 10_007 + seed)
        for sample_index in range(samples_per_seed):
            env = gym.make("ChemWorld", task_id=task_id, seed=seed)
            invalid = 0
            try:
                _, task_info = env.reset(seed=seed)
                recipe = sample_task_recipe(task_info, rng)
                final_observation: Mapping[str, Any] = {}
                final_info: Mapping[str, Any] = {}
                for action in compile_recipe(recipe, task_info=task_info):
                    observation, _, _, _, info = env.step(action)
                    final_observation = observation
                    final_info = info
                    invalid += int(bool(info["constraint_flags"].get("precondition_failed")))
                terminal = final_info.get("last_terminal_summary")
                if not isinstance(terminal, Mapping):
                    raise TaskValidityPowerError("final assay terminal summary is missing")
                primary_value = final_observation.get(primary_metric)
                if primary_value is None:
                    raise TaskValidityPowerError("primary metric is missing")
                vector = recipe.get("metadata", {}).get("search_vector")
                if not isinstance(vector, list):
                    raise TaskValidityPowerError("recipe vector is missing")
                measurement_cost = float(final_info.get("measurement_cost", math.nan))
                total_cost = float(terminal["cost"])
                rows.append(
                    {
                        "task_id": task_id,
                        "seed": int(seed),
                        "sample_index": sample_index,
                        "vector": [float(value) for value in vector],
                        "primary": float(np.asarray(primary_value).reshape(-1)[0]),
                        "score": float(terminal["leaderboard_score"]),
                        "risk": float(terminal["safety_risk"]),
                        "process_cost": total_cost - measurement_cost,
                        "measurement_cost": measurement_cost,
                        "total_cost": total_cost,
                        "invalid_action_count": invalid,
                    }
                )
            finally:
                env.close()
    return rows


def _behavior_probe_report(
    rows: Sequence[dict[str, Any]],
    *,
    proposed_risk_limit: float,
    proposed_cost_limit: float,
    selected_count: int,
) -> dict[str, dict[str, Any]]:
    selections: dict[str, list[dict[str, Any]]] = {
        "random_recipe": [],
        "local_primary_climb": [],
        "information_space_filling": [],
        "risk_blind_primary_oracle_probe": [],
    }
    for seed in sorted({int(row["seed"]) for row in rows}):
        seed_rows = [row for row in rows if int(row["seed"]) == seed]
        selections["random_recipe"].extend(seed_rows[:selected_count])
        initial = seed_rows[:3]
        best = max(initial, key=lambda row: float(row["primary"]))
        remaining = seed_rows[3:]
        local = sorted(
            remaining,
            key=lambda row: _distance(row["vector"], best["vector"]),
        )[: max(0, selected_count - len(initial))]
        selections["local_primary_climb"].extend([*initial, *local])
        selections["information_space_filling"].extend(
            _farthest_point_selection(seed_rows, selected_count)
        )
        selections["risk_blind_primary_oracle_probe"].extend(
            sorted(seed_rows, key=lambda row: float(row["primary"]), reverse=True)[
                :selected_count
            ]
        )
    reports: dict[str, dict[str, Any]] = {}
    for probe_id, selected in selections.items():
        primary = np.asarray([row["primary"] for row in selected], dtype=float)
        risks = np.asarray([row["risk"] for row in selected], dtype=float)
        costs = np.asarray([row["process_cost"] for row in selected], dtype=float)
        reports[probe_id] = {
            "selected_count": len(selected),
            "mean_primary": float(np.mean(primary)),
            "mean_risk": float(np.mean(risks)),
            "mean_process_cost": float(np.mean(costs)),
            "risk_exceedance_rate": float(np.mean(risks > proposed_risk_limit)),
            "cost_exceedance_rate": float(np.mean(costs > proposed_cost_limit)),
            "formal_method_evidence": False,
        }
    return reports


def _power_report(
    rows: Sequence[dict[str, Any]],
    *,
    sesoi: float,
    selected_count: int,
    protocol: Mapping[str, Any],
) -> dict[str, Any]:
    random_by_seed: list[float] = []
    local_by_seed: list[float] = []
    relative_cost_effects: list[float] = []
    for seed in sorted({int(row["seed"]) for row in rows}):
        seed_rows = [row for row in rows if int(row["seed"]) == seed]
        random_rows = seed_rows[:selected_count]
        initial = seed_rows[: min(3, selected_count)]
        best = max(initial, key=lambda row: float(row["primary"]))
        local_rows = [
            *initial,
            *sorted(
                seed_rows[3:],
                key=lambda row: _distance(row["vector"], best["vector"]),
            )[: max(0, selected_count - len(initial))],
        ]
        random_by_seed.append(
            float(np.mean([float(row["primary"]) for row in random_rows]))
        )
        local_by_seed.append(float(np.mean([float(row["primary"]) for row in local_rows])))
        random_cost = float(np.mean([float(row["process_cost"]) for row in random_rows]))
        local_cost = float(np.mean([float(row["process_cost"]) for row in local_rows]))
        relative_cost_effects.append((local_cost - random_cost) / random_cost)
    paired = np.asarray(local_by_seed) - np.asarray(random_by_seed)
    paired_sd = float(np.std(paired, ddof=1))
    power = protocol["power"]
    z_alpha = NormalDist().inv_cdf(1.0 - float(power["objective_two_sided_alpha"]) / 2.0)
    z_power = NormalDist().inv_cdf(float(power["target_power"]))
    objective_n = max(2, math.ceil(((z_alpha + z_power) * paired_sd / sesoi) ** 2))
    simultaneous_alpha = float(power["familywise_alpha"]) / int(
        power["simultaneous_comparison_count"]
    )
    safety_margin = float(power["safety_noninferiority_margin"])
    safety_zero_event_n = math.ceil(
        math.log(simultaneous_alpha) / math.log(1.0 - safety_margin)
    )
    costs = np.asarray([row["process_cost"] for row in rows], dtype=float)
    cost_cv = float(np.std(costs, ddof=1) / np.mean(costs))
    paired_cost_sd = float(np.std(np.asarray(relative_cost_effects), ddof=1))
    cost_margin = float(power["cost_relative_noninferiority_margin"])
    z_simultaneous = NormalDist().inv_cdf(1.0 - simultaneous_alpha)
    cost_n = max(
        2,
        math.ceil(((z_simultaneous + z_power) * paired_cost_sd / cost_margin) ** 2),
    )
    recommended = max(
        int(power["candidate_paired_seed_count"]),
        objective_n,
        safety_zero_event_n,
        cost_n,
    )
    return {
        "pilot_seed_count": len(paired),
        "paired_primary_sd_proxy": paired_sd,
        "objective_required_seed_count": objective_n,
        "safety_zero_adverse_required_seed_count": safety_zero_event_n,
        "unpaired_process_cost_cv_diagnostic": cost_cv,
        "paired_relative_cost_sd_proxy": paired_cost_sd,
        "cost_required_seed_count": cost_n,
        "simultaneous_one_sided_alpha": simultaneous_alpha,
        "candidate_paired_seed_count": power["candidate_paired_seed_count"],
        "recommended_paired_seed_count": recommended,
        "twenty_seed_objective_powered": objective_n <= 20,
        "twenty_seed_joint_noninferiority_powered": safety_zero_event_n <= 20
        and cost_n <= 20,
        "estimation_boundary": "prospective_dev_diagnostic_not_method_evidence",
    }


def _farthest_point_selection(
    rows: Sequence[dict[str, Any]], count: int
) -> list[dict[str, Any]]:
    selected = [rows[0]]
    remaining = list(rows[1:])
    while remaining and len(selected) < count:
        candidate = max(
            remaining,
            key=lambda row: min(
                _distance(row["vector"], chosen["vector"]) for chosen in selected
            ),
        )
        selected.append(candidate)
        remaining.remove(candidate)
    return selected


def _distance(left: Any, right: Any) -> float:
    return float(np.linalg.norm(np.asarray(left, dtype=float) - np.asarray(right, dtype=float)))


def _distribution(values: np.ndarray) -> dict[str, float | int]:
    return {
        "count": int(values.size),
        "minimum": float(np.min(values)),
        "q25": float(np.quantile(values, 0.25)),
        "median": float(np.median(values)),
        "q75": float(np.quantile(values, 0.75)),
        "maximum": float(np.max(values)),
        "mean": float(np.mean(values)),
        "std": float(np.std(values, ddof=1)),
        "spread": float(np.ptp(values)),
    }


def _spearman(left: np.ndarray, right: np.ndarray) -> float:
    left_rank = _ranks(left)
    right_rank = _ranks(right)
    return float(np.corrcoef(left_rank, right_rank)[0, 1])


def _ranks(values: np.ndarray) -> np.ndarray:
    order = np.argsort(values, kind="mergesort")
    ranks = np.empty(values.size, dtype=float)
    ranks[order] = np.arange(values.size, dtype=float)
    return ranks


def _read_object(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise TaskValidityPowerError(f"JSON object required: {path}")
    return payload


def _resolve_path(workspace: Path, raw_path: Any) -> Path:
    path = (workspace / str(raw_path)).resolve()
    try:
        path.relative_to(workspace.resolve())
    except ValueError as exc:
        raise TaskValidityPowerError("dependency path escapes workspace") from exc
    return path


def _canonical_sha256(payload: Mapping[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False).encode(
        "utf-8"
    )
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
    "TaskValidityPowerError",
    "load_task_validity_power_protocol",
    "run_task_validity_power",
]
