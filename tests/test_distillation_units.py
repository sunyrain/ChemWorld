from __future__ import annotations

import json

import numpy as np
import pytest

from chemworld.physchem.distillation_adapter_manifest import (
    INTEGRATION_OPERATIONS,
    OWNED_PATHS,
    REPLACED_MODEL_IDS,
    DutyLimitedDistillationProvider,
    duty_limited_distillation_adapter_manifest,
    duty_limited_distillation_provider_contract,
)
from chemworld.physchem.distillation_units import (
    DISTILLATION_ENGINE_MODEL_ID,
    DUTY_LIMITED_DISTILLATION_MODEL_ID,
    IDAES_COMMIT,
    IDAES_CONDENSER_PATH,
    IDAES_REBOILER_PATH,
    IDAES_TRAY_COLUMN_PATH,
    DistillationComponentSpec,
    DutyLimitedDistillationRequest,
    ShortcutColumnSpec,
    duty_limited_distillation_model_card,
    simulate_duty_limited_distillation,
)
from chemworld.physchem.maturity import ModelAdapterManifest, validate_model_card
from chemworld.physchem.separations import vle_shortcut_distillation


def _component(
    component_id: str,
    *,
    vapor_pressure_Pa: float,
    latent_heat_J_mol: float,
    heat_capacity_J_mol_K: float = 100.0,
    evaluation_temperature_K: float = 360.0,
    thermal_limit_K: float = 450.0,
) -> DistillationComponentSpec:
    return DistillationComponentSpec(
        component_id=component_id,
        vapor_pressure_Pa=vapor_pressure_Pa,
        latent_heat_J_mol=latent_heat_J_mol,
        liquid_heat_capacity_J_mol_K=heat_capacity_J_mol_K,
        evaluation_temperature_K=evaluation_temperature_K,
        thermal_limit_K=thermal_limit_K,
        provenance_id=f"wf60-{component_id}-property-profile-v1",
    )


def _specs(
    *,
    light_vapor_pressure_Pa: float = 220_000.0,
    heavy_vapor_pressure_Pa: float = 50_000.0,
    evaluation_temperature_K: float = 360.0,
) -> dict[str, DistillationComponentSpec]:
    return {
        "light": _component(
            "light",
            vapor_pressure_Pa=light_vapor_pressure_Pa,
            latent_heat_J_mol=30_000.0,
            evaluation_temperature_K=evaluation_temperature_K,
        ),
        "heavy": _component(
            "heavy",
            vapor_pressure_Pa=heavy_vapor_pressure_Pa,
            latent_heat_J_mol=42_000.0,
            evaluation_temperature_K=evaluation_temperature_K,
        ),
    }


def _column(**overrides: object) -> ShortcutColumnSpec:
    values: dict[str, object] = {
        "theoretical_stages": 10.0,
        "stage_efficiency": 0.70,
        "maximum_reboiler_power_W": 1_000_000.0,
        "maximum_condenser_power_W": 1_000_000.0,
        "maximum_internal_vapor_rate_mol_s": 10.0,
        "maximum_batch_amount_mol": 100.0,
        "minimum_bottoms_amount_mol": 0.0,
        "maximum_distillate_cut_fraction": 0.95,
        "minimum_pressure_Pa": 10_000.0,
        "maximum_pressure_Pa": 200_000.0,
        "maximum_temperature_K": 450.0,
        "maximum_duration_s": 10_000.0,
        "maximum_reflux_ratio": 10.0,
        "provenance_id": "wf60-bench-shortcut-column-v1",
    }
    values.update(overrides)
    return ShortcutColumnSpec(**values)  # type: ignore[arg-type]


