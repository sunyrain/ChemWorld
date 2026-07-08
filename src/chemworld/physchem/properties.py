"""Property-correlation evaluators for the ChemWorld physchem core."""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, isfinite, log
from typing import Literal

from chemworld.foundation.units import Quantity, convert_value
from chemworld.physchem.maturity import MaturityLevel, ModelCard, ValidationEvidence
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
class VaporPressureReport:
    """Vapor/sublimation pressure with derivative and method provenance."""

    pressure: PropertyEvaluation
    temperature_derivative_value: float
    temperature_derivative_unit: str
    dln_pressure_dT_1_K: float
    method_family: str
    validity_status: str
    reference_reading: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.pressure.property_id not in {"vapor_pressure", "sublimation_pressure"}:
            raise ValueError("VaporPressureReport requires vapor or sublimation pressure")
        if not isfinite(self.temperature_derivative_value):
            raise ValueError("temperature derivative must be finite")
        if self.pressure.value <= 0:
            raise ValueError("pressure value must be positive")
        if not isfinite(self.dln_pressure_dT_1_K):
            raise ValueError("log-pressure derivative must be finite")
        if self.validity_status not in {"valid", "out_of_range"}:
            raise ValueError("validity_status must be valid or out_of_range")
        object.__setattr__(self, "reference_reading", tuple(self.reference_reading))

    @property
    def pressure_pa(self) -> float:
        return self.pressure.to("Pa").value

    @property
    def dp_dt_pa_per_k(self) -> float:
        return self.temperature_derivative_value * _pressure_unit_to_pa_factor(
            self.pressure.unit
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "pressure": self.pressure.to_dict(),
            "temperature_derivative_value": self.temperature_derivative_value,
            "temperature_derivative_unit": self.temperature_derivative_unit,
            "dP_dT_Pa_per_K": self.dp_dt_pa_per_k,
            "dln_pressure_dT_1_K": self.dln_pressure_dT_1_K,
            "method_family": self.method_family,
            "validity_status": self.validity_status,
            "reference_reading": list(self.reference_reading),
        }


