"""Instrument observation module for ChemWorld."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from chemworld.world.operations import DOWNSTREAM_OBSERVATION_KEYS


def processed_estimate(
    values: dict[str, float | None],
    observed_mask: dict[str, bool],
) -> dict[str, float | None]:
    estimate_keys = (
        "yield",
        "selectivity",
        "conversion",
        "byproduct_signal",
        "degradation_warning",
        *DOWNSTREAM_OBSERVATION_KEYS,
    )
    return {key: values.get(key) for key in estimate_keys if observed_mask.get(key, False)}


def raw_signal(instrument_id: str, values: dict[str, float | None]) -> dict[str, Any]:
    def observed(key: str) -> float:
        value = values.get(key)
        return 0.0 if value is None else float(value)

    if instrument_id == "uvvis":
        yield_value = observed("yield")
        conversion = observed("conversion")
        phase_ratio = observed("phase_ratio")
        flow_conversion = observed("flow_conversion")
        energy_efficiency = observed("energy_efficiency")
        return {
            "kind": "uvvis_spectrum",
            "wavelength_nm": [360, 420, 510, 620, 710],
            "absorbance": [
                round(0.08 + 0.25 * conversion, 6),
                round(0.05 + 0.35 * yield_value, 6),
                round(0.04 + 0.15 * max(conversion - yield_value, 0.0), 6),
                round(0.03 + 0.10 * phase_ratio, 6),
                round(0.03 + 0.15 * max(flow_conversion, energy_efficiency), 6),
            ],
        }
    if instrument_id == "hplc":
        yield_value = observed("yield")
        byproduct = observed("byproduct_signal")
        purity = observed("purity")
        impurity = observed("impurity_signal")
        crystal_purity = observed("crystal_purity")
        distillate_purity = observed("distillate_purity")
        return {
            "kind": "hplc_chromatogram",
            "peaks": [
                {
                    "retention_time_min": 1.18,
                    "peak_area": round(900.0 * max(1.0 - yield_value, 0.0), 6),
                    "assignment": "A_proxy",
                },
                {
                    "retention_time_min": 2.74,
                    "peak_area": round(
                        1200.0 * max(yield_value, purity, crystal_purity, distillate_purity),
                        6,
                    ),
                    "assignment": "P_proxy",
                },
                {
                    "retention_time_min": 3.52,
                    "peak_area": round(900.0 * max(byproduct, impurity), 6),
                    "assignment": "byproduct_proxy",
                },
            ],
        }
    if instrument_id == "gc":
        byproduct = observed("byproduct_signal")
        degradation = observed("degradation_warning")
        distillate_purity = observed("distillate_purity")
        return {
            "kind": "gc_chromatogram",
            "peaks": [
                {
                    "retention_time_min": 0.82,
                    "peak_area": round(800.0 * byproduct, 6),
                    "assignment": "volatile_byproduct_proxy",
                },
                {
                    "retention_time_min": 1.65,
                    "peak_area": round(800.0 * degradation, 6),
                    "assignment": "degradation_proxy",
                },
                {
                    "retention_time_min": 2.18,
                    "peak_area": round(1000.0 * distillate_purity, 6),
                    "assignment": "distillate_product_proxy",
                },
            ],
        }
    if instrument_id == "final_assay":
        return {
            "kind": "final_assay_packet",
            "quality": "high",
            "channels": [
                "hplc",
                "gc",
                "calibrated_mass_balance",
                "phase_partition",
                "purification_accounting",
                "crystallization_accounting",
                "distillation_accounting",
                "flow_reactor_summary",
                "electrochemical_summary",
            ],
        }
    return {}


def observation_units() -> dict[str, str]:
    return {
        "yield": "dimensionless",
        "selectivity": "dimensionless",
        "conversion": "dimensionless",
        "byproduct_signal": "dimensionless",
        "degradation_warning": "dimensionless",
        "virtual_spectrum_summary": "dimensionless",
        **dict.fromkeys(DOWNSTREAM_OBSERVATION_KEYS, "dimensionless"),
        "cost": "currency",
        "safety_risk": "risk",
        "score": "dimensionless",
    }


def base_public_values(*, cost: float, safety_risk: float) -> dict[str, float | None]:
    return {
        "yield": None,
        "selectivity": None,
        "conversion": None,
        "byproduct_signal": None,
        "degradation_warning": None,
        "virtual_spectrum_summary": None,
        **dict.fromkeys(DOWNSTREAM_OBSERVATION_KEYS, None),
        "cost": min(1.0, cost),
        "safety_risk": safety_risk,
        "score": 0.0,
    }


def base_observed_mask() -> dict[str, bool]:
    return {
        "yield": False,
        "selectivity": False,
        "conversion": False,
        "byproduct_signal": False,
        "degradation_warning": False,
        "virtual_spectrum_summary": False,
        **dict.fromkeys(DOWNSTREAM_OBSERVATION_KEYS, False),
        "cost": True,
        "safety_risk": True,
        "score": True,
    }


@dataclass(frozen=True)
class ObservationModuleSpec:
    module_id: str = "instrument_observation"
    version: str = "0.3"
    layers: tuple[str, ...] = ("raw_signal", "processed_estimate", "uncertainty")

    def to_dict(self) -> dict[str, object]:
        return {
            "module_id": self.module_id,
            "version": self.version,
            "layers": list(self.layers),
            "partial_observation": True,
            "downstream_keys": list(DOWNSTREAM_OBSERVATION_KEYS),
        }


__all__ = [
    "ObservationModuleSpec",
    "base_observed_mask",
    "base_public_values",
    "observation_units",
    "processed_estimate",
    "raw_signal",
]