def _request(
    *,
    feed: dict[str, float] | None = None,
    specs: dict[str, DistillationComponentSpec] | None = None,
    column: ShortcutColumnSpec | None = None,
    pressure_Pa: float = 100_000.0,
    initial_temperature_K: float = 360.0,
    operating_temperature_K: float = 360.0,
    duration_s: float = 1_000.0,
    reflux_ratio: float = 2.0,
    cut: float = 0.40,
    light_key: str = "light",
    heavy_key: str = "heavy",
) -> DutyLimitedDistillationRequest:
    return DutyLimitedDistillationRequest(
        feed_amounts_mol=feed or {"light": 1.0, "heavy": 1.0},
        component_specs=specs or _specs(evaluation_temperature_K=operating_temperature_K),
        light_key=light_key,
        heavy_key=heavy_key,
        pressure_Pa=pressure_Pa,
        initial_temperature_K=initial_temperature_K,
        operating_temperature_K=operating_temperature_K,
        duration_s=duration_s,
        reflux_ratio=reflux_ratio,
        requested_distillate_cut_fraction=cut,
        column=column or _column(),
    )


def _assert_closed(result) -> None:
    assert result.material_balance_error_mol <= 1.0e-9
    assert result.energy_balance_error_J <= 1.0e-8
    for component_id, feed_amount in result.feed_amounts_mol.items():
        recovered = sum(outlet[component_id] for outlet in result.outlets.values())
        assert recovered == pytest.approx(feed_amount, abs=1.0e-9)
    assert result.total_reboiler_duty_J == pytest.approx(
        result.sensible_heat_J + result.latent_reboiler_duty_J
    )
    assert result.condenser_duty_J == pytest.approx(result.latent_reboiler_duty_J)


def test_unconstrained_limit_matches_existing_vle_fenske_engine() -> None:
    request = _request()
    result = simulate_duty_limited_distillation(request)
    reference = vle_shortcut_distillation(
        request.feed_amounts_mol,
        vapor_pressures_Pa={
            key: value.vapor_pressure_Pa for key, value in request.component_specs.items()
        },
        pressure_Pa=request.pressure_Pa,
        temperature_K=request.operating_temperature_K,
        light_key=request.light_key,
        heavy_key=request.heavy_key,
        distillate_cut_fraction=request.requested_distillate_cut_fraction,
        theoretical_stages=request.column.theoretical_stages,
        reflux_ratio=request.reflux_ratio,
        stage_efficiency=request.column.stage_efficiency,
        latent_heats_J_mol={
            key: value.latent_heat_J_mol for key, value in request.component_specs.items()
        },
        vapor_fugacity_coefficients={"light": 1.0, "heavy": 1.0},
    )

    assert result.model_id == DUTY_LIMITED_DISTILLATION_MODEL_ID
    assert result.engine_model_id == DISTILLATION_ENGINE_MODEL_ID
    assert result.actual_distillate_cut_fraction == pytest.approx(0.40)
    assert result.limiting_constraint == "requested_cut"
    assert result.cut_endpoint_met is True
    for outlet_id in reference.outlets:
        assert result.outlets[outlet_id] == pytest.approx(reference.outlets[outlet_id])
    assert result.latent_reboiler_duty_J == pytest.approx(reference.ledger.heat_duty_J)
    assert result.light_key_distillate_purity > 0.5
    assert result.heavy_key_bottoms_purity > 0.5
    _assert_closed(result)


def test_binary_fenske_and_underwood_diagnostics_are_explicit() -> None:
    result = simulate_duty_limited_distillation(_request())

    assert result.fug_available is True
    assert result.observed_fenske_stage_count == pytest.approx(result.effective_stages)
    assert result.fenske_stage_residual == pytest.approx(0.0, abs=1.0e-12)
    assert result.fenske_minimum_stages == pytest.approx(result.effective_stages)
    assert result.underwood_theta is not None
    assert 1.0 < result.underwood_theta < result.relative_volatilities["light"]
    assert result.minimum_reflux_ratio is not None
    assert result.minimum_reflux_ratio > 0.0
    assert result.gilliland_x is not None
    assert 0.0 < result.gilliland_x < 1.0
    assert result.gilliland_y is not None
    assert 0.0 <= result.gilliland_y < 1.0
    assert result.required_theoretical_stages is not None
    assert result.required_theoretical_stages > result.fenske_minimum_stages
    assert result.installed_equilibrium_stage_margin is not None


