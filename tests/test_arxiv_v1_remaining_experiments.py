from __future__ import annotations

import json
from pathlib import Path

from scripts.audit_arxiv_v1_remaining_experiments import (
    audit_remaining_experiments,
)


def _trajectory(path: Path, *, starts: int, finals: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "agent_view": {
            "tool_json": {
                "campaign_state": {
                    "final_assay_count": finals,
                    "discarded_batches": [],
                    "campaign_resources": {
                        "state": {"vessel_starts": starts},
                    },
                }
            }
        }
    }
    path.write_text(json.dumps(payload) + "\n", encoding="utf-8")


def test_remaining_audit_separates_opportunities_starts_and_final_assays(
    tmp_path: Path,
) -> None:
    cells = []
    cell_number = 0
    for world_seed in (1, 3):
        for replicate_number in range(1, 6):
            for condition in (
                "opaque_codes",
                "anonymous_nominal_properties",
            ):
                cell_number += 1
                cell_id = f"cell-{cell_number:03d}"
                state = "pending"
                authoritative = None
                if cell_number == 1:
                    state = "right_censored"
                    authoritative = f"{cell_id}/attempt-01"
                    _trajectory(
                        tmp_path / authoritative / "trajectory.jsonl",
                        starts=3,
                        finals=2,
                    )
                elif cell_number == 2:
                    state = "completed"
                    authoritative = f"{cell_id}/attempt-01"
                    _trajectory(
                        tmp_path / authoritative / "trajectory.jsonl",
                        starts=6,
                        finals=6,
                    )
                cells.append(
                    {
                        "cell": {
                            "cell_id": cell_id,
                            "world_seed": world_seed,
                            "trajectory_replicate_id": f"r{replicate_number:02d}",
                            "condition_id": condition,
                        },
                        "state": state,
                        "authoritative_attempt_dir": authoritative,
                    }
                )
    manifest = {
        "planned_physical_experiment_count": 120,
        "cells": cells,
    }
    manifest_path = tmp_path / "matrix_manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    report = audit_remaining_experiments(manifest_path)
    formal = report["formal_terminal_accounting"]
    bounds = report["final_count_bounds_if_all_unresolved_slots_complete"]

    assert formal["completed_cells"] == 1
    assert formal["right_censored_cells"] == 1
    assert formal["cells_still_to_terminalize"] == 18
    assert formal["vessel_opportunity_slots_still_to_resolve"] == 108
    assert formal["executed_vessels_in_terminal_cells"] == 9
    assert formal["completed_final_assays_in_terminal_cells"] == 8
    assert formal["started_right_censored_vessels_in_terminal_cells"] == 1
    assert formal["unstarted_slots_lost_to_terminal_cell_censoring"] == 3
    assert bounds["maximum_g2_v0_5_executed_vessels"] == 117
    assert bounds["maximum_g2_v0_5_completed_final_assays"] == 116
    assert bounds["planned_opportunity_denominator"] == 29_760
    assert report["paired_analysis_capacity"]["right_censored_pairs"] == 1
    assert report["paired_analysis_capacity"][
        "maximum_possible_completed_pairs"
    ] == 9
