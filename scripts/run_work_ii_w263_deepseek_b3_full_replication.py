#!/usr/bin/env python
"""Run the failure-aware W2-63 DeepSeek B3 full-cohort successor."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from collections.abc import Mapping, Sequence
from copy import deepcopy
from pathlib import Path
from typing import Any

try:
    from scripts.run_work_ii_reviewer_followups import (
        _atomic_json,
        _canonical,
        _prepare_b3_from_provider_free_source,
        _Progress,
        _run_b3_cell,
        _static_provider_check,
        _write_b3_report,
    )
except ModuleNotFoundError:  # direct execution from the scripts directory
    from run_work_ii_reviewer_followups import (
        _atomic_json,
        _canonical,
        _prepare_b3_from_provider_free_source,
        _Progress,
        _run_b3_cell,
        _static_provider_check,
        _write_b3_report,
    )

from chemworld.eval.work_ii_reviewer_followup import summarize_b3_results

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROTOCOL = (
    ROOT / "configs/benchmark/work_ii_w263_deepseek_b3_full_replication_v0.1.json"
)
DEFAULT_SOURCE_ROOT = (
    ROOT
    / "runs/formal/work-ii-as-study-b3-identifiable-law-action-v0.2-20260827-restart1"
)
DEFAULT_OUTPUT_ROOT = (
    ROOT
    / "runs/development/work-ii-w2-63-deepseek-b3-full-replication-v0.1-20260902"
)


def _provider_receipts(result: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    receipts: list[Mapping[str, Any]] = []
    for predecessor in result.get("infrastructure_predecessors", []):
        if isinstance(predecessor, Mapping):
            receipts.extend(
                item
                for item in predecessor.get("provider_receipts", [])
                if isinstance(item, Mapping)
            )
    receipts.extend(
        item
        for item in result.get("provider_receipts", [])
        if isinstance(item, Mapping)
    )
    return receipts


def _tool_event_count(result: Mapping[str, Any]) -> int:
    return sum(int(receipt.get("tool_event_count", 0)) for receipt in _provider_receipts(result))


def _completed_receipt_count(result: Mapping[str, Any]) -> int:
    return sum(receipt.get("status") == "completed" for receipt in _provider_receipts(result))


def _halt_reasons(result: Mapping[str, Any]) -> list[str]:
    reasons: list[str] = []
    tool_events = _tool_event_count(result)
    if tool_events:
        reasons.append(f"tool_contamination:{tool_events}")
    failure = result.get("failure")
    failure = failure if isinstance(failure, Mapping) else {}
    classification = failure.get("classification")
    if (
        result.get("status") != "completed"
        and classification in {"provider_infrastructure", "runner_infrastructure"}
        and not _provider_receipts(result)
    ):
        reasons.append(f"zero_receipt_{classification}")
    return reasons


def _validate_manifest(manifest: Mapping[str, Any]) -> None:
    if manifest.get("cell_count") != 30 or manifest.get("cluster_count") != 5:
        raise ValueError("W2-63 requires exactly 30 cells across five world clusters")
    provider = manifest.get("provider")
    provider = provider if isinstance(provider, Mapping) else {}
    if (
        provider.get("id") != "deepseek"
        or provider.get("model") != "deepseek-v4-flash"
        or provider.get("reasoning_effort") != "high"
    ):
        raise ValueError("W2-63 DeepSeek provider binding differs from the frozen contract")
    cells = manifest.get("cells", [])
    if len(cells) != 30:
        raise ValueError("W2-63 manifest cell list is incomplete")
    if any(cell.get("action_selection_encoding", "query_id") != "query_id" for cell in cells):
        raise ValueError("W2-63 action selection must retain query-ID encoding")
    if any(
        cell.get("stage_status_encoding", "explicit_const") != "explicit_const"
        for cell in cells
    ):
        raise ValueError("W2-63 stage status must retain the W2-56 explicit schema")


def _interrupted_result(cell: Mapping[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {
        "schema_version": "chemworld-work-ii-as-study-b3-cell-result-0.2",
        "study_id": cell["study_id"],
        "phase": "formal",
        "cell_id": cell["cell_id"],
        "cluster_id": cell["cluster_id"],
        "replicate_block_id": cell["replicate_block_id"],
        "replicate_index": int(cell["replicate_index"]),
        "locus": cell["locus"],
        "task_id": cell["task_id"],
        "world_seed": cell["world_seed"],
        "arm": cell["arm"],
        "action_selection_encoding": cell.get("action_selection_encoding", "query_id"),
        "stage_status_encoding": cell.get("stage_status_encoding", "explicit_const"),
        "public_packet_sha256": cell["public_packet_sha256"],
        "participant_physical_experiment_count": 0,
        "status": "failed",
        "failure": {
            "type": "InterruptedMarkedAttempt",
            "message": (
                "attempt marker exists without a terminal result; "
                "provider call is not repeated"
            ),
            "classification": "interrupted_marked",
        },
        "provider_receipts": [],
        "provider_attempt_count": 1,
        "infrastructure_predecessors": [],
    }
    result["result_sha256"] = hashlib.sha256(_canonical(result).encode("utf-8")).hexdigest()
    return result


def _run_summary(
    manifest: Mapping[str, Any],
    results: Sequence[Mapping[str, Any]],
    *,
    status: str,
    halt: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    result_by_id = {str(result["cell_id"]): result for result in results}
    scheduled = [str(cell["cell_id"]) for cell in manifest["cells"]]
    failures = [result for result in results if result.get("status") != "completed"]
    receipts = [receipt for result in results for receipt in _provider_receipts(result)]
    return {
        "schema_version": "chemworld-work-ii-w2-63-run-summary-0.1",
        "status": status,
        "study_id": manifest["study_id"],
        "scheduled_session_count": len(scheduled),
        "terminal_session_count": len(result_by_id),
        "completed_session_count": sum(
            result.get("status") == "completed" for result in results
        ),
        "failure_count": len(failures),
        "missing_session_count": sum(cell_id not in result_by_id for cell_id in scheduled),
        "missing_cell_ids": [cell_id for cell_id in scheduled if cell_id not in result_by_id],
        "failure_cell_ids": [str(result["cell_id"]) for result in failures],
        "provider_receipt_count": len(receipts),
        "completed_provider_receipt_count": sum(
            receipt.get("status") == "completed" for receipt in receipts
        ),
        "tool_event_count": sum(
            int(receipt.get("tool_event_count", 0)) for receipt in receipts
        ),
        "participant_physical_experiment_count": 0,
        "operational_canary_cell_ids": scheduled[:3],
        "operational_canary_terminal_count": sum(
            cell_id in result_by_id for cell_id in scheduled[:3]
        ),
        "halt": deepcopy(dict(halt)) if isinstance(halt, Mapping) else None,
    }


def _load_results(output_root: Path) -> list[dict[str, Any]]:
    return [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted((output_root / "cells").glob("*.json"))
    ]


def _execute(
    manifest: Mapping[str, Any],
    *,
    output_root: Path,
    progress: _Progress,
    resume: bool,
) -> int:
    cells_dir = output_root / "cells"
    attempts_dir = output_root / "attempts"
    cells_dir.mkdir(parents=True, exist_ok=True)
    attempts_dir.mkdir(parents=True, exist_ok=True)
    if not resume and (any(cells_dir.glob("*.json")) or any(attempts_dir.glob("*.json"))):
        raise RuntimeError("W2-63 root already contains attempts; use --resume to preserve them")
    provider = deepcopy(dict(manifest["provider"]))
    provider["infrastructure_retry_limit"] = 0
    started = time.perf_counter()
    total = len(manifest["cells"])
    for index, cell in enumerate(manifest["cells"], start=1):
        result_path = cells_dir / f"{cell['cell_id']}.json"
        marker_path = attempts_dir / f"{cell['cell_id']}.json"
        if result_path.is_file():
            continue
        if marker_path.is_file():
            result = _interrupted_result(cell)
        else:
            _atomic_json(
                marker_path,
                {
                    "schema_version": "chemworld-work-ii-w2-63-attempt-marker-0.1",
                    "cell_id": cell["cell_id"],
                    "manifest_sha256": manifest["manifest_sha256"],
                    "attempt_index": 1,
                },
            )
            result = _run_b3_cell(
                cell,
                provider=provider,
                progress=progress,
                phase="formal",
            )
        _atomic_json(result_path, result)
        reasons = _halt_reasons(result)
        elapsed = max(time.perf_counter() - started, 1.0e-9)
        terminal = len(_load_results(output_root))
        throughput = terminal / elapsed
        progress.emit(
            {
                "stage": "w2_63_progress",
                "cell_id": cell["cell_id"],
                "terminal_sessions": terminal,
                "total_sessions": total,
                "throughput_sessions_per_minute": round(throughput * 60.0, 3),
                "eta_seconds": round((total - terminal) / throughput, 1),
                "halt_reasons": reasons,
            }
        )
        if reasons:
            halt = {
                "schema_version": "chemworld-work-ii-w2-63-halt-0.1",
                "cell_id": cell["cell_id"],
                "manifest_index": index,
                "reasons": reasons,
            }
            _atomic_json(output_root / "halt.json", halt)
            results = _load_results(output_root)
            _atomic_json(
                output_root / "run_summary.json",
                _run_summary(manifest, results, status="halted", halt=halt),
            )
            return 2
    results = _load_results(output_root)
    scientific = summarize_b3_results(manifest, results)
    _atomic_json(output_root / "summary.json", scientific)
    _write_b3_report(scientific, output_root / "REPORT_ZH.md")
    _atomic_json(
        output_root / "run_summary.json",
        _run_summary(manifest, results, status="terminal_complete"),
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--protocol", type=Path, default=DEFAULT_PROTOCOL)
    parser.add_argument("--source-root", type=Path, default=DEFAULT_SOURCE_ROOT)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--prepare", action="store_true")
    parser.add_argument("--static-provider-check", action="store_true")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--analyze", action="store_true")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--allow-provider-execution", action="store_true")
    args = parser.parse_args()
    if not any((args.prepare, args.static_provider_check, args.execute, args.analyze)):
        parser.error("select --prepare, --static-provider-check, --execute, or --analyze")
    protocol = args.protocol if args.protocol.is_absolute() else ROOT / args.protocol
    source_root = args.source_root if args.source_root.is_absolute() else ROOT / args.source_root
    output_root = args.output_root if args.output_root.is_absolute() else ROOT / args.output_root
    output_root.mkdir(parents=True, exist_ok=True)
    progress = _Progress(output_root / "progress.jsonl")
    manifest_path = output_root / "input_manifest.json"
    if args.prepare:
        if manifest_path.is_file() and not args.resume:
            raise RuntimeError("W2-63 manifest is already materialized; use --resume to validate")
        manifest = _prepare_b3_from_provider_free_source(
            protocol,
            source_root=source_root,
            output_root=output_root,
            progress=progress,
        )
    elif manifest_path.is_file():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    else:
        raise RuntimeError("W2-63 requires --prepare before execution or analysis")
    _validate_manifest(manifest)
    if args.static_provider_check:
        static = _static_provider_check(manifest["provider"], output_root=output_root)
        if not static["ready"]:
            return 3
    if args.execute:
        if not args.allow_provider_execution:
            raise RuntimeError("W2-63 provider execution requires --allow-provider-execution")
        if (output_root / "halt.json").is_file():
            raise RuntimeError("W2-63 is halted; do not relaunch without a new authorized block")
        return _execute(manifest, output_root=output_root, progress=progress, resume=args.resume)
    if args.analyze:
        results = _load_results(output_root)
        scientific = summarize_b3_results(manifest, results)
        _atomic_json(output_root / "summary.json", scientific)
        _write_b3_report(scientific, output_root / "REPORT_ZH.md")
        status = "terminal_complete" if len(results) == len(manifest["cells"]) else "partial"
        _atomic_json(
            output_root / "run_summary.json",
            _run_summary(manifest, results, status=status),
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
