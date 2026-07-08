"""Reactor model cards for ChemWorld."""

from __future__ import annotations

from chemworld.physchem.maturity import MaturityLevel, ModelCard, ValidationEvidence


def reactor_model_cards() -> tuple[ModelCard, ...]:
    return (
        ModelCard(
            model_id="dynamic_batch_heat_release_jacket_sampling",
            module_id="reactors",
            title="Dynamic Batch Reactor With Heat Release And Sampling",
            maturity=MaturityLevel.REFERENCE_VALIDATED,
            summary=(
                "Event-driven dynamic batch reactor slice with material "
                "balances, thermochemistry-derived reaction heat, wall/jacket "
                "heat transfer, destructive sampling events, and auditable "
                "material/energy ledgers."
            ),
            equations=(
                "dn/dt = S r(n, T)",
                "rhoCp V dT/dt = Q_jacket - Q_loss - sum_i DeltaH_i(T) r_i V",
                "Q_jacket = UA_jacket (T_jacket(t) - T) + Q_fixed",
                "Q_loss = UA_env (T - T_env)",
                "sample event: n_j <- n_j(1 - V_sample/V), V <- V - V_sample",
            ),
            assumptions=(
                "well-mixed liquid-phase batch reactor",
                "constant density heat-capacity basis rhoCp V",
                "sampling removes a representative well-mixed fraction",
                "reaction enthalpy uses supplied NASA7 species thermochemistry when available",
            ),
            validity_limits=(
                "no pressure dynamics, vapor-liquid equilibrium, or wall thermal inertia",
                "sample events must leave positive reactor volume",
                "NASA7 reaction enthalpy requires thermochemistry for every reacting species",
            ),
            failure_modes=(
                "negative duration, volume, sample volume, or temperature raises errors",
                "missing species thermochemistry raises a KeyError when NASA7 heat is requested",
                "ODE solver failure raises RuntimeError instead of silently clipping",
            ),
            units={
                "amount": "mol",
                "volume": "L",
                "temperature": "K",
                "heat_capacity_density": "J/(L*K)",
                "heat_duty": "W",
                "energy_ledger": "J",
            },
            reference_reading=(
                (
                    "Cantera: reference_repos/cantera/src/zeroD/Reactor.cpp "
                    "separates species production, wall heat Qdot, inlet/outlet "
                    "enthalpy, and energy-equation terms."
                ),
                (
                    "Cantera: reference_repos/cantera/src/zeroD/"
                    "IdealGasReactor.cpp uses mass*cv*dT/dt as the energy "
                    "equation left-hand side for temperature-state reactors."
                ),
                (
                    "IDAES: modular property packages expose enthalpy/internal "
                    "energy flow and density terms for control-volume energy "
                    "balances."
                ),
            ),
            validation_evidence=(
                ValidationEvidence(
                    evidence_id="dynamic-batch-adiabatic-rise-test",
                    evidence_type="unit_test",
                    description=(
                        "Exothermic reaction with NASA7 enthalpy produces the "
                        "expected adiabatic temperature rise from the integrated "
                        "reaction-heat ledger."
                    ),
                    status="implemented",
                    command_or_path="tests/test_reactor_models.py",
                    tolerance="pytest.approx local tolerances",
                ),
                ValidationEvidence(
                    evidence_id="dynamic-batch-sampling-ledger-test",
                    evidence_type="unit_test",
                    description=(
                        "Destructive sampling reduces volume, records material_out, "
                        "and preserves elemental material balance."
                    ),
                    status="implemented",
                    command_or_path="tests/test_reactor_models.py",
                    tolerance="material balance error < 1e-8 mol",
                ),
            ),
            model_limit_notes=(
                (
                    "This slice closes the dynamic batch heat-release and sampling "
                    "kernel, not a full Cantera/IDAES reactor clone."
                ),
                (
                    "Pressure dynamics, gas expansion work, variable Cp mixtures, "
                    "and vapor-liquid phase change remain explicit future slices."
                ),
            ),
            intended_use=(
                "reaction calorimetry task design",
                "heat-release-aware campaign simulation",
                "safe-operation benchmark scenarios with explicit material and energy ledgers",
            ),
        ),
        ModelCard(
            model_id="cstr_exothermic_multiplicity_reference",
            module_id="reactors",
            title="Exothermic CSTR Multiple-Steady-State Reference Slice",
            maturity=MaturityLevel.REFERENCE_VALIDATED,
            summary=(
                "ChemWorld-owned steady-state CSTR reference problem for an "
                "exothermic first-order reaction. It solves the coupled "
                "steady-state material and energy balances as scalar energy "
                "roots and classifies local stability using the dynamic CSTR "
                "Jacobian."
            ),
            equations=(
                "0 = q(C_Af - C_A) - V k(T) C_A",
                "C_A(T) = C_Af / (1 + k(T) V/q)",
                "0 = (-DeltaH) V k(T) C_A(T) - rhoCp q(T - Tf) - UA(T - Tc)",
                "k(T) = A exp(-Ea/(RT))",
            ),
            assumptions=(
                "well-mixed liquid-phase CSTR",
                "constant volume and density heat capacity",
                "single irreversible A=>P first-order exothermic reaction",
                "heat removal represented by inlet sensible heat and UA coolant term",
            ),
            validity_limits=(
                "validated only for scalar first-order exothermic CSTR multiplicity",
                (
                    "no pressure dynamics, vapor phase, nonideal heat capacity, "
                    "or full plant hydraulics"
                ),
                "temperature roots must be bracketed inside the declared temperature bounds",
            ),
            failure_modes=(
                (
                    "invalid nonpositive flow, volume, heat capacity, or "
                    "Arrhenius parameters raise errors"
                ),
                "endothermic delta_h is rejected for this multiplicity case",
                "missing roots outside scan bounds are reported as absent rather than extrapolated",
            ),
            units={
                "concentration": "mol/L",
                "volumetric_flow": "L/s",
                "volume": "L",
                "temperature": "K",
                "heat_capacity_density": "J/(L*K)",
                "heat_duty": "W",
                "rate_constant": "1/s",
            },
            reference_reading=(
                (
                    "Cantera: reference_repos/cantera/doc/sphinx/userguide/"
                    "reactor-tutorial.md describes CSTR residence time and "
                    "advance_to_steady_state."
                ),
                (
                    "Cantera: reference_repos/cantera/samples/python/reactors/"
                    "continuous_reactor.py uses reservoirs, MassFlowController, "
                    "PressureController, and ReactorNet for a stirred reactor."
                ),
                (
                    "IDAES: reference_repos/idaes-pse/idaes/models/unit_models/"
                    "cstr.py builds a 0D control volume with material, energy, "
                    "and reaction extent balances."
                ),
                (
                    "IDAES: cstr_performance_eqn sets rate_reaction_extent = "
                    "volume * reaction_rate."
                ),
            ),
            validation_evidence=(
                ValidationEvidence(
                    evidence_id="cstr-multiplicity-root-test",
                    evidence_type="unit_test",
                    description=(
                        "The default case has three energy-balance roots with "
                        "stable/unstable/stable local dynamics."
                    ),
                    status="implemented",
                    command_or_path="tests/test_reactor_models.py",
                    tolerance="root residual <= 1e-6 W",
                ),
                ValidationEvidence(
                    evidence_id="cstr-performance-equation-test",
                    evidence_type="unit_test",
                    description=(
                        "At each root, the material-balance concentration and "
                        "reaction heat satisfy the CSTR performance equation."
                    ),
                    status="implemented",
                    command_or_path="tests/test_reactor_models.py",
                    tolerance="pytest.approx local tolerances",
                ),
            ),
            model_limit_notes=(
                (
                    "This is a professional reference slice for multiplicity, "
                    "not a full IDAES clone."
                ),
                (
                    "Future work should add Cantera dynamic cross-checks and "
                    "plant-scale heat-transfer variants."
                ),
            ),
            intended_use=(
                "CSTR ignition/extinction task design",
                "reactor-model maturity reporting",
                "reference case for agents reasoning about multiple steady states",
            ),
        ),
    )




__all__ = [
    "reactor_model_cards",
]
