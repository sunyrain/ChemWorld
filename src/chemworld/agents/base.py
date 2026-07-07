"""Agent interface used by ChemWorld runners."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol


@dataclass(frozen=True)
class HistoryRecord:
    step: int
    action: dict[str, Any]
    observation: dict[str, float | None]
    reward: float
    info: dict[str, Any]


class Agent(Protocol):
    """Minimal interface for benchmark agents."""

    name: str

    def reset(self, task_info: dict[str, Any], seed: int) -> None:
        """Prepare the agent for one task instance."""

    def act(self, history: list[HistoryRecord]) -> dict[str, Any]:
        """Choose the next experiment action."""

    def update(
        self,
        action: dict[str, Any],
        observation: dict[str, float | None],
        reward: float,
        info: dict[str, Any],
    ) -> None:
        """Receive feedback after an experiment."""

    def manifest(self) -> dict[str, Any]:
        """Return reproducibility metadata."""


class BaseAgent:
    """Convenience base class for official baselines."""

    name = "base"

    def reset(self, task_info: dict[str, Any], seed: int) -> None:
        self.task_info = task_info
        self.seed = seed

    def update(
        self,
        action: dict[str, Any],
        observation: dict[str, float | None],
        reward: float,
        info: dict[str, Any],
    ) -> None:
        del action, observation, reward, info

    def manifest(self) -> dict[str, Any]:
        return {
            "agent_name": self.name,
            "agent_family": self.__class__.__name__,
            "seed": getattr(self, "seed", None),
        }
