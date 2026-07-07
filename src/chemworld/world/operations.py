"""Operation registry for the unified ChemWorld language."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from chemworld.core.batch_reactor import (
    CRYSTALLIZATION_OPERATIONS,
    DISTILLATION_OPERATIONS,
    DOWNSTREAM_OBSERVATION_KEYS,
    ELECTROCHEMISTRY_OPERATIONS,
    FLOW_OPERATIONS,
    INSTRUMENTS,
    OPERATION_TYPES,
    REACTION_OPERATIONS,
    SEPARATION_OPERATIONS,
    batch_reactor_operations,
    batch_reactor_state_variables,
)


@dataclass(frozen=True)
class OperationContract:
    operation_id: str
    module: str
    required_fields: tuple[str, ...]
    preconditions: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "operation_id": self.operation_id,
            "module": self.module,
            "required_fields": list(self.required_fields),
            "preconditions": list(self.preconditions),
        }


def operation_contracts() -> dict[str, OperationContract]:
    reaction = set(REACTION_OPERATIONS)
    separation = set(SEPARATION_OPERATIONS)
    crystallization = set(CRYSTALLIZATION_OPERATIONS)
    distillation = set(DISTILLATION_OPERATIONS)
    flow = set(FLOW_OPERATIONS)
    electrochemistry = set(ELECTROCHEMISTRY_OPERATIONS)
    contracts: dict[str, OperationContract] = {}
    for operation in batch_reactor_operations():
        if operation.id in separation:
            module = "separation"
        elif operation.id in crystallization:
            module = "crystallization"
        elif operation.id in distillation:
            module = "distillation"
        elif operation.id in flow:
            module = "continuous_flow"
        elif operation.id in electrochemistry:
            module = "electrochemistry"
        elif operation.id in reaction:
            module = "reaction"
        else:
            module = "general"
        contracts[operation.id] = OperationContract(
            operation_id=operation.id,
            module=module,
            required_fields=operation.required_fields,
            preconditions=operation.preconditions,
        )
    return contracts


__all__ = [
    "CRYSTALLIZATION_OPERATIONS",
    "DISTILLATION_OPERATIONS",
    "DOWNSTREAM_OBSERVATION_KEYS",
    "ELECTROCHEMISTRY_OPERATIONS",
    "FLOW_OPERATIONS",
    "INSTRUMENTS",
    "OPERATION_TYPES",
    "REACTION_OPERATIONS",
    "SEPARATION_OPERATIONS",
    "OperationContract",
    "batch_reactor_operations",
    "batch_reactor_state_variables",
    "operation_contracts",
]
