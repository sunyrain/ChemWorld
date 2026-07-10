from __future__ import annotations

import json
from math import sqrt

import numpy as np
import pytest
from scipy.optimize import least_squares

from chemworld.physchem.drying_adapter_manifest import (
    OWNED_PATHS,
    SorbentDryingProvider,
    sorbent_drying_adapter_manifest,
    sorbent_drying_provider_contract,
)
from chemworld.physchem.drying_units import (
    DRYING_MODEL_ID,
    IDAES_ADSORPTION_PATH,
    IDAES_COMMIT,
    SorbentBedSpec,
    SorbentDryingRequest,
    simulate_sorbent_drying,
    sorbent_drying_model_card,
)
from chemworld.physchem.maturity import ModelAdapterManifest, validate_model_card


def _sorbent(
    *,
    mass_kg: float = 0.5,
    capacity_mol_per_kg: float = 2.0,
    affinities: dict[str, float] | None = None,
    rate_per_s: float = 0.02,
    initial_loading: dict[str, float] | None = None,
    max_liquid_volume_L: float | None = 2.0,
) -> SorbentBedSpec:
    return SorbentBedSpec(
        sorbent_id="declared_sorbent_card",
        sorbent_mass_kg=mass_kg,
        site_capacity_mol_per_kg=capacity_mol_per_kg,
        affinity_L_per_mol=(
            {"water": 8.0, "product": 0.05}
            if affinities is None
            else affinities
        ),
        mass_transfer_rate_per_s=rate_per_s,
        initial_loading_mol_per_kg=initial_loading or {},
        max_liquid_volume_L=max_liquid_volume_L,
    )


def _request(
    *,
    wet: dict[str, float] | None = None,
    volume_L: float = 1.0,
    drying_ids: tuple[str, ...] = ("water",),
    contact_time_s: float = 300.0,
    sorbent: SorbentBedSpec | None = None,
    retained_volume_L: float = 0.0,
    product_id: str | None = "product",
    target_residual_fraction: float = 0.05,
) -> SorbentDryingRequest:
    return SorbentDryingRequest(
        wet_liquid_amounts_mol=wet or {"water": 1.0, "product": 0.5, "solvent": 8.0},
        liquid_volume_L=volume_L,
        drying_component_ids=drying_ids,
        contact_time_s=contact_time_s,
        sorbent=sorbent or _sorbent(),
        retained_liquid_volume_L=retained_volume_L,
        product_component_id=product_id,
        target_residual_drying_fraction=target_residual_fraction,
    )


def _assert_closed(result) -> None:
    assert result.material_balance_error_mol <= 1.0e-10
    assert result.volume_balance_error_L <= 1.0e-10
    assert max(result.component_balance_error_mol.values(), default=0.0) <= 1.0e-10


def test_single_component_equilibrium_matches_closed_form_quadratic() -> None:
    total_mol = 1.4
    volume_L = 1.2
    mass_kg = 0.6
    capacity = 2.5
    affinity = 3.0
    request = _request(
        wet={"water": total_mol},
        volume_L=volume_L,
        contact_time_s=1.0e6,
        product_id=None,
        sorbent=_sorbent(
            mass_kg=mass_kg,
            capacity_mol_per_kg=capacity,
            affinities={"water": affinity},
            rate_per_s=1.0,
        ),
    )
    result = simulate_sorbent_drying(request)
    a = volume_L * affinity
    b = volume_L + mass_kg * capacity * affinity - total_mol * affinity
    c = -total_mol
    concentration = (-b + sqrt(b * b - 4.0 * a * c)) / (2.0 * a)
    expected_loading = capacity * affinity * concentration / (1.0 + affinity * concentration)
    assert result.dried_liquid_amounts_mol["water"] / volume_L == pytest.approx(
        concentration,
        abs=1.0e-11,
    )
    assert result.final_sorbent_loading_mol_per_kg["water"] == pytest.approx(
        expected_loading,
        abs=1.0e-11,
    )
    _assert_closed(result)


