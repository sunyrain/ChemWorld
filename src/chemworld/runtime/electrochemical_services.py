"""Electrochemical setup and conversion services for the transactional runtime."""

from __future__ import annotations

from typing import Any

import numpy as np

from chemworld.foundation import (
    WorldState,
    equipment_settings,
    process_with_metrics,
    upsert_equipment_record,
)
from chemworld.physchem.electrochem_double_layer import (
    DoubleLayerRCSpec,
    simulate_double_layer_current_step,
)
from chemworld.physchem.electrochem_transport import (
    DiffusionLayerSpec,
    diffusion_layer_current_response,
)
from chemworld.physchem.electrochemistry import (
    FARADAY_C_PER_MOL,
    R_J_PER_MOL_K,
    ElectrodeReactionSpec,
    ElectrolyteResistanceSpec,
    run_electrolysis,
)
from chemworld.physchem.equilibrium_chemistry import (
    SolubilityProductSpec,
    solve_aqueous_electrolyte_equilibrium,
)
from chemworld.runtime.species import MechanismSpeciesView
from chemworld.world.actions import ELECTROLYTE_PROFILES
from chemworld.world.material_counterfactual import resolve_material_law_index
from chemworld.world.parameters import ChemWorldParameters

AQUEOUS_ELECTROLYTE_PROFILE_PARAMETERS: tuple[dict[str, float], ...] = (
    {
        "electrolyte_conductivity_S_m": 0.8,
        "electrode_gap_m": 0.006,
        "electrode_area_m2": 0.004,
        "contact_resistance_ohm": 0.50,
        "diffusivity_m2_s": 3.0e-10,
        "diffusion_layer_thickness_m": 2.5e-3,
        "double_layer_capacitance_F_m2": 0.25,
        "acid_concentration_mol_L": 0.015,
        "supporting_electrolyte_concentration_mol_L": 0.003,
        "precipitating_salt_concentration_mol_L": 0.001,
        "electrolyte_acid_pka": 4.76,
        "electrolyte_ksp": 1.0e-7,
    },
    {
        "electrolyte_conductivity_S_m": 12.0,
        "electrode_gap_m": 0.003,
        "electrode_area_m2": 0.004,
        "contact_resistance_ohm": 0.12,
        "diffusivity_m2_s": 1.2e-9,
        "diffusion_layer_thickness_m": 8.0e-4,
        "double_layer_capacitance_F_m2": 0.20,
        "acid_concentration_mol_L": 0.010,
        "supporting_electrolyte_concentration_mol_L": 0.080,
        "precipitating_salt_concentration_mol_L": 0.001,
        "electrolyte_acid_pka": 4.76,
        "electrolyte_ksp": 1.0e-8,
    },
    {
        "electrolyte_conductivity_S_m": 6.0,
        "electrode_gap_m": 0.004,
        "electrode_area_m2": 0.004,
        "contact_resistance_ohm": 0.20,
        "diffusivity_m2_s": 8.0e-10,
        "diffusion_layer_thickness_m": 1.2e-3,
        "double_layer_capacitance_F_m2": 0.18,
        "acid_concentration_mol_L": 0.050,
        "supporting_electrolyte_concentration_mol_L": 0.040,
        "precipitating_salt_concentration_mol_L": 5.0e-4,
        "electrolyte_acid_pka": 3.20,
        "electrolyte_ksp": 1.0e-6,
    },
    {
        "electrolyte_conductivity_S_m": 2.0,
        "electrode_gap_m": 0.005,
        "electrode_area_m2": 0.004,
        "contact_resistance_ohm": 0.35,
        "diffusivity_m2_s": 2.0e-10,
        "diffusion_layer_thickness_m": 3.0e-3,
        "double_layer_capacitance_F_m2": 0.30,
        "acid_concentration_mol_L": 0.005,
        "supporting_electrolyte_concentration_mol_L": 0.015,
        "precipitating_salt_concentration_mol_L": 0.050,
        "electrolyte_acid_pka": 6.20,
        "electrolyte_ksp": 1.0e-12,
    },
)


def _action_float(action: dict[str, Any], key: str, default: float) -> float:
    value = action.get(key, default)
    return float(np.asarray(value).reshape(-1)[0])


