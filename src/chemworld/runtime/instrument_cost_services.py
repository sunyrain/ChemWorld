"""Instrument cost and destructive sampling helpers for ChemWorld Runtime v2."""

from __future__ import annotations

from typing import Any

from chemworld.foundation import PhysicalConstitution, WorldState, scale_phase_ledger
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
        metadata = state.metadata.copy()
        if instrument_id == "final_assay":
            metadata["final_assay_done"] = True
            metadata["final_assay_time_s"] = state.ledger.time_s
        return state.replace(
            species_amounts=species,
            phases=scale_phase_ledger(
                state.phases,
                amount_factor=1.0 - fraction,
                volume_factor=1.0 - fraction,
            ),
            volume_L=state.volume_L - volume,
            ledger=ledger,
            metadata=metadata,
        )


__all__ = ["ChemWorldInstrumentCostServices"]
