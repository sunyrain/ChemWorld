#!/usr/bin/env python3
"""Run one Work II electrochemical world with one Codex session per prior arm."""

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


def _campaign_card(config: Mapping[str, Any]) -> CampaignResourceCard:
    campaign = config["campaign"]
    return CampaignResourceCard(
        card_id="work-ii-electrochemical-k4",
        operation_attempt_limit=int(campaign["operation_attempt_limit"]),
        vessel_start_limit=int(campaign["vessel_start_limit"]),
        final_assay_limit=int(campaign["final_assay_limit"]),
        nonfinal_instrument_use_limit=int(campaign["nonfinal_instrument_use_limit"]),
        stock_limits=dict(campaign["stock_limits"]),
        process_time_limit_s=float(campaign["process_time_limit_s"]),
        operation_repeat_limits=dict(campaign["operation_repeat_limits"]),
        metadata={
            "pilot_id": config["pilot_id"],
            "process_time_policy": dict(campaign["process_time_policy"]),
            "scope": "one_task_prior_world_cell",
        },
    )


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
        actions.append(action)
        is_final_assay = (
            row.get("transaction_status") == "committed"
            and row.get("operation_type") == "measure"
            and row.get("instrument") == "final_assay"
        )
        if is_final_assay:
            experiments.append(
                {
                    "experiment_index": len(experiments) + 1,
                    "operations": actions,
                    "leaderboard_score": row.get("leaderboard_score"),
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
    resource_rejection_count = sum(
        1 for row in records if row.get("transaction_status") == "campaign_resource_rejected"
    )
    final_campaign_resources: dict[str, Any] = {}
    if records:
        last_view = records[-1].get("agent_view", {})
        if isinstance(last_view, Mapping):
            tool_json = last_view.get("tool_json", {})
            if isinstance(tool_json, Mapping):
                campaign_state = tool_json.get("campaign_state", {})
                if isinstance(campaign_state, Mapping):
                    candidate = campaign_state.get("campaign_resources", {})
                    if isinstance(candidate, Mapping):
                        final_campaign_resources = dict(candidate)
    return {
        "operation_attempt_count": len(records),
        "complete_experiment_count": len(experiments),
        "right_censored_open_experiment": bool(actions),
        "experiments": experiments,
        "belief_snapshots": snapshots,
        "resource_rejection_count": resource_rejection_count,
        "final_campaign_resources": final_campaign_resources,
        "prior_reliability_trajectory": [
            item["prior_assessment"]["reliability_probability"] for item in snapshots
        ],
        "suspected_misindexed_fields_trajectory": [
            item["prior_assessment"]["suspected_misindexed_fields"] for item in snapshots
        ],
    }


def _qualification(
    *,
    analysis: Mapping[str, Any],
    exact_replay: Mapping[str, Any],
    method_resources: Mapping[str, Any],
    method_resource_limits: Mapping[str, Any],
    receipts: list[dict[str, Any]],
    process_time_limit_s: float,
) -> dict[str, Any]:
    """Apply the frozen per-cell qualification contract fail-closed."""

    receipt = receipts[0] if len(receipts) == 1 else {}
    usage = method_resources
    limits = method_resource_limits
    resources = analysis.get("final_campaign_resources", {})
    resources = resources if isinstance(resources, Mapping) else {}
    state = resources.get("state", {})
    state = state if isinstance(state, Mapping) else {}
    report_only = state.get("report_only", {})
    report_only = report_only if isinstance(report_only, Mapping) else {}
    operation_counts = state.get("operation_committed_counts", {})
    operation_counts = operation_counts if isinstance(operation_counts, Mapping) else {}
    snapshots = analysis.get("belief_snapshots", [])
    snapshots = snapshots if isinstance(snapshots, list) else []
    stages = [item.get("stage") for item in snapshots if isinstance(item, Mapping)]
    checks = {
        "four_complete_experiments": analysis.get("complete_experiment_count") == 4
        and analysis.get("right_censored_open_experiment") is False,
        "four_typed_belief_checkpoints": len(snapshots) == 4
        and stages == ["pre_evidence", "post_neutral", "post_discriminating", "final"],
        "one_campaign_session": len(receipts) == 1
        and method_resources.get("provider_session_count") == 1
        and receipt.get("session_scope") == "campaign",
        "provider_session_completed": receipt.get("status") == "completed"
        and receipt.get("return_code") == 0
        and receipt.get("final_payload_valid") is True
        and receipt.get("final_payload_status") == "campaign_complete",
        "tool_integrity": receipt.get("experiment_tool_integrity_verified_after_session") is True
        and receipt.get("lab_tool_integrity_verified_after_session") is True
        and receipt.get("mcp_tool_integrity_verified_after_session") is True,
        "no_resource_rejection": analysis.get("resource_rejection_count") == 0,
        "campaign_terminal": resources.get("campaign_terminal") is True
        and state.get("closed_batches") == 4
        and state.get("final_assays") == 4,
        "process_time_reconciled": "process_time_s" in report_only
        and float(report_only.get("process_time_s", 0.0)) <= process_time_limit_s,
        "electrolyze_repeat_reconciled": 4 <= int(operation_counts.get("electrolyze", -1)) <= 5,
        "exact_replay": exact_replay.get("verified") is True,
        "provider_usage_reconciled": method_resources.get("provider_usage_pending") is False
        and method_resources.get("provider_usage_accounting_complete") is True
        and usage.get("in_flight_model_call_count") == 0
        and int(usage.get("input_token_count", 0)) <= int(limits.get("input_token_limit", 0))
        and int(usage.get("uncached_input_token_count", 0))
        <= int(limits.get("uncached_input_token_limit", 0))
        and int(usage.get("output_token_count", 0)) <= int(limits.get("output_token_limit", 0)),
    }
    return {
        "passed": all(checks.values()),
        "checks": checks,
        "failed_checks": [name for name, passed in checks.items() if not passed],
    }


def _run_cell(
    *,
    config: Mapping[str, Any],
    world_seed: int,
    arm: str,
    cell_index: int,
    total_cells: int,
    cell_root: Path,
    progress_path: Path,
) -> dict[str, Any]:
    cell_started = perf_counter()
    _progress(
        progress_path,
        {
            "stage": "cell_started",
            "world_seed": world_seed,
            "cell": cell_index,
            "total_cells": total_cells,
            "arm": arm,
        },
    )
    cell_root.mkdir(parents=True, exist_ok=False)
    card = _campaign_card(config)
    provider = config["provider"]
    completed = 0
    failure: dict[str, str] | None = None
    with tempfile.TemporaryDirectory(prefix="chemworld-work-ii-cell-") as temporary:
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

        def on_step(record: Any, trace: list[dict[str, Any]]) -> None:
            nonlocal completed
            del trace
            if record.event_type in {"experiment_end", "batch_discard"}:
                completed += 1
            resources = record.info.get("campaign_resources", {})
            _progress(
                progress_path,
                {
                    "stage": "operation",
                    "world_seed": world_seed,
                    "cell": cell_index,
                    "total_cells": total_cells,
                    "arm": arm,
                    "operation": record.action.get("operation"),
                    "instrument": record.action.get("instrument"),
                    "transaction_status": record.info.get("transaction_status"),
                    "step": record.step,
                    "complete_experiments": completed,
                    "target_experiments": 4,
                    "remaining_resources": resources.get("state", {}).get("remaining"),
                    "elapsed_s": round(perf_counter() - cell_started, 1),
                },
            )

        try:
            history = run_agent(
                env_id=get_task(config["task_id"]).env_id,
                agent=agent,
                world_split=config["world_split"],
                budget=int(config["method_resources"]["operation_limit"]),
                objective=config["objective"],
                seed=world_seed,
                agent_seed=0,
                observation_seed=world_seed,
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
                observation_noise_namespace=(
                    f"{config['observation_noise_namespace']}--seed{world_seed}"
                ),
            )
            del history
        except Exception as error:  # preserve the failed cell and stop the next seed block
            failure = {"type": type(error).__name__, "message": str(error)[:1000]}
        receipts = agent.provider_receipts()
        usage = agent.method_resource_usage()
    trajectory_path = cell_root / "trajectory.jsonl"
    records = load_jsonl(trajectory_path) if trajectory_path.exists() else []
    analysis = _analyze(records, receipts)
    replay = (
        verify_records(records, tolerance=0.0).to_dict()
        if records
        else {"verified": False, "checked_steps": 0, "max_abs_error": None, "mismatches": []}
    )
    qualification = _qualification(
        analysis=analysis,
        exact_replay=replay,
        method_resources=usage,
        method_resource_limits=config["method_resources"],
        receipts=receipts,
        process_time_limit_s=float(config["campaign"]["process_time_limit_s"]),
    )
    row = {
        "arm": arm,
        "completed": failure is None and qualification["passed"],
        "failure": failure,
        "analysis": analysis,
        "method_resources": usage,
        "provider_receipts": receipts,
        "exact_replay": replay,
        "qualification": qualification,
        "elapsed_s": round(perf_counter() - cell_started, 1),
    }
    write_json_atomic(cell_root / "summary.json", row)
    _progress(
        progress_path,
        {
            "stage": "cell_completed",
            "world_seed": world_seed,
            "cell": cell_index,
            "total_cells": total_cells,
            "arm": arm,
            "completed": row["completed"],
            "complete_experiments": analysis["complete_experiment_count"],
            "target_experiments": 4,
            "qualification_failed_checks": qualification["failed_checks"],
            "elapsed_s": row["elapsed_s"],
        },
    )
    return row


def run(args: argparse.Namespace) -> dict[str, Any]:
    config = _load(args.config.resolve())
    world_seed = int(args.world_seed if args.world_seed is not None else config["world_seed"])
    output = args.output.resolve()
    progress_path = args.progress_file.resolve()
    all_arms = list(config["prior_arms"])
    if args.prior_arm is not None:
        if args.prior_arm not in all_arms:
            raise ValueError(f"unknown prior arm: {args.prior_arm}")
        output.parent.mkdir(parents=True, exist_ok=True)
        arms = [args.prior_arm]
    else:
        output.mkdir(parents=True, exist_ok=False)
        arms = all_arms
    results: list[dict[str, Any]] = []
    started = perf_counter()
    for arm in arms:
        cell_index = all_arms.index(arm) + 1
        cell_root = output if args.prior_arm is not None else output / arm
        row = _run_cell(
            config=config,
            world_seed=world_seed,
            arm=arm,
            cell_index=cell_index,
            total_cells=len(all_arms),
            cell_root=cell_root,
            progress_path=progress_path,
        )
        results.append(row)
        if not row["completed"]:
            break
    report = {
        "schema_version": "chemworld-work-ii-campaign-pilot-report-0.1",
        "pilot_id": config["pilot_id"],
        "cell_id": f"{config['pilot_id']}--seed{world_seed}",
        "formal_result": False,
        "config_sha256": canonical_json_sha256(config),
        "world_seed": world_seed,
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
    parser.add_argument("--world-seed", type=int)
    parser.add_argument("--prior-arm")
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
