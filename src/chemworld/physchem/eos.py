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

from chemworld.physchem.maturity import MaturityLevel, ModelCard, ValidationEvidence

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
    a_c: float
    a_alpha: float
    b: float
    alpha: float
    kappa: float
    da_alpha_dT: float

    def to_dict(self) -> dict[str, object]:
        return {
            "component_id": self.component_id,
            "a_c": self.a_c,
            "a_alpha": self.a_alpha,
            "b": self.b,
            "alpha": self.alpha,
            "kappa": self.kappa,
            "da_alpha_dT": self.da_alpha_dT,
        }


@dataclass(frozen=True)
class EOSMixtureParameters:
    a_mix: float
    da_mix_dT: float
    b_mix: float
    a_matrix: tuple[tuple[float, ...], ...]
    da_matrix_dT: tuple[tuple[float, ...], ...]
    b_values: tuple[float, ...]
    pure_parameters: tuple[CubicPureParameters, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "a_mix": self.a_mix,
            "da_mix_dT": self.da_mix_dT,
            "b_mix": self.b_mix,
            "a_matrix": [list(row) for row in self.a_matrix],
            "da_matrix_dT": [list(row) for row in self.da_matrix_dT],
            "b_values": list(self.b_values),
            "pure_parameters": [params.to_dict() for params in self.pure_parameters],
        }


@dataclass(frozen=True)
class CubicResidualProperties:
    model: CubicModel
    z_factor: float
    root_selection_policy: str
    molar_residual_enthalpy_J_mol: float
    molar_residual_entropy_J_mol_K: float
    molar_residual_gibbs_J_mol: float
    departure_log_argument: float
    da_mix_dT: float

    def to_dict(self) -> dict[str, object]:
        return {
            "model": self.model,
            "z_factor": self.z_factor,
            "root_selection_policy": self.root_selection_policy,
            "molar_residual_enthalpy_J_mol": self.molar_residual_enthalpy_J_mol,
            "molar_residual_entropy_J_mol_K": self.molar_residual_entropy_J_mol_K,
            "molar_residual_gibbs_J_mol": self.molar_residual_gibbs_J_mol,
            "departure_log_argument": self.departure_log_argument,
            "da_mix_dT": self.da_mix_dT,
        }


