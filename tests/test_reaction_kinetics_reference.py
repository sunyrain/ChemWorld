from __future__ import annotations

import math

import pytest

from chemworld.physchem.reaction_network import (
    BatchSolverOptions,
    BatchTerminationEvent,
    RateLawSpec,
    ReactionNetworkSpec,
    ReactionSpec,
    SpeciesSpec,
    cantera_comparable_reaction_cases,
    evaluate_against_independent_scipy,
    evaluate_rate_law,
    finite_difference_reaction_sensitivities,
)
from chemworld.physchem.reaction_rate_contracts import audit_reaction_rate_contract


def _isomerization_network(
    *,
    rate_law: RateLawSpec | None = None,
    forward_orders: dict[str, float] | None = None,
) -> ReactionNetworkSpec:
    return ReactionNetworkSpec(
        network_id="reference_isomerization",
        species=(
            SpeciesSpec("A", "C2H4O2"),
            SpeciesSpec("P", "C2H4O2"),
        ),
        reactions=(
            ReactionSpec.from_equation(
                reaction_id="target",
                equation="A => P",
                rate_law=rate_law or RateLawSpec("target_rate", "mass_action", {"k": 0.1}),
                forward_orders=forward_orders,
            ),
        ),
    )


def test_explicit_reaction_orders_are_independent_of_stoichiometry() -> None:
    network = _isomerization_network(forward_orders={"A": 0.5})
    reaction = network.reactions[0]
    assert reaction.reactants == {"A": 1.0}
    assert reaction.kinetic_forward_orders == {"A": 0.5}

    rate = evaluate_rate_law(
        reaction,
        concentrations_mol_L={"A": 0.25, "P": 0.0},
        temperature_K=350.0,
    )
    assert rate == pytest.approx(0.05)
    contract = audit_reaction_rate_contract(
        ReactionSpec.from_equation(
            reaction_id="explicit_order",
            equation="A => P",
            rate_law=RateLawSpec("arr", "arrhenius", {"A": 0.1}),
            forward_orders={"A": 0.5},
        )
    )
    assert contract.forward_order == pytest.approx(0.5)
    assert contract.forward_rate_constant_unit == "L^-0.5 mol^0.5 s^-1"

    payload = network.to_dict()
    restored = ReactionNetworkSpec.from_dict(payload)
    assert restored.reactions[0].kinetic_forward_orders == {"A": 0.5}
    legacy_payload = _isomerization_network().to_dict()
    assert "forward_orders" not in legacy_payload["reactions"][0]
    assert "uses_activities" not in legacy_payload["reactions"][0]["rate_law"]


def test_activity_basis_is_explicit_and_uses_dimensionless_activity() -> None:
    reaction = ReactionSpec.from_equation(
        reaction_id="activity_rate",
        equation="A => P",
        rate_law=RateLawSpec(
            "activity_arrhenius",
            "arrhenius",
            {"A": 2.0},
            uses_activities=True,
            standard_concentration_mol_L=2.0,
        ),
    )
    rate = evaluate_rate_law(
        reaction,
        concentrations_mol_L={"A": 0.5, "P": 0.0},
        activity_coefficients={"A": 0.8, "P": 1.0},
        temperature_K=300.0,
    )
    assert rate == pytest.approx(0.4)
    contract = audit_reaction_rate_contract(reaction)
    assert contract.passed
    assert contract.kinetic_basis == "activity"
    assert contract.forward_rate_constant_unit == "mol L^-1 s^-1"


def test_element_and_charge_conservation_are_both_enforced() -> None:
    with pytest.raises(ValueError, match="charge balanced"):
        ReactionNetworkSpec(
            network_id="charge_violation",
            species=(
                SpeciesSpec("A_plus", "Na", charge=1),
                SpeciesSpec("A", "Na", charge=0),
            ),
            reactions=(
                ReactionSpec.from_equation(
                    reaction_id="bad_charge",
                    equation="A_plus => A",
                    rate_law=RateLawSpec("bad", "mass_action", {"k": 1.0}),
                ),
            ),
        )

    network = _isomerization_network()
    diagnostic = network.diagnose_mechanism({"P": 1.0})
    assert diagnostic.stoichiometric_rank == 1
    assert diagnostic.conservation_law_dimension == 1
    assert diagnostic.blocked_reactions == ("target",)
    assert diagnostic.unreachable_species == ("A",)
    assert not diagnostic.passed


