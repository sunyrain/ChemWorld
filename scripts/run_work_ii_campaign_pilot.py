#!/usr/bin/env python3
"""Run one Work II electrochemical world with one Codex session per prior arm."""

from __future__ import annotations

import argparse
import contextlib
import json
import tempfile
from collections.abc import Mapping
from pathlib import Path
from time import perf_counter
from typing import Any, cast

from chemworld.agents.interactive_codex_experiment import (
    InteractiveCodexExperimentAgent,
    ProviderAuthMode,
)
from chemworld.campaign_resources import CampaignResourceCard
from chemworld.data.logging import load_jsonl
from chemworld.eval.provenance import canonical_json_sha256, file_sha256, write_json_atomic
from chemworld.eval.runner import run_agent
from chemworld.eval.verify import verify_records
from chemworld.eval.work_ii_blind import (
    build_blind_evaluation_plan,
    validate_blind_evaluation_plan,
)
from chemworld.eval.work_ii_cost import validate_qualification_cost_ledger
from chemworld.eval.work_ii_formal import (
    build_checkpoint_contract as _checkpoint_contract,
)
from chemworld.eval.work_ii_formal import (
    build_formal_preflight,
    validate_formal_bindings,
    validate_formal_preflight,
)
from chemworld.eval.work_ii_process_profile import (
    build_work_ii_execution_artifacts,
)
from chemworld.eval.work_ii_qualification import (
    METHOD_QUALIFICATION_REPORT_VERSION,
    REQUIRED_CELL_QUALIFICATION_CHECKS,
    method_qualification_report_sha256,
    validate_qualification_attempt_authorization,
    validate_qualification_execution_authorization,
)
from chemworld.tasks import get_task

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "configs/benchmark/work_ii_campaign_pilot.json"
DEFAULT_DESIGN = ROOT / "configs/benchmark/work_ii_formal_design_v0.1.json"
DEFAULT_ANALYSIS = ROOT / "configs/benchmark/work_ii_analysis_plan_v0.1.json"


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object")
    return value


def _resolve_optional_path(value: Any) -> str | None:
    if value is None:
        return None
    path = Path(str(value))
    if not path.is_absolute():
        path = ROOT / path
    return str(path.resolve())


def _arm_contract(config: Mapping[str, Any], arm: str) -> Mapping[str, Any]:
    value = config["prior_arms"][arm]
    if not isinstance(value, Mapping):
        raise ValueError(f"prior_arms.{arm} must be an object")
    return value


def _arm_material_information(config: Mapping[str, Any], arm: str) -> dict[str, Any]:
    contract = _arm_contract(config, arm)
    value = contract.get("material_information", contract)
    if not isinstance(value, Mapping):
        raise ValueError(f"prior_arms.{arm}.material_information must be an object")
    return dict(value)


def _arm_initial_world_model(
    config: Mapping[str, Any], arm: str
) -> dict[str, Any] | None:
    value = _arm_contract(config, arm).get("initial_world_model")
    if value is None:
        return None
    if not isinstance(value, Mapping):
        raise ValueError(f"prior_arms.{arm}.initial_world_model must be an object")
    return dict(value)


def _campaign_card(config: Mapping[str, Any]) -> CampaignResourceCard:
    campaign = config["campaign"]
    return CampaignResourceCard(
        card_id=str(campaign.get("card_id", f"work-ii-{config['task_id']}-k4")),
        operation_attempt_limit=int(campaign["operation_attempt_limit"]),
        vessel_start_limit=int(campaign["vessel_start_limit"]),
        final_assay_limit=int(campaign["final_assay_limit"]),
        nonfinal_instrument_use_limit=int(campaign["nonfinal_instrument_use_limit"]),
        stock_limits=dict(campaign["stock_limits"]),
        process_time_limit_s=float(campaign["process_time_limit_s"]),
        implicit_operation_time_s=dict(campaign.get("implicit_operation_time_s", {})),
        operation_repeat_limits=dict(campaign["operation_repeat_limits"]),
        metadata={
            "pilot_id": config["pilot_id"],
            "task_id": config["task_id"],
            "process_time_policy": dict(campaign["process_time_policy"]),
            "closeout_policy": dict(campaign["closeout_policy"]),
            "scope": "one_task_prior_world_cell",
        },
    )


