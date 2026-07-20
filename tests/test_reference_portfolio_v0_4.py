from __future__ import annotations

import copy
import json
from collections import Counter
from pathlib import Path
from typing import Any

import pytest

from chemworld.eval.reference_plan_v0_4 import (
    ReferencePlanError,
    audit_reference_plan,
    build_reference_run_plan,
    load_reference_portfolio_v0_4,
    load_reference_regret_v0_4,
    signed_regret,
)

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "workstreams" / "benchmark_v1" / "reports" / "reference-plan-v0.4.json"


def test_exact_reference_run_plan_has_four_independent_sources_per_target() -> None:
    plan = load_reference_portfolio_v0_4()
    runs = build_reference_run_plan(plan)
    counts = Counter(
        (row["task_id"], row["opaque_pair_index"]) for row in runs
    )
    assert len(runs) == 1600
    assert len(counts) == 400
    assert set(counts.values()) == {4}
    assert len({row["run_id"] for row in runs}) == 1600
    assert len({row["builder_seed"] for row in runs}) == 1600
    assert {row["reference_search_base_seed"] for row in runs} == set(
        range(12000, 12100)
    )
    assert all(row["target_binding"] == "private_bench_manifest_lookup_only" for row in runs)


def test_resource_envelope_matches_task_recipe_plan() -> None:
    plan = load_reference_portfolio_v0_4()
    runs = build_reference_run_plan(plan)
    assert sum(row["complete_experiment_budget"] for row in runs) == 64000
    assert sum(row["maximum_operation_count"] for row in runs) == 656000
    assert plan["run_plan"]["planned_source_metric_record_count"] == 3200
    assert plan["target_grid"]["expected_reference_cell_count"] == 800


def test_reference_controls_are_ready_without_results_or_private_values() -> None:
    plan = load_reference_portfolio_v0_4()
    regret = load_reference_regret_v0_4()
    report = audit_reference_plan(plan, regret)
    assert report["controls_ready"] is True
    assert report["formal_results_present"] is False
    assert report["benchmark_claim_allowed"] is False
    assert report["run_counts"] == {
        "private_pair_count": 100,
        "reference_cell_count": 800,
        "source_run_count": 1600,
        "source_metric_record_count": 3200,
        "complete_experiment_count": 64000,
        "maximum_operation_count": 656000,
    }
    assert report["private_seed_values_reported"] is False
    assert report["private_world_parameters_reported"] is False
    assert all(report["controls"].values())
    assert all(report["adversarial_probes"].values())


def test_reference_is_not_oracle_and_negative_regret_is_preserved() -> None:
    plan = load_reference_portfolio_v0_4()
    regret = load_reference_regret_v0_4()
    assert plan["reference_semantics"]["is_oracle"] is False
    assert plan["reference_semantics"]["evaluated_method_may_exceed_reference"] is True
    assert regret["reference_semantics"]["negative_regret_policy"] == "preserve_and_report"
    assert signed_regret(0.8, 0.9) == pytest.approx(-0.1)


def test_builder_identity_cannot_overlap_evaluated_methods() -> None:
    plan = copy.deepcopy(load_reference_portfolio_v0_4())
    plan["builder_contract"]["builder_id"] = "ppo"
    report = audit_reference_plan(plan, load_reference_regret_v0_4())
    assert report["controls_ready"] is False
    assert report["controls"][
        "reference_builder_identity_code_and_rng_are_independent"
    ] is False


def test_duplicate_or_missing_source_profile_is_rejected() -> None:
    duplicate = copy.deepcopy(load_reference_portfolio_v0_4())
    duplicate["source_profiles"][1]["source_id"] = duplicate["source_profiles"][0][
        "source_id"
    ]
    with pytest.raises(ReferencePlanError, match="four independent"):
        build_reference_run_plan(duplicate)
    missing = copy.deepcopy(load_reference_portfolio_v0_4())
    missing["source_profiles"].pop()
    with pytest.raises(ReferencePlanError, match="four independent"):
        build_reference_run_plan(missing)


@pytest.mark.parametrize(
    ("mutator", "control"),
    [
        (
            lambda plan, regret: plan["target_grid"].update(
                {"private_bench_pair_count": 20}
            ),
            "target_grid_binds_private_core4_without_seed_exposure",
        ),
        (
            lambda plan, regret: plan["run_plan"].update(
                {"planned_source_run_count": 800}
            ),
            "resource_plan_matches_executable_task_recipes",
        ),
        (
            lambda plan, regret: plan["evidence_contract"].update(
                {"formal_reference_results_present_now": True}
            ),
            "evidence_requires_four_replayed_accounted_sources_before_scoring",
        ),
        (
            lambda plan, regret: regret["reference_semantics"].update(
                {"negative_regret_policy": "clip_to_zero"}
            ),
            "regret_protocol_matches_portfolio_and_preserves_negative_regret",
        ),
        (
            lambda plan, regret: plan["parent_bindings"]["statistical_plan"].update(
                {"protocol_sha256": "a" * 64}
            ),
            "formal_and_statistical_parents_are_hash_bound",
        ),
    ],
)
def test_reference_plan_tampering_fails_closed(mutator: Any, control: str) -> None:
    plan = copy.deepcopy(load_reference_portfolio_v0_4())
    regret = copy.deepcopy(load_reference_regret_v0_4())
    mutator(plan, regret)
    report = audit_reference_plan(plan, regret)
    assert report["controls_ready"] is False
    assert report["controls"][control] is False


def test_checked_in_reference_plan_report_is_ready_but_evidence_absent() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    assert report["controls_ready"] is True
    assert report["status"] == "reference_plan_frozen_evidence_not_generated"
    assert report["formal_results_present"] is False
    assert report["benchmark_claim_allowed"] is False
    assert report["controls"]["formal_and_statistical_parents_are_hash_bound"] is True
    assert report["controls"]["resource_plan_matches_executable_task_recipes"] is True
    assert report["run_counts"]["source_run_count"] == 1600
    assert report["run_counts"]["reference_cell_count"] == 800
    assert report["minimum_sources_per_task_pair_metric"] == 4
    assert report["reference_semantics"]["is_oracle"] is False
