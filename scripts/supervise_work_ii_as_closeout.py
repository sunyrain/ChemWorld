#!/usr/bin/env python3
"""Run one provider-free A-S closeout check or execute its integration once."""

from __future__ import annotations

import argparse
import json
import shutil
from collections.abc import Callable, Mapping
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from chemworld.eval.provenance import write_json_atomic
from chemworld.eval.work_ii_resource_calibration import (
    build_resource_calibration_execution_manifest,
    build_resource_calibration_readiness,
    validate_resource_calibration_manifest,
    validate_resource_calibration_readiness,
)

if __package__:
    from scripts.integrate_work_ii_as_development_result import (
        integrate_development_result,
    )
else:
    from integrate_work_ii_as_development_result import integrate_development_result

DEFAULT_PROTOCOL_MANIFEST = Path(
    "configs/benchmark/work_ii_resource_calibration_manifest_v0.1.json"
)
DEFAULT_DYNAMIC_MANIFEST = Path(
    "workstreams/flagship_tasks/reports/"
    "work-ii-resource-calibration-execution-manifest-v0.1.json"
)


def _timestamp() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def _inside(root: Path, path: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
    except ValueError:
        return False
    return True


def _external_path(path: Path, roots: tuple[Path, Path], *, label: str) -> Path:
    resolved = path.resolve()
    if any(_inside(root, resolved) for root in roots):
        raise ValueError(f"{label} must remain outside both repositories")
    return resolved


def _source_summary_path(source_root: Path, source_summary: Path) -> Path:
    path = source_summary if source_summary.is_absolute() else source_root / source_summary
    path = path.resolve()
    if not _inside(source_root, path):
        raise ValueError("A-S source summary escapes the source repository")
    return path


def _append_event(event_log: Path, event: Mapping[str, Any]) -> None:
    event_log.parent.mkdir(parents=True, exist_ok=True)
    with event_log.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(dict(event), ensure_ascii=False, sort_keys=True) + "\n")


def _rollback_passing_integration(
    *,
    source_root: Path,
    destination_root: Path,
    integration: Mapping[str, Any],
) -> None:
    """Remove only paths published by this passing integration attempt."""

    relative_paths: list[str] = []
    if source_root != destination_root and isinstance(integration.get("raw_run"), str):
        relative_paths.append(str(integration["raw_run"]))
    for key in ("canonical_summary", "canonical_package"):
        if isinstance(integration.get(key), str):
            relative_paths.append(str(integration[key]))
    d1 = integration.get("canonical_d1_configs")
    if isinstance(d1, Mapping):
        relative_paths.extend(str(path) for path in d1.values() if isinstance(path, str))
    for relative in reversed(relative_paths):
        path = (destination_root / relative).resolve()
        if path == destination_root or not _inside(destination_root, path):
            raise RuntimeError("refusing unsafe A-S closeout rollback path")
        if path.is_dir():
            shutil.rmtree(path)
        elif path.exists():
            path.unlink()


