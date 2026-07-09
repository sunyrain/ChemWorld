"""Crystallization state-update helpers for ChemWorld Runtime v2."""

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
                metadata={"solvent_loss": solvent_loss},
            ),
            "solid": PhaseRecord(
                phase_id="solid",
                vessel_id=state.vessel_id,
                phase_type="solid",
                volume_L=0.0,
                species_amounts_mol=solid_amounts,
                settled=True,
                selected=solid_selected,
                metadata={"solvent_loss": 0.0},
            ),
        }
    )


class ChemWorldCrystallizationServices:
    """Apply seed, cooling crystallization, and filtration updates."""

    def __init__(self, species_view: MechanismSpeciesView) -> None:
        self.species_view = species_view

    def seed_crystals(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        seed_mass = float(np.clip(_action_float(action, "seed_mass_g", 0.005), 0.0, 0.050))
        equipment = upsert_equipment_record(
            state.equipment,
            equipment_id="crystallizer",
            equipment_type="crystallizer",
            attached_vessel_id=state.vessel_id,
            status="seeded" if seed_mass > 0.0 else "configured",
            settings={
                "crystal_seeded": seed_mass > 0.0,
                "crystal_seed_mass_g": seed_mass,
                "last_seed_time_s": state.ledger.time_s,
            },
        )
        ledger = state.ledger.with_updates(cost=state.ledger.cost + 0.012 + 0.20 * seed_mass)
        return state.replace(ledger=ledger, equipment=equipment)

    def cool_crystallize(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        duration = float(np.clip(_action_float(action, "duration_s", 1200.0), 0.0, 14_400.0))
        target_temperature = float(
            np.clip(_action_float(action, "target_temperature_K", 278.15), 250.0, 330.0)
        )
        cooling_depth = float(np.clip((state.temperature_K - target_temperature) / 55.0, 0.0, 1.0))
        time_factor = float(np.clip(1.0 - np.exp(-duration / 1800.0), 0.0, 1.0))
        crystallizer_settings = equipment_settings(state.equipment, "crystallizer")
        seed_factor = 1.08 if bool(crystallizer_settings.get("crystal_seeded", False)) else 0.92
        p_mol = self.species_view.target_amount(state)
        impurity_mol = self.species_view.impurity_amount(state)
        crystallized = float(np.clip(p_mol * cooling_depth * time_factor * seed_factor, 0.0, p_mol))
        occluded_impurity = float(
            np.clip(impurity_mol * (0.035 + 0.080 * cooling_depth) * time_factor, 0.0, impurity_mol)
        )
        crystal_purity = crystallized / max(crystallized + occluded_impurity, 1.0e-12)
        process_metrics = {} if state.process is None else state.process.metrics
        initial_p = max(
            float(process_metrics.get("pre_separation_product_mol", p_mol)),
            p_mol,
            1.0e-12,
        )
        process = process_with_metrics(
            state.process,
            pre_separation_product_mol=initial_p,
            crystal_yield=float(np.clip(crystallized / initial_p, 0.0, 1.0)),
            crystal_purity=float(np.clip(crystal_purity, 0.0, 1.0)),
            crystal_size=float(np.clip(0.25 + 0.65 * time_factor * seed_factor, 0.0, 1.0)),
        )
        ledger = state.ledger.with_updates(
            time_s=state.ledger.time_s + duration,
            cost=state.ledger.cost + 0.018 + duration / 3600.0 * 0.018,
            risk=max(0.0, state.ledger.risk - 0.02 * cooling_depth),
        )
        phases = _crystallization_phases(
            state,
            target_species=self.species_view.primary_target_species,
            impurity_species=self.species_view.primary_impurity_species,
            product_mol=crystallized,
            impurity_mol=occluded_impurity,
        )
        return state.replace(
            temperature_K=target_temperature,
            ledger=ledger,
            process=process,
            phases=phases,
        )

    def filter_crystals(self, state: WorldState) -> WorldState:
        metadata = state.metadata.copy()
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
        metadata.update(
            {
                "crystals_filtered": True,
            }
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
        return state.replace(ledger=ledger, metadata=metadata, phases=phases, process=process)


__all__ = ["ChemWorldCrystallizationServices"]
