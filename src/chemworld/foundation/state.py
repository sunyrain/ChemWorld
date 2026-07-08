"""Hidden state, public observations, and experiment ledger."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field, replace
from typing import Any


@dataclass(frozen=True)
class SpeciesLedger:
    """Species definitions, roles, and initial amounts.

    Phase ledgers are the primary material-state source; global species totals
    are derived from phase contents.
    """

    species_roles: dict[str, tuple[str, ...]] = field(default_factory=dict)
    initial_amounts_mol: dict[str, float] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "species_roles", deepcopy(self.species_roles))
        object.__setattr__(self, "initial_amounts_mol", deepcopy(self.initial_amounts_mol))

    def to_dict(self) -> dict[str, Any]:
        return {
            "species_roles": {
                species_id: list(roles) for species_id, roles in self.species_roles.items()
            },
            "initial_amounts_mol": deepcopy(self.initial_amounts_mol),
        }


@dataclass(frozen=True)
class PhaseRecord:
    phase_id: str
    vessel_id: str
    phase_type: str
    volume_L: float
    species_amounts_mol: dict[str, float]
    settled: bool = False
    selected: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "species_amounts_mol", deepcopy(self.species_amounts_mol))

    def to_dict(self) -> dict[str, Any]:
        return {
            "phase_id": self.phase_id,
            "vessel_id": self.vessel_id,
            "phase_type": self.phase_type,
            "volume_L": self.volume_L,
            "species_amounts_mol": deepcopy(self.species_amounts_mol),
            "settled": self.settled,
            "selected": self.selected,
        }


@dataclass(frozen=True)
class PhaseLedger:
    phases: dict[str, PhaseRecord] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "phases", deepcopy(self.phases))

    def total_amounts_mol(self) -> dict[str, float]:
        totals: dict[str, float] = {}
        for phase in self.phases.values():
            for species_id, amount in phase.species_amounts_mol.items():
                totals[species_id] = totals.get(species_id, 0.0) + float(amount)
        return totals

    def to_dict(self) -> dict[str, Any]:
        return {phase_id: phase.to_dict() for phase_id, phase in self.phases.items()}


@dataclass(frozen=True)
class VesselRecord:
    vessel_id: str
    vessel_type: str
    max_volume_L: float
    max_temperature_K: float
    max_pressure_Pa: float
    phase_ids: tuple[str, ...] = ()
    temperature_K: float = 298.15
    pressure_Pa: float = 101_325.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "vessel_id": self.vessel_id,
            "vessel_type": self.vessel_type,
            "max_volume_L": self.max_volume_L,
            "max_temperature_K": self.max_temperature_K,
            "max_pressure_Pa": self.max_pressure_Pa,
            "phase_ids": list(self.phase_ids),
            "temperature_K": self.temperature_K,
            "pressure_Pa": self.pressure_Pa,
        }


@dataclass(frozen=True)
class VesselLedger:
    vessels: dict[str, VesselRecord] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "vessels", deepcopy(self.vessels))

    def to_dict(self) -> dict[str, Any]:
        return {vessel_id: vessel.to_dict() for vessel_id, vessel in self.vessels.items()}


@dataclass(frozen=True)
class EquipmentRecord:
    equipment_id: str
    equipment_type: str
    attached_vessel_id: str
    status: str = "idle"
    settings: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "settings", deepcopy(self.settings))

    def to_dict(self) -> dict[str, Any]:
        return {
            "equipment_id": self.equipment_id,
            "equipment_type": self.equipment_type,
            "attached_vessel_id": self.attached_vessel_id,
            "status": self.status,
            "settings": deepcopy(self.settings),
        }


@dataclass(frozen=True)
class EquipmentLedger:
    equipment: dict[str, EquipmentRecord] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "equipment", deepcopy(self.equipment))

    def to_dict(self) -> dict[str, Any]:
        return {
            equipment_id: equipment.to_dict()
            for equipment_id, equipment in self.equipment.items()
        }


@dataclass(frozen=True)
class VesselThermalRecord:
    vessel_id: str
    energy_jacket_J: float = 0.0
    heat_reaction_J: float = 0.0
    heat_loss_J: float = 0.0

    def to_dict(self) -> dict[str, float | str]:
        return self.__dict__.copy()


@dataclass(frozen=True)
class ThermalLedger:
    vessels: dict[str, VesselThermalRecord] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "vessels", deepcopy(self.vessels))

    def to_dict(self) -> dict[str, Any]:
        return {vessel_id: record.to_dict() for vessel_id, record in self.vessels.items()}


@dataclass(frozen=True)
class ProcessLedger:
    time_s: float = 0.0
    cost: float = 0.0
    risk: float = 0.0
    sample_consumed_L: float = 0.0
    waste_L: float = 0.0

    def to_dict(self) -> dict[str, float]:
        return self.__dict__.copy()


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
    species: SpeciesLedger | None = None
    phases: PhaseLedger | None = None
    vessels: VesselLedger | None = None
    equipment: EquipmentLedger | None = None
    thermal: ThermalLedger | None = None
    process: ProcessLedger | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "species_amounts", deepcopy(self.species_amounts))
        object.__setattr__(self, "units", deepcopy(self.units))
        object.__setattr__(self, "metadata", deepcopy(self.metadata))
        species = self.species or SpeciesLedger(
            initial_amounts_mol={
                key: float(value)
                for key, value in self.species_amounts.items()
                if float(value) > 0.0
            }
        )
        phase = PhaseRecord(
            phase_id="reactor_liquid",
            vessel_id=self.vessel_id,
            phase_type=self.phase,
            volume_L=self.volume_L,
            species_amounts_mol=self.species_amounts,
            settled=bool(self.metadata.get("phase_settled", False)),
            selected=str(self.metadata.get("selected_phase", "")) == "reactor_liquid",
        )
        phases = (
            PhaseLedger({"reactor_liquid": phase})
            if self.phases is None or set(self.phases.phases) == {"reactor_liquid"}
            else self.phases
        )
        vessel = VesselRecord(
            vessel_id=self.vessel_id,
            vessel_type=self.vessel_id,
            max_volume_L=float(self.metadata.get("max_volume_L", 0.10)),
            max_temperature_K=float(self.metadata.get("max_temperature_K", 470.0)),
            max_pressure_Pa=float(self.metadata.get("max_pressure_Pa", 550_000.0)),
            phase_ids=tuple(phases.phases),
            temperature_K=self.temperature_K,
            pressure_Pa=self.pressure_Pa,
        )
        vessels = (
            VesselLedger({self.vessel_id: vessel})
            if self.vessels is None or set(self.vessels.vessels) == {self.vessel_id}
            else self.vessels
        )
        equipment = (
            EquipmentLedger(
                {
                    "batch_reactor": EquipmentRecord(
                        "batch_reactor",
                        "batch_reactor",
                        attached_vessel_id=self.vessel_id,
                        status="terminated" if self.terminated else "idle",
                        settings={
                            key: deepcopy(value)
                            for key, value in self.metadata.items()
                            if key
                            in {
                                "solvent",
                                "catalyst",
                                "stirring_speed_rpm",
                                "flow_rate_mL_min",
                                "residence_time_s",
                                "potential_V",
                                "current_mA",
                            }
                        },
                    )
                }
            )
            if self.equipment is None or set(self.equipment.equipment) == {"batch_reactor"}
            else self.equipment
        )
        thermal = (
            ThermalLedger(
                {
                    self.vessel_id: VesselThermalRecord(
                        self.vessel_id,
                        energy_jacket_J=self.ledger.energy_jacket_J,
                        heat_reaction_J=self.ledger.heat_reaction_J,
                        heat_loss_J=self.ledger.heat_loss_J,
                    )
                }
            )
            if self.thermal is None or set(self.thermal.vessels) == {self.vessel_id}
            else self.thermal
        )
        process = ProcessLedger(
            time_s=self.ledger.time_s,
            cost=self.ledger.cost,
            risk=self.ledger.risk,
            sample_consumed_L=self.ledger.sample_consumed_L,
            waste_L=0.0 if self.process is None else self.process.waste_L,
        )
        object.__setattr__(self, "species", species)
        object.__setattr__(self, "phases", phases)
        object.__setattr__(self, "vessels", vessels)
        object.__setattr__(self, "equipment", equipment)
        object.__setattr__(self, "thermal", thermal)
        object.__setattr__(self, "process", process)

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
            "units": deepcopy(self.units),
            "metadata": deepcopy(self.metadata),
            "species": None if self.species is None else self.species.to_dict(),
            "phases": None if self.phases is None else self.phases.to_dict(),
            "vessels": None if self.vessels is None else self.vessels.to_dict(),
            "equipment": None if self.equipment is None else self.equipment.to_dict(),
            "thermal": None if self.thermal is None else self.thermal.to_dict(),
            "process": None if self.process is None else self.process.to_dict(),
        }
        if include_hidden:
            payload["species_amounts"] = deepcopy(self.species_amounts)
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
