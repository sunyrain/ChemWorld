"""Phase-equilibrium model cards for ChemWorld."""

from __future__ import annotations

from chemworld.physchem.maturity import MaturityLevel, ModelCard, ValidationEvidence


def activity_model_cards() -> tuple[ModelCard, ...]:
    """Return model cards for the implemented activity-coefficient models."""

    return (
        ModelCard(
            model_id="wilson_activity_coefficients",
            module_id="phase_equilibrium",
            title="Wilson Activity Coefficients",
            maturity=MaturityLevel.REFERENCE_VALIDATED,
            summary=(
                "JSON-friendly Wilson gamma model for VLE-oriented benchmark "
                "tasks with explicit asymmetric interaction parameters."
            ),
            equations=(
                "ln(gamma_i) = 1 - ln(sum_j x_j Lambda_ij) - "
                "sum_j x_j Lambda_ji / sum_k x_k Lambda_jk",
                "Lambda_ij = exp(a_ij + b_ij/T + c_ij ln(T) + "
                "d_ij T + e_ij/T**2 + f_ij T**2)",
            ),
            assumptions=(
                "Liquid mole fractions are normalized before evaluation.",
                "All off-diagonal Wilson interactions are directional and must "
                "be declared explicitly.",
                "Wilson is intended for liquid-phase VLE activity coefficients, "
                "not LLE prediction.",
            ),
            validity_limits=(
                "Requires positive finite Lambda values for all off-diagonal "
                "pairs.",
                "Temperature-dependent coefficients are accepted but only "
                "validated on fixed-lambda benchmark cases.",
            ),
            failure_modes=(
                "Missing directional interaction parameters fail during spec "
                "construction.",
                "Nonpositive Lambda values fail before gamma evaluation.",
                "Near-singular composition sums raise validation errors rather "
                "than being clipped.",
            ),
            units={
                "temperature": "K",
                "composition": "mole fraction",
                "gamma": "dimensionless",
                "lambda_a/lambda_c": "dimensionless",
                "lambda_b": "K",
                "lambda_d": "1/K",
                "lambda_e": "K^2",
                "lambda_f": "1/K^2",
            },
            reference_reading=(
                "reference_repos/thermo/thermo/wilson.py: Wilson_gammas and "
                "Wilson class",
                "reference_repos/phasepy/phasepy/actmodels/wilson.py: compact "
                "ln gamma API",
            ),
            validation_evidence=(
                ValidationEvidence(
                    evidence_id="thermo-wilson-binary-gammas",
                    evidence_type="optional_reference_test",
                    description=(
                        "Compares fixed-lambda Wilson activity coefficients "
                        "against thermo.wilson.Wilson_gammas."
                    ),
                    status="implemented",
                    reference_backend="thermo",
                    command_or_path=(
                        "tests/reference/test_optional_reference_backends.py"
                    ),
                    tolerance="rtol=1e-12",
                ),
            ),
            model_limit_notes=(
                "This card validates the gamma equations and parameter contract; "
                "it is not a complete Wilson parameter database.",
            ),
            intended_use=(
                "Reference-validated nonideal VLE benchmark slices.",
                "Solvent and volatility tasks where liquid nonideality matters.",
            ),
        ),
        ModelCard(
            model_id="nrtl_activity_coefficients",
            module_id="phase_equilibrium",
            title="NRTL Activity Coefficients",
            maturity=MaturityLevel.REFERENCE_VALIDATED,
            summary=(
                "General asymmetric NRTL gamma model for binary and "
                "multicomponent benchmark mixtures."
            ),
            equations=(
                "tau_ij = A_ij + B_ij/T + E_ij ln(T) + F_ij T + "
                "G_ij/T**2 + H_ij T**2",
                "alpha_ij = c_ij + d_ij T",
                "G_ij = exp(-alpha_ij tau_ij)",
                "ln(gamma_i) follows the standard local-composition NRTL sum "
                "over directional pair interactions.",
            ),
            assumptions=(
                "Liquid mole fractions are normalized before evaluation.",
                "Every off-diagonal tau and alpha interaction is directional "
                "and explicit.",
                "The current validation covers binary fixed-parameter cases; "
                "the implementation supports any number of components.",
            ),
            validity_limits=(
                "Requires positive alpha values for off-diagonal pairs.",
                "Temperature-dependent tau/alpha coefficients are accepted but "
                "need system-specific validation.",
            ),
            failure_modes=(
                "Missing tau or alpha parameters fail during spec construction.",
                "Nonpositive alpha values fail before gamma evaluation.",
                "Singular NRTL denominator states raise validation errors rather "
                "than being clipped.",
            ),
            units={
                "temperature": "K",
                "composition": "mole fraction",
                "gamma": "dimensionless",
                "tau_a/tau_e/alpha_c": "dimensionless",
                "tau_b": "K",
                "tau_f": "1/K",
                "tau_g": "K^2",
                "tau_h": "1/K^2",
                "alpha_d": "1/K",
            },
            reference_reading=(
                "reference_repos/thermo/thermo/nrtl.py: NRTL_gammas_binaries "
                "and NRTL class",
                "reference_repos/phasepy/phasepy/actmodels/nrtl.py: compact "
                "matrix tau/G API",
            ),
            validation_evidence=(
                ValidationEvidence(
                    evidence_id="thermo-nrtl-binary-gammas",
                    evidence_type="optional_reference_test",
                    description=(
                        "Compares fixed binary NRTL activity coefficients "
                        "against thermo.nrtl.NRTL_gammas_binaries."
                    ),
                    status="implemented",
                    reference_backend="thermo",
                    command_or_path=(
                        "tests/reference/test_optional_reference_backends.py"
                    ),
                    tolerance="rtol=1e-12",
                ),
            ),
            model_limit_notes=(
                "This card validates the NRTL equation path and parameter "
                "contract; it does not provide a public interaction-parameter "
                "database.",
            ),
            intended_use=(
                "Reference-validated nonideal VLE/LLE benchmark slices.",
                "Future solvent-selection and liquid-phase separation tasks.",
            ),
        ),
    )




__all__ = [
    "activity_model_cards",
]