@dataclass(frozen=True)
class EOSState:
    eos_id: str
    model: str
    phase: str
    root_selection_policy: str
    temperature_K: float
    pressure_Pa: float
    composition: dict[str, float]
    compressibility_factor: float
    molar_volume_m3_mol: float
    fugacity_coefficients: dict[str, float]
    molar_residual_enthalpy_J_mol: float
    molar_residual_entropy_J_mol_K: float
    molar_residual_gibbs_J_mol: float
    roots: tuple[float, ...]
    mixture_parameters: dict[str, object] = field(default_factory=dict)
    residual_properties: dict[str, object] = field(default_factory=dict)

    def to_dict(self) -> dict[str, object]:
        return {
            "eos_id": self.eos_id,
            "model": self.model,
            "phase": self.phase,
            "root_selection_policy": self.root_selection_policy,
            "temperature_K": self.temperature_K,
            "pressure_Pa": self.pressure_Pa,
            "composition": dict(self.composition),
            "compressibility_factor": self.compressibility_factor,
            "molar_volume_m3_mol": self.molar_volume_m3_mol,
            "fugacity_coefficients": dict(self.fugacity_coefficients),
            "molar_residual_enthalpy_J_mol": self.molar_residual_enthalpy_J_mol,
            "molar_residual_entropy_J_mol_K": self.molar_residual_entropy_J_mol_K,
            "molar_residual_gibbs_J_mol": self.molar_residual_gibbs_J_mol,
            "roots": list(self.roots),
            "mixture_parameters": dict(self.mixture_parameters),
            "residual_properties": dict(self.residual_properties),
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
        root_selection_policy="ideal_single_root",
        temperature_K=temperature_K,
        pressure_Pa=pressure_Pa,
        composition=normalized,
        compressibility_factor=1.0,
        molar_volume_m3_mol=ideal_gas_molar_volume(temperature_K, pressure_Pa),
        fugacity_coefficients=dict.fromkeys(normalized, 1.0),
        molar_residual_enthalpy_J_mol=0.0,
        molar_residual_entropy_J_mol_K=0.0,
        molar_residual_gibbs_J_mol=0.0,
        roots=(1.0,),
        residual_properties=CubicResidualProperties(
            model="peng_robinson",
            z_factor=1.0,
            root_selection_policy="ideal_single_root",
            molar_residual_enthalpy_J_mol=0.0,
            molar_residual_entropy_J_mol_K=0.0,
            molar_residual_gibbs_J_mol=0.0,
            departure_log_argument=1.0,
            da_mix_dT=0.0,
        ).to_dict(),
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
    alpha_base = 1.0 + kappa * (1.0 - tr_sqrt)
    alpha = alpha_base**2
    d_alpha_dT = -kappa * alpha_base / (
        component.critical_temperature_K * max(tr_sqrt, 1e-300)
    )
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
        a_c=a,
        a_alpha=a * alpha,
        b=b,
        alpha=alpha,
        kappa=kappa,
        da_alpha_dT=a * d_alpha_dT,
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
    da_matrix_dT = [[0.0 for _ in range(n)] for _ in range(n)]
    for i, left in enumerate(spec.components):
        for j, right in enumerate(spec.components):
            kij = _binary_interaction(spec, left.component_id, right.component_id)
            a_matrix[i][j] = sqrt(pure[i].a_alpha * pure[j].a_alpha) * (1.0 - kij)
            da_matrix_dT[i][j] = _cross_a_temperature_derivative(
                pure[i],
                pure[j],
                kij=kij,
            )
    a_mix = sum(x[i] * x[j] * a_matrix[i][j] for i in range(n) for j in range(n))
    da_mix_dT = sum(
        x[i] * x[j] * da_matrix_dT[i][j] for i in range(n) for j in range(n)
    )
    b_values = tuple(params.b for params in pure)
    b_mix = sum(x[i] * b_values[i] for i in range(n))
    if a_mix < 0 or b_mix <= 0:
        raise ValueError("Invalid cubic mixture parameters")
    return EOSMixtureParameters(
        a_mix=a_mix,
        da_mix_dT=da_mix_dT,
        b_mix=b_mix,
        a_matrix=tuple(tuple(row) for row in a_matrix),
        da_matrix_dT=tuple(tuple(row) for row in da_matrix_dT),
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
    root_selection_policy = cubic_root_selection_policy(phase=phase, roots=roots)
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
    residuals = cubic_residual_properties(
        spec,
        normalized,
        z_factor=z_factor,
        mixture=mixture,
        temperature_K=temperature_K,
        pressure_Pa=pressure_Pa,
        root_selection_policy=root_selection_policy,
        fugacity_coefficients=fugacity,
    )
    return EOSState(
        eos_id=spec.eos_id,
        model=spec.model,
        phase=phase,
        root_selection_policy=root_selection_policy,
        temperature_K=temperature_K,
        pressure_Pa=pressure_Pa,
        composition=normalized,
        compressibility_factor=z_factor,
        molar_volume_m3_mol=z_factor * ideal_gas_molar_volume(temperature_K, pressure_Pa),
        fugacity_coefficients=fugacity,
        molar_residual_enthalpy_J_mol=residuals.molar_residual_enthalpy_J_mol,
        molar_residual_entropy_J_mol_K=residuals.molar_residual_entropy_J_mol_K,
        molar_residual_gibbs_J_mol=residuals.molar_residual_gibbs_J_mol,
        roots=roots,
        mixture_parameters=mixture.to_dict(),
        residual_properties=residuals.to_dict(),
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


def cubic_root_selection_policy(
    *,
    phase: PhaseRoot,
    roots: tuple[float, ...],
) -> str:
    if not roots:
        raise ValueError("roots cannot be empty")
    if len(roots) == 1:
        return "single_admissible_root"
    if phase == "liquid":
        return "smallest_z_liquid"
    if phase == "vapor":
        return "largest_z_vapor"
    if phase == "stable":
        return "minimum_molar_residual_gibbs"
    raise ValueError(f"Unsupported phase root selector: {phase}")


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


def cubic_departure_log_argument(
    *,
    model: CubicModel,
    z_factor: float,
    b_reduced: float,
) -> float:
    if b_reduced < 0.0 or not isfinite(b_reduced):
        raise ValueError("b_reduced must be finite and nonnegative")
    if z_factor <= b_reduced or not isfinite(z_factor):
        raise ValueError("z_factor must be finite and greater than B")
    if b_reduced <= 1e-14:
        return 1.0
    if model == "peng_robinson":
        sqrt2 = sqrt(2.0)
        log_argument = (z_factor + (1.0 + sqrt2) * b_reduced) / (
            z_factor + (1.0 - sqrt2) * b_reduced
        )
    elif model == "srk":
        log_argument = (z_factor + b_reduced) / z_factor
    else:
        raise ValueError(f"Unsupported cubic EOS model: {model}")
    if log_argument <= 0.0 or not isfinite(log_argument):
        raise ValueError("cubic departure logarithm argument is not positive")
    return log_argument


def cubic_residual_properties(
    spec: CubicEOSSpec,
    composition: Mapping[str, float],
    *,
    z_factor: float,
    mixture: EOSMixtureParameters,
    temperature_K: float,
    pressure_Pa: float,
    root_selection_policy: str,
    fugacity_coefficients: Mapping[str, float] | None = None,
) -> CubicResidualProperties:
    _validate_tp(temperature_K, pressure_Pa)
    x = _composition_vector(spec, composition)
    a_reduced, b_reduced = cubic_ab(
        mixture,
        temperature_K=temperature_K,
        pressure_Pa=pressure_Pa,
    )
    if b_reduced <= 1e-14 or a_reduced <= 1e-14:
        return CubicResidualProperties(
            model=spec.model,
            z_factor=z_factor,
            root_selection_policy=root_selection_policy,
            molar_residual_enthalpy_J_mol=0.0,
            molar_residual_entropy_J_mol_K=0.0,
            molar_residual_gibbs_J_mol=0.0,
            departure_log_argument=1.0,
            da_mix_dT=mixture.da_mix_dT,
        )

    log_argument = cubic_departure_log_argument(
        model=spec.model,
        z_factor=z_factor,
        b_reduced=b_reduced,
    )
    if spec.model == "peng_robinson":
        denominator = 2.0 * sqrt(2.0) * mixture.b_mix
    elif spec.model == "srk":
        denominator = mixture.b_mix
    else:
        raise ValueError(f"Unsupported cubic EOS model: {spec.model}")
    if denominator <= 0.0:
        raise ValueError("cubic residual denominator must be positive")

    departure_log = log(log_argument)
    attractive_departure = (
        (temperature_K * mixture.da_mix_dT - mixture.a_mix)
        / denominator
        * departure_log
    )
    entropy_departure = mixture.da_mix_dT / denominator * departure_log
    residual_enthalpy = (
        R_J_PER_MOL_K * temperature_K * (z_factor - 1.0) + attractive_departure
    )
    z_minus_b = z_factor - b_reduced
    if z_minus_b <= 0.0:
        raise ValueError("z_factor - B must be positive for residual entropy")
    residual_entropy = R_J_PER_MOL_K * log(z_minus_b) + entropy_departure
    if fugacity_coefficients is None:
        fugacity_coefficients = cubic_fugacity_coefficients(
            spec,
            composition,
            z_factor=z_factor,
            mixture=mixture,
            temperature_K=temperature_K,
            pressure_Pa=pressure_Pa,
        )
    residual_gibbs = R_J_PER_MOL_K * temperature_K * sum(
        x[index] * log(max(float(fugacity_coefficients[component_id]), 1e-300))
        for index, component_id in enumerate(spec.component_ids)
    )
    return CubicResidualProperties(
        model=spec.model,
        z_factor=z_factor,
        root_selection_policy=root_selection_policy,
        molar_residual_enthalpy_J_mol=residual_enthalpy,
        molar_residual_entropy_J_mol_K=residual_entropy,
        molar_residual_gibbs_J_mol=residual_gibbs,
        departure_log_argument=log_argument,
        da_mix_dT=mixture.da_mix_dT,
    )


def eos_model_cards() -> tuple[ModelCard, ...]:
    return (
        ModelCard(
            model_id="cubic_eos_pr_srk_residuals",
            module_id="eos",
            title="Peng-Robinson/SRK Cubic EOS Fugacity And Residual Properties",
            maturity=MaturityLevel.REFERENCE_VALIDATED,
            summary=(
                "Compact PR/SRK cubic-EOS slice with one-fluid mixing, explicit "
                "root selection, fugacity coefficients, and molar residual "
                "enthalpy/entropy/Gibbs properties."
            ),
            equations=(
                "a_i(T)=Omega_a R^2 Tc_i^2/Pc_i alpha_i(T)",
                "b_i=Omega_b R Tc_i/Pc_i",
                "a_mix=sum_i sum_j x_i x_j sqrt(a_i a_j)(1-k_ij)",
                "b_mix=sum_i x_i b_i",
                "PR: H^R=RT(Z-1)+(T da/dT-a)/(2 sqrt(2) b) ln((Z+(1+sqrt(2))B)/(Z+(1-sqrt(2))B))",
                "SRK: H^R=RT(Z-1)+(T da/dT-a)/b ln((Z+B)/Z)",
                "S^R=R ln(Z-B)+(da/dT/c) ln(argument), with c=2 sqrt(2) b for PR and b for SRK",
            ),
            assumptions=(
                "Classical quadratic mixing rules with optional symmetric k_ij.",
                "Pure-component alpha functions use the standard PR and SRK acentric-factor forms.",
                "Residual properties are molar mixture departures from ideal gas "
                "at the same T/P/composition.",
            ),
            validity_limits=(
                "Requires positive critical temperature, critical pressure, "
                "pressure, and temperature.",
                "Root selection is explicit but no phase-stability or "
                "phase-envelope solve is claimed.",
                "Near-critical and highly associating/polar fluids require "
                "stronger EOS or fitted parameters.",
            ),
            failure_modes=(
                "No admissible real Z root raises ValueError.",
                "Invalid composition ids, negative composition entries, or "
                "nonpositive log arguments raise ValueError.",
                "Missing binary parameters default to k_ij=0 and should be "
                "governed by scenario metadata.",
            ),
            units={
                "temperature": "K",
                "pressure": "Pa",
                "molar_volume": "m^3/mol",
                "residual_enthalpy": "J/mol",
                "residual_entropy": "J/(mol*K)",
                "fugacity_coefficient": "dimensionless",
            },
            reference_reading=(
                "reference_repos/thermo/thermo/eos.py "
                "main_derivatives_and_departures and PR/SRK classes",
                "reference_repos/phasepy/phasepy/cubic/cubicpure.py and "
                "cubicmix.py logfug/EntropyR/EnthalpyR APIs",
                "reference_repos/thermopack/addon/pycThermopack/thermopack/"
                "thermo.py residual enthalpy/entropy API",
                "reference_repos/teqp/teqp/__init__.py exposes fugacity and "
                "critical/VLE architecture hooks",
            ),
            validation_evidence=(
                ValidationEvidence(
                    evidence_id="default-eos-residual-tests",
                    evidence_type="unit_tests",
                    description=(
                        "Default tests cover low-pressure ideal-gas limits, explicit "
                        "root policy, Gibbs consistency with fugacity coefficients, "
                        "and positive PR/SRK mixture fugacity coefficients."
                    ),
                    status="passing",
                    command_or_path="python -m pytest tests/test_eos.py",
                    tolerance="relative tolerances documented in tests",
                ),
                ValidationEvidence(
                    evidence_id="optional-thermo-eos-reference",
                    evidence_type="optional_reference_backend",
                    description=(
                        "Optional checks compare selected pure-fluid PR/SRK vapor "
                        "root Z, phi, H_dep, and S_dep against thermo.eos when "
                        "CHEMWORLD_RUN_REFERENCE_TESTS=1."
                    ),
                    status="optional",
                    reference_backend="thermo",
                    command_or_path=(
                        "CHEMWORLD_RUN_REFERENCE_TESTS=1 python -m pytest "
                        "tests/reference/test_optional_reference_backends.py"
                    ),
                    tolerance="1e-6 relative for reference backend comparisons",
                ),
            ),
            intended_use=(
                "Benchmark dense-gas and vapor-loss calculations.",
                "Future flash, distillation, and reactor energy-balance modules "
                "that need compact residual properties.",
            ),
        ),
    )


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


def _cross_a_temperature_derivative(
    left: CubicPureParameters,
    right: CubicPureParameters,
    *,
    kij: float,
) -> float:
    if left.a_alpha <= 0.0 or right.a_alpha <= 0.0:
        return 0.0
    cross_a = sqrt(left.a_alpha * right.a_alpha) * (1.0 - kij)
    return 0.5 * cross_a * (
        left.da_alpha_dT / left.a_alpha + right.da_alpha_dT / right.a_alpha
    )


__all__ = [
    "CubicEOSSpec",
    "CubicModel",
    "CubicPureParameters",
    "CubicResidualProperties",
    "EOSComponentSpec",
    "EOSMixtureParameters",
    "EOSState",
    "PhaseRoot",
    "cubic_ab",
    "cubic_compressibility_roots",
    "cubic_departure_log_argument",
    "cubic_fugacity_coefficients",
    "cubic_mixture_parameters",
    "cubic_pure_parameters",
    "cubic_residual_properties",
    "cubic_root_selection_policy",
    "eos_model_cards",
    "evaluate_cubic_eos",
    "ideal_gas_molar_volume",
    "ideal_gas_pressure",
    "ideal_gas_state",
    "select_cubic_root",
]
