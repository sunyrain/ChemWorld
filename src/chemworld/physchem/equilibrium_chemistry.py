"""Reaction-equilibrium, electrolyte, and precipitation kernels for ChemWorld."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from itertools import pairwise
from math import exp, isfinite, log, log10
from typing import Literal

import numpy as np
from scipy.optimize import brentq, least_squares

from chemworld.physchem.reaction_network import R_J_PER_MOL_K, parse_reaction_equation

EquilibriumActivityModel = Literal["concentration"]
_ACTIVITY_FLOOR = 1e-30


@dataclass(frozen=True)
class EquilibriumReactionSpec:
    """Mass-action equilibrium reaction with van't Hoff temperature dependence."""

    reaction_id: str
    stoichiometry: dict[str, float]
    log10_k_ref: float
    reference_temperature_K: float = 298.15
    delta_h_J_mol: float = 0.0
    activity_model: EquilibriumActivityModel = "concentration"
    metadata: dict[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.reaction_id:
            raise ValueError("reaction_id cannot be empty")
        if not self.stoichiometry:
            raise ValueError("stoichiometry cannot be empty")
        if not any(value < 0.0 for value in self.stoichiometry.values()):
            raise ValueError("equilibrium reaction must contain at least one reactant")
        if not any(value > 0.0 for value in self.stoichiometry.values()):
            raise ValueError("equilibrium reaction must contain at least one product")
        if any(not isfinite(value) or value == 0.0 for value in self.stoichiometry.values()):
            raise ValueError("stoichiometric coefficients must be finite and nonzero")
        _finite(self.log10_k_ref, "log10_k_ref")
        _positive(self.reference_temperature_K, "reference_temperature_K")
        _finite(self.delta_h_J_mol, "delta_h_J_mol")
        if self.activity_model != "concentration":
            raise ValueError(f"Unsupported activity model: {self.activity_model}")

    @classmethod
    def from_equation(
        cls,
        *,
        reaction_id: str,
        equation: str,
        log10_k_ref: float,
        reference_temperature_K: float = 298.15,
        delta_h_J_mol: float = 0.0,
        metadata: dict[str, object] | None = None,
    ) -> EquilibriumReactionSpec:
        stoichiometry, _ = parse_reaction_equation(equation)
        return cls(
            reaction_id=reaction_id,
            stoichiometry=stoichiometry,
            log10_k_ref=log10_k_ref,
            reference_temperature_K=reference_temperature_K,
            delta_h_J_mol=delta_h_J_mol,
            metadata={} if metadata is None else dict(metadata),
        )

    def equilibrium_constant(self, temperature_K: float) -> float:
        return equilibrium_constant_vant_hoff(
            log10_k_ref=self.log10_k_ref,
            temperature_K=temperature_K,
            reference_temperature_K=self.reference_temperature_K,
            delta_h_J_mol=self.delta_h_J_mol,
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "reaction_id": self.reaction_id,
            "stoichiometry": dict(self.stoichiometry),
            "log10_k_ref": self.log10_k_ref,
            "reference_temperature_K": self.reference_temperature_K,
            "delta_h_J_mol": self.delta_h_J_mol,
            "activity_model": self.activity_model,
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True)
class EquilibriumSystemSpec:
    """A compact equilibrium problem at fixed T, P, and volume."""

    system_id: str
    reactions: tuple[EquilibriumReactionSpec, ...]
    temperature_K: float = 298.15
    pressure_Pa: float = 101_325.0
    volume_L: float = 1.0
    metadata: dict[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.system_id:
            raise ValueError("system_id cannot be empty")
        if not self.reactions:
            raise ValueError("Equilibrium system must contain at least one reaction")
        reaction_ids = [reaction.reaction_id for reaction in self.reactions]
        if len(reaction_ids) != len(set(reaction_ids)):
            raise ValueError("Duplicate reaction_id values are not allowed")
        _positive(self.temperature_K, "temperature_K")
        _positive(self.pressure_Pa, "pressure_Pa")
        _positive(self.volume_L, "volume_L")

    @property
    def species_ids(self) -> tuple[str, ...]:
        ids = sorted({key for reaction in self.reactions for key in reaction.stoichiometry})
        return tuple(ids)

    def to_dict(self) -> dict[str, object]:
        return {
            "system_id": self.system_id,
            "reactions": [reaction.to_dict() for reaction in self.reactions],
            "temperature_K": self.temperature_K,
            "pressure_Pa": self.pressure_Pa,
            "volume_L": self.volume_L,
            "species_ids": list(self.species_ids),
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True)
class EquilibriumResult:
    """Solved reaction-equilibrium state."""

    system_id: str
    initial_amounts_mol: dict[str, float]
    final_amounts_mol: dict[str, float]
    extents_mol: dict[str, float]
    equilibrium_constants: dict[str, float]
    reaction_quotients: dict[str, float]
    residuals_log: dict[str, float]
    converged: bool
    iterations: int
    metadata: dict[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.system_id:
            raise ValueError("system_id cannot be empty")
        _validate_amounts(self.initial_amounts_mol, "initial_amounts_mol")
        _validate_amounts(self.final_amounts_mol, "final_amounts_mol")
        if any(not isfinite(value) for value in self.extents_mol.values()):
            raise ValueError("extents must be finite")
        if any(
            value <= 0.0 or not isfinite(value)
            for value in self.equilibrium_constants.values()
        ):
            raise ValueError("equilibrium constants must be positive and finite")
        if any(value <= 0.0 or not isfinite(value) for value in self.reaction_quotients.values()):
            raise ValueError("reaction quotients must be positive and finite")
        if any(not isfinite(value) for value in self.residuals_log.values()):
            raise ValueError("residuals must be finite")
        if self.iterations < 0:
            raise ValueError("iterations cannot be negative")

    def conversion(self, species_id: str) -> float:
        initial = self.initial_amounts_mol.get(species_id, 0.0)
        if initial <= 0.0:
            return 0.0
        return _clip01((initial - self.final_amounts_mol.get(species_id, 0.0)) / initial)

    def to_dict(self) -> dict[str, object]:
        return {
            "system_id": self.system_id,
            "initial_amounts_mol": dict(self.initial_amounts_mol),
            "final_amounts_mol": dict(self.final_amounts_mol),
            "extents_mol": dict(self.extents_mol),
            "equilibrium_constants": dict(self.equilibrium_constants),
            "reaction_quotients": dict(self.reaction_quotients),
            "residuals_log": dict(self.residuals_log),
            "converged": self.converged,
            "iterations": self.iterations,
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True)
class AcidBaseResult:
    """Monoprotic acid/base equilibrium in water."""

    species_amounts_mol: dict[str, float]
    pH: float
    pOH: float
    hydrogen_mol_L: float
    hydroxide_mol_L: float
    acid_dissociation_fraction: float
    charge_balance_error_eq: float
    ionic_strength_mol_kg: float
    metadata: dict[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _validate_amounts(self.species_amounts_mol, "species_amounts_mol")
        _finite(self.pH, "pH")
        _finite(self.pOH, "pOH")
        _positive(self.hydrogen_mol_L, "hydrogen_mol_L")
        _positive(self.hydroxide_mol_L, "hydroxide_mol_L")
        if not 0.0 <= self.acid_dissociation_fraction <= 1.0:
            raise ValueError("acid_dissociation_fraction must be between 0 and 1")
        _finite(self.charge_balance_error_eq, "charge_balance_error_eq")
        _nonnegative(self.ionic_strength_mol_kg, "ionic_strength_mol_kg")

    def to_dict(self) -> dict[str, object]:
        return {
            "species_amounts_mol": dict(self.species_amounts_mol),
            "pH": self.pH,
            "pOH": self.pOH,
            "hydrogen_mol_L": self.hydrogen_mol_L,
            "hydroxide_mol_L": self.hydroxide_mol_L,
            "acid_dissociation_fraction": self.acid_dissociation_fraction,
            "charge_balance_error_eq": self.charge_balance_error_eq,
            "ionic_strength_mol_kg": self.ionic_strength_mol_kg,
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True)
class SolubilityProductSpec:
    """Binary salt solubility-product model."""

    precipitate_id: str
    cation_id: str
    anion_id: str
    ksp: float
    cation_stoich: float = 1.0
    anion_stoich: float = 1.0
    metadata: dict[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.precipitate_id:
            raise ValueError("precipitate_id cannot be empty")
        if not self.cation_id or not self.anion_id:
            raise ValueError("ion ids cannot be empty")
        _positive(self.ksp, "ksp")
        _positive(self.cation_stoich, "cation_stoich")
        _positive(self.anion_stoich, "anion_stoich")

    def to_dict(self) -> dict[str, object]:
        return {
            "precipitate_id": self.precipitate_id,
            "cation_id": self.cation_id,
            "anion_id": self.anion_id,
            "ksp": self.ksp,
            "cation_stoich": self.cation_stoich,
            "anion_stoich": self.anion_stoich,
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True)
class PrecipitationResult:
    """Precipitation or dissolution proxy result."""

    final_amounts_mol: dict[str, float]
    precipitated_mol: float
    ion_product: float
    saturation_index: float
    material_balance_error_mol: float
    metadata: dict[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _validate_amounts(self.final_amounts_mol, "final_amounts_mol")
        _nonnegative(self.precipitated_mol, "precipitated_mol")
        _nonnegative(self.ion_product, "ion_product")
        _finite(self.saturation_index, "saturation_index")
        _nonnegative(self.material_balance_error_mol, "material_balance_error_mol")

    def to_dict(self) -> dict[str, object]:
        return {
            "final_amounts_mol": dict(self.final_amounts_mol),
            "precipitated_mol": self.precipitated_mol,
            "ion_product": self.ion_product,
            "saturation_index": self.saturation_index,
            "material_balance_error_mol": self.material_balance_error_mol,
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True)
class ChargeBalanceResult:
    """Electroneutrality adjustment result."""

    adjusted_amounts_mol: dict[str, float]
    initial_charge_eq: float
    final_charge_eq: float
    adjustment_mol: float
    adjusted_species_id: str
    metadata: dict[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _validate_amounts(self.adjusted_amounts_mol, "adjusted_amounts_mol")
        _finite(self.initial_charge_eq, "initial_charge_eq")
        _finite(self.final_charge_eq, "final_charge_eq")
        _finite(self.adjustment_mol, "adjustment_mol")
        if not self.adjusted_species_id:
            raise ValueError("adjusted_species_id cannot be empty")

    def to_dict(self) -> dict[str, object]:
        return {
            "adjusted_amounts_mol": dict(self.adjusted_amounts_mol),
            "initial_charge_eq": self.initial_charge_eq,
            "final_charge_eq": self.final_charge_eq,
            "adjustment_mol": self.adjustment_mol,
            "adjusted_species_id": self.adjusted_species_id,
            "metadata": dict(self.metadata),
        }


def equilibrium_constant_vant_hoff(
    *,
    log10_k_ref: float,
    temperature_K: float,
    reference_temperature_K: float = 298.15,
    delta_h_J_mol: float = 0.0,
) -> float:
    """Return K(T) from a reference K and reaction enthalpy."""

    _finite(log10_k_ref, "log10_k_ref")
    _positive(temperature_K, "temperature_K")
    _positive(reference_temperature_K, "reference_temperature_K")
    _finite(delta_h_J_mol, "delta_h_J_mol")
    ln_k_ref = log(10.0) * log10_k_ref
    ln_k = ln_k_ref - delta_h_J_mol / R_J_PER_MOL_K * (
        1.0 / temperature_K - 1.0 / reference_temperature_K
    )
    return exp(ln_k)


def reaction_extent_bounds(
    reaction: EquilibriumReactionSpec,
    initial_amounts_mol: Mapping[str, float],
) -> tuple[float, float]:
    """Return scalar extent bounds that preserve nonnegative amounts."""

    initial = _amounts(initial_amounts_mol)
    lower = -float("inf")
    upper = float("inf")
    for species_id, coefficient in reaction.stoichiometry.items():
        amount = initial.get(species_id, 0.0)
        if coefficient > 0.0:
            lower = max(lower, -amount / coefficient)
        elif coefficient < 0.0:
            upper = min(upper, amount / -coefficient)
    if lower == -float("inf"):
        lower = 0.0
    if upper == float("inf"):
        upper = max(sum(initial.values()), 1.0)
    if upper < lower:
        raise ValueError("No feasible reaction extent preserves nonnegative amounts")
    return lower, upper


def solve_reaction_extent(
    reaction: EquilibriumReactionSpec,
    initial_amounts_mol: Mapping[str, float],
    *,
    volume_L: float,
    temperature_K: float,
    tolerance: float = 1e-10,
) -> EquilibriumResult:
    """Solve one reversible reaction by scalar extent."""

    system = EquilibriumSystemSpec(
        system_id=reaction.reaction_id,
        reactions=(reaction,),
        temperature_K=temperature_K,
        volume_L=volume_L,
    )
    return solve_mass_action_equilibrium(
        system,
        initial_amounts_mol,
        tolerance=tolerance,
    )


def solve_mass_action_equilibrium(
    system: EquilibriumSystemSpec,
    initial_amounts_mol: Mapping[str, float],
    *,
    tolerance: float = 1e-10,
    max_iterations: int = 200,
) -> EquilibriumResult:
    """Solve fixed-T, fixed-volume mass-action equilibrium in extent space."""

    initial = _complete_amounts(_amounts(initial_amounts_mol), system.species_ids)
    if len(system.reactions) == 1:
        return _solve_single_reaction(system, initial, tolerance=tolerance)

    extent_scale = max(sum(initial.values()), 1.0)
    lower = np.full(len(system.reactions), -extent_scale, dtype=float)
    upper = np.full(len(system.reactions), extent_scale, dtype=float)
    guess = np.clip(np.zeros(len(system.reactions)), lower, upper)

    def residual(x: np.ndarray) -> np.ndarray:
        amounts = _amounts_from_extents(system.reactions, initial, x.tolist())
        penalties = [
            min(0.0, amount) * 1e6
            for species_id, amount in amounts.items()
            if species_id in system.species_ids
        ]
        values = _log_residuals(system, _project_nonnegative(amounts))
        return np.asarray(values + penalties, dtype=float)

    solved = least_squares(
        residual,
        guess,
        bounds=(lower, upper),
        xtol=tolerance,
        ftol=tolerance,
        gtol=tolerance,
        max_nfev=max_iterations,
    )
    extents = solved.x.tolist()
    amounts = _project_nonnegative(_amounts_from_extents(system.reactions, initial, extents))
    residual_values = _log_residuals(system, amounts)
    return _build_equilibrium_result(
        system,
        initial,
        amounts,
        extents,
        converged=bool(solved.success and max(abs(v) for v in residual_values) < 1e-6),
        iterations=int(solved.nfev),
        metadata={"solver": "least_squares", "message": str(solved.message)},
    )


def reaction_quotient(
    amounts_mol: Mapping[str, float],
    stoichiometry: Mapping[str, float],
    *,
    volume_L: float,
    activity_floor: float = _ACTIVITY_FLOOR,
) -> float:
    """Return concentration-based reaction quotient."""

    log_q = reaction_quotient_log(
        amounts_mol,
        stoichiometry,
        volume_L=volume_L,
        activity_floor=activity_floor,
    )
    return _safe_exp(log_q)


def reaction_quotient_log(
    amounts_mol: Mapping[str, float],
    stoichiometry: Mapping[str, float],
    *,
    volume_L: float,
    activity_floor: float = _ACTIVITY_FLOOR,
) -> float:
    _positive(volume_L, "volume_L")
    _positive(activity_floor, "activity_floor")
    amounts = _amounts(amounts_mol)
    total = 0.0
    for species_id, coefficient in stoichiometry.items():
        concentration = max(amounts.get(species_id, 0.0) / volume_L, activity_floor)
        total += coefficient * log(concentration)
    return total


def water_ion_product(temperature_K: float = 298.15) -> float:
    """Return a compact water ion-product estimate, K_w = [H+][OH-]."""

    _positive(temperature_K, "temperature_K")
    pkw_table = (
        (273.15, 14.94),
        (298.15, 14.00),
        (323.15, 13.26),
        (348.15, 12.70),
        (373.15, 12.26),
    )
    if temperature_K <= pkw_table[0][0]:
        pkw = pkw_table[0][1]
    elif temperature_K >= pkw_table[-1][0]:
        pkw = pkw_table[-1][1]
    else:
        pkw = pkw_table[-1][1]
        for (t0, p0), (t1, p1) in pairwise(pkw_table):
            if t0 <= temperature_K <= t1:
                weight = (temperature_K - t0) / (t1 - t0)
                pkw = (1.0 - weight) * p0 + weight * p1
                break
    return 10.0 ** (-pkw)


def solve_monoprotic_acid_base(
    *,
    acid_total_mol: float,
    volume_L: float,
    pka: float,
    temperature_K: float = 298.15,
    strong_cation_mol: float = 0.0,
    strong_anion_mol: float = 0.0,
    acid_id: str = "HA",
    conjugate_base_id: str = "A-",
    proton_id: str = "H+",
    hydroxide_id: str = "OH-",
    cation_id: str = "M+",
    anion_id: str = "X-",
) -> AcidBaseResult:
    """Solve a monoprotic weak-acid equilibrium with electroneutrality."""

    _nonnegative(acid_total_mol, "acid_total_mol")
    _positive(volume_L, "volume_L")
    _finite(pka, "pka")
    _positive(temperature_K, "temperature_K")
    _nonnegative(strong_cation_mol, "strong_cation_mol")
    _nonnegative(strong_anion_mol, "strong_anion_mol")

    total_acid_conc = acid_total_mol / volume_L
    strong_cation_conc = strong_cation_mol / volume_L
    strong_anion_conc = strong_anion_mol / volume_L
    ka = 10.0 ** (-pka)
    kw = water_ion_product(temperature_K)

    def residual(hydrogen: float) -> float:
        conjugate_base = total_acid_conc * ka / (ka + hydrogen) if total_acid_conc else 0.0
        hydroxide = kw / hydrogen
        return hydrogen + strong_cation_conc - (
            hydroxide + conjugate_base + strong_anion_conc
        )

    low = 1e-14
    high = max(1.0, 10.0 * (total_acid_conc + strong_cation_conc + strong_anion_conc + ka))
    while residual(high) < 0.0:
        high *= 10.0
        if high > 1e6:
            raise ValueError("Could not bracket acid/base hydrogen concentration")
    hydrogen = brentq(residual, low, high, xtol=1e-14, rtol=1e-12, maxiter=200)
    hydroxide = kw / hydrogen
    conjugate_base = total_acid_conc * ka / (ka + hydrogen) if total_acid_conc else 0.0
    acid = max(total_acid_conc - conjugate_base, 0.0)
    pH = -log10(hydrogen)
    pOH = -log10(hydroxide)
    amounts = {
        acid_id: acid * volume_L,
        conjugate_base_id: conjugate_base * volume_L,
        proton_id: hydrogen * volume_L,
        hydroxide_id: hydroxide * volume_L,
    }
    charges = {acid_id: 0, conjugate_base_id: -1, proton_id: 1, hydroxide_id: -1}
    if strong_cation_mol > 0.0:
        amounts[cation_id] = strong_cation_mol
        charges[cation_id] = 1
    if strong_anion_mol > 0.0:
        amounts[anion_id] = strong_anion_mol
        charges[anion_id] = -1
    charge_error = net_charge_equivalents(amounts, charges)
    acid_dissociation_fraction = (
        0.0 if total_acid_conc <= 0.0 else conjugate_base / total_acid_conc
    )
    ionic_strength_value = ionic_strength_from_amounts(
        amounts,
        charges,
        solvent_mass_kg=volume_L,
    )
    return AcidBaseResult(
        species_amounts_mol=amounts,
        pH=pH,
        pOH=pOH,
        hydrogen_mol_L=hydrogen,
        hydroxide_mol_L=hydroxide,
        acid_dissociation_fraction=acid_dissociation_fraction,
        charge_balance_error_eq=charge_error,
        ionic_strength_mol_kg=ionic_strength_value,
        metadata={
            "Ka": ka,
            "Kw": kw,
            "temperature_K": temperature_K,
            "volume_L": volume_L,
        },
    )


def precipitate_if_supersaturated(
    amounts_mol: Mapping[str, float],
    spec: SolubilityProductSpec,
    *,
    volume_L: float,
) -> PrecipitationResult:
    """Apply a binary solubility-product precipitation step."""

    amounts = _amounts(amounts_mol)
    _positive(volume_L, "volume_L")
    initial_cation = amounts.get(spec.cation_id, 0.0)
    initial_anion = amounts.get(spec.anion_id, 0.0)
    initial_product = _ion_product(
        initial_cation,
        initial_anion,
        spec=spec,
        volume_L=volume_L,
    )
    initial_saturation_index = log10(max(initial_product, _ACTIVITY_FLOOR) / spec.ksp)
    if initial_product <= spec.ksp:
        final = dict(amounts)
        final.setdefault(spec.precipitate_id, amounts.get(spec.precipitate_id, 0.0))
        return PrecipitationResult(
            final_amounts_mol=final,
            precipitated_mol=0.0,
            ion_product=initial_product,
            saturation_index=initial_saturation_index,
            material_balance_error_mol=0.0,
            metadata={"status": "undersaturated_or_saturated", "spec": spec.to_dict()},
        )

    max_precip = min(initial_cation / spec.cation_stoich, initial_anion / spec.anion_stoich)
    if max_precip <= 0.0:
        return PrecipitationResult(
            final_amounts_mol=dict(amounts),
            precipitated_mol=0.0,
            ion_product=initial_product,
            saturation_index=initial_saturation_index,
            material_balance_error_mol=0.0,
            metadata={"status": "missing_ion", "spec": spec.to_dict()},
        )

    def residual(precipitated: float) -> float:
        cation = max(initial_cation - spec.cation_stoich * precipitated, 0.0)
        anion = max(initial_anion - spec.anion_stoich * precipitated, 0.0)
        return _ion_product(cation, anion, spec=spec, volume_L=volume_L) - spec.ksp

    upper = max_precip * (1.0 - 1e-12)
    precipitated = brentq(residual, 0.0, upper, xtol=1e-14, rtol=1e-12, maxiter=200)
    final = dict(amounts)
    final[spec.cation_id] = max(initial_cation - spec.cation_stoich * precipitated, 0.0)
    final[spec.anion_id] = max(initial_anion - spec.anion_stoich * precipitated, 0.0)
    final[spec.precipitate_id] = final.get(spec.precipitate_id, 0.0) + precipitated
    final_product = _ion_product(
        final[spec.cation_id],
        final[spec.anion_id],
        spec=spec,
        volume_L=volume_L,
    )
    balance_error = abs(
        (initial_cation + initial_anion)
        - (
            final[spec.cation_id]
            + final[spec.anion_id]
            + precipitated * (spec.cation_stoich + spec.anion_stoich)
        )
    )
    return PrecipitationResult(
        final_amounts_mol=final,
        precipitated_mol=precipitated,
        ion_product=final_product,
        saturation_index=log10(max(final_product, _ACTIVITY_FLOOR) / spec.ksp),
        material_balance_error_mol=balance_error,
        metadata={
            "status": "precipitated",
            "initial_ion_product": initial_product,
            "initial_saturation_index": initial_saturation_index,
            "spec": spec.to_dict(),
        },
    )


def net_charge_equivalents(
    amounts_mol: Mapping[str, float],
    charges: Mapping[str, int | float],
) -> float:
    """Return total charge equivalents in moles."""

    amounts = _amounts(amounts_mol)
    return sum(
        amounts.get(species_id, 0.0) * float(charges.get(species_id, 0.0))
        for species_id in amounts
    )


def balance_charge_by_adjusting_ion(
    amounts_mol: Mapping[str, float],
    charges: Mapping[str, int | float],
    *,
    adjustable_species_id: str,
) -> ChargeBalanceResult:
    """Adjust one charged species to enforce electroneutrality."""

    amounts = _amounts(amounts_mol)
    if adjustable_species_id not in charges:
        raise ValueError("adjustable species must have a declared charge")
    charge = float(charges[adjustable_species_id])
    if charge == 0.0:
        raise ValueError("adjustable species must be charged")
    initial_charge = net_charge_equivalents(amounts, charges)
    adjustment = -initial_charge / charge
    new_amount = amounts.get(adjustable_species_id, 0.0) + adjustment
    if new_amount < -1e-12:
        raise ValueError("charge-balance adjustment would make amount negative")
    adjusted = dict(amounts)
    adjusted[adjustable_species_id] = max(new_amount, 0.0)
    final_charge = net_charge_equivalents(adjusted, charges)
    return ChargeBalanceResult(
        adjusted_amounts_mol=adjusted,
        initial_charge_eq=initial_charge,
        final_charge_eq=final_charge,
        adjustment_mol=adjustment,
        adjusted_species_id=adjustable_species_id,
        metadata={"method": "single_ion_adjustment"},
    )


def ionic_strength(
    molalities_mol_kg: Mapping[str, float],
    charges: Mapping[str, int | float],
) -> float:
    """Return ionic strength from molalities and charges."""

    molalities = _amounts(molalities_mol_kg)
    return 0.5 * sum(
        molality * float(charges.get(species_id, 0.0)) ** 2
        for species_id, molality in molalities.items()
    )


def ionic_strength_from_amounts(
    amounts_mol: Mapping[str, float],
    charges: Mapping[str, int | float],
    *,
    solvent_mass_kg: float,
) -> float:
    """Return ionic strength using amounts and solvent mass."""

    _positive(solvent_mass_kg, "solvent_mass_kg")
    molalities = {
        species_id: amount / solvent_mass_kg
        for species_id, amount in _amounts(amounts_mol).items()
        if float(charges.get(species_id, 0.0)) != 0.0
    }
    return ionic_strength(molalities, charges)


def solid_solubility_mole_fraction(
    *,
    temperature_K: float,
    melting_temperature_K: float,
    enthalpy_fusion_J_mol: float,
    liquid_heat_capacity_J_mol_K: float = 0.0,
    solid_heat_capacity_J_mol_K: float = 0.0,
    activity_coefficient: float = 1.0,
) -> float:
    """Return a eutectic-style ideal solid solubility mole fraction."""

    _positive(temperature_K, "temperature_K")
    _positive(melting_temperature_K, "melting_temperature_K")
    _positive(enthalpy_fusion_J_mol, "enthalpy_fusion_J_mol")
    _positive(activity_coefficient, "activity_coefficient")
    _finite(liquid_heat_capacity_J_mol_K, "liquid_heat_capacity_J_mol_K")
    _finite(solid_heat_capacity_J_mol_K, "solid_heat_capacity_J_mol_K")
    delta_cp = liquid_heat_capacity_J_mol_K - solid_heat_capacity_J_mol_K
    exponent = -(
        (
            enthalpy_fusion_J_mol * (1.0 - temperature_K / melting_temperature_K)
            - delta_cp * (melting_temperature_K - temperature_K)
        )
        / (R_J_PER_MOL_K * temperature_K)
        + delta_cp / R_J_PER_MOL_K * log(melting_temperature_K / temperature_K)
    )
    return _clip01(exp(exponent) / activity_coefficient)


def _solve_single_reaction(
    system: EquilibriumSystemSpec,
    initial: dict[str, float],
    *,
    tolerance: float,
) -> EquilibriumResult:
    reaction = system.reactions[0]
    lower, upper = reaction_extent_bounds(reaction, initial)
    span = max(upper - lower, 1.0)
    lo = lower + 1e-12 * span
    hi = upper - 1e-12 * span

    def residual(extent: float) -> float:
        amounts = _amounts_from_extents((reaction,), initial, [extent])
        return _log_residuals(system, amounts)[0]

    f_lo = residual(lo)
    f_hi = residual(hi)
    if abs(f_lo) < tolerance:
        extent = lo
        converged = True
    elif abs(f_hi) < tolerance:
        extent = hi
        converged = True
    elif f_lo * f_hi < 0.0:
        extent = float(brentq(residual, lo, hi, xtol=tolerance, rtol=tolerance, maxiter=200))
        converged = True
    else:
        candidates = (lo, hi, max(lower, min(0.0, upper)))
        extent = min(candidates, key=lambda value: abs(residual(value)))
        converged = abs(residual(extent)) < 1e-6
    amounts = _project_nonnegative(_amounts_from_extents((reaction,), initial, [extent]))
    return _build_equilibrium_result(
        system,
        initial,
        amounts,
        [extent],
        converged=converged,
        iterations=1,
        metadata={"solver": "brentq_extent" if converged else "bounded_residual_min"},
    )


def _build_equilibrium_result(
    system: EquilibriumSystemSpec,
    initial: dict[str, float],
    amounts: dict[str, float],
    extents: list[float],
    *,
    converged: bool,
    iterations: int,
    metadata: dict[str, object],
) -> EquilibriumResult:
    constants = {
        reaction.reaction_id: reaction.equilibrium_constant(system.temperature_K)
        for reaction in system.reactions
    }
    quotients = {
        reaction.reaction_id: reaction_quotient(
            amounts,
            reaction.stoichiometry,
            volume_L=system.volume_L,
        )
        for reaction in system.reactions
    }
    residual_values = _log_residuals(system, amounts)
    return EquilibriumResult(
        system_id=system.system_id,
        initial_amounts_mol=dict(initial),
        final_amounts_mol={key: amounts.get(key, 0.0) for key in sorted(amounts)},
        extents_mol={
            reaction.reaction_id: extents[index]
            for index, reaction in enumerate(system.reactions)
        },
        equilibrium_constants=constants,
        reaction_quotients=quotients,
        residuals_log={
            reaction.reaction_id: residual_values[index]
            for index, reaction in enumerate(system.reactions)
        },
        converged=converged,
        iterations=iterations,
        metadata={
            **metadata,
            "temperature_K": system.temperature_K,
            "pressure_Pa": system.pressure_Pa,
            "volume_L": system.volume_L,
        },
    )


def _log_residuals(system: EquilibriumSystemSpec, amounts: Mapping[str, float]) -> list[float]:
    values = []
    for reaction in system.reactions:
        log_q = reaction_quotient_log(
            amounts,
            reaction.stoichiometry,
            volume_L=system.volume_L,
        )
        log_k = log(max(reaction.equilibrium_constant(system.temperature_K), _ACTIVITY_FLOOR))
        values.append(log_q - log_k)
    return values


def _amounts_from_extents(
    reactions: tuple[EquilibriumReactionSpec, ...],
    initial: Mapping[str, float],
    extents: list[float],
) -> dict[str, float]:
    amounts = dict(initial)
    for reaction, extent in zip(reactions, extents, strict=True):
        for species_id, coefficient in reaction.stoichiometry.items():
            amounts[species_id] = amounts.get(species_id, 0.0) + coefficient * extent
    return amounts


def _complete_amounts(amounts: dict[str, float], species_ids: tuple[str, ...]) -> dict[str, float]:
    complete = dict(amounts)
    for species_id in species_ids:
        complete.setdefault(species_id, 0.0)
    return complete


def _ion_product(
    cation_mol: float,
    anion_mol: float,
    *,
    spec: SolubilityProductSpec,
    volume_L: float,
) -> float:
    cation_conc = max(cation_mol / volume_L, 0.0)
    anion_conc = max(anion_mol / volume_L, 0.0)
    return cation_conc**spec.cation_stoich * anion_conc**spec.anion_stoich


def _amounts(amounts_mol: Mapping[str, float]) -> dict[str, float]:
    amounts = {key: float(value) for key, value in amounts_mol.items()}
    _validate_amounts(amounts, "amounts_mol")
    return amounts


def _validate_amounts(amounts_mol: Mapping[str, float], name: str) -> None:
    for species_id, amount in amounts_mol.items():
        if not species_id:
            raise ValueError(f"{name} contains an empty species id")
        _nonnegative(float(amount), f"{name}[{species_id}]")


def _project_nonnegative(amounts: Mapping[str, float]) -> dict[str, float]:
    return {
        species_id: 0.0 if abs(amount) < 1e-12 else max(amount, 0.0)
        for species_id, amount in amounts.items()
    }


def _safe_exp(value: float) -> float:
    if value > 700.0:
        return exp(700.0)
    if value < -700.0:
        return exp(-700.0)
    return exp(value)


def _clip01(value: float) -> float:
    return max(0.0, min(1.0, value))


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
        raise ValueError(f"{name} cannot be negative")
