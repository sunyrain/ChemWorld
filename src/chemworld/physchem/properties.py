"""Property-correlation evaluators for the ChemWorld physchem core."""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, isfinite, log
from typing import Literal

from chemworld.foundation.units import Quantity, convert_value
from chemworld.physchem.specs import ComponentSpec, MixtureSpec, PropertyCorrelation

R_J_PER_MOL_K = 8.31446261815324
STANDARD_PRESSURE_PA = 101325.0

ValidityPolicy = Literal["warn", "raise", "ignore"]


@dataclass(frozen=True)
class PropertyEvaluation:
    property_id: str
    correlation_id: str
    equation_id: str
    value: float
    unit: str
    inputs: dict[str, float]
    warnings: tuple[str, ...] = ()

    @property
    def valid(self) -> bool:
        return not self.warnings

    def quantity(self) -> Quantity:
        return Quantity(self.value, self.unit)

    def to(self, target_unit: str) -> PropertyEvaluation:
        return PropertyEvaluation(
            property_id=self.property_id,
            correlation_id=self.correlation_id,
            equation_id=self.equation_id,
            value=convert_value(self.value, self.unit, target_unit),
            unit=target_unit,
            inputs=dict(self.inputs),
            warnings=self.warnings,
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "property_id": self.property_id,
            "correlation_id": self.correlation_id,
            "equation_id": self.equation_id,
            "value": self.value,
            "unit": self.unit,
            "inputs": dict(self.inputs),
            "warnings": list(self.warnings),
            "valid": self.valid,
        }


@dataclass(frozen=True)
class ComponentPropertyPackage:
    component: ComponentSpec
    correlations: tuple[PropertyCorrelation, ...]

    def __post_init__(self) -> None:
        ids = [correlation.correlation_id for correlation in self.correlations]
        if len(ids) != len(set(ids)):
            raise ValueError("Duplicate correlation_id values are not allowed")

    def by_property(self, property_id: str) -> tuple[PropertyCorrelation, ...]:
        return tuple(
            correlation
            for correlation in self.correlations
            if correlation.property_id == property_id
        )

    def evaluate(
        self,
        property_id: str,
        *,
        temperature_K: float,
        pressure_Pa: float | None = None,
        validity_policy: ValidityPolicy = "warn",
    ) -> PropertyEvaluation:
        candidates = self.by_property(property_id)
        if not candidates:
            raise ValueError(
                f"No correlation for property {property_id!r} on component "
                f"{self.component.identifier!r}"
            )
        chosen = _choose_valid_correlation(
            candidates,
            temperature_K=temperature_K,
            pressure_Pa=pressure_Pa,
        )
        return evaluate_correlation(
            chosen,
            temperature_K=temperature_K,
            pressure_Pa=pressure_Pa,
            molecular_weight_g_mol=self.component.molecular_weight_g_mol,
            validity_policy=validity_policy,
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "component": self.component.to_dict(),
            "correlations": [correlation.to_dict() for correlation in self.correlations],
        }


def evaluate_correlation(
    correlation: PropertyCorrelation,
    *,
    temperature_K: float,
    pressure_Pa: float | None = None,
    molecular_weight_g_mol: float | None = None,
    validity_policy: ValidityPolicy = "warn",
) -> PropertyEvaluation:
    """Evaluate a supported property correlation.

    Inputs are supplied in canonical benchmark units. Each correlation declares
    the units its coefficients expect; this function performs the conversion.
    """

    if temperature_K <= 0:
        raise ValueError("temperature_K must be positive")
    if pressure_Pa is not None and pressure_Pa <= 0:
        raise ValueError("pressure_Pa must be positive")

    inputs = {"temperature": _convert_input(temperature_K, "K", correlation, "temperature")}
    if pressure_Pa is not None:
        inputs["pressure"] = _convert_input(pressure_Pa, "Pa", correlation, "pressure")
    warnings = _validity_warnings(correlation, inputs)
    if warnings and validity_policy == "raise":
        raise ValueError("; ".join(warnings))

    value = _evaluate_equation(
        correlation,
        inputs=inputs,
        temperature_K=temperature_K,
        pressure_Pa=pressure_Pa,
        molecular_weight_g_mol=molecular_weight_g_mol,
    )
    _ensure_finite_positive(value, correlation)
    return PropertyEvaluation(
        property_id=correlation.property_id,
        correlation_id=correlation.correlation_id,
        equation_id=correlation.equation_id,
        value=value,
        unit=correlation.output_unit,
        inputs=inputs,
        warnings=() if validity_policy == "ignore" else warnings,
    )


