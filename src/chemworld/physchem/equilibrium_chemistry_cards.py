"""Equilibrium-chemistry model cards for ChemWorld."""

from __future__ import annotations

from chemworld.physchem.maturity import MaturityLevel, ModelCard, ValidationEvidence


def equilibrium_chemistry_model_cards() -> tuple[ModelCard, ...]:
    """Return model cards for equilibrium-chemistry kernels."""

    return (
        ModelCard(
            model_id="fixed_tp_ideal_gibbs_minimization",
            module_id="equilibrium_chemistry",
            title="Fixed-TP Ideal Gibbs Minimization",
            maturity=MaturityLevel.REFERENCE_VALIDATED,
            summary=(
                "Small constrained Gibbs minimization slice for benchmark "
                "species sets with element, charge, phase, and nonnegativity constraints."
            ),
            equations=(
                "min_n G = sum_i n_i G_i^0 + R T sum_i n_i ln(x_i_phase)",
                "element constraints: A_element n = b_element",
                "charge constraint: z^T n = q_target",
                "phase restrictions: n_i = 0 for species in disallowed phases",
                "bounds: n_i >= 0",
            ),
            assumptions=(
                "Fixed temperature and pressure.",
                "Ideal mixing within each non-solid phase.",
                "Pure condensed solid activities are treated as one.",
                "Species standard Gibbs energies are supplied by the caller.",
            ),
            validity_limits=(
                "Small benchmark systems with explicit species and phases.",
                "No thermodynamic database, activity-coefficient model, or phase stability search.",
                "No automatic species generation or redox/electron basis selection.",
            ),
            failure_modes=(
                "Unknown initial species, nonphysical amounts, duplicate species ids, "
                "or nonpositive T/P raise ValueError.",
                "Phase restrictions with nonzero disallowed initial species raise ValueError.",
                "If allowed species cannot carry a target element, the solver raises ValueError.",
                "Numerical nonconvergence is reported in the result metadata rather than hidden.",
            ),
            units={
                "amount": "mol",
                "standard_gibbs": "J/mol",
                "total_gibbs": "J",
                "temperature": "K",
                "pressure": "Pa",
                "charge": "mol charge equivalents",
            },
            reference_reading=(
                "reference_repos/reaktoro/Reaktoro/Equilibrium/EquilibriumSpecs.hpp",
                "reference_repos/reaktoro/Reaktoro/Equilibrium/SmartEquilibriumSolver.hpp",
                "reference_repos/cantera/doc/sphinx/userguide/python-tutorial.md "
                "chemical equilibrium section",
                "reference_repos/pycalphad/pycalphad/core/equilibrium.py",
            ),
            validation_evidence=(
                ValidationEvidence(
                    evidence_id="analytical-ideal-isomerization",
                    evidence_type="unit_tests",
                    description=(
                        "For A and B with identical element vectors, ideal Gibbs "
                        "minimization reproduces n_B/n_A = exp[-(G_B^0-G_A^0)/RT]."
                    ),
                    status="passing",
                    command_or_path="python -m pytest tests/test_equilibrium_chemistry.py",
                    tolerance="rel=1e-7",
                ),
            ),
            model_limit_notes=(
                "This is a ChemWorld-local professional slice, not a Reaktoro clone.",
                "Database-backed aqueous speciation and CALPHAD phase selection "
                "remain future work.",
            ),
            intended_use=(
                "Small hidden equilibrium scenarios for local world-model learning.",
                "Auditable element/charge/phase-constrained equilibrium tasks.",
            ),
        ),
    )




__all__ = [
    "equilibrium_chemistry_model_cards",
]
