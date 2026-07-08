"""Reaction advancement and thermal-risk helpers for ChemWorld Runtime v2."""

from __future__ import annotations

from typing import Any

import numpy as np

from chemworld.foundation import WorldState, equipment_settings, upsert_equipment_record
from chemworld.runtime.species import MechanismSpeciesView
from chemworld.world.parameters import ChemWorldParameters
from chemworld.world.reaction_kernel import integrate_compiled_reaction_ode
from chemworld.world.thermal_kernel import pressure_and_risk


def _action_float(action: dict[str, Any], key: str, default: float) -> float:
    value = action.get(key, default)
    return float(np.asarray(value).reshape(-1)[0])


class ChemWorldReactionThermalServices:
    """Advance reaction state and apply thermal pressure/risk ledgers."""

    def __init__(
        self,
        world: ChemWorldParameters,
        species_view: MechanismSpeciesView,
    ) -> None:
        self.world = world
        self.species_view = species_view

    def integrate(
        self,
        state: WorldState,
        action: dict[str, Any],
        *,
        heat: bool,
    ) -> WorldState:
        duration = float(np.clip(_action_float(action, "duration_s", 600.0), 0.0, 14_400.0))
        target_temperature = _action_float(action, "target_temperature_K", state.temperature_K)
        reactor_settings = equipment_settings(state.equipment, "batch_reactor")
        stirring_speed = _action_float(
            action,
            "stirring_speed_rpm",
            float(reactor_settings.get("stirring_speed_rpm", 600.0)),
        )
        compiled_mechanism = self.species_view.mechanism
        if compiled_mechanism is None:
            raise RuntimeError("Runtime v2 reaction advancement requires a compiled mechanism")
        result = integrate_compiled_reaction_ode(
            state=state,
            world=self.world,
            compiled_mechanism=compiled_mechanism,
            duration_s=duration,
            target_temperature_K=target_temperature,
            heat=heat,
            stirring_speed_rpm=stirring_speed,
        )
        if result is None:
            return state
        ledger = state.ledger.with_updates(
            time_s=state.ledger.time_s + result.duration_s,
            cost=state.ledger.cost + result.cost_delta,
            energy_jacket_J=state.ledger.energy_jacket_J + result.energy_jacket_J,
            heat_reaction_J=state.ledger.heat_reaction_J + result.heat_reaction_J,
            heat_loss_J=state.ledger.heat_loss_J + result.heat_loss_J,
        )
        equipment = upsert_equipment_record(
            state.equipment,
            equipment_id="batch_reactor",
            equipment_type="batch_reactor",
            attached_vessel_id=state.vessel_id,
            status="configured",
            settings={"stirring_speed_rpm": result.stirring_speed_rpm},
        )
        return state.replace(
            species_amounts=result.species_amounts,
            temperature_K=result.temperature_K,
            ledger=ledger,
            equipment=equipment,
        )

    def with_risk_and_pressure(self, state: WorldState) -> WorldState:
        pressure, risk = pressure_and_risk(
            state=state,
            solvent_risks=self.world.solvent_risks,
        )
        return state.replace(pressure_Pa=pressure, ledger=state.ledger.with_updates(risk=risk))


__all__ = ["ChemWorldReactionThermalServices"]
