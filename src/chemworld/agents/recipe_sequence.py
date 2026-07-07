"""Utilities for agents that plan terminal recipes but execute event actions."""

from __future__ import annotations

from typing import Any

from chemworld.agents.base import BaseAgent, HistoryRecord
from chemworld.core.batch_reactor import recipe_to_event_sequence

DEFAULT_RECIPE_EVENT_COUNT = 6


class RecipeSequenceMixin(BaseAgent):
    """Queue event-level operations for one recipe-style recommendation."""

    def reset(self, task_info: dict[str, Any], seed: int) -> None:
        super().reset(task_info, seed)
        self._pending_events: list[dict[str, Any]] = []
        self._active_recipe: dict[str, Any] | None = None
        self._recipe_history: list[HistoryRecord] = []

    def _pop_pending_event(self) -> dict[str, Any] | None:
        if self._pending_events:
            return dict(self._pending_events.pop(0))
        return None

    def _start_recipe(self, recipe: dict[str, Any]) -> dict[str, Any]:
        self._active_recipe = dict(recipe)
        self._pending_events = recipe_to_event_sequence(recipe)
        event = self._pop_pending_event()
        if event is None:
            raise RuntimeError("recipe_to_event_sequence returned no executable events")
        return event

    def update(
        self,
        action: dict[str, Any],
        observation: dict[str, float | None],
        reward: float,
        info: dict[str, Any],
    ) -> None:
        if (
            self._active_recipe is not None
            and action.get("operation") == "measure"
            and action.get("instrument") == "final_assay"
        ):
            self._recipe_history.append(
                HistoryRecord(
                    step=len(self._recipe_history) + 1,
                    action=dict(self._active_recipe),
                    observation=dict(observation),
                    reward=float(reward),
                    info=dict(info),
                )
            )
            self._active_recipe = None
