"""Phase-equilibrium utilities for ChemWorld.

The functions here provide a compact thermodynamic layer for benchmark tasks:
activity coefficients, Raoult-law K-values, isothermal flash, bubble/dew point
estimates, and a material-conserving liquid-liquid extraction stage.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from math import exp, isfinite, log
from typing import Literal

from chemworld.foundation.units import convert_value
from chemworld.physchem.equilibrium_cards import activity_model_cards
from chemworld.physchem.property_reports import ValidityPolicy
from chemworld.physchem.saturation import (
    PureSaturationReport,
    pure_saturation_pressure_report,
)
from chemworld.physchem.specs import PropertyCorrelation

ActivityModel = Literal["ideal", "margules", "wilson", "nrtl"]
VLESolveMode = Literal["bubble_temperature", "dew_temperature"]
FlashPhaseStatus = Literal["all_liquid", "two_phase", "all_vapor"]


@dataclass(frozen=True)
class ActivityModelSpec:
    model_id: str
    component_ids: tuple[str, ...]
    model: ActivityModel = "ideal"
    parameters: dict[str, float] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.model_id:
            raise ValueError("model_id cannot be empty")
        if self.model not in {"ideal", "margules", "wilson", "nrtl"}:
            raise ValueError(f"Unsupported activity model: {self.model}")
        if not self.component_ids:
            raise ValueError("component_ids cannot be empty")
        if len(self.component_ids) != len(set(self.component_ids)):
            raise ValueError("Duplicate component ids are not allowed")
        if any(not isfinite(value) for value in self.parameters.values()):
            raise ValueError("activity-model parameters must be finite")
        _validate_activity_parameter_contract(self)

    def to_dict(self) -> dict[str, object]:
        return {
            "model_id": self.model_id,
            "component_ids": list(self.component_ids),
            "model": self.model,
            "parameters": dict(self.parameters),
        }


@dataclass(frozen=True)
class FlashResult:
    vapor_fraction: float
    liquid_composition: dict[str, float]
    vapor_composition: dict[str, float]
    k_values: dict[str, float]

    def to_dict(self) -> dict[str, object]:
        return {
            "vapor_fraction": self.vapor_fraction,
            "liquid_composition": dict(self.liquid_composition),
            "vapor_composition": dict(self.vapor_composition),
            "k_values": dict(self.k_values),
        }


@dataclass(frozen=True)
class RachfordRiceDiagnosticReport:
    overall_composition: dict[str, float]
    k_values: dict[str, float]
    vapor_fraction: float
    liquid_composition: dict[str, float]
    vapor_composition: dict[str, float]
    objective_at_zero: float
    objective_at_one: float
    residual: float
    iterations: int
    phase_status: FlashPhaseStatus
    warnings: tuple[str, ...] = ()
    reference_reading: tuple[str, ...] = (
        "reference_repos/chemicals/chemicals/rachford_rice.py: "
        "Rachford-Rice objective conventions",
        "reference_repos/thermo/thermo/flash/flash_base.py: "
        "ideal flash workflow notes",
    )

    def __post_init__(self) -> None:
        if self.phase_status not in {"all_liquid", "two_phase", "all_vapor"}:
            raise ValueError("Unsupported Rachford-Rice phase status")
        if not 0.0 <= self.vapor_fraction <= 1.0:
            raise ValueError("vapor_fraction must be in [0, 1]")
        for field_name in (
            "objective_at_zero",
            "objective_at_one",
            "residual",
        ):
            if not isfinite(float(getattr(self, field_name))):
                raise ValueError(f"{field_name} must be finite")
        if self.iterations < 0:
            raise ValueError("iterations cannot be negative")
        object.__setattr__(self, "warnings", tuple(self.warnings))
        object.__setattr__(self, "reference_reading", tuple(self.reference_reading))

    def to_dict(self) -> dict[str, object]:
        return {
            "overall_composition": dict(self.overall_composition),
            "k_values": dict(self.k_values),
            "vapor_fraction": self.vapor_fraction,
            "liquid_composition": dict(self.liquid_composition),
            "vapor_composition": dict(self.vapor_composition),
            "objective_at_zero": self.objective_at_zero,
            "objective_at_one": self.objective_at_one,
            "residual": self.residual,
            "iterations": self.iterations,
            "phase_status": self.phase_status,
            "warnings": list(self.warnings),
            "reference_reading": list(self.reference_reading),
        }


@dataclass(frozen=True)
class VLETemperatureReport:
    solve_mode: VLESolveMode
    pressure_Pa: float
    temperature_K: float
    feed_composition: dict[str, float]
    liquid_composition: dict[str, float]
    vapor_composition: dict[str, float]
    vapor_pressures_Pa: dict[str, float]
    k_values: dict[str, float]
    residual: float
    residual_type: str
    iterations: int
    converged: bool
    bracket_temperature_K: tuple[float, float]
    saturation_reports: dict[str, PureSaturationReport]
    warnings: tuple[str, ...] = ()
    reference_reading: tuple[str, ...] = (
        "reference_repos/thermo/thermo/flash/flash_base.py: ideal bubble/dew "
        "temperature workflow",
        "reference_repos/chemicals/chemicals/rachford_rice.py: phase split "
        "diagnostic conventions",
    )

    def __post_init__(self) -> None:
        if self.solve_mode not in {"bubble_temperature", "dew_temperature"}:
            raise ValueError("Unsupported VLE temperature solve mode")
        if self.pressure_Pa <= 0 or not isfinite(self.pressure_Pa):
            raise ValueError("pressure_Pa must be positive and finite")
        if self.temperature_K <= 0 or not isfinite(self.temperature_K):
            raise ValueError("temperature_K must be positive and finite")
        if not isfinite(self.residual):
            raise ValueError("residual must be finite")
        if self.iterations < 0:
            raise ValueError("iterations cannot be negative")
        lower, upper = self.bracket_temperature_K
        if lower <= 0 or upper <= lower:
            raise ValueError("bracket_temperature_K must be positive and increasing")
        object.__setattr__(self, "warnings", tuple(self.warnings))
        object.__setattr__(self, "reference_reading", tuple(self.reference_reading))

    def to_dict(self) -> dict[str, object]:
        return {
            "solve_mode": self.solve_mode,
            "pressure_Pa": self.pressure_Pa,
            "temperature_K": self.temperature_K,
            "feed_composition": dict(self.feed_composition),
            "liquid_composition": dict(self.liquid_composition),
            "vapor_composition": dict(self.vapor_composition),
            "vapor_pressures_Pa": dict(self.vapor_pressures_Pa),
            "k_values": dict(self.k_values),
            "residual": self.residual,
            "residual_type": self.residual_type,
            "iterations": self.iterations,
            "converged": self.converged,
            "bracket_temperature_K": list(self.bracket_temperature_K),
            "saturation_reports": {
                component_id: report.to_dict()
                for component_id, report in self.saturation_reports.items()
            },
            "warnings": list(self.warnings),
            "reference_reading": list(self.reference_reading),
        }


@dataclass(frozen=True)
class LLEStageResult:
    organic_amounts_mol: dict[str, float]
    aqueous_amounts_mol: dict[str, float]
    recovery_to_organic: dict[str, float]
    phase_volumes_L: dict[str, float]
    material_balance_error_mol: float

    def to_dict(self) -> dict[str, object]:
        return {
            "organic_amounts_mol": dict(self.organic_amounts_mol),
            "aqueous_amounts_mol": dict(self.aqueous_amounts_mol),
            "recovery_to_organic": dict(self.recovery_to_organic),
            "phase_volumes_L": dict(self.phase_volumes_L),
            "material_balance_error_mol": self.material_balance_error_mol,
        }


def activity_coefficients(
    spec: ActivityModelSpec,
    composition: Mapping[str, float],
    *,
    temperature_K: float,
) -> dict[str, float]:
    if temperature_K <= 0:
        raise ValueError("temperature_K must be positive")
    x = _composition_vector(spec.component_ids, composition)
    if spec.model == "ideal":
        return dict.fromkeys(spec.component_ids, 1.0)
    if spec.model == "margules":
        return _margules_gamma(spec, x)
    if spec.model == "wilson":
        return _wilson_gamma(spec, x, temperature_K=temperature_K)
    if spec.model == "nrtl":
        return _nrtl_gamma(spec, x, temperature_K=temperature_K)
    raise ValueError(f"Unsupported activity model: {spec.model}")


def raoult_k_values(
    activity_model: ActivityModelSpec,
    liquid_composition: Mapping[str, float],
    *,
    vapor_pressures_Pa: Mapping[str, float],
    pressure_Pa: float,
    temperature_K: float,
    vapor_fugacity_coefficients: Mapping[str, float] | None = None,
) -> dict[str, float]:
    if pressure_Pa <= 0:
        raise ValueError("pressure_Pa must be positive")
    gamma = activity_coefficients(
        activity_model,
        liquid_composition,
        temperature_K=temperature_K,
    )
    phi = (
        dict.fromkeys(activity_model.component_ids, 1.0)
        if vapor_fugacity_coefficients is None
        else dict(vapor_fugacity_coefficients)
    )
    k_values = {}
    for component_id in activity_model.component_ids:
        psat = float(vapor_pressures_Pa[component_id])
        if psat < 0:
            raise ValueError("vapor pressures cannot be negative")
        phi_i = max(float(phi.get(component_id, 1.0)), 1e-12)
        k_values[component_id] = gamma[component_id] * psat / (phi_i * pressure_Pa)
    return k_values


def rachford_rice_vapor_fraction(
    overall_composition: Mapping[str, float],
    k_values: Mapping[str, float],
    *,
    tolerance: float = 1e-12,
    max_iterations: int = 200,
) -> float:
    z = _normalize_composition(overall_composition)
    _validate_k_values(z, k_values)

    def objective(beta: float) -> float:
        return sum(
            z[component_id]
            * (k_values[component_id] - 1.0)
            / (1.0 + beta * (k_values[component_id] - 1.0))
            for component_id in z
        )

    f0 = objective(0.0)
    f1 = objective(1.0)
    if f0 <= 0.0:
        return 0.0
    if f1 >= 0.0:
        return 1.0

    low = 0.0
    high = 1.0
    for _ in range(max_iterations):
        mid = 0.5 * (low + high)
        value = objective(mid)
        if abs(value) < tolerance:
            return mid
        if value > 0.0:
            low = mid
        else:
            high = mid
    return 0.5 * (low + high)


def rachford_rice_diagnostic_report(
    overall_composition: Mapping[str, float],
    k_values: Mapping[str, float],
    *,
    tolerance: float = 1e-12,
    max_iterations: int = 200,
) -> RachfordRiceDiagnosticReport:
    if tolerance <= 0:
        raise ValueError("tolerance must be positive")
    if max_iterations <= 0:
        raise ValueError("max_iterations must be positive")
    z = _normalize_composition(overall_composition)
    _validate_k_values(z, k_values)
    k = {component_id: float(k_values[component_id]) for component_id in z}

    def objective(beta: float) -> float:
        return sum(
            z[component_id]
            * (k[component_id] - 1.0)
            / (1.0 + beta * (k[component_id] - 1.0))
            for component_id in z
        )

    f0 = objective(0.0)
    f1 = objective(1.0)
    warnings: list[str] = []
    iterations = 0
    if f0 <= 0.0:
        beta = 0.0
        phase_status: FlashPhaseStatus = "all_liquid"
        warnings.append("Rachford-Rice objective indicates a single liquid phase")
    elif f1 >= 0.0:
        beta = 1.0
        phase_status = "all_vapor"
        warnings.append("Rachford-Rice objective indicates a single vapor phase")
    else:
        low = 0.0
        high = 1.0
        beta = 0.5
        phase_status = "two_phase"
        for iteration in range(1, max_iterations + 1):
            beta = 0.5 * (low + high)
            value = objective(beta)
            iterations = iteration
            if abs(value) < tolerance:
                break
            if value > 0.0:
                low = beta
            else:
                high = beta
        else:
            warnings.append(
                "Rachford-Rice bisection reached max_iterations before tolerance"
            )
    liquid = {
        component_id: z[component_id] / (1.0 + beta * (k[component_id] - 1.0))
        for component_id in z
    }
    liquid = _normalize_composition(liquid)
    vapor = {
        component_id: k[component_id] * liquid[component_id]
        for component_id in z
    }
    vapor = _normalize_composition(vapor)
    return RachfordRiceDiagnosticReport(
        overall_composition=z,
        k_values=k,
        vapor_fraction=beta,
        liquid_composition=liquid,
        vapor_composition=vapor,
        objective_at_zero=f0,
        objective_at_one=f1,
        residual=objective(beta),
        iterations=iterations,
        phase_status=phase_status,
        warnings=tuple(warnings),
    )


def flash_isothermal(
    overall_composition: Mapping[str, float],
    k_values: Mapping[str, float],
) -> FlashResult:
    z = _normalize_composition(overall_composition)
    _validate_k_values(z, k_values)
    beta = rachford_rice_vapor_fraction(z, k_values)
    liquid = {
        component_id: z[component_id]
        / (1.0 + beta * (k_values[component_id] - 1.0))
        for component_id in z
    }
    liquid = _normalize_composition(liquid)
    vapor = {
        component_id: k_values[component_id] * liquid[component_id]
        for component_id in z
    }
    vapor = _normalize_composition(vapor)
    return FlashResult(
        vapor_fraction=beta,
        liquid_composition=liquid,
        vapor_composition=vapor,
        k_values={component_id: float(k_values[component_id]) for component_id in z},
    )


def bubble_temperature_report(
    liquid_composition: Mapping[str, float],
    *,
    vapor_pressure_correlations: Mapping[str, PropertyCorrelation],
    activity_model: ActivityModelSpec,
    pressure_Pa: float,
    temperature_bounds_K: tuple[float, float] | None = None,
    validity_policy: ValidityPolicy = "raise",
    tolerance_K: float = 1e-7,
    tolerance_log_pressure: float = 1e-10,
    max_iterations: int = 100,
) -> VLETemperatureReport:
    """Solve a mixture bubble temperature with auditable K-value diagnostics."""

    x = _composition_vector_mapping(activity_model.component_ids, liquid_composition)
    _validate_vle_temperature_inputs(
        pressure_Pa=pressure_Pa,
        tolerance_K=tolerance_K,
        tolerance_log_pressure=tolerance_log_pressure,
        max_iterations=max_iterations,
    )
    _validate_vapor_pressure_correlations(
        activity_model.component_ids,
        vapor_pressure_correlations,
    )
    lower, upper = _mixture_temperature_bounds_k(
        activity_model.component_ids,
        vapor_pressure_correlations,
        temperature_bounds_K=temperature_bounds_K,
    )

    def evaluate(
        temperature_K: float,
    ) -> tuple[float, dict[str, float], dict[str, PureSaturationReport]]:
        vapor_pressures, saturation_reports = _vapor_pressures_from_correlations(
            activity_model.component_ids,
            vapor_pressure_correlations,
            temperature_K=temperature_K,
            validity_policy=validity_policy,
        )
        bubble = bubble_pressure_pa(
            x,
            vapor_pressures_Pa=vapor_pressures,
            activity_model=activity_model,
            temperature_K=temperature_K,
        )
        return log(bubble / pressure_Pa), vapor_pressures, saturation_reports

    solve = _solve_vle_temperature(
        evaluate,
        lower=lower,
        upper=upper,
        tolerance_K=tolerance_K,
        tolerance_log_pressure=tolerance_log_pressure,
        max_iterations=max_iterations,
        residual_label="bubble pressure",
    )
    residual, vapor_pressures, saturation_reports = evaluate(solve.temperature_K)
    k_values = raoult_k_values(
        activity_model,
        x,
        vapor_pressures_Pa=vapor_pressures,
        pressure_Pa=pressure_Pa,
        temperature_K=solve.temperature_K,
    )
    vapor = _normalize_composition(
        {component_id: x[component_id] * k_values[component_id] for component_id in x}
    )
    return VLETemperatureReport(
        solve_mode="bubble_temperature",
        pressure_Pa=pressure_Pa,
        temperature_K=solve.temperature_K,
        feed_composition=x,
        liquid_composition=x,
        vapor_composition=vapor,
        vapor_pressures_Pa=vapor_pressures,
        k_values=k_values,
        residual=residual,
        residual_type="log_bubble_pressure_ratio",
        iterations=solve.iterations,
        converged=solve.converged,
        bracket_temperature_K=(lower, upper),
        saturation_reports=saturation_reports,
        warnings=solve.warnings,
    )


def dew_temperature_report(
    vapor_composition: Mapping[str, float],
    *,
    vapor_pressure_correlations: Mapping[str, PropertyCorrelation],
    activity_model: ActivityModelSpec,
    pressure_Pa: float,
    temperature_bounds_K: tuple[float, float] | None = None,
    validity_policy: ValidityPolicy = "raise",
    tolerance_K: float = 1e-7,
    tolerance_log_pressure: float = 1e-10,
    max_iterations: int = 100,
    composition_iterations: int = 50,
) -> VLETemperatureReport:
    """Solve a mixture dew temperature with liquid-composition diagnostics."""

    y = _composition_vector_mapping(activity_model.component_ids, vapor_composition)
    _validate_vle_temperature_inputs(
        pressure_Pa=pressure_Pa,
        tolerance_K=tolerance_K,
        tolerance_log_pressure=tolerance_log_pressure,
        max_iterations=max_iterations,
    )
    if composition_iterations <= 0:
        raise ValueError("composition_iterations must be positive")
    _validate_vapor_pressure_correlations(
        activity_model.component_ids,
        vapor_pressure_correlations,
    )
    lower, upper = _mixture_temperature_bounds_k(
        activity_model.component_ids,
        vapor_pressure_correlations,
        temperature_bounds_K=temperature_bounds_K,
    )

    def evaluate(
        temperature_K: float,
    ) -> tuple[float, dict[str, float], dict[str, PureSaturationReport]]:
        vapor_pressures, saturation_reports = _vapor_pressures_from_correlations(
            activity_model.component_ids,
            vapor_pressure_correlations,
            temperature_K=temperature_K,
            validity_policy=validity_policy,
        )
        dew_pressure, _liquid = _dew_pressure_and_liquid_composition(
            y,
            vapor_pressures_Pa=vapor_pressures,
            activity_model=activity_model,
            temperature_K=temperature_K,
            iterations=composition_iterations,
        )
        return log(dew_pressure / pressure_Pa), vapor_pressures, saturation_reports

    solve = _solve_vle_temperature(
        evaluate,
        lower=lower,
        upper=upper,
        tolerance_K=tolerance_K,
        tolerance_log_pressure=tolerance_log_pressure,
        max_iterations=max_iterations,
        residual_label="dew pressure",
    )
    residual, vapor_pressures, saturation_reports = evaluate(solve.temperature_K)
    _dew_pressure, liquid = _dew_pressure_and_liquid_composition(
        y,
        vapor_pressures_Pa=vapor_pressures,
        activity_model=activity_model,
        temperature_K=solve.temperature_K,
        iterations=composition_iterations,
    )
    k_values = raoult_k_values(
        activity_model,
        liquid,
        vapor_pressures_Pa=vapor_pressures,
        pressure_Pa=pressure_Pa,
        temperature_K=solve.temperature_K,
    )
    vapor = _normalize_composition(
        {
            component_id: k_values[component_id] * liquid[component_id]
            for component_id in liquid
        }
    )
    return VLETemperatureReport(
        solve_mode="dew_temperature",
        pressure_Pa=pressure_Pa,
        temperature_K=solve.temperature_K,
        feed_composition=y,
        liquid_composition=liquid,
        vapor_composition=vapor,
        vapor_pressures_Pa=vapor_pressures,
        k_values=k_values,
        residual=residual,
        residual_type="log_dew_pressure_ratio",
        iterations=solve.iterations,
        converged=solve.converged,
        bracket_temperature_K=(lower, upper),
        saturation_reports=saturation_reports,
        warnings=solve.warnings,
    )


def bubble_pressure_pa(
    liquid_composition: Mapping[str, float],
    *,
    vapor_pressures_Pa: Mapping[str, float],
    activity_model: ActivityModelSpec,
    temperature_K: float,
) -> float:
    x = _normalize_composition(liquid_composition)
    gamma = activity_coefficients(activity_model, x, temperature_K=temperature_K)
    return sum(
        x[component_id] * gamma[component_id] * float(vapor_pressures_Pa[component_id])
        for component_id in x
    )


def dew_pressure_pa(
    vapor_composition: Mapping[str, float],
    *,
    vapor_pressures_Pa: Mapping[str, float],
    activity_model: ActivityModelSpec,
    temperature_K: float,
    iterations: int = 50,
) -> float:
    pressure, _liquid = _dew_pressure_and_liquid_composition(
        vapor_composition,
        vapor_pressures_Pa=vapor_pressures_Pa,
        activity_model=activity_model,
        temperature_K=temperature_K,
        iterations=iterations,
    )
    return pressure


def liquid_liquid_split(
    feed_amounts_mol: Mapping[str, float],
    *,
    partition_coefficients: Mapping[str, float],
    aqueous_volume_L: float,
    organic_volume_L: float,
    stage_efficiency: float = 1.0,
    entrainment_fraction: float = 0.0,
) -> LLEStageResult:
    if aqueous_volume_L <= 0 or organic_volume_L <= 0:
        raise ValueError("phase volumes must be positive")
    if not 0.0 <= stage_efficiency <= 1.0:
        raise ValueError("stage_efficiency must be between 0 and 1")
    if not 0.0 <= entrainment_fraction < 1.0:
        raise ValueError("entrainment_fraction must be in [0, 1)")
    if any(value < 0 for value in feed_amounts_mol.values()):
        raise ValueError("feed amounts cannot be negative")

    organic = {}
    aqueous = {}
    recovery = {}
    for component_id, amount in feed_amounts_mol.items():
        coefficient = float(partition_coefficients.get(component_id, 1.0))
        if coefficient < 0:
            raise ValueError("partition coefficients cannot be negative")
        ideal_organic = amount * coefficient * organic_volume_L
        ideal_organic /= coefficient * organic_volume_L + aqueous_volume_L
        organic_amount = stage_efficiency * ideal_organic
        aqueous_amount = amount - organic_amount
        entrained = entrainment_fraction * aqueous_amount
        organic_amount += entrained
        aqueous_amount -= entrained
        organic[component_id] = max(organic_amount, 0.0)
        aqueous[component_id] = max(aqueous_amount, 0.0)
        recovery[component_id] = 0.0 if amount <= 0 else organic[component_id] / amount
    balance_error = max(
        (
            abs(feed_amounts_mol[key] - organic.get(key, 0.0) - aqueous.get(key, 0.0))
            for key in feed_amounts_mol
        ),
        default=0.0,
    )
    return LLEStageResult(
        organic_amounts_mol=organic,
        aqueous_amounts_mol=aqueous,
        recovery_to_organic=recovery,
        phase_volumes_L={
            "aqueous": aqueous_volume_L * (1.0 - entrainment_fraction),
            "organic": organic_volume_L + aqueous_volume_L * entrainment_fraction,
        },
        material_balance_error_mol=balance_error,
    )


@dataclass(frozen=True)
class _VLETemperatureSolve:
    temperature_K: float
    residual: float
    iterations: int
    converged: bool
    warnings: tuple[str, ...]


def _solve_vle_temperature(
    evaluator: Callable[
        [float],
        tuple[float, dict[str, float], dict[str, PureSaturationReport]],
    ],
    *,
    lower: float,
    upper: float,
    tolerance_K: float,
    tolerance_log_pressure: float,
    max_iterations: int,
    residual_label: str,
) -> _VLETemperatureSolve:
    f_lower = _evaluate_temperature_residual(evaluator, lower)
    f_upper = _evaluate_temperature_residual(evaluator, upper)
    if abs(f_lower) <= tolerance_log_pressure:
        return _VLETemperatureSolve(lower, f_lower, 0, True, ())
    if abs(f_upper) <= tolerance_log_pressure:
        return _VLETemperatureSolve(upper, f_upper, 0, True, ())
    if f_lower * f_upper > 0.0:
        raise ValueError(
            f"{residual_label} target is outside the temperature bracket: "
            f"residuals=({f_lower:g}, {f_upper:g})"
        )

    left = lower
    right = upper
    f_left = f_lower
    final_temperature = lower
    final_residual = f_lower
    for iteration in range(1, max_iterations + 1):
        mid = 0.5 * (left + right)
        f_mid = _evaluate_temperature_residual(evaluator, mid)
        final_temperature = mid
        final_residual = f_mid
        if abs(f_mid) <= tolerance_log_pressure or (right - left) <= tolerance_K:
            return _VLETemperatureSolve(mid, f_mid, iteration, True, ())
        if f_left * f_mid <= 0.0:
            right = mid
        else:
            left = mid
            f_left = f_mid
    return _VLETemperatureSolve(
        final_temperature,
        final_residual,
        max_iterations,
        False,
        (f"{residual_label} solve reached max_iterations before tolerance",),
    )

def _evaluate_temperature_residual(
    evaluator: Callable[
        [float],
        tuple[float, dict[str, float], dict[str, PureSaturationReport]],
    ],
    temperature_K: float,
) -> float:
    residual, _vapor_pressures, _reports = evaluator(temperature_K)
    if not isfinite(residual):
        raise ValueError("VLE temperature residual must be finite")
    return float(residual)


def _validate_vle_temperature_inputs(
    *,
    pressure_Pa: float,
    tolerance_K: float,
    tolerance_log_pressure: float,
    max_iterations: int,
) -> None:
    if pressure_Pa <= 0 or not isfinite(pressure_Pa):
        raise ValueError("pressure_Pa must be positive and finite")
    if tolerance_K <= 0 or tolerance_log_pressure <= 0:
        raise ValueError("VLE temperature tolerances must be positive")
    if max_iterations <= 0:
        raise ValueError("max_iterations must be positive")


def _validate_vapor_pressure_correlations(
    component_ids: tuple[str, ...],
    correlations: Mapping[str, PropertyCorrelation],
) -> None:
    missing = sorted(set(component_ids) - set(correlations))
    extra = sorted(set(correlations) - set(component_ids))
    if missing or extra:
        raise ValueError(
            "vapor pressure correlation keys must match components: "
            f"missing={missing}, extra={extra}"
        )
    for component_id in component_ids:
        correlation = correlations[component_id]
        if correlation.property_id not in {"vapor_pressure", "sublimation_pressure"}:
            raise ValueError(
                f"correlation for {component_id!r} must be a vapor pressure "
                "or sublimation pressure correlation"
            )


def _mixture_temperature_bounds_k(
    component_ids: tuple[str, ...],
    correlations: Mapping[str, PropertyCorrelation],
    *,
    temperature_bounds_K: tuple[float, float] | None,
) -> tuple[float, float]:
    if temperature_bounds_K is not None:
        lower, upper = temperature_bounds_K
        if lower <= 0 or upper <= lower:
            raise ValueError("temperature_bounds_K must be positive and increasing")
        return float(lower), float(upper)
    lower_candidates: list[float] = []
    upper_candidates: list[float] = []
    for component_id in component_ids:
        correlation = correlations[component_id]
        bounds = correlation.validity_ranges.get("temperature")
        if bounds is None:
            lower_candidates.append(200.0)
            upper_candidates.append(650.0)
            continue
        source_unit = correlation.input_units["temperature"]
        lower_candidates.append(convert_value(bounds[0], source_unit, "K"))
        upper_candidates.append(convert_value(bounds[1], source_unit, "K"))
    lower = max(lower_candidates)
    upper = min(upper_candidates)
    if lower >= upper:
        raise ValueError(
            "vapor-pressure correlations do not have an overlapping temperature range"
        )
    return lower, upper


def _vapor_pressures_from_correlations(
    component_ids: tuple[str, ...],
    correlations: Mapping[str, PropertyCorrelation],
    *,
    temperature_K: float,
    validity_policy: ValidityPolicy,
) -> tuple[dict[str, float], dict[str, PureSaturationReport]]:
    vapor_pressures: dict[str, float] = {}
    reports: dict[str, PureSaturationReport] = {}
    for component_id in component_ids:
        report = pure_saturation_pressure_report(
            correlations[component_id],
            temperature_K=temperature_K,
            validity_policy=validity_policy,
        )
        vapor_pressures[component_id] = report.saturation_pressure_Pa
        reports[component_id] = report
    return vapor_pressures, reports


def _dew_pressure_and_liquid_composition(
    vapor_composition: Mapping[str, float],
    *,
    vapor_pressures_Pa: Mapping[str, float],
    activity_model: ActivityModelSpec,
    temperature_K: float,
    iterations: int,
) -> tuple[float, dict[str, float]]:
    if iterations <= 0:
        raise ValueError("iterations must be positive")
    y = _composition_vector_mapping(activity_model.component_ids, vapor_composition)
    _validate_vapor_pressure_values(y, vapor_pressures_Pa)
    pressure = 1.0 / sum(y[key] / float(vapor_pressures_Pa[key]) for key in y)
    liquid = dict(y)
    for _ in range(iterations):
        gamma = activity_coefficients(activity_model, liquid, temperature_K=temperature_K)
        denominator = sum(
            y[key] / (gamma[key] * float(vapor_pressures_Pa[key]))
            for key in y
        )
        if denominator <= 0.0 or not isfinite(denominator):
            raise ValueError("dew pressure denominator must be positive and finite")
        pressure = 1.0 / denominator
        liquid = _normalize_composition(
            {
                key: y[key]
                * pressure
                / (gamma[key] * float(vapor_pressures_Pa[key]))
                for key in y
            }
        )
    return pressure, liquid


def _validate_vapor_pressure_values(
    composition: Mapping[str, float],
    vapor_pressures_Pa: Mapping[str, float],
) -> None:
    missing = sorted(set(composition) - set(vapor_pressures_Pa))
    extra = sorted(set(vapor_pressures_Pa) - set(composition))
    if missing or extra:
        raise ValueError(
            "vapor pressure keys must match composition: "
            f"missing={missing}, extra={extra}"
        )
    if any(
        value <= 0 or not isfinite(float(value))
        for value in vapor_pressures_Pa.values()
    ):
        raise ValueError("vapor pressures must be finite and positive")


def _margules_gamma(spec: ActivityModelSpec, x: tuple[float, ...]) -> dict[str, float]:
    gamma = {}
    for i, component_id in enumerate(spec.component_ids):
        ln_gamma = 0.0
        for j, other_id in enumerate(spec.component_ids):
            if i == j:
                continue
            ln_gamma += _pair_parameter(spec, component_id, other_id, prefix="A") * x[j] ** 2
        gamma[component_id] = exp(ln_gamma)
    return gamma


def _wilson_gamma(
    spec: ActivityModelSpec,
    x: tuple[float, ...],
    *,
    temperature_K: float,
) -> dict[str, float]:
    lambdas = _wilson_lambda_matrix(spec, temperature_K)
    n = len(spec.component_ids)
    sums = []
    for i in range(n):
        total = sum(x[j] * lambdas[i][j] for j in range(n))
        if total <= 0.0 or not isfinite(total):
            raise ValueError("Wilson lambda composition sum must be positive")
        sums.append(total)

    gamma = {}
    for i, component_id in enumerate(spec.component_ids):
        log_gamma = 1.0 - log(sums[i])
        log_gamma -= sum(x[j] * lambdas[j][i] / sums[j] for j in range(n))
        gamma[component_id] = exp(log_gamma)
    return gamma


def _nrtl_gamma(
    spec: ActivityModelSpec,
    x: tuple[float, ...],
    *,
    temperature_K: float,
) -> dict[str, float]:
    n = len(spec.component_ids)
    tau = [[0.0 for _ in range(n)] for _ in range(n)]
    g = [[1.0 for _ in range(n)] for _ in range(n)]
    for i, left in enumerate(spec.component_ids):
        for j, right in enumerate(spec.component_ids):
            if i == j:
                continue
            tau[i][j] = _nrtl_tau(spec, left, right, temperature_K)
            alpha = _nrtl_alpha(spec, left, right, temperature_K)
            if alpha <= 0.0:
                raise ValueError("NRTL alpha values must be positive")
            g[i][j] = exp(-alpha * tau[i][j])

    gamma = {}
    for i, component_id in enumerate(spec.component_ids):
        denominator_i = sum(x[k] * g[k][i] for k in range(n))
        if denominator_i <= 0.0 or not isfinite(denominator_i):
            raise ValueError("NRTL denominator must be positive")
        first = sum(x[j] * tau[j][i] * g[j][i] for j in range(n)) / denominator_i
        second = 0.0
        for j in range(n):
            denominator = sum(x[k] * g[k][j] for k in range(n))
            weighted_tau = sum(x[m] * tau[m][j] * g[m][j] for m in range(n))
            if denominator <= 0.0 or not isfinite(denominator):
                raise ValueError("NRTL denominator must be positive")
            second += (
                x[j]
                * g[i][j]
                / denominator
                * (tau[i][j] - weighted_tau / denominator)
            )
        gamma[component_id] = exp(first + second)
    return gamma


def _wilson_lambda_matrix(
    spec: ActivityModelSpec,
    temperature_K: float,
) -> list[list[float]]:
    component_ids = spec.component_ids
    n = len(component_ids)
    matrix = [[1.0 for _ in range(n)] for _ in range(n)]
    for i, left in enumerate(component_ids):
        for j, right in enumerate(component_ids):
            if i == j:
                continue
            value = _wilson_lambda(spec, left, right, temperature_K)
            if value <= 0.0 or not isfinite(value):
                raise ValueError("Wilson Lambda values must be finite and positive")
            matrix[i][j] = value
    return matrix


def _wilson_lambda(
    spec: ActivityModelSpec,
    left: str,
    right: str,
    temperature_K: float,
) -> float:
    direct = _directional_parameter(spec, "lambda", left, right, default=None)
    if direct is not None:
        return direct
    exponent = (
        _directional_value(spec, "lambda_a", left, right, default=0.0)
        + _directional_value(spec, "lambda_b", left, right, default=0.0)
        / temperature_K
        + _directional_value(spec, "lambda_c", left, right, default=0.0)
        * log(temperature_K)
        + _directional_value(spec, "lambda_d", left, right, default=0.0)
        * temperature_K
        + _directional_value(spec, "lambda_e", left, right, default=0.0)
        / temperature_K**2
        + _directional_value(spec, "lambda_f", left, right, default=0.0)
        * temperature_K**2
    )
    return exp(exponent)


def _nrtl_tau(
    spec: ActivityModelSpec,
    left: str,
    right: str,
    temperature_K: float,
) -> float:
    direct = _directional_parameter(spec, "tau", left, right, default=None)
    if direct is not None:
        return direct
    return (
        _directional_value(spec, "tau_a", left, right, default=0.0)
        + _directional_value(spec, "tau_b", left, right, default=0.0)
        / temperature_K
        + _directional_value(spec, "tau_e", left, right, default=0.0)
        * log(temperature_K)
        + _directional_value(spec, "tau_f", left, right, default=0.0)
        * temperature_K
        + _directional_value(spec, "tau_g", left, right, default=0.0)
        / temperature_K**2
        + _directional_value(spec, "tau_h", left, right, default=0.0)
        * temperature_K**2
    )


def _nrtl_alpha(
    spec: ActivityModelSpec,
    left: str,
    right: str,
    temperature_K: float,
) -> float:
    direct = _directional_parameter(spec, "alpha", left, right, default=None)
    if direct is not None:
        return direct
    return (
        _directional_value(spec, "alpha_c", left, right, default=0.0)
        + _directional_value(spec, "alpha_d", left, right, default=0.0)
        * temperature_K
    )


def _validate_activity_parameter_contract(spec: ActivityModelSpec) -> None:
    if spec.model in {"ideal", "margules"}:
        return
    for left in spec.component_ids:
        for right in spec.component_ids:
            if left == right:
                continue
            if spec.model == "wilson":
                _validate_pair_has_any(
                    spec,
                    left,
                    right,
                    (
                        "lambda",
                        "lambda_a",
                        "lambda_b",
                        "lambda_c",
                        "lambda_d",
                        "lambda_e",
                        "lambda_f",
                    ),
                )
                direct = _directional_parameter(spec, "lambda", left, right, default=None)
                if direct is not None and direct <= 0.0:
                    raise ValueError("Wilson Lambda values must be positive")
            if spec.model == "nrtl":
                _validate_pair_has_any(
                    spec,
                    left,
                    right,
                    ("tau", "tau_a", "tau_b", "tau_e", "tau_f", "tau_g", "tau_h"),
                )
                _validate_pair_has_any(
                    spec,
                    left,
                    right,
                    ("alpha", "alpha_c", "alpha_d"),
                )
                direct_alpha = _directional_parameter(
                    spec,
                    "alpha",
                    left,
                    right,
                    default=None,
                )
                if direct_alpha is not None and direct_alpha <= 0.0:
                    raise ValueError("NRTL alpha values must be positive")


def _validate_pair_has_any(
    spec: ActivityModelSpec,
    left: str,
    right: str,
    prefixes: tuple[str, ...],
) -> None:
    if not any(_has_directional_parameter(spec, prefix, left, right) for prefix in prefixes):
        allowed = ", ".join(prefixes)
        raise ValueError(
            f"{spec.model} requires one of {{{allowed}}} for pair {left}|{right}"
        )


def _has_directional_parameter(
    spec: ActivityModelSpec,
    prefix: str,
    left: str,
    right: str,
) -> bool:
    return f"{prefix}:{left}|{right}" in spec.parameters


def _directional_parameter(
    spec: ActivityModelSpec,
    prefix: str,
    left: str,
    right: str,
    *,
    default: float | None,
) -> float | None:
    key = f"{prefix}:{left}|{right}"
    if key not in spec.parameters:
        return default
    return float(spec.parameters[key])


def _directional_value(
    spec: ActivityModelSpec,
    prefix: str,
    left: str,
    right: str,
    *,
    default: float,
) -> float:
    value = _directional_parameter(spec, prefix, left, right, default=None)
    return default if value is None else value


def _pair_parameter(
    spec: ActivityModelSpec,
    left: str,
    right: str,
    *,
    prefix: str,
    default: float = 0.0,
) -> float:
    return float(
        spec.parameters.get(
            f"{prefix}:{left}|{right}",
            spec.parameters.get(f"{prefix}:{right}|{left}", default),
        )
    )


def _composition_vector(
    component_ids: tuple[str, ...],
    composition: Mapping[str, float],
) -> tuple[float, ...]:
    return tuple(
        _composition_vector_mapping(component_ids, composition)[component_id]
        for component_id in component_ids
    )


def _composition_vector_mapping(
    component_ids: tuple[str, ...],
    composition: Mapping[str, float],
) -> dict[str, float]:
    normalized = _normalize_composition(composition)
    missing = sorted(set(component_ids) - set(normalized))
    extra = sorted(set(normalized) - set(component_ids))
    if missing or extra:
        raise ValueError(f"Composition ids do not match model: missing={missing}, extra={extra}")
    return {component_id: normalized[component_id] for component_id in component_ids}


def _normalize_composition(composition: Mapping[str, float]) -> dict[str, float]:
    if not composition:
        raise ValueError("composition cannot be empty")
    if any(value < 0 or not isfinite(value) for value in composition.values()):
        raise ValueError("composition values must be finite and nonnegative")
    total = sum(composition.values())
    if total <= 0:
        raise ValueError("composition must contain positive material")
    return {component_id: float(value) / total for component_id, value in composition.items()}


def _validate_k_values(
    composition: Mapping[str, float],
    k_values: Mapping[str, float],
) -> None:
    missing = sorted(set(composition) - set(k_values))
    extra = sorted(set(k_values) - set(composition))
    if missing or extra:
        raise ValueError(f"K-value ids do not match composition: missing={missing}, extra={extra}")
    if any(value <= 0 or not isfinite(value) for value in k_values.values()):
        raise ValueError("K-values must be finite and positive")


__all__ = [
    "ActivityModel",
    "ActivityModelSpec",
    "FlashPhaseStatus",
    "FlashResult",
    "LLEStageResult",
    "RachfordRiceDiagnosticReport",
    "VLESolveMode",
    "VLETemperatureReport",
    "activity_coefficients",
    "activity_model_cards",
    "bubble_pressure_pa",
    "bubble_temperature_report",
    "dew_pressure_pa",
    "dew_temperature_report",
    "flash_isothermal",
    "liquid_liquid_split",
    "rachford_rice_diagnostic_report",
    "rachford_rice_vapor_fraction",
    "raoult_k_values",
]
