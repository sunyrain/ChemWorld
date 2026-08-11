from __future__ import annotations

import math
from collections import Counter
from pathlib import Path
from typing import Any

import numpy as np
from scripts.run_work_ii_mechanism_oracle_qualification import (
    ROOT,
    InMemoryMechanismEvaluator,
    _load,
    _q1_coordinate_schema,
    _run_optimizer,
)
from scripts.run_work_ii_q1_response_surface import TASK_SPECS

from chemworld.eval.work_ii_mechanism_oracle_qualification import (
    EXPECTED_OPTIMIZER_REQUESTS,
    FULL_PERTURBATION_COUNT,
    INITIAL_POPULATION_SIZE,
    OPTIMIZER_GENERATIONS,
    TARGET_GRID_SIDE,
    VALIDATION_EXECUTION_COUNT,
    analyze_mechanism_oracle_world,
    balanced_initial_population,
    full_dimensional_perturbations,
    local_target_grid,
    select_validation_candidates,
)

TASK_ID = "reaction-safety-constrained"


def test_balanced_population_and_local_design_cover_frozen_contract() -> None:
    schema = _q1_coordinate_schema(TASK_ID)
    population = balanced_initial_population(TASK_ID, 0, schema)
    assert len(population) == INITIAL_POPULATION_SIZE
    assert all(len(vector) == len(schema) for vector in population)
    assert all(0.0 <= value <= 1.0 for vector in population for value in vector)

    category_pairs = Counter((int(vector[4] * 4), int(vector[6] * 4)) for vector in population)
    assert len(category_pairs) == 16
    assert set(category_pairs.values()) == {8}

    optimum = population[0]
    grid = local_target_grid(optimum, (0, 1))
    perturbations = full_dimensional_perturbations(TASK_ID, 0, optimum, schema)
    assert len(grid) == TARGET_GRID_SIDE**2
    assert {(row["grid_i"], row["grid_j"]) for row in grid} == {
        (i, j) for i in range(TARGET_GRID_SIDE) for j in range(TARGET_GRID_SIDE)
    }
    assert len(perturbations) == FULL_PERTURBATION_COUNT
    assert all(vector[4] == optimum[4] for vector in perturbations)
    assert all(vector[6] == optimum[6] for vector in perturbations)


def test_validation_candidate_selection_enforces_separation() -> None:
    rows = []
    for index in range(20):
        rows.append(
            {
                "evaluation_id": f"m{index:03d}",
                "status": "completed",
                "safe": True,
                "score": 1.0 - 0.01 * index,
                "safety_risk": 0.1,
                "vector": [0.1 * index, 0.0],
            }
        )
    selected = select_validation_candidates(rows, count=8, minimum_distance=0.15)
    assert len(selected) == 8
    for left_index, left in enumerate(selected):
        for right in selected[left_index + 1 :]:
            distance = np.linalg.norm(
                np.asarray(left["vector"], dtype=float) - np.asarray(right["vector"], dtype=float)
            )
            assert distance >= 0.15


def _synthetic_mechanism_rows() -> list[dict[str, Any]]:
    rows = []
    for index in range(100):
        fraction = index / 99.0
        rows.append(
            {
                "evaluation_id": f"m{index + 1:06d}",
                "status": "completed",
                "safe": True,
                "score": 0.20 + 0.60 * fraction,
                "safety_risk": 0.32 if index < 10 else 0.10,
                "vector": [fraction, 0.5],
                "metrics": {"yield": 0.10 + 0.80 * fraction},
            }
        )
    return rows


def _synthetic_target_grid() -> list[dict[str, Any]]:
    rows = []
    for i_value in range(TARGET_GRID_SIDE):
        for j_value in range(TARGET_GRID_SIDE):
            x_value = (i_value - 4) / 4.0
            y_value = (j_value - 4) / 4.0
            score = 0.80 - 0.08 * x_value**2 - 0.08 * y_value**2 + 0.04 * x_value
            rows.append(
                {
                    "status": "completed",
                    "safe": True,
                    "score": score,
                    "safety_risk": 0.10,
                    "vector": [0.34 + 0.04 * i_value, 0.34 + 0.04 * j_value],
                    "grid_i": i_value,
                    "grid_j": j_value,
                }
            )
    return rows


def _synthetic_validation_rows() -> list[dict[str, Any]]:
    rows = []
    for candidate_rank in range(1, 9):
        center = 0.80 - 0.01 * (candidate_rank - 1)
        for replicate, offset in enumerate((-0.005, 0.0, 0.005), start=1):
            rows.append(
                {
                    "candidate_rank": candidate_rank,
                    "replicate": replicate,
                    "status": "completed",
                    "score": center + offset,
                    "exact_replay": {"verified": True},
                }
            )
    return rows


