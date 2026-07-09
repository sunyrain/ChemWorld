"""Chemical ontology registry for the shared ChemWorld law."""

from __future__ import annotations

from chemworld.foundation import StateVariable, Substance

SPECIES = ("A", "P", "B", "D", "E", "Cat_active", "Cat_dead")


def chemworld_substances() -> dict[str, Substance]:
    """Return the substance registry used by the shared physical-chemical law."""

    return {
        "A": Substance("A", "reactant A", {"C": 1}),
        "P": Substance("P", "target product P", {"C": 1}),
        "B": Substance("B", "byproduct B", {"C": 1}),
        "D": Substance("D", "degradation product D", {"C": 1}),
        "E": Substance("E", "coupled impurity E", {"C": 2}),
        "Cat_active": Substance("Cat_active", "active catalyst", {"Cat": 1}, role="catalyst"),
        "Cat_dead": Substance("Cat_dead", "deactivated catalyst", {"Cat": 1}, role="catalyst"),
    }


def chemworld_state_variables() -> tuple[StateVariable, ...]:
    """Return public and hidden state-variable contracts for ChemWorld."""

    return (
        StateVariable("species_amounts", "mol", hidden=True),
        StateVariable("volume_L", "L", hidden=True),
        StateVariable("temperature_K", "K", hidden=True),
        StateVariable("pressure_Pa", "Pa", hidden=True),
        StateVariable("metadata.stirring_speed_rpm", "rpm", hidden=True),
        StateVariable("ledger.cost", "currency", hidden=False),
        StateVariable("ledger.risk", "risk", hidden=False),
        StateVariable("ledger.time_s", "s", hidden=False),
        StateVariable("metadata.phase_ledger", "dimensionless", hidden=True),
        StateVariable("metadata.purity", "dimensionless", hidden=True),
        StateVariable("metadata.recovery", "dimensionless", hidden=True),
        StateVariable("metadata.process_mass_balance_error", "dimensionless", hidden=True),
        StateVariable("metadata.crystal_yield", "dimensionless", hidden=True),
        StateVariable("metadata.distillate_purity", "dimensionless", hidden=True),
        StateVariable("process.metrics.flow_conversion", "dimensionless", hidden=True),
        StateVariable(
            "process.metrics.electrochemical_selectivity",
            "dimensionless",
            hidden=True,
        ),
        StateVariable("process.metrics.energy_efficiency", "dimensionless", hidden=True),
    )


__all__ = ["SPECIES", "chemworld_state_variables", "chemworld_substances"]
