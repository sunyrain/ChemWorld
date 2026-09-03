#!/usr/bin/env python3
"""Run and analyze the prospective W2-61 action-aligned extension of W2-50."""

from __future__ import annotations

import argparse
import json
import math
import random
import statistics
import time
from collections import defaultdict
from collections.abc import Mapping, Sequence
from copy import deepcopy
from pathlib import Path
from typing import Any

from run_work_ii_evidence_to_action_formal import _autonomous_thread_id
from run_work_ii_w250_matched_extension_pilot import (
    _candidate_packet,
    _load,
    _ranking_from_result,
    _run_condition,
    _sanitized_task_contract,
    _sha256_file,
    _write_once_or_match,
)
from run_work_ii_w250_yoked_schema_repair import (
    W250YokedRepairClient,
    provider_compatible_yoked_snapshot_schema,
)
from work_ii_longitudinal_runtime import Progress

from chemworld.data.logging import load_jsonl
from chemworld.eval.provenance import canonical_json_sha256, write_json_atomic
from chemworld.eval.work_ii_evidence_to_action import score_terminal_ranking
from chemworld.eval.work_ii_evidence_to_action_runtime import (
    build_donor_derivatives,
    build_recipient_context,
)

ROOT = Path(__file__).resolve().parents[1]
CURRENT_PATH = ROOT / "configs/current.json"
NOTE_PATH = (
    "workstreams/flagship_tasks/"
    "WORK_II_W250_ACTION_ALIGNED_CAUSAL_EXTENSION_EXPERIMENT_NOTE.md"
)
DEFAULT_OUTPUTS = {
    "deepseek": ROOT
    / "runs/development/"
    "work-ii-w2-61-deepseek-action-aligned-recipients-v0.1-20260902",
    "codex": ROOT
    / "runs/development/"
    "work-ii-w2-61-codex-action-aligned-recipients-v0.1-20260902",
}
DEFAULT_REPORTS = {
    participant: ROOT
    / "workstreams/flagship_tasks/reports/"
    / f"work-ii-w2-61-{participant}-action-aligned-causal-extension-v0.1.json"
    for participant in ("deepseek", "codex")
}
ALWAYS_RECIPIENT_CONDITIONS = ("no_evidence",)
DONOR_DEPENDENT_RECIPIENT_CONDITIONS = ("learned_law_only", "yoked_evidence")
RECIPIENT_CONDITIONS = (
    *ALWAYS_RECIPIENT_CONDITIONS,
    *DONOR_DEPENDENT_RECIPIENT_CONDITIONS,
)
DISPLAY_CONDITIONS = (
    "no_evidence",
    "yoked_evidence",
    "autonomous_exploration",
    "learned_law_only",
)
PRIMARY_CONTRASTS = (
    ("autonomous_exploration", "no_evidence"),
    ("yoked_evidence", "no_evidence"),
    ("learned_law_only", "no_evidence"),
    ("autonomous_exploration", "yoked_evidence"),
)
EXPECTED_SCHEDULED_STRATA = 45
BOOTSTRAP_SEED = 20260902
BOOTSTRAP_REPLICATES = 10_000


def _current_w250_binding(participant: str) -> dict[str, Any]:
    current = _load(CURRENT_PATH)
    work_ii = current.get("work_ii")
    work_ii = work_ii if isinstance(work_ii, Mapping) else {}
    binding_name = (
        "w2_50_open_action"
        if participant == "deepseek"
        else "w2_61_codex_open_action_donor"
    )
    binding = work_ii.get(binding_name)
    if not isinstance(binding, Mapping):
        raise ValueError(f"configs/current.json lacks the current {participant} donor binding")
    normalized = deepcopy(dict(binding))
    for key in ("root", "input_manifest", "summary"):
        path = ROOT / str(normalized.get(key, ""))
        missing = not path.is_dir() if key == "root" else not path.is_file()
        if missing:
            raise FileNotFoundError(f"current W2-50 binding is missing {key}: {path}")
    manifest_path = ROOT / str(normalized["input_manifest"])
    summary_path = ROOT / str(normalized["summary"])
    if _sha256_file(manifest_path) != normalized.get("input_manifest_sha256"):
        raise RuntimeError("current W2-50 input-manifest binding drifted")
    if _sha256_file(summary_path) != normalized.get("summary_sha256"):
        raise RuntimeError("current W2-50 summary binding drifted")
    expected_model = "deepseek-v4-flash" if participant == "deepseek" else "gpt-5.6-sol"
    if normalized.get("model", expected_model) != expected_model:
        raise RuntimeError(f"current {participant} donor model binding drifted")
    return normalized


def _one_summary_row(rows: object, *, cell_id: str) -> dict[str, Any]:
    if not isinstance(rows, list):
        raise ValueError("W2-50 summary lacks cell rows")
    matches = [
        dict(row)
        for row in rows
        if isinstance(row, Mapping) and row.get("cell_id") == cell_id
    ]
    if len(matches) != 1:
        raise ValueError(f"expected exactly one W2-50 summary row for {cell_id}")
    return matches[0]


