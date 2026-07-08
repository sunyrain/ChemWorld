"""Property-correlation evaluators for the ChemWorld physchem core."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from math import exp, isfinite, log, sqrt
from typing import Literal

from chemworld.foundation.units import Quantity, convert_value
from chemworld.physchem.property_cards import (
    _HEAT_ENTHALPY_REFERENCE_READING,
    _TRANSPORT_REFERENCE_READING,
    _VOLUME_REFERENCE_READING,
)
from chemworld.physchem.specs import ComponentSpec, MixtureSpec, PropertyCorrelation

R_J_PER_MOL_K = 8.31446261815324
STANDARD_PRESSURE_PA = 101325.0
ValidityPolicy = Literal["warn", "raise", "ignore"]
PhaseLabel = Literal["solid", "liquid", "gas"]
_PHASES = {"solid", "liquid", "gas"}


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
class MolarVolumeReport:
    """Molar volume, optional density, and compressibility diagnostics."""

    evaluation: PropertyEvaluation
    phase: str
    method_family: str
    density_kg_m3: float | None = None
    compressibility_factor: float | None = None
    compressibility_status: str = "not_applicable"
    reference_reading: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _validate_phase(self.phase)
        if self.evaluation.property_id not in {
            "liquid_molar_volume",
            "gas_molar_volume",
        }:
            raise ValueError("MolarVolumeReport requires a molar-volume property")
        molar_volume = self.evaluation.to("m^3/mol").value
        if molar_volume <= 0 or not isfinite(molar_volume):
            raise ValueError("molar volume must be positive and finite")
        if self.density_kg_m3 is not None and self.density_kg_m3 <= 0:
            raise ValueError("density_kg_m3 must be positive when provided")
        if self.compressibility_factor is not None and (
            self.compressibility_factor <= 0
            or not isfinite(self.compressibility_factor)
        ):
            raise ValueError("compressibility_factor must be positive and finite")
        if self.compressibility_status not in {
            "ideal",
            "low_correction",
            "moderate_correction",
            "large_correction",
            "not_applicable",
        }:
            raise ValueError("invalid compressibility_status")
        object.__setattr__(self, "reference_reading", tuple(self.reference_reading))

    @property
    def molar_volume_m3_mol(self) -> float:
        return self.evaluation.to("m^3/mol").value

    def to_dict(self) -> dict[str, object]:
        return {
            "property": self.evaluation.to_dict(),
            "phase": self.phase,
            "method_family": self.method_family,
            "molar_volume_m3_mol": self.molar_volume_m3_mol,
            "density_kg_m3": self.density_kg_m3,
            "compressibility_factor": self.compressibility_factor,
            "compressibility_status": self.compressibility_status,
            "reference_reading": list(self.reference_reading),
        }


@dataclass(frozen=True)
class MixtureVolumeLedger:
    """Amgat-style mixture molar-volume ledger."""

    ledger_id: str
    phase: str
    contributions: dict[str, dict[str, float]]
    mixture_molar_volume_m3_mol: float
    mixture_density_kg_m3: float | None = None
    warnings: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.ledger_id:
            raise ValueError("ledger_id cannot be empty")
        _validate_phase(self.phase)
        if not self.contributions:
            raise ValueError("MixtureVolumeLedger requires contributions")
        if self.mixture_molar_volume_m3_mol <= 0:
            raise ValueError("mixture_molar_volume_m3_mol must be positive")
        if self.mixture_density_kg_m3 is not None and self.mixture_density_kg_m3 <= 0:
            raise ValueError("mixture_density_kg_m3 must be positive when provided")
        recomputed = sum(
            entry["mole_fraction"] * entry["molar_volume_m3_mol"]
            for entry in self.contributions.values()
        )
        if abs(recomputed - self.mixture_molar_volume_m3_mol) > 1e-12:
            raise ValueError("mixture molar volume must match contributions")
        object.__setattr__(
            self,
            "contributions",
            {
                component_id: dict(contribution)
                for component_id, contribution in self.contributions.items()
            },
        )
        object.__setattr__(self, "warnings", tuple(self.warnings))

    def to_dict(self) -> dict[str, object]:
        return {
            "ledger_id": self.ledger_id,
            "phase": self.phase,
            "contributions": {
                component_id: dict(contribution)
                for component_id, contribution in self.contributions.items()
            },
            "mixture_molar_volume_m3_mol": self.mixture_molar_volume_m3_mol,
            "mixture_density_kg_m3": self.mixture_density_kg_m3,
            "warnings": list(self.warnings),
        }


@dataclass(frozen=True)
class TransportPropertyReport:
    """Transport property value with validity and uncertainty metadata."""

    evaluation: PropertyEvaluation
    phase: str
    method_family: str
    validity_status: str
    relative_uncertainty: float | None = None
    uncertainty_note: str = ""
    reference_reading: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _validate_phase(self.phase)
        if self.evaluation.property_id not in {
            "liquid_viscosity",
            "gas_viscosity",
            "mixture_viscosity",
            "thermal_conductivity",
            "mixture_thermal_conductivity",
            "binary_gas_diffusivity",
            "effective_gas_diffusivity",
            "thermal_diffusivity",
        }:
            raise ValueError("TransportPropertyReport requires a transport property")
        if self.evaluation.value <= 0 or not isfinite(self.evaluation.value):
            raise ValueError("transport property value must be positive and finite")
        if self.validity_status not in {"valid", "out_of_range", "estimated"}:
            raise ValueError("invalid transport validity_status")
        if self.relative_uncertainty is not None and (
            self.relative_uncertainty < 0 or not isfinite(self.relative_uncertainty)
        ):
            raise ValueError("relative_uncertainty must be nonnegative when provided")
        object.__setattr__(self, "reference_reading", tuple(self.reference_reading))

    def to_dict(self) -> dict[str, object]:
        return {
            "property": self.evaluation.to_dict(),
            "phase": self.phase,
            "method_family": self.method_family,
            "validity_status": self.validity_status,
            "relative_uncertainty": self.relative_uncertainty,
            "uncertainty_note": self.uncertainty_note,
            "reference_reading": list(self.reference_reading),
        }


@dataclass(frozen=True)
class MixtureTransportLedger:
    """Mixture transport-property ledger with method-specific contributions."""

    ledger_id: str
    phase: str
    property_id: str
    method_family: str
    unit: str
    mixture_value: float
    contributions: dict[str, dict[str, float]]
    warnings: tuple[str, ...] = ()
    reference_reading: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.ledger_id:
            raise ValueError("ledger_id cannot be empty")
        _validate_phase(self.phase)
        if self.property_id not in {
            "mixture_viscosity",
            "mixture_thermal_conductivity",
            "effective_gas_diffusivity",
        }:
            raise ValueError("MixtureTransportLedger requires a mixture transport property")
        if self.mixture_value <= 0 or not isfinite(self.mixture_value):
            raise ValueError("mixture_value must be positive and finite")
        if not self.contributions:
            raise ValueError("MixtureTransportLedger requires contributions")
        object.__setattr__(
            self,
            "contributions",
            {
                component_id: dict(contribution)
                for component_id, contribution in self.contributions.items()
            },
        )
        object.__setattr__(self, "warnings", tuple(self.warnings))
        object.__setattr__(self, "reference_reading", tuple(self.reference_reading))

    def to_dict(self) -> dict[str, object]:
        return {
            "ledger_id": self.ledger_id,
            "phase": self.phase,
            "property_id": self.property_id,
            "method_family": self.method_family,
            "unit": self.unit,
            "mixture_value": self.mixture_value,
            "contributions": {
                component_id: dict(contribution)
                for component_id, contribution in self.contributions.items()
            },
            "warnings": list(self.warnings),
            "reference_reading": list(self.reference_reading),
        }


@dataclass(frozen=True)
class PhaseTransitionSpec:
    """A signed, auditable phase-transition enthalpy contract."""

    transition_id: str
    from_phase: str
    to_phase: str
    transition_temperature_K: float
    enthalpy_correlation: PropertyCorrelation
    source_note: str = ""

    def __post_init__(self) -> None:
        if not self.transition_id:
            raise ValueError("transition_id cannot be empty")
        _validate_phase(self.from_phase)
        _validate_phase(self.to_phase)
        if self.from_phase == self.to_phase:
            raise ValueError("phase transition must connect different phases")
        if self.transition_temperature_K <= 0:
            raise ValueError("transition_temperature_K must be positive")
        if self.enthalpy_correlation.property_id not in {
            "heat_of_vaporization",
            "heat_of_fusion",
        }:
            raise ValueError(
                "PhaseTransitionSpec requires heat_of_vaporization or "
                "heat_of_fusion correlation"
            )

    def connects(self, phase_a: str, phase_b: str) -> bool:
        return {phase_a, phase_b} == {self.from_phase, self.to_phase}

    def direction_sign(self, from_phase: str, to_phase: str) -> float:
        if from_phase == self.from_phase and to_phase == self.to_phase:
            return 1.0
        if from_phase == self.to_phase and to_phase == self.from_phase:
            return -1.0
        raise ValueError(
            f"Transition {self.transition_id!r} does not connect "
            f"{from_phase!r} -> {to_phase!r}"
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "transition_id": self.transition_id,
            "from_phase": self.from_phase,
            "to_phase": self.to_phase,
            "transition_temperature_K": self.transition_temperature_K,
            "enthalpy_correlation": self.enthalpy_correlation.to_dict(),
            "source_note": self.source_note,
        }


@dataclass(frozen=True)
class PhaseEnthalpyReport:
    """Molar enthalpy change across a declared phase path."""

    component_id: str
    initial_phase: str
    final_phase: str
    initial_temperature_K: float
    final_temperature_K: float
    reference_temperature_K: float
    sensible_enthalpy_J_mol: float
    transition_enthalpy_J_mol: float
    total_enthalpy_J_mol: float
    heat_capacity_correlation_ids: tuple[str, ...]
    transition_ids: tuple[str, ...] = ()
    validity_warnings: tuple[str, ...] = ()
    reference_reading: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.component_id:
            raise ValueError("component_id cannot be empty")
        _validate_phase(self.initial_phase)
        _validate_phase(self.final_phase)
        for name, value in {
            "initial_temperature_K": self.initial_temperature_K,
            "final_temperature_K": self.final_temperature_K,
            "reference_temperature_K": self.reference_temperature_K,
            "sensible_enthalpy_J_mol": self.sensible_enthalpy_J_mol,
            "transition_enthalpy_J_mol": self.transition_enthalpy_J_mol,
            "total_enthalpy_J_mol": self.total_enthalpy_J_mol,
        }.items():
            if not isfinite(value):
                raise ValueError(f"{name} must be finite")
        if self.initial_temperature_K <= 0 or self.final_temperature_K <= 0:
            raise ValueError("enthalpy report temperatures must be positive")
        if self.reference_temperature_K <= 0:
            raise ValueError("reference_temperature_K must be positive")
        if abs(
            self.sensible_enthalpy_J_mol
            + self.transition_enthalpy_J_mol
            - self.total_enthalpy_J_mol
        ) > 1e-8:
            raise ValueError("total_enthalpy_J_mol must equal sensible + transition")
        object.__setattr__(
            self,
            "heat_capacity_correlation_ids",
            tuple(self.heat_capacity_correlation_ids),
        )
        object.__setattr__(self, "transition_ids", tuple(self.transition_ids))
        object.__setattr__(self, "validity_warnings", tuple(self.validity_warnings))
        object.__setattr__(self, "reference_reading", tuple(self.reference_reading))

    def to_dict(self) -> dict[str, object]:
        return {
            "component_id": self.component_id,
            "initial_phase": self.initial_phase,
            "final_phase": self.final_phase,
            "initial_temperature_K": self.initial_temperature_K,
            "final_temperature_K": self.final_temperature_K,
            "reference_temperature_K": self.reference_temperature_K,
            "sensible_enthalpy_J_mol": self.sensible_enthalpy_J_mol,
            "transition_enthalpy_J_mol": self.transition_enthalpy_J_mol,
            "total_enthalpy_J_mol": self.total_enthalpy_J_mol,
            "heat_capacity_correlation_ids": list(self.heat_capacity_correlation_ids),
            "transition_ids": list(self.transition_ids),
            "validity_warnings": list(self.validity_warnings),
            "reference_reading": list(self.reference_reading),
        }


@dataclass(frozen=True)
class MixtureEnthalpyLedger:
    """Mole-weighted enthalpy ledger for reactor and separation duties."""

    ledger_id: str
    contributions: dict[str, dict[str, float]]
    total_enthalpy_change_J: float
    warnings: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.ledger_id:
            raise ValueError("ledger_id cannot be empty")
        if not self.contributions:
            raise ValueError("MixtureEnthalpyLedger requires contributions")
        if not isfinite(self.total_enthalpy_change_J):
            raise ValueError("total_enthalpy_change_J must be finite")
        recomputed = sum(
            contribution["enthalpy_change_J"]
            for contribution in self.contributions.values()
        )
        if abs(recomputed - self.total_enthalpy_change_J) > 1e-8:
            raise ValueError("total_enthalpy_change_J must match contributions")
        object.__setattr__(
            self,
            "contributions",
            {
                component_id: dict(contribution)
                for component_id, contribution in self.contributions.items()
            },
        )
        object.__setattr__(self, "warnings", tuple(self.warnings))

    def to_dict(self) -> dict[str, object]:
        return {
            "ledger_id": self.ledger_id,
            "contributions": {
                component_id: dict(contribution)
                for component_id, contribution in self.contributions.items()
            },
            "total_enthalpy_change_J": self.total_enthalpy_change_J,
            "warnings": list(self.warnings),
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
    _ensure_positive_heat_capacity_interval(heat_capacity_correlation, T0, T1)
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


def heat_capacity_report(
    heat_capacity_correlation: PropertyCorrelation,
    *,
    temperature_K: float,
    validity_policy: ValidityPolicy = "warn",
) -> PropertyEvaluation:
    """Evaluate a phase-aware heat-capacity correlation with strict positivity."""

    _validate_heat_capacity_correlation(heat_capacity_correlation)
    result = evaluate_correlation(
        heat_capacity_correlation,
        temperature_K=temperature_K,
        validity_policy=validity_policy,
    )
    if result.value <= 0:
        raise ValueError(
            f"Heat capacity must be positive: {heat_capacity_correlation.correlation_id}"
        )
    return result


def phase_sensible_enthalpy_report(
    *,
    component_id: str,
    phase: str,
    heat_capacity_correlation: PropertyCorrelation,
    initial_temperature_K: float,
    final_temperature_K: float,
    reference_temperature_K: float = 298.15,
    validity_policy: ValidityPolicy = "warn",
) -> PhaseEnthalpyReport:
    """Report same-phase sensible enthalpy with an explicit reference state."""

    _validate_phase(phase)
    _validate_heat_capacity_correlation(heat_capacity_correlation)
    _validate_correlation_phase(heat_capacity_correlation, phase)
    if reference_temperature_K <= 0:
        raise ValueError("reference_temperature_K must be positive")
    initial_relative = sensible_enthalpy_change(
        heat_capacity_correlation,
        initial_temperature_K=reference_temperature_K,
        final_temperature_K=initial_temperature_K,
        validity_policy=validity_policy,
    )
    final_relative = sensible_enthalpy_change(
        heat_capacity_correlation,
        initial_temperature_K=reference_temperature_K,
        final_temperature_K=final_temperature_K,
        validity_policy=validity_policy,
    )
    sensible_delta = final_relative.value - initial_relative.value
    warnings = initial_relative.warnings + final_relative.warnings
    return PhaseEnthalpyReport(
        component_id=component_id,
        initial_phase=phase,
        final_phase=phase,
        initial_temperature_K=initial_temperature_K,
        final_temperature_K=final_temperature_K,
        reference_temperature_K=reference_temperature_K,
        sensible_enthalpy_J_mol=sensible_delta,
        transition_enthalpy_J_mol=0.0,
        total_enthalpy_J_mol=sensible_delta,
        heat_capacity_correlation_ids=(heat_capacity_correlation.correlation_id,),
        validity_warnings=() if validity_policy == "ignore" else warnings,
        reference_reading=_HEAT_ENTHALPY_REFERENCE_READING,
    )


def phase_transition_enthalpy(
    transition: PhaseTransitionSpec,
    *,
    from_phase: str,
    to_phase: str,
    temperature_K: float | None = None,
    validity_policy: ValidityPolicy = "warn",
) -> PropertyEvaluation:
    """Return signed molar latent heat for a declared transition direction."""

    _validate_phase(from_phase)
    _validate_phase(to_phase)
    if from_phase == to_phase:
        raise ValueError("phase_transition_enthalpy requires different phases")
    sign = transition.direction_sign(from_phase, to_phase)
    temperature = (
        transition.transition_temperature_K
        if temperature_K is None
        else temperature_K
    )
    latent = evaluate_correlation(
        transition.enthalpy_correlation,
        temperature_K=temperature,
        validity_policy=validity_policy,
    )
    if latent.value < 0:
        raise ValueError(f"Latent heat must be nonnegative: {transition.transition_id}")
    return PropertyEvaluation(
        property_id=f"{transition.enthalpy_correlation.property_id}_signed",
        correlation_id=transition.enthalpy_correlation.correlation_id,
        equation_id=transition.enthalpy_correlation.equation_id,
        value=sign * latent.to("J/mol").value,
        unit="J/mol",
        inputs={
            "temperature": latent.inputs["temperature"],
            "direction_sign": sign,
        },
        warnings=latent.warnings,
    )


def phase_path_enthalpy_report(
    *,
    component_id: str,
    heat_capacity_correlations: Mapping[str, PropertyCorrelation],
    transitions: Sequence[PhaseTransitionSpec],
    initial_phase: str,
    final_phase: str,
    initial_temperature_K: float,
    final_temperature_K: float,
    reference_temperature_K: float = 298.15,
    validity_policy: ValidityPolicy = "warn",
) -> PhaseEnthalpyReport:
    """Integrate heat capacity and latent heat along a phase path."""

    _validate_phase(initial_phase)
    _validate_phase(final_phase)
    if reference_temperature_K <= 0:
        raise ValueError("reference_temperature_K must be positive")
    phase_path = _phase_path(initial_phase, final_phase, transitions)
    current_phase = initial_phase
    current_temperature = initial_temperature_K
    sensible_total = 0.0
    transition_total = 0.0
    warnings: list[str] = []
    cp_ids: list[str] = []
    transition_ids: list[str] = []
    for next_phase, transition in phase_path:
        cp = _heat_capacity_for_phase(heat_capacity_correlations, current_phase)
        cp_ids.append(cp.correlation_id)
        _validate_correlation_phase(cp, current_phase)
        sensible = sensible_enthalpy_change(
            cp,
            initial_temperature_K=current_temperature,
            final_temperature_K=transition.transition_temperature_K,
            validity_policy=validity_policy,
        )
        latent = phase_transition_enthalpy(
            transition,
            from_phase=current_phase,
            to_phase=next_phase,
            validity_policy=validity_policy,
        )
        sensible_total += sensible.value
        transition_total += latent.value
        warnings.extend(sensible.warnings)
        warnings.extend(latent.warnings)
        transition_ids.append(transition.transition_id)
        current_phase = next_phase
        current_temperature = transition.transition_temperature_K
    cp = _heat_capacity_for_phase(heat_capacity_correlations, current_phase)
    cp_ids.append(cp.correlation_id)
    _validate_correlation_phase(cp, current_phase)
    final_sensible = sensible_enthalpy_change(
        cp,
        initial_temperature_K=current_temperature,
        final_temperature_K=final_temperature_K,
        validity_policy=validity_policy,
    )
    sensible_total += final_sensible.value
    warnings.extend(final_sensible.warnings)
    return PhaseEnthalpyReport(
        component_id=component_id,
        initial_phase=initial_phase,
        final_phase=final_phase,
        initial_temperature_K=initial_temperature_K,
        final_temperature_K=final_temperature_K,
        reference_temperature_K=reference_temperature_K,
        sensible_enthalpy_J_mol=sensible_total,
        transition_enthalpy_J_mol=transition_total,
        total_enthalpy_J_mol=sensible_total + transition_total,
        heat_capacity_correlation_ids=tuple(dict.fromkeys(cp_ids)),
        transition_ids=tuple(transition_ids),
        validity_warnings=() if validity_policy == "ignore" else tuple(warnings),
        reference_reading=_HEAT_ENTHALPY_REFERENCE_READING,
    )


def mixture_enthalpy_ledger(
    *,
    component_amounts_mol: Mapping[str, float],
    component_reports: Mapping[str, PhaseEnthalpyReport],
    ledger_id: str = "mixture_enthalpy_ledger",
) -> MixtureEnthalpyLedger:
    """Build a mole-weighted enthalpy ledger from component reports."""

    if not component_amounts_mol:
        raise ValueError("component_amounts_mol cannot be empty")
    contributions: dict[str, dict[str, float]] = {}
    warnings: list[str] = []
    total = 0.0
    for component_id, amount_mol in component_amounts_mol.items():
        if amount_mol < 0:
            raise ValueError(f"amount_mol cannot be negative for {component_id!r}")
        if component_id not in component_reports:
            raise ValueError(f"Missing enthalpy report for component {component_id!r}")
        report = component_reports[component_id]
        if report.component_id != component_id:
            raise ValueError(
                f"Report component_id {report.component_id!r} does not match "
                f"ledger key {component_id!r}"
            )
        contribution = amount_mol * report.total_enthalpy_J_mol
        total += contribution
        contributions[component_id] = {
            "amount_mol": amount_mol,
            "molar_enthalpy_change_J_mol": report.total_enthalpy_J_mol,
            "enthalpy_change_J": contribution,
        }
        warnings.extend(report.validity_warnings)
    return MixtureEnthalpyLedger(
        ledger_id=ledger_id,
        contributions=contributions,
        total_enthalpy_change_J=total,
        warnings=tuple(warnings),
    )


def molar_volume_to_density_kg_m3(
    molar_volume_m3_mol: float,
    molecular_weight_g_mol: float,
) -> float:
    """Convert molar volume to mass density."""

    if molar_volume_m3_mol <= 0:
        raise ValueError("molar_volume_m3_mol must be positive")
    if molecular_weight_g_mol <= 0:
        raise ValueError("molecular_weight_g_mol must be positive")
    return molecular_weight_g_mol / 1000.0 / molar_volume_m3_mol


def density_to_molar_volume_m3_mol(
    density_kg_m3: float,
    molecular_weight_g_mol: float,
) -> float:
    """Convert mass density to molar volume."""

    if density_kg_m3 <= 0:
        raise ValueError("density_kg_m3 must be positive")
    if molecular_weight_g_mol <= 0:
        raise ValueError("molecular_weight_g_mol must be positive")
    return molecular_weight_g_mol / 1000.0 / density_kg_m3


def molar_volume_report(
    correlation: PropertyCorrelation,
    *,
    temperature_K: float,
    phase: str,
    molecular_weight_g_mol: float | None = None,
    validity_policy: ValidityPolicy = "warn",
) -> MolarVolumeReport:
    """Evaluate a liquid or correlation-based molar-volume report."""

    _validate_phase(phase)
    if correlation.property_id not in {
        "liquid_molar_volume",
        "gas_molar_volume",
    }:
        raise ValueError("molar_volume_report requires a molar-volume property")
    result = evaluate_correlation(
        correlation,
        temperature_K=temperature_K,
        validity_policy=validity_policy,
    )
    density = (
        molar_volume_to_density_kg_m3(result.to("m^3/mol").value, molecular_weight_g_mol)
        if molecular_weight_g_mol is not None
        else None
    )
    return MolarVolumeReport(
        evaluation=result,
        phase=phase,
        density_kg_m3=density,
        method_family=_molar_volume_method_family(correlation.equation_id),
        compressibility_status="not_applicable",
        reference_reading=_VOLUME_REFERENCE_READING,
    )


def ideal_gas_molar_volume_report(
    *,
    temperature_K: float,
    pressure_Pa: float,
    molecular_weight_g_mol: float | None = None,
) -> MolarVolumeReport:
    """Ideal-gas molar volume with optional density conversion."""

    if temperature_K <= 0:
        raise ValueError("temperature_K must be positive")
    if pressure_Pa <= 0:
        raise ValueError("pressure_Pa must be positive")
    molar_volume = R_J_PER_MOL_K * temperature_K / pressure_Pa
    density = (
        molar_volume_to_density_kg_m3(molar_volume, molecular_weight_g_mol)
        if molecular_weight_g_mol is not None
        else None
    )
    return MolarVolumeReport(
        evaluation=PropertyEvaluation(
            property_id="gas_molar_volume",
            correlation_id="ideal_gas_molar_volume",
            equation_id="ideal_gas_law",
            value=molar_volume,
            unit="m^3/mol",
            inputs={"temperature": temperature_K, "pressure": pressure_Pa},
        ),
        phase="gas",
        method_family="ideal_gas",
        density_kg_m3=density,
        compressibility_factor=1.0,
        compressibility_status="ideal",
        reference_reading=_VOLUME_REFERENCE_READING,
    )


def second_virial_coefficient_report(
    correlation: PropertyCorrelation,
    *,
    temperature_K: float,
    validity_policy: ValidityPolicy = "warn",
) -> PropertyEvaluation:
    """Evaluate a second virial coefficient in m^3/mol."""

    if correlation.property_id != "second_virial_coefficient":
        raise ValueError(
            "second_virial_coefficient_report requires second_virial_coefficient"
        )
    result = evaluate_correlation(
        correlation,
        temperature_K=temperature_K,
        validity_policy=validity_policy,
    )
    return result.to("m^3/mol")


def virial_gas_molar_volume_report(
    *,
    temperature_K: float,
    pressure_Pa: float,
    second_virial_m3_mol: float,
    molecular_weight_g_mol: float | None = None,
    warning_threshold: float = 0.05,
) -> MolarVolumeReport:
    """Second-virial gas molar volume from Z = 1 + B/Vm."""

    if temperature_K <= 0:
        raise ValueError("temperature_K must be positive")
    if pressure_Pa <= 0:
        raise ValueError("pressure_Pa must be positive")
    if warning_threshold <= 0:
        raise ValueError("warning_threshold must be positive")
    rt = R_J_PER_MOL_K * temperature_K
    discriminant = rt * rt + 4.0 * pressure_Pa * rt * second_virial_m3_mol
    if discriminant <= 0:
        raise ValueError("second virial coefficient gives no positive gas-volume root")
    molar_volume = (rt + sqrt(discriminant)) / (2.0 * pressure_Pa)
    if molar_volume <= 0:
        raise ValueError("virial gas molar volume root must be positive")
    z_factor = pressure_Pa * molar_volume / rt
    correction = abs(second_virial_m3_mol / molar_volume)
    if correction <= 1e-12:
        status = "ideal"
    elif correction <= warning_threshold:
        status = "low_correction"
    elif correction <= 4.0 * warning_threshold:
        status = "moderate_correction"
    else:
        status = "large_correction"
    density = (
        molar_volume_to_density_kg_m3(molar_volume, molecular_weight_g_mol)
        if molecular_weight_g_mol is not None
        else None
    )
    return MolarVolumeReport(
        evaluation=PropertyEvaluation(
            property_id="gas_molar_volume",
            correlation_id="second_virial_gas_molar_volume",
            equation_id="second_virial_volume_root",
            value=molar_volume,
            unit="m^3/mol",
            inputs={
                "temperature": temperature_K,
                "pressure": pressure_Pa,
                "second_virial_m3_mol": second_virial_m3_mol,
            },
        ),
        phase="gas",
        method_family="second_virial",
        density_kg_m3=density,
        compressibility_factor=z_factor,
        compressibility_status=status,
        reference_reading=_VOLUME_REFERENCE_READING,
    )


def mixture_molar_volume_ledger(
    *,
    component_mole_fractions: Mapping[str, float],
    component_molar_volumes_m3_mol: Mapping[str, float],
    component_molecular_weights_g_mol: Mapping[str, float] | None = None,
    phase: str = "liquid",
    ledger_id: str = "mixture_molar_volume_ledger",
) -> MixtureVolumeLedger:
    """Amgat-style mole-fraction mixture molar volume ledger."""

    _validate_phase(phase)
    if not component_mole_fractions:
        raise ValueError("component_mole_fractions cannot be empty")
    total_fraction = sum(component_mole_fractions.values())
    if abs(total_fraction - 1.0) > 1e-9:
        raise ValueError("component mole fractions must sum to 1")
    contributions: dict[str, dict[str, float]] = {}
    mixture_molar_volume = 0.0
    average_mw = 0.0
    for component_id, mole_fraction in component_mole_fractions.items():
        if mole_fraction < 0:
            raise ValueError(f"negative mole fraction for {component_id!r}")
        if component_id not in component_molar_volumes_m3_mol:
            raise ValueError(f"missing molar volume for {component_id!r}")
        molar_volume = component_molar_volumes_m3_mol[component_id]
        if molar_volume <= 0:
            raise ValueError(f"molar volume must be positive for {component_id!r}")
        contribution = mole_fraction * molar_volume
        mixture_molar_volume += contribution
        entry = {
            "mole_fraction": mole_fraction,
            "molar_volume_m3_mol": molar_volume,
            "volume_contribution_m3_mol": contribution,
        }
        if component_molecular_weights_g_mol is not None:
            if component_id not in component_molecular_weights_g_mol:
                raise ValueError(f"missing molecular weight for {component_id!r}")
            mw = component_molecular_weights_g_mol[component_id]
            if mw <= 0:
                raise ValueError(
                    f"molecular weight must be positive for {component_id!r}"
                )
            average_mw += mole_fraction * mw
            entry["molecular_weight_g_mol"] = mw
        contributions[component_id] = entry
    density = (
        molar_volume_to_density_kg_m3(mixture_molar_volume, average_mw)
        if component_molecular_weights_g_mol is not None
        else None
    )
    return MixtureVolumeLedger(
        ledger_id=ledger_id,
        phase=phase,
        contributions=contributions,
        mixture_molar_volume_m3_mol=mixture_molar_volume,
        mixture_density_kg_m3=density,
        warnings=(
            "Amgat ideal-volume mixing; no excess volume contribution included.",
        ),
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


def transport_property_report(
    correlation: PropertyCorrelation,
    *,
    temperature_K: float,
    phase: str,
    pressure_Pa: float | None = None,
    molecular_weight_g_mol: float | None = None,
    validity_policy: ValidityPolicy = "warn",
    relative_uncertainty: float | None = None,
    uncertainty_note: str = "",
) -> TransportPropertyReport:
    """Evaluate a pure-component transport property with method metadata."""

    _validate_phase(phase)
    if correlation.property_id not in {
        "liquid_viscosity",
        "gas_viscosity",
        "thermal_conductivity",
    }:
        raise ValueError(
            "transport_property_report requires viscosity or thermal_conductivity"
        )
    result = evaluate_correlation(
        correlation,
        temperature_K=temperature_K,
        pressure_Pa=pressure_Pa,
        molecular_weight_g_mol=molecular_weight_g_mol,
        validity_policy=validity_policy,
    )
    return TransportPropertyReport(
        evaluation=result,
        phase=phase,
        method_family=_transport_method_family(correlation.equation_id),
        validity_status="out_of_range" if result.warnings else "valid",
        relative_uncertainty=relative_uncertainty,
        uncertainty_note=uncertainty_note,
        reference_reading=_TRANSPORT_REFERENCE_READING,
    )


def gas_thermal_conductivity_dippr9b_report(
    *,
    temperature_K: float,
    molecular_weight_g_mol: float,
    molar_cv_J_mol_K: float,
    viscosity_Pa_s: float,
    critical_temperature_K: float | None = None,
    molecule_type: str = "linear",
    relative_uncertainty: float = 0.2,
) -> TransportPropertyReport:
    """DIPPR9B-style gas thermal conductivity from Cv and viscosity."""

    if temperature_K <= 0:
        raise ValueError("temperature_K must be positive")
    if molecular_weight_g_mol <= 0:
        raise ValueError("molecular_weight_g_mol must be positive")
    if molar_cv_J_mol_K <= 0:
        raise ValueError("molar_cv_J_mol_K must be positive")
    if viscosity_Pa_s <= 0:
        raise ValueError("viscosity_Pa_s must be positive")
    cv_j_kmol_k = molar_cv_J_mol_K * 1000.0
    if molecule_type == "monoatomic":
        conductivity = 2.5 * viscosity_Pa_s * cv_j_kmol_k / molecular_weight_g_mol
    elif molecule_type == "nonlinear":
        conductivity = (
            viscosity_Pa_s
            / molecular_weight_g_mol
            * (1.15 * cv_j_kmol_k + 16903.36)
        )
    elif molecule_type == "linear":
        if critical_temperature_K is None or critical_temperature_K <= 0:
            raise ValueError("linear DIPPR9B gas conductivity requires positive Tc")
        reduced_temperature = temperature_K / critical_temperature_K
        conductivity = (
            viscosity_Pa_s
            / molecular_weight_g_mol
            * (1.30 * cv_j_kmol_k + 14644.0 - 2928.80 / reduced_temperature)
        )
    else:
        raise ValueError("molecule_type must be monoatomic, linear, or nonlinear")
    if conductivity <= 0 or not isfinite(conductivity):
        raise ValueError("DIPPR9B gas conductivity returned nonpositive value")
    return TransportPropertyReport(
        evaluation=PropertyEvaluation(
            property_id="thermal_conductivity",
            correlation_id="dippr9b_gas_thermal_conductivity",
            equation_id="dippr9b_gas_thermal_conductivity",
            value=conductivity,
            unit="W/(m*K)",
            inputs={
                "temperature": temperature_K,
                "molecular_weight_g_mol": molecular_weight_g_mol,
                "molar_cv_J_mol_K": molar_cv_J_mol_K,
                "viscosity_Pa_s": viscosity_Pa_s,
                "critical_temperature_K": critical_temperature_K or 0.0,
            },
            warnings=(
                "DIPPR9B is an empirical gas thermal-conductivity estimate; "
                "accuracy depends on pure-gas viscosity and molecule type.",
            ),
        ),
        phase="gas",
        method_family="DIPPR9B",
        validity_status="estimated",
        relative_uncertainty=relative_uncertainty,
        uncertainty_note="DIPPR-style empirical gas conductivity estimate.",
        reference_reading=_TRANSPORT_REFERENCE_READING,
    )


def wilke_gas_mixture_viscosity_ledger(
    *,
    component_mole_fractions: Mapping[str, float],
    component_viscosities_Pa_s: Mapping[str, float],
    component_molecular_weights_g_mol: Mapping[str, float],
    ledger_id: str = "wilke_gas_mixture_viscosity",
) -> MixtureTransportLedger:
    """Wilke low-pressure gas-mixture viscosity ledger."""

    fractions = _validated_fraction_mapping(component_mole_fractions, "mole")
    _require_same_keys(fractions, component_viscosities_Pa_s, "viscosity")
    _require_same_keys(fractions, component_molecular_weights_g_mol, "molecular weight")
    component_ids = tuple(fractions)
    contributions: dict[str, dict[str, float]] = {}
    mixture_viscosity = 0.0
    for i in component_ids:
        yi = fractions[i]
        mui = component_viscosities_Pa_s[i]
        mwi = component_molecular_weights_g_mol[i]
        if mui <= 0:
            raise ValueError(f"viscosity must be positive for {i!r}")
        if mwi <= 0:
            raise ValueError(f"molecular weight must be positive for {i!r}")
        denominator = 0.0
        for j in component_ids:
            muj = component_viscosities_Pa_s[j]
            mwj = component_molecular_weights_g_mol[j]
            if muj <= 0:
                raise ValueError(f"viscosity must be positive for {j!r}")
            if mwj <= 0:
                raise ValueError(f"molecular weight must be positive for {j!r}")
            phi_ij = (
                (1.0 + sqrt(mui / muj) * (mwj / mwi) ** 0.25) ** 2.0
                / sqrt(8.0 * (1.0 + mwi / mwj))
            )
            denominator += fractions[j] * phi_ij
        partial = yi * mui / denominator
        mixture_viscosity += partial
        contributions[i] = {
            "mole_fraction": yi,
            "viscosity_Pa_s": mui,
            "molecular_weight_g_mol": mwi,
            "wilke_denominator": denominator,
            "partial_viscosity_Pa_s": partial,
        }
    return MixtureTransportLedger(
        ledger_id=ledger_id,
        phase="gas",
        property_id="mixture_viscosity",
        method_family="Wilke",
        unit="Pa*s",
        mixture_value=mixture_viscosity,
        contributions=contributions,
        warnings=(
            "Wilke low-pressure gas-mixture rule; hydrogen-rich systems can "
            "have larger errors and pure-component viscosity errors propagate.",
        ),
        reference_reading=_TRANSPORT_REFERENCE_READING,
    )


def liquid_mixture_thermal_conductivity_dippr9h_ledger(
    *,
    component_mass_fractions: Mapping[str, float],
    component_thermal_conductivities_W_m_K: Mapping[str, float],
    ledger_id: str = "dippr9h_liquid_mixture_conductivity",
) -> MixtureTransportLedger:
    """DIPPR9H/Vredeveld liquid-mixture thermal-conductivity ledger."""

    fractions = _validated_fraction_mapping(component_mass_fractions, "mass")
    _require_same_keys(fractions, component_thermal_conductivities_W_m_K, "conductivity")
    inverse_square_sum = 0.0
    contributions: dict[str, dict[str, float]] = {}
    max_k = 0.0
    min_k = float("inf")
    for component_id, mass_fraction in fractions.items():
        conductivity = component_thermal_conductivities_W_m_K[component_id]
        if conductivity <= 0:
            raise ValueError(f"thermal conductivity must be positive for {component_id!r}")
        term = mass_fraction / (conductivity * conductivity)
        inverse_square_sum += term
        max_k = max(max_k, conductivity)
        min_k = min(min_k, conductivity)
        contributions[component_id] = {
            "mass_fraction": mass_fraction,
            "thermal_conductivity_W_m_K": conductivity,
            "inverse_square_contribution": term,
        }
    warnings = ["DIPPR9H assumes nonaqueous liquid mixtures and can deviate up to 20%."]
    if max_k > 2.0 * min_k:
        warnings.append(
            "Component conductivities differ by more than 2x; DIPPR9H warning applies."
        )
    return MixtureTransportLedger(
        ledger_id=ledger_id,
        phase="liquid",
        property_id="mixture_thermal_conductivity",
        method_family="DIPPR9H",
        unit="W/(m*K)",
        mixture_value=1.0 / sqrt(inverse_square_sum),
        contributions=contributions,
        warnings=tuple(warnings),
        reference_reading=_TRANSPORT_REFERENCE_READING,
    )


def binary_gas_diffusivity_fuller_report(
    *,
    temperature_K: float,
    pressure_Pa: float,
    molecular_weight_a_g_mol: float,
    molecular_weight_b_g_mol: float,
    diffusion_volume_a: float,
    diffusion_volume_b: float,
    component_a: str = "A",
    component_b: str = "B",
    relative_uncertainty: float = 0.2,
) -> TransportPropertyReport:
    """Fuller-Schettler-Giddings binary gas diffusivity estimate."""

    if temperature_K <= 0:
        raise ValueError("temperature_K must be positive")
    if pressure_Pa <= 0:
        raise ValueError("pressure_Pa must be positive")
    if molecular_weight_a_g_mol <= 0 or molecular_weight_b_g_mol <= 0:
        raise ValueError("molecular weights must be positive")
    if diffusion_volume_a <= 0 or diffusion_volume_b <= 0:
        raise ValueError("diffusion volumes must be positive")
    pressure_atm = pressure_Pa / 101325.0
    mass_factor = sqrt(
        (molecular_weight_a_g_mol + molecular_weight_b_g_mol)
        / (2.0 * molecular_weight_a_g_mol * molecular_weight_b_g_mol)
    )
    diffusion_cm2_s = (
        1.43e-3
        * temperature_K**1.75
        * mass_factor
        / (
            pressure_atm
            * (diffusion_volume_a ** (1.0 / 3.0) + diffusion_volume_b ** (1.0 / 3.0))
            ** 2.0
        )
    )
    warnings = [
        "Fuller gas diffusivity is an empirical low-pressure estimate based on "
        "diffusion volumes.",
    ]
    if pressure_atm < 0.05 or pressure_atm > 20.0:
        warnings.append("pressure outside nominal Fuller low/moderate-pressure range")
    if temperature_K < 250.0 or temperature_K > 1500.0:
        warnings.append("temperature outside broad gas-diffusivity screening range")
    return TransportPropertyReport(
        evaluation=PropertyEvaluation(
            property_id="binary_gas_diffusivity",
            correlation_id=f"fuller_diffusivity:{component_a}:{component_b}",
            equation_id="fuller_schettler_giddings",
            value=diffusion_cm2_s * 1e-4,
            unit="m^2/s",
            inputs={
                "temperature": temperature_K,
                "pressure": pressure_Pa,
                "molecular_weight_a_g_mol": molecular_weight_a_g_mol,
                "molecular_weight_b_g_mol": molecular_weight_b_g_mol,
                "diffusion_volume_a": diffusion_volume_a,
                "diffusion_volume_b": diffusion_volume_b,
            },
            warnings=tuple(warnings),
        ),
        phase="gas",
        method_family="Fuller-Schettler-Giddings",
        validity_status="estimated",
        relative_uncertainty=relative_uncertainty,
        uncertainty_note="Screening estimate; requires calibrated diffusion volumes.",
        reference_reading=_TRANSPORT_REFERENCE_READING,
    )


def gas_mixture_effective_diffusivity_ledger(
    *,
    target_component: str,
    component_mole_fractions: Mapping[str, float],
    binary_diffusivities_m2_s: Mapping[str, float],
    ledger_id: str = "gas_mixture_effective_diffusivity",
) -> MixtureTransportLedger:
    """Mixture-averaged gas diffusivity for one dilute/trace component."""

    fractions = _validated_fraction_mapping(component_mole_fractions, "mole")
    if target_component not in fractions:
        raise ValueError("target_component must appear in component_mole_fractions")
    others = [component_id for component_id in fractions if component_id != target_component]
    if not others:
        raise ValueError("effective diffusivity requires at least two components")
    denominator = 0.0
    contributions: dict[str, dict[str, float]] = {}
    for component_id in others:
        if component_id not in binary_diffusivities_m2_s:
            raise ValueError(f"missing binary diffusivity for {component_id!r}")
        diffusivity = binary_diffusivities_m2_s[component_id]
        if diffusivity <= 0:
            raise ValueError(f"binary diffusivity must be positive for {component_id!r}")
        term = fractions[component_id] / diffusivity
        denominator += term
        contributions[component_id] = {
            "mole_fraction": fractions[component_id],
            "binary_diffusivity_m2_s": diffusivity,
            "resistance_term_s_m2": term,
        }
    if denominator <= 0:
        raise ValueError("effective diffusivity denominator must be positive")
    target_fraction = fractions[target_component]
    effective = (1.0 - target_fraction) / denominator
    contributions[target_component] = {
        "mole_fraction": target_fraction,
        "effective_diffusivity_m2_s": effective,
    }
    return MixtureTransportLedger(
        ledger_id=ledger_id,
        phase="gas",
        property_id="effective_gas_diffusivity",
        method_family="mixture-averaged gas diffusivity",
        unit="m^2/s",
        mixture_value=effective,
        contributions=contributions,
        warnings=(
            "Mixture-averaged diffusivity assumes binary diffusivities are "
            "available for all non-target components.",
        ),
        reference_reading=_TRANSPORT_REFERENCE_READING,
    )


def thermal_diffusivity_report(
    *,
    thermal_conductivity_W_m_K: float,
    density_kg_m3: float,
    heat_capacity_J_kg_K: float,
    phase: str,
) -> TransportPropertyReport:
    """Thermal diffusivity alpha = k/(rho Cp)."""

    _validate_phase(phase)
    if thermal_conductivity_W_m_K <= 0:
        raise ValueError("thermal_conductivity_W_m_K must be positive")
    if density_kg_m3 <= 0:
        raise ValueError("density_kg_m3 must be positive")
    if heat_capacity_J_kg_K <= 0:
        raise ValueError("heat_capacity_J_kg_K must be positive")
    value = thermal_conductivity_W_m_K / (density_kg_m3 * heat_capacity_J_kg_K)
    return TransportPropertyReport(
        evaluation=PropertyEvaluation(
            property_id="thermal_diffusivity",
            correlation_id="thermal_diffusivity_from_k_rho_cp",
            equation_id="thermal_diffusivity_definition",
            value=value,
            unit="m^2/s",
            inputs={
                "thermal_conductivity_W_m_K": thermal_conductivity_W_m_K,
                "density_kg_m3": density_kg_m3,
                "heat_capacity_J_kg_K": heat_capacity_J_kg_K,
            },
        ),
        phase=phase,
        method_family="definition",
        validity_status="valid",
        reference_reading=_TRANSPORT_REFERENCE_READING,
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
    if equation == "rackett_liquid_molar_volume":
        Tc = coeffs["Tc"]
        Pc = coeffs["Pc"]
        Zc = coeffs["Zc"]
        if Tc <= 0 or Pc <= 0 or Zc <= 0:
            raise ValueError("Rackett requires positive Tc, Pc, and Zc")
        if temperature_K >= Tc:
            raise ValueError("Rackett liquid molar volume requires T < Tc")
        exponent = 1.0 + (1.0 - temperature_K / Tc) ** (2.0 / 7.0)
        return R_J_PER_MOL_K * Tc / Pc * Zc**exponent
    if equation == "crc_second_virial":
        t = 298.15 / T - 1.0
        return 1e-6 * (
            coeffs.get("a1", 0.0)
            + t
            * (
                coeffs.get("a2", 0.0)
                + t
                * (
                    coeffs.get("a3", 0.0)
                    + t * (coeffs.get("a4", 0.0) + t * coeffs.get("a5", 0.0))
                )
            )
        )
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
    if equation == "linear_thermal_conductivity":
        conductivity = coeffs["k_ref"] * (
            1.0 + coeffs.get("alpha", 0.0) * (T - coeffs["T_ref"])
        )
        return conductivity
    if equation == "thermal_conductivity_polynomial":
        return (
            coeffs.get("a", 0.0)
            + coeffs.get("b", 0.0) * T
            + coeffs.get("c", 0.0) * T**2
            + coeffs.get("d", 0.0) * T**3
        )
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


def _validate_phase(phase: str) -> None:
    if phase not in _PHASES:
        raise ValueError(f"Unsupported phase {phase!r}; expected one of {sorted(_PHASES)}")


def _validate_heat_capacity_correlation(correlation: PropertyCorrelation) -> None:
    if correlation.equation_id != "cp_polynomial":
        raise ValueError("Only cp_polynomial supports analytic heat-capacity reports")
    if correlation.property_id not in {
        "heat_capacity",
        "ideal_gas_heat_capacity",
        "liquid_heat_capacity",
        "solid_heat_capacity",
    }:
        raise ValueError(
            "heat-capacity report requires heat_capacity, ideal_gas_heat_capacity, "
            "liquid_heat_capacity, or solid_heat_capacity"
        )


def _validate_correlation_phase(correlation: PropertyCorrelation, phase: str) -> None:
    declared_phase = correlation.metadata.get("phase")
    if declared_phase is not None and declared_phase != phase:
        raise ValueError(
            f"Correlation {correlation.correlation_id!r} declares phase "
            f"{declared_phase!r}, not {phase!r}"
        )
    property_phase = {
        "ideal_gas_heat_capacity": "gas",
        "liquid_heat_capacity": "liquid",
        "solid_heat_capacity": "solid",
    }.get(correlation.property_id)
    if property_phase is not None and property_phase != phase:
        raise ValueError(
            f"Correlation {correlation.correlation_id!r} is for "
            f"{property_phase!r}, not {phase!r}"
        )


def _ensure_positive_heat_capacity_interval(
    correlation: PropertyCorrelation,
    initial_temperature: float,
    final_temperature: float,
) -> None:
    _validate_heat_capacity_correlation(correlation)
    if initial_temperature <= 0 or final_temperature <= 0:
        raise ValueError("Heat-capacity integration temperatures must be positive")
    lower = min(initial_temperature, final_temperature)
    upper = max(initial_temperature, final_temperature)
    sample_temperatures = (
        lower,
        lower + 0.25 * (upper - lower),
        lower + 0.50 * (upper - lower),
        lower + 0.75 * (upper - lower),
        upper,
    )
    for temperature in sample_temperatures:
        cp = _cp_polynomial(temperature, correlation.coefficients)
        if cp <= 0 or not isfinite(cp):
            raise ValueError(
                f"Heat capacity must stay positive over integration interval: "
                f"{correlation.correlation_id}"
            )


def _heat_capacity_for_phase(
    correlations: Mapping[str, PropertyCorrelation],
    phase: str,
) -> PropertyCorrelation:
    _validate_phase(phase)
    if phase not in correlations:
        raise ValueError(f"Missing heat-capacity correlation for phase {phase!r}")
    correlation = correlations[phase]
    _validate_heat_capacity_correlation(correlation)
    return correlation


def _phase_path(
    initial_phase: str,
    final_phase: str,
    transitions: Sequence[PhaseTransitionSpec],
) -> tuple[tuple[str, PhaseTransitionSpec], ...]:
    if initial_phase == final_phase:
        return ()
    queue: list[tuple[str, tuple[tuple[str, PhaseTransitionSpec], ...]]] = [
        (initial_phase, ())
    ]
    visited = {initial_phase}
    while queue:
        phase, path = queue.pop(0)
        for transition in transitions:
            next_phase: str | None = None
            if transition.from_phase == phase:
                next_phase = transition.to_phase
            elif transition.to_phase == phase:
                next_phase = transition.from_phase
            if next_phase is None or next_phase in visited:
                continue
            next_path = (*path, (next_phase, transition))
            if next_phase == final_phase:
                return next_path
            visited.add(next_phase)
            queue.append((next_phase, next_path))
    raise ValueError(
        f"No phase-transition path from {initial_phase!r} to {final_phase!r}"
    )


def _ensure_finite_positive(value: float, correlation: PropertyCorrelation) -> None:
    if not isfinite(value):
        raise ValueError(f"Correlation returned non-finite value: {correlation.correlation_id}")
    if correlation.property_id in {
        "vapor_pressure",
        "sublimation_pressure",
        "heat_capacity",
        "ideal_gas_heat_capacity",
        "liquid_heat_capacity",
        "solid_heat_capacity",
        "heat_of_vaporization",
        "heat_of_fusion",
        "liquid_molar_volume",
        "gas_molar_volume",
        "liquid_density",
        "gas_density",
        "liquid_viscosity",
        "gas_viscosity",
        "thermal_conductivity",
        "mixture_viscosity",
        "mixture_thermal_conductivity",
        "binary_gas_diffusivity",
        "effective_gas_diffusivity",
        "thermal_diffusivity",
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


def _molar_volume_method_family(equation_id: str) -> str:
    if equation_id == "rackett_liquid_molar_volume":
        return "Rackett"
    if equation_id == "crc_second_virial":
        return "CRC second virial"
    return equation_id


def _transport_method_family(equation_id: str) -> str:
    if equation_id == "andrade_viscosity":
        return "Andrade/Arrhenius viscosity"
    if equation_id == "sutherland_gas_viscosity":
        return "Sutherland gas viscosity"
    if equation_id == "linear_thermal_conductivity":
        return "linear thermal conductivity"
    if equation_id == "thermal_conductivity_polynomial":
        return "thermal conductivity polynomial"
    return equation_id


def _validated_fraction_mapping(
    fractions: Mapping[str, float],
    fraction_name: str,
) -> dict[str, float]:
    if not fractions:
        raise ValueError(f"component_{fraction_name}_fractions cannot be empty")
    total = sum(fractions.values())
    if abs(total - 1.0) > 1e-9:
        raise ValueError(f"component {fraction_name} fractions must sum to 1")
    normalized: dict[str, float] = {}
    for component_id, fraction in fractions.items():
        if not component_id:
            raise ValueError("component id cannot be empty")
        if fraction < 0 or not isfinite(fraction):
            raise ValueError(f"invalid {fraction_name} fraction for {component_id!r}")
        normalized[component_id] = float(fraction)
    return normalized


def _require_same_keys(
    reference: Mapping[str, float],
    values: Mapping[str, float],
    value_name: str,
) -> None:
    missing = sorted(set(reference) - set(values))
    extra = sorted(set(values) - set(reference))
    if missing or extra:
        raise ValueError(
            f"{value_name} keys must match components; missing={missing}, extra={extra}"
        )


def _clamp(value: float, lower: float, upper: float) -> float:
    return min(max(value, lower), upper)
