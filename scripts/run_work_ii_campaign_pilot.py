#!/usr/bin/env python3
"""Run the seed-0 Work II electrochemical campaign with one Codex MCP session per arm."""

from __future__ import annotations

import argparse
import json
import tempfile
from collections.abc import Mapping
from pathlib import Path
from time import perf_counter
from typing import Any

from chemworld.agents.interactive_codex_experiment import InteractiveCodexExperimentAgent
from chemworld.campaign_resources import CampaignResourceCard
from chemworld.data.logging import load_jsonl
from chemworld.eval.provenance import canonical_json_sha256, write_json_atomic
from chemworld.eval.runner import run_agent
from chemworld.eval.verify import verify_records
from chemworld.tasks import get_task

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "configs/benchmark/work_ii_campaign_pilot.json"


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object")
    return value


def _checkpoint_contract(config: Mapping[str, Any], arm: str) -> dict[str, Any]:
    nominal = arm != "opaque"
    queries = [
        {"query_id": "q-low", "electrolyte_profile": 0, "solvent": 0},
        {"query_id": "q-electrolyte", "electrolyte_profile": 3, "solvent": 0},
        {"query_id": "q-solvent", "electrolyte_profile": 0, "solvent": 3},
        {"query_id": "q-high", "electrolyte_profile": 3, "solvent": 3},
    ]
    metric_ids = ["selective_product_yield", "energy_efficiency", "safety_risk"]
    feature_ids = [
        "electrolyte_profile",
        "solvent",
        "reagent_amount_mol",
        "potential_V",
        "current_mA",
        "duration_s",
    ]
    return {
        "schema_version": "chemworld-work-ii-campaign-checkpoint-contract-0.1",
        "snapshot_stages": ["pre_evidence", "post_neutral", "post_discriminating", "final"],
        "checkpoint_complete_experiments": list(
            config["campaign"]["checkpoint_complete_experiments"]
        ),
        "query_metric_contract": {row["query_id"]: metric_ids for row in queries},
        "held_out_queries": [
            {
                "query_id": row["query_id"],
                "feature_values": {
                    "electrolyte_profile": row["electrolyte_profile"],
                    "solvent": row["solvent"],
                    "reagent_amount_mol": 0.01,
                    "potential_V": 0.8,
                    "current_mA": 100.0,
                    "duration_s": 1800.0,
                },
                "metric_ids": metric_ids,
            }
            for row in queries
        ],
        "allowed_feature_ids": feature_ids,
        "allowed_metric_ids": metric_ids,
        "allowed_prior_fields": ["electrolyte_profile", "solvent"],
        "evidence_catalog": [f"experiment-{index}-final-assay" for index in range(1, 5)],
        "nominal_information_available": nominal,
        "stage_labels_are_checkpoint_ids_only": True,
        "physical_experiment_selection_authority": "participant",
    }


def _progress(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(dict(payload), ensure_ascii=False, sort_keys=True) + "\n")
    print(json.dumps(dict(payload), ensure_ascii=False, sort_keys=True), flush=True)


def _analyze(records: list[dict[str, Any]], receipts: list[dict[str, Any]]) -> dict[str, Any]:
    experiments: list[dict[str, Any]] = []
    actions: list[dict[str, Any]] = []
    for row in records:
        action = dict(row.get("action", {}))
        info = row.get("info", {}) if isinstance(row.get("info"), dict) else {}
        actions.append(action)
        if info.get("experiment_ended") is True:
            experiments.append(
                {
                    "experiment_index": len(experiments) + 1,
                    "operations": actions,
                    "leaderboard_score": info.get("leaderboard_score"),
                    "final_metrics": {
                        key: row.get("observation", {}).get(key)
                        for key in (
                            "selective_product_yield",
                            "energy_efficiency",
                            "safety_risk",
                            "score",
                        )
                    },
                }
            )
            actions = []
    snapshots = [item for receipt in receipts for item in receipt.get("belief_snapshots", [])]
    return {
        "operation_attempt_count": len(records),
        "complete_experiment_count": len(experiments),
        "right_censored_open_experiment": bool(actions),
        "experiments": experiments,
        "belief_snapshots": snapshots,
        "prior_reliability_trajectory": [
            item["prior_assessment"]["reliability_probability"] for item in snapshots
        ],
        "suspected_misindexed_fields_trajectory": [
            item["prior_assessment"]["suspected_misindexed_fields"] for item in snapshots
        ],
    }


