"""Shared reactor contracts and lightweight validation helpers."""

from __future__ import annotations

from dataclasses import dataclass, field
from math import isfinite
from typing import Literal

SteadyStateStability = Literal["stable", "unstable", "marginal"]
JacketInterpolationMode = Literal["step", "linear"]


@dataclass(frozen=True)
class HeatTransferSpec:
    rho_cp_J_per_L_K: float = 4180.0
    ua_W_per_K: float = 0.0
    environment_temperature_K: float = 298.15
    jacket_ua_W_per_K: float = 0.0
    jacket_temperature_K: float | None = None
    fixed_heat_W: float = 0.0

    def __post_init__(self) -> None:
        if self.rho_cp_J_per_L_K <= 0:
            raise ValueError("rho_cp_J_per_L_K must be positive")
        if self.ua_W_per_K < 0 or self.jacket_ua_W_per_K < 0:
            raise ValueError("Heat-transfer coefficients cannot be negative")
        if self.environment_temperature_K <= 0:
            raise ValueError("environment_temperature_K must be positive")
        if self.jacket_temperature_K is not None and self.jacket_temperature_K <= 0:
            raise ValueError("jacket_temperature_K must be positive")

    def jacket_heat_w(self, temperature_K: float) -> float:
        jacket = 0.0
        if self.jacket_temperature_K is not None:
            jacket = self.jacket_ua_W_per_K * (self.jacket_temperature_K - temperature_K)
        return self.fixed_heat_W + jacket

    def heat_loss_w(self, temperature_K: float) -> float:
        return self.ua_W_per_K * (temperature_K - self.environment_temperature_K)


@dataclass(frozen=True)
class JacketTemperatureProgram:
    """Time-dependent jacket setpoint for dynamic batch energy balances."""

    setpoints: tuple[tuple[float, float], ...]
    mode: JacketInterpolationMode = "step"

    def __post_init__(self) -> None:
        if not self.setpoints:
            raise ValueError("jacket setpoints cannot be empty")
        previous_time = -1.0
        for time_s, temperature_K in self.setpoints:
            if time_s < 0:
                raise ValueError("jacket setpoint times cannot be negative")
            if time_s < previous_time:
                raise ValueError("jacket setpoints must be sorted by time")
            if temperature_K <= 0:
                raise ValueError("jacket setpoint temperatures must be positive")
            previous_time = time_s
        if self.mode not in {"step", "linear"}:
            raise ValueError("jacket program mode must be 'step' or 'linear'")

    def temperature_at(self, time_s: float) -> float:
        if time_s <= self.setpoints[0][0]:
            return float(self.setpoints[0][1])
        for (left_time, left_temperature), (
            right_time,
            right_temperature,
        ) in zip(self.setpoints, self.setpoints[1:], strict=False):
            if left_time <= time_s <= right_time:
                if self.mode == "step" or right_time == left_time:
                    return float(left_temperature)
                fraction = (time_s - left_time) / (right_time - left_time)
                return float(
                    left_temperature
                    + fraction * (right_temperature - left_temperature)
                )
        return float(self.setpoints[-1][1])

    def to_dict(self) -> dict[str, object]:
        return {
            "setpoints": [
                {"time_s": time_s, "temperature_K": temperature_K}
                for time_s, temperature_K in self.setpoints
            ],
            "mode": self.mode,
        }


@dataclass(frozen=True)
class FeedStreamSpec:
    species_flows_mol_s: dict[str, float]
    volumetric_flow_L_s: float
    temperature_K: float = 298.15

    def __post_init__(self) -> None:
        if self.volumetric_flow_L_s < 0:
            raise ValueError("volumetric_flow_L_s cannot be negative")
        if self.temperature_K <= 0:
            raise ValueError("temperature_K must be positive")
        if any(value < 0 for value in self.species_flows_mol_s.values()):
            raise ValueError("species flows cannot be negative")

    def flow_for(self, species_id: str) -> float:
        return float(self.species_flows_mol_s.get(species_id, 0.0))


@dataclass(frozen=True)
class SemiBatchFeedSpec:
    stream: FeedStreamSpec
    start_s: float = 0.0
    end_s: float = 0.0

    def __post_init__(self) -> None:
        if self.start_s < 0 or self.end_s < 0:
            raise ValueError("feed times cannot be negative")
        if self.end_s < self.start_s:
            raise ValueError("end_s cannot be earlier than start_s")

    def is_active(self, time_s: float) -> bool:
        return self.start_s <= time_s <= self.end_s

    def species_flow(self, species_id: str, time_s: float) -> float:
        if not self.is_active(time_s):
            return 0.0
        return self.stream.flow_for(species_id)

    def volumetric_flow(self, time_s: float) -> float:
        if not self.is_active(time_s):
            return 0.0
        return self.stream.volumetric_flow_L_s


@dataclass(frozen=True)
class SamplingEventSpec:
    """A well-mixed destructive sample removed from a dynamic batch reactor."""

    time_s: float
    volume_L: float
    label: str = "sample"

    def __post_init__(self) -> None:
        if self.time_s < 0:
            raise ValueError("sampling time_s cannot be negative")
        if self.volume_L <= 0:
            raise ValueError("sampling volume_L must be positive")
        if not self.label.strip():
            raise ValueError("sampling label cannot be empty")

    def to_dict(self) -> dict[str, object]:
        return {
            "time_s": self.time_s,
            "volume_L": self.volume_L,
            "label": self.label,
        }


