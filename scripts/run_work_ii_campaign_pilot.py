#!/usr/bin/env python3
"""Run one Work II electrochemical world with one Codex session per prior arm."""

from __future__ import annotations

import argparse
import contextlib
import json
import sys
import tempfile
import time
from collections.abc import Callable, Mapping
from pathlib import Path
from time import perf_counter
from typing import Any, cast

from chemworld.agents.interactive_codex_experiment import (
    InteractiveCodexExperimentAgent,
    ProviderAuthMode,
    validated_mcp_tool_failure_budget,
)
from chemworld.campaign_resources import CampaignResourceCard
from chemworld.data.logging import load_jsonl
from chemworld.eval.provenance import canonical_json_sha256, file_sha256, write_json_atomic
from chemworld.eval.runner import run_agent
from chemworld.eval.verify import verify_records
from chemworld.eval.work_ii_ap_d1_development import (
    DEFAULT_AP_D1_READINESS,
    validate_and_claim_ap_d1_development_attempt,
)
from chemworld.eval.work_ii_blind import (
    build_blind_evaluation_plan,
    effective_blind_evaluator_contract,
    validate_blind_evaluation_plan,
)
from chemworld.eval.work_ii_cost import validate_qualification_cost_ledger
from chemworld.eval.work_ii_d1_execution import validate_d1_qualification_evidence
from chemworld.eval.work_ii_execution_mode import validate_release_d1_config
from chemworld.eval.work_ii_formal import (
    build_checkpoint_contract as _checkpoint_contract,
)
from chemworld.eval.work_ii_formal import (
    validate_formal_bindings,
    validate_formal_preflight,
)
from chemworld.eval.work_ii_method_qualification_local import (
    validate_method_qualification_local_manifest,
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
from chemworld.eval.work_ii_resource_calibration_v02 import (
    AGENT_INVALID_ENFORCEMENT_POLICY,
    PROVIDER_ERROR_ENFORCEMENT_POLICY,
)
from chemworld.eval.work_ii_resource_calibration_v02 import (
    pattern_key as resource_calibration_pattern_key,
)
from chemworld.eval.work_ii_resource_calibration_v02 import (
    validate_authorization as validate_resource_calibration_authorization,
)
from chemworld.tasks import get_task

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "configs/benchmark/work_ii_campaign_pilot.json"
DEFAULT_DESIGN = ROOT / "configs/benchmark/work_ii_formal_design_v0.2.json"
DEFAULT_ANALYSIS = ROOT / "configs/benchmark/work_ii_analysis_plan_v0.2.json"

TEMP_DIRECTORY_CLEANUP_RETRY_LIMIT = 20
TEMP_DIRECTORY_CLEANUP_RETRY_INTERVAL_S = 0.05


def _cleanup_temporary_directory_best_effort(
    temporary: tempfile.TemporaryDirectory[str],
) -> dict[str, Any]:
    """Clean a closed cell workspace without replacing its durable closeout."""

    last_error: OSError | None = None
    for attempt in range(1, TEMP_DIRECTORY_CLEANUP_RETRY_LIMIT + 1):
        try:
            temporary.cleanup()
            return {"status": "completed", "attempts": attempt}
        except OSError as error:
            last_error = error
            if attempt < TEMP_DIRECTORY_CLEANUP_RETRY_LIMIT:
                time.sleep(TEMP_DIRECTORY_CLEANUP_RETRY_INTERVAL_S)
    assert last_error is not None
    return {
        "status": "deferred",
        "attempts": TEMP_DIRECTORY_CLEANUP_RETRY_LIMIT,
        "error_type": type(last_error).__name__,
        "error": str(last_error)[:1000],
    }


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


def _arm_initial_world_model(config: Mapping[str, Any], arm: str) -> dict[str, Any] | None:
    value = _arm_contract(config, arm).get("initial_world_model")
    if value is None:
        return None
    if not isinstance(value, Mapping):
        raise ValueError(f"prior_arms.{arm}.initial_world_model must be an object")
    return dict(value)


def _recipe_coverage_contract(config: Mapping[str, Any]) -> dict[str, Any]:
    """Expose the runner's recipe-diversity qualification to the participant."""

    campaign = config["campaign"]
    qualification = config.get("qualification")
    qualification = qualification if isinstance(qualification, Mapping) else {}
    target = int(campaign["complete_experiments"])
    minimum_unique = int(qualification.get("minimum_unique_recipes", 0))
    raw_maximum_repeats = qualification.get("maximum_exact_repeats")
    maximum_repeats = (
        target if raw_maximum_repeats is None else int(raw_maximum_repeats)
    )
    if not 0 <= minimum_unique <= target:
        raise ValueError(
            "minimum_unique_recipes must be between zero and complete_experiments"
        )
    if not 0 <= maximum_repeats <= target:
        raise ValueError(
            "maximum_exact_repeats must be between zero and complete_experiments"
        )
    return {
        "target_complete_experiments": target,
        "minimum_unique_recipes": minimum_unique,
        "maximum_exact_repeats": maximum_repeats,
        "recipe_identity_semantics": {
            "unit": "completed_experiment",
            "identity_basis": (
                "exact equality of the ordered committed lab action objects from batch "
                "start through the final assay, including operation names and every "
                "submitted action parameter"
            ),
            "rejected_or_rolled_back_attempts_included": False,
            "exact_repeat_count": (
                "target completed experiments minus the number of distinct recipes"
            ),
        },
    }


def _campaign_card(config: Mapping[str, Any]) -> CampaignResourceCard:
    campaign = config["campaign"]
    return CampaignResourceCard(
        card_id=str(campaign.get("card_id", f"work-ii-{config['task_id']}-k4")),
        operation_attempt_limit=int(campaign["operation_attempt_limit"]),
        vessel_start_limit=int(campaign["vessel_start_limit"]),
        final_assay_limit=int(campaign["final_assay_limit"]),
        nonfinal_instrument_use_limit=int(campaign["nonfinal_instrument_use_limit"]),
        stock_limits=dict(campaign["stock_limits"]),
        per_instrument_limits=dict(campaign.get("per_instrument_limits", {})),
        process_time_limit_s=float(campaign["process_time_limit_s"]),
        implicit_operation_time_s=dict(campaign.get("implicit_operation_time_s", {})),
        operation_repeat_limits=dict(campaign["operation_repeat_limits"]),
        metadata={
            "pilot_id": config["pilot_id"],
            "task_id": config["task_id"],
            "process_time_policy": dict(campaign["process_time_policy"]),
            "closeout_policy": dict(campaign["closeout_policy"]),
            "recipe_coverage_contract": _recipe_coverage_contract(config),
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


def _required_operation_counts(config: Mapping[str, Any]) -> dict[str, Any]:
    qualification = config.get("qualification")
    qualification = qualification if isinstance(qualification, Mapping) else {}
    value = qualification.get("required_operation_counts")
    if value is None:
        if "w2_26_runtime_identity" in config:
            raise ValueError(
                "W2-26 runtime config requires explicit required_operation_counts"
            )
        return {}
    if not isinstance(value, Mapping):
        raise ValueError("required_operation_counts must be an object")
    return dict(value)


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
    if manifest.get("formal_execution_allowed") is not True:
        raise RuntimeError("formal manifest does not authorize participant execution")
    errors = validate_formal_bindings(ROOT, manifest)
    if errors:
        raise RuntimeError("formal manifest binding validation failed: " + "; ".join(errors))
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


def _prospective_cohort_context(
    args: argparse.Namespace,
    *,
    config_path: Path,
    config: Mapping[str, Any],
    world_seed: int,
    arms: list[str],
) -> dict[str, Any] | None:
    """Bind one cell to the lightweight DeepSeek C2 prospective plan.

    This is intentionally a single-plan execution check, not another release or
    readiness chain.  It protects the fixed task/world/arm denominator while
    leaving provider usage as report-only accounting.
    """

    execute = bool(getattr(args, "prospective_cohort_execution", False))
    plan_value = getattr(args, "prospective_cohort_plan", None)
    cell_id = getattr(args, "prospective_cell_id", None)
    if not execute:
        if plan_value is not None or cell_id is not None:
            raise RuntimeError(
                "prospective cohort inputs require --prospective-cohort-execution"
            )
        return None
    if plan_value is None or not isinstance(cell_id, str) or not cell_id:
        raise RuntimeError(
            "prospective cohort execution requires --prospective-cohort-plan "
            "and --prospective-cell-id"
        )
    if len(arms) != 1:
        raise RuntimeError("prospective cohort children execute exactly one arm")
    plan_path = Path(plan_value).resolve()
    try:
        plan_path.relative_to(ROOT.resolve())
    except ValueError as error:
        raise RuntimeError("prospective cohort plan must be inside the repository") from error
    plan = _load(plan_path)
    if (
        plan.get("schema_version")
        != "chemworld-work-ii-deepseek-c2-prospective-0.1"
        or plan.get("status") != "public_execution_authorized"
    ):
        raise RuntimeError("prospective cohort plan is not execution-authorized")
    provider = plan.get("provider")
    provider = provider if isinstance(provider, Mapping) else {}
    config_provider = config.get("provider")
    config_provider = config_provider if isinstance(config_provider, Mapping) else {}
    if (
        provider.get("id") != "deepseek"
        or provider.get("model") != "deepseek-v4-flash"
        or provider.get("resource_limits") != "report_only"
        or config_provider.get("id") != provider.get("id")
        or config_provider.get("model") != provider.get("model")
    ):
        raise RuntimeError("prospective cohort provider differs from the DeepSeek plan")
    matches: list[dict[str, Any]] = []
    for block in plan.get("public_blocks", []):
        if not isinstance(block, Mapping):
            continue
        for task in block.get("tasks", []):
            if not isinstance(task, Mapping):
                continue
            expected_config = (ROOT / str(task.get("config", ""))).resolve()
            seeds = task.get("world_seeds")
            seeds = seeds if isinstance(seeds, list) else []
            if (
                expected_config == config_path.resolve()
                and task.get("task_id") == config.get("task_id")
                and world_seed in seeds
            ):
                matches.append(
                    {
                        "cohort_id": plan.get("cohort_id"),
                        "block": block.get("block"),
                        "locus": block.get("locus"),
                        "task_id": task.get("task_id"),
                        "world_seed": world_seed,
                        "prior_arm": arms[0],
                        "rounds": block.get("rounds_per_session"),
                        "cell_id": cell_id,
                        "plan_path": plan_path.relative_to(ROOT.resolve()).as_posix(),
                        "resource_limits": "report_only",
                    }
                )
    if len(matches) != 1:
        raise RuntimeError("prospective cohort child is not a unique scheduled task/world")
    expected_cell_id = (
        f"{matches[0]['block']}--{matches[0]['task_id']}--"
        f"seed{world_seed}--{arms[0]}"
    )
    if cell_id != expected_cell_id:
        raise RuntimeError("prospective cohort cell id differs from its fixed schedule")
    if int(config.get("campaign", {}).get("complete_experiments", -1)) != int(
        matches[0]["rounds"]
    ):
        raise RuntimeError("prospective cohort round count differs from its fixed schedule")
    return matches[0]


def _qualification_execution_context(
    args: argparse.Namespace,
    *,
    config_path: Path,
    world_seed: int,
    arms: list[str],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]] | None:
    execute = bool(getattr(args, "qualification_execution", False))
    manifest_value = getattr(args, "qualification_manifest", None)
    authorization_value = getattr(args, "qualification_authorization", None)
    attempt_value = getattr(args, "qualification_attempt_authorization", None)
    ledger_value = getattr(args, "qualification_cost_ledger", None)
    if not execute:
        if any(
            value is not None
            for value in (
                manifest_value,
                authorization_value,
                attempt_value,
                ledger_value,
            )
        ):
            raise RuntimeError(
                "qualification authorization inputs require --qualification-execution"
            )
        return None
    if getattr(args, "formal_manifest", None) is not None:
        raise RuntimeError("qualification execution cannot also be a formal cell")
    if manifest_value is None:
        raise RuntimeError("qualification execution requires --qualification-manifest")
    if authorization_value is None:
        raise RuntimeError("qualification execution requires --qualification-authorization")
    if attempt_value is None:
        raise RuntimeError("qualification execution requires --qualification-attempt-authorization")
    if ledger_value is None:
        raise RuntimeError("qualification execution requires --qualification-cost-ledger")
    manifest_path = Path(manifest_value).resolve()
    authorization_path = Path(authorization_value).resolve()
    for path, label in (
        (manifest_path, "qualification manifest"),
        (authorization_path, "qualification authorization"),
    ):
        try:
            path.relative_to(ROOT.resolve())
        except ValueError as error:
            raise RuntimeError(f"{label} must be inside the repository") from error
    try:
        relative_authorization = authorization_path.relative_to(ROOT.resolve()).as_posix()
    except ValueError as error:
        raise RuntimeError("qualification authorization must be inside the repository") from error
    manifest = _load(manifest_path)
    manifest_errors = validate_method_qualification_local_manifest(ROOT, manifest)
    if manifest_errors:
        raise RuntimeError(
            "qualification manifest failed: " + "; ".join(manifest_errors)
        )
    authorization = _load(authorization_path)
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
        authorization.get("qualification_manifest_sha256")
        != manifest.get("manifest_sha256")
        or config_path.resolve()
        != (ROOT / str(schedule["campaign_config_path"])).resolve()
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
            "path": manifest_path.relative_to(ROOT.resolve()).as_posix(),
            "sha256": file_sha256(manifest_path),
            "qualification_manifest_sha256": manifest["manifest_sha256"],
        },
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


def _resource_calibration_execution_context(
    args: argparse.Namespace,
    *,
    config_path: Path,
    world_seed: int,
    arms: list[str],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]] | None:
    execute = bool(getattr(args, "resource_calibration_execution", False))
    values = (
        getattr(args, "resource_calibration_manifest", None),
        getattr(args, "resource_calibration_authorization", None),
        getattr(args, "resource_calibration_cost_reservation", None),
    )
    if not execute:
        if any(value is not None for value in values):
            raise RuntimeError(
                "resource-calibration inputs require --resource-calibration-execution"
            )
        return None
    if any(value is None for value in values):
        raise RuntimeError("resource-calibration execution requires all gate artifacts")
    if len(arms) != 1:
        raise RuntimeError("resource calibration executes exactly one arm per child")
    manifest_path, authorization_path, reservation_path = (
        Path(value).resolve() for value in values
    )
    for path, label in (
        (manifest_path, "resource-calibration manifest"),
        (authorization_path, "resource-calibration authorization"),
        (reservation_path, "resource-calibration reservation"),
    ):
        try:
            path.relative_to(ROOT.resolve())
        except ValueError as error:
            raise RuntimeError(f"{label} must be inside the repository") from error
    manifest = _load(manifest_path)
    authorization = _load(authorization_path)
    errors = validate_resource_calibration_authorization(ROOT, authorization, manifest_path)
    if errors:
        raise RuntimeError("resource-calibration authorization failed: " + "; ".join(errors))
    matches = [
        pattern
        for pattern in manifest.get("patterns", [])
        if isinstance(pattern, Mapping)
        and pattern.get("world_seed") == world_seed
        and pattern.get("campaign_config_binding", {}).get("path")
        == config_path.relative_to(ROOT).as_posix()
    ]
    reservation = _load(reservation_path)
    config_binding = matches[0].get("campaign_config_binding", {}) if len(matches) == 1 else {}
    config_digest = (
        file_sha256(config_path)
        if config_binding.get("hash_kind") == "file_sha256"
        else canonical_json_sha256(_load(config_path))
        if config_binding.get("hash_kind") == "canonical_json_sha256"
        else None
    )
    if (
        len(matches) != 1
        or config_digest != config_binding.get("sha256")
        or resource_calibration_pattern_key(reservation)
        != resource_calibration_pattern_key(matches[0])
        or reservation.get("authorization_sha256") != authorization.get("authorization_sha256")
        or reservation.get("currency_ceiling_usd")
        != authorization.get("currency_ceiling_usd")
    ):
        raise RuntimeError("resource-calibration child differs from its authorized pattern")
    return (
        manifest,
        authorization,
        {
            "manifest": {
                "path": manifest_path.relative_to(ROOT).as_posix(),
                "file_sha256": file_sha256(manifest_path),
                "canonical_json_sha256": canonical_json_sha256(manifest),
            },
            "authorization": {
                "path": authorization_path.relative_to(ROOT).as_posix(),
                "file_sha256": file_sha256(authorization_path),
                "authorization_sha256": authorization["authorization_sha256"],
            },
            "cost_reservation": {
                "path": reservation_path.relative_to(ROOT).as_posix(),
                "file_sha256": file_sha256(reservation_path),
                "locus": reservation["locus"],
                "task_id": reservation["task_id"],
                "rounds": reservation["rounds"],
                "attempt_number": reservation["attempt_number"],
                "reservation_sequence_number": reservation[
                    "reservation_sequence_number"
                ],
                "authorization_sha256": reservation["authorization_sha256"],
            },
            "pattern": {
                "rounds": matches[0]["rounds"],
                "locus": matches[0]["locus"],
                "task_id": matches[0]["task_id"],
                "world_seed": matches[0]["world_seed"],
                "prior_arm": arms[0],
                "campaign_config_sha256": config_binding["sha256"],
                "campaign_config_hash_kind": config_binding["hash_kind"],
            },
        },
    )


