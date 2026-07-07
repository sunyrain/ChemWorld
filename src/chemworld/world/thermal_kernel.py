"""Thermal and safety-law module for ChemWorld."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ThermalModuleSpec:
    module_id: str = "thermal"
    version: str = "0.2"
    laws: tuple[str, ...] = (
        "jacket_heat_input",
        "heat_loss_to_environment",
        "reaction_enthalpy",
        "temperature_pressure_risk_proxy",
    )

    def to_dict(self) -> dict[str, object]:
        return {
            "module_id": self.module_id,
            "version": self.version,
            "laws": list(self.laws),
            "state_ledgers": [
                "energy_jacket_J",
                "heat_reaction_J",
                "heat_loss_J",
                "temperature_K",
                "pressure_Pa",
                "risk",
            ],
        }


__all__ = ["ThermalModuleSpec"]