@dataclass(frozen=True)
class ReactorState:
    amounts_mol: dict[str, float]
    volume_L: float
    temperature_K: float
    time_s: float
    energy_jacket_J: float = 0.0
    heat_reaction_J: float = 0.0
    heat_loss_J: float = 0.0
    material_in_mol: dict[str, float] = field(default_factory=dict)
    material_out_mol: dict[str, float] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.volume_L <= 0:
            raise ValueError("volume_L must be positive")
        if self.temperature_K <= 0:
            raise ValueError("temperature_K must be positive")
        if self.time_s < 0:
            raise ValueError("time_s cannot be negative")
        for label, values in {
            "amounts_mol": self.amounts_mol,
            "material_in_mol": self.material_in_mol,
            "material_out_mol": self.material_out_mol,
        }.items():
            if any(value < -1e-12 for value in values.values()):
                raise ValueError(f"{label} cannot contain negative amounts")

    def to_dict(self) -> dict[str, object]:
        return {
            "amounts_mol": dict(self.amounts_mol),
            "volume_L": self.volume_L,
            "temperature_K": self.temperature_K,
            "time_s": self.time_s,
            "energy_jacket_J": self.energy_jacket_J,
            "heat_reaction_J": self.heat_reaction_J,
            "heat_loss_J": self.heat_loss_J,
            "material_in_mol": dict(self.material_in_mol),
            "material_out_mol": dict(self.material_out_mol),
        }


@dataclass(frozen=True)
class ReactorResult:
    reactor_id: str
    model_id: str
    network_id: str
    initial_state: ReactorState
    final_state: ReactorState
    times_s: tuple[float, ...]
    amounts_mol: dict[str, tuple[float, ...]]
    temperatures_K: tuple[float, ...]
    material_balance_error_mol: float
    metadata: dict[str, object] = field(default_factory=dict)

    @property
    def diagnostics(self) -> ReactorDiagnostics:
        """Return deterministic conservation, positivity, and energy-ledger checks."""

        trajectory_values = [value for values in self.amounts_mol.values() for value in values]
        minimum_amount = min(trajectory_values, default=0.0)
        warnings: list[str] = []
        if minimum_amount < -1.0e-10:
            warnings.append("negative_species_amount")
        if self.material_balance_error_mol > 1.0e-8:
            warnings.append("material_balance_residual_exceeds_tolerance")
        return ReactorDiagnostics(
            material_balance_error_mol=self.material_balance_error_mol,
            minimum_species_amount_mol=float(minimum_amount),
            nonnegative_species=minimum_amount >= -1.0e-10,
            energy_ledger_net_J=(
                self.final_state.energy_jacket_J
                + self.final_state.heat_reaction_J
                - self.final_state.heat_loss_J
            ),
            warnings=tuple(warnings),
        )

    def conversion(self, reactant_id: str) -> float:
        initial = self.initial_state.amounts_mol.get(reactant_id, 0.0)
        final = self.final_state.amounts_mol.get(reactant_id, 0.0)
        if initial <= 0:
            return 0.0
        return max(0.0, min(1.0, (initial - final) / initial))

    def yield_on(self, product_id: str, reactant_id: str) -> float:
        initial_reactant = self.initial_state.amounts_mol.get(reactant_id, 0.0)
        final_product = self.final_state.amounts_mol.get(product_id, 0.0)
        initial_product = self.initial_state.amounts_mol.get(product_id, 0.0)
        if initial_reactant <= 0:
            return 0.0
        return max(0.0, (final_product - initial_product) / initial_reactant)

    def to_dict(self) -> dict[str, object]:
        return {
            "reactor_id": self.reactor_id,
            "model_id": self.model_id,
            "network_id": self.network_id,
            "initial_state": self.initial_state.to_dict(),
            "final_state": self.final_state.to_dict(),
            "times_s": list(self.times_s),
            "amounts_mol": {
                species_id: list(values) for species_id, values in self.amounts_mol.items()
            },
            "temperatures_K": list(self.temperatures_K),
            "material_balance_error_mol": self.material_balance_error_mol,
            "diagnostics": self.diagnostics.to_dict(),
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True)
class ReactorDiagnostics:
    """Machine-readable checks attached to every reactor result."""

    material_balance_error_mol: float
    minimum_species_amount_mol: float
    nonnegative_species: bool
    energy_ledger_net_J: float
    warnings: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, object]:
        return {
            "material_balance_error_mol": self.material_balance_error_mol,
            "minimum_species_amount_mol": self.minimum_species_amount_mol,
            "nonnegative_species": self.nonnegative_species,
            "energy_ledger_net_J": self.energy_ledger_net_J,
            "warnings": list(self.warnings),
        }


def _positive(value: float, name: str) -> None:
    if value <= 0 or not isfinite(value):
        raise ValueError(f"{name} must be finite and positive")


__all__ = [
    "FeedStreamSpec",
    "HeatTransferSpec",
    "JacketInterpolationMode",
    "JacketTemperatureProgram",
    "ReactorDiagnostics",
    "ReactorResult",
    "ReactorState",
    "SamplingEventSpec",
    "SemiBatchFeedSpec",
    "SteadyStateStability",
]