def _agent_invalid_online_limits(
    provider: Mapping[str, Any],
    *,
    agent_invalid_enforcement: str | None,
) -> tuple[int | None, int | None]:
    """Resolve participant-invalid online limits without relaxing normal execution."""

    if agent_invalid_enforcement is None:
        return (
            int(provider.get("max_recovered_mcp_tool_failures", 0)),
            int(provider.get("max_consecutive_mcp_tool_failures", 0)),
        )
    if agent_invalid_enforcement != AGENT_INVALID_ENFORCEMENT_POLICY:
        raise RuntimeError("resource calibration agent-invalid policy is not frozen")
    return None, None


def _provider_error_online_limit(
    provider: Mapping[str, Any],
    *,
    provider_error_enforcement: str | None,
) -> int | None:
    """Disable only W2-26 online interruption while retaining every error event."""

    if provider_error_enforcement is None:
        return int(provider.get("max_provider_error_events", 0))
    if provider_error_enforcement != PROVIDER_ERROR_ENFORCEMENT_POLICY:
        raise RuntimeError("resource calibration provider-error policy is not frozen")
    return None


def _release_d1_execution_context(
    args: argparse.Namespace,
    *,
    config: Mapping[str, Any],
) -> Path | None:
    """Fail closed for Q2-derived D1 while leaving separately authorized runners intact."""

    qualification = config.get("qualification")
    qualification = qualification if isinstance(qualification, Mapping) else {}
    is_q2_d1 = (
        "execution_context" in config
        or "legacy_source_evidence" in config
        or qualification.get("q2_passed") is True
    )
    manifest_value = getattr(args, "release_manifest", None)
    if not is_q2_d1:
        if manifest_value is not None:
            raise RuntimeError("release manifest is only valid for a Q2-derived D1 config")
        return None
    if manifest_value is None:
        raise RuntimeError("provider D1 execution requires a release manifest")
    manifest_path = Path(manifest_value).resolve()
    try:
        manifest_path.relative_to(ROOT.resolve())
    except ValueError as error:
        raise RuntimeError("provider D1 release manifest must be inside the repository") from error
    errors = validate_release_d1_config(
        ROOT,
        config,
        manifest_path,
        require_provider_authorized=True,
    )
    if errors:
        raise RuntimeError("provider release D1 validation failed: " + "; ".join(errors))
    evidence_errors = validate_d1_qualification_evidence(ROOT, config)
    if evidence_errors:
        raise RuntimeError(
            "provider D1 qualification evidence failed: " + "; ".join(evidence_errors)
        )
    return manifest_path


