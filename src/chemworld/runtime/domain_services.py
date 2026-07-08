"""Operation composition services for ChemWorld runtime v2.

This module wires primitive reagent/sample helpers to focused Runtime v2
services. It is intentionally called by operation kernels rather than by
``ChemWorldEnv`` directly.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import numpy as np

from chemworld.core.actions import CATALYSTS, SOLVENTS
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
from chemworld.runtime.reaction_thermal_services import ChemWorldReactionThermalServices
from chemworld.runtime.record_services import ChemWorldOperationRecorder
from chemworld.runtime.species import MechanismSpeciesView
from chemworld.world.instruments import chemworld_instruments
from chemworld.world.ontology import chemworld_substances
from chemworld.world.operations import operation_name
from chemworld.world.parameters import ChemWorldParameters


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


def _action_float(action: dict[str, Any], key: str, default: float) -> float:
    value = action.get(key, default)
    return float(np.asarray(value).reshape(-1)[0])


def _action_index(action: dict[str, Any], key: str, default: int, count: int) -> int:
    return int(np.clip(int(_action_float(action, key, float(default))), 0, count - 1))


class ChemWorldDomainServices:
    """Runtime domain services called by operation kernels.

    Operation dispatch is table-driven so adding a new operation does not
    require editing a central ``if/elif`` block.
    """

    def __init__(
        self,
        world: ChemWorldParameters,
        constitution: PhysicalConstitution,
        compiled_mechanism: CompiledMechanism | None = None,
    ) -> None:
        self.world = world
        self.constitution = constitution
        self.species_view = MechanismSpeciesView(compiled_mechanism)
        self.operation_recorder = ChemWorldOperationRecorder(constitution)
        self.reaction_thermal = ChemWorldReactionThermalServices(world)
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
            next_state = self._penalize_invalid(state)
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
            "add_reagent": self._add_reagent,
            "add_solvent": self._add_solvent,
            "add_catalyst": self._add_catalyst,
            "heat": lambda state, action: self.reaction_thermal.integrate(
                state, action, heat=True
            ),
            "wait": lambda state, action: self.reaction_thermal.integrate(
                state, action, heat=False
            ),
            "sample": self._sample,
            "quench": lambda state, _action: self._quench(state),
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
            "evaporate": self._evaporate,
            "distill": self.distillation.distill,
            "collect_fraction": self.distillation.collect_fraction,
            "set_flow_rate": self.flow.set_flow_rate,
            "run_flow": self.flow.run_flow,
            "set_potential": self.electrochemical.set_potential,
            "electrolyze": self.electrochemical.electrolyze,
            "terminate": lambda state, _action: state.replace(terminated=True),
            "measure": self.instrument_cost.apply_measurement_cost,
        }

    def penalize_invalid(self, state: WorldState) -> WorldState:
        return self._penalize_invalid(state)

    def record_operation(
        self,
        operation: str,
        before: WorldState,
        after: WorldState,
        preconditions: dict[str, bool],
        action: dict[str, Any],
    ) -> OperationRecord:
        return self.operation_recorder.record(operation, before, after, preconditions, action)

    def _add_reagent(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        amount = float(np.clip(_action_float(action, "amount_mol", 0.003), 0.0, 0.040))
        species = state.species_amounts.copy()
        reactant = self.species_view.reactant_species(state)
        species[reactant] = species.get(reactant, 0.0) + amount
        metadata = state.metadata.copy()
        metadata = self.species_view.record_added_reactant(
            metadata,
            reactant_species=reactant,
            amount_mol=amount,
        )
        ledger = state.ledger.with_updates(cost=state.ledger.cost + 0.03 * amount / 0.01)
        return state.replace(species_amounts=species, ledger=ledger, metadata=metadata)

    def _add_solvent(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        volume = float(np.clip(_action_float(action, "volume_L", 0.025), 0.0, 0.080))
        solvent = _action_index(action, "solvent", 0, len(SOLVENTS))
        metadata = state.metadata.copy()
        metadata["solvent"] = solvent
        ledger = state.ledger.with_updates(
            cost=state.ledger.cost + volume * 8.0 * float(self.world.solvent_costs[solvent])
        )
        return state.replace(volume_L=state.volume_L + volume, ledger=ledger, metadata=metadata)

    def _add_catalyst(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        amount = float(np.clip(_action_float(action, "catalyst_amount_mol", 0.00020), 0.0, 0.005))
        catalyst = _action_index(action, "catalyst", 0, len(CATALYSTS))
        species = state.species_amounts.copy()
        active_catalyst = self.species_view.active_catalyst_species(state)
        species[active_catalyst] = species.get(active_catalyst, 0.0) + amount
        metadata = state.metadata.copy()
        metadata["catalyst"] = catalyst
        ledger = state.ledger.with_updates(
            cost=state.ledger.cost
            + 4.0 * amount / 0.001 * float(self.world.catalyst_costs[catalyst])
        )
        return state.replace(species_amounts=species, ledger=ledger, metadata=metadata)

    def _sample(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        volume = float(np.clip(_action_float(action, "sample_volume_L", 0.0001), 0.0, 0.002))
        volume = min(volume, max(state.volume_L, 0.0))
        fraction = 0.0 if state.volume_L <= 0 else volume / state.volume_L
        species = {key: value * (1.0 - fraction) for key, value in state.species_amounts.items()}
        ledger = state.ledger.with_updates(
            sample_consumed_L=state.ledger.sample_consumed_L + volume,
            cost=state.ledger.cost + 0.01,
        )
        return state.replace(
            species_amounts=species,
            volume_L=state.volume_L - volume,
            ledger=ledger,
        )

    def _quench(self, state: WorldState) -> WorldState:
        target = max(298.15, state.temperature_K - 45.0)
        ledger = state.ledger.with_updates(cost=state.ledger.cost + 0.03)
        return state.replace(temperature_K=target, quenched=True, ledger=ledger)

    def _evaporate(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        duration = float(np.clip(_action_float(action, "duration_s", 600.0), 0.0, 14_400.0))
        target_temperature = float(
            np.clip(_action_float(action, "target_temperature_K", 328.15), 298.15, 390.0)
        )
        removal = float(
            np.clip(
                0.08 + duration / 7200.0 + (target_temperature - 298.15) / 420.0,
                0.0,
                0.70,
            )
        )
        metadata = state.metadata.copy()
        metadata["solvent_loss"] = min(1.0, float(metadata.get("solvent_loss", 0.0)) + removal)
        ledger = state.ledger.with_updates(
            time_s=state.ledger.time_s + duration,
            cost=state.ledger.cost + duration / 3600.0 * 0.040,
            risk=min(1.0, state.ledger.risk + 0.04 * removal),
            energy_jacket_J=state.ledger.energy_jacket_J + 45.0 * duration,
        )
        return state.replace(
            volume_L=state.volume_L * (1.0 - 0.55 * removal),
            temperature_K=target_temperature,
            ledger=ledger,
            metadata=metadata,
        )

    def _penalize_invalid(self, state: WorldState) -> WorldState:
        ledger = state.ledger.with_updates(
            cost=state.ledger.cost + 0.01,
            risk=min(1.0, state.ledger.risk + 0.08),
        )
        return state.replace(ledger=ledger)
