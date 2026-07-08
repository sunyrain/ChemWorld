from __future__ import annotations

import pytest

from chemworld.physchem import (
    BatchReactorModel,
    CSTRModel,
    CSTRMultiplicitySpec,
    DynamicBatchReactorModel,
    FeedStreamSpec,
    HeatTransferSpec,
    JacketTemperatureProgram,
    NASA7SpeciesThermo,
    NASA7TemperatureSegment,
    PFRModel,
    RateLawSpec,
    ReactionNetworkSpec,
    ReactionSpec,
    SamplingEventSpec,
    SemiBatchFeedSpec,
    SemiBatchReactorModel,
    SpeciesSpec,
    cstr_multiple_steady_state_reference_case,
    reactor_model_cards,
    solve_cstr_multiple_steady_states,
    validate_model_card,
)

R_GAS = 8.31446261815324


def _constant_cp_thermo(
    species_id: str,
    *,
    enthalpy_offset_J_mol: float = 0.0,
) -> NASA7SpeciesThermo:
    return NASA7SpeciesThermo(
        species_id=species_id,
        segments=(
            NASA7TemperatureSegment(
                min_temperature_K=200.0,
                max_temperature_K=2500.0,
                coefficients=(3.5, 0.0, 0.0, 0.0, 0.0, enthalpy_offset_J_mol / R_GAS, 0.0),
                label=f"{species_id}:constant-cp",
            ),
        ),
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


def test_dynamic_batch_uses_nasa7_reaction_enthalpy_for_adiabatic_temperature_rise() -> None:
    network = ReactionNetworkSpec(
        network_id="dynamic_thermochemical_batch",
        species=(
            SpeciesSpec("A", "C2H4O2"),
            SpeciesSpec("P", "C2H4O2"),
        ),
        reactions=(
            ReactionSpec.from_equation(
                reaction_id="target",
                equation="A => P",
                rate_law=RateLawSpec("target_rate", "mass_action", {"k": 0.03}),
                delta_h_J_per_mol=0.0,
            ),
        ),
    )
    model = DynamicBatchReactorModel(network)
    result = model.simulate(
        {"A": 1.0},
        initial_volume_L=1.0,
        temperature_K=320.0,
        duration_s=120.0,
        heat_transfer=HeatTransferSpec(rho_cp_J_per_L_K=1000.0),
        species_thermo={
            "A": _constant_cp_thermo("A"),
            "P": _constant_cp_thermo("P", enthalpy_offset_J_mol=-12_000.0),
        },
        evaluation_times_s=(0.0, 60.0, 120.0),
    )

    assert result.metadata["heat_source"] == "nasa7_reaction_enthalpy"
    assert result.final_state.amounts_mol["P"] > 0.9
    assert result.final_state.heat_reaction_J < 0.0
    expected_temperature = 320.0 - result.final_state.heat_reaction_J / 1000.0
    assert result.final_state.temperature_K == pytest.approx(expected_temperature, rel=2e-4)


def test_dynamic_batch_sampling_event_updates_volume_and_material_out_ledger() -> None:
    model = DynamicBatchReactorModel(_isomerization_network(k=0.0))
    result = model.simulate(
        {"A": 1.0},
        initial_volume_L=1.0,
        temperature_K=300.0,
        duration_s=20.0,
        sampling_events=(SamplingEventSpec(time_s=10.0, volume_L=0.2),),
        evaluation_times_s=(0.0, 10.0, 20.0),
    )

    assert result.final_state.volume_L == pytest.approx(0.8)
    assert result.final_state.amounts_mol["A"] == pytest.approx(0.8)
    assert result.final_state.material_out_mol["A"] == pytest.approx(0.2)
    assert result.material_balance_error_mol < 1e-10
    assert result.metadata["sample_events"][0]["remaining_volume_L"] == pytest.approx(0.8)
    assert result.metadata["volume_L_timeseries"][-1] == pytest.approx(0.8)


def test_dynamic_batch_jacket_program_heats_reactor_and_records_energy() -> None:
    model = DynamicBatchReactorModel(_isomerization_network(k=0.0))
    result = model.simulate(
        {"A": 1.0},
        initial_volume_L=1.0,
        temperature_K=300.0,
        duration_s=80.0,
        heat_transfer=HeatTransferSpec(
            rho_cp_J_per_L_K=500.0,
            jacket_ua_W_per_K=2.0,
        ),
        jacket_program=JacketTemperatureProgram(
            ((0.0, 320.0), (40.0, 340.0)),
            mode="linear",
        ),
        evaluation_times_s=(0.0, 40.0, 80.0),
    )

    assert result.final_state.temperature_K > 300.0
    assert result.final_state.energy_jacket_J > 0.0
    assert result.metadata["jacket_program"]["mode"] == "linear"


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


def test_cstr_multiple_steady_state_reference_case_has_three_roots() -> None:
    spec = cstr_multiple_steady_state_reference_case()
    result = solve_cstr_multiple_steady_states(spec)

    assert len(result.steady_states) == 3
    assert result.temperatures_k == pytest.approx(
        (301.09292796381203, 339.9926749511754, 367.1096762683921),
        rel=1e-8,
        abs=1e-8,
    )
    assert tuple(point.stability for point in result.steady_states) == (
        "stable",
        "unstable",
        "stable",
    )
    assert len(result.stable_temperatures_k) == 2

    for point in result.steady_states:
        assert abs(point.residual_W) <= 1e-6
        assert point.heat_generation_w == pytest.approx(point.heat_removal_w, abs=1e-6)
        expected_a = spec.feed_concentration_A_mol_L / (
            1.0 + spec.rate_constant_s_inv(point.temperature_K) * spec.residence_time_s
        )
        assert point.concentration_A_mol_L == pytest.approx(expected_a)
        assert point.concentration_P_mol_L == pytest.approx(
            spec.feed_concentration_A_mol_L - expected_a
        )
        assert 0.0 < point.conversion < 1.0


def test_cstr_multiplicity_spec_exposes_balanced_network() -> None:
    spec = cstr_multiple_steady_state_reference_case()
    network = spec.network()
    assert network.check_element_balance()
    assert network.reactions[0].delta_h_J_per_mol < 0.0
    assert network.reactions[0].rate_law.parameters["A"] == spec.arrhenius_A_s_inv


def test_reactor_model_cards_document_cstr_multiplicity_slice() -> None:
    cards = reactor_model_cards()
    card = next(
        card
        for card in cards
        if card.model_id == "cstr_exothermic_multiplicity_reference"
    )
    assert card.maturity.value == "reference_validated"
    assert validate_model_card(card) == []
    assert any("Cantera" in note for note in card.reference_reading)
    assert any("IDAES" in note for note in card.reference_reading)


def test_reactor_model_cards_document_dynamic_batch_slice() -> None:
    cards = reactor_model_cards()
    card = next(
        card
        for card in cards
        if card.model_id == "dynamic_batch_heat_release_jacket_sampling"
    )
    assert card.maturity.value == "reference_validated"
    assert validate_model_card(card) == []
    assert any("Cantera" in note for note in card.reference_reading)
    assert any("IDAES" in note for note in card.reference_reading)
    assert any("sample" in mode for mode in card.failure_modes)


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
    with pytest.raises(ValueError, match="sampling volume"):
        DynamicBatchReactorModel(network).simulate(
            {"A": 1.0},
            initial_volume_L=1.0,
            temperature_K=300.0,
            duration_s=10.0,
            sampling_events=(SamplingEventSpec(time_s=1.0, volume_L=1.0),),
        )
    with pytest.raises(ValueError, match="volumetric_flow_L_s must be positive"):
        PFRModel(network, reactor_volume_L=1.0, volumetric_flow_L_s=0.0)
    with pytest.raises(ValueError, match="exothermic"):
        CSTRMultiplicitySpec(
            case_id="bad",
            feed_concentration_A_mol_L=1.0,
            volumetric_flow_L_s=1.0,
            volume_L=1.0,
            feed_temperature_K=300.0,
            coolant_temperature_K=290.0,
            ua_W_per_K=1.0,
            rho_cp_J_per_L_K=4180.0,
            delta_h_J_per_mol=10.0,
            arrhenius_A_s_inv=1.0,
            arrhenius_Ea_J_per_mol=10_000.0,
            temperature_bounds_K=(290.0, 400.0),
        )
