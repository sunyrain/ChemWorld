"""Continuous-flow process module for the shared ChemWorld law."""

from __future__ import annotations

from dataclasses import dataclass

from chemworld.world.operations import FLOW_OPERATIONS


@dataclass(frozen=True)
class ContinuousFlowModuleSpec:
    module_id: str = "continuous_flow"
    version: str = "0.2"
    operations: tuple[str, ...] = FLOW_OPERATIONS
    laws: tuple[str, ...] = (
        "compiled_network_pfr_residence_time",
        "geometry_resolved_axial_profile",
        "darcy_weisbach_pressure_drop",
        "distributed_thermal_boundary",
        "material_and_energy_ledgers",
    )

    def to_dict(self) -> dict[str, object]:
        return {
            "module_id": self.module_id,
            "version": self.version,
            "operations": list(self.operations),
            "laws": list(self.laws),
            "tracked_metrics": ["flow_conversion", "yield", "safety_risk"],
        }


__all__ = ["ContinuousFlowModuleSpec"]
