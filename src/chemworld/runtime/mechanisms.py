"""Mechanism compilation for ChemWorld runtime v2."""

from __future__ import annotations

import json
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Any

import yaml

from chemworld.physchem.mechanism_library import (
    MechanismScenarioCard,
    get_mechanism_card,
    list_mechanism_cards,
    load_library_mechanism,
)
from chemworld.physchem.reaction_network import ReactionNetworkSpec

MECHANISM_SCHEMA_VERSION = "chemworld_mechanism_v1"

SCENARIO_MECHANISM_DEFAULTS = {
    "reaction-optimization": "simple_batch_reaction",
    "reaction-safety": "catalyst_deactivation",
    "reaction-mechanism": "autocatalytic_reaction",
    "reaction-to-assay": "simple_batch_reaction",
    "reaction-to-purification": "reaction_extraction",
    "reaction-to-crystallization": "simple_batch_reaction",
    "reaction-to-distillation": "reactive_distillation_lite",
    "flow-reaction-optimization": "pfr_hotspot",
    "electrochemical-conversion": "electrochemical_conversion",
    "partition-discovery": "reaction_extraction",
    "purity-yield-tradeoff": "reaction_extraction",
    "generalization": "parallel_series_reaction",
    "low-budget-characterization": "autocatalytic_reaction",
    "tool-agent-planning": "reaction_extraction",
}


@dataclass(frozen=True)
class ScoreSpec:
    target_species: tuple[str, ...]
    impurity_species: tuple[str, ...]
    initial_limiting_species: str | None

    @property
    def reactant_species(self) -> str | None:
        return self.initial_limiting_species

    @property
    def product_species(self) -> str | None:
        return self.target_species[0] if self.target_species else None

    def to_dict(self) -> dict[str, Any]:
        return {
            "target_species": list(self.target_species),
            "impurity_species": list(self.impurity_species),
            "initial_limiting_species": self.initial_limiting_species,
        }


@dataclass(frozen=True)
class CompiledMechanism:
    mechanism_id: str
    mechanism_version: str
    mechanism_hash: str
    network: ReactionNetworkSpec
    species_index: dict[str, int]
    stoichiometric_matrix: tuple[tuple[float, ...], ...]
    reaction_enthalpies: dict[str, float]
    species_roles: dict[str, tuple[str, ...]]
    observable_mapping: dict[str, tuple[str, ...]]
    score_spec: ScoreSpec
    initial_amount_policy: dict[str, float]

    def to_dict(self) -> dict[str, Any]:
        return {
            "mechanism_id": self.mechanism_id,
            "mechanism_version": self.mechanism_version,
            "mechanism_hash": self.mechanism_hash,
            "species_index": dict(self.species_index),
            "stoichiometric_matrix": [list(row) for row in self.stoichiometric_matrix],
            "reaction_enthalpies": dict(self.reaction_enthalpies),
            "species_roles": {
                species_id: list(roles) for species_id, roles in self.species_roles.items()
            },
            "observable_mapping": {
                key: list(value) for key, value in self.observable_mapping.items()
            },
            "score_spec": self.score_spec.to_dict(),
            "initial_amount_policy": dict(self.initial_amount_policy),
        }


def compile_mechanism_for_scenario(scenario_id: str) -> CompiledMechanism:
    mechanism_id = mechanism_id_for_scenario(scenario_id)
    return compile_mechanism(mechanism_id, require_runtime_roles=True)


def mechanism_id_for_scenario(scenario_id: str) -> str:
    if scenario_id in SCENARIO_MECHANISM_DEFAULTS:
        return SCENARIO_MECHANISM_DEFAULTS[scenario_id]
    for card in list_mechanism_cards():
        if card.scenario_id == scenario_id:
            return card.mechanism_id
    return "simple_batch_reaction"


def compile_mechanism(
    card_or_mechanism_id: str | MechanismScenarioCard,
    *,
    require_runtime_roles: bool | None = None,
) -> CompiledMechanism:
    card = (
        card_or_mechanism_id
        if isinstance(card_or_mechanism_id, MechanismScenarioCard)
        else get_mechanism_card(card_or_mechanism_id)
    )
    _validate_raw_mechanism_schema(card.resolved_mechanism_path)
    network = load_library_mechanism(card)
    species_roles = {
        species.species_id: tuple(species.observable_aliases)
        for species in network.species
    }
    observable_mapping = _observable_mapping(network, card)
    initial_limiting_species = _initial_limiting_species(card)
    _validate_compiled_role_contract(
        network,
        card,
        observable_mapping=observable_mapping,
        initial_limiting_species=initial_limiting_species,
        require_runtime_roles=(
            card.scenario_id in SCENARIO_MECHANISM_DEFAULTS
            if require_runtime_roles is None
            else require_runtime_roles
        ),
    )
    return CompiledMechanism(
        mechanism_id=network.network_id,
        mechanism_version=MECHANISM_SCHEMA_VERSION,
        mechanism_hash=mechanism_hash(card.resolved_mechanism_path),
        network=network,
        species_index=network.species_index,
        stoichiometric_matrix=network.stoichiometric_matrix(),
        reaction_enthalpies={
            reaction.reaction_id: reaction.delta_h_J_per_mol
            for reaction in network.reactions
        },
        species_roles=species_roles,
        observable_mapping=observable_mapping,
        score_spec=ScoreSpec(
            target_species=card.target_species,
            impurity_species=card.impurity_species,
            initial_limiting_species=initial_limiting_species,
        ),
        initial_amount_policy=dict(card.initial_amounts_mol),
    )


