"""Hidden material-law counterfactuals with an unchanged public interface."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, replace
from typing import Any, Literal, cast

import numpy as np

from chemworld.world.scenario import ScenarioInstance

MaterialField = Literal["catalyst", "solvent"]

MATERIAL_LAW_COUNTERFACTUAL_VERSION = "chemworld-material-law-counterfactual-0.1"


@dataclass(frozen=True)
class MaterialLawCounterfactual:
    """Permute hidden material effects without changing public names or codes."""

    material_field: MaterialField
    public_to_baseline: tuple[int, ...]

    def __post_init__(self) -> None:
        if self.material_field not in {"catalyst", "solvent"}:
            raise ValueError("material_field must be catalyst or solvent")
        if sorted(self.public_to_baseline) != list(range(len(self.public_to_baseline))):
            raise ValueError("public_to_baseline must be a permutation of [0, n)")
        if all(index == value for index, value in enumerate(self.public_to_baseline)):
            raise ValueError("material-law counterfactual must be non-identity")

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> MaterialLawCounterfactual:
        if payload.get("kind") != "material_law_counterfactual":
            raise ValueError(
                "material-law counterfactual kind must be 'material_law_counterfactual'"
            )
        raw_permutation = payload.get("public_to_baseline")
        if not isinstance(raw_permutation, list) or not all(
            isinstance(value, int) and not isinstance(value, bool)
            for value in raw_permutation
        ):
            raise ValueError("public_to_baseline must be a list of integers")
        return cls(
            material_field=cast(MaterialField, str(payload.get("material_field"))),
            public_to_baseline=tuple(raw_permutation),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "kind": "material_law_counterfactual",
            "material_field": self.material_field,
            "public_to_baseline": list(self.public_to_baseline),
        }


def material_law_counterfactual_hash(
    counterfactual: MaterialLawCounterfactual,
) -> str:
    payload = {
        "version": MATERIAL_LAW_COUNTERFACTUAL_VERSION,
        "counterfactual": counterfactual.to_dict(),
    }
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def apply_material_law_counterfactual(
    instance: ScenarioInstance,
    counterfactual: MaterialLawCounterfactual,
) -> ScenarioInstance:
    """Execute swapped hidden effects while holding public material facts fixed.

    Only kinetic-effect rows are permuted. Public names, action schemas, costs,
    risks, and all non-material hidden parameters remain unchanged.
    """

    parameters = instance.parameters
    catalyst_effects = np.array(parameters.catalyst_effects, copy=True)
    solvent_effects = np.array(parameters.solvent_effects, copy=True)
    target = (
        catalyst_effects
        if counterfactual.material_field == "catalyst"
        else solvent_effects
    )
    if len(counterfactual.public_to_baseline) != target.shape[0]:
        raise ValueError(
            "material-law permutation length does not match the selected material catalog"
        )
    remapped = target[np.asarray(counterfactual.public_to_baseline, dtype=int), :]
    if counterfactual.material_field == "catalyst":
        catalyst_effects = remapped
    else:
        solvent_effects = remapped

    contract_hash = material_law_counterfactual_hash(counterfactual)
    parameters = replace(
        parameters,
        world_id=f"{parameters.world_id}:material-law-{contract_hash[:12]}",
        provider=f"{parameters.provider}+material-law-counterfactual",
        catalyst_effects=catalyst_effects,
        solvent_effects=solvent_effects,
    )
    state = instance.initial_state.replace(
        metadata={
            **instance.initial_state.metadata,
            "material_law_counterfactual_version": (
                MATERIAL_LAW_COUNTERFACTUAL_VERSION
            ),
            "material_law_counterfactual_hash": contract_hash,
        }
    )
    return replace(instance, parameters=parameters, initial_state=state)


__all__ = [
    "MATERIAL_LAW_COUNTERFACTUAL_VERSION",
    "MaterialLawCounterfactual",
    "apply_material_law_counterfactual",
    "material_law_counterfactual_hash",
]
