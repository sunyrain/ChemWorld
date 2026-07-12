from __future__ import annotations

import json
from pathlib import Path

import pytest

from chemworld.physchem.maturity import ModelAdapterManifest, validate_model_card
from chemworld.physchem.reaction_adapter_manifest import (
    OWNED_PATHS,
    ReactionRateContractProvider,
    reaction_rate_adapter_manifest,
    reaction_rate_provider_contract,
)
from chemworld.physchem.reaction_network_specs import RateLawSpec, ReactionSpec
from chemworld.physchem.reaction_rate_contracts import (
    CANTERA_COMMIT,
    RMG_PY_COMMIT,
    audit_reaction_rate_contract,
    concentration_equilibrium_constant_unit,
    rate_coefficient_unit,
    reaction_rate_contract_model_card,
)


def _reaction(
    equation: str,
    equation_id: str,
    parameters: dict[str, object],
) -> ReactionSpec:
    return ReactionSpec.from_equation(
        reaction_id="reference_rate",
        equation=equation,
        rate_law=RateLawSpec("reference_rate_law", equation_id, parameters),
    )


def test_rate_coefficient_units_follow_concentration_order_and_temperature_power() -> None:
    assert rate_coefficient_unit(1.0) == "s^-1"
    assert rate_coefficient_unit(2.0) == "L mol^-1 s^-1"
    assert rate_coefficient_unit(3.0) == "L^2 mol^-2 s^-1"
    assert rate_coefficient_unit(2.0, temperature_exponent=0.5) == ("L mol^-1 s^-1 K^-0.5")
    with pytest.raises(ValueError, match="overall_order"):
        rate_coefficient_unit(0.0)
    with pytest.raises(ValueError, match="temperature_exponent"):
        rate_coefficient_unit(1.0, temperature_exponent=float("nan"))
    assert concentration_equilibrium_constant_unit(0.0) == "dimensionless"
    assert concentration_equilibrium_constant_unit(-1.0) == "(mol/L)^-1"


def test_arrhenius_and_modified_arrhenius_contracts_are_explicit() -> None:
    first_order = audit_reaction_rate_contract(
        _reaction(
            "A => B",
            "arrhenius",
            {"A": 2.0, "Ea_J_per_mol": 15_000.0},
        )
    )
    assert first_order.passed
    assert first_order.forward_order == 1.0
    assert first_order.forward_rate_constant_unit == "s^-1"
    assert first_order.activation_energy_unit == "J/mol"

    modified = audit_reaction_rate_contract(
        _reaction(
            "A + B => C",
            "modified_arrhenius",
            {"A": 3.0, "b": 0.5, "Ea_J_per_mol": 8_000.0},
        )
    )
    assert modified.passed
    assert modified.forward_order == 2.0
    assert modified.forward_rate_constant_unit == "L mol^-1 s^-1 K^-0.5"


def test_reversible_contract_tracks_forward_and_reverse_orders() -> None:
    report = audit_reaction_rate_contract(
        _reaction(
            "A + B <=> C",
            "reversible_arrhenius",
            {
                "A": 4.0,
                "Ea_J_per_mol": 12_000.0,
                "A_reverse": 0.5,
                "Ea_reverse_J_per_mol": 6_000.0,
            },
        )
    )
    assert report.passed
    assert report.forward_order == 2.0
    assert report.reverse_order == 1.0
    assert report.forward_rate_constant_unit == "L mol^-1 s^-1"
    assert report.reverse_rate_constant_unit == "s^-1"
    assert report.equilibrium_constant_unit is None


def test_explicit_equilibrium_constant_requires_concentration_basis() -> None:
    missing_basis = audit_reaction_rate_contract(
        _reaction(
            "A + B <=> C",
            "reversible_arrhenius",
            {"A": 4.0, "K_eq": 2.0},
        )
    )
    assert not missing_basis.passed
    assert "K_eq_basis='concentration'" in "; ".join(missing_basis.violations)

    report = audit_reaction_rate_contract(
        _reaction(
            "A + B <=> C",
            "reversible_arrhenius",
            {
                "A": 4.0,
                "b": 0.5,
                "K_eq": 2.0,
                "K_eq_basis": "concentration",
            },
        )
    )
    assert report.passed
    assert report.equilibrium_constant_unit == "(mol/L)^-1"
    assert report.reverse_rate_constant_unit == "s^-1 K^-0.5"


def test_third_body_contract_adds_one_effective_concentration_order() -> None:
    report = audit_reaction_rate_contract(
        _reaction(
            "A => B",
            "third_body_arrhenius",
            {
                "A": 1.0,
                "Ea_J_per_mol": 2_000.0,
                "default_efficiency": 1.0,
                "third_body_efficiencies": {"bath": 2.0},
            },
        )
    )
    assert report.passed
    assert report.forward_order == 1.0
    assert report.effective_forward_order == 2.0
    assert report.forward_rate_constant_unit == "L mol^-1 s^-1"


