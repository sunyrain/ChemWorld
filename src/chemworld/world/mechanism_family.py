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

MechanismFamilyMode = Literal[
    "rate_law_family",
    "topology_family",
    "constitutive_law_family",
]
RateLawReactionRole = Literal[
    "primary_competing_pathway",
    "primary_target_pathway",
]
RateLawTransformId = Literal["arrhenius_form_and_scale_stress_v1"]
MECHANISM_FAMILY_INTERVENTION_VERSION = "chemworld-mechanism-family-intervention-0.5"
REACTION_MECHANISM_TASKS = (
    "reaction-to-crystallization",
    "reaction-to-distillation",
    "flow-reaction-optimization",
)
PARTITION_MECHANISM_TASKS = ("partition-discovery",)
ELECTROCHEMICAL_MECHANISM_TASKS = ("electrochemical-conversion",)
EQUILIBRIUM_MECHANISM_TASKS = ("equilibrium-characterization",)
CONSTITUTIVE_MECHANISM_TASKS = (
    *PARTITION_MECHANISM_TASKS,
    *ELECTROCHEMICAL_MECHANISM_TASKS,
    *EQUILIBRIUM_MECHANISM_TASKS,
)
MECHANISM_REACHABLE_TASKS = (
    *PARTITION_MECHANISM_TASKS,
    *REACTION_MECHANISM_TASKS,
    *ELECTROCHEMICAL_MECHANISM_TASKS,
    *EQUILIBRIUM_MECHANISM_TASKS,
)
MECHANISM_TASK_MODES: dict[str, tuple[MechanismFamilyMode, ...]] = {
    **dict.fromkeys(CONSTITUTIVE_MECHANISM_TASKS, ("constitutive_law_family",)),
    **dict.fromkeys(REACTION_MECHANISM_TASKS, ("rate_law_family", "topology_family")),
}


@dataclass(frozen=True)
class RateLawFamilyChange:
    """Declarative target and transform for a reaction rate-law intervention."""

    reaction_role: RateLawReactionRole = "primary_competing_pathway"
    transform_id: RateLawTransformId = "arrhenius_form_and_scale_stress_v1"
    reference_temperature_K: float = 350.0
    reference_rate_multiplier_at_full_severity: float = 8.0
    temperature_exponent_at_full_severity: float = 0.75

    def __post_init__(self) -> None:
        if self.reaction_role not in {
            "primary_competing_pathway",
            "primary_target_pathway",
        }:
            raise ValueError(f"unsupported rate-law reaction role: {self.reaction_role}")
        if self.transform_id != "arrhenius_form_and_scale_stress_v1":
            raise ValueError(f"unsupported rate-law transform: {self.transform_id}")
        if (
            not np.isfinite(self.reference_temperature_K)
            or self.reference_temperature_K <= 0.0
        ):
            raise ValueError("rate-law reference temperature must be finite and positive")
        if (
            not np.isfinite(self.reference_rate_multiplier_at_full_severity)
            or self.reference_rate_multiplier_at_full_severity <= 1.0
        ):
            raise ValueError(
                "rate-law reference multiplier must be finite and greater than one"
            )
        if (
            not np.isfinite(self.temperature_exponent_at_full_severity)
            or self.temperature_exponent_at_full_severity <= 0.0
        ):
            raise ValueError(
                "rate-law temperature exponent must be finite and positive"
            )

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> RateLawFamilyChange:
        allowed = {
            "reaction_role",
            "transform_id",
            "reference_temperature_K",
            "reference_rate_multiplier_at_full_severity",
            "temperature_exponent_at_full_severity",
        }
        unknown = sorted(set(payload) - allowed)
        if unknown:
            raise ValueError(f"unknown rate-law change fields: {unknown}")
        return cls(
            reaction_role=cast(
                RateLawReactionRole,
                str(payload.get("reaction_role", "primary_competing_pathway")),
            ),
            transform_id=cast(
                RateLawTransformId,
                str(
                    payload.get(
                        "transform_id",
                        "arrhenius_form_and_scale_stress_v1",
                    )
                ),
            ),
            reference_temperature_K=float(payload.get("reference_temperature_K", 350.0)),
            reference_rate_multiplier_at_full_severity=float(
                payload.get("reference_rate_multiplier_at_full_severity", 8.0)
            ),
            temperature_exponent_at_full_severity=float(
                payload.get("temperature_exponent_at_full_severity", 0.75)
            ),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "reaction_role": self.reaction_role,
            "transform_id": self.transform_id,
            "reference_temperature_K": self.reference_temperature_K,
            "reference_rate_multiplier_at_full_severity": (
                self.reference_rate_multiplier_at_full_severity
            ),
            "temperature_exponent_at_full_severity": (
                self.temperature_exponent_at_full_severity
            ),
        }


