from __future__ import annotations

import copy
import json
import os
from pathlib import Path

from chemworld.agents.task_recipes import task_recipe_event_count
from chemworld.eval.operation_baseline_development import (
    DEFAULT_REPORT_PATH,
    NUMERIC_THREAD_ENV_VARS,
    NUMERIC_THREADS_PER_WORKER,
    _numeric_worker_environment,
    audit_operation_development_plan,
    build_operation_development_cells,
    load_operation_development_plan,
    run_operation_baseline_development_audit,
)
from chemworld.tasks import get_task

FROZEN_REPORT = (
    Path(__file__).resolve().parents[1]
    / "workstreams"
    / "benchmark_v1"
    / "reports"
    / "operation-baselines-dev-v0.4.json"
)


def test_v041_report_namespace_preserves_frozen_v04_history() -> None:
    assert DEFAULT_REPORT_PATH.name == "operation-baselines-dev-v0.4.1.json"
    assert FROZEN_REPORT.is_file()
    assert DEFAULT_REPORT_PATH != FROZEN_REPORT


def test_numeric_worker_environment_is_bounded_and_restored(monkeypatch) -> None:
    for index, name in enumerate(NUMERIC_THREAD_ENV_VARS):
        if index % 2:
            monkeypatch.delenv(name, raising=False)
        else:
            monkeypatch.setenv(name, str(index + 3))
    before = {name: os.environ.get(name) for name in NUMERIC_THREAD_ENV_VARS}

    with _numeric_worker_environment():
        assert all(
            os.environ[name] == str(NUMERIC_THREADS_PER_WORKER)
            for name in NUMERIC_THREAD_ENV_VARS
        )

    assert {name: os.environ.get(name) for name in NUMERIC_THREAD_ENV_VARS} == before


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


def test_frozen_full_operation_report_passes_without_bench_or_reference_feedback() -> None:
    report = json.loads(FROZEN_REPORT.read_text(encoding="utf-8"))

    assert report["status"] == "formal_operation_baselines_ready"
    assert report["formal_operation_baselines_ready"] is True
    assert report["source_tree_clean_at_start"] is True
    assert report["cell_count"] == 288
    assert report["split_scope"] == ["train", "dev"]
    assert report["bench_results_present"] is False
    assert report["reference_search_results_used"] is False
    assert report["acceptance"] == {
        "action_diversity_controls_pass": True,
        "all_accounting_complete": True,
        "all_cells_complete": True,
        "all_checked_replays_deterministic": True,
        "all_decision_audits_complete": True,
        "all_method_controls_pass": True,
        "all_primary_values_complete": True,
        "bench_feedback_used": False,
        "full_preregistered_development_scope": True,
        "nonrandom_invalid_controls_pass": True,
        "operation_random_invalid_actions_retained": True,
        "operation_random_invalid_operation_count": 1563,
        "reference_search_feedback_used": False,
        "rule_measurement_adaptation_controls_pass": True,
        "source_tree_clean_at_start": True,
    }
    summaries = report["method_summaries"]
    assert set(summaries) == {"operation_random", "observation_blind", "rule_based"}
    assert summaries["operation_random"]["invalid_operation_count"] == 1563
    assert summaries["observation_blind"]["invalid_operation_count"] == 0
    assert summaries["rule_based"]["invalid_operation_count"] == 0
    assert all(
        summary["cell_count"] == 96
        and summary["all_cells_complete"]
        and summary["all_primary_values_complete"]
        and summary["all_decision_audits_complete"]
        and summary["deterministic_replay"]
        and summary["accounting_complete"]
        for summary in summaries.values()
    )
    assert all(
        task_summary["measurement_adaptation_count"] > 0
        for task_summary in summaries["rule_based"]["task_summaries"].values()
    )