def test_reboiler_power_reduces_cut_and_identifies_constraint() -> None:
    result = simulate_duty_limited_distillation(
        _request(column=_column(maximum_reboiler_power_W=10.0))
    )

    assert 0.0 < result.actual_distillate_cut_fraction < 0.40
    assert result.limiting_constraint == "reboiler_duty"
    assert result.cut_endpoint_met is False
    assert result.average_reboiler_power_W <= 10.0 + 1.0e-8
    assert result.average_reboiler_power_W > 9.9
    assert any("reboiler_duty" in warning for warning in result.warnings)
    _assert_closed(result)


def test_condenser_power_reduces_cut_independently() -> None:
    result = simulate_duty_limited_distillation(
        _request(column=_column(maximum_condenser_power_W=8.0))
    )

    assert 0.0 < result.actual_distillate_cut_fraction < 0.40
    assert result.limiting_constraint == "condenser_duty"
    assert result.average_condenser_power_W <= 8.0 + 1.0e-8
    assert result.average_condenser_power_W > 7.9
    _assert_closed(result)


def test_internal_vapor_rate_reduces_cut_independently() -> None:
    result = simulate_duty_limited_distillation(
        _request(column=_column(maximum_internal_vapor_rate_mol_s=1.0e-4))
    )

    assert 0.0 < result.actual_distillate_cut_fraction < 0.40
    assert result.limiting_constraint == "internal_vapor_rate"
    assert result.internal_vapor_rate_mol_s <= 1.0e-4 + 1.0e-12
    assert result.internal_vapor_rate_mol_s > 0.99e-4
    _assert_closed(result)


def test_sensible_heating_shortfall_returns_partial_temperature_and_no_cut() -> None:
    result = simulate_duty_limited_distillation(
        _request(
            initial_temperature_K=300.0,
            operating_temperature_K=360.0,
            duration_s=100.0,
            column=_column(maximum_reboiler_power_W=5.0),
        )
    )

    assert result.limiting_constraint == "insufficient_sensible_heat"
    assert result.actual_distillate_cut_fraction == 0.0
    assert result.final_temperature_K == pytest.approx(302.5)
    assert result.sensible_heat_J == pytest.approx(500.0)
    assert result.latent_reboiler_duty_J == 0.0
    assert result.outlets["bottoms"] == result.feed_amounts_mol
    _assert_closed(result)


def test_below_bubble_operation_returns_explicit_no_cut() -> None:
    result = simulate_duty_limited_distillation(
        _request(
            specs=_specs(
                light_vapor_pressure_Pa=80_000.0,
                heavy_vapor_pressure_Pa=20_000.0,
            )
        )
    )

    assert result.bubble_pressure_Pa == pytest.approx(50_000.0)
    assert result.bubble_pressure_margin_Pa == pytest.approx(-50_000.0)
    assert result.limiting_constraint == "below_bubble_point"
    assert result.actual_distillate_cut_fraction == 0.0
    assert result.cut_endpoint_met is False
    _assert_closed(result)


@pytest.mark.parametrize(
    ("column", "expected_cut", "constraint"),
    [
        (_column(maximum_distillate_cut_fraction=0.20), 0.20, "column_cut_limit"),
        (_column(minimum_bottoms_amount_mol=1.50), 0.25, "minimum_bottoms_amount"),
    ],
)
def test_column_cut_and_residual_bottoms_limits_are_enforced(
    column: ShortcutColumnSpec,
    expected_cut: float,
    constraint: str,
) -> None:
    result = simulate_duty_limited_distillation(_request(column=column))
    assert result.actual_distillate_cut_fraction == pytest.approx(expected_cut)
    assert result.limiting_constraint == constraint
    _assert_closed(result)


def test_higher_reflux_improves_purity_and_raises_internal_duty() -> None:
    low = simulate_duty_limited_distillation(_request(reflux_ratio=0.25))
    high = simulate_duty_limited_distillation(_request(reflux_ratio=4.0))

    assert high.actual_distillate_cut_fraction == pytest.approx(low.actual_distillate_cut_fraction)
    assert high.light_key_distillate_purity > low.light_key_distillate_purity
    assert high.heavy_key_bottoms_purity > low.heavy_key_bottoms_purity
    assert high.internal_vapor_mol > low.internal_vapor_mol
    assert high.total_reboiler_duty_J > low.total_reboiler_duty_J
    _assert_closed(low)
    _assert_closed(high)


