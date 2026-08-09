from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

from chemworld.eval.work_ii_formal import (
    FORMAL_ARMS,
    FORMAL_SNAPSHOT_STAGES,
    build_checkpoint_contract,
    build_formal_preflight,
    validate_formal_preflight,
)

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "configs/benchmark/work_ii_formal_design_v0.1.json"
ANALYSIS = ROOT / "configs/benchmark/work_ii_analysis_plan_v0.1.json"


def test_formal_preflight_materializes_exact_outcome_blind_denominators() -> None:
    report = build_formal_preflight(ROOT, DESIGN, ANALYSIS)

    assert report["status"] == "passed_execution_blocked"
    assert report["formal_result"] is False
    assert report["formal_execution_allowed"] is False
    assert report["errors"] == []
    assert validate_formal_preflight(report) == []
    assert report["expected_counts"] == {
        "tasks": 5,
        "independent_task_world_clusters": 25,
        "participant_cells": 75,
        "provider_sessions": 75,
        "provider_repeats_per_cell": 1,
        "complete_experiments": 300,
        "belief_checkpoints": 300,
        "checkpoint_held_out_queries": 1200,
        "checkpoint_held_out_query_metrics": 4080,
        "blind_final_recommendations": None,
    }
    assert len(report["blocking_requirements"]) == 5


def test_formal_schedule_is_task_world_arm_ordered_and_unique() -> None:
    report = build_formal_preflight(ROOT, DESIGN, ANALYSIS)
    cells = report["cells"]

    assert [cell["prior_arm"] for cell in cells[:3]] == list(FORMAL_ARMS)
    assert {cell["world_cluster_id"] for cell in cells[:3]} == {
        "work-ii-public-01-01"
    }
    assert cells[0]["world_seed"] == 672326802
    assert cells[-1]["world_seed"] == 930008953
    assert len({cell["cell_id"] for cell in cells}) == 75
    assert len({cell["cell_key_sha256"] for cell in cells}) == 75
    assert all(cell["provider_session_limit"] == 1 for cell in cells)
    assert all(
        cell["terminal_states"] == ["completed", "right_censored", "failed"]
        for cell in cells
    )
    assert not any("private" in cell for cell in cells)


def test_all_formal_task_configs_use_neutral_checkpoint_ids() -> None:
    report = build_formal_preflight(ROOT, DESIGN, ANALYSIS)
    for binding in report["task_bindings"]:
        config_path = ROOT / binding["campaign_config"]["path"]
        config = json.loads(config_path.read_text(encoding="utf-8"))
        contract = build_checkpoint_contract(config, "opaque")
        assert tuple(contract["snapshot_stages"]) == FORMAL_SNAPSHOT_STAGES
        assert contract["physical_experiment_selection_authority"] == "participant"


def test_formal_preflight_self_hash_fails_closed() -> None:
    report = build_formal_preflight(ROOT, DESIGN, ANALYSIS)
    tampered = deepcopy(report)
    tampered["cells"][0]["world_seed"] += 1
    assert "formal preflight self-hash mismatch" in validate_formal_preflight(tampered)
