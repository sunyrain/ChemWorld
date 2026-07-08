"""Runtime v2 public surface for ChemWorld.

The package exports a stable facade, but imports are intentionally lazy. Scenario
generation only needs the mechanism compiler; eager importing the full runtime
would pull in action validation while the action codec is still initializing.
"""

from typing import Any

__all__ = [
    "ChemWorldElectrochemicalServices",
    "ChemWorldInstrumentCostServices",
    "ChemWorldObservationKernel",
    "ChemWorldOperationRecorder",
    "ChemWorldPhaseSeparationServices",
    "ChemWorldReactionThermalServices",
    "ChemWorldRuntime",
    "CompiledMechanism",
    "KernelPlan",
    "KernelResult",
    "MechanismSpeciesView",
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
    if name == "MechanismSpeciesView":
        from chemworld.runtime import species

        return getattr(species, name)
    if name == "ChemWorldOperationRecorder":
        from chemworld.runtime import record_services

        return getattr(record_services, name)
    if name == "ChemWorldElectrochemicalServices":
        from chemworld.runtime import electrochemical_services

        return getattr(electrochemical_services, name)
    if name == "ChemWorldInstrumentCostServices":
        from chemworld.runtime import instrument_cost_services

        return getattr(instrument_cost_services, name)
    if name == "ChemWorldPhaseSeparationServices":
        from chemworld.runtime import phase_separation_services

        return getattr(phase_separation_services, name)
    if name == "ChemWorldReactionThermalServices":
        from chemworld.runtime import reaction_thermal_services

        return getattr(reaction_thermal_services, name)
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
    if name == "ChemWorldObservationKernel":
        from chemworld.runtime import observation_services

        return getattr(observation_services, name)
    if name == "make_chemworld_constitution":
        from chemworld.runtime import domain_services

        return getattr(domain_services, name)
    raise AttributeError(f"module 'chemworld.runtime' has no attribute {name!r}")
