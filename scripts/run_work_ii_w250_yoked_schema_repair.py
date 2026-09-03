#!/usr/bin/env python3
"""Repair the provider-facing yoked schema while preserving the original failed attempt."""

from __future__ import annotations

import argparse
import json
import time
from collections.abc import Mapping, Sequence
from copy import deepcopy
from pathlib import Path
from typing import Any

from run_work_ii_evidence_to_action_formal import CodexRecipientSessionClient
from run_work_ii_w250_matched_extension_pilot import (
    DEFAULT_OUTPUT as ORIGINAL_OUTPUT,
)
from run_work_ii_w250_matched_extension_pilot import (
    DONOR_CELL_ID,
    _load,
    _result_path,
    _run_condition,
    _summary,
    _write_once_or_match,
    build_pilot_inputs,
)
from work_ii_longitudinal_runtime import Progress

from chemworld.eval.provenance import canonical_json_sha256
from chemworld.eval.work_ii_evidence_to_action_runtime import yoked_snapshot_output_schema

ROOT = Path(__file__).resolve().parents[1]
PREVIOUS_REPAIR_OUTPUT = (
    ROOT / "runs/development/w2-50-matched-extension-pilot-yoked-schema-repair-20260825"
)
DEFAULT_OUTPUT = (
    ROOT
    / "runs/development/"
    "w2-50-matched-extension-pilot-yoked-opaque-contract-repair-20260825"
)
NOTE_PATH = (
    "workstreams/flagship_tasks/"
    "WORK_II_W250_YOKED_OPAQUE_CONTRACT_REPAIR_EXPERIMENT_NOTE.md"
)
UNCONDITIONAL_BASES = frozenset({"linear", "quadratic", "cubic", "interaction"})


def provider_compatible_yoked_snapshot_schema(
    *,
    stage: str,
    query_metric_contract: Mapping[str, Sequence[str]],
    allowed_feature_ids: Sequence[str],
    allowed_metric_ids: Sequence[str],
    allowed_prior_fields: Sequence[str],
    evidence_catalog: Sequence[str],
    nominal_information_available: bool,
) -> dict[str, Any]:
    """Project the exact validator contract into the provider's supported schema subset."""

    schema = yoked_snapshot_output_schema(
        stage=stage,
        query_metric_contract=query_metric_contract,
        allowed_feature_ids=allowed_feature_ids,
        allowed_metric_ids=allowed_metric_ids,
        allowed_prior_fields=allowed_prior_fields,
        evidence_catalog=evidence_catalog,
        nominal_information_available=nominal_information_available,
    )
    rendered = json.dumps(schema, ensure_ascii=False, sort_keys=True)
    if "oneOf" in rendered or "anyOf" in rendered:
        raise ValueError("provider-compatible yoked schema still contains a union branch")
    return schema


def normalize_nullable_law_terms(payload: Mapping[str, Any]) -> dict[str, Any]:
    """Remove only the null compatibility field before the unchanged typed-law validator."""

    normalized = deepcopy(dict(payload))
    law = normalized.get("law_summary")
    if not isinstance(law, Mapping):
        return normalized
    metric_laws = law.get("metric_laws")
    if not isinstance(metric_laws, list):
        return normalized
    for metric_law in metric_laws:
        if not isinstance(metric_law, dict):
            continue
        terms = metric_law.get("terms")
        if not isinstance(terms, list):
            continue
        for term in terms:
            if (
                isinstance(term, dict)
                and term.get("basis") in UNCONDITIONAL_BASES
                and term.get("category_value") is None
            ):
                term.pop("category_value")
    return normalized


class W250YokedRepairClient(CodexRecipientSessionClient):
    """Use a provider-compatible schema and retain the exact downstream validators."""

    def _schema_for_snapshot(self, context: Mapping[str, Any]) -> dict[str, Any]:
        evidence_ids = [
            str(event["evidence_id"])
            for round_row in context.get("visible_yoked_evidence_rounds", [])
            if isinstance(round_row, Mapping)
            for event in round_row.get("events", [])
            if isinstance(event, Mapping) and isinstance(event.get("evidence_id"), str)
        ]
        return provider_compatible_yoked_snapshot_schema(
            stage=str(context["stage"]),
            query_metric_contract=self.query_metric_contract,
            allowed_feature_ids=self.allowed_feature_ids,
            allowed_metric_ids=self.allowed_metric_ids,
            allowed_prior_fields=self.allowed_prior_fields,
            evidence_catalog=evidence_ids,
            nominal_information_available=self.nominal_information_available,
        )

    def complete_json(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int = 4096,
        output_schema: Mapping[str, Any] | None = None,
    ) -> Any:
        context = json.loads(user_prompt)
        is_snapshot = (
            isinstance(context, Mapping)
            and context.get("condition") == "yoked_evidence"
            and context.get("stage") != "terminal_ranking"
        )
        if is_snapshot:
            system_prompt += (
                "\nFor every law term include category_value. Use null exactly for linear, "
                "quadratic, cubic, and interaction terms; use the actual string or numeric "
                "category for categorical or conditional terms."
            )
        completion = super().complete_json(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            max_tokens=max_tokens,
            output_schema=output_schema,
        )
        return completion