def test_requested_cut_response_is_monotonic_in_unconstrained_domain() -> None:
    results = [simulate_duty_limited_distillation(_request(cut=cut)) for cut in (0.10, 0.30, 0.60)]
    assert [result.actual_distillate_cut_fraction for result in results] == pytest.approx(
        [0.10, 0.30, 0.60]
    )
    assert results[0].light_key_recovery < results[1].light_key_recovery
    assert results[1].light_key_recovery < results[2].light_key_recovery
    assert results[0].latent_reboiler_duty_J < results[1].latent_reboiler_duty_J
    assert results[1].latent_reboiler_duty_J < results[2].latent_reboiler_duty_J


def test_multicomponent_cut_closes_but_binary_fug_is_withheld() -> None:
    feed = {"light": 0.8, "middle": 1.0, "heavy": 0.7}
    specs = {
        "light": _component("light", vapor_pressure_Pa=250_000.0, latent_heat_J_mol=28_000.0),
        "middle": _component("middle", vapor_pressure_Pa=110_000.0, latent_heat_J_mol=35_000.0),
        "heavy": _component("heavy", vapor_pressure_Pa=45_000.0, latent_heat_J_mol=44_000.0),
    }
    result = simulate_duty_limited_distillation(_request(feed=feed, specs=specs, cut=0.50))

    assert result.fug_available is False
    assert result.fenske_minimum_stages is None
    assert any("multicomponent" in warning for warning in result.warnings)
    assert result.outlets["distillate"]["light"] > result.outlets["distillate"]["heavy"]
    _assert_closed(result)


def test_near_thermal_limit_is_visible_without_degradation_claim() -> None:
    specs = {
        key: _component(
            key,
            vapor_pressure_Pa=value.vapor_pressure_Pa,
            latent_heat_J_mol=value.latent_heat_J_mol,
            evaluation_temperature_K=360.0,
            thermal_limit_K=364.0,
        )
        for key, value in _specs().items()
    }
    result = simulate_duty_limited_distillation(_request(specs=specs))
    assert result.minimum_thermal_margin_K == pytest.approx(4.0)
    assert any("within 5 K" in warning for warning in result.warnings)


