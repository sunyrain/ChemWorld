"""Phase-ledger and downstream separation helpers for ChemWorld Runtime v2."""

from __future__ import annotations

from typing import Any

import numpy as np

from chemworld.foundation import (
    WorldState,
    equipment_settings,
    process_with_metrics,
    upsert_equipment_record,
)
from chemworld.foundation.state import (
    EquipmentLedger,
    PhaseLedger,
    PhaseRecord,
    selected_phase_id,
)
from chemworld.runtime.species import MechanismSpeciesView
from chemworld.world.parameters import ChemWorldParameters
from chemworld.world.phase_kernel import partition_split
from chemworld.world.separation_kernel import downstream_truth_values
from chemworld.world.species_roles import PHASE_PRODUCT_AMOUNT_KEY


def _action_float(action: dict[str, Any], key: str, default: float) -> float:
    value = action.get(key, default)
    return float(np.asarray(value).reshape(-1)[0])


def _empty_phase(volume_L: float = 0.0) -> dict[str, float]:
    return {
        "volume_L": volume_L,
        PHASE_PRODUCT_AMOUNT_KEY: 0.0,
        "impurity_mol": 0.0,
        "solvent_loss": 0.0,
    }


def _phase_type(phase_name: str) -> str:
    if phase_name in {"organic", "aqueous", "solid"}:
        return phase_name
    return "liquid"


_SELECTED_PHASE_UNSET = object()
PHASE_PROCESS_METRIC_KEYS = frozenset(
    {
        "purity",
        "recovery",
        "phase_ratio",
        "product_in_organic",
        "product_in_aqueous",
        "impurity_signal",
        "solvent_loss",
        "process_mass_balance_error",
    }
)