def test_parallel_series_competition_has_non_degenerate_sensitivity() -> None:
    network = ReactionNetworkSpec(
        network_id="parallel_series_competition",
        species=tuple(SpeciesSpec(name, "C2H4O2") for name in ("A", "P", "I", "D")),
        reactions=(
            ReactionSpec.from_equation(
                reaction_id="direct_target",
                equation="A => P",
                rate_law=RateLawSpec("k1", "mass_action", {"k": 0.08}),
            ),
            ReactionSpec.from_equation(
                reaction_id="parallel_intermediate",
                equation="A => I",
                rate_law=RateLawSpec("k2", "mass_action", {"k": 0.05}),
            ),
            ReactionSpec.from_equation(
                reaction_id="series_target",
                equation="I => P",
                rate_law=RateLawSpec("k3", "mass_action", {"k": 0.03}),
            ),
            ReactionSpec.from_equation(
                reaction_id="target_degradation",
                equation="P => D",
                rate_law=RateLawSpec("k4", "mass_action", {"k": 0.01}),
            ),
        ),
    )
    report = finite_difference_reaction_sensitivities(
        network,
        {"A": 1.0},
        volume_L=1.0,
        temperature_K=350.0,
        duration_s=20.0,
        observable_species_id="P",
        perturbation_log_step=1.0e-4,
    )
    sensitivities = {
        entry.reaction_id: entry.derivative_dobservable_dln_parameter for entry in report.entries
    }
    assert sensitivities["direct_target"] > 1.0e-3
    assert sensitivities["series_target"] > 1.0e-3
    assert sensitivities["target_degradation"] < -1.0e-3
    assert len({round(abs(value), 6) for value in sensitivities.values()}) >= 3
    assert report.nondegeneracy_summary["passed"] is True
    assert report.nondegeneracy_summary["distinct_response_magnitude_count"] >= 3


def test_catalytic_activity_and_deactivation_change_target_response() -> None:
    network = ReactionNetworkSpec(
        network_id="catalyst_deactivation",
        species=(
            SpeciesSpec("A", "C2H4O2"),
            SpeciesSpec("P", "C2H4O2"),
            SpeciesSpec("Cat_active", "Pt", catalyst=True),
            SpeciesSpec("Cat_dead", "Pt", catalyst=True),
        ),
        reactions=(
            ReactionSpec.from_equation(
                reaction_id="catalysed_target",
                equation="A => P",
                rate_law=RateLawSpec(
                    "catalytic",
                    "catalytic_activity",
                    {
                        "A": 1.0,
                        "catalyst_species": "Cat_active",
                        "reference_concentration_mol_L": 0.1,
                    },
                ),
            ),
            ReactionSpec.from_equation(
                reaction_id="deactivation",
                equation="Cat_active => Cat_dead",
                rate_law=RateLawSpec(
                    "deactivation_rate",
                    "catalyst_deactivation",
                    {"A": 0.2, "species": "Cat_active"},
                ),
            ),
        ),
    )
    active = network.integrate_batch(
        {"A": 1.0, "Cat_active": 0.1},
        volume_L=1.0,
        temperature_K=350.0,
        duration_s=3.0,
    )
    low_catalyst = network.integrate_batch(
        {"A": 1.0, "Cat_active": 0.01},
        volume_L=1.0,
        temperature_K=350.0,
        duration_s=3.0,
    )
    assert active.final_amounts_mol["P"] > low_catalyst.final_amounts_mol["P"]
    assert active.final_amounts_mol["Cat_active"] < 0.1
    assert active.final_amounts_mol["Cat_dead"] > 0.0


