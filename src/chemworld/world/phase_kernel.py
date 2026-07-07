"""Phase and partition-law module for ChemWorld."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


def partition_split(
    *,
    product_mol: float,
    impurity_mol: float,
    solvent: int,
    temperature_K: float,
    duration_s: float,
    stirring_speed_rpm: float,
    organic_volume_L: float,
    aqueous_volume_L: float,
) -> dict[str, float]:
    partition_base = np.array([0.65, 1.25, 2.20, 1.55])
    temperature_factor = 1.0 + 0.0025 * (temperature_K - 298.15)
    mix_factor = 0.75 + 0.25 * (1.0 - np.exp(-duration_s / 240.0)) * (
        0.70 + 0.30 * stirring_speed_rpm / 1200.0
    )
    partition = max(0.05, float(partition_base[solvent] * temperature_factor * mix_factor))
    v_org = max(organic_volume_L, 1.0e-9)
    v_aq = max(aqueous_volume_L, 1.0e-9)
    product_organic_fraction = float(
        np.clip(partition * v_org / (v_aq + partition * v_org), 0.0, 1.0)
    )
    impurity_organic_fraction = float(
        np.clip(0.35 * product_organic_fraction + 0.10 * solvent, 0.0, 0.85)
    )
    return {
        "partition_coefficient": partition,
        "organic_product_mol": product_mol * product_organic_fraction,
        "aqueous_product_mol": product_mol * (1.0 - product_organic_fraction),
        "organic_impurity_mol": impurity_mol * impurity_organic_fraction,
        "aqueous_impurity_mol": impurity_mol * (1.0 - impurity_organic_fraction),
    }


@dataclass(frozen=True)
class PhaseModuleSpec:
    module_id: str = "phase_partition"
    version: str = "0.3"
    laws: tuple[str, ...] = (
        "aqueous_organic_phase_volume_balance",
        "partition_coefficient_proxy",
        "solubility_limit_proxy",
        "entrainment_loss_proxy",
    )

    def to_dict(self) -> dict[str, object]:
        return {
            "module_id": self.module_id,
            "version": self.version,
            "laws": list(self.laws),
            "phases": ["reactor_liquid", "aqueous", "organic", "solid"],
            "observable_proxies": [
                "phase_ratio",
                "product_in_organic",
                "product_in_aqueous",
                "solvent_loss",
                "process_mass_balance_error",
            ],
        }


__all__ = ["PhaseModuleSpec", "partition_split"]