def test_synthetic_relative_oracle_surface_passes_all_frozen_gates() -> None:
    report = analyze_mechanism_oracle_world(
        _synthetic_mechanism_rows(),
        _synthetic_target_grid(),
        _synthetic_validation_rows(),
        optimizer_request_count=EXPECTED_OPTIMIZER_REQUESTS,
        optimizer_generation_count=OPTIMIZER_GENERATIONS,
        task_threshold=0.70,
        safety_limit=0.35,
        primary_metric="yield",
        target_indices=(0, 1),
        require_safety_frontier=True,
    )
    assert report["passed"] is True
    assert all(report["checks"].values())
    assert report["observed_validation_exact_replay_count"] == VALIDATION_EXECUTION_COUNT
    assert report["historical_threshold_reaching_count"] > 0


def test_relative_oracle_gate_rejects_nonreplayable_flat_surface() -> None:
    mechanism_rows = _synthetic_mechanism_rows()
    for row in mechanism_rows:
        row["score"] = 0.5
        row["metrics"]["yield"] = 0.5
        row["safety_risk"] = 0.1
    target_rows = _synthetic_target_grid()
    for row in target_rows:
        row["score"] = 0.5
    validation_rows = _synthetic_validation_rows()
    validation_rows[0]["exact_replay"] = {"verified": False}
    report = analyze_mechanism_oracle_world(
        mechanism_rows,
        target_rows,
        validation_rows,
        optimizer_request_count=EXPECTED_OPTIMIZER_REQUESTS - 1,
        optimizer_generation_count=OPTIMIZER_GENERATIONS - 1,
        task_threshold=0.70,
        safety_limit=0.35,
        primary_metric="yield",
        target_indices=(0, 1),
        require_safety_frontier=True,
    )
    assert report["passed"] is False
    assert report["checks"]["optimizer_requests_complete"] is False
    assert report["checks"]["all_observed_validation_exact_replay"] is False
    assert report["checks"]["safe_dynamic_range"] is False
    assert report["checks"]["local_law_identifiable"] is False
    assert report["checks"]["safety_frontier_coverage"] is False


def test_optimizer_attempts_all_frozen_generations() -> None:
    class SyntheticEvaluator:
        def evaluate(
            self,
            vector: list[float] | np.ndarray,
            *,
            phase: str,
        ) -> dict[str, Any]:
            values = np.asarray(vector, dtype=float)
            return {
                "status": "completed",
                "safe": True,
                "score": float(1.0 - np.mean((values - 0.5) ** 2)),
                "safety_risk": 0.1,
                "phase": phase,
            }

    schema = [
        {"coordinate": 0, "control_id": "x", "kind": "linear"},
        {"coordinate": 1, "control_id": "y", "kind": "linear"},
    ]
    initial = balanced_initial_population(TASK_ID, 0, schema)
    report = _run_optimizer(
        SyntheticEvaluator(),  # type: ignore[arg-type]
        task_id=TASK_ID,
        world_seed=0,
        schema=schema,
        initial_population=initial,
    )
    assert report["request_count"] == EXPECTED_OPTIMIZER_REQUESTS
    assert report["generation_count"] == OPTIMIZER_GENERATIONS


def test_reaction_mechanism_evaluator_completes_low_mid_high_recipes() -> None:
    spec = TASK_SPECS[TASK_ID]
    config_path = Path(ROOT, str(spec["config"]))
    evaluator = InMemoryMechanismEvaluator(
        task_id=TASK_ID,
        config=_load(config_path),
        spec=spec,
        world_seed=0,
    )
    try:
        rows = [
            evaluator.evaluate(vector, phase="direct_test")
            for vector in (
                [0.05] * 8,
                [0.50] * 8,
                [0.95] * 8,
            )
        ]
    finally:
        evaluator.close()
    assert all(row["status"] == "completed" for row in rows)
    assert all(math.isfinite(float(row["score"])) for row in rows)
    assert all(math.isfinite(float(row["safety_risk"])) for row in rows)
    assert all(set(row["metrics"]) == set(spec["metrics"]) for row in rows)
    forbidden = {"species", "rate_constants", "mechanism", "hidden"}
    assert all(not forbidden.intersection(row) for row in rows)


def test_reaction_mechanism_evaluator_retains_dynamic_constitution_failure() -> None:
    spec = TASK_SPECS[TASK_ID]
    config_path = Path(ROOT, str(spec["config"]))
    evaluator = InMemoryMechanismEvaluator(
        task_id=TASK_ID,
        config=_load(config_path),
        spec=spec,
        world_seed=0,
    )
    try:
        row = evaluator.evaluate(
            [
                0.936209324747324,
                0.024569489061832428,
                0.8398885484784842,
                0.207385815680027,
                0.7181448694318533,
                0.25351104512810707,
                0.24715753830969334,
                0.08105175383388996,
            ],
            phase="physical_failure_test",
        )
    finally:
        evaluator.close()
    assert row["status"] == "physical_failure"
    assert row["failure"] is None
    assert row["physical_failure"]["rollback_reason"] == "constitution_failed"
    assert row["physical_failure"]["failed_checks"] == ["vessel_temperature_bound"]
    assert evaluator.failure_count == 0
    assert evaluator.physical_failure_count == 1
