"""General reaction-network engine for ChemWorld."""

from __future__ import annotations

import json
import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field, replace
from math import exp, isfinite
from pathlib import Path
from typing import Any, Literal

import numpy as np
import yaml
from scipy.integrate import solve_ivp

from chemworld.physchem.elements import element_matrix, parse_formula

R_J_PER_MOL_K = 8.31446261815324
Arrow = Literal["=>", "<=>"]


@dataclass(frozen=True)
class SpeciesSpec:
    species_id: str
    formula: str
    phase: str = "liquid"
    charge: int = 0
    catalyst: bool = False
    observable_aliases: tuple[str, ...] = ()
    metadata: dict[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.species_id:
            raise ValueError("species_id cannot be empty")
        parse_formula(self.formula)
        object.__setattr__(self, "observable_aliases", tuple(self.observable_aliases))

    @property
    def composition(self) -> dict[str, float]:
        return parse_formula(self.formula)

    def to_dict(self) -> dict[str, object]:
        return {
            "species_id": self.species_id,
            "formula": self.formula,
            "composition": self.composition,
            "phase": self.phase,
            "charge": self.charge,
            "catalyst": self.catalyst,
            "observable_aliases": list(self.observable_aliases),
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True)
class RateLawSpec:
    rate_law_id: str
    equation_id: str
    parameters: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.rate_law_id:
            raise ValueError("rate_law_id cannot be empty")
        if self.equation_id not in {
            "mass_action",
            "arrhenius",
            "modified_arrhenius",
            "reversible_arrhenius",
            "catalytic_activity",
            "catalyst_deactivation",
            "langmuir_hinshelwood",
            "michaelis_menten",
        }:
            raise ValueError(f"Unsupported rate law: {self.equation_id}")

    def to_dict(self) -> dict[str, object]:
        return {
            "rate_law_id": self.rate_law_id,
            "equation_id": self.equation_id,
            "parameters": dict(self.parameters),
        }


@dataclass(frozen=True)
class ReactionSpec:
    reaction_id: str
    equation: str
    stoichiometry: dict[str, float]
    reversible: bool
    rate_law: RateLawSpec
    delta_h_J_per_mol: float = 0.0
    equilibrium_model_id: str = ""
    metadata: dict[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.reaction_id:
            raise ValueError("reaction_id cannot be empty")
        if not self.stoichiometry:
            raise ValueError("Reaction stoichiometry cannot be empty")
        if not any(value < 0 for value in self.stoichiometry.values()):
            raise ValueError("Reaction must contain at least one reactant")
        if not any(value > 0 for value in self.stoichiometry.values()):
            raise ValueError("Reaction must contain at least one product")
        if any(value == 0 for value in self.stoichiometry.values()):
            raise ValueError("Zero stoichiometric coefficients are not stored")

    @classmethod
    def from_equation(
        cls,
        *,
        reaction_id: str,
        equation: str,
        rate_law: RateLawSpec,
        delta_h_J_per_mol: float = 0.0,
        equilibrium_model_id: str = "",
        metadata: dict[str, object] | None = None,
    ) -> ReactionSpec:
        stoichiometry, reversible = parse_reaction_equation(equation)
        return cls(
            reaction_id=reaction_id,
            equation=equation,
            stoichiometry=stoichiometry,
            reversible=reversible,
            rate_law=rate_law,
            delta_h_J_per_mol=delta_h_J_per_mol,
            equilibrium_model_id=equilibrium_model_id,
            metadata={} if metadata is None else dict(metadata),
        )

    @property
    def reactants(self) -> dict[str, float]:
        return {
            species_id: -coefficient
            for species_id, coefficient in self.stoichiometry.items()
            if coefficient < 0
        }

    @property
    def products(self) -> dict[str, float]:
        return {
            species_id: coefficient
            for species_id, coefficient in self.stoichiometry.items()
            if coefficient > 0
        }

    def to_dict(self) -> dict[str, object]:
        return {
            "reaction_id": self.reaction_id,
            "equation": self.equation,
            "stoichiometry": dict(self.stoichiometry),
            "reversible": self.reversible,
            "rate_law": self.rate_law.to_dict(),
            "delta_h_J_per_mol": self.delta_h_J_per_mol,
            "equilibrium_model_id": self.equilibrium_model_id,
            "metadata": dict(self.metadata),
        }


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
    ) -> dict[str, float]:
        concentrations = self._concentrations(amounts_mol, volume_L=volume_L)
        return {
            reaction.reaction_id: evaluate_rate_law(
                reaction,
                concentrations_mol_L=concentrations,
                temperature_K=temperature_K,
            )
            for reaction in self.reactions
        }

    def amount_derivatives(
        self,
        amounts_mol: Mapping[str, float],
        *,
        volume_L: float,
        temperature_K: float,
    ) -> dict[str, float]:
        rates = self.reaction_rates(
            amounts_mol,
            volume_L=volume_L,
            temperature_K=temperature_K,
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
        species = tuple(_species_from_dict(item) for item in payload["species"])
        reactions = tuple(_reaction_from_dict(item) for item in payload["reactions"])
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


def parse_reaction_equation(equation: str) -> tuple[dict[str, float], bool]:
    if "<=>" in equation:
        left, right = equation.split("<=>", 1)
        reversible = True
    elif "=>" in equation:
        left, right = equation.split("=>", 1)
        reversible = False
    elif "->" in equation:
        left, right = equation.split("->", 1)
        reversible = False
    else:
        raise ValueError(f"Reaction equation is missing an arrow: {equation}")
    stoichiometry: dict[str, float] = {}
    _merge_side(stoichiometry, left, sign=-1.0)
    _merge_side(stoichiometry, right, sign=1.0)
    cleaned = {
        species_id: value
        for species_id, value in stoichiometry.items()
        if value != 0.0
    }
    return cleaned, reversible


def evaluate_rate_law(
    reaction: ReactionSpec,
    *,
    concentrations_mol_L: Mapping[str, float],
    temperature_K: float,
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
        forward = _mass_action_rate(
            reaction.reactants,
            concentrations_mol_L,
            _arrhenius_k(params, temperature_K),
        )
        reverse_params = _reverse_params(params)
        reverse = _mass_action_rate(
            reaction.products,
            concentrations_mol_L,
            _arrhenius_k(reverse_params, temperature_K),
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


def _species_from_dict(payload: Mapping[str, Any]) -> SpeciesSpec:
    return SpeciesSpec(
        species_id=str(payload["species_id"]),
        formula=str(payload["formula"]),
        phase=str(payload.get("phase", "liquid")),
        charge=int(payload.get("charge", 0)),
        catalyst=bool(payload.get("catalyst", False)),
        observable_aliases=tuple(
            str(value) for value in payload.get("observable_aliases", ())
        ),
        metadata=dict(payload.get("metadata", {})),
    )


def _reaction_from_dict(payload: Mapping[str, Any]) -> ReactionSpec:
    rate_payload = payload["rate_law"]
    rate_law = RateLawSpec(
        rate_law_id=str(rate_payload["rate_law_id"]),
        equation_id=str(rate_payload["equation_id"]),
        parameters=dict(rate_payload.get("parameters", {})),
    )
    if "stoichiometry" in payload:
        stoichiometry = {
            str(key): float(value) for key, value in payload["stoichiometry"].items()
        }
        reversible = bool(payload.get("reversible", "<=>" in str(payload.get("equation", ""))))
        return ReactionSpec(
            reaction_id=str(payload["reaction_id"]),
            equation=str(payload.get("equation", "")),
            stoichiometry=stoichiometry,
            reversible=reversible,
            rate_law=rate_law,
            delta_h_J_per_mol=float(payload.get("delta_h_J_per_mol", 0.0)),
            equilibrium_model_id=str(payload.get("equilibrium_model_id", "")),
            metadata=dict(payload.get("metadata", {})),
        )
    return ReactionSpec.from_equation(
        reaction_id=str(payload["reaction_id"]),
        equation=str(payload["equation"]),
        rate_law=rate_law,
        delta_h_J_per_mol=float(payload.get("delta_h_J_per_mol", 0.0)),
        equilibrium_model_id=str(payload.get("equilibrium_model_id", "")),
        metadata=dict(payload.get("metadata", {})),
    )


def _merge_side(stoichiometry: dict[str, float], side: str, *, sign: float) -> None:
    for token in side.split("+"):
        token = token.strip()
        if not token:
            continue
        coefficient, species_id = _parse_species_term(token)
        stoichiometry[species_id] = stoichiometry.get(species_id, 0.0) + sign * coefficient


_TERM_RE = re.compile(r"^(?:(\d+(?:\.\d*)?|\.\d+)\s+)?([A-Za-z_][A-Za-z0-9_().-]*)$")


def _parse_species_term(token: str) -> tuple[float, str]:
    match = _TERM_RE.match(token)
    if not match:
        raise ValueError(f"Invalid reaction term: {token}")
    coefficient = 1.0 if match.group(1) is None else float(match.group(1))
    if coefficient <= 0:
        raise ValueError(f"Reaction coefficients must be positive: {token}")
    return coefficient, match.group(2)


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
