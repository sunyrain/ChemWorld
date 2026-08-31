#!/usr/bin/env python
"""Prepare, execute, and analyze reviewer-requested Work II follow-ups."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
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

from chemworld.eval.work_ii_reviewer_followup import (
    B3_ARMS,
    B3_CELL_VERSION,
    b3_output_schema,
    build_b3_manifest,
    evaluate_b3_selected_action,
    prepare_b3,
    resolve_b3_selected_action_query_id,
    summarize_b3_canary_closeout,
    summarize_b3_results,
    validate_b3_payload,
)
from chemworld.eval.work_ii_study_b import score_prediction_payload

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_B3_PROTOCOL = (
    ROOT / "configs/benchmark/work_ii_as_study_b3_identifiable_law_action_v0.1.json"
)
DEFAULT_B3_OUTPUT = (
    ROOT / "runs/formal/work-ii-as-study-b3-identifiable-law-action-v0.1-20260815"
)


def _b3_provider_free_contract(protocol: Mapping[str, Any]) -> dict[str, Any]:
    provider_or_participant_fields = {
        "study_id",
        "status",
        "experiment_note",
        "provider",
        "execution",
        "action_selection_encoding",
        "stage_status_encoding",
    }
    return {
        key: deepcopy(value)
        for key, value in protocol.items()
        if key not in provider_or_participant_fields
    }


def _b3_execution_authorized(
    manifest: Mapping[str, Any], *, phase: str
) -> bool:
    if phase not in {"canary", "formal"}:
        raise ValueError("B3 execution phase must be canary or formal")
    execution = manifest.get("execution")
    execution = execution if isinstance(execution, Mapping) else {}
    field = f"{phase}_execution_authorized"
    if field in execution:
        return execution.get(field) is True
    return "participant_execution_blocked" not in str(manifest.get("protocol_status"))


def _prepare_b3_from_provider_free_source(
    protocol_path: Path,
    *,
    source_root: Path,
    output_root: Path,
    progress: _Progress,
) -> dict[str, Any]:
    source_root = source_root.resolve()
    output_root = output_root.resolve()
    if source_root == output_root:
        raise ValueError("B3 provider-free reuse source and output roots must differ")
    source_manifest_path = source_root / "input_manifest.json"
    if not source_manifest_path.is_file():
        raise ValueError("B3 provider-free reuse source manifest is unavailable")
    source_manifest = json.loads(source_manifest_path.read_text(encoding="utf-8"))
    source_digest = source_manifest.get("manifest_sha256")
    observed_digest = hashlib.sha256(
        _canonical(
            {key: value for key, value in source_manifest.items() if key != "manifest_sha256"}
        ).encode("utf-8")
    ).hexdigest()
    if source_digest != observed_digest:
        raise ValueError("B3 provider-free reuse source manifest digest is invalid")
    source_protocol_path = ROOT / str(source_manifest["protocol_path"])
    source_protocol = json.loads(source_protocol_path.read_text(encoding="utf-8"))
    target_protocol = json.loads(protocol_path.read_text(encoding="utf-8"))
    if _b3_provider_free_contract(source_protocol) != _b3_provider_free_contract(
        target_protocol
    ):
        raise ValueError("B3 provider-free reuse science contract differs from the target")
    manifest = build_b3_manifest(
        protocol_path,
        repository_root=ROOT,
        output_root=source_root,
    )
    _atomic_json(output_root / "input_manifest.json", manifest)
    progress.emit(
        {
            "stage": "b3_provider_free_truth_reused",
            "source_root": str(source_root),
            "qualification_sha256": manifest["qualification_sha256"],
            "public_truth_sha256": manifest["public_truth_sha256"],
            "completed_cells": 0,
            "total_cells": manifest["cell_count"],
            "provider_calls": 0,
        }
    )
    return manifest


def _b3_initial_prompt(cell: Mapping[str, Any]) -> str:
    packet = cell["public_packet"]
    public = {
        "task_id": cell["task_id"],
        "initial_world_model": cell["initial_world_model"],
        "candidate_mechanism_families": packet["candidate_mechanism_families"],
        "metric_range": packet["metric_range"],
        "scoring_action_queries": packet["scoring_action_queries"],
    }
    return (
        "You are a scientific participant in a two-turn constitutive-law identification study. "
        "Do not use shell, files, web, apps, plugins, MCP, or any other tool. No measured evidence "
        "is available in this turn. Use only the supplied initial model, anonymous candidate "
        "families, public reference coefficients, and query controls. Commit independently to one "
        "mechanism family, one numerical reference-coefficient exponent, one typed executable law, "
        "and predictions for every metric of every unseen scoring/action query. Return only the "
        "schema-conforming JSON. model_summary must be a concise public scientific statement, not "
        "private chain-of-thought.\n\nINPUT:\n"
        + json.dumps(public, ensure_ascii=False, sort_keys=True)
    )


def _b3_evidence_prompt(cell: Mapping[str, Any]) -> str:
    packet = cell["public_packet"]
    public = {
        "task_id": cell["task_id"],
        "candidate_mechanism_families": packet["candidate_mechanism_families"],
        "evidence": packet["evidence"],
        "scoring_action_queries": packet["scoring_action_queries"],
    }
    action_selection_encoding = str(cell.get("action_selection_encoding", "query_id"))
    if action_selection_encoding == "query_id":
        selection_field = "selected_action_query_id"
        selection_instruction = (
            "select exactly one scoring/action query ID as the novel action you would execute "
            "and return it as selected_action_query_id"
        )
    else:
        selection_field = "selected_action_index"
        selection_instruction = (
            "select exactly one visible zero-based action_index (0 through 7) as the novel "
            "action you would execute and return it as selected_action_index"
        )
    return (
        "The evaluator now reveals the fixed evidence packet. Each evidence recipe reports both "
        "the public linear-reference calibration and the measured target-world observation under "
        "the same controls. The scoring/action queries are disjoint and have never been executed "
        "for you. Treat the evidence as authoritative. Update the mechanism family, exponent, "
        f"typed law, and all predictions, then {selection_instruction}. The first-turn JSON shape "
        "is not sufficient for this turn. In addition to the updated model fields, the post JSON "
        f"must include both {selection_field} and evidence_assessment. Do not invent a free-text "
        "recipe. Return only "
        "schema-conforming "
        "JSON; summaries must be public scientific statements, not private chain-of-thought.\n\n"
        "EVIDENCE_INPUT:\n"
        + json.dumps(public, ensure_ascii=False, sort_keys=True)
    )


def _run_b3_cell_attempt(
    cell: Mapping[str, Any],
    *,
    provider: Mapping[str, Any],
    progress: _Progress,
    phase: str,
) -> dict[str, Any]:
    cell_id = str(cell["cell_id"])
    started = time.perf_counter()
    progress.emit({"stage": f"b3_{phase}_cell_started", "cell_id": cell_id})
    result: dict[str, Any] = {
        "schema_version": B3_CELL_VERSION,
        "study_id": cell["study_id"],
        "phase": phase,
        "cell_id": cell_id,
        "cluster_id": cell["cluster_id"],
        "replicate_block_id": cell.get(
            "replicate_block_id", f"{cell['cluster_id']}--replicate-01"
        ),
        "replicate_index": int(cell.get("replicate_index", 1)),
        "locus": cell["locus"],
        "task_id": cell["task_id"],
        "world_seed": cell["world_seed"],
        "arm": cell["arm"],
        "action_selection_encoding": cell.get(
            "action_selection_encoding", "query_id"
        ),
        "stage_status_encoding": cell.get("stage_status_encoding", "explicit_const"),
        "public_packet_sha256": cell["public_packet_sha256"],
        "participant_physical_experiment_count": 0,
    }
    receipts: list[dict[str, Any]] = []
    pre_payload: Mapping[str, Any] | None = None
    post_payload: Mapping[str, Any] | None = None
    try:
        with tempfile.TemporaryDirectory(prefix="chemworld-study-b3-") as temporary:
            temp_root = Path(temporary)
            workspace = temp_root / "workspace"
            workspace.mkdir()
            environment = _prepare_b3_environment(temp_root, provider)
            pre_schema = temp_root / "pre.schema.json"
            post_schema = temp_root / "post.schema.json"
            queries = cell["public_packet"]["scoring_action_queries"]
            action_selection_encoding = str(
                cell.get("action_selection_encoding", "query_id")
            )
            stage_status_encoding = str(
                cell.get("stage_status_encoding", "explicit_const")
            )
            _atomic_json(
                pre_schema,
                b3_output_schema(
                    queries,
                    stage="pre",
                    action_selection_encoding=action_selection_encoding,
                    stage_status_encoding=stage_status_encoding,
                ),
            )
            _atomic_json(
                post_schema,
                b3_output_schema(
                    queries,
                    stage="post",
                    action_selection_encoding=action_selection_encoding,
                    stage_status_encoding=stage_status_encoding,
                ),
            )
            initial = _b3_initial_command(provider, pre_schema, workspace)

            def liveness(turn: str) -> Callable[[dict[str, Any]], None]:
                return lambda payload: progress.emit(
                    {
                        "stage": f"b3_{phase}_turn_liveness",
                        "cell_id": cell_id,
                        "turn": turn,
                        **payload,
                    }
                )

            pre = _launch_turn(
                initial,
                _b3_initial_prompt(cell),
                cwd=workspace,
                environment=environment,
                timeout_s=float(provider["request_timeout_s"]),
                liveness=liveness("pre"),
            )
            receipts.append({key: value for key, value in pre.items() if key != "final_payload"})
            pre_payload = pre.get("final_payload")
            pre_errors = (
                validate_b3_payload(
                    pre_payload,
                    queries,
                    stage="pre",
                    action_selection_encoding=action_selection_encoding,
                    stage_status_encoding=stage_status_encoding,
                )
                if isinstance(pre_payload, Mapping)
                else ["pre final payload is unavailable"]
            )
            thread_id = pre.get("thread_id")
            if pre.get("status") != "completed" or not isinstance(thread_id, str):
                raise _ProviderInfrastructureError(
                    "B3 pre turn did not complete with a persistent thread"
                )
            if pre_errors:
                raise _ParticipantSchemaError("; ".join(pre_errors))
            post = _launch_turn(
                _resume_command(initial, thread_id=thread_id, schema_path=post_schema),
                _b3_evidence_prompt(cell),
                cwd=workspace,
                environment=environment,
                timeout_s=float(provider["request_timeout_s"]),
                liveness=liveness("post"),
            )
            receipts.append({key: value for key, value in post.items() if key != "final_payload"})
            post_payload = post.get("final_payload")
            post_errors = (
                validate_b3_payload(
                    post_payload,
                    queries,
                    stage="post",
                    action_selection_encoding=action_selection_encoding,
                    stage_status_encoding=stage_status_encoding,
                )
                if isinstance(post_payload, Mapping)
                else ["post final payload is unavailable"]
            )
            if post.get("status") != "completed":
                raise _ProviderInfrastructureError("B3 post turn did not complete")
            if post.get("thread_id") != thread_id:
                raise _ProviderInfrastructureError("B3 post turn did not preserve the Codex thread")
            if post_errors:
                raise _ParticipantSchemaError("; ".join(post_errors))
            assert isinstance(pre_payload, Mapping)
            assert isinstance(post_payload, Mapping)
            selected_query_id = resolve_b3_selected_action_query_id(
                post_payload,
                queries,
                action_selection_encoding=action_selection_encoding,
            )
            selected_action = evaluate_b3_selected_action(cell, selected_query_id)
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
                    "selected_action": selected_action,
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
        if isinstance(pre_payload, Mapping):
            result["pre_submission"] = deepcopy(dict(pre_payload))
        if isinstance(post_payload, Mapping):
            result["post_submission"] = deepcopy(dict(post_payload))
    result["elapsed_s"] = round(time.perf_counter() - started, 3)
    result["result_sha256"] = hashlib.sha256(_canonical(result).encode("utf-8")).hexdigest()
    progress.emit(
        {
            "stage": f"b3_{phase}_cell_terminal",
            "cell_id": cell_id,
            "status": result["status"],
            "elapsed_s": result["elapsed_s"],
        }
    )
    return result


def _run_b3_cell(
    cell: Mapping[str, Any],
    *,
    provider: Mapping[str, Any],
    progress: _Progress,
    phase: str,
) -> dict[str, Any]:
    retry_limit = int(provider.get("infrastructure_retry_limit", 0))
    predecessors: list[dict[str, Any]] = []
    for attempt_index in range(retry_limit + 1):
        result = _run_b3_cell_attempt(
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
                "stage": f"b3_{phase}_infrastructure_retry",
                "cell_id": cell["cell_id"],
                "completed_attempts": attempt_index + 1,
                "maximum_attempts": retry_limit + 1,
            }
        )
    raise AssertionError("unreachable A-S Study B3 retry loop")


def _execute_b3_cells(
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
            if (
                existing.get("schema_version") == B3_CELL_VERSION
                and existing.get("study_id") == cell.get("study_id")
                and existing.get("cell_id") == cell.get("cell_id")
                and existing.get("action_selection_encoding", "query_id")
                == cell.get("action_selection_encoding", "query_id")
                and existing.get("stage_status_encoding", "explicit_const")
                == cell.get("stage_status_encoding", "explicit_const")
            ):
                results.append(existing)
                continue
        pending.append(cell)
    total = len(cells)
    completed = len(results)
    started = time.perf_counter()
    progress.emit(
        {
            "stage": f"b3_{phase}_execution_started",
            "completed_cells": completed,
            "total_cells": total,
            "workers": workers,
        }
    )
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(
                _run_b3_cell,
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
            remaining = total - completed
            progress.emit(
                {
                    "stage": f"b3_{phase}_progress",
                    "cell_id": result["cell_id"],
                    "completed_cells": completed,
                    "total_cells": total,
                    "failed_cells": sum(item.get("status") != "completed" for item in results),
                    "throughput_cells_per_minute": round(throughput * 60.0, 3),
                    "eta_seconds": round(remaining / throughput, 1) if throughput > 0 else None,
                }
            )
    return results


def _b3_canary_qualified(results: Sequence[Mapping[str, Any]]) -> tuple[bool, list[str]]:
    errors: list[str] = []
    if len(results) != 3 or {item.get("arm") for item in results} != set(B3_ARMS):
        errors.append("B3 canary denominator or arm coverage differs from three arms")
    if len({item.get("public_packet_sha256") for item in results}) != 1:
        errors.append("B3 canary arms did not receive an identical public packet")
    for result in results:
        if result.get("status") != "completed" or result.get("same_thread") is not True:
            errors.append(f"B3 canary cell {result.get('cell_id')} did not complete two turns")
            continue
        for stage in ("pre_submission", "post_submission"):
            payload = result.get(stage)
            if not isinstance(payload, Mapping) or not isinstance(
                payload.get("typed_law"), Mapping
            ):
                errors.append(f"B3 canary cell {result.get('cell_id')} lacks {stage} typed law")
        if result.get("scores", {}).get("post", {}).get("term_count") != 32:
            errors.append(
                f"B3 canary cell {result.get('cell_id')} has the wrong scoring denominator"
            )
        if (
            result.get("selected_action", {}).get("participant_executed_before_selection")
            is not False
        ):
            errors.append(f"B3 canary cell {result.get('cell_id')} action was not novel")
    return not errors, errors


def _prepare_b3_environment(
    temp_root: Path, provider: Mapping[str, Any]
) -> dict[str, str]:
    return _prepare_codex_home(temp_root, provider)


def _b3_initial_command(
    provider: Mapping[str, Any], schema_path: Path, workspace: Path
) -> list[str]:
    command = _initial_command(provider, schema_path, workspace)
    disable_index = command.index("--sandbox")
    command[disable_index:disable_index] = ["--disable", "shell_tool"]
    return command


def _static_provider_check(
    provider: Mapping[str, Any], *, output_root: Path
) -> dict[str, Any]:
    executable = shutil.which("codex")
    auth_mode = str(provider.get("auth_mode"))
    errors: list[str] = []
    login_verified = None
    cli_version = None
    if executable is None:
        errors.append("Codex CLI is unavailable on PATH")
    else:
        version = subprocess.run(
            [executable, "--version"], capture_output=True, text=True, timeout=30, check=False
        )
        cli_version = (version.stdout or version.stderr).strip() or None
        if version.returncode != 0:
            errors.append("Codex CLI version query failed")
        if auth_mode == "chatgpt_subscription_cached_login":
            login = subprocess.run(
                [executable, "login", "status"],
                capture_output=True,
                text=True,
                timeout=30,
                check=False,
            )
            status = f"{login.stdout}\n{login.stderr}".lower()
            login_verified = login.returncode == 0 and "logged in using chatgpt" in status
            if not login_verified:
                errors.append("Codex CLI cached ChatGPT subscription login is unavailable")
    with tempfile.TemporaryDirectory(prefix="chemworld-b3-static-") as temporary:
        root = Path(temporary)
        schema = root / "schema.json"
        workspace = root / "workspace"
        workspace.mkdir()
        _atomic_json(schema, {"type": "object", "additionalProperties": False})
        command = _b3_initial_command(provider, schema, workspace) if executable else []
    rendered = " ".join(command)
    command_ready = bool(
        command
        and str(provider.get("model")) in command
        and f'model_reasoning_effort="{provider.get("reasoning_effort")}"' in rendered
        and "--disable shell_tool" in rendered
        and "--disable apps" in rendered
        and "--disable multi_agent" in rendered
        and "--disable plugins" in rendered
    )
    if not command_ready:
        errors.append("B3 participant command contract is incomplete")
    result = {
        "schema_version": "chemworld-work-ii-b3-provider-static-check-0.1",
        "provider_id": provider.get("id"),
        "model": provider.get("model"),
        "reasoning_effort": provider.get("reasoning_effort"),
        "wire_api": provider.get("wire_api"),
        "auth_mode": auth_mode,
        "codex_cli_available": executable is not None,
        "codex_cli_version": cli_version,
        "cached_chatgpt_login_verified": login_verified,
        "command_contract_ready": command_ready,
        "provider_calls": 0,
        "ready": not errors,
        "errors": errors,
    }
    _atomic_json(output_root / "provider_static_check.json", result)
    return result


def _write_b3_report(summary: Mapping[str, Any], path: Path) -> None:
    lines = [
        "# Work II A-S Study B3 结构律识别与新动作结果",
        "",
        f"状态: `{summary['status']}`; 完成 {summary['completed_cell_count']}/"
        f"{summary['scheduled_cell_count']} sessions; 失败 {summary['failed_cell_count']}。",
        "",
        "B3 将 anonymous mechanism family、指数、typed executable law、未展示查询预测与"
        " `selected_action_query_id` 分开计分。动作只来自 participant 从未执行的 evaluator-owned"
        " scoring roster。",
        "",
        f"rank/Top-1/regret 使用全部 {summary['all_world_rank_regret_cell_denominator']} 个完成"
        " cell; gain 仅使用冻结 action-opportunity 合格世界中的 "
        f"{summary['action_opportunity_eligible_gain_cell_denominator']} 个完成 cell。",
        "",
        "| arm | 完成 | family=power | exponent ±0.10 | post error | Top-1 | 平均 rank | "
        "平均 regret | gain 分母 | gain>0 | gain≥阈值 | 平均 gain |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for arm in B3_ARMS:
        row = summary["by_arm"][arm]
        post_error = row["mean_post_error"]
        action_gain = row["mean_action_gain"]
        action_gain_text = "—" if action_gain is None else f"{action_gain:.4f}"
        lines.append(
            f"| {arm} | {row['completed_cell_count']} | "
            f"{row['exact_family_recovery_count']} | {row['exponent_within_0_10_count']} | "
            f"{post_error:.4f} | {row['top1_selected_count']} | "
            f"{row['mean_selected_true_rank']:.3f} | {row['mean_normalized_regret']:.4f} | "
            f"{row['action_opportunity_eligible_gain_denominator']} | "
            f"{row['positive_action_gain_count']} | "
            f"{row['action_gain_at_least_0_02_count']} | {action_gain_text} |"
        )
    if summary["failures"]:
        lines.extend(["", "## 保留失败", ""])
        lines.extend(
            f"- `{item['cell_id']}`: `{item['failure']}`" for item in summary["failures"]
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--study", choices=("b3",), default="b3")
    parser.add_argument("--protocol", type=Path, default=DEFAULT_B3_PROTOCOL)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_B3_OUTPUT)
    parser.add_argument("--prepare", action="store_true")
    parser.add_argument("--canary", action="store_true")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--analyze", action="store_true")
    parser.add_argument("--static-provider-check", action="store_true")
    parser.add_argument("--reuse-provider-free-root", type=Path)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--workers", type=int, default=3)
    args = parser.parse_args()
    if not any(
        (args.prepare, args.canary, args.execute, args.analyze, args.static_provider_check)
    ):
        parser.error(
            "select at least one of --prepare, --canary, --execute, --analyze, or "
            "--static-provider-check"
        )
    if not 1 <= args.workers <= 3:
        parser.error("--workers must be between 1 and 3")
    output_root = args.output_root.resolve()
    output_root.mkdir(parents=True, exist_ok=True)
    progress = _Progress(output_root / "progress.jsonl")
    protocol_path = args.protocol if args.protocol.is_absolute() else ROOT / args.protocol
    manifest_path = output_root / "input_manifest.json"
    if args.prepare or not manifest_path.is_file():
        if args.reuse_provider_free_root is not None:
            source_root = (
                args.reuse_provider_free_root
                if args.reuse_provider_free_root.is_absolute()
                else ROOT / args.reuse_provider_free_root
            )
            manifest = _prepare_b3_from_provider_free_source(
                protocol_path,
                source_root=source_root,
                output_root=output_root,
                progress=progress,
            )
        else:
            manifest = prepare_b3(
                protocol_path,
                repository_root=ROOT,
                output_root=output_root,
                progress=progress.emit,
            )
    else:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    progress.emit(
        {
            "stage": "b3_provider_free_preflight_complete",
            "completed_cells": 0,
            "total_cells": manifest["cell_count"],
            "clusters": manifest["cluster_count"],
        }
    )
    if args.static_provider_check:
        static = _static_provider_check(manifest["provider"], output_root=output_root)
        if not static["ready"]:
            return 3
    if args.prepare and not any(
        (args.canary, args.execute, args.analyze, args.static_provider_check)
    ):
        return 0
    provider = deepcopy(manifest["provider"])
    provider["infrastructure_retry_limit"] = int(
        manifest["execution"]["infrastructure_retry_limit"]
    )
    if args.canary:
        if not _b3_execution_authorized(manifest, phase="canary"):
            raise RuntimeError("A-S Study B3 canary execution is not authorized")
        canary_path = output_root / "canary_summary.json"
        if canary_path.is_file() and not args.resume:
            raise RuntimeError(
                "A-S Study B3 canary is already terminal; use --resume only to revalidate"
            )
        first_cluster = manifest["cells"][0]["cluster_id"]
        canary_cells = [
            cell
            for cell in manifest["cells"]
            if cell["cluster_id"] == first_cluster and int(cell.get("replicate_index", 1)) == 1
        ]
        canary_results = _execute_b3_cells(
            canary_cells,
            provider=provider,
            output_dir=output_root / "canary",
            progress=progress,
            phase="canary",
            workers=args.workers,
            resume=args.resume,
        )
        qualified, errors = _b3_canary_qualified(canary_results)
        canary_summary = {
            "schema_version": "chemworld-work-ii-as-study-b3-canary-summary-0.1",
            "qualified": qualified,
            "session_count": len(canary_results),
            "errors": errors,
            "scientific_outcomes_used_for_design": False,
        }
        _atomic_json(output_root / "canary_summary.json", canary_summary)
        _atomic_json(
            output_root / "canary_closeout.json",
            summarize_b3_canary_closeout(manifest, canary_results, canary_summary),
        )
        if not qualified:
            progress.emit({"stage": "b3_canary_failed", "errors": errors})
            return 2
        progress.emit({"stage": "b3_canary_qualified", "completed_cells": 3, "total_cells": 3})
    if args.execute:
        if not _b3_execution_authorized(manifest, phase="formal"):
            raise RuntimeError("A-S Study B3 formal execution is not authorized")
        canary_path = output_root / "canary_summary.json"
        canary_ok = (
            canary_path.is_file()
            and json.loads(canary_path.read_text(encoding="utf-8")).get("qualified") is True
        )
        if not canary_ok:
            raise RuntimeError("A-S Study B3 formal execution requires a qualified canary")
        results = _execute_b3_cells(
            manifest["cells"],
            provider=provider,
            output_dir=output_root / "cells",
            progress=progress,
            phase="formal",
            workers=args.workers,
            resume=args.resume,
        )
        summary = summarize_b3_results(manifest, results)
        _atomic_json(output_root / "summary.json", summary)
        _write_b3_report(summary, output_root / "REPORT_ZH.md")
    if args.analyze and not args.execute:
        results = [
            json.loads(path.read_text(encoding="utf-8"))
            for path in sorted((output_root / "cells").glob("*.json"))
        ]
        summary = summarize_b3_results(manifest, results)
        _atomic_json(output_root / "summary.json", summary)
        _write_b3_report(summary, output_root / "REPORT_ZH.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
