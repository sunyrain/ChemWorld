"""LLM adapter interfaces.

This module deliberately avoids direct API dependencies. Reproducible LLM
experiments should declare model metadata, prompt templates, cache policy, and
offline replay files in the agent manifest.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from chemworld.agents.base import BaseAgent, HistoryRecord
from chemworld.agents.recipe_sequence import RecipeSequenceMixin
from chemworld.core.actions import canonicalize_action

DEFAULT_PROMPT_TEMPLATE = """You are planning the next virtual ChemWorld reaction experiment.
Task info:
{task_info}

History:
{history}

Return one JSON object with keys temperature, time, initial_concentration,
stirring_speed, catalyst, solvent, hypothesis, rationale.
"""


class LLMPlannerAgent(RecipeSequenceMixin, BaseAgent):
    """Abstract adapter for online or cached LLM planners."""

    name = "llm_planner"

    def __init__(self, prompt_template: str = DEFAULT_PROMPT_TEMPLATE) -> None:
        self.prompt_template = prompt_template

    def act(self, history: list[HistoryRecord]) -> dict[str, Any]:
        del history
        pending = self._pop_pending_event()
        if pending is not None:
            return pending

        prompt = self.build_prompt(self._recipe_history)
        response = self.complete(prompt)
        payload = json.loads(response)
        return self._start_recipe(canonicalize_action(payload))

    def build_prompt(self, history: list[HistoryRecord]) -> str:
        compact_history = [
            {
                "step": record.step,
                "action": record.action,
                "observation": record.observation,
                "reward": record.reward,
            }
            for record in history
        ]
        return self.prompt_template.format(
            task_info=json.dumps(self.task_info, sort_keys=True),
            history=json.dumps(compact_history, sort_keys=True),
        )

    def complete(self, prompt: str) -> str:
        raise NotImplementedError(
            "LLMPlannerAgent is an adapter. Implement complete() or use ReplayLLMAgent."
        )

    def manifest(self) -> dict[str, Any]:
        manifest = super().manifest()
        manifest.update(
            {
                "prompt_template": self.prompt_template,
                "requires_online_model": True,
            }
        )
        return manifest


class ReplayLLMAgent(LLMPlannerAgent):
    """Replay cached LLM decisions from a JSONL file for deterministic evaluation."""

    name = "llm_replay"

    def __init__(
        self,
        replay_path: str | Path,
        prompt_template: str = DEFAULT_PROMPT_TEMPLATE,
    ) -> None:
        super().__init__(prompt_template=prompt_template)
        self.replay_path = Path(replay_path)

    def reset(self, task_info: dict[str, Any], seed: int) -> None:
        super().reset(task_info, seed)
        with self.replay_path.open("r", encoding="utf-8") as handle:
            self._responses = [json.loads(line) for line in handle if line.strip()]
        self._index = 0

    def complete(self, prompt: str) -> str:
        del prompt
        if self._index >= len(self._responses):
            raise RuntimeError(f"Replay file exhausted: {self.replay_path}")
        payload = self._responses[self._index]
        self._index += 1
        return json.dumps(payload)

    def manifest(self) -> dict[str, Any]:
        manifest = super().manifest()
        manifest.update(
            {
                "requires_online_model": False,
                "replay_path": str(self.replay_path),
            }
        )
        return manifest