@pytest.mark.parametrize("equation_id", ["lindemann_falloff", "troe_falloff"])
def test_falloff_contract_separates_low_and_high_pressure_units(
    equation_id: str,
) -> None:
    parameters: dict[str, object] = {
        "low_A": 2.0,
        "low_b": -1.0,
        "low_Ea_J_per_mol": 1_000.0,
        "high_A": 4.0,
        "high_b": 0.0,
        "high_Ea_J_per_mol": 2_000.0,
    }
    if equation_id == "troe_falloff":
        parameters.update({"troe_a": 0.5, "troe_T1": 1_000.0, "troe_T3": 100.0})
    report = audit_reaction_rate_contract(_reaction("A => B", equation_id, parameters))
    assert report.passed
    assert report.low_pressure_rate_constant_unit == "L mol^-1 s^-1 K"
    assert report.high_pressure_rate_constant_unit == "s^-1"
    assert report.forward_rate_constant_unit == report.high_pressure_rate_constant_unit


@pytest.mark.parametrize(
    ("equation_id", "parameters", "message"),
    [
        ("arrhenius", {"Ea_J_per_mol": 1.0}, "missing numeric rate-law parameter: A"),
        ("modified_arrhenius", {"A": 1.0}, "requires explicit b"),
        (
            "third_body_arrhenius",
            {"A": 1.0, "third_body_efficiencies": {"bath": -1.0}},
            "must be nonnegative",
        ),
        (
            "troe_falloff",
            {
                "low_A": 1.0,
                "high_A": 1.0,
                "troe_a": 1.5,
                "troe_T1": 1_000.0,
                "troe_T3": 100.0,
            },
            "troe_a must lie in [0, 1]",
        ),
    ],
)
def test_invalid_rate_contracts_return_auditable_violations(
    equation_id: str,
    parameters: dict[str, object],
    message: str,
) -> None:
    report = audit_reaction_rate_contract(_reaction("A => B", equation_id, parameters))
    assert not report.passed
    assert message in "; ".join(report.violations)


def test_provider_uses_wf00_result_contract_for_success_and_failure() -> None:
    provider = ReactionRateContractProvider()
    reaction = _reaction("A => B", "arrhenius", {"A": 1.0})
    success = provider.evaluate({"reaction": reaction})
    assert success.success
    assert success.outputs["contract"]["passed"] is True
    assert success.diagnostics["forward_order"] == 1.0

    failure = provider.evaluate({"reaction": "not-a-reaction"})
    assert not failure.success
    assert failure.failure_reason == "reaction must be a ReactionSpec"
    assert failure.outputs == {}

    invalid = provider.evaluate({"reaction": _reaction("A => B", "arrhenius", {"A": -1.0})})
    assert not invalid.success
    assert "A must be positive" in str(invalid.failure_reason)


def test_adapter_manifest_is_claim_bound_and_hash_verified() -> None:
    contract = reaction_rate_provider_contract()
    manifest = reaction_rate_adapter_manifest()
    assert manifest.provider_contract == contract
    assert manifest.owned_paths == OWNED_PATHS
    assert manifest.status == "proposal"
    payload = manifest.to_dict()
    assert ModelAdapterManifest.from_dict(payload).to_dict() == payload
    payload["owner_workstream"] = "tampered"
    with pytest.raises(ValueError, match="hash mismatch"):
        ModelAdapterManifest.from_dict(payload)


def test_model_card_limits_reference_validated_claim_to_unit_contract() -> None:
    card = reaction_rate_contract_model_card()
    assert validate_model_card(card) == []
    assert card.model_id == "chemworld_arrhenius_unit_contract_vnext"
    assert any("only" in note.lower() for note in card.model_limit_notes)
    assert any(
        evidence.evidence_id == "arrhenius-invalid-declaration-domain-tests"
        and evidence.status == "implemented"
        for evidence in card.validation_evidence
    )


def test_contract_serialization_and_provenance_are_deterministic() -> None:
    report = audit_reaction_rate_contract(
        _reaction("A => B", "arrhenius", {"A": 1.0, "Ea_J_per_mol": 0.0})
    )
    left = json.dumps(report.to_dict(), sort_keys=True)
    right = json.dumps(report.to_dict(), sort_keys=True)
    assert left == right
    assert CANTERA_COMMIT in " ".join(report.provenance)
    assert RMG_PY_COMMIT in " ".join(report.provenance)


def test_declared_reference_source_paths_exist_when_reference_repos_are_present() -> None:
    root = Path(__file__).resolve().parents[1]
    reference_root = root / "reference_repos"
    if not reference_root.is_dir():
        pytest.skip("optional reference_repos checkout is unavailable")
    cantera_header = reference_root / "cantera" / "include" / "cantera" / "kinetics" / "Arrhenius.h"
    rmg_arrhenius = reference_root / "rmg-py" / "rmgpy" / "kinetics" / "arrhenius.pyx"
    assert cantera_header.is_file()
    assert rmg_arrhenius.is_file()