def run(args: argparse.Namespace) -> dict[str, Any]:
    config = _load(args.config.resolve())
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    progress_path = args.progress_file.resolve()
    results: list[dict[str, Any]] = []
    arms = list(config["prior_arms"])
    started = perf_counter()
    for cell_index, arm in enumerate(arms, start=1):
        cell_started = perf_counter()
        _progress(
            progress_path,
            {"stage": "cell_started", "cell": cell_index, "total_cells": len(arms), "arm": arm},
        )
        cell_root = output / arm
        cell_root.mkdir()
        card = CampaignResourceCard(
            card_id=f"work-ii-{arm}-seed0",
            operation_attempt_limit=int(config["campaign"]["operation_attempt_limit"]),
            vessel_start_limit=int(config["campaign"]["vessel_start_limit"]),
            final_assay_limit=int(config["campaign"]["final_assay_limit"]),
            nonfinal_instrument_use_limit=int(config["campaign"]["nonfinal_instrument_use_limit"]),
            stock_limits=dict(config["campaign"]["stock_limits"]),
            metadata={"pilot_id": config["pilot_id"], "prior_arm": arm, "world_seed": 0},
        )
        provider = config["provider"]
        completed = 0
        with tempfile.TemporaryDirectory(prefix=f"chemworld-work-ii-{arm}-") as temporary:
            agent = InteractiveCodexExperimentAgent(
                workspace=Path(temporary) / "workspace",
                role_id="work_ii_wellau_sol_medium_persistent_campaign",
                model=str(provider["model"]),
                reasoning_effort=str(provider["reasoning_effort"]),
                model_provider=str(provider["id"]),
                model_provider_name=str(provider["name"]),
                model_provider_base_url=str(provider["base_url"]),
                model_provider_env_key=str(provider["env_key"]),
                model_provider_wire_api=str(provider["wire_api"]),
                request_timeout_s=float(provider["request_timeout_s"]),
                finalization_timeout_s=float(provider["finalization_timeout_s"]),
                pre_action_restart_limit=0,
                session_scope="campaign",
                belief_checkpoint_contract=_checkpoint_contract(config, arm),
            )

            def on_step(
                record: Any,
                trace: list[dict[str, Any]],
                *,
                active_cell: int = cell_index,
                active_arm: str = arm,
                active_started: float = cell_started,
            ) -> None:
                nonlocal completed
                del trace
                if record.event_type in {"experiment_end", "batch_discard"}:
                    completed += 1
                resources = record.info.get("campaign_resources", {})
                _progress(
                    progress_path,
                    {
                        "stage": "operation",
                        "cell": active_cell,
                        "total_cells": len(arms),
                        "arm": active_arm,
                        "operation": record.action.get("operation"),
                        "instrument": record.action.get("instrument"),
                        "transaction_status": record.info.get("transaction_status"),
                        "step": record.step,
                        "complete_experiments": completed,
                        "target_experiments": 4,
                        "remaining_resources": resources.get("state", {}).get("remaining"),
                        "elapsed_s": round(perf_counter() - active_started, 1),
                    },
                )

            history = run_agent(
                env_id=get_task(config["task_id"]).env_id,
                agent=agent,
                world_split=config["world_split"],
                budget=int(config["method_resources"]["operation_limit"]),
                objective=config["objective"],
                seed=0,
                agent_seed=0,
                task_id=config["task_id"],
                output_path=cell_root / "trajectory.jsonl",
                budget_override=int(config["method_resources"]["operation_limit"]),
                episode_mode_override=config["episode_mode"],
                step_callback=on_step,
                method_resource_limits=dict(config["method_resources"]),
                material_information=dict(config["prior_arms"][arm]),
                campaign_resource_card=card,
                electrochemical_material_family_id=config["electrochemical_material_family_id"],
                electrochemical_workflow_mode=config["electrochemical_workflow_mode"],
                scoring_contract_id=config["scoring_contract_id"],
                observation_noise_mode=config["observation_noise_mode"],
                observation_noise_namespace=f"{config['observation_noise_namespace']}--{arm}",
            )
            del history
            receipts = agent.provider_receipts()
            usage = agent.method_resource_usage()
        records = load_jsonl(cell_root / "trajectory.jsonl")
        analysis = _analyze(records, receipts)
        replay = verify_records(records, tolerance=0.0).to_dict()
        row = {
            "arm": arm,
            "completed": analysis["complete_experiment_count"] == 4
            and not analysis["right_censored_open_experiment"],
            "analysis": analysis,
            "method_resources": usage,
            "provider_receipts": receipts,
            "exact_replay": replay,
            "elapsed_s": round(perf_counter() - cell_started, 1),
        }
        write_json_atomic(cell_root / "summary.json", row)
        results.append(row)
        _progress(
            progress_path,
            {
                "stage": "cell_completed",
                "cell": cell_index,
                "total_cells": len(arms),
                "arm": arm,
                "completed": row["completed"],
                "elapsed_s": row["elapsed_s"],
            },
        )
    report = {
        "schema_version": "chemworld-work-ii-campaign-pilot-report-0.1",
        "pilot_id": config["pilot_id"],
        "formal_result": False,
        "config_sha256": canonical_json_sha256(config),
        "world_seed": 0,
        "cell_count": len(results),
        "completed_cell_count": sum(row["completed"] for row in results),
        "elapsed_s": round(perf_counter() - started, 1),
        "results": results,
    }
    write_json_atomic(output / "report.json", report)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--progress-file", type=Path, required=True)
    args = parser.parse_args()
    report = run(args)
    print(
        json.dumps(
            {
                "completed_cells": report["completed_cell_count"],
                "cell_count": report["cell_count"],
                "output": str(args.output),
            },
            ensure_ascii=False,
        ),
        flush=True,
    )
    return 0 if report["completed_cell_count"] == report["cell_count"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
