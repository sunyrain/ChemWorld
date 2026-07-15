"""Thermal and safety-law module for ChemWorld."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from chemworld.foundation import WorldState, equipment_settings, selected_phase_id


def pressure_and_risk(
    *,
    state: WorldState,
    solvent_risks: np.ndarray,
    pressure_override_Pa: float | None = None,
) -> tuple[float, float]:
    reactor_settings = equipment_settings(state.equipment, "batch_reactor")
    solvent = int(reactor_settings.get("solvent", 0))
    active_amounts = state.species_amounts
    active_phase_id = selected_phase_id(state.phases)
    if state.phases is not None and active_phase_id in state.phases.phases:
        active_amounts = state.phases.phases[active_phase_id].species_amounts_mol
    total_amount = sum(
        value for key, value in active_amounts.items() if not key.startswith("Cat")
    )
    concentration = 0.0 if state.volume_L <= 0 else total_amount / state.volume_L
    pressure = (
        101_325.0 * (state.temperature_K / 298.15) * (1.0 + 0.025 * concentration)
        if pressure_override_Pa is None
        else float(pressure_override_Pa)
    )
    if pressure <= 0.0 or not np.isfinite(pressure):
        raise ValueError("pressure_override_Pa must be positive and finite")
    exotherm_risk = min(1.0, abs(state.ledger.heat_reaction_J) / 2500.0)
    temperature_risk = 1.0 / (1.0 + np.exp(-(state.temperature_K - 405.0) / 13.0))
    concentration_risk = 1.0 / (1.0 + np.exp(-(concentration - 0.8) / 0.22))
    risk = float(
        np.clip(
            0.30 * temperature_risk
            + 0.20 * concentration_risk
            + 0.20 * exotherm_risk
            + 0.18 * solvent_risks[solvent]
            + 0.12 * (pressure / 550_000.0),
            0.0,
            1.0,
        )
    )
    return float(pressure), risk


@dataclass(frozen=True)
class ThermalModuleSpec:
    module_id: str = "thermal"
    version: str = "0.3"
    laws: tuple[str, ...] = (
        "jacket_heat_input",
        "heat_loss_to_environment",
        "reaction_enthalpy",
        "temperature_pressure_risk_proxy",
    )

    def to_dict(self) -> dict[str, object]:
        return {
            "module_id": self.module_id,
            "version": self.version,
            "laws": list(self.laws),
            "state_ledgers": [
                "energy_jacket_J",
                "heat_reaction_J",
                "heat_loss_J",
                "temperature_K",
                "pressure_Pa",
                "risk",
            ],
        }


__all__ = ["ThermalModuleSpec", "pressure_and_risk"]
