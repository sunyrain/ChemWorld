"""Instrument cost and destructive-sampling services for the transactional runtime."""

from __future__ import annotations

from typing import Any

from chemworld.foundation import (
    PhysicalConstitution,
    WorldState,
    equipment_settings,
    instrument_equipment_id,
    scale_phase_ledger,
    upsert_equipment_record,
)
from chemworld.world.operations import instrument_name


class ChemWorldInstrumentCostServices:
    """Apply measurement cost, sample consumption, and assay markers."""

    def __init__(self, constitution: PhysicalConstitution) -> None:
        self.constitution = constitution

    def apply_measurement_cost(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        instrument_id = instrument_name(action.get("instrument", "hplc"))
        instrument = self.constitution.instruments[instrument_id]
        volume = min(instrument.sample_volume_L, max(state.volume_L, 0.0))
        fraction = 0.0 if state.volume_L <= 0 else volume / state.volume_L
        species = {key: value * (1.0 - fraction) for key, value in state.species_amounts.items()}
        ledger = state.ledger.with_updates(
            cost=state.ledger.cost + instrument.cost,
            sample_consumed_L=state.ledger.sample_consumed_L + volume,
        )
        equipment_id = instrument_equipment_id(instrument_id)
        previous_settings = equipment_settings(state.equipment, equipment_id)
        use_count = int(previous_settings.get("use_count", 0)) + 1
        equipment = upsert_equipment_record(
            state.equipment,
            equipment_id=equipment_id,
            equipment_type="instrument",
            attached_vessel_id=state.vessel_id,
            status="completed" if instrument_id == "final_assay" else "used",
            settings={
                "instrument_id": instrument_id,
                "last_time_s": state.ledger.time_s,
                "last_cost": instrument.cost,
                "last_sample_consumed_L": volume,
                "use_count": use_count,
            },
        )
        return state.replace(
            species_amounts=species,
            phases=scale_phase_ledger(
                state.phases,
                amount_factor=1.0 - fraction,
                volume_factor=1.0 - fraction,
            ),
            volume_L=state.volume_L - volume,
            ledger=ledger,
            equipment=equipment,
        )


__all__ = ["ChemWorldInstrumentCostServices"]
