"""Example student submission.

This file deliberately does not create a ChemWorld environment. The teacher-side
runner owns reset/step/evaluation and only asks this agent for the next action.
"""

from __future__ import annotations

from typing import Any


class StudentAgent:
    def __init__(self) -> None:
        self.task_info: dict[str, Any] = {}
        self.plan: list[dict[str, Any]] = []

    def reset(self, task_info: dict[str, Any], seed: int) -> None:
        del seed
        self.task_info = task_info
        allowed = set(task_info.get("allowed_operations", []))
        purification = "separate_phase" in allowed
        self.plan = [
            {"operation": "add_solvent", "volume_L": 0.028, "solvent": 2},
            {"operation": "add_reagent", "amount_mol": 0.010},
            {"operation": "add_catalyst", "catalyst_amount_mol": 0.00025, "catalyst": 1},
            {
                "operation": "heat",
                "target_temperature_K": 385.0,
                "duration_s": 1500.0,
                "stirring_speed_rpm": 720.0,
            },
            {"operation": "wait", "duration_s": 900.0, "stirring_speed_rpm": 720.0},
            {"operation": "measure", "instrument": "hplc"},
            {"operation": "quench"},
        ]
        if purification:
            self.plan.extend(
                [
                    {"operation": "add_phase", "phase": "aqueous", "volume_L": 0.012},
                    {
                        "operation": "add_extractant",
                        "extractant": "organic",
                        "volume_L": 0.018,
                    },
                    {"operation": "mix", "duration_s": 240.0, "stirring_speed_rpm": 850.0},
                    {"operation": "settle", "duration_s": 420.0},
                    {"operation": "separate_phase", "target_phase": "organic"},
                    {"operation": "wash", "wash_volume_L": 0.008},
                    {"operation": "dry"},
                    {"operation": "concentrate", "duration_s": 600.0},
                    {"operation": "transfer", "transfer_fraction": 0.97},
                ]
            )
        self.plan.extend(
            [
                {"operation": "terminate"},
                {"operation": "measure", "instrument": "final_assay"},
            ]
        )

    def act(self, history: list[dict[str, Any]]) -> dict[str, Any]:
        step = len(history)
        if step < len(self.plan):
            return dict(self.plan[step])
        return {"operation": "measure", "instrument": "final_assay"}

    def update(
        self,
        action: dict[str, Any],
        observation: dict[str, Any],
        reward: float,
        info: dict[str, Any],
    ) -> None:
        del action, observation, reward, info


def make_agent() -> StudentAgent:
    return StudentAgent()