def _world_interventions(config: Mapping[str, Any]) -> list[dict[str, Any]]:
    value = config.get("world_interventions", [])
    if not isinstance(value, list):
        raise ValueError("world_interventions must be a list")
    interventions = []
    for index, item in enumerate(value):
        if not isinstance(item, Mapping):
            raise ValueError(f"world_interventions[{index}] must be an object")
        interventions.append(dict(item))
    return interventions


def _formal_cell_context(
    args: argparse.Namespace,
    *,
    config_path: Path,
) -> tuple[dict[str, Any], dict[str, Any]] | None:
    manifest_path = getattr(args, "formal_manifest", None)
    cell_key = getattr(args, "formal_cell_key", None)
    allow = bool(getattr(args, "allow_formal_execution", False))
    supplied = (manifest_path is not None, cell_key is not None, allow)
    if not any(supplied):
        return None
    if not all(supplied):
        raise RuntimeError(
            "formal cell execution requires --formal-manifest, --formal-cell-key, "
            "and --allow-formal-execution together"
        )
    manifest = _load(Path(manifest_path).resolve())
    manifest_errors = validate_formal_preflight(manifest)
    if manifest_errors:
        raise RuntimeError("formal manifest validation failed: " + "; ".join(manifest_errors))
    errors = validate_formal_bindings(ROOT, manifest)
    if errors:
        raise RuntimeError("formal manifest binding validation failed: " + "; ".join(errors))
    if manifest.get("formal_execution_allowed") is not True:
        raise RuntimeError("formal manifest does not authorize participant execution")
    if manifest.get("blocking_requirements"):
        raise RuntimeError("formal manifest still contains blocking requirements")
    matches = [
        dict(cell)
        for cell in manifest.get("cells", [])
        if isinstance(cell, Mapping) and cell.get("cell_key_sha256") == cell_key
    ]
    if len(matches) != 1:
        raise RuntimeError("formal cell key does not identify exactly one scheduled cell")
    cell = matches[0]
    expected_config = (ROOT / str(cell["campaign_config_path"])).resolve()
    if config_path.resolve() != expected_config:
        raise RuntimeError("formal cell campaign config path differs from its manifest")
    if file_sha256(config_path) != cell.get("campaign_config_sha256"):
        raise RuntimeError("formal cell campaign config digest differs from its manifest")
    if getattr(args, "world_seed", None) != int(cell["world_seed"]):
        raise RuntimeError("formal cell world seed differs from its manifest")
    if getattr(args, "prior_arm", None) != str(cell["prior_arm"]):
        raise RuntimeError("formal cell prior arm differs from its manifest")
    return manifest, cell


