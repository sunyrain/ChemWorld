"""Domain services for ChemWorld runtime v2.

This module owns the current compact physical calculations for reaction,
thermal, phase, separation, process, electrochemical, and instrument-cost
updates. It is intentionally called by operation kernels rather than by
``ChemWorldEnv`` directly.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import numpy as np

from chemworld.core.actions import CATALYSTS, SOLVENTS
from chemworld.foundation import (
    Observation,
    OperationRecord,
    PhysicalConstitution,
    Vessel,
    WorldState,
)
from chemworld.physchem.electrochemistry import ElectrodeReactionSpec, run_electrolysis
from chemworld.physchem.separations import vle_shortcut_distillation
from chemworld.runtime.mechanisms import CompiledMechanism
from chemworld.runtime.species import MechanismSpeciesView
from chemworld.world.instruments import chemworld_instruments
from chemworld.world.observation_kernel import (
    base_observed_mask,
    base_public_values,
    observation_units,
    processed_estimate,
    raw_signal,
)
from chemworld.world.ontology import chemworld_substances
from chemworld.world.operations import instrument_name, operation_name
from chemworld.world.parameters import ChemWorldParameters
from chemworld.world.phase_kernel import partition_split
from chemworld.world.reaction_kernel import integrate_reaction_ode
from chemworld.world.scoring import score_observation
from chemworld.world.separation_kernel import downstream_truth_values
from chemworld.world.species_roles import (
    LEGACY_PHASE_PRODUCT_AMOUNT_KEY,
    PHASE_PRODUCT_AMOUNT_KEY,
)
from chemworld.world.thermal_kernel import pressure_and_risk


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
            return next_state, self._record(operation, before, next_state, preconditions, action)

        try:
            next_state = self.operation_methods()[operation](state, action)
        except KeyError as exc:
            raise ValueError(f"Unsupported operation: {operation}") from exc

        next_state = self._with_risk_and_pressure(next_state)
        return next_state, self._record(operation, before, next_state, preconditions, action)

    def operation_methods(
        self,
    ) -> dict[str, Callable[[WorldState, dict[str, Any]], WorldState]]:
        return {
            "add_reagent": self._add_reagent,
            "add_solvent": self._add_solvent,
            "add_catalyst": self._add_catalyst,
            "heat": lambda state, action: self._integrate(state, action, heat=True),
            "wait": lambda state, action: self._integrate(state, action, heat=False),
            "sample": self._sample,
            "quench": lambda state, _action: self._quench(state),
            "add_phase": self._add_phase,
            "add_extractant": self._add_extractant,
            "mix": self._mix_phases,
            "settle": self._settle_phases,
            "separate_phase": self._separate_phase,
            "wash": self._wash_phase,
            "dry": lambda state, _action: self._dry_phase(state),
            "concentrate": self._concentrate_phase,
            "transfer": self._transfer_phase,
            "seed_crystals": self._seed_crystals,
            "cool_crystallize": self._cool_crystallize,
            "filter_crystals": lambda state, _action: self._filter_crystals(state),
            "evaporate": self._evaporate,
            "distill": self._distill,
            "collect_fraction": self._collect_fraction,
            "set_flow_rate": self._set_flow_rate,
            "run_flow": self._run_flow,
            "set_potential": self._set_potential,
            "electrolyze": self._electrolyze,
            "terminate": lambda state, _action: state.replace(terminated=True),
            "measure": self._apply_measurement_cost,
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
        return self._record(operation, before, after, preconditions, action)

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

    def _phase_ledger(self, state: WorldState) -> dict[str, dict[str, float]]:
        raw = state.metadata.get("phase_ledger", {})
        ledger: dict[str, dict[str, float]] = {}
        for phase_name, values in dict(raw).items():
            product_amount = values.get(
                PHASE_PRODUCT_AMOUNT_KEY,
                values.get(LEGACY_PHASE_PRODUCT_AMOUNT_KEY, 0.0),
            )
            ledger[str(phase_name)] = {
                "volume_L": float(values.get("volume_L", 0.0)),
                PHASE_PRODUCT_AMOUNT_KEY: float(product_amount),
                "impurity_mol": float(values.get("impurity_mol", 0.0)),
                "solvent_loss": float(values.get("solvent_loss", 0.0)),
            }
        if "reactor_liquid" not in ledger:
            ledger["reactor_liquid"] = {
                "volume_L": state.volume_L,
                PHASE_PRODUCT_AMOUNT_KEY: self.species_view.target_amount(state),
                "impurity_mol": self.species_view.impurity_amount(state),
                "solvent_loss": 0.0,
            }
        return ledger

    def _write_phase_metadata(
        self,
        state: WorldState,
        phase_ledger: dict[str, dict[str, float]],
        *,
        updates: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        metadata = state.metadata.copy()
        metadata["phase_ledger"] = phase_ledger
        metadata.update(
            downstream_truth_values(
                state,
                phase_ledger,
                product_amount_mol=self.species_view.target_amount(state),
                impurity_amount_mol=self.species_view.impurity_amount(state),
            )
        )
        if updates:
            metadata.update(updates)
        return metadata

    def _add_phase(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        volume = float(np.clip(_action_float(action, "volume_L", 0.015), 0.0, 0.060))
        phase_name = str(action.get("phase", "aqueous"))
        if phase_name not in {"aqueous", "organic"}:
            phase_name = "organic"
        phase_ledger = self._phase_ledger(state)
        phase = phase_ledger.setdefault(
            phase_name,
            {
                "volume_L": 0.0,
                PHASE_PRODUCT_AMOUNT_KEY: 0.0,
                "impurity_mol": 0.0,
                "solvent_loss": 0.0,
            },
        )
        phase["volume_L"] += volume
        metadata = self._write_phase_metadata(
            state,
            phase_ledger,
            updates={"phase_system": True, "phase_settled": False, "selected_phase": None},
        )
        ledger = state.ledger.with_updates(cost=state.ledger.cost + 0.015 + 0.35 * volume)
        return state.replace(volume_L=state.volume_L + volume, ledger=ledger, metadata=metadata)

    def _add_extractant(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        volume = float(np.clip(_action_float(action, "volume_L", 0.018), 0.0, 0.060))
        extractant = str(action.get("extractant", "organic"))
        phase_ledger = self._phase_ledger(state)
        organic = phase_ledger.setdefault(
            "organic",
            {
                "volume_L": 0.0,
                PHASE_PRODUCT_AMOUNT_KEY: 0.0,
                "impurity_mol": 0.0,
                "solvent_loss": 0.0,
            },
        )
        organic["volume_L"] += volume
        metadata = self._write_phase_metadata(
            state,
            phase_ledger,
            updates={
                "phase_system": True,
                "phase_settled": False,
                "extractant": extractant,
                "selected_phase": None,
            },
        )
        solvent = int(state.metadata.get("solvent", 0))
        risk = min(1.0, state.ledger.risk + 0.04 + 0.05 * float(self.world.solvent_risks[solvent]))
        ledger = state.ledger.with_updates(
            cost=state.ledger.cost + 0.025 + 0.80 * volume,
            risk=risk,
        )
        return state.replace(volume_L=state.volume_L + volume, ledger=ledger, metadata=metadata)

    def _mix_phases(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        duration = float(np.clip(_action_float(action, "duration_s", 180.0), 0.0, 1800.0))
        stirring = float(np.clip(_action_float(action, "stirring_speed_rpm", 700.0), 100.0, 1200.0))
        phase_ledger = self._phase_ledger(state)
        phase_ledger.setdefault(
            "aqueous",
            {
                "volume_L": max(
                    state.volume_L - phase_ledger.get("organic", {}).get("volume_L", 0.0), 0.0
                ),
                PHASE_PRODUCT_AMOUNT_KEY: 0.0,
                "impurity_mol": 0.0,
                "solvent_loss": 0.0,
            },
        )
        organic = phase_ledger.setdefault(
            "organic",
            {
                "volume_L": 0.015,
                PHASE_PRODUCT_AMOUNT_KEY: 0.0,
                "impurity_mol": 0.0,
                "solvent_loss": 0.0,
            },
        )
        aqueous = phase_ledger["aqueous"]
        p_total = self.species_view.target_amount(state)
        impurity_total = self.species_view.impurity_amount(state)
        solvent = int(state.metadata.get("solvent", 0))
        split = partition_split(
            product_mol=p_total,
            impurity_mol=impurity_total,
            solvent=solvent,
            temperature_K=state.temperature_K,
            duration_s=duration,
            stirring_speed_rpm=stirring,
            organic_volume_L=organic["volume_L"],
            aqueous_volume_L=aqueous["volume_L"],
        )
        organic[PHASE_PRODUCT_AMOUNT_KEY] = split["organic_product_mol"]
        aqueous[PHASE_PRODUCT_AMOUNT_KEY] = split["aqueous_product_mol"]
        organic["impurity_mol"] = split["organic_impurity_mol"]
        aqueous["impurity_mol"] = split["aqueous_impurity_mol"]
        phase_ledger["reactor_liquid"] = {
            "volume_L": state.volume_L,
            PHASE_PRODUCT_AMOUNT_KEY: p_total,
            "impurity_mol": impurity_total,
            "solvent_loss": 0.0,
        }
        metadata = self._write_phase_metadata(
            state,
            phase_ledger,
            updates={
                "phase_system": True,
                "phase_settled": False,
                "partition_coefficient": split["partition_coefficient"],
                "stirring_speed_rpm": stirring,
            },
        )
        ledger = state.ledger.with_updates(
            time_s=state.ledger.time_s + duration,
            cost=state.ledger.cost + 0.01 + duration / 3600.0 * 0.015,
        )
        return state.replace(ledger=ledger, metadata=metadata)

    def _settle_phases(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        duration = float(np.clip(_action_float(action, "duration_s", 300.0), 0.0, 3600.0))
        phase_ledger = self._phase_ledger(state)
        metadata = self._write_phase_metadata(
            state,
            phase_ledger,
            updates={"phase_system": True, "phase_settled": duration >= 60.0},
        )
        ledger = state.ledger.with_updates(
            time_s=state.ledger.time_s + duration,
            cost=state.ledger.cost + duration / 3600.0 * 0.006,
        )
        return state.replace(ledger=ledger, metadata=metadata)

    def _separate_phase(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        target = str(action.get("target_phase", "organic"))
        if target not in {"organic", "aqueous"}:
            target = "organic"
        phase_ledger = self._phase_ledger(state)
        selected = phase_ledger.get(
            target,
            {
                "volume_L": state.volume_L,
                PHASE_PRODUCT_AMOUNT_KEY: self.species_view.target_amount(state),
                "impurity_mol": 0.0,
                "solvent_loss": 0.0,
            },
        )
        entrainment_loss = 0.025 if target == "organic" else 0.045
        retained_p = selected[PHASE_PRODUCT_AMOUNT_KEY] * (1.0 - entrainment_loss)
        retained_impurity = selected["impurity_mol"] * (1.0 + 0.20 * entrainment_loss)
        phase_ledger[target] = {
            "volume_L": selected["volume_L"] * (1.0 - 0.015),
            PHASE_PRODUCT_AMOUNT_KEY: retained_p,
            "impurity_mol": retained_impurity,
            "solvent_loss": selected.get("solvent_loss", 0.0) + entrainment_loss,
        }
        metadata = self._write_phase_metadata(
            state,
            phase_ledger,
            updates={"selected_phase": target, "phase_system": True, "phase_settled": True},
        )
        ledger = state.ledger.with_updates(cost=state.ledger.cost + 0.025)
        return state.replace(
            volume_L=phase_ledger[target]["volume_L"], ledger=ledger, metadata=metadata
        )

    def _wash_phase(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        volume = float(np.clip(_action_float(action, "wash_volume_L", 0.010), 0.0, 0.040))
        phase_ledger = self._phase_ledger(state)
        target = str(state.metadata.get("selected_phase") or "organic")
        phase = phase_ledger.setdefault(
            target,
            {
                "volume_L": state.volume_L,
                PHASE_PRODUCT_AMOUNT_KEY: self.species_view.target_amount(state),
                "impurity_mol": 0.0,
                "solvent_loss": 0.0,
            },
        )
        impurity_removal = float(np.clip(0.18 + 8.0 * volume, 0.0, 0.65))
        phase["impurity_mol"] *= 1.0 - impurity_removal
        phase[PHASE_PRODUCT_AMOUNT_KEY] *= 1.0 - 0.015
        phase["volume_L"] += volume * 0.35
        phase["solvent_loss"] += 0.012
        metadata = self._write_phase_metadata(
            state, phase_ledger, updates={"selected_phase": target}
        )
        ledger = state.ledger.with_updates(cost=state.ledger.cost + 0.02 + 0.25 * volume)
        return state.replace(volume_L=phase["volume_L"], ledger=ledger, metadata=metadata)

    def _dry_phase(self, state: WorldState) -> WorldState:
        phase_ledger = self._phase_ledger(state)
        target = str(state.metadata.get("selected_phase") or "organic")
        phase = phase_ledger.setdefault(
            target,
            {
                "volume_L": state.volume_L,
                PHASE_PRODUCT_AMOUNT_KEY: self.species_view.target_amount(state),
                "impurity_mol": 0.0,
                "solvent_loss": 0.0,
            },
        )
        phase["solvent_loss"] = max(0.0, phase.get("solvent_loss", 0.0) * 0.35)
        phase["volume_L"] *= 0.92
        metadata = self._write_phase_metadata(
            state, phase_ledger, updates={"selected_phase": target}
        )
        ledger = state.ledger.with_updates(
            time_s=state.ledger.time_s + 300.0, cost=state.ledger.cost + 0.018
        )
        return state.replace(volume_L=phase["volume_L"], ledger=ledger, metadata=metadata)

    def _concentrate_phase(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        duration = float(np.clip(_action_float(action, "duration_s", 300.0), 0.0, 3600.0))
        phase_ledger = self._phase_ledger(state)
        target = str(state.metadata.get("selected_phase") or "organic")
        phase = phase_ledger.setdefault(
            target,
            {
                "volume_L": state.volume_L,
                PHASE_PRODUCT_AMOUNT_KEY: self.species_view.target_amount(state),
                "impurity_mol": 0.0,
                "solvent_loss": 0.0,
            },
        )
        concentration_factor = float(np.clip(1.0 - duration / 7200.0, 0.45, 1.0))
        phase["volume_L"] *= concentration_factor
        phase[PHASE_PRODUCT_AMOUNT_KEY] *= 1.0 - 0.01 * (1.0 - concentration_factor)
        phase["solvent_loss"] += 0.025 * (1.0 - concentration_factor)
        metadata = self._write_phase_metadata(
            state, phase_ledger, updates={"selected_phase": target}
        )
        ledger = state.ledger.with_updates(
            time_s=state.ledger.time_s + duration,
            cost=state.ledger.cost + duration / 3600.0 * 0.035,
            risk=min(1.0, state.ledger.risk + 0.015 * (1.0 - concentration_factor)),
        )
        return state.replace(volume_L=phase["volume_L"], ledger=ledger, metadata=metadata)

    def _transfer_phase(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        fraction = float(np.clip(_action_float(action, "transfer_fraction", 0.98), 0.0, 1.0))
        phase_ledger = self._phase_ledger(state)
        target = str(state.metadata.get("selected_phase") or "organic")
        phase = phase_ledger.setdefault(
            target,
            {
                "volume_L": state.volume_L,
                PHASE_PRODUCT_AMOUNT_KEY: self.species_view.target_amount(state),
                "impurity_mol": 0.0,
                "solvent_loss": 0.0,
            },
        )
        phase[PHASE_PRODUCT_AMOUNT_KEY] *= fraction
        phase["impurity_mol"] *= fraction
        phase["volume_L"] *= fraction
        phase["solvent_loss"] += 1.0 - fraction
        metadata = self._write_phase_metadata(
            state, phase_ledger, updates={"selected_phase": target}
        )
        ledger = state.ledger.with_updates(cost=state.ledger.cost + 0.01)
        return state.replace(volume_L=phase["volume_L"], ledger=ledger, metadata=metadata)

    def _seed_crystals(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        seed_mass = float(np.clip(_action_float(action, "seed_mass_g", 0.005), 0.0, 0.050))
        metadata = state.metadata.copy()
        metadata["crystal_seeded"] = seed_mass > 0.0
        metadata["crystal_seed_mass_g"] = seed_mass
        ledger = state.ledger.with_updates(cost=state.ledger.cost + 0.012 + 0.20 * seed_mass)
        return state.replace(ledger=ledger, metadata=metadata)

    def _cool_crystallize(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        duration = float(np.clip(_action_float(action, "duration_s", 1200.0), 0.0, 14_400.0))
        target_temperature = float(
            np.clip(_action_float(action, "target_temperature_K", 278.15), 250.0, 330.0)
        )
        cooling_depth = float(np.clip((state.temperature_K - target_temperature) / 55.0, 0.0, 1.0))
        time_factor = float(np.clip(1.0 - np.exp(-duration / 1800.0), 0.0, 1.0))
        seed_factor = 1.08 if bool(state.metadata.get("crystal_seeded", False)) else 0.92
        p_mol = self.species_view.target_amount(state)
        impurity_mol = self.species_view.impurity_amount(state)
        crystallized = float(np.clip(p_mol * cooling_depth * time_factor * seed_factor, 0.0, p_mol))
        occluded_impurity = float(
            np.clip(impurity_mol * (0.035 + 0.080 * cooling_depth) * time_factor, 0.0, impurity_mol)
        )
        crystal_purity = crystallized / max(crystallized + occluded_impurity, 1.0e-12)
        initial_p = max(
            float(state.metadata.get("pre_separation_product_mol", p_mol)),
            p_mol,
            1.0e-12,
        )
        metadata = state.metadata.copy()
        metadata.update(
            {
                "crystallization_active": True,
                "crystal_product_mol": crystallized,
                "crystal_impurity_mol": occluded_impurity,
                "crystal_yield": float(np.clip(crystallized / initial_p, 0.0, 1.0)),
                "crystal_purity": float(np.clip(crystal_purity, 0.0, 1.0)),
                "crystal_size": float(np.clip(0.25 + 0.65 * time_factor * seed_factor, 0.0, 1.0)),
            }
        )
        ledger = state.ledger.with_updates(
            time_s=state.ledger.time_s + duration,
            cost=state.ledger.cost + 0.018 + duration / 3600.0 * 0.018,
            risk=max(0.0, state.ledger.risk - 0.02 * cooling_depth),
        )
        return state.replace(temperature_K=target_temperature, ledger=ledger, metadata=metadata)

    def _filter_crystals(self, state: WorldState) -> WorldState:
        metadata = state.metadata.copy()
        product = float(metadata.get("crystal_product_mol", 0.0)) * 0.96
        impurity = float(metadata.get("crystal_impurity_mol", 0.0)) * 0.92
        purity = product / max(product + impurity, 1.0e-12)
        initial_p = max(
            float(
                state.metadata.get(
                    "pre_separation_product_mol",
                    self.species_view.target_amount(state),
                )
            ),
            self.species_view.target_amount(state),
            1.0e-12,
        )
        metadata.update(
            {
                "selected_phase": "solid",
                "crystals_filtered": True,
                "crystal_product_mol": product,
                "crystal_impurity_mol": impurity,
                "crystal_yield": float(np.clip(product / initial_p, 0.0, 1.0)),
                "crystal_purity": float(np.clip(purity, 0.0, 1.0)),
                "recovery": float(np.clip(product / initial_p, 0.0, 1.0)),
                "purity": float(np.clip(purity, 0.0, 1.0)),
                "solvent_loss": min(1.0, float(metadata.get("solvent_loss", 0.0)) + 0.04),
            }
        )
        ledger = state.ledger.with_updates(
            time_s=state.ledger.time_s + 480.0,
            cost=state.ledger.cost + 0.026,
        )
        return state.replace(ledger=ledger, metadata=metadata)

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

    def _distill(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        duration = float(np.clip(_action_float(action, "duration_s", 1200.0), 0.0, 14_400.0))
        target_temperature = float(
            np.clip(_action_float(action, "target_temperature_K", 345.15), 298.15, 430.0)
        )
        reflux = float(np.clip(_action_float(action, "reflux_ratio", 1.5), 0.0, 10.0))
        p_mol = self.species_view.target_amount(state)
        impurity_mol = self.species_view.impurity_amount(state)
        distillate_cut = float(np.clip(0.25 + duration / 9000.0, 0.05, 0.90))
        theoretical_stages = float(np.clip(2.0 + duration / 900.0, 1.0, 20.0))
        if p_mol + impurity_mol <= 1.0e-12:
            distillate_product = 0.0
            distillate_impurity = 0.0
            distillate_purity = 0.0
            distillation_metadata: dict[str, object] = {"no_distillable_material": True}
            heat_duty = (70.0 + 8.0 * reflux) * duration
            distillation_cost = 0.045 + duration / 3600.0 * (0.065 + 0.012 * reflux)
            distillation_risk = 0.035 + 0.06 * ((target_temperature - 298.15) / 132.0)
        else:
            distillation = vle_shortcut_distillation(
                {"product": p_mol, "impurity": impurity_mol},
                vapor_pressures_Pa={"product": 78_000.0, "impurity": 18_000.0},
                pressure_Pa=max(state.pressure_Pa, 1.0),
                temperature_K=target_temperature,
                light_key="product",
                heavy_key="impurity",
                distillate_cut_fraction=distillate_cut,
                theoretical_stages=theoretical_stages,
                reflux_ratio=reflux,
                stage_efficiency=0.62,
                latent_heats_J_mol={"product": 38_000.0, "impurity": 55_000.0},
            )
            distillate = distillation.outlet("distillate")
            distillate_product = distillate.get("product", 0.0)
            distillate_impurity = distillate.get("impurity", 0.0)
            distillate_purity = distillation.purity("product", "distillate")
            distillation_metadata = distillation.ledger.metadata
            heat_duty = distillation.ledger.heat_duty_J
            distillation_cost = distillation.ledger.cost
            distillation_risk = distillation.ledger.risk
        initial_p = max(
            float(state.metadata.get("pre_separation_product_mol", p_mol)),
            p_mol,
            1.0e-12,
        )
        metadata = state.metadata.copy()
        metadata.update(
            {
                "distillation_active": True,
                "distillate_product_mol": float(distillate_product),
                "distillate_impurity_mol": float(distillate_impurity),
                "distillate_purity": float(np.clip(distillate_purity, 0.0, 1.0)),
                "distillate_recovery": float(np.clip(distillate_product / initial_p, 0.0, 1.0)),
                "distillation_model": "vle_shortcut_distillation",
                "distillation_kernel": distillation_metadata,
            }
        )
        risk = min(1.0, state.ledger.risk + distillation_risk)
        ledger = state.ledger.with_updates(
            time_s=state.ledger.time_s + duration,
            cost=state.ledger.cost + distillation_cost,
            risk=risk,
            energy_jacket_J=state.ledger.energy_jacket_J + heat_duty,
        )
        return state.replace(
            volume_L=max(state.volume_L * 0.62, 0.001),
            temperature_K=target_temperature,
            ledger=ledger,
            metadata=metadata,
        )

    def _collect_fraction(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        fraction = float(np.clip(_action_float(action, "transfer_fraction", 0.90), 0.0, 1.0))
        product = float(state.metadata.get("distillate_product_mol", 0.0)) * fraction
        impurity = float(state.metadata.get("distillate_impurity_mol", 0.0)) * fraction
        purity = product / max(product + impurity, 1.0e-12)
        initial_p = max(
            float(
                state.metadata.get(
                    "pre_separation_product_mol",
                    self.species_view.target_amount(state),
                )
            ),
            self.species_view.target_amount(state),
            1.0e-12,
        )
        metadata = state.metadata.copy()
        metadata.update(
            {
                "selected_phase": "distillate",
                "fraction_collected": True,
                "distillate_product_mol": product,
                "distillate_impurity_mol": impurity,
                "distillate_purity": float(np.clip(purity, 0.0, 1.0)),
                "distillate_recovery": float(np.clip(product / initial_p, 0.0, 1.0)),
                "purity": float(np.clip(purity, 0.0, 1.0)),
                "recovery": float(np.clip(product / initial_p, 0.0, 1.0)),
            }
        )
        ledger = state.ledger.with_updates(cost=state.ledger.cost + 0.018)
        return state.replace(volume_L=state.volume_L * fraction, ledger=ledger, metadata=metadata)

    def _set_flow_rate(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        flow_rate = float(np.clip(_action_float(action, "flow_rate_mL_min", 1.0), 0.01, 20.0))
        residence = float(np.clip(_action_float(action, "residence_time_s", 600.0), 1.0, 7200.0))
        metadata = state.metadata.copy()
        metadata["flow_rate_mL_min"] = flow_rate
        metadata["residence_time_s"] = residence
        ledger = state.ledger.with_updates(cost=state.ledger.cost + 0.012)
        return state.replace(ledger=ledger, metadata=metadata)

    def _run_flow(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        residence = float(
            state.metadata.get(
                "residence_time_s",
                _action_float(action, "duration_s", 600.0),
            )
        )
        duration = float(
            np.clip(_action_float(action, "duration_s", residence), residence, 14_400.0)
        )
        target_temperature = float(
            np.clip(_action_float(action, "target_temperature_K", 348.15), 298.15, 430.0)
        )
        effective_action = {
            "duration_s": residence,
            "target_temperature_K": target_temperature,
            "stirring_speed_rpm": 900.0,
        }
        reacted_state = self._integrate(state, effective_action, heat=True)
        initial_a = max(self.species_view.initial_reactant_amount(state), 1.0e-12)
        conversion = float(
            np.clip(
                (initial_a - self.species_view.reactant_amount(reacted_state)) / initial_a,
                0.0,
                1.0,
            )
        )
        metadata = reacted_state.metadata.copy()
        metadata["flow_conversion"] = conversion
        metadata["flow_campaign_time_s"] = duration
        ledger = reacted_state.ledger.with_updates(
            time_s=state.ledger.time_s + duration,
            cost=reacted_state.ledger.cost + duration / 3600.0 * 0.030,
            risk=min(1.0, reacted_state.ledger.risk + 0.015 * (target_temperature > 390.0)),
        )
        return reacted_state.replace(ledger=ledger, metadata=metadata)

    def _set_potential(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        potential = float(np.clip(_action_float(action, "potential_V", 1.20), -3.0, 3.0))
        current = float(np.clip(_action_float(action, "current_mA", 50.0), 0.0, 500.0))
        metadata = state.metadata.copy()
        metadata["potential_V"] = potential
        metadata["current_mA"] = current
        risk = min(1.0, state.ledger.risk + 0.02 * max(abs(potential) - 1.5, 0.0))
        ledger = state.ledger.with_updates(cost=state.ledger.cost + 0.010, risk=risk)
        return state.replace(ledger=ledger, metadata=metadata)

    def _electrolyze(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        duration = float(np.clip(_action_float(action, "duration_s", 900.0), 0.0, 14_400.0))
        potential = float(state.metadata.get("potential_V", 1.20))
        current_mA = float(state.metadata.get("current_mA", 50.0))
        species = state.species_amounts.copy()
        reactant = self.species_view.reactant_species(state)
        product = self.species_view.primary_target_species
        impurity = self.species_view.primary_impurity_species
        a_mol = species.get(reactant, 0.0)
        volume = max(state.volume_L, 1.0e-9)
        catalyst = int(state.metadata.get("catalyst", 0))
        solvent = int(state.metadata.get("solvent", 0))
        exchange_current_density = 28.0 * float(self.world.catalyst_effects[catalyst, 0])
        exchange_current_density *= float(self.world.solvent_effects[solvent, 0])
        electrochemical_spec = ElectrodeReactionSpec(
            reaction_id=f"{reactant}_to_{product}_electrochemical",
            electrons_transferred=2.0,
            standard_potential_V=1.05,
            reaction_quotient_exponents={product: 1.0, reactant: -1.0},
            exchange_current_density_A_m2=exchange_current_density,
            electrode_area_m2=0.004,
            faradaic_efficiency_ref=0.91,
            product_selectivity_ref=0.90,
            overpotential_selectivity_sensitivity_V_inv=0.45,
        )
        activities = {
            reactant: max(a_mol / volume, 1.0e-12),
            product: max(species.get(product, 0.0) / volume, 1.0e-12),
        }
        result = run_electrolysis(
            electrochemical_spec,
            electrode_potential_V=potential,
            duration_s=duration,
            activities=activities,
            available_substrate_mol=a_mol,
            temperature_K=state.temperature_K,
            applied_current_A=current_mA / 1000.0,
        )
        species[reactant] = a_mol - result.converted_mol
        species[product] = species.get(product, 0.0) + result.product_mol
        species[impurity] = species.get(impurity, 0.0) + result.byproduct_mol
        metadata = state.metadata.copy()
        metadata["electrochemical_model"] = "nernst_butler_volmer_faradaic_v1"
        metadata["electrochemical_selectivity"] = result.product_selectivity
        metadata["faradaic_efficiency"] = result.faradaic_efficiency
        metadata["energy_efficiency"] = result.energy_efficiency
        metadata["equilibrium_potential_V"] = result.equilibrium_potential_V
        metadata["overpotential_V"] = result.overpotential_V
        metadata["kinetic_current_A"] = result.kinetic_current_A
        metadata["actual_current_A"] = result.actual_current_A
        metadata["charge_C"] = result.charge_C
        metadata["faradaic_charge_C"] = result.faradaic_charge_C
        metadata["electrical_work_J"] = result.electrical_work_J
        overpotential_risk = max(abs(result.overpotential_V) - 0.35, 0.0)
        ledger = state.ledger.with_updates(
            time_s=state.ledger.time_s + duration,
            cost=state.ledger.cost + 0.018 + result.electrical_work_J / 250_000.0,
            risk=min(
                1.0,
                state.ledger.risk
                + 0.015
                + 0.025 * abs(potential)
                + 0.035 * overpotential_risk,
            ),
            energy_jacket_J=state.ledger.energy_jacket_J + result.electrical_work_J,
        )
        return state.replace(species_amounts=species, ledger=ledger, metadata=metadata)

    def _apply_measurement_cost(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        instrument_id = instrument_name(action.get("instrument", "hplc"))
        instrument = self.constitution.instruments[instrument_id]
        volume = min(instrument.sample_volume_L, max(state.volume_L, 0.0))
        fraction = 0.0 if state.volume_L <= 0 else volume / state.volume_L
        species = {key: value * (1.0 - fraction) for key, value in state.species_amounts.items()}
        ledger = state.ledger.with_updates(
            cost=state.ledger.cost + instrument.cost,
            sample_consumed_L=state.ledger.sample_consumed_L + volume,
        )
        metadata = state.metadata.copy()
        if instrument_id == "final_assay":
            metadata["final_assay_done"] = True
            metadata["final_assay_time_s"] = state.ledger.time_s
        return state.replace(
            species_amounts=species,
            volume_L=state.volume_L - volume,
            ledger=ledger,
            metadata=metadata,
        )

    def _penalize_invalid(self, state: WorldState) -> WorldState:
        ledger = state.ledger.with_updates(
            cost=state.ledger.cost + 0.01,
            risk=min(1.0, state.ledger.risk + 0.08),
        )
        return state.replace(ledger=ledger)

    def _integrate(self, state: WorldState, action: dict[str, Any], *, heat: bool) -> WorldState:
        duration = float(np.clip(_action_float(action, "duration_s", 600.0), 0.0, 14_400.0))
        target_temperature = _action_float(action, "target_temperature_K", state.temperature_K)
        stirring_speed = _action_float(
            action,
            "stirring_speed_rpm",
            float(state.metadata.get("stirring_speed_rpm", 600.0)),
        )
        result = integrate_reaction_ode(
            state=state,
            world=self.world,
            duration_s=duration,
            target_temperature_K=target_temperature,
            heat=heat,
            stirring_speed_rpm=stirring_speed,
        )
        if result is None:
            return state
        ledger = state.ledger.with_updates(
            time_s=state.ledger.time_s + result.duration_s,
            cost=state.ledger.cost + result.cost_delta,
            energy_jacket_J=state.ledger.energy_jacket_J + result.energy_jacket_J,
            heat_reaction_J=state.ledger.heat_reaction_J + result.heat_reaction_J,
            heat_loss_J=state.ledger.heat_loss_J + result.heat_loss_J,
        )
        metadata = state.metadata.copy()
        metadata["stirring_speed_rpm"] = result.stirring_speed_rpm
        return state.replace(
            species_amounts=result.species_amounts,
            temperature_K=result.temperature_K,
            ledger=ledger,
            metadata=metadata,
        )

    def _with_risk_and_pressure(self, state: WorldState) -> WorldState:
        pressure, risk = pressure_and_risk(
            state=state,
            solvent_risks=self.world.solvent_risks,
        )
        return state.replace(pressure_Pa=pressure, ledger=state.ledger.with_updates(risk=risk))

    def _record(
        self,
        operation: str,
        before: WorldState,
        after: WorldState,
        preconditions: dict[str, bool],
        action: dict[str, Any] | None = None,
    ) -> OperationRecord:
        action = action or {}
        report = self.constitution.check_state(after)
        material_check = self.constitution.check_material_conservation(before, after)
        if operation in {
            "add_reagent",
            "add_catalyst",
            "add_solvent",
            "sample",
            "measure",
            "add_phase",
            "add_extractant",
            "mix",
            "settle",
            "separate_phase",
            "wash",
            "dry",
            "concentrate",
            "transfer",
        }:
            material_check = material_check.__class__(
                "material_conservation",
                True,
                "material delta allowed or phase-ledger conserved for operation",
                value=0.0,
                tolerance=self.constitution.tolerance,
            )
        checks = [*report.checks, material_check]
        measurement_cost = 0.0
        sample_consumed = 0.0
        instrument = None
        preconditions_passed = all(preconditions.values())
        if operation == "measure":
            instrument = instrument_name(action.get("instrument", "hplc"))
            if preconditions_passed:
                measurement_cost = self.constitution.instruments[instrument].cost
                sample_consumed = self.constitution.instruments[instrument].sample_volume_L
        state_delta_summary = {
            "delta_time_s": after.ledger.time_s - before.ledger.time_s,
            "delta_cost": after.ledger.cost - before.ledger.cost,
            "delta_risk": after.ledger.risk - before.ledger.risk,
            "delta_temperature_K": after.temperature_K - before.temperature_K,
            "delta_volume_L": after.volume_L - before.volume_L,
        }
        if operation == "electrolyze":
            for key in (
                "equilibrium_potential_V",
                "overpotential_V",
                "actual_current_A",
                "charge_C",
                "faradaic_charge_C",
                "faradaic_efficiency",
                "electrical_work_J",
            ):
                if key in after.metadata:
                    state_delta_summary[key] = after.metadata[key]
        return OperationRecord(
            operation_type=operation,
            preconditions=preconditions,
            state_delta_summary=state_delta_summary,
            constitution_checks=[check.to_dict() for check in checks],
            instrument=instrument,
            measurement_cost=measurement_cost,
            sample_consumed_L=sample_consumed,
        )


class ChemWorldObservationKernel:
    def __init__(
        self,
        constitution: PhysicalConstitution,
        objective: str,
        compiled_mechanism: CompiledMechanism | None = None,
    ) -> None:
        self.constitution = constitution
        self.objective = objective
        self.compiled_mechanism = compiled_mechanism
        self.species_view = MechanismSpeciesView(compiled_mechanism)

    def observe(
        self,
        state: WorldState,
        action: dict[str, Any],
        rng: np.random.Generator,
    ) -> Observation:
        operation = operation_name(action["operation"])
        if operation != "measure":
            last = dict(state.metadata.get("last_observation", {}))
            last_mask = dict(state.metadata.get("last_observed_mask", {}))
            values = self._base_public_values(state)
            observed_mask = self._base_observed_mask()
            values.update(last)
            observed_mask.update({str(key): bool(value) for key, value in last_mask.items()})
            values["cost"] = min(1.0, state.ledger.cost)
            values["safety_risk"] = state.ledger.risk
            observed_mask["cost"] = True
            observed_mask["safety_risk"] = True
            values["score"] = self._score(values)
            observed_mask["score"] = True
            return Observation(
                values=values,
                units=self._observation_units(),
                observed_mask=observed_mask,
                processed_estimate=self._processed_estimate(values, observed_mask),
            )

        instrument_id = instrument_name(action.get("instrument", "hplc"))
        instrument = self.constitution.instruments[instrument_id]
        truth_values = self._truth_values(state)
        noisy = self._base_public_values(state)
        observed_mask = self._base_observed_mask()
        for key in instrument.observable_keys:
            std = instrument.noise_std.get(key, 0.0)
            noisy[key] = float(np.clip(truth_values[key] + rng.normal(0.0, std), 0.0, 1.0))
            observed_mask[key] = True

        if observed_mask["byproduct_signal"] and observed_mask["degradation_warning"]:
            byproduct_signal = self._observed_value(noisy, "byproduct_signal")
            degradation_warning = self._observed_value(noisy, "degradation_warning")
            noisy["virtual_spectrum_summary"] = float(
                np.clip(
                    0.55 * byproduct_signal + 0.45 * degradation_warning,
                    0.0,
                    1.0,
                )
            )
            observed_mask["virtual_spectrum_summary"] = True
        noisy["cost"] = min(1.0, state.ledger.cost)
        noisy["safety_risk"] = state.ledger.risk
        observed_mask["cost"] = True
        observed_mask["safety_risk"] = True
        noisy["score"] = self._score(noisy)
        observed_mask["score"] = True
        return Observation(
            values=noisy,
            units=self._observation_units(),
            observed_mask=observed_mask,
            raw_signal=self._raw_signal(instrument_id, noisy, state, rng),
            processed_estimate=self._processed_estimate(noisy, observed_mask),
            uncertainty={
                f"{key}_std": float(std)
                for key, std in instrument.noise_std.items()
                if observed_mask.get(key, False)
            },
            instrument_id=instrument_id,
            cost=instrument.cost,
            sample_consumed_L=instrument.sample_volume_L,
        )

    def failed_observation(self) -> Observation:
        """Return a non-informative observation for failed action preconditions."""

        units = self._observation_units()
        return Observation(
            values=dict.fromkeys(units, None),
            units=units,
            observed_mask=dict.fromkeys(units, False),
            raw_signal={},
            processed_estimate={},
            uncertainty={},
            instrument_id=None,
            cost=0.0,
            sample_consumed_L=0.0,
        )

    @staticmethod
    def _processed_estimate(
        values: dict[str, float | None],
        observed_mask: dict[str, bool],
    ) -> dict[str, float | None]:
        return processed_estimate(values, observed_mask)

    @staticmethod
    def _raw_signal(
        instrument_id: str,
        values: dict[str, float | None],
        state: WorldState,
        rng: np.random.Generator,
    ) -> dict[str, Any]:
        replicate_count = 3 if instrument_id == "final_assay" else 2
        return raw_signal(
            instrument_id,
            values,
            species_amounts_mol=state.species_amounts,
            volume_L=state.volume_L,
            seed=int(rng.integers(0, 2**31 - 1)),
            replicate_count=replicate_count,
        )

    @staticmethod
    def _observation_units() -> dict[str, str]:
        return observation_units()

    @staticmethod
    def _base_public_values(state: WorldState) -> dict[str, float | None]:
        return base_public_values(cost=state.ledger.cost, safety_risk=state.ledger.risk)

    @staticmethod
    def _base_observed_mask() -> dict[str, bool]:
        return base_observed_mask()

    @staticmethod
    def _observed_value(values: dict[str, float | None], key: str) -> float:
        value = values.get(key)
        return 0.0 if value is None else float(value)

    def _score(self, values: dict[str, float | None]) -> float:
        return score_observation(
            objective=self.objective,
            product_yield=self._observed_value(values, "yield"),
            selectivity=self._observed_value(values, "selectivity"),
            conversion=self._observed_value(values, "conversion"),
            cost=self._observed_value(values, "cost"),
            safety_risk=self._observed_value(values, "safety_risk"),
        )

    def _truth_values(self, state: WorldState) -> dict[str, float]:
        truth = self.species_view.truth_values(state)
        truth.update(
            downstream_truth_values(
                state,
                product_amount_mol=self.species_view.target_amount(state),
                impurity_amount_mol=self.species_view.impurity_amount(state),
                initial_product_mol=max(self.species_view.initial_reactant_amount(state), 1.0e-12),
            )
        )
        return truth
