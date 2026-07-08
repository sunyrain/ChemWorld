"""Operation kernel registry and runtime profile for ChemWorld runtime v2."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol

from chemworld.foundation import OperationRecord, WorldState
from chemworld.operation_validator import OperationValidation
from chemworld.runtime.domain_services import ChemWorldDomainServices, DomainServiceRegistry
from chemworld.runtime.mechanisms import CompiledMechanism
from chemworld.runtime.transactions import StatePatch, TransactionManager, WorldEvent
from chemworld.tasks import TaskSpec
from chemworld.world.operations import OPERATION_TYPES, operation_contracts


@dataclass(frozen=True)
class TaskRuntimeProfile:
    world_law_id: str
    allowed_operations: frozenset[str]
    required_kernels: frozenset[str]
    optional_kernels: frozenset[str]
    required_domain_services: frozenset[str]
    required_capabilities: frozenset[str]
    allowed_instruments: frozenset[str]

    @classmethod
    def from_task(cls, task: TaskSpec | None) -> TaskRuntimeProfile:
        if task is None:
            allowed = frozenset(OPERATION_TYPES)
            instruments: frozenset[str] = frozenset()
        else:
            allowed = frozenset(task.allowed_operations)
            instruments = frozenset(task.allowed_instruments)
        contracts = operation_contracts()
        service_registry = DomainServiceRegistry.default()
        required_domain_services = service_registry.service_ids_for_operations(allowed)
        capabilities = frozenset(
            contracts[operation].module for operation in allowed if operation in contracts
        )
        return cls(
            world_law_id=(
                "chemworld-physical-chemistry"
                if task is None
                else task.world_law_id
            ),
            allowed_operations=allowed,
            required_kernels=allowed,
            optional_kernels=frozenset(OPERATION_TYPES) - allowed,
            required_domain_services=required_domain_services,
            required_capabilities=capabilities,
            allowed_instruments=instruments,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "world_law_id": self.world_law_id,
            "allowed_operations": sorted(self.allowed_operations),
            "required_kernels": sorted(self.required_kernels),
            "optional_kernels": sorted(self.optional_kernels),
            "required_domain_services": sorted(self.required_domain_services),
            "required_capabilities": sorted(self.required_capabilities),
            "allowed_instruments": sorted(self.allowed_instruments),
        }

    def is_operation_allowed(self, operation_type: str) -> bool:
        return operation_type in self.allowed_operations

    def is_domain_service_required(self, service_id: str) -> bool:
        return service_id in self.required_domain_services


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


@dataclass(frozen=True)
class ServiceOperationKernel:
    operation_type: str
    module: str
    kernel_version: str = "runtime-v2.0"

    @property
    def kernel_id(self) -> str:
        return f"chemworld.operation.{self.operation_type}"

    @property
    def required_capabilities(self) -> frozenset[str]:
        return frozenset({self.module})

    def validate(
        self,
        state: WorldState,
        action: dict[str, Any],
        context: RuntimeContext,
    ) -> OperationValidation | None:
        del state, action, context
        return None

    def plan(
        self,
        state: WorldState,
        action: dict[str, Any],
        context: RuntimeContext,
    ) -> KernelPlan:
        del state, action, context
        return KernelPlan(
            operation_type=self.operation_type,
            kernel_id=self.kernel_id,
            affected_ledgers=_affected_ledgers(self.operation_type),
            required_capabilities=tuple(sorted(self.required_capabilities)),
        )

    def apply(
        self,
        state: WorldState,
        action: dict[str, Any],
        context: RuntimeContext,
    ) -> KernelResult:
        before = state
        domain_service_id = context.domain_services.service_id_for_operation(self.operation_type)
        affected = _affected_ledgers(self.operation_type)
        next_state, record = context.domain_services.apply_operation(state, action)
        failed_preconditions = tuple(
            key for key, passed in record.preconditions.items() if not passed
        )
        if failed_preconditions:
            rejection_event = WorldEvent(
                event_type="operation_rejected",
                operation_type=self.operation_type,
                payload={
                    "kernel_id": self.kernel_id,
                    "domain_service_id": domain_service_id,
                    "affected_ledgers": list(affected),
                    "failed_preconditions": list(failed_preconditions),
                },
            )
            transaction = context.transaction_manager.rollback(
                state=before,
                operation_type=self.operation_type,
                rollback_reason="precondition_failed",
                failed_preconditions=failed_preconditions,
                events=(rejection_event,),
            )
            record = context.domain_services.record_operation(
                self.operation_type,
                before,
                transaction.state,
                record.preconditions,
                action,
            )
            return KernelResult(
                state=transaction.state,
                operation_record=record,
                events=transaction.events,
                patches=transaction.patches,
                state_delta_summary=record.state_delta_summary,
                cost_delta=transaction.state.ledger.cost - before.ledger.cost,
                risk_delta=transaction.state.ledger.risk - before.ledger.risk,
                sample_delta=(
                    transaction.state.ledger.sample_consumed_L
                    - before.ledger.sample_consumed_L
                ),
                affected_ledgers=("process",),
                kernel_id=self.kernel_id,
                kernel_version=self.kernel_version,
                transaction_status=transaction.transaction_status,
                rollback_reason=transaction.rollback_reason,
            )
        patch = StatePatch(
            patch_type="replace_state",
            affected_ledgers=affected,
            state=next_state,
            summary=record.state_delta_summary,
        )
        event = WorldEvent(
            event_type="operation_applied",
            operation_type=self.operation_type,
            payload={
                "kernel_id": self.kernel_id,
                "domain_service_id": domain_service_id,
                "affected_ledgers": list(affected),
            },
        )
        transaction = context.transaction_manager.commit(
            state=before,
            operation_type=self.operation_type,
            events=(event,),
            patches=(patch,),
        )
        if transaction.transaction_status != "committed":
            record = context.domain_services.record_operation(
                self.operation_type,
                before,
                transaction.state,
                record.preconditions,
                action,
            )
        return KernelResult(
            state=transaction.state,
            operation_record=record,
            events=transaction.events,
            patches=transaction.patches,
            state_delta_summary=record.state_delta_summary,
            cost_delta=transaction.state.ledger.cost - before.ledger.cost,
            risk_delta=transaction.state.ledger.risk - before.ledger.risk,
            sample_delta=(
                transaction.state.ledger.sample_consumed_L - before.ledger.sample_consumed_L
            ),
            affected_ledgers=affected,
            kernel_id=self.kernel_id,
            kernel_version=self.kernel_version,
            transaction_status=transaction.transaction_status,
            rollback_reason=transaction.rollback_reason,
        )


class OperationKernelRegistry:
    def __init__(self, kernels: list[OperationKernel]) -> None:
        self._kernels = {kernel.operation_type: kernel for kernel in kernels}
        if len(self._kernels) != len(kernels):
            raise ValueError("Duplicate operation kernels are not allowed")

    @classmethod
    def default(cls) -> OperationKernelRegistry:
        contracts = operation_contracts()
        return cls(
            [
                ServiceOperationKernel(
                    operation_type=operation_type,
                    module=contracts[operation_type].module
                    if operation_type in contracts
                    else "general",
                )
                for operation_type in OPERATION_TYPES
            ]
        )

    def validate_profile(self, profile: TaskRuntimeProfile) -> None:
        missing = sorted(profile.required_kernels - set(self._kernels))
        if missing:
            raise ValueError(f"Missing required operation kernels: {missing}")
        kernel_capabilities = frozenset(
            capability
            for operation in profile.required_kernels
            for capability in self._kernels[operation].required_capabilities
        )
        missing_capabilities = sorted(profile.required_capabilities - kernel_capabilities)
        if missing_capabilities:
            raise ValueError(
                f"Missing required operation kernel capabilities: {missing_capabilities}"
            )

    def has(self, operation_type: str) -> bool:
        return operation_type in self._kernels

    def get(self, operation_type: str) -> OperationKernel:
        try:
            return self._kernels[operation_type]
        except KeyError as exc:
            raise ValueError(f"No operation kernel registered for {operation_type!r}") from exc

    def to_dict(self) -> dict[str, Any]:
        return {
            operation_type: {
                "kernel_id": kernel.kernel_id,
                "kernel_version": kernel.kernel_version,
                "required_capabilities": sorted(kernel.required_capabilities),
            }
            for operation_type, kernel in sorted(self._kernels.items())
        }


def _affected_ledgers(operation_type: str) -> tuple[str, ...]:
    material = {
        "add_reagent",
        "add_catalyst",
        "add_solvent",
        "sample",
        "heat",
        "wait",
        "add_phase",
        "add_extractant",
        "mix",
        "settle",
        "separate_phase",
        "wash",
        "dry",
        "concentrate",
        "transfer",
        "seed_crystals",
        "cool_crystallize",
        "filter_crystals",
        "evaporate",
        "distill",
        "collect_fraction",
        "run_flow",
        "electrolyze",
    }
    affected = ["process"]
    if operation_type in material:
        affected.append("species")
        affected.append("phases")
    if operation_type in {
        "add_solvent",
        "heat",
        "wait",
        "quench",
        "evaporate",
        "distill",
        "run_flow",
    }:
        affected.append("thermal")
        affected.append("vessels")
    if operation_type in {
        "add_solvent",
        "add_catalyst",
        "heat",
        "wait",
        "mix",
        "seed_crystals",
        "set_flow_rate",
        "set_potential",
        "electrolyze",
        "distill",
        "measure",
    }:
        affected.append("equipment")
    if operation_type == "measure":
        affected.append("observation")
    return tuple(dict.fromkeys(affected))


__all__ = [
    "KernelPlan",
    "KernelResult",
    "OperationKernel",
    "OperationKernelRegistry",
    "RuntimeContext",
    "ServiceOperationKernel",
    "TaskRuntimeProfile",
]