def _ap_development_execution_context(
    args: argparse.Namespace,
    *,
    config_path: Path,
    config: Mapping[str, Any],
    output: Path,
) -> dict[str, Any] | None:
    """Authorize one child only through the explicit development D1 contract."""

    execute = bool(getattr(args, "ap_development_execution", False))
    authorization_value = getattr(args, "ap_development_authorization", None)
    readiness_value = getattr(args, "ap_development_readiness", None)
    authorized_root_value = getattr(args, "ap_development_authorized_output_root", None)
    attempt_receipt_value = getattr(args, "ap_development_attempt_receipt", None)
    cost_ledger_value = getattr(args, "ap_development_cost_ledger", None)
    if not execute:
        if any(
            value is not None
            for value in (
                authorization_value,
                readiness_value,
                authorized_root_value,
                attempt_receipt_value,
                cost_ledger_value,
            )
        ):
            raise RuntimeError(
                "A-P development authorization inputs require --ap-development-execution"
            )
        return None
    if any(
        value is None
        for value in (
            authorization_value,
            readiness_value,
            authorized_root_value,
            attempt_receipt_value,
            cost_ledger_value,
        )
    ):
        raise RuntimeError(
            "A-P development execution requires authorization, readiness and "
            "the authorized parent output root"
        )
    if (
        any(
            getattr(args, field, None) is not None
            for field in (
                "release_manifest",
                "formal_manifest",
                "qualification_authorization",
                "resource_calibration_authorization",
            )
        )
        or bool(getattr(args, "qualification_execution", False))
        or bool(getattr(args, "resource_calibration_execution", False))
    ):
        raise RuntimeError("A-P development execution cannot cross another execution mode")
    authorization_path = Path(authorization_value).resolve()
    readiness_path = Path(readiness_value).resolve()
    authorized_root = Path(authorized_root_value).resolve()
    authorization = _load(authorization_path)
    if not output.resolve().is_relative_to(authorized_root):
        raise RuntimeError("A-P development child output escapes its authorized root")
    if getattr(args, "prior_arm", None) is None:
        raise RuntimeError("A-P development child requires one parent-scheduled arm")
    try:
        attempt_claim = validate_and_claim_ap_d1_development_attempt(
            ROOT,
            config_path=config_path,
            output_root=authorized_root,
            attempt_output=output,
            attempt_receipt_path=Path(attempt_receipt_value).resolve(),
            cost_ledger_path=Path(cost_ledger_value).resolve(),
            world_seed=int(args.world_seed),
            arm=str(args.prior_arm),
            authorization_path=authorization_path,
            readiness_path=readiness_path,
        )
    except (OSError, TypeError, ValueError, json.JSONDecodeError) as error:
        raise RuntimeError(f"A-P development attempt gate failed: {error}") from error
    qualification = config.get("qualification")
    qualification = qualification if isinstance(qualification, Mapping) else {}
    if (
        config.get("formal_result") is not False
        or qualification.get("formal_r5_authorized") is not False
        or qualification.get("execution_authorized") is not False
    ):
        raise RuntimeError("A-P development config crossed its non-formal boundary")
    return {
        "authorization_path": str(authorization_path),
        "approved_at": authorization["approved_at"],
        "authorized_by": "user",
        "currency": authorization["currency"],
        "currency_ceiling_usd": authorization["currency_ceiling_usd"],
        "formal_result": False,
        "formal_r5_authorized": False,
        "attempt_claim": attempt_claim,
    }


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
        committed = row.get("transaction_status") == "committed"
        if committed:
            committed_actions.append(action)
        is_final_assay = (
            committed
            and row.get("operation_type") == "measure"
            and row.get("instrument") == "final_assay"
        )
        if is_final_assay:
            recipe_sha256 = canonical_json_sha256(committed_actions)
            raw_lifecycle_index = row.get("experiment_index")
            lifecycle_experiment_index = (
                raw_lifecycle_index + 1
                if isinstance(raw_lifecycle_index, int)
                and not isinstance(raw_lifecycle_index, bool)
                and raw_lifecycle_index >= 0
                else len(experiments) + 1
            )
            completed_ordinal = len(experiments) + 1
            experiments.append(
                {
                    "experiment_index": lifecycle_experiment_index,
                    "lifecycle_experiment_index": lifecycle_experiment_index,
                    "experiment_index_base": 1,
                    "batch_id": f"batch-{lifecycle_experiment_index:04d}",
                    "completed_ordinal": completed_ordinal,
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
        elif committed and row.get("operation_type") == "discard_batch":
            # A discarded vessel is a closed lifecycle but not a completed
            # experiment.  Never let its operations leak into the recipe hash
            # of the fresh batch that follows.
            actions = []
            committed_actions = []
    snapshots = [item for receipt in receipts for item in receipt.get("belief_snapshots", [])]
    resource_rejection_count = sum(
        1 for row in records if row.get("transaction_status") == "campaign_resource_rejected"
    )
    unsafe_outcome_count = sum(
        bool(row.get("observation", {}).get("flags", {}).get("unsafe"))
        for row in records
        if isinstance(row.get("observation"), Mapping)
        and isinstance(row.get("observation", {}).get("flags"), Mapping)
    )
    dynamic_physical_failure_count = sum(
        row.get("transaction_status") == "rolled_back"
        and row.get("rollback_reason") == "constitution_failed"
        for row in records
    )
    final_campaign_resources: dict[str, Any] = {}
    last_legal_action_count: int | None = None
    if records:
        last_view = records[-1].get("agent_view", {})
        if isinstance(last_view, Mapping):
            tool_json = last_view.get("tool_json", {})
            if isinstance(tool_json, Mapping):
                available_actions = tool_json.get("available_actions")
                if isinstance(available_actions, list):
                    last_legal_action_count = sum(
                        isinstance(action, Mapping)
                        and action.get("valid") is not False
                        for action in available_actions
                    )
                campaign_state = tool_json.get("campaign_state", {})
                if isinstance(campaign_state, Mapping):
                    candidate = campaign_state.get("campaign_resources", {})
                    if isinstance(candidate, Mapping):
                        final_campaign_resources = dict(candidate)
    terminal_receipts = [
        receipt
        for receipt in receipts
        if receipt.get("pre_action_retry_classification") == "terminal_accepted"
    ]
    receipt = (
        terminal_receipts[0]
        if len(terminal_receipts) == 1
        else receipts[0]
        if len(receipts) == 1
        else {}
    )
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
    campaign_terminal = final_campaign_resources.get("campaign_terminal") is True
    return {
        "operation_attempt_count": len(records),
        "committed_operation_count": sum(
            row.get("transaction_status") == "committed" for row in records
        ),
        "complete_experiment_count": len(experiments),
        "closed_batch_count": max(
            (
                int(row["experiment_index"]) + 1
                for row in records
                if row.get("experiment_ended") is True
                and isinstance(row.get("experiment_index"), int)
                and not isinstance(row.get("experiment_index"), bool)
            ),
            default=len(experiments),
        ),
        "completed_experiment_indices": [
            int(item["lifecycle_experiment_index"]) for item in experiments
        ],
        "right_censored_open_experiment": bool(actions),
        "last_legal_action_count": last_legal_action_count,
        "nonterminal_no_legal_actions": not campaign_terminal
        and bool(actions)
        and last_legal_action_count == 0,
        "experiments": experiments,
        "unique_recipe_count": len(set(recipe_hashes)),
        "exact_repeat_count": len(recipe_hashes) - len(set(recipe_hashes)),
        "belief_snapshots": snapshots,
        "resource_rejection_count": resource_rejection_count,
        "unsafe_outcome_count": unsafe_outcome_count,
        "dynamic_physical_failure_count": dynamic_physical_failure_count,
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


def _w2_26_campaign_receipt_contract(
    receipts: list[dict[str, Any]],
    method_resources: Mapping[str, Any],
    *,
    unlimited_provider_continuations: bool = False,
) -> dict[str, Any]:
    """Separate accepted-session identity from bounded zero-action process attempts."""

    terminal_indices = [
        index
        for index, receipt in enumerate(receipts)
        if receipt.get("pre_action_retry_classification") == "terminal_accepted"
        and isinstance(receipt.get("accepted_action_count"), int)
        and not isinstance(receipt.get("accepted_action_count"), bool)
        and int(receipt["accepted_action_count"]) > 0
    ]
    terminal_index = terminal_indices[0] if len(terminal_indices) == 1 else None
    predecessors = receipts[:terminal_index] if terminal_index is not None else []
    predecessor_valid = (
        unlimited_provider_continuations or len(predecessors) <= 1
    ) and all(
        receipt.get("status") == "interrupted_before_next_action"
        and receipt.get("accepted_action_count") == 0
        and receipt.get("pre_action_retry_classification")
        == "eligible_zero_action_infrastructure_predecessor"
        and receipt.get("failure_type")
        in {"process_exited_before_first_request", "request_wait_timeout"}
        and (
            (
                receipt.get("usage_observed") is True
                and receipt.get("usage_complete") is True
            )
            or (
                receipt.get("failure_type") == "process_exited_before_first_request"
                and receipt.get("usage_accounting_scope")
                == "unobserved_not_attributable_pre_action_process_attempt"
                and receipt.get("usage_observed") is False
                and receipt.get("thread_id") is None
                and receipt.get("event_counts") == {}
                and receipt.get("tool_events") == []
                and receipt.get("provider_errors") == []
            )
        )
        and receipt.get("provider_error_event_count") == 0
        and receipt.get("mcp_tool_calls") == []
        and receipt.get("belief_snapshot_count") == 0
        and receipt.get("final_recommendation") is None
        and receipt.get("mcp_tool_integrity_verified_after_session") is True
        and receipt.get("experiment_tool_integrity_verified_after_session") is True
        and receipt.get("lab_tool_integrity_verified_after_session") is True
        for receipt in predecessors
    )
    process_attempt_count = method_resources.get("provider_process_attempt_count")
    logical_turn_count = method_resources.get(
        "logical_codex_turn_count", process_attempt_count
    )
    accepted_receipt = receipts[terminal_index] if terminal_index is not None else {}
    continuation_count = accepted_receipt.get("accepted_turn_continuation_count", 0)
    thread_turns = accepted_receipt.get("turn_receipts", [])
    thread_id = accepted_receipt.get("thread_id")
    legacy_single_turn_receipt = continuation_count == 0 and thread_turns == []
    same_thread_continuation_valid = legacy_single_turn_receipt or (
        isinstance(continuation_count, int)
        and not isinstance(continuation_count, bool)
        and continuation_count >= 0
        and (unlimited_provider_continuations or continuation_count <= 1)
        and isinstance(thread_turns, list)
        and len(thread_turns) == continuation_count + 1
        and all(
            isinstance(turn, dict)
            and turn.get("turn_index") == index
            and turn.get("thread_id") == thread_id
            and turn.get("usage_complete") is True
            and turn.get("provider_error_event_count") == 0
            for index, turn in enumerate(thread_turns, start=1)
        )
    )
    process_attempt_count_valid = (
        isinstance(process_attempt_count, int)
        and not isinstance(process_attempt_count, bool)
        and process_attempt_count >= 1
        and (unlimited_provider_continuations or process_attempt_count <= 3)
    )
    predecessor_count = len(predecessors)
    accepted_participant_model_call_count = 1 + continuation_count
    counters_reconciled = (
        process_attempt_count_valid
        and method_resources.get("provider_session_count") == 1
        and method_resources.get("model_call_count")
        == accepted_participant_model_call_count
        and logical_turn_count == process_attempt_count
        and process_attempt_count
        == predecessor_count + accepted_participant_model_call_count
        and method_resources.get("accepted_provider_session_count") == 1
        and method_resources.get("accepted_participant_model_call_count")
        == accepted_participant_model_call_count
        and method_resources.get("unattributed_pre_action_process_attempt_count")
        == sum(
            receipt.get("usage_accounting_scope")
            == "unobserved_not_attributable_pre_action_process_attempt"
            for receipt in predecessors
        )
    )
    valid = (
        terminal_index is not None
        and terminal_index == len(receipts) - 1
        and process_attempt_count_valid
        and predecessor_valid
        and same_thread_continuation_valid
        and counters_reconciled
    )
    return {
        "valid": valid,
        "accepted_receipt": (
            receipts[terminal_index] if valid and terminal_index is not None else {}
        ),
        "accepted_provider_session_count": 1 if valid else 0,
        "accepted_participant_model_call_count": (
            accepted_participant_model_call_count if valid else 0
        ),
        "provider_process_attempt_count": process_attempt_count,
        "logical_codex_turn_count": logical_turn_count,
        "accepted_turn_continuation_count": continuation_count,
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
    agent_invalid_enforcement: str | None = None,
    provider_error_enforcement: str | None = None,
    unlimited_provider_continuations: bool = False,
    terminal_action_readout_required: bool = False,
    terminal_action_prediction_mode: str = "full_metrics",
) -> dict[str, Any]:
    """Apply the frozen per-cell qualification contract fail-closed."""

    if max_resource_rejections < 0:
        raise ValueError("max_resource_rejections must be non-negative")
    if agent_invalid_enforcement not in {None, AGENT_INVALID_ENFORCEMENT_POLICY}:
        raise ValueError("unsupported agent-invalid enforcement policy")
    if provider_error_enforcement not in {None, PROVIDER_ERROR_ENFORCEMENT_POLICY}:
        raise ValueError("unsupported provider-error enforcement policy")
    if terminal_action_prediction_mode not in {"full_metrics", "ranking_only"}:
        raise ValueError("unsupported terminal action prediction mode")

    w2_26_retry_contract_enabled = (
        agent_invalid_enforcement == AGENT_INVALID_ENFORCEMENT_POLICY
        and provider_error_enforcement == PROVIDER_ERROR_ENFORCEMENT_POLICY
    )
    w2_26_receipt_contract = (
        _w2_26_campaign_receipt_contract(
            receipts,
            method_resources,
            unlimited_provider_continuations=unlimited_provider_continuations,
        )
        if w2_26_retry_contract_enabled
        else None
    )
    receipt = (
        w2_26_receipt_contract["accepted_receipt"]
        if w2_26_receipt_contract is not None
        else receipts[0]
        if len(receipts) == 1
        else {}
    )
    usage = method_resources
    limits = method_resource_limits
    operational_limits = operational_limits or {}
    try:
        mcp_failure_budget = validated_mcp_tool_failure_budget(receipt)
    except ValueError:
        mcp_failure_budget = None
    elapsed_value = receipt.get("session_elapsed_s")
    provider_error_value = receipt.get("provider_error_event_count")
    operational_receipt_complete = (
        mcp_failure_budget is not None
        and isinstance(elapsed_value, (int, float))
        and not isinstance(elapsed_value, bool)
        and float(elapsed_value) >= 0.0
        and isinstance(provider_error_value, int)
        and not isinstance(provider_error_value, bool)
        and provider_error_value >= 0
    )
    agent_invalid_reconciled = (
        agent_invalid_enforcement == AGENT_INVALID_ENFORCEMENT_POLICY
        or (
            mcp_failure_budget is not None
            and int(mcp_failure_budget["scientific_episode_count"])
            <= int(operational_limits.get("max_recovered_mcp_tool_failures", 0))
            and int(mcp_failure_budget["scientific_episode_maximum"])
            <= int(operational_limits.get("max_consecutive_mcp_tool_failures", 0))
        )
    )
    if not operational_receipt_complete:
        provider_error_reconciled = False
    else:
        observed_provider_errors = max(
            int(provider_error_value),
            int(mcp_failure_budget["provider_network_count"]),
        )
        provider_error_reconciled = (
            observed_provider_errors == 0
            if provider_error_enforcement == PROVIDER_ERROR_ENFORCEMENT_POLICY
            else observed_provider_errors
            <= int(operational_limits.get("max_provider_error_events", 0))
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
    selected_action_query_id = recommendation.get("selected_action_query_id")
    action_predictions = recommendation.get("candidate_predictions")
    action_ranking = recommendation.get("ranking")
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
        target_experiments if maximum_exact_repeats is None else int(maximum_exact_repeats)
    )
    host_commit_required = (
        receipt.get("final_recommendation_source") == "host_mcp_commit"
        or isinstance(receipt.get("final_recommendation_commit"), Mapping)
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
                int(analysis.get("unique_recipe_count", 0)) >= int(minimum_unique_recipes)
                and int(analysis.get("exact_repeat_count", target_experiments))
                <= exact_repeat_limit
                and int(analysis.get("unique_recipe_count", 0))
                + int(analysis.get("exact_repeat_count", 0))
                == target_experiments
            )
        ),
        "one_campaign_session": (
            w2_26_receipt_contract["valid"]
            if w2_26_receipt_contract is not None
            else len(receipts) == 1
            and method_resources.get("provider_session_count") == 1
        )
        and receipt.get("session_scope") == "campaign",
        "provider_session_completed": provider_terminal_completed,
        "final_recommendation_committed": (
            (
                isinstance(selected_action_query_id, str)
                and bool(selected_action_query_id)
                and isinstance(action_ranking, list)
                and bool(action_ranking)
                and action_ranking[0] == selected_action_query_id
                and (
                    "candidate_predictions" not in recommendation
                    if terminal_action_prediction_mode == "ranking_only"
                    else isinstance(action_predictions, list) and bool(action_predictions)
                )
                if terminal_action_readout_required
                else isinstance(selected_experiment_index, int)
                and not isinstance(selected_experiment_index, bool)
                and any(
                    item.get("lifecycle_experiment_index", item.get("experiment_index"))
                    == selected_experiment_index
                    for item in analysis.get("experiments", [])
                    if isinstance(item, Mapping)
                )
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
        and isinstance(state.get("closed_batches"), int)
        and not isinstance(state.get("closed_batches"), bool)
        and int(state["closed_batches"]) >= target_experiments
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
        and (
            w2_26_receipt_contract is not None
            or (
                int(usage.get("input_token_count", 0))
                <= int(limits.get("input_token_limit", 0))
                and int(usage.get("uncached_input_token_count", 0))
                <= int(limits.get("uncached_input_token_limit", 0))
                and int(usage.get("output_token_count", 0))
                <= int(limits.get("output_token_limit", 0))
            )
        ),
        "provider_operational_limits_reconciled": (
            (
                w2_26_receipt_contract is not None
                and operational_receipt_complete
                and int(mcp_failure_budget["unclassified_count"]) == 0
            )
            or not operational_limits
            or (
                operational_receipt_complete
                and float(receipt["session_elapsed_s"])
                <= float(operational_limits.get("session_wall_time_limit_s", float("inf")))
                and agent_invalid_reconciled
                and int(mcp_failure_budget["transport_count"])
                <= int(operational_limits.get("max_recovered_mcp_tool_failures", 0))
                and int(mcp_failure_budget["transport_maximum"])
                <= int(operational_limits.get("max_consecutive_mcp_tool_failures", 0))
                and int(mcp_failure_budget["unclassified_count"]) == 0
                and provider_error_reconciled
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
        "agent_invalid_operational_policy": {
            "enforcement": (
                AGENT_INVALID_ENFORCEMENT_POLICY
                if agent_invalid_enforcement == AGENT_INVALID_ENFORCEMENT_POLICY
                else "source_config_hard_limits"
            ),
            "participant_payload_auto_repair": False,
            "raw_mcp_failures_retained": True,
            "observed_recovered_count": (
                None
                if mcp_failure_budget is None
                else int(mcp_failure_budget["scientific_count"])
            ),
            "observed_maximum_consecutive_count": (
                None
                if mcp_failure_budget is None
                else int(mcp_failure_budget["scientific_maximum"])
            ),
            "observed_recovery_episode_count": (
                None
                if mcp_failure_budget is None
                else int(mcp_failure_budget["scientific_episode_count"])
            ),
            "observed_maximum_consecutive_recovery_episode_count": (
                None
                if mcp_failure_budget is None
                else int(mcp_failure_budget["scientific_episode_maximum"])
            ),
        },
        "provider_error_operational_policy": {
            "enforcement": (
                PROVIDER_ERROR_ENFORCEMENT_POLICY
                if provider_error_enforcement == PROVIDER_ERROR_ENFORCEMENT_POLICY
                else "source_config_hard_limit"
            ),
            "online_interruption_disabled": (
                provider_error_enforcement == PROVIDER_ERROR_ENFORCEMENT_POLICY
            ),
            "post_session_zero_tolerance": (
                provider_error_enforcement == PROVIDER_ERROR_ENFORCEMENT_POLICY
            ),
            "observed_event_count": (
                int(provider_error_value)
                if isinstance(provider_error_value, int)
                and not isinstance(provider_error_value, bool)
                else None
            ),
            "passed": provider_error_reconciled,
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
    agent_invalid_enforcement: str | None = None,
    provider_error_enforcement: str | None = None,
    provider_resource_limits_report_only: bool = False,
    agent_factory: Callable[..., Any] | None = None,
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
    (
        max_recovered_mcp_tool_failures,
        max_consecutive_mcp_tool_failures,
    ) = _agent_invalid_online_limits(
        provider,
        agent_invalid_enforcement=agent_invalid_enforcement,
    )
    max_provider_error_events = _provider_error_online_limit(
        provider,
        provider_error_enforcement=provider_error_enforcement,
    )
    completed = 0
    target_experiments = int(config["campaign"]["complete_experiments"])
    runtime_method_resource_limits = dict(config["method_resources"])
    if provider_resource_limits_report_only:
        for field in (
            "input_token_limit",
            "uncached_input_token_limit",
            "output_token_limit",
            "model_call_limit",
        ):
            # The ledger requires a numeric bound while provider usage is still
            # in flight. sys.maxsize preserves that accounting protocol without
            # imposing an experiment-relevant token ceiling.
            runtime_method_resource_limits[field] = sys.maxsize
        runtime_method_resource_limits["wall_time_limit_s"] = None
    failure: dict[str, str] | None = None
    temporary_directory = tempfile.TemporaryDirectory(prefix="chemworld-work-ii-cell-")
    # Keep the cell workspace alive until its receipts, qualification, and
    # durable summary have been closed out. Cleanup is explicitly deferred.
    with contextlib.nullcontext(temporary_directory.name) as temporary:

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

        agent = (agent_factory or InteractiveCodexExperimentAgent)(
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
            max_recovered_mcp_tool_failures=max_recovered_mcp_tool_failures,
            max_consecutive_mcp_tool_failures=max_consecutive_mcp_tool_failures,
            max_provider_error_events=max_provider_error_events,
            session_progress_callback=on_session_progress,
            session_progress_interval_s=float(provider.get("progress_interval_s", 30.0)),
            # W2-26 alone admits one typed, zero-action infrastructure predecessor.
            # Other paths retain their explicit provider setting (normally zero).
            pre_action_restart_limit=(
                sys.maxsize
                if provider_resource_limits_report_only
                else 1
                if agent_invalid_enforcement == AGENT_INVALID_ENFORCEMENT_POLICY
                and provider_error_enforcement == PROVIDER_ERROR_ENFORCEMENT_POLICY
                else int(provider.get("pre_action_restart_limit", 0))
            ),
            accepted_turn_continuation_limit=(
                sys.maxsize
                if provider_resource_limits_report_only
                else int(provider.get("accepted_turn_continuation_limit", 0))
            ),
            provider_process_attempt_limit=(
                sys.maxsize
                if provider_resource_limits_report_only
                else int(provider["provider_process_attempt_limit"])
                if provider.get("provider_process_attempt_limit") is not None
                else None
            ),
            session_scope="campaign",
            belief_checkpoint_contract=_checkpoint_contract(config, arm),
            initial_world_model=_arm_initial_world_model(config, arm),
            terminal_action_readout_contract=(
                dict(config["terminal_action_readout"])
                if isinstance(config.get("terminal_action_readout"), Mapping)
                else None
            ),
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
                method_resource_limits=runtime_method_resource_limits,
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
            maximum_experiment_count=int(
                config["campaign"].get("vessel_start_limit", target_experiments)
            ),
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
        required_operation_counts=_required_operation_counts(config),
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
            if config.get("qualification", {}).get("maximum_exact_repeats") is not None
            else None
        ),
        agent_invalid_enforcement=agent_invalid_enforcement,
        provider_error_enforcement=provider_error_enforcement,
        unlimited_provider_continuations=provider_resource_limits_report_only,
        terminal_action_readout_required=isinstance(
            config.get("terminal_action_readout"), Mapping
        ),
        terminal_action_prediction_mode=str(
            config.get("terminal_action_readout", {}).get(
                "prediction_mode", "full_metrics"
            )
            if isinstance(config.get("terminal_action_readout"), Mapping)
            else "full_metrics"
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
    row["temporary_workspace_cleanup"] = _cleanup_temporary_directory_best_effort(
        temporary_directory
    )
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
    prospective_context = _prospective_cohort_context(
        args,
        config_path=config_path,
        config=config,
        world_seed=world_seed,
        arms=arms,
    )
    qualification_context = _qualification_execution_context(
        args,
        config_path=config_path,
        world_seed=world_seed,
        arms=arms,
    )
    calibration_context = _resource_calibration_execution_context(
        args,
        config_path=config_path,
        world_seed=world_seed,
        arms=arms,
    )
    if qualification_context is not None and calibration_context is not None:
        raise RuntimeError("one child cannot be both qualification and resource calibration")
    agent_invalid_enforcement = None
    provider_error_enforcement = None
    if calibration_context is not None:
        runtime_enforcement = calibration_context[1].get("runtime_enforcement")
        runtime_enforcement = (
            runtime_enforcement if isinstance(runtime_enforcement, Mapping) else {}
        )
        agent_invalid_enforcement = runtime_enforcement.get(
            "agent_invalid_enforcement"
        )
        if agent_invalid_enforcement != AGENT_INVALID_ENFORCEMENT_POLICY:
            raise RuntimeError("resource calibration agent-invalid policy is not frozen")
        provider_error_enforcement = runtime_enforcement.get(
            "provider_error_enforcement"
        )
        if provider_error_enforcement != PROVIDER_ERROR_ENFORCEMENT_POLICY:
            raise RuntimeError("resource calibration provider-error policy is not frozen")
    if prospective_context is not None:
        if any(
            context is not None
            for context in (formal_context, qualification_context, calibration_context)
        ):
            raise RuntimeError("prospective cohort execution must be the only evidence mode")
        agent_invalid_enforcement = AGENT_INVALID_ENFORCEMENT_POLICY
        provider_error_enforcement = PROVIDER_ERROR_ENFORCEMENT_POLICY
    ap_development_context = _ap_development_execution_context(
        args,
        config_path=config_path,
        config=config,
        output=output,
    )
    if ap_development_context is not None and (
        formal_context is not None
        or qualification_context is not None
        or calibration_context is not None
        or prospective_context is not None
    ):
        raise RuntimeError("A-P development D1 must be the only execution mode")
    release_manifest_path = None
    if (
        formal_context is None
        and qualification_context is None
        and calibration_context is None
        and ap_development_context is None
        and prospective_context is None
    ):
        release_manifest_path = _release_d1_execution_context(args, config=config)
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
            agent_invalid_enforcement=agent_invalid_enforcement,
            provider_error_enforcement=provider_error_enforcement,
            provider_resource_limits_report_only=(
                prospective_context is not None
                or (
                    calibration_context is not None
                    and calibration_context[1].get("unlimited_spend_authorized") is True
                )
            ),
        )
        if qualification_context is not None:
            row["qualification_attempt_authorization_binding"] = qualification_context[3]
            write_json_atomic(cell_root / "summary.json", row)
        if calibration_context is not None:
            row["resource_calibration_execution_binding"] = calibration_context[2]
            write_json_atomic(cell_root / "summary.json", row)
        if formal_cell is not None:
            row["formal_cell"] = formal_cell
            row["formal_result"] = True
            row["formal_preflight_sha256"] = formal_manifest["preflight_sha256"]
            if row["completed"]:
                blind_contract = effective_blind_evaluator_contract(
                    formal_cell,
                    formal_manifest["blind_evaluator_contract"],
                )
                plan = build_blind_evaluation_plan(
                    formal_cell,
                    row,
                    blind_contract,
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
                    "scheduled_execution_count": formal_cell["blind_validation_execution_count"],
                    "executed_count": 0,
                    "denominator_retained": True,
                }
            write_json_atomic(cell_root / "summary.json", row)
        if prospective_context is not None:
            row["prospective_formal_result"] = True
            row["prospective_cohort_cell"] = prospective_context
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
        "prospective_formal_result": prospective_context is not None,
        "prospective_cohort_cell": prospective_context,
        "qualification_manifest_sha256": (
            qualification_context[0].get("qualification_manifest_sha256")
            if qualification_context is not None
            else None
        ),
        "execution_context": (
            dict(config["execution_context"]) if release_manifest_path is not None else None
        ),
        "legacy_source_evidence": (
            config.get("legacy_source_evidence") if release_manifest_path is not None else None
        ),
        "provider_execution_authorized": (
            release_manifest_path is not None
            or ap_development_context is not None
            or prospective_context is not None
        ),
        "development_only": ap_development_context is not None,
        "release_manifest": (
            {
                "path": release_manifest_path.relative_to(ROOT.resolve()).as_posix(),
                "sha256": file_sha256(release_manifest_path),
            }
            if release_manifest_path is not None
            else None
        ),
        "qualification_execution_authorized": qualification_context is not None,
        "qualification_execution_authorization_binding": (
            qualification_context[2] if qualification_context is not None else None
        ),
        "qualification_manifest_binding": (
            qualification_context[1] if qualification_context is not None else None
        ),
        "qualification_attempt_authorization_binding": (
            qualification_context[3] if qualification_context is not None else None
        ),
        "resource_calibration_execution_binding": (
            calibration_context[2] if calibration_context is not None else None
        ),
        "ap_development_execution_authorized": ap_development_context is not None,
        "ap_development_authorization": ap_development_context,
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
    parser.add_argument("--release-manifest", type=Path)
    parser.add_argument("--formal-manifest", type=Path)
    parser.add_argument("--formal-cell-key")
    parser.add_argument("--allow-formal-execution", action="store_true")
    parser.add_argument("--prospective-cohort-execution", action="store_true")
    parser.add_argument("--prospective-cohort-plan", type=Path)
    parser.add_argument("--prospective-cell-id")
    parser.add_argument("--qualification-execution", action="store_true")
    parser.add_argument("--qualification-manifest", type=Path)
    parser.add_argument("--qualification-authorization", type=Path)
    parser.add_argument("--qualification-attempt-authorization", type=Path)
    parser.add_argument("--qualification-cost-ledger", type=Path)
    parser.add_argument("--resource-calibration-execution", action="store_true")
    parser.add_argument("--resource-calibration-manifest", type=Path)
    parser.add_argument("--resource-calibration-authorization", type=Path)
    parser.add_argument("--resource-calibration-cost-reservation", type=Path)
    parser.add_argument("--ap-development-execution", action="store_true")
    parser.add_argument("--ap-development-authorization", type=Path)
    parser.add_argument(
        "--ap-development-readiness",
        type=Path,
        default=None,
        help=f"defaults conceptually to {DEFAULT_AP_D1_READINESS}",
    )
    parser.add_argument("--ap-development-authorized-output-root", type=Path)
    parser.add_argument("--ap-development-attempt-receipt", type=Path)
    parser.add_argument("--ap-development-cost-ledger", type=Path)
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
