"""Phase and partition-law module for ChemWorld."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TypedDict

import numpy as np

from chemworld.physchem.equilibrium import liquid_liquid_split


class PartitionSplitResult(TypedDict):
    partition_coefficient: float
    impurity_partition_coefficient: float
    organic_product_mol: float
    aqueous_product_mol: float
    organic_impurity_mol: float
    aqueous_impurity_mol: float
    lle_phase_status: str
    lle_minimum_tpd_like: float
    lle_partition_log_spread: float


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
) -> PartitionSplitResult:
    partition_base = np.array([0.65, 1.25, 2.20, 1.55])
    temperature_factor = 1.0 + 0.0025 * (temperature_K - 298.15)
    mix_factor = 0.75 + 0.25 * (1.0 - np.exp(-duration_s / 240.0)) * (
        0.70 + 0.30 * stirring_speed_rpm / 1200.0
    )
    partition = max(0.05, float(partition_base[solvent] * temperature_factor * mix_factor))
    v_org = max(organic_volume_L, 1.0e-9)
    v_aq = max(aqueous_volume_L, 1.0e-9)
    impurity_partition = max(0.05, float(0.18 * partition + 0.08 * (solvent + 1)))
    feed = {"product": max(product_mol, 0.0), "impurity": max(impurity_mol, 0.0)}
    if sum(feed.values()) > 0.0:
        split = liquid_liquid_split(
            feed,
            partition_coefficients={
                "product": partition,
                "impurity": impurity_partition,
            },
            aqueous_volume_L=v_aq,
            organic_volume_L=v_org,
            stage_efficiency=float(np.clip(mix_factor, 0.0, 1.0)),
            temperature_K=temperature_K,
            initialization_policy="partition_weighted_runtime",
        )
        organic_product_mol = split.organic_amounts_mol["product"]
        aqueous_product_mol = split.aqueous_amounts_mol["product"]
        organic_impurity_mol = split.organic_amounts_mol["impurity"]
        aqueous_impurity_mol = split.aqueous_amounts_mol["impurity"]
        diagnostic: dict[str, object] = split.stability_diagnostic or {}
    else:
        organic_product_mol = aqueous_product_mol = 0.0
        organic_impurity_mol = aqueous_impurity_mol = 0.0
        diagnostic = {
            "phase_status": "single_liquid",
            "minimum_tpd_like": 0.0,
            "partition_log_spread": 0.0,
        }
    return {
        "partition_coefficient": partition,
        "impurity_partition_coefficient": impurity_partition,
        "organic_product_mol": organic_product_mol,
        "aqueous_product_mol": aqueous_product_mol,
        "organic_impurity_mol": organic_impurity_mol,
        "aqueous_impurity_mol": aqueous_impurity_mol,
        "lle_phase_status": str(diagnostic.get("phase_status", "single_liquid")),
        "lle_minimum_tpd_like": _diagnostic_float(
            diagnostic.get("minimum_tpd_like", 0.0)
        ),
        "lle_partition_log_spread": _diagnostic_float(
            diagnostic.get("partition_log_spread", 0.0)
        ),
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
        "tpd_style_phase_stability_diagnostic",
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


def _diagnostic_float(value: object, default: float = 0.0) -> float:
    return float(value) if isinstance(value, int | float) else default


__all__ = ["PartitionSplitResult", "PhaseModuleSpec", "partition_split"]
