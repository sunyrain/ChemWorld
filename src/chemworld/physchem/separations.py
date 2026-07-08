"""Separation and downstream unit-operation kernels for ChemWorld."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from math import exp, isfinite, log, log1p

from chemworld.physchem.equilibrium import (
    ActivityModelSpec,
    flash_isothermal,
    liquid_liquid_split,
    raoult_k_values,
)
from chemworld.physchem.maturity import MaturityLevel, ModelCard, ValidationEvidence


@dataclass(frozen=True)
class SeparationLedger:
    unit_id: str
    cost: float
    risk: float
    heat_duty_J: float = 0.0
    solvent_loss_mol: float = 0.0
    material_balance_error_mol: float = 0.0
    metadata: dict[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.cost < 0:
            raise ValueError("cost cannot be negative")
        if not 0.0 <= self.risk <= 1.0:
            raise ValueError("risk must be between 0 and 1")
        if self.heat_duty_J < 0:
            raise ValueError("heat_duty_J cannot be negative")
        if self.solvent_loss_mol < 0:
            raise ValueError("solvent_loss_mol cannot be negative")
        if self.material_balance_error_mol < 0:
            raise ValueError("material_balance_error_mol cannot be negative")

    def to_dict(self) -> dict[str, object]:
        return {
            "unit_id": self.unit_id,
            "cost": self.cost,
            "risk": self.risk,
            "heat_duty_J": self.heat_duty_J,
            "solvent_loss_mol": self.solvent_loss_mol,
            "material_balance_error_mol": self.material_balance_error_mol,
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True)
class SeparationResult:
    operation_id: str
    outlets: dict[str, dict[str, float]]
    ledger: SeparationLedger

    def __post_init__(self) -> None:
        if not self.operation_id:
            raise ValueError("operation_id cannot be empty")
        if not self.outlets:
            raise ValueError("separation result must contain at least one outlet")
        for outlet_id, amounts in self.outlets.items():
            if not outlet_id:
                raise ValueError("outlet ids cannot be empty")
            if any(value < -1e-12 for value in amounts.values()):
                raise ValueError("outlet amounts cannot be negative")

    def outlet(self, outlet_id: str) -> dict[str, float]:
        return dict(self.outlets[outlet_id])

    def recovery(self, component_id: str, outlet_id: str, feed_amount_mol: float) -> float:
        if feed_amount_mol <= 0:
            return 0.0
        return _clip01(self.outlets[outlet_id].get(component_id, 0.0) / feed_amount_mol)

    def purity(
        self,
        component_id: str,
        outlet_id: str,
        *,
        ignored_components: Sequence[str] = (),
    ) -> float:
        outlet = self.outlets[outlet_id]
        denominator = sum(
            amount
            for key, amount in outlet.items()
            if key not in set(ignored_components) and amount > 0
        )
        if denominator <= 0:
            return 0.0
        return _clip01(outlet.get(component_id, 0.0) / denominator)

    def to_dict(self) -> dict[str, object]:
        return {
            "operation_id": self.operation_id,
            "outlets": {key: dict(value) for key, value in self.outlets.items()},
            "ledger": self.ledger.to_dict(),
        }


def liquid_liquid_extraction(
    feed_amounts_mol: Mapping[str, float],
    *,
    partition_coefficients: Mapping[str, float],
    aqueous_volume_L: float,
    organic_volume_L: float,
    stages: int = 1,
    stage_efficiency: float = 1.0,
    entrainment_fraction: float = 0.0,
    solvent_loss_fraction: float = 0.0,
) -> SeparationResult:
    feed = _amounts(feed_amounts_mol)
    if stages <= 0:
        raise ValueError("stages must be positive")
    if not 0.0 <= solvent_loss_fraction < 1.0:
        raise ValueError("solvent_loss_fraction must be in [0, 1)")
    raffinate = dict(feed)
    extract = dict.fromkeys(feed, 0.0)
    solvent_loss_mol = 0.0
    phase_volume = max(organic_volume_L, 1e-12)
    for _ in range(stages):
        split = liquid_liquid_split(
            raffinate,
            partition_coefficients=partition_coefficients,
            aqueous_volume_L=aqueous_volume_L,
            organic_volume_L=organic_volume_L,
            stage_efficiency=stage_efficiency,
            entrainment_fraction=entrainment_fraction,
        )
        extract = _add_amounts(extract, split.organic_amounts_mol)
        raffinate = split.aqueous_amounts_mol
        solvent_loss_mol += solvent_loss_fraction * phase_volume
    outlets = {"extract": extract, "raffinate": raffinate}
    cost = 0.35 * stages + 0.08 * organic_volume_L * stages + 0.04 * aqueous_volume_L
    risk = _clip01(0.04 * stages + 0.25 * entrainment_fraction + 0.15 * solvent_loss_fraction)
    return SeparationResult(
        operation_id="liquid_liquid_extraction",
        outlets=outlets,
        ledger=SeparationLedger(
            unit_id="liquid_liquid_extraction",
            cost=cost,
            risk=risk,
            solvent_loss_mol=solvent_loss_mol,
            material_balance_error_mol=_component_balance_error(feed, outlets),
            metadata={
                "stages": stages,
                "stage_efficiency": stage_efficiency,
                "entrainment_fraction": entrainment_fraction,
            },
        ),
    )


def evaporation_flash(
    feed_amounts_mol: Mapping[str, float],
    *,
    k_values: Mapping[str, float],
    latent_heats_J_mol: Mapping[str, float],
    approach_to_equilibrium: float = 1.0,
    max_vapor_fraction: float = 1.0,
) -> SeparationResult:
    feed = _amounts(feed_amounts_mol)
    if not 0.0 <= approach_to_equilibrium <= 1.0:
        raise ValueError("approach_to_equilibrium must be between 0 and 1")
    if not 0.0 <= max_vapor_fraction <= 1.0:
        raise ValueError("max_vapor_fraction must be between 0 and 1")
    flash = flash_isothermal(feed, k_values)
    beta = min(flash.vapor_fraction * approach_to_equilibrium, max_vapor_fraction)
    vapor, liquid = _flash_amount_split(feed, k_values, beta)
    heat_duty = sum(
        vapor[component_id] * float(latent_heats_J_mol.get(component_id, 35_000.0))
        for component_id in vapor
    )
    total_liquid = max(sum(liquid.values()), 1e-12)
    concentration_risk = max((amount / total_liquid for amount in liquid.values()), default=0.0)
    outlets = {"vapor": vapor, "liquid": liquid}
    return SeparationResult(
        operation_id="evaporation_flash",
        outlets=outlets,
        ledger=SeparationLedger(
            unit_id="evaporation_flash",
            cost=heat_duty / 1_000_000.0 + 0.20 * beta,
            risk=_clip01(0.10 + 0.40 * beta + 0.20 * concentration_risk),
            heat_duty_J=heat_duty,
            material_balance_error_mol=_component_balance_error(feed, outlets),
            metadata={
                "equilibrium_vapor_fraction": flash.vapor_fraction,
                "actual_vapor_fraction": beta,
            },
        ),
    )


def vle_shortcut_distillation(
    feed_amounts_mol: Mapping[str, float],
    *,
    vapor_pressures_Pa: Mapping[str, float],
    pressure_Pa: float,
    temperature_K: float,
    light_key: str,
    heavy_key: str,
    distillate_cut_fraction: float,
    theoretical_stages: float,
    reflux_ratio: float = 1.0,
    stage_efficiency: float = 1.0,
    activity_model: ActivityModelSpec | None = None,
    latent_heats_J_mol: Mapping[str, float] | None = None,
    vapor_fugacity_coefficients: Mapping[str, float] | None = None,
) -> SeparationResult:
    """Shortcut distillation with VLE-derived relative volatilities.

    Component distribution ratios obey a Fenske-style constant-relative-
    volatility relationship:

        (D_i/B_i) / (D_j/B_j) = (alpha_i/alpha_j)**N_eff

    A single cut parameter is then solved so the requested total distillate
    cut is met exactly.
    """

    feed = _amounts(feed_amounts_mol)
    if not 0.0 <= distillate_cut_fraction <= 1.0:
        raise ValueError("distillate_cut_fraction must be between 0 and 1")
    if pressure_Pa <= 0 or temperature_K <= 0:
        raise ValueError("pressure_Pa and temperature_K must be positive")
    if light_key not in feed or heavy_key not in feed:
        raise ValueError("light_key and heavy_key must be present in feed")
    if light_key == heavy_key:
        raise ValueError("light_key and heavy_key must be distinct")
    if theoretical_stages <= 0:
        raise ValueError("theoretical_stages must be positive")
    if reflux_ratio < 0:
        raise ValueError("reflux_ratio cannot be negative")
    if not 0.0 <= stage_efficiency <= 1.0:
        raise ValueError("stage_efficiency must be between 0 and 1")

    component_ids = tuple(feed)
    if activity_model is None:
        activity_model = ActivityModelSpec(
            "ideal_distillation_activity",
            component_ids,
            "ideal",
        )
    elif set(activity_model.component_ids) != set(component_ids):
        raise ValueError("activity_model components must match feed components")
    component_ids = activity_model.component_ids
    _validate_positive_mapping(
        vapor_pressures_Pa,
        component_ids=component_ids,
        value_name="vapor_pressures_Pa",
    )
    if latent_heats_J_mol is not None:
        _validate_positive_mapping(
            latent_heats_J_mol,
            component_ids=component_ids,
            value_name="latent_heats_J_mol",
        )

    total_feed = sum(feed.values())
    overall_composition = {
        component_id: feed[component_id] / total_feed for component_id in component_ids
    }
    k_values = raoult_k_values(
        activity_model,
        overall_composition,
        vapor_pressures_Pa=vapor_pressures_Pa,
        pressure_Pa=pressure_Pa,
        temperature_K=temperature_K,
        vapor_fugacity_coefficients=vapor_fugacity_coefficients,
    )
    flash = flash_isothermal(overall_composition, k_values)
    heavy_key_k = k_values[heavy_key]
    if heavy_key_k <= 0.0:
        raise ValueError("heavy_key VLE K-value must be positive")
    relative_volatilities = {
        component_id: k_values[component_id] / heavy_key_k for component_id in component_ids
    }
    key_relative_volatility = relative_volatilities[light_key]
    if key_relative_volatility <= 1.0:
        raise ValueError("light_key must be more volatile than heavy_key")

    reflux_effectiveness = 0.0 if reflux_ratio == 0.0 else reflux_ratio / (1.0 + reflux_ratio)
    effective_stages = theoretical_stages * stage_efficiency * reflux_effectiveness
    separation_factors = {
        component_id: relative_volatilities[component_id] ** effective_stages
        for component_id in component_ids
    }
    target_distillate = total_feed * distillate_cut_fraction
    distillate = _shortcut_distillate_split(feed, separation_factors, target_distillate)
    bottoms = {component_id: feed[component_id] - distillate[component_id] for component_id in feed}
    latent_heats = dict.fromkeys(component_ids, 35_000.0)
    if latent_heats_J_mol is not None:
        latent_heats.update({key: float(value) for key, value in latent_heats_J_mol.items()})
    distillate_total = sum(distillate.values())
    average_latent_heat = (
        0.0
        if distillate_total <= 0.0
        else sum(
            distillate[component_id] * latent_heats[component_id]
            for component_id in component_ids
        )
        / distillate_total
    )
    internal_vapor_mol = distillate_total * (1.0 + reflux_ratio)
    heat_duty = internal_vapor_mol * average_latent_heat
    distribution_ratios = {
        component_id: _safe_distribution_ratio(distillate[component_id], bottoms[component_id])
        for component_id in component_ids
    }
    observed_stage_count = _observed_fenske_stage_count(
        distribution_ratios,
        relative_volatilities,
        light_key=light_key,
        heavy_key=heavy_key,
    )
    temperature_risk = max(temperature_K - 298.15, 0.0) / 150.0
    pressure_risk = max(pressure_Pa / 101_325.0 - 1.0, 0.0) / 8.0
    outlets = {"distillate": distillate, "bottoms": bottoms}
    return SeparationResult(
        operation_id="vle_shortcut_distillation",
        outlets=outlets,
        ledger=SeparationLedger(
            unit_id="vle_shortcut_distillation",
            cost=heat_duty / 850_000.0 + 0.08 * theoretical_stages + 0.10 * reflux_ratio,
            risk=_clip01(
                0.08
                + 0.04 * log1p(reflux_ratio)
                + 0.08 * flash.vapor_fraction
                + 0.05 * temperature_risk
                + 0.04 * pressure_risk
            ),
            heat_duty_J=heat_duty,
            material_balance_error_mol=_component_balance_error(feed, outlets),
            metadata={
                "distillate_cut_fraction": distillate_cut_fraction,
                "reflux_ratio": reflux_ratio,
                "reflux_effectiveness": reflux_effectiveness,
                "theoretical_stages": theoretical_stages,
                "stage_efficiency": stage_efficiency,
                "effective_stages": effective_stages,
                "light_key": light_key,
                "heavy_key": heavy_key,
                "k_values": dict(k_values),
                "relative_volatilities": dict(relative_volatilities),
                "separation_factors": dict(separation_factors),
                "distribution_ratios": dict(distribution_ratios),
                "observed_fenske_stage_count": observed_stage_count,
                "flash_anchor": flash.to_dict(),
                "internal_vapor_mol": internal_vapor_mol,
                "average_latent_heat_J_mol": average_latent_heat,
                "condenser_duty_J": heat_duty,
            },
        ),
    )


def separation_model_cards() -> tuple[ModelCard, ...]:
    return (
        ModelCard(
            model_id="vle_shortcut_distillation",
            module_id="separations",
            title="VLE-Coupled Shortcut Distillation",
            maturity=MaturityLevel.REFERENCE_VALIDATED,
            summary=(
                "Constant-relative-volatility shortcut distillation model "
                "whose separation factors are derived from Raoult/activity "
                "VLE K-values rather than arbitrary volatility scores."
            ),
            equations=(
                "K_i = gamma_i Psat_i / (phi_i P)",
                "alpha_i,HK = K_i / K_HK",
                "N_eff = N_theoretical * tray_efficiency * R/(1+R)",
                "(D_i/B_i)/(D_j/B_j) = (alpha_i/alpha_j)**N_eff",
                "sum_i D_i = distillate_cut * sum_i F_i",
            ),
            assumptions=(
                "constant relative volatility at the supplied temperature and pressure",
                "total condenser/reboiler shortcut behavior represented by reflux-scaled stages",
                "no tray hydraulics, flooding, pressure profile, or rigorous MESH solve",
                "latent heat duty scales with internal vapor traffic",
            ),
            validity_limits=(
                "requires positive vapor pressures and positive VLE K-values",
                "light key must be more volatile than heavy key under supplied VLE conditions",
                "intended for benchmark-scale binary or small multicomponent separations",
                "not valid for azeotropic, reactive, or multiple-liquid-phase columns",
            ),
            failure_modes=(
                "missing feed, vapor-pressure, or latent-heat components raise validation errors",
                (
                    "invalid pressure, temperature, cut fraction, reflux, or "
                    "stage efficiency fails early"
                ),
                "key order that contradicts VLE K-values fails instead of silently swapping labels",
            ),
            units={
                "feed_amount": "mol",
                "pressure": "Pa",
                "temperature": "K",
                "vapor_pressure": "Pa",
                "latent_heat": "J/mol",
                "heat_duty": "J",
            },
            reference_reading=(
                (
                    "IDAES: reference_repos/idaes-pse/idaes/models/unit_models/"
                    "flash.py builds a 0D flash with phase-equilibrium state "
                    "blocks, material balances, energy balances, and vapor/liquid outlets."
                ),
                (
                    "IDAES: activity_coeff_prop_pack.py _make_flash_eq defines "
                    "total/component balances and a smooth VLE flash formulation."
                ),
                (
                    "thermo: README and thermo.flash.flash_vl.FlashVL show "
                    "FlashVL objects built from constants, property correlations, "
                    "liquid/gas phases, and PT/VF flash specifications."
                ),
                (
                    "phasepy: phasepy.equilibrium.flash solves PT flash with "
                    "K-values, Rachford-Rice mass balance, accelerated "
                    "successive substitution, and Gibbs minimization fallback."
                ),
            ),
            validation_evidence=(
                ValidationEvidence(
                    evidence_id="vle-shortcut-fenske-identity",
                    evidence_type="unit_test",
                    description=(
                        "Binary and multicomponent tests verify material "
                        "balance, VLE-derived key ordering, and the analytical "
                        "Fenske distribution-ratio identity."
                    ),
                    status="implemented",
                    command_or_path="tests/test_separations.py",
                    tolerance="pytest.approx local tolerances",
                ),
            ),
            model_limit_notes=(
                "This is a professional shortcut slice for benchmark tasks, "
                "not a replacement for rigorous IDAES column MESH models.",
                "Azeotrope detection, Underwood/Gilliland sizing, tray "
                "hydraulics, pressure-drop profiles, and column costing remain open work.",
            ),
            intended_use=(
                "reaction-to-purification task kernels",
                "purity/recovery/cost tradeoff benchmark cases",
                "agent planning tasks that need interpretable VLE-coupled separation behavior",
            ),
        ),
    )


def crystallize(
    feed_amounts_mol: Mapping[str, float],
    *,
    target_component: str,
    solubility_mol_L: float,
    solvent_volume_L: float,
    crystal_growth_efficiency: float = 0.85,
    impurity_occlusion_fraction: float = 0.02,
    cooling_delta_K: float = 20.0,
) -> SeparationResult:
    feed = _amounts(feed_amounts_mol)
    if target_component not in feed:
        raise ValueError("target_component must be present in feed")
    if solubility_mol_L < 0 or solvent_volume_L <= 0:
        raise ValueError("solubility must be nonnegative and solvent volume positive")
    if not 0.0 <= crystal_growth_efficiency <= 1.0:
        raise ValueError("crystal_growth_efficiency must be between 0 and 1")
    if not 0.0 <= impurity_occlusion_fraction <= 1.0:
        raise ValueError("impurity_occlusion_fraction must be between 0 and 1")
    saturation_capacity = solubility_mol_L * solvent_volume_L
    target_crystal = max(feed[target_component] - saturation_capacity, 0.0)
    target_crystal *= crystal_growth_efficiency
    crystals = dict.fromkeys(feed, 0.0)
    mother_liquor = dict(feed)
    crystals[target_component] = target_crystal
    mother_liquor[target_component] -= target_crystal
    target_fraction = target_crystal / max(feed[target_component], 1e-12)
    for component_id, amount in feed.items():
        if component_id == target_component:
            continue
        occluded = amount * impurity_occlusion_fraction * target_fraction
        crystals[component_id] = occluded
        mother_liquor[component_id] -= occluded
    size_proxy = _clip01(crystal_growth_efficiency * (1.0 - exp(-cooling_delta_K / 25.0)))
    outlets = {"crystals": crystals, "mother_liquor": mother_liquor}
    return SeparationResult(
        operation_id="crystallization",
        outlets=outlets,
        ledger=SeparationLedger(
            unit_id="crystallization",
            cost=0.20 + 0.01 * max(cooling_delta_K, 0.0) + 0.03 * solvent_volume_L,
            risk=_clip01(0.08 + 0.15 * target_fraction + 0.01 * max(cooling_delta_K, 0.0)),
            material_balance_error_mol=_component_balance_error(feed, outlets),
            metadata={
                "saturation_capacity_mol": saturation_capacity,
                "crystal_size_proxy": size_proxy,
                "target_crystal_mol": target_crystal,
            },
        ),
    )


def filter_cake(
    slurry_amounts_mol: Mapping[str, float],
    *,
    solid_component: str,
    solid_recovery: float = 0.95,
    impurity_retention_fraction: float = 0.10,
    wash_efficiency: float = 0.0,
    solid_wash_loss_fraction: float = 0.0,
) -> SeparationResult:
    feed = _amounts(slurry_amounts_mol)
    if solid_component not in feed:
        raise ValueError("solid_component must be present in slurry")
    for name, value in {
        "solid_recovery": solid_recovery,
        "impurity_retention_fraction": impurity_retention_fraction,
        "wash_efficiency": wash_efficiency,
        "solid_wash_loss_fraction": solid_wash_loss_fraction,
    }.items():
        if not 0.0 <= value <= 1.0:
            raise ValueError(f"{name} must be between 0 and 1")
    cake = dict.fromkeys(feed, 0.0)
    filtrate = dict.fromkeys(feed, 0.0)
    solid_to_cake = feed[solid_component] * solid_recovery * (1.0 - solid_wash_loss_fraction)
    cake[solid_component] = solid_to_cake
    filtrate[solid_component] = feed[solid_component] - solid_to_cake
    impurity_retained = impurity_retention_fraction * (1.0 - wash_efficiency)
    for component_id, amount in feed.items():
        if component_id == solid_component:
            continue
        retained = amount * impurity_retained
        cake[component_id] = retained
        filtrate[component_id] = amount - retained
    outlets = {"cake": cake, "filtrate": filtrate}
    return SeparationResult(
        operation_id="filtration",
        outlets=outlets,
        ledger=SeparationLedger(
            unit_id="filtration",
            cost=0.12 + 0.25 * wash_efficiency + 0.08 * sum(feed.values()),
            risk=_clip01(0.04 + 0.12 * solid_wash_loss_fraction),
            material_balance_error_mol=_component_balance_error(feed, outlets),
            metadata={
                "solid_recovery": solid_recovery,
                "wash_efficiency": wash_efficiency,
            },
        ),
    )


def dry_solid(
    wet_cake_amounts_mol: Mapping[str, float],
    *,
    solvent_component: str,
    target_component: str,
    residual_solvent_fraction: float = 0.02,
    drying_efficiency: float = 0.95,
    temperature_K: float = 330.0,
    duration_h: float = 1.0,
    degradation_rate_per_h: float = 0.0,
    degradation_product_id: str | None = None,
) -> SeparationResult:
    feed = _amounts(wet_cake_amounts_mol)
    if solvent_component not in feed or target_component not in feed:
        raise ValueError("solvent_component and target_component must be present")
    if not 0.0 <= residual_solvent_fraction <= 1.0:
        raise ValueError("residual_solvent_fraction must be between 0 and 1")
    if not 0.0 <= drying_efficiency <= 1.0:
        raise ValueError("drying_efficiency must be between 0 and 1")
    if temperature_K <= 0 or duration_h < 0 or degradation_rate_per_h < 0:
        raise ValueError("drying temperature, duration, and degradation rate are invalid")
    dried = dict(feed)
    vapor = dict.fromkeys(feed, 0.0)
    residual_solvent = feed[solvent_component] * residual_solvent_fraction
    removable = max(feed[solvent_component] - residual_solvent, 0.0)
    removed = removable * drying_efficiency
    dried[solvent_component] -= removed
    vapor[solvent_component] = removed
    temp_factor = max(0.0, (temperature_K - 298.15) / 80.0)
    degraded = min(
        dried[target_component],
        dried[target_component] * degradation_rate_per_h * duration_h * temp_factor,
    )
    if degraded > 0.0:
        product_id = degradation_product_id or f"{target_component}_degraded"
        dried[target_component] -= degraded
        dried[product_id] = dried.get(product_id, 0.0) + degraded
    heat_duty = 40_000.0 * removed
    outlets = {"dried_solid": dried, "vapor": vapor}
    return SeparationResult(
        operation_id="drying",
        outlets=outlets,
        ledger=SeparationLedger(
            unit_id="drying",
            cost=heat_duty / 900_000.0 + 0.05 * duration_h,
            risk=_clip01(
                0.05
                + 0.25 * temp_factor
                + 0.30 * degraded / max(feed[target_component], 1e-12)
            ),
            heat_duty_J=heat_duty,
            material_balance_error_mol=_total_balance_error(feed, outlets),
            metadata={
                "removed_solvent_mol": removed,
                "degraded_target_mol": degraded,
                "residual_solvent_fraction": residual_solvent_fraction,
            },
        ),
    )


def downstream_score(
    result: SeparationResult,
    *,
    target_component: str,
    target_outlet: str,
    feed_target_mol: float,
    ignored_purity_components: Sequence[str] = (),
) -> float:
    purity = result.purity(
        target_component,
        target_outlet,
        ignored_components=ignored_purity_components,
    )
    recovery = result.recovery(target_component, target_outlet, feed_target_mol)
    penalty = 0.05 * result.ledger.cost + 0.25 * result.ledger.risk
    return _clip01(0.55 * purity + 0.45 * recovery - penalty)


def _shortcut_distillate_split(
    feed: Mapping[str, float],
    separation_factors: Mapping[str, float],
    target_distillate_mol: float,
) -> dict[str, float]:
    if target_distillate_mol <= 0.0:
        return dict.fromkeys(feed, 0.0)
    total_feed = sum(feed.values())
    if target_distillate_mol >= total_feed:
        return dict(feed)
    for component_id in feed:
        factor = float(separation_factors[component_id])
        if factor <= 0.0 or not isfinite(factor):
            raise ValueError("separation factors must be finite and positive")

    def distillate_total(theta: float) -> float:
        total = 0.0
        for component_id, amount in feed.items():
            ratio = theta * separation_factors[component_id]
            total += amount * ratio / (1.0 + ratio)
        return total

    low = 0.0
    high = 1.0
    while distillate_total(high) < target_distillate_mol:
        high *= 2.0
    for _ in range(200):
        mid = 0.5 * (low + high)
        if distillate_total(mid) < target_distillate_mol:
            low = mid
        else:
            high = mid
    theta = 0.5 * (low + high)
    return {
        component_id: amount
        * (theta * separation_factors[component_id])
        / (1.0 + theta * separation_factors[component_id])
        for component_id, amount in feed.items()
    }


def _safe_distribution_ratio(distillate_mol: float, bottoms_mol: float) -> float:
    if distillate_mol <= 0.0 and bottoms_mol <= 0.0:
        return 0.0
    if bottoms_mol <= 0.0:
        return float("inf")
    return distillate_mol / bottoms_mol


def _observed_fenske_stage_count(
    distribution_ratios: Mapping[str, float],
    relative_volatilities: Mapping[str, float],
    *,
    light_key: str,
    heavy_key: str,
) -> float | None:
    light_distribution = distribution_ratios[light_key]
    heavy_distribution = distribution_ratios[heavy_key]
    key_alpha = relative_volatilities[light_key] / relative_volatilities[heavy_key]
    if (
        light_distribution <= 0.0
        or heavy_distribution <= 0.0
        or not isfinite(light_distribution)
        or not isfinite(heavy_distribution)
        or key_alpha <= 1.0
    ):
        return None
    return log(light_distribution / heavy_distribution) / log(key_alpha)


def _flash_amount_split(
    feed: Mapping[str, float],
    k_values: Mapping[str, float],
    vapor_fraction: float,
) -> tuple[dict[str, float], dict[str, float]]:
    total = max(sum(feed.values()), 1e-12)
    vapor = {}
    liquid = {}
    for component_id, amount in feed.items():
        z_i = amount / total
        k_i = float(k_values[component_id])
        x_i = z_i / max(1.0 + vapor_fraction * (k_i - 1.0), 1e-12)
        y_i = k_i * x_i
        vapor[component_id] = vapor_fraction * total * y_i
        liquid[component_id] = (1.0 - vapor_fraction) * total * x_i
    correction = _component_balance_error(feed, {"vapor": vapor, "liquid": liquid})
    if correction > 1e-10:
        for component_id, amount in feed.items():
            current = vapor[component_id] + liquid[component_id]
            if current > 0:
                scale = amount / current
                vapor[component_id] *= scale
                liquid[component_id] *= scale
    return vapor, liquid


def _amounts(amounts: Mapping[str, float]) -> dict[str, float]:
    if not amounts:
        raise ValueError("amount mapping cannot be empty")
    if any(value < -1e-12 for value in amounts.values()):
        raise ValueError("amounts cannot be negative")
    return {component_id: max(float(amount), 0.0) for component_id, amount in amounts.items()}


def _validate_positive_mapping(
    values: Mapping[str, float],
    *,
    component_ids: Sequence[str],
    value_name: str,
) -> None:
    missing = [component_id for component_id in component_ids if component_id not in values]
    if missing:
        raise ValueError(f"{value_name} missing components: {missing}")
    for component_id in component_ids:
        value = float(values[component_id])
        if value <= 0.0 or not isfinite(value):
            raise ValueError(f"{value_name} values must be finite and positive")


def _add_amounts(left: Mapping[str, float], right: Mapping[str, float]) -> dict[str, float]:
    result = dict(left)
    for component_id, amount in right.items():
        result[component_id] = result.get(component_id, 0.0) + amount
    return result


def _component_balance_error(
    feed: Mapping[str, float],
    outlets: Mapping[str, Mapping[str, float]],
) -> float:
    component_ids = set(feed)
    for outlet in outlets.values():
        component_ids.update(outlet)
    return max(
        (
            abs(
                feed.get(component_id, 0.0)
                - sum(outlet.get(component_id, 0.0) for outlet in outlets.values())
            )
            for component_id in component_ids
        ),
        default=0.0,
    )


def _total_balance_error(
    feed: Mapping[str, float],
    outlets: Mapping[str, Mapping[str, float]],
) -> float:
    feed_total = sum(feed.values())
    outlet_total = sum(sum(outlet.values()) for outlet in outlets.values())
    return abs(feed_total - outlet_total)


def _clip01(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


__all__ = [
    "SeparationLedger",
    "SeparationResult",
    "crystallize",
    "downstream_score",
    "dry_solid",
    "evaporation_flash",
    "filter_cake",
    "liquid_liquid_extraction",
    "separation_model_cards",
    "vle_shortcut_distillation",
]
