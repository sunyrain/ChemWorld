"""Downstream separation-law module for ChemWorld."""

from dataclasses import dataclass


@dataclass(frozen=True)
class SeparationModuleSpec:
    module_id: str = "separation"
    version: str = "0.2"
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


__all__ = ["SeparationModuleSpec"]