def sensible_enthalpy_change(
    heat_capacity_correlation: PropertyCorrelation,
    *,
    initial_temperature_K: float,
    final_temperature_K: float,
    validity_policy: ValidityPolicy = "warn",
) -> PropertyEvaluation:
    """Integrate a supported molar heat-capacity correlation in J/mol."""

    if heat_capacity_correlation.equation_id != "cp_polynomial":
        raise ValueError("Only cp_polynomial supports analytic enthalpy integration")
    T0 = _convert_input(initial_temperature_K, "K", heat_capacity_correlation, "temperature")
    T1 = _convert_input(final_temperature_K, "K", heat_capacity_correlation, "temperature")
    warnings = _validity_warnings(heat_capacity_correlation, {"temperature": T0})
    warnings += _validity_warnings(heat_capacity_correlation, {"temperature": T1})
    if warnings and validity_policy == "raise":
        raise ValueError("; ".join(warnings))
    coeffs = heat_capacity_correlation.coefficients
    value = _cp_polynomial_integral(T1, coeffs) - _cp_polynomial_integral(T0, coeffs)
    return PropertyEvaluation(
        property_id="sensible_enthalpy",
        correlation_id=heat_capacity_correlation.correlation_id,
        equation_id="cp_polynomial_integral",
        value=value,
        unit="J/mol",
        inputs={
            "initial_temperature": T0,
            "final_temperature": T1,
        },
        warnings=() if validity_policy == "ignore" else warnings,
    )


def mixture_density(
    mixture: MixtureSpec,
    component_densities_kg_m3: tuple[float, ...],
) -> PropertyEvaluation:
    """Ideal liquid-mixture density from mass-fraction specific volumes."""

    if len(component_densities_kg_m3) != len(mixture.component_ids):
        raise ValueError("Density vector must match mixture components")
    if any(rho <= 0 for rho in component_densities_kg_m3):
        raise ValueError("Component densities must be positive")
    specific_volume = sum(
        w / rho
        for w, rho in zip(
            mixture.mass_fractions,
            component_densities_kg_m3,
            strict=True,
        )
    )
    return PropertyEvaluation(
        property_id="mixture_density",
        correlation_id="ideal_specific_volume_mixing",
        equation_id="ideal_specific_volume_mixing",
        value=1.0 / specific_volume,
        unit="kg/m^3",
        inputs={"temperature": mixture.temperature_K, "pressure": mixture.pressure_Pa},
    )


def mixture_viscosity_log_rule(
    mixture: MixtureSpec,
    component_viscosities_Pa_s: tuple[float, ...],
) -> PropertyEvaluation:
    """Logarithmic liquid-mixture viscosity rule."""

    if len(component_viscosities_Pa_s) != len(mixture.component_ids):
        raise ValueError("Viscosity vector must match mixture components")
    if any(mu <= 0 for mu in component_viscosities_Pa_s):
        raise ValueError("Component viscosities must be positive")
    log_mu = sum(
        z * log(mu)
        for z, mu in zip(
            mixture.mole_fractions,
            component_viscosities_Pa_s,
            strict=True,
        )
    )
    return PropertyEvaluation(
        property_id="mixture_viscosity",
        correlation_id="log_mole_fraction_mixing",
        equation_id="log_mole_fraction_mixing",
        value=exp(log_mu),
        unit="Pa*s",
        inputs={"temperature": mixture.temperature_K, "pressure": mixture.pressure_Pa},
    )


def volatility_risk_from_psat(
    vapor_pressure: PropertyEvaluation,
    *,
    ambient_pressure_Pa: float = STANDARD_PRESSURE_PA,
    low_ratio: float = 0.05,
    high_ratio: float = 1.0,
) -> PropertyEvaluation:
    psat_Pa = vapor_pressure.to("Pa").value
    if ambient_pressure_Pa <= 0:
        raise ValueError("ambient_pressure_Pa must be positive")
    ratio = psat_Pa / ambient_pressure_Pa
    risk = _clamp((ratio - low_ratio) / (high_ratio - low_ratio), 0.0, 1.0)
    return PropertyEvaluation(
        property_id="volatility_risk",
        correlation_id=f"{vapor_pressure.correlation_id}:volatility_risk",
        equation_id="volatility_risk_proxy",
        value=risk,
        unit="dimensionless",
        inputs={"vapor_pressure_Pa": psat_Pa, "ambient_pressure_Pa": ambient_pressure_Pa},
    )


def thermal_hazard_proxy(
    *,
    temperature_K: float,
    onset_temperature_K: float,
    severe_temperature_K: float,
) -> PropertyEvaluation:
    if onset_temperature_K >= severe_temperature_K:
        raise ValueError("onset_temperature_K must be below severe_temperature_K")
    risk = _clamp(
        (temperature_K - onset_temperature_K)
        / (severe_temperature_K - onset_temperature_K),
        0.0,
        1.0,
    )
    return PropertyEvaluation(
        property_id="thermal_hazard",
        correlation_id="thermal_hazard_proxy",
        equation_id="linear_thermal_hazard_proxy",
        value=risk,
        unit="dimensionless",
        inputs={
            "temperature_K": temperature_K,
            "onset_temperature_K": onset_temperature_K,
            "severe_temperature_K": severe_temperature_K,
        },
    )


