"""Evidence-level audits of how benchmark agents interact with ChemWorld."""

from __future__ import annotations

from collections import Counter, defaultdict
from collections.abc import Sequence
from statistics import fmean
from typing import Any

from chemworld.tasks import SERIOUS_TASK_IDS

INTERACTION_AUDIT_SCHEMA_VERSION = "chemworld-agent-interaction-audit-0.1"
FORMAL_CLASSIC_METHODS = (
    "random",
    "lhs",
    "gp_bo",
    "structured_gp_bo",
    "structured_safe_gp_bo",
)
EXPANDED_CLASSIC_METHODS = (
    "greedy",
    "gp_pi",
    "gp_ucb",
    "rf_ei",
)

_METHOD_CAPABILITIES: dict[str, dict[str, Any]] = {
    "random": {
        "updates_between_experiments": False,
        "adapts_within_experiment": False,
        "uses_intermediate_measurements": False,
        "uses_spectra": False,
        "categorical_encoding": "native recipe sampling",
    },
    "lhs": {
        "updates_between_experiments": False,
        "adapts_within_experiment": False,
        "uses_intermediate_measurements": False,
        "uses_spectra": False,
        "categorical_encoding": "stratified scalar recipe coordinates",
    },
    "gp_bo": {
        "updates_between_experiments": True,
        "adapts_within_experiment": False,
        "uses_intermediate_measurements": False,
        "uses_spectra": False,
        "categorical_encoding": "ordinal scalar coordinates",
    },
    "structured_gp_bo": {
        "updates_between_experiments": True,
        "adapts_within_experiment": False,
        "uses_intermediate_measurements": False,
        "uses_spectra": False,
        "categorical_encoding": "continuous plus material one-hot",
    },
    "structured_safe_gp_bo": {
        "updates_between_experiments": True,
        "adapts_within_experiment": False,
        "uses_intermediate_measurements": False,
        "uses_spectra": False,
        "categorical_encoding": "continuous plus material one-hot",
    },
}


