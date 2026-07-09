"""Continuous-flow state-update helpers for ChemWorld Runtime v2."""

from __future__ import annotations

from typing import Any

import numpy as np

from chemworld.foundation import (
    WorldState,
    equipment_settings,
    process_with_metrics,
    upsert_equipment_record,
)
from chemworld.runtime.reaction_thermal_services import ChemWorldReactionThermalServices
from chemworld.runtime.species import MechanismSpeciesView


def _action_float(action: dict[str, Any], key: str, default: float) -> float:
    value = action.get(key, default)
    return float(np.asarray(value).reshape(-1)[0])


class ChemWorldFlowServices:
    """Apply flow setup and residence-time conversion updates."""

    def __init__(
        self,
        species_view: MechanismSpeciesView,
        reaction_thermal: ChemWorldReactionThermalServices,
    ) -> None:
        self.species_view = species_view
        self.reaction_thermal = reaction_thermal

    def set_flow_rate(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        flow_rate = float(np.clip(_action_float(action, "flow_rate_mL_min", 1.0), 0.01, 20.0))
        residence = float(np.clip(_action_float(action, "residence_time_s", 600.0), 1.0, 7200.0))
        equipment = upsert_equipment_record(
            state.equipment,
            equipment_id="flow_reactor",
            equipment_type="continuous_flow_reactor",
            attached_vessel_id=state.vessel_id,
            status="configured",
            settings={
                "flow_rate_mL_min": flow_rate,
                "residence_time_s": residence,
            },
        )
        ledger = state.ledger.with_updates(cost=state.ledger.cost + 0.012)
        return state.replace(ledger=ledger, equipment=equipment)

    def run_flow(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        flow_settings = equipment_settings(state.equipment, "flow_reactor")
        residence = float(
            flow_settings.get(
                "residence_time_s",
                _action_float(action, "duration_s", 600.0),
            )
        )
        flow_rate = float(flow_settings.get("flow_rate_mL_min", 1.0))
        duration = float(
            np.clip(_action_float(action, "duration_s", residence), residence, 14_400.0)
        )
        target_temperature = float(
            np.clip(_action_float(action, "target_temperature_K", 348.15), 298.15, 430.0)
        )
        effective_action = {
            "duration_s": residence,
            "target_temperature_K": target_temperature,
            "stirring_speed_rpm": 900.0,
        }
        reacted_state = self.reaction_thermal.integrate(state, effective_action, heat=True)
        initial_a = max(self.species_view.initial_reactant_amount(state), 1.0e-12)
        conversion = float(
            np.clip(
                (initial_a - self.species_view.reactant_amount(reacted_state)) / initial_a,
                0.0,
                1.0,
            )
        )
        process = process_with_metrics(
            reacted_state.process,
            flow_conversion=conversion,
            flow_campaign_time_s=duration,
            flow_throughput_mL=flow_rate * duration / 60.0,
        )
        ledger = reacted_state.ledger.with_updates(
            time_s=state.ledger.time_s + duration,
            cost=reacted_state.ledger.cost + duration / 3600.0 * 0.030,
            risk=min(1.0, reacted_state.ledger.risk + 0.015 * (target_temperature > 390.0)),
        )
        return reacted_state.replace(ledger=ledger, process=process)


__all__ = ["ChemWorldFlowServices"]
