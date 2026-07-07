"""Instrument contracts for partial observation in ChemWorld."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from chemworld.foundation import Instrument


def batch_reactor_instruments() -> dict[str, Instrument]:
    """Return instrument definitions used by the shared observation law."""

    return {
        "hplc": Instrument(
            "hplc",
            "HPLC",
            (
                "yield",
                "selectivity",
                "byproduct_signal",
                "purity",
                "impurity_signal",
                "crystal_purity",
                "distillate_purity",
            ),
            cost=0.08,
            sample_volume_L=0.00020,
            noise_std={
                "yield": 0.012,
                "selectivity": 0.018,
                "byproduct_signal": 0.012,
                "purity": 0.015,
                "impurity_signal": 0.015,
                "crystal_purity": 0.018,
                "distillate_purity": 0.014,
            },
        ),
        "gc": Instrument(
            "gc",
            "GC",
            ("byproduct_signal", "degradation_warning", "distillate_purity"),
            cost=0.06,
            sample_volume_L=0.00015,
            noise_std={
                "byproduct_signal": 0.018,
                "degradation_warning": 0.018,
                "distillate_purity": 0.020,
            },
        ),
        "uvvis": Instrument(
            "uvvis",
            "UV-vis",
            ("yield", "conversion", "phase_ratio", "flow_conversion", "energy_efficiency"),
            cost=0.025,
            sample_volume_L=0.00005,
            noise_std={
                "yield": 0.045,
                "conversion": 0.035,
                "phase_ratio": 0.040,
                "flow_conversion": 0.040,
                "energy_efficiency": 0.045,
            },
        ),
        "final_assay": Instrument(
            "final_assay",
            "Final assay",
            (
                "yield",
                "selectivity",
                "conversion",
                "byproduct_signal",
                "degradation_warning",
                "purity",
                "recovery",
                "phase_ratio",
                "product_in_organic",
                "product_in_aqueous",
                "impurity_signal",
                "solvent_loss",
                "process_mass_balance_error",
                "crystal_yield",
                "crystal_purity",
                "crystal_size",
                "distillate_purity",
                "distillate_recovery",
                "flow_conversion",
                "electrochemical_selectivity",
                "energy_efficiency",
            ),
            cost=0.16,
            sample_volume_L=0.00030,
            noise_std={
                "yield": 0.006,
                "selectivity": 0.010,
                "conversion": 0.008,
                "byproduct_signal": 0.008,
                "degradation_warning": 0.008,
                "purity": 0.008,
                "recovery": 0.010,
                "phase_ratio": 0.012,
                "product_in_organic": 0.010,
                "product_in_aqueous": 0.010,
                "impurity_signal": 0.008,
                "solvent_loss": 0.012,
                "process_mass_balance_error": 0.004,
                "crystal_yield": 0.010,
                "crystal_purity": 0.010,
                "crystal_size": 0.025,
                "distillate_purity": 0.010,
                "distillate_recovery": 0.012,
                "flow_conversion": 0.012,
                "electrochemical_selectivity": 0.012,
                "energy_efficiency": 0.016,
            },
            requires_terminated=True,
        ),
    }


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


__all__ = ["InstrumentContract", "batch_reactor_instruments", "instrument_contracts"]
