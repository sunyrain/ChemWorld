"""Phase-ledger and downstream separation helpers for ChemWorld Runtime v2."""

from __future__ import annotations

from typing import Any

import numpy as np

from chemworld.foundation import WorldState
from chemworld.runtime.species import MechanismSpeciesView
from chemworld.world.parameters import ChemWorldParameters
from chemworld.world.phase_kernel import partition_split
from chemworld.world.separation_kernel import downstream_truth_values
from chemworld.world.species_roles import (
    LEGACY_PHASE_PRODUCT_AMOUNT_KEY,
    PHASE_PRODUCT_AMOUNT_KEY,
)


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


class ChemWorldPhaseSeparationServices:
    """Maintain phase ledgers and execute extraction-style separation steps."""

    def __init__(self, world: ChemWorldParameters, species_view: MechanismSpeciesView) -> None:
        self.world = world
        self.species_view = species_view

    def phase_ledger(self, state: WorldState) -> dict[str, dict[str, float]]:
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

    def write_phase_metadata(
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

    def add_phase(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        volume = float(np.clip(_action_float(action, "volume_L", 0.015), 0.0, 0.060))
        phase_name = str(action.get("phase", "aqueous"))
        if phase_name not in {"aqueous", "organic"}:
            phase_name = "organic"
        phase_ledger = self.phase_ledger(state)
        phase = phase_ledger.setdefault(phase_name, _empty_phase())
        phase["volume_L"] += volume
        metadata = self.write_phase_metadata(
            state,
            phase_ledger,
            updates={"phase_system": True, "phase_settled": False, "selected_phase": None},
        )
        ledger = state.ledger.with_updates(cost=state.ledger.cost + 0.015 + 0.35 * volume)
        return state.replace(volume_L=state.volume_L + volume, ledger=ledger, metadata=metadata)

    def add_extractant(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        volume = float(np.clip(_action_float(action, "volume_L", 0.018), 0.0, 0.060))
        extractant = str(action.get("extractant", "organic"))
        phase_ledger = self.phase_ledger(state)
        organic = phase_ledger.setdefault("organic", _empty_phase())
        organic["volume_L"] += volume
        metadata = self.write_phase_metadata(
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
        metadata = self.write_phase_metadata(
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

    def settle_phases(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        duration = float(np.clip(_action_float(action, "duration_s", 300.0), 0.0, 3600.0))
        phase_ledger = self.phase_ledger(state)
        metadata = self.write_phase_metadata(
            state,
            phase_ledger,
            updates={"phase_system": True, "phase_settled": duration >= 60.0},
        )
        ledger = state.ledger.with_updates(
            time_s=state.ledger.time_s + duration,
            cost=state.ledger.cost + duration / 3600.0 * 0.006,
        )
        return state.replace(ledger=ledger, metadata=metadata)

    def separate_phase(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        target = str(action.get("target_phase", "organic"))
        if target not in {"organic", "aqueous"}:
            target = "organic"
        phase_ledger = self.phase_ledger(state)
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
        metadata = self.write_phase_metadata(
            state,
            phase_ledger,
            updates={"selected_phase": target, "phase_system": True, "phase_settled": True},
        )
        ledger = state.ledger.with_updates(cost=state.ledger.cost + 0.025)
        return state.replace(
            volume_L=phase_ledger[target]["volume_L"], ledger=ledger, metadata=metadata
        )

    def wash_phase(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        volume = float(np.clip(_action_float(action, "wash_volume_L", 0.010), 0.0, 0.040))
        phase_ledger = self.phase_ledger(state)
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
        metadata = self.write_phase_metadata(
            state, phase_ledger, updates={"selected_phase": target}
        )
        ledger = state.ledger.with_updates(cost=state.ledger.cost + 0.02 + 0.25 * volume)
        return state.replace(volume_L=phase["volume_L"], ledger=ledger, metadata=metadata)

    def dry_phase(self, state: WorldState) -> WorldState:
        phase_ledger = self.phase_ledger(state)
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
        metadata = self.write_phase_metadata(
            state, phase_ledger, updates={"selected_phase": target}
        )
        ledger = state.ledger.with_updates(
            time_s=state.ledger.time_s + 300.0, cost=state.ledger.cost + 0.018
        )
        return state.replace(volume_L=phase["volume_L"], ledger=ledger, metadata=metadata)

    def concentrate_phase(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        duration = float(np.clip(_action_float(action, "duration_s", 300.0), 0.0, 3600.0))
        phase_ledger = self.phase_ledger(state)
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
        metadata = self.write_phase_metadata(
            state, phase_ledger, updates={"selected_phase": target}
        )
        ledger = state.ledger.with_updates(
            time_s=state.ledger.time_s + duration,
            cost=state.ledger.cost + duration / 3600.0 * 0.035,
            risk=min(1.0, state.ledger.risk + 0.015 * (1.0 - concentration_factor)),
        )
        return state.replace(volume_L=phase["volume_L"], ledger=ledger, metadata=metadata)

    def transfer_phase(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        fraction = float(np.clip(_action_float(action, "transfer_fraction", 0.98), 0.0, 1.0))
        phase_ledger = self.phase_ledger(state)
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
        metadata = self.write_phase_metadata(
            state, phase_ledger, updates={"selected_phase": target}
        )
        ledger = state.ledger.with_updates(cost=state.ledger.cost + 0.01)
        return state.replace(volume_L=phase["volume_L"], ledger=ledger, metadata=metadata)


__all__ = ["ChemWorldPhaseSeparationServices"]
