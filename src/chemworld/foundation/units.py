"""Lightweight canonical unit system for JSON-friendly benchmark state."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class UnitSpec:
    """A supported physical unit and its canonical dimension."""

    unit: str
    dimension: str
    canonical_unit: str


@dataclass(frozen=True)
class Quantity:
    value: float
    unit: str

    def to(self, target_unit: str) -> Quantity:
        return Quantity(convert_value(self.value, self.unit, target_unit), target_unit)

    def to_dict(self) -> dict[str, float | str]:
        return {"value": self.value, "unit": self.unit}


_UNIT_TABLE: dict[str, tuple[str, str, float, float]] = {
    "K": ("temperature", "K", 1.0, 0.0),
    "degC": ("temperature", "K", 1.0, 273.15),
    "s": ("time", "s", 1.0, 0.0),
    "min": ("time", "s", 60.0, 0.0),
    "h": ("time", "s", 3600.0, 0.0),
    "L": ("volume", "L", 1.0, 0.0),
    "mL": ("volume", "L", 0.001, 0.0),
    "mol": ("amount", "mol", 1.0, 0.0),
    "mmol": ("amount", "mol", 0.001, 0.0),
    "mol/L": ("concentration", "mol/L", 1.0, 0.0),
    "J": ("energy", "J", 1.0, 0.0),
    "kJ": ("energy", "J", 1000.0, 0.0),
    "Pa": ("pressure", "Pa", 1.0, 0.0),
    "bar": ("pressure", "Pa", 100000.0, 0.0),
    "currency": ("cost", "currency", 1.0, 0.0),
    "risk": ("risk", "risk", 1.0, 0.0),
    "dimensionless": ("dimensionless", "dimensionless", 1.0, 0.0),
}


def unit_spec(unit: str) -> UnitSpec:
    if unit not in _UNIT_TABLE:
        raise ValueError(f"Unsupported unit: {unit}")
    dimension, canonical_unit, _, _ = _UNIT_TABLE[unit]
    return UnitSpec(unit=unit, dimension=dimension, canonical_unit=canonical_unit)


def canonical_unit(unit: str) -> str:
    return unit_spec(unit).canonical_unit


def convert_value(value: float, source_unit: str, target_unit: str) -> float:
    """Convert between supported units with affine temperature handling."""

    if source_unit not in _UNIT_TABLE:
        raise ValueError(f"Unsupported source unit: {source_unit}")
    if target_unit not in _UNIT_TABLE:
        raise ValueError(f"Unsupported target unit: {target_unit}")

    source_dimension, _, source_scale, source_offset = _UNIT_TABLE[source_unit]
    target_dimension, _, target_scale, target_offset = _UNIT_TABLE[target_unit]
    if source_dimension != target_dimension:
        raise ValueError(f"Cannot convert {source_unit} to {target_unit}")

    canonical_value = value * source_scale + source_offset
    return (canonical_value - target_offset) / target_scale


def supported_units() -> dict[str, UnitSpec]:
    return {unit: unit_spec(unit) for unit in sorted(_UNIT_TABLE)}

