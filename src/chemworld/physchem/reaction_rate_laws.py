"""Rate-law evaluation helpers for reaction networks."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import replace
from math import exp, isfinite
from typing import Any, Protocol, TypeVar, cast

from chemworld.physchem.reaction_network_specs import ReactionSpec

R_J_PER_MOL_K = 8.31446261815324


class ReactionNetworkLike(Protocol):
    @property
    def reactions(self) -> tuple[ReactionSpec, ...]: ...


NetworkT = TypeVar("NetworkT", bound=ReactionNetworkLike)
ThermochemicalReverseRate = Callable[
    [ReactionSpec, Mapping[str, object], float, Mapping[str, Any]],
    float,
]


def evaluate_rate_law(
    reaction: ReactionSpec,
    *,
    concentrations_mol_L: Mapping[str, float],
    temperature_K: float,
    species_thermo: Mapping[str, Any] | None = None,
    thermochemical_reverse_rate_constant: ThermochemicalReverseRate | None = None,
) -> float:
    if temperature_K <= 0:
        raise ValueError("temperature_K must be positive")
    params = reaction.rate_law.parameters
    equation_id = reaction.rate_law.equation_id
    if equation_id == "mass_action":
        return mass_action_rate(
            reaction.reactants,
            concentrations_mol_L,
            float(params["k"]),
        )
    if equation_id in {"arrhenius", "modified_arrhenius"}:
        k = arrhenius_k(params, temperature_K)
        return mass_action_rate(reaction.reactants, concentrations_mol_L, k)
    if equation_id == "reversible_arrhenius":
        forward_rate_constant = arrhenius_k(params, temperature_K)
        forward = mass_action_rate(
            reaction.reactants,
            concentrations_mol_L,
            forward_rate_constant,
        )
        reverse_k = reverse_rate_constant(
            reaction,
            params,
            temperature_K=temperature_K,
            forward_rate_constant=forward_rate_constant,
            species_thermo=species_thermo,
            thermochemical_reverse_rate_constant=thermochemical_reverse_rate_constant,
        )
        reverse = mass_action_rate(
            reaction.products,
            concentrations_mol_L,
            reverse_k,
        )
        return forward - reverse
    if equation_id == "catalytic_activity":
        base = mass_action_rate(
            reaction.reactants,
            concentrations_mol_L,
            arrhenius_k(params, temperature_K),
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
        return arrhenius_k(params, temperature_K) * max(
            concentrations_mol_L.get(species, 0.0),
            0.0,
        )
    if equation_id == "langmuir_hinshelwood":
        k = arrhenius_k(params, temperature_K)
        numerator = mass_action_rate(reaction.reactants, concentrations_mol_L, k)
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


def mass_action_rate(
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


def arrhenius_k(params: Mapping[str, object], temperature_K: float) -> float:
    A = float_param(params, "A", default=float_param(params, "k", default=0.0))
    b = float_param(params, "b", default=0.0)
    Ea = float_param(
        params,
        "Ea_J_per_mol",
        default=float_param(params, "Ea", default=0.0),
    )
    return A * temperature_K**b * exp(-Ea / (R_J_PER_MOL_K * temperature_K))


def reaction_order_delta(reaction: ReactionSpec) -> float:
    return sum(reaction.stoichiometry.values())


def reverse_rate_constant(
    reaction: ReactionSpec,
    params: Mapping[str, object],
    *,
    temperature_K: float,
    forward_rate_constant: float,
    species_thermo: Mapping[str, Any] | None,
    thermochemical_reverse_rate_constant: ThermochemicalReverseRate | None,
) -> float:
    if "A_reverse" in params:
        return arrhenius_k(reverse_params(params), temperature_K)
    if "K_eq" in params:
        K_eq = float_param(params, "K_eq")
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
        if thermochemical_reverse_rate_constant is None:
            raise ValueError(
                "NASA7 reversible_arrhenius requires thermochemical reverse-rate callback"
            )
        return thermochemical_reverse_rate_constant(
            reaction,
            params,
            temperature_K,
            species_thermo,
        )
    raise ValueError(
        "reversible_arrhenius requires A_reverse, K_eq, or K_eq_source='nasa7'"
    )


def reverse_params(params: Mapping[str, object]) -> dict[str, object]:
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
        K_eq = float_param(params, "K_eq")
        if K_eq <= 0:
            raise ValueError("K_eq must be positive")
        return {
            "A": float_param(params, "A", default=0.0) / K_eq,
            "b": params.get("b", 0.0),
            "Ea_J_per_mol": params.get("Ea_J_per_mol", params.get("Ea", 0.0)),
        }
    raise ValueError("reversible_arrhenius requires A_reverse or K_eq")


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


def positive_reaction_parameter(
    network: ReactionNetworkLike,
    reaction_id: str,
    parameter_name: str,
) -> float:
    reaction = reaction_by_id(network, reaction_id)
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


def with_reaction_parameter(
    network: NetworkT,
    reaction_id: str,
    parameter_name: str,
    value: float,
) -> NetworkT:
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
    return cast(NetworkT, replace(cast(Any, network), reactions=tuple(reactions)))


def reaction_by_id(network: ReactionNetworkLike, reaction_id: str) -> ReactionSpec:
    for reaction in network.reactions:
        if reaction.reaction_id == reaction_id:
            return reaction
    raise ValueError(f"Unknown reaction id: {reaction_id}")


def float_param(
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
    raise ValueError(
        f"Rate-law parameter {key} must be numeric, got {type(value).__name__}"
    )


__all__ = [
    "R_J_PER_MOL_K",
    "ReactionNetworkLike",
    "ThermochemicalReverseRate",
    "arrhenius_k",
    "evaluate_rate_law",
    "float_param",
    "mass_action_rate",
    "positive_reaction_parameter",
    "reaction_by_id",
    "reaction_order_delta",
    "reverse_params",
    "reverse_rate_constant",
    "reverse_rate_constant_from_equilibrium",
    "with_reaction_parameter",
]
