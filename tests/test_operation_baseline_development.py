from __future__ import annotations

import copy

from chemworld.agents.task_recipes import task_recipe_event_count
from chemworld.eval.operation_baseline_development import (
    audit_operation_development_plan,
    build_operation_development_cells,
    load_operation_development_plan,
    run_operation_baseline_development_audit,
)
from chemworld.tasks import get_task


def test_operation_development_plan_is_public_split_only_and_fail_closed() -> None:
    plan = load_operation_development_plan()
    report = audit_operation_development_plan(plan)
    assert report["plan_ready"] is True
    assert report["bench_access_allowed"] is False
    assert report["reference_search_access_allowed"] is False

    tampered = copy.deepcopy(plan)
    tampered["bench_access_allowed"] = True
    tampered_report = audit_operation_development_plan(tampered)
    assert tampered_report["plan_ready"] is False
    assert "bench_access_guard_invalid" in tampered_report["reasons"]


def test_operation_development_cells_bind_budget_sources_and_paired_rng() -> None:
    cells = build_operation_development_cells(
        tasks=("partition-discovery",),
        train_seeds=(10_000,),
        dev_seeds=(11_000,),
        complete_experiments=2,
    )
    assert len(cells) == 6
    expected_limit = 2 * task_recipe_event_count(get_task("partition-discovery").to_dict()) * 2
    for split, seed in (("train", 10_000), ("dev", 11_000)):
        paired = [cell for cell in cells if cell.split == split]
        assert {cell.world_seed for cell in paired} == {seed}
        assert len({cell.method_seed for cell in paired}) == 1
        assert {cell.operation_limit for cell in paired} == {expected_limit}
        assert all(cell.world_interventions for cell in paired)
        assert all(len(cell.formal_protocol_sha256) == 64 for cell in paired)
        assert all(len(cell.method_freeze_sha256) == 64 for cell in paired)
        assert all(len(cell.development_plan_sha256) == 64 for cell in paired)
        assert all(len(cell.method_artifact_sha256) == 64 for cell in paired)


def test_partial_operation_development_is_resumable_and_never_formal(tmp_path) -> None:
    kwargs = {
        "tasks": ("partition-discovery",),
        "train_seeds": (10_000,),
        "dev_seeds": (11_000,),
        "complete_experiments": 2,
        "workers": 1,
        "cache_root": tmp_path / "cache",
        "report_path": tmp_path / "report.json",
    }
    first = run_operation_baseline_development_audit(**kwargs)
    second = run_operation_baseline_development_audit(**kwargs)

    assert first == second
    assert first["formal_operation_baselines_ready"] is False
    assert first["status"] == "development_diagnostic_only"
    assert first["bench_results_present"] is False
    assert first["reference_search_results_used"] is False
    assert first["cell_count"] == 6
    assert first["acceptance"]["full_preregistered_development_scope"] is False
    assert first["acceptance"]["all_method_controls_pass"] is True
    assert first["acceptance"]["all_checked_replays_deterministic"] is True
    assert first["acceptance"]["nonrandom_invalid_controls_pass"] is True
    assert first["acceptance"]["rule_measurement_adaptation_controls_pass"] is True
    assert first["acceptance"]["operation_random_invalid_actions_retained"] is True
