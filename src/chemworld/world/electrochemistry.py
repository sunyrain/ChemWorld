"""Electrochemistry process module for the shared ChemWorld law."""

from __future__ import annotations

from dataclasses import dataclass

from chemworld.world.operations import ELECTROCHEMISTRY_OPERATIONS


@dataclass(frozen=True)
class ElectrochemistryModuleSpec:
    module_id: str = "electrochemistry"
    version: str = "0.1"
    operations: tuple[str, ...] = ELECTROCHEMISTRY_OPERATIONS
    laws: tuple[str, ...] = (
        "charge_controls_conversion_proxy",
        "potential_controls_selectivity",
        "electrical_energy_efficiency",
    )

    def to_dict(self) -> dict[str, object]:
        return {
            "module_id": self.module_id,
            "version": self.version,
            "operations": list(self.operations),
            "laws": list(self.laws),
            "tracked_metrics": [
                "electrochemical_selectivity",
                "energy_efficiency",
                "yield",
            ],
        }


__all__ = ["ElectrochemistryModuleSpec"]
