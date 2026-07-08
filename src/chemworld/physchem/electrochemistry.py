"""Electrochemical thermodynamics and charge-accounting kernels.

This module implements a compact, auditable electrochemistry core for the
shared ChemWorld law.  The sign convention follows the usual electrode-kinetics
form: positive overpotential gives positive anodic Butler-Volmer current, while
negative overpotential gives cathodic current.  Benchmark conversion uses the
absolute Faradaic charge because the virtual task tracks extent, selectivity,
and energy accounting rather than electrode polarity.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from math import exp, isfinite, log
from typing import Any

from chemworld.physchem.electrochemistry_cards import electrochemistry_model_cards
from chemworld.physchem.reaction_network import R_J_PER_MOL_K

FARADAY_C_PER_MOL = 96485.33212
_ACTIVITY_FLOOR = 1.0e-30
_EXPONENT_LIMIT = 80.0


@dataclass(frozen=True)
class ElectrodeReactionSpec:
    """Single electrode reaction contract.

    ``reaction_quotient_exponents`` stores the stoichiometric exponents used in
    ``Q = prod(activity_i ** exponent_i)``.  For a reduction-like virtual
    conversion ``A -> P``, use ``{"P": 1, "A": -1}``.
    """

    reaction_id: str
    electrons_transferred: float
    standard_potential_V: float
    reaction_quotient_exponents: dict[str, float]
    exchange_current_density_A_m2: float
    electrode_area_m2: float
    alpha_anodic: float = 0.5
    alpha_cathodic: float = 0.5
    faradaic_efficiency_ref: float = 0.90
    product_selectivity_ref: float = 0.88
    overpotential_selectivity_sensitivity_V_inv: float = 0.55
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.reaction_id.strip():
            raise ValueError("reaction_id cannot be empty")
        _positive(self.electrons_transferred, "electrons_transferred")
        _finite(self.standard_potential_V, "standard_potential_V")
        if not self.reaction_quotient_exponents:
            raise ValueError("reaction_quotient_exponents cannot be empty")
        for key, value in self.reaction_quotient_exponents.items():
            if not key.strip():
                raise ValueError("reaction quotient species ids cannot be empty")
            _finite(value, f"reaction_quotient_exponents[{key!r}]")
            if value == 0.0:
                raise ValueError("reaction quotient exponents cannot be zero")
        _nonnegative(self.exchange_current_density_A_m2, "exchange_current_density_A_m2")
        _positive(self.electrode_area_m2, "electrode_area_m2")
        _positive(self.alpha_anodic, "alpha_anodic")
        _positive(self.alpha_cathodic, "alpha_cathodic")
        _fraction(self.faradaic_efficiency_ref, "faradaic_efficiency_ref")
        _fraction(self.product_selectivity_ref, "product_selectivity_ref")
        _nonnegative(
            self.overpotential_selectivity_sensitivity_V_inv,
            "overpotential_selectivity_sensitivity_V_inv",
        )

    @property
    def exchange_current_a(self) -> float:
        return self.exchange_current_density_A_m2 * self.electrode_area_m2

    def to_dict(self) -> dict[str, Any]:
        return {
            "reaction_id": self.reaction_id,
            "electrons_transferred": self.electrons_transferred,
            "standard_potential_V": self.standard_potential_V,
            "reaction_quotient_exponents": dict(self.reaction_quotient_exponents),
            "exchange_current_density_A_m2": self.exchange_current_density_A_m2,
            "electrode_area_m2": self.electrode_area_m2,
            "exchange_current_A": self.exchange_current_a,
            "alpha_anodic": self.alpha_anodic,
            "alpha_cathodic": self.alpha_cathodic,
            "faradaic_efficiency_ref": self.faradaic_efficiency_ref,
            "product_selectivity_ref": self.product_selectivity_ref,
            "overpotential_selectivity_sensitivity_V_inv": (
                self.overpotential_selectivity_sensitivity_V_inv
            ),
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True)
class ElectrolysisResult:
    """Terminal electrolysis accounting for one operation."""

    reaction_id: str
    equilibrium_potential_V: float
    overpotential_V: float
    kinetic_current_A: float
    actual_current_A: float
    charge_C: float
    faradaic_charge_C: float
    extent_mol: float
    converted_mol: float
    product_mol: float
    byproduct_mol: float
    faradaic_efficiency: float
    product_selectivity: float
    electrical_work_J: float
    reversible_work_J: float
    energy_efficiency: float
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "reaction_id": self.reaction_id,
            "equilibrium_potential_V": self.equilibrium_potential_V,
            "overpotential_V": self.overpotential_V,
            "kinetic_current_A": self.kinetic_current_A,
            "actual_current_A": self.actual_current_A,
            "charge_C": self.charge_C,
            "faradaic_charge_C": self.faradaic_charge_C,
            "extent_mol": self.extent_mol,
            "converted_mol": self.converted_mol,
            "product_mol": self.product_mol,
            "byproduct_mol": self.byproduct_mol,
            "faradaic_efficiency": self.faradaic_efficiency,
            "product_selectivity": self.product_selectivity,
            "electrical_work_J": self.electrical_work_J,
            "reversible_work_J": self.reversible_work_J,
            "energy_efficiency": self.energy_efficiency,
            "metadata": dict(self.metadata),
        }


def reaction_quotient_from_activities(
    activities: dict[str, float],
    exponents: dict[str, float],
) -> float:
    """Return ``Q`` from dimensionless activities and stoichiometric exponents."""

    log_q = reaction_quotient_log_from_activities(activities, exponents)
    return exp(_clamp(log_q, -_EXPONENT_LIMIT, _EXPONENT_LIMIT))


def reaction_quotient_log_from_activities(
    activities: dict[str, float],
    exponents: dict[str, float],
) -> float:
    """Return ``ln(Q)`` with a positive activity floor."""

    if not exponents:
        raise ValueError("exponents cannot be empty")
    total = 0.0
    for species_id, exponent in exponents.items():
        _finite(exponent, f"exponent[{species_id!r}]")
        activity = max(float(activities.get(species_id, _ACTIVITY_FLOOR)), _ACTIVITY_FLOOR)
        total += exponent * log(activity)
    return total


def equilibrium_potential_from_delta_g(
    *,
    delta_g_reaction_J_mol: float,
    electrons_transferred: float,
) -> float:
    """Return ``E_eq = -Delta G_rxn / (n F)`` in volts."""

    _finite(delta_g_reaction_J_mol, "delta_g_reaction_J_mol")
    _positive(electrons_transferred, "electrons_transferred")
    return -delta_g_reaction_J_mol / (electrons_transferred * FARADAY_C_PER_MOL)


def nernst_potential(
    spec: ElectrodeReactionSpec,
    activities: dict[str, float],
    *,
    temperature_K: float = 298.15,
) -> float:
    """Return the Nernst equilibrium potential for an electrode reaction."""

    _positive(temperature_K, "temperature_K")
    log_q = reaction_quotient_log_from_activities(
        activities,
        spec.reaction_quotient_exponents,
    )
    return spec.standard_potential_V - (
        R_J_PER_MOL_K * temperature_K / (spec.electrons_transferred * FARADAY_C_PER_MOL)
    ) * log_q


def butler_volmer_current(
    spec: ElectrodeReactionSpec,
    *,
    electrode_potential_V: float,
    activities: dict[str, float],
    temperature_K: float = 298.15,
) -> float:
    """Return signed Butler-Volmer current in amperes."""

    _finite(electrode_potential_V, "electrode_potential_V")
    _positive(temperature_K, "temperature_K")
    equilibrium_potential = nernst_potential(spec, activities, temperature_K=temperature_K)
    overpotential = electrode_potential_V - equilibrium_potential
    coefficient = spec.electrons_transferred * FARADAY_C_PER_MOL / (
        R_J_PER_MOL_K * temperature_K
    )
    anodic = exp(
        _clamp(
            spec.alpha_anodic * coefficient * overpotential,
            -_EXPONENT_LIMIT,
            _EXPONENT_LIMIT,
        )
    )
    cathodic = exp(
        _clamp(
            -spec.alpha_cathodic * coefficient * overpotential,
            -_EXPONENT_LIMIT,
            _EXPONENT_LIMIT,
        )
    )
    return spec.exchange_current_a * (anodic - cathodic)


def faradaic_extent_mol(
    *,
    current_A: float,
    duration_s: float,
    electrons_transferred: float,
    faradaic_efficiency: float = 1.0,
) -> float:
    """Convert electrical charge to reaction extent through Faraday's law."""

    _finite(current_A, "current_A")
    _nonnegative(duration_s, "duration_s")
    _positive(electrons_transferred, "electrons_transferred")
    _fraction(faradaic_efficiency, "faradaic_efficiency")
    charge_C = abs(current_A) * duration_s
    return charge_C * faradaic_efficiency / (electrons_transferred * FARADAY_C_PER_MOL)