def _stratum_inputs(
    *,
    donor_root: Path,
    manifest_cell: Mapping[str, Any],
    summary_cell: Mapping[str, Any],
    participant: str,
    donor_eligible: bool,
) -> dict[str, Any]:
    cell_id = str(manifest_cell["cell_id"])
    config_path = donor_root / str(manifest_cell["campaign_config_path"])
    config = _load(config_path)
    candidate_packet = _candidate_packet(config)
    checkpoint = config.get("belief_checkpoint")
    checkpoint = checkpoint if isinstance(checkpoint, Mapping) else {}
    held_out = checkpoint.get("held_out_queries")
    held_out = held_out if isinstance(held_out, list) else []
    query_metric_contract = {
        str(row["query_id"]): [str(item) for item in row["metric_ids"]]
        for row in held_out
        if isinstance(row, Mapping)
    }
    if len(query_metric_contract) != 8:
        raise ValueError(f"{cell_id}: donor checkpoint contract does not contain eight queries")
    arm = str(summary_cell["arm"])
    prior_arms = config.get("prior_arms")
    prior_arms = prior_arms if isinstance(prior_arms, Mapping) else {}
    arm_config = prior_arms.get(arm)
    if not isinstance(arm_config, Mapping) or not isinstance(
        arm_config.get("initial_world_model"), Mapping
    ):
        raise ValueError(f"{cell_id}: donor initial world model is missing")
    candidate_truth = manifest_cell.get("candidate_truth")
    if not isinstance(candidate_truth, Mapping):
        raise ValueError(f"{cell_id}: candidate truth is missing")
    provider = config.get("provider")
    expected_model = "deepseek-v4-flash" if participant == "deepseek" else "gpt-5.6-sol"
    if not isinstance(provider, Mapping) or provider.get("model") != expected_model:
        raise ValueError(f"{cell_id}: provider differs from the frozen {participant} donor")
    if participant == "codex" and provider.get("reasoning_effort") != "medium":
        raise ValueError(f"{cell_id}: Codex donor reasoning effort is not medium")
    payload = {
        "provider": deepcopy(dict(provider)),
        "task_contract": _sanitized_task_contract(
            config,
            world_seed=int(manifest_cell["world_seed"]),
        ),
        "initial_world_model": deepcopy(dict(arm_config["initial_world_model"])),
        "candidate_packet": candidate_packet,
        "candidate_truth": deepcopy(dict(candidate_truth)),
        "query_metric_contract": query_metric_contract,
        "allowed_feature_ids": [str(item) for item in checkpoint["allowed_feature_ids"]],
        "allowed_metric_ids": [str(item) for item in checkpoint["allowed_metric_ids"]],
        "allowed_prior_fields": [str(item) for item in checkpoint["allowed_prior_fields"]],
        "nominal_information_available": (
            arm_config["initial_world_model"].get("availability")
            != "opaque_for_target_locus"
        ),
        "source": {
            "campaign_config_path": str(config_path.relative_to(ROOT)).replace("\\", "/"),
            "campaign_config_sha256": _sha256_file(config_path),
            "cell_result_sha256": summary_cell.get("result_sha256"),
        },
    }
    if not donor_eligible:
        return payload
    if int(summary_cell.get("campaign_complete_experiment_count", 0) or 0) != 12:
        raise ValueError(f"{cell_id}: eligible donor lacks 12 completed experiments")
    ranking = summary_cell.get("participant_ranking")
    if not isinstance(ranking, list) or len(ranking) != 8 or len(set(map(str, ranking))) != 8:
        raise ValueError(f"{cell_id}: eligible donor lacks a complete ranking")
    trajectory_path = donor_root / "formal/campaigns" / cell_id / "trajectory.jsonl"
    trajectory = load_jsonl(trajectory_path)
    candidate_ids = [str(row["query_id"]) for row in candidate_packet["candidates"]]
    donor_result = {
        "status": str(summary_cell["status"]),
        "campaign_summary": deepcopy(dict(summary_cell["campaign_summary"])),
    }
    derivatives = build_donor_derivatives(
        donor_cell_id=cell_id,
        donor_result=donor_result,
        trajectory_rows=trajectory,
        candidate_query_ids=candidate_ids,
    )
    if int(derivatives["yoked_evidence_packet"].get("complete_experiment_count", 0)) != 12:
        raise ValueError(f"{cell_id}: donor derivative lost experiments")
    donor_score = score_terminal_ranking(ranking, candidate_truth)
    if donor_score["selected_rank"] != summary_cell.get("selected_rank"):
        raise ValueError(f"{cell_id}: recomputed donor rank drifted")
    payload.update(
        {
            "donor_derivatives": derivatives,
            "existing_autonomous_score": donor_score,
            "existing_autonomous_thread_id": _autonomous_thread_id(summary_cell),
            "existing_autonomous_provider_call_count": int(
                summary_cell["campaign_summary"]
                .get("method_resources", {})
                .get("provider_session_count", 0)
                or 0
            ),
        }
    )
    payload["source"].update(
        {
            "trajectory_path": str(trajectory_path.relative_to(ROOT)).replace("\\", "/"),
            "trajectory_sha256": _sha256_file(trajectory_path),
        }
    )
    return payload