def test_multicomponent_equilibrium_matches_independent_scipy_solve() -> None:
    wet = {"water": 1.2, "product": 0.4, "ethanol": 2.0}
    affinities = {"water": 6.0, "product": 0.08, "ethanol": 0.6}
    mass_kg = 0.7
    capacity = 2.2
    volume_L = 1.5
    result = simulate_sorbent_drying(
        _request(
            wet=wet,
            volume_L=volume_L,
            contact_time_s=1.0e6,
            sorbent=_sorbent(
                mass_kg=mass_kg,
                capacity_mol_per_kg=capacity,
                affinities=affinities,
                rate_per_s=1.0,
            ),
        )
    )
    component_ids = tuple(affinities)

    def residual(log_concentrations: np.ndarray) -> np.ndarray:
        concentrations = np.exp(log_concentrations)
        denominator = 1.0 + sum(
            affinities[key] * concentrations[index]
            for index, key in enumerate(component_ids)
        )
        return np.array(
            [
                (
                    volume_L * concentrations[index]
                    + mass_kg
                    * capacity
                    * affinities[key]
                    * concentrations[index]
                    / denominator
                    - wet[key]
                )
                / max(wet[key], 1.0e-12)
                for index, key in enumerate(component_ids)
            ]
        )

    reference = least_squares(
        residual,
        np.log([wet[key] / volume_L for key in component_ids]),
        xtol=1.0e-14,
        ftol=1.0e-14,
        gtol=1.0e-14,
    )
    assert reference.success
    concentrations = np.exp(reference.x)
    denominator = 1.0 + sum(
        affinities[key] * concentrations[index]
        for index, key in enumerate(component_ids)
    )
    for index, key in enumerate(component_ids):
        expected_loading = (
            capacity * affinities[key] * concentrations[index] / denominator
        )
        assert result.final_sorbent_loading_mol_per_kg[key] == pytest.approx(
            expected_loading,
            abs=1.0e-10,
        )
    assert result.equilibrium_residual <= 1.0e-11
    _assert_closed(result)


def test_zero_contact_preserves_loading_and_only_mechanical_retention_acts() -> None:
    result = simulate_sorbent_drying(
        _request(contact_time_s=0.0, retained_volume_L=0.1)
    )
    assert result.contact_fraction_of_equilibrium == 0.0
    assert result.net_sorption_amounts_mol == pytest.approx(
        {"water": 0.0, "product": 0.0}
    )
    assert result.dried_liquid_amounts_mol == pytest.approx(
        {"water": 0.9, "product": 0.45, "solvent": 7.2}
    )
    assert result.product_recovery == pytest.approx(0.9)
    assert any("zero effective contact" in warning for warning in result.warnings)
    _assert_closed(result)


def test_zero_capacity_is_a_bounded_no_uptake_limit() -> None:
    result = simulate_sorbent_drying(
        _request(
            sorbent=_sorbent(capacity_mol_per_kg=0.0),
            retained_volume_L=0.0,
        )
    )
    assert result.net_sorption_amounts_mol == pytest.approx(
        {"water": 0.0, "product": 0.0}
    )
    assert result.dried_liquid_amounts_mol == pytest.approx(
        {"water": 1.0, "product": 0.5, "solvent": 8.0}
    )
    assert any("zero sorbent capacity" in warning for warning in result.warnings)
    _assert_closed(result)


def test_more_contact_time_monotonically_increases_uptake_from_fresh_sorbent() -> None:
    short = simulate_sorbent_drying(_request(contact_time_s=5.0))
    medium = simulate_sorbent_drying(_request(contact_time_s=50.0))
    long = simulate_sorbent_drying(_request(contact_time_s=500.0))
    assert (
        short.net_sorption_amounts_mol["water"]
        < medium.net_sorption_amounts_mol["water"]
        < long.net_sorption_amounts_mol["water"]
    )
    assert (
        short.dried_liquid_amounts_mol["water"]
        > medium.dried_liquid_amounts_mol["water"]
        > long.dried_liquid_amounts_mol["water"]
    )
    for result in (short, medium, long):
        _assert_closed(result)


