"""Instrument contracts for partial observation in ChemWorld."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from chemworld.core.batch_reactor import batch_reactor_instruments


@dataclass(frozen=True)
class InstrumentContract:
    instrument_id: str
    observable_keys: tuple[str, ...]
    raw_signal_schema: dict[str, Any]
    processed_estimate_schema: dict[str, Any]
    uncertainty_model: str
    noise_model: dict[str, float]
    cost: float
    latency_s: float
    sample_consumption_L: float
    destructive: bool
    requires_terminated: bool
    calibration_profile: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "instrument_id": self.instrument_id,
            "observable_keys": list(self.observable_keys),
            "raw_signal_schema": self.raw_signal_schema,
            "processed_estimate_schema": self.processed_estimate_schema,
            "uncertainty_model": self.uncertainty_model,
            "noise_model": self.noise_model,
            "cost": self.cost,
            "latency_s": self.latency_s,
            "sample_consumption_L": self.sample_consumption_L,
            "destructive": self.destructive,
            "requires_terminated": self.requires_terminated,
            "calibration_profile": self.calibration_profile,
        }


def instrument_contracts() -> dict[str, InstrumentContract]:
    """Return formal contracts for every instrument available in ChemWorld."""

    latency = {
        "uvvis": 90.0,
        "gc": 480.0,
        "hplc": 600.0,
        "final_assay": 1200.0,
    }
    calibration = {
        "uvvis": "coarse_proxy_public_calibration",
        "gc": "volatile_byproduct_public_calibration",
        "hplc": "chromatography_public_calibration",
        "final_assay": "leaderboard_grade_calibration",
    }
    contracts: dict[str, InstrumentContract] = {}
    for instrument_id, instrument in batch_reactor_instruments().items():
        processed_schema = {
            key: {"type": "number", "minimum": 0.0, "maximum": 1.0}
            for key in instrument.observable_keys
        }
        contracts[instrument_id] = InstrumentContract(
            instrument_id=instrument_id,
            observable_keys=instrument.observable_keys,
            raw_signal_schema={
                "type": "object",
                "additionalProperties": {"type": ["number", "string", "boolean"]},
            },
            processed_estimate_schema={
                "type": "object",
                "properties": processed_schema,
                "additionalProperties": False,
            },
            uncertainty_model="instrument_noise_std_plus_process_proxy",
            noise_model=dict(instrument.noise_std),
            cost=float(instrument.cost),
            latency_s=latency.get(instrument_id, 300.0),
            sample_consumption_L=float(instrument.sample_volume_L),
            destructive=instrument.sample_volume_L > 0.0,
            requires_terminated=bool(instrument.requires_terminated),
            calibration_profile=calibration.get(instrument_id, "public_calibration"),
        )
    return contracts


__all__ = ["InstrumentContract", "instrument_contracts"]
