"""Electrochemical setup and conversion helpers for ChemWorld Runtime v2."""

from __future__ import annotations

from typing import Any

import numpy as np

from chemworld.foundation import WorldState, equipment_settings, upsert_equipment_record
from chemworld.physchem.electrochemistry import ElectrodeReactionSpec, run_electrolysis
from chemworld.runtime.species import MechanismSpeciesView
from chemworld.world.parameters import ChemWorldParameters


def _action_float(action: dict[str, Any], key: str, default: float) -> float:
    value = action.get(key, default)
    return float(np.asarray(value).reshape(-1)[0])


class ChemWorldElectrochemicalServices:
    """Apply electrochemical operating conditions and faradaic conversion."""

    def __init__(self, world: ChemWorldParameters, species_view: MechanismSpeciesView) -> None:
        self.world = world
        self.species_view = species_view

    def set_potential(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        potential = float(np.clip(_action_float(action, "potential_V", 1.20), -3.0, 3.0))
        current = float(np.clip(_action_float(action, "current_mA", 50.0), 0.0, 500.0))
        equipment = upsert_equipment_record(
            state.equipment,
            equipment_id="electrochemical_cell",
            equipment_type="electrochemical_cell",
            attached_vessel_id=state.vessel_id,
            status="configured",
            settings={
                "potential_V": potential,
                "current_mA": current,
            },
        )
        risk = min(1.0, state.ledger.risk + 0.02 * max(abs(potential) - 1.5, 0.0))
        ledger = state.ledger.with_updates(cost=state.ledger.cost + 0.010, risk=risk)
        return state.replace(ledger=ledger, equipment=equipment)

    def electrolyze(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        duration = float(np.clip(_action_float(action, "duration_s", 900.0), 0.0, 14_400.0))
        cell_settings = equipment_settings(state.equipment, "electrochemical_cell")
        potential = float(cell_settings.get("potential_V", 1.20))
        current_mA = float(cell_settings.get("current_mA", 50.0))
        species = state.species_amounts.copy()
        reactant = self.species_view.reactant_species(state)
        product = self.species_view.primary_target_species
        impurity = self.species_view.primary_impurity_species
        a_mol = species.get(reactant, 0.0)
        volume = max(state.volume_L, 1.0e-9)
        catalyst = int(state.metadata.get("catalyst", 0))
        solvent = int(state.metadata.get("solvent", 0))
        exchange_current_density = 28.0 * float(self.world.catalyst_effects[catalyst, 0])
        exchange_current_density *= float(self.world.solvent_effects[solvent, 0])
        electrochemical_spec = ElectrodeReactionSpec(
            reaction_id=f"{reactant}_to_{product}_electrochemical",
            electrons_transferred=2.0,
            standard_potential_V=1.05,
            reaction_quotient_exponents={product: 1.0, reactant: -1.0},
            exchange_current_density_A_m2=exchange_current_density,
            electrode_area_m2=0.004,
            faradaic_efficiency_ref=0.91,
            product_selectivity_ref=0.90,
            overpotential_selectivity_sensitivity_V_inv=0.45,
        )
        activities = {
            reactant: max(a_mol / volume, 1.0e-12),
            product: max(species.get(product, 0.0) / volume, 1.0e-12),
        }
        result = run_electrolysis(
            electrochemical_spec,
            electrode_potential_V=potential,
            duration_s=duration,
            activities=activities,
            available_substrate_mol=a_mol,
            temperature_K=state.temperature_K,
            applied_current_A=current_mA / 1000.0,
        )
        species[reactant] = a_mol - result.converted_mol
        species[product] = species.get(product, 0.0) + result.product_mol
        species[impurity] = species.get(impurity, 0.0) + result.byproduct_mol
        metadata = state.metadata.copy()
        metadata["electrochemical_model"] = "nernst_butler_volmer_faradaic_v1"
        metadata["electrochemical_selectivity"] = result.product_selectivity
        metadata["faradaic_efficiency"] = result.faradaic_efficiency
        metadata["energy_efficiency"] = result.energy_efficiency
        metadata["equilibrium_potential_V"] = result.equilibrium_potential_V
        metadata["overpotential_V"] = result.overpotential_V
        metadata["kinetic_current_A"] = result.kinetic_current_A
        metadata["actual_current_A"] = result.actual_current_A
        metadata["charge_C"] = result.charge_C
        metadata["faradaic_charge_C"] = result.faradaic_charge_C
        metadata["electrical_work_J"] = result.electrical_work_J
        overpotential_risk = max(abs(result.overpotential_V) - 0.35, 0.0)
        ledger = state.ledger.with_updates(
            time_s=state.ledger.time_s + duration,
            cost=state.ledger.cost + 0.018 + result.electrical_work_J / 250_000.0,
            risk=min(
                1.0,
                state.ledger.risk
                + 0.015
                + 0.025 * abs(potential)
                + 0.035 * overpotential_risk,
            ),
            energy_jacket_J=state.ledger.energy_jacket_J + result.electrical_work_J,
        )
        return state.replace(species_amounts=species, ledger=ledger, metadata=metadata)


__all__ = ["ChemWorldElectrochemicalServices"]
