"""Separation and downstream unit-operation kernels for ChemWorld."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from math import exp, log1p

from chemworld.physchem.equilibrium import flash_isothermal, liquid_liquid_split


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


def simple_distillation(
    feed_amounts_mol: Mapping[str, float],
    *,
    volatility_scores: Mapping[str, float],
    distillate_cut_fraction: float,
    reflux_ratio: float = 1.0,
    stage_efficiency: float = 1.0,
) -> SeparationResult:
    feed = _amounts(feed_amounts_mol)
    if not 0.0 <= distillate_cut_fraction <= 1.0:
        raise ValueError("distillate_cut_fraction must be between 0 and 1")
    if reflux_ratio < 0:
        raise ValueError("reflux_ratio cannot be negative")
    if not 0.0 <= stage_efficiency <= 1.0:
        raise ValueError("stage_efficiency must be between 0 and 1")
    selectivity_power = max(0.1, stage_efficiency * (1.0 + log1p(reflux_ratio)))
    weights = {
        component_id: amount * max(float(volatility_scores.get(component_id, 1.0)), 1e-12)
        ** selectivity_power
        for component_id, amount in feed.items()
    }
    target_distillate = sum(feed.values()) * distillate_cut_fraction
    total_weight = max(sum(weights.values()), 1e-12)
    distillate = {
        component_id: min(
            feed[component_id],
            target_distillate * weights[component_id] / total_weight,
        )
        for component_id in feed
    }
    bottoms = {component_id: feed[component_id] - distillate[component_id] for component_id in feed}
    heat_duty = 28_000.0 * sum(distillate.values()) * (1.0 + 0.35 * reflux_ratio)
    outlets = {"distillate": distillate, "bottoms": bottoms}
    return SeparationResult(
        operation_id="simple_distillation",
        outlets=outlets,
        ledger=SeparationLedger(
            unit_id="simple_distillation",
            cost=heat_duty / 800_000.0 + 0.10 * reflux_ratio,
            risk=_clip01(0.12 + 0.08 * reflux_ratio + 0.25 * distillate_cut_fraction),
            heat_duty_J=heat_duty,
            material_balance_error_mol=_component_balance_error(feed, outlets),
            metadata={
                "distillate_cut_fraction": distillate_cut_fraction,
                "reflux_ratio": reflux_ratio,
                "selectivity_power": selectivity_power,
            },
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
    "simple_distillation",
]