def build_agent_interaction_audit(
    results: Sequence[dict[str, Any]],
    *,
    task_lab_artifacts: Sequence[dict[str, Any]] = (),
    expected_tasks: Sequence[str] = SERIOUS_TASK_IDS,
    expected_methods: Sequence[str] = FORMAL_CLASSIC_METHODS,
) -> dict[str, Any]:
    """Summarize retained interaction evidence and fail closed on missing surfaces."""

    if not results:
        raise ValueError("agent interaction audit requires formal result rows")
    _validate_result_fields(results)
    observed_tasks = sorted({str(row["task_id"]) for row in results})
    observed_methods = sorted({str(row["baseline_agent"]) for row in results})
    expected_task_set = set(expected_tasks)
    expected_method_set = set(expected_methods)
    matrix_complete = (
        set(observed_tasks) == expected_task_set
        and set(observed_methods) == expected_method_set
        and _matrix_cells_complete(results, expected_tasks, expected_methods)
    )

    methods = {
        method: _method_summary(
            [row for row in results if row["baseline_agent"] == method],
            capabilities=_METHOD_CAPABILITIES.get(method, {}),
        )
        for method in observed_methods
    }
    tasks = {
        task_id: _task_risk_summary(
            [row for row in results if row["task_id"] == task_id]
        )
        for task_id in observed_tasks
    }
    total_violations = sum(int(row["safety_violations"]) for row in results)
    risk_values = [float(row["mean_safety_risk"]) for row in results]
    risk_observed = any(value > 1.0e-12 for value in risk_values)
    constraint_active = total_violations > 0
    llm_artifact_count = len(task_lab_artifacts)
    retained_llm_trajectories = sum(
        bool(item.get("trajectory_retained")) for item in task_lab_artifacts
    )
    retained_llm_verified = sum(bool(item.get("verified")) for item in task_lab_artifacts)
    formally_evaluated_methods = set(observed_methods)
    missing_expanded = sorted(set(EXPANDED_CLASSIC_METHODS) - formally_evaluated_methods)

    gates = {
        "formal_classic_matrix_complete": matrix_complete,
        "risk_field_mapping_valid": all("mean_safety_risk" in row for row in results),
        "continuous_risk_observed": risk_observed,
        "safety_constraint_active": constraint_active,
        "safe_method_evaluation_informative": risk_observed and constraint_active,
        "expanded_classic_artifacts_retained": not missing_expanded,
        "formal_llm_artifacts_retained": llm_artifact_count > 0
        and retained_llm_trajectories == llm_artifact_count
        and retained_llm_verified == llm_artifact_count,
        "spectral_policy_formally_evaluated": any(
            bool(item.get("uses_spectra")) and bool(item.get("verified"))
            for item in task_lab_artifacts
        ),
        "within_experiment_adaptation_formally_evaluated": any(
            bool(item.get("adapts_within_experiment")) and bool(item.get("verified"))
            for item in task_lab_artifacts
        ),
    }
    blockers = []
    if not constraint_active:
        blockers.append(
            "Continuous risk is present, but no formal run reaches the safety constraint; "
            "safe optimization is not identified."
        )
    if missing_expanded:
        blockers.append(
            "Greedy, GP-PI, GP-UCB and RF-EI are implemented but lack retained formal "
            "artifacts under the publication protocol."
        )
    if not gates["formal_llm_artifacts_retained"]:
        blockers.append(
            "No retained, replay-verified multi-seed real-LLM artifact is available for "
            "formal comparison."
        )
    if not gates["spectral_policy_formally_evaluated"]:
        blockers.append(
            "The formal classical agents optimize recipe-to-final-score mappings and do "
            "not consume intermediate spectra."
        )
    if not gates["within_experiment_adaptation_formally_evaluated"]:
        blockers.append(
            "No formal method changes an in-progress experiment in response to an "
            "intermediate observation."
        )

    ready = all(gates.values())
    return {
        "schema_version": INTERACTION_AUDIT_SCHEMA_VERSION,
        "status": "ready" if ready else "blocked",
        "ready": ready,
        "formal_result_count": len(results),
        "formal_tasks": observed_tasks,
        "formal_methods": observed_methods,
        "methods": methods,
        "tasks": tasks,
        "safety_comparison": _paired_safe_comparison(results, observed_tasks),
        "llm_evidence": {
            "artifact_count": llm_artifact_count,
            "retained_trajectory_count": retained_llm_trajectories,
            "verified_artifact_count": retained_llm_verified,
            "formal_evidence_ready": gates["formal_llm_artifacts_retained"],
        },
        "coverage_gaps": {
            "implemented_but_not_formal_classic_methods": missing_expanded,
            "real_llm": not gates["formal_llm_artifacts_retained"],
            "spectral_decision_policy": not gates["spectral_policy_formally_evaluated"],
            "within_experiment_adaptation": not gates[
                "within_experiment_adaptation_formally_evaluated"
            ],
        },
        "gates": gates,
        "blockers": blockers,
    }


def _validate_result_fields(results: Sequence[dict[str, Any]]) -> None:
    required = {
        "task_id",
        "baseline_agent",
        "seed",
        "total_score",
        "mean_safety_risk",
        "safety_violations",
        "invalid_action_count",
        "final_assay_count",
        "bo_initial_recipe_count",
        "bo_acquisition_recipe_count",
        "bo_entered_acquisition",
        "observation_use_summary",
        "resource_usage",
        "verified",
    }
    for index, row in enumerate(results):
        missing = sorted(required - set(row))
        if missing:
            raise ValueError(f"formal result row {index} is missing fields: {missing}")
        if row["verified"] is not True:
            raise ValueError(f"formal result row {index} is not replay verified")
        if not isinstance(row["mean_safety_risk"], int | float):
            raise ValueError(f"formal result row {index} has non-numeric mean_safety_risk")


