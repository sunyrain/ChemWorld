"""Hidden state, public observations, and experiment ledger."""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Any


@dataclass(frozen=True)
class Ledger:
    time_s: float = 0.0
    cost: float = 0.0
    risk: float = 0.0
    sample_consumed_L: float = 0.0
    energy_jacket_J: float = 0.0
    heat_reaction_J: float = 0.0
    heat_loss_J: float = 0.0

    def with_updates(self, **updates: float) -> Ledger:
        return replace(self, **updates)

    def to_dict(self) -> dict[str, float]:
        return self.__dict__.copy()


@dataclass(frozen=True)
class WorldState:
    species_amounts: dict[str, float]
    volume_L: float
    temperature_K: float
    pressure_Pa: float
    phase: str
    vessel_id: str
    terminated: bool = False
    quenched: bool = False
    ledger: Ledger = field(default_factory=Ledger)
    units: dict[str, str] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self, *, include_hidden: bool = True) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "volume_L": self.volume_L,
            "temperature_K": self.temperature_K,
            "pressure_Pa": self.pressure_Pa,
            "phase": self.phase,
            "vessel_id": self.vessel_id,
            "terminated": self.terminated,
            "quenched": self.quenched,
            "ledger": self.ledger.to_dict(),
            "units": self.units,
            "metadata": self.metadata,
        }
        if include_hidden:
            payload["species_amounts"] = self.species_amounts.copy()
        return payload

    def replace(self, **updates: Any) -> WorldState:
        return replace(self, **updates)


@dataclass(frozen=True)
class Observation:
    values: dict[str, float | None]
    units: dict[str, str]
    observed_mask: dict[str, bool] = field(default_factory=dict)
    raw_signal: dict[str, Any] = field(default_factory=dict)
    processed_estimate: dict[str, float | None] = field(default_factory=dict)
    uncertainty: dict[str, float] = field(default_factory=dict)
    instrument_id: str | None = None
    cost: float = 0.0
    sample_consumed_L: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "values": self.values.copy(),
            "units": self.units.copy(),
            "observed_mask": self.observed_mask.copy(),
            "observed_keys": [key for key, observed in self.observed_mask.items() if observed],
            "raw_signal": self.raw_signal.copy(),
            "processed_estimate": self.processed_estimate.copy(),
            "uncertainty": self.uncertainty.copy(),
            "instrument_id": self.instrument_id,
            "cost": self.cost,
            "sample_consumed_L": self.sample_consumed_L,
        }


@dataclass(frozen=True)
class OperationRecord:
    operation_type: str
    preconditions: dict[str, bool]
    state_delta_summary: dict[str, float]
    constitution_checks: list[dict[str, object]]
    instrument: str | None = None
    measurement_cost: float = 0.0
    sample_consumed_L: float = 0.0

    def to_dict(self) -> dict[str, object]:
        return {
            "operation_type": self.operation_type,
            "preconditions": self.preconditions,
            "state_delta_summary": self.state_delta_summary,
            "constitution_checks": self.constitution_checks,
            "instrument": self.instrument,
            "measurement_cost": self.measurement_cost,
            "sample_consumed": self.sample_consumed_L,
        }
