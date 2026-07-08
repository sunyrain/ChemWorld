"""JSON-friendly component, mixture, and property-correlation specs."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field
from math import isfinite
from typing import Any, ClassVar

from chemworld.foundation.units import unit_spec
from chemworld.physchem.elements import (
    hill_formula,
    mass_fractions_from_formula,
    molecular_weight,
    parse_formula,
)

_VALID_PHASES = {"gas", "liquid", "solid", "aqueous", "organic", "unknown"}
_FRACTION_TOL = 1e-9
_MOLECULAR_WEIGHT_REL_TOL = 0.02

_PHASE_COMPATIBILITY: dict[str, set[str]] = {
    "gas": {"gas", "unknown"},
    "liquid": {"liquid", "aqueous", "organic", "unknown"},
    "aqueous": {"liquid", "aqueous", "unknown"},
    "organic": {"liquid", "organic", "unknown"},
    "solid": {"solid", "unknown"},
    "unknown": _VALID_PHASES,
}

_EQUATION_CONTRACTS: dict[str, dict[str, object]] = {
    "antoine": {
        "required_coefficients": {"A", "B", "C"},
        "input_dimensions": {"temperature": "temperature"},
        "output_dimension": "pressure",
    },
    "wagner": {
        "required_coefficients": {"Tc", "Pc", "a", "b", "c", "d"},
        "input_dimensions": {"temperature": "temperature"},
        "output_dimension": "pressure",
    },
    "dippr101_vapor_pressure": {
        "required_coefficients": {"A", "B", "C", "D", "E"},
        "input_dimensions": {"temperature": "temperature"},
        "output_dimension": "pressure",
    },
    "cp_polynomial": {
        "required_coefficients": {"a"},
        "input_dimensions": {"temperature": "temperature"},
        "output_dimension": "molar_heat_capacity",
    },
    "watson_hvap": {
        "required_coefficients": {"Tc", "T_ref", "Hvap_ref"},
        "input_dimensions": {"temperature": "temperature"},
        "output_dimension": "molar_enthalpy",
    },
    "constant_phase_change_enthalpy": {
        "required_coefficients": {"delta_h"},
        "input_dimensions": {"temperature": "temperature"},
        "output_dimension": "molar_enthalpy",
    },
    "linear_liquid_density": {
        "required_coefficients": {"rho_ref", "T_ref"},
        "input_dimensions": {"temperature": "temperature"},
        "output_dimension": "mass_density",
    },
    "ideal_gas_density": {
        "required_coefficients": {"unused"},
        "input_dimensions": {"temperature": "temperature", "pressure": "pressure"},
        "output_dimension": "mass_density",
    },
    "andrade_viscosity": {
        "required_coefficients": {"A", "B"},
        "input_dimensions": {"temperature": "temperature"},
        "output_dimension": "dynamic_viscosity",
    },
    "sutherland_gas_viscosity": {
        "required_coefficients": {"mu_ref", "T_ref", "S"},
        "input_dimensions": {"temperature": "temperature"},
        "output_dimension": "dynamic_viscosity",
    },
    "surface_tension_power": {
        "required_coefficients": {"Tc", "T_ref", "sigma_ref"},
        "input_dimensions": {"temperature": "temperature"},
        "output_dimension": "surface_tension",
    },
}


@dataclass(frozen=True)
class ComponentSpec:
    """A compact component identity and composition record.

    The spec intentionally stores only stable identity, composition, phase, and
    policy metadata. Property models live in `PropertyCorrelation` records.
    """

    identifier: str
    formula: str
    molecular_weight_g_mol: float | None = None
    charge: int = 0
    default_phase: str = "liquid"
    safety_tags: tuple[str, ...] = ()
    allowed_property_correlations: tuple[str, ...] = ()
    aliases: tuple[str, ...] = ()
    metadata: dict[str, object] = field(default_factory=dict)
    molecular_weight_rel_tolerance: ClassVar[float] = _MOLECULAR_WEIGHT_REL_TOL

    def __post_init__(self) -> None:
        if not self.identifier:
            raise ValueError("Component identifier cannot be empty")
        if self.identifier.strip() != self.identifier or any(
            char.isspace() for char in self.identifier
        ):
            raise ValueError(
                "Component identifier cannot contain leading, trailing, or "
                "internal whitespace"
            )
        if self.default_phase not in _VALID_PHASES:
            raise ValueError(f"Unsupported default phase: {self.default_phase}")
        composition = parse_formula(self.formula)
        calculated_mw = molecular_weight(composition)
        if self.molecular_weight_g_mol is None:
            object.__setattr__(self, "molecular_weight_g_mol", calculated_mw)
        elif self.molecular_weight_g_mol <= 0:
            raise ValueError("molecular_weight_g_mol must be positive")
        elif (
            abs(self.molecular_weight_g_mol - calculated_mw) / calculated_mw
            > self.molecular_weight_rel_tolerance
        ):
            raise ValueError(
                "molecular_weight_g_mol is inconsistent with formula-derived "
                f"value {calculated_mw:g} g/mol"
            )
        if not isinstance(self.charge, int):
            raise ValueError("charge must be an integer")
        _validate_string_tuple(self.safety_tags, "safety_tags")
        _validate_string_tuple(
            self.allowed_property_correlations,
            "allowed_property_correlations",
        )
        _validate_string_tuple(self.aliases, "aliases")
        object.__setattr__(self, "safety_tags", tuple(self.safety_tags))
        object.__setattr__(
            self,
            "allowed_property_correlations",
            tuple(self.allowed_property_correlations),
        )
        object.__setattr__(self, "aliases", tuple(self.aliases))
        object.__setattr__(self, "metadata", dict(self.metadata))

    @property
    def composition(self) -> dict[str, float]:
        return parse_formula(self.formula)

    @property
    def hill_formula(self) -> str:
        return hill_formula(self.composition)

    def element_mass_fractions(self) -> dict[str, float]:
        return mass_fractions_from_formula(self.composition)

    def to_dict(self) -> dict[str, object]:
        return {
            "identifier": self.identifier,
            "formula": self.formula,
            "hill_formula": self.hill_formula,
            "composition": self.composition,
            "molecular_weight_g_mol": self.molecular_weight_g_mol,
            "charge": self.charge,
            "default_phase": self.default_phase,
            "safety_tags": list(self.safety_tags),
            "allowed_property_correlations": list(self.allowed_property_correlations),
            "aliases": list(self.aliases),
            "metadata": dict(self.metadata),
            "units": {"molecular_weight_g_mol": "g/mol"},
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> ComponentSpec:
        return cls(
            identifier=str(payload["identifier"]),
            formula=str(payload["formula"]),
            molecular_weight_g_mol=(
                None
                if payload.get("molecular_weight_g_mol") is None
                else float(payload["molecular_weight_g_mol"])
            ),
            charge=int(payload.get("charge", 0)),
            default_phase=str(payload.get("default_phase", "liquid")),
            safety_tags=tuple(str(value) for value in payload.get("safety_tags", ())),
            allowed_property_correlations=tuple(
                str(value)
                for value in payload.get("allowed_property_correlations", ())
            ),
            aliases=tuple(str(value) for value in payload.get("aliases", ())),
            metadata=dict(payload.get("metadata", {})),
        )


@dataclass(frozen=True)
class MixtureSpec:
    """A phase-local mixture state with both mole and mass fractions."""

    component_ids: tuple[str, ...]
    molecular_weights_g_mol: tuple[float, ...]
    mole_fractions: tuple[float, ...]
    mass_fractions: tuple[float, ...]
    phase_label: str
    temperature_K: float
    pressure_Pa: float

    def __post_init__(self) -> None:
        if not self.component_ids:
            raise ValueError("Mixture must contain at least one component")
        if len(self.component_ids) != len(set(self.component_ids)):
            raise ValueError("Mixture component_ids must be unique")
        _validate_string_tuple(self.component_ids, "component_ids")
        if self.phase_label not in _VALID_PHASES:
            raise ValueError(f"Unsupported phase label: {self.phase_label}")
        n = len(self.component_ids)
        if (
            len(self.molecular_weights_g_mol) != n
            or len(self.mole_fractions) != n
            or len(self.mass_fractions) != n
        ):
            raise ValueError("Fraction vectors must match component_ids length")
        if any(value <= 0 for value in self.molecular_weights_g_mol):
            raise ValueError("molecular_weights_g_mol must be positive")
        _validate_fraction_vector(self.mole_fractions, "mole_fractions")
        _validate_fraction_vector(self.mass_fractions, "mass_fractions")
        if self.temperature_K <= 0:
            raise ValueError("temperature_K must be positive")
        if self.pressure_Pa <= 0:
            raise ValueError("pressure_Pa must be positive")

    @classmethod
    def from_mole_fractions(
        cls,
        components: Sequence[ComponentSpec],
        mole_fractions: Sequence[float],
        *,
        phase_label: str,
        temperature_K: float,
        pressure_Pa: float,
    ) -> MixtureSpec:
        _validate_component_phase_compatibility(components, phase_label)
        zs = _normalize_fractions(tuple(float(value) for value in mole_fractions))
        ws = mass_fractions_from_mole_fractions(components, zs)
        return cls(
            component_ids=tuple(component.identifier for component in components),
            molecular_weights_g_mol=tuple(_mw(component) for component in components),
            mole_fractions=zs,
            mass_fractions=ws,
            phase_label=phase_label,
            temperature_K=temperature_K,
            pressure_Pa=pressure_Pa,
        )

    @classmethod
    def from_mass_fractions(
        cls,
        components: Sequence[ComponentSpec],
        mass_fractions: Sequence[float],
        *,
        phase_label: str,
        temperature_K: float,
        pressure_Pa: float,
    ) -> MixtureSpec:
        _validate_component_phase_compatibility(components, phase_label)
        ws = _normalize_fractions(tuple(float(value) for value in mass_fractions))
        zs = mole_fractions_from_mass_fractions(components, ws)
        return cls(
            component_ids=tuple(component.identifier for component in components),
            molecular_weights_g_mol=tuple(_mw(component) for component in components),
            mole_fractions=zs,
            mass_fractions=ws,
            phase_label=phase_label,
            temperature_K=temperature_K,
            pressure_Pa=pressure_Pa,
        )

    @property
    def average_molecular_weight_g_mol(self) -> float:
        return sum(
            z * mw
            for z, mw in zip(
                self.mole_fractions,
                self.molecular_weights_g_mol,
                strict=True,
            )
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "component_ids": list(self.component_ids),
            "molecular_weights_g_mol": list(self.molecular_weights_g_mol),
            "mole_fractions": list(self.mole_fractions),
            "mass_fractions": list(self.mass_fractions),
            "phase_label": self.phase_label,
            "temperature_K": self.temperature_K,
            "pressure_Pa": self.pressure_Pa,
            "average_molecular_weight_g_mol": self.average_molecular_weight_g_mol,
            "units": {
                "temperature_K": "K",
                "pressure_Pa": "Pa",
                "average_molecular_weight_g_mol": "g/mol",
            },
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> MixtureSpec:
        return cls(
            component_ids=tuple(str(value) for value in payload["component_ids"]),
            molecular_weights_g_mol=tuple(
                float(value) for value in payload["molecular_weights_g_mol"]
            ),
            mole_fractions=tuple(float(value) for value in payload["mole_fractions"]),
            mass_fractions=tuple(float(value) for value in payload["mass_fractions"]),
            phase_label=str(payload["phase_label"]),
            temperature_K=float(payload["temperature_K"]),
            pressure_Pa=float(payload["pressure_Pa"]),
        )


@dataclass(frozen=True)
class PropertyCorrelation:
    """A portable property-correlation declaration with explicit units."""

    correlation_id: str
    equation_id: str
    coefficients: dict[str, float]
    input_units: dict[str, str]
    output_unit: str
    property_id: str = ""
    validity_ranges: dict[str, tuple[float, float]] = field(default_factory=dict)
    source_note: str = ""
    metadata: dict[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.correlation_id:
            raise ValueError("correlation_id cannot be empty")
        if self.correlation_id.strip() != self.correlation_id:
            raise ValueError("correlation_id cannot contain leading or trailing whitespace")
        if self.property_id and not self.property_id.replace("_", "").isalnum():
            raise ValueError(f"Invalid property_id: {self.property_id}")
        if not self.equation_id:
            raise ValueError("equation_id cannot be empty")
        if self.equation_id not in _EQUATION_CONTRACTS:
            raise ValueError(f"Unsupported property equation_id: {self.equation_id}")
        if not self.coefficients:
            raise ValueError("coefficients cannot be empty")
        _validate_coefficients(self.coefficients, self.equation_id)
        contract = _EQUATION_CONTRACTS[self.equation_id]
        output_spec = unit_spec(self.output_unit)
        expected_output_dimension = str(contract["output_dimension"])
        if output_spec.dimension != expected_output_dimension:
            raise ValueError(
                f"output_unit for {self.equation_id} must have dimension "
                f"{expected_output_dimension}, got {output_spec.dimension}"
            )
        input_dimensions = contract["input_dimensions"]
        if not isinstance(input_dimensions, dict):
            raise TypeError("Internal equation contract input_dimensions must be a mapping")
        for field_name, unit in self.input_units.items():
            if not field_name:
                raise ValueError("input unit field names cannot be empty")
            spec = unit_spec(unit)
            expected_dimension = input_dimensions.get(field_name)
            if expected_dimension is None:
                raise ValueError(
                    f"Unexpected input field {field_name!r} for equation {self.equation_id}"
                )
            if spec.dimension != expected_dimension:
                raise ValueError(
                    f"input_units[{field_name!r}] must have dimension "
                    f"{expected_dimension}, got {spec.dimension}"
                )
        for required_field in input_dimensions:
            if required_field not in self.input_units:
                raise ValueError(
                    f"Missing input unit for field {required_field!r} on {self.equation_id}"
                )
        for variable, bounds in self.validity_ranges.items():
            if variable not in input_dimensions:
                raise ValueError(
                    f"Validity range field {variable!r} is not an input of {self.equation_id}"
                )
            if len(bounds) != 2:
                raise ValueError(f"Validity range must have two values: {variable}")
            lower, upper = bounds
            if lower >= upper:
                raise ValueError(f"Invalid validity range for {variable}: {bounds}")
        object.__setattr__(self, "coefficients", dict(self.coefficients))
        object.__setattr__(self, "input_units", dict(self.input_units))
        object.__setattr__(self, "validity_ranges", dict(self.validity_ranges))
        object.__setattr__(self, "metadata", dict(self.metadata))

    def to_dict(self) -> dict[str, object]:
        return {
            "correlation_id": self.correlation_id,
            "property_id": self.property_id,
            "equation_id": self.equation_id,
            "coefficients": dict(self.coefficients),
            "input_units": dict(self.input_units),
            "output_unit": self.output_unit,
            "validity_ranges": {
                key: list(value) for key, value in self.validity_ranges.items()
            },
            "source_note": self.source_note,
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> PropertyCorrelation:
        return cls(
            correlation_id=str(payload["correlation_id"]),
            equation_id=str(payload["equation_id"]),
            coefficients={
                str(key): float(value)
                for key, value in dict(payload["coefficients"]).items()
            },
            input_units={
                str(key): str(value)
                for key, value in dict(payload["input_units"]).items()
            },
            output_unit=str(payload["output_unit"]),
            property_id=str(payload.get("property_id", "")),
            validity_ranges={
                str(key): (float(value[0]), float(value[1]))
                for key, value in dict(payload.get("validity_ranges", {})).items()
            },
            source_note=str(payload.get("source_note", "")),
            metadata=dict(payload.get("metadata", {})),
        )

    def model_card(self) -> dict[str, object]:
        output = unit_spec(self.output_unit)
        required = _required_coefficients(self.equation_id)
        return {
            "correlation_id": self.correlation_id,
            "property_id": self.property_id,
            "equation_id": self.equation_id,
            "required_coefficients": sorted(required),
            "input_units": dict(self.input_units),
            "output_unit": self.output_unit,
            "output_dimension": output.dimension,
            "validity_ranges": {
                key: list(value) for key, value in self.validity_ranges.items()
            },
            "source_note": self.source_note,
            "metadata": dict(self.metadata),
        }


def mass_fractions_from_mole_fractions(
    components: Sequence[ComponentSpec],
    mole_fractions: Sequence[float],
) -> tuple[float, ...]:
    _validate_component_fraction_lengths(components, mole_fractions)
    zs = _normalize_fractions(tuple(float(value) for value in mole_fractions))
    weighted = tuple(z * _mw(component) for component, z in zip(components, zs, strict=True))
    total = sum(weighted)
    if total <= 0:
        raise ValueError("Mixture molecular weight denominator must be positive")
    return tuple(value / total for value in weighted)


def mole_fractions_from_mass_fractions(
    components: Sequence[ComponentSpec],
    mass_fractions: Sequence[float],
) -> tuple[float, ...]:
    _validate_component_fraction_lengths(components, mass_fractions)
    ws = _normalize_fractions(tuple(float(value) for value in mass_fractions))
    weighted = tuple(w / _mw(component) for component, w in zip(components, ws, strict=True))
    total = sum(weighted)
    if total <= 0:
        raise ValueError("Mixture mole-fraction denominator must be positive")
    return tuple(value / total for value in weighted)


def _mw(component: ComponentSpec) -> float:
    assert component.molecular_weight_g_mol is not None
    return component.molecular_weight_g_mol


def _validate_component_fraction_lengths(
    components: Sequence[ComponentSpec],
    fractions: Sequence[float],
) -> None:
    if not components:
        raise ValueError("At least one component is required")
    if len(components) != len(fractions):
        raise ValueError("components and fractions must have the same length")


def _validate_fraction_vector(fractions: tuple[float, ...], name: str) -> None:
    if any(value < 0 for value in fractions):
        raise ValueError(f"{name} cannot contain negative values")
    if abs(sum(fractions) - 1.0) > _FRACTION_TOL:
        raise ValueError(f"{name} must sum to 1")


def _normalize_fractions(fractions: tuple[float, ...]) -> tuple[float, ...]:
    if any(value < 0 for value in fractions):
        raise ValueError("Fractions cannot be negative")
    total = sum(fractions)
    if total <= 0:
        raise ValueError("Fraction total must be positive")
    return tuple(value / total for value in fractions)


def _validate_string_tuple(values: Sequence[str], field_name: str) -> None:
    seen: set[str] = set()
    for value in values:
        if not isinstance(value, str):
            raise ValueError(f"{field_name} values must be strings")
        if not value or value.strip() != value:
            raise ValueError(f"{field_name} values cannot be empty or padded")
        if value in seen:
            raise ValueError(f"{field_name} values must be unique")
        seen.add(value)


def _validate_component_phase_compatibility(
    components: Sequence[ComponentSpec],
    phase_label: str,
) -> None:
    allowed = _PHASE_COMPATIBILITY[phase_label]
    incompatible = [
        component.identifier
        for component in components
        if component.default_phase not in allowed
    ]
    if incompatible:
        raise ValueError(
            f"Components are not compatible with phase {phase_label!r}: {incompatible}"
        )


def _validate_coefficients(coefficients: dict[str, float], equation_id: str) -> None:
    required = _required_coefficients(equation_id)
    missing = sorted(required - set(coefficients))
    if missing:
        raise ValueError(f"Missing coefficients for {equation_id}: {missing}")
    for key, value in coefficients.items():
        if not isinstance(value, int | float):
            raise ValueError(f"Coefficient {key!r} must be numeric")
        if not isfinite(float(value)):
            raise ValueError(f"Coefficient {key!r} must be finite")


def _required_coefficients(equation_id: str) -> set[str]:
    required = _EQUATION_CONTRACTS[equation_id]["required_coefficients"]
    if not isinstance(required, set):
        raise TypeError("Internal equation contract required_coefficients must be a set")
    return {str(value) for value in required}


def property_equation_contracts() -> dict[str, dict[str, object]]:
    """Return JSON-friendly contracts for supported property equations."""

    contracts: dict[str, dict[str, object]] = {}
    for equation_id, contract in _EQUATION_CONTRACTS.items():
        input_dimensions = contract["input_dimensions"]
        if not isinstance(input_dimensions, dict):
            raise TypeError("Internal equation contract input_dimensions must be a mapping")
        contracts[equation_id] = {
            "required_coefficients": sorted(_required_coefficients(equation_id)),
            "input_dimensions": {
                str(field): str(dimension)
                for field, dimension in input_dimensions.items()
            },
            "output_dimension": str(contract["output_dimension"]),
        }
    return contracts


def supported_property_equations() -> tuple[str, ...]:
    """Return stable equation identifiers accepted by `PropertyCorrelation`."""

    return tuple(sorted(_EQUATION_CONTRACTS))


__all__ = [
    "ComponentSpec",
    "MixtureSpec",
    "PropertyCorrelation",
    "mass_fractions_from_mole_fractions",
    "mole_fractions_from_mass_fractions",
    "property_equation_contracts",
    "supported_property_equations",
]