def build_inputs(*, participant: str) -> dict[str, Any]:
    """Materialize all original W2-50 strata through the current artifact binding."""

    if participant not in {"deepseek", "codex"}:
        raise ValueError("unsupported W2-61 participant")
    binding = _current_w250_binding(participant)
    donor_root = ROOT / str(binding["root"])
    manifest = _load(ROOT / str(binding["input_manifest"]))
    summary = _load(ROOT / str(binding["summary"]))
    cells = manifest.get("cells")
    if not isinstance(cells, list) or len(cells) != EXPECTED_SCHEDULED_STRATA:
        raise ValueError("current W2-50 input manifest does not preserve 45 strata")

    strata: list[dict[str, Any]] = []
    seen: set[str] = set()
    for index, raw_cell in enumerate(cells, start=1):
        if not isinstance(raw_cell, Mapping):
            raise ValueError("W2-50 input manifest contains a malformed cell")
        manifest_cell = dict(raw_cell)
        cell_id = str(manifest_cell["cell_id"])
        if cell_id in seen:
            raise ValueError(f"duplicate W2-50 cell: {cell_id}")
        seen.add(cell_id)
        summary_cell = _one_summary_row(summary.get("cell_rows"), cell_id=cell_id)
        task_id = str(manifest_cell["task_id"])
        world_seed = int(manifest_cell["world_seed"])
        prior_arm = str(summary_cell["arm"])
        status = str(summary_cell["status"])
        admitted = status == "completed_uncontaminated"
        stratum = {
            "stratum_index": index,
            "stratum_id": cell_id,
            "cluster_id": str(manifest_cell["cluster_id"]),
            "task_id": task_id,
            "world_seed": world_seed,
            "prior_arm": prior_arm,
            "donor_status": status,
            "admitted": admitted,
            "recipient_conditions": [
                *ALWAYS_RECIPIENT_CONDITIONS,
                *(DONOR_DEPENDENT_RECIPIENT_CONDITIONS if admitted else ()),
            ],
        }
        stratum["inputs"] = _stratum_inputs(
            donor_root=donor_root,
            manifest_cell=manifest_cell,
            summary_cell=summary_cell,
            participant=participant,
            donor_eligible=admitted,
        )
        if not admitted:
            stratum["blocked_recipient_reason"] = "retained_w2_50_donor_failure"
            stratum["donor_failure"] = {
                "status": status,
                "result_sha256": summary_cell.get("result_sha256"),
                "campaign_complete_experiment_count": summary_cell.get(
                    "campaign_complete_experiment_count"
                ),
            }
        strata.append(stratum)

    admitted = sum(bool(row["admitted"]) for row in strata)
    if participant == "deepseek" and admitted != 42:
        raise ValueError("W2-50 admitted donor denominator drifted")
    new_sessions = EXPECTED_SCHEDULED_STRATA + admitted * len(
        DONOR_DEPENDENT_RECIPIENT_CONDITIONS
    )
    payload = {
        "schema_version": "chemworld-work-ii-w2-61-input-0.1",
        "study_id": f"work-ii-w2-61-{participant}-action-aligned-causal-extension-v0.1",
        "formal_result": False,
        "prospective_development_experiment": True,
        "experiment_note": NOTE_PATH,
        "participant": participant,
        "model": "deepseek-v4-flash" if participant == "deepseek" else "gpt-5.6-sol",
        "reasoning_effort": "high" if participant == "deepseek" else "medium",
        "current_binding": deepcopy(binding),
        "condition_order_for_display": list(DISPLAY_CONDITIONS),
        "recipient_execution_order": list(RECIPIENT_CONDITIONS),
        "scheduled_stratum_count": EXPECTED_SCHEDULED_STRATA,
        "admitted_stratum_count": admitted,
        "retained_donor_failure_count": EXPECTED_SCHEDULED_STRATA - admitted,
        "scheduled_condition_slot_count": EXPECTED_SCHEDULED_STRATA * 4,
        "new_recipient_session_count": new_sessions,
        "new_physical_experiment_count": 0,
        "new_truth_execution_count": 0,
        "strata": strata,
    }
    payload["input_sha256"] = canonical_json_sha256(payload)
    return payload


