"""General reaction-network engine for ChemWorld."""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field, replace
from math import isfinite
from pathlib import Path
from typing import Any

import numpy as np
import yaml

from chemworld.physchem import reaction_network_specs as network_specs
from chemworld.physchem import reaction_rate_laws as rate_laws
from chemworld.physchem import reaction_reference_cases as reference_cases
from chemworld.physchem import reaction_sensitivity as sensitivity
from chemworld.physchem.elements import element_matrix
from chemworld.physchem.solver_backend import DEFAULT_REACTION_ODE_POLICY, solve_ode

Arrow = network_specs.Arrow
RateLawSpec = network_specs.RateLawSpec
ReactionSpec = network_specs.ReactionSpec
SpeciesSpec = network_specs.SpeciesSpec
parse_reaction_equation = network_specs.parse_reaction_equation
reaction_from_dict = network_specs.reaction_from_dict
species_from_dict = network_specs.species_from_dict
R_J_PER_MOL_K = rate_laws.R_J_PER_MOL_K
reverse_rate_constant_from_equilibrium = rate_laws.reverse_rate_constant_from_equilibrium
effective_third_body_concentration = rate_laws.effective_third_body_concentration
falloff_reduced_pressure = rate_laws.falloff_reduced_pressure
lindemann_falloff_rate_constant = rate_laws.lindemann_falloff_rate_constant
prefixed_arrhenius_params = rate_laws.prefixed_arrhenius_params
third_body_efficiencies = rate_laws.third_body_efficiencies
troe_broadening_factor = rate_laws.troe_broadening_factor
troe_falloff_rate_constant = rate_laws.troe_falloff_rate_constant
_arrhenius_k = rate_laws.arrhenius_k
_evaluate_rate_law = rate_laws.evaluate_rate_law
_float_param = rate_laws.float_param
_reaction_order_delta = rate_laws.reaction_order_delta
AnalyticalODECase = reference_cases.AnalyticalODECase
ReactionODEReferenceCase = reference_cases.ReactionODEReferenceCase
ReactionODEReferenceResult = reference_cases.ReactionODEReferenceResult
cantera_comparable_reaction_cases = reference_cases.cantera_comparable_reaction_cases
integrate_reaction_ode_reference_case = reference_cases.integrate_reaction_ode_reference_case
evaluate_reaction_ode_reference_case = reference_cases.evaluate_reaction_ode_reference_case
ReactionSensitivityEntry = sensitivity.ReactionSensitivityEntry
ReactionSensitivityReport = sensitivity.ReactionSensitivityReport
finite_difference_reaction_sensitivities = sensitivity.finite_difference_reaction_sensitivities
kinetic_sensitivity_parameter_candidates = sensitivity.kinetic_sensitivity_parameter_candidates


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
        report = solve_ode(
            rhs,
            y0,
            time_span_s=(0.0, duration_s),
            evaluation_times_s=t_eval,
            policy=DEFAULT_REACTION_ODE_POLICY,
        )
        report.raise_for_failure("Reaction-network integration")
        result = report.raw_result
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
            solver_diagnostic=report.diagnostic.to_dict(),
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
                raise ValueError(f"Species amount cannot be negative: {species_id}={amount}")
            concentrations[species_id] = max(amount, 0.0) / volume_L
        return concentrations


@dataclass(frozen=True)
class BatchIntegrationResult:
    network_id: str
    species_ids: tuple[str, ...]
    times_s: tuple[float, ...]
    amounts_mol: tuple[tuple[float, ...], ...]
    final_amounts_mol: dict[str, float]
    solver_diagnostic: dict[str, object] = field(default_factory=dict)

    def to_dict(self) -> dict[str, object]:
        return {
            "network_id": self.network_id,
            "species_ids": list(self.species_ids),
            "times_s": list(self.times_s),
            "amounts_mol": [list(row) for row in self.amounts_mol],
            "final_amounts_mol": dict(self.final_amounts_mol),
            "solver_diagnostic": dict(self.solver_diagnostic),
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
            "concentration_equilibrium_constant": (self.concentration_equilibrium_constant),
            "dimensionless_equilibrium_constant": (self.dimensionless_equilibrium_constant),
            "delta_g_J_mol": self.delta_g_J_mol,
            "reaction_order_delta": self.reaction_order_delta,
            "standard_concentration_mol_L": self.standard_concentration_mol_L,
            "source": self.source,
        }


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
    if concentration_equilibrium_constant <= 0 or not isfinite(concentration_equilibrium_constant):
        raise ValueError("thermochemical concentration equilibrium constant is invalid")
    return (
        concentration_equilibrium_constant,
        thermo_result.equilibrium_constant,
        thermo_result.delta_g_J_mol,
    )


def evaluate_rate_law(
    reaction: ReactionSpec,
    *,
    concentrations_mol_L: Mapping[str, float],
    temperature_K: float,
    species_thermo: Mapping[str, Any] | None = None,
) -> float:
    return _evaluate_rate_law(
        reaction,
        concentrations_mol_L=concentrations_mol_L,
        temperature_K=temperature_K,
        species_thermo=species_thermo,
        thermochemical_reverse_rate_constant=_thermochemical_reverse_rate_constant,
    )


def _thermochemical_reverse_rate_constant(
    reaction: ReactionSpec,
    params: Mapping[str, object],
    temperature_K: float,
    species_thermo: Mapping[str, Any],
) -> float:
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
