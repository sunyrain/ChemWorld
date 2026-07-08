from __future__ import annotations

import pytest

from chemworld.physchem import (
    FluidState,
    PipeSpec,
    counterflow_effectiveness,
    darcy_friction_factor,
    flow_regime,
    heat_exchanger_counterflow,
    homogeneous_two_phase_pressure_drop,
    internal_heat_transfer_coefficient,
    jacket_heat_transfer,
    mixing_power,
    nusselt_internal_flow,
    overall_heat_transfer_coefficient,
    packed_bed_pressure_drop_ergun,
    peclet_heat_number,
    pipe_pressure_drop,
    prandtl_number,
    pump_work,
    reynolds_number,
)


def test_dimensionless_numbers_and_flow_regime_are_physical() -> None:
    water = FluidState(
        density_kg_m3=998.0,
        viscosity_Pa_s=0.001,
        heat_capacity_J_kg_K=4180.0,
        thermal_conductivity_W_m_K=0.60,
    )
    low_re = reynolds_number(
        density_kg_m3=water.density_kg_m3,
        velocity_m_s=0.01,
        diameter_m=0.02,
        viscosity_Pa_s=water.viscosity_Pa_s,
    )
    high_re = reynolds_number(
        density_kg_m3=water.density_kg_m3,
        velocity_m_s=2.5,
        diameter_m=0.02,
        viscosity_Pa_s=water.viscosity_Pa_s,
    )
    pr = prandtl_number(
        heat_capacity_J_kg_K=water.heat_capacity_J_kg_K,
        viscosity_Pa_s=water.viscosity_Pa_s,
        thermal_conductivity_W_m_K=water.thermal_conductivity_W_m_K,
    )

    assert high_re > low_re
    assert flow_regime(low_re) == "laminar"
    assert flow_regime(high_re) == "turbulent"
    assert pr > 1.0
    assert peclet_heat_number(reynolds=high_re, prandtl=pr) == pytest.approx(high_re * pr)


def test_friction_factor_transitions_from_laminar_to_turbulent() -> None:
    laminar = darcy_friction_factor(reynolds=1000.0, relative_roughness=0.0)
    turbulent_smooth = darcy_friction_factor(reynolds=100_000.0, relative_roughness=0.0)
    turbulent_rough = darcy_friction_factor(reynolds=100_000.0, relative_roughness=0.01)

    assert laminar == pytest.approx(0.064)
    assert turbulent_smooth < laminar
    assert turbulent_rough > turbulent_smooth


def test_pipe_pressure_drop_increases_with_flow_and_length() -> None:
    water = FluidState(density_kg_m3=1000.0, viscosity_Pa_s=0.001)
    short_pipe = PipeSpec(length_m=5.0, diameter_m=0.025, roughness_m=1e-5)
    long_pipe = PipeSpec(length_m=20.0, diameter_m=0.025, roughness_m=1e-5)

    slow = pipe_pressure_drop(short_pipe, water, volumetric_flow_m3_s=2e-4)
    fast = pipe_pressure_drop(short_pipe, water, volumetric_flow_m3_s=8e-4)
    long = pipe_pressure_drop(long_pipe, water, volumetric_flow_m3_s=2e-4)

    assert fast.pressure_drop_total_Pa > slow.pressure_drop_total_Pa
    assert long.pressure_drop_total_Pa > slow.pressure_drop_total_Pa
    assert fast.pump_work_W > slow.pump_work_W >= 0.0
    assert fast.to_dict()["regime"] in {"transitional", "turbulent"}


def test_pump_work_and_mixing_power_are_nonnegative() -> None:
    assert pump_work(
        pressure_drop_Pa=100_000.0,
        volumetric_flow_m3_s=0.002,
        efficiency=0.5,
    ) == pytest.approx(400.0)

    mixed = mixing_power(
        power_number=5.0,
        density_kg_m3=950.0,
        impeller_diameter_m=0.08,
        rotational_speed_rev_s=12.0,
        liquid_volume_m3=0.010,
    )

    assert mixed["power_W"] > 0.0
    assert mixed["power_density_W_m3"] == pytest.approx(mixed["power_W"] / 0.010)


def test_nusselt_and_heat_transfer_coefficient_increase_with_turbulence() -> None:
    laminar_nu = nusselt_internal_flow(reynolds=1000.0, prandtl=7.0)
    turbulent_nu = nusselt_internal_flow(reynolds=50_000.0, prandtl=7.0)
    h_laminar = internal_heat_transfer_coefficient(
        nusselt=laminar_nu,
        thermal_conductivity_W_m_K=0.60,
        diameter_m=0.02,
    )
    h_turbulent = internal_heat_transfer_coefficient(
        nusselt=turbulent_nu,
        thermal_conductivity_W_m_K=0.60,
        diameter_m=0.02,
    )

    assert turbulent_nu > laminar_nu
    assert h_turbulent > h_laminar


def test_jacket_heat_transfer_scales_with_area_and_temperature_difference() -> None:
    base = jacket_heat_transfer(
        area_m2=1.0,
        overall_u_W_m2_K=250.0,
        reactor_temperature_K=320.0,
        jacket_temperature_K=360.0,
        duration_s=60.0,
    )
    larger_area = jacket_heat_transfer(
        area_m2=2.0,
        overall_u_W_m2_K=250.0,
        reactor_temperature_K=320.0,
        jacket_temperature_K=360.0,
        duration_s=60.0,
    )
    cooling = jacket_heat_transfer(
        area_m2=1.0,
        overall_u_W_m2_K=250.0,
        reactor_temperature_K=360.0,
        jacket_temperature_K=320.0,
        duration_s=60.0,
    )

    assert larger_area.heat_transfer_W == pytest.approx(2.0 * base.heat_transfer_W)
    assert base.heat_energy_J == pytest.approx(base.heat_transfer_W * 60.0)
    assert cooling.heat_transfer_W < 0.0


