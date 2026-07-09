"""Runtime constitution factory for the default ChemWorld vessel and instruments."""

from __future__ import annotations

from chemworld.foundation import PhysicalConstitution, Vessel
from chemworld.world.instruments import chemworld_instruments
from chemworld.world.ontology import chemworld_substances


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


__all__ = ["make_chemworld_constitution"]