def provider_free_canary(inputs: Mapping[str, Any]) -> dict[str, Any]:
    checked_no_evidence = 0
    checked_donor_dependent = 0
    snapshot_schema_count = 0
    for stratum in inputs["strata"]:
        data = stratum["inputs"]
        common = {
            "task_contract": data["task_contract"],
            "initial_world_model": data["initial_world_model"],
            "candidate_packet": data["candidate_packet"],
        }
        no_evidence = build_recipient_context(
            condition="no_evidence",
            stage="terminal_ranking",
            **common,
        )
        if no_evidence.get("visible_law_artifact") is not None:
            raise ValueError("no-evidence canary received a law artifact")
        checked_no_evidence += 1
        if not stratum["admitted"]:
            continue
        learned = build_recipient_context(
            condition="learned_law_only",
            stage="terminal_ranking",
            law_artifact=data["donor_derivatives"]["learned_law_artifact"],
            **common,
        )
        yoked_pre = build_recipient_context(
            condition="yoked_evidence",
            stage="pre_evidence",
            yoked_evidence_packet=data["donor_derivatives"]["yoked_evidence_packet"],
            **common,
        )
        yoked_terminal = build_recipient_context(
            condition="yoked_evidence",
            stage="terminal_ranking",
            yoked_evidence_packet=data["donor_derivatives"]["yoked_evidence_packet"],
            **common,
        )
        if learned.get("visible_yoked_evidence_rounds"):
            raise ValueError("learned-law-only canary received donor evidence")
        if yoked_pre.get("candidate_packet") is not None:
            raise ValueError("yoked candidate packet leaked before terminal")
        if len(yoked_terminal.get("candidate_packet", [])) != 8:
            raise ValueError("yoked terminal canary lacks eight candidates")
        rounds = data["donor_derivatives"]["yoked_evidence_packet"][
            "checkpoint_rounds"
        ]
        visible_ids: list[str] = []
        for stage, visible_round_count in (
            ("pre_evidence", 0),
            ("after_experiment_3", 3),
            ("after_experiment_6", 6),
            ("after_experiment_9", 9),
            ("final", 12),
        ):
            visible_ids = [
                str(event["evidence_id"])
                for row in rounds[:visible_round_count]
                for event in row["events"]
            ]
            schema = provider_compatible_yoked_snapshot_schema(
                stage=stage,
                query_metric_contract=data["query_metric_contract"],
                allowed_feature_ids=data["allowed_feature_ids"],
                allowed_metric_ids=data["allowed_metric_ids"],
                allowed_prior_fields=data["allowed_prior_fields"],
                evidence_catalog=visible_ids,
                nominal_information_available=bool(data["nominal_information_available"]),
            )
            rendered = json.dumps(schema, ensure_ascii=False, sort_keys=True)
            if "oneOf" in rendered or "anyOf" in rendered:
                raise ValueError("provider-free canary retained a union schema")
            snapshot_schema_count += 1
        checked_donor_dependent += 1
    if checked_no_evidence != EXPECTED_SCHEDULED_STRATA:
        raise ValueError("provider-free no-evidence canary coverage drifted")
    if checked_donor_dependent != inputs["admitted_stratum_count"]:
        raise ValueError("provider-free canary coverage drifted")
    return {
        "schema_version": "chemworld-work-ii-w2-61-provider-free-canary-0.1",
        "status": "passed",
        "checked_no_evidence_strata": checked_no_evidence,
        "checked_admitted_strata": checked_donor_dependent,
        "checked_recipient_contexts": checked_no_evidence
        + checked_donor_dependent * 3,
        "checked_yoked_snapshot_schemas": snapshot_schema_count,
        "candidate_preterminal_reveal_count": 0,
        "provider_calls": 0,
        "physical_experiments": 0,
        "truth_executions": 0,
    }


def _result_path(output_root: Path, cell_id: str, condition: str) -> Path:
    return output_root / "results" / cell_id / f"{condition}.json"


def _attempt_path(output_root: Path, cell_id: str, condition: str) -> Path:
    return output_root / "attempts" / cell_id / f"{condition}.json"


def _condition_receipts(client: W250YokedRepairClient, condition: str) -> list[dict[str, Any]]:
    return [deepcopy(row) for row in client.receipts if row.get("condition") == condition]


def _failure_classification(error: Exception) -> str:
    classification = getattr(error, "classification", None)
    if isinstance(classification, str):
        return classification
    if isinstance(error, ValueError):
        return "participant_schema"
    return "runner_or_provider"


def _zero_action_platform_defect(receipts: Sequence[Mapping[str, Any]]) -> bool:
    if not receipts:
        return True
    return all(
        row.get("thread_id") is None
        and not row.get("usage")
        and int(row.get("tool_event_count", 0) or 0) == 0
        for row in receipts
    )


def _interrupted_result(
    *,
    output_root: Path,
    cell_id: str,
    condition: str,
) -> dict[str, Any]:
    turn_root = output_root / "provider-turns" / cell_id / condition
    turn_count = len(list(turn_root.glob("turn-*.json"))) if turn_root.is_dir() else 0
    return {
        "condition": condition,
        "status": "interrupted_retained",
        "failure_classification": "process_interruption_after_attempt_marker",
        "failure_message": (
            "attempt marker exists without a terminal result; session not relaunched"
        ),
        "observed_provider_turn_file_count": turn_count,
        "provider_call_count": turn_count,
        "physical_experiment_count": 0,
    }


