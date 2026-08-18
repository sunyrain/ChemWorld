#!/usr/bin/env python
"""Run paired terminal-only schema replays under one fixed correct context."""

from __future__ import annotations

import argparse
import hashlib
import json
import tempfile
import time
from collections.abc import Mapping, Sequence
from concurrent.futures import ThreadPoolExecutor, as_completed
from copy import deepcopy
from pathlib import Path
from typing import Any

from run_work_ii_study_b import (
    _atomic_json,
    _canonical,
    _initial_command,
    _launch_turn,
    _ParticipantSchemaError,
    _prepare_codex_home,
    _Progress,
    _ProviderInfrastructureError,
)

from chemworld.eval.work_ii_terminal_schema_canary import (
    CANARY_VERSION,
    CONDITIONS,
    evaluate_terminal_payload,
    summarize_fixed_context_replay,
    terminal_output_schema,
    validate_terminal_payload,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = (
    ROOT
    / "runs/formal/work-ii-as-study-b4-law-guided-decision-v0.1-20260816/input_manifest.json"
)
DEFAULT_OUTPUT = (
    ROOT
    / "runs/development/work-ii-terminal-schema-fixed-context-replay-v0.1-20260816"
)
TARGET_CLUSTER = "A_S_B4--partition-discovery--seed368103785"
FIXED_LAW = {
    "mechanism_family": "FAMILY_B_POWER",
    "reference_exponent": 1.75,
    "law_type": "reference_coefficient_power",
    "law_statement": (
        "D_effective = D_reference ^ 1.75 * process_factor; infer the public process-factor "
        "dependence from the fixed evidence rows"
    ),
}


def _prompt(cell: Mapping[str, Any], *, condition: str) -> str:
    packet = cell["public_packet"]
    public = {
        "task_id": cell["task_id"],
        "fixed_mechanism_law": FIXED_LAW,
        "metric_range": packet["metric_range"],
        "fixed_evidence": packet["evidence"],
        "outcome_hidden_candidates": packet["unseen_action_candidates"],
        "selection_rule": "rank all eight candidates exactly once and select ranking[0]",
    }
    prediction_instruction = (
        "Predict all four published metrics for every candidate, then "
        if condition == "full_32"
        else "Do not submit per-candidate numeric predictions; "
    )
    return (
        "You are a scientific participant in a development-only terminal contract replay. Do not "
        "use tools, shell, files, web, apps, plugins, or MCP. The evaluator supplies one frozen "
        "correct mechanism law and fixed visible evidence; do not revise or re-identify the law. "
        + prediction_instruction
        + "return a complete unique ranking, select exactly ranking[0], report selection "
        "confidence, and briefly explain how the frozen law and evidence determine the order. "
        "Candidate outcomes "
        "and ranks are hidden. Return only schema-conforming JSON.\n\nFIXED_CONTEXT:\n"
        + json.dumps(public, ensure_ascii=False, sort_keys=True)
    )


def _run_attempt(
    cell: Mapping[str, Any],
    *,
    condition: str,
    replicate: int,
    provider: Mapping[str, Any],
    progress: _Progress,
) -> dict[str, Any]:
    cell_id = f"terminal-fixed-r{replicate}--{condition}"
    started = time.perf_counter()
    progress.emit(
        {"stage": "terminal_fixed_cell_started", "cell_id": cell_id, "condition": condition}
    )
    result: dict[str, Any] = {
        "schema_version": CANARY_VERSION,
        "study_id": "work-ii-terminal-schema-fixed-context-replay-v0.1",
        "cell_id": cell_id,
        "cluster_id": cell["cluster_id"],
        "world_seed": cell["world_seed"],
        "replicate": replicate,
        "condition": condition,
        "fixed_law": deepcopy(FIXED_LAW),
        "public_packet_sha256": cell["public_packet_sha256"],
        "participant_physical_experiment_count": 0,
    }
    receipts: list[dict[str, Any]] = []
    try:
        with tempfile.TemporaryDirectory(prefix="chemworld-terminal-fixed-replay-") as temporary:
            temp_root = Path(temporary)
            workspace = temp_root / "workspace"
            workspace.mkdir()
            environment = _prepare_codex_home(temp_root, provider)
            schema_path = temp_root / "terminal.schema.json"
            queries = cell["public_packet"]["unseen_action_candidates"]
            _atomic_json(schema_path, terminal_output_schema(queries, condition=condition))
            command = _initial_command(provider, schema_path, workspace)

            def liveness(payload: dict[str, Any]) -> None:
                progress.emit(
                    {
                        "stage": "terminal_fixed_turn_liveness",
                        "cell_id": cell_id,
                        "condition": condition,
                        **payload,
                    }
                )

            turn = _launch_turn(
                command,
                _prompt(cell, condition=condition),
                cwd=workspace,
                environment=environment,
                timeout_s=float(provider["request_timeout_s"]),
                liveness=liveness,
            )
            receipts.append({key: value for key, value in turn.items() if key != "final_payload"})
            payload = turn.get("final_payload")
            errors = (
                validate_terminal_payload(payload, queries, condition=condition)
                if isinstance(payload, Mapping)
                else ["terminal final payload is unavailable"]
            )
            if turn.get("status") != "completed":
                raise _ProviderInfrastructureError("fixed-context terminal turn did not complete")
            if errors:
                raise _ParticipantSchemaError("; ".join(errors))
            assert isinstance(payload, Mapping)
            result.update(
                {
                    "status": "completed",
                    "terminal_submission": deepcopy(dict(payload)),
                    "terminal_evaluation": evaluate_terminal_payload(
                        cell, payload, condition=condition
                    ),
                    "provider_receipts": receipts,
                }
            )
    except Exception as error:
        result.update(
            {
                "status": "failed",
                "failure": {
                    "type": type(error).__name__,
                    "message": str(error)[:2000],
                    "classification": (
                        "provider_infrastructure"
                        if isinstance(error, _ProviderInfrastructureError)
                        else "participant_schema"
                        if isinstance(error, _ParticipantSchemaError)
                        else "runner_infrastructure"
                    ),
                },
                "provider_receipts": receipts,
            }
        )
    result["elapsed_s"] = round(time.perf_counter() - started, 3)
    result["result_sha256"] = hashlib.sha256(_canonical(result).encode("utf-8")).hexdigest()
    progress.emit(
        {
            "stage": "terminal_fixed_cell_terminal",
            "cell_id": cell_id,
            "condition": condition,
            "status": result["status"],
            "elapsed_s": result["elapsed_s"],
        }
    )
    return result


def _run_cell(
    cell: Mapping[str, Any],
    *,
    condition: str,
    replicate: int,
    provider: Mapping[str, Any],
    progress: _Progress,
) -> dict[str, Any]:
    retry_limit = int(provider.get("infrastructure_retry_limit", 0))
    predecessors: list[dict[str, Any]] = []
    for attempt_index in range(retry_limit + 1):
        result = _run_attempt(
            cell,
            condition=condition,
            replicate=replicate,
            provider=provider,
            progress=progress,
        )
        result["provider_attempt_index"] = attempt_index + 1
        failure = result.get("failure")
        classification = failure.get("classification") if isinstance(failure, Mapping) else None
        retryable = classification in {"provider_infrastructure", "runner_infrastructure"}
        if result.get("status") == "completed" or not retryable or attempt_index >= retry_limit:
            result["provider_attempt_count"] = attempt_index + 1
            result["infrastructure_predecessors"] = predecessors
            result.pop("result_sha256", None)
            result["result_sha256"] = hashlib.sha256(
                _canonical(result).encode("utf-8")
            ).hexdigest()
            return result
        predecessors.append(
            {
                "provider_attempt_index": attempt_index + 1,
                "failure": deepcopy(result.get("failure")),
                "provider_receipts": deepcopy(result.get("provider_receipts", [])),
                "elapsed_s": result.get("elapsed_s"),
                "result_sha256": result.get("result_sha256"),
            }
        )
        progress.emit(
            {
                "stage": "terminal_fixed_infrastructure_retry",
                "cell_id": result["cell_id"],
                "completed_attempts": attempt_index + 1,
                "maximum_attempts": retry_limit + 1,
            }
        )
    raise AssertionError("unreachable fixed-context replay retry loop")


def _schedule(cell: Mapping[str, Any]) -> list[tuple[Mapping[str, Any], str, int]]:
    return [
        (cell, "full_32", 1),
        (cell, "lean_ranking", 2),
        (cell, "full_32", 3),
        (cell, "lean_ranking", 1),
        (cell, "full_32", 2),
        (cell, "lean_ranking", 3),
    ]


def _execute(
    scheduled: Sequence[tuple[Mapping[str, Any], str, int]],
    *,
    provider: Mapping[str, Any],
    output: Path,
    progress: _Progress,
    workers: int,
    resume: bool,
) -> list[dict[str, Any]]:
    cell_root = output / "cells"
    cell_root.mkdir(parents=True, exist_ok=True)
    results: list[dict[str, Any]] = []
    pending: list[tuple[Mapping[str, Any], str, int]] = []
    for cell, condition, replicate in scheduled:
        cell_id = f"terminal-fixed-r{replicate}--{condition}"
        path = cell_root / f"{cell_id}.json"
        if resume and path.is_file():
            results.append(json.loads(path.read_text(encoding="utf-8")))
        else:
            pending.append((cell, condition, replicate))
    completed = len(results)
    started = time.perf_counter()
    progress.emit(
        {
            "stage": "terminal_fixed_execution_started",
            "completed_sessions": completed,
            "total_sessions": len(scheduled),
            "workers": workers,
        }
    )
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(
                _run_cell,
                cell,
                condition=condition,
                replicate=replicate,
                provider=provider,
                progress=progress,
            ): (cell, condition, replicate)
            for cell, condition, replicate in pending
        }
        for future in as_completed(futures):
            result = future.result()
            _atomic_json(cell_root / f"{result['cell_id']}.json", result)
            results.append(result)
            completed += 1
            elapsed = max(time.perf_counter() - started, 1.0e-9)
            throughput = completed / elapsed
            progress.emit(
                {
                    "stage": "terminal_fixed_progress",
                    "cell_id": result["cell_id"],
                    "completed_sessions": completed,
                    "total_sessions": len(scheduled),
                    "failed_sessions": sum(
                        item.get("status") != "completed" for item in results
                    ),
                    "throughput_sessions_per_minute": round(throughput * 60.0, 3),
                    "eta_seconds": (
                        round((len(scheduled) - completed) / throughput, 1)
                        if throughput > 0
                        else None
                    ),
                }
            )
    return sorted(results, key=lambda item: str(item["cell_id"]))


