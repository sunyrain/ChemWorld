"""Material removed from the active vessel and retained as identified samples."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from math import isfinite
from typing import Any


@dataclass(frozen=True)
class StoredSample:
    sample_id: str
    source_vessel_id: str
    collection_operation: str
    collected_at_s: float
    volume_L: float
    species_amounts_mol: dict[str, float]
    temperature_K: float
    solvent: int
    quenched: bool
    seed_target_mol: float = 0.0

    def __post_init__(self) -> None:
        values = [self.collected_at_s, self.volume_L, self.temperature_K, self.seed_target_mol]
        values.extend(self.species_amounts_mol.values())
        if not self.sample_id or not all(isfinite(x) and x >= 0 for x in values):
            raise ValueError("Stored sample requires an identity and finite nonnegative inventory")
        object.__setattr__(self, "species_amounts_mol", deepcopy(self.species_amounts_mol))

    def to_dict(self) -> dict[str, Any]:
        return deepcopy(self.__dict__)

    def public_summary(self) -> dict[str, Any]:
        return {
            "sample_id": self.sample_id,
            "source_vessel_id": self.source_vessel_id,
            "collection_operation": self.collection_operation,
            "collected_at_s": self.collected_at_s,
            "volume_L": self.volume_L,
            "quenched": self.quenched,
        }


@dataclass(frozen=True)
class SampleLedger:
    samples: dict[str, StoredSample] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if any(key != sample.sample_id for key, sample in self.samples.items()):
            raise ValueError("Sample ledger keys must match sample identities")
        object.__setattr__(self, "samples", deepcopy(self.samples))

    def append(self, sample: StoredSample) -> SampleLedger:
        if sample.sample_id in self.samples:
            raise ValueError(f"Sample identity already exists: {sample.sample_id}")
        return SampleLedger({**self.samples, sample.sample_id: sample})

    def total_amounts_mol(self) -> dict[str, float]:
        totals: dict[str, float] = {}
        for sample in self.samples.values():
            for species, amount in sample.species_amounts_mol.items():
                totals[species] = totals.get(species, 0.0) + amount
        return totals

    def to_dict(self) -> dict[str, Any]:
        return {key: sample.to_dict() for key, sample in self.samples.items()}

    def public_summary(self) -> list[dict[str, Any]]:
        return [sample.public_summary() for sample in self.samples.values()]