def _qualification_execution_context(
    args: argparse.Namespace,
    *,
    config_path: Path,
    world_seed: int,
    arms: list[str],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]] | None:
    execute = bool(getattr(args, "qualification_execution", False))
    authorization_value = getattr(args, "qualification_authorization", None)
    attempt_value = getattr(args, "qualification_attempt_authorization", None)
    ledger_value = getattr(args, "qualification_cost_ledger", None)
    if not execute:
        if any(value is not None for value in (authorization_value, attempt_value, ledger_value)):
            raise RuntimeError(
                "qualification authorization inputs require --qualification-execution"
            )
        return None
    if getattr(args, "formal_manifest", None) is not None:
        raise RuntimeError("qualification execution cannot also be a formal cell")
    if authorization_value is None:
        raise RuntimeError("qualification execution requires --qualification-authorization")
    if attempt_value is None:
        raise RuntimeError("qualification execution requires --qualification-attempt-authorization")
    if ledger_value is None:
        raise RuntimeError("qualification execution requires --qualification-cost-ledger")
    authorization_path = Path(authorization_value).resolve()
    try:
        relative_authorization = authorization_path.relative_to(ROOT.resolve()).as_posix()
    except ValueError as error:
        raise RuntimeError("qualification authorization must be inside the repository") from error
    authorization = _load(authorization_path)
    manifest = build_formal_preflight(ROOT, DEFAULT_DESIGN, DEFAULT_ANALYSIS)
    errors = validate_qualification_execution_authorization(ROOT, authorization, manifest)
    if errors:
        raise RuntimeError("qualification execution authorization failed: " + "; ".join(errors))
    attempt_path = Path(attempt_value).resolve()
    ledger_path = Path(ledger_value).resolve()
    for path, label in (
        (attempt_path, "qualification attempt authorization"),
        (ledger_path, "qualification cost ledger"),
    ):
        try:
            path.relative_to(ROOT.resolve())
        except ValueError as error:
            raise RuntimeError(f"{label} must be inside the repository") from error
    attempt = _load(attempt_path)
    attempt_errors = validate_qualification_attempt_authorization(attempt, authorization)
    if attempt_errors:
        raise RuntimeError(
            "qualification attempt authorization failed: " + "; ".join(attempt_errors)
        )
    ledger = _load(ledger_path)
    cost_contract = authorization.get("qualification_currency_budget")
    if not isinstance(cost_contract, Mapping):
        raise RuntimeError("qualification authorization lacks its cost contract")
    ledger_errors = validate_qualification_cost_ledger(manifest, cost_contract, ledger)
    if ledger_errors:
        raise RuntimeError("qualification cost ledger failed: " + "; ".join(ledger_errors))
    if attempt.get("qualification_cost_ledger_sha256") != ledger.get(
        "qualification_cost_ledger_sha256"
    ):
        raise RuntimeError("qualification attempt does not bind the current cost ledger")
    schedule = authorization["qualification_schedule"]
    if (
        config_path.resolve() != (ROOT / str(schedule["campaign_config_path"])).resolve()
        or file_sha256(config_path) != schedule["campaign_config_sha256"]
        or world_seed != schedule["world_seed"]
        or len(arms) != 1
        or arms[0] != attempt.get("arm")
        or getattr(args, "prior_arm", None) != arms[0]
    ):
        raise RuntimeError("qualification execution differs from its parent-authorized arm")
    return (
        authorization,
        {
            "path": relative_authorization,
            "sha256": file_sha256(authorization_path),
            "authorization_sha256": authorization["authorization_sha256"],
        },
        {
            "path": attempt_path.relative_to(ROOT.resolve()).as_posix(),
            "sha256": file_sha256(attempt_path),
            "attempt_authorization_sha256": attempt["attempt_authorization_sha256"],
            "qualification_cost_ledger_path": ledger_path.relative_to(ROOT.resolve()).as_posix(),
            "qualification_cost_ledger_sha256": ledger["qualification_cost_ledger_sha256"],
        },
    )


