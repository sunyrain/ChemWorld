"""Instrument observation module for ChemWorld."""

from dataclasses import dataclass

from chemworld.core.batch_reactor import ChemWorldObservationKernel, DOWNSTREAM_OBSERVATION_KEYS


@dataclass(frozen=True)
class ObservationModuleSpec:
    module_id: str = "instrument_observation"
    version: str = "0.2"
    layers: tuple[str, ...] = ("raw_signal", "processed_estimate", "uncertainty")

    def to_dict(self) -> dict[str, object]:
        return {
            "module_id": self.module_id,
            "version": self.version,
            "layers": list(self.layers),
            "partial_observation": True,
            "downstream_keys": list(DOWNSTREAM_OBSERVATION_KEYS),
        }


__all__ = ["ChemWorldObservationKernel", "ObservationModuleSpec"]
