#!/usr/bin/env python3
"""Run three W2-50-matched non-oracle recipient sessions without rerunning the donor."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from collections.abc import Mapping
from copy import deepcopy
from pathlib import Path
from typing import Any

from run_work_ii_evidence_to_action_formal import (
    CodexRecipientSessionClient,
    _autonomous_thread_id,
    _public_task_contract_for_config,
)
from work_ii_longitudinal_runtime import Progress

from chemworld.data.logging import load_jsonl
from chemworld.eval.provenance import canonical_json_sha256, write_json_atomic
from chemworld.eval.work_ii_evidence_to_action import score_terminal_ranking
from chemworld.eval.work_ii_evidence_to_action_runtime import (
    build_donor_derivatives,
    build_recipient_context,
    execute_terminal_recipient,
    execute_yoked_recipient,
)

ROOT = Path(__file__).resolve().parents[1]
DONOR_ROOT = (
    ROOT
    / "runs/formal/work-ii-deepseek-multi-task-open-action-five-world-v0.1-20260817-formal2"
)
DONOR_CELL_ID = "A_S_MULTI_TASK_OAD--electrochemical-conversion--seed0--opaque"
CONDITION_ORDER = ("no_evidence", "learned_law_only", "yoked_evidence")
DEFAULT_OUTPUT = ROOT / "runs/development/w2-50-matched-extension-pilot-20260825"
NOTE_PATH = (
    "workstreams/flagship_tasks/"
    "WORK_II_W250_MATCHED_EXTENSION_PILOT_EXPERIMENT_NOTE.md"
)


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain one JSON object")
    return value


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _write_once_or_match(path: Path, payload: Mapping[str, Any]) -> None:
    normalized = deepcopy(dict(payload))
    if path.is_file():
        if _load(path) != normalized:
            raise RuntimeError(f"retained pilot artifact differs: {path}")
        return
    write_json_atomic(path, normalized)


def _first_matching_row(
    rows: object,
    *,
    key: str,
    value: str,
) -> dict[str, Any]:
    if not isinstance(rows, list):
        raise ValueError("expected a list of donor records")
    matches = [dict(row) for row in rows if isinstance(row, Mapping) and row.get(key) == value]
    if len(matches) != 1:
        raise ValueError(f"expected one donor record for {key}={value}")
    return matches[0]


def _sanitized_task_contract(config: Mapping[str, Any], *, world_seed: int) -> dict[str, Any]:
    contract = _public_task_contract_for_config(config, world_seed=world_seed)
    terminal = deepcopy(dict(contract.get("terminal_decision_contract", {})))
    candidates = terminal.pop("candidate_queries", None)
    if not isinstance(candidates, list) or len(candidates) != 8:
        raise ValueError("W2-50 terminal contract lacks eight public candidates")
    terminal.pop("contract_sha256", None)
    terminal["candidate_count"] = len(candidates)
    terminal["candidate_packet_reveal"] = "condition_specific_recipient_context"
    contract["terminal_decision_contract"] = terminal
    return contract


def _candidate_packet(config: Mapping[str, Any]) -> dict[str, Any]:
    terminal = config.get("terminal_action_readout")
    terminal = terminal if isinstance(terminal, Mapping) else {}
    raw = terminal.get("candidate_queries")
    candidates = [deepcopy(dict(row)) for row in raw] if isinstance(raw, list) else []
    query_ids = [str(row.get("query_id")) for row in candidates]
    if len(candidates) != 8 or len(set(query_ids)) != 8:
        raise ValueError("W2-50 candidate packet is incomplete")
    forbidden = {
        "candidate_pool_ranks",
        "candidate_truth",
        "hidden_evaluator_fields",
        "presented_candidate_ranks",
    }
    if any(forbidden & set(map(str, row)) for row in candidates):
        raise ValueError("W2-50 public candidate packet contains hidden evaluator fields")
    return {
        "schema_version": "chemworld-work-ii-w250-public-candidate-packet-0.1",
        "task_id": str(config["task_id"]),
        "world_seed": int(config["world_seed"]),
        "candidate_outcomes_included": False,
        "candidate_ranks_included": False,
        "candidates": candidates,
    }


def build_pilot_inputs(*, donor_root: Path = DONOR_ROOT) -> dict[str, Any]:
    """Materialize the fixed donor products and public recipient inputs without provider calls."""

    manifest_path = donor_root / "input_manifest.json"
    summary_path = donor_root / "summary.json"
    manifest = _load(manifest_path)
    summary = _load(summary_path)
    cells = manifest.get("cells")
    if not isinstance(cells, list) or not cells:
        raise ValueError("W2-50 input manifest has no cells")
    first_cell = cells[0]
    if not isinstance(first_cell, Mapping) or first_cell.get("cell_id") != DONOR_CELL_ID:
        raise ValueError("the deterministic first W2-50 cell differs from the frozen pilot donor")
    manifest_cell = dict(first_cell)
    summary_cell = _first_matching_row(
        summary.get("cell_rows"), key="cell_id", value=DONOR_CELL_ID
    )
    if summary_cell.get("status") != "completed_uncontaminated":
        raise ValueError("the fixed W2-50 pilot donor is not eligible")
    if int(summary_cell.get("campaign_complete_experiment_count", 0)) != 12:
        raise ValueError("the fixed W2-50 pilot donor did not complete 12 experiments")
    ranking = summary_cell.get("participant_ranking")
    if not isinstance(ranking, list) or len(ranking) != 8 or len(set(map(str, ranking))) != 8:
        raise ValueError("the fixed W2-50 pilot donor lacks a complete terminal ranking")

    config_path = donor_root / str(manifest_cell["campaign_config_path"])
    config = _load(config_path)
    trajectory_path = donor_root / "formal/campaigns" / DONOR_CELL_ID / "trajectory.jsonl"
    trajectory = load_jsonl(trajectory_path)
    packet = _candidate_packet(config)
    candidate_ids = [str(row["query_id"]) for row in packet["candidates"]]
    donor_result = {
        "status": str(summary_cell["status"]),
        "campaign_summary": deepcopy(dict(summary_cell["campaign_summary"])),
    }
    derivatives = build_donor_derivatives(
        donor_cell_id=DONOR_CELL_ID,
        donor_result=donor_result,
        trajectory_rows=trajectory,
        candidate_query_ids=candidate_ids,
    )
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
        raise ValueError("W2-50 donor checkpoint contract does not contain eight queries")
    arm = str(summary_cell["arm"])
    prior = config.get("prior_arms")
    prior = prior if isinstance(prior, Mapping) else {}
    arm_config = prior.get(arm)
    if not isinstance(arm_config, Mapping) or not isinstance(
        arm_config.get("initial_world_model"), Mapping
    ):
        raise ValueError("W2-50 donor initial world model is missing")
    candidate_truth = manifest_cell.get("candidate_truth")
    if not isinstance(candidate_truth, Mapping):
        raise ValueError("W2-50 donor candidate truth is missing")
    donor_score = score_terminal_ranking(ranking, candidate_truth)
    if donor_score["selected_rank"] != summary_cell.get("selected_rank"):
        raise ValueError("recomputed W2-50 donor rank differs from the retained summary")

    payload = {
        "schema_version": "chemworld-work-ii-w250-matched-extension-pilot-input-0.1",
        "study_id": "work-ii-w250-matched-extension-pilot-20260825",
        "formal_result": False,
        "development_pilot": True,
        "experiment_note": NOTE_PATH,
        "condition_order": list(CONDITION_ORDER),
        "new_session_count": 3,
        "new_physical_experiment_count": 0,
        "donor": {
            "cell_id": DONOR_CELL_ID,
            "task_id": str(manifest_cell["task_id"]),
            "world_seed": int(manifest_cell["world_seed"]),
            "prior_arm": arm,
            "status": str(summary_cell["status"]),
            "existing_autonomous_score": donor_score,
            "existing_autonomous_thread_id": _autonomous_thread_id(summary_cell),
            "existing_autonomous_provider_call_count": int(
                summary_cell["campaign_summary"]
                .get("method_resources", {})
                .get("provider_session_count", 0)
                or 0
            ),
            "input_manifest_sha256": _sha256_file(manifest_path),
            "summary_sha256": _sha256_file(summary_path),
            "cell_result_sha256": summary_cell.get("result_sha256"),
            "trajectory_sha256": _sha256_file(trajectory_path),
        },
        "provider": deepcopy(dict(config["provider"])),
        "task_contract": _sanitized_task_contract(
            config, world_seed=int(manifest_cell["world_seed"])
        ),
        "initial_world_model": deepcopy(dict(arm_config["initial_world_model"])),
        "candidate_packet": packet,
        "candidate_truth": deepcopy(dict(candidate_truth)),
        "query_metric_contract": query_metric_contract,
        "allowed_feature_ids": [str(item) for item in checkpoint["allowed_feature_ids"]],
        "allowed_metric_ids": [str(item) for item in checkpoint["allowed_metric_ids"]],
        "allowed_prior_fields": [str(item) for item in checkpoint["allowed_prior_fields"]],
        "nominal_information_available": (
            arm_config["initial_world_model"].get("availability")
            != "opaque_for_target_locus"
        ),
        "donor_derivatives": derivatives,
    }
    payload["input_sha256"] = canonical_json_sha256(payload)
    return payload


def _ranking_from_result(condition: str, result: Mapping[str, Any]) -> list[str] | None:
    source: object = result
    if condition == "yoked_evidence":
        source = result.get("terminal_result")
    if not isinstance(source, Mapping):
        return None
    submission = source.get("submission")
    if not isinstance(submission, Mapping) or not isinstance(submission.get("ranking"), list):
        return None
    return [str(item) for item in submission["ranking"]]


def _result_path(output_root: Path, condition: str) -> Path:
    return output_root / "results" / f"{condition}.json"


def _run_condition(
    condition: str,
    *,
    client: CodexRecipientSessionClient,
    inputs: Mapping[str, Any],
) -> dict[str, Any]:
    common = {
        "task_contract": inputs["task_contract"],
        "initial_world_model": inputs["initial_world_model"],
        "candidate_packet": inputs["candidate_packet"],
    }
    if condition == "no_evidence":
        context = build_recipient_context(
            condition=condition,
            stage="terminal_ranking",
            **common,
        )
        result = execute_terminal_recipient(client, context)
        return {**result, "physical_experiment_count": 0, "provider_call_count": 1}
    if condition == "learned_law_only":
        context = build_recipient_context(
            condition=condition,
            stage="terminal_ranking",
            law_artifact=inputs["donor_derivatives"]["learned_law_artifact"],
            **common,
        )
        result = execute_terminal_recipient(client, context)
        return {**result, "physical_experiment_count": 0, "provider_call_count": 1}
    if condition == "yoked_evidence":
        return execute_yoked_recipient(
            client,
            yoked_evidence_packet=inputs["donor_derivatives"]["yoked_evidence_packet"],
            query_metric_contract=inputs["query_metric_contract"],
            allowed_feature_ids=inputs["allowed_feature_ids"],
            allowed_metric_ids=inputs["allowed_metric_ids"],
            allowed_prior_fields=inputs["allowed_prior_fields"],
            nominal_information_available=bool(inputs["nominal_information_available"]),
            **common,
        )
    raise ValueError(f"unsupported pilot condition: {condition}")


def _summary(
    *,
    inputs: Mapping[str, Any],
    results: Mapping[str, Mapping[str, Any]],
    audit: Mapping[str, Any],
) -> dict[str, Any]:
    rows = [
        {
            "condition": "autonomous_exploration",
            "source": "retained_w2_50",
            "status": inputs["donor"]["status"],
            **deepcopy(dict(inputs["donor"]["existing_autonomous_score"])),
        }
    ]
    scores: dict[str, Mapping[str, Any]] = {
        "autonomous_exploration": inputs["donor"]["existing_autonomous_score"]
    }
    for condition in CONDITION_ORDER:
        result = results.get(condition)
        if not isinstance(result, Mapping):
            rows.append({"condition": condition, "source": "new_pilot", "status": "not_started"})
            continue
        ranking = _ranking_from_result(condition, result)
        score = score_terminal_ranking(ranking, inputs["candidate_truth"])
        rows.append(
            {
                "condition": condition,
                "source": "new_pilot",
                "status": str(result.get("status", score["status"])),
                **score,
            }
        )
        scores[condition] = score
    contrasts = []
    for treatment, control in (
        ("yoked_evidence", "no_evidence"),
        ("learned_law_only", "no_evidence"),
        ("autonomous_exploration", "yoked_evidence"),
        ("autonomous_exploration", "no_evidence"),
    ):
        if treatment not in scores or control not in scores:
            continue
        contrasts.append(
            {
                "contrast": f"{treatment}_minus_{control}",
                "normalized_regret_difference": (
                    float(scores[treatment]["failure_aware_normalized_regret"])
                    - float(scores[control]["failure_aware_normalized_regret"])
                ),
            }
        )
    payload = {
        "schema_version": "chemworld-work-ii-w250-matched-extension-pilot-summary-0.1",
        "study_id": inputs["study_id"],
        "formal_result": False,
        "development_pilot": True,
        "donor_cell_id": inputs["donor"]["cell_id"],
        "fixed_new_session_count": 3,
        "attempted_new_session_count": len(results),
        "completed_new_session_count": sum(
            row.get("status") == "completed" for row in results.values()
        ),
        "provider_call_count": sum(
            int(row.get("provider_call_count", 0) or 0) for row in results.values()
        ),
        "new_physical_experiment_count": 0,
        "condition_rows": rows,
        "single_stratum_contrasts": contrasts,
        "fresh_session_audit": deepcopy(dict(audit)),
    }
    payload["summary_sha256"] = canonical_json_sha256(payload)
    return payload


def execute_pilot(
    *,
    inputs: Mapping[str, Any],
    output_root: Path,
    progress: Progress,
) -> dict[str, Any]:
    if (output_root / "summary.json").is_file():
        return _load(output_root / "summary.json")
    if (output_root / "provider-turns").exists() or (output_root / "results").exists():
        raise RuntimeError("partial pilot output exists and must be retained for inspection")
    results: dict[str, dict[str, Any]] = {}
    audit: dict[str, Any] = {}
    started = time.perf_counter()
    with CodexRecipientSessionClient(
        provider=inputs["provider"],
        stratum_id=str(inputs["donor"]["cell_id"]),
        output_root=output_root / "provider-turns",
        progress=progress,
        query_metric_contract=inputs["query_metric_contract"],
        allowed_feature_ids=inputs["allowed_feature_ids"],
        allowed_metric_ids=inputs["allowed_metric_ids"],
        allowed_prior_fields=inputs["allowed_prior_fields"],
        nominal_information_available=bool(inputs["nominal_information_available"]),
    ) as client:
        for index, condition in enumerate(CONDITION_ORDER, start=1):
            progress.emit(
                {
                    "stage": "w250_matched_extension_condition_started",
                    "condition": condition,
                    "completed_sessions": index - 1,
                    "total_sessions": len(CONDITION_ORDER),
                }
            )
            try:
                result = _run_condition(condition, client=client, inputs=inputs)
            except Exception as error:
                result = {
                    "condition": condition,
                    "status": "failed_retained",
                    "failure_type": type(error).__name__,
                    "failure_message": str(error),
                    "provider_call_count": max(
                        0,
                        client.total_provider_call_count
                        - sum(
                            int(row.get("provider_call_count", 0) or 0)
                            for row in results.values()
                        ),
                    ),
                    "physical_experiment_count": 0,
                }
                _write_once_or_match(_result_path(output_root, condition), result)
                results[condition] = result
                progress.emit(
                    {
                        "stage": "w250_matched_extension_condition_failed",
                        "condition": condition,
                        "completed_sessions": index - 1,
                        "total_sessions": len(CONDITION_ORDER),
                        "failure_type": type(error).__name__,
                    }
                )
                break
            _write_once_or_match(_result_path(output_root, condition), result)
            results[condition] = result
            progress.emit(
                {
                    "stage": "w250_matched_extension_condition_completed",
                    "condition": condition,
                    "completed_sessions": index,
                    "total_sessions": len(CONDITION_ORDER),
                    "elapsed_s": round(time.perf_counter() - started, 1),
                }
            )
        audit = client.session_audit(
            autonomous_thread_id=inputs["donor"]["existing_autonomous_thread_id"],
            autonomous_provider_call_count=int(
                inputs["donor"]["existing_autonomous_provider_call_count"]
            ),
        )
    summary = _summary(inputs=inputs, results=results, audit=audit)
    _write_once_or_match(output_root / "summary.json", summary)
    progress.emit(
        {
            "stage": "w250_matched_extension_pilot_terminal",
            "completed_sessions": summary["completed_new_session_count"],
            "total_sessions": summary["fixed_new_session_count"],
            "provider_calls": summary["provider_call_count"],
            "physical_experiments": 0,
            "elapsed_s": round(time.perf_counter() - started, 1),
        }
    )
    return summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--donor-root", type=Path, default=DONOR_ROOT)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--materialize", action="store_true")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--allow-provider-execution", action="store_true")
    args = parser.parse_args()
    if not (args.materialize or args.execute):
        parser.error("select --materialize or --execute")
    if args.execute and not args.allow_provider_execution:
        parser.error("provider execution requires --allow-provider-execution")
    donor_root = args.donor_root if args.donor_root.is_absolute() else ROOT / args.donor_root
    output_root = args.output_root if args.output_root.is_absolute() else ROOT / args.output_root
    output_root.mkdir(parents=True, exist_ok=True)
    progress = Progress(output_root / "progress.jsonl")
    inputs = build_pilot_inputs(donor_root=donor_root.resolve())
    _write_once_or_match(output_root / "input_bundle.json", inputs)
    progress.emit(
        {
            "stage": "w250_matched_extension_materialized",
            "donor_cell_id": DONOR_CELL_ID,
            "new_sessions": 3,
            "physical_experiments": 0,
            "provider_calls": 0,
        }
    )
    if args.execute:
        execute_pilot(inputs=inputs, output_root=output_root, progress=progress)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
