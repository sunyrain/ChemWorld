"""Executable mechanism-family interventions for causally reachable tasks."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, replace
from math import exp, log
from typing import Any, Literal, cast

import numpy as np

from chemworld.physchem.reaction_network import ReactionNetworkSpec
from chemworld.physchem.reaction_network_specs import RateLawSpec, ReactionSpec
from chemworld.runtime.mechanism_manifest import CompiledMechanism
from chemworld.world.scenario import ScenarioInstance

MechanismFamilyMode = Literal["rate_law_family", "topology_family"]
MECHANISM_FAMILY_INTERVENTION_VERSION = "chemworld-mechanism-family-intervention-0.1"
MECHANISM_REACHABLE_TASKS = (
    "reaction-to-crystallization",
    "reaction-to-distillation",
    "flow-reaction-optimization",
)


@dataclass(frozen=True)
class MechanismFamilyIntervention:
    mode: MechanismFamilyMode
    severity: float

    def __post_init__(self) -> None:
        if self.mode not in {"rate_law_family", "topology_family"}:
            raise ValueError(f"unsupported mechanism-family mode: {self.mode}")
        if not np.isfinite(self.severity) or not 0.0 < self.severity <= 1.0:
            raise ValueError("mechanism-family severity must be finite and in (0, 1]")

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> MechanismFamilyIntervention:
        if payload.get("kind") != "mechanism_family":
            raise ValueError("mechanism intervention kind must be 'mechanism_family'")
        return cls(
            mode=cast(MechanismFamilyMode, str(payload["mode"])),
            severity=float(payload["severity"]),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "kind": "mechanism_family",
            "mode": self.mode,
            "severity": self.severity,
        }


def apply_mechanism_family_intervention(
    instance: ScenarioInstance,
    intervention: MechanismFamilyIntervention,
) -> ScenarioInstance:
    """Bind a derived compiled mechanism and opaque provenance to a world."""

    if instance.spec.scenario_id not in MECHANISM_REACHABLE_TASKS:
        raise ValueError(
            f"task {instance.spec.scenario_id!r} does not causally execute CompiledMechanism"
        )
    base_hash = str(
        instance.compiled_mechanism.network.metadata.get(
            "base_mechanism_hash",
            instance.compiled_mechanism.mechanism_hash,
        )
    )
    contract_hash = mechanism_intervention_hash(
        base_mechanism_hash=base_hash,
        intervention=intervention,
    )
    parameters = replace(
        instance.parameters,
        world_id=f"{instance.parameters.world_id}:mechanism-{contract_hash[:12]}",
        provider=f"{instance.parameters.provider}+mechanism-family",
    )
    metadata = {
        **instance.initial_state.metadata,
        "mechanism_id": instance.compiled_mechanism.mechanism_id,
        "mechanism_hash": instance.compiled_mechanism.mechanism_hash,
        "mechanism_family_intervention_version": MECHANISM_FAMILY_INTERVENTION_VERSION,
        "mechanism_family_intervention_hash": contract_hash,
    }
    return replace(
        instance,
        parameters=parameters,
        initial_state=instance.initial_state.replace(metadata=metadata),
    )


def derive_mechanism_family(
    base: CompiledMechanism,
    intervention: MechanismFamilyIntervention,
) -> CompiledMechanism:
    network = (
        _rate_law_variant(base.network, intervention.severity)
        if intervention.mode == "rate_law_family"
        else _topology_variant(base, intervention.severity)
    )
    network = replace(
        network,
        metadata={**network.metadata, "base_mechanism_hash": base.mechanism_hash},
    )
    payload = {
        "version": MECHANISM_FAMILY_INTERVENTION_VERSION,
        "base_mechanism_hash": base.mechanism_hash,
        "intervention": intervention.to_dict(),
        "network": network.to_dict(),
    }
    derived_hash = hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    opaque_id = f"mechanism-family-{derived_hash[:12]}"
    validation = replace(
        base.manifest.validation_report,
        mechanism_id=opaque_id,
        mechanism_hash=derived_hash,
        source_path=f"{base.manifest.validation_report.source_path}#derived",
        reaction_count=len(network.reactions),
        rate_law_equation_ids=tuple(
            sorted({reaction.rate_law.equation_id for reaction in network.reactions})
        ),
        warnings=(
            *base.manifest.validation_report.warnings,
            "programmatic mechanism-family derivative validated by ReactionNetworkSpec",
        ),
    )
    manifest = replace(
        base.manifest,
        mechanism_id=opaque_id,
        mechanism_hash=derived_hash,
        source_path=validation.source_path,
        species_count=len(network.species),
        reaction_count=len(network.reactions),
        rate_law_equation_ids=validation.rate_law_equation_ids,
        validation_report=validation,
    )
    return replace(
        base,
        mechanism_id=opaque_id,
        mechanism_hash=derived_hash,
        network=network,
        species_index=network.species_index,
        stoichiometric_matrix=network.stoichiometric_matrix(),
        reaction_enthalpies={
            reaction.reaction_id: reaction.delta_h_J_per_mol for reaction in network.reactions
        },
        manifest=manifest,
    )


def mechanism_intervention_hash(
    *,
    base_mechanism_hash: str,
    intervention: MechanismFamilyIntervention,
) -> str:
    payload = {
        "version": MECHANISM_FAMILY_INTERVENTION_VERSION,
        "base_mechanism_hash": base_mechanism_hash,
        "intervention": intervention.to_dict(),
    }
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def _rate_law_variant(network: ReactionNetworkSpec, severity: float) -> ReactionNetworkSpec:
    reactions = list(network.reactions)
    selected_index = next(
        (
            index
            for index, reaction in enumerate(reactions)
            if reaction.rate_law.equation_id in {"arrhenius", "modified_arrhenius"}
        ),
        None,
    )
    if selected_index is None:
        raise ValueError(f"mechanism {network.network_id!r} has no transformable rate law")
    reaction = reactions[selected_index]
    parameters = dict(reaction.rate_law.parameters)
    reference_temperature = 350.0
    if reaction.rate_law.equation_id == "arrhenius":
        exponent = 0.35 * severity
        parameters["b"] = exponent
        parameters["A"] = float(parameters["A"]) / reference_temperature**exponent
        equation_id = "modified_arrhenius"
    else:
        exponent = float(parameters.pop("b", 0.0))
        parameters["A"] = float(parameters["A"]) * reference_temperature**exponent
        equation_id = "arrhenius"
    reactions[selected_index] = replace(
        reaction,
        rate_law=RateLawSpec(
            rate_law_id=f"family-{reaction.rate_law.rate_law_id}",
            equation_id=equation_id,
            parameters=parameters,
        ),
    )
    return replace(
        network,
        network_id=f"{network.network_id}-family",
        reactions=tuple(reactions),
        metadata={**network.metadata, "derived_family": True},
    )


def _topology_variant(base: CompiledMechanism, severity: float) -> ReactionNetworkSpec:
    network = base.network
    limiting = base.score_spec.initial_limiting_species
    targets = set(base.score_spec.target_species)
    forward = next(
        (
            reaction
            for reaction in network.reactions
            if limiting in reaction.reactants and targets.intersection(reaction.products)
        ),
        network.reactions[0],
    )
    reverse = ReactionSpec(
        reaction_id="family_reverse_channel",
        equation=f"reverse({forward.equation})",
        stoichiometry={
            species_id: -coefficient for species_id, coefficient in forward.stoichiometry.items()
        },
        reversible=False,
        rate_law=RateLawSpec(
            rate_law_id="family_reverse_mass_action",
            equation_id="mass_action",
            parameters={"k": 0.00025 * exp(log(2.0) * severity)},
        ),
        delta_h_J_per_mol=-forward.delta_h_J_per_mol,
        metadata={"derived_family": True},
    )
    return replace(
        network,
        network_id=f"{network.network_id}-family",
        reactions=(*network.reactions, reverse),
        metadata={**network.metadata, "derived_family": True},
    )


__all__ = [
    "MECHANISM_FAMILY_INTERVENTION_VERSION",
    "MECHANISM_REACHABLE_TASKS",
    "MechanismFamilyIntervention",
    "apply_mechanism_family_intervention",
    "derive_mechanism_family",
    "mechanism_intervention_hash",
]