def _stiff_robertson_network() -> ReactionNetworkSpec:
    species = tuple(SpeciesSpec(name, "H2") for name in ("A", "B", "C"))
    return ReactionNetworkSpec(
        network_id="robertson_like",
        species=species,
        reactions=(
            ReactionSpec.from_equation(
                reaction_id="slow_init",
                equation="A => B",
                rate_law=RateLawSpec("k1", "mass_action", {"k": 0.04}),
            ),
            ReactionSpec.from_equation(
                reaction_id="fast_dimer_path",
                equation="B => C",
                rate_law=RateLawSpec("k2", "mass_action", {"k": 3.0e7}),
                forward_orders={"B": 2.0},
            ),
            ReactionSpec.from_equation(
                reaction_id="fast_recycle",
                equation="B => A",
                rate_law=RateLawSpec("k3", "mass_action", {"k": 1.0e4}),
                forward_orders={"B": 1.0, "C": 1.0},
            ),
        ),
    )


def test_stiff_solver_jacobian_nonnegative_and_conservation_diagnostics() -> None:
    network = _stiff_robertson_network()
    result = network.integrate_batch(
        {"A": 1.0},
        volume_L=1.0,
        temperature_K=300.0,
        duration_s=1.0e3,
        evaluation_times_s=(0.0, 1.0, 100.0, 1.0e3),
        solver_options=BatchSolverOptions(
            method="BDF",
            rtol=1.0e-8,
            atol_mol=1.0e-12,
            use_jacobian=True,
        ),
    )
    assert result.solver_diagnostic["jacobian_used"] is True
    assert result.solver_diagnostic["nonnegative_passed"] is True
    assert result.solver_diagnostic["maximum_conservation_drift_mol"] < 1.0e-7
    assert sum(result.final_amounts_mol.values()) == pytest.approx(1.0, abs=1.0e-7)
    assert min(min(row) for row in result.amounts_mol) >= 0.0


def test_nonstiff_solver_and_terminal_event_are_auditable() -> None:
    network = _isomerization_network()
    result = network.integrate_batch(
        {"A": 1.0},
        volume_L=1.0,
        temperature_K=300.0,
        duration_s=100.0,
        solver_options=BatchSolverOptions(method="DOP853", rtol=1.0e-10),
        termination_events=(
            BatchTerminationEvent(
                event_id="target_conversion",
                species_id="A",
                threshold_mol=0.2,
                direction=-1,
            ),
        ),
    )
    assert result.solver_diagnostic["triggered_events"] == ["target_conversion"]
    assert result.times_s[-1] == pytest.approx(math.log(5.0) / 0.1, rel=2.0e-7)
    assert result.final_amounts_mol["A"] == pytest.approx(0.2, abs=2.0e-8)


def test_analytical_and_independent_scipy_boundaries_both_pass() -> None:
    results = [
        evaluate_against_independent_scipy(case, method="DOP853")
        for case in cantera_comparable_reaction_cases()
    ]
    assert all(result.passed for result in results)
    assert max(result.max_abs_error_mol for result in results) < 2.0e-8
    assert all(result.nfev > 0 for result in results)


def test_invalid_numerical_and_state_contracts_fail_before_solver() -> None:
    network = _isomerization_network()
    with pytest.raises(ValueError, match="nonnegative"):
        network.integrate_batch(
            {"A": -1.0},
            volume_L=1.0,
            temperature_K=300.0,
            duration_s=1.0,
        )
    with pytest.raises(ValueError, match="use_jacobian"):
        BatchSolverOptions(method="RK45", use_jacobian=True)
    with pytest.raises(ValueError, match="sorted"):
        network.integrate_batch(
            {"A": 1.0},
            volume_L=1.0,
            temperature_K=300.0,
            duration_s=2.0,
            evaluation_times_s=(1.0, 0.5),
        )