def test_competitive_selectivity_limits_product_sorption() -> None:
    result = simulate_sorbent_drying(
        _request(
            sorbent=_sorbent(
                affinities={"water": 20.0, "product": 0.01},
                rate_per_s=0.2,
            )
        )
    )
    water_fraction = result.net_sorption_amounts_mol["water"] / 1.0
    product_fraction = result.net_sorption_amounts_mol["product"] / 0.5
    assert water_fraction > 20.0 * product_fraction
    assert result.product_recovery is not None
    assert result.product_recovery > 0.99
    _assert_closed(result)


def test_shared_site_capacity_is_never_exceeded() -> None:
    capacity = 0.4
    result = simulate_sorbent_drying(
        _request(
            wet={"water": 100.0, "product": 50.0, "solvent": 1.0},
            sorbent=_sorbent(
                mass_kg=0.3,
                capacity_mol_per_kg=capacity,
                affinities={"water": 100.0, "product": 20.0},
                rate_per_s=2.0,
            ),
        )
    )
    assert sum(result.final_sorbent_loading_mol_per_kg.values()) <= capacity
    assert sum(result.final_sorbent_loading_mol_per_kg.values()) == pytest.approx(
        capacity,
        rel=1.0e-4,
    )
    assert any("95% loaded" in warning for warning in result.warnings)
    _assert_closed(result)


def test_initially_loaded_sorbent_can_desorb_without_losing_material() -> None:
    result = simulate_sorbent_drying(
        _request(
            wet={"water": 0.01, "product": 0.5, "solvent": 8.0},
            sorbent=_sorbent(
                affinities={"water": 0.1, "product": 0.001},
                rate_per_s=1.0,
                initial_loading={"water": 1.5},
            ),
        )
    )
    assert result.net_sorption_amounts_mol["water"] < 0.0
    assert result.dried_liquid_amounts_mol["water"] > 0.01
    assert any("desorbs" in warning for warning in result.warnings)
    _assert_closed(result)


def test_mechanical_retention_is_explicit_product_and_volume_loss() -> None:
    no_retention = simulate_sorbent_drying(_request(retained_volume_L=0.0))
    retained = simulate_sorbent_drying(_request(retained_volume_L=0.2))
    assert retained.product_recovery == pytest.approx(
        0.8 * no_retention.product_recovery
    )
    assert retained.dried_liquid_volume_L == pytest.approx(0.8)
    for component_id, amount in retained.retained_liquid_amounts_mol.items():
        expected_spent = (
            retained.final_sorbent_amounts_mol.get(component_id, 0.0) + amount
        )
        assert retained.spent_sorbent_inventory_mol[component_id] == pytest.approx(
            expected_spent
        )
    _assert_closed(retained)


def test_full_liquid_retention_is_explicit_and_closed() -> None:
    result = simulate_sorbent_drying(_request(retained_volume_L=1.0))
    assert result.dried_liquid_volume_L == 0.0
    assert sum(result.dried_liquid_amounts_mol.values()) == pytest.approx(0.0)
    assert result.product_recovery == 0.0
    assert any("all liquid" in warning for warning in result.warnings)
    _assert_closed(result)


def test_declared_drying_endpoint_is_evaluated_without_hiding_residual() -> None:
    result = simulate_sorbent_drying(
        _request(target_residual_fraction=0.9, contact_time_s=300.0)
    )
    assert result.endpoint_met is True
    assert result.residual_drying_component_fraction <= 0.9
    strict = simulate_sorbent_drying(
        _request(target_residual_fraction=0.01, contact_time_s=1.0)
    )
    assert strict.endpoint_met is False
    assert any("endpoint was not met" in warning for warning in strict.warnings)
    _assert_closed(result)
    _assert_closed(strict)


