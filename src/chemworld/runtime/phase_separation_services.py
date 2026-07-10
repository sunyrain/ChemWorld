"""Phase-ledger and downstream separation helpers for ChemWorld Runtime v2."""

from __future__ import annotations

from typing import Any

import numpy as np

from chemworld.foundation import (
    WorldState,
    equipment_settings,
    upsert_equipment_record,
)
from chemworld.foundation.state import selected_phase_id
from chemworld.physchem.extraction_units import (
    DistributionCoefficientModelSpec,
    activity_corrected_extraction_train,
)
from chemworld.runtime.phase_ledger_services import (
    ChemWorldPhaseLedgerServices,
    action_float,
    empty_phase,
)
from chemworld.runtime.species import MechanismSpeciesView
from chemworld.world.parameters import ChemWorldParameters
from chemworld.world.phase_kernel import partition_split
from chemworld.world.species_roles import PHASE_PRODUCT_AMOUNT_KEY


class ChemWorldPhaseSeparationServices:
    """Maintain phase ledgers and execute extraction-style separation steps."""

    def __init__(self, world: ChemWorldParameters, species_view: MechanismSpeciesView) -> None:
        self.world = world
        self.species_view = species_view
        self.phase_ledgers = ChemWorldPhaseLedgerServices(species_view)

    def add_phase(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        volume = float(np.clip(action_float(action, "volume_L", 0.015), 0.0, 0.060))
        phase_name = str(action.get("phase", "aqueous"))
        if phase_name not in {"aqueous", "organic"}:
            phase_name = "organic"
        phase_ledger = self.phase_ledgers.phase_ledger(state)
        phase = phase_ledger.setdefault(phase_name, empty_phase())
        phase["volume_L"] += volume
        ledger = state.ledger.with_updates(cost=state.ledger.cost + 0.015 + 0.35 * volume)
        return self.phase_ledgers.with_phase_ledger(
            state,
            phase_ledger,
            phase_settled=False,
            selected_phase=None,
            ledger=ledger,
            volume_L=state.volume_L + volume,
        )

    def add_extractant(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        volume = float(np.clip(action_float(action, "volume_L", 0.018), 0.0, 0.060))
        extractant = str(action.get("extractant", "organic"))
        phase_ledger = self.phase_ledgers.phase_ledger(state)
        organic = phase_ledger.setdefault("organic", empty_phase())
        organic["volume_L"] += volume
        reactor_settings = equipment_settings(state.equipment, "batch_reactor")
        solvent = int(reactor_settings.get("solvent", 0))
        risk = min(1.0, state.ledger.risk + 0.04 + 0.05 * float(self.world.solvent_risks[solvent]))
        ledger = state.ledger.with_updates(
            cost=state.ledger.cost + 0.025 + 0.80 * volume,
            risk=risk,
        )
        return self.phase_ledgers.with_phase_ledger(
            state,
            phase_ledger,
            metadata_updates={"extractant": extractant},
            phase_settled=False,
            selected_phase=None,
            ledger=ledger,
            volume_L=state.volume_L + volume,
        )

    def mix_phases(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        duration = float(np.clip(action_float(action, "duration_s", 180.0), 0.0, 1800.0))
        stirring = float(np.clip(action_float(action, "stirring_speed_rpm", 700.0), 100.0, 1200.0))
        phase_ledger = self.phase_ledgers.phase_ledger(state)
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
        organic = phase_ledger.setdefault("organic", empty_phase(0.015))
        aqueous = phase_ledger["aqueous"]
        p_total = self.phase_ledgers.phase_product_amount(state)
        impurity_total = self.phase_ledgers.phase_impurity_amount(state)
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
        return self.phase_ledgers.with_phase_ledger(
            state,
            phase_ledger,
            metadata_updates={
                "partition_coefficient": split["partition_coefficient"],
                "impurity_partition_coefficient": split["impurity_partition_coefficient"],
                "lle_phase_status": split["lle_phase_status"],
                "lle_minimum_tpd_like": split["lle_minimum_tpd_like"],
                "lle_partition_log_spread": split["lle_partition_log_spread"],
                "extraction_model_id": split["extraction_model_id"],
                "extraction_converged": split["extraction_converged"],
                "extraction_material_balance_error_mol": split[
                    "extraction_material_balance_error_mol"
                ],
                "extraction_entrained_aqueous_volume_L": split[
                    "extraction_entrained_aqueous_volume_L"
                ],
            },
            phase_settled=False,
            ledger=ledger,
            equipment=equipment,
        )

    def settle_phases(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        duration = float(np.clip(action_float(action, "duration_s", 300.0), 0.0, 3600.0))
        phase_ledger = self.phase_ledgers.phase_ledger(state)
        ledger = state.ledger.with_updates(
            time_s=state.ledger.time_s + duration,
            cost=state.ledger.cost + duration / 3600.0 * 0.006,
        )
        return self.phase_ledgers.with_phase_ledger(
            state,
            phase_ledger,
            phase_settled=duration >= 60.0,
            ledger=ledger,
        )

    def separate_phase(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        target = str(action.get("target_phase", "organic"))
        if target not in {"organic", "aqueous"}:
            target = "organic"
        phase_ledger = self.phase_ledgers.phase_ledger(state)
        selected = phase_ledger.get(
            target,
            {
                "volume_L": state.volume_L,
                PHASE_PRODUCT_AMOUNT_KEY: self.phase_ledgers.phase_product_amount(state),
                "impurity_mol": 0.0,
                "solvent_loss": 0.0,
            },
        )
        entrained_volume_L = float(
            state.metadata.get("extraction_entrained_aqueous_volume_L", 0.0)
        )
        contact_volume_L = sum(
            max(float(values.get("volume_L", 0.0)), 0.0)
            for values in phase_ledger.values()
        )
        entrainment_fraction = float(
            np.clip(entrained_volume_L / max(contact_volume_L, 1.0e-12), 0.0, 1.0)
        )
        phase_ledger[target] = {
            "volume_L": selected["volume_L"],
            PHASE_PRODUCT_AMOUNT_KEY: selected[PHASE_PRODUCT_AMOUNT_KEY],
            "impurity_mol": selected["impurity_mol"],
            "solvent_loss": selected.get("solvent_loss", 0.0) + entrainment_fraction,
        }
        ledger = state.ledger.with_updates(cost=state.ledger.cost + 0.025)
        return self.phase_ledgers.with_phase_ledger(
            state,
            phase_ledger,
            phase_settled=True,
            selected_phase=target,
            ledger=ledger,
            volume_L=phase_ledger[target]["volume_L"],
        )

    def wash_phase(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        volume = float(np.clip(action_float(action, "wash_volume_L", 0.010), 0.0, 0.040))
        phase_ledger = self.phase_ledgers.phase_ledger(state)
        target = selected_phase_id(state.phases) or "organic"
        phase = phase_ledger.setdefault(
            target,
            {
                "volume_L": state.volume_L,
                PHASE_PRODUCT_AMOUNT_KEY: self.phase_ledgers.phase_product_amount(state),
                "impurity_mol": 0.0,
                "solvent_loss": 0.0,
            },
        )
        feed = {
            "product": max(float(phase[PHASE_PRODUCT_AMOUNT_KEY]), 0.0),
            "impurity": max(float(phase["impurity_mol"]), 0.0),
        }
        if sum(feed.values()) <= 0.0 or target != "organic":
            ledger = state.ledger.with_updates(
                cost=state.ledger.cost + 0.02 + 0.25 * volume
            )
            return self.phase_ledgers.with_phase_ledger(
                state,
                phase_ledger,
                selected_phase=target,
                ledger=ledger,
                volume_L=phase["volume_L"],
            )
        distribution_model = DistributionCoefficientModelSpec(
            model_id="runtime_wash_distribution_v1",
            component_ids=("product", "impurity"),
            intrinsic_partition_coefficients={
                "product": max(
                    float(state.metadata.get("partition_coefficient", 1.0)),
                    0.05,
                ),
                "impurity": max(
                    float(
                        state.metadata.get("impurity_partition_coefficient", 0.25)
                    ),
                    0.05,
                ),
            },
            provenance_id="chemworld-world-law-v0.2-wash-policy",
        )
        result = activity_corrected_extraction_train(
            feed,
            distribution_model=distribution_model,
            target_component="product",
            aqueous_volume_L=max(volume, 1.0e-9),
            organic_volume_L=max(float(phase["volume_L"]), 1.0e-9),
            extraction_stages=1,
            extraction_stage_efficiency=0.95,
            extraction_entrainment_fraction=0.01,
            temperature_K=state.temperature_K,
        )
        retained = result.outlet("extract")
        removed = result.outlet("raffinate")
        stage = result.stage_reports[0]
        phase[PHASE_PRODUCT_AMOUNT_KEY] = retained["product"]
        phase["impurity_mol"] = retained["impurity"]
        phase["volume_L"] += stage.entrained_aqueous_volume_L
        phase["solvent_loss"] += stage.entrained_aqueous_volume_L / max(
            volume,
            1.0e-12,
        )
        wash_waste = phase_ledger.setdefault("wash_aqueous", empty_phase())
        wash_waste[PHASE_PRODUCT_AMOUNT_KEY] += removed["product"]
        wash_waste["impurity_mol"] += removed["impurity"]
        wash_waste["volume_L"] += max(
            volume - stage.entrained_aqueous_volume_L,
            0.0,
        )
        ledger = state.ledger.with_updates(
            cost=state.ledger.cost + 0.02 + 0.25 * volume,
            risk=min(1.0, state.ledger.risk + 0.02 * result.risk),
        )
        return self.phase_ledgers.with_phase_ledger(
            state,
            phase_ledger,
            metadata_updates={
                "wash_model_id": result.model_id,
                "wash_distribution_model_id": result.distribution_model_id,
                "wash_material_balance_error_mol": result.material_balance_error_mol,
                "wash_converged": all(
                    report.converged for report in result.stage_reports
                ),
                "wash_entrained_aqueous_volume_L": (
                    result.entrained_aqueous_volume_L
                ),
            },
            selected_phase=target,
            ledger=ledger,
            volume_L=phase["volume_L"],
        )

    def dry_phase(self, state: WorldState) -> WorldState:
        phase_ledger = self.phase_ledgers.phase_ledger(state)
        target = selected_phase_id(state.phases) or "organic"
        phase = phase_ledger.setdefault(
            target,
            {
                "volume_L": state.volume_L,
                PHASE_PRODUCT_AMOUNT_KEY: self.phase_ledgers.phase_product_amount(state),
                "impurity_mol": 0.0,
                "solvent_loss": 0.0,
            },
        )
        phase["solvent_loss"] = max(0.0, phase.get("solvent_loss", 0.0) * 0.35)
        phase["volume_L"] *= 0.92
        ledger = state.ledger.with_updates(
            time_s=state.ledger.time_s + 300.0, cost=state.ledger.cost + 0.018
        )
        return self.phase_ledgers.with_phase_ledger(
            state,
            phase_ledger,
            selected_phase=target,
            ledger=ledger,
            volume_L=phase["volume_L"],
        )

    def concentrate_phase(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        duration = float(np.clip(action_float(action, "duration_s", 300.0), 0.0, 3600.0))
        phase_ledger = self.phase_ledgers.phase_ledger(state)
        target = selected_phase_id(state.phases) or "organic"
        phase = phase_ledger.setdefault(
            target,
            {
                "volume_L": state.volume_L,
                PHASE_PRODUCT_AMOUNT_KEY: self.phase_ledgers.phase_product_amount(state),
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
        return self.phase_ledgers.with_phase_ledger(
            state,
            phase_ledger,
            selected_phase=target,
            ledger=ledger,
            volume_L=phase["volume_L"],
        )

    def transfer_phase(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        fraction = float(np.clip(action_float(action, "transfer_fraction", 0.98), 0.0, 1.0))
        phase_ledger = self.phase_ledgers.phase_ledger(state)
        target = selected_phase_id(state.phases) or "organic"
        phase = phase_ledger.setdefault(
            target,
            {
                "volume_L": state.volume_L,
                PHASE_PRODUCT_AMOUNT_KEY: self.phase_ledgers.phase_product_amount(state),
                "impurity_mol": 0.0,
                "solvent_loss": 0.0,
            },
        )
        phase[PHASE_PRODUCT_AMOUNT_KEY] *= fraction
        phase["impurity_mol"] *= fraction
        phase["volume_L"] *= fraction
        phase["solvent_loss"] += 1.0 - fraction
        ledger = state.ledger.with_updates(cost=state.ledger.cost + 0.01)
        return self.phase_ledgers.with_phase_ledger(
            state,
            phase_ledger,
            selected_phase=target,
            ledger=ledger,
            volume_L=phase["volume_L"],
        )


__all__ = ["ChemWorldPhaseSeparationServices"]
