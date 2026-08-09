#!/usr/bin/env python3
"""Build/check the Work II formal matrix preflight; execution remains fail-closed."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from collections.abc import Mapping
from pathlib import Path
from typing import Any
from uuid import uuid4

from chemworld.eval.provenance import file_sha256, write_json_atomic
from chemworld.eval.work_ii_formal import (
    WorkIIFormalCellStore,
    build_formal_preflight,
    validate_formal_bindings,
    validate_formal_preflight,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DESIGN = ROOT / "configs/benchmark/work_ii_formal_design_v0.1.json"
DEFAULT_ANALYSIS = ROOT / "configs/benchmark/work_ii_analysis_plan_v0.1.json"
DEFAULT_PREFLIGHT = (
    ROOT
    / "workstreams/flagship_tasks/reports/"
    "work-ii-formal-matrix-runner-preflight-v0.1.json"
)
CELL_RUNNER = ROOT / "scripts/run_work_ii_campaign_pilot.py"


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--preflight", action="store_true")
    mode.add_argument("--execute", action="store_true")
    parser.add_argument("--design", type=Path, default=DEFAULT_DESIGN)
    parser.add_argument("--analysis", type=Path, default=DEFAULT_ANALYSIS)
    parser.add_argument("--output", type=Path, default=DEFAULT_PREFLIGHT)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--output-root", type=Path)
    parser.add_argument("--progress-file", type=Path)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--allow-formal-execution", action="store_true")
    parser.add_argument("--qualification-receipt", type=Path)
    parser.add_argument("--currency-ceiling-usd", type=float)
    return parser.parse_args()


def _run_preflight(args: argparse.Namespace) -> int:
    if any(
        (
            args.manifest is not None,
            args.output_root is not None,
            args.progress_file is not None,
            args.resume,
            args.allow_formal_execution,
            args.qualification_receipt is not None,
            args.currency_ceiling_usd is not None,
        )
    ):
        raise RuntimeError("execution-only options cannot be used with --preflight")
    report = build_formal_preflight(ROOT, args.design, args.analysis)
    errors = validate_formal_preflight(report)
    if errors or report["errors"]:
        raise RuntimeError(
            "formal preflight validation failed: "
            + "; ".join([*report["errors"], *errors])
        )
    output = args.output.resolve()
    if args.check:
        if not output.is_file():
            raise RuntimeError(f"missing committed formal preflight: {output}")
        committed = json.loads(output.read_text(encoding="utf-8"))
        if committed != report:
            raise RuntimeError("committed formal preflight differs from deterministic rebuild")
    else:
        write_json_atomic(output, report)
    print(
        json.dumps(
            {
                "status": report["status"],
                "formal_execution_allowed": report["formal_execution_allowed"],
                "tasks": report["expected_counts"]["tasks"],
                "clusters": report["expected_counts"]["independent_task_world_clusters"],
                "cells": report["expected_counts"]["participant_cells"],
                "complete_experiments": report["expected_counts"]["complete_experiments"],
                "blocking_requirement_count": len(report["blocking_requirements"]),
                "preflight_sha256": report["preflight_sha256"],
                "output": str(output),
                "check": bool(args.check),
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


def _emit(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rendered = json.dumps(dict(payload), ensure_ascii=False, sort_keys=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(rendered + "\n")
    print(rendered, flush=True)


def _load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object")
    return value


def _terminal_state(summary: Mapping[str, Any]) -> tuple[str, str]:
    qualification = summary.get("qualification")
    exact_replay = summary.get("exact_replay")
    if (
        summary.get("completed") is True
        and isinstance(qualification, Mapping)
        and qualification.get("passed") is True
        and isinstance(exact_replay, Mapping)
        and exact_replay.get("verified") is True
    ):
        return "completed", "scientific_completed_qualified_campaign"
    analysis = summary.get("analysis")
    operation_attempts = (
        int(analysis.get("operation_attempt_count", 0))
        if isinstance(analysis, Mapping)
        else 0
    )
    if operation_attempts > 0:
        return (
            "right_censored",
            "method_right_censored_failure_after_accepted_operation",
        )
    return "failed", "method_failed_unscorable_before_first_operation"


def _result_binding(
    output_root: Path,
    attempt_root: Path,
    summary: Mapping[str, Any],
    *,
    return_code: int,
) -> dict[str, Any]:
    def bind(path: Path) -> dict[str, Any] | None:
        if not path.is_file():
            return None
        return {
            "path": path.relative_to(output_root).as_posix(),
            "sha256": file_sha256(path),
        }

    receipts = summary.get("provider_receipts")
    return {
        "return_code": int(return_code),
        "summary": bind(attempt_root / "summary.json"),
        "report": bind(attempt_root / "report.json"),
        "trajectory": bind(attempt_root / "trajectory.jsonl"),
        "completed": summary.get("completed") is True,
        "analysis": summary.get("analysis"),
        "method_resources": summary.get("method_resources"),
        "exact_replay": summary.get("exact_replay"),
        "qualification": summary.get("qualification"),
        "provider_receipt_count": len(receipts) if isinstance(receipts, list) else 0,
    }


def _unfinalized_trajectory_evidence(path: Path) -> dict[str, Any] | None:
    """Treat any persisted trajectory bytes as scientific use that forbids replacement."""

    if not path.is_file() or path.stat().st_size == 0:
        return None
    nonempty_lines = 0
    valid_json_lines = 0
    with path.open("r", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            if not line.strip():
                continue
            nonempty_lines += 1
            try:
                json.loads(line)
            except json.JSONDecodeError:
                continue
            valid_json_lines += 1
    return {
        "trajectory_byte_count": path.stat().st_size,
        "nonempty_line_count": nonempty_lines,
        "valid_json_line_count": valid_json_lines,
        "malformed_or_partial_line_count": nonempty_lines - valid_json_lines,
    }


def execute_manifest(
    *,
    manifest: Mapping[str, Any],
    manifest_path: Path,
    output_root: Path,
    progress_path: Path,
    resume: bool,
    cell_runner: Path = CELL_RUNNER,
) -> dict[str, Any]:
    """Execute canonical missing cells in same-world three-arm subprocess triplets."""

    binding_errors = validate_formal_bindings(ROOT, manifest)
    if binding_errors:
        raise RuntimeError(
            "formal manifest binding validation failed: " + "; ".join(binding_errors)
        )
    if manifest.get("formal_execution_allowed") is not True:
        raise RuntimeError("formal manifest does not authorize participant execution")
    if manifest.get("blocking_requirements"):
        raise RuntimeError("formal manifest still contains blocking requirements")
    output_root = output_root.resolve()
    if output_root.exists() and not resume:
        raise FileExistsError(f"refusing to overwrite formal output root: {output_root}")
    if not output_root.exists() and resume:
        raise FileNotFoundError("missing-only resume requires an existing output root")
    output_root.mkdir(parents=True, exist_ok=resume)
    manifest_copy = output_root / "execution_manifest.json"
    if manifest_copy.exists():
        if _load_object(manifest_copy) != dict(manifest):
            raise RuntimeError("existing execution manifest differs from the requested manifest")
    else:
        write_json_atomic(manifest_copy, dict(manifest))
    store = WorkIIFormalCellStore(output_root / "store", manifest)
    pending = store.pending_cells(resume=resume)
    pending_keys = {str(cell["cell_key_sha256"]) for cell in pending}
    clusters: list[list[dict[str, Any]]] = []
    for cell in manifest.get("cells", []):
        if not isinstance(cell, Mapping) or cell.get("cell_key_sha256") not in pending_keys:
            continue
        candidate = dict(cell)
        if not clusters or clusters[-1][0]["world_cluster_id"] != candidate["world_cluster_id"]:
            clusters.append([])
        clusters[-1].append(candidate)
    infrastructure_failures = 0
    _emit(
        progress_path,
        {
            "event": "formal_matrix_started" if not resume else "formal_matrix_resumed",
            "expected_cells": len(manifest.get("cells", [])),
            "terminal_cells_before_start": len(manifest.get("cells", [])) - len(pending),
            "pending_cells": len(pending),
        },
    )
    for cluster_index, cells in enumerate(clusters, start=1):
        processes: list[dict[str, Any]] = []
        _emit(
            progress_path,
            {
                "event": "world_triplet_started",
                "cluster_index": cluster_index,
                "world_cluster_id": cells[0]["world_cluster_id"],
                "active_cell_count": len(cells),
                "max_concurrency": 3,
            },
        )
        for cell in cells:
            key = str(cell["cell_key_sha256"])
            attempt_id = uuid4().hex
            store.record_provider_attempt_launch(key, attempt_id=attempt_id)
            attempt_root = output_root / "attempts" / key / attempt_id
            log_path = output_root / "logs" / key / f"{attempt_id}.log"
            log_path.parent.mkdir(parents=True, exist_ok=True)
            child_progress = output_root / "progress" / key / f"{attempt_id}.jsonl"
            command = [
                sys.executable,
                str(cell_runner),
                "--config",
                str((ROOT / str(cell["campaign_config_path"])).resolve()),
                "--output",
                str(attempt_root),
                "--progress-file",
                str(child_progress),
                "--world-seed",
                str(cell["world_seed"]),
                "--prior-arm",
                str(cell["prior_arm"]),
                "--formal-manifest",
                str(manifest_copy.resolve()),
                "--formal-cell-key",
                key,
                "--allow-formal-execution",
            ]
            log_handle = log_path.open("w", encoding="utf-8")
            kwargs: dict[str, Any] = {}
            if os.name == "nt":
                kwargs["creationflags"] = getattr(subprocess, "CREATE_NO_WINDOW", 0)
            try:
                process = subprocess.Popen(
                    command,
                    cwd=ROOT,
                    stdout=log_handle,
                    stderr=subprocess.STDOUT,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    **kwargs,
                )
            except OSError as error:
                log_handle.write(f"provider process launch failed: {type(error).__name__}\n")
                log_handle.close()
                infrastructure_failures += 1
                store.record_infrastructure_failure(
                    key,
                    error,
                    log_reference=log_path.relative_to(output_root).as_posix(),
                    log_sha256=file_sha256(log_path),
                )
                _emit(
                    progress_path,
                    {
                        "event": "formal_cell_infrastructure_failure",
                        "cell_id": cell["cell_id"],
                        "error_type": type(error).__name__,
                    },
                )
                continue
            processes.append(
                {
                    "cell": cell,
                    "process": process,
                    "log_handle": log_handle,
                    "log_path": log_path,
                    "attempt_root": attempt_root,
                }
            )
        triplet_started = time.monotonic()
        next_heartbeat = triplet_started + 30.0
        while True:
            active = [
                state
                for state in processes
                if state["process"].poll() is None
            ]
            if not active:
                break
            now = time.monotonic()
            if now >= next_heartbeat:
                _emit(
                    progress_path,
                    {
                        "event": "world_triplet_heartbeat",
                        "cluster_index": cluster_index,
                        "world_cluster_id": cells[0]["world_cluster_id"],
                        "active_cell_count": len(active),
                        "elapsed_seconds": round(now - triplet_started, 3),
                    },
                )
                next_heartbeat = now + 30.0
            time.sleep(min(1.0, max(0.05, next_heartbeat - now)))
        for state in processes:
            process = state["process"]
            return_code = process.wait()
            state["log_handle"].close()
            cell = state["cell"]
            key = str(cell["cell_key_sha256"])
            summary_path = state["attempt_root"] / "summary.json"
            try:
                summary = _load_object(summary_path)
                formal_cell = summary.get("formal_cell")
                if (
                    summary.get("formal_result") is not True
                    or not isinstance(formal_cell, Mapping)
                    or formal_cell.get("cell_key_sha256") != key
                ):
                    raise ValueError("cell summary lacks its exact formal binding")
                terminal_state, reason_code = _terminal_state(summary)
                store.write_terminal(
                    key,
                    state=terminal_state,
                    reason_code=reason_code,
                    result=_result_binding(
                        output_root,
                        state["attempt_root"],
                        summary,
                        return_code=return_code,
                    ),
                )
                _emit(
                    progress_path,
                    {
                        "event": "formal_cell_terminal",
                        "cell_id": cell["cell_id"],
                        "state": terminal_state,
                    },
                )
            except (OSError, ValueError, json.JSONDecodeError) as error:
                log_path = state["log_path"]
                trajectory_evidence = _unfinalized_trajectory_evidence(
                    state["attempt_root"] / "trajectory.jsonl"
                )
                if trajectory_evidence is not None:
                    partial_summary = {
                        "completed": False,
                        "analysis": {
                            "operation_attempt_count": max(
                                1, int(trajectory_evidence["nonempty_line_count"])
                            )
                        },
                    }
                    result = _result_binding(
                        output_root,
                        state["attempt_root"],
                        partial_summary,
                        return_code=return_code,
                    )
                    result["unfinalized_trajectory_evidence"] = trajectory_evidence
                    result["summary_validation_error_type"] = type(error).__name__
                    store.write_terminal(
                        key,
                        state="right_censored",
                        reason_code=(
                            "method_right_censored_unfinalized_child_after_trajectory_evidence"
                        ),
                        result=result,
                    )
                    _emit(
                        progress_path,
                        {
                            "event": "formal_cell_terminal",
                            "cell_id": cell["cell_id"],
                            "state": "right_censored",
                            "unfinalized_trajectory_evidence": True,
                        },
                    )
                else:
                    infrastructure_failures += 1
                    store.record_infrastructure_failure(
                        key,
                        error,
                        log_reference=log_path.relative_to(output_root).as_posix(),
                        log_sha256=file_sha256(log_path),
                    )
                    _emit(
                        progress_path,
                        {
                            "event": "formal_cell_infrastructure_failure",
                            "cell_id": cell["cell_id"],
                            "error_type": type(error).__name__,
                        },
                    )
        if infrastructure_failures:
            break
    audit = store.audit()
    write_json_atomic(output_root / "store_audit.json", audit)
    report = {
        "schema_version": "chemworld-work-ii-formal-execution-progress-0.1",
        "formal_result": False,
        "status": (
            "all_cells_terminal"
            if audit["complete"]
            else "infrastructure_incomplete_missing_only_resume_required"
        ),
        "expected_cell_count": audit["expected_cell_count"],
        "terminal_count": audit["terminal_count"],
        "state_counts": audit["state_counts"],
        "missing_cell_count": len(audit["missing_cell_key_sha256"]),
        "infrastructure_failure_count_this_attempt": infrastructure_failures,
        "store_audit_sha256": audit["audit_sha256"],
    }
    write_json_atomic(output_root / "execution_progress.json", report)
    _emit(progress_path, {"event": "formal_matrix_attempt_finished", **report})
    return report


def _run_execute(args: argparse.Namespace) -> int:
    if args.check or args.output != DEFAULT_PREFLIGHT:
        raise RuntimeError("--check and --output apply only to --preflight")
    required = {
        "--manifest": args.manifest,
        "--output-root": args.output_root,
        "--qualification-receipt": args.qualification_receipt,
        "--currency-ceiling-usd": args.currency_ceiling_usd,
        "--progress-file": args.progress_file,
    }
    missing = [name for name, value in required.items() if value is None]
    if missing:
        raise RuntimeError("--execute is missing required options: " + ", ".join(missing))
    if not args.allow_formal_execution:
        raise RuntimeError("--execute requires --allow-formal-execution")
    manifest = json.loads(args.manifest.resolve().read_text(encoding="utf-8"))
    if not isinstance(manifest, dict):
        raise RuntimeError("formal manifest must contain an object")
    errors = validate_formal_preflight(manifest)
    if errors:
        raise RuntimeError("formal manifest validation failed: " + "; ".join(errors))
    if manifest.get("formal_execution_allowed") is not True:
        blockers = manifest.get("blocking_requirements", [])
        raise RuntimeError(
            "formal execution remains blocked by the committed manifest: "
            + "; ".join(str(item) for item in blockers)
        )
    binding_errors = validate_formal_bindings(ROOT, manifest)
    if binding_errors:
        raise RuntimeError(
            "formal manifest binding validation failed: " + "; ".join(binding_errors)
        )
    receipt = _load_object(args.qualification_receipt.resolve())
    if (
        receipt.get("schema_version")
        != "chemworld-work-ii-method-qualification-receipt-0.1"
        or receipt.get("status") != "passed"
        or receipt.get("formal_preflight_sha256") != manifest.get("preflight_sha256")
    ):
        raise RuntimeError("method qualification receipt does not authorize this manifest")
    approved_ceiling = receipt.get("approved_currency_ceiling_usd")
    if (
        isinstance(approved_ceiling, bool)
        or not isinstance(approved_ceiling, int | float)
        or float(approved_ceiling) != float(args.currency_ceiling_usd)
        or float(approved_ceiling) <= 0.0
    ):
        raise RuntimeError("currency ceiling differs from the qualification receipt")
    report = execute_manifest(
        manifest=manifest,
        manifest_path=args.manifest,
        output_root=args.output_root,
        progress_path=args.progress_file,
        resume=bool(args.resume),
    )
    return 0 if report["status"] == "all_cells_terminal" else 1


def main() -> int:
    args = _parse_args()
    return _run_preflight(args) if args.preflight else _run_execute(args)


if __name__ == "__main__":
    raise SystemExit(main())
