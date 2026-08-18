#!/usr/bin/env python
"""Prepare, canary, execute, and analyze Work II A-S Study B4."""

from __future__ import annotations

import argparse
import hashlib
import json
import tempfile
import time
from collections.abc import Callable, Mapping, Sequence
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
    _resume_command,
)

from chemworld.eval.work_ii_b4_decision import (
    B4_ARMS,
    B4_CELL_VERSION,
    b4_output_schema,
    evaluate_b4_decision,
    prepare_b4,
    summarize_b4_results,
    validate_b4_payload,
)
from chemworld.eval.work_ii_study_b import score_prediction_payload

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROTOCOL = (
    ROOT / "configs/benchmark/work_ii_as_study_b4_law_guided_decision_v0.1.json"
)
DEFAULT_OUTPUT = (
    ROOT / "runs/formal/work-ii-as-study-b4-law-guided-decision-v0.1-20260816"
)


def _initial_prompt(cell: Mapping[str, Any]) -> str:
    packet = cell["public_packet"]
    public = {
        "task_id": cell["task_id"],
        "initial_world_model": cell["initial_world_model"],
        "candidate_mechanism_families": packet["candidate_mechanism_families"],
        "metric_range": packet["metric_range"],
        "unseen_action_candidates": packet["unseen_action_candidates"],
    }
    return (
        "You are a scientific participant in a two-turn law-guided decision study. Do not use "
        "shell, files, web, apps, plugins, MCP, or any other tool. No measured evidence is "
        "available in this turn. Commit to one anonymous mechanism family, a numerical "
        "reference-coefficient exponent, one typed executable law, and predictions for every "
        "metric of every unseen action "
        "candidate. Do not choose an action yet. Return only schema-conforming JSON. model_summary "
        "must be a concise public scientific statement, not private chain-of-thought.\n\nINPUT:\n"
        + json.dumps(public, ensure_ascii=False, sort_keys=True)
    )


def _evidence_prompt(cell: Mapping[str, Any]) -> str:
    packet = cell["public_packet"]
    public = {
        "task_id": cell["task_id"],
        "candidate_mechanism_families": packet["candidate_mechanism_families"],
        "evidence": packet["evidence"],
        "unseen_action_candidates": packet["unseen_action_candidates"],
        "decision_options": packet["decision_options"],
        "improvement_margin": packet["improvement_margin"],
    }
    return (
        "The evaluator now reveals the fixed structural evidence packet. Each evidence recipe "
        "contains a linear-reference calibration and target-world observations under identical "
        "controls. The action candidates remain unexecuted and their truth/ranks are hidden. "
        "Update the family, exponent, typed law, and all predictions. Then either execute exactly "
        "one candidate query ID or retain the visible evidence incumbent. Use RETAIN_INCUMBENT "
        "as the selected_action_query_id only when decision_type is retain_incumbent. Relative "
        "quality is primary; exceeding the incumbent by the displayed margin is secondary. Return "
        "only schema-conforming JSON and concise public summaries.\n\nEVIDENCE_INPUT:\n"
        + json.dumps(public, ensure_ascii=False, sort_keys=True)
    )


