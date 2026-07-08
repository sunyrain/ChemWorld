"""Domain services for ChemWorld runtime v2.

This module owns the remaining compact state-changing calculations that have
not yet been split into narrower Runtime v2 services. It is intentionally
called by operation kernels rather than by ``ChemWorldEnv`` directly.
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
from chemworld.physchem.separations import vle_shortcut_distillation
from chemworld.runtime.electrochemical_services import ChemWorldElectrochemicalServices
from chemworld.runtime.mechanisms import CompiledMechanism
from chemworld.runtime.phase_separation_services import ChemWorldPhaseSeparationServices
from chemworld.runtime.reaction_thermal_services import ChemWorldReactionThermalServices
from chemworld.runtime.record_services import ChemWorldOperationRecorder
from chemworld.runtime.species import MechanismSpeciesView
from chemworld.world.instruments import chemworld_instruments
from chemworld.world.ontology import chemworld_substances
from chemworld.world.operations import instrument_name, operation_name
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
        self.electrochemical = ChemWorldElectrochemicalServices(world, self.species_view)

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
            "seed_crystals": self._seed_crystals,
            "cool_crystallize": self._cool_crystallize,
            "filter_crystals": lambda state, _action: self._filter_crystals(state),
            "evaporate": self._evaporate,
            "distill": self._distill,
            "collect_fraction": self._collect_fraction,
            "set_flow_rate": self._set_flow_rate,
            "run_flow": self._run_flow,
            "set_potential": self.electrochemical.set_potential,
            "electrolyze": self.electrochemical.electrolyze,
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
        reacted_state = self.reaction_thermal.integrate(state, effective_action, heat=True)
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
