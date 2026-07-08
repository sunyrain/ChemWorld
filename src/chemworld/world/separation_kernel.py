"""Downstream separation-law module for ChemWorld."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from chemworld.foundation import WorldState
from chemworld.world.species_roles import (
    LEGACY_PHASE_PRODUCT_AMOUNT_KEY,
    PHASE_PRODUCT_AMOUNT_KEY,
)


def downstream_truth_values(
    state: WorldState,
    phase_ledger: dict[str, dict[str, float]] | None = None,
    *,
    product_amount_mol: float | None = None,
    impurity_amount_mol: float | None = None,
    initial_product_mol: float | None = None,
) -> dict[str, float]:
    phase_ledger = phase_ledger or dict(state.metadata.get("phase_ledger", {}))
    product_amount = (
        float(product_amount_mol)
        if product_amount_mol is not None
        else state.species_amounts.get("P", 0.0)
    )
    impurity_amount = (
        float(impurity_amount_mol)
        if impurity_amount_mol is not None
        else state.species_amounts.get("B", 0.0)
        + state.species_amounts.get("D", 0.0)
        + state.species_amounts.get("E", 0.0)
    )
    initial_p = max(
        (
            float(initial_product_mol)
            if initial_product_mol is not None
            else float(
                state.metadata.get(
                    "pre_separation_product_mol",
                    state.metadata.get("max_product_mol", product_amount),
                )
            )
        ),
        product_amount,
        1.0e-12,
    )
    organic = phase_ledger.get("organic", {})
    aqueous = phase_ledger.get("aqueous", {})
    selected_phase = str(state.metadata.get("selected_phase") or "organic")
    selected = phase_ledger.get(selected_phase, organic or aqueous or {})
    product_in_organic = float(
        organic.get(PHASE_PRODUCT_AMOUNT_KEY, organic.get(LEGACY_PHASE_PRODUCT_AMOUNT_KEY, 0.0))
    )
    product_in_aqueous = float(
        aqueous.get(PHASE_PRODUCT_AMOUNT_KEY, aqueous.get(LEGACY_PHASE_PRODUCT_AMOUNT_KEY, 0.0))
    )
    selected_product = float(
        selected.get(
            PHASE_PRODUCT_AMOUNT_KEY,
            selected.get(LEGACY_PHASE_PRODUCT_AMOUNT_KEY, product_amount),
        )
    )
    selected_impurity = float(
        selected.get(
            "impurity_mol",
            impurity_amount,
        )
    )
    organic_volume = float(organic.get("volume_L", 0.0))
    aqueous_volume = float(aqueous.get("volume_L", max(state.volume_L - organic_volume, 0.0)))
    total_phase_product = product_in_organic + product_in_aqueous
    purity = selected_product / max(selected_product + selected_impurity, 1.0e-12)
    recovery = selected_product / initial_p
    phase_ratio = organic_volume / max(organic_volume + aqueous_volume, 1.0e-12)
    solvent_loss = float(selected.get("solvent_loss", 0.0))
    mass_balance_error = abs(total_phase_product - product_amount) / initial_p
    return {
        "purity": float(np.clip(purity, 0.0, 1.0)),
        "recovery": float(np.clip(recovery, 0.0, 1.0)),
        "phase_ratio": float(np.clip(phase_ratio, 0.0, 1.0)),
        "product_in_organic": float(np.clip(product_in_organic / initial_p, 0.0, 1.0)),
        "product_in_aqueous": float(np.clip(product_in_aqueous / initial_p, 0.0, 1.0)),
        "impurity_signal": float(np.clip(selected_impurity / initial_p, 0.0, 1.0)),
        "solvent_loss": float(np.clip(solvent_loss, 0.0, 1.0)),
        "process_mass_balance_error": float(np.clip(mass_balance_error, 0.0, 1.0)),
        "crystal_yield": float(np.clip(float(state.metadata.get("crystal_yield", 0.0)), 0.0, 1.0)),
        "crystal_purity": float(
            np.clip(float(state.metadata.get("crystal_purity", 0.0)), 0.0, 1.0)
        ),
        "crystal_size": float(np.clip(float(state.metadata.get("crystal_size", 0.0)), 0.0, 1.0)),
        "distillate_purity": float(
            np.clip(float(state.metadata.get("distillate_purity", 0.0)), 0.0, 1.0)
        ),
        "distillate_recovery": float(
            np.clip(float(state.metadata.get("distillate_recovery", 0.0)), 0.0, 1.0)
        ),
        "flow_conversion": float(
            np.clip(float(state.metadata.get("flow_conversion", 0.0)), 0.0, 1.0)
        ),
        "electrochemical_selectivity": float(
            np.clip(float(state.metadata.get("electrochemical_selectivity", 0.0)), 0.0, 1.0)
        ),
        "energy_efficiency": float(
            np.clip(float(state.metadata.get("energy_efficiency", 0.0)), 0.0, 1.0)
        ),
    }


@dataclass(frozen=True)
class SeparationModuleSpec:
    module_id: str = "separation"
    version: str = "0.3"
    operations: tuple[str, ...] = (
        "add_phase",
        "add_extractant",
        "mix",
        "settle",
        "separate_phase",
        "wash",
        "dry",
        "concentrate",
        "transfer",
    )

    def to_dict(self) -> dict[str, object]:
        return {
            "module_id": self.module_id,
            "version": self.version,
            "operations": list(self.operations),
            "tracked_metrics": [
                "purity",
                "recovery",
                "phase_ratio",
                "process_mass_balance_error",
            ],
        }


__all__ = ["SeparationModuleSpec", "downstream_truth_values"]
