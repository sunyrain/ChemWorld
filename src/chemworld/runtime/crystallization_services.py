"""Crystallization state-update helpers for ChemWorld Runtime v2."""

from __future__ import annotations

from typing import Any

import numpy as np

from chemworld.foundation import WorldState
from chemworld.runtime.species import MechanismSpeciesView


def _action_float(action: dict[str, Any], key: str, default: float) -> float:
    value = action.get(key, default)
    return float(np.asarray(value).reshape(-1)[0])


class ChemWorldCrystallizationServices:
    """Apply seed, cooling crystallization, and filtration updates."""

    def __init__(self, species_view: MechanismSpeciesView) -> None:
        self.species_view = species_view

    def seed_crystals(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        seed_mass = float(np.clip(_action_float(action, "seed_mass_g", 0.005), 0.0, 0.050))
        metadata = state.metadata.copy()
        metadata["crystal_seeded"] = seed_mass > 0.0
        metadata["crystal_seed_mass_g"] = seed_mass
        ledger = state.ledger.with_updates(cost=state.ledger.cost + 0.012 + 0.20 * seed_mass)
        return state.replace(ledger=ledger, metadata=metadata)

    def cool_crystallize(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        duration = float(np.clip(_action_float(action, "duration_s", 1200.0), 0.0, 14_400.0))
        target_temperature = float(
            np.clip(_action_float(action, "target_temperature_K", 278.15), 250.0, 330.0)
        )
        cooling_depth = float(np.clip((state.temperature_K - target_temperature) / 55.0, 0.0, 1.0))
        time_factor = float(np.clip(1.0 - np.exp(-duration / 1800.0), 0.0, 1.0))
        seed_factor = 1.08 if bool(state.metadata.get("crystal_seeded", False)) else 0.92
        p_mol = self.species_view.target_amount(state)
        impurity_mol = self.species_view.impurity_amount(state)
        crystallized = float(np.clip(p_mol * cooling_depth * time_factor * seed_factor, 0.0, p_mol))
        occluded_impurity = float(
            np.clip(impurity_mol * (0.035 + 0.080 * cooling_depth) * time_factor, 0.0, impurity_mol)
        )
        crystal_purity = crystallized / max(crystallized + occluded_impurity, 1.0e-12)
        initial_p = max(
            float(state.metadata.get("pre_separation_product_mol", p_mol)),
            p_mol,
            1.0e-12,
        )
        metadata = state.metadata.copy()
        metadata.update(
            {
                "crystallization_active": True,
                "crystal_product_mol": crystallized,
                "crystal_impurity_mol": occluded_impurity,
                "crystal_yield": float(np.clip(crystallized / initial_p, 0.0, 1.0)),
                "crystal_purity": float(np.clip(crystal_purity, 0.0, 1.0)),
                "crystal_size": float(np.clip(0.25 + 0.65 * time_factor * seed_factor, 0.0, 1.0)),
            }
        )
        ledger = state.ledger.with_updates(
            time_s=state.ledger.time_s + duration,
            cost=state.ledger.cost + 0.018 + duration / 3600.0 * 0.018,
            risk=max(0.0, state.ledger.risk - 0.02 * cooling_depth),
        )
        return state.replace(temperature_K=target_temperature, ledger=ledger, metadata=metadata)

    def filter_crystals(self, state: WorldState) -> WorldState:
        metadata = state.metadata.copy()
        product = float(metadata.get("crystal_product_mol", 0.0)) * 0.96
        impurity = float(metadata.get("crystal_impurity_mol", 0.0)) * 0.92
        purity = product / max(product + impurity, 1.0e-12)
        initial_p = max(
            float(
                state.metadata.get(
                    "pre_separation_product_mol",
                    self.species_view.target_amount(state),
                )
            ),
            self.species_view.target_amount(state),
            1.0e-12,
        )
        metadata.update(
            {
                "selected_phase": "solid",
                "crystals_filtered": True,
                "crystal_product_mol": product,
                "crystal_impurity_mol": impurity,
                "crystal_yield": float(np.clip(product / initial_p, 0.0, 1.0)),
                "crystal_purity": float(np.clip(purity, 0.0, 1.0)),
                "recovery": float(np.clip(product / initial_p, 0.0, 1.0)),
                "purity": float(np.clip(purity, 0.0, 1.0)),
                "solvent_loss": min(1.0, float(metadata.get("solvent_loss", 0.0)) + 0.04),
            }
        )
        ledger = state.ledger.with_updates(
            time_s=state.ledger.time_s + 480.0,
            cost=state.ledger.cost + 0.026,
        )
        return state.replace(ledger=ledger, metadata=metadata)


__all__ = ["ChemWorldCrystallizationServices"]
