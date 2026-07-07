"""Phase and partition-law module for ChemWorld."""

from dataclasses import dataclass


@dataclass(frozen=True)
class PhaseModuleSpec:
    module_id: str = "phase_partition"
    version: str = "0.2"
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


__all__ = ["PhaseModuleSpec"]