def _original_results(original_root: Path) -> dict[str, dict[str, Any]]:
    results = {
        condition: _load(_result_path(original_root, condition))
        for condition in ("no_evidence", "learned_law_only", "yoked_evidence")
    }
    if results["no_evidence"].get("status") != "completed":
        raise ValueError("original no-evidence result is not complete")
    if results["learned_law_only"].get("status") != "completed":
        raise ValueError("original learned-law-only result is not complete")
    if results["yoked_evidence"].get("status") != "failed_retained":
        raise ValueError("original yoked provider-schema failure is not retained")
    return results


def _thread_ids(root: Path) -> set[str]:
    values: set[str] = set()
    for path in (root / "provider-turns").glob("*/turn-*.json"):
        receipt = _load(path).get("receipt")
        if isinstance(receipt, Mapping) and isinstance(receipt.get("thread_id"), str):
            values.add(str(receipt["thread_id"]))
    return values


def execute_repair(
    *,
    inputs: Mapping[str, Any],
    original_root: Path,
    previous_repair_root: Path,
    output_root: Path,
    progress: Progress,
) -> dict[str, Any]:
    if (output_root / "summary.json").is_file():
        return _load(output_root / "summary.json")
    if (output_root / "provider-turns").exists() or (output_root / "results").exists():
        raise RuntimeError("partial yoked repair output exists and must be retained for inspection")
    original = _original_results(original_root)
    previous_repair = _load(_result_path(previous_repair_root, "yoked_evidence"))
    if previous_repair.get("status") != "failed_retained":
        raise ValueError("previous opaque-contract failure is not retained")
    original_threads = _thread_ids(original_root) | _thread_ids(previous_repair_root)
    started = time.perf_counter()
    progress.emit(
        {
            "stage": "w250_yoked_schema_repair_started",
            "completed_sessions": 0,
            "total_sessions": 1,
            "physical_experiments": 0,
        }
    )
    with W250YokedRepairClient(
        provider=inputs["provider"],
        stratum_id=f"{DONOR_CELL_ID}--yoked-schema-repair",
        output_root=output_root / "provider-turns",
        progress=progress,
        query_metric_contract=inputs["query_metric_contract"],
        allowed_feature_ids=inputs["allowed_feature_ids"],
        allowed_metric_ids=inputs["allowed_metric_ids"],
        allowed_prior_fields=inputs["allowed_prior_fields"],
        nominal_information_available=bool(inputs["nominal_information_available"]),
    ) as client:
        try:
            repaired = _run_condition("yoked_evidence", client=client, inputs=inputs)
        except Exception as error:
            repaired = {
                "condition": "yoked_evidence",
                "status": "failed_retained",
                "failure_type": type(error).__name__,
                "failure_message": str(error),
                "provider_call_count": client.total_provider_call_count,
                "physical_experiment_count": 0,
            }
        _write_once_or_match(_result_path(output_root, "yoked_evidence"), repaired)
        repair_threads = {
            str(receipt["thread_id"])
            for receipt in client.receipts
            if isinstance(receipt.get("thread_id"), str)
        }
        repair_audit = client.session_audit(
            autonomous_thread_id=inputs["donor"]["existing_autonomous_thread_id"],
            autonomous_provider_call_count=int(
                inputs["donor"]["existing_autonomous_provider_call_count"]
            ),
        )
        combined_audit = {
            "original_completed_recipient_threads": 2,
            "repair_yoked_turn_count": sum(
                receipt.get("condition") == "yoked_evidence" for receipt in client.receipts
            ),
            "repair_yoked_same_thread": len(repair_threads) == 1,
            "repair_thread_distinct_from_original_attempts": not (
                repair_threads & original_threads
            ),
            "forbidden_tool_event_count": sum(
                int(receipt.get("tool_event_count", 0)) for receipt in client.receipts
            ),
            "repair_session_audit": repair_audit,
        }
        combined_audit["passed"] = (
            repair_audit.get("passed") is True
            and combined_audit["repair_yoked_turn_count"] == 6
            and combined_audit["repair_yoked_same_thread"] is True
            and combined_audit["repair_thread_distinct_from_original_attempts"] is True
            and combined_audit["forbidden_tool_event_count"] == 0
        )

    combined_results = {
        "no_evidence": original["no_evidence"],
        "learned_law_only": original["learned_law_only"],
        "yoked_evidence": repaired,
    }
    summary = _summary(inputs=inputs, results=combined_results, audit=combined_audit)
    summary.pop("summary_sha256", None)
    summary.update(
        {
            "schema_version": (
                "chemworld-work-ii-w250-matched-extension-yoked-schema-repair-summary-0.1"
            ),
            "experiment_note": NOTE_PATH,
            "original_pilot_root": str(original_root.relative_to(ROOT)).replace("\\", "/"),
            "original_yoked_failure_retained": True,
            "schema_repair_yoked_failure_retained": True,
            "prior_failed_provider_call_count": (
                int(original["yoked_evidence"].get("provider_call_count", 0) or 0)
                + int(previous_repair.get("provider_call_count", 0) or 0)
            ),
            "valid_session_provider_call_count": sum(
                int(row.get("provider_call_count", 0) or 0)
                for row in combined_results.values()
            ),
            "total_provider_attempt_count_including_retained_failures": (
                sum(
                    int(row.get("provider_call_count", 0) or 0)
                    for row in combined_results.values()
                )
                + int(original["yoked_evidence"].get("provider_call_count", 0) or 0)
                + int(previous_repair.get("provider_call_count", 0) or 0)
            ),
            "repair_elapsed_s": round(time.perf_counter() - started, 1),
        }
    )
    summary["summary_sha256"] = canonical_json_sha256(summary)
    _write_once_or_match(output_root / "summary.json", summary)
    progress.emit(
        {
            "stage": "w250_yoked_schema_repair_terminal",
            "completed_sessions": int(repaired.get("status") == "completed"),
            "total_sessions": 1,
            "repair_provider_calls": repaired.get("provider_call_count", 0),
            "total_provider_attempts": summary[
                "total_provider_attempt_count_including_retained_failures"
            ],
            "physical_experiments": 0,
            "elapsed_s": summary["repair_elapsed_s"],
        }
    )
    return summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--original-root", type=Path, default=ORIGINAL_OUTPUT)
    parser.add_argument(
        "--previous-repair-root", type=Path, default=PREVIOUS_REPAIR_OUTPUT
    )
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--materialize", action="store_true")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--allow-provider-execution", action="store_true")
    args = parser.parse_args()
    if not (args.materialize or args.execute):
        parser.error("select --materialize or --execute")
    if args.execute and not args.allow_provider_execution:
        parser.error("provider execution requires --allow-provider-execution")
    original_root = (
        args.original_root if args.original_root.is_absolute() else ROOT / args.original_root
    ).resolve()
    previous_repair_root = (
        args.previous_repair_root
        if args.previous_repair_root.is_absolute()
        else ROOT / args.previous_repair_root
    ).resolve()
    output_root = (
        args.output_root if args.output_root.is_absolute() else ROOT / args.output_root
    ).resolve()
    output_root.mkdir(parents=True, exist_ok=True)
    inputs = build_pilot_inputs()
    original_summary = _load(original_root / "summary.json")
    previous_repair_summary = _load(previous_repair_root / "summary.json")
    binding = {
        "schema_version": "chemworld-work-ii-w250-yoked-schema-repair-input-0.1",
        "study_id": inputs["study_id"],
        "experiment_note": NOTE_PATH,
        "donor_cell_id": inputs["donor"]["cell_id"],
        "pilot_input_sha256": inputs["input_sha256"],
        "original_pilot_summary_sha256": original_summary["summary_sha256"],
        "previous_repair_summary_sha256": previous_repair_summary["summary_sha256"],
        "fixed_condition": "yoked_evidence",
        "fixed_session_count": 1,
        "fixed_turn_count": 6,
        "new_physical_experiment_count": 0,
    }
    binding["input_binding_sha256"] = canonical_json_sha256(binding)
    _write_once_or_match(output_root / "input_binding.json", binding)
    progress = Progress(output_root / "progress.jsonl")
    progress.emit(
        {
            "stage": "w250_yoked_schema_repair_materialized",
            "sessions": 1,
            "turns": 6,
            "provider_calls": 0,
            "physical_experiments": 0,
        }
    )
    if args.execute:
        execute_repair(
            inputs=inputs,
            original_root=original_root,
            previous_repair_root=previous_repair_root,
            output_root=output_root,
            progress=progress,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
