"""Greedy local perturbation baseline."""

from __future__ import annotations

from typing import Any

import numpy as np

from chemworld.agents.base import BaseAgent, HistoryRecord
from chemworld.agents.recipe_sequence import RecipeSequenceMixin
from chemworld.core.actions import ACTION_BOUNDS, CATALYSTS, SOLVENTS, sample_random_action


class GreedyLocalAgent(RecipeSequenceMixin, BaseAgent):
    name = "greedy_local"

    def __init__(self, warmup: int = 5, perturbation_scale: float = 0.18) -> None:
        self.warmup = warmup
        self.perturbation_scale = perturbation_scale

    def reset(self, task_info: dict[str, Any], seed: int) -> None:
        super().reset(task_info, seed)
        self.rng = np.random.default_rng(seed)

    def act(self, history: list[HistoryRecord]) -> dict[str, Any]:
        del history
        pending = self._pop_pending_event()
        if pending is not None:
            return pending

        recipe_history = self._recipe_history
        if len(recipe_history) < self.warmup:
            return self._start_recipe(sample_random_action(self.rng))

        best = max(recipe_history, key=lambda item: item.reward)
        action = dict(best.action)
        for key, bound in ACTION_BOUNDS.items():
            width = bound.high - bound.low
            action[key] = float(
                np.clip(
                    float(action[key]) + self.rng.normal(0.0, self.perturbation_scale * width),
                    bound.low,
                    bound.high,
                )
            )

        if self.rng.random() < 0.20:
            action["catalyst"] = int(self.rng.integers(0, len(CATALYSTS)))
        if self.rng.random() < 0.20:
            action["solvent"] = int(self.rng.integers(0, len(SOLVENTS)))
        return self._start_recipe(action)
