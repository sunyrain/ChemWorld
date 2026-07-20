"""Shared helpers for the serious-task demonstration notebooks.

The helpers deliberately consume only the public task contract and public
observations.  Mechanism-family interventions are supplied by teacher/demo
code to create paired worlds; their identity is never read from an agent view.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any

import gymnasium as gym
import numpy as np
import pandas as pd

import chemworld  # noqa: F401 - registers the Gymnasium environment
from chemworld.agents.task_recipes import (
    task_recipe_dimension,
    task_recipe_from_unit_vector,
)
from chemworld.tasks import get_task


@dataclass(frozen=True)
class DemoRun:
    """Public evidence retained from one complete candidate experiment."""

    task_id: str
    seed: int
    search_vector: tuple[float, ...]
    recipe: tuple[dict[str, Any], ...]
    trace: pd.DataFrame
    metrics: dict[str, float | None]
    final_info: dict[str, Any]


def task_card(task_id: str) -> dict[str, Any]:
    """Return the versioned public task card used by a demo."""

    return get_task(task_id).to_card()


def standard_probe_vectors(task_id: str) -> dict[str, np.ndarray]:
    """Return three deterministic, task-shaped candidate interventions."""

    dimension = task_recipe_dimension(get_task(task_id).to_dict())
    return {
        "low": np.full(dimension, 0.20, dtype=float),
        "mid": np.full(dimension, 0.50, dtype=float),
        "high": np.full(dimension, 0.80, dtype=float),
    }


def recipe_frame(task_id: str, vector: Sequence[float]) -> pd.DataFrame:
    """Compile a normalized vector through the public task recipe adapter."""

    task = get_task(task_id)
    recipe = task_recipe_from_unit_vector(task.to_dict(), np.asarray(vector, dtype=float))
    return pd.DataFrame(
        [
            {"step": index, "operation": action["operation"], "payload": action}
            for index, action in enumerate(recipe["steps"], start=1)
        ]
    )


def run_vector(
    task_id: str,
    vector: Sequence[float],
    *,
    seed: int = 0,
    world_interventions: Sequence[Mapping[str, Any]] = (),
) -> DemoRun:
    """Execute one task-aware recipe and retain public observations only."""

    task = get_task(task_id)
    values = np.asarray(vector, dtype=float).reshape(-1)
    recipe_payload = task_recipe_from_unit_vector(task.to_dict(), values)
    recipe = tuple(dict(action) for action in recipe_payload["steps"])
    kwargs = task.env_kwargs(seed=seed)
    if world_interventions:
        kwargs["world_interventions"] = [dict(item) for item in world_interventions]
    env = gym.make(task.env_id, **kwargs)
    rows: list[dict[str, Any]] = []
    final_info: dict[str, Any] = {}
    try:
        env.reset(seed=seed)
        for step, action in enumerate(recipe, start=1):
            validation = env.unwrapped.validate_action(action)
            _observation, reward, terminated, truncated, info = env.step(action)
            final_info = dict(info)
            estimates = info.get("processed_estimate", {})
            rows.append(
                {
                    "step": step,
                    "operation": action["operation"],
                    "valid_before_step": bool(validation["valid"]),
                    "transaction_status": info.get("transaction_status"),
                    "reward": float(reward),
                    "leaderboard_score": info.get("leaderboard_score"),
                    "observed_keys": ", ".join(info.get("observed_keys", ())),
                    "processed_estimate": dict(estimates)
                    if isinstance(estimates, dict)
                    else {},
                    "precondition_failed": bool(
                        info.get("constraint_flags", {}).get("precondition_failed", False)
                    ),
                    "terminated": bool(terminated),
                    "truncated": bool(truncated),
                }
            )
            if terminated or truncated:
                break
    finally:
        env.close()

    estimates = final_info.get("processed_estimate", {})
    if not isinstance(estimates, dict):
        estimates = {}
    metrics: dict[str, float | None] = {
        metric: _optional_float(estimates.get(metric)) for metric in task.success_metrics
    }
    metrics["leaderboard_score"] = _optional_float(final_info.get("leaderboard_score"))
    metrics["cost"] = _optional_float(final_info.get("cost"))
    metrics["safety_risk"] = _optional_float(
        estimates.get("safety_risk", final_info.get("safety_risk"))
    )
    return DemoRun(
        task_id=task_id,
        seed=seed,
        search_vector=tuple(float(value) for value in values),
        recipe=recipe,
        trace=pd.DataFrame(rows),
        metrics=metrics,
        final_info=final_info,
    )


def compare_vectors(
    task_id: str,
    vectors: Mapping[str, Sequence[float]],
    *,
    seed: int = 0,
    world_interventions: Sequence[Mapping[str, Any]] = (),
) -> pd.DataFrame:
    """Compare public final feedback from several candidate interventions."""

    rows: list[dict[str, Any]] = []
    for label, vector in vectors.items():
        run = run_vector(
            task_id,
            vector,
            seed=seed,
            world_interventions=world_interventions,
        )
        rows.append(
            {
                "candidate": label,
                **run.metrics,
                "all_actions_valid": bool(run.trace["valid_before_step"].all()),
                "operation_count": len(run.trace),
            }
        )
    return pd.DataFrame(rows)


def compare_hidden_worlds(
    task_id: str,
    vector: Sequence[float],
    *,
    mechanism_mode: str,
    seed: int = 0,
    severity: float = 0.8,
) -> pd.DataFrame:
    """Run one public intervention in two opaque worlds.

    The mode is visible only to the notebook author who constructs the paired
    control.  A benchmark Agent would receive neither the mode nor the labels
    below; it would have to infer the change from public feedback.
    """

    conditions: tuple[tuple[str, tuple[dict[str, Any], ...]], ...] = (
        ("World A", ()),
        (
            "World B",
            (
                {
                    "kind": "mechanism_family",
                    "mode": mechanism_mode,
                    "severity": severity,
                },
            ),
        ),
    )
    rows: list[dict[str, Any]] = []
    for label, interventions in conditions:
        run = run_vector(
            task_id,
            vector,
            seed=seed,
            world_interventions=interventions,
        )
        rows.append(
            {
                "opaque_world": label,
                **run.metrics,
                "all_actions_valid": bool(run.trace["valid_before_step"].all()),
            }
        )
    return pd.DataFrame(rows)


def measurement_trace(run: DemoRun) -> pd.DataFrame:
    """Select feedback-bearing steps from a run for compact display."""

    return run.trace.loc[
        run.trace["operation"].eq("measure"),
        [
            "step",
            "operation",
            "reward",
            "leaderboard_score",
            "observed_keys",
            "processed_estimate",
        ],
    ].reset_index(drop=True)


def _optional_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        number = float(np.asarray(value).reshape(-1)[0])
    except (TypeError, ValueError, IndexError):
        return None
    return number if np.isfinite(number) else None


__all__ = [
    "DemoRun",
    "compare_hidden_worlds",
    "compare_vectors",
    "measurement_trace",
    "recipe_frame",
    "run_vector",
    "standard_probe_vectors",
    "task_card",
]
