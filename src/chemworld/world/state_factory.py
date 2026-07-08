"""Initial-state factories for ChemWorld scenarios."""

from __future__ import annotations

from chemworld.foundation import WorldState, upsert_equipment_record
from chemworld.world.ontology import SPECIES


def initial_chemworld_state() -> WorldState:
    """Return the canonical empty batch-reactor state for scenario generation."""

    state = WorldState(
        species_amounts=dict.fromkeys(SPECIES, 0.0),
        volume_L=0.0,
        temperature_K=298.15,
        pressure_Pa=101_325.0,
        phase="liquid",
        vessel_id="batch_reactor",
        units={
            "amount": "mol",
            "volume": "L",
            "temperature": "K",
            "pressure": "Pa",
            "time": "s",
            "cost": "currency",
            "risk": "risk",
        },
    ).replace(
        metadata={
            "initial_A_mol": 0.0,
            "last_observation": {},
        }
    )
    return state.replace(
        equipment=upsert_equipment_record(
            state.equipment,
            equipment_id="batch_reactor",
            equipment_type="batch_reactor",
            attached_vessel_id=state.vessel_id,
            status="idle",
            settings={"solvent": 0, "catalyst": 0, "stirring_speed_rpm": 600.0},
        )
    )


__all__ = ["initial_chemworld_state"]
