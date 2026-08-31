#!/usr/bin/env python
"""Prepare, canary, execute, and analyze Work II Study B."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
import threading
import time
from collections.abc import Callable, Mapping, Sequence
from concurrent.futures import ThreadPoolExecutor, as_completed
from copy import deepcopy
from pathlib import Path
from typing import Any

from chemworld.eval.work_ii_study_b import (
    STUDY_B_CELL_VERSION,
    build_study_b_manifest,
    prediction_output_schema,
    score_prediction_payload,
    summarize_study_b_results,
    validate_prediction_payload,
)
from chemworld.eval.work_ii_study_b2 import (
    STUDY_B2_PROTOCOL_VERSION,
    build_study_b2_manifest,
    prepare_study_b2_truth,
    summarize_study_b2_results,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROTOCOL = ROOT / "configs/benchmark/work_ii_study_b_matched_evidence_v0.1.json"
DEFAULT_OUTPUT = (
    ROOT / "runs/formal/work-ii-study-b-matched-evidence-v0.1-20260815"
)


class _ProviderInfrastructureError(RuntimeError):
    pass


class _ParticipantSchemaError(RuntimeError):
    pass


def _canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(temporary, path)


class _Progress:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.lock = threading.Lock()
        path.parent.mkdir(parents=True, exist_ok=True)

    def emit(self, payload: Mapping[str, Any]) -> None:
        row = {"timestamp": time.time(), **dict(payload)}
        line = _canonical(row) + "\n"
        with self.lock, self.path.open("a", encoding="utf-8") as handle:
            handle.write(line)
        stage = row.get("stage")
        cell = row.get("cell_id", "-")
        suffix = ""
        for completed_key, total_key, label in (
            ("completed_cells", "total_cells", "cells"),
            ("completed_units", "total_units", "units"),
            ("completed_truth_queries", "total_truth_queries", "truth"),
            ("completed_worlds", "total_worlds", "worlds"),
            ("completed_queries", "total_queries", "queries"),
        ):
            completed = row.get(completed_key)
            total = row.get(total_key)
            if completed is not None and total is not None:
                suffix += f" {label}={completed}/{total}"
        if row.get("elapsed_s") is not None:
            suffix += f" elapsed_s={row['elapsed_s']}"
        print(f"[study-b] {stage} {cell}{suffix}", flush=True)


class _EventState:
    """Retain final structured output and bounded provider metadata, never reasoning bodies."""

    def __init__(self) -> None:
        self.lock = threading.Lock()
        self.thread_id: str | None = None
        self.final_message: str | None = None
        self.usage: dict[str, Any] = {}
        self.event_counts: dict[str, int] = {}
        self.provider_errors: list[dict[str, Any]] = []
        self.tool_event_count = 0
        self.stderr_bytes = 0
        self.stderr_sha256 = hashlib.sha256()

    def consume_stdout(self, stream: Any) -> None:
        for line in stream:
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            if not isinstance(event, Mapping):
                continue
            event_type = str(event.get("type", "unknown"))
            with self.lock:
                self.event_counts[event_type] = self.event_counts.get(event_type, 0) + 1
                if event_type == "thread.started" and isinstance(event.get("thread_id"), str):
                    self.thread_id = str(event["thread_id"])
                if isinstance(event.get("usage"), Mapping):
                    self.usage = deepcopy(dict(event["usage"]))
                if event_type in {"error", "turn.failed"}:
                    raw = event.get("message")
                    if event_type == "turn.failed" and isinstance(event.get("error"), Mapping):
                        raw = event["error"].get("message")
                    if isinstance(raw, str):
                        encoded = raw.encode("utf-8", errors="replace")
                        self.provider_errors.append(
                            {
                                "byte_count": len(encoded),
                                "sha256": hashlib.sha256(encoded).hexdigest(),
                                "http_status_codes": sorted(
                                    {
                                        int(value)
                                        for value in re.findall(r"\b([1-5]\d{2})\b", raw)
                                    }
                                ),
                            }
                        )
                if event_type != "item.completed" or not isinstance(event.get("item"), Mapping):
                    continue
                item = event["item"]
                item_type = item.get("type")
                if item_type == "agent_message" and isinstance(item.get("text"), str):
                    self.final_message = str(item["text"])
                elif item_type in {
                    "command_execution",
                    "file_change",
                    "dynamic_tool_call",
                    "mcp_tool_call",
                } or (isinstance(item_type, str) and "mcp" in item_type):
                    self.tool_event_count += 1

    def consume_stderr(self, stream: Any) -> None:
        for chunk in iter(lambda: stream.read(4096), ""):
            encoded = chunk.encode("utf-8", errors="replace")
            with self.lock:
                self.stderr_bytes += len(encoded)
                self.stderr_sha256.update(encoded)

    def snapshot(self) -> dict[str, Any]:
        with self.lock:
            return {
                "thread_id": self.thread_id,
                "usage": deepcopy(self.usage),
                "event_counts": dict(self.event_counts),
                "provider_errors": deepcopy(self.provider_errors),
                "tool_event_count": self.tool_event_count,
                "stderr_byte_count": self.stderr_bytes,
                "stderr_sha256": self.stderr_sha256.hexdigest(),
                "final_message": self.final_message,
            }


def _parse_payload(message: Any) -> dict[str, Any] | None:
    if not isinstance(message, str):
        return None
    candidate = message.strip()
    if candidate.startswith("```") and candidate.endswith("```"):
        lines = candidate.splitlines()
        candidate = "\n".join(lines[1:-1]).strip()
    try:
        value = json.loads(candidate)
    except json.JSONDecodeError:
        return None
    return value if isinstance(value, dict) else None


def _launch_turn(
    command: Sequence[str],
    prompt: str,
    *,
    cwd: Path,
    environment: Mapping[str, str],
    timeout_s: float,
    liveness: Callable[[dict[str, Any]], None],
) -> dict[str, Any]:
    kwargs: dict[str, Any] = {}
    if os.name == "nt":
        kwargs["creationflags"] = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    process = subprocess.Popen(
        list(command),
        cwd=cwd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        errors="replace",
        text=True,
        env=dict(environment),
        **kwargs,
    )
    if process.stdin is None or process.stdout is None or process.stderr is None:
        process.kill()
        raise RuntimeError("Codex subprocess streams are unavailable")
    state = _EventState()
    stdout_thread = threading.Thread(
        target=state.consume_stdout, args=(process.stdout,), daemon=True
    )
    stderr_thread = threading.Thread(
        target=state.consume_stderr, args=(process.stderr,), daemon=True
    )
    stdout_thread.start()
    stderr_thread.start()
    process.stdin.write(prompt)
    process.stdin.close()
    started = time.perf_counter()
    next_progress = started + 30.0
    timed_out = False
    while process.poll() is None:
        now = time.perf_counter()
        if now - started >= timeout_s:
            timed_out = True
            process.terminate()
            try:
                process.wait(timeout=10.0)
            except subprocess.TimeoutExpired:
                process.kill()
            break
        if now >= next_progress:
            snap = state.snapshot()
            liveness(
                {
                    "elapsed_s": round(now - started, 1),
                    "thread_id_observed": snap["thread_id"] is not None,
                    "event_counts": snap["event_counts"],
                }
            )
            next_progress = now + 30.0
        time.sleep(0.5)
    return_code = process.wait(timeout=15.0)
    stdout_thread.join(timeout=5.0)
    stderr_thread.join(timeout=5.0)
    snapshot = state.snapshot()
    payload = _parse_payload(snapshot.pop("final_message"))
    return {
        **snapshot,
        "status": "timeout" if timed_out else "completed" if return_code == 0 else "failed",
        "return_code": return_code,
        "elapsed_s": round(time.perf_counter() - started, 3),
        "prompt_byte_count": len(prompt.encode("utf-8")),
        "prompt_sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
        "final_payload": payload,
    }


def _prepare_codex_home(temp_root: Path, provider: Mapping[str, Any]) -> dict[str, str]:
    if provider.get("auth_mode") == "chatgpt_subscription_cached_login":
        codex_home = temp_root / "codex-home"
        codex_home.mkdir(parents=True, exist_ok=False)
        source_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
        source_auth = source_home / "auth.json"
        if not source_auth.is_file():
            raise RuntimeError("OpenAI Codex cached login is unavailable")
        shutil.copyfile(source_auth, codex_home / "auth.json")
        environment = os.environ.copy()
        environment["CODEX_HOME"] = str(codex_home)
        return environment
    if provider.get("auth_mode") != "experimental_bearer_token":
        raise RuntimeError("unsupported Study B provider authentication mode")
    api_key_path = Path(str(provider["api_key_file"]))
    if not api_key_path.is_absolute():
        api_key_path = ROOT / api_key_path
    model_catalog = Path(str(provider["model_catalog_json"]))
    if not model_catalog.is_absolute():
        model_catalog = ROOT / model_catalog
    key = api_key_path.read_text(encoding="utf-8").strip()
    if not key:
        raise RuntimeError("configured DeepSeek API key is empty")
    if not model_catalog.is_file():
        raise RuntimeError("configured DeepSeek model catalog does not exist")
    codex_home = temp_root / "codex-home"
    codex_home.mkdir(parents=True, exist_ok=False)
    lines = [
        f"model = {json.dumps(str(provider['model']))}",
        f"model_provider = {json.dumps(str(provider['id']))}",
        f"model_reasoning_effort = {json.dumps(str(provider['reasoning_effort']))}",
        'preferred_auth_method = "apikey"',
        'forced_login_method = "api"',
        f"model_catalog_json = {json.dumps(model_catalog.resolve().as_posix())}",
        "",
        f"[model_providers.{provider['id']}]",
        f"name = {json.dumps(str(provider['name']))}",
        f"base_url = {json.dumps(str(provider['base_url']).rstrip('/') + '/')}",
        f"wire_api = {json.dumps(str(provider['wire_api']))}",
        f"experimental_bearer_token = {json.dumps(key)}",
        "supports_websockets = false",
    ]
    (codex_home / "config.toml").write_text("\n".join(lines) + "\n", encoding="utf-8")
    environment = os.environ.copy()
    environment["CODEX_HOME"] = str(codex_home)
    return environment


def _initial_command(provider: Mapping[str, Any], schema_path: Path, workspace: Path) -> list[str]:
    executable = shutil.which("codex")
    if executable is None:
        raise RuntimeError("Codex CLI is unavailable on PATH")
    command = [
        executable,
        "exec",
        "--json",
        "--ignore-rules",
        "--skip-git-repo-check",
        "--output-schema",
        str(schema_path),
        "--disable",
        "apps",
        "--disable",
        "multi_agent",
        "--disable",
        "plugins",
        "--sandbox",
        "read-only",
        "-c",
        'approval_policy="never"',
        "-c",
        'web_search="disabled"',
        "-c",
        f"model_provider={json.dumps(str(provider['id']))}",
        "-c",
        f"model_reasoning_effort={json.dumps(str(provider['reasoning_effort']))}",
        "-m",
        str(provider["model"]),
        "-C",
        str(workspace),
    ]
    if provider.get("auth_mode") == "chatgpt_subscription_cached_login":
        command.insert(2, "--ignore-user-config")
        model_index = command.index("-m")
        provider_id = str(provider["id"])
        command[model_index:model_index] = [
            "-c",
            (
                f"model_providers.{provider_id}="
                '{name="OpenAI",wire_api="responses",requires_openai_auth=true,'
                "supports_websockets=false}"
            ),
        ]
    return command


def _resume_command(initial: Sequence[str], *, thread_id: str, schema_path: Path) -> list[str]:
    command = [*initial[:2], "resume", *initial[2:]]
    schema_index = command.index("--output-schema")
    command[schema_index + 1] = str(schema_path)
    for option in ("--sandbox", "-C"):
        index = command.index(option)
        del command[index : index + 2]
    command.extend([thread_id, "-"])
    return command


def _initial_prompt(cell: Mapping[str, Any]) -> str:
    packet = cell["public_packet"]
    public = {
        "task_id": cell["task_id"],
        "initial_world_model": cell["initial_world_model"],
        "metric_range": packet["metric_range"],
        "scoring_queries": packet["scoring_queries"],
    }
    return (
        "You are a scientific participant in a matched-evidence belief-updating study. "
        "Do not use shell, files, web, apps, plugins, MCP, or other tools. No experimental "
        "evidence is available in this first turn. Use only the supplied task and initial world "
        "model to predict every requested metric for every scoring query. Values must be in "
        "[0,1]. Return only the schema-conforming JSON; model_summary must be a concise public "
        "scientific summary, not private chain-of-thought.\n\nINPUT:\n"
        + json.dumps(public, ensure_ascii=False, sort_keys=True)
    )


def _evidence_prompt(cell: Mapping[str, Any]) -> str:
    packet = cell["public_packet"]
    public = {
        "task_id": cell["task_id"],
        "evidence": packet["evidence"],
        "scoring_queries": packet["scoring_queries"],
    }
    return (
        "The evaluator now reveals the fixed matched-evidence packet below. Treat these measured "
        "observations as authoritative. Without using any tool, update your model and predict all "
        "metrics for the same scoring queries. Do not merely repeat the evidence values because "
        "the scoring queries are disjoint. Return only schema-conforming JSON. model_summary and "
        "evidence_assessment must be concise public scientific summaries, not private "
        "chain-of-thought.\n\nMATCHED_EVIDENCE_INPUT:\n"
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
    progress.emit({"stage": f"{phase}_cell_started", "cell_id": cell_id})
    result: dict[str, Any] = {
        "schema_version": STUDY_B_CELL_VERSION,
        "study_id": cell.get("study_id", "work-ii-study-b-matched-evidence-v0.1"),
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
    provider_receipts: list[dict[str, Any]] = []
    try:
        with tempfile.TemporaryDirectory(prefix="chemworld-study-b-") as temporary:
            temp_root = Path(temporary)
            workspace = temp_root / "workspace"
            workspace.mkdir()
            environment = _prepare_codex_home(temp_root, provider)
            pre_schema = temp_root / "pre.schema.json"
            post_schema = temp_root / "post.schema.json"
            scoring_queries = cell["public_packet"]["scoring_queries"]
            _atomic_json(pre_schema, prediction_output_schema(scoring_queries, stage="pre"))
            _atomic_json(post_schema, prediction_output_schema(scoring_queries, stage="post"))
            initial = _initial_command(provider, pre_schema, workspace)

            def liveness(turn: str) -> Callable[[dict[str, Any]], None]:
                return lambda payload: progress.emit(
                    {
                        "stage": f"{phase}_turn_liveness",
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
            provider_receipts.append(
                {key: value for key, value in pre.items() if key != "final_payload"}
            )
            pre_payload = pre.get("final_payload")
            pre_errors = (
                validate_prediction_payload(pre_payload, scoring_queries, stage="pre")
                if isinstance(pre_payload, Mapping)
                else ["pre final payload is unavailable"]
            )
            thread_id = pre.get("thread_id")
            if pre.get("status") != "completed" or not isinstance(thread_id, str):
                raise _ProviderInfrastructureError(
                    "pre turn did not complete with a persistent thread"
                )
            if pre_errors:
                raise _ParticipantSchemaError("; ".join(pre_errors))
            resumed = _resume_command(initial, thread_id=thread_id, schema_path=post_schema)
            post = _launch_turn(
                resumed,
                _evidence_prompt(cell),
                cwd=workspace,
                environment=environment,
                timeout_s=float(provider["request_timeout_s"]),
                liveness=liveness("post"),
            )
            provider_receipts.append(
                {key: value for key, value in post.items() if key != "final_payload"}
            )
            post_payload = post.get("final_payload")
            post_errors = (
                validate_prediction_payload(post_payload, scoring_queries, stage="post")
                if isinstance(post_payload, Mapping)
                else ["post final payload is unavailable"]
            )
            if post.get("status") != "completed":
                raise _ProviderInfrastructureError("post turn did not complete")
            if post.get("thread_id") != thread_id:
                raise _ProviderInfrastructureError(
                    "post turn did not preserve the original Codex thread"
                )
            if post_errors:
                raise _ParticipantSchemaError("; ".join(post_errors))
            assert isinstance(pre_payload, Mapping)
            assert isinstance(post_payload, Mapping)
            result.update(
                {
                    "status": "completed",
                    "same_thread": True,
                    "pre_prediction": deepcopy(dict(pre_payload)),
                    "post_prediction": deepcopy(dict(post_payload)),
                    "scores": {
                        "pre": score_prediction_payload(pre_payload, cell["scoring_truth"]),
                        "post": score_prediction_payload(post_payload, cell["scoring_truth"]),
                    },
                    "provider_receipts": provider_receipts,
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
                "provider_receipts": provider_receipts,
            }
        )
    result["elapsed_s"] = round(time.perf_counter() - started, 3)
    result["result_sha256"] = hashlib.sha256(_canonical(result).encode("utf-8")).hexdigest()
    progress.emit(
        {
            "stage": f"{phase}_cell_terminal",
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
        if result.get("status") == "completed":
            result["provider_attempt_count"] = attempt_index + 1
            result["infrastructure_predecessors"] = predecessors
            result.pop("result_sha256", None)
            result["result_sha256"] = hashlib.sha256(
                _canonical(result).encode("utf-8")
            ).hexdigest()
            return result
        failure = result.get("failure")
        classification = failure.get("classification") if isinstance(failure, Mapping) else None
        retryable = classification in {"provider_infrastructure", "runner_infrastructure"}
        if not retryable or attempt_index >= retry_limit:
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
                "stage": f"{phase}_infrastructure_retry",
                "cell_id": cell["cell_id"],
                "completed_attempts": attempt_index + 1,
                "maximum_attempts": retry_limit + 1,
            }
        )
    raise AssertionError("unreachable Study B retry loop")


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
            if existing.get("schema_version") == STUDY_B_CELL_VERSION:
                results.append(existing)
                continue
        pending.append(cell)
    total = len(cells)
    completed = len(results)
    progress.emit(
        {
            "stage": f"{phase}_execution_started",
            "completed_cells": completed,
            "total_cells": total,
            "workers": workers,
        }
    )
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(
                _run_cell, cell, provider=provider, progress=progress, phase=phase
            ): cell
            for cell in pending
        }
        for future in as_completed(futures):
            result = future.result()
            _atomic_json(output_dir / f"{result['cell_id']}.json", result)
            results.append(result)
            completed += 1
            progress.emit(
                {
                    "stage": f"{phase}_progress",
                    "cell_id": result["cell_id"],
                    "completed_cells": completed,
                    "total_cells": total,
                    "failed_cells": sum(item.get("status") != "completed" for item in results),
                }
            )
    return results


def _canary_qualified(
    results: Sequence[Mapping[str, Any]], *, expected_term_count: int
) -> tuple[bool, list[str]]:
    errors: list[str] = []
    if len(results) != 3:
        errors.append("canary denominator differs from three arms")
    if {result.get("arm") for result in results} != {
        "opaque",
        "aligned_nominal",
        "misindexed_nominal",
    }:
        errors.append("canary arm coverage is incomplete")
    if len({result.get("public_packet_sha256") for result in results}) != 1:
        errors.append("canary arms did not receive an identical evidence packet")
    for result in results:
        if result.get("status") != "completed" or result.get("same_thread") is not True:
            errors.append(f"canary cell {result.get('cell_id')} did not complete two turns")
        scores = result.get("scores")
        if not isinstance(scores, Mapping) or any(
            scores.get(stage, {}).get("term_count") != expected_term_count
            for stage in ("pre", "post")
        ):
            errors.append(f"canary cell {result.get('cell_id')} has the wrong denominator")
    return not errors, errors


def _write_report(summary: Mapping[str, Any], path: Path) -> None:
    lines = [
        f"# {summary['study_id']} matched-evidence 结果",
        "",
        f"状态: `{summary['status']}`; 完成 {summary['completed_cell_count']}/"
        f"{summary['scheduled_cell_count']} sessions; 失败 {summary['failed_cell_count']}。",
        "",
        "Study B 不含 participant 物理实验。主量为同一模型看到固定证据前后的未展示查询误差下降, "
        "并比较 misindexed 与 aligned 的更新增益。",
        "",
        "## 分 locus 结果",
        "",
        "| locus | 完整 worlds | opaque 更新 | aligned 更新 | misindexed 更新 | "
        "主对比 | 主对比>0 worlds |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in summary["locus_rows"]:
        gains = row["mean_update_gain_by_arm"]
        lines.append(
            f"| {row['locus']} | {row['cluster_count']} | {gains['opaque']:.4f} | "
            f"{gains['aligned_nominal']:.4f} | {gains['misindexed_nominal']:.4f} | "
            f"{row['mean_primary_contrast']:.4f} | "
            f"{row['positive_primary_contrast_world_count']}/{row['cluster_count']} |"
        )
    if summary["status"] != "completed":
        lines.extend(
            [
                "",
                "当前仅为进度性结果; 只有全部 scheduled cells terminal 后才解释 "
                "seeking 与 updating 机制。",
            ]
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
    protocol = json.loads(protocol_path.read_text(encoding="utf-8"))
    if protocol.get("schema_version") == STUDY_B2_PROTOCOL_VERSION:
        prepare_study_b2_truth(
            protocol_path,
            repository_root=ROOT,
            output_root=output_root,
            progress=progress.emit,
        )
        manifest = build_study_b2_manifest(
            protocol_path,
            repository_root=ROOT,
            output_root=output_root,
        )
        summarize = summarize_study_b2_results
    else:
        manifest = build_study_b_manifest(args.protocol, repository_root=ROOT)
        summarize = summarize_study_b_results
    expected_term_count = int(
        manifest.get(
            "scoring_term_count",
            sum(
                len(query["metric_ids"])
                for query in manifest["cells"][0]["public_packet"]["scoring_queries"]
            ),
        )
    )
    _atomic_json(output_root / "input_manifest.json", manifest)
    progress.emit(
        {
            "stage": "provider_free_preflight_complete",
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
        canary_cells = [cell for cell in manifest["cells"] if cell["cluster_id"] == first_cluster]
        canary_results = _execute_cells(
            canary_cells,
            provider=provider,
            output_dir=output_root / "canary",
            progress=progress,
            phase="canary",
            workers=args.workers,
            resume=args.resume,
        )
        qualified, errors = _canary_qualified(
            canary_results,
            expected_term_count=expected_term_count,
        )
        canary_summary = {
            "schema_version": "chemworld-work-ii-study-b-canary-summary-0.1",
            "qualified": qualified,
            "session_count": len(canary_results),
            "errors": errors,
            "scientific_outcomes_used_for_design": False,
        }
        _atomic_json(output_root / "canary_summary.json", canary_summary)
        if not qualified:
            progress.emit({"stage": "canary_failed", "errors": errors})
            return 2
        progress.emit({"stage": "canary_qualified", "completed_cells": 3, "total_cells": 3})
    if args.execute:
        canary_path = output_root / "canary_summary.json"
        canary_qualified = (
            canary_path.is_file()
            and json.loads(canary_path.read_text(encoding="utf-8"))["qualified"] is True
        )
        if not canary_qualified:
            raise RuntimeError(
                "formal matched-evidence execution requires a qualified three-arm canary"
            )
        results = _execute_cells(
            manifest["cells"],
            provider=provider,
            output_dir=output_root / "cells",
            progress=progress,
            phase="formal",
            workers=args.workers,
            resume=args.resume,
        )
        summary = summarize(manifest, results)
        _atomic_json(output_root / "summary.json", summary)
        _write_report(summary, output_root / "REPORT_ZH.md")
    if args.analyze and not args.execute:
        results = [
            json.loads(path.read_text(encoding="utf-8"))
            for path in sorted((output_root / "cells").glob("*.json"))
        ]
        summary = summarize(manifest, results)
        _atomic_json(output_root / "summary.json", summary)
        _write_report(summary, output_root / "REPORT_ZH.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
