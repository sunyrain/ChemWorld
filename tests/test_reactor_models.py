from __future__ import annotations

import pytest

from chemworld.physchem import (
    BatchReactorModel,
    CSTRModel,
    FeedStreamSpec,
    HeatTransferSpec,
    PFRModel,
    RateLawSpec,
    ReactionNetworkSpec,
    ReactionSpec,
    SemiBatchFeedSpec,
    SemiBatchReactorModel,
    SpeciesSpec,
)


def _isomerization_network(k: float = 0.02) -> ReactionNetworkSpec:
    return ReactionNetworkSpec(
        network_id="test_isomerization",
        species=(
            SpeciesSpec("A", "C2H4O2"),
            SpeciesSpec("P", "C2H4O2"),
        ),
        reactions=(
            ReactionSpec.from_equation(
                reaction_id="target",
                equation="A => P",
                rate_law=RateLawSpec("target_rate", "mass_action", {"k": k}),
                delta_h_J_per_mol=-12_000.0,
            ),
        ),
    )


def test_batch_reactor_tracks_material_and_energy_ledgers() -> None:
    model = BatchReactorModel(_isomerization_network())
    result = model.simulate(
        {"A": 1.0},
        volume_L=1.0,
        temperature_K=320.0,
        duration_s=100.0,
        heat_transfer=HeatTransferSpec(
            ua_W_per_K=0.1,
            jacket_ua_W_per_K=0.2,
            jacket_temperature_K=340.0,
        ),
        evaluation_times_s=(0.0, 50.0, 100.0),
    )

    assert result.final_state.amounts_mol["P"] > 0.0
    assert result.final_state.amounts_mol["A"] < 1.0
    assert result.material_balance_error_mol < 1e-8
    assert result.final_state.energy_jacket_J > 0.0
    assert result.conversion("A") == pytest.approx(1.0 - result.final_state.amounts_mol["A"])


def test_semibatch_reactor_adds_feed_and_preserves_elements() -> None:
    network = _isomerization_network(k=0.03)
    model = SemiBatchReactorModel(
        network,
        feeds=(
            SemiBatchFeedSpec(
                FeedStreamSpec(
                    {"A": 0.01},
                    volumetric_flow_L_s=0.001,
                    temperature_K=310.0,
                ),
                start_s=0.0,
                end_s=100.0,
            ),
        ),
    )
    result = model.simulate(
        {"A": 0.2},
        initial_volume_L=1.0,
        temperature_K=320.0,
        duration_s=150.0,
        evaluation_times_s=(0.0, 75.0, 150.0),
    )

    assert result.final_state.volume_L > 1.0
    assert result.final_state.material_in_mol["A"] == pytest.approx(1.0, rel=2e-3)
    assert result.final_state.amounts_mol["P"] > 0.0
    assert result.material_balance_error_mol < 1e-7


def test_cstr_conversion_increases_with_residence_time() -> None:
    network = _isomerization_network(k=0.08)
    inlet = FeedStreamSpec({"A": 0.01}, volumetric_flow_L_s=0.01, temperature_K=320.0)
    small = CSTRModel(network, inlet=inlet, volume_L=0.2).simulate_to_steady_state(
        temperature_K=320.0,
    )
    large = CSTRModel(network, inlet=inlet, volume_L=1.0).simulate_to_steady_state(
        temperature_K=320.0,
    )

    small_product_concentration = small.final_state.amounts_mol["P"] / small.final_state.volume_L
    large_product_concentration = large.final_state.amounts_mol["P"] / large.final_state.volume_L
    assert large_product_concentration > small_product_concentration
    assert large.material_balance_error_mol < 1e-6


def test_pfr_conversion_increases_with_residence_time() -> None:
    network = _isomerization_network(k=0.08)
    fast = PFRModel(network, reactor_volume_L=0.2, volumetric_flow_L_s=0.01).simulate(
        {"A": 1.0},
        temperature_K=320.0,
    )
    slow = PFRModel(network, reactor_volume_L=1.0, volumetric_flow_L_s=0.01).simulate(
        {"A": 1.0},
        temperature_K=320.0,
    )

    assert slow.yield_on("P", "A") > fast.yield_on("P", "A")
    assert slow.material_balance_error_mol < 1e-8


def test_reactor_models_reject_invalid_specs() -> None:
    network = _isomerization_network()
    with pytest.raises(ValueError, match="volume_L must be positive"):
        CSTRModel(network, FeedStreamSpec({"A": 1.0}, 1.0), volume_L=0.0)
    with pytest.raises(ValueError, match="volumetric_flow_L_s must be positive"):
        PFRModel(network, reactor_volume_L=1.0, volumetric_flow_L_s=0.0)
