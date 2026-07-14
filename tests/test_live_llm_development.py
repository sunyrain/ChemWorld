from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

from chemworld.eval.formal_matrix import build_formal_matrix_plan
from chemworld.eval.live_llm_development import (
    DEFAULT_CACHE_ROOT,
    build_live_llm_development_bundle,
    evaluate_live_llm_promotion,
    prepare_live_llm_development,
    run_live_llm_development,
)

ROOT = Path(__file__).resolve().parents[1]


def test_default_private_cache_is_source_commit_scoped() -> None:
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()

    assert DEFAULT_CACHE_ROOT.parent.name == "live-llm-dev-v0.4.8"
    assert DEFAULT_CACHE_ROOT.name == commit


def test_live_pilot_is_exact_paired_core_matrix_without_seed_disclosure() -> None:
    bundle = build_live_llm_development_bundle(stage="live_pilot")
    plan = build_formal_matrix_plan(bundle.manifest)
    serialized = json.dumps(bundle.manifest, sort_keys=True)

    assert bundle.pair_count == 1
    assert bundle.cell_count == 4 * 2 * 3
    assert bundle.maximum_provider_call_count == 2880
    assert len(plan.cells) == bundle.cell_count
    assert set(plan.spectrum_conditions_by_method["live_llm_a"]) == {
        "assigned",
        "unassigned",
        "masked",
    }
    assert bundle.manifest["metadata"]["development_contract"]["bench_accessed"] is False
    assert "10000" not in serialized
    assert all("world_seed" not in cell for cell in bundle.manifest["cells"])
    assert bundle.manifest["metadata"]["matrix_contract"]["operation_limits_by_task"] == {
        "partition-discovery": 40,
        "reaction-to-crystallization": 44,
        "reaction-to-distillation": 44,
        "flow-reaction-optimization": 32,
    }
    protocol_report = json.loads(
        (
            Path(__file__).resolve().parents[1]
            / "workstreams/benchmark_v1/reports/formal-protocol-v0.4.json"
        ).read_text(encoding="utf-8")
    )
    assert {cell["backend_semantic_sha256"] for cell in bundle.manifest["cells"]} == {
        protocol_report["backend_semantic_sha256"]
    }


def test_development_matrix_uses_only_four_public_dev_pairs() -> None:
    bundle = build_live_llm_development_bundle(stage="development_matrix")
    plan = build_formal_matrix_plan(bundle.manifest)

    assert bundle.pair_count == 4
    assert bundle.cell_count == 4 * 2 * 3 * 4
    assert bundle.maximum_provider_call_count == 23040
    assert plan.checkpoints == (1, 2, 4)
    assert plan.limits.api_max_concurrency == 4
    assert plan.limits.matrix_monetary_cost_usd_limit == pytest.approx(bundle.cell_count * 0.35)


def test_candidate_screen_is_small_and_precedes_live_pilot() -> None:
    bundle = build_live_llm_development_bundle(stage="candidate_screen")

    assert bundle.pair_count == 1
    assert bundle.cell_count == 1 * 2 * 3
    assert bundle.maximum_provider_call_count == 396
    assert bundle.manifest["metadata"]["matrix_contract"]["tasks"] == [
        "reaction-to-crystallization",
    ]
    assert bundle.manifest["metadata"]["matrix_contract"]["operation_limits_by_task"] == {
        "reaction-to-crystallization": 22
    }
    assert bundle.manifest["metadata"]["orchestration"][
        "matrix_monetary_cost_usd_limit"
    ] == pytest.approx(2.1)
    assert len(bundle.manifest["metadata"]["development_contract"]["development_plan_sha256"]) == 64


def test_paid_stage_scope_and_seed_set_are_frozen_before_provider_use() -> None:
    with pytest.raises(ValueError, match="task scope is frozen"):
        build_live_llm_development_bundle(stage="candidate_screen", tasks=("partition-discovery",))
    with pytest.raises(ValueError, match="method scope is frozen"):
        build_live_llm_development_bundle(stage="candidate_screen", methods=("live_llm_b",))
    with pytest.raises(ValueError, match="spectrum scope is frozen"):
        build_live_llm_development_bundle(
            stage="candidate_screen", spectrum_conditions=("assigned", "masked")
        )
    with pytest.raises(ValueError, match="seed set is frozen"):
        build_live_llm_development_bundle(stage="candidate_screen", seeds=(10_001,))


def test_promotion_gate_rejects_accounted_but_noncompleting_configuration() -> None:
    def cell(method: str, task: str, *, succeeded: bool) -> dict[str, object]:
        return {
            "method_id": method,
            "task_id": task,
            "status": "succeeded" if succeeded else "failed",
            "replay_verified": succeeded,
            "resource_axes": {
                "complete_experiment_count": 1 if succeeded else 0,
                "input_token_count": 100_000,
                "wall_time_s": 100.0,
            },
        }

    cells = [
        cell(method, task, succeeded=method == "live_llm_b")
        for method in ("live_llm_a", "live_llm_b")
        for task in ("reaction-to-crystallization",)
        for _ in range(3)
    ]
    report = {
        "infrastructure_errors": [],
        "audit": {
            "cells": cells,
            "exact_cartesian_matrix_complete": True,
            "paired_conditions_complete": True,
            "all_required_resource_accounting_complete": True,
            "all_successes_replay_verified": True,
        },
    }

    gate = evaluate_live_llm_promotion(report, stage="candidate_screen")

    assert gate["passed"] is False
    assert gate["decision"] == "reject_or_redesign"
    assert gate["checks"]["minimum_per_method_completion_rate"] is False
    assert gate["checks"]["every_method_has_success"] is False


def test_larger_paid_stage_cannot_bypass_candidate_screen(tmp_path) -> None:
    with pytest.raises(RuntimeError, match="candidate_screen"):
        run_live_llm_development(
            stage="live_pilot",
            cache_root=tmp_path,
            report_path=None,
        )


def test_live_development_rejects_bench_reference_or_partial_spectrum_design() -> None:
    with pytest.raises(ValueError, match="stage must"):
        build_live_llm_development_bundle(stage="bench")
    with pytest.raises(ValueError, match="spectrum scope is frozen"):
        build_live_llm_development_bundle(
            stage="live_pilot", spectrum_conditions=("assigned", "masked")
        )
    with pytest.raises(ValueError, match="outside the public formal range"):
        build_live_llm_development_bundle(stage="development_matrix", seeds=(12_000,))


def test_prepare_writes_private_runtimes_outside_public_report_tree(tmp_path) -> None:
    bundle, manifest_path, runtime_root, output_root = prepare_live_llm_development(
        stage="live_pilot",
        cache_root=tmp_path,
    )

    assert manifest_path.is_file()
    assert runtime_root.is_dir()
    assert len(list(runtime_root.glob("*.json"))) == bundle.cell_count
    assert not output_root.exists()
    runtime = json.loads(next(runtime_root.glob("*.json")).read_text(encoding="utf-8"))
    assert runtime["world_seed"] == 10_000
    assert "world_seed" not in json.loads(manifest_path.read_text(encoding="utf-8"))["cells"][0]