def _bounded_action_float(
    action: dict[str, Any],
    key: str,
    default: float,
    *,
    low: float,
    high: float,
    inclusive_low: bool = True,
) -> float:
    value = _action_float(action, key, default)
    lower_ok = value >= low if inclusive_low else value > low
    if not np.isfinite(value) or not lower_ok or value > high:
        comparator = "<=" if inclusive_low else "<"
        raise ValueError(f"{key} must satisfy {low} {comparator} value <= {high}")
    return value


def _bounded_action_index(action: dict[str, Any], key: str, count: int) -> int:
    value = action.get(key)
    if isinstance(value, bool) or not isinstance(value, int) or not 0 <= value < count:
        raise ValueError(f"{key} must be an integer index in [0, {count - 1}]")
    return value


class ChemWorldElectrochemicalServices:
    """Apply electrochemical operating conditions and faradaic conversion."""

    def __init__(self, world: ChemWorldParameters, species_view: MechanismSpeciesView) -> None:
        self.world = world
        self.species_view = species_view

    def set_potential(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        electrolyte_profile = _bounded_action_index(
            action,
            "electrolyte_profile",
            len(ELECTROLYTE_PROFILES),
        )
        hidden_profile = resolve_material_law_index(
            state.metadata,
            material_field="electrolyte_profile",
            public_index=electrolyte_profile,
            catalog_size=len(ELECTROLYTE_PROFILES),
        )
        profile = AQUEOUS_ELECTROLYTE_PROFILE_PARAMETERS[hidden_profile]
        previous_cell_settings = equipment_settings(state.equipment, "electrochemical_cell")
        potential = _bounded_action_float(action, "potential_V", 1.20, low=-3.0, high=3.0)
        current = _bounded_action_float(action, "current_mA", 50.0, low=1.0e-3, high=500.0)
        conductivity = _bounded_action_float(
            action,
            "electrolyte_conductivity_S_m",
            profile["electrolyte_conductivity_S_m"],
            low=0.0,
            high=100.0,
            inclusive_low=False,
        )
        electrode_gap = _bounded_action_float(
            action,
            "electrode_gap_m",
            profile["electrode_gap_m"],
            low=1.0e-5,
            high=0.050,
        )
        electrode_area = _bounded_action_float(
            action,
            "electrode_area_m2",
            profile["electrode_area_m2"],
            low=1.0e-5,
            high=0.20,
        )
        contact_resistance = _bounded_action_float(
            action,
            "contact_resistance_ohm",
            profile["contact_resistance_ohm"],
            low=0.0,
            high=100.0,
        )
        voltage_window = _bounded_action_float(action, "voltage_window_V", 2.5, low=0.1, high=10.0)
        diffusivity = _bounded_action_float(
            action,
            "diffusivity_m2_s",
            profile["diffusivity_m2_s"],
            low=1.0e-12,
            high=1.0e-7,
        )
        diffusion_layer = _bounded_action_float(
            action,
            "diffusion_layer_thickness_m",
            profile["diffusion_layer_thickness_m"],
            low=1.0e-7,
            high=1.0e-2,
        )
        capacitance = _bounded_action_float(
            action,
            "double_layer_capacitance_F_m2",
            profile["double_layer_capacitance_F_m2"],
            low=1.0e-5,
            high=100.0,
        )
        acid_total = _bounded_action_float(
            action,
            "electrolyte_acid_total_mol",
            profile["acid_concentration_mol_L"] * state.volume_L,
            low=0.0,
            high=max(state.volume_L, 1.0e-6),
        )
        supporting_electrolyte = _bounded_action_float(
            action,
            "supporting_electrolyte_mol",
            profile["supporting_electrolyte_concentration_mol_L"] * state.volume_L,
            low=0.0,
            high=0.50 * state.volume_L,
        )
        precipitating_salt = _bounded_action_float(
            action,
            "precipitating_salt_mol",
            profile["precipitating_salt_concentration_mol_L"] * state.volume_L,
            low=0.0,
            high=0.10 * state.volume_L,
        )
        acid_pka = _bounded_action_float(
            action,
            "electrolyte_acid_pka",
            profile["electrolyte_acid_pka"],
            low=-2.0,
            high=16.0,
        )
        solubility_product = _bounded_action_float(
            action,
            "electrolyte_ksp",
            profile["electrolyte_ksp"],
            low=1.0e-30,
            high=1.0,
        )
        activity_iterations_raw = _bounded_action_float(
            action,
            "equilibrium_max_activity_iterations",
            64.0,
            low=1.0,
            high=128.0,
        )
        precipitation_passes_raw = _bounded_action_float(
            action,
            "equilibrium_max_precipitation_passes",
            3.0,
            low=1.0,
            high=16.0,
        )
        if not activity_iterations_raw.is_integer() or not precipitation_passes_raw.is_integer():
            raise ValueError("equilibrium iteration/pass limits must be integers")
        activity_tolerance = _bounded_action_float(
            action,
            "equilibrium_activity_tolerance",
            1.0e-10,
            low=1.0e-14,
            high=1.0e-3,
        )
        setpoint_history = list(previous_cell_settings.get("setpoint_history", ()))
        setpoint_history.append(
            {
                "setpoint_index": len(setpoint_history) + 1,
                "configured_time_s": state.ledger.time_s,
                "potential_V": potential,
                "current_mA": current,
                "electrolyte_profile": electrolyte_profile,
            }
        )
        equipment = upsert_equipment_record(
            state.equipment,
            equipment_id="electrochemical_cell",
            equipment_type="electrochemical_cell",
            attached_vessel_id=state.vessel_id,
            status="configured",
            settings={
                "potential_V": potential,
                "current_mA": current,
                "electrolyte_profile": electrolyte_profile,
                "electrolyte_profile_id": ELECTROLYTE_PROFILES[electrolyte_profile],
                "electrolyte_profile_model": "bounded_aqueous_electrolyte_profiles_v1",
                "electrolyte_conductivity_S_m": conductivity,
                "electrode_gap_m": electrode_gap,
                "electrode_area_m2": electrode_area,
                "contact_resistance_ohm": contact_resistance,
                "voltage_window_V": voltage_window,
                "diffusivity_m2_s": diffusivity,
                "diffusion_layer_thickness_m": diffusion_layer,
                "double_layer_capacitance_F_m2": capacitance,
                "electrolyte_acid_total_mol": acid_total,
                "electrolyte_acid_pka": acid_pka,
                "supporting_electrolyte_mol": supporting_electrolyte,
                "precipitating_salt_mol": precipitating_salt,
                "electrolyte_ksp": solubility_product,
                "equilibrium_max_activity_iterations": int(activity_iterations_raw),
                "equilibrium_max_precipitation_passes": int(precipitation_passes_raw),
                "equilibrium_activity_tolerance": activity_tolerance,
                "setpoint_history": setpoint_history,
            },
        )
        risk = min(1.0, state.ledger.risk + 0.02 * max(abs(potential) - 1.5, 0.0))
        ledger = state.ledger.with_updates(cost=state.ledger.cost + 0.010, risk=risk)
        return state.replace(ledger=ledger, equipment=equipment)

    def electrolyze(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        duration = _bounded_action_float(action, "duration_s", 900.0, low=1.0, high=14_400.0)
        cell_settings = equipment_settings(state.equipment, "electrochemical_cell")
        if not cell_settings:
            raise ValueError("electrolyze requires a configured electrochemical cell")
        potential = float(cell_settings["potential_V"])
        current_mA = float(cell_settings["current_mA"])
        conductivity = float(cell_settings["electrolyte_conductivity_S_m"])
        if conductivity <= 0.0 or not np.isfinite(conductivity):
            raise ValueError("electrolyze requires a finite positive electrolyte conductivity")
        voltage_window = float(cell_settings["voltage_window_V"])
        if abs(potential) > voltage_window:
            raise ValueError("electrode potential exceeds the configured voltage window")

        try:
            aqueous = solve_aqueous_electrolyte_equilibrium(
                acid_total_mol=float(cell_settings["electrolyte_acid_total_mol"]),
                volume_L=state.volume_L,
                pka=float(cell_settings["electrolyte_acid_pka"]),
                temperature_K=state.temperature_K,
                supporting_electrolyte_mol=float(cell_settings["supporting_electrolyte_mol"]),
                precipitating_salt_mol=float(cell_settings["precipitating_salt_mol"]),
                solubility_product=SolubilityProductSpec(
                    precipitate_id="ElectrolyteSalt(s)",
                    cation_id="Salt+",
                    anion_id="Salt-",
                    ksp=float(cell_settings["electrolyte_ksp"]),
                ),
                max_precipitation_passes=int(cell_settings["equilibrium_max_precipitation_passes"]),
                max_activity_iterations=int(cell_settings["equilibrium_max_activity_iterations"]),
                activity_tolerance=float(cell_settings["equilibrium_activity_tolerance"]),
            )
        except RuntimeError as error:
            raise ValueError(f"electrolyte equilibrium failed closed: {error}") from error
        resistance_multiplier = self.world.domain_parameter("electro_resistance_multiplier")
        resistance = ElectrolyteResistanceSpec(
            electrolyte_conductivity_S_m=float(conductivity / resistance_multiplier),
            electrode_gap_m=float(cell_settings.get("electrode_gap_m", 0.004)),
            electrode_area_m2=float(cell_settings.get("electrode_area_m2", 0.004)),
            contact_resistance_ohm=(
                float(cell_settings.get("contact_resistance_ohm", 0.20)) * resistance_multiplier
            ),
            voltage_window_V=float(cell_settings.get("voltage_window_V", 2.5)),
        )
        species = state.species_amounts.copy()
        reactant = self.species_view.reactant_species(state)
        product = self.species_view.primary_target_species
        impurity = self.species_view.primary_impurity_species
        a_mol = species.get(reactant, 0.0)
        if a_mol <= 0.0 or not np.isfinite(a_mol):
            raise ValueError("electrolyze requires positive finite reactant inventory")
        volume = max(state.volume_L, 1.0e-9)
        reactor_settings = equipment_settings(state.equipment, "batch_reactor")
        catalyst = int(reactor_settings.get("catalyst", 0))
        solvent = int(reactor_settings.get("solvent", 0))
        exchange_current_density = 28.0 * float(self.world.catalyst_effects[catalyst, 0])
        exchange_current_density *= float(self.world.solvent_effects[solvent, 0])
        exchange_current_density *= self.world.domain_parameter(
            "electro_exchange_current_multiplier"
        )
        transfer_asymmetry = self.world.domain_parameter("electro_transfer_asymmetry_multiplier")
        alpha_anodic = 0.5 * transfer_asymmetry
        alpha_cathodic = 1.0 - alpha_anodic
        selectivity_decay = self.world.domain_parameter("electro_selectivity_decay_multiplier")
        standard_potential_multiplier = self.world.domain_parameter(
            "electro_standard_potential_multiplier"
        )
        electrochemical_spec = ElectrodeReactionSpec(
            reaction_id=f"{reactant}_to_{product}_electrochemical",
            electrons_transferred=2.0,
            standard_potential_V=1.05 * standard_potential_multiplier,
            reaction_quotient_exponents={product: 1.0, reactant: -1.0},
            exchange_current_density_A_m2=exchange_current_density,
            electrode_area_m2=float(cell_settings["electrode_area_m2"]),
            alpha_anodic=alpha_anodic,
            alpha_cathodic=alpha_cathodic,
            faradaic_efficiency_ref=0.91,
            product_selectivity_ref=0.90,
            overpotential_selectivity_sensitivity_V_inv=0.45 * selectivity_decay,
        )
        redox_activity_coefficient = aqueous.activity_coefficient_ratio**0.5
        activities = {
            reactant: max(a_mol / volume * redox_activity_coefficient, 1.0e-12),
            product: max(species.get(product, 0.0) / volume, 1.0e-12),
        }
        preliminary = run_electrolysis(
            electrochemical_spec,
            electrode_potential_V=potential,
            duration_s=duration,
            activities=activities,
            available_substrate_mol=a_mol,
            temperature_K=state.temperature_K,
            applied_current_A=current_mA / 1000.0,
            electrolyte_resistance=resistance,
        )
        if abs(preliminary.actual_current_A) <= 1.0e-12:
            raise ValueError("electrochemical driving force produced no executable current")
        charge_transfer_resistance = (
            R_J_PER_MOL_K
            * state.temperature_K
            / (
                electrochemical_spec.electrons_transferred
                * FARADAY_C_PER_MOL
                * max(electrochemical_spec.exchange_current_a, 1.0e-12)
            )
        )
        double_layer = simulate_double_layer_current_step(
            DoubleLayerRCSpec(
                model_id="runtime_randles_double_layer",
                double_layer_capacitance_F_m2=float(cell_settings["double_layer_capacitance_F_m2"]),
                electrode_area_m2=float(cell_settings["electrode_area_m2"]),
                series_resistance_ohm=resistance.total_resistance_ohm,
                charge_transfer_resistance_ohm=charge_transfer_resistance,
                provenance_id="chemworld_runtime_electrochemical_services",
            ),
            current_step_A=preliminary.actual_current_A,
            duration_s=duration,
            sample_interval_s=max(duration / 20.0, 1.0e-6),
        )
        transport = diffusion_layer_current_response(
            DiffusionLayerSpec(
                model_id="runtime_planar_diffusion_layer",
                electrons_transferred=electrochemical_spec.electrons_transferred,
                electrode_area_m2=float(cell_settings["electrode_area_m2"]),
                diffusivity_m2_s=float(cell_settings["diffusivity_m2_s"]),
                diffusion_layer_thickness_m=float(cell_settings["diffusion_layer_thickness_m"]),
                electrolyte_volume_m3=state.volume_L * 1.0e-3,
                provenance_id="chemworld_runtime_electrochemical_services",
            ),
            bulk_concentration_mol_m3=a_mol / (state.volume_L * 1.0e-3),
            applied_current_A=preliminary.actual_current_A,
            duration_s=duration,
            kinetic_current_A=preliminary.kinetic_current_A,
        )
        useful_charge_limit = min(
            abs(double_layer.faradaic_charge_C),
            transport.useful_charge_C,
        )
        result = run_electrolysis(
            electrochemical_spec,
            electrode_potential_V=potential,
            duration_s=duration,
            activities=activities,
            available_substrate_mol=a_mol,
            temperature_K=state.temperature_K,
            applied_current_A=current_mA / 1000.0,
            electrolyte_resistance=resistance,
            useful_charge_limit_C=useful_charge_limit,
            capacitive_charge_C=abs(double_layer.capacitive_charge_C),
        )
        species[reactant] = a_mol - result.converted_mol
        species[product] = species.get(product, 0.0) + result.product_mol
        species[impurity] = species.get(impurity, 0.0) + result.byproduct_mol
        material_balance_residual = abs(
            result.converted_mol - result.product_mol - result.byproduct_mol
        )
        if material_balance_residual > 1.0e-12:
            raise RuntimeError("electrolysis material ledger did not close")
        if abs(result.charge_balance_residual_C) > 1.0e-9:
            raise RuntimeError("electrolysis charge ledger did not close")
        if abs(result.energy_balance_residual_J) > 1.0e-8:
            raise RuntimeError("electrolysis energy ledger did not close")
        process = process_with_metrics(
            state.process,
            electrochemical_selectivity=result.product_selectivity,
            faradaic_efficiency=result.faradaic_efficiency,
            transport_efficiency=float(np.clip(transport.current_efficiency, 0.0, 1.0)),
            ohmic_efficiency=float(
                np.clip(
                    1.0 - result.ohmic_loss_J / max(result.electrical_work_J, 1.0e-12),
                    0.0,
                    1.0,
                )
            ),
            energy_efficiency=result.energy_efficiency,
            equilibrium_potential_V=result.equilibrium_potential_V,
            measured_potential_V=result.measured_potential_V,
            interfacial_potential_V=result.interfacial_potential_V,
            overpotential_V=result.overpotential_V,
            kinetic_current_A=result.kinetic_current_A,
            actual_current_A=result.actual_current_A,
            charge_C=result.charge_C,
            faradaic_charge_C=result.faradaic_charge_C,
            electrical_work_J=result.electrical_work_J,
            interfacial_work_J=result.interfacial_work_J,
            ohmic_loss_J=result.ohmic_loss_J,
            electrolyte_resistance_ohm=result.electrolyte_resistance_ohm,
            contact_resistance_ohm=result.contact_resistance_ohm,
            total_resistance_ohm=result.total_resistance_ohm,
            uncompensated_voltage_drop_V=result.uncompensated_voltage_drop_V,
            voltage_window_exceeded=float(result.voltage_window_exceeded),
            capacitive_charge_C=result.capacitive_charge_C,
            side_reaction_charge_C=result.side_reaction_charge_C,
            charge_balance_residual_C=result.charge_balance_residual_C,
            material_balance_residual_mol=material_balance_residual,
            energy_balance_residual_J=result.energy_balance_residual_J,
            signed_terminal_work_J=result.signed_terminal_work_J,
            signed_interfacial_work_J=result.signed_interfacial_work_J,
            transport_useful_charge_C=transport.useful_charge_C,
            transport_current_efficiency=transport.current_efficiency,
            limiting_current_A=transport.initial_limiting_current_A,
            mass_transfer_limited=float(transport.mass_transfer_limited_initially),
            double_layer_time_constant_s=double_layer.time_constant_s,
            electrolyte_pH=aqueous.acid_base.pH,
            electrolyte_acid_dissociation_fraction=(
                aqueous.acid_base.acid_dissociation_fraction
            ),
            electrolyte_ionic_strength_mol_kg=(aqueous.acid_base.ionic_strength_mol_kg),
            electrolyte_charge_balance_error_eq=aqueous.charge_balance_error_eq,
            electrolyte_material_balance_error_mol=aqueous.material_balance_error_mol,
            electrolyte_precipitated_mol=(aqueous.precipitation.total_precipitated_mol),
            redox_activity_coefficient=redox_activity_coefficient,
        )
        overpotential_risk = max(abs(result.overpotential_V) - 0.35, 0.0)
        ledger = state.ledger.with_updates(
            time_s=state.ledger.time_s + duration,
            cost=state.ledger.cost + 0.018 + result.electrical_work_J / 250_000.0,
            risk=min(
                1.0,
                state.ledger.risk
                + 0.015
                + 0.025 * abs(potential)
                + 0.035 * overpotential_risk
                + 0.020 * float(result.voltage_window_exceeded),
            ),
            energy_jacket_J=state.ledger.energy_jacket_J + result.electrical_work_J,
        )
        equipment = upsert_equipment_record(
            state.equipment,
            equipment_id="electrochemical_cell",
            equipment_type="electrochemical_cell",
            attached_vessel_id=state.vessel_id,
            status="configured",
            settings={
                **cell_settings,
                "electrolysis_history": [
                    *list(cell_settings.get("electrolysis_history", ())),
                    {
                        "execution_index": len(
                            tuple(cell_settings.get("electrolysis_history", ()))
                        )
                        + 1,
                        "start_time_s": state.ledger.time_s,
                        "end_time_s": state.ledger.time_s + duration,
                        "potential_V": potential,
                        "current_mA": current_mA,
                        "electrolyte_profile": int(cell_settings["electrolyte_profile"]),
                    },
                ],
                "runtime_model_ids": (
                    "nernst_butler_volmer_faradaic_v1",
                    transport.model_id,
                    double_layer.model_id,
                    "aqueous_acid_base_ph_observation",
                ),
                "mechanism_id": self.species_view.mechanism.mechanism_id,
                "mechanism_hash": self.species_view.mechanism.mechanism_hash,
                "transport_diagnostic": {
                    "model_id": transport.model_id,
                    "limiting_current_A": transport.initial_limiting_current_A,
                    "current_efficiency": transport.current_efficiency,
                    "charge_balance_residual_C": transport.charge_balance_residual_C,
                    "material_balance_residual_mol": (transport.material_balance_residual_mol),
                    "warnings": transport.warnings,
                },
                "double_layer_diagnostic": {
                    "model_id": double_layer.model_id,
                    "time_constant_s": double_layer.time_constant_s,
                    "faradaic_charge_C": double_layer.faradaic_charge_C,
                    "capacitive_charge_C": double_layer.capacitive_charge_C,
                    "charge_balance_residual_C": (double_layer.charge_balance_residual_C),
                    "warnings": double_layer.warnings,
                },
                "aqueous_equilibrium_diagnostic": {
                    "model_id": "aqueous_acid_base_ph_observation",
                    "converged": aqueous.converged,
                    "iterations": aqueous.iterations,
                    "pH": aqueous.acid_base.pH,
                    "ionic_strength_mol_kg": (aqueous.acid_base.ionic_strength_mol_kg),
                    "charge_balance_error_eq": aqueous.charge_balance_error_eq,
                    "material_balance_error_mol": aqueous.material_balance_error_mol,
                    "precipitated_mol": aqueous.precipitation.total_precipitated_mol,
                    "applicability": aqueous.applicability,
                },
            },
        )
        return state.replace(
            species_amounts=species,
            ledger=ledger,
            process=process,
            equipment=equipment,
        )


__all__ = ["ChemWorldElectrochemicalServices"]