@pytest.mark.parametrize(
    ("factory", "message"),
    [
        (
            lambda: _component(
                "bad",
                vapor_pressure_Pa=-1.0,
                latent_heat_J_mol=30_000.0,
            ),
            "vapor_pressure_Pa",
        ),
        (
            lambda: _column(stage_efficiency=0.0),
            "must be positive",
        ),
        (
            lambda: _column(minimum_pressure_Pa=200_000.0, maximum_pressure_Pa=100_000.0),
            "cannot exceed",
        ),
        (
            lambda: _request(specs={"light": _specs()["light"]}),
            "exactly match",
        ),
        (
            lambda: _request(specs=_specs(evaluation_temperature_K=350.0)),
            "evaluated at operating_temperature_K",
        ),
        (
            lambda: _request(pressure_Pa=5_000.0),
            "pressure domain",
        ),
        (
            lambda: _request(operating_temperature_K=460.0),
            "column maximum",
        ),
        (
            lambda: _request(duration_s=20_000.0),
            "duration_s exceeds",
        ),
        (
            lambda: _request(reflux_ratio=20.0),
            "reflux_ratio exceeds",
        ),
        (
            lambda: _request(feed={"light": 60.0, "heavy": 60.0}),
            "maximum_batch_amount_mol",
        ),
        (
            lambda: _request(cut=1.2),
            "requested_distillate_cut_fraction",
        ),
    ],
)
def test_invalid_distillation_domains_fail_explicitly(factory, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        factory()


def test_key_order_contradicting_vle_fails_instead_of_swapping_labels() -> None:
    request = _request(light_key="heavy", heavy_key="light")
    with pytest.raises(ValueError, match="more volatile"):
        simulate_duty_limited_distillation(request)


def test_deterministic_domain_sweep_preserves_all_capacity_ledgers() -> None:
    rng = np.random.default_rng(20260711)
    for _ in range(20):
        feed = {
            "light": float(rng.uniform(0.4, 2.0)),
            "heavy": float(rng.uniform(0.4, 2.0)),
        }
        specs = _specs(
            light_vapor_pressure_Pa=float(rng.uniform(180_000.0, 300_000.0)),
            heavy_vapor_pressure_Pa=float(rng.uniform(40_000.0, 90_000.0)),
        )
        column = _column(
            maximum_reboiler_power_W=float(rng.uniform(5.0, 500.0)),
            maximum_condenser_power_W=float(rng.uniform(5.0, 500.0)),
            maximum_internal_vapor_rate_mol_s=float(rng.uniform(1.0e-4, 0.2)),
            minimum_bottoms_amount_mol=float(rng.uniform(0.0, 0.2)),
            maximum_distillate_cut_fraction=float(rng.uniform(0.4, 0.9)),
        )
        requested_cut = float(rng.uniform(0.0, 0.9))
        request = _request(
            feed=feed,
            specs=specs,
            column=column,
            pressure_Pa=30_000.0,
            duration_s=float(rng.uniform(50.0, 1_000.0)),
            reflux_ratio=float(rng.uniform(0.0, 5.0)),
            cut=requested_cut,
        )
        result = simulate_duty_limited_distillation(request)
        assert result.average_reboiler_power_W <= (column.maximum_reboiler_power_W + 1.0e-7)
        assert result.average_condenser_power_W <= (column.maximum_condenser_power_W + 1.0e-7)
        assert result.internal_vapor_rate_mol_s <= (
            column.maximum_internal_vapor_rate_mol_s + 1.0e-10
        )
        assert 0.0 <= result.actual_distillate_cut_fraction <= requested_cut + 1.0e-9
        _assert_closed(result)


def test_provider_returns_contract_complete_success_and_failure() -> None:
    provider = DutyLimitedDistillationProvider()
    success = provider.evaluate({"request": _request()})
    assert success.success is True
    assert success.outputs["distillation_result"]["model_id"] == DUTY_LIMITED_DISTILLATION_MODEL_ID
    assert success.diagnostics["cut_endpoint_met"] is True
    assert success.diagnostics["material_balance_error_mol"] <= 1.0e-9

    invalid = provider.evaluate({"request": {}})
    assert invalid.success is False
    assert invalid.outputs == {}
    assert invalid.failure_reason == "request must be a DutyLimitedDistillationRequest"

    bad_keys = provider.evaluate({"request": _request(light_key="heavy", heavy_key="light")})
    assert bad_keys.success is False
    assert "more volatile" in str(bad_keys.failure_reason)


def test_model_card_and_runtime_replacement_manifest_are_auditable() -> None:
    card = duty_limited_distillation_model_card()
    assert validate_model_card(card) == []
    assert card.model_id == DUTY_LIMITED_DISTILLATION_MODEL_ID
    assert any(IDAES_COMMIT in reference for reference in card.reference_reading)
    assert any(IDAES_TRAY_COLUMN_PATH in reference for reference in card.reference_reading)
    assert any(IDAES_CONDENSER_PATH in reference for reference in card.reference_reading)
    assert any(IDAES_REBOILER_PATH in reference for reference in card.reference_reading)
    assert any("not rigorous" in note for note in card.model_limit_notes)

    contract = duty_limited_distillation_provider_contract()
    manifest = duty_limited_distillation_adapter_manifest()
    assert manifest.provider_contract == contract
    assert manifest.owned_paths == OWNED_PATHS
    assert manifest.integration_operations == INTEGRATION_OPERATIONS
    assert manifest.replaces_model_ids == REPLACED_MODEL_IDS
    payload = manifest.to_dict()
    assert ModelAdapterManifest.from_dict(payload).to_dict() == payload
    payload["adapter_version"] = "tampered"
    with pytest.raises(ValueError, match="hash mismatch"):
        ModelAdapterManifest.from_dict(payload)


def test_distillation_result_serialization_is_deterministic() -> None:
    request = _request(column=_column(maximum_reboiler_power_W=25.0))
    left = json.dumps(
        simulate_duty_limited_distillation(request).to_dict(),
        sort_keys=True,
    )
    right = json.dumps(
        simulate_duty_limited_distillation(request).to_dict(),
        sort_keys=True,
    )
    assert left == right