def execute(
    *,
    inputs: Mapping[str, Any],
    output_root: Path,
    progress: Progress,
) -> None:
    halt_path = output_root / "halt.json"
    if halt_path.is_file():
        raise RuntimeError(f"W2-61 root is halted and immutable: {_load(halt_path)}")
    execution_strata = list(inputs["strata"])
    total_sessions = int(inputs["new_recipient_session_count"])
    completed_before = sum(
        _result_path(output_root, row["stratum_id"], condition).is_file()
        for row in execution_strata
        for condition in row["recipient_conditions"]
    )
    started = time.perf_counter()
    completed = completed_before
    for stratum_index, stratum in enumerate(execution_strata, start=1):
        cell_id = str(stratum["stratum_id"])
        data = stratum["inputs"]
        pending = [
            condition
            for condition in stratum["recipient_conditions"]
            if not _result_path(output_root, cell_id, condition).is_file()
        ]
        if not pending:
            continue
        with W250YokedRepairClient(
            provider=data["provider"],
            stratum_id=cell_id,
            output_root=output_root / "provider-turns" / cell_id,
            progress=progress,
            query_metric_contract=data["query_metric_contract"],
            allowed_feature_ids=data["allowed_feature_ids"],
            allowed_metric_ids=data["allowed_metric_ids"],
            allowed_prior_fields=data["allowed_prior_fields"],
            nominal_information_available=bool(data["nominal_information_available"]),
        ) as client:
            for condition in pending:
                result_path = _result_path(output_root, cell_id, condition)
                attempt_path = _attempt_path(output_root, cell_id, condition)
                if attempt_path.is_file():
                    result = _interrupted_result(
                        output_root=output_root,
                        cell_id=cell_id,
                        condition=condition,
                    )
                    _write_once_or_match(result_path, result)
                    completed += 1
                    continue
                _write_once_or_match(
                    attempt_path,
                    {
                        "schema_version": "chemworld-work-ii-w2-61-attempt-0.1",
                        "study_id": inputs["study_id"],
                        "input_sha256": inputs["input_sha256"],
                        "stratum_id": cell_id,
                        "stratum_index": int(stratum["stratum_index"]),
                        "condition": condition,
                        "attempt_ordinal": completed + 1,
                    },
                )
                progress.emit(
                    {
                        "stage": "w2_61_recipient_session_started",
                        "stratum_id": cell_id,
                        "stratum_index": stratum_index,
                        "condition": condition,
                        "completed_sessions": completed,
                        "total_sessions": total_sessions,
                    }
                )
                receipt_start = len(client.receipts)
                try:
                    result = _run_condition(condition, client=client, inputs=data)
                except Exception as error:
                    receipts = _condition_receipts(client, condition)
                    result = {
                        "condition": condition,
                        "status": "failed_retained",
                        "failure_type": type(error).__name__,
                        "failure_classification": _failure_classification(error),
                        "failure_message": str(error),
                        "provider_call_count": len(client.receipts) - receipt_start,
                        "provider_receipts": receipts,
                        "physical_experiment_count": 0,
                    }
                    _write_once_or_match(result_path, result)
                    completed += 1
                    progress.emit(
                        {
                            "stage": "w2_61_recipient_session_failed",
                            "stratum_id": cell_id,
                            "condition": condition,
                            "completed_sessions": completed,
                            "total_sessions": total_sessions,
                            "failure_classification": result["failure_classification"],
                        }
                    )
                    if result["failure_classification"] == "contamination":
                        _write_once_or_match(
                            halt_path,
                            {
                                "status": "halted_on_contamination",
                                "stratum_id": cell_id,
                                "condition": condition,
                                "completed_sessions": completed,
                                "total_sessions": total_sessions,
                            },
                        )
                        raise RuntimeError("W2-61 halted on contamination") from error
                    if (
                        completed_before == 0
                        and completed == 1
                        and _zero_action_platform_defect(receipts)
                    ):
                        _write_once_or_match(
                            halt_path,
                            {
                                "status": "halted_on_first_stratum_zero_action_platform_defect",
                                "stratum_id": cell_id,
                                "condition": condition,
                                "completed_sessions": completed,
                                "total_sessions": total_sessions,
                            },
                        )
                        raise RuntimeError(
                            "W2-61 first in-denominator stratum exposed a zero-action "
                            "platform defect"
                        ) from error
                    continue
                _write_once_or_match(result_path, result)
                completed += 1
                elapsed = time.perf_counter() - started
                rate = completed / elapsed if elapsed > 0.0 else 0.0
                eta_s = (total_sessions - completed) / rate if rate > 0.0 else None
                progress.emit(
                    {
                        "stage": "w2_61_recipient_session_completed",
                        "stratum_id": cell_id,
                        "condition": condition,
                        "completed_sessions": completed,
                        "total_sessions": total_sessions,
                        "throughput_sessions_per_hour": round(rate * 3600.0, 2),
                        "eta_minutes": None if eta_s is None else round(eta_s / 60.0, 1),
                        "elapsed_s": round(elapsed, 1),
                    }
                )


