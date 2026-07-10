"""Crystallization state-update services for the transactional runtime."""

from __future__ import annotations

from typing import Any

import numpy as np

from chemworld.foundation import (
    WorldState,
    equipment_settings,
    process_with_metrics,
    upsert_equipment_record,
)
from chemworld.foundation.state import PhaseLedger, PhaseRecord
from chemworld.physchem.crystallization_units import (
    CrystallizationKineticsSpec,
    SolubilityCurveSpec,
    cooling_crystallization,
)
from chemworld.physchem.elements import molecular_weight
from chemworld.runtime.species import MechanismSpeciesView


def _action_float(action: dict[str, Any], key: str, default: float) -> float:
    value = action.get(key, default)
    return float(np.asarray(value).reshape(-1)[0])


def _solid_phase_amounts(
    state: WorldState,
    *,
    target_species: str,
    impurity_species: str,
) -> tuple[float, float]:
    if state.phases is None or "solid" not in state.phases.phases:
        return 0.0, 0.0
    solid = state.phases.phases["solid"]
    return (
        float(solid.species_amounts_mol.get(target_species, 0.0)),
        float(solid.species_amounts_mol.get(impurity_species, 0.0)),
    )


def _crystallization_phases(
    state: WorldState,
    *,
    target_species: str,
    impurity_species: str,
    product_mol: float,
    impurity_mol: float,
    mother_liquor_volume_L: float | None = None,
    solvent_loss: float = 0.0,
    solid_selected: bool = True,
) -> PhaseLedger:
    mother_liquor_volume = (
        state.volume_L if mother_liquor_volume_L is None else mother_liquor_volume_L
    )
    product_mol = float(np.clip(product_mol, 0.0, state.species_amounts.get(target_species, 0.0)))
    impurity_mol = float(
        np.clip(impurity_mol, 0.0, state.species_amounts.get(impurity_species, 0.0))
    )
    solid_amounts = dict.fromkeys(state.species_amounts, 0.0)
    solid_amounts[target_species] = product_mol
    solid_amounts[impurity_species] = impurity_mol
    liquor_amounts = state.species_amounts.copy()
    liquor_amounts[target_species] = max(
        liquor_amounts.get(target_species, 0.0) - product_mol,
        0.0,
    )
    liquor_amounts[impurity_species] = max(
        liquor_amounts.get(impurity_species, 0.0) - impurity_mol,
        0.0,
    )
    return PhaseLedger(
        {
            "mother_liquor": PhaseRecord(
                phase_id="mother_liquor",
                vessel_id=state.vessel_id,
                phase_type="liquid",
                volume_L=mother_liquor_volume,
                species_amounts_mol=liquor_amounts,
                settled=True,
                selected=not solid_selected,
                metadata={},
            ),
            "solid": PhaseRecord(
                phase_id="solid",
                vessel_id=state.vessel_id,
                phase_type="solid",
                volume_L=0.0,
                species_amounts_mol=solid_amounts,
                settled=True,
                selected=solid_selected,
                metadata={},
            ),
        }
    )


