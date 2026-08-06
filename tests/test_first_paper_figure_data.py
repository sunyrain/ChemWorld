from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

from scripts.build_first_paper_figure_data import (
    SCHEMA,
    build_figure_data,
    canonical_sha256,
)

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = (
    ROOT / "paper/figures/first-paper-world-instrument-v1" / "first-paper-figure-data-v1.json"
)


def test_committed_figure_data_is_current_bound_and_reproducible() -> None:
    committed = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    assert committed == build_figure_data(ROOT)
    assert committed["schema_version"] == SCHEMA
    declared = committed["figure_data_sha256"]
    unhashed = {key: value for key, value in committed.items() if key != "figure_data_sha256"}
    assert declared == canonical_sha256(unhashed)
    assert len(committed["source_bindings"]) == 5
    assert all(row["sha256"] for row in committed["source_bindings"])


def test_figure_data_preserves_exact_censuses_and_claim_boundaries() -> None:
    data = build_figure_data(ROOT)
    assert data["figure_1"]["reference_counts"] == {
        "reference_tasks": 15,
        "typed_operations": 28,
        "instruments": 5,
        "task_metric_bindings": 62,
    }
    assert len(data["figure_2"]["patterns"]) == 8
    assert data["figure_2"]["generated_composition_count"] == 52
    assert data["figure_2"]["unseen_composition_count"] == 8
    assert data["figure_2"]["new_topology_pattern_count"] == 3
    assert data["figure_2"]["new_topology_case_count"] == 18
    assert data["figure_2"]["aggregate_coverage_denominators"] == {
        "continuous_strata": 212,
        "discrete_levels": 60,
        "discrete_pair_interactions": 180,
        "ordered_operation_interactions": 84,
    }
    pattern_rows = {row["pattern"]: row for row in data["figure_2"]["patterns"]}
    assert {
        pattern for pattern, row in pattern_rows.items() if not row["reference_topology_overlap"]
    } == {
        "phase-observation",
        "phase-separation-observation",
        "reaction-continuous-flow-observation",
    }
    assert pattern_rows["reaction-distillation-observation"]["reference_topology_overlap"]
    assert pattern_rows["reaction-distillation-observation"]["unseen_reference_identity"]
    assert data["figure_3"]["zero_findings"] == {
        "failure_classes": 0,
        "missing_receipts": 0,
        "public_private_leakage": 0,
    }
    assert data["figure_4"]["totals"]["submitted_actions"]["denominator"] == 89
    assert data["figure_4"]["recovery"]["subsequent_commits"] == 18
    assert data["figure_5"]["pair_count"] == 6
    assert data["figure_5"]["trace_count"] == 24
    assert all(data["claim_boundary"].values())


def test_agent_and_endpoint_example_are_not_collapsed_into_one_score() -> None:
    data = build_figure_data(ROOT)["figure_6"]
    agent = data["complete_agent"]
    assert (agent["submitted"], agent["committed"], agent["rolled_back"]) == (15, 15, 0)
    assert agent["provider"] == {
        "sessions": 1,
        "logical_turns": 1,
        "mcp_calls": 17,
        "mcp_steps": 15,
        "input_tokens": 493092,
        "cache_hit_tokens": 440832,
        "cache_miss_tokens": 52260,
        "output_tokens": 2973,
    }
    endpoint = data["endpoint_near_example"]
    assert endpoint["world_seed"] == 1
    assert endpoint["trajectory_replicate_id"] == "r03"
    assert endpoint["raw_terminal_score"] == 0.0025746301991926845
    assert endpoint["best_discovery_fraction"] == 0.39999999999999997
    assert endpoint["online_retention_rate"] == 0.39999999999999997
    assert endpoint["maximum_drawdown"] == -0.3055942146928859
    assert endpoint["terminal_to_best_ratio"] == 0.17283116587037617

    tampered = deepcopy(data)
    tampered["endpoint_near_example"]["raw_terminal_score"] = 1.0
    assert tampered != data