def run_electrolysis(
    spec: ElectrodeReactionSpec,
    *,
    electrode_potential_V: float,
    duration_s: float,
    activities: dict[str, float],
    available_substrate_mol: float,
    temperature_K: float = 298.15,
    applied_current_A: float | None = None,
) -> ElectrolysisResult:
    """Run a terminal electrolysis accounting step.

    The kinetic Butler-Volmer current sets the sign and kinetic upper bound.  If
    ``applied_current_A`` is provided, the actual current magnitude is capped by
    the kinetic current magnitude, approximating a finite cell/power-supply
    constraint without solving a full coupled electrochemical cell.
    """

    _finite(electrode_potential_V, "electrode_potential_V")
    _nonnegative(duration_s, "duration_s")
    _nonnegative(available_substrate_mol, "available_substrate_mol")
    _positive(temperature_K, "temperature_K")
    if applied_current_A is not None:
        _finite(applied_current_A, "applied_current_A")

    equilibrium_potential = nernst_potential(spec, activities, temperature_K=temperature_K)
    overpotential = electrode_potential_V - equilibrium_potential
    kinetic_current = butler_volmer_current(
        spec,
        electrode_potential_V=electrode_potential_V,
        activities=activities,
        temperature_K=temperature_K,
    )
    kinetic_magnitude = abs(kinetic_current)
    if applied_current_A is None:
        actual_current = kinetic_current
    else:
        requested_magnitude = abs(applied_current_A)
        actual_magnitude = min(requested_magnitude, kinetic_magnitude)
        sign_source = kinetic_current if kinetic_magnitude > 0.0 else applied_current_A
        actual_current = _copy_sign(actual_magnitude, sign_source)

    overpotential_stress = max(abs(overpotential) - 0.15, 0.0)
    faradaic_efficiency = _clip01(
        spec.faradaic_efficiency_ref
        * exp(-spec.overpotential_selectivity_sensitivity_V_inv * overpotential_stress)
    )
    product_selectivity = _clip01(
        spec.product_selectivity_ref
        * exp(-0.5 * spec.overpotential_selectivity_sensitivity_V_inv * overpotential_stress)
    )
    extent = faradaic_extent_mol(
        current_A=actual_current,
        duration_s=duration_s,
        electrons_transferred=spec.electrons_transferred,
        faradaic_efficiency=faradaic_efficiency,
    )
    converted = min(available_substrate_mol, extent)
    product_mol = converted * product_selectivity
    byproduct_mol = converted - product_mol
    charge = abs(actual_current) * duration_s
    faradaic_charge = charge * faradaic_efficiency
    electrical_work = abs(electrode_potential_V * actual_current * duration_s)
    reversible_work = min(
        abs(equilibrium_potential) * faradaic_charge,
        electrical_work,
    )
    energy_efficiency = 0.0
    if electrical_work > 0.0:
        energy_efficiency = _clip01((reversible_work / electrical_work) * product_selectivity)
    return ElectrolysisResult(
        reaction_id=spec.reaction_id,
        equilibrium_potential_V=equilibrium_potential,
        overpotential_V=overpotential,
        kinetic_current_A=kinetic_current,
        actual_current_A=actual_current,
        charge_C=charge,
        faradaic_charge_C=faradaic_charge,
        extent_mol=extent,
        converted_mol=converted,
        product_mol=product_mol,
        byproduct_mol=byproduct_mol,
        faradaic_efficiency=faradaic_efficiency,
        product_selectivity=product_selectivity,
        electrical_work_J=electrical_work,
        reversible_work_J=reversible_work,
        energy_efficiency=energy_efficiency,
        metadata={
            "model_id": "nernst_butler_volmer_faradaic_v1",
            "temperature_K": temperature_K,
            "applied_current_A": applied_current_A,
            "kinetic_current_limited": (
                applied_current_A is not None and abs(applied_current_A) > kinetic_magnitude
            ),
        },
    )


def _finite(value: float, name: str) -> None:
    if not isfinite(value):
        raise ValueError(f"{name} must be finite")


def _positive(value: float, name: str) -> None:
    _finite(value, name)
    if value <= 0.0:
        raise ValueError(f"{name} must be positive")


def _nonnegative(value: float, name: str) -> None:
    _finite(value, name)
    if value < 0.0:
        raise ValueError(f"{name} must be nonnegative")


def _fraction(value: float, name: str) -> None:
    _finite(value, name)
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must be between 0 and 1")


def _clip01(value: float) -> float:
    return max(0.0, min(1.0, value))


def _clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def _copy_sign(magnitude: float, sign_source: float) -> float:
    if sign_source < 0.0:
        return -magnitude
    return magnitude


__all__ = [
    "FARADAY_C_PER_MOL",
    "ElectrodeReactionSpec",
    "ElectrolysisResult",
    "butler_volmer_current",
    "electrochemistry_model_cards",
    "equilibrium_potential_from_delta_g",
    "faradaic_extent_mol",
    "nernst_potential",
    "reaction_quotient_from_activities",
    "reaction_quotient_log_from_activities",
    "run_electrolysis",
]