def _condition_row(
    *,
    stratum: Mapping[str, Any],
    condition: str,
    result: Mapping[str, Any] | None,
) -> dict[str, Any]:
    admitted = bool(stratum["admitted"])
    data = stratum.get("inputs")
    truth = data.get("candidate_truth") if isinstance(data, Mapping) else None
    if condition == "autonomous_exploration":
        score = (
            deepcopy(dict(data["existing_autonomous_score"]))
            if admitted and isinstance(data, Mapping)
            else {
                "status": "failed_missing_terminal_ranking",
                "selected_action_query_id": None,
                "selected_rank": None,
                "top1": 0,
                "within_0_01_of_best": 0,
                "raw_regret": None,
                "failure_aware_normalized_regret": 1.0,
                "pairwise_ranking_agreement_excluding_truth_gaps_below_0_01": None,
                "qualified_pair_count": 0,
            }
        )
        status = str(stratum["donor_status"])
        source = "retained_w2_50"
        provider_calls = (
            int(data["existing_autonomous_provider_call_count"])
            if admitted and isinstance(data, Mapping)
            else 0
        )
    elif not admitted and condition in DONOR_DEPENDENT_RECIPIENT_CONDITIONS:
        score = {
            "status": "blocked_on_donor_failure",
            "selected_action_query_id": None,
            "selected_rank": None,
            "top1": 0,
            "within_0_01_of_best": 0,
            "raw_regret": None,
            "failure_aware_normalized_regret": 1.0,
            "pairwise_ranking_agreement_excluding_truth_gaps_below_0_01": None,
            "qualified_pair_count": 0,
        }
        status = "blocked_on_retained_donor_failure"
        source = "blocked_recipient_slot"
        provider_calls = 0
    else:
        ranking = _ranking_from_result(condition, result or {})
        score = score_terminal_ranking(ranking, truth)
        status = str((result or {}).get("status", "not_started"))
        source = "new_w2_61_recipient"
        provider_calls = int((result or {}).get("provider_call_count", 0) or 0)
    return {
        "stratum_id": str(stratum["stratum_id"]),
        "cluster_id": str(stratum["cluster_id"]),
        "task_id": str(stratum["task_id"]),
        "world_seed": int(stratum["world_seed"]),
        "prior_arm": str(stratum["prior_arm"]),
        "condition": condition,
        "source": source,
        "status": status,
        "admitted_stratum": admitted,
        "analysis_eligible": admitted,
        "scheduled_for_execution": condition == "autonomous_exploration"
        or condition in ALWAYS_RECIPIENT_CONDITIONS
        or admitted,
        "provider_call_count": provider_calls,
        **score,
    }


def _mean(values: Sequence[float]) -> float | None:
    return statistics.fmean(values) if values else None


def _quantile(sorted_values: Sequence[float], probability: float) -> float | None:
    if not sorted_values:
        return None
    position = probability * (len(sorted_values) - 1)
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return float(sorted_values[lower])
    weight = position - lower
    return float(sorted_values[lower] * (1.0 - weight) + sorted_values[upper] * weight)


