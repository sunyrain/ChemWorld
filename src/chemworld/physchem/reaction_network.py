"""General reaction-network engine for ChemWorld."""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field, replace
from math import exp, isfinite
from pathlib import Path
from typing import Any, Literal

import numpy as np
import yaml
from scipy.integrate import solve_ivp

from chemworld.physchem.elements import element_matrix
from chemworld.physchem.reaction_network_specs import (
    Arrow,  # noqa: F401
    RateLawSpec,
    ReactionSpec,
    SpeciesSpec,
    parse_reaction_equation,  # noqa: F401
    reaction_from_dict,
    species_from_dict,
)

R_J_PER_MOL_K = 8.31446261815324
AnalyticalODECase = Literal["irreversible_first_order", "reversible_first_order"]


@dataclass(frozen=True)
class ReactionNetworkSpec:
    network_id: str
    species: tuple[SpeciesSpec, ...]
    reactions: tuple[ReactionSpec, ...]
    units: dict[str, str] = field(default_factory=lambda: {"amount": "mol", "volume": "L"})
    metadata: dict[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.network_id:
            raise ValueError("network_id cannot be empty")
        species_ids = [species.species_id for species in self.species]
        reaction_ids = [reaction.reaction_id for reaction in self.reactions]
        if len(species_ids) != len(set(species_ids)):
            raise ValueError("Duplicate species_id values are not allowed")
        if len(reaction_ids) != len(set(reaction_ids)):
            raise ValueError("Duplicate reaction_id values are not allowed")
        known = set(species_ids)
        for reaction in self.reactions:
            missing = sorted(set(reaction.stoichiometry) - known)
            if missing:
                raise ValueError(
                    f"Reaction {reaction.reaction_id} references unknown species: {missing}"
                )
        self.check_element_balance(raise_on_error=True)

    @property
    def species_ids(self) -> tuple[str, ...]:
        return tuple(species.species_id for species in self.species)

    @property
    def reaction_ids(self) -> tuple[str, ...]:
        return tuple(reaction.reaction_id for reaction in self.reactions)

    @property
    def species_index(self) -> dict[str, int]:
        return {species_id: idx for idx, species_id in enumerate(self.species_ids)}

    def stoichiometric_matrix(self) -> tuple[tuple[float, ...], ...]:
        index = self.species_index
        matrix = [[0.0 for _ in self.reactions] for _ in self.species]
        for reaction_idx, reaction in enumerate(self.reactions):
            for species_id, coefficient in reaction.stoichiometry.items():
                matrix[index[species_id]][reaction_idx] = coefficient
        return tuple(tuple(row) for row in matrix)

    def element_matrix(self) -> tuple[tuple[tuple[float, ...], ...], tuple[str, ...]]:
        return element_matrix([species.composition for species in self.species])

    def element_balance_residuals(self) -> dict[str, dict[str, float]]:
        matrix, element_order = self.element_matrix()
        stoich = self.stoichiometric_matrix()
        residuals: dict[str, dict[str, float]] = {}
        for reaction_idx, reaction in enumerate(self.reactions):
            reaction_residuals = {}
            for element_idx, element in enumerate(element_order):
                residual = sum(
                    matrix[species_idx][element_idx] * stoich[species_idx][reaction_idx]
                    for species_idx in range(len(self.species))
                )
                if abs(residual) > 1e-12:
                    reaction_residuals[element] = residual
            residuals[reaction.reaction_id] = reaction_residuals
        return residuals

    def check_element_balance(self, *, raise_on_error: bool = False) -> bool:
        residuals = self.element_balance_residuals()
        passed = all(not reaction_residuals for reaction_residuals in residuals.values())
        if raise_on_error and not passed:
            raise ValueError(f"Reaction network is not element balanced: {residuals}")
        return passed

    def reaction_rates(
        self,
        amounts_mol: Mapping[str, float],
        *,
        volume_L: float,
        temperature_K: float,
        species_thermo: Mapping[str, Any] | None = None,
    ) -> dict[str, float]:
        concentrations = self._concentrations(amounts_mol, volume_L=volume_L)
        return {
            reaction.reaction_id: evaluate_rate_law(
                reaction,
                concentrations_mol_L=concentrations,
                temperature_K=temperature_K,
                species_thermo=species_thermo,
            )
            for reaction in self.reactions
        }

    def amount_derivatives(
        self,
        amounts_mol: Mapping[str, float],
        *,
        volume_L: float,
        temperature_K: float,
        species_thermo: Mapping[str, Any] | None = None,
    ) -> dict[str, float]:
        rates = self.reaction_rates(
            amounts_mol,
            volume_L=volume_L,
            temperature_K=temperature_K,
            species_thermo=species_thermo,
        )
        derivatives = dict.fromkeys(self.species_ids, 0.0)
        for reaction in self.reactions:
            rate_mol_L_s = rates[reaction.reaction_id]
            for species_id, coefficient in reaction.stoichiometry.items():
                derivatives[species_id] += coefficient * rate_mol_L_s * volume_L
        return derivatives

    def integrate_batch(
        self,
        initial_amounts_mol: Mapping[str, float],
        *,
        volume_L: float,
        temperature_K: float,
        duration_s: float,
        evaluation_times_s: Sequence[float] | None = None,
        species_thermo: Mapping[str, Any] | None = None,
    ) -> BatchIntegrationResult:
        if duration_s < 0:
            raise ValueError("duration_s cannot be negative")
        if volume_L <= 0:
            raise ValueError("volume_L must be positive")
        y0 = np.array(
            [
                max(float(initial_amounts_mol.get(species_id, 0.0)), 0.0)
                for species_id in self.species_ids
            ]
        )

        def rhs(_time_s: float, y: np.ndarray) -> np.ndarray:
            amounts = {
                species_id: max(float(value), 0.0)
                for species_id, value in zip(self.species_ids, y, strict=True)
            }
            derivatives = self.amount_derivatives(
                amounts,
                volume_L=volume_L,
                temperature_K=temperature_K,
                species_thermo=species_thermo,
            )
            return np.array([derivatives[species_id] for species_id in self.species_ids])

        if evaluation_times_s is None:
            t_eval = None
        else:
            t_eval = np.array(tuple(evaluation_times_s), dtype=float)
        result = solve_ivp(
            rhs,
            (0.0, duration_s),
            y0,
            t_eval=t_eval,
            method="LSODA",
            rtol=1e-8,
            atol=1e-12,
        )
        if not result.success:
            raise RuntimeError(f"Reaction-network integration failed: {result.message}")
        final = {
            species_id: max(float(result.y[idx, -1]), 0.0)
            for idx, species_id in enumerate(self.species_ids)
        }
        return BatchIntegrationResult(
            network_id=self.network_id,
            species_ids=self.species_ids,
            times_s=tuple(float(value) for value in result.t),
            amounts_mol=tuple(
                tuple(max(float(value), 0.0) for value in result.y[idx])
                for idx in range(len(self.species_ids))
            ),
            final_amounts_mol=final,
        )

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> ReactionNetworkSpec:
        species = tuple(species_from_dict(item) for item in payload["species"])
        reactions = tuple(reaction_from_dict(item) for item in payload["reactions"])
        return cls(
            network_id=str(payload["network_id"]),
            species=species,
            reactions=reactions,
            units=dict(payload.get("units", {"amount": "mol", "volume": "L"})),
            metadata=dict(payload.get("metadata", {})),
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "network_id": self.network_id,
            "species": [species.to_dict() for species in self.species],
            "reactions": [reaction.to_dict() for reaction in self.reactions],
            "stoichiometric_matrix": [list(row) for row in self.stoichiometric_matrix()],
            "element_balance_residuals": self.element_balance_residuals(),
            "units": dict(self.units),
            "metadata": dict(self.metadata),
        }

    def _concentrations(
        self,
        amounts_mol: Mapping[str, float],
        *,
        volume_L: float,
    ) -> dict[str, float]:
        if volume_L <= 0:
            raise ValueError("volume_L must be positive")
        concentrations = {}
        for species_id in self.species_ids:
            amount = float(amounts_mol.get(species_id, 0.0))
            if amount < -1e-15:
                raise ValueError(
                    f"Species amount cannot be negative: {species_id}={amount}"
                )
            concentrations[species_id] = max(amount, 0.0) / volume_L
        return concentrations


@dataclass(frozen=True)
class BatchIntegrationResult:
    network_id: str
    species_ids: tuple[str, ...]
    times_s: tuple[float, ...]
    amounts_mol: tuple[tuple[float, ...], ...]
    final_amounts_mol: dict[str, float]

    def to_dict(self) -> dict[str, object]:
        return {
            "network_id": self.network_id,
            "species_ids": list(self.species_ids),
            "times_s": list(self.times_s),
            "amounts_mol": [list(row) for row in self.amounts_mol],
            "final_amounts_mol": dict(self.final_amounts_mol),
        }


@dataclass(frozen=True)
class ReactionODEReferenceCase:
    """A small, auditable ODE case with an analytical solution.

    These cases intentionally target the constant-volume, isothermal,
    homogeneous reaction-network slice that Cantera ReactorNet and RMG
    elementary Arrhenius rates also cover. They are not copied from either
    project; they provide ChemWorld-owned reference problems for validating the
    local stoichiometric ODE integrator.
    """

    case_id: str
    title: str
    network: ReactionNetworkSpec
    initial_amounts_mol: dict[str, float]
    volume_L: float
    temperature_K: float
    duration_s: float
    evaluation_times_s: tuple[float, ...]
    analytical_case: AnalyticalODECase
    parameters: dict[str, float]
    reference_notes: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.case_id.strip():
            raise ValueError("case_id cannot be empty")
        if self.volume_L <= 0:
            raise ValueError("volume_L must be positive")
        if self.temperature_K <= 0:
            raise ValueError("temperature_K must be positive")
        if self.duration_s < 0:
            raise ValueError("duration_s cannot be negative")
        if not self.evaluation_times_s:
            raise ValueError("evaluation_times_s cannot be empty")
        if self.evaluation_times_s[0] < 0:
            raise ValueError("evaluation_times_s cannot contain negative times")
        if self.evaluation_times_s[-1] > self.duration_s:
            raise ValueError("evaluation_times_s cannot exceed duration_s")
        if tuple(sorted(self.evaluation_times_s)) != tuple(self.evaluation_times_s):
            raise ValueError("evaluation_times_s must be sorted")
        for species_id, amount in self.initial_amounts_mol.items():
            if species_id not in self.network.species_ids:
                raise ValueError(f"Unknown initial species: {species_id}")
            if amount < 0:
                raise ValueError(f"Initial amount cannot be negative: {species_id}")

    def analytical_amounts_mol(self, time_s: float) -> dict[str, float]:
        if time_s < 0:
            raise ValueError("time_s cannot be negative")
        if self.analytical_case == "irreversible_first_order":
            k_s = self.parameters["k_s^-1"]
            initial_a = self.initial_amounts_mol.get("A", 0.0)
            initial_b = self.initial_amounts_mol.get("B", 0.0)
            amount_a = initial_a * exp(-k_s * time_s)
            amount_b = initial_b + initial_a - amount_a
            return {
                species_id: (
                    amount_a if species_id == "A"
                    else amount_b if species_id == "B"
                    else self.initial_amounts_mol.get(species_id, 0.0)
                )
                for species_id in self.network.species_ids
            }
        if self.analytical_case == "reversible_first_order":
            k_forward_s = self.parameters["k_forward_s^-1"]
            k_reverse_s = self.parameters["k_reverse_s^-1"]
            initial_a = self.initial_amounts_mol.get("A", 0.0)
            initial_b = self.initial_amounts_mol.get("B", 0.0)
            total = initial_a + initial_b
            rate_sum = k_forward_s + k_reverse_s
            amount_a_eq = k_reverse_s * total / rate_sum
            amount_a = amount_a_eq + (initial_a - amount_a_eq) * exp(-rate_sum * time_s)
            amount_b = total - amount_a
            return {
                species_id: (
                    amount_a if species_id == "A"
                    else amount_b if species_id == "B"
                    else self.initial_amounts_mol.get(species_id, 0.0)
                )
                for species_id in self.network.species_ids
            }
        raise ValueError(f"Unsupported analytical ODE case: {self.analytical_case}")

    def analytical_trajectory_mol(self) -> tuple[dict[str, float], ...]:
        return tuple(
            self.analytical_amounts_mol(time_s)
            for time_s in self.evaluation_times_s
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "case_id": self.case_id,
            "title": self.title,
            "network": self.network.to_dict(),
            "initial_amounts_mol": dict(self.initial_amounts_mol),
            "volume_L": self.volume_L,
            "temperature_K": self.temperature_K,
            "duration_s": self.duration_s,
            "evaluation_times_s": list(self.evaluation_times_s),
            "analytical_case": self.analytical_case,
            "parameters": dict(self.parameters),
            "reference_notes": list(self.reference_notes),
        }


@dataclass(frozen=True)
class ReactionODEReferenceResult:
    case_id: str
    passed: bool
    max_abs_error_mol: float
    max_rel_error: float
    tolerance: dict[str, float]
    final_amounts_mol: dict[str, float]
    analytical_final_amounts_mol: dict[str, float]

    def to_dict(self) -> dict[str, object]:
        return {
            "case_id": self.case_id,
            "passed": self.passed,
            "max_abs_error_mol": self.max_abs_error_mol,
            "max_rel_error": self.max_rel_error,
            "tolerance": dict(self.tolerance),
            "final_amounts_mol": dict(self.final_amounts_mol),
            "analytical_final_amounts_mol": dict(self.analytical_final_amounts_mol),
        }


@dataclass(frozen=True)
class ThermochemicalDetailedBalanceResult:
    """Forward and reverse rate constants linked by reaction thermochemistry."""

    reaction_id: str
    temperature_K: float
    forward_rate_constant: float
    reverse_rate_constant: float
    concentration_equilibrium_constant: float
    dimensionless_equilibrium_constant: float
    delta_g_J_mol: float
    reaction_order_delta: float
    standard_concentration_mol_L: float
    source: str = "nasa7"

    def to_dict(self) -> dict[str, object]:
        return {
            "reaction_id": self.reaction_id,
            "temperature_K": self.temperature_K,
            "forward_rate_constant": self.forward_rate_constant,
            "reverse_rate_constant": self.reverse_rate_constant,
            "concentration_equilibrium_constant": (
                self.concentration_equilibrium_constant
            ),
            "dimensionless_equilibrium_constant": (
                self.dimensionless_equilibrium_constant
            ),
            "delta_g_J_mol": self.delta_g_J_mol,
            "reaction_order_delta": self.reaction_order_delta,
            "standard_concentration_mol_L": self.standard_concentration_mol_L,
            "source": self.source,
        }


@dataclass(frozen=True)
class ReactionSensitivityEntry:
    """Finite-difference sensitivity for one kinetic parameter."""

    reaction_id: str
    parameter_name: str
    observable: str
    baseline_parameter_value: float
    perturbation_log_step: float
    baseline_observable_value: float
    plus_observable_value: float
    minus_observable_value: float
    derivative_dobservable_dln_parameter: float
    normalized_sensitivity: float | None
    local_observable_std: float
    local_normalized_std: float | None

    @property
    def parameter_id(self) -> str:
        return f"{self.reaction_id}.{self.parameter_name}"

    @property
    def direction(self) -> Literal["positive", "negative", "near_zero"]:
        if abs(self.derivative_dobservable_dln_parameter) < 1e-15:
            return "near_zero"
        if self.derivative_dobservable_dln_parameter > 0:
            return "positive"
        return "negative"

    @property
    def rank_score(self) -> float:
        if self.normalized_sensitivity is not None:
            return abs(self.normalized_sensitivity)
        return abs(self.derivative_dobservable_dln_parameter)

    def to_dict(self) -> dict[str, object]:
        return {
            "parameter_id": self.parameter_id,
            "reaction_id": self.reaction_id,
            "parameter_name": self.parameter_name,
            "observable": self.observable,
            "baseline_parameter_value": self.baseline_parameter_value,
            "perturbation_log_step": self.perturbation_log_step,
            "baseline_observable_value": self.baseline_observable_value,
            "plus_observable_value": self.plus_observable_value,
            "minus_observable_value": self.minus_observable_value,
            "derivative_dobservable_dln_parameter": (
                self.derivative_dobservable_dln_parameter
            ),
            "normalized_sensitivity": self.normalized_sensitivity,
            "local_observable_std": self.local_observable_std,
            "local_normalized_std": self.local_normalized_std,
            "direction": self.direction,
            "rank_score": self.rank_score,
        }


@dataclass(frozen=True)
class ReactionSensitivityReport:
    """JSON-friendly local kinetic sensitivity report."""

    network_id: str
    observable: str
    observable_species_id: str
    baseline_observable_value: float
    volume_L: float
    temperature_K: float
    duration_s: float
    perturbation_log_step: float
    relative_parameter_uncertainty: float
    entries: tuple[ReactionSensitivityEntry, ...]
    method: str = "central_finite_difference_log_parameter"

    @property
    def uncertainty_summary(self) -> dict[str, float | None]:
        variance = sum(entry.local_observable_std**2 for entry in self.entries)
        observable_std = float(np.sqrt(variance))
        normalized_variance = sum(
            entry.local_normalized_std**2
            for entry in self.entries
            if entry.local_normalized_std is not None
        )
        normalized_std: float | None
        if abs(self.baseline_observable_value) > 1e-15:
            normalized_std = float(np.sqrt(normalized_variance))
        else:
            normalized_std = None
        return {
            "relative_parameter_uncertainty": self.relative_parameter_uncertainty,
            "observable_std_estimate": observable_std,
            "normalized_std_estimate": normalized_std,
        }

    def ranked_entries(self, limit: int | None = None) -> tuple[ReactionSensitivityEntry, ...]:
        ranked = tuple(
            sorted(
                self.entries,
                key=lambda entry: entry.rank_score,
                reverse=True,
            )
        )
        if limit is None:
            return ranked
        if limit < 0:
            raise ValueError("limit cannot be negative")
        return ranked[:limit]

    def explanation_ranking(self, limit: int = 3) -> tuple[dict[str, object], ...]:
        return tuple(
            {
                "rank": index + 1,
                "parameter_id": entry.parameter_id,
                "reaction_id": entry.reaction_id,
                "parameter_name": entry.parameter_name,
                "direction": entry.direction,
                "normalized_sensitivity": entry.normalized_sensitivity,
                "interpretation": (
                    f"{entry.parameter_id} has a {entry.direction} local effect "
                    f"on {self.observable}."
                ),
            }
            for index, entry in enumerate(self.ranked_entries(limit))
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "network_id": self.network_id,
            "observable": self.observable,
            "observable_species_id": self.observable_species_id,
            "baseline_observable_value": self.baseline_observable_value,
            "volume_L": self.volume_L,
            "temperature_K": self.temperature_K,
            "duration_s": self.duration_s,
            "perturbation_log_step": self.perturbation_log_step,
            "relative_parameter_uncertainty": self.relative_parameter_uncertainty,
            "method": self.method,
            "entries": [entry.to_dict() for entry in self.entries],
            "uncertainty_summary": self.uncertainty_summary,
            "explanation_ranking": list(self.explanation_ranking()),
        }


def cantera_comparable_reaction_cases() -> tuple[ReactionODEReferenceCase, ...]:
    """Return ChemWorld-owned constant-volume ODE reference cases.

    The cases are deliberately minimal but professional: each has a balanced
    stoichiometric network, SI-like rate parameters, an analytical trajectory,
    and the same mass-action structure used by Cantera/RMG elementary kinetics.
    """

    species = (
        SpeciesSpec("A", "C2H4O2", phase="gas"),
        SpeciesSpec("B", "C2H4O2", phase="gas"),
    )
    irreversible_k = 0.035
    reversible_k_forward = 0.018
    reversible_k_reverse = 0.006
    common_notes = (
        "reference_repos/cantera/doc/sphinx/yaml/reactions.md: reaction "
        "equations use => for irreversible and <=> for reversible reactions.",
        "reference_repos/cantera/test/python/test_reaction.py: ArrheniusRate "
        "uses A*T**b*exp(-Ea/RT).",
        "reference_repos/rmg-py/rmgpy/kinetics/arrhenius.pyx: "
        "Arrhenius.get_rate_coefficient applies A*(T/T0)**n*exp(-Ea/RT).",
        "reference_repos/rmg-py/rmgpy/reaction.py: reverse rates are obtained "
        "from k_forward/K_eq for reversible reactions.",
    )
    return (
        ReactionODEReferenceCase(
            case_id="cantera_comparable_irreversible_first_order",
            title="Irreversible A => B first-order batch ODE",
            network=ReactionNetworkSpec(
                "cantera_comparable_irreversible_first_order",
                species,
                (
                    ReactionSpec.from_equation(
                        reaction_id="r1",
                        equation="A => B",
                        rate_law=RateLawSpec(
                            "r1_mass_action",
                            "mass_action",
                            {"k": irreversible_k},
                        ),
                    ),
                ),
                metadata={
                    "reference_family": "constant-volume homogeneous batch reactor",
                    "source": "chemworld_owned_analytical_case",
                },
            ),
            initial_amounts_mol={"A": 1.2, "B": 0.05},
            volume_L=1.0,
            temperature_K=700.0,
            duration_s=160.0,
            evaluation_times_s=(0.0, 20.0, 80.0, 160.0),
            analytical_case="irreversible_first_order",
            parameters={"k_s^-1": irreversible_k},
            reference_notes=common_notes,
        ),
        ReactionODEReferenceCase(
            case_id="cantera_comparable_reversible_first_order",
            title="Reversible A <=> B first-order batch ODE with finite K_eq",
            network=ReactionNetworkSpec(
                "cantera_comparable_reversible_first_order",
                species,
                (
                    ReactionSpec.from_equation(
                        reaction_id="r1",
                        equation="A <=> B",
                        rate_law=RateLawSpec(
                            "r1_reversible_arrhenius",
                            "reversible_arrhenius",
                            {
                                "A": reversible_k_forward,
                                "Ea_J_per_mol": 0.0,
                                "K_eq": reversible_k_forward / reversible_k_reverse,
                            },
                        ),
                    ),
                ),
                metadata={
                    "reference_family": "constant-volume homogeneous batch reactor",
                    "source": "chemworld_owned_analytical_case",
                },
            ),
            initial_amounts_mol={"A": 0.9, "B": 0.1},
            volume_L=1.0,
            temperature_K=750.0,
            duration_s=500.0,
            evaluation_times_s=(0.0, 50.0, 200.0, 500.0),
            analytical_case="reversible_first_order",
            parameters={
                "k_forward_s^-1": reversible_k_forward,
                "k_reverse_s^-1": reversible_k_reverse,
                "K_eq": reversible_k_forward / reversible_k_reverse,
            },
            reference_notes=common_notes,
        ),
    )


def integrate_reaction_ode_reference_case(
    case: ReactionODEReferenceCase,
) -> BatchIntegrationResult:
    return case.network.integrate_batch(
        case.initial_amounts_mol,
        volume_L=case.volume_L,
        temperature_K=case.temperature_K,
        duration_s=case.duration_s,
        evaluation_times_s=case.evaluation_times_s,
    )


def evaluate_reaction_ode_reference_case(
    case: ReactionODEReferenceCase,
    *,
    rtol: float = 1e-7,
    atol_mol: float = 1e-9,
) -> ReactionODEReferenceResult:
    if rtol < 0 or atol_mol < 0:
        raise ValueError("rtol and atol_mol must be nonnegative")
    numerical = integrate_reaction_ode_reference_case(case)
    analytical = case.analytical_trajectory_mol()
    max_abs_error = 0.0
    max_rel_error = 0.0
    passed = True
    for species_index, species_id in enumerate(numerical.species_ids):
        for time_index, _time_s in enumerate(numerical.times_s):
            numerical_value = numerical.amounts_mol[species_index][time_index]
            analytical_value = analytical[time_index][species_id]
            abs_error = abs(numerical_value - analytical_value)
            rel_error = abs_error / max(abs(analytical_value), atol_mol)
            max_abs_error = max(max_abs_error, abs_error)
            max_rel_error = max(max_rel_error, rel_error)
            if abs_error > atol_mol + rtol * abs(analytical_value):
                passed = False
    analytical_final = analytical[-1]
    return ReactionODEReferenceResult(
        case_id=case.case_id,
        passed=passed,
        max_abs_error_mol=max_abs_error,
        max_rel_error=max_rel_error,
        tolerance={"rtol": rtol, "atol_mol": atol_mol},
        final_amounts_mol=numerical.final_amounts_mol,
        analytical_final_amounts_mol=analytical_final,
    )


def thermochemical_detailed_balance(
    reaction: ReactionSpec,
    *,
    species_thermo: Mapping[str, Any],
    temperature_K: float,
    standard_concentration_mol_L: float = 1.0,
) -> ThermochemicalDetailedBalanceResult:
    """Compute reverse rate constant from NASA7 reaction thermochemistry.

    The concentration equilibrium constant is consistent with ChemWorld's
    mass-action rate powers:

    ``K_c = K_dimensionless * C0 ** sum(nu_i)``.
    """

    if reaction.rate_law.equation_id != "reversible_arrhenius":
        raise ValueError("thermochemical detailed balance requires reversible_arrhenius")
    forward_rate_constant = _arrhenius_k(reaction.rate_law.parameters, temperature_K)
    concentration_equilibrium_constant, dimensionless_equilibrium_constant, delta_g = (
        thermochemical_concentration_equilibrium_constant(
            reaction,
            species_thermo=species_thermo,
            temperature_K=temperature_K,
            standard_concentration_mol_L=standard_concentration_mol_L,
        )
    )
    return ThermochemicalDetailedBalanceResult(
        reaction_id=reaction.reaction_id,
        temperature_K=temperature_K,
        forward_rate_constant=forward_rate_constant,
        reverse_rate_constant=reverse_rate_constant_from_equilibrium(
            forward_rate_constant=forward_rate_constant,
            concentration_equilibrium_constant=concentration_equilibrium_constant,
        ),
        concentration_equilibrium_constant=concentration_equilibrium_constant,
        dimensionless_equilibrium_constant=dimensionless_equilibrium_constant,
        delta_g_J_mol=delta_g,
        reaction_order_delta=_reaction_order_delta(reaction),
        standard_concentration_mol_L=standard_concentration_mol_L,
    )


def thermochemical_concentration_equilibrium_constant(
    reaction: ReactionSpec,
    *,
    species_thermo: Mapping[str, Any],
    temperature_K: float,
    standard_concentration_mol_L: float = 1.0,
) -> tuple[float, float, float]:
    """Return ``(K_c, K_dimensionless, Delta G)`` from species thermo."""

    if temperature_K <= 0:
        raise ValueError("temperature_K must be positive")
    if standard_concentration_mol_L <= 0 or not isfinite(standard_concentration_mol_L):
        raise ValueError("standard_concentration_mol_L must be finite and positive")
    from chemworld.physchem.thermochemistry import reaction_thermochemistry

    thermo_result = reaction_thermochemistry(
        reaction_id=reaction.reaction_id,
        stoichiometry=reaction.stoichiometry,
        species_thermo=species_thermo,
        temperature_K=temperature_K,
    )
    concentration_equilibrium_constant = (
        thermo_result.equilibrium_constant
        * standard_concentration_mol_L ** _reaction_order_delta(reaction)
    )
    if concentration_equilibrium_constant <= 0 or not isfinite(
        concentration_equilibrium_constant
    ):
        raise ValueError("thermochemical concentration equilibrium constant is invalid")
    return (
        concentration_equilibrium_constant,
        thermo_result.equilibrium_constant,
        thermo_result.delta_g_J_mol,
    )


def reverse_rate_constant_from_equilibrium(
    *,
    forward_rate_constant: float,
    concentration_equilibrium_constant: float,
) -> float:
    """Return ``k_reverse = k_forward / K_c`` with explicit validation."""

    if forward_rate_constant < 0 or not isfinite(forward_rate_constant):
        raise ValueError("forward_rate_constant must be finite and nonnegative")
    if concentration_equilibrium_constant <= 0 or not isfinite(
        concentration_equilibrium_constant
    ):
        raise ValueError("concentration_equilibrium_constant must be finite and positive")
    return forward_rate_constant / concentration_equilibrium_constant


def finite_difference_reaction_sensitivities(
    network: ReactionNetworkSpec,
    initial_amounts_mol: Mapping[str, float],
    *,
    volume_L: float,
    temperature_K: float,
    duration_s: float,
    observable_species_id: str,
    parameters: Sequence[tuple[str, str]] | None = None,
    perturbation_log_step: float = 1e-4,
    relative_parameter_uncertainty: float = 0.10,
    species_thermo: Mapping[str, Any] | None = None,
) -> ReactionSensitivityReport:
    """Return local finite-difference kinetic sensitivities.

    Sensitivities use Cantera-style normalized response coefficients:

    ``S = (1/y) d y / d ln(p)``

    for positive rate multiplier-like parameters. The implementation is a
    deterministic ChemWorld-local central finite difference and is intended for
    benchmark explanation/model-learning hooks, not for replacing adjoint
    sensitivity solvers.
    """

    if observable_species_id not in network.species_ids:
        raise ValueError(f"Unknown observable species: {observable_species_id}")
    if perturbation_log_step <= 0 or not isfinite(perturbation_log_step):
        raise ValueError("perturbation_log_step must be finite and positive")
    if perturbation_log_step > 0.1:
        raise ValueError("perturbation_log_step is too large for local sensitivity")
    if relative_parameter_uncertainty < 0 or not isfinite(relative_parameter_uncertainty):
        raise ValueError("relative_parameter_uncertainty must be finite and nonnegative")
    candidates = (
        tuple(parameters)
        if parameters is not None
        else kinetic_sensitivity_parameter_candidates(network)
    )
    if not candidates:
        raise ValueError("No positive kinetic sensitivity parameters were found")

    baseline = network.integrate_batch(
        initial_amounts_mol,
        volume_L=volume_L,
        temperature_K=temperature_K,
        duration_s=duration_s,
        species_thermo=species_thermo,
    )
    baseline_value = baseline.final_amounts_mol[observable_species_id]
    entries: list[ReactionSensitivityEntry] = []
    factor = exp(perturbation_log_step)
    for reaction_id, parameter_name in candidates:
        baseline_parameter = _positive_reaction_parameter(
            network,
            reaction_id,
            parameter_name,
        )
        plus_network = _with_reaction_parameter(
            network,
            reaction_id,
            parameter_name,
            baseline_parameter * factor,
        )
        minus_network = _with_reaction_parameter(
            network,
            reaction_id,
            parameter_name,
            baseline_parameter / factor,
        )
        plus = plus_network.integrate_batch(
            initial_amounts_mol,
            volume_L=volume_L,
            temperature_K=temperature_K,
            duration_s=duration_s,
            species_thermo=species_thermo,
        )
        minus = minus_network.integrate_batch(
            initial_amounts_mol,
            volume_L=volume_L,
            temperature_K=temperature_K,
            duration_s=duration_s,
            species_thermo=species_thermo,
        )
        plus_value = plus.final_amounts_mol[observable_species_id]
        minus_value = minus.final_amounts_mol[observable_species_id]
        derivative = (plus_value - minus_value) / (2.0 * perturbation_log_step)
        normalized: float | None = None
        local_normalized_std: float | None = None
        if abs(baseline_value) > 1e-15:
            normalized = derivative / baseline_value
            local_normalized_std = abs(normalized) * relative_parameter_uncertainty
        entries.append(
            ReactionSensitivityEntry(
                reaction_id=reaction_id,
                parameter_name=parameter_name,
                observable=f"final_amount:{observable_species_id}",
                baseline_parameter_value=baseline_parameter,
                perturbation_log_step=perturbation_log_step,
                baseline_observable_value=baseline_value,
                plus_observable_value=plus_value,
                minus_observable_value=minus_value,
                derivative_dobservable_dln_parameter=derivative,
                normalized_sensitivity=normalized,
                local_observable_std=abs(derivative) * relative_parameter_uncertainty,
                local_normalized_std=local_normalized_std,
            )
        )
    return ReactionSensitivityReport(
        network_id=network.network_id,
        observable=f"final_amount:{observable_species_id}",
        observable_species_id=observable_species_id,
        baseline_observable_value=baseline_value,
        volume_L=volume_L,
        temperature_K=temperature_K,
        duration_s=duration_s,
        perturbation_log_step=perturbation_log_step,
        relative_parameter_uncertainty=relative_parameter_uncertainty,
        entries=tuple(entries),
    )


def kinetic_sensitivity_parameter_candidates(
    network: ReactionNetworkSpec,
    *,
    parameter_names: Sequence[str] = ("k", "A", "A_reverse", "K_eq", "vmax", "Km"),
) -> tuple[tuple[str, str], ...]:
    """Return positive multiplier-like kinetic parameters for sensitivities."""

    allowed = set(parameter_names)
    candidates: list[tuple[str, str]] = []
    for reaction in network.reactions:
        for parameter_name, value in reaction.rate_law.parameters.items():
            if parameter_name not in allowed:
                continue
            if isinstance(value, int | float | str):
                numeric = float(value)
                if numeric > 0 and isfinite(numeric):
                    candidates.append((reaction.reaction_id, parameter_name))
    return tuple(candidates)


def evaluate_rate_law(
    reaction: ReactionSpec,
    *,
    concentrations_mol_L: Mapping[str, float],
    temperature_K: float,
    species_thermo: Mapping[str, Any] | None = None,
) -> float:
    if temperature_K <= 0:
        raise ValueError("temperature_K must be positive")
    params = reaction.rate_law.parameters
    equation_id = reaction.rate_law.equation_id
    if equation_id == "mass_action":
        return _mass_action_rate(
            reaction.reactants,
            concentrations_mol_L,
            float(params["k"]),
        )
    if equation_id in {"arrhenius", "modified_arrhenius"}:
        k = _arrhenius_k(params, temperature_K)
        return _mass_action_rate(reaction.reactants, concentrations_mol_L, k)
    if equation_id == "reversible_arrhenius":
        forward_rate_constant = _arrhenius_k(params, temperature_K)
        forward = _mass_action_rate(
            reaction.reactants,
            concentrations_mol_L,
            forward_rate_constant,
        )
        reverse_rate_constant = _reverse_rate_constant(
            reaction,
            params,
            temperature_K=temperature_K,
            forward_rate_constant=forward_rate_constant,
            species_thermo=species_thermo,
        )
        reverse = _mass_action_rate(
            reaction.products,
            concentrations_mol_L,
            reverse_rate_constant,
        )
        return forward - reverse
    if equation_id == "catalytic_activity":
        base = _mass_action_rate(
            reaction.reactants,
            concentrations_mol_L,
            _arrhenius_k(params, temperature_K),
        )
        catalyst_species = str(params.get("catalyst_species", ""))
        reference = float(params.get("reference_concentration_mol_L", 1.0))
        exponent = float(params.get("activity_order", 1.0))
        if not catalyst_species:
            raise ValueError("catalytic_activity requires catalyst_species")
        activity = max(concentrations_mol_L.get(catalyst_species, 0.0), 0.0) / reference
        return base * activity**exponent
    if equation_id == "catalyst_deactivation":
        species = str(params.get("species", ""))
        if not species:
            raise ValueError("catalyst_deactivation requires species")
        return _arrhenius_k(params, temperature_K) * max(
            concentrations_mol_L.get(species, 0.0),
            0.0,
        )
    if equation_id == "langmuir_hinshelwood":
        k = _arrhenius_k(params, temperature_K)
        numerator = _mass_action_rate(reaction.reactants, concentrations_mol_L, k)
        adsorption = params.get("adsorption", {})
        if not isinstance(adsorption, dict):
            raise ValueError("langmuir_hinshelwood adsorption must be a mapping")
        denominator = 1.0 + sum(
            float(K) * max(concentrations_mol_L.get(str(species_id), 0.0), 0.0)
            for species_id, K in adsorption.items()
        )
        power = float(params.get("denominator_power", 1.0))
        return numerator / denominator**power
    if equation_id == "michaelis_menten":
        substrate = str(params["substrate"])
        concentration = max(concentrations_mol_L.get(substrate, 0.0), 0.0)
        return float(params["vmax"]) * concentration / (float(params["Km"]) + concentration)
    raise ValueError(f"Unsupported rate law: {equation_id}")


def load_mechanism(path: str | Path) -> ReactionNetworkSpec:
    source = Path(path)
    text = source.read_text(encoding="utf-8")
    if source.suffix.lower() == ".json":
        payload = json.loads(text)
    elif source.suffix.lower() in {".yaml", ".yml"}:
        payload = yaml.safe_load(text)
    else:
        raise ValueError(f"Unsupported mechanism file extension: {source.suffix}")
    if not isinstance(payload, dict):
        raise ValueError("Mechanism file must contain a mapping")
    return ReactionNetworkSpec.from_dict(payload)


def perturb_network_parameters(
    network: ReactionNetworkSpec,
    *,
    seed: int,
    relative_std: float = 0.05,
) -> ReactionNetworkSpec:
    if relative_std < 0:
        raise ValueError("relative_std cannot be negative")
    rng = np.random.default_rng(seed)
    reactions = []
    for reaction in network.reactions:
        params = dict(reaction.rate_law.parameters)
        if "A" in params and isinstance(params["A"], int | float):
            factor = float(np.exp(rng.normal(0.0, relative_std)))
            params["A"] = float(params["A"]) * factor
        elif "k" in params and isinstance(params["k"], int | float):
            factor = float(np.exp(rng.normal(0.0, relative_std)))
            params["k"] = float(params["k"]) * factor
        reactions.append(
            replace(
                reaction,
                rate_law=replace(reaction.rate_law, parameters=params),
            )
        )
    return replace(
        network,
        reactions=tuple(reactions),
        metadata={**network.metadata, "parameter_perturbation_seed": seed},
    )


def _mass_action_rate(
    reactants: Mapping[str, float],
    concentrations_mol_L: Mapping[str, float],
    k: float,
) -> float:
    if k < 0 or not isfinite(k):
        raise ValueError("Rate coefficient must be finite and nonnegative")
    rate = k
    for species_id, order in reactants.items():
        concentration = max(float(concentrations_mol_L.get(species_id, 0.0)), 0.0)
        rate *= concentration**order
    return rate


def _arrhenius_k(params: Mapping[str, object], temperature_K: float) -> float:
    A = _float_param(params, "A", default=_float_param(params, "k", default=0.0))
    b = _float_param(params, "b", default=0.0)
    Ea = _float_param(
        params,
        "Ea_J_per_mol",
        default=_float_param(params, "Ea", default=0.0),
    )
    return A * temperature_K**b * exp(-Ea / (R_J_PER_MOL_K * temperature_K))


def _reaction_order_delta(reaction: ReactionSpec) -> float:
    return sum(reaction.stoichiometry.values())


def _reverse_rate_constant(
    reaction: ReactionSpec,
    params: Mapping[str, object],
    *,
    temperature_K: float,
    forward_rate_constant: float,
    species_thermo: Mapping[str, Any] | None,
) -> float:
    if "A_reverse" in params:
        return _arrhenius_k(_reverse_params(params), temperature_K)
    if "K_eq" in params:
        K_eq = _float_param(params, "K_eq")
        if K_eq <= 0:
            raise ValueError("K_eq must be positive")
        return reverse_rate_constant_from_equilibrium(
            forward_rate_constant=forward_rate_constant,
            concentration_equilibrium_constant=K_eq,
        )
    source = str(params.get("K_eq_source", params.get("equilibrium_source", ""))).lower()
    if source in {"nasa7", "species_thermo", "thermochemistry"}:
        if species_thermo is None:
            raise ValueError("NASA7 reversible_arrhenius requires species_thermo")
        standard_concentration = _float_param(
            params,
            "standard_concentration_mol_L",
            default=1.0,
        )
        return thermochemical_detailed_balance(
            reaction,
            species_thermo=species_thermo,
            temperature_K=temperature_K,
            standard_concentration_mol_L=standard_concentration,
        ).reverse_rate_constant
    raise ValueError(
        "reversible_arrhenius requires A_reverse, K_eq, or K_eq_source='nasa7'"
    )


def _reverse_params(params: Mapping[str, object]) -> dict[str, object]:
    if "A_reverse" in params:
        return {
            "A": params["A_reverse"],
            "b": params.get("b_reverse", 0.0),
            "Ea_J_per_mol": params.get(
                "Ea_reverse_J_per_mol",
                params.get("Ea_reverse", 0.0),
            ),
        }
    if "K_eq" in params:
        K_eq = _float_param(params, "K_eq")
        if K_eq <= 0:
            raise ValueError("K_eq must be positive")
        return {
            "A": _float_param(params, "A", default=0.0) / K_eq,
            "b": params.get("b", 0.0),
            "Ea_J_per_mol": params.get("Ea_J_per_mol", params.get("Ea", 0.0)),
        }
    raise ValueError("reversible_arrhenius requires A_reverse or K_eq")


def _positive_reaction_parameter(
    network: ReactionNetworkSpec,
    reaction_id: str,
    parameter_name: str,
) -> float:
    reaction = _reaction_by_id(network, reaction_id)
    if parameter_name not in reaction.rate_law.parameters:
        raise ValueError(f"Reaction {reaction_id!r} has no parameter {parameter_name!r}")
    value = reaction.rate_law.parameters[parameter_name]
    if not isinstance(value, int | float | str):
        raise ValueError(
            f"Reaction parameter {reaction_id}.{parameter_name} must be numeric"
        )
    numeric = float(value)
    if numeric <= 0 or not isfinite(numeric):
        raise ValueError(
            f"Reaction parameter {reaction_id}.{parameter_name} must be finite and positive"
        )
    return numeric


def _with_reaction_parameter(
    network: ReactionNetworkSpec,
    reaction_id: str,
    parameter_name: str,
    value: float,
) -> ReactionNetworkSpec:
    if value <= 0 or not isfinite(value):
        raise ValueError("perturbed reaction parameter must be finite and positive")
    reactions: list[ReactionSpec] = []
    found = False
    for reaction in network.reactions:
        if reaction.reaction_id != reaction_id:
            reactions.append(reaction)
            continue
        found = True
        if parameter_name not in reaction.rate_law.parameters:
            raise ValueError(
                f"Reaction {reaction_id!r} has no parameter {parameter_name!r}"
            )
        params = dict(reaction.rate_law.parameters)
        params[parameter_name] = value
        reactions.append(
            replace(
                reaction,
                rate_law=replace(reaction.rate_law, parameters=params),
            )
        )
    if not found:
        raise ValueError(f"Unknown reaction id: {reaction_id}")
    return replace(network, reactions=tuple(reactions))


def _reaction_by_id(network: ReactionNetworkSpec, reaction_id: str) -> ReactionSpec:
    for reaction in network.reactions:
        if reaction.reaction_id == reaction_id:
            return reaction
    raise ValueError(f"Unknown reaction id: {reaction_id}")


def _float_param(
    params: Mapping[str, object],
    key: str,
    *,
    default: float | None = None,
) -> float:
    if key not in params:
        if default is None:
            raise ValueError(f"Missing numeric rate-law parameter: {key}")
        return default
    value = params[key]
    if isinstance(value, int | float | str):
        return float(value)
    raise ValueError(f"Rate-law parameter {key} must be numeric, got {type(value).__name__}")
