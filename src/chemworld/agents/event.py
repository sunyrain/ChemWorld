"""Event-sequence baseline agents for foundation-backed environments."""

from __future__ import annotations

from typing import Any

from chemworld.agents.base import BaseAgent, HistoryRecord


class ScriptedChemistryAgent(BaseAgent):
    """A simple chemistry-aware event planner for ChemWorld tasks."""

    name = "scripted_chemistry"

    def act(self, history: list[HistoryRecord]) -> dict[str, Any]:
        step = len(history)
        budget = int(self.task_info.get("budget", 30))
        purification_enabled = "separate_phase" in set(self.task_info.get("allowed_operations", []))
        sequence: list[dict[str, Any]] = [
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
            {"operation": "wait", "duration_s": 600.0, "stirring_speed_rpm": 720.0},
            {"operation": "measure", "instrument": "uvvis"},
            {"operation": "quench"},
        ]
        if purification_enabled:
            sequence.extend(
                [
                    {"operation": "add_phase", "phase": "aqueous", "volume_L": 0.012},
                    {"operation": "add_extractant", "extractant": "organic", "volume_L": 0.018},
                    {"operation": "mix", "duration_s": 240.0, "stirring_speed_rpm": 850.0},
                    {"operation": "settle", "duration_s": 420.0},
                    {"operation": "separate_phase", "target_phase": "organic"},
                    {"operation": "wash", "wash_volume_L": 0.008},
                    {"operation": "dry"},
                    {"operation": "concentrate", "duration_s": 600.0},
                    {"operation": "transfer", "transfer_fraction": 0.97},
                    {"operation": "measure", "instrument": "hplc"},
                ]
            )
        sequence.extend(
            [
                {"operation": "terminate"},
                {"operation": "measure", "instrument": "final_assay"},
            ]
        )
        if step < len(sequence):
            return sequence[step]
        if step >= budget - 1:
            return {"operation": "measure", "instrument": "final_assay"}
        return {"operation": "wait", "duration_s": 300.0}