def _progress(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rendered = json.dumps(dict(payload), ensure_ascii=False, sort_keys=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(rendered + "\n")
    with contextlib.suppress(BrokenPipeError, OSError, ValueError):
        print(rendered, flush=True)


def _analyze(
    records: list[dict[str, Any]],
    receipts: list[dict[str, Any]],
    *,
    final_metric_ids: list[str],
) -> dict[str, Any]:
    experiments: list[dict[str, Any]] = []
    actions: list[dict[str, Any]] = []
    committed_actions: list[dict[str, Any]] = []
    for row in records:
        action = dict(row.get("action", {}))
        actions.append(action)
        if row.get("transaction_status") == "committed":
            committed_actions.append(action)
        is_final_assay = (
            row.get("transaction_status") == "committed"
            and row.get("operation_type") == "measure"
            and row.get("instrument") == "final_assay"
        )
        if is_final_assay:
            recipe_sha256 = canonical_json_sha256(committed_actions)
            experiments.append(
                {
                    "experiment_index": len(experiments) + 1,
                    "operations": actions,
                    "committed_operations": committed_actions,
                    "recipe_sha256": recipe_sha256,
                    "leaderboard_score": row.get("leaderboard_score"),
                    "final_metrics": {
                        key: row.get("observation", {}).get(key) for key in final_metric_ids
                    },
                }
            )
            actions = []
            committed_actions = []
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
    receipt = receipts[0] if len(receipts) == 1 else {}
    recommendation = receipt.get("final_recommendation")
    recommendation = dict(recommendation) if isinstance(recommendation, Mapping) else None
    experiment_scores = [
        (int(item["experiment_index"]), float(item["leaderboard_score"]))
        for item in experiments
        if isinstance(item.get("leaderboard_score"), int | float)
        and not isinstance(item.get("leaderboard_score"), bool)
    ]
    incumbent_index = (
        min(experiment_scores, key=lambda item: (-item[1], item[0]))[0]
        if experiment_scores
        else None
    )
    recipe_hashes = [str(item["recipe_sha256"]) for item in experiments]
    return {
        "operation_attempt_count": len(records),
        "complete_experiment_count": len(experiments),
        "right_censored_open_experiment": bool(actions),
        "experiments": experiments,
        "unique_recipe_count": len(set(recipe_hashes)),
        "exact_repeat_count": len(recipe_hashes) - len(set(recipe_hashes)),
        "belief_snapshots": snapshots,
        "resource_rejection_count": resource_rejection_count,
        "final_campaign_resources": final_campaign_resources,
        "final_recommendation": recommendation,
        "final_recommendation_sha256": receipt.get("final_recommendation_sha256"),
        "observed_incumbent_experiment_index": incumbent_index,
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
    required_operation_counts: Mapping[str, Any],
    required_snapshot_stages: list[str] | None = None,
    operational_limits: Mapping[str, Any] | None = None,
    max_resource_rejections: int = 0,
    minimum_unique_recipes: int = 0,
    maximum_exact_repeats: int | None = None,
) -> dict[str, Any]:
    """Apply the frozen per-cell qualification contract fail-closed."""

    if max_resource_rejections < 0:
        raise ValueError("max_resource_rejections must be non-negative")

    receipt = receipts[0] if len(receipts) == 1 else {}
    usage = method_resources
    limits = method_resource_limits
    operational_limits = operational_limits or {}
    operational_receipt_complete = all(
        isinstance(receipt.get(field), (int, float)) and not isinstance(receipt.get(field), bool)
        for field in (
            "session_elapsed_s",
            "recovered_mcp_tool_failure_count",
            "maximum_consecutive_mcp_tool_failure_count",
            "provider_error_event_count",
        )
    )
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
    recommendation = analysis.get("final_recommendation")
    recommendation = recommendation if isinstance(recommendation, Mapping) else {}
    selected_experiment_index = recommendation.get("selected_experiment_index")
    recommendation_hash = canonical_json_sha256(recommendation) if recommendation else None
    expected_stages = required_snapshot_stages or [
        "pre_evidence",
        "post_neutral",
        "post_discriminating",
        "final",
    ]
    required_operations_reconciled = True
    for operation, bounds in required_operation_counts.items():
        low, high = (int(bounds[0]), int(bounds[1]))
        observed = int(operation_counts.get(operation, -1))
        required_operations_reconciled = required_operations_reconciled and low <= observed <= high
    target_experiments = int(method_resource_limits["complete_experiment_limit"])
    exact_repeat_limit = (
        target_experiments
        if maximum_exact_repeats is None
        else int(maximum_exact_repeats)
    )
    host_commit_required = receipt.get("schema_version") == (
        "chemworld-interactive-codex-session-receipt-0.2"
    )
    provider_terminal_completed = (
        receipt.get("status") == "completed"
        and receipt.get("return_code") == 0
        and (
            (
                host_commit_required
                and receipt.get("final_recommendation_source") == "host_mcp_commit"
            )
            or (
                not host_commit_required
                and receipt.get("final_payload_valid") is True
                and receipt.get("final_payload_status") == "campaign_complete"
            )
        )
    )
    checks = {
        "planned_complete_experiments": analysis.get("complete_experiment_count")
        == target_experiments
        and analysis.get("right_censored_open_experiment") is False,
        "typed_belief_checkpoints_complete": len(snapshots) == len(expected_stages)
        and stages == expected_stages,
        "recipe_diversity_reconciled": (
            True
            if minimum_unique_recipes <= 0 and maximum_exact_repeats is None
            else (
                int(analysis.get("unique_recipe_count", 0))
                >= int(minimum_unique_recipes)
                and int(analysis.get("exact_repeat_count", target_experiments))
                <= exact_repeat_limit
                and int(analysis.get("unique_recipe_count", 0))
                + int(analysis.get("exact_repeat_count", 0))
                == target_experiments
            )
        ),
        "one_campaign_session": len(receipts) == 1
        and method_resources.get("provider_session_count") == 1
        and receipt.get("session_scope") == "campaign",
        "provider_session_completed": provider_terminal_completed,
        "final_recommendation_committed": (
            isinstance(selected_experiment_index, int)
            and not isinstance(selected_experiment_index, bool)
            and 1 <= selected_experiment_index <= target_experiments
            and any(
                item.get("experiment_index") == selected_experiment_index
                for item in analysis.get("experiments", [])
                if isinstance(item, Mapping)
            )
            and recommendation_hash == analysis.get("final_recommendation_sha256")
            and recommendation_hash == receipt.get("final_recommendation_sha256")
            and (
                not host_commit_required
                or (
                    receipt.get("final_recommendation_source") == "host_mcp_commit"
                    and any(
                        item.get("tool") == "commit_final_recommendation"
                        and item.get("status") == "completed"
                        for item in receipt.get("mcp_tool_calls", [])
                        if isinstance(item, Mapping)
                    )
                )
            )
        ),
        "tool_integrity": receipt.get("experiment_tool_integrity_verified_after_session") is True
        and receipt.get("lab_tool_integrity_verified_after_session") is True
        and receipt.get("mcp_tool_integrity_verified_after_session") is True,
        "no_resource_rejection": int(analysis.get("resource_rejection_count", 0))
        <= max_resource_rejections,
        "campaign_terminal": resources.get("campaign_terminal") is True
        and state.get("closed_batches") == target_experiments
        and state.get("final_assays") == target_experiments,
        "process_time_reconciled": "process_time_s" in report_only
        and float(report_only.get("process_time_s", 0.0)) <= process_time_limit_s,
        "task_required_operations_reconciled": required_operations_reconciled,
        "exact_replay": exact_replay.get("verified") is True,
        "execution_audit": isinstance(analysis.get("execution_audit"), Mapping)
        and analysis["execution_audit"].get("passed") is True,
        "provider_usage_reconciled": method_resources.get("provider_usage_pending") is False
        and method_resources.get("provider_usage_accounting_complete") is True
        and usage.get("in_flight_model_call_count") == 0
        and int(usage.get("input_token_count", 0)) <= int(limits.get("input_token_limit", 0))
        and int(usage.get("uncached_input_token_count", 0))
        <= int(limits.get("uncached_input_token_limit", 0))
        and int(usage.get("output_token_count", 0)) <= int(limits.get("output_token_limit", 0)),
        "provider_operational_limits_reconciled": (
            not operational_limits
            or (
                operational_receipt_complete
                and float(receipt["session_elapsed_s"])
                <= float(operational_limits.get("session_wall_time_limit_s", float("inf")))
                and int(receipt["recovered_mcp_tool_failure_count"])
                <= int(operational_limits.get("max_recovered_mcp_tool_failures", 0))
                and int(receipt["maximum_consecutive_mcp_tool_failure_count"])
                <= int(operational_limits.get("max_consecutive_mcp_tool_failures", 0))
                and int(receipt["provider_error_event_count"])
                <= int(operational_limits.get("max_provider_error_events", 0))
            )
        ),
    }
    if tuple(checks) != REQUIRED_CELL_QUALIFICATION_CHECKS:
        raise RuntimeError("cell qualification checks drifted from the frozen method gate")
    return {
        "passed": all(checks.values()),
        "checks": checks,
        "failed_checks": [name for name, passed in checks.items() if not passed],
        "resource_rejection_policy": {
            "observed": int(analysis.get("resource_rejection_count", 0)),
            "maximum": int(max_resource_rejections),
            "semantics": "retained_participant_behavior_no_host_repair",
            "passed": checks["no_resource_rejection"],
        },
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
    world_interventions = _world_interventions(config)
    provider = config["provider"]
    completed = 0
    target_experiments = int(config["campaign"]["complete_experiments"])
    failure: dict[str, str] | None = None
    with tempfile.TemporaryDirectory(prefix="chemworld-work-ii-cell-") as temporary:
        def on_session_progress(payload: dict[str, Any]) -> None:
            _progress(
                progress_path,
                {
                    "stage": "provider_session_liveness",
                    "world_seed": world_seed,
                    "cell": cell_index,
                    "total_cells": total_cells,
                    "arm": arm,
                    **payload,
                    "elapsed_s": round(perf_counter() - cell_started, 1),
                },
            )

        agent = InteractiveCodexExperimentAgent(
            workspace=Path(temporary) / "workspace",
            role_id=f"work_ii_{provider['id']}_{provider['model']}_persistent_campaign",
            model=str(provider["model"]),
            reasoning_effort=str(provider["reasoning_effort"]),
            model_provider=str(provider["id"]),
            model_provider_name=str(provider["name"]),
            model_provider_base_url=str(provider["base_url"]),
            model_provider_env_key=(
                str(provider["env_key"]) if provider.get("env_key") is not None else None
            ),
            model_provider_wire_api=str(provider["wire_api"]),
            model_provider_auth_mode=cast(
                ProviderAuthMode, str(provider.get("auth_mode", "env_key"))
            ),
            model_provider_api_key_file=_resolve_optional_path(provider.get("api_key_file")),
            model_provider_model_catalog_json=_resolve_optional_path(
                provider.get("model_catalog_json")
            ),
            model_provider_preferred_auth_method=(
                str(provider["preferred_auth_method"])
                if provider.get("preferred_auth_method") is not None
                else None
            ),
            model_provider_forced_login_method=(
                str(provider["forced_login_method"])
                if provider.get("forced_login_method") is not None
                else None
            ),
            request_timeout_s=float(provider["request_timeout_s"]),
            finalization_timeout_s=float(provider["finalization_timeout_s"]),
            session_wall_time_limit_s=float(provider["session_wall_time_limit_s"])
            if provider.get("session_wall_time_limit_s") is not None
            else None,
            max_recovered_mcp_tool_failures=int(provider.get("max_recovered_mcp_tool_failures", 0)),
            max_consecutive_mcp_tool_failures=int(
                provider.get("max_consecutive_mcp_tool_failures", 0)
            ),
            max_provider_error_events=int(provider.get("max_provider_error_events", 0)),
            session_progress_callback=on_session_progress,
            session_progress_interval_s=float(provider.get("progress_interval_s", 30.0)),
            pre_action_restart_limit=0,
            session_scope="campaign",
            belief_checkpoint_contract=_checkpoint_contract(config, arm),
            initial_world_model=_arm_initial_world_model(config, arm),
        )

        def on_step(record: Any, trace: list[dict[str, Any]]) -> None:
            nonlocal completed
            del trace
            if record.event_type in {"experiment_end", "batch_discard"}:
                completed += 1
            resources = record.info.get("campaign_resources", {})
            provider_usage = agent.method_resource_usage()
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
                    "target_experiments": target_experiments,
                    "remaining_resources": resources.get("state", {}).get("remaining"),
                    "provider_usage_pending": provider_usage.get("provider_usage_pending"),
                    "session_elapsed_s": provider_usage.get("session_elapsed_s"),
                    "recovered_mcp_tool_failure_count": provider_usage.get(
                        "recovered_mcp_tool_failure_count"
                    ),
                    "provider_error_event_count": provider_usage.get("provider_error_event_count"),
                    "input_token_count": (
                        None
                        if provider_usage.get("provider_usage_pending")
                        else provider_usage.get("input_token_count")
                    ),
                    "uncached_input_token_count": (
                        None
                        if provider_usage.get("provider_usage_pending")
                        else provider_usage.get("uncached_input_token_count")
                    ),
                    "output_token_count": (
                        None
                        if provider_usage.get("provider_usage_pending")
                        else provider_usage.get("output_token_count")
                    ),
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
                material_information=_arm_material_information(config, arm),
                campaign_resource_card=card,
                electrochemical_material_family_id=config.get("electrochemical_material_family_id"),
                crystallization_material_family_id=config.get("crystallization_material_family_id"),
                electrochemical_workflow_mode=config.get("electrochemical_workflow_mode"),
                scoring_contract_id=config.get("scoring_contract_id"),
                observation_noise_mode=config["observation_noise_mode"],
                observation_noise_namespace=(
                    f"{config['observation_noise_namespace']}--seed{world_seed}"
                ),
                world_interventions=world_interventions,
            )
            del history
        except Exception as error:  # preserve the failed cell and stop the next seed block
            failure = {"type": type(error).__name__, "message": str(error)[:1000]}
        receipts = agent.provider_receipts()
        usage = agent.method_resource_usage()
    trajectory_path = cell_root / "trajectory.jsonl"
    records = load_jsonl(trajectory_path) if trajectory_path.exists() else []
    analysis = _analyze(
        records,
        receipts,
        final_metric_ids=[
            str(item)
            for item in config.get("analysis", {}).get(
                "final_metric_ids",
                [
                    "selective_product_yield",
                    "energy_efficiency",
                    "safety_risk",
                    "score",
                ],
            )
        ],
    )
    replay = (
        verify_records(
            records,
            tolerance=0.0,
            world_interventions=world_interventions,
        ).to_dict()
        if records
        else {"verified": False, "checked_steps": 0, "max_abs_error": None, "mismatches": []}
    )
    trajectory_terminal_state = (
        "completed"
        if analysis["complete_experiment_count"] == target_experiments
        and analysis["right_censored_open_experiment"] is False
        else "right_censored"
        if records
        else "failed"
    )
    analysis.update(
        build_work_ii_execution_artifacts(
            records,
            replay,
            planned_experiment_count=target_experiments,
            terminal_state=trajectory_terminal_state,
            hidden_identity={
                "prior_arm": arm,
                "world_seed": world_seed,
            },
        )
    )
    qualification = _qualification(
        analysis=analysis,
        exact_replay=replay,
        method_resources=usage,
        method_resource_limits=config["method_resources"],
        receipts=receipts,
        process_time_limit_s=float(config["campaign"]["process_time_limit_s"]),
        required_operation_counts=dict(
            config.get("qualification", {}).get(
                "required_operation_counts", {"electrolyze": [4, 5]}
            )
        ),
        required_snapshot_stages=list(_checkpoint_contract(config, arm)["snapshot_stages"]),
        operational_limits=provider,
        max_resource_rejections=int(
            config.get("qualification", {}).get("max_resource_rejections", 0)
        ),
        minimum_unique_recipes=int(
            config.get("qualification", {}).get("minimum_unique_recipes", 0)
        ),
        maximum_exact_repeats=(
            int(config["qualification"]["maximum_exact_repeats"])
            if config.get("qualification", {}).get("maximum_exact_repeats")
            is not None
            else None
        ),
    )
    row = {
        "arm": arm,
        "world_law_id": config.get("world_law_id"),
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
            "target_experiments": target_experiments,
            "qualification_failed_checks": qualification["failed_checks"],
            "elapsed_s": row["elapsed_s"],
        },
    )
    return row


def run(args: argparse.Namespace) -> dict[str, Any]:
    config_path = args.config.resolve()
    config = _load(config_path)
    formal_context = _formal_cell_context(args, config_path=config_path)
    formal_manifest = formal_context[0] if formal_context is not None else None
    formal_cell = formal_context[1] if formal_context is not None else None
    world_seed = int(args.world_seed if args.world_seed is not None else config["world_seed"])
    output = args.output.resolve()
    progress_path = args.progress_file.resolve()
    all_arms = list(config["prior_arms"])
    if args.prior_arm is not None:
        if args.prior_arm not in all_arms:
            raise ValueError(f"unknown prior arm: {args.prior_arm}")
        arms = [args.prior_arm]
    else:
        arms = all_arms
    qualification_context = _qualification_execution_context(
        args,
        config_path=config_path,
        world_seed=world_seed,
        arms=arms,
    )
    if args.prior_arm is not None:
        output.parent.mkdir(parents=True, exist_ok=True)
    else:
        output.mkdir(parents=True, exist_ok=False)
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
        if qualification_context is not None:
            row["qualification_attempt_authorization_binding"] = qualification_context[2]
            write_json_atomic(cell_root / "summary.json", row)
        if formal_cell is not None:
            row["formal_cell"] = formal_cell
            row["formal_result"] = True
            row["formal_preflight_sha256"] = formal_manifest["preflight_sha256"]
            if row["completed"]:
                plan = build_blind_evaluation_plan(
                    formal_cell,
                    row,
                    formal_manifest["blind_evaluator_contract"],
                )
                plan_errors = validate_blind_evaluation_plan(plan)
                if plan_errors:
                    raise RuntimeError(
                        "blind evaluator plan validation failed: " + "; ".join(plan_errors)
                    )
                plan_path = cell_root / "blind_evaluation_plan.json"
                write_json_atomic(plan_path, plan)
                row["blind_evaluation_plan"] = {
                    "path": "blind_evaluation_plan.json",
                    "sha256": file_sha256(plan_path),
                    "plan_sha256": plan["plan_sha256"],
                    "scheduled_execution_count": plan["blind_execution_count"],
                }
            else:
                row["blind_evaluation_plan"] = {
                    "status": "not_materialized_for_noncompleted_cell",
                    "scheduled_execution_count": 6,
                    "executed_count": 0,
                    "denominator_retained": True,
                }
            write_json_atomic(cell_root / "summary.json", row)
        results.append(row)
    report = {
        "schema_version": (
            "chemworld-work-ii-formal-cell-report-0.1"
            if formal_cell is not None
            else METHOD_QUALIFICATION_REPORT_VERSION
        ),
        "pilot_id": config["pilot_id"],
        "cell_id": (
            formal_cell["cell_id"]
            if formal_cell is not None
            else f"{config['pilot_id']}--seed{world_seed}"
        ),
        "formal_cell_key_sha256": (
            formal_cell["cell_key_sha256"] if formal_cell is not None else None
        ),
        "formal_result": formal_cell is not None,
        "qualification_execution_authorized": qualification_context is not None,
        "qualification_execution_authorization_binding": (
            qualification_context[1] if qualification_context is not None else None
        ),
        "qualification_attempt_authorization_binding": (
            qualification_context[2] if qualification_context is not None else None
        ),
        "config_sha256": canonical_json_sha256(config),
        "config_file_sha256": file_sha256(config_path),
        "world_seed": world_seed,
        "cell_count": len(results),
        "completed_cell_count": sum(row["completed"] for row in results),
        "elapsed_s": round(perf_counter() - started, 1),
        "results": results,
    }
    report["report_sha256"] = method_qualification_report_sha256(report)
    write_json_atomic(output / "report.json", report)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--progress-file", type=Path, required=True)
    parser.add_argument("--world-seed", type=int)
    parser.add_argument("--prior-arm")
    parser.add_argument("--formal-manifest", type=Path)
    parser.add_argument("--formal-cell-key")
    parser.add_argument("--allow-formal-execution", action="store_true")
    parser.add_argument("--qualification-execution", action="store_true")
    parser.add_argument("--qualification-authorization", type=Path)
    parser.add_argument("--qualification-attempt-authorization", type=Path)
    parser.add_argument("--qualification-cost-ledger", type=Path)
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