class ChemWorldPhaseSeparationServices:
    """Maintain phase ledgers and execute extraction-style separation steps."""

    def __init__(self, world: ChemWorldParameters, species_view: MechanismSpeciesView) -> None:
        self.world = world
        self.species_view = species_view

    def phase_ledger(self, state: WorldState) -> dict[str, dict[str, float]]:
        ledger: dict[str, dict[str, float]] = {}
        if state.phases is not None:
            for phase_name, phase in state.phases.phases.items():
                ledger[str(phase_name)] = self._phase_record_to_entry(phase)
            if ledger:
                return ledger
        if "reactor_liquid" not in ledger:
            ledger["reactor_liquid"] = {
                "volume_L": state.volume_L,
                PHASE_PRODUCT_AMOUNT_KEY: self._phase_product_amount(state),
                "impurity_mol": self._phase_impurity_amount(state),
                "solvent_loss": 0.0,
            }
        return ledger

    def phase_ledger_records(
        self,
        state: WorldState,
        phase_ledger: dict[str, dict[str, float]],
        *,
        settled: bool | None = None,
        selected_phase: str | None = None,
        preserve_selection: bool = True,
    ) -> PhaseLedger:
        species_template = dict.fromkeys(state.species_amounts, 0.0)
        phases: dict[str, PhaseRecord] = {}
        has_split_phases = bool({"organic", "aqueous"} & set(phase_ledger))

        for phase_name, values in phase_ledger.items():
            previous_phase = (
                None if state.phases is None else state.phases.phases.get(phase_name)
            )
            phase_settled = (
                bool(previous_phase.settled)
                if settled is None and previous_phase is not None
                else bool(settled)
            )
            if selected_phase is None:
                phase_selected = (
                    bool(previous_phase.selected)
                    if preserve_selection and previous_phase
                    else False
                )
            else:
                phase_selected = selected_phase == phase_name
            species_amounts = species_template.copy()
            if phase_name == "reactor_liquid":
                species_amounts.update(
                    {key: float(value) for key, value in state.species_amounts.items()}
                )
            else:
                species_amounts[self._product_species_for_phase(phase_name, state)] = float(
                    values.get(PHASE_PRODUCT_AMOUNT_KEY, 0.0)
                )
                species_amounts[self._impurity_species_for_phase(phase_name, state)] = float(
                    values.get("impurity_mol", 0.0)
                )
            phases[phase_name] = PhaseRecord(
                phase_id=phase_name,
                vessel_id=state.vessel_id,
                phase_type=_phase_type(phase_name),
                volume_L=float(values.get("volume_L", 0.0)),
                species_amounts_mol=species_amounts,
                settled=phase_settled,
                selected=phase_selected,
                metadata={"solvent_loss": float(values.get("solvent_loss", 0.0))},
            )

        if has_split_phases:
            carrier_phase = "aqueous" if "aqueous" in phases else next(iter(phases))
            carrier = phases[carrier_phase]
            species_amounts = carrier.species_amounts_mol.copy()
            split_species = self._product_candidate_species() | self._impurity_candidate_species()
            for species_id, amount in state.species_amounts.items():
                if species_id not in split_species:
                    species_amounts[species_id] = float(amount)
            phases[carrier_phase] = PhaseRecord(
                phase_id=carrier.phase_id,
                vessel_id=carrier.vessel_id,
                phase_type=carrier.phase_type,
                volume_L=carrier.volume_L,
                species_amounts_mol=species_amounts,
                settled=carrier.settled,
                selected=carrier.selected,
                metadata=carrier.metadata,
            )

        return PhaseLedger(phases)

    def _phase_record_to_entry(self, phase: PhaseRecord) -> dict[str, float]:
        product_amount = sum(
            float(phase.species_amounts_mol.get(species_id, 0.0))
            for species_id in self._product_candidate_species()
        )
        impurity_amount = sum(
            float(phase.species_amounts_mol.get(species_id, 0.0))
            for species_id in self._impurity_candidate_species()
        )
        return {
            "volume_L": float(phase.volume_L),
            PHASE_PRODUCT_AMOUNT_KEY: product_amount,
            "impurity_mol": impurity_amount,
            "solvent_loss": float(phase.metadata.get("solvent_loss", 0.0)),
        }

    def _species_with_alias(self, alias: str) -> str | None:
        mechanism = self.species_view.mechanism
        for species_id, aliases in mechanism.species_roles.items():
            if alias in aliases:
                return species_id
        return None

    @staticmethod
    def _phase_suffix_family(species_id: str) -> set[str]:
        family = {species_id}
        for suffix in ("_org", "_aq"):
            if species_id.endswith(suffix):
                base = species_id[: -len(suffix)]
                family.update({base, f"{base}_org", f"{base}_aq"})
        return family

    def _product_candidate_species(self) -> set[str]:
        candidates: set[str] = set()
        for species_id in self.species_view.target_species:
            candidates.update(self._phase_suffix_family(species_id))
        for alias in ("product_organic", "product_aqueous"):
            alias_species_id = self._species_with_alias(alias)
            if alias_species_id is not None:
                candidates.update(self._phase_suffix_family(alias_species_id))
        return candidates

    def _impurity_candidate_species(self) -> set[str]:
        candidates: set[str] = set()
        for species_id in self.species_view.impurity_species:
            candidates.update(self._phase_suffix_family(species_id))
        for species_id in self.species_view.byproduct_species:
            candidates.update(self._phase_suffix_family(species_id))
        for species_id in self.species_view.degradation_species:
            candidates.update(self._phase_suffix_family(species_id))
        for alias in ("byproduct_organic", "byproduct_aqueous", "degradation_product"):
            alias_species_id = self._species_with_alias(alias)
            if alias_species_id is not None:
                candidates.update(self._phase_suffix_family(alias_species_id))
        return candidates

    def _product_species_for_phase(self, phase_name: str, state: WorldState) -> str:
        if phase_name == "organic":
            return (
                self._species_with_alias("product_organic")
                or self.species_view.primary_target_species
            )
        if phase_name == "aqueous":
            aqueous = self._species_with_alias("product_aqueous")
            if aqueous is not None:
                return aqueous
        for species_id in sorted(self._product_candidate_species()):
            if species_id in state.species_amounts:
                return species_id
        return self.species_view.primary_target_species

    def _impurity_species_for_phase(self, phase_name: str, state: WorldState) -> str:
        if phase_name == "organic":
            organic = self._species_with_alias("byproduct_organic")
            if organic is not None:
                return organic
        if phase_name == "aqueous":
            aqueous = self._species_with_alias("byproduct_aqueous")
            if aqueous is not None:
                return aqueous
        for species_id in sorted(self._impurity_candidate_species()):
            if species_id in state.species_amounts:
                return species_id
        return self.species_view.primary_impurity_species

    def _phase_product_amount(self, state: WorldState) -> float:
        return sum(
            float(state.species_amounts.get(species_id, 0.0))
            for species_id in self._product_candidate_species()
        )

    def _phase_impurity_amount(self, state: WorldState) -> float:
        return sum(
            float(state.species_amounts.get(species_id, 0.0))
            for species_id in self._impurity_candidate_species()
        )

    def phase_metadata(
        self,
        state: WorldState,
        phase_ledger: dict[str, dict[str, float]],
        *,
        updates: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        metadata = state.metadata.copy()
        metadata.pop("phase_ledger", None)
        metadata.pop("phase_system", None)
        metadata.pop("phase_settled", None)
        metadata.pop("selected_phase", None)
        metadata.pop("stirring_speed_rpm", None)
        if updates:
            metadata.update(updates)
        return metadata

    def phase_process_metrics(
        self,
        state: WorldState,
        phase_ledger: dict[str, dict[str, float]],
    ) -> dict[str, float]:
        truth_values = downstream_truth_values(
            state,
            phase_ledger,
            product_amount_mol=self._phase_product_amount(state),
            impurity_amount_mol=self._phase_impurity_amount(state),
            target_species=self.species_view.target_species_for_state(state),
            impurity_species=self.species_view.impurity_species_for_state(state),
        )
        return {
            key: float(value)
            for key, value in truth_values.items()
            if key in PHASE_PROCESS_METRIC_KEYS
        }

    def with_phase_ledger(
        self,
        state: WorldState,
        phase_ledger: dict[str, dict[str, float]],
        *,
        metadata_updates: dict[str, Any] | None = None,
        phase_settled: bool | None = None,
        selected_phase: str | None | object = _SELECTED_PHASE_UNSET,
        ledger: Any | None = None,
        volume_L: float | None = None,
        equipment: EquipmentLedger | None = None,
    ) -> WorldState:
        metadata_updates = {} if metadata_updates is None else metadata_updates.copy()
        preserve_selection = selected_phase is _SELECTED_PHASE_UNSET
        selected_phase_value: str | None = None
        if preserve_selection:
            selected_phase_value = selected_phase_id(state.phases)
        elif selected_phase is None:
            selected_phase_value = None
        elif selected_phase is not None:
            selected_phase_value = str(selected_phase)
        metadata = self.phase_metadata(state, phase_ledger, updates=metadata_updates)
        phases = self.phase_ledger_records(
            state,
            phase_ledger,
            settled=None if phase_settled is None else bool(phase_settled),
            selected_phase=selected_phase_value,
            preserve_selection=preserve_selection,
        )
        species_amounts = phases.total_amounts_mol()
        process = process_with_metrics(
            state.process,
            **self.phase_process_metrics(state, phase_ledger),
        )
        return state.replace(
            species_amounts=species_amounts,
            phases=phases,
            volume_L=state.volume_L if volume_L is None else volume_L,
            ledger=state.ledger if ledger is None else ledger,
            metadata=metadata,
            equipment=state.equipment if equipment is None else equipment,
            process=process,
        )

    def add_phase(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        volume = float(np.clip(_action_float(action, "volume_L", 0.015), 0.0, 0.060))
        phase_name = str(action.get("phase", "aqueous"))
        if phase_name not in {"aqueous", "organic"}:
            phase_name = "organic"
        phase_ledger = self.phase_ledger(state)
        phase = phase_ledger.setdefault(phase_name, _empty_phase())
        phase["volume_L"] += volume
        ledger = state.ledger.with_updates(cost=state.ledger.cost + 0.015 + 0.35 * volume)
        return self.with_phase_ledger(
            state,
            phase_ledger,
            phase_settled=False,
            selected_phase=None,
            ledger=ledger,
            volume_L=state.volume_L + volume,
        )

    def add_extractant(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        volume = float(np.clip(_action_float(action, "volume_L", 0.018), 0.0, 0.060))
        extractant = str(action.get("extractant", "organic"))
        phase_ledger = self.phase_ledger(state)
        organic = phase_ledger.setdefault("organic", _empty_phase())
        organic["volume_L"] += volume
        reactor_settings = equipment_settings(state.equipment, "batch_reactor")
        solvent = int(reactor_settings.get("solvent", 0))
        risk = min(1.0, state.ledger.risk + 0.04 + 0.05 * float(self.world.solvent_risks[solvent]))
        ledger = state.ledger.with_updates(
            cost=state.ledger.cost + 0.025 + 0.80 * volume,
            risk=risk,
        )
        return self.with_phase_ledger(
            state,
            phase_ledger,
            metadata_updates={"extractant": extractant},
            phase_settled=False,
            selected_phase=None,
            ledger=ledger,
            volume_L=state.volume_L + volume,
        )

    def mix_phases(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        duration = float(np.clip(_action_float(action, "duration_s", 180.0), 0.0, 1800.0))
        stirring = float(np.clip(_action_float(action, "stirring_speed_rpm", 700.0), 100.0, 1200.0))
        phase_ledger = self.phase_ledger(state)
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
        organic = phase_ledger.setdefault("organic", _empty_phase(0.015))
        aqueous = phase_ledger["aqueous"]
        p_total = self._phase_product_amount(state)
        impurity_total = self._phase_impurity_amount(state)
        reactor_settings = equipment_settings(state.equipment, "batch_reactor")
        solvent = int(reactor_settings.get("solvent", 0))
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
        phase_ledger.pop("reactor_liquid", None)
        equipment = upsert_equipment_record(
            state.equipment,
            equipment_id="phase_mixer",
            equipment_type="phase_mixer",
            attached_vessel_id=state.vessel_id,
            status="configured",
            settings={"stirring_speed_rpm": stirring},
        )
        ledger = state.ledger.with_updates(
            time_s=state.ledger.time_s + duration,
            cost=state.ledger.cost + 0.01 + duration / 3600.0 * 0.015,
        )
        return self.with_phase_ledger(
            state,
            phase_ledger,
            metadata_updates={"partition_coefficient": split["partition_coefficient"]},
            phase_settled=False,
            ledger=ledger,
            equipment=equipment,
        )

    def settle_phases(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        duration = float(np.clip(_action_float(action, "duration_s", 300.0), 0.0, 3600.0))
        phase_ledger = self.phase_ledger(state)
        ledger = state.ledger.with_updates(
            time_s=state.ledger.time_s + duration,
            cost=state.ledger.cost + duration / 3600.0 * 0.006,
        )
        return self.with_phase_ledger(
            state,
            phase_ledger,
            phase_settled=duration >= 60.0,
            ledger=ledger,
        )

    def separate_phase(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        target = str(action.get("target_phase", "organic"))
        if target not in {"organic", "aqueous"}:
            target = "organic"
        phase_ledger = self.phase_ledger(state)
        selected = phase_ledger.get(
            target,
            {
                "volume_L": state.volume_L,
                PHASE_PRODUCT_AMOUNT_KEY: self._phase_product_amount(state),
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
        ledger = state.ledger.with_updates(cost=state.ledger.cost + 0.025)
        return self.with_phase_ledger(
            state,
            phase_ledger,
            phase_settled=True,
            selected_phase=target,
            ledger=ledger,
            volume_L=phase_ledger[target]["volume_L"],
        )

    def wash_phase(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        volume = float(np.clip(_action_float(action, "wash_volume_L", 0.010), 0.0, 0.040))
        phase_ledger = self.phase_ledger(state)
        target = selected_phase_id(state.phases) or "organic"
        phase = phase_ledger.setdefault(
            target,
            {
                "volume_L": state.volume_L,
                PHASE_PRODUCT_AMOUNT_KEY: self._phase_product_amount(state),
                "impurity_mol": 0.0,
                "solvent_loss": 0.0,
            },
        )
        impurity_removal = float(np.clip(0.18 + 8.0 * volume, 0.0, 0.65))
        phase["impurity_mol"] *= 1.0 - impurity_removal
        phase[PHASE_PRODUCT_AMOUNT_KEY] *= 1.0 - 0.015
        phase["volume_L"] += volume * 0.35
        phase["solvent_loss"] += 0.012
        ledger = state.ledger.with_updates(cost=state.ledger.cost + 0.02 + 0.25 * volume)
        return self.with_phase_ledger(
            state,
            phase_ledger,
            selected_phase=target,
            ledger=ledger,
            volume_L=phase["volume_L"],
        )

    def dry_phase(self, state: WorldState) -> WorldState:
        phase_ledger = self.phase_ledger(state)
        target = selected_phase_id(state.phases) or "organic"
        phase = phase_ledger.setdefault(
            target,
            {
                "volume_L": state.volume_L,
                PHASE_PRODUCT_AMOUNT_KEY: self._phase_product_amount(state),
                "impurity_mol": 0.0,
                "solvent_loss": 0.0,
            },
        )
        phase["solvent_loss"] = max(0.0, phase.get("solvent_loss", 0.0) * 0.35)
        phase["volume_L"] *= 0.92
        ledger = state.ledger.with_updates(
            time_s=state.ledger.time_s + 300.0, cost=state.ledger.cost + 0.018
        )
        return self.with_phase_ledger(
            state,
            phase_ledger,
            selected_phase=target,
            ledger=ledger,
            volume_L=phase["volume_L"],
        )

    def concentrate_phase(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        duration = float(np.clip(_action_float(action, "duration_s", 300.0), 0.0, 3600.0))
        phase_ledger = self.phase_ledger(state)
        target = selected_phase_id(state.phases) or "organic"
        phase = phase_ledger.setdefault(
            target,
            {
                "volume_L": state.volume_L,
                PHASE_PRODUCT_AMOUNT_KEY: self._phase_product_amount(state),
                "impurity_mol": 0.0,
                "solvent_loss": 0.0,
            },
        )
        concentration_factor = float(np.clip(1.0 - duration / 7200.0, 0.45, 1.0))
        phase["volume_L"] *= concentration_factor
        phase[PHASE_PRODUCT_AMOUNT_KEY] *= 1.0 - 0.01 * (1.0 - concentration_factor)
        phase["solvent_loss"] += 0.025 * (1.0 - concentration_factor)
        ledger = state.ledger.with_updates(
            time_s=state.ledger.time_s + duration,
            cost=state.ledger.cost + duration / 3600.0 * 0.035,
            risk=min(1.0, state.ledger.risk + 0.015 * (1.0 - concentration_factor)),
        )
        return self.with_phase_ledger(
            state,
            phase_ledger,
            selected_phase=target,
            ledger=ledger,
            volume_L=phase["volume_L"],
        )

    def transfer_phase(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        fraction = float(np.clip(_action_float(action, "transfer_fraction", 0.98), 0.0, 1.0))
        phase_ledger = self.phase_ledger(state)
        target = selected_phase_id(state.phases) or "organic"
        phase = phase_ledger.setdefault(
            target,
            {
                "volume_L": state.volume_L,
                PHASE_PRODUCT_AMOUNT_KEY: self._phase_product_amount(state),
                "impurity_mol": 0.0,
                "solvent_loss": 0.0,
            },
        )
        phase[PHASE_PRODUCT_AMOUNT_KEY] *= fraction
        phase["impurity_mol"] *= fraction
        phase["volume_L"] *= fraction
        phase["solvent_loss"] += 1.0 - fraction
        ledger = state.ledger.with_updates(cost=state.ledger.cost + 0.01)
        return self.with_phase_ledger(
            state,
            phase_ledger,
            selected_phase=target,
            ledger=ledger,
            volume_L=phase["volume_L"],
        )


__all__ = ["ChemWorldPhaseSeparationServices"]
