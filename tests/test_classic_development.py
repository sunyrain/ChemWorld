from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

import chemworld.eval.classic_development as classic_development
from chemworld.eval.classic_development import (
    DEFAULT_CACHE_ROOT,
    DEFAULT_PLAN_PATH,
    DEFAULT_REPORT_PATH,
    NUMERIC_THREAD_ENV_VARS,
    NUMERIC_THREADS_PER_WORKER,
    _numeric_worker_environment,
    audit_classic_development_plan,
    build_development_cells,
    load_classic_development_plan,
    run_classic_development_audit,
)

FROZEN_REPORT = (
    Path(__file__).resolve().parents[1]
    / "workstreams"
    / "benchmark_v1"
    / "reports"
    / "classic-dev-v0.4.json"
)


def test_default_cache_uses_real_git_common_directory_in_worktrees() -> None:
    assert DEFAULT_CACHE_ROOT.parent.name == "chemworld-private"
    assert DEFAULT_CACHE_ROOT.name == "classic-dev-v0.4.1"
    assert DEFAULT_CACHE_ROOT.parent.parent.is_dir()
    assert DEFAULT_REPORT_PATH.name == "classic-dev-v0.4.1.json"
    assert DEFAULT_REPORT_PATH != FROZEN_REPORT


def test_v041_development_plan_freezes_preflight_and_formal_scopes() -> None:
    assert DEFAULT_PLAN_PATH.name == "classic_development_plan.json"
    plan = load_classic_development_plan()
    report = audit_classic_development_plan(plan)

    assert report["plan_ready"] is True
    assert report["bench_access_allowed"] is False
    assert report["reference_search_access_allowed"] is False
    assert plan["preflight_scope"] == {
        "train_seeds": [10_000],
        "dev_seeds": [11_000],
        "complete_experiments_per_cell": 8,
        "expected_cell_count": 64,
        "rationale": (
            "Eight experiments exceed the four-point surrogate warmup and exercise "
            "multiple fit/acquisition updates without selecting methods from this diagnostic."
        ),
    }
    assert plan["formal_scope"]["expected_cell_count"] == 768


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


def test_development_cells_use_only_public_ranges_and_paired_method_rng() -> None:
    cells = build_development_cells(
        tasks=("partition-discovery",),
        methods=("random", "lhs"),
        train_seeds=(10_000,),
        dev_seeds=(11_000,),
        complete_experiments=5,
    )
    assert len(cells) == 4
    for split, seed in (("train", 10_000), ("dev", 11_000)):
        paired = [cell for cell in cells if cell.split == split]
        assert {cell.world_seed for cell in paired} == {seed}
        assert len({cell.method_seed for cell in paired}) == 1
        assert all(cell.world_interventions for cell in paired)
        assert all(cell.world_interventions[0]["mode"] != "extrapolation" for cell in paired)
        assert all(len(cell.formal_protocol_sha256) == 64 for cell in paired)
        assert all(len(cell.method_artifact_sha256) == 64 for cell in paired)
        assert all(len(cell.source_commit) == 40 for cell in paired)


def test_development_audit_is_resumable_deterministic_and_never_formal_when_partial(
    tmp_path,
) -> None:
    kwargs = {
        "tasks": ("partition-discovery",),
        "methods": ("random", "structured_gp_ei"),
        "train_seeds": (10_000,),
        "dev_seeds": (11_000,),
        "complete_experiments": 5,
        "workers": 1,
        "cache_root": tmp_path / "cache",
        "report_path": tmp_path / "report.json",
    }
    first = run_classic_development_audit(**kwargs)
    second = run_classic_development_audit(**kwargs)
    assert first == second
    assert first["formal_classic_matrix_ready"] is False
    assert first["status"] == "development_diagnostic_only"
    assert first["bench_results_present"] is False
    assert first["reference_search_results_used"] is False
    assert first["acceptance"]["all_method_controls_pass"] is True
    assert first["method_summaries"]["structured_gp_ei"]["acquisition_effective"] is True
    assert first["method_summaries"]["random"]["deterministic_replay"] is True
    assert first["source_commit_stable"] is True
    assert first["source_commit"] == first["source_commit_before_report"]
    assert {cell["source_commit"] for cell in first["cells"]} == {
        first["source_commit"]
    }


def test_classic_development_rejects_head_drift_during_cell_issuance(
    monkeypatch,
    tmp_path,
) -> None:
    commits = iter(("a" * 40, "b" * 40))
    monkeypatch.setattr(classic_development, "_git_commit", lambda: next(commits))

    with pytest.raises(RuntimeError, match="source commit changed"):
        run_classic_development_audit(
            tasks=("partition-discovery",),
            methods=("random",),
            train_seeds=(10_000,),
            dev_seeds=(11_000,),
            complete_experiments=5,
            workers=1,
            cache_root=tmp_path / "cache",
            report_path=None,
        )


def test_frozen_full_development_report_passes_without_bench_or_reference_feedback() -> None:
    report = json.loads(FROZEN_REPORT.read_text(encoding="utf-8"))
    assert report["status"] == "formal_classic_matrix_ready"
    assert report["formal_classic_matrix_ready"] is True
    assert report["cell_count"] == 768
    assert report["bench_results_present"] is False
    assert report["reference_search_results_used"] is False
    assert report["acceptance"] == {
        "all_accounting_complete": True,
        "all_cells_complete": True,
        "all_checked_replays_deterministic": True,
        "all_method_controls_pass": True,
        "bench_feedback_used": False,
        "full_preregistered_development_scope": True,
    }
    assert set(report["family_champions"].values()) == {
        "lhs",
        "greedy_local",
        "structured_gp_ucb",
        "structured_safe_gp_ei",
    }
    assert all(
        summary["budget_curve_non_degenerate"]
        and summary["deterministic_replay"]
        and summary["accounting_complete"]
        and summary["invalid_operation_count"] == 0
        for summary in report["method_summaries"].values()
    )
