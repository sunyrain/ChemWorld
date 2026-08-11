from __future__ import annotations

import json
import math
from typing import Any

import pytest

from scripts.run_work_ii_q1_response_surface import ROOT, TASK_SPECS, _load, _q0_audit
from chemworld.eval.work_ii_response_surface_qualification import (
    ADAPTIVE_RECIPE_COUNT,
    BROAD_RECIPE_COUNT,
    TOTAL_RECIPE_COUNT,
    analyze_q1_world,
    broad_sobol_design,
    build_adaptive_design,
    select_adaptive_anchors,
)


@pytest.mark.parametrize("task_id", sorted(TASK_SPECS))
def test_q0_audit_passes_and_is_json_serializable(task_id: str) -> None:
    spec = TASK_SPECS[task_id]
    config = _load((ROOT / spec["config"]).resolve())
    audit = _q0_audit(task_id, config, spec)

    assert audit["passed"] is True
    json.dumps(audit, ensure_ascii=False, allow_nan=False, sort_keys=True)


def _synthetic_metrics(vector: list[float]) -> tuple[float, float]:
    x_value, y_value, context = vector[0], vector[1], vector[2]
    score = 0.55 + 0.58 * (2.0 * context - 1.0) * math.sin(
        2.0 * math.pi * x_value
    )
    score += 0.18 * math.cos(2.0 * math.pi * y_value)
    score = min(max(score, 0.02), 0.95)
    safety = 0.25 + 0.30 * x_value
    return score, safety


def _row(
    recipe_id: str,
    vector: list[float],
    *,
    phase: str,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    score, safety = _synthetic_metrics(vector)
    row = {
        "recipe_id": recipe_id,
        "phase": phase,
        "vector": vector,
        "status": "completed",
        "score": score,
        "safety_risk": safety,
        "metrics": {"score": score, "yield": score, "safety_risk": safety},
        "exact_replay": {"verified": True},
    }
    if extra:
        row.update(extra)
    return row


def test_broad_and_adaptive_designs_are_deterministic_and_exact_size() -> None:
    first = broad_sobol_design("synthetic-task", 3, 7)
    second = broad_sobol_design("synthetic-task", 3, 7)
    assert first == second
    assert len(first) == BROAD_RECIPE_COUNT
    assert all(len(vector) == 7 for vector in first)

    schema = [
        {"coordinate": index, "control_id": f"x{index}", "kind": "linear"}
        for index in range(7)
    ]
    broad_rows = [
        _row(f"b{index:04d}", vector, phase="broad")
        for index, vector in enumerate(first, start=1)
    ]
    anchors = select_adaptive_anchors(
        broad_rows,
        schema=schema,
        target_indices=(0, 1),
        task_threshold=0.40,
        safety_limit=0.35,
    )
    adaptive = build_adaptive_design(anchors, target_indices=(0, 1))
    assert len(anchors) == 28
    assert len(adaptive) == ADAPTIVE_RECIPE_COUNT
    assert BROAD_RECIPE_COUNT + len(adaptive) == TOTAL_RECIPE_COUNT
    assert sum(item["phase"] == "local_refinement" for item in adaptive) == 112
    assert sum(item["phase"] == "noise_repeat" for item in adaptive) == 16


def test_synthetic_surface_passes_all_frozen_q1_gates() -> None:
    schema = [
        {"coordinate": index, "control_id": f"x{index}", "kind": "linear"}
        for index in range(7)
    ]
    vectors = broad_sobol_design("synthetic-pass", 0, 7)
    broad_rows = [
        _row(f"b{index:04d}", vector, phase="broad")
        for index, vector in enumerate(vectors, start=1)
    ]
    anchors = select_adaptive_anchors(
        broad_rows,
        schema=schema,
        target_indices=(0, 1),
        task_threshold=0.40,
        safety_limit=0.35,
    )
    designs = build_adaptive_design(anchors, target_indices=(0, 1))
    adaptive_rows = [
        _row(
            f"a{index:04d}",
            list(design["vector"]),
            phase=str(design["phase"]),
            extra={
                key: value
                for key, value in design.items()
                if key not in {"phase", "vector"}
            },
        )
        for index, design in enumerate(designs, start=1)
    ]
    report = analyze_q1_world(
        broad_rows,
        adaptive_rows,
        target_indices=(0, 1),
        task_threshold=0.40,
        safety_limit=0.35,
        primary_metric="yield",
        require_safety_frontier=True,
    )
    assert report["completed_recipe_count"] == 512
    assert report["exact_replay_count"] == 512
    assert report["passed"] is True, report["checks"]


def test_q1_rejects_a_saturated_unreachable_surface() -> None:
    vectors = broad_sobol_design("synthetic-fail", 0, 7)
    broad_rows = []
    for index, vector in enumerate(vectors, start=1):
        broad_rows.append(
            {
                "recipe_id": f"b{index:04d}",
                "phase": "broad",
                "vector": vector,
                "status": "completed",
                "score": 0.0,
                "safety_risk": 0.05,
                "metrics": {"score": 0.0, "yield": 0.0, "safety_risk": 0.05},
                "exact_replay": {"verified": True},
            }
        )
    adaptive_rows = [
        {
            "recipe_id": f"a{index:04d}",
            "phase": "adaptive_unavailable",
            "vector": [0.5] * 7,
            "status": "failed",
            "score": None,
            "safety_risk": None,
            "metrics": None,
            "exact_replay": None,
        }
        for index in range(1, ADAPTIVE_RECIPE_COUNT + 1)
    ]
    report = analyze_q1_world(
        broad_rows,
        adaptive_rows,
        target_indices=(0, 1),
        task_threshold=0.70,
        safety_limit=0.35,
        primary_metric="yield",
        require_safety_frontier=True,
    )
    assert report["passed"] is False
    assert report["checks"]["absolute_reachability"] is False
    assert report["checks"]["floor_not_saturated"] is False
    assert report["checks"]["all_512_completed"] is False
