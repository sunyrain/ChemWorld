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
        ModelCard(
            model_id="ideal_gamma_vle_temperature_reports",
            module_id="phase_equilibrium",
            title="Raoult-Law Bubble/Dew Temperature Reports",
            maturity=MaturityLevel.REFERENCE_VALIDATED,
            summary=(
                "Auditable mixture bubble-temperature, dew-temperature, "
                "K-value, and Rachford-Rice diagnostic reports built from "
                "component vapor-pressure reports and activity coefficients."
            ),
            equations=(
                "K_i = gamma_i P_sat,i(T) / (phi_i P)",
                "bubble point: sum_i x_i K_i = 1",
                "dew point: sum_i y_i / K_i = 1",
                "Rachford-Rice: sum_i z_i (K_i - 1) / "
                "(1 + beta (K_i - 1)) = 0",
            ),
            assumptions=(
                "Default vapor fugacity coefficients are one.",
                "Temperature solves use bracketed log-pressure residuals.",
                "Component vapor pressures come from explicit "
                "PropertyCorrelation records and pure saturation reports.",
                "Liquid nonideality is supplied by the selected "
                "ActivityModelSpec; no EOS liquid-volume correction is applied.",
            ),
            validity_limits=(
                "Requires all components to have vapor-pressure correlations "
                "with overlapping temperature validity ranges.",
                "Pressure must be inside the requested bubble/dew bracket.",
                "Validated on curated ideal ethanol/water style regression "
                "cases and Rachford-Rice closure tests.",
            ),
            failure_modes=(
                "Missing vapor-pressure correlations fail before solving.",
                "Nonpositive pressure, K-values, or vapor pressures fail.",
                "No sign change in the requested temperature bracket raises a "
                "diagnostic error rather than silently extrapolating.",
            ),
            units={
                "temperature": "K",
                "pressure": "Pa",
                "composition": "mole fraction",
                "K_value": "dimensionless",
                "Rachford-Rice beta": "dimensionless vapor fraction",
            },
            reference_reading=(
                "reference_repos/thermo/thermo/flash/flash_base.py: ideal "
                "bubble/dew/flash workflow notes",
                "reference_repos/chemicals/chemicals/rachford_rice.py: "
                "Rachford-Rice objective conventions",
            ),
            validation_evidence=(
                ValidationEvidence(
                    evidence_id="curated-ideal-binary-bubble-dew-temperature",
                    evidence_type="unit_test",
                    description=(
                        "Checks curated vapor-pressure based ideal binary "
                        "bubble/dew ordering, residual closure, and K-value "
                        "sums."
                    ),
                    status="implemented",
                    command_or_path="tests/test_phase_equilibrium.py",
                    tolerance="log-pressure residual <= 1e-8",
                ),
                ValidationEvidence(
                    evidence_id="rachford-rice-diagnostic-closure",
                    evidence_type="unit_test",
                    description=(
                        "Checks two-phase vapor fraction, single-phase "
                        "classification, and objective residual diagnostics."
                    ),
                    status="implemented",
                    command_or_path="tests/test_phase_equilibrium.py",
                    tolerance="absolute objective residual <= 1e-10",
                ),
            ),
            model_limit_notes=(
                "This is a transparent benchmark VLE diagnostic layer, not a "
                "replacement for a full EOS/GE flash package or a parameter "
                "database.",
            ),
            intended_use=(
                "Distillation, evaporation, and volatility benchmark tasks "
                "that need auditable phase-boundary diagnostics.",
                "Teaching notebooks where students inspect K-values and "
                "Rachford-Rice phase status.",
            ),
        ),
        ModelCard(
            model_id="gamma_phi_k_values_and_azeotrope_diagnostics",
            module_id="phase_equilibrium",
            title="Gamma-Phi K-Values and Binary Azeotrope Diagnostics",
            maturity=MaturityLevel.REFERENCE_VALIDATED,
            summary=(
                "Auditable gamma-phi K-value reports and binary isothermal "
                "relative-volatility crossing diagnostics for flash and "
                "distillation benchmark tasks."
            ),
            equations=(
                "K_i = gamma_i P_sat,i phi_i^l,ref Poynting_i / (phi_i^v P)",
                "relative volatility: alpha_light,heavy = K_light / K_heavy",
                "azeotrope-risk residual: r(x) = ln(alpha_light,heavy(x))",
            ),
            assumptions=(
                "Vapor fugacity coefficients, liquid reference fugacity "
                "coefficients, and Poynting factors are caller-supplied "
                "positive dimensionless mappings or default to one.",
                "The azeotrope diagnostic is an isothermal composition-grid "
                "scan of relative-volatility crossing, not a full phase "
                "stability or pressure-composition azeotrope solver.",
                "Activity coefficients come from ActivityModelSpec, so model "
                "parameter provenance remains outside the solver.",
            ),
            validity_limits=(
                "Requires finite positive pressure, vapor pressures, fugacity "
                "coefficients, and Poynting factors.",
                "The binary diagnostic requires exactly two components and a "
                "composition grid strictly inside (0, 1).",
                "Validated on formula closure, nonideal crossing, and "
                "no-crossing regression tests.",
            ),
            failure_modes=(
                "Missing or extra phi/Poynting keys fail before K-value "
                "evaluation.",
                "Nonpositive fugacity coefficients fail rather than being "
                "clipped.",
                "No relative-volatility sign change is reported as a "
                "diagnostic status with warnings, not as an exception.",
            ),
            units={
                "temperature": "K",
                "pressure": "Pa",
                "composition": "mole fraction",
                "gamma": "dimensionless",
                "phi": "dimensionless",
                "Poynting": "dimensionless",
                "K_value": "dimensionless",
                "relative_volatility": "dimensionless",
            },
            reference_reading=(
                "reference_repos/chemicals/chemicals/flash_basic.py: K_value "
                "gamma-phi equation hierarchy",
                "reference_repos/thermo/thermo/phases/phase.py: fugacity "
                "coefficient reporting conventions",
            ),
            validation_evidence=(
                ValidationEvidence(
                    evidence_id="gamma-phi-factor-closure",
                    evidence_type="unit_test",
                    description=(
                        "Checks K-values against explicit gamma, vapor phi, "
                        "liquid-reference phi, and Poynting factors."
                    ),
                    status="implemented",
                    command_or_path="tests/test_phase_equilibrium.py",
                    tolerance="pytest.approx formula closure",
                ),
                ValidationEvidence(
                    evidence_id="binary-azeotrope-crossing-diagnostic",
                    evidence_type="unit_test",
                    description=(
                        "Checks a Margules binary case with ln(alpha) crossing "
                        "and an ideal no-crossing control case."
                    ),
                    status="implemented",
                    command_or_path="tests/test_phase_equilibrium.py",
                    tolerance="bracketed residual sign change",
                ),
            ),
            model_limit_notes=(
                "The diagnostic highlights azeotrope risk for benchmark "
                "planning. It is not a rigorous gamma-phi flash, tangent-plane "
                "stability test, or azeotrope curve tracer.",
            ),
            intended_use=(
                "Distillation and flash tasks that need visible K-value "
                "provenance and relative-volatility warnings.",
                "Scenario cards that vary public/private nonideality without "
                "hiding the diagnostic contract.",
            ),
        ),
    )




__all__ = [
    "activity_model_cards",
]