@dataclass(frozen=True)
class MechanismFamilyIntervention:
    mode: MechanismFamilyMode
    severity: float
    rate_law_change: RateLawFamilyChange | None = None

    def __post_init__(self) -> None:
        if self.mode not in {
            "rate_law_family",
            "topology_family",
            "constitutive_law_family",
        }:
            raise ValueError(f"unsupported mechanism-family mode: {self.mode}")
        if not np.isfinite(self.severity) or not 0.0 < self.severity <= 1.0:
            raise ValueError("mechanism-family severity must be finite and in (0, 1]")
        if self.mode != "rate_law_family" and self.rate_law_change is not None:
            raise ValueError("rate_law_change is only valid for rate_law_family")

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> MechanismFamilyIntervention:
        if payload.get("kind") != "mechanism_family":
            raise ValueError("mechanism intervention kind must be 'mechanism_family'")
        allowed = {"kind", "mode", "severity", "rate_law_change"}
        unknown = sorted(set(payload) - allowed)
        if unknown:
            raise ValueError(f"unknown mechanism-family intervention fields: {unknown}")
        mode = cast(MechanismFamilyMode, str(payload["mode"]))
        rate_law_payload = payload.get("rate_law_change")
        if rate_law_payload is not None and not isinstance(rate_law_payload, dict):
            raise ValueError("rate_law_change must be an object")
        return cls(
            mode=mode,
            severity=float(payload["severity"]),
            rate_law_change=(
                RateLawFamilyChange.from_dict(rate_law_payload)
                if isinstance(rate_law_payload, dict)
                else None
            ),
        )

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "kind": "mechanism_family",
            "mode": self.mode,
            "severity": self.severity,
        }
        if self.mode == "rate_law_family":
            payload["rate_law_change"] = self.resolved_rate_law_change.to_dict()
        return payload

    @property
    def resolved_rate_law_change(self) -> RateLawFamilyChange:
        if self.mode != "rate_law_family":
            raise ValueError("only rate_law_family has a rate-law change contract")
        return self.rate_law_change or RateLawFamilyChange()


