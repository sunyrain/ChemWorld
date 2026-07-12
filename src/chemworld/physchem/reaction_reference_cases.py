"""Analytical ODE reference cases for reaction-network validation."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from math import exp
from typing import Any, Literal, Protocol

import numpy as np
from scipy.integrate import solve_ivp

from chemworld.physchem.reaction_network_specs import (
    RateLawSpec,
    ReactionSpec,
    SpeciesSpec,
)

AnalyticalODECase = Literal["irreversible_first_order", "reversible_first_order"]


class BatchIntegrationResultLike(Protocol):
    @property
    def species_ids(self) -> tuple[str, ...]: ...

    @property
    def times_s(self) -> tuple[float, ...]: ...

    @property
    def amounts_mol(self) -> tuple[tuple[float, ...], ...]: ...

    @property
    def final_amounts_mol(self) -> dict[str, float]: ...


class ReactionNetworkReference(Protocol):
    @property
    def species_ids(self) -> tuple[str, ...]: ...

    def integrate_batch(
        self,
        initial_amounts_mol: Mapping[str, float],
        *,
        volume_L: float,
        temperature_K: float,
        duration_s: float,
        evaluation_times_s: Sequence[float] | None = None,
        species_thermo: Mapping[str, Any] | None = None,
    ) -> BatchIntegrationResultLike: ...

    def to_dict(self) -> dict[str, object]: ...

    def amount_derivatives(
        self,
        amounts_mol: Mapping[str, float],
        *,
        volume_L: float,
        temperature_K: float,
        species_thermo: Mapping[str, Any] | None = None,
    ) -> dict[str, float]: ...


@dataclass(frozen=True)
class ReactionODEReferenceCase:
    """A small, auditable ODE case with an analytical solution."""

    case_id: str
    title: str
    network: ReactionNetworkReference
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
                    amount_a
                    if species_id == "A"
                    else amount_b
                    if species_id == "B"
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
                    amount_a
                    if species_id == "A"
                    else amount_b
                    if species_id == "B"
                    else self.initial_amounts_mol.get(species_id, 0.0)
                )
                for species_id in self.network.species_ids
            }
        raise ValueError(f"Unsupported analytical ODE case: {self.analytical_case}")

    def analytical_trajectory_mol(self) -> tuple[dict[str, float], ...]:
        return tuple(self.analytical_amounts_mol(time_s) for time_s in self.evaluation_times_s)

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
class IndependentSciPyReferenceResult:
    """Cross-check against a separately invoked SciPy solver boundary."""

    case_id: str
    method: str
    passed: bool
    max_abs_error_mol: float
    rtol: float
    atol_mol: float
    nfev: int

    def to_dict(self) -> dict[str, object]:
        return {
            "case_id": self.case_id,
            "method": self.method,
            "passed": self.passed,
            "max_abs_error_mol": self.max_abs_error_mol,
            "rtol": self.rtol,
            "atol_mol": self.atol_mol,
            "nfev": self.nfev,
            "backend": "scipy.integrate.solve_ivp (independent invocation)",
        }


def cantera_comparable_reaction_cases() -> tuple[ReactionODEReferenceCase, ...]:
    """Return ChemWorld-owned constant-volume ODE reference cases."""

    from chemworld.physchem.reaction_network import ReactionNetworkSpec

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
) -> BatchIntegrationResultLike:
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


def evaluate_against_independent_scipy(
    case: ReactionODEReferenceCase,
    *,
    method: Literal["RK45", "DOP853", "Radau", "BDF"] = "DOP853",
    rtol: float = 1.0e-10,
    atol_mol: float = 1.0e-12,
    comparison_rtol: float = 2.0e-7,
    comparison_atol_mol: float = 2.0e-9,
) -> IndependentSciPyReferenceResult:
    """Compare ChemWorld integration to a direct, separately configured solve_ivp.

    This does not claim an independent physics library.  It verifies the public
    network contract across a separate solver invocation, method, and tolerance
    policy; optional Cantera checks remain a distinct boundary.
    """

    if min(rtol, atol_mol, comparison_rtol, comparison_atol_mol) <= 0.0:
        raise ValueError("reference and comparison tolerances must be positive")
    species_ids = case.network.species_ids
    y0 = np.asarray(
        [case.initial_amounts_mol.get(species_id, 0.0) for species_id in species_ids],
        dtype=float,
    )

    def independent_rhs(_time_s: float, y: np.ndarray) -> np.ndarray:
        amounts = {
            species_id: max(float(value), 0.0)
            for species_id, value in zip(species_ids, y, strict=True)
        }
        derivatives = case.network.amount_derivatives(
            amounts,
            volume_L=case.volume_L,
            temperature_K=case.temperature_K,
        )
        return np.asarray([derivatives[species_id] for species_id in species_ids])

    independent = solve_ivp(
        independent_rhs,
        (0.0, case.duration_s),
        y0,
        method=method,
        t_eval=np.asarray(case.evaluation_times_s, dtype=float),
        rtol=rtol,
        atol=atol_mol,
    )
    if not independent.success:
        raise RuntimeError(f"independent SciPy reference failed: {independent.message}")
    chemworld = integrate_reaction_ode_reference_case(case)
    chemworld_values = np.asarray(chemworld.amounts_mol, dtype=float)
    independent_values = np.asarray(independent.y, dtype=float)
    errors = np.abs(chemworld_values - independent_values)
    limits = comparison_atol_mol + comparison_rtol * np.abs(independent_values)
    return IndependentSciPyReferenceResult(
        case_id=case.case_id,
        method=method,
        passed=bool(np.all(errors <= limits)),
        max_abs_error_mol=float(np.max(errors)),
        rtol=rtol,
        atol_mol=atol_mol,
        nfev=int(independent.nfev),
    )


__all__ = [
    "AnalyticalODECase",
    "BatchIntegrationResultLike",
    "IndependentSciPyReferenceResult",
    "ReactionNetworkReference",
    "ReactionODEReferenceCase",
    "ReactionODEReferenceResult",
    "cantera_comparable_reaction_cases",
    "evaluate_against_independent_scipy",
    "evaluate_reaction_ode_reference_case",
    "integrate_reaction_ode_reference_case",
]
