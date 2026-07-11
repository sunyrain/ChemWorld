"""Continuous-flow state-update services for the transactional runtime."""

from __future__ import annotations

from math import pi
from typing import Any

import numpy as np

from chemworld.foundation import (
    WorldState,
    equipment_settings,
    process_with_metrics,
    upsert_equipment_record,
)
from chemworld.physchem.pfr_reactors import PFRGeometrySpec, PFRModel
from chemworld.runtime.reaction_thermal_services import ChemWorldReactionThermalServices
from chemworld.runtime.species import MechanismSpeciesView


def _action_float(action: dict[str, Any], key: str, default: float) -> float:
    value = action.get(key, default)
    return float(np.asarray(value).reshape(-1)[0])


class ChemWorldFlowServices:
    """Apply flow setup and a geometry-resolved PFR state update."""

    def __init__(
        self,
        species_view: MechanismSpeciesView,
        reaction_thermal: ChemWorldReactionThermalServices,
    ) -> None:
        self.species_view = species_view
        self.reaction_thermal = reaction_thermal
        self.world = reaction_thermal.world

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
        ) * self.world.domain_parameter("flow_residence_multiplier")
        flow_rate = float(flow_settings.get("flow_rate_mL_min", 1.0))
        duration = float(
            np.clip(_action_float(action, "duration_s", residence), residence, 14_400.0)
        )
        target_temperature = float(
            np.clip(_action_float(action, "target_temperature_K", 348.15), 298.15, 430.0)
        )
        volumetric_flow_L_s = flow_rate / 1000.0 / 60.0
        reactor_volume_L = volumetric_flow_L_s * residence
        inner_diameter_m = 0.004
        cross_section_area_m2 = pi * inner_diameter_m**2 / 4.0
        geometry = PFRGeometrySpec(
            length_m=(reactor_volume_L / 1000.0) / cross_section_area_m2,
            inner_diameter_m=inner_diameter_m,
            roughness_m=1.0e-6,
            fluid_density_kg_m3=950.0,
            fluid_viscosity_Pa_s=1.2e-3,
            boundary_ua_W_per_m_K=(
                5.0 * self.world.domain_parameter("flow_boundary_ua_multiplier")
            ),
            boundary_temperature_K=target_temperature,
        )
        model = PFRModel(
            network=self.species_view.mechanism.network,
            reactor_volume_L=reactor_volume_L,
            volumetric_flow_L_s=volumetric_flow_L_s,
            geometry=geometry,
            inlet_pressure_Pa=max(state.pressure_Pa, 101_325.0),
            reactor_id="chemworld_runtime_pfr_v1",
            rate_multiplier=self.world.domain_parameter("flow_rate_multiplier"),
        )
        inlet_concentrations = {
            species_id: max(state.species_amounts.get(species_id, 0.0), 0.0)
            / max(state.volume_L, 1.0e-12)
            for species_id in model.network.species_ids
        }
        result = model.simulate(
            inlet_concentrations,
            temperature_K=target_temperature,
            axial_positions_m=(0.0, geometry.length_m * 0.5, geometry.length_m),
        )
        state_scale = state.volume_L / reactor_volume_L
        species_amounts = state.species_amounts.copy()
        for species_id, amount_mol in result.final_state.amounts_mol.items():
            species_amounts[species_id] = max(amount_mol * state_scale, 0.0)
        reactant_id = self.species_view.reactant_species(state)
        conversion = result.conversion(reactant_id)
        process = process_with_metrics(
            state.process,
            flow_conversion=conversion,
            flow_campaign_time_s=duration,
            flow_throughput_mL=flow_rate * duration / 60.0,
        )
        ledger = state.ledger.with_updates(
            time_s=state.ledger.time_s + duration,
            cost=state.ledger.cost + duration / 3600.0 * 0.030,
            energy_jacket_J=(
                state.ledger.energy_jacket_J + result.final_state.energy_jacket_J * state_scale
            ),
            heat_reaction_J=(
                state.ledger.heat_reaction_J + result.final_state.heat_reaction_J * state_scale
            ),
            heat_loss_J=(state.ledger.heat_loss_J + result.final_state.heat_loss_J * state_scale),
            risk=min(1.0, state.ledger.risk + 0.015 * (target_temperature > 390.0)),
        )
        pressure_payload = result.metadata.get("pressures_Pa")
        pressure_drop_payload = result.metadata.get("pressure_drop_Pa")
        reynolds_payload = result.metadata.get("reynolds_number")
        if not isinstance(pressure_payload, tuple | list) or not pressure_payload:
            raise RuntimeError("PFR result is missing its pressure profile")
        if not isinstance(pressure_drop_payload, int | float):
            raise RuntimeError("PFR result is missing pressure_drop_Pa")
        if not isinstance(reynolds_payload, int | float):
            raise RuntimeError("PFR result is missing reynolds_number")
        pressures = tuple(float(value) for value in pressure_payload)
        equipment = upsert_equipment_record(
            state.equipment,
            equipment_id="flow_reactor",
            equipment_type="continuous_flow_reactor",
            attached_vessel_id=state.vessel_id,
            status="completed",
            settings={
                "flow_model_id": "pfr",
                "runtime_adapter_id": "chemworld_geometry_resolved_pfr_v1",
                "reactor_volume_L": reactor_volume_L,
                "geometry": geometry.to_dict(),
                "outlet_pressure_Pa": pressures[-1],
                "pressure_drop_Pa": float(pressure_drop_payload),
                "reynolds_number": float(reynolds_payload),
                "solver_diagnostic": result.metadata["solver_diagnostic"],
                "material_balance_error_mol": result.material_balance_error_mol,
            },
        )
        return state.replace(
            species_amounts=species_amounts,
            temperature_K=result.final_state.temperature_K,
            pressure_Pa=pressures[-1],
            ledger=ledger,
            process=process,
            equipment=equipment,
        )


__all__ = ["ChemWorldFlowServices"]
