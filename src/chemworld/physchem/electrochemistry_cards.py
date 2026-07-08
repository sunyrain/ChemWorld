"""Electrochemistry model cards for ChemWorld."""

from __future__ import annotations

from chemworld.physchem.maturity import MaturityLevel, ModelCard, ValidationEvidence


def electrochemistry_model_cards() -> tuple[ModelCard, ...]:
    """Return model-card metadata for the electrochemistry slice."""

    return (
        ModelCard(
            model_id="nernst_butler_volmer_faradaic_v1",
            module_id="electrochemistry",
            title="Nernst, Butler-Volmer, and Faradaic conversion kernel",
            maturity=MaturityLevel.REFERENCE_VALIDATED,
            summary=(
                "Compact electrochemical thermodynamics and charge-accounting "
                "kernel for virtual electrode-conversion tasks."
            ),
            equations=(
                "E_eq = E0 - RT/(nF) ln Q",
                "i = i0 A [exp(alpha_a nF eta/RT) - exp(-alpha_c nF eta/RT)]",
                "extent = |i| t FE / (nF)",
                "W_elec = |E_cell i t|",
            ),
            assumptions=(
                "Activities are dimensionless and supplied by the world state.",
                "No double-layer dynamics, ohmic drop, or spatial transport gradients.",
                "A finite applied current is capped by the Butler-Volmer kinetic current.",
            ),
            validity_limits=(
                "Designed for benchmark-scale virtual conversions, not battery design.",
                "Requires positive temperature and positive electron number.",
                "Extreme overpotentials are exponent-clipped for numerical stability.",
            ),
            failure_modes=(
                "Missing activity calibration can distort Nernst potentials.",
                "Mass-transfer limitation and electrolyte resistance are not yet explicit.",
                "Large time steps do not update activities continuously during electrolysis.",
            ),
            units={
                "potential": "V",
                "current": "A",
                "charge": "C",
                "extent": "mol",
                "energy": "J",
            },
            reference_reading=(
                "Cantera lithium_ion_battery.py: Butler-Volmer current and equilibrium voltage",
                "Standard electrochemical thermodynamics: DeltaG = -nFE",
            ),
            validation_evidence=(
                ValidationEvidence(
                    evidence_id="electrochemistry-identity-tests",
                    evidence_type="unit-test",
                    description=(
                        "Nernst direction, zero-current equilibrium, Butler-Volmer sign, "
                        "and Faraday charge conversion tests."
                    ),
                    status="implemented",
                    command_or_path="tests/test_electrochemistry.py",
                    tolerance="1e-9 to 1e-6 relative checks",
                ),
            ),
            model_limit_notes=(
                "This slice replaces the previous empirical electrolysis proxy but "
                "remains below a full porous-electrode or electrochemical-cell model.",
            ),
            intended_use=(
                "Electrochemical conversion benchmark tasks.",
                "Teaching and agent evaluation where charge accounting must be visible.",
            ),
        ),
    )




__all__ = [
    "electrochemistry_model_cards",
]