def test_deterministic_domain_sweep_preserves_capacity_and_closure() -> None:
    rng = np.random.default_rng(20260711)
    for _ in range(50):
        volume = float(rng.uniform(0.2, 1.8))
        capacity = float(rng.uniform(0.0, 4.0))
        initial_total = float(rng.uniform(0.0, capacity))
        water_share = float(rng.uniform(0.0, 1.0))
        initial_loading = {
            "water": initial_total * water_share,
            "product": initial_total * (1.0 - water_share),
        }
        result = simulate_sorbent_drying(
            _request(
                wet={
                    "water": float(rng.uniform(0.01, 4.0)),
                    "product": float(rng.uniform(0.01, 2.0)),
                    "solvent": float(rng.uniform(0.1, 15.0)),
                },
                volume_L=volume,
                contact_time_s=float(rng.uniform(0.0, 1000.0)),
                retained_volume_L=volume * float(rng.uniform(0.0, 1.0)),
                sorbent=_sorbent(
                    mass_kg=float(rng.uniform(0.0, 1.0)),
                    capacity_mol_per_kg=capacity,
                    affinities={
                        "water": float(10.0 ** rng.uniform(-2.0, 2.0)),
                        "product": float(10.0 ** rng.uniform(-3.0, 1.0)),
                    },
                    rate_per_s=float(rng.uniform(0.0, 0.2)),
                    initial_loading=initial_loading,
                ),
            )
        )
        assert sum(result.final_sorbent_loading_mol_per_kg.values()) <= (
            capacity + 1.0e-10
        )
        _assert_closed(result)


@pytest.mark.parametrize(
    ("factory", "message"),
    [
        (lambda: _sorbent(mass_kg=-1.0), "sorbent_mass_kg"),
        (lambda: _sorbent(affinities={}), "at least one"),
        (
            lambda: _sorbent(initial_loading={"water": 3.0}),
            "exceeds shared site capacity",
        ),
        (lambda: _request(volume_L=0.0), "liquid_volume_L"),
        (lambda: _request(drying_ids=("missing",)), "absent from wet liquid"),
        (lambda: _request(retained_volume_L=1.1), "cannot exceed"),
        (
            lambda: _request(target_residual_fraction=1.1),
            "target_residual_drying_fraction",
        ),
        (
            lambda: _request(
                volume_L=2.1,
                sorbent=_sorbent(max_liquid_volume_L=2.0),
            ),
            "contactor maximum",
        ),
    ],
)
def test_invalid_drying_domains_fail_explicitly(factory, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        factory()


def test_provider_uses_wf00_contract_for_success_and_failure() -> None:
    provider = SorbentDryingProvider()
    success = provider.evaluate({"request": _request()})
    assert success.success is True
    assert success.outputs["drying_result"]["model_id"] == DRYING_MODEL_ID
    assert success.diagnostics["material_balance_error_mol"] <= 1.0e-10
    assert success.diagnostics["residual_drying_component_fraction"] < 1.0
    assert success.diagnostics["endpoint_met"] in {True, False}

    failure = provider.evaluate({"request": {}})
    assert failure.success is False
    assert failure.failure_reason == "request must be a SorbentDryingRequest"
    assert failure.outputs == {}


def test_model_card_and_adapter_are_bounded_hash_verified_evidence() -> None:
    card = sorbent_drying_model_card()
    assert validate_model_card(card) == []
    assert card.model_id == DRYING_MODEL_ID
    assert any(IDAES_COMMIT in reference for reference in card.reference_reading)
    assert any(IDAES_ADSORPTION_PATH in reference for reference in card.reference_reading)
    assert any("not sorbent selection" in note for note in card.model_limit_notes)

    contract = sorbent_drying_provider_contract()
    manifest = sorbent_drying_adapter_manifest()
    assert manifest.provider_contract == contract
    assert manifest.owned_paths == OWNED_PATHS
    assert manifest.replaces_model_ids == ()
    payload = manifest.to_dict()
    assert ModelAdapterManifest.from_dict(payload).to_dict() == payload
    payload["adapter_version"] = "tampered"
    with pytest.raises(ValueError, match="hash mismatch"):
        ModelAdapterManifest.from_dict(payload)


def test_drying_result_serialization_is_deterministic() -> None:
    request = _request(retained_volume_L=0.05)
    left = json.dumps(simulate_sorbent_drying(request).to_dict(), sort_keys=True)
    right = json.dumps(simulate_sorbent_drying(request).to_dict(), sort_keys=True)
    assert left == right
