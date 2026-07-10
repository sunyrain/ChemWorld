"""Distillation state-update services for the transactional runtime."""

from __future__ import annotations

from typing import Any

import numpy as np

from chemworld.foundation import WorldState, process_with_metrics, upsert_equipment_record
from chemworld.foundation.state import PhaseLedger, PhaseRecord
from chemworld.physchem.separations import vle_shortcut_distillation
from chemworld.runtime.species import MechanismSpeciesView


def _action_float(action: dict[str, Any], key: str, default: float) -> float:
    value = action.get(key, default)
    return float(np.asarray(value).reshape(-1)[0])


def _distillate_phase_amounts(
    state: WorldState,
    *,
    target_species: tuple[str, ...],
    impurity_species: tuple[str, ...],
) -> tuple[float, float]:
    if state.phases is None or "distillate" not in state.phases.phases:
        return 0.0, 0.0
    distillate = state.phases.phases["distillate"]
    return (
        sum(
            float(distillate.species_amounts_mol.get(species_id, 0.0))
            for species_id in target_species
        ),
        sum(
            float(distillate.species_amounts_mol.get(species_id, 0.0))
            for species_id in impurity_species
        ),
    )


def _allocated_amounts(
    source_amounts: dict[str, float],
    species_ids: tuple[str, ...],
    total_mol: float,
) -> dict[str, float]:
    source_total = sum(
        max(float(source_amounts.get(species_id, 0.0)), 0.0)
        for species_id in species_ids
    )
    allocated_total = min(max(float(total_mol), 0.0), source_total)
    if source_total <= 1.0e-12 or allocated_total <= 0.0:
        return dict.fromkeys(species_ids, 0.0)
    return {
        species_id: allocated_total
        * max(float(source_amounts.get(species_id, 0.0)), 0.0)
        / source_total
        for species_id in species_ids
    }


def _distillation_phases(
    state: WorldState,
    *,
    target_species: tuple[str, ...],
    impurity_species: tuple[str, ...],
    product_mol: float,
    impurity_mol: float,
    distillate_volume_L: float,
    bottoms_volume_L: float,
    solvent_loss: float = 0.0,
    distillate_selected: bool = True,
) -> PhaseLedger:
    distillate_amounts = dict.fromkeys(state.species_amounts, 0.0)
    allocated_targets = _allocated_amounts(
        state.species_amounts,
        target_species,
        product_mol,
    )
    allocated_impurities = _allocated_amounts(
        state.species_amounts,
        impurity_species,
        impurity_mol,
    )
    for species_id, amount_mol in allocated_targets.items():
        distillate_amounts[species_id] = amount_mol
    for species_id, amount_mol in allocated_impurities.items():
        distillate_amounts[species_id] = amount_mol
    bottoms_amounts = state.species_amounts.copy()
    for species_id, amount_mol in distillate_amounts.items():
        bottoms_amounts[species_id] = max(
            bottoms_amounts.get(species_id, 0.0) - amount_mol,
            0.0,
        )
    return PhaseLedger(
        {
            "bottoms": PhaseRecord(
                phase_id="bottoms",
                vessel_id=state.vessel_id,
                phase_type="liquid",
                volume_L=max(bottoms_volume_L, 0.0),
                species_amounts_mol=bottoms_amounts,
                settled=True,
                selected=not distillate_selected,
                metadata={},
            ),
            "distillate": PhaseRecord(
                phase_id="distillate",
                vessel_id=state.vessel_id,
                phase_type="liquid",
                volume_L=max(distillate_volume_L, 0.0),
                species_amounts_mol=distillate_amounts,
                settled=True,
                selected=distillate_selected,
                metadata={},
            ),
        }
    )


