"""Instrument contracts for partial observation in ChemWorld."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from chemworld.foundation import Instrument
from chemworld.world.spectra import raw_signal_schema


def chemworld_instruments() -> dict[str, Instrument]:
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
        "ph_meter": Instrument(
            "ph_meter",
            "pH meter",
            (
                "pH_normalized",
                "acid_dissociation_fraction",
                "precipitation_signal",
                "equilibrium_residual",
                "equilibrium_confidence",
            ),
            cost=0.018,
            sample_volume_L=0.00003,
            noise_std={
                "pH_normalized": 0.004,
                "acid_dissociation_fraction": 0.015,
                "precipitation_signal": 0.020,
                "equilibrium_residual": 0.010,
                "equilibrium_confidence": 0.012,
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
                "pH_normalized",
                "acid_dissociation_fraction",
                "precipitation_signal",
                "equilibrium_residual",
                "equilibrium_confidence",
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
                "pH_normalized": 0.002,
                "acid_dissociation_fraction": 0.006,
                "precipitation_signal": 0.006,
                "equilibrium_residual": 0.004,
                "equilibrium_confidence": 0.006,
            },
            requires_terminated=True,
        ),
    }


@dataclass(frozen=True)
class InstrumentContract:
    instrument_id: str
    observable_keys: tuple[str, ...]
    input_state_schema: dict[str, Any]
    axis_contract: dict[str, Any]
    raw_signal_schema: dict[str, Any]
    processed_estimate_schema: dict[str, Any]
    uncertainty_model: str
    noise_model: dict[str, float]
    calibration_contract: dict[str, Any]
    detection_contract: dict[str, Any]
    saturation_contract: dict[str, Any]
    baseline_drift_contract: dict[str, Any]
    missingness_contract: dict[str, Any]
    cost: float
    latency_s: float
    sample_consumption_L: float
    destructive: bool
    requires_terminated: bool
    calibration_profile: str
    synthetic_boundary: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "instrument_id": self.instrument_id,
            "observable_keys": list(self.observable_keys),
            "input_state_schema": self.input_state_schema,
            "axis_contract": self.axis_contract,
            "raw_signal_schema": self.raw_signal_schema,
            "processed_estimate_schema": self.processed_estimate_schema,
            "uncertainty_model": self.uncertainty_model,
            "noise_model": self.noise_model,
            "calibration_contract": self.calibration_contract,
            "detection_contract": self.detection_contract,
            "saturation_contract": self.saturation_contract,
            "baseline_drift_contract": self.baseline_drift_contract,
            "missingness_contract": self.missingness_contract,
            "cost": self.cost,
            "latency_s": self.latency_s,
            "sample_consumption_L": self.sample_consumption_L,
            "destructive": self.destructive,
            "requires_terminated": self.requires_terminated,
            "calibration_profile": self.calibration_profile,
            "synthetic_boundary": self.synthetic_boundary,
        }


def instrument_contracts() -> dict[str, InstrumentContract]:
    """Return formal contracts for every instrument available in ChemWorld."""

    latency = {
        "uvvis": 90.0,
        "ph_meter": 45.0,
        "gc": 480.0,
        "hplc": 600.0,
        "final_assay": 1200.0,
    }
    calibration = {
        "uvvis": "beer_lambert_public_calibration_v2",
        "ph_meter": "nernstian_public_ph_calibration_v2",
        "gc": "retention_plate_public_calibration_v2",
        "hplc": "retention_plate_public_calibration_v2",
        "final_assay": "synthetic_multichannel_public_calibration_v2",
    }
    axes: dict[str, dict[str, Any]] = {
        "uvvis": {"key": "wavelength_nm", "unit": "nm", "range": [320.0, 760.0]},
        "ph_meter": {"key": "replicate_index", "unit": "index", "range": None},
        "gc": {"key": "time_min", "unit": "min", "range": [0.0, 4.0]},
        "hplc": {"key": "time_min", "unit": "min", "range": [0.0, 6.0]},
        "final_assay": {
            "key": "channel_specific",
            "unit": "declared_per_channel",
            "range": None,
        },
    }
    calibration_methods = {
        "uvvis": "Beer-Lambert absorbance with blank, path length, and dilution",
        "ph_meter": "Nernstian electrode response at declared temperature",
        "gc": "retention factor, dead time, theoretical plates, and detector response",
        "hplc": "retention factor, dead time, theoretical plates, and detector response",
        "final_assay": "independent declared calibration for each synthetic channel",
    }
    lod = {"uvvis": 0.0025, "gc": 0.0012, "hplc": 0.0008}
    contracts: dict[str, InstrumentContract] = {}
    for instrument_id, instrument in chemworld_instruments().items():
        processed_schema = {
            key: {"type": ["number", "null"], "minimum": 0.0, "maximum": 1.0}
            for key in instrument.observable_keys
        }
        contracts[instrument_id] = InstrumentContract(
            instrument_id=instrument_id,
            observable_keys=instrument.observable_keys,
            input_state_schema={
                "physical_state": "virtual_liquid_sample",
                "required_public_fields": ["sample_basis_volume_L", "replicate_count"],
                "forbidden_fields": [
                    "hidden_species_amounts",
                    "private_seed",
                    "provider_parameters",
                ],
            },
            axis_contract=dict(axes[instrument_id]),
            raw_signal_schema=raw_signal_schema(instrument_id),
            processed_estimate_schema={
                "type": "object",
                "properties": processed_schema,
                "additionalProperties": False,
            },
            uncertainty_model="instrument_noise_std_plus_process_proxy",
            noise_model=dict(instrument.noise_std),
            calibration_contract={
                "profile": calibration[instrument_id],
                "method": calibration_methods[instrument_id],
                "status": "synthetic_reference_calibration",
            },
            detection_contract={
                "lod_mol_L": lod.get(instrument_id),
                "loq_mol_L": (
                    None if instrument_id not in lod else 10.0 / 3.3 * lod[instrument_id]
                ),
                "below_lod": "null_processed_estimate_with_missingness_reason",
            },
            saturation_contract={
                "policy": "clip_and_flag_outside_declared_linear_range",
                "upper_linear_range_mol_L": (
                    5.0 if instrument_id in {"uvvis", "gc", "hplc"} else None
                ),
            },
            baseline_drift_contract={
                "baseline": "declared_in_public_packet",
                "drift": "linear_axis_drift_declared_in_public_packet",
            },
            missingness_contract={
                "below_lod": "processed value is null; raw trace remains available",
                "failed_measurement": "no signal packet and no instrument charge",
                "masking": "removes spectral evidence only; does not alter world state",
            },
            cost=float(instrument.cost),
            latency_s=latency.get(instrument_id, 300.0),
            sample_consumption_L=float(instrument.sample_volume_L),
            destructive=instrument.sample_volume_L > 0.0,
            requires_terminated=bool(instrument.requires_terminated),
            calibration_profile=calibration.get(instrument_id, "public_calibration"),
            synthetic_boundary=(
                "Bounded synthetic benchmark instrument; it does not predict real samples, "
                "replace an empirical spectral library, or emulate a physical device."
            ),
        )
    return contracts


__all__ = ["InstrumentContract", "chemworld_instruments", "instrument_contracts"]
