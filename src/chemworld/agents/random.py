"""Uniform random search baseline."""

from __future__ import annotations

from typing import Any

import numpy as np

from chemworld.agents.base import BaseAgent, HistoryRecord


class RandomAgent(BaseAgent):
    name = "random"

    def reset(self, task_info: dict[str, Any], seed: int) -> None:
        super().reset(task_info, seed)
        self.rng = np.random.default_rng(seed)

    def act(self, history: list[HistoryRecord]) -> dict[str, Any]:
        step = len(history)
        budget = int(self.task_info.get("budget", 30))
        if step == 0:
            return {
                "operation": "add_solvent",
                "volume_L": float(self.rng.uniform(0.018, 0.040)),
                "solvent": int(self.rng.integers(0, 4)),
            }
        if step == 1:
            return {"operation": "add_reagent", "amount_mol": float(self.rng.uniform(0.002, 0.020))}
        if step == 2:
            return {
                "operation": "add_catalyst",
                "catalyst_amount_mol": float(self.rng.uniform(0.00008, 0.0006)),
                "catalyst": int(self.rng.integers(0, 4)),
            }
        if step == max(3, budget - 2):
            return {"operation": "terminate"}
        if step >= max(4, budget - 1):
            return {"operation": "measure", "instrument": "final_assay"}
        if step == 3:
            return {
                "operation": "heat",
                "target_temperature_K": float(self.rng.uniform(330.0, 430.0)),
                "duration_s": float(self.rng.uniform(600.0, 2400.0)),
                "stirring_speed_rpm": float(self.rng.uniform(250.0, 1000.0)),
            }
        if step % 3 == 0:
            return {"operation": "measure", "instrument": "hplc"}
        return {"operation": "wait", "duration_s": float(self.rng.uniform(300.0, 1800.0))}
