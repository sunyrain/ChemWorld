"""Thermochemistry model cards for ChemWorld."""

from __future__ import annotations

from chemworld.physchem.maturity import MaturityLevel, ModelCard, ValidationEvidence


def thermochemistry_model_cards() -> tuple[ModelCard, ...]:
    """Return model-card metadata for the NASA7 thermochemistry slice."""

    return (
        ModelCard(
            model_id="nasa7_species_reaction_thermochemistry_v1",
            module_id="thermochemistry",
            title="NASA7 Species And Reaction Thermochemistry",
            maturity=MaturityLevel.REFERENCE_VALIDATED,
            summary=(
                "ChemWorld-local NASA7 thermochemistry slice for Cp/H/S/G "
                "species properties and reaction Delta H, Delta G, and K_eq."
            ),
            equations=(
                "Cp/R = a0 + a1 T + a2 T^2 + a3 T^3 + a4 T^4",
                "H/RT = a0 + a1 T/2 + a2 T^2/3 + a3 T^3/4 + a4 T^4/5 + a5/T",
                "S/R = a0 ln(T) + a1 T + a2 T^2/2 + a3 T^3/3 + a4 T^4/4 + a6",
                "G = H - T S",
                "Delta G_rxn = sum_i nu_i G_i; K = exp(-Delta G_rxn/RT)",
            ),
            assumptions=(
                "NASA7 coefficients represent standard-state species properties.",
                "Reaction thermochemistry is formed by stoichiometric summation.",
                "Activities and pressure corrections are outside this first slice.",
            ),
            validity_limits=(
                "Only NASA7 coefficient rows are supported.",
                "Temperature must lie inside at least one declared segment.",
                "NASA9, Shomate, group additivity, and pressure corrections are not included.",
            ),
            failure_modes=(
                "Unsupported thermo models raise ValueError.",
                "Missing species thermochemistry raises KeyError.",
                "Overlapping or invalid temperature ranges raise ValueError.",
                "Large equilibrium-constant exponents are clipped for numerical safety.",
            ),
            units={
                "temperature": "K",
                "cp": "J/mol/K",
                "enthalpy": "J/mol",
                "entropy": "J/mol/K",
                "gibbs": "J/mol",
                "equilibrium_constant": "dimensionless",
            },
            reference_reading=(
                "Cantera NasaPoly1/NasaPoly2 formulas and continuity validation.",
                "Cantera YAML NASA7 species thermo format.",
                "RMG NASA polynomial export to Cantera YAML.",
            ),
            validation_evidence=(
                ValidationEvidence(
                    evidence_id="nasa7-identity-tests",
                    evidence_type="unit-test",
                    description=(
                        "NASA7 Cp/H/S identities, Cantera-style YAML parsing, "
                        "reaction Delta G to K_eq, and continuity diagnostics."
                    ),
                    status="implemented",
                    command_or_path="tests/test_thermochemistry.py",
                    tolerance="analytical identities checked at 1e-12 to 1e-9 relative tolerances",
                ),
            ),
            model_limit_notes=(
                "This closes a thermochemistry polynomial slice, not a full "
                "Cantera/RMG thermochemistry database or group-additivity engine.",
            ),
            intended_use=(
                "Reaction-network thermochemistry sanity checks.",
                "Future reactor energy-balance and reversible-rate hardening.",
            ),
        ),
    )




__all__ = [
    "thermochemistry_model_cards",
]
