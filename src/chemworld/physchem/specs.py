"""JSON-friendly component, mixture, and property-correlation specs."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field

from chemworld.foundation.units import canonical_unit
from chemworld.physchem.elements import (
    hill_formula,
    mass_fractions_from_formula,
    molecular_weight,
    parse_formula,
)

_VALID_PHASES = {"gas", "liquid", "solid", "aqueous", "organic", "unknown"}
_FRACTION_TOL = 1e-9


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

    def __post_init__(self) -> None:
        if not self.identifier:
            raise ValueError("Component identifier cannot be empty")
        if self.default_phase not in _VALID_PHASES:
            raise ValueError(f"Unsupported default phase: {self.default_phase}")
        composition = parse_formula(self.formula)
        calculated_mw = molecular_weight(composition)
        if self.molecular_weight_g_mol is None:
            object.__setattr__(self, "molecular_weight_g_mol", calculated_mw)
        elif self.molecular_weight_g_mol <= 0:
            raise ValueError("molecular_weight_g_mol must be positive")
        object.__setattr__(self, "safety_tags", tuple(self.safety_tags))
        object.__setattr__(
            self,
            "allowed_property_correlations",
            tuple(self.allowed_property_correlations),
        )
        object.__setattr__(self, "aliases", tuple(self.aliases))

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

    def __post_init__(self) -> None:
        if not self.correlation_id:
            raise ValueError("correlation_id cannot be empty")
        if self.property_id and not self.property_id.replace("_", "").isalnum():
            raise ValueError(f"Invalid property_id: {self.property_id}")
        if not self.equation_id:
            raise ValueError("equation_id cannot be empty")
        if not self.coefficients:
            raise ValueError("coefficients cannot be empty")
        canonical_unit(self.output_unit)
        for field_name, unit in self.input_units.items():
            if not field_name:
                raise ValueError("input unit field names cannot be empty")
            canonical_unit(unit)
        for variable, bounds in self.validity_ranges.items():
            if len(bounds) != 2:
                raise ValueError(f"Validity range must have two values: {variable}")
            lower, upper = bounds
            if lower >= upper:
                raise ValueError(f"Invalid validity range for {variable}: {bounds}")

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