def test_overall_heat_transfer_coefficient_penalizes_fouling() -> None:
    clean = overall_heat_transfer_coefficient(
        inner_h_W_m2_K=1200.0,
        outer_h_W_m2_K=800.0,
        wall_thickness_m=0.002,
        wall_conductivity_W_m_K=16.0,
    )
    fouled = overall_heat_transfer_coefficient(
        inner_h_W_m2_K=1200.0,
        outer_h_W_m2_K=800.0,
        wall_thickness_m=0.002,
        wall_conductivity_W_m_K=16.0,
        fouling_inner_m2_K_W=0.001,
    )

    assert clean > fouled


def test_counterflow_heat_exchanger_conserves_stream_energy() -> None:
    small = heat_exchanger_counterflow(
        hot_inlet_temperature_K=380.0,
        cold_inlet_temperature_K=295.0,
        hot_mass_flow_kg_s=0.4,
        cold_mass_flow_kg_s=0.6,
        hot_heat_capacity_J_kg_K=2500.0,
        cold_heat_capacity_J_kg_K=4200.0,
        overall_u_W_m2_K=300.0,
        area_m2=0.8,
    )
    large = heat_exchanger_counterflow(
        hot_inlet_temperature_K=380.0,
        cold_inlet_temperature_K=295.0,
        hot_mass_flow_kg_s=0.4,
        cold_mass_flow_kg_s=0.6,
        hot_heat_capacity_J_kg_K=2500.0,
        cold_heat_capacity_J_kg_K=4200.0,
        overall_u_W_m2_K=300.0,
        area_m2=2.0,
    )
    hot_heat_lost = 0.4 * 2500.0 * (380.0 - large.hot_outlet_temperature_K)
    cold_heat_gained = 0.6 * 4200.0 * (large.cold_outlet_temperature_K - 295.0)

    assert 0.0 < small.effectiveness < large.effectiveness < 1.0
    assert large.heat_transfer_W > small.heat_transfer_W
    assert hot_heat_lost == pytest.approx(cold_heat_gained)
    assert large.to_dict()["heat_transfer_W"] == pytest.approx(large.heat_transfer_W)
    assert counterflow_effectiveness(ntu=1.0, capacity_ratio=1.0) == pytest.approx(0.5)


def test_packed_bed_pressure_drop_increases_with_velocity() -> None:
    gas = FluidState(density_kg_m3=1.2, viscosity_Pa_s=1.8e-5)
    slow = packed_bed_pressure_drop_ergun(
        fluid=gas,
        superficial_velocity_m_s=0.05,
        bed_length_m=0.5,
        particle_diameter_m=0.002,
        void_fraction=0.42,
    )
    fast = packed_bed_pressure_drop_ergun(
        fluid=gas,
        superficial_velocity_m_s=0.20,
        bed_length_m=0.5,
        particle_diameter_m=0.002,
        void_fraction=0.42,
    )

    assert fast.pressure_drop_Pa > slow.pressure_drop_Pa
    assert fast.inertial_term_Pa_m > slow.inertial_term_Pa_m


def test_homogeneous_two_phase_pressure_drop_tracks_quality() -> None:
    liquid_like = homogeneous_two_phase_pressure_drop(
        mass_flux_kg_m2_s=40.0,
        length_m=2.0,
        diameter_m=0.01,
        liquid_density_kg_m3=950.0,
        vapor_density_kg_m3=4.0,
        liquid_viscosity_Pa_s=0.001,
        vapor_viscosity_Pa_s=1.2e-5,
        vapor_quality=0.0,
    )
    mixed = homogeneous_two_phase_pressure_drop(
        mass_flux_kg_m2_s=40.0,
        length_m=2.0,
        diameter_m=0.01,
        liquid_density_kg_m3=950.0,
        vapor_density_kg_m3=4.0,
        liquid_viscosity_Pa_s=0.001,
        vapor_viscosity_Pa_s=1.2e-5,
        vapor_quality=0.35,
    )

    assert mixed.mixture_density_kg_m3 < liquid_like.mixture_density_kg_m3
    assert mixed.homogeneous_velocity_m_s > liquid_like.homogeneous_velocity_m_s
    assert mixed.pressure_drop_Pa > 0.0


def test_transport_validation_fails_fast() -> None:
    with pytest.raises(ValueError, match="diameter_m"):
        PipeSpec(length_m=1.0, diameter_m=0.0)
    with pytest.raises(ValueError, match="efficiency"):
        pump_work(pressure_drop_Pa=100.0, volumetric_flow_m3_s=1e-4, efficiency=1.5)
    with pytest.raises(ValueError, match="hot inlet"):
        heat_exchanger_counterflow(
            hot_inlet_temperature_K=300.0,
            cold_inlet_temperature_K=310.0,
            hot_mass_flow_kg_s=0.1,
            cold_mass_flow_kg_s=0.1,
            hot_heat_capacity_J_kg_K=1000.0,
            cold_heat_capacity_J_kg_K=1000.0,
            overall_u_W_m2_K=100.0,
            area_m2=1.0,
        )
    with pytest.raises(ValueError, match="void_fraction"):
        packed_bed_pressure_drop_ergun(
            fluid=FluidState(density_kg_m3=1000.0, viscosity_Pa_s=0.001),
            superficial_velocity_m_s=0.1,
            bed_length_m=1.0,
            particle_diameter_m=0.001,
            void_fraction=0.99,
        )
