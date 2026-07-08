"""Distillation state-update helpers for ChemWorld Runtime v2."""

from __future__ import annotations

from typing import Any

import numpy as np

from chemworld.foundation import WorldState
from chemworld.physchem.separations import vle_shortcut_distillation
from chemworld.runtime.species import MechanismSpeciesView


def _action_float(action: dict[str, Any], key: str, default: float) -> float:
    value = action.get(key, default)
    return float(np.asarray(value).reshape(-1)[0])


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
        initial_p = max(
            float(state.metadata.get("pre_separation_product_mol", p_mol)),
            p_mol,
            1.0e-12,
        )
        metadata = state.metadata.copy()
        metadata.update(
            {
                "distillation_active": True,
                "distillate_product_mol": float(distillate_product),
                "distillate_impurity_mol": float(distillate_impurity),
                "distillate_purity": float(np.clip(distillate_purity, 0.0, 1.0)),
                "distillate_recovery": float(np.clip(distillate_product / initial_p, 0.0, 1.0)),
                "distillation_model": "vle_shortcut_distillation",
                "distillation_kernel": distillation_metadata,
            }
        )
        risk = min(1.0, state.ledger.risk + distillation_risk)
        ledger = state.ledger.with_updates(
            time_s=state.ledger.time_s + duration,
            cost=state.ledger.cost + distillation_cost,
            risk=risk,
            energy_jacket_J=state.ledger.energy_jacket_J + heat_duty,
        )
        return state.replace(
            volume_L=max(state.volume_L * 0.62, 0.001),
            temperature_K=target_temperature,
            ledger=ledger,
            metadata=metadata,
        )

    def collect_fraction(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        fraction = float(np.clip(_action_float(action, "transfer_fraction", 0.90), 0.0, 1.0))
        product = float(state.metadata.get("distillate_product_mol", 0.0)) * fraction
        impurity = float(state.metadata.get("distillate_impurity_mol", 0.0)) * fraction
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
        metadata = state.metadata.copy()
        metadata.update(
            {
                "selected_phase": "distillate",
                "fraction_collected": True,
                "distillate_product_mol": product,
                "distillate_impurity_mol": impurity,
                "distillate_purity": float(np.clip(purity, 0.0, 1.0)),
                "distillate_recovery": float(np.clip(product / initial_p, 0.0, 1.0)),
                "purity": float(np.clip(purity, 0.0, 1.0)),
                "recovery": float(np.clip(product / initial_p, 0.0, 1.0)),
            }
        )
        ledger = state.ledger.with_updates(cost=state.ledger.cost + 0.018)
        return state.replace(volume_L=state.volume_L * fraction, ledger=ledger, metadata=metadata)


__all__ = ["ChemWorldDistillationServices"]
