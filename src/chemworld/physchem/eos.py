"""Equation-of-state utilities for ChemWorld.

This module implements a compact local EOS core for benchmark use. It supports
ideal-gas states plus Peng-Robinson and Soave-Redlich-Kwong cubic equations of
state with classical one-fluid mixing rules and fugacity coefficients.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from math import exp, isfinite, log, sqrt
from typing import Literal

import numpy as np

R_J_PER_MOL_K = 8.31446261815324
CubicModel = Literal["peng_robinson", "srk"]
PhaseRoot = Literal["vapor", "liquid", "stable"]


@dataclass(frozen=True)
class EOSComponentSpec:
    component_id: str
    critical_temperature_K: float
    critical_pressure_Pa: float
    acentric_factor: float = 0.0

    def __post_init__(self) -> None:
        if not self.component_id:
            raise ValueError("component_id cannot be empty")
        if self.critical_temperature_K <= 0:
            raise ValueError("critical_temperature_K must be positive")
        if self.critical_pressure_Pa <= 0:
            raise ValueError("critical_pressure_Pa must be positive")

    def to_dict(self) -> dict[str, object]:
        return {
            "component_id": self.component_id,
            "critical_temperature_K": self.critical_temperature_K,
            "critical_pressure_Pa": self.critical_pressure_Pa,
            "acentric_factor": self.acentric_factor,
        }


@dataclass(frozen=True)
class CubicEOSSpec:
    eos_id: str
    model: CubicModel
    components: tuple[EOSComponentSpec, ...]
    binary_interaction: dict[str, float] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.model not in {"peng_robinson", "srk"}:
            raise ValueError(f"Unsupported cubic EOS model: {self.model}")
        if not self.components:
            raise ValueError("Cubic EOS requires at least one component")
        ids = [component.component_id for component in self.components]
        if len(ids) != len(set(ids)):
            raise ValueError("Duplicate EOS component ids are not allowed")
        if any(not isfinite(value) for value in self.binary_interaction.values()):
            raise ValueError("binary interaction values must be finite")

    @property
    def component_ids(self) -> tuple[str, ...]:
        return tuple(component.component_id for component in self.components)

    def to_dict(self) -> dict[str, object]:
        return {
            "eos_id": self.eos_id,
            "model": self.model,
            "components": [component.to_dict() for component in self.components],
            "binary_interaction": dict(self.binary_interaction),
        }


@dataclass(frozen=True)
class CubicPureParameters:
    component_id: str
    a_alpha: float
    b: float
    alpha: float
    kappa: float

    def to_dict(self) -> dict[str, object]:
        return {
            "component_id": self.component_id,
            "a_alpha": self.a_alpha,
            "b": self.b,
            "alpha": self.alpha,
            "kappa": self.kappa,
        }


@dataclass(frozen=True)
class EOSMixtureParameters:
    a_mix: float
    b_mix: float
    a_matrix: tuple[tuple[float, ...], ...]
    b_values: tuple[float, ...]
    pure_parameters: tuple[CubicPureParameters, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "a_mix": self.a_mix,
            "b_mix": self.b_mix,
            "a_matrix": [list(row) for row in self.a_matrix],
            "b_values": list(self.b_values),
            "pure_parameters": [params.to_dict() for params in self.pure_parameters],
        }


@dataclass(frozen=True)
class EOSState:
    eos_id: str
    model: str
    phase: str
    temperature_K: float
    pressure_Pa: float
    composition: dict[str, float]
    compressibility_factor: float
    molar_volume_m3_mol: float
    fugacity_coefficients: dict[str, float]
    roots: tuple[float, ...]
    mixture_parameters: dict[str, object] = field(default_factory=dict)

    def to_dict(self) -> dict[str, object]:
        return {
            "eos_id": self.eos_id,
            "model": self.model,
            "phase": self.phase,
            "temperature_K": self.temperature_K,
            "pressure_Pa": self.pressure_Pa,
            "composition": dict(self.composition),
            "compressibility_factor": self.compressibility_factor,
            "molar_volume_m3_mol": self.molar_volume_m3_mol,
            "fugacity_coefficients": dict(self.fugacity_coefficients),
            "roots": list(self.roots),
            "mixture_parameters": dict(self.mixture_parameters),
        }


def ideal_gas_molar_volume(temperature_K: float, pressure_Pa: float) -> float:
    _validate_tp(temperature_K, pressure_Pa)
    return R_J_PER_MOL_K * temperature_K / pressure_Pa


def ideal_gas_pressure(
    *,
    amount_mol: float,
    volume_m3: float,
    temperature_K: float,
) -> float:
    if amount_mol < 0:
        raise ValueError("amount_mol cannot be negative")
    if volume_m3 <= 0:
        raise ValueError("volume_m3 must be positive")
    if temperature_K <= 0:
        raise ValueError("temperature_K must be positive")
    return amount_mol * R_J_PER_MOL_K * temperature_K / volume_m3


def ideal_gas_state(
    composition: Mapping[str, float],
    *,
    temperature_K: float,
    pressure_Pa: float,
) -> EOSState:
    normalized = _normalize_composition(composition)
    return EOSState(
        eos_id="ideal_gas",
        model="ideal_gas",
        phase="vapor",
        temperature_K=temperature_K,
        pressure_Pa=pressure_Pa,
        composition=normalized,
        compressibility_factor=1.0,
        molar_volume_m3_mol=ideal_gas_molar_volume(temperature_K, pressure_Pa),
        fugacity_coefficients=dict.fromkeys(normalized, 1.0),
        roots=(1.0,),
    )


def cubic_pure_parameters(
    component: EOSComponentSpec,
    *,
    model: CubicModel,
    temperature_K: float,
) -> CubicPureParameters:
    if temperature_K <= 0:
        raise ValueError("temperature_K must be positive")
    tr_sqrt = sqrt(temperature_K / component.critical_temperature_K)
    omega = component.acentric_factor
    if model == "peng_robinson":
        omega_a = 0.45724
        omega_b = 0.07780
        kappa = 0.37464 + 1.54226 * omega - 0.26992 * omega**2
    elif model == "srk":
        omega_a = 0.42747
        omega_b = 0.08664
        kappa = 0.480 + 1.574 * omega - 0.176 * omega**2
    else:
        raise ValueError(f"Unsupported cubic EOS model: {model}")
    alpha = (1.0 + kappa * (1.0 - tr_sqrt)) ** 2
    a = (
        omega_a
        * R_J_PER_MOL_K**2
        * component.critical_temperature_K**2
        / component.critical_pressure_Pa
    )
    b = omega_b * R_J_PER_MOL_K * component.critical_temperature_K
    b /= component.critical_pressure_Pa
    return CubicPureParameters(
        component_id=component.component_id,
        a_alpha=a * alpha,
        b=b,
        alpha=alpha,
        kappa=kappa,
    )


def cubic_mixture_parameters(
    spec: CubicEOSSpec,
    composition: Mapping[str, float],
    *,
    temperature_K: float,
) -> EOSMixtureParameters:
    x = _composition_vector(spec, composition)
    pure = tuple(
        cubic_pure_parameters(component, model=spec.model, temperature_K=temperature_K)
        for component in spec.components
    )
    n = len(spec.components)
    a_matrix = [[0.0 for _ in range(n)] for _ in range(n)]
    for i, left in enumerate(spec.components):
        for j, right in enumerate(spec.components):
            kij = _binary_interaction(spec, left.component_id, right.component_id)
            a_matrix[i][j] = sqrt(pure[i].a_alpha * pure[j].a_alpha) * (1.0 - kij)
    a_mix = sum(x[i] * x[j] * a_matrix[i][j] for i in range(n) for j in range(n))
    b_values = tuple(params.b for params in pure)
    b_mix = sum(x[i] * b_values[i] for i in range(n))
    if a_mix < 0 or b_mix <= 0:
        raise ValueError("Invalid cubic mixture parameters")
    return EOSMixtureParameters(
        a_mix=a_mix,
        b_mix=b_mix,
        a_matrix=tuple(tuple(row) for row in a_matrix),
        b_values=b_values,
        pure_parameters=pure,
    )


def cubic_ab(
    mixture: EOSMixtureParameters,
    *,
    temperature_K: float,
    pressure_Pa: float,
) -> tuple[float, float]:
    _validate_tp(temperature_K, pressure_Pa)
    a_reduced = mixture.a_mix * pressure_Pa / (R_J_PER_MOL_K**2 * temperature_K**2)
    b_reduced = mixture.b_mix * pressure_Pa / (R_J_PER_MOL_K * temperature_K)
    return a_reduced, b_reduced


def cubic_compressibility_roots(
    spec: CubicEOSSpec,
    composition: Mapping[str, float],
    *,
    temperature_K: float,
    pressure_Pa: float,
) -> tuple[float, ...]:
    mixture = cubic_mixture_parameters(spec, composition, temperature_K=temperature_K)
    a_reduced, b_reduced = cubic_ab(
        mixture,
        temperature_K=temperature_K,
        pressure_Pa=pressure_Pa,
    )
    if spec.model == "peng_robinson":
        coefficients = (
            1.0,
            -(1.0 - b_reduced),
            a_reduced - 3.0 * b_reduced**2 - 2.0 * b_reduced,
            -(a_reduced * b_reduced - b_reduced**2 - b_reduced**3),
        )
    else:
        coefficients = (
            1.0,
            -1.0,
            a_reduced - b_reduced - b_reduced**2,
            -a_reduced * b_reduced,
        )
    roots = np.roots(coefficients)
    real_roots = sorted(
        float(root.real)
        for root in roots
        if abs(root.imag) < 1e-8 and root.real > b_reduced + 1e-10
    )
    if not real_roots:
        raise ValueError("Cubic EOS produced no physically admissible Z roots")
    return tuple(real_roots)


def evaluate_cubic_eos(
    spec: CubicEOSSpec,
    composition: Mapping[str, float],
    *,
    temperature_K: float,
    pressure_Pa: float,
    phase: PhaseRoot = "vapor",
) -> EOSState:
    _validate_tp(temperature_K, pressure_Pa)
    normalized = _normalize_composition(composition)
    mixture = cubic_mixture_parameters(spec, normalized, temperature_K=temperature_K)
    roots = cubic_compressibility_roots(
        spec,
        normalized,
        temperature_K=temperature_K,
        pressure_Pa=pressure_Pa,
    )
    z_factor = select_cubic_root(
        spec,
        normalized,
        roots=roots,
        mixture=mixture,
        temperature_K=temperature_K,
        pressure_Pa=pressure_Pa,
        phase=phase,
    )
    fugacity = cubic_fugacity_coefficients(
        spec,
        normalized,
        z_factor=z_factor,
        mixture=mixture,
        temperature_K=temperature_K,
        pressure_Pa=pressure_Pa,
    )
    return EOSState(
        eos_id=spec.eos_id,
        model=spec.model,
        phase=phase,
        temperature_K=temperature_K,
        pressure_Pa=pressure_Pa,
        composition=normalized,
        compressibility_factor=z_factor,
        molar_volume_m3_mol=z_factor * ideal_gas_molar_volume(temperature_K, pressure_Pa),
        fugacity_coefficients=fugacity,
        roots=roots,
        mixture_parameters=mixture.to_dict(),
    )


def select_cubic_root(
    spec: CubicEOSSpec,
    composition: Mapping[str, float],
    *,
    roots: tuple[float, ...],
    mixture: EOSMixtureParameters,
    temperature_K: float,
    pressure_Pa: float,
    phase: PhaseRoot,
) -> float:
    if phase == "liquid":
        return min(roots)
    if phase == "vapor":
        return max(roots)
    if phase != "stable":
        raise ValueError(f"Unsupported phase root selector: {phase}")
    normalized = _normalize_composition(composition)
    x = _composition_vector(spec, normalized)
    candidates = []
    for root in roots:
        fugacity = cubic_fugacity_coefficients(
            spec,
            normalized,
            z_factor=root,
            mixture=mixture,
            temperature_K=temperature_K,
            pressure_Pa=pressure_Pa,
        )
        residual_g = sum(
            x[index] * log(max(fugacity[component_id], 1e-300))
            for index, component_id in enumerate(spec.component_ids)
        )
        candidates.append((residual_g, root))
    return min(candidates)[1]


def cubic_fugacity_coefficients(
    spec: CubicEOSSpec,
    composition: Mapping[str, float],
    *,
    z_factor: float,
    mixture: EOSMixtureParameters,
    temperature_K: float,
    pressure_Pa: float,
) -> dict[str, float]:
    x = _composition_vector(spec, composition)
    a_reduced, b_reduced = cubic_ab(
        mixture,
        temperature_K=temperature_K,
        pressure_Pa=pressure_Pa,
    )
    if b_reduced <= 1e-14 or a_reduced <= 1e-14:
        return dict.fromkeys(spec.component_ids, 1.0)
    if z_factor <= b_reduced:
        raise ValueError("z_factor must be greater than reduced covolume B")
    a_mix = max(mixture.a_mix, 1e-300)
    b_mix = max(mixture.b_mix, 1e-300)
    coefficients = {}
    for i, component_id in enumerate(spec.component_ids):
        bi_over_b = mixture.b_values[i] / b_mix
        attraction_sum = sum(x[j] * mixture.a_matrix[i][j] for j in range(len(x)))
        attraction_term = 2.0 * attraction_sum / a_mix - bi_over_b
        if spec.model == "peng_robinson":
            sqrt2 = sqrt(2.0)
            log_argument = (
                z_factor + (1.0 + sqrt2) * b_reduced
            ) / (z_factor + (1.0 - sqrt2) * b_reduced)
            attraction = a_reduced / (2.0 * sqrt2 * b_reduced)
        else:
            log_argument = (z_factor + b_reduced) / z_factor
            attraction = a_reduced / b_reduced
        ln_phi = (
            bi_over_b * (z_factor - 1.0)
            - log(z_factor - b_reduced)
            - attraction * attraction_term * log(log_argument)
        )
        coefficients[component_id] = exp(ln_phi)
    return coefficients


def _validate_tp(temperature_K: float, pressure_Pa: float) -> None:
    if temperature_K <= 0:
        raise ValueError("temperature_K must be positive")
    if pressure_Pa <= 0:
        raise ValueError("pressure_Pa must be positive")


def _normalize_composition(composition: Mapping[str, float]) -> dict[str, float]:
    if not composition:
        raise ValueError("composition cannot be empty")
    if any(value < 0 or not isfinite(value) for value in composition.values()):
        raise ValueError("composition values must be finite and nonnegative")
    total = sum(composition.values())
    if total <= 0:
        raise ValueError("composition must contain positive material")
    return {component_id: float(value) / total for component_id, value in composition.items()}


def _composition_vector(
    spec: CubicEOSSpec,
    composition: Mapping[str, float],
) -> tuple[float, ...]:
    normalized = _normalize_composition(composition)
    missing = sorted(set(spec.component_ids) - set(normalized))
    extra = sorted(set(normalized) - set(spec.component_ids))
    if missing or extra:
        raise ValueError(f"Composition ids do not match EOS spec: missing={missing}, extra={extra}")
    return tuple(normalized[component_id] for component_id in spec.component_ids)


def _binary_interaction(spec: CubicEOSSpec, left: str, right: str) -> float:
    if left == right:
        return 0.0
    return float(
        spec.binary_interaction.get(
            f"{left}|{right}",
            spec.binary_interaction.get(f"{right}|{left}", 0.0),
        )
    )


__all__ = [
    "CubicEOSSpec",
    "CubicModel",
    "CubicPureParameters",
    "EOSComponentSpec",
    "EOSMixtureParameters",
    "EOSState",
    "PhaseRoot",
    "cubic_ab",
    "cubic_compressibility_roots",
    "cubic_fugacity_coefficients",
    "cubic_mixture_parameters",
    "cubic_pure_parameters",
    "evaluate_cubic_eos",
    "ideal_gas_molar_volume",
    "ideal_gas_pressure",
    "ideal_gas_state",
    "select_cubic_root",
]
