"""Operation-kernel data contracts for Runtime v2."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol

from chemworld.foundation import OperationRecord, WorldState
from chemworld.operation_validator import OperationValidation
from chemworld.runtime.domain_services import ChemWorldDomainServices
from chemworld.runtime.mechanisms import CompiledMechanism
from chemworld.runtime.profiles import TaskRuntimeProfile
from chemworld.runtime.transactions import StatePatch, TransactionManager, WorldEvent
from chemworld.tasks import TaskSpec


@dataclass(frozen=True)
class RuntimeContext:
    task_spec: TaskSpec | None
    profile: TaskRuntimeProfile
    compiled_mechanism: CompiledMechanism
    domain_services: ChemWorldDomainServices
    transaction_manager: TransactionManager
    debug_truth: bool = False


@dataclass(frozen=True)
class KernelPlan:
    operation_type: str
    kernel_id: str
    affected_ledgers: tuple[str, ...]
    required_capabilities: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "operation_type": self.operation_type,
            "kernel_id": self.kernel_id,
            "affected_ledgers": list(self.affected_ledgers),
            "required_capabilities": list(self.required_capabilities),
        }


@dataclass(frozen=True)
class KernelResult:
    state: WorldState
    operation_record: OperationRecord
    events: tuple[WorldEvent, ...]
    patches: tuple[StatePatch, ...]
    state_delta_summary: dict[str, Any]
    cost_delta: float
    risk_delta: float
    sample_delta: float
    affected_ledgers: tuple[str, ...]
    kernel_id: str
    kernel_version: str
    transaction_status: str
    rollback_reason: str | None


class OperationKernel(Protocol):
    @property
    def operation_type(self) -> str:
        ...

    @property
    def kernel_id(self) -> str:
        ...

    @property
    def kernel_version(self) -> str:
        ...

    @property
    def required_capabilities(self) -> frozenset[str]:
        ...

    def validate(
        self,
        state: WorldState,
        action: dict[str, Any],
        context: RuntimeContext,
    ) -> OperationValidation | None:
        ...

    def plan(
        self,
        state: WorldState,
        action: dict[str, Any],
        context: RuntimeContext,
    ) -> KernelPlan:
        ...

    def apply(
        self,
        state: WorldState,
        action: dict[str, Any],
        context: RuntimeContext,
    ) -> KernelResult:
        ...


__all__ = [
    "KernelPlan",
    "KernelResult",
    "OperationKernel",
    "RuntimeContext",
]