def _write_report(summary: Mapping[str, Any], path: Path) -> None:
    lines = [
        "# Work II terminal schema fixed-context replay",
        "",
        f"状态: `{summary['status']}`; 完成 {summary['completed_session_count']}/"
        f"{summary['scheduled_session_count']} sessions。",
        "",
        "| condition | 完成 | payload failure | provider-error associated | output tokens | "
        "elapsed s | 平均选择排名 | normalized regret | Kendall tau | prediction MAE |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for condition in CONDITIONS:
        row = summary["by_condition"][condition]

        def show(value: Any, digits: int = 3) -> str:
            return "n/a" if value is None else f"{float(value):.{digits}f}"

        lines.append(
            f"| {condition} | {row['completed_session_count']}/"
            f"{row['scheduled_session_count']} | {row['participant_schema_failure_count']} | "
            f"{row['provider_error_associated_failure_count']} | "
            f"{show(row['mean_output_tokens'], 1)} | {show(row['mean_elapsed_s'], 1)} | "
            f"{show(row['mean_selected_rank'])} | "
            f"{show(row['mean_normalized_regret'], 4)} | "
            f"{show(row['mean_ranking_kendall_tau'], 4)} | "
            f"{show(row['mean_prediction_mae'], 4)} |"
        )
    lines.extend(
        [
            "",
            "该结果固定并直接提供正确机制, 只诊断 terminal output contract; "
            "不测机制发现或纵向学习。",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-manifest", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--analyze", action="store_true")
    parser.add_argument("--allow-provider-execution", action="store_true")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--workers", type=int, default=3)
    args = parser.parse_args()
    if not args.execute and not args.analyze:
        parser.error("select --execute or --analyze")
    if not 1 <= args.workers <= 3:
        parser.error("--workers must be between 1 and 3")
    if args.execute and not args.allow_provider_execution:
        parser.error("--execute requires --allow-provider-execution")
    source = args.source_manifest.resolve()
    if not source.is_file():
        raise FileNotFoundError(f"source B4 manifest is unavailable: {source}")
    manifest = json.loads(source.read_text(encoding="utf-8"))
    source_cells = [
        cell for cell in manifest["cells"] if cell.get("cluster_id") == TARGET_CLUSTER
    ]
    if len(source_cells) != 3:
        raise ValueError("fixed-context source cluster does not contain three arms")
    cell = next(item for item in source_cells if item.get("arm") == "opaque")
    scheduled = _schedule(cell)
    output = args.output_root.resolve()
    output.mkdir(parents=True, exist_ok=True)
    progress = _Progress(output / "progress.jsonl")
    provider = deepcopy(manifest["provider"])
    provider["infrastructure_retry_limit"] = int(
        manifest.get("execution", {}).get("infrastructure_retry_limit", 0)
    )
    if args.execute:
        results = _execute(
            scheduled,
            provider=provider,
            output=output,
            progress=progress,
            workers=args.workers,
            resume=args.resume,
        )
    else:
        results = [
            json.loads(path.read_text(encoding="utf-8"))
            for path in sorted((output / "cells").glob("*.json"))
        ]
    summary = summarize_fixed_context_replay(results)
    _atomic_json(output / "summary.json", summary)
    _write_report(summary, output / "REPORT_ZH.md")
    progress.emit(
        {
            "stage": "terminal_fixed_analysis_complete",
            "completed_sessions": summary["completed_session_count"],
            "total_sessions": summary["scheduled_session_count"],
            "status": summary["status"],
        }
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
