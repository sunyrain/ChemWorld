"""Fluid mechanics and heat-transfer kernels for ChemWorld.

The functions in this module intentionally cover a compact engineering core:
dimensionless groups, pipe pressure drop, pump work, mixing power, jacket heat
transfer, counterflow heat exchangers, packed beds, and a homogeneous two-phase
pressure-drop proxy.  They are local implementations aligned with standard
chemical-engineering correlations, not wrappers around reference projects.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from math import exp, isfinite, log, log10, pi
from typing import Literal

GRAVITY_M_S2 = 9.80665

FlowRegime = Literal["laminar", "transitional", "turbulent"]


@dataclass(frozen=True)
class FluidState:
    """Single-phase fluid properties in SI units."""

    density_kg_m3: float
    viscosity_Pa_s: float
    heat_capacity_J_kg_K: float = 4180.0
    thermal_conductivity_W_m_K: float = 0.6

    def __post_init__(self) -> None:
        _positive(self.density_kg_m3, "density_kg_m3")
        _positive(self.viscosity_Pa_s, "viscosity_Pa_s")
        _positive(self.heat_capacity_J_kg_K, "heat_capacity_J_kg_K")
        _positive(self.thermal_conductivity_W_m_K, "thermal_conductivity_W_m_K")

    def to_dict(self) -> dict[str, float]:
        return {
            "density_kg_m3": self.density_kg_m3,
            "viscosity_Pa_s": self.viscosity_Pa_s,
            "heat_capacity_J_kg_K": self.heat_capacity_J_kg_K,
            "thermal_conductivity_W_m_K": self.thermal_conductivity_W_m_K,
        }


@dataclass(frozen=True)
class PipeSpec:
    """Straight circular pipe segment."""

    length_m: float
    diameter_m: float
    roughness_m: float = 0.0
    elevation_change_m: float = 0.0
    fittings_loss_coefficient: float = 0.0

    def __post_init__(self) -> None:
        _positive(self.length_m, "length_m")
        _positive(self.diameter_m, "diameter_m")
        _nonnegative(self.roughness_m, "roughness_m")
        _nonnegative(self.fittings_loss_coefficient, "fittings_loss_coefficient")

    @property
    def area_m2(self) -> float:
        return pi * self.diameter_m**2 / 4.0

    @property
    def relative_roughness(self) -> float:
        return self.roughness_m / self.diameter_m

    def to_dict(self) -> dict[str, float]:
        return {
            "length_m": self.length_m,
            "diameter_m": self.diameter_m,
            "roughness_m": self.roughness_m,
            "elevation_change_m": self.elevation_change_m,
            "fittings_loss_coefficient": self.fittings_loss_coefficient,
        }


@dataclass(frozen=True)
class FlowResult:
    """Pipe-flow calculation with pressure drop and pump-work ledger."""

    volumetric_flow_m3_s: float
    mass_flow_kg_s: float
    velocity_m_s: float
    reynolds: float
    friction_factor: float
    pressure_drop_friction_Pa: float
    pressure_drop_fittings_Pa: float
    pressure_drop_static_Pa: float
    pressure_drop_total_Pa: float
    pump_work_W: float
    regime: FlowRegime
    metadata: dict[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _nonnegative(self.volumetric_flow_m3_s, "volumetric_flow_m3_s")
        _nonnegative(self.mass_flow_kg_s, "mass_flow_kg_s")
        _nonnegative(self.velocity_m_s, "velocity_m_s")
        _nonnegative(self.reynolds, "reynolds")
        _nonnegative(self.friction_factor, "friction_factor")
        _nonnegative(self.pressure_drop_friction_Pa, "pressure_drop_friction_Pa")
        _nonnegative(self.pressure_drop_fittings_Pa, "pressure_drop_fittings_Pa")
        _nonnegative(self.pressure_drop_total_Pa, "pressure_drop_total_Pa")
        _nonnegative(self.pump_work_W, "pump_work_W")

    def to_dict(self) -> dict[str, object]:
        return {
            "volumetric_flow_m3_s": self.volumetric_flow_m3_s,
            "mass_flow_kg_s": self.mass_flow_kg_s,
            "velocity_m_s": self.velocity_m_s,
            "reynolds": self.reynolds,
            "friction_factor": self.friction_factor,
            "pressure_drop_friction_Pa": self.pressure_drop_friction_Pa,
            "pressure_drop_fittings_Pa": self.pressure_drop_fittings_Pa,
            "pressure_drop_static_Pa": self.pressure_drop_static_Pa,
            "pressure_drop_total_Pa": self.pressure_drop_total_Pa,
            "pump_work_W": self.pump_work_W,
            "regime": self.regime,
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True)
class HeatTransferResult:
    """Signed heat-transfer result.

    Positive heat-transfer rates mean heat enters the controlled object.  For a
    reactor jacket this means heat enters the reactor; for a cooler it may be
    negative.
    """

    operation_id: str
    heat_transfer_W: float
    heat_energy_J: float
    overall_u_W_m2_K: float
    area_m2: float
    driving_force_K: float
    metadata: dict[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _finite(self.heat_transfer_W, "heat_transfer_W")
        _finite(self.heat_energy_J, "heat_energy_J")
        _positive(self.overall_u_W_m2_K, "overall_u_W_m2_K")
        _positive(self.area_m2, "area_m2")
        _finite(self.driving_force_K, "driving_force_K")

    def to_dict(self) -> dict[str, object]:
        return {
            "operation_id": self.operation_id,
            "heat_transfer_W": self.heat_transfer_W,
            "heat_energy_J": self.heat_energy_J,
            "overall_u_W_m2_K": self.overall_u_W_m2_K,
            "area_m2": self.area_m2,
            "driving_force_K": self.driving_force_K,
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True)
class HeatExchangerResult:
    """Counterflow heat-exchanger calculation using the effectiveness-NTU method."""

    heat_transfer_W: float
    hot_outlet_temperature_K: float
    cold_outlet_temperature_K: float
    effectiveness: float
    ntu: float
    capacity_ratio: float
    c_min_W_K: float
    c_max_W_K: float
    metadata: dict[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _nonnegative(self.heat_transfer_W, "heat_transfer_W")
        _positive(self.hot_outlet_temperature_K, "hot_outlet_temperature_K")
        _positive(self.cold_outlet_temperature_K, "cold_outlet_temperature_K")
        if not 0.0 <= self.effectiveness <= 1.0:
            raise ValueError("effectiveness must be between 0 and 1")
        _nonnegative(self.ntu, "ntu")
        if not 0.0 <= self.capacity_ratio <= 1.0:
            raise ValueError("capacity_ratio must be between 0 and 1")
        _positive(self.c_min_W_K, "c_min_W_K")
        _positive(self.c_max_W_K, "c_max_W_K")

    def to_dict(self) -> dict[str, object]:
        return {
            "heat_transfer_W": self.heat_transfer_W,
            "hot_outlet_temperature_K": self.hot_outlet_temperature_K,
            "cold_outlet_temperature_K": self.cold_outlet_temperature_K,
            "effectiveness": self.effectiveness,
            "ntu": self.ntu,
            "capacity_ratio": self.capacity_ratio,
            "c_min_W_K": self.c_min_W_K,
            "c_max_W_K": self.c_max_W_K,
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True)
class PackedBedResult:
    """Ergun packed-bed pressure-drop result."""

    pressure_drop_Pa: float
    reynolds_particle: float
    viscous_term_Pa_m: float
    inertial_term_Pa_m: float
    metadata: dict[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _nonnegative(self.pressure_drop_Pa, "pressure_drop_Pa")
        _nonnegative(self.reynolds_particle, "reynolds_particle")
        _nonnegative(self.viscous_term_Pa_m, "viscous_term_Pa_m")
        _nonnegative(self.inertial_term_Pa_m, "inertial_term_Pa_m")

    def to_dict(self) -> dict[str, object]:
        return {
            "pressure_drop_Pa": self.pressure_drop_Pa,
            "reynolds_particle": self.reynolds_particle,
            "viscous_term_Pa_m": self.viscous_term_Pa_m,
            "inertial_term_Pa_m": self.inertial_term_Pa_m,
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True)
class TwoPhasePressureDropResult:
    """Homogeneous-model two-phase pressure-drop proxy."""

    pressure_drop_Pa: float
    mixture_density_kg_m3: float
    mixture_viscosity_Pa_s: float
    homogeneous_velocity_m_s: float
    reynolds: float
    friction_factor: float
    metadata: dict[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _nonnegative(self.pressure_drop_Pa, "pressure_drop_Pa")
        _positive(self.mixture_density_kg_m3, "mixture_density_kg_m3")
        _positive(self.mixture_viscosity_Pa_s, "mixture_viscosity_Pa_s")
        _nonnegative(self.homogeneous_velocity_m_s, "homogeneous_velocity_m_s")
        _nonnegative(self.reynolds, "reynolds")
        _nonnegative(self.friction_factor, "friction_factor")

    def to_dict(self) -> dict[str, object]:
        return {
            "pressure_drop_Pa": self.pressure_drop_Pa,
            "mixture_density_kg_m3": self.mixture_density_kg_m3,
            "mixture_viscosity_Pa_s": self.mixture_viscosity_Pa_s,
            "homogeneous_velocity_m_s": self.homogeneous_velocity_m_s,
            "reynolds": self.reynolds,
            "friction_factor": self.friction_factor,
            "metadata": dict(self.metadata),
        }


def reynolds_number(
    *,
    density_kg_m3: float,
    velocity_m_s: float,
    diameter_m: float,
    viscosity_Pa_s: float,
) -> float:
    """Return Reynolds number for internal flow."""

    _positive(density_kg_m3, "density_kg_m3")
    _nonnegative(velocity_m_s, "velocity_m_s")
    _positive(diameter_m, "diameter_m")
    _positive(viscosity_Pa_s, "viscosity_Pa_s")
    return density_kg_m3 * velocity_m_s * diameter_m / viscosity_Pa_s


def prandtl_number(
    *,
    heat_capacity_J_kg_K: float,
    viscosity_Pa_s: float,
    thermal_conductivity_W_m_K: float,
) -> float:
    """Return Prandtl number from heat capacity, viscosity, and conductivity."""

    _positive(heat_capacity_J_kg_K, "heat_capacity_J_kg_K")
    _positive(viscosity_Pa_s, "viscosity_Pa_s")
    _positive(thermal_conductivity_W_m_K, "thermal_conductivity_W_m_K")
    return heat_capacity_J_kg_K * viscosity_Pa_s / thermal_conductivity_W_m_K


def peclet_heat_number(*, reynolds: float, prandtl: float) -> float:
    """Return heat-transfer Peclet number."""

    _nonnegative(reynolds, "reynolds")
    _positive(prandtl, "prandtl")
    return reynolds * prandtl


def nusselt_internal_flow(
    *,
    reynolds: float,
    prandtl: float,
    heating: bool = True,
    laminar_nusselt: float = 3.66,
) -> float:
    """Return a smooth internal-flow Nusselt estimate.

    The turbulent branch uses a Dittus-Boelter style relation.  The transitional
    interval is blended between the laminar and turbulent limits to avoid
    discontinuities in agent rollouts.
    """

    _nonnegative(reynolds, "reynolds")
    _positive(prandtl, "prandtl")
    _positive(laminar_nusselt, "laminar_nusselt")
    exponent = 0.4 if heating else 0.3
    turbulent = 0.023 * max(reynolds, 1e-12) ** 0.8 * prandtl**exponent
    if reynolds < 2300.0:
        return laminar_nusselt
    if reynolds > 10_000.0:
        return turbulent
    weight = (reynolds - 2300.0) / 7700.0
    return (1.0 - weight) * laminar_nusselt + weight * turbulent


def internal_heat_transfer_coefficient(
    *,
    nusselt: float,
    thermal_conductivity_W_m_K: float,
    diameter_m: float,
) -> float:
    """Convert Nusselt number to an internal heat-transfer coefficient."""

    _nonnegative(nusselt, "nusselt")
    _positive(thermal_conductivity_W_m_K, "thermal_conductivity_W_m_K")
    _positive(diameter_m, "diameter_m")
    return nusselt * thermal_conductivity_W_m_K / diameter_m


def flow_regime(reynolds: float) -> FlowRegime:
    """Classify internal flow regime."""

    _nonnegative(reynolds, "reynolds")
    if reynolds < 2300.0:
        return "laminar"
    if reynolds < 4000.0:
        return "transitional"
    return "turbulent"


def darcy_friction_factor(*, reynolds: float, relative_roughness: float = 0.0) -> float:
    """Return Darcy friction factor for circular-pipe flow.

    Laminar flow uses 64/Re. Turbulent flow uses the explicit Haaland
    approximation. Transitional flow is smoothly blended.
    """

    _positive(reynolds, "reynolds")
    _nonnegative(relative_roughness, "relative_roughness")
    if reynolds < 2300.0:
        return 64.0 / reynolds
    turbulent = _haaland_friction_factor(reynolds, relative_roughness)
    if reynolds >= 4000.0:
        return turbulent
    laminar_at_transition = 64.0 / 2300.0
    weight = (reynolds - 2300.0) / 1700.0
    return (1.0 - weight) * laminar_at_transition + weight * turbulent


def pipe_pressure_drop(
    pipe: PipeSpec,
    fluid: FluidState,
    *,
    volumetric_flow_m3_s: float,
    pump_efficiency: float = 0.70,
) -> FlowResult:
    """Calculate single-phase pressure drop with friction, fittings, and static head."""

    _nonnegative(volumetric_flow_m3_s, "volumetric_flow_m3_s")
    velocity = volumetric_flow_m3_s / pipe.area_m2
    mass_flow = volumetric_flow_m3_s * fluid.density_kg_m3
    if volumetric_flow_m3_s == 0.0:
        return FlowResult(
            volumetric_flow_m3_s=0.0,
            mass_flow_kg_s=0.0,
            velocity_m_s=0.0,
            reynolds=0.0,
            friction_factor=0.0,
            pressure_drop_friction_Pa=0.0,
            pressure_drop_fittings_Pa=0.0,
            pressure_drop_static_Pa=max(
                fluid.density_kg_m3 * GRAVITY_M_S2 * pipe.elevation_change_m,
                0.0,
            ),
            pressure_drop_total_Pa=max(
                fluid.density_kg_m3 * GRAVITY_M_S2 * pipe.elevation_change_m,
                0.0,
            ),
            pump_work_W=0.0,
            regime="laminar",
            metadata={
                "pipe": pipe.to_dict(),
                "fluid": fluid.to_dict(),
                "note": "zero flow",
            },
        )
    re = reynolds_number(
        density_kg_m3=fluid.density_kg_m3,
        velocity_m_s=velocity,
        diameter_m=pipe.diameter_m,
        viscosity_Pa_s=fluid.viscosity_Pa_s,
    )
    friction = darcy_friction_factor(reynolds=re, relative_roughness=pipe.relative_roughness)
    dynamic_pressure = 0.5 * fluid.density_kg_m3 * velocity**2
    friction_drop = friction * pipe.length_m / pipe.diameter_m * dynamic_pressure
    fittings_drop = pipe.fittings_loss_coefficient * dynamic_pressure
    static_drop = fluid.density_kg_m3 * GRAVITY_M_S2 * pipe.elevation_change_m
    total_drop = max(friction_drop + fittings_drop + static_drop, 0.0)
    return FlowResult(
        volumetric_flow_m3_s=volumetric_flow_m3_s,
        mass_flow_kg_s=mass_flow,
        velocity_m_s=velocity,
        reynolds=re,
        friction_factor=friction,
        pressure_drop_friction_Pa=friction_drop,
        pressure_drop_fittings_Pa=fittings_drop,
        pressure_drop_static_Pa=static_drop,
        pressure_drop_total_Pa=total_drop,
        pump_work_W=pump_work(
            pressure_drop_Pa=total_drop,
            volumetric_flow_m3_s=volumetric_flow_m3_s,
            efficiency=pump_efficiency,
        ),
        regime=flow_regime(re),
        metadata={
            "pipe": pipe.to_dict(),
            "fluid": fluid.to_dict(),
            "dynamic_pressure_Pa": dynamic_pressure,
        },
    )


def pump_work(*, pressure_drop_Pa: float, volumetric_flow_m3_s: float, efficiency: float) -> float:
    """Return hydraulic pump work in W."""

    _nonnegative(pressure_drop_Pa, "pressure_drop_Pa")
    _nonnegative(volumetric_flow_m3_s, "volumetric_flow_m3_s")
    if not 0.0 < efficiency <= 1.0:
        raise ValueError("efficiency must be in (0, 1]")
    return pressure_drop_Pa * volumetric_flow_m3_s / efficiency


def mixing_power(
    *,
    power_number: float,
    density_kg_m3: float,
    impeller_diameter_m: float,
    rotational_speed_rev_s: float,
    liquid_volume_m3: float | None = None,
) -> dict[str, float]:
    """Return impeller power and optional volumetric power density.

    The base relation is P = Np rho N^3 D^5, suitable for turbulent impeller
    scaling and useful as a first-order process-cost/safety signal.
    """

    _positive(power_number, "power_number")
    _positive(density_kg_m3, "density_kg_m3")
    _positive(impeller_diameter_m, "impeller_diameter_m")
    _nonnegative(rotational_speed_rev_s, "rotational_speed_rev_s")
    power = (
        power_number
        * density_kg_m3
        * rotational_speed_rev_s**3
        * impeller_diameter_m**5
    )
    result = {"power_W": power}
    if liquid_volume_m3 is not None:
        _positive(liquid_volume_m3, "liquid_volume_m3")
        result["power_density_W_m3"] = power / liquid_volume_m3
    return result


def overall_heat_transfer_coefficient(
    *,
    inner_h_W_m2_K: float,
    outer_h_W_m2_K: float,
    wall_thickness_m: float,
    wall_conductivity_W_m_K: float,
    fouling_inner_m2_K_W: float = 0.0,
    fouling_outer_m2_K_W: float = 0.0,
) -> float:
    """Return U from film, fouling, and wall thermal resistances."""

    _positive(inner_h_W_m2_K, "inner_h_W_m2_K")
    _positive(outer_h_W_m2_K, "outer_h_W_m2_K")
    _nonnegative(wall_thickness_m, "wall_thickness_m")
    _positive(wall_conductivity_W_m_K, "wall_conductivity_W_m_K")
    _nonnegative(fouling_inner_m2_K_W, "fouling_inner_m2_K_W")
    _nonnegative(fouling_outer_m2_K_W, "fouling_outer_m2_K_W")
    resistance = (
        1.0 / inner_h_W_m2_K
        + fouling_inner_m2_K_W
        + wall_thickness_m / wall_conductivity_W_m_K
        + fouling_outer_m2_K_W
        + 1.0 / outer_h_W_m2_K
    )
    return 1.0 / resistance


def jacket_heat_transfer(
    *,
    area_m2: float,
    overall_u_W_m2_K: float,
    reactor_temperature_K: float,
    jacket_temperature_K: float,
    duration_s: float = 0.0,
) -> HeatTransferResult:
    """Return signed jacket heat transfer into the reactor."""

    _positive(area_m2, "area_m2")
    _positive(overall_u_W_m2_K, "overall_u_W_m2_K")
    _positive(reactor_temperature_K, "reactor_temperature_K")
    _positive(jacket_temperature_K, "jacket_temperature_K")
    _nonnegative(duration_s, "duration_s")
    driving_force = jacket_temperature_K - reactor_temperature_K
    heat_rate = overall_u_W_m2_K * area_m2 * driving_force
    return HeatTransferResult(
        operation_id="jacket_heat_transfer",
        heat_transfer_W=heat_rate,
        heat_energy_J=heat_rate * duration_s,
        overall_u_W_m2_K=overall_u_W_m2_K,
        area_m2=area_m2,
        driving_force_K=driving_force,
        metadata={
            "reactor_temperature_K": reactor_temperature_K,
            "jacket_temperature_K": jacket_temperature_K,
            "duration_s": duration_s,
        },
    )


def counterflow_effectiveness(*, ntu: float, capacity_ratio: float) -> float:
    """Return counterflow heat-exchanger effectiveness."""

    _nonnegative(ntu, "ntu")
    if not 0.0 <= capacity_ratio <= 1.0:
        raise ValueError("capacity_ratio must be between 0 and 1")
    if ntu == 0.0:
        return 0.0
    if abs(capacity_ratio - 1.0) < 1e-9:
        return ntu / (1.0 + ntu)
    exponential = exp(-ntu * (1.0 - capacity_ratio))
    effectiveness = (1.0 - exponential) / (1.0 - capacity_ratio * exponential)
    return _clip01(effectiveness)


def heat_exchanger_counterflow(
    *,
    hot_inlet_temperature_K: float,
    cold_inlet_temperature_K: float,
    hot_mass_flow_kg_s: float,
    cold_mass_flow_kg_s: float,
    hot_heat_capacity_J_kg_K: float,
    cold_heat_capacity_J_kg_K: float,
    overall_u_W_m2_K: float,
    area_m2: float,
) -> HeatExchangerResult:
    """Calculate counterflow heat exchange using the effectiveness-NTU method."""

    _positive(hot_inlet_temperature_K, "hot_inlet_temperature_K")
    _positive(cold_inlet_temperature_K, "cold_inlet_temperature_K")
    if hot_inlet_temperature_K < cold_inlet_temperature_K:
        raise ValueError("hot inlet temperature must be >= cold inlet temperature")
    _positive(hot_mass_flow_kg_s, "hot_mass_flow_kg_s")
    _positive(cold_mass_flow_kg_s, "cold_mass_flow_kg_s")
    _positive(hot_heat_capacity_J_kg_K, "hot_heat_capacity_J_kg_K")
    _positive(cold_heat_capacity_J_kg_K, "cold_heat_capacity_J_kg_K")
    _positive(overall_u_W_m2_K, "overall_u_W_m2_K")
    _positive(area_m2, "area_m2")

    c_hot = hot_mass_flow_kg_s * hot_heat_capacity_J_kg_K
    c_cold = cold_mass_flow_kg_s * cold_heat_capacity_J_kg_K
    c_min = min(c_hot, c_cold)
    c_max = max(c_hot, c_cold)
    capacity_ratio = c_min / c_max
    ntu = overall_u_W_m2_K * area_m2 / c_min
    effectiveness = counterflow_effectiveness(ntu=ntu, capacity_ratio=capacity_ratio)
    heat_transfer = effectiveness * c_min * (
        hot_inlet_temperature_K - cold_inlet_temperature_K
    )
    hot_outlet = hot_inlet_temperature_K - heat_transfer / c_hot
    cold_outlet = cold_inlet_temperature_K + heat_transfer / c_cold
    return HeatExchangerResult(
        heat_transfer_W=heat_transfer,
        hot_outlet_temperature_K=hot_outlet,
        cold_outlet_temperature_K=cold_outlet,
        effectiveness=effectiveness,
        ntu=ntu,
        capacity_ratio=capacity_ratio,
        c_min_W_K=c_min,
        c_max_W_K=c_max,
        metadata={
            "c_hot_W_K": c_hot,
            "c_cold_W_K": c_cold,
            "overall_u_W_m2_K": overall_u_W_m2_K,
            "area_m2": area_m2,
        },
    )


def packed_bed_pressure_drop_ergun(
    *,
    fluid: FluidState,
    superficial_velocity_m_s: float,
    bed_length_m: float,
    particle_diameter_m: float,
    void_fraction: float,
    sphericity: float = 1.0,
) -> PackedBedResult:
    """Return packed-bed pressure drop from the Ergun equation."""

    _nonnegative(superficial_velocity_m_s, "superficial_velocity_m_s")
    _positive(bed_length_m, "bed_length_m")
    _positive(particle_diameter_m, "particle_diameter_m")
    if not 0.05 < void_fraction < 0.95:
        raise ValueError("void_fraction must be in (0.05, 0.95)")
    if not 0.1 <= sphericity <= 1.0:
        raise ValueError("sphericity must be in [0.1, 1]")
    effective_particle = particle_diameter_m * sphericity
    re_particle = (
        fluid.density_kg_m3
        * superficial_velocity_m_s
        * effective_particle
        / fluid.viscosity_Pa_s
    )
    eps = void_fraction
    viscous = (
        150.0
        * (1.0 - eps) ** 2
        * fluid.viscosity_Pa_s
        * superficial_velocity_m_s
        / (eps**3 * effective_particle**2)
    )
    inertial = (
        1.75
        * (1.0 - eps)
        * fluid.density_kg_m3
        * superficial_velocity_m_s**2
        / (eps**3 * effective_particle)
    )
    return PackedBedResult(
        pressure_drop_Pa=(viscous + inertial) * bed_length_m,
        reynolds_particle=re_particle,
        viscous_term_Pa_m=viscous,
        inertial_term_Pa_m=inertial,
        metadata={
            "bed_length_m": bed_length_m,
            "particle_diameter_m": particle_diameter_m,
            "void_fraction": void_fraction,
            "sphericity": sphericity,
        },
    )


def homogeneous_two_phase_pressure_drop(
    *,
    mass_flux_kg_m2_s: float,
    length_m: float,
    diameter_m: float,
    liquid_density_kg_m3: float,
    vapor_density_kg_m3: float,
    liquid_viscosity_Pa_s: float,
    vapor_viscosity_Pa_s: float,
    vapor_quality: float,
    roughness_m: float = 0.0,
) -> TwoPhasePressureDropResult:
    """Return a homogeneous two-phase pressure-drop proxy.

    This is intentionally a first-order benchmark model. It is useful for
    ranking risky operations and generating observations, not for detailed
    two-fluid equipment design.
    """

    _nonnegative(mass_flux_kg_m2_s, "mass_flux_kg_m2_s")
    _positive(length_m, "length_m")
    _positive(diameter_m, "diameter_m")
    _positive(liquid_density_kg_m3, "liquid_density_kg_m3")
    _positive(vapor_density_kg_m3, "vapor_density_kg_m3")
    _positive(liquid_viscosity_Pa_s, "liquid_viscosity_Pa_s")
    _positive(vapor_viscosity_Pa_s, "vapor_viscosity_Pa_s")
    if not 0.0 <= vapor_quality <= 1.0:
        raise ValueError("vapor_quality must be between 0 and 1")
    _nonnegative(roughness_m, "roughness_m")
    quality = vapor_quality
    mixture_density = 1.0 / (
        quality / vapor_density_kg_m3 + (1.0 - quality) / liquid_density_kg_m3
    )
    mixture_viscosity = exp(
        quality * log(vapor_viscosity_Pa_s)
        + (1.0 - quality) * log(liquid_viscosity_Pa_s)
    )
    velocity = mass_flux_kg_m2_s / mixture_density if mixture_density > 0 else 0.0
    if mass_flux_kg_m2_s == 0.0:
        re = 0.0
        friction = 0.0
        pressure_drop = 0.0
    else:
        re = mass_flux_kg_m2_s * diameter_m / mixture_viscosity
        friction = darcy_friction_factor(
            reynolds=re,
            relative_roughness=roughness_m / diameter_m,
        )
        pressure_drop = friction * length_m / diameter_m * (
            0.5 * mixture_density * velocity**2
        )
    return TwoPhasePressureDropResult(
        pressure_drop_Pa=pressure_drop,
        mixture_density_kg_m3=mixture_density,
        mixture_viscosity_Pa_s=mixture_viscosity,
        homogeneous_velocity_m_s=velocity,
        reynolds=re,
        friction_factor=friction,
        metadata={
            "mass_flux_kg_m2_s": mass_flux_kg_m2_s,
            "length_m": length_m,
            "diameter_m": diameter_m,
            "vapor_quality": vapor_quality,
            "roughness_m": roughness_m,
        },
    )


def _haaland_friction_factor(reynolds: float, relative_roughness: float) -> float:
    argument = (relative_roughness / 3.7) ** 1.11 + 6.9 / reynolds
    return 1.0 / (-1.8 * log10(argument)) ** 2


def _clip01(value: float) -> float:
    return max(0.0, min(1.0, value))


def _finite(value: float, name: str) -> None:
    if not isfinite(value):
        raise ValueError(f"{name} must be finite")


def _positive(value: float, name: str) -> None:
    _finite(value, name)
    if value <= 0.0:
        raise ValueError(f"{name} must be positive")


def _nonnegative(value: float, name: str) -> None:
    _finite(value, name)
    if value < 0.0:
        raise ValueError(f"{name} cannot be negative")
