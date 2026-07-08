"""Initial-state factories for ChemWorld scenarios."""

from __future__ import annotations

from chemworld.foundation import WorldState
from chemworld.world.ontology import SPECIES
from chemworld.world.species_roles import PHASE_PRODUCT_AMOUNT_KEY


def initial_chemworld_state() -> WorldState:
    """Return the canonical empty batch-reactor state for scenario generation."""

    return WorldState(
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
            "solvent": 0,
            "catalyst": 0,
            "stirring_speed_rpm": 600.0,
            "last_observation": {},
            "phase_ledger": {
                "reactor_liquid": {
                    "volume_L": 0.0,
                    PHASE_PRODUCT_AMOUNT_KEY: 0.0,
                    "impurity_mol": 0.0,
                    "solvent_loss": 0.0,
                }
            },
        }
    )


__all__ = ["initial_chemworld_state"]
