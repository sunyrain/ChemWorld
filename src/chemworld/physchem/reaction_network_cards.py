"""Reaction-network model cards for ChemWorld."""

from __future__ import annotations

from chemworld.physchem.maturity import MaturityLevel, ModelCard, ValidationEvidence


def reaction_kinetics_model_cards() -> tuple[ModelCard, ...]:
    return (
        ModelCard(
            model_id="reaction_ode_mass_action_arrhenius_reference_slice",
            module_id="reaction_kinetics",
            title="Mass-Action and Arrhenius Reaction-Network ODE Slice",
            maturity=MaturityLevel.REFERENCE_VALIDATED,
            summary=(
                "ChemWorld-owned balanced reaction-network ODE implementation "
                "for isothermal constant-volume batch kinetics. The validated "
                "slice covers first-order irreversible and reversible elementary "
                "mass-action cases with analytical solutions and Cantera/RMG-style "
                "Arrhenius parameterization. It also includes a compact pressure-"
                "dependent slice for third-body, Lindemann, and Troe falloff rates."
            ),
            equations=(
                "dn/dt = V * S * r(c, T)",
                "r_forward = k_f prod_i c_i^nu_i",
                "k(T) = A T^b exp(-Ea/(RT))",
                (
                    "r_net = k_f c_A - k_r c_B, "
                    "k_r = k_f / K_eq for the validated reversible case"
                ),
                (
                    "K_c(T) = exp(-Delta G_rxn^0/RT) * C0^(sum nu_i) "
                    "for the NASA7 detailed-balance slice"
                ),
                "[M]_eff = sum_i alpha_i C_i",
                "Pr = k0(T) [M]_eff / k_inf(T)",
                "k_Lindemann = k_inf Pr / (1 + Pr)",
                "k_Troe = k_Lindemann F_Troe(T, Pr, a, T1, T2, T3)",
                "S = (1/y) d y / d ln(p) for finite-difference sensitivity reports",
            ),
            assumptions=(
                "well-mixed homogeneous phase",
                "constant volume",
                "constant temperature",
                "element-balanced stoichiometric reactions",
                "activities approximated by concentrations for this validated slice",
                "falloff tests use homogeneous gas-phase collision-efficiency proxies",
            ),
            validity_limits=(
                "validated ODE reference cases are first-order A=>B and A<=>B networks",
                (
                    "falloff validation is limited to compact third-body, Lindemann, "
                    "and Troe formulas; no chemically activated bimolecular pressure "
                    "dependence or surface-coverage model is included"
                ),
                "rate coefficient units must be consistent with mol/L concentration powers",
            ),
            failure_modes=(
                "negative or nonfinite rate coefficients raise errors",
                "unbalanced mechanisms fail at ReactionNetworkSpec construction",
                (
                    "very stiff large networks may require tighter solver policy "
                    "in future professional reactor tasks"
                ),
                "negative collision efficiencies and invalid Troe parameters raise errors",
            ),
            units={
                "amount": "mol",
                "volume": "L",
                "temperature": "K",
                "time": "s",
                "rate": "mol/L/s",
            },
            reference_reading=(
                (
                    "Cantera: reference_repos/cantera/doc/sphinx/reference/"
                    "reactors/index.md covers ReactorNet ODE/DAE integration."
                ),
                (
                    "Cantera: reference_repos/cantera/doc/sphinx/yaml/"
                    "reactions.md covers equation and rate-constant contracts."
                ),
                (
                    "Cantera: reference_repos/cantera/test/python/"
                    "test_reaction.py covers ArrheniusRate formulas."
                ),
                (
                    "RMG-Py: reference_repos/rmg-py/rmgpy/kinetics/"
                    "arrhenius.pyx covers get_rate_coefficient."
                ),
                (
                    "RMG-Py: reference_repos/rmg-py/rmgpy/reaction.py "
                    "covers reverse rates from k_forward/K_eq."
                ),
                (
                    "Cantera: reference_repos/cantera/include/cantera/zeroD/"
                    "ReactorNet.h defines normalized sensitivity coefficients "
                    "S=(1/y)dy/dp for registered reaction multipliers."
                ),
                (
                    "RMG/Arkane: reference_repos/rmg-py/arkane/"
                    "sensitivity.py perturbs kinetic/energy parameters, reruns "
                    "the job, and reports finite-difference sensitivity coefficients."
                ),
            ),
            validation_evidence=(
                ValidationEvidence(
                    evidence_id="reaction-ode-analytical-cases",
                    evidence_type="unit_test",
                    description=(
                        "Irreversible and reversible first-order batch ODE "
                        "cases compare numerical integration against analytical trajectories."
                    ),
                    status="implemented",
                    command_or_path="tests/test_reaction_network.py",
                    tolerance="rtol=1e-7, atol=1e-9 mol",
                ),
                ValidationEvidence(
                    evidence_id="cantera-arrhenius-rate-optional",
                    evidence_type="optional_reference_test",
                    description=(
                        "If Cantera is importable, compare ChemWorld Arrhenius "
                        "rate constants against ct.ArrheniusRate for the same A, b, Ea."
                    ),
                    status="implemented_optional",
                    reference_backend="Cantera",
                    command_or_path="tests/reference/test_optional_reference_backends.py",
                    tolerance="rtol=1e-12",
                ),
                ValidationEvidence(
                    evidence_id="nasa7-detailed-balance-rate-test",
                    evidence_type="unit_test",
                    description=(
                        "NASA7 species Gibbs energies determine K_eq(T), reverse "
                        "rate constants, and the equilibrium ratio in a reversible "
                        "batch ODE case."
                    ),
                    status="implemented",
                    command_or_path="tests/test_reaction_network.py",
                    tolerance="equilibrium ratio checked at 5e-3 relative tolerance",
                ),
                ValidationEvidence(
                    evidence_id="pressure-dependent-falloff-rate-tests",
                    evidence_type="unit_test",
                    description=(
                        "Third-body collision efficiencies, Lindemann low/high-pressure "
                        "limits, Troe broadening, and bath-gas-sensitive batch ODE "
                        "integration are checked with deterministic compact cases."
                    ),
                    status="implemented",
                    command_or_path="tests/test_reaction_network.py",
                    tolerance="pytest.approx local tolerances for analytical limits",
                ),
                ValidationEvidence(
                    evidence_id="kinetic-finite-difference-sensitivity-test",
                    evidence_type="unit_test",
                    description=(
                        "Finite-difference sensitivity of an irreversible "
                        "first-order batch product amount matches the analytical "
                        "d ln(y) / d ln(k) expression and emits a ranked explanation report."
                    ),
                    status="implemented",
                    command_or_path="tests/test_reaction_network.py",
                    tolerance="relative local sensitivity checked at 5e-4",
                ),
            ),
            model_limit_notes=(
                (
                    "This validates the bounded reaction-ODE slice represented by "
                    "this model card; broader kinetics remain outside its scope."
                ),
                (
                    "Future tasks must add falloff, pressure dependence, and "
                    "adjoint/global sensitivity checks beyond the compact D5B slice."
                ),
            ),
            intended_use=(
                "benchmark reaction-network sanity checks",
                "mechanism-card validation",
                "pressure-dependent qualitative kinetics checks",
                "foundation for task-specific reaction optimization and reactor models",
            ),
        ),
    )




__all__ = [
    "reaction_kinetics_model_cards",
]
