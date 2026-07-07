"""Crystallization process module for the shared ChemWorld law."""

from __future__ import annotations

from dataclasses import dataclass

from chemworld.core.batch_reactor import CRYSTALLIZATION_OPERATIONS


@dataclass(frozen=True)
class CrystallizationModuleSpec:
    module_id: str = "crystallization"
    version: str = "0.1"
    operations: tuple[str, ...] = CRYSTALLIZATION_OPERATIONS
    laws: tuple[str, ...] = (
        "cooling_driven_supersaturation_proxy",
        "seeded_nucleation_quality_factor",
        "filtration_recovery_loss",
    )

    def to_dict(self) -> dict[str, object]:
        return {
            "module_id": self.module_id,
            "version": self.version,
            "operations": list(self.operations),
            "laws": list(self.laws),
            "tracked_metrics": ["crystal_yield", "crystal_purity", "crystal_size"],
        }


__all__ = ["CrystallizationModuleSpec"]