@dataclass(frozen=True)
class ComponentPropertyPackage:
    component: ComponentSpec
    correlations: tuple[PropertyCorrelation, ...]

    def __post_init__(self) -> None:
        ids = [correlation.correlation_id for correlation in self.correlations]
        if len(ids) != len(set(ids)):
            raise ValueError("Duplicate correlation_id values are not allowed")
        allowed = set(self.component.allowed_property_correlations)
        if allowed:
            disallowed = [
                correlation.correlation_id
                for correlation in self.correlations
                if correlation.correlation_id not in allowed
                and correlation.property_id not in allowed
                and correlation.equation_id not in allowed
            ]
            if disallowed:
                raise ValueError(
                    "Correlations are not allowed by component policy: "
                    f"{disallowed}"
                )

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

    def vapor_pressure_report(
        self,
        *,
        temperature_K: float,
        property_id: str = "vapor_pressure",
        validity_policy: ValidityPolicy = "warn",
    ) -> VaporPressureReport:
        candidates = self.by_property(property_id)
        if not candidates:
            raise ValueError(
                f"No correlation for property {property_id!r} on component "
                f"{self.component.identifier!r}"
            )
        chosen = _choose_valid_correlation(
            candidates,
            temperature_K=temperature_K,
            pressure_Pa=None,
        )
        return vapor_pressure_report(
            chosen,
            temperature_K=temperature_K,
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


def vapor_pressure_report(
    correlation: PropertyCorrelation,
    *,
    temperature_K: float,
    validity_policy: ValidityPolicy = "warn",
) -> VaporPressureReport:
    """Evaluate pressure and analytic temperature derivative for vapor models."""

    if correlation.property_id not in {"vapor_pressure", "sublimation_pressure"}:
        raise ValueError("vapor_pressure_report requires vapor or sublimation pressure")
    pressure = evaluate_correlation(
        correlation,
        temperature_K=temperature_K,
        validity_policy=validity_policy,
    )
    derivative = vapor_pressure_temperature_derivative(
        correlation,
        temperature_K=temperature_K,
        validity_policy=validity_policy,
    )
    pressure_value = pressure.value
    dln = derivative.value / pressure_value
    return VaporPressureReport(
        pressure=pressure,
        temperature_derivative_value=derivative.value,
        temperature_derivative_unit=derivative.unit,
        dln_pressure_dT_1_K=dln,
        method_family=_vapor_pressure_method_family(correlation.equation_id),
        validity_status="valid" if not pressure.warnings else "out_of_range",
        reference_reading=(
            "reference_repos/chemicals/chemicals/vapor_pressure.py: "
            "Antoine, Wagner, dWagner_dT",
            "reference_repos/chemicals/chemicals/dippr.py: EQ101 order=1 "
            "derivative",
            "reference_repos/thermo/thermo/vapor_pressure.py: "
            "VaporPressure ranked methods and validity limits",
        ),
    )


def vapor_pressure_temperature_derivative(
    correlation: PropertyCorrelation,
    *,
    temperature_K: float,
    validity_policy: ValidityPolicy = "warn",
) -> PropertyEvaluation:
    """Analytic `dP_sat/dT` in the correlation output unit per kelvin."""

    if correlation.property_id not in {"vapor_pressure", "sublimation_pressure"}:
        raise ValueError(
            "vapor_pressure_temperature_derivative requires vapor or "
            "sublimation pressure"
        )
    pressure = evaluate_correlation(
        correlation,
        temperature_K=temperature_K,
        validity_policy=validity_policy,
    )
    inputs = {
        "temperature": _convert_input(temperature_K, "K", correlation, "temperature")
    }
    derivative = _evaluate_temperature_derivative(
        correlation,
        inputs=inputs,
        pressure_value=pressure.value,
    )
    if not isfinite(derivative):
        raise ValueError(
            f"Correlation derivative returned non-finite value: "
            f"{correlation.correlation_id}"
        )
    return PropertyEvaluation(
        property_id=f"{correlation.property_id}_temperature_derivative",
        correlation_id=f"{correlation.correlation_id}:dP_dT",
        equation_id=f"{correlation.equation_id}_temperature_derivative",
        value=derivative,
        unit=f"{correlation.output_unit}/K",
        inputs=inputs,
        warnings=pressure.warnings,
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
        if T + coeffs["C"] <= 0:
            raise ValueError("Antoine vapor pressure singularity: T + C must be positive")
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
    if equation == "dippr101_vapor_pressure":
        return exp(
            coeffs["A"]
            + coeffs["B"] / T
            + coeffs["C"] * log(T)
            + coeffs["D"] * T ** coeffs["E"]
        )
    if equation == "cp_polynomial":
        return _cp_polynomial(T, coeffs)
    if equation == "watson_hvap":
        Tc = coeffs["Tc"]
        T_ref = coeffs["T_ref"]
        if temperature_K >= Tc:
            return 0.0
        ratio = (1.0 - temperature_K / Tc) / (1.0 - T_ref / Tc)
        return coeffs["Hvap_ref"] * ratio ** coeffs.get("exponent", 0.38)
    if equation == "constant_phase_change_enthalpy":
        return coeffs["delta_h"]
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
    if equation == "sutherland_gas_viscosity":
        T_ref = coeffs["T_ref"]
        if T_ref <= 0:
            raise ValueError("sutherland_gas_viscosity requires positive T_ref")
        S = coeffs["S"]
        if T + S <= 0 or T_ref + S <= 0:
            raise ValueError("sutherland_gas_viscosity has invalid Sutherland constant")
        return coeffs["mu_ref"] * (T / T_ref) ** 1.5 * (T_ref + S) / (T + S)
    if equation == "surface_tension_power":
        Tc = coeffs["Tc"]
        T_ref = coeffs["T_ref"]
        if temperature_K >= Tc:
            return 0.0
        ratio = (1.0 - temperature_K / Tc) / (1.0 - T_ref / Tc)
        return coeffs["sigma_ref"] * ratio ** coeffs.get("exponent", 1.26)
    raise ValueError(f"Unsupported property equation_id: {equation}")


def _evaluate_temperature_derivative(
    correlation: PropertyCorrelation,
    *,
    inputs: dict[str, float],
    pressure_value: float,
) -> float:
    equation = correlation.equation_id
    coeffs = correlation.coefficients
    T = inputs["temperature"]
    if equation == "antoine":
        base = coeffs.get("base", 10.0)
        denominator = T + coeffs["C"]
        if denominator <= 0:
            raise ValueError("Antoine vapor pressure singularity: T + C must be positive")
        return pressure_value * log(base) * coeffs["B"] / denominator**2
    if equation == "wagner":
        Tc = coeffs["Tc"]
        if Tc <= T:
            raise ValueError("Wagner vapor pressure derivative requires T < Tc")
        tau = 1.0 - T / Tc
        reduced_temperature = T / Tc
        numerator = (
            coeffs["a"] * tau
            + coeffs["b"] * tau**1.5
            + coeffs["c"] * tau**3.0
            + coeffs["d"] * tau**6.0
        )
        dnumerator_dtau = (
            coeffs["a"]
            + 1.5 * coeffs["b"] * tau**0.5
            + 3.0 * coeffs["c"] * tau**2.0
            + 6.0 * coeffs["d"] * tau**5.0
        )
        dnumerator_dT = -dnumerator_dtau / Tc
        dreduced_temperature_dT = 1.0 / Tc
        dexponent_dT = (
            dnumerator_dT * reduced_temperature
            - numerator * dreduced_temperature_dT
        ) / reduced_temperature**2
        return pressure_value * dexponent_dT
    if equation == "dippr101_vapor_pressure":
        return pressure_value * (
            -coeffs["B"] / T**2
            + coeffs["C"] / T
            + coeffs["D"] * coeffs["E"] * T ** (coeffs["E"] - 1.0)
        )
    raise ValueError(
        f"Unsupported vapor-pressure derivative equation_id: {equation}"
    )


def property_correlation_model_cards() -> tuple[ModelCard, ...]:
    """Return model cards for generic property-correlation families."""

    return (
        ModelCard(
            model_id="vapor_pressure_correlation_families",
            module_id="properties",
            title="Vapor-Pressure Correlation Families",
            maturity=MaturityLevel.REFERENCE_VALIDATED,
            summary=(
                "Formula-level vapor and sublimation pressure evaluators with "
                "explicit validity ranges, analytic temperature derivatives, "
                "and JSON-friendly reports."
            ),
            equations=(
                "Antoine: log_base(P) = A - B/(T + C)",
                "Wagner original 3,6 form: ln(P/Pc) = "
                "(a*tau + b*tau**1.5 + c*tau**3 + d*tau**6)/Tr",
                "DIPPR101: P = exp(A + B/T + C*ln(T) + D*T**E)",
                "dP/dT is analytic for Antoine, Wagner, and DIPPR101 reports.",
            ),
            assumptions=(
                "Coefficient units must match each PropertyCorrelation input "
                "and output unit declaration.",
                "Validity ranges are treated as benchmark contracts; callers "
                "choose warn, raise, or ignore policy.",
                "Sublimation pressure uses the same formula families when a "
                "caller supplies sublimation-pressure coefficients.",
            ),
            validity_limits=(
                "No automatic method ranking beyond the caller-provided "
                "correlation order in ComponentPropertyPackage.",
                "No data-table vendoring; only explicitly curated coefficients "
                "are shipped.",
                "Critical-region behavior is limited to declared correlation "
                "validity bounds.",
            ),
            failure_modes=(
                "Unsupported equations fail before derivative evaluation.",
                "Antoine singularities fail when T + C is nonpositive.",
                "Wagner reports fail at or above the declared critical temperature.",
                "Out-of-range calls can hard-fail with validity_policy='raise'.",
            ),
            units={
                "temperature": "K or declared temperature unit",
                "pressure": "Pa or declared pressure unit",
                "dP_dT": "declared_pressure_unit/K",
                "dlnP_dT": "1/K",
            },
            reference_reading=(
                "reference_repos/chemicals/chemicals/vapor_pressure.py: "
                "Antoine, Wagner, dWagner_dT, vapor-pressure data families",
                "reference_repos/chemicals/chemicals/dippr.py: EQ101 and "
                "order=1 derivative",
                "reference_repos/thermo/thermo/vapor_pressure.py: "
                "VaporPressure method ranking, validity limits, and derivative API",
            ),
            validation_evidence=(
                ValidationEvidence(
                    evidence_id="antoine-vapor-pressure-derivative-test",
                    evidence_type="unit_test",
                    description=(
                        "Checks Antoine pressure and analytic derivative "
                        "against central finite differences."
                    ),
                    status="implemented",
                    command_or_path="tests/test_physchem_properties.py",
                    tolerance="rtol=1e-5",
                ),
                ValidationEvidence(
                    evidence_id="dippr101-vapor-pressure-derivative-test",
                    evidence_type="unit_test",
                    description=(
                        "Checks DIPPR101 analytic dP/dT against central finite "
                        "differences for curated compounds."
                    ),
                    status="implemented",
                    command_or_path="tests/test_physchem_properties.py",
                    tolerance="rtol=1e-5",
                ),
            ),
            model_limit_notes=(
                "This is a compact formula-family implementation, not a "
                "replacement for chemicals/thermo data coverage or EOS-based "
                "critical-region saturation solvers.",
            ),
            intended_use=(
                "Flash, distillation, volatility-risk, and safety-envelope "
                "tasks requiring auditable vapor-pressure values and slopes.",
                "Benchmark datasets that need replayable property reports with "
                "validity status.",
            ),
        ),
    )


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
        "sublimation_pressure",
        "heat_capacity",
        "heat_of_vaporization",
        "heat_of_fusion",
        "liquid_density",
        "gas_density",
        "liquid_viscosity",
        "gas_viscosity",
        "surface_tension",
    } and value < 0:
        raise ValueError(f"Correlation returned negative value: {correlation.correlation_id}")


def _pressure_unit_to_pa_factor(unit: str) -> float:
    return convert_value(1.0, unit, "Pa")


def _vapor_pressure_method_family(equation_id: str) -> str:
    if equation_id == "dippr101_vapor_pressure":
        return "DIPPR101"
    if equation_id == "antoine":
        return "Antoine"
    if equation_id == "wagner":
        return "Wagner"
    return equation_id


def _clamp(value: float, lower: float, upper: float) -> float:
    return min(max(value, lower), upper)
