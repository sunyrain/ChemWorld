"""Preregistered paired inference and failure handling for formal protocol 0.4."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import subprocess
from collections import Counter
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

import numpy as np

from chemworld.physchem.mechanism_library import configuration_root

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_PROTOCOL_PATH = (
    configuration_root() / "benchmark" / "statistical_analysis_plan_v0.4.json"
)
DEFAULT_REPORT_PATH = (
    ROOT
    / "workstreams"
    / "benchmark_v1"
    / "reports"
    / "statistical-analysis-plan-v0.4.json"
)
PROTOCOL_VERSION = "chemworld-statistical-analysis-plan-0.4"
CORE_TASKS = (
    "partition-discovery",
    "reaction-to-crystallization",
    "reaction-to-distillation",
    "flow-reaction-optimization",
)
FAILURE_CLASSES = (
    "invalid_action",
    "provider_model_failure",
    "runtime_failure",
    "budget_overrun",
    "incomplete_accounting",
)
JOINT_REQUIREMENTS = (
    "positive_objective_interval",
    "holm_adjusted_p_at_or_below_alpha",
    "mean_effect_reaches_task_sesoi",
    "safety_noninferiority",
    "cost_noninferiority",
    "complete_pair_matrix",
    "all_candidate_and_comparator_trajectories_replay_verified",
    "all_required_resource_accounting_complete",
)
CHAMPION_ELIGIBILITY = (
    "all_planned_dev_cells_present",
    "all_dev_trajectories_replay_verified",
    "all_dev_resource_ledgers_complete",
    "no_budget_overrun",
    "frozen_method_or_prompt_or_checkpoint_hash",
)
CHAMPION_RANKING = (
    "number_of_core_tasks_reaching_dev_sesoi_with_safety_and_cost_noninferiority",
    "mean_normalized_primary_anytime_auc",
    "lower_risk_exceedance_rate",
    "lower_relative_process_cost",
    "lower_resource_use_only_as_final_tie_breaker",
)


class FormalStatisticsError(RuntimeError):
    """Raised when a formal analysis matrix is ambiguous or malformed."""


def load_statistical_analysis_plan(path: Path | None = None) -> dict[str, Any]:
    resolved = DEFAULT_PROTOCOL_PATH if path is None else path
    payload = _read_object(resolved)
    if payload.get("schema_version") != PROTOCOL_VERSION:
        raise FormalStatisticsError("unsupported statistical analysis plan")
    return payload


def paired_percentile_interval(
    effects: Sequence[float],
    *,
    confidence_level: float,
    bootstrap_samples: int,
    seed_material: str,
) -> tuple[float, float]:
    values = _finite_vector(effects, minimum_size=2)
    if not 0.5 < confidence_level < 1.0:
        raise FormalStatisticsError("confidence level must be in (0.5, 1)")
    if bootstrap_samples < 1_000:
        raise FormalStatisticsError("formal bootstrap requires at least 1,000 samples")
    if np.all(values == values[0]):
        return float(values[0]), float(values[0])
    rng = np.random.default_rng(_derived_seed(seed_material))
    indices = rng.integers(0, values.size, size=(bootstrap_samples, values.size))
    means = values[indices].mean(axis=1)
    tail = (1.0 - confidence_level) / 2.0
    return (
        float(np.quantile(means, tail, method="lower")),
        float(np.quantile(means, 1.0 - tail, method="higher")),
    )


def paired_sign_flip_p_value(
    effects: Sequence[float], *, randomization_samples: int, seed_material: str
) -> float:
    """Deterministic two-sided paired randomization test without a large allocation."""

    values = _finite_vector(effects, minimum_size=2)
    if randomization_samples < 10_000:
        raise FormalStatisticsError("formal randomization test requires at least 10,000 samples")
    observed = abs(float(values.mean()))
    if observed == 0.0 or np.all(values == 0.0):
        return 1.0
    if np.all(values == values[0]):
        # Only all-positive and all-negative signs equal the observed absolute mean.
        return min(1.0, 2.0 ** (1 - values.size))
    rng = np.random.default_rng(_derived_seed(seed_material))
    exceedances = 0
    completed = 0
    batch_size = 4096
    while completed < randomization_samples:
        batch = min(batch_size, randomization_samples - completed)
        signs = rng.integers(0, 2, size=(batch, values.size), dtype=np.int8) * 2 - 1
        randomized = np.abs((signs * values).mean(axis=1))
        exceedances += int(np.count_nonzero(randomized >= observed - 1.0e-15))
        completed += batch
    return (exceedances + 1.0) / (randomization_samples + 1.0)


def holm_adjusted_p_values(p_values: Mapping[str, float]) -> dict[str, float]:
    if not p_values:
        raise FormalStatisticsError("Holm correction requires at least one test")
    ordered: list[tuple[str, float]] = []
    for key, value in p_values.items():
        if not math.isfinite(float(value)) or not 0.0 <= float(value) <= 1.0:
            raise FormalStatisticsError("p-values must be finite and in [0, 1]")
        ordered.append((str(key), float(value)))
    ordered.sort(key=lambda item: (item[1], item[0]))
    count = len(ordered)
    running = 0.0
    adjusted: dict[str, float] = {}
    for index, (key, value) in enumerate(ordered):
        running = max(running, min(1.0, (count - index) * value))
        adjusted[key] = running
    return adjusted


def analyze_paired_contrast(
    rows: Sequence[Mapping[str, Any]],
    *,
    protocol: Mapping[str, Any],
    candidate: str,
    comparator: str,
    pair_ids: Sequence[str],
    contrast_id: str | None = None,
) -> dict[str, Any]:
    """Apply the complete joint rule while retaining every expected pair."""

    if not candidate or not comparator or candidate == comparator:
        raise FormalStatisticsError("candidate and comparator must be distinct non-empty ids")
    expected_pairs = tuple(str(pair_id) for pair_id in pair_ids)
    if len(expected_pairs) != len(set(expected_pairs)) or not expected_pairs:
        raise FormalStatisticsError("pair ids must be non-empty and unique")
    population = protocol.get("analysis_population", {})
    expected_count = int(population.get("paired_identity_count", 0))
    if len(expected_pairs) != expected_count:
        raise FormalStatisticsError(
            f"formal analysis requires {expected_count} paired identities"
        )
    task_ids = tuple(str(task) for task in population.get("formal_core_tasks", ()))
    if task_ids != CORE_TASKS:
        raise FormalStatisticsError("formal core task scope drifted")
    active_contrast = contrast_id or str(protocol["primary_contrast"]["contrast_id"])
    indexed = _index_rows(
        rows,
        candidate=candidate,
        comparator=comparator,
        task_ids=task_ids,
        pair_ids=expected_pairs,
    )
    objective = protocol["objective_inference"]
    constraints = protocol["constraint_inference"]
    failure_policy = protocol["failure_denominator"]
    raw_p_values: dict[str, float] = {}
    cards: dict[str, dict[str, Any]] = {}
    for task_id in task_ids:
        expected_keys = [
            (task_id, method_id, pair_id)
            for pair_id in expected_pairs
            for method_id in (candidate, comparator)
        ]
        missing = [key for key in expected_keys if key not in indexed]
        if missing:
            cards[task_id] = _incomplete_task_card(
                task_id,
                expected_pair_count=expected_count,
                missing_row_count=len(missing),
                missing_pair_count=len({key[2] for key in missing}),
            )
            raw_p_values[task_id] = 1.0
            continue
        primary_effects: list[float] = []
        safety_effects: list[float] = []
        cost_effects: list[float] = []
        failure_counts: dict[str, Counter[str]] = {
            candidate: Counter(),
            comparator: Counter(),
        }
        all_replay = True
        all_accounting = True
        candidate_successes = 0
        comparator_successes = 0
        cost_available = True
        for pair_id in expected_pairs:
            candidate_row = indexed[(task_id, candidate, pair_id)]
            comparator_row = indexed[(task_id, comparator, pair_id)]
            candidate_value = _effective_row(candidate_row, failure_policy)
            comparator_value = _effective_row(comparator_row, failure_policy)
            candidate_successes += int(candidate_value["status"] == "success")
            comparator_successes += int(comparator_value["status"] == "success")
            if candidate_value["failure_class"] is not None:
                failure_counts[candidate][candidate_value["failure_class"]] += 1
            if comparator_value["failure_class"] is not None:
                failure_counts[comparator][comparator_value["failure_class"]] += 1
            all_replay = all_replay and bool(candidate_value["replay_verified"])
            all_replay = all_replay and bool(comparator_value["replay_verified"])
            all_accounting = all_accounting and bool(candidate_value["accounting_complete"])
            all_accounting = all_accounting and bool(
                comparator_value["accounting_complete"]
            )
            primary_effects.append(
                float(candidate_value["primary_value"])
                - float(comparator_value["primary_value"])
            )
            safety_effects.append(
                float(candidate_value["risk_exceedance_rate"])
                - float(comparator_value["risk_exceedance_rate"])
            )
            candidate_cost = candidate_value["process_cost"]
            comparator_cost = comparator_value["process_cost"]
            if (
                candidate_cost is None
                or comparator_cost is None
                or float(comparator_cost) <= 0.0
            ):
                cost_available = False
            else:
                cost_effects.append(
                    (float(candidate_cost) - float(comparator_cost))
                    / float(comparator_cost)
                )

        seed_base = f"{protocol['protocol_id']}|{active_contrast}|{task_id}"
        interval = paired_percentile_interval(
            primary_effects,
            confidence_level=float(objective["confidence_level"]),
            bootstrap_samples=int(objective["bootstrap_samples"]),
            seed_material=seed_base + "|objective-bootstrap",
        )
        p_value = paired_sign_flip_p_value(
            primary_effects,
            randomization_samples=int(objective["randomization_samples"]),
            seed_material=seed_base + "|objective-randomization",
        )
        raw_p_values[task_id] = p_value
        safety = _noninferiority_card(
            safety_effects,
            margin=float(constraints["safety"]["noninferiority_margin"]),
            upper_quantile=float(constraints["one_sided_upper_quantile"]),
            bootstrap_samples=int(constraints["bootstrap_samples"]),
            seed_material=seed_base + "|safety",
        )
        cost = (
            _noninferiority_card(
                cost_effects,
                margin=float(constraints["cost"]["noninferiority_margin"]),
                upper_quantile=float(constraints["one_sided_upper_quantile"]),
                bootstrap_samples=int(constraints["bootstrap_samples"]),
                seed_material=seed_base + "|cost",
            )
            if cost_available and len(cost_effects) == expected_count
            else {
                "mean_effect": None,
                "simultaneous_upper_confidence_bound": None,
                "noninferiority_margin": float(
                    constraints["cost"]["noninferiority_margin"]
                ),
                "noninferiority_passed": False,
                "reason": "cost unavailable or comparator cost non-positive",
            }
        )
        cards[task_id] = {
            "task_id": task_id,
            "expected_pair_count": expected_count,
            "observed_pair_count": expected_count,
            "missing_row_count": 0,
            "matrix_complete": True,
            "mean_paired_primary_effect": float(np.mean(primary_effects)),
            "paired_primary_interval": list(interval),
            "raw_sign_flip_p_value": p_value,
            "holm_adjusted_p_value": None,
            "sesoi": float(objective["task_sesoi"][task_id]),
            "positive_objective_interval": interval[0] > 0.0,
            "mean_effect_reaches_task_sesoi": float(np.mean(primary_effects))
            >= float(objective["task_sesoi"][task_id]),
            "safety": safety,
            "cost": cost,
            "candidate_success_count": candidate_successes,
            "comparator_success_count": comparator_successes,
            "failure_counts": {
                candidate: dict(sorted(failure_counts[candidate].items())),
                comparator: dict(sorted(failure_counts[comparator].items())),
            },
            "all_trajectories_replay_verified": all_replay,
            "all_required_resource_accounting_complete": all_accounting,
            "joint_primary_rule_passed": False,
        }

    adjusted = holm_adjusted_p_values(raw_p_values)
    alpha = float(objective["familywise_alpha"])
    for task_id, card in cards.items():
        card["holm_adjusted_p_value"] = adjusted[task_id]
        card["holm_adjusted_p_at_or_below_alpha"] = adjusted[task_id] <= alpha
        card["joint_primary_rule_passed"] = bool(
            card["matrix_complete"]
            and card.get("positive_objective_interval") is True
            and card["holm_adjusted_p_at_or_below_alpha"]
            and card.get("mean_effect_reaches_task_sesoi") is True
            and card.get("safety", {}).get("noninferiority_passed") is True
            and card.get("cost", {}).get("noninferiority_passed") is True
            and card.get("all_trajectories_replay_verified") is True
            and card.get("all_required_resource_accounting_complete") is True
        )

    return {
        "schema_version": "chemworld-formal-paired-analysis-0.4",
        "protocol_id": protocol.get("protocol_id"),
        "contrast_id": active_contrast,
        "candidate": candidate,
        "comparator": comparator,
        "paired_identity_count": expected_count,
        "cross_task_primary_scalar": None,
        "task_decisions": cards,
        "task_pass_count": sum(
            bool(card["joint_primary_rule_passed"]) for card in cards.values()
        ),
        "benchmark_wide_joint_rule_passed": all(
            card["joint_primary_rule_passed"] for card in cards.values()
        ),
        "formal_results_present": True,
        "benchmark_claim_allowed": False,
    }


def select_dev_family_champion(
    rows: Sequence[Mapping[str, Any]],
    *,
    protocol: Mapping[str, Any],
    family: str,
) -> dict[str, Any]:
    """Select one preregistered family champion using Dev evidence only."""

    policy = protocol.get("family_champion_selection")
    if not _champion_policy_ready(policy):
        raise FormalStatisticsError("family champion policy is not frozen")
    assert isinstance(policy, Mapping)
    families = policy["families"]
    assert isinstance(families, Mapping)
    raw_methods = families.get(family)
    if not isinstance(raw_methods, Sequence) or isinstance(raw_methods, (str, bytes)):
        raise FormalStatisticsError(f"unknown champion family: {family}")
    expected_methods = tuple(str(method_id) for method_id in raw_methods)
    indexed: dict[str, Mapping[str, Any]] = {}
    forbidden_keys: list[str] = []
    for row in rows:
        method_id = str(row.get("method_id", ""))
        split = row.get("split")
        if split != "dev":
            raise FormalStatisticsError("family champion selection accepts Dev rows only")
        forbidden_keys.extend(
            str(key) for key in row if str(key).lower().startswith("bench")
        )
        if method_id not in expected_methods:
            raise FormalStatisticsError("selection row contains a method outside the family")
        if method_id in indexed:
            raise FormalStatisticsError("duplicate family champion selection row")
        indexed[method_id] = row
    if forbidden_keys:
        raise FormalStatisticsError("Bench information is forbidden during champion selection")
    missing = sorted(set(expected_methods) - set(indexed))
    if missing:
        raise FormalStatisticsError(f"family selection rows are incomplete: {missing}")

    ranked: list[dict[str, Any]] = []
    for method_id in expected_methods:
        row = indexed[method_id]
        eligibility = {
            key: row.get(key) is True for key in CHAMPION_ELIGIBILITY
        }
        identity = str(row.get("frozen_identity_sha256", ""))
        if not _is_sha256(identity):
            eligibility["frozen_method_or_prompt_or_checkpoint_hash"] = False
        tasks_reaching = _integer_in_range(
            row.get("core_tasks_reaching_joint_sesoi"),
            label="core_tasks_reaching_joint_sesoi",
            lower=0,
            upper=len(CORE_TASKS),
        )
        auc = _finite_number(
            row.get("mean_normalized_primary_anytime_auc"),
            "mean_normalized_primary_anytime_auc",
        )
        risk = _bounded_number(row.get("risk_exceedance_rate"), "risk_exceedance_rate")
        cost = _nonnegative_number(row.get("relative_process_cost"), "relative_process_cost")
        resource = _nonnegative_number(
            row.get("resource_use_tiebreak"), "resource_use_tiebreak"
        )
        ranked.append(
            {
                "method_id": method_id,
                "eligible": all(eligibility.values()),
                "eligibility": eligibility,
                "frozen_identity_sha256": identity,
                "core_tasks_reaching_joint_sesoi": tasks_reaching,
                "mean_normalized_primary_anytime_auc": auc,
                "risk_exceedance_rate": risk,
                "relative_process_cost": cost,
                "resource_use_tiebreak": resource,
            }
        )
    eligible = [item for item in ranked if item["eligible"]]
    if not eligible:
        raise FormalStatisticsError("no eligible Dev family champion candidate")
    eligible.sort(
        key=lambda item: (
            -int(item["core_tasks_reaching_joint_sesoi"]),
            -float(item["mean_normalized_primary_anytime_auc"]),
            float(item["risk_exceedance_rate"]),
            float(item["relative_process_cost"]),
            float(item["resource_use_tiebreak"]),
            str(item["method_id"]),
        )
    )
    return {
        "schema_version": "chemworld-dev-family-champion-selection-0.4",
        "protocol_id": protocol.get("protocol_id"),
        "family": family,
        "selection_split": "dev",
        "bench_information_used": False,
        "expected_candidate_count": len(expected_methods),
        "eligible_candidate_count": len(eligible),
        "selected_method_id": eligible[0]["method_id"],
        "selected_identity_sha256": eligible[0]["frozen_identity_sha256"],
        "ranking": eligible,
        "policy_sha256": _canonical_sha256(policy),
    }


def audit_statistical_analysis_plan(
    protocol: Mapping[str, Any],
    *,
    workspace: Path = ROOT,
    run_synthetic: bool = True,
) -> dict[str, Any]:
    controls: dict[str, bool] = {}
    controls["schema_and_state_are_nonclaiming"] = (
        protocol.get("schema_version") == PROTOCOL_VERSION
        and protocol.get("status") == "preregistered_controls_no_formal_results"
        and protocol.get("formal_results_present") is False
        and protocol.get("benchmark_claim_allowed") is False
    )
    controls["parent_protocols_and_reports_are_hash_bound"] = _parents_ready(
        protocol.get("parent_bindings"), workspace
    )
    population = protocol.get("analysis_population", {})
    controls["population_is_100_paired_core4_without_scalarization"] = (
        isinstance(population, Mapping)
        and population.get("unit") == "paired_task_private_bench_identity"
        and population.get("paired_identity_count") == 100
        and tuple(population.get("formal_core_tasks", ())) == CORE_TASKS
        and population.get("required_spectrum_condition_for_primary") == "masked"
        and population.get("all_expected_pairs_remain_in_denominator") is True
        and population.get("task_level_inference_only") is True
        and population.get("cross_task_primary_scalar") is None
    )
    primary = protocol.get("primary_contrast", {})
    controls["one_primary_operation_contrast_is_frozen"] = (
        isinstance(primary, Mapping)
        and primary.get("contrast_id")
        == "operation_champion_vs_operation_random_masked"
        and tuple(primary.get("candidate_pool", ()))
        == ("rule_based", "ppo", "sac", "live_llm_a", "live_llm_b")
        and primary.get("comparator") == "operation_random"
        and primary.get("spectrum_condition") == "masked"
        and primary.get("one_candidate_is_frozen_before_bench") is True
        and primary.get("per_task_claims_only") is True
    )
    controls["objective_inference_and_holm_are_frozen"] = _objective_ready(
        protocol.get("objective_inference"), workspace
    )
    controls["constraint_noninferiority_matches_power_design"] = _constraints_ready(
        protocol.get("constraint_inference")
    )
    joint = protocol.get("joint_primary_rule", {})
    controls["joint_rule_cannot_be_replaced_by_total_score"] = (
        isinstance(joint, Mapping)
        and tuple(joint.get("required_per_task", ())) == JOINT_REQUIREMENTS
        and joint.get("total_score_can_replace_joint_rule") is False
        and joint.get("partial_success_label") == "not_allowed"
        and joint.get("task_failure_does_not_hide_other_task_results") is True
    )
    controls["failure_denominator_is_complete_and_fail_closed"] = _failure_policy_ready(
        protocol.get("failure_denominator")
    )
    controls["family_champions_use_dev_only_and_freeze_before_bench"] = (
        _champion_policy_ready(protocol.get("family_champion_selection"))
    )
    controls["secondary_reporting_is_separate_and_complete"] = _secondary_ready(
        protocol.get("secondary_reporting")
    )

    synthetic = _synthetic_fixture_audit(protocol) if run_synthetic else {}
    controls["synthetic_null_has_no_false_positive"] = (
        not run_synthetic
        or synthetic.get("null", {}).get("benchmark_wide_joint_rule_passed") is False
    )
    controls["synthetic_positive_has_expected_power"] = (
        not run_synthetic
        or synthetic.get("positive", {}).get("benchmark_wide_joint_rule_passed") is True
    )
    controls["synthetic_unsafe_and_cost_regressing_are_rejected"] = (
        not run_synthetic
        or (
            synthetic.get("unsafe", {}).get("objective_all_tasks_passed") is True
            and synthetic.get("unsafe", {}).get("benchmark_wide_joint_rule_passed") is False
            and synthetic.get("cost_regressing", {}).get("objective_all_tasks_passed") is True
            and synthetic.get("cost_regressing", {}).get(
                "benchmark_wide_joint_rule_passed"
            )
            is False
        )
    )
    controls["synthetic_failed_runs_remain_in_denominator"] = (
        not run_synthetic
        or (
            synthetic.get("failed_runs", {}).get("minimum_observed_pair_count") == 100
            and synthetic.get("failed_runs", {}).get("candidate_success_count") == 99
            and synthetic.get("failed_runs", {}).get("benchmark_wide_joint_rule_passed")
            is False
        )
    )
    controls_ready = all(controls.values())
    commit, dirty = _git_provenance(workspace)
    return {
        "schema_version": "chemworld-statistical-analysis-plan-audit-0.4",
        "protocol_id": protocol.get("protocol_id"),
        "status": "statistical_plan_frozen_no_formal_results"
        if controls_ready
        else "statistical_plan_controls_failed",
        "controls_ready": controls_ready,
        "formal_results_present": False,
        "benchmark_claim_allowed": False,
        "source_commit": commit,
        "source_tree_dirty": dirty,
        "protocol_sha256": _canonical_sha256(protocol),
        "paired_identity_count": population.get("paired_identity_count")
        if isinstance(population, Mapping)
        else None,
        "formal_core_tasks": list(CORE_TASKS),
        "primary_contrast": primary.get("contrast_id")
        if isinstance(primary, Mapping)
        else None,
        "synthetic_fixtures": synthetic,
        "controls": controls,
        "limitations": [
            "Synthetic fixtures validate estimator behavior; they are not benchmark results.",
            "Only one primary contrast receives the P0-powered confirmatory claim allocation.",
            (
                "Secondary family comparisons remain task-level and separately "
                "multiplicity-controlled."
            ),
        ],
        "next_gates": [
            "freeze the independent reference portfolio plan",
            "bind this evaluator into the formal cell runner and preflight",
            "select and freeze family champions using Dev evidence only",
        ],
    }


def _index_rows(
    rows: Sequence[Mapping[str, Any]],
    *,
    candidate: str,
    comparator: str,
    task_ids: tuple[str, ...],
    pair_ids: tuple[str, ...],
) -> dict[tuple[str, str, str], Mapping[str, Any]]:
    indexed: dict[tuple[str, str, str], Mapping[str, Any]] = {}
    expected_tasks = set(task_ids)
    expected_methods = {candidate, comparator}
    expected_pairs = set(pair_ids)
    for row in rows:
        task_id = str(row.get("task_id", ""))
        method_id = str(row.get("method_id", ""))
        pair_id = str(row.get("pair_id", ""))
        if task_id not in expected_tasks or method_id not in expected_methods:
            continue
        if pair_id not in expected_pairs:
            raise FormalStatisticsError("unexpected pair identity in formal matrix")
        key = (task_id, method_id, pair_id)
        if key in indexed:
            raise FormalStatisticsError("duplicate formal result row")
        indexed[key] = row
    return indexed


def _effective_row(
    row: Mapping[str, Any], failure_policy: Mapping[str, Any]
) -> dict[str, Any]:
    status = row.get("status")
    if status not in {"success", "failure"}:
        raise FormalStatisticsError("result status must be success or failure")
    replay = row.get("replay_verified")
    accounting = row.get("accounting_complete")
    if not isinstance(replay, bool) or not isinstance(accounting, bool):
        raise FormalStatisticsError("replay and accounting flags must be explicit booleans")
    failure_class: str | None = None
    if status == "failure":
        raw_class = row.get("failure_class")
        if raw_class not in FAILURE_CLASSES:
            raise FormalStatisticsError("failed result has an unknown failure class")
        failure_class = str(raw_class)
        primary = float(failure_policy["failed_method_primary_value"])
        risk = float(failure_policy["failed_method_risk_exceedance_rate"])
    else:
        if row.get("failure_class") is not None:
            raise FormalStatisticsError("successful result cannot have a failure class")
        primary = _finite_number(row.get("primary_value"), "primary_value")
        risk = _finite_number(row.get("risk_exceedance_rate"), "risk_exceedance_rate")
        if not 0.0 <= risk <= 1.0:
            raise FormalStatisticsError("risk exceedance rate must be in [0, 1]")
    raw_cost = row.get("process_cost")
    process_cost = (
        None
        if raw_cost is None
        else _finite_number(raw_cost, "process_cost")
    )
    if process_cost is not None and process_cost < 0.0:
        raise FormalStatisticsError("process cost cannot be negative")
    return {
        "status": status,
        "failure_class": failure_class,
        "primary_value": primary,
        "risk_exceedance_rate": risk,
        "process_cost": process_cost,
        "replay_verified": replay,
        "accounting_complete": accounting,
    }


def _noninferiority_card(
    effects: Sequence[float],
    *,
    margin: float,
    upper_quantile: float,
    bootstrap_samples: int,
    seed_material: str,
) -> dict[str, Any]:
    values = _finite_vector(effects, minimum_size=2)
    if not 0.5 < upper_quantile < 1.0:
        raise FormalStatisticsError("upper quantile must be in (0.5, 1)")
    if not math.isfinite(margin) or margin < 0.0:
        raise FormalStatisticsError("noninferiority margin must be finite and non-negative")
    if np.all(values == values[0]):
        upper = float(values[0])
    else:
        rng = np.random.default_rng(_derived_seed(seed_material))
        indices = rng.integers(0, values.size, size=(bootstrap_samples, values.size))
        means = values[indices].mean(axis=1)
        upper = float(np.quantile(means, upper_quantile, method="higher"))
    return {
        "mean_effect": float(values.mean()),
        "simultaneous_upper_confidence_bound": upper,
        "noninferiority_margin": margin,
        "noninferiority_passed": upper <= margin,
    }


def _incomplete_task_card(
    task_id: str,
    *,
    expected_pair_count: int,
    missing_row_count: int,
    missing_pair_count: int,
) -> dict[str, Any]:
    return {
        "task_id": task_id,
        "expected_pair_count": expected_pair_count,
        "observed_pair_count": expected_pair_count - missing_pair_count,
        "missing_row_count": missing_row_count,
        "missing_pair_count": missing_pair_count,
        "matrix_complete": False,
        "raw_sign_flip_p_value": 1.0,
        "holm_adjusted_p_value": None,
        "positive_objective_interval": False,
        "mean_effect_reaches_task_sesoi": False,
        "safety": {"noninferiority_passed": False},
        "cost": {"noninferiority_passed": False},
        "all_trajectories_replay_verified": False,
        "all_required_resource_accounting_complete": False,
        "joint_primary_rule_passed": False,
    }


def _parents_ready(raw: Any, workspace: Path) -> bool:
    if not isinstance(raw, Mapping) or set(raw) != {
        "formal_protocol",
        "formal_protocol_report",
        "interaction_strata",
        "interaction_strata_report",
    }:
        return False
    loaded: dict[str, dict[str, Any]] = {}
    for name, binding in raw.items():
        if not isinstance(binding, Mapping):
            return False
        path = _resolve_workspace_path(workspace, binding.get("path"))
        if path is None or not path.is_file() or _file_sha256(path) != binding.get(
            "file_sha256"
        ):
            return False
        loaded[str(name)] = _read_object(path)
    return (
        _canonical_sha256(loaded["formal_protocol"])
        == raw["formal_protocol"].get("protocol_sha256")
        and loaded["formal_protocol_report"].get("controls_ready") is True
        and loaded["formal_protocol_report"].get("protocol_sha256")
        == raw["formal_protocol"].get("protocol_sha256")
        and _canonical_sha256(loaded["interaction_strata"])
        == raw["interaction_strata"].get("protocol_sha256")
        and loaded["interaction_strata_report"].get("controls_ready") is True
        and loaded["interaction_strata_report"].get("protocol_sha256")
        == raw["interaction_strata"].get("protocol_sha256")
    )


def _objective_ready(raw: Any, workspace: Path) -> bool:
    if not isinstance(raw, Mapping):
        return False
    formal = _read_object(workspace / "configs" / "benchmark" / "formal_protocol_v0.4.json")
    expected_sesoi = {
        task_id: float(formal["task_roles"]["formal_core"][task_id]["sesoi"])
        for task_id in CORE_TASKS
    }
    return (
        raw.get("estimand") == "candidate_minus_comparator_mean_paired_primary_metric"
        and raw.get("direction") == "higher_is_better"
        and raw.get("interval") == "paired_percentile_bootstrap"
        and raw.get("confidence_level") == 0.95
        and raw.get("bootstrap_samples") == 20_000
        and raw.get("hypothesis_test") == "paired_sign_flip_randomization"
        and raw.get("randomization_samples") == 100_000
        and raw.get("multiple_comparison_policy")
        == "holm_across_four_core_tasks_within_primary_contrast"
        and raw.get("familywise_alpha") == 0.05
        and raw.get("direction_rule")
        == "paired_confidence_interval_lower_bound_above_zero"
        and raw.get("practical_rule")
        == "mean_paired_effect_at_least_task_specific_sesoi"
        and raw.get("task_sesoi") == expected_sesoi
    )


def _constraints_ready(raw: Any) -> bool:
    if not isinstance(raw, Mapping):
        return False
    safety = raw.get("safety", {})
    cost = raw.get("cost", {})
    return (
        raw.get("bootstrap_samples") == 20_000
        and raw.get("familywise_alpha") == 0.05
        and raw.get("simultaneous_comparison_count") == 8
        and raw.get("one_sided_upper_quantile") == 0.99375
        and isinstance(safety, Mapping)
        and safety.get("estimand")
        == "candidate_minus_comparator_absolute_risk_exceedance_rate"
        and safety.get("noninferiority_margin") == 0.05
        and safety.get("pass_rule")
        == "simultaneous_upper_confidence_bound_at_or_below_margin"
        and isinstance(cost, Mapping)
        and cost.get("estimand") == "candidate_minus_comparator_cost_relative_to_comparator"
        and cost.get("noninferiority_margin") == 0.05
        and cost.get("pass_rule")
        == "simultaneous_upper_confidence_bound_at_or_below_margin"
    )


def _failure_policy_ready(raw: Any) -> bool:
    return (
        isinstance(raw, Mapping)
        and tuple(raw.get("required_statuses", ())) == ("success", "failure")
        and tuple(raw.get("failure_classes", ())) == FAILURE_CLASSES
        and raw.get("failed_method_primary_value") == 0.0
        and raw.get("failed_method_risk_exceedance_rate") == 1.0
        and raw.get("missing_pair") == "matrix_incomplete_no_claim"
        and raw.get("duplicate_pair") == "reject_analysis"
        and raw.get("replay_failure") == "retain_pair_and_fail_joint_rule"
        and raw.get("accounting_failure") == "retain_pair_and_fail_joint_rule"
        and raw.get("automatic_rerun_or_drop") == "forbidden"
        and raw.get("missing_or_nonfinite_endpoint")
        == "classify_failure_and_use_frozen_worst_case"
        and raw.get("infrastructure_retry")
        == "separate_attempt_lineage_only_same_cell_identity"
    )


def _champion_policy_ready(raw: Any) -> bool:
    if not isinstance(raw, Mapping):
        return False
    families = raw.get("families", {})
    return (
        raw.get("selection_split") == "dev_only"
        and raw.get("bench_information_allowed") is False
        and isinstance(families, Mapping)
        and tuple(families.get("rl", ())) == ("ppo", "sac")
        and tuple(families.get("llm", ())) == ("live_llm_a", "live_llm_b")
        and tuple(families.get("operation_primary", ()))
        == ("rule_based", "ppo", "sac", "live_llm_a", "live_llm_b")
        and tuple(raw.get("eligibility", ())) == CHAMPION_ELIGIBILITY
        and tuple(raw.get("lexicographic_ranking", ())) == CHAMPION_RANKING
        and raw.get("tie_breaker") == "lexicographically_smallest_frozen_method_id"
        and raw.get("selection_artifact_frozen_before_bench") is True
        and raw.get("bench_hyperparameter_prompt_checkpoint_or_seed_selection")
        == "forbidden"
    )


def _secondary_ready(raw: Any) -> bool:
    return (
        isinstance(raw, Mapping)
        and raw.get("confidence_intervals_required") is True
        and raw.get("holm_within_each_named_secondary_family") is True
        and raw.get("negative_results_required") is True
        and raw.get("completion_and_failure_class_counts_required") is True
        and raw.get("wins_ties_losses_required") is True
        and tuple(raw.get("anytime_checkpoints", ())) == (4, 8, 12, 20, 40)
        and raw.get("resource_frontier_reported_without_scalarization") is True
    )


def _synthetic_fixture_audit(protocol: Mapping[str, Any]) -> dict[str, Any]:
    pair_ids = tuple(f"pair-{index:03d}" for index in range(100))
    output: dict[str, Any] = {}
    for fixture in ("null", "positive", "unsafe", "cost_regressing", "failed_runs"):
        rows = _synthetic_rows(protocol, pair_ids=pair_ids, fixture=fixture)
        result = analyze_paired_contrast(
            rows,
            protocol=protocol,
            candidate="candidate",
            comparator="operation_random",
            pair_ids=pair_ids,
        )
        decisions = result["task_decisions"]
        output[fixture] = {
            "benchmark_wide_joint_rule_passed": result[
                "benchmark_wide_joint_rule_passed"
            ],
            "task_pass_count": result["task_pass_count"],
            "objective_all_tasks_passed": all(
                card["positive_objective_interval"]
                and card["holm_adjusted_p_at_or_below_alpha"]
                and card["mean_effect_reaches_task_sesoi"]
                for card in decisions.values()
            ),
            "minimum_observed_pair_count": min(
                int(card["observed_pair_count"]) for card in decisions.values()
            ),
            "candidate_success_count": min(
                int(card.get("candidate_success_count", 0)) for card in decisions.values()
            ),
        }
    return output


def _synthetic_rows(
    protocol: Mapping[str, Any], *, pair_ids: tuple[str, ...], fixture: str
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    sesoi = protocol["objective_inference"]["task_sesoi"]
    for task_id in CORE_TASKS:
        for index, pair_id in enumerate(pair_ids):
            base = 0.4 + (index % 5) * 0.0001
            candidate_primary = base if fixture == "null" else base + 1.5 * float(sesoi[task_id])
            candidate_risk = 0.4 if fixture == "unsafe" else 0.2
            candidate_cost = 120.0 if fixture == "cost_regressing" else 100.0
            rows.append(
                {
                    "task_id": task_id,
                    "method_id": "operation_random",
                    "pair_id": pair_id,
                    "status": "success",
                    "failure_class": None,
                    "primary_value": base,
                    "risk_exceedance_rate": 0.2,
                    "process_cost": 100.0,
                    "replay_verified": True,
                    "accounting_complete": True,
                }
            )
            candidate_row: dict[str, Any] = {
                "task_id": task_id,
                "method_id": "candidate",
                "pair_id": pair_id,
                "status": "success",
                "failure_class": None,
                "primary_value": candidate_primary,
                "risk_exceedance_rate": candidate_risk,
                "process_cost": candidate_cost,
                "replay_verified": True,
                "accounting_complete": True,
            }
            if fixture == "failed_runs" and index == 0:
                candidate_row.update(
                    {
                        "status": "failure",
                        "failure_class": "runtime_failure",
                        "primary_value": None,
                        "risk_exceedance_rate": None,
                        "replay_verified": False,
                        "accounting_complete": False,
                    }
                )
            rows.append(candidate_row)
    return rows


def _finite_vector(values: Sequence[float], *, minimum_size: int) -> np.ndarray:
    vector = np.asarray(values, dtype=float)
    if vector.ndim != 1 or vector.size < minimum_size or not np.all(np.isfinite(vector)):
        raise FormalStatisticsError("paired effects must be a finite one-dimensional vector")
    return vector


def _finite_number(value: Any, label: str) -> float:
    try:
        result = float(value)
    except (TypeError, ValueError) as exc:
        raise FormalStatisticsError(f"{label} must be finite") from exc
    if not math.isfinite(result):
        raise FormalStatisticsError(f"{label} must be finite")
    return result


def _bounded_number(value: Any, label: str) -> float:
    result = _finite_number(value, label)
    if not 0.0 <= result <= 1.0:
        raise FormalStatisticsError(f"{label} must be in [0, 1]")
    return result


def _nonnegative_number(value: Any, label: str) -> float:
    result = _finite_number(value, label)
    if result < 0.0:
        raise FormalStatisticsError(f"{label} must be non-negative")
    return result


def _integer_in_range(value: Any, *, label: str, lower: int, upper: int) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or not lower <= value <= upper:
        raise FormalStatisticsError(f"{label} must be an integer in [{lower}, {upper}]")
    return value


def _is_sha256(value: str) -> bool:
    return len(value) == 64 and all(character in "0123456789abcdef" for character in value)


def _derived_seed(material: str) -> int:
    return int.from_bytes(hashlib.sha256(material.encode("utf-8")).digest()[:8], "big")


def _resolve_workspace_path(workspace: Path, raw: Any) -> Path | None:
    if not isinstance(raw, str) or not raw.strip() or Path(raw).is_absolute():
        return None
    resolved = (workspace / raw).resolve()
    try:
        resolved.relative_to(workspace.resolve())
    except ValueError:
        return None
    return resolved


def _read_object(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise FormalStatisticsError("JSON object required")
    return payload


def _canonical_sha256(payload: Mapping[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--protocol", type=Path, default=DEFAULT_PROTOCOL_PATH)
    parser.add_argument("--output", type=Path, default=DEFAULT_REPORT_PATH)
    args = parser.parse_args()
    report = audit_statistical_analysis_plan(load_statistical_analysis_plan(args.protocol))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "controls_ready": report["controls_ready"],
                "paired_identity_count": report["paired_identity_count"],
                "synthetic_fixture_count": len(report["synthetic_fixtures"]),
                "output": str(args.output),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if report["controls_ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = [
    "FormalStatisticsError",
    "analyze_paired_contrast",
    "audit_statistical_analysis_plan",
    "holm_adjusted_p_values",
    "load_statistical_analysis_plan",
    "paired_percentile_interval",
    "paired_sign_flip_p_value",
    "select_dev_family_champion",
]
