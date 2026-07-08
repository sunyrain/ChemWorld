"""Runtime v2 engine facade used by ChemWorldEnv."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from chemworld.foundation import OperationRecord, PhysicalConstitution, WorldState
from chemworld.runtime.domain_services import ChemWorldDomainServices
from chemworld.runtime.kernels import (
    KernelResult,
    OperationKernelRegistry,
    RuntimeContext,
    TaskRuntimeProfile,
)
from chemworld.runtime.mechanisms import CompiledMechanism
from chemworld.runtime.transactions import TransactionManager
from chemworld.tasks import TaskSpec
from chemworld.world.parameters import ChemWorldParameters


@dataclass(frozen=True)
class RuntimeStepResult:
    state: WorldState
    operation_record: OperationRecord
    kernel_result: KernelResult

    def info_payload(self) -> dict[str, Any]:
        return {
            "kernel_id": self.kernel_result.kernel_id,
            "kernel_version": self.kernel_result.kernel_version,
            "affected_ledgers": list(self.kernel_result.affected_ledgers),
            "world_events": [
                event.to_dict() for event in self.kernel_result.events
            ],
            "state_patches_summary": [
                patch.to_dict() for patch in self.kernel_result.patches
            ],
            "cost_delta": self.kernel_result.cost_delta,
            "risk_delta": self.kernel_result.risk_delta,
            "sample_delta": self.kernel_result.sample_delta,
            "transaction_status": self.kernel_result.transaction_status,
            "rollback_reason": self.kernel_result.rollback_reason,
        }


class ChemWorldRuntime:
    """Transactional operation runtime for a ChemWorld task/scenario."""

    def __init__(
        self,
        *,
        world: ChemWorldParameters,
        constitution: PhysicalConstitution,
        task_spec: TaskSpec | None,
        compiled_mechanism: CompiledMechanism,
        debug_truth: bool = False,
        registry: OperationKernelRegistry | None = None,
    ) -> None:
        self.world = world
        self.constitution = constitution
        self.task_spec = task_spec
        self.compiled_mechanism = compiled_mechanism
        self.profile = TaskRuntimeProfile.from_task(task_spec)
        self.registry = registry or OperationKernelRegistry.default()
        self.registry.validate_profile(self.profile)
        self.domain_services = ChemWorldDomainServices(
            world,
            constitution,
            compiled_mechanism=compiled_mechanism,
        )
        self.transaction_manager = TransactionManager(constitution)
        self.context = RuntimeContext(
            task_spec=task_spec,
            profile=self.profile,
            compiled_mechanism=compiled_mechanism,
            domain_services=self.domain_services,
            transaction_manager=self.transaction_manager,
            debug_truth=debug_truth,
        )

    def apply_transaction(
        self,
        state: WorldState,
        action: dict[str, Any],
    ) -> RuntimeStepResult:
        kernel = self.registry.get(str(action["operation"]))
        result = kernel.apply(state, action, self.context)
        return RuntimeStepResult(
            state=result.state,
            operation_record=result.operation_record,
            kernel_result=result,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "profile": self.profile.to_dict(),
            "operation_kernels": self.registry.to_dict(),
            "domain_services": self.domain_services.to_dict(),
            "compiled_mechanism": self.compiled_mechanism.to_dict(),
        }


__all__ = ["ChemWorldRuntime", "RuntimeStepResult"]
