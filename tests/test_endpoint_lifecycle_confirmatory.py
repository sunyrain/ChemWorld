from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

import numpy as np
import pytest
from scripts import run_g2_trajectory_replication as runner

from chemworld.eval.endpoint_lifecycle_confirmatory import (
    fit_random_intercept_reml,
    leave_one_world_out_r_squared,
    profile_lower_bound,
)
from chemworld.eval.provenance import canonical_json_sha256

CONFIG = Path("configs/benchmark/g2_endpoint_lifecycle_confirmatory_v0.6.json")


def _synthetic_rows(*, residual_sigma: float) -> list[dict[str, Any]]:
    rng = np.random.default_rng(42)
    rows: list[dict[str, Any]] = []
    for world in range(16):
        world_effect = rng.normal(0.0, 0.08)
        for replicate in range(5):
            endpoint = rng.normal(0.0, 0.12)
            lifecycle = 0.05 + 0.15 * endpoint + world_effect + rng.normal(0.0, residual_sigma)
            rows.append(
                {
                    "world_seed": world,
                    "schedule_time_block": replicate + 1,
                    "nominal_minus_opaque": {
                        "best_final_score": endpoint,
                        "terminal_to_global_best_ratio": lifecycle,
                    },
                }
            )
    return rows


def test_confirmatory_protocol_is_outcome_blind_complete_and_balanced() -> None:
    protocol = runner._load_protocol(CONFIG.resolve())
    cells = runner._scheduled_cells(protocol)

    assert protocol["claim_policy"]["confirmatory"] is True
    assert protocol["confirmatory_freeze"]["interim_score_inspection"] is False
    assert protocol["confirmatory_freeze"]["outcome_dependent_expansion"] is False
    assert len(protocol["task"]["world_seeds"]) == 16
    assert set(protocol["task"]["world_seeds"]).isdisjoint(range(10))
    assert len(cells) == 160
    assert len({cell["cell_id"] for cell in cells}) == 160
    assert len({(cell["world_seed"], cell["trajectory_replicate_id"]) for cell in cells}) == 80
    first = Counter(cell["condition_id"] for cell in cells if cell["within_pair_order"] == 1)
    assert first == Counter({"anonymous_nominal_properties": 40, "opaque_codes": 40})
    for world in protocol["task"]["world_seeds"]:
        world_first = Counter(
            cell["condition_id"]
            for cell in cells
            if cell["world_seed"] == world and cell["within_pair_order"] == 1
        )
        assert sorted(world_first.values()) == [2, 3]
    assert all(
        len(
            {
                cell["schedule_time_block"]
                for cell in cells
                if cell["trajectory_replicate_id"] == replicate
            }
        )
        == 1
        for replicate in ("r01", "r02", "r03", "r04", "r05")
    )


def test_confirmatory_freeze_files_are_byte_bound() -> None:
    raw = json.loads(CONFIG.read_text(encoding="utf-8"))
    for key in (
        "qualification_report",
        "full_schedule",
        "analysis_plan",
        "power_report",
    ):
        binding = raw["confirmatory_freeze"][key]
        path = Path(binding["path"])
        import hashlib

        assert hashlib.sha256(path.read_bytes()).hexdigest() == binding["sha256"]
    schedule = json.loads(
        Path(raw["confirmatory_freeze"]["full_schedule"]["path"]).read_text(encoding="utf-8")
    )
    unhashed = dict(schedule)
    declared = unhashed.pop("schedule_sha256")
    assert declared == canonical_json_sha256(unhashed)


def test_reml_recovers_material_unexplained_lifecycle_variation() -> None:
    rows = _synthetic_rows(residual_sigma=0.26)
    fit = fit_random_intercept_reml(rows)
    lower = profile_lower_bound(fit)

    assert fit["n_pairs"] == 80
    assert fit["world_count"] == 16
    assert fit["sigma_unexplained"] == pytest.approx(0.24439, rel=0.02)
    assert lower > 0.15
    assert np.isfinite(leave_one_world_out_r_squared(rows))


def test_reml_does_not_clear_margin_for_small_residual_variation() -> None:
    rows = _synthetic_rows(residual_sigma=0.08)
    fit = fit_random_intercept_reml(rows)

    assert fit["sigma_unexplained"] < 0.15
    assert profile_lower_bound(fit) < 0.15


def test_confirmatory_pair_batches_preserve_time_block_barrier() -> None:
    protocol = runner._load_protocol(CONFIG.resolve())
    cells = runner._scheduled_cells(protocol)
    states = [{"cell": cell, "state": "pending"} for cell in cells]

    batch = runner._next_pair_batch(states, maximum_pairs=4)
    assert len(batch) == 4
    assert all(len(pair) == 2 for pair in batch)
    assert {cell["schedule_time_block"] for pair in batch for cell in pair} == {1}

    first_block_ids = {cell["cell_id"] for cell in cells if cell["schedule_time_block"] == 1}
    advanced = [
        {
            "cell": state["cell"],
            "state": ("completed" if state["cell"]["cell_id"] in first_block_ids else "pending"),
        }
        for state in states
    ]
    next_batch = runner._next_pair_batch(advanced, maximum_pairs=4)
    assert {cell["schedule_time_block"] for pair in next_batch for cell in pair} == {2}