def apply_mechanism_family_intervention(
    instance: ScenarioInstance,
    intervention: MechanismFamilyIntervention,
) -> ScenarioInstance:
    """Bind a derived compiled mechanism and opaque provenance to a world."""

    task_id = instance.spec.scenario_id
    if task_id not in MECHANISM_REACHABLE_TASKS:
        raise ValueError(f"task {task_id!r} does not expose a mechanism-family intervention")
    if intervention.mode not in MECHANISM_TASK_MODES[task_id]:
        raise ValueError(
            f"mode {intervention.mode!r} is not causally reachable for task {task_id!r}"
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
    domain_parameters = dict(instance.parameters.domain_parameters)
    if intervention.mode == "constitutive_law_family":
        if task_id == "partition-discovery":
            domain_parameters["partition_coefficient_exponent"] = (
                1.0 + 0.75 * intervention.severity
            )
        elif task_id == "electrochemical-conversion":
            domain_parameters["electro_transfer_asymmetry_multiplier"] = (
                1.0 + 0.40 * intervention.severity
            )
            domain_parameters["electro_selectivity_decay_multiplier"] = (
                1.0 + 2.00 * intervention.severity
            )
            domain_parameters["electro_standard_potential_multiplier"] = (
                1.0 + 0.25 * intervention.severity
            )
    parameters = replace(
        instance.parameters,
        world_id=f"{instance.parameters.world_id}:mechanism-{contract_hash[:12]}",
        provider=f"{instance.parameters.provider}+mechanism-family",
        domain_parameters=domain_parameters,
    )
    metadata = {
        **instance.initial_state.metadata,
        "mechanism_id": instance.compiled_mechanism.mechanism_id,
        "mechanism_hash": instance.compiled_mechanism.mechanism_hash,
        "mechanism_family_intervention_version": MECHANISM_FAMILY_INTERVENTION_VERSION,
        "mechanism_family_intervention_hash": contract_hash,
    }
    if task_id == "equilibrium-characterization":
        metadata["equilibrium_activity_coefficient_ratio"] = exp(
            log(6.0) * intervention.severity
        )
    return replace(
        instance,
        parameters=parameters,
        initial_state=instance.initial_state.replace(metadata=metadata),
    )


def derive_mechanism_family(
    base: CompiledMechanism,
    intervention: MechanismFamilyIntervention,
) -> CompiledMechanism:
    if intervention.mode == "constitutive_law_family":
        raise ValueError(
            "constitutive-law families modify executed world laws, not ReactionNetworkSpec"
        )
    network = (
        _rate_law_variant(
            base,
            intervention.severity,
            intervention.resolved_rate_law_change,
        )
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


def _rate_law_variant(
    base: CompiledMechanism,
    severity: float,
    change: RateLawFamilyChange,
) -> ReactionNetworkSpec:
    network = base.network
    reactions = list(network.reactions)
    selected_index = _select_rate_law_reaction(
        base,
        reaction_role=change.reaction_role,
    )
    reaction = reactions[selected_index]
    parameters = dict(reaction.rate_law.parameters)
    reference_temperature = change.reference_temperature_K
    activity_factor = exp(
        log(change.reference_rate_multiplier_at_full_severity) * severity
    )
    if reaction.rate_law.equation_id == "arrhenius":
        # A mechanism-family shift must be observable over the task's practical
        # temperature/concentration range, not merely have a different equation id.
        # The transform is an explicitly declared operational stress, not a claim
        # that the synthetic multiplier is a fitted material constant.
        exponent = change.temperature_exponent_at_full_severity * severity
        parameters["b"] = exponent
        parameters["A"] = (
            float(parameters["A"])
            * activity_factor
            / reference_temperature**exponent
        )
        equation_id = "modified_arrhenius"
    else:
        exponent = float(parameters.pop("b", 0.0))
        parameters["A"] = (
            float(parameters["A"])
            * reference_temperature**exponent
            / activity_factor
        )
        equation_id = "arrhenius"
    reactions[selected_index] = replace(
        reaction,
        rate_law=replace(
            reaction.rate_law,
            rate_law_id=f"family-{reaction.rate_law.rate_law_id}",
            equation_id=equation_id,
            parameters=parameters,
        ),
    )
    return replace(
        network,
        network_id=f"{network.network_id}-family",
        reactions=tuple(reactions),
        metadata={
            **network.metadata,
            "derived_family": True,
            "derived_family_target_reaction_id": reaction.reaction_id,
            "derived_family_target_reaction_role": change.reaction_role,
            "derived_family_transform_id": change.transform_id,
            "derived_family_reference_temperature_K": reference_temperature,
            "derived_family_reference_rate_multiplier": activity_factor,
        },
    )


def _select_rate_law_reaction(
    base: CompiledMechanism,
    *,
    reaction_role: RateLawReactionRole,
) -> int:
    """Resolve a semantic reaction role without depending on declaration order."""

    targets = set(base.score_spec.target_species)
    limiting = base.score_spec.initial_limiting_species
    feed_species = {limiting}
    feed_species.update(
        species_id
        for species_id, roles in base.species_roles.items()
        if any("reactant" in role for role in roles)
    )
    candidates: list[int] = []
    for index, reaction in enumerate(base.network.reactions):
        if reaction.rate_law.equation_id not in {"arrhenius", "modified_arrhenius"}:
            continue
        reactants = set(reaction.reactants)
        products = set(reaction.products)
        if reaction_role == "primary_target_pathway":
            matches = bool(reactants & feed_species) and bool(products & targets)
        else:
            matches = (
                bool(reactants & feed_species)
                and not bool(reactants & targets)
                and not bool(products & targets)
            )
        if matches:
            candidates.append(index)
    if len(candidates) != 1:
        reaction_ids = [base.network.reactions[index].reaction_id for index in candidates]
        raise ValueError(
            f"mechanism {base.network.network_id!r} requires exactly one transformable "
            f"{reaction_role!r} rate law; found {reaction_ids}"
        )
    return candidates[0]


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
    "CONSTITUTIVE_MECHANISM_TASKS",
    "ELECTROCHEMICAL_MECHANISM_TASKS",
    "EQUILIBRIUM_MECHANISM_TASKS",
    "MECHANISM_FAMILY_INTERVENTION_VERSION",
    "MECHANISM_REACHABLE_TASKS",
    "MECHANISM_TASK_MODES",
    "PARTITION_MECHANISM_TASKS",
    "REACTION_MECHANISM_TASKS",
    "MechanismFamilyIntervention",
    "RateLawFamilyChange",
    "apply_mechanism_family_intervention",
    "derive_mechanism_family",
    "mechanism_intervention_hash",
]