def _run_cell_attempt(
    cell: Mapping[str, Any],
    *,
    provider: Mapping[str, Any],
    progress: _Progress,
    phase: str,
) -> dict[str, Any]:
    cell_id = str(cell["cell_id"])
    started = time.perf_counter()
    progress.emit({"stage": f"b4_{phase}_cell_started", "cell_id": cell_id})
    result: dict[str, Any] = {
        "schema_version": B4_CELL_VERSION,
        "study_id": cell["study_id"],
        "phase": phase,
        "cell_id": cell_id,
        "cluster_id": cell["cluster_id"],
        "locus": cell["locus"],
        "task_id": cell["task_id"],
        "world_seed": cell["world_seed"],
        "arm": cell["arm"],
        "public_packet_sha256": cell["public_packet_sha256"],
        "participant_physical_experiment_count": 0,
    }
    receipts: list[dict[str, Any]] = []
    try:
        with tempfile.TemporaryDirectory(prefix="chemworld-study-b4-") as temporary:
            temp_root = Path(temporary)
            workspace = temp_root / "workspace"
            workspace.mkdir()
            environment = _prepare_codex_home(temp_root, provider)
            pre_schema = temp_root / "pre.schema.json"
            post_schema = temp_root / "post.schema.json"
            queries = cell["public_packet"]["unseen_action_candidates"]
            _atomic_json(pre_schema, b4_output_schema(queries, stage="pre"))
            _atomic_json(post_schema, b4_output_schema(queries, stage="post"))
            initial = _initial_command(provider, pre_schema, workspace)

            def liveness(turn: str) -> Callable[[dict[str, Any]], None]:
                return lambda payload: progress.emit(
                    {
                        "stage": f"b4_{phase}_turn_liveness",
                        "cell_id": cell_id,
                        "turn": turn,
                        **payload,
                    }
                )

            pre = _launch_turn(
                initial,
                _initial_prompt(cell),
                cwd=workspace,
                environment=environment,
                timeout_s=float(provider["request_timeout_s"]),
                liveness=liveness("pre"),
            )
            receipts.append({key: value for key, value in pre.items() if key != "final_payload"})
            pre_payload = pre.get("final_payload")
            pre_errors = (
                validate_b4_payload(pre_payload, queries, stage="pre")
                if isinstance(pre_payload, Mapping)
                else ["pre final payload is unavailable"]
            )
            thread_id = pre.get("thread_id")
            if pre.get("status") != "completed" or not isinstance(thread_id, str):
                raise _ProviderInfrastructureError(
                    "B4 pre turn did not complete with a persistent thread"
                )
            if pre_errors:
                raise _ParticipantSchemaError("; ".join(pre_errors))

            post = _launch_turn(
                _resume_command(initial, thread_id=thread_id, schema_path=post_schema),
                _evidence_prompt(cell),
                cwd=workspace,
                environment=environment,
                timeout_s=float(provider["request_timeout_s"]),
                liveness=liveness("post"),
            )
            receipts.append({key: value for key, value in post.items() if key != "final_payload"})
            post_payload = post.get("final_payload")
            post_errors = (
                validate_b4_payload(post_payload, queries, stage="post")
                if isinstance(post_payload, Mapping)
                else ["post final payload is unavailable"]
            )
            if post.get("status") != "completed":
                raise _ProviderInfrastructureError("B4 post turn did not complete")
            if post.get("thread_id") != thread_id:
                raise _ProviderInfrastructureError("B4 post turn did not preserve the Codex thread")
            if post_errors:
                raise _ParticipantSchemaError("; ".join(post_errors))
            assert isinstance(pre_payload, Mapping)
            assert isinstance(post_payload, Mapping)
            result.update(
                {
                    "status": "completed",
                    "same_thread": True,
                    "pre_submission": deepcopy(dict(pre_payload)),
                    "post_submission": deepcopy(dict(post_payload)),
                    "scores": {
                        "pre": score_prediction_payload(pre_payload, cell["scoring_truth"]),
                        "post": score_prediction_payload(post_payload, cell["scoring_truth"]),
                    },
                    "decision_evaluation": evaluate_b4_decision(cell, post_payload),
                    "provider_receipts": receipts,
                }
            )
    except Exception as error:  # retained terminal failure, never outcome-replaced
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
            "stage": f"b4_{phase}_cell_terminal",
            "cell_id": cell_id,
            "status": result["status"],
            "elapsed_s": result["elapsed_s"],
        }
    )
    return result


def _run_cell(
    cell: Mapping[str, Any],
    *,
    provider: Mapping[str, Any],
    progress: _Progress,
    phase: str,
) -> dict[str, Any]:
    retry_limit = int(provider.get("infrastructure_retry_limit", 0))
    predecessors: list[dict[str, Any]] = []
    for attempt_index in range(retry_limit + 1):
        result = _run_cell_attempt(
            cell,
            provider=provider,
            progress=progress,
            phase=phase,
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
                "stage": f"b4_{phase}_infrastructure_retry",
                "cell_id": cell["cell_id"],
                "completed_attempts": attempt_index + 1,
                "maximum_attempts": retry_limit + 1,
            }
        )
    raise AssertionError("unreachable A-S Study B4 retry loop")