def supervise_once(
    *,
    source_root: Path,
    source_summary: Path,
    destination_root: Path,
    execute: bool,
    emit: Callable[[Mapping[str, Any]], None] | None = None,
) -> dict[str, Any]:
    """Check once, or execute integration and W2-26 zero-call preflight once."""

    source_root = source_root.resolve()
    destination_root = destination_root.resolve()
    summary_path = _source_summary_path(source_root, source_summary)
    if not source_root.is_dir() or not destination_root.is_dir():
        raise FileNotFoundError("source and destination repository roots must exist")
    if not summary_path.is_file():
        return {
            "status": "waiting_for_source_summary",
            "execute_requested": execute,
            "provider_calls_executed": 0,
            "source_summary": str(summary_path),
        }
    if not execute:
        return {
            "status": "ready_for_execute",
            "execute_requested": False,
            "provider_calls_executed": 0,
            "source_summary": str(summary_path),
        }

    def evidence_progress(label: str, completed: int, total: int) -> None:
        if emit is not None:
            emit(
                {
                    "event": "as_deep_validation_progress",
                    "candidate_world": label,
                    "completed_receipts": completed,
                    "total_receipts": total,
                }
            )

    integration = integrate_development_result(
        source_root=source_root,
        source_summary=summary_path,
        destination_root=destination_root,
        evidence_progress=evidence_progress,
    )
    if integration.get("provider_execution_authorized") is not False:
        raise RuntimeError("A-S integration crossed its provider-free boundary")
    if emit is not None:
        emit({"event": "as_integration_complete", **integration})

    if integration.get("resource_calibration_candidate_ready") is not True:
        if integration.get("status") != (
            "integrated_scientific_rejection_w2_26_blocked"
        ):
            raise RuntimeError("A-S integration returned an invalid non-ready state")
        return {
            "status": "scientific_rejection_integrated",
            "execute_requested": True,
            "provider_calls_executed": 0,
            "integration": integration,
            "w2_26_manifest_generated": False,
            "w2_26_preflight": None,
        }

    protocol_path = destination_root / DEFAULT_PROTOCOL_MANIFEST
    dynamic_path = destination_root / DEFAULT_DYNAMIC_MANIFEST
    manifest_written = False
    try:
        if dynamic_path.exists():
            raise FileExistsError(
                f"refusing to overwrite W2-26 dynamic manifest: {dynamic_path}"
            )
        manifest = build_resource_calibration_execution_manifest(
            destination_root,
            protocol_path,
        )
        manifest_errors = validate_resource_calibration_manifest(
            destination_root, manifest
        )
        if manifest_errors:
            raise RuntimeError(
                "W2-26 dynamic manifest validation failed: "
                + "; ".join(manifest_errors)
            )
        write_json_atomic(dynamic_path, manifest)
        manifest_written = True
        preflight = build_resource_calibration_readiness(
            destination_root, dynamic_path
        )
        preflight_errors = validate_resource_calibration_readiness(preflight)
        if preflight_errors:
            raise RuntimeError(
                "W2-26 preflight validation failed: " + "; ".join(preflight_errors)
            )
        if (
            preflight.get("status") != "ready_authorization_blocked"
            or preflight.get("missing_pattern_rounds") != []
            or preflight.get("provider_execution_allowed") is not False
            or preflight.get("provider_calls_executed") != 0
        ):
            raise RuntimeError("W2-26 preflight did not reach the zero-call ready state")
    except Exception:
        if manifest_written and dynamic_path.exists():
            dynamic_path.unlink()
        _rollback_passing_integration(
            source_root=source_root,
            destination_root=destination_root,
            integration=integration,
        )
        raise

    if emit is not None:
        emit(
            {
                "event": "w2_26_preflight_complete",
                "status": preflight["status"],
                "missing_pattern_rounds": preflight["missing_pattern_rounds"],
                "provider_calls_executed": preflight["provider_calls_executed"],
            }
        )
    return {
        "status": "integrated_w2_26_preflight_ready",
        "execute_requested": True,
        "provider_calls_executed": 0,
        "integration": integration,
        "w2_26_manifest_generated": True,
        "w2_26_manifest": DEFAULT_DYNAMIC_MANIFEST.as_posix(),
        "w2_26_preflight": preflight,
    }


def supervise_and_record(
    *,
    source_root: Path,
    source_summary: Path,
    destination_root: Path,
    status_output: Path,
    event_log: Path,
    execute: bool,
) -> tuple[dict[str, Any], int]:
    """Run one supervisor turn and always emit an external terminal status."""

    source_root = source_root.resolve()
    destination_root = destination_root.resolve()
    roots = (source_root, destination_root)
    status_output = _external_path(status_output, roots, label="status output")
    event_log = _external_path(event_log, roots, label="event log")

    def emit(event: Mapping[str, Any]) -> None:
        _append_event(event_log, {"at": _timestamp(), **dict(event)})

    emit({"event": "as_closeout_supervisor_started", "execute": execute})
    try:
        result = supervise_once(
            source_root=source_root,
            source_summary=source_summary,
            destination_root=destination_root,
            execute=execute,
            emit=emit,
        )
        exit_code = 0
    except Exception as error:
        result = {
            "status": "fail_closed",
            "execute_requested": execute,
            "provider_calls_executed": 0,
            "error_type": type(error).__name__,
            "error": str(error),
        }
        exit_code = 1
    terminal = {"at": _timestamp(), **result}
    write_json_atomic(status_output, terminal)
    emit({"event": "as_closeout_supervisor_terminal", **result})
    return terminal, exit_code


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--source-summary", type=Path, required=True)
    parser.add_argument("--destination-root", type=Path, required=True)
    parser.add_argument("--status-output", type=Path, required=True)
    parser.add_argument("--event-log", type=Path, required=True)
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()
    result, exit_code = supervise_and_record(
        source_root=args.source_root,
        source_summary=args.source_summary,
        destination_root=args.destination_root,
        status_output=args.status_output,
        event_log=args.event_log,
        execute=bool(args.execute),
    )
    print(json.dumps(result, ensure_ascii=False, sort_keys=True), flush=True)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
