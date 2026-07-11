"""Audit the World Law v0.4 provider graph and real operation execution paths."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import gymnasium as gym

import chemworld  # noqa: F401
from chemworld.foundation import equipment_settings
from chemworld.runtime.model_reachability import (
    audit_model_reachability,
    default_model_reachability_registry,
)
from chemworld.tasks import list_tasks
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
    "mix": ("chemworld_stability_aware_lle_vnext",),
    "wash": ("chemworld_stability_aware_lle_vnext",),
    "dry": ("chemworld_sorbent_drying_vnext",),
    "concentrate": ("chemworld_vacuum_concentration_vnext",),
    "transfer": ("chemworld_transfer_holdup_vnext",),
    "distill": ("chemworld_duty_limited_distillation_vnext",),
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
    equipment = {
        "dry": equipment_settings(purification_state.equipment, "sorbent_dryer"),
        "concentrate": equipment_settings(
            purification_state.equipment, "vacuum_concentrator"
        ),
        "transfer": equipment_settings(purification_state.equipment, "transfer_line"),
        "distill": equipment_settings(
            distillation_state.equipment, "distillation_column"
        ),
    }
    model_ids = {
        "mix": purification_state.metadata.get("extraction_model_id"),
        "wash": purification_state.metadata.get("wash_model_id"),
        "dry": equipment["dry"].get("drying_model_id"),
        "concentrate": equipment["concentrate"].get("concentration_model_id"),
        "transfer": equipment["transfer"].get("transfer_model_id"),
        "distill": equipment["distill"].get("distillation_model"),
    }
    return {
        "passed": all(status == "committed" for status in purification_statuses)
        and all(status == "committed" for status in distillation_statuses)
        and model_ids
        == {operation: models[0] for operation, models in EXPECTED_OPERATION_MODELS.items()},
        "model_ids": model_ids,
        "purification_transaction_statuses": purification_statuses,
        "distillation_transaction_statuses": distillation_statuses,
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