def _execute_cells(
    cells: Sequence[Mapping[str, Any]],
    *,
    provider: Mapping[str, Any],
    output_dir: Path,
    progress: _Progress,
    phase: str,
    workers: int,
    resume: bool,
) -> list[dict[str, Any]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    results: list[dict[str, Any]] = []
    pending: list[Mapping[str, Any]] = []
    for cell in cells:
        path = output_dir / f"{cell['cell_id']}.json"
        if resume and path.is_file():
            existing = json.loads(path.read_text(encoding="utf-8"))
            if existing.get("schema_version") == B4_CELL_VERSION:
                results.append(existing)
                continue
        pending.append(cell)
    total = len(cells)
    completed = len(results)
    started = time.perf_counter()
    progress.emit(
        {
            "stage": f"b4_{phase}_execution_started",
            "completed_cells": completed,
            "total_cells": total,
            "workers": workers,
        }
    )
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(
                _run_cell,
                cell,
                provider=provider,
                progress=progress,
                phase=phase,
            ): cell
            for cell in pending
        }
        for future in as_completed(futures):
            result = future.result()
            _atomic_json(output_dir / f"{result['cell_id']}.json", result)
            results.append(result)
            completed += 1
            elapsed = max(time.perf_counter() - started, 1.0e-9)
            throughput = completed / elapsed
            progress.emit(
                {
                    "stage": f"b4_{phase}_progress",
                    "cell_id": result["cell_id"],
                    "completed_cells": completed,
                    "total_cells": total,
                    "failed_cells": sum(item.get("status") != "completed" for item in results),
                    "throughput_cells_per_minute": round(throughput * 60.0, 3),
                    "eta_seconds": (
                        round((total - completed) / throughput, 1) if throughput > 0 else None
                    ),
                }
            )
    return results


def _canary_qualified(results: Sequence[Mapping[str, Any]]) -> tuple[bool, list[str]]:
    errors: list[str] = []
    if len(results) != 3 or {item.get("arm") for item in results} != set(B4_ARMS):
        errors.append("B4 canary denominator or arm coverage differs from three arms")
    if len({item.get("public_packet_sha256") for item in results}) != 1:
        errors.append("B4 canary arms did not receive an identical public packet")
    for result in results:
        if result.get("status") != "completed" or result.get("same_thread") is not True:
            errors.append(f"B4 canary cell {result.get('cell_id')} did not complete two turns")
            continue
        if result.get("scores", {}).get("post", {}).get("term_count") != 32:
            errors.append(f"B4 canary cell {result.get('cell_id')} has the wrong denominator")
        decision = result.get("decision_evaluation")
        if not isinstance(decision, Mapping):
            errors.append(f"B4 canary cell {result.get('cell_id')} lacks decision evaluation")
    return not errors, errors