def _evaluate_equation(
    correlation: PropertyCorrelation,
    *,
    inputs: dict[str, float],
    temperature_K: float,
    pressure_Pa: float | None,
    molecular_weight_g_mol: float | None,
) -> float:
    equation = correlation.equation_id
    coeffs = correlation.coefficients
    T = inputs["temperature"]
    if equation == "antoine":
        base = coeffs.get("base", 10.0)
        return base ** (coeffs["A"] - coeffs["B"] / (T + coeffs["C"]))
    if equation == "wagner":
        Tc = coeffs["Tc"]
        Pc = coeffs["Pc"]
        if temperature_K >= Tc:
            raise ValueError("Wagner vapor pressure requires T < Tc")
        tau = 1.0 - temperature_K / Tc
        exponent = (
            coeffs["a"] * tau
            + coeffs["b"] * tau**1.5
            + coeffs["c"] * tau**3.0
            + coeffs["d"] * tau**6.0
        ) / (1.0 - tau)
        return Pc * exp(exponent)
    if equation == "cp_polynomial":
        return _cp_polynomial(T, coeffs)
    if equation == "watson_hvap":
        Tc = coeffs["Tc"]
        T_ref = coeffs["T_ref"]
        if temperature_K >= Tc:
            return 0.0
        ratio = (1.0 - temperature_K / Tc) / (1.0 - T_ref / Tc)
        return coeffs["Hvap_ref"] * ratio ** coeffs.get("exponent", 0.38)
    if equation == "linear_liquid_density":
        rho = coeffs["rho_ref"] * (1.0 - coeffs.get("alpha", 0.0) * (T - coeffs["T_ref"]))
        return rho
    if equation == "ideal_gas_density":
        if molecular_weight_g_mol is None:
            raise ValueError("ideal_gas_density requires molecular_weight_g_mol")
        pressure = pressure_Pa if pressure_Pa is not None else STANDARD_PRESSURE_PA
        mw_kg_mol = molecular_weight_g_mol / 1000.0
        return pressure * mw_kg_mol / (R_J_PER_MOL_K * temperature_K)
    if equation == "andrade_viscosity":
        return coeffs["A"] * exp(coeffs["B"] / T)
    if equation == "surface_tension_power":
        Tc = coeffs["Tc"]
        T_ref = coeffs["T_ref"]
        if temperature_K >= Tc:
            return 0.0
        ratio = (1.0 - temperature_K / Tc) / (1.0 - T_ref / Tc)
        return coeffs["sigma_ref"] * ratio ** coeffs.get("exponent", 1.26)
    raise ValueError(f"Unsupported property equation_id: {equation}")


def _cp_polynomial(T: float, coeffs: dict[str, float]) -> float:
    return (
        coeffs.get("a", 0.0)
        + coeffs.get("b", 0.0) * T
        + coeffs.get("c", 0.0) * T**2
        + coeffs.get("d", 0.0) * T**3
        + coeffs.get("e", 0.0) * T**4
    )


def _cp_polynomial_integral(T: float, coeffs: dict[str, float]) -> float:
    return (
        coeffs.get("a", 0.0) * T
        + 0.5 * coeffs.get("b", 0.0) * T**2
        + (1.0 / 3.0) * coeffs.get("c", 0.0) * T**3
        + 0.25 * coeffs.get("d", 0.0) * T**4
        + 0.2 * coeffs.get("e", 0.0) * T**5
    )


def _convert_input(
    value: float,
    source_unit: str,
    correlation: PropertyCorrelation,
    field_name: str,
) -> float:
    target_unit = correlation.input_units.get(field_name, source_unit)
    return convert_value(value, source_unit, target_unit)


def _validity_warnings(
    correlation: PropertyCorrelation,
    inputs: dict[str, float],
) -> tuple[str, ...]:
    warnings = []
    for field_name, value in inputs.items():
        bounds = correlation.validity_ranges.get(field_name)
        if bounds is None:
            continue
        lower, upper = bounds
        if value < lower or value > upper:
            warnings.append(
                f"{field_name}={value:g} outside validity range "
                f"[{lower:g}, {upper:g}] for {correlation.correlation_id}"
            )
    return tuple(warnings)


def _choose_valid_correlation(
    correlations: tuple[PropertyCorrelation, ...],
    *,
    temperature_K: float,
    pressure_Pa: float | None,
) -> PropertyCorrelation:
    for correlation in correlations:
        inputs = {"temperature": _convert_input(temperature_K, "K", correlation, "temperature")}
        if pressure_Pa is not None:
            inputs["pressure"] = _convert_input(pressure_Pa, "Pa", correlation, "pressure")
        if not _validity_warnings(correlation, inputs):
            return correlation
    return correlations[0]


def _ensure_finite_positive(value: float, correlation: PropertyCorrelation) -> None:
    if not isfinite(value):
        raise ValueError(f"Correlation returned non-finite value: {correlation.correlation_id}")
    if correlation.property_id in {
        "vapor_pressure",
        "heat_capacity",
        "heat_of_vaporization",
        "liquid_density",
        "gas_density",
        "liquid_viscosity",
        "surface_tension",
    } and value < 0:
        raise ValueError(f"Correlation returned negative value: {correlation.correlation_id}")


def _clamp(value: float, lower: float, upper: float) -> float:
    return min(max(value, lower), upper)
