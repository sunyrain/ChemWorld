"""Virtual spectroscopy and chromatography signal synthesis for ChemWorld."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np


@dataclass(frozen=True)
class SignalPeak:
    center: float
    width: float
    area: float
    assignment: str

    def to_dict(self, *, center_key: str, width_key: str) -> dict[str, Any]:
        return {
            center_key: round(float(self.center), 6),
            width_key: round(float(self.width), 6),
            "area": round(float(self.area), 6),
            "assignment": self.assignment,
        }


def _observed(values: dict[str, float | None], key: str) -> float:
    value = values.get(key)
    return 0.0 if value is None else float(np.clip(value, 0.0, 1.0))


def _axis(start: float, stop: float, points: int) -> np.ndarray:
    return np.linspace(start, stop, points, dtype=float)


def _gaussian(axis: np.ndarray, peak: SignalPeak) -> np.ndarray:
    width = max(float(peak.width), 1.0e-6)
    height = float(peak.area) / (width * np.sqrt(2.0 * np.pi))
    return height * np.exp(-0.5 * ((axis - float(peak.center)) / width) ** 2)


def _rounded(values: np.ndarray | list[float], digits: int = 6) -> list[float]:
    return [round(float(value), digits) for value in values]


def _chromatogram(
    *,
    kind: str,
    time_min: np.ndarray,
    peaks: tuple[SignalPeak, ...],
    baseline: float,
) -> dict[str, Any]:
    intensity = np.full_like(time_min, fill_value=baseline, dtype=float)
    for peak in peaks:
        intensity += _gaussian(time_min, peak)
    max_intensity = float(np.max(intensity))
    if max_intensity > 0.0:
        intensity = intensity / max_intensity
    return {
        "kind": kind,
        "time_min": _rounded(time_min),
        "intensity": _rounded(intensity),
        "peaks": [
            peak.to_dict(center_key="retention_time_min", width_key="width_min")
            for peak in peaks
        ],
        "baseline": round(float(baseline), 6),
        "normalization": "max_intensity",
    }


def hplc_chromatogram(values: dict[str, float | None]) -> dict[str, Any]:
    """Return a compact HPLC chromatogram with reactant, product, and impurity peaks."""

    product = max(
        _observed(values, "yield"),
        _observed(values, "purity"),
        _observed(values, "crystal_purity"),
        _observed(values, "distillate_purity"),
    )
    reactant = max(1.0 - _observed(values, "conversion"), 0.0)
    impurity = max(_observed(values, "byproduct_signal"), _observed(values, "impurity_signal"))
    degradation = _observed(values, "degradation_warning")
    peaks = (
        SignalPeak(1.15, 0.055, 260.0 * reactant, "A_proxy"),
        SignalPeak(2.62, 0.075, 720.0 * product, "P_proxy"),
        SignalPeak(3.36, 0.090, 380.0 * impurity, "byproduct_proxy"),
        SignalPeak(4.18, 0.110, 240.0 * degradation, "degradation_proxy"),
    )
    return _chromatogram(
        kind="hplc_chromatogram",
        time_min=_axis(0.0, 6.0, 121),
        peaks=peaks,
        baseline=0.012,
    )


def gc_chromatogram(values: dict[str, float | None]) -> dict[str, Any]:
    """Return a compact GC chromatogram for volatile byproducts and distillate quality."""

    volatile = _observed(values, "byproduct_signal")
    degradation = _observed(values, "degradation_warning")
    distillate = _observed(values, "distillate_purity")
    solvent_loss = _observed(values, "solvent_loss")
    peaks = (
        SignalPeak(0.62, 0.040, 280.0 * solvent_loss, "solvent_loss_proxy"),
        SignalPeak(1.05, 0.050, 520.0 * volatile, "volatile_byproduct_proxy"),
        SignalPeak(1.74, 0.060, 430.0 * degradation, "degradation_proxy"),
        SignalPeak(2.45, 0.080, 620.0 * distillate, "distillate_product_proxy"),
    )
    return _chromatogram(
        kind="gc_chromatogram",
        time_min=_axis(0.0, 4.0, 101),
        peaks=peaks,
        baseline=0.010,
    )


def uvvis_spectrum(values: dict[str, float | None]) -> dict[str, Any]:
    """Return a UV-vis absorbance spectrum with broad proxy bands."""

    wavelength = _axis(320.0, 760.0, 111)
    bands = (
        SignalPeak(365.0, 32.0, 0.42 * _observed(values, "conversion"), "conversion_band"),
        SignalPeak(430.0, 38.0, 0.62 * _observed(values, "yield"), "product_band"),
        SignalPeak(
            515.0,
            44.0,
            0.36 * max(_observed(values, "byproduct_signal"), _observed(values, "impurity_signal")),
            "impurity_band",
        ),
        SignalPeak(640.0, 58.0, 0.24 * _observed(values, "phase_ratio"), "phase_proxy_band"),
        SignalPeak(
            705.0,
            46.0,
            0.28
            * max(
                _observed(values, "flow_conversion"),
                _observed(values, "energy_efficiency"),
            ),
            "process_proxy_band",
        ),
    )
    absorbance = np.full_like(wavelength, 0.025, dtype=float)
    for band in bands:
        absorbance += _gaussian(wavelength, band)
    return {
        "kind": "uvvis_spectrum",
        "wavelength_nm": _rounded(wavelength),
        "absorbance": _rounded(absorbance),
        "bands": [
            band.to_dict(center_key="center_nm", width_key="width_nm") for band in bands
        ],
        "baseline": 0.025,
    }


def ir_spectrum(values: dict[str, float | None]) -> dict[str, Any]:
    """Return a low-resolution IR-like transmittance spectrum."""

    wavenumber = _axis(400.0, 4000.0, 121)
    product = max(_observed(values, "yield"), _observed(values, "purity"))
    impurity = max(_observed(values, "byproduct_signal"), _observed(values, "impurity_signal"))
    degradation = _observed(values, "degradation_warning")
    bands = (
        SignalPeak(820.0, 55.0, 0.16 * impurity, "impurity_fingerprint"),
        SignalPeak(1180.0, 70.0, 0.20 * product, "product_fingerprint"),
        SignalPeak(1720.0, 85.0, 0.24 * degradation, "degradation_carbonyl_proxy"),
        SignalPeak(2960.0, 120.0, 0.10 + 0.12 * product, "organic_CH_proxy"),
        SignalPeak(
            3360.0,
            150.0,
            0.18 * _observed(values, "solvent_loss"),
            "residual_solvent_proxy",
        ),
    )
    absorbance = np.zeros_like(wavenumber, dtype=float)
    for band in bands:
        absorbance += _gaussian(wavenumber, band)
    transmittance = np.clip(1.0 - absorbance, 0.02, 1.0)
    return {
        "kind": "ir_spectrum",
        "wavenumber_cm-1": _rounded(wavenumber),
        "transmittance": _rounded(transmittance),
        "bands": [
            band.to_dict(center_key="center_cm-1", width_key="width_cm-1") for band in bands
        ],
    }


def nmr_spectrum(values: dict[str, float | None]) -> dict[str, Any]:
    """Return a toy 1H NMR-like spectrum for product and impurity proxies."""

    shift = _axis(0.0, 12.0, 121)
    product = max(_observed(values, "yield"), _observed(values, "purity"))
    impurity = max(_observed(values, "byproduct_signal"), _observed(values, "impurity_signal"))
    degradation = _observed(values, "degradation_warning")
    peaks = (
        SignalPeak(1.28, 0.045, 0.32 * product, "product_aliphatic_proxy"),
        SignalPeak(3.72, 0.055, 0.26 * product, "product_heteroatom_proxy"),
        SignalPeak(6.85, 0.070, 0.22 * impurity, "byproduct_aromatic_proxy"),
        SignalPeak(9.55, 0.085, 0.18 * degradation, "degradation_aldehyde_proxy"),
    )
    intensity = np.full_like(shift, 0.004, dtype=float)
    for peak in peaks:
        intensity += _gaussian(shift, peak)
    max_intensity = float(np.max(intensity))
    if max_intensity > 0.0:
        intensity = intensity / max_intensity
    return {
        "kind": "nmr_1h_spectrum",
        "chemical_shift_ppm": _rounded(shift),
        "intensity": _rounded(intensity),
        "peaks": [
            peak.to_dict(center_key="shift_ppm", width_key="width_ppm") for peak in peaks
        ],
        "reference": "TMS_0ppm_proxy",
    }


def final_assay_spectra(values: dict[str, float | None]) -> dict[str, Any]:
    """Return the multi-instrument spectral packet used by final assay records."""

    return {
        "kind": "final_assay_packet",
        "quality": "leaderboard_grade",
        "channels": ["hplc", "gc", "uvvis", "ir", "nmr", "calibrated_mass_balance"],
        "spectra": {
            "hplc": hplc_chromatogram(values),
            "gc": gc_chromatogram(values),
            "uvvis": uvvis_spectrum(values),
            "ir": ir_spectrum(values),
            "nmr": nmr_spectrum(values),
        },
        "mass_balance": {
            "process_mass_balance_error": round(
                _observed(values, "process_mass_balance_error"),
                6,
            ),
            "recovery": round(_observed(values, "recovery"), 6),
            "purity": round(_observed(values, "purity"), 6),
        },
    }


def raw_signal_schema(instrument_id: str) -> dict[str, Any]:
    """Return the JSON-friendly raw-signal schema advertised by an instrument."""

    if instrument_id in {"hplc", "gc"}:
        axis = "time_min"
        signal = "intensity"
    elif instrument_id == "uvvis":
        axis = "wavelength_nm"
        signal = "absorbance"
    elif instrument_id == "final_assay":
        return {
            "type": "object",
            "required": ["kind", "channels", "spectra", "mass_balance"],
            "properties": {
                "kind": {"const": "final_assay_packet"},
                "channels": {"type": "array", "items": {"type": "string"}},
                "spectra": {"type": "object"},
                "mass_balance": {"type": "object"},
            },
            "additionalProperties": True,
        }
    else:
        axis = "x"
        signal = "y"
    return {
        "type": "object",
        "required": ["kind", axis, signal],
        "properties": {
            "kind": {"type": "string"},
            axis: {"type": "array", "items": {"type": "number"}},
            signal: {"type": "array", "items": {"type": "number"}},
            "peaks": {"type": "array"},
            "bands": {"type": "array"},
        },
        "additionalProperties": True,
    }


__all__ = [
    "SignalPeak",
    "final_assay_spectra",
    "gc_chromatogram",
    "hplc_chromatogram",
    "ir_spectrum",
    "nmr_spectrum",
    "raw_signal_schema",
    "uvvis_spectrum",
]
