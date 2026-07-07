"""Latin hypercube search baseline."""

from __future__ import annotations

from typing import Any

import numpy as np

from chemworld.agents.base import BaseAgent, HistoryRecord
from chemworld.agents.recipe_sequence import DEFAULT_RECIPE_EVENT_COUNT, RecipeSequenceMixin
from chemworld.core.actions import ACTION_BOUNDS, CATALYSTS, SOLVENTS, vector_to_action


class LatinHypercubeAgent(RecipeSequenceMixin, BaseAgent):
    name = "latin_hypercube"

    def reset(self, task_info: dict[str, Any], seed: int) -> None:
        super().reset(task_info, seed)
        self.rng = np.random.default_rng(seed)
        budget = max(1, int(task_info["budget"]) // DEFAULT_RECIPE_EVENT_COUNT)
        dims = 6
        design = np.zeros((budget, dims), dtype=float)
        for dim in range(dims):
            bins = (np.arange(budget, dtype=float) + self.rng.random(budget)) / budget
            self.rng.shuffle(bins)
            design[:, dim] = bins
        self._actions = [vector_to_action(row) for row in design]

    def act(self, history: list[HistoryRecord]) -> dict[str, Any]:
        del history
        pending = self._pop_pending_event()
        if pending is not None:
            return pending

        index = min(len(self._recipe_history), len(self._actions) - 1)
        action = self._actions[index]
        action["catalyst"] = int(np.clip(action["catalyst"], 0, len(CATALYSTS) - 1))
        action["solvent"] = int(np.clip(action["solvent"], 0, len(SOLVENTS) - 1))
        for key, bound in ACTION_BOUNDS.items():
            action[key] = float(np.clip(action[key], bound.low, bound.high))
        return self._start_recipe(dict(action))