def _write_report(summary: Mapping[str, Any], path: Path) -> None:
    lines = [
        "# Work II A-S Study B4 law-guided decision 结果",
        "",
        f"状态: `{summary['status']}`; 完成 {summary['completed_cell_count']}/"
        f"{summary['scheduled_cell_count']} sessions; 失败 {summary['failed_cell_count']}。",
        "",
        "| arm | 完成 | family=power | exponent ±0.10 | Top-1 | 平均选择排名 | "
        "平均 normalized regret | 正确 abstain | 错误 abstain | 错误 execute |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for arm in B4_ARMS:
        row = summary["by_arm"][arm]
        mean_rank = row["mean_selected_rank"]
        mean_rank_text = "n/a" if mean_rank is None else f"{mean_rank:.3f}"
        mean_regret = row["mean_normalized_policy_regret"]
        mean_regret_text = "n/a" if mean_regret is None else f"{mean_regret:.4f}"
        lines.append(
            f"| {arm} | {row['completed_cell_count']} | "
            f"{row['exact_family_recovery_count']} | {row['exponent_within_0_10_count']} | "
            f"{row['top1_candidate_count']} | "
            f"{mean_rank_text} | "
            f"{mean_regret_text} | "
            f"{row['correct_abstention_count']} | {row['false_abstention_count']} | "
            f"{row['false_execution_count']} |"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--protocol", type=Path, default=DEFAULT_PROTOCOL)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--prepare", action="store_true")
    parser.add_argument("--canary", action="store_true")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--analyze", action="store_true")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--workers", type=int, default=3)
    args = parser.parse_args()
    if not any((args.prepare, args.canary, args.execute, args.analyze)):
        parser.error("select at least one of --prepare, --canary, --execute, or --analyze")
    if not 1 <= args.workers <= 3:
        parser.error("--workers must be between 1 and 3")
    output_root = args.output_root.resolve()
    output_root.mkdir(parents=True, exist_ok=True)
    progress = _Progress(output_root / "progress.jsonl")
    protocol_path = args.protocol if args.protocol.is_absolute() else ROOT / args.protocol
    manifest_path = output_root / "input_manifest.json"
    if args.prepare or not manifest_path.is_file():
        manifest = prepare_b4(
            protocol_path,
            repository_root=ROOT,
            output_root=output_root,
            progress=progress.emit,
        )
    else:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    progress.emit(
        {
            "stage": "b4_provider_free_preflight_complete",
            "completed_cells": 0,
            "total_cells": manifest["cell_count"],
            "clusters": manifest["cluster_count"],
        }
    )
    if args.prepare and not any((args.canary, args.execute, args.analyze)):
        return 0
    provider = deepcopy(manifest["provider"])
    provider["infrastructure_retry_limit"] = int(
        manifest["execution"]["infrastructure_retry_limit"]
    )
    if args.canary:
        first_cluster = manifest["cells"][0]["cluster_id"]
        canary_cells = [
            cell for cell in manifest["cells"] if cell["cluster_id"] == first_cluster
        ]
        canary_results = _execute_cells(
            canary_cells,
            provider=provider,
            output_dir=output_root / "canary",
            progress=progress,
            phase="canary",
            workers=args.workers,
            resume=args.resume,
        )
        qualified, errors = _canary_qualified(canary_results)
        canary_summary = {
            "schema_version": "chemworld-work-ii-as-study-b4-canary-summary-0.1",
            "qualified": qualified,
            "session_count": len(canary_results),
            "errors": errors,
            "scientific_outcomes_used_for_design": False,
        }
        _atomic_json(output_root / "canary_summary.json", canary_summary)
        if not qualified:
            progress.emit({"stage": "b4_canary_failed", "errors": errors})
            return 2
        progress.emit({"stage": "b4_canary_qualified", "completed_cells": 3, "total_cells": 3})
    if args.execute:
        canary_path = output_root / "canary_summary.json"
        canary_ok = (
            canary_path.is_file()
            and json.loads(canary_path.read_text(encoding="utf-8")).get("qualified") is True
        )
        if not canary_ok:
            raise RuntimeError("A-S Study B4 formal execution requires a qualified canary")
        results = _execute_cells(
            manifest["cells"],
            provider=provider,
            output_dir=output_root / "cells",
            progress=progress,
            phase="formal",
            workers=args.workers,
            resume=args.resume,
        )
        summary = summarize_b4_results(manifest, results)
        _atomic_json(output_root / "summary.json", summary)
        _write_report(summary, output_root / "REPORT_ZH.md")
    if args.analyze and not args.execute:
        results = [
            json.loads(path.read_text(encoding="utf-8"))
            for path in sorted((output_root / "cells").glob("*.json"))
        ]
        summary = summarize_b4_results(manifest, results)
        _atomic_json(output_root / "summary.json", summary)
        _write_report(summary, output_root / "REPORT_ZH.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