class ChemWorldCrystallizationServices:
    """Apply seed, cooling crystallization, and filtration updates."""

    def __init__(self, species_view: MechanismSpeciesView) -> None:
        self.species_view = species_view

    def _target_molecular_weight_kg_mol(self) -> float:
        target = self.species_view.primary_target_species
        species = self.species_view.mechanism.network.species[
            self.species_view.mechanism.network.species_index[target]
        ]
        return molecular_weight(species.composition) / 1000.0

    def seed_crystals(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        seed_mass = float(np.clip(_action_float(action, "seed_mass_g", 0.005), 0.0, 0.050))
        target_species = self.species_view.primary_target_species
        impurity_species = self.species_view.primary_impurity_species
        seed_target_mol = seed_mass / 1000.0 / self._target_molecular_weight_kg_mol()
        species_amounts = state.species_amounts.copy()
        species_amounts[target_species] = (
            species_amounts.get(target_species, 0.0) + seed_target_mol
        )
        augmented_state = state.replace(species_amounts=species_amounts)
        phases = _crystallization_phases(
            augmented_state,
            target_species=target_species,
            impurity_species=impurity_species,
            product_mol=seed_target_mol,
            impurity_mol=0.0,
            solid_selected=False,
        )
        equipment = upsert_equipment_record(
            augmented_state.equipment,
            equipment_id="crystallizer",
            equipment_type="crystallizer",
            attached_vessel_id=augmented_state.vessel_id,
            status="seeded" if seed_mass > 0.0 else "configured",
            settings={
                "crystal_seeded": seed_mass > 0.0,
                "crystal_seed_mass_g": seed_mass,
                "seed_target_mol": seed_target_mol,
                "last_seed_time_s": augmented_state.ledger.time_s,
                "seed_model_id": "explicit_target_seed_mass_v1",
            },
        )
        process_metrics = {} if state.process is None else state.process.metrics
        initial_target = max(
            float(
                process_metrics.get(
                    "pre_separation_product_mol",
                    self.species_view.target_amount(state),
                )
            ),
            self.species_view.target_amount(state),
            1.0e-12,
        )
        process = process_with_metrics(
            augmented_state.process,
            pre_separation_product_mol=initial_target,
        )
        ledger = augmented_state.ledger.with_updates(
            cost=augmented_state.ledger.cost + 0.012 + 0.20 * seed_mass
        )
        return augmented_state.replace(
            ledger=ledger,
            equipment=equipment,
            phases=phases,
            process=process,
        )

    def cool_crystallize(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        duration = float(np.clip(_action_float(action, "duration_s", 1200.0), 0.0, 14_400.0))
        target_temperature = float(
            np.clip(_action_float(action, "target_temperature_K", 278.15), 250.0, 330.0)
        )
        crystallizer_settings = equipment_settings(state.equipment, "crystallizer")
        target_species = self.species_view.primary_target_species
        impurity_species = self.species_view.primary_impurity_species
        seed_mass_g = float(crystallizer_settings.get("crystal_seed_mass_g", 0.0))
        seed_target_mol = float(crystallizer_settings.get("seed_target_mol", 0.0))
        p_mol = self.species_view.target_amount(state)
        dissolved_product_mol = max(p_mol - seed_target_mol, 0.0)
        impurity_mol = self.species_view.impurity_amount(state)
        target_molecular_weight = self._target_molecular_weight_kg_mol()
        initial_concentration = dissolved_product_mol / max(state.volume_L, 1.0e-12)
        solubility = SolubilityCurveSpec(
            model_id="runtime_vanthoff_target_solubility_v1",
            reference_solubility_mol_L=max(initial_concentration, 1.0e-9),
            reference_temperature_K=state.temperature_K,
            dissolution_enthalpy_J_mol=20_000.0,
            minimum_temperature_K=250.0,
            maximum_temperature_K=430.0,
            provenance_id="chemworld-world-law-v0.2-solubility-policy",
        )
        kinetics = CrystallizationKineticsSpec(
            model_id="runtime_cooling_population_balance_v1",
            primary_nucleation_coefficient_per_L_s=2.0e7,
            primary_nucleation_exponent=2.0,
            growth_coefficient_m_s=2.0e-8,
            growth_exponent=1.0,
            crystal_density_kg_m3=1200.0,
            target_molecular_weight_kg_mol=target_molecular_weight,
            nucleus_diameter_m=8.0e-6,
            impurity_occlusion_mol_per_mol=0.02,
            supersaturation_occlusion_factor=0.5,
            fines_threshold_m=20.0e-6,
            provenance_id="chemworld-world-law-v0.2-crystallization-kinetics",
        )
        result = cooling_crystallization(
            {
                target_species: dissolved_product_mol,
                impurity_species: impurity_mol,
            },
            target_component=target_species,
            impurity_component=impurity_species,
            solvent_volume_L=max(state.volume_L, 1.0e-9),
            initial_temperature_K=state.temperature_K,
            final_temperature_K=target_temperature,
            duration_s=max(duration, 1.0e-9),
            solubility_curve=solubility,
            kinetics=kinetics,
            seed_mass_g=seed_mass_g,
            seed_diameter_m=100.0e-6,
            time_steps=max(24, min(120, round(duration / 30.0))),
        )
        crystallized = result.crystals_amounts_mol[target_species]
        occluded_impurity = result.crystals_amounts_mol[impurity_species]
        process_metrics = {} if state.process is None else state.process.metrics
        initial_p = max(
            float(process_metrics.get("pre_separation_product_mol", dissolved_product_mol)),
            dissolved_product_mol,
            1.0e-12,
        )
        process = process_with_metrics(
            state.process,
            pre_separation_product_mol=initial_p,
            crystal_yield=float(np.clip(result.target_recovery, 0.0, 1.0)),
            crystal_purity=float(np.clip(result.crystal_purity, 0.0, 1.0)),
            crystal_size=float(
                np.clip(result.crystal_size_distribution.d50_m / 250.0e-6, 0.0, 1.0)
            ),
        )
        cooling_depth = float(
            np.clip((state.temperature_K - target_temperature) / 55.0, 0.0, 1.0)
        )
        ledger = state.ledger.with_updates(
            time_s=state.ledger.time_s + duration,
            cost=state.ledger.cost + 0.018 + duration / 3600.0 * 0.018,
            risk=max(0.0, state.ledger.risk - 0.02 * cooling_depth),
        )
        phases = _crystallization_phases(
            state,
            target_species=target_species,
            impurity_species=impurity_species,
            product_mol=crystallized,
            impurity_mol=occluded_impurity,
        )
        equipment = upsert_equipment_record(
            state.equipment,
            equipment_id="crystallizer",
            equipment_type="crystallizer",
            attached_vessel_id=state.vessel_id,
            status="completed",
            settings={
                "crystallization_model_id": result.model_id,
                "solubility_model_id": solubility.model_id,
                "kinetics_model_id": kinetics.model_id,
                "material_balance_error_mol": result.material_balance_error_mol,
                "maximum_supersaturation_ratio": result.maximum_supersaturation_ratio,
                "final_supersaturation_ratio": result.final_supersaturation_ratio,
                "csd_d10_m": result.crystal_size_distribution.d10_m,
                "csd_d50_m": result.crystal_size_distribution.d50_m,
                "csd_d90_m": result.crystal_size_distribution.d90_m,
                "csd_cv": result.crystal_size_distribution.coefficient_of_variation,
                "csd_fines_number_fraction": (
                    result.crystal_size_distribution.fines_number_fraction
                ),
                "model_warnings": list(result.warnings),
                "provenance": result.provenance,
            },
        )
        return state.replace(
            temperature_K=target_temperature,
            ledger=ledger,
            process=process,
            phases=phases,
            equipment=equipment,
        )

    def filter_crystals(self, state: WorldState) -> WorldState:
        target_species = self.species_view.primary_target_species
        impurity_species = self.species_view.primary_impurity_species
        solid_product, solid_impurity = _solid_phase_amounts(
            state,
            target_species=target_species,
            impurity_species=impurity_species,
        )
        product = solid_product * 0.96
        impurity = solid_impurity * 0.92
        purity = product / max(product + impurity, 1.0e-12)
        process_metrics = {} if state.process is None else state.process.metrics
        target_amount = self.species_view.target_amount(state)
        initial_p = max(
            float(process_metrics.get("pre_separation_product_mol", target_amount)),
            target_amount,
            1.0e-12,
        )
        solvent_loss = min(
            1.0,
            float(process_metrics.get("solvent_loss", 0.0)) + 0.04,
        )
        equipment = upsert_equipment_record(
            state.equipment,
            equipment_id="crystal_filter",
            equipment_type="solid_liquid_filter",
            attached_vessel_id=state.vessel_id,
            status="completed",
            settings={
                "crystals_filtered": True,
                "filtered_product_mol": product,
                "filtered_impurity_mol": impurity,
                "filter_purity": purity,
            },
        )
        process = process_with_metrics(
            state.process,
            pre_separation_product_mol=initial_p,
            solvent_loss=solvent_loss,
            crystal_yield=float(np.clip(product / initial_p, 0.0, 1.0)),
            crystal_purity=float(np.clip(purity, 0.0, 1.0)),
            recovery=float(np.clip(product / initial_p, 0.0, 1.0)),
            purity=float(np.clip(purity, 0.0, 1.0)),
        )
        ledger = state.ledger.with_updates(
            time_s=state.ledger.time_s + 480.0,
            cost=state.ledger.cost + 0.026,
        )
        phases = _crystallization_phases(
            state,
            target_species=target_species,
            impurity_species=impurity_species,
            product_mol=product,
            impurity_mol=impurity,
            mother_liquor_volume_L=state.volume_L * 0.92,
            solvent_loss=solvent_loss,
        )
        return state.replace(
            ledger=ledger,
            phases=phases,
            process=process,
            equipment=equipment,
        )


__all__ = ["ChemWorldCrystallizationServices"]