def _matrix_cells_complete(
    results: Sequence[dict[str, Any]],
    tasks: Sequence[str],
    methods: Sequence[str],
) -> bool:
    seeds_by_cell: dict[tuple[str, str], set[int]] = defaultdict(set)
    counts: Counter[tuple[str, str, int]] = Counter()
    for row in results:
        key = (str(row["task_id"]), str(row["baseline_agent"]))
        seed = int(row["seed"])
        seeds_by_cell[key].add(seed)
        counts[(*key, seed)] += 1
    reference_seeds: set[int] | None = None
    for task_id in tasks:
        for method in methods:
            seeds = seeds_by_cell.get((task_id, method), set())
            if not seeds:
                return False
            if reference_seeds is None:
                reference_seeds = seeds
            if seeds != reference_seeds:
                return False
            if any(counts[(task_id, method, seed)] != 1 for seed in seeds):
                return False
    return reference_seeds is not None


def _method_summary(
    rows: Sequence[dict[str, Any]],
    *,
    capabilities: dict[str, Any],
) -> dict[str, Any]:
    instruments: Counter[str] = Counter()
    for row in rows:
        instruments.update(row["observation_use_summary"].get("instrument_counts", {}))
    return {
        "run_count": len(rows),
        "task_count": len({str(row["task_id"]) for row in rows}),
        "seed_count": len({int(row["seed"]) for row in rows}),
        "mean_total_score": fmean(float(row["total_score"]) for row in rows),
        "mean_safety_risk": fmean(float(row["mean_safety_risk"]) for row in rows),
        "risk_range_across_run_means": [
            min(float(row["mean_safety_risk"]) for row in rows),
            max(float(row["mean_safety_risk"]) for row in rows),
        ],
        "safety_violation_count": sum(int(row["safety_violations"]) for row in rows),
        "invalid_action_count": sum(int(row["invalid_action_count"]) for row in rows),
        "mean_complete_experiments": fmean(float(row["final_assay_count"]) for row in rows),
        "acquisition_entry_rate": fmean(
            float(bool(row["bo_entered_acquisition"])) for row in rows
        ),
        "mean_initial_recipe_count": fmean(
            float(row["bo_initial_recipe_count"]) for row in rows
        ),
        "mean_acquisition_recipe_count": fmean(
            float(row["bo_acquisition_recipe_count"]) for row in rows
        ),
        "mean_run_wall_time_s": fmean(
            float(row["resource_usage"]["run_wall_time_s"]) for row in rows
        ),
        "instrument_measurement_counts": dict(sorted(instruments.items())),
        "capabilities": dict(capabilities),
    }


def _task_risk_summary(rows: Sequence[dict[str, Any]]) -> dict[str, Any]:
    values = [float(row["mean_safety_risk"]) for row in rows]
    return {
        "run_count": len(rows),
        "mean_safety_risk": fmean(values),
        "min_run_mean_safety_risk": min(values),
        "max_run_mean_safety_risk": max(values),
        "safety_violation_count": sum(int(row["safety_violations"]) for row in rows),
    }


def _paired_safe_comparison(
    results: Sequence[dict[str, Any]],
    tasks: Sequence[str],
) -> dict[str, Any]:
    output: dict[str, Any] = {}
    for task_id in tasks:
        by_method_seed = {
            (str(row["baseline_agent"]), int(row["seed"])): row
            for row in results
            if row["task_id"] == task_id
        }
        seeds = sorted(
            seed
            for method, seed in by_method_seed
            if method == "structured_safe_gp_bo"
            and ("structured_gp_bo", seed) in by_method_seed
        )
        if not seeds:
            continue
        effects: dict[str, list[float]] = {
            "mean_safety_risk": [],
            "safety_aware_score": [],
            "total_score": [],
        }
        for seed in seeds:
            safe = by_method_seed[("structured_safe_gp_bo", seed)]
            base = by_method_seed[("structured_gp_bo", seed)]
            for field in effects:
                effects[field].append(float(safe[field]) - float(base[field]))
        output[task_id] = {
            "seed_count": len(seeds),
            "safe_minus_structured_gp": {
                field: fmean(values) for field, values in effects.items()
            },
        }
    return output


__all__ = [
    "EXPANDED_CLASSIC_METHODS",
    "FORMAL_CLASSIC_METHODS",
    "INTERACTION_AUDIT_SCHEMA_VERSION",
    "build_agent_interaction_audit",
]