class ChemWorldDistillationServices:
    """Apply shortcut distillation and fraction collection updates."""

    def __init__(self, species_view: MechanismSpeciesView) -> None:
        self.species_view = species_view

    def distill(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        duration = float(np.clip(_action_float(action, "duration_s", 1200.0), 0.0, 14_400.0))
        target_temperature = float(
            np.clip(_action_float(action, "target_temperature_K", 345.15), 298.15, 430.0)
        )
        reflux = float(np.clip(_action_float(action, "reflux_ratio", 1.5), 0.0, 10.0))
        target_species = self.species_view.target_species_for_state(state)
        impurity_species = self.species_view.impurity_species_for_state(state)
        p_mol = self.species_view.target_amount(state)
        impurity_mol = self.species_view.impurity_amount(state)
        distillate_cut = float(np.clip(0.25 + duration / 9000.0, 0.05, 0.90))
        theoretical_stages = float(np.clip(2.0 + duration / 900.0, 1.0, 20.0))
        if p_mol + impurity_mol <= 1.0e-12:
            distillate_product = 0.0
            distillate_impurity = 0.0
            distillate_purity = 0.0
            distillation_metadata: dict[str, object] = {"no_distillable_material": True}
            heat_duty = (70.0 + 8.0 * reflux) * duration
            distillation_cost = 0.045 + duration / 3600.0 * (0.065 + 0.012 * reflux)
            distillation_risk = 0.035 + 0.06 * ((target_temperature - 298.15) / 132.0)
        else:
            distillation = vle_shortcut_distillation(
                {"product": p_mol, "impurity": impurity_mol},
                vapor_pressures_Pa={"product": 78_000.0, "impurity": 18_000.0},
                pressure_Pa=max(state.pressure_Pa, 1.0),
                temperature_K=target_temperature,
                light_key="product",
                heavy_key="impurity",
                distillate_cut_fraction=distillate_cut,
                theoretical_stages=theoretical_stages,
                reflux_ratio=reflux,
                stage_efficiency=0.62,
                latent_heats_J_mol={"product": 38_000.0, "impurity": 55_000.0},
            )
            distillate = distillation.outlet("distillate")
            distillate_product = distillate.get("product", 0.0)
            distillate_impurity = distillate.get("impurity", 0.0)
            distillate_purity = distillation.purity("product", "distillate")
            distillation_metadata = distillation.ledger.metadata
            heat_duty = distillation.ledger.heat_duty_J
            distillation_cost = distillation.ledger.cost
            distillation_risk = distillation.ledger.risk
        process_metrics = {} if state.process is None else state.process.metrics
        initial_p = max(
            float(process_metrics.get("pre_separation_product_mol", p_mol)),
            p_mol,
            1.0e-12,
        )
        equipment = upsert_equipment_record(
            state.equipment,
            equipment_id="distillation_column",
            equipment_type="shortcut_distillation_column",
            attached_vessel_id=state.vessel_id,
            status="distilled",
            settings={
                "distillation_model": "vle_shortcut_distillation",
                "distillation_kernel": distillation_metadata,
                "distillate_cut_fraction": distillate_cut,
                "theoretical_stages": theoretical_stages,
                "reflux_ratio": reflux,
            },
        )
        solvent_loss = float(process_metrics.get("solvent_loss", 0.0))
        process = process_with_metrics(
            state.process,
            pre_separation_product_mol=initial_p,
            solvent_loss=solvent_loss,
            distillate_purity=float(np.clip(distillate_purity, 0.0, 1.0)),
            distillate_recovery=float(np.clip(distillate_product / initial_p, 0.0, 1.0)),
        )
        risk = min(1.0, state.ledger.risk + distillation_risk)
        ledger = state.ledger.with_updates(
            time_s=state.ledger.time_s + duration,
            cost=state.ledger.cost + distillation_cost,
            risk=risk,
            energy_jacket_J=state.ledger.energy_jacket_J + heat_duty,
        )
        volume_after_distill = max(state.volume_L * 0.62, 0.001)
        phases = _distillation_phases(
            state,
            target_species=target_species,
            impurity_species=impurity_species,
            product_mol=distillate_product,
            impurity_mol=distillate_impurity,
            distillate_volume_L=volume_after_distill * distillate_cut,
            bottoms_volume_L=volume_after_distill * max(1.0 - distillate_cut, 0.0),
            solvent_loss=solvent_loss,
        )
        return state.replace(
            volume_L=volume_after_distill,
            temperature_K=target_temperature,
            ledger=ledger,
            equipment=equipment,
            process=process,
            phases=phases,
        )

    def collect_fraction(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        fraction = float(np.clip(_action_float(action, "transfer_fraction", 0.90), 0.0, 1.0))
        target_species = self.species_view.target_species_for_state(state)
        impurity_species = self.species_view.impurity_species_for_state(state)
        distillate_product, distillate_impurity = _distillate_phase_amounts(
            state,
            target_species=target_species,
            impurity_species=impurity_species,
        )
        product = distillate_product * fraction
        impurity = distillate_impurity * fraction
        purity = product / max(product + impurity, 1.0e-12)
        process_metrics = {} if state.process is None else state.process.metrics
        target_amount = self.species_view.target_amount(state)
        initial_p = max(
            float(process_metrics.get("pre_separation_product_mol", target_amount)),
            target_amount,
            1.0e-12,
        )
        equipment = upsert_equipment_record(
            state.equipment,
            equipment_id="distillation_column",
            equipment_type="shortcut_distillation_column",
            attached_vessel_id=state.vessel_id,
            status="fraction_collected",
            settings={
                "fraction_collected": True,
                "transfer_fraction": fraction,
                "collected_product_mol": product,
                "collected_impurity_mol": impurity,
                "collected_purity": purity,
            },
        )
        solvent_loss = float(process_metrics.get("solvent_loss", 0.0))
        process = process_with_metrics(
            state.process,
            pre_separation_product_mol=initial_p,
            solvent_loss=solvent_loss,
            distillate_purity=float(np.clip(purity, 0.0, 1.0)),
            distillate_recovery=float(np.clip(product / initial_p, 0.0, 1.0)),
            purity=float(np.clip(purity, 0.0, 1.0)),
            recovery=float(np.clip(product / initial_p, 0.0, 1.0)),
        )
        ledger = state.ledger.with_updates(cost=state.ledger.cost + 0.018)
        phases = _distillation_phases(
            state,
            target_species=target_species,
            impurity_species=impurity_species,
            product_mol=product,
            impurity_mol=impurity,
            distillate_volume_L=state.volume_L * fraction,
            bottoms_volume_L=state.volume_L * max(1.0 - fraction, 0.0),
            solvent_loss=solvent_loss,
        )
        return state.replace(
            volume_L=state.volume_L * fraction,
            ledger=ledger,
            equipment=equipment,
            process=process,
            phases=phases,
        )


__all__ = ["ChemWorldDistillationServices"]
