"""Continuous-flow process module for the shared ChemWorld law."""

from __future__ import annotations

from dataclasses import dataclass

from chemworld.core.batch_reactor import FLOW_OPERATIONS


@dataclass(frozen=True)
class ContinuousFlowModuleSpec:
    module_id: str = "continuous_flow"
    version: str = "0.1"
    operations: tuple[str, ...] = FLOW_OPERATIONS
    laws: tuple[str, ...] = (
        "residence_time_controls_conversion",
        "flow_temperature_controls_safety",
        "semi_batch_state_projection",
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