def _condition_summary(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    admitted = [row for row in rows if row["analysis_eligible"]]
    completed = [
        row
        for row in admitted
        if row["status"] in {"completed", "completed_uncontaminated"}
    ]
    ranks = [float(row["selected_rank"]) for row in completed if row["selected_rank"] is not None]
    pairwise = [
        float(row["pairwise_ranking_agreement_excluding_truth_gaps_below_0_01"])
        for row in completed
        if row["pairwise_ranking_agreement_excluding_truth_gaps_below_0_01"] is not None
    ]
    return {
        "admitted_count": len(admitted),
        "completed_count": len(completed),
        "failure_or_incomplete_count": len(admitted) - len(completed),
        "mean_failure_aware_normalized_regret": _mean(
            [float(row["failure_aware_normalized_regret"]) for row in admitted]
        ),
        "mean_selected_rank_completed": _mean(ranks),
        "top1_count": sum(int(row["top1"]) for row in admitted),
        "top1_rate": _mean([float(row["top1"]) for row in admitted]),
        "within_0_01_count": sum(int(row["within_0_01_of_best"]) for row in admitted),
        "within_0_01_rate": _mean(
            [float(row["within_0_01_of_best"]) for row in admitted]
        ),
        "mean_near_tie_aware_pairwise_agreement_completed": _mean(pairwise),
    }


def _paired_contrast(
    *,
    rows: Sequence[Mapping[str, Any]],
    treatment: str,
    control: str,
    expected_pair_count: int,
) -> dict[str, Any]:
    by_stratum: dict[str, dict[str, Mapping[str, Any]]] = defaultdict(dict)
    for row in rows:
        if row["analysis_eligible"]:
            by_stratum[str(row["stratum_id"])][str(row["condition"])] = row
    pairs = []
    for stratum_id, conditions in by_stratum.items():
        if treatment not in conditions or control not in conditions:
            continue
        treatment_row = conditions[treatment]
        control_row = conditions[control]
        pairs.append(
            {
                "stratum_id": stratum_id,
                "cluster_id": str(treatment_row["cluster_id"]),
                "task_id": str(treatment_row["task_id"]),
                "prior_arm": str(treatment_row["prior_arm"]),
                "regret_difference": float(
                    treatment_row["failure_aware_normalized_regret"]
                )
                - float(control_row["failure_aware_normalized_regret"]),
                "top1_difference": int(treatment_row["top1"]) - int(control_row["top1"]),
                "within_0_01_difference": int(treatment_row["within_0_01_of_best"])
                - int(control_row["within_0_01_of_best"]),
            }
        )
    if len(pairs) != expected_pair_count:
        raise ValueError(f"paired contrast {treatment}-{control} lost admitted strata")
    clusters: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for pair in pairs:
        clusters[pair["cluster_id"]].append(pair)
    cluster_ids = sorted(clusters)
    rng = random.Random(f"{BOOTSTRAP_SEED}:{treatment}:{control}")
    bootstrap: list[float] = []
    for _ in range(BOOTSTRAP_REPLICATES):
        sampled_pairs = [
            pair
            for cluster_id in rng.choices(cluster_ids, k=len(cluster_ids))
            for pair in clusters[cluster_id]
        ]
        bootstrap.append(statistics.fmean(pair["regret_difference"] for pair in sampled_pairs))
    bootstrap.sort()
    return {
        "contrast": f"{treatment}_minus_{control}",
        "negative_regret_difference_favors": treatment,
        "paired_stratum_count": len(pairs),
        "task_world_cluster_count": len(cluster_ids),
        "mean_failure_aware_normalized_regret_difference": statistics.fmean(
            pair["regret_difference"] for pair in pairs
        ),
        "task_world_cluster_bootstrap_95_interval": [
            _quantile(bootstrap, 0.025),
            _quantile(bootstrap, 0.975),
        ],
        "mean_top1_difference": statistics.fmean(pair["top1_difference"] for pair in pairs),
        "mean_within_0_01_difference": statistics.fmean(
            pair["within_0_01_difference"] for pair in pairs
        ),
        "wins_ties_losses_on_regret": {
            "wins": sum(pair["regret_difference"] < 0.0 for pair in pairs),
            "ties": sum(pair["regret_difference"] == 0.0 for pair in pairs),
            "losses": sum(pair["regret_difference"] > 0.0 for pair in pairs),
        },
        "by_task": {
            task_id: {
                "paired_stratum_count": len(task_pairs),
                "mean_regret_difference": statistics.fmean(
                    pair["regret_difference"] for pair in task_pairs
                ),
            }
            for task_id in sorted({pair["task_id"] for pair in pairs})
            for task_pairs in [[pair for pair in pairs if pair["task_id"] == task_id]]
        },
        "by_prior_arm": {
            prior_arm: {
                "paired_stratum_count": len(arm_pairs),
                "mean_regret_difference": statistics.fmean(
                    pair["regret_difference"] for pair in arm_pairs
                ),
            }
            for prior_arm in sorted({pair["prior_arm"] for pair in pairs})
            for arm_pairs in [[pair for pair in pairs if pair["prior_arm"] == prior_arm]]
        },
    }


def analyze(*, inputs: Mapping[str, Any], output_root: Path) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    result_status_counts: dict[str, int] = defaultdict(int)
    for stratum in inputs["strata"]:
        cell_id = str(stratum["stratum_id"])
        for condition in DISPLAY_CONDITIONS:
            result = None
            scheduled = condition in stratum["recipient_conditions"]
            if condition != "autonomous_exploration" and scheduled:
                path = _result_path(output_root, cell_id, condition)
                if path.is_file():
                    result = _load(path)
                else:
                    result = {
                        "condition": condition,
                        "status": "not_started",
                        "provider_call_count": 0,
                    }
            row = _condition_row(stratum=stratum, condition=condition, result=result)
            rows.append(row)
            result_status_counts[row["status"]] += 1
    if len(rows) != EXPECTED_SCHEDULED_STRATA * 4:
        raise ValueError("W2-61 condition-slot denominator drifted")

    recipient_rows = [
        row for row in rows if row["source"] == "new_w2_61_recipient"
    ]
    condition_summaries = {
        condition: _condition_summary([row for row in rows if row["condition"] == condition])
        for condition in DISPLAY_CONDITIONS
    }
    expected_new_sessions = int(inputs["new_recipient_session_count"])
    admitted_count = int(inputs["admitted_stratum_count"])
    donor_failure_count = int(inputs["retained_donor_failure_count"])
    all_recipient_terminal = all(
        row["status"] not in {"not_started"} for row in recipient_rows
    ) and len(recipient_rows) == expected_new_sessions
    contrasts = (
        [
            _paired_contrast(
                rows=rows,
                treatment=treatment,
                control=control,
                expected_pair_count=admitted_count,
            )
            for treatment, control in PRIMARY_CONTRASTS
        ]
        if all_recipient_terminal
        else []
    )
    payload = {
        "schema_version": "chemworld-work-ii-w2-61-summary-0.1",
        "study_id": inputs["study_id"],
        "formal_result": False,
        "prospective_development_experiment": True,
        "experiment_note": NOTE_PATH,
        "participant": inputs["participant"],
        "model": inputs["model"],
        "reasoning_effort": inputs["reasoning_effort"],
        "status": "terminal_complete" if all_recipient_terminal else "partial_retained",
        "input_sha256": inputs["input_sha256"],
        "denominators": {
            "scheduled_strata": EXPECTED_SCHEDULED_STRATA,
            "admitted_strata": admitted_count,
            "retained_donor_failures": donor_failure_count,
            "scheduled_condition_slots": EXPECTED_SCHEDULED_STRATA * 4,
            "new_recipient_sessions": expected_new_sessions,
            "terminal_new_recipient_sessions": sum(
                row["status"] != "not_started" for row in recipient_rows
            ),
            "completed_new_recipient_sessions": sum(
                row["status"] == "completed" for row in recipient_rows
            ),
            "failed_or_interrupted_new_recipient_sessions": sum(
                row["status"] not in {"completed", "not_started"} for row in recipient_rows
            ),
            "blocked_recipient_slots": donor_failure_count
            * len(DONOR_DEPENDENT_RECIPIENT_CONDITIONS),
            "new_provider_calls": sum(row["provider_call_count"] for row in recipient_rows),
            "new_physical_experiments": 0,
            "new_truth_executions": 0,
        },
        "result_status_counts_all_180_slots": dict(sorted(result_status_counts.items())),
        "condition_summaries": condition_summaries,
        "primary_paired_contrasts": contrasts,
        "bootstrap": {
            "unit": "task_world_cluster",
            "replicates": BOOTSTRAP_REPLICATES,
            "seed": BOOTSTRAP_SEED,
        },
        "condition_rows": rows,
        "source_binding": deepcopy(inputs["current_binding"]),
    }
    payload["summary_sha256"] = canonical_json_sha256(payload)
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--participant", choices=("deepseek", "codex"), required=True)
    parser.add_argument("--output-root", type=Path)
    parser.add_argument("--report-output", type=Path)
    parser.add_argument("--materialize", action="store_true")
    parser.add_argument("--provider-free-canary", action="store_true")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--analyze", action="store_true")
    parser.add_argument("--allow-provider-execution", action="store_true")
    args = parser.parse_args()
    if not (args.materialize or args.provider_free_canary or args.execute or args.analyze):
        parser.error("select at least one action")
    if args.execute and not args.allow_provider_execution:
        parser.error("provider execution requires --allow-provider-execution")
    selected_output = args.output_root or DEFAULT_OUTPUTS[args.participant]
    selected_report = args.report_output or DEFAULT_REPORTS[args.participant]
    output_root = selected_output if selected_output.is_absolute() else ROOT / selected_output
    report_output = selected_report if selected_report.is_absolute() else ROOT / selected_report
    output_root.mkdir(parents=True, exist_ok=True)
    progress = Progress(output_root / "progress.jsonl")
    inputs = build_inputs(participant=args.participant)
    _write_once_or_match(output_root / "input_bundle.json", inputs)
    progress.emit(
        {
            "stage": "w2_61_materialized",
            "scheduled_strata": EXPECTED_SCHEDULED_STRATA,
            "participant": args.participant,
            "admitted_strata": inputs["admitted_stratum_count"],
            "new_sessions": inputs["new_recipient_session_count"],
            "provider_calls": 0,
            "physical_experiments": 0,
        }
    )
    if args.provider_free_canary:
        canary = provider_free_canary(inputs)
        _write_once_or_match(output_root / "provider_free_canary.json", canary)
        progress.emit({"stage": "w2_61_provider_free_canary_passed", **canary})
    if args.execute:
        execute(inputs=inputs, output_root=output_root, progress=progress)
    if args.execute or args.analyze:
        summary = analyze(inputs=inputs, output_root=output_root)
        write_json_atomic(output_root / "summary.json", summary)
        if summary["status"] == "terminal_complete":
            write_json_atomic(report_output, summary)
        progress.emit(
            {
                "stage": "w2_61_analysis_complete",
                "status": summary["status"],
                **summary["denominators"],
            }
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
