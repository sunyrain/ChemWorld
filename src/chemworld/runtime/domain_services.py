"""Operation composition services for ChemWorld runtime v2.

This module wires primitive helpers to focused Runtime v2 services. It is
intentionally called by operation kernels rather than by ``ChemWorldEnv``
directly.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from chemworld.foundation import (
    OperationRecord,
    PhysicalConstitution,
    Vessel,
    WorldState,
)
from chemworld.runtime.crystallization_services import ChemWorldCrystallizationServices
from chemworld.runtime.distillation_services import ChemWorldDistillationServices
from chemworld.runtime.electrochemical_services import ChemWorldElectrochemicalServices
from chemworld.runtime.flow_services import ChemWorldFlowServices
from chemworld.runtime.instrument_cost_services import ChemWorldInstrumentCostServices
from chemworld.runtime.mechanisms import CompiledMechanism
from chemworld.runtime.phase_separation_services import ChemWorldPhaseSeparationServices
from chemworld.runtime.primitive_services import ChemWorldPrimitiveOperationServices
from chemworld.runtime.reaction_thermal_services import ChemWorldReactionThermalServices
from chemworld.runtime.record_services import ChemWorldOperationRecorder
from chemworld.runtime.species import MechanismSpeciesView
from chemworld.world.instruments import chemworld_instruments
from chemworld.world.ontology import chemworld_substances
from chemworld.world.operations import OPERATION_TYPES, operation_name
from chemworld.world.parameters import ChemWorldParameters


@dataclass(frozen=True)
class DomainServiceContract:
    service_id: str
    module: str
    service_class: str
    operations: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "service_id": self.service_id,
            "module": self.module,
            "service_class": self.service_class,
            "operations": list(self.operations),
        }


@dataclass(frozen=True)
class DomainServiceRegistry:
    contracts: tuple[DomainServiceContract, ...]

    @classmethod
    def default(cls) -> DomainServiceRegistry:
        return cls(
            (
                DomainServiceContract(
                    "primitive_operations",
                    "reaction",
                    "ChemWorldPrimitiveOperationServices",
                    (
                        "add_reagent",
                        "add_solvent",
                        "add_catalyst",
                        "sample",
                        "quench",
                        "evaporate",
                        "terminate",
                    ),
                ),
                DomainServiceContract(
                    "reaction_thermal",
                    "reaction",
                    "ChemWorldReactionThermalServices",
                    ("heat", "wait"),
                ),
                DomainServiceContract(
                    "phase_separation",
                    "separation",
                    "ChemWorldPhaseSeparationServices",
                    (
                        "add_phase",
                        "add_extractant",
                        "mix",
                        "settle",
                        "separate_phase",
                        "wash",
                        "dry",
                        "concentrate",
                        "transfer",
                    ),
                ),
                DomainServiceContract(
                    "crystallization",
                    "crystallization",
                    "ChemWorldCrystallizationServices",
                    ("seed_crystals", "cool_crystallize", "filter_crystals"),
                ),
                DomainServiceContract(
                    "distillation",
                    "distillation",
                    "ChemWorldDistillationServices",
                    ("distill", "collect_fraction"),
                ),
                DomainServiceContract(
                    "continuous_flow",
                    "continuous_flow",
                    "ChemWorldFlowServices",
                    ("set_flow_rate", "run_flow"),
                ),
                DomainServiceContract(
                    "electrochemistry",
                    "electrochemistry",
                    "ChemWorldElectrochemicalServices",
                    ("set_potential", "electrolyze"),
                ),
                DomainServiceContract(
                    "instrument_cost",
                    "observation",
                    "ChemWorldInstrumentCostServices",
                    ("measure",),
                ),
            )
        )

    def validate_operation_coverage(self) -> None:
        owners: dict[str, str] = {}
        duplicates: list[str] = []
        for contract in self.contracts:
            for operation in contract.operations:
                if operation in owners:
                    duplicates.append(operation)
                owners[operation] = contract.service_id
        missing = sorted(set(OPERATION_TYPES) - set(owners))
        extra = sorted(set(owners) - set(OPERATION_TYPES))
        if duplicates or missing or extra:
            details = {
                "duplicates": sorted(duplicates),
                "missing": missing,
                "extra": extra,
            }
            raise ValueError(f"Invalid domain service registry operation coverage: {details}")

    def service_id_for_operation(self, operation: str) -> str:
        for contract in self.contracts:
            if operation in contract.operations:
                return contract.service_id
        raise ValueError(f"No domain service registered for operation {operation!r}")

    def operation_map(self) -> dict[str, str]:
        return {
            operation: contract.service_id
            for contract in self.contracts
            for operation in contract.operations
        }

    def to_dict(self) -> dict[str, Any]:
        return {
            "services": {
                contract.service_id: contract.to_dict()
                for contract in self.contracts
            },
            "operation_service_map": self.operation_map(),
        }


def make_chemworld_constitution() -> PhysicalConstitution:
    return PhysicalConstitution(
        substances=chemworld_substances(),
        vessel=Vessel(
            "batch_reactor",
            "Virtual 100 mL jacketed batch reactor",
            max_volume_L=0.10,
            max_temperature_K=470.0,
            max_pressure_Pa=550_000.0,
        ),
        instruments=chemworld_instruments(),
        max_yield=1.0,
        tolerance=5.0e-7,
    )


class ChemWorldDomainServices:
    """Runtime domain services called by operation kernels.

    Operation dispatch is table-driven so adding a new operation does not
    require editing a central ``if/elif`` block.
    """

    def __init__(
        self,
        world: ChemWorldParameters,
        constitution: PhysicalConstitution,
        compiled_mechanism: CompiledMechanism,
    ) -> None:
        self.world = world
        self.constitution = constitution
        self.service_registry = DomainServiceRegistry.default()
        self.service_registry.validate_operation_coverage()
        self.species_view = MechanismSpeciesView(compiled_mechanism)
        self.operation_recorder = ChemWorldOperationRecorder(constitution)
        self.primitive = ChemWorldPrimitiveOperationServices(world, self.species_view)
        self.reaction_thermal = ChemWorldReactionThermalServices(world, self.species_view)
        self.phase_separation = ChemWorldPhaseSeparationServices(world, self.species_view)
        self.crystallization = ChemWorldCrystallizationServices(self.species_view)
        self.distillation = ChemWorldDistillationServices(self.species_view)
        self.flow = ChemWorldFlowServices(self.species_view, self.reaction_thermal)
        self.electrochemical = ChemWorldElectrochemicalServices(world, self.species_view)
        self.instrument_cost = ChemWorldInstrumentCostServices(constitution)

    def apply_operation(
        self,
        state: WorldState,
        action: dict[str, Any],
    ) -> tuple[WorldState, OperationRecord]:
        operation = operation_name(action["operation"])
        before = state
        preconditions = self.constitution.check_preconditions(operation, state, action)
        if not all(preconditions.values()):
            next_state = self.primitive.penalize_invalid(state)
            return next_state, self.operation_recorder.record(
                operation,
                before,
                next_state,
                preconditions,
                action,
            )

        try:
            next_state = self.operation_methods()[operation](state, action)
        except KeyError as exc:
            raise ValueError(f"Unsupported operation: {operation}") from exc

        next_state = self.reaction_thermal.with_risk_and_pressure(next_state)
        return next_state, self.operation_recorder.record(
            operation,
            before,
            next_state,
            preconditions,
            action,
        )

    def operation_methods(
        self,
    ) -> dict[str, Callable[[WorldState, dict[str, Any]], WorldState]]:
        return {
            "add_reagent": self.primitive.add_reagent,
            "add_solvent": self.primitive.add_solvent,
            "add_catalyst": self.primitive.add_catalyst,
            "heat": lambda state, action: self.reaction_thermal.integrate(
                state, action, heat=True
            ),
            "wait": lambda state, action: self.reaction_thermal.integrate(
                state, action, heat=False
            ),
            "sample": self.primitive.sample,
            "quench": lambda state, _action: self.primitive.quench(state),
            "add_phase": self.phase_separation.add_phase,
            "add_extractant": self.phase_separation.add_extractant,
            "mix": self.phase_separation.mix_phases,
            "settle": self.phase_separation.settle_phases,
            "separate_phase": self.phase_separation.separate_phase,
            "wash": self.phase_separation.wash_phase,
            "dry": lambda state, _action: self.phase_separation.dry_phase(state),
            "concentrate": self.phase_separation.concentrate_phase,
            "transfer": self.phase_separation.transfer_phase,
            "seed_crystals": self.crystallization.seed_crystals,
            "cool_crystallize": self.crystallization.cool_crystallize,
            "filter_crystals": lambda state, _action: self.crystallization.filter_crystals(state),
            "evaporate": self.primitive.evaporate,
            "distill": self.distillation.distill,
            "collect_fraction": self.distillation.collect_fraction,
            "set_flow_rate": self.flow.set_flow_rate,
            "run_flow": self.flow.run_flow,
            "set_potential": self.electrochemical.set_potential,
            "electrolyze": self.electrochemical.electrolyze,
            "terminate": lambda state, _action: state.replace(terminated=True),
            "measure": self.instrument_cost.apply_measurement_cost,
        }

    def service_id_for_operation(self, operation: str) -> str:
        return self.service_registry.service_id_for_operation(operation)

    def to_dict(self) -> dict[str, Any]:
        return self.service_registry.to_dict()

    def penalize_invalid(self, state: WorldState) -> WorldState:
        return self.primitive.penalize_invalid(state)

    def record_operation(
        self,
        operation: str,
        before: WorldState,
        after: WorldState,
        preconditions: dict[str, bool],
        action: dict[str, Any],
    ) -> OperationRecord:
        return self.operation_recorder.record(operation, before, after, preconditions, action)
