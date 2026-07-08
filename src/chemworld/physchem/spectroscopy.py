"""Local spectroscopy and chromatography signal synthesis for ChemWorld."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from math import isfinite, sqrt
from typing import Any, Literal

import numpy as np

from chemworld.physchem.mechanism_library import MechanismScenarioCard
from chemworld.physchem.reaction_network import ReactionNetworkSpec

PeakShape = Literal["gaussian", "lorentzian"]


@dataclass(frozen=True)
class CalibrationCurve:
    slope: float
    intercept: float = 0.0
    lower_limit: float = 0.0
    upper_limit: float = 1.0e6
    noise_relative: float = 0.03

    def __post_init__(self) -> None:
        if self.slope <= 0.0 or not isfinite(self.slope):
            raise ValueError("Calibration slope must be finite and positive")
        if self.lower_limit < 0.0 or self.upper_limit <= self.lower_limit:
            raise ValueError("Calibration limits must be nonnegative and increasing")
        if self.noise_relative < 0.0:
            raise ValueError("Calibration noise cannot be negative")

    def response(self, concentration_mol_L: float) -> float:
        concentration = float(np.clip(concentration_mol_L, self.lower_limit, self.upper_limit))
        return self.intercept + self.slope * concentration

    def estimate_concentration(self, response: float) -> float:
        concentration = (float(response) - self.intercept) / self.slope
        return float(np.clip(concentration, self.lower_limit, self.upper_limit))

    def to_dict(self) -> dict[str, float]:
        return {
            "slope": self.slope,
            "intercept": self.intercept,
            "lower_limit": self.lower_limit,
            "upper_limit": self.upper_limit,
            "noise_relative": self.noise_relative,
        }


@dataclass(frozen=True)
class SpectralFeatureSpec:
    species_id: str
    instrument_id: str
    center: float
    width: float
    response_factor: float
    detection_limit_mol_L: float
    assignment: str
    group: str
    shape: PeakShape = "gaussian"
    calibration: CalibrationCurve = field(
        default_factory=lambda: CalibrationCurve(slope=1.0),
    )
    metadata: dict[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.width <= 0.0 or not isfinite(self.width):
            raise ValueError("Feature width must be finite and positive")
        if self.response_factor <= 0.0 or not isfinite(self.response_factor):
            raise ValueError("Feature response_factor must be finite and positive")
        if self.detection_limit_mol_L < 0.0:
            raise ValueError("Feature detection limit cannot be negative")

    def to_dict(self) -> dict[str, object]:
        return {
            "species_id": self.species_id,
            "instrument_id": self.instrument_id,
            "center": self.center,
            "width": self.width,
            "response_factor": self.response_factor,
            "detection_limit_mol_L": self.detection_limit_mol_L,
            "assignment": self.assignment,
            "group": self.group,
            "shape": self.shape,
            "calibration": self.calibration.to_dict(),
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True)
class InstrumentSignalSpec:
    instrument_id: str
    kind: str
    axis_key: str
    signal_key: str
    axis_unit: str
    axis_start: float
    axis_stop: float
    points: int
    baseline: float
    baseline_drift: float
    noise_std: float
    features: tuple[SpectralFeatureSpec, ...]
    normalize: bool = True
    signal_mode: Literal["positive", "transmittance"] = "positive"

    def __post_init__(self) -> None:
        if self.axis_stop <= self.axis_start:
            raise ValueError("Signal axis_stop must be greater than axis_start")
        if self.points < 5:
            raise ValueError("Signal axis must contain at least five points")
        if self.baseline < 0.0 or self.noise_std < 0.0:
            raise ValueError("Baseline and noise must be nonnegative")

    @property
    def axis(self) -> np.ndarray:
        return np.linspace(self.axis_start, self.axis_stop, self.points, dtype=float)

    def to_dict(self) -> dict[str, object]:
        return {
            "instrument_id": self.instrument_id,
            "kind": self.kind,
            "axis_key": self.axis_key,
            "signal_key": self.signal_key,
            "axis_unit": self.axis_unit,
            "axis_start": self.axis_start,
            "axis_stop": self.axis_stop,
            "points": self.points,
            "baseline": self.baseline,
            "baseline_drift": self.baseline_drift,
            "noise_std": self.noise_std,
            "normalize": self.normalize,
            "signal_mode": self.signal_mode,
            "features": [feature.to_dict() for feature in self.features],
        }


@dataclass(frozen=True)
class SpectralMeasurement:
    instrument_id: str
    kind: str
    axis_key: str
    signal_key: str
    axis: tuple[float, ...]
    signal: tuple[float, ...]
    replicate_signals: tuple[tuple[float, ...], ...]
    peaks: tuple[dict[str, object], ...]
    processed_estimates: dict[str, float]
    uncertainty: dict[str, float]
    metadata: dict[str, object]

    def to_dict(self) -> dict[str, Any]:
        return {
            "kind": self.kind,
            self.axis_key: list(self.axis),
            self.signal_key: list(self.signal),
            "replicate_signals": [list(signal) for signal in self.replicate_signals],
            "replicate_count": len(self.replicate_signals),
            "peaks": [dict(peak) for peak in self.peaks],
            "processed_estimates": dict(self.processed_estimates),
            "uncertainty": dict(self.uncertainty),
            "metadata": dict(self.metadata),
        }


def build_signal_spec_from_card(
    instrument_id: str,
    card: MechanismScenarioCard,
    network: ReactionNetworkSpec,
) -> InstrumentSignalSpec:
    return build_signal_spec(
        instrument_id,
        network.species_ids,
        target_species=card.target_species,
        impurity_species=card.impurity_species,
        formulas={species.species_id: species.formula for species in network.species},
    )


def build_signal_spec(
    instrument_id: str,
    species_ids: Sequence[str],
    *,
    target_species: Sequence[str] = (),
    impurity_species: Sequence[str] = (),
    formulas: Mapping[str, str] | None = None,
) -> InstrumentSignalSpec:
    features = default_feature_specs(
        instrument_id,
        species_ids,
        target_species=target_species,
        impurity_species=impurity_species,
        formulas={} if formulas is None else formulas,
    )
    if instrument_id == "hplc":
        return InstrumentSignalSpec(
            instrument_id="hplc",
            kind="hplc_chromatogram",
            axis_key="time_min",
            signal_key="intensity",
            axis_unit="min",
            axis_start=0.0,
            axis_stop=6.0,
            points=241,
            baseline=0.010,
            baseline_drift=0.004,
            noise_std=0.002,
            features=features,
        )
    if instrument_id == "gc":
        return InstrumentSignalSpec(
            instrument_id="gc",
            kind="gc_chromatogram",
            axis_key="time_min",
            signal_key="intensity",
            axis_unit="min",
            axis_start=0.0,
            axis_stop=4.0,
            points=201,
            baseline=0.008,
            baseline_drift=0.003,
            noise_std=0.0025,
            features=features,
        )
    if instrument_id == "uvvis":
        return InstrumentSignalSpec(
            instrument_id="uvvis",
            kind="uvvis_spectrum",
            axis_key="wavelength_nm",
            signal_key="absorbance",
            axis_unit="nm",
            axis_start=320.0,
            axis_stop=760.0,
            points=221,
            baseline=0.020,
            baseline_drift=0.006,
            noise_std=0.0015,
            features=features,
            normalize=False,
        )
    if instrument_id == "ir":
        return InstrumentSignalSpec(
            instrument_id="ir",
            kind="ir_spectrum",
            axis_key="wavenumber_cm-1",
            signal_key="transmittance",
            axis_unit="cm-1",
            axis_start=400.0,
            axis_stop=4000.0,
            points=241,
            baseline=0.0,
            baseline_drift=0.002,
            noise_std=0.001,
            features=features,
            normalize=False,
            signal_mode="transmittance",
        )
    if instrument_id == "nmr":
        return InstrumentSignalSpec(
            instrument_id="nmr",
            kind="nmr_1h_spectrum",
            axis_key="chemical_shift_ppm",
            signal_key="intensity",
            axis_unit="ppm",
            axis_start=0.0,
            axis_stop=12.0,
            points=241,
            baseline=0.004,
            baseline_drift=0.001,
            noise_std=0.001,
            features=features,
        )
    raise ValueError(f"Unsupported instrument_id={instrument_id!r}")


def default_feature_specs(
    instrument_id: str,
    species_ids: Sequence[str],
    *,
    target_species: Sequence[str] = (),
    impurity_species: Sequence[str] = (),
    formulas: Mapping[str, str] | None = None,
) -> tuple[SpectralFeatureSpec, ...]:
    targets = set(target_species)
    impurities = set(impurity_species)
    formula_map = {} if formulas is None else dict(formulas)
    features: list[SpectralFeatureSpec] = []
    for species_id in species_ids:
        role = _species_role(species_id, targets=targets, impurities=impurities)
        features.extend(_features_for_species(instrument_id, species_id, role, formula_map))
    return tuple(features)


def synthesize_signal(
    spec: InstrumentSignalSpec,
    amounts_mol: Mapping[str, float],
    *,
    volume_L: float,
    seed: int = 0,
    replicate_count: int = 1,
) -> SpectralMeasurement:
    if volume_L <= 0.0:
        raise ValueError("volume_L must be positive")
    if replicate_count <= 0:
        raise ValueError("replicate_count must be positive")
    concentrations = {
        species_id: max(float(amount), 0.0) / volume_L
        for species_id, amount in amounts_mol.items()
    }
    axis = spec.axis
    peaks = _feature_peaks(spec.features, concentrations)
    overlap_groups = detect_peak_overlap(peaks)
    detected_peaks = _annotate_peaks(peaks, overlap_groups)
    rng = np.random.default_rng(seed)
    replicate_signals: list[tuple[float, ...]] = []
    for _ in range(replicate_count):
        signal = _baseline(axis, spec.baseline, spec.baseline_drift)
        for peak in peaks:
            if bool(peak["detected"]):
                signal += _peak_shape(axis, peak)
        if spec.signal_mode == "transmittance":
            signal = np.clip(1.0 - signal, 0.02, 1.0)
        if spec.noise_std:
            signal = signal + rng.normal(0.0, spec.noise_std, size=signal.shape)
        if spec.signal_mode == "transmittance":
            signal = np.clip(signal, 0.0, 1.0)
        else:
            signal = np.clip(signal, 0.0, None)
            if spec.normalize and float(np.max(signal)) > 0.0:
                signal = signal / float(np.max(signal))
        replicate_signals.append(tuple(_rounded_array(signal)))
    mean_signal = tuple(
        _rounded_array(np.mean(np.array(replicate_signals, dtype=float), axis=0))
    )
    processed, uncertainty = _processed_from_peaks(
        spec.features,
        concentrations,
        detected_peaks,
        replicate_count=replicate_count,
    )
    return SpectralMeasurement(
        instrument_id=spec.instrument_id,
        kind=spec.kind,
        axis_key=spec.axis_key,
        signal_key=spec.signal_key,
        axis=tuple(_rounded_array(axis)),
        signal=mean_signal,
        replicate_signals=tuple(replicate_signals),
        peaks=tuple(detected_peaks),
        processed_estimates=processed,
        uncertainty=uncertainty,
        metadata={
            "axis_unit": spec.axis_unit,
            "baseline": spec.baseline,
            "baseline_drift": spec.baseline_drift,
            "calibration_profile": f"{spec.instrument_id}_species_calibration_v1",
            "detection_limits_mol_L": {
                feature.species_id: feature.detection_limit_mol_L
                for feature in spec.features
            },
            "peak_overlap": any(bool(peak["overlap_group"]) for peak in detected_peaks),
        },
    )


def synthesize_signal_from_card(
    instrument_id: str,
    card: MechanismScenarioCard,
    network: ReactionNetworkSpec,
    amounts_mol: Mapping[str, float],
    *,
    volume_L: float,
    seed: int = 0,
    replicate_count: int = 1,
) -> SpectralMeasurement:
    spec = build_signal_spec_from_card(instrument_id, card, network)
    return synthesize_signal(
        spec,
        amounts_mol,
        volume_L=volume_L,
        seed=seed,
        replicate_count=replicate_count,
    )


def detect_peak_overlap(peaks: Sequence[Mapping[str, object]]) -> dict[int, int]:
    groups: dict[int, int] = {}
    next_group = 1
    for idx, peak in enumerate(peaks):
        if not bool(peak["detected"]):
            continue
        center = _as_float(peak["center"])
        width = _as_float(peak["width"])
        for other_idx, other in enumerate(peaks[:idx]):
            if not bool(other["detected"]):
                continue
            distance = abs(center - _as_float(other["center"]))
            limit = 0.85 * (width + _as_float(other["width"]))
            if distance <= limit:
                group = groups.get(other_idx, next_group)
                groups[other_idx] = group
                groups[idx] = group
                if group == next_group:
                    next_group += 1
                break
    return groups


def _features_for_species(
    instrument_id: str,
    species_id: str,
    role: str,
    formulas: Mapping[str, str],
) -> tuple[SpectralFeatureSpec, ...]:
    if instrument_id == "hplc":
        return (_chromatography_feature(instrument_id, species_id, role),)
    if instrument_id == "gc":
        if not _gc_visible(species_id, role):
            return ()
        return (_chromatography_feature(instrument_id, species_id, role),)
    if instrument_id == "uvvis":
        return (_uvvis_feature(species_id, role),)
    if instrument_id == "ir":
        return _ir_features(species_id, role, formulas.get(species_id, ""))
    if instrument_id == "nmr":
        return _nmr_features(species_id, role)
    raise ValueError(f"Unsupported instrument_id={instrument_id!r}")


def _chromatography_feature(
    instrument_id: str,
    species_id: str,
    role: str,
) -> SpectralFeatureSpec:
    if instrument_id == "hplc":
        centers = {
            "reactant": 1.15,
            "target": 2.62,
            "byproduct": 3.28,
            "degradation": 4.05,
            "catalyst": 5.25,
            "other": 2.10,
        }
        width = 0.055 if role in {"reactant", "target"} else 0.085
        response = 950.0 if role == "target" else 620.0
        detection = 0.0008
    else:
        centers = {
            "reactant": 0.82,
            "target": 2.35,
            "byproduct": 1.08,
            "degradation": 1.72,
            "catalyst": 3.40,
            "other": 1.55,
        }
        width = 0.040 if role in {"reactant", "byproduct"} else 0.060
        response = 760.0 if role == "target" else 560.0
        detection = 0.0012
    center = centers.get(role, centers["other"]) + _stable_offset(species_id, scale=0.18)
    return SpectralFeatureSpec(
        species_id=species_id,
        instrument_id=instrument_id,
        center=center,
        width=width,
        response_factor=response,
        detection_limit_mol_L=detection,
        assignment=f"{species_id}_{role}",
        group=role,
        calibration=CalibrationCurve(
            slope=response,
            lower_limit=detection,
            upper_limit=5.0,
            noise_relative=0.025,
        ),
    )


def _uvvis_feature(species_id: str, role: str) -> SpectralFeatureSpec:
    centers = {
        "reactant": 365.0,
        "target": 430.0,
        "byproduct": 515.0,
        "degradation": 560.0,
        "catalyst": 680.0,
        "other": 470.0,
    }
    center = centers.get(role, centers["other"]) + _stable_offset(species_id, scale=18.0)
    return SpectralFeatureSpec(
        species_id=species_id,
        instrument_id="uvvis",
        center=center,
        width=34.0 if role != "catalyst" else 48.0,
        response_factor=0.75 if role == "target" else 0.45,
        detection_limit_mol_L=0.0025,
        assignment=f"{species_id}_{role}_band",
        group=role,
        calibration=CalibrationCurve(
            slope=0.75 if role == "target" else 0.45,
            lower_limit=0.0025,
            upper_limit=5.0,
            noise_relative=0.05,
        ),
    )


def _ir_features(species_id: str, role: str, formula: str) -> tuple[SpectralFeatureSpec, ...]:
    formula_upper = formula.upper()
    centers = [1180.0 + _stable_offset(species_id, scale=35.0)]
    if "O" in formula_upper and "C" in formula_upper:
        centers.append(1720.0 + _stable_offset(species_id + "carbonyl", scale=40.0))
    if "H" in formula_upper and "O" in formula_upper:
        centers.append(3360.0 + _stable_offset(species_id + "oh", scale=60.0))
    if "C" in formula_upper and "H" in formula_upper:
        centers.append(2960.0 + _stable_offset(species_id + "ch", scale=45.0))
    response = 0.18 if role == "target" else 0.12
    return tuple(
        SpectralFeatureSpec(
            species_id=species_id,
            instrument_id="ir",
            center=center,
            width=65.0 if center < 2000.0 else 120.0,
            response_factor=response,
            detection_limit_mol_L=0.004,
            assignment=f"{species_id}_{role}_ir_{idx}",
            group=role,
            calibration=CalibrationCurve(
                slope=response,
                lower_limit=0.004,
                upper_limit=5.0,
                noise_relative=0.06,
            ),
        )
        for idx, center in enumerate(centers)
    )


def _nmr_features(species_id: str, role: str) -> tuple[SpectralFeatureSpec, ...]:
    centers = {
        "reactant": (2.05, 4.20),
        "target": (1.28, 3.72),
        "byproduct": (2.40, 6.85),
        "degradation": (2.20, 9.55),
        "catalyst": (0.65,),
        "other": (3.20,),
    }
    response = 0.35 if role == "target" else 0.24
    return tuple(
        SpectralFeatureSpec(
            species_id=species_id,
            instrument_id="nmr",
            center=center + _stable_offset(f"{species_id}{idx}", scale=0.08),
            width=0.045 if center < 5.0 else 0.070,
            response_factor=response,
            detection_limit_mol_L=0.003,
            assignment=f"{species_id}_{role}_nmr_{idx}",
            group=role,
            calibration=CalibrationCurve(
                slope=response,
                lower_limit=0.003,
                upper_limit=5.0,
                noise_relative=0.04,
            ),
        )
        for idx, center in enumerate(centers.get(role, centers["other"]))
    )


def _species_role(species_id: str, *, targets: set[str], impurities: set[str]) -> str:
    lowered = species_id.lower()
    if species_id in targets:
        return "target"
    if species_id in impurities:
        if lowered.startswith("d") or "degrad" in lowered:
            return "degradation"
        return "byproduct"
    if lowered in {"a", "acid", "alcohol", "ox"} or "reactant" in lowered:
        return "reactant"
    if lowered.startswith("cat"):
        return "catalyst"
    if lowered.startswith("p") or species_id in {"Ester", "Red"}:
        return "target"
    if lowered.startswith(("b", "s", "d", "e")) or "impurity" in lowered:
        return "byproduct"
    return "other"


def _gc_visible(species_id: str, role: str) -> bool:
    lowered = species_id.lower()
    if "vapor" in lowered or "volatile" in lowered:
        return True
    if any(token in lowered for token in ("alcohol", "water", "ether", "solvent")):
        return True
    return role in {"byproduct", "degradation", "target"}


def _feature_peaks(
    features: Sequence[SpectralFeatureSpec],
    concentrations_mol_L: Mapping[str, float],
) -> list[dict[str, object]]:
    peaks: list[dict[str, object]] = []
    for feature in features:
        concentration = max(float(concentrations_mol_L.get(feature.species_id, 0.0)), 0.0)
        detected = concentration >= feature.detection_limit_mol_L
        raw_area = feature.calibration.response(concentration) * feature.response_factor
        area = raw_area if detected else 0.0
        peaks.append(
            {
                "species_id": feature.species_id,
                "assignment": feature.assignment,
                "group": feature.group,
                "center": feature.center,
                "width": feature.width,
                "area": area,
                "detected": detected,
                "detection_limit_mol_L": feature.detection_limit_mol_L,
                "response_factor": feature.response_factor,
                "shape": feature.shape,
                "calibration": feature.calibration,
            }
        )
    return peaks


def _annotate_peaks(
    peaks: Sequence[Mapping[str, object]],
    overlap_groups: Mapping[int, int],
) -> list[dict[str, object]]:
    annotated: list[dict[str, object]] = []
    for idx, peak in enumerate(peaks):
        calibration = peak["calibration"]
        if not isinstance(calibration, CalibrationCurve):
            raise TypeError("Internal peak calibration must be a CalibrationCurve")
        area = _as_float(peak["area"])
        response = area / max(_as_float(peak["response_factor"]), 1.0e-12)
        estimated = calibration.estimate_concentration(response)
        annotated.append(
            {
                "species_id": str(peak["species_id"]),
                "assignment": str(peak["assignment"]),
                "group": str(peak["group"]),
                "center": round(_as_float(peak["center"]), 6),
                "width": round(_as_float(peak["width"]), 6),
                "area": round(area, 6),
                "detected": bool(peak["detected"]),
                "detection_limit_mol_L": round(
                    _as_float(peak["detection_limit_mol_L"]),
                    9,
                ),
                "estimated_concentration_mol_L": round(estimated, 9),
                "overlap_group": overlap_groups.get(idx),
            }
        )
    return annotated


def _processed_from_peaks(
    features: Sequence[SpectralFeatureSpec],
    concentrations: Mapping[str, float],
    peaks: Sequence[Mapping[str, object]],
    *,
    replicate_count: int,
) -> tuple[dict[str, float], dict[str, float]]:
    by_species_feature = {(feature.species_id, feature.assignment): feature for feature in features}
    estimates: dict[str, list[float]] = {}
    uncertainties: dict[str, list[float]] = {}
    for peak in peaks:
        if not bool(peak["detected"]):
            continue
        species_id = str(peak["species_id"])
        assignment = str(peak["assignment"])
        feature = by_species_feature[(species_id, assignment)]
        concentration = concentrations.get(species_id, 0.0)
        relative = feature.calibration.noise_relative / sqrt(float(replicate_count))
        estimates.setdefault(species_id, []).append(float(concentration))
        uncertainties.setdefault(species_id, []).append(max(concentration * relative, 1.0e-9))
    processed = {
        species_id: round(float(np.mean(values)), 9)
        for species_id, values in sorted(estimates.items())
    }
    uncertainty = {
        f"{species_id}_std_mol_L": round(float(np.mean(values)), 9)
        for species_id, values in sorted(uncertainties.items())
    }
    return processed, uncertainty


def _baseline(axis: np.ndarray, intercept: float, drift: float) -> np.ndarray:
    span = max(float(axis[-1] - axis[0]), 1.0)
    normalized = (axis - axis[0]) / span
    return intercept + drift * normalized


def _peak_shape(axis: np.ndarray, peak: Mapping[str, object]) -> np.ndarray:
    center = _as_float(peak["center"])
    width = max(_as_float(peak["width"]), 1.0e-9)
    area = _as_float(peak["area"])
    if str(peak["shape"]) == "lorentzian":
        gamma = width / 2.0
        return area * (gamma / np.pi) / ((axis - center) ** 2 + gamma**2)
    height = area / (width * np.sqrt(2.0 * np.pi))
    return height * np.exp(-0.5 * ((axis - center) / width) ** 2)


def _stable_offset(text: str, *, scale: float) -> float:
    bucket = sum((idx + 1) * ord(char) for idx, char in enumerate(text)) % 101
    return ((bucket / 100.0) - 0.5) * scale


def _rounded_array(values: np.ndarray, digits: int = 6) -> list[float]:
    return [round(float(value), digits) for value in values]


def _as_float(value: object) -> float:
    if isinstance(value, int | float | str):
        return float(value)
    raise TypeError(f"Expected a numeric value, got {type(value).__name__}")


__all__ = [
    "CalibrationCurve",
    "InstrumentSignalSpec",
    "SpectralFeatureSpec",
    "SpectralMeasurement",
    "build_signal_spec",
    "build_signal_spec_from_card",
    "default_feature_specs",
    "detect_peak_overlap",
    "synthesize_signal",
    "synthesize_signal_from_card",
]
