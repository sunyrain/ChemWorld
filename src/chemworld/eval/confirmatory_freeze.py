"""Pre-result freeze for the vNext confirmatory benchmark protocol."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
from typing import Any

from chemworld.physchem.mechanism_library import configuration_root
from chemworld.tasks import SERIOUS_TASK_IDS
from chemworld.world.world_family import AxisIntervention, axes_for_task

CONFIRMATORY_FREEZE_PROTOCOL_VERSION = "chemworld-confirmatory-freeze-protocol-0.3"
CONFIRMATORY_FREEZE_AUDIT_VERSION = "chemworld-confirmatory-freeze-audit-0.3"
DEFAULT_CONFIRMATORY_FREEZE_PATH = (
    configuration_root() / "benchmark" / "confirmatory_freeze_vnext.json"
)
ROOT = Path(__file__).resolve().parents[3]
REPORT_ROOT = ROOT / "workstreams" / "benchmark_v1" / "reports"


def load_confirmatory_freeze(
    path: str | Path = DEFAULT_CONFIRMATORY_FREEZE_PATH,
) -> dict[str, Any]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("confirmatory freeze must be a JSON object")
    return payload


def audit_confirmatory_freeze(protocol: dict[str, Any]) -> dict[str, Any]:
    """Verify that task, effect, seed, world, and dependency freezes are coherent."""

    task_validity = _load_report("task-validity-vnext.json")
    method_report = _load_report("method-protocol-vnext.json")
    world_report = _load_report("world-family-axis-controls.json")
    harness_report = _load_report("public-harness-controls.json")
    score_replay_report = _load_report("score-replay-controls.json")
    risk_cost_report = _load_report("risk-cost-signal-controls.json")
    exploit_report = _load_report("exploit-matrix-controls.json")
    method_protocol = json.loads(
        (configuration_root() / "benchmark" / "method_protocol_vnext.json").read_text(
            encoding="utf-8"
        )
    )

    roles = protocol.get("task_roles", {})
    core_tasks = tuple(roles.get("core", ()))
    exploratory_tasks = tuple(roles.get("exploratory", ()))
    recommendation = task_validity.get("suite_recommendation", {})
    primary = protocol.get("primary_comparison", {})
    confirmation_seeds = tuple(int(seed) for seed in primary.get("paired_confirmatory_seeds", ()))
    method_seeds = tuple(int(seed) for seed in method_protocol.get("confirmatory_seed_ids", ()))

    sesoi_checks, sesoi_cards = _audit_sesoi(protocol, task_validity, core_tasks)
    split_checks, split_summary = _audit_world_allocation(
        protocol, core_tasks, confirmation_seeds
    )
    dependency_checks = {
        "task_validity_controls": task_validity.get("controls_ready") is True,
        "method_resource_controls": method_report.get("controls_ready") is True,
        "world_family_controls": world_report.get("controls_ready") is True,
        "public_harness_controls": harness_report.get("controls_ready") is True,
        "score_replay_controls": score_replay_report.get("controls_ready") is True,
        "risk_cost_controls": risk_cost_report.get("controls_ready") is True,
        "exploit_matrix_controls": exploit_report.get("controls_ready") is True,
    }
    checks = {
        "schema": protocol.get("schema_version") == CONFIRMATORY_FREEZE_PROTOCOL_VERSION,
        "candidate_is_non_claiming": protocol.get("benchmark_claim_allowed") is False,
        "freeze_is_versioned": protocol.get("freeze_rule")
        == "changes_require_new_protocol_id_and_discard_prechange_results",
        "supersedes_objective_only_protocol": protocol.get("supersedes_protocol_id")
        == "chemworld-vnext-confirmatory-freeze-0.2",
        "superseded_cohort_is_diagnostic": protocol.get("superseded_cohort_policy")
        == "seeds_20_39_are_diagnostic_only_and_must_not_be_reused",
        "core_matches_task_validity": core_tasks
        == tuple(recommendation.get("recommended_core_tasks", ())),
        "exploratory_scope": exploratory_tasks
        == ("electrochemical-conversion", "equilibrium-characterization"),
        "all_serious_tasks_classified": set(core_tasks) | set(exploratory_tasks)
        == set(SERIOUS_TASK_IDS),
        "task_roles_disjoint": not (set(core_tasks) & set(exploratory_tasks)),
        "confirmatory_seed_count": len(confirmation_seeds) == 20,
        "confirmatory_seeds_unique": len(set(confirmation_seeds)) == len(confirmation_seeds),
        "confirmatory_seeds_are_fresh": not (set(confirmation_seeds) & set(range(20, 40))),
        "confirmatory_seeds_match_method_protocol": confirmation_seeds == method_seeds,
        "method_protocol_requires_joint_constraints": method_protocol.get(
            "confirmatory_decision_contract", {}
        ).get("objective_safety_and_cost_joint_rule_required")
        is True,
        "complete_experiment_budget_matches": primary.get("complete_experiments_per_run")
        == method_protocol.get("evaluation_budget", {}).get("complete_experiments"),
        "decision_rule_is_joint": _decision_rule_is_joint(
            primary.get("decision_rule", {}), task_count=len(core_tasks)
        ),
        **sesoi_checks,
        **split_checks,
        **dependency_checks,
    }
    controls_ready = all(checks.values())
    missing_methods = list(method_report.get("missing_required_methods", ()))
    primary_method_ids = (
        str(primary.get("candidate_method", "")),
        str(primary.get("comparator", "")),
    )
    method_cards = method_report.get("methods", {})
    primary_methods_ready = bool(all(primary_method_ids)) and all(
        _method_implementation_ready(method_cards, method_id) for method_id in primary_method_ids
    )
    exploit_matrix_complete = exploit_report.get("controls_ready") is True
    primary_classical_rerun_ready = (
        controls_ready and primary_methods_ready and exploit_matrix_complete
    )
    confirmatory_rerun_ready = primary_classical_rerun_ready and not missing_methods
    return {
        "schema_version": CONFIRMATORY_FREEZE_AUDIT_VERSION,
        "protocol_id": protocol.get("protocol_id"),
        "protocol_sha256": _canonical_sha256(protocol),
        "status": (
            "primary_classical_rerun_ready_full_matrix_pending"
            if primary_classical_rerun_ready and not confirmatory_rerun_ready
            else "frozen_waiting_for_primary_dependencies"
            if controls_ready and not primary_classical_rerun_ready
            else "confirmatory_rerun_ready"
            if confirmatory_rerun_ready
            else "freeze_controls_failed"
        ),
        "controls_ready": controls_ready,
        "protocol_frozen": controls_ready,
        "confirmatory_rerun_ready": confirmatory_rerun_ready,
        "primary_classical_rerun_ready": primary_classical_rerun_ready,
        "primary_methods_ready": primary_methods_ready,
        "primary_method_ids": list(primary_method_ids),
        "benchmark_claim_allowed": False,
        "publication_ready": False,
        "checks": checks,
        "task_roles": {"core": list(core_tasks), "exploratory": list(exploratory_tasks)},
        "sesoi": sesoi_cards,
        "world_family_allocation": split_summary,
        "confirmatory_seeds": list(confirmation_seeds),
        "constraint_noninferiority": primary.get("decision_rule", {}).get(
            "constraint_noninferiority", {}
        ),
        "missing_required_methods": missing_methods,
        "exploit_matrix_complete": exploit_matrix_complete,
        "evidence_sha256": {
            "task_validity": _file_sha256(REPORT_ROOT / "task-validity-vnext.json"),
            "method_protocol": _file_sha256(
                configuration_root() / "benchmark" / "method_protocol_vnext.json"
            ),
            "world_family_controls": _file_sha256(REPORT_ROOT / "world-family-axis-controls.json"),
            "public_harness_controls": _file_sha256(REPORT_ROOT / "public-harness-controls.json"),
            "score_replay_controls": _file_sha256(REPORT_ROOT / "score-replay-controls.json"),
            "risk_cost_controls": _file_sha256(REPORT_ROOT / "risk-cost-signal-controls.json"),
            "exploit_matrix_controls": _file_sha256(REPORT_ROOT / "exploit-matrix-controls.json"),
        },
        "known_blockers": [
            (
                "The objective-only 0.2 cohort is diagnostic and cannot be reused after "
                "adding safety and cost noninferiority gates."
            ),
            "PPO, SAC, and two live LLM adapters are not yet eligible for the formal matrix.",
            (
                "The primary classical slice may run, but no cross-family claim is allowed "
                "before PPO, SAC, both live LLM roles, and every failure are retained."
            ),
        ],
        "remaining_release_gates": list(protocol.get("remaining_release_gates", ())),
    }


def _audit_sesoi(
    protocol: dict[str, Any],
    task_validity: dict[str, Any],
    core_tasks: tuple[str, ...],
) -> tuple[dict[str, bool], dict[str, Any]]:
    config = protocol.get("sesoi", {})
    floor = float(config.get("absolute_floor", math.nan))
    fraction = float(config.get("response_surface_fraction", math.nan))
    decimals = int(config.get("round_decimal_places", -1))
    configured = config.get("tasks", {})
    cards: dict[str, Any] = {}
    source_matches = True
    derivation_matches = True
    metric_matches = True
    for task_id in core_tasks:
        source_card = task_validity.get("task_cards", {}).get(task_id, {})
        source_spread = float(source_card.get("response_surface", {}).get("spread", math.nan))
        source_metric = str(source_card.get("declared_primary_metric", ""))
        task_config = configured.get(task_id, {})
        configured_spread = float(task_config.get("response_surface_spread", math.nan))
        configured_sesoi = float(task_config.get("sesoi", math.nan))
        expected_sesoi = round(max(floor, fraction * source_spread), decimals)
        source_matches = source_matches and math.isclose(
            configured_spread, source_spread, rel_tol=0.0, abs_tol=1.0e-12
        )
        derivation_matches = derivation_matches and math.isclose(
            configured_sesoi, expected_sesoi, rel_tol=0.0, abs_tol=10.0 ** (-decimals)
        )
        metric_matches = metric_matches and task_config.get("primary_metric") == source_metric
        cards[task_id] = {
            "primary_metric": source_metric,
            "response_surface_spread": source_spread,
            "absolute_floor": floor,
            "response_surface_fraction": fraction,
            "sesoi": configured_sesoi,
            "derivation_uses_method_effect": False,
        }
    checks = {
        "sesoi_scope": tuple(configured) == core_tasks,
        "sesoi_source_spreads_match": source_matches,
        "sesoi_derivation_matches": derivation_matches,
        "sesoi_primary_metrics_match": metric_matches,
        "sesoi_excludes_method_effects": config.get("uses_method_effects") is False,
        "sesoi_parameters_valid": math.isfinite(floor)
        and math.isfinite(fraction)
        and 0.0 < floor < 1.0
        and 0.0 < fraction < 1.0
        and decimals >= 1,
    }
    return checks, cards


def _audit_world_allocation(
    protocol: dict[str, Any],
    core_tasks: tuple[str, ...],
    confirmation_seeds: tuple[int, ...],
) -> tuple[dict[str, bool], dict[str, Any]]:
    allocation = protocol.get("world_family_allocation", {})
    splits = {name: allocation.get(name, {}) for name in ("train", "dev", "bench")}
    seed_sets = {name: _split_seeds(payload) for name, payload in splits.items()}
    generalization_seeds = {int(seed) for seed in splits["bench"].get("generalization_seeds", ())}
    cells = {
        name: {
            (str(mode), float(severity))
            for mode, severities in payload.get("cells", {}).items()
            for severity in severities
        }
        for name, payload in splits.items()
    }
    interventions_valid = True
    axes_complete = True
    for task_id in core_tasks:
        axes = axes_for_task(task_id)
        axes_complete = axes_complete and len(axes) == 2
        for axis in axes:
            for split_cells in cells.values():
                for mode, severity in split_cells:
                    try:
                        AxisIntervention.from_dict(
                            {"axis_id": axis.axis_id, "mode": mode, "severity": severity}
                        )
                    except (TypeError, ValueError):
                        interventions_valid = False
    pairwise_cell_disjoint = all(
        not (cells[left] & cells[right])
        for left, right in (("train", "dev"), ("train", "bench"), ("dev", "bench"))
    )
    all_bench_modes = {mode for mode, _ in cells["bench"]} == {
        "interpolation",
        "extrapolation",
        "composition",
        "observation_noise",
    }
    no_train_dev_extrapolation = all(
        mode != "extrapolation" for name in ("train", "dev") for mode, _ in cells[name]
    )
    seed_roles_disjoint = (
        not (seed_sets["train"] & seed_sets["dev"])
        and not (seed_sets["train"] & seed_sets["bench"])
        and not (seed_sets["dev"] & seed_sets["bench"])
        and not (generalization_seeds & seed_sets["train"])
        and not (generalization_seeds & seed_sets["dev"])
        and not (generalization_seeds & seed_sets["bench"])
    )
    checks = {
        "two_axes_per_core_task": axes_complete,
        "world_interventions_valid": interventions_valid,
        "world_cells_pairwise_disjoint": pairwise_cell_disjoint,
        "world_seed_roles_disjoint": seed_roles_disjoint,
        "bench_seeds_match_primary_cohort": seed_sets["bench"] == set(confirmation_seeds),
        "bench_covers_all_shift_modes": all_bench_modes,
        "extrapolation_reserved_for_bench": no_train_dev_extrapolation,
        "bench_axis_identity_hidden": allocation.get("axis_identity_visible_to_agent") is False,
        "bench_finetuning_forbidden": allocation.get("bench_finetuning_allowed") is False,
    }
    summary = {
        "seed_counts": {
            **{name: len(seeds) for name, seeds in seed_sets.items()},
            "bench_generalization": len(generalization_seeds),
        },
        "cell_counts_per_axis": {name: len(value) for name, value in cells.items()},
        "core_axis_count": sum(len(axes_for_task(task_id)) for task_id in core_tasks),
        "train_dev_extrapolation_cells": 0,
        "paired_world_policy": allocation.get("paired_world_policy"),
    }
    return checks, summary


def _split_seeds(payload: dict[str, Any]) -> set[int]:
    bounds = payload.get("base_seeds", {})
    start = int(bounds.get("start", 0))
    stop = int(bounds.get("stop_inclusive", -1))
    return set(range(start, stop + 1)) if stop >= start else set()


def _decision_rule_is_joint(rule: dict[str, Any], *, task_count: int) -> bool:
    constraints = rule.get("constraint_noninferiority", {})
    safety = constraints.get("safety", {})
    cost = constraints.get("cost", {})
    comparison_count = int(constraints.get("comparison_count", 0))
    familywise_alpha = float(constraints.get("familywise_alpha", math.nan))
    expected_quantile = 1.0 - familywise_alpha / comparison_count if comparison_count else math.nan
    return (
        float(rule.get("paired_bootstrap_ci_low_above", math.nan)) == 0.0
        and int(rule.get("deterministic_bootstrap_samples", 0)) >= 5_000
        and float(rule.get("holm_adjusted_alpha", math.nan)) == 0.05
        and rule.get("mean_effect_must_reach_task_sesoi") is True
        and rule.get("objective_safety_and_cost_must_all_pass_per_task") is True
        and constraints.get("simultaneous_method")
        == "bonferroni_percentile_upper_bound"
        and familywise_alpha == 0.05
        and comparison_count == task_count * 2
        and constraints.get("uses_prior_candidate_constraint_effects") is False
        and math.isclose(
            float(constraints.get("upper_quantile", math.nan)),
            expected_quantile,
            rel_tol=0.0,
            abs_tol=1.0e-12,
        )
        and safety.get("metric") == "risk_budget_exceedance_rate"
        and safety.get("effect") == "candidate_minus_comparator_absolute_rate"
        and float(safety.get("maximum_noninferiority_margin", math.nan)) == 0.05
        and safety.get("margin_rationale")
        == "at most two additional exceedances per 40-experiment campaign"
        and cost.get("metric") == "campaign_total_cost_per_complete_experiment"
        and cost.get("effect") == "candidate_minus_comparator_relative_to_comparator"
        and float(cost.get("maximum_noninferiority_margin", math.nan)) == 0.05
        and cost.get("margin_rationale")
        == "task-independent five-percent relative resource tolerance"
        and rule.get("all_runs_must_pass_replay") is True
        and rule.get("failed_runs_are_reported_not_dropped") is True
    )


def _method_implementation_ready(method_cards: object, implementation: str) -> bool:
    if not isinstance(method_cards, dict):
        return False
    matching = [
        card
        for method_id, card in method_cards.items()
        if method_id == implementation
        or (isinstance(card, dict) and card.get("implementation") == implementation)
    ]
    return len(matching) == 1 and matching[0].get("implementation_contract_ready") is True


def _load_report(filename: str) -> dict[str, Any]:
    return json.loads((REPORT_ROOT / filename).read_text(encoding="utf-8"))


def _canonical_sha256(payload: dict[str, Any]) -> str:
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def _file_sha256(path: Path) -> str:
    if path.suffix.lower() == ".json":
        return canonical_json_file_sha256(path)
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json_file_sha256(path: str | Path) -> str:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("canonical evidence JSON must be an object")
    return _canonical_sha256(payload)


__all__ = [
    "CONFIRMATORY_FREEZE_AUDIT_VERSION",
    "CONFIRMATORY_FREEZE_PROTOCOL_VERSION",
    "DEFAULT_CONFIRMATORY_FREEZE_PATH",
    "audit_confirmatory_freeze",
    "canonical_json_file_sha256",
    "load_confirmatory_freeze",
]
