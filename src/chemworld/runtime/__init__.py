"""Runtime v2 public surface for ChemWorld.

The package exports a stable facade, but imports are intentionally lazy. Scenario
generation only needs the mechanism compiler; eager importing the full runtime
would pull in action validation while the action codec is still initializing.
"""

from typing import Any

__all__ = [
    "ChemWorldObservationKernel",
    "ChemWorldRuntime",
    "CompiledMechanism",
    "KernelPlan",
    "KernelResult",
    "OperationKernel",
    "OperationKernelRegistry",
    "RuntimeContext",
    "RuntimeStepResult",
    "ScoreSpec",
    "ServiceOperationKernel",
    "StatePatch",
    "TaskRuntimeProfile",
    "TransactionManager",
    "TransactionResult",
    "WorldEvent",
    "compile_mechanism",
    "compile_mechanism_for_scenario",
    "make_chemworld_constitution",
    "mechanism_hash",
    "mechanism_id_for_scenario",
]

_MECHANISM_EXPORTS = {
    "CompiledMechanism",
    "ScoreSpec",
    "compile_mechanism",
    "compile_mechanism_for_scenario",
    "mechanism_hash",
    "mechanism_id_for_scenario",
}


def __getattr__(name: str) -> Any:
    if name in _MECHANISM_EXPORTS:
        from chemworld.runtime import mechanisms

        return getattr(mechanisms, name)
    if name in {"WorldEvent", "StatePatch", "TransactionManager", "TransactionResult"}:
        from chemworld.runtime import transactions

        return getattr(transactions, name)
    if name in {
        "KernelPlan",
        "KernelResult",
        "OperationKernel",
        "OperationKernelRegistry",
        "RuntimeContext",
        "ServiceOperationKernel",
        "TaskRuntimeProfile",
    }:
        from chemworld.runtime import kernels

        return getattr(kernels, name)
    if name in {"ChemWorldRuntime", "RuntimeStepResult"}:
        from chemworld.runtime import engine

        return getattr(engine, name)
    if name in {"ChemWorldObservationKernel", "make_chemworld_constitution"}:
        from chemworld.runtime import domain_services

        return getattr(domain_services, name)
    raise AttributeError(f"module 'chemworld.runtime' has no attribute {name!r}")
