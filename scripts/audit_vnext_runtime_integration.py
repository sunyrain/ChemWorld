"""Audit the World Law v0.4 provider graph and real operation execution paths."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import gymnasium as gym

import chemworld  # noqa: F401
from chemworld.foundation import equipment_settings, instrument_equipment_id
from chemworld.runtime.model_reachability import (
    audit_model_reachability,
    default_model_reachability_registry,
)
from chemworld.tasks import list_tasks
from chemworld.world.instruments import INSTRUMENT_RUNTIME_MODEL_ID
from chemworld.world.parameters import WORLD_FAMILY_VERSION

SCHEMA_VERSION = "chemworld-vnext-runtime-integration-audit-0.1"
EXPECTED_WORLD_LAW = "chemworld-physical-chemistry-v0.4"
RETIRED_ROUTE_MODEL_IDS = frozenset(
    {
        "chemworld_separation_proxy",
        "activity_corrected_extraction_train_v1",
        "lle_phase_stability_diagnostic_v1",
        "vle_shortcut_distillation",
    }
)
EXPECTED_OPERATION_MODELS = {
    "heat": (
        "reaction_ode_mass_action_arrhenius_reference_slice",
        "dynamic_batch_heat_release_jacket_sampling",
    ),
    "wait": (
        "reaction_ode_mass_action_arrhenius_reference_slice",
        "dynamic_batch_heat_release_jacket_sampling",
    ),
    "mix": ("chemworld_stability_aware_lle_vnext",),
    "wash": ("chemworld_stability_aware_lle_vnext",),
    "dry": ("chemworld_sorbent_drying_vnext",),
    "concentrate": ("chemworld_vacuum_concentration_vnext",),
    "transfer": ("chemworld_transfer_holdup_vnext",),
    "cool_crystallize": ("cooling_crystallization_population_balance_v1",),
    "distill": ("chemworld_duty_limited_distillation_vnext",),
    "electrolyze": (
        "nernst_butler_volmer_faradaic_v1",
        "diffusion_layer_limiting_current_v1",
        "randles_double_layer_transient_v1",
        "aqueous_acid_base_ph_observation",
    ),
    "measure": (INSTRUMENT_RUNTIME_MODEL_ID,),
}


@dataclass(frozen=True)
class AuditCheck:
    check_id: str
    passed: bool
    evidence: Any

    def to_dict(self) -> dict[str, Any]:
        return {
            "check_id": self.check_id,
            "passed": self.passed,
            "evidence": self.evidence,
        }


def _run_actions(task_id: str, actions: tuple[dict[str, Any], ...]) -> tuple[Any, list[str]]:
    task = next(task for task in list_tasks() if task.task_id == task_id)
    env = gym.make("ChemWorld", task_id=task_id, seed=task.seeds[0])
    statuses: list[str] = []
    try:
        env.reset(seed=task.seeds[0])
        for action in actions:
            _, _, _, _, info = env.step(action)
            statuses.append(str(info["transaction_status"]))
        return env.unwrapped._state, statuses  # type: ignore[attr-defined]
    finally:
        env.close()


def _execution_probe() -> dict[str, Any]:
    reaction = (
        {"operation": "add_solvent", "volume_L": 0.028, "solvent": 2},
        {"operation": "add_reagent", "amount_mol": 0.010},
        {
            "operation": "add_catalyst",
            "catalyst_amount_mol": 0.00025,
            "catalyst": 1,
        },
        {
            "operation": "heat",
            "target_temperature_K": 385.0,
            "duration_s": 1500.0,
            "stirring_speed_rpm": 720.0,
        },
        {"operation": "wait", "duration_s": 900.0, "stirring_speed_rpm": 720.0},
    )
    purification = (
        *reaction,
        {"operation": "quench"},
        {"operation": "add_phase", "phase": "aqueous", "volume_L": 0.012},
        {
            "operation": "add_extractant",
            "extractant": "organic",
            "volume_L": 0.018,
        },
        {"operation": "mix", "duration_s": 240.0, "stirring_speed_rpm": 850.0},
        {"operation": "settle", "duration_s": 420.0},
        {"operation": "separate_phase", "target_phase": "organic"},
        {"operation": "wash", "wash_volume_L": 0.008},
        {"operation": "dry"},
        {"operation": "concentrate", "duration_s": 600.0},
        {"operation": "transfer", "transfer_fraction": 0.97},
    )
    purification_state, purification_statuses = _run_actions(
        "reaction-to-purification", purification
    )
    distillation_state, distillation_statuses = _run_actions(
        "reaction-to-distillation",
        (
            *reaction,
            {"operation": "evaporate", "target_temperature_K": 335.0, "duration_s": 600.0},
            {
                "operation": "distill",
                "target_temperature_K": 360.0,
                "duration_s": 1500.0,
                "reflux_ratio": 2.0,
            },
        ),
    )
    assay_state, assay_statuses = _run_actions(
        "reaction-to-assay",
        (
            {"operation": "add_solvent", "volume_L": 0.026, "solvent": 2},
            {"operation": "add_reagent", "amount_mol": 0.010},
            {"operation": "measure", "instrument": "uvvis"},
            {"operation": "measure", "instrument": "hplc"},
            {"operation": "measure", "instrument": "gc"},
            {"operation": "terminate"},
            {"operation": "measure", "instrument": "final_assay"},
        ),
    )
    ph_state, ph_statuses = _run_actions(
        "equilibrium-characterization",
        (
            {"operation": "add_solvent", "volume_L": 0.026, "solvent": 1},
            {"operation": "add_reagent", "amount_mol": 0.010},
            {"operation": "measure", "instrument": "ph_meter"},
        ),
    )
    electro_state, electro_statuses = _run_actions(
        "electrochemical-conversion",
        (
            {"operation": "add_solvent", "volume_L": 0.026, "solvent": 1},
            {"operation": "add_reagent", "amount_mol": 0.010},
            {"operation": "set_potential", "potential_V": 1.15, "current_mA": 75.0},
            {"operation": "electrolyze", "duration_s": 1800.0},
        ),
    )
    crystallization_state, crystallization_statuses = _run_actions(
        "reaction-to-crystallization",
        (
            *reaction,
            {"operation": "seed_crystals", "seed_mass_g": 0.006},
            {
                "operation": "cool_crystallize",
                "target_temperature_K": 278.15,
                "duration_s": 1800.0,
            },
        ),
    )
    instrument_settings = {
        instrument_id: equipment_settings(
            (ph_state if instrument_id == "ph_meter" else assay_state).equipment,
            instrument_equipment_id(instrument_id),
        )
        for instrument_id in ("uvvis", "hplc", "gc", "ph_meter", "final_assay")
    }
    equipment = {
        "reaction_reactor": equipment_settings(
            purification_state.equipment, "batch_reactor"
        ),
        "dry": equipment_settings(purification_state.equipment, "sorbent_dryer"),
        "concentrate": equipment_settings(
            purification_state.equipment, "vacuum_concentrator"
        ),
        "transfer": equipment_settings(purification_state.equipment, "transfer_line"),
        "distill": equipment_settings(
            distillation_state.equipment, "distillation_column"
        ),
        "instruments": instrument_settings,
        "electrochem": equipment_settings(
            electro_state.equipment, "electrochemical_cell"
        ),
        "crystallization": equipment_settings(
            crystallization_state.equipment, "crystallizer"
        ),
    }
    model_ids = {
        "heat": [
            equipment["reaction_reactor"].get("reaction_model_id"),
            equipment["reaction_reactor"].get("reactor_model_id"),
        ],
        "wait": [
            equipment["reaction_reactor"].get("reaction_model_id"),
            equipment["reaction_reactor"].get("reactor_model_id"),
        ],
        "mix": purification_state.metadata.get("extraction_model_id"),
        "wash": purification_state.metadata.get("wash_model_id"),
        "dry": equipment["dry"].get("drying_model_id"),
        "concentrate": equipment["concentrate"].get("concentration_model_id"),
        "transfer": equipment["transfer"].get("transfer_model_id"),
        "cool_crystallize": equipment["crystallization"].get(
            "crystallization_model_id"
        ),
        "distill": equipment["distill"].get("distillation_model"),
        "electrolyze": list(equipment["electrochem"].get("runtime_model_ids", ())),
        "measure": instrument_settings["uvvis"].get("model_id"),
    }
    instrument_model_ids = {
        "uvvis": [INSTRUMENT_RUNTIME_MODEL_ID, "beer_lambert_uvvis"],
        "hplc": [INSTRUMENT_RUNTIME_MODEL_ID, "chromatography_retention_plate"],
        "gc": [INSTRUMENT_RUNTIME_MODEL_ID, "chromatography_retention_plate"],
        "ph_meter": [
            INSTRUMENT_RUNTIME_MODEL_ID,
            "aqueous_acid_base_ph_observation",
            "potentiometric_ph_public_reference",
        ],
        "final_assay": [INSTRUMENT_RUNTIME_MODEL_ID],
    }
    expected_execution_model_ids = {
        operation: models[0] if len(models) == 1 else list(models)
        for operation, models in EXPECTED_OPERATION_MODELS.items()
    }
    return {
        "passed": all(status == "committed" for status in purification_statuses)
        and all(status == "committed" for status in distillation_statuses)
        and all(status == "committed" for status in assay_statuses)
        and all(status == "committed" for status in ph_statuses)
        and all(status == "committed" for status in electro_statuses)
        and all(status == "committed" for status in crystallization_statuses)
        and model_ids
        == expected_execution_model_ids
        and all(
            settings.get("model_id") == INSTRUMENT_RUNTIME_MODEL_ID
            and settings.get("provider_path")
            and settings.get("execution_history")
            for settings in instrument_settings.values()
        ),
        "model_ids": model_ids,
        "instrument_model_ids": instrument_model_ids,
        "purification_transaction_statuses": purification_statuses,
        "distillation_transaction_statuses": distillation_statuses,
        "instrument_transaction_statuses": {
            "assay": assay_statuses,
            "ph": ph_statuses,
        },
        "electrochemical_transaction_statuses": electro_statuses,
        "crystallization_transaction_statuses": crystallization_statuses,
        "typed_inventory_phases": sorted(purification_state.phases.phases),
        "provider_diagnostics": equipment,
    }


def build_audit() -> dict[str, Any]:
    registry = default_model_reachability_registry()
    provider_ids = {provider.model_id for provider in registry.providers.providers}
    routes = {
        operation: registry.route_for_operation(operation).model_ids
        for operation in EXPECTED_OPERATION_MODELS
    }
    reachability = audit_model_reachability()
    execution = _execution_probe()
    checks = (
        AuditCheck(
            "world_law_advanced",
            WORLD_FAMILY_VERSION == EXPECTED_WORLD_LAW,
            WORLD_FAMILY_VERSION,
        ),
        AuditCheck(
            "single_declared_runtime_routes",
            routes == EXPECTED_OPERATION_MODELS,
            {key: list(value) for key, value in routes.items()},
        ),
        AuditCheck(
            "retired_routes_absent",
            not RETIRED_ROUTE_MODEL_IDS.intersection(provider_ids),
            sorted(RETIRED_ROUTE_MODEL_IDS.intersection(provider_ids)),
        ),
        AuditCheck(
            "no_runtime_fallback_provider",
            all(
                provider.role.value != "runtime_fallback"
                for provider in registry.providers.providers
            ),
            sorted(
                provider.model_id
                for provider in registry.providers.providers
                if provider.role.value == "runtime_fallback"
            ),
        ),
        AuditCheck(
            "task_route_declarations_aligned",
            reachability["contract_integrity_passed"]
            and reachability["declaration_gap_count"] == 0,
            {
                "provider_count": reachability["provider_count"],
                "route_count": reachability["route_count"],
                "task_count": reachability["task_count"],
                "gap_count": reachability["declaration_gap_count"],
            },
        ),
        AuditCheck("providers_execute_in_transactions", execution["passed"], execution),
    )
    return {
        "schema_version": SCHEMA_VERSION,
        "world_law_id": WORLD_FAMILY_VERSION,
        "passed": all(check.passed for check in checks),
        "check_count": len(checks),
        "checks": [check.to_dict() for check in checks],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("workstreams/world_foundation/reports/wf-110-runtime-integration.json"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(__file__).resolve().parents[1]
    report = build_audit()
    output = args.output if args.output.is_absolute() else root / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output), **report}, indent=2, sort_keys=True))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