def mechanism_hash(path: str | Path) -> str:
    payload = _raw_mechanism_payload(Path(path))
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return sha256(canonical.encode("utf-8")).hexdigest()


def _validate_raw_mechanism_schema(path: Path) -> None:
    payload = _raw_mechanism_payload(path)
    schema_version = str(payload.get("schema_version", ""))
    if schema_version != MECHANISM_SCHEMA_VERSION:
        raise ValueError(
            f"Unsupported mechanism schema_version={schema_version!r}; "
            f"expected {MECHANISM_SCHEMA_VERSION!r}"
        )


def _raw_mechanism_payload(path: Path) -> dict[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Mechanism file must contain a mapping: {path}")
    return payload


def _observable_mapping(
    network: ReactionNetworkSpec,
    card: MechanismScenarioCard,
) -> dict[str, tuple[str, ...]]:
    roles: dict[str, list[str]] = {
        "reactant": [],
        "target": list(card.target_species),
        "impurity": list(card.impurity_species),
        "product": list(card.target_species),
        "byproduct": [],
        "degradation": [],
        "catalyst": [],
    }
    for species in network.species:
        aliases = set(species.observable_aliases)
        if "reactant" in aliases or "oxidized_reactant" in aliases:
            roles["reactant"].append(species.species_id)
        if "side_product" in aliases or "byproduct" in aliases:
            roles["byproduct"].append(species.species_id)
        if "degradation_product" in aliases or species.species_id.lower().startswith("d"):
            roles["degradation"].append(species.species_id)
        if species.catalyst or "catalyst" in aliases:
            roles["catalyst"].append(species.species_id)
    return {key: tuple(dict.fromkeys(value)) for key, value in roles.items()}


def _initial_limiting_species(card: MechanismScenarioCard) -> str | None:
    positive = [
        species_id
        for species_id, amount in card.initial_amounts_mol.items()
        if amount > 0.0
    ]
    return positive[0] if positive else None


def _validate_compiled_role_contract(
    network: ReactionNetworkSpec,
    card: MechanismScenarioCard,
    *,
    observable_mapping: dict[str, tuple[str, ...]],
    initial_limiting_species: str | None,
    require_runtime_roles: bool,
) -> None:
    species_ids = set(network.species_ids)
    errors: list[str] = []

    if not card.target_species:
        errors.append("target_species cannot be empty")
    if require_runtime_roles and not card.impurity_species:
        errors.append("impurity_species cannot be empty for Runtime v2 scoring")
    if initial_limiting_species is None:
        errors.append("initial_amounts_mol must contain at least one positive species")

    unknown_initial = sorted(set(card.initial_amounts_mol) - species_ids)
    if unknown_initial:
        errors.append(f"initial species not in mechanism: {unknown_initial}")
    unknown_target = sorted(set(card.target_species) - species_ids)
    if unknown_target:
        errors.append(f"target species not in mechanism: {unknown_target}")
    unknown_impurity = sorted(set(card.impurity_species) - species_ids)
    if unknown_impurity:
        errors.append(f"impurity species not in mechanism: {unknown_impurity}")
    if initial_limiting_species is not None and initial_limiting_species not in species_ids:
        errors.append(f"initial limiting species not in mechanism: {initial_limiting_species!r}")

    for role, species in observable_mapping.items():
        unknown_role_species = sorted(set(species) - species_ids)
        if unknown_role_species:
            errors.append(
                f"observable role {role!r} contains unknown species: {unknown_role_species}"
            )

    if initial_limiting_species is not None:
        reactants = observable_mapping.get("reactant", ())
        if reactants and initial_limiting_species not in reactants:
            errors.append(
                "initial limiting species must be included in observable reactant role "
                f"when reactants are declared: {initial_limiting_species!r}"
            )

    if errors:
        raise ValueError(
            f"Mechanism {card.mechanism_id!r} does not satisfy Runtime v2 role contract: "
            + "; ".join(errors)
        )


__all__ = [
    "MECHANISM_SCHEMA_VERSION",
    "SCENARIO_MECHANISM_DEFAULTS",
    "CompiledMechanism",
    "ScoreSpec",
    "compile_mechanism",
    "compile_mechanism_for_scenario",
    "mechanism_hash",
    "mechanism_id_for_scenario",
]
