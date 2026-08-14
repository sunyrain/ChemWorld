#!/usr/bin/env python3
"""Build, authorize, or execute the full task-specific W2-26 calibration."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from collections.abc import Mapping
from pathlib import Path
from uuid import uuid4

from chemworld.eval.provenance import (
    canonical_json_sha256,
    file_sha256,
    write_json_atomic,
)
from chemworld.eval.work_ii_resource_calibration_v02 import (
    DEEPSEEK_PLANNING_RESOURCE_LIMITS,
    DEEPSEEK_PROVIDER_CONTRACT,
    DEEPSEEK_PROVIDER_RUNTIME,
    DEEPSEEK_RUNTIME_CONFIG_ROOT,
    RESOURCE_CALIBRATION_ARMS,
    cell_has_platform_defect,
    pattern_key,
    pattern_slug,
)
from chemworld.eval.work_ii_resource_calibration_v02 import (
    build_authorization as build_resource_calibration_authorization,
)
from chemworld.eval.work_ii_resource_calibration_v02 import (
    build_execution_manifest as build_resource_calibration_execution_manifest,
)
from chemworld.eval.work_ii_resource_calibration_v02 import (
    build_summary as build_resource_calibration_summary,
)
from chemworld.eval.work_ii_resource_calibration_v02 import (
    empty_summary as empty_resource_calibration_summary,
)
from chemworld.eval.work_ii_resource_calibration_v02 import (
    validate_authorization as validate_resource_calibration_authorization,
)
from chemworld.eval.work_ii_resource_calibration_v02 import (
    validate_manifest as validate_resource_calibration_manifest,
)
from chemworld.eval.work_ii_resource_calibration_v02 import (
    validate_summary as validate_resource_calibration_summary,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = (
    ROOT / "configs/benchmark/work_ii_resource_calibration_manifest_v0.2.json"
)
DEFAULT_FORMAL_DESIGN = ROOT / "configs/benchmark/work_ii_formal_design_v0.2.json"
DEFAULT_AP_SELECTION_PROTOCOL = (
    ROOT / "configs/benchmark/work_ii_c2_ap_selection_protocol_v0.1.json"
)
DEFAULT_AS_SELECTION_PROTOCOL = (
    ROOT / "configs/benchmark/work_ii_c2_as_selection_protocol_v0.1.json"
)
DEFAULT_AP_Q2_GENERATION = (
    ROOT / "workstreams/flagship_tasks/reports/"
    "work-ii-reaction-safety-matched-prior-qualification-20260811.json"
)
DEFAULT_AS_Q2_GENERATION = (
    ROOT / "workstreams/flagship_tasks/reports/"
    "work-ii-as-paired-law-q1-q2-five-world-20260812.json"
)
CELL_RUNNER = ROOT / "scripts/run_work_ii_campaign_pilot.py"


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object")
    return value


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--output", type=Path)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--summary-template", action="store_true")
    mode.add_argument("--authorize", action="store_true")
    mode.add_argument("--execute", action="store_true")
    mode.add_argument("--build-execution-manifest", action="store_true")
    parser.add_argument("--formal-design", type=Path, default=DEFAULT_FORMAL_DESIGN)
    parser.add_argument("--ap-selection-protocol", type=Path, default=DEFAULT_AP_SELECTION_PROTOCOL)
    parser.add_argument("--as-selection-protocol", type=Path, default=DEFAULT_AS_SELECTION_PROTOCOL)
    parser.add_argument("--ap-q2-generation", type=Path, default=DEFAULT_AP_Q2_GENERATION)
    parser.add_argument("--as-q2-generation", type=Path, default=DEFAULT_AS_Q2_GENERATION)
    parser.add_argument("--authorization", type=Path)
    parser.add_argument("--allow-provider-execution", action="store_true")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--currency-ceiling-usd", type=float)
    parser.add_argument("--approved-at")
    parser.add_argument("--pricing-source")
    parser.add_argument("--pricing-observed-at")
    parser.add_argument("--cache-hit-input-usd-per-million", type=float)
    parser.add_argument("--cache-miss-input-usd-per-million", type=float)
    parser.add_argument("--output-usd-per-million", type=float)
    parser.add_argument("--unlimited-spend-authorized", action="store_true")
    parser.add_argument("--provider-contract-confirmed-by-user", action="store_true")
    parser.add_argument("--credential-rotation-confirmed-by-user", action="store_true")
    parser.add_argument(
        "--provider-cohort",
        choices=("source", "deepseek-v4-flash"),
        default="source",
        help="materialize an isolated provider cohort without changing scientific coverage",
    )
    return parser.parse_args()


def _inside_root(path: Path, *, label: str) -> Path:
    resolved = path.resolve()
    try:
        resolved.relative_to(ROOT.resolve())
    except ValueError as error:
        raise RuntimeError(f"{label} must be inside the repository") from error
    return resolved


def _write_once(path: Path, payload: Mapping[str, object]) -> None:
    if path.exists():
        raise RuntimeError(f"refusing to replace immutable W2-26 artifact: {path}")
    write_json_atomic(path, dict(payload))


def _emit(path: Path, payload: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rendered = json.dumps(dict(payload), ensure_ascii=False, sort_keys=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(rendered + "\n")
    print(rendered, flush=True)


def _observed_currency(
    row: Mapping[str, object], authorization: Mapping[str, object]
) -> float | None:
    if authorization.get("unlimited_spend_authorized") is True:
        return None
    method = row.get("method_resources")
    method = method if isinstance(method, Mapping) else {}
    pricing = authorization.get("pricing")
    pricing = pricing if isinstance(pricing, Mapping) else {}
    input_tokens = int(method.get("input_token_count", 0))
    uncached = int(method.get("uncached_input_token_count", 0))
    output = int(method.get("output_token_count", 0))
    return round(
        (
            max(0, input_tokens - uncached) * float(pricing["cache_hit_input"])
            + uncached * float(pricing["cache_miss_input"])
            + output * float(pricing["output"])
        )
        / 1_000_000,
        12,
    )


def _load_and_validate_reservations(
    output_root: Path, authorization: Mapping[str, object]
) -> float | None:
    unlimited = authorization.get("unlimited_spend_authorized") is True
    rows = []
    contracts = {
        pattern_key(row): row
        for row in authorization["pattern_attempt_contracts"]
    }
    for path in output_root.glob(
        "triplet_attempts/*/attempt-*/cost_reservation.json"
    ):
        row = _load(path)
        key = pattern_key(row)
        attempt = int(row.get("attempt_number", -1))
        sequence = int(row.get("reservation_sequence_number", -1))
        expected = contracts.get(key)
        if (
            expected is None
            or attempt not in {1, 2}
            or sequence <= 0
            or path.parent.parent.name != pattern_slug(row)
            or row.get("authorization_sha256")
            != authorization.get("authorization_sha256")
            or (
                row.get("reserved_cost_usd")
                != expected.get("initial_triplet_cost_cap_usd")
            )
        ):
            raise RuntimeError("W2-26 cost reservation receipt is invalid")
        rows.append((sequence, key, attempt, path, row))
    sequences = sorted(sequence for sequence, *_rest in rows)
    if sequences != list(range(1, len(rows) + 1)):
        raise RuntimeError("W2-26 cost reservation sequence is not contiguous")
    observed_attempts: dict[tuple[str, str, int], list[int]] = {}
    for _sequence, key, attempt, _path, _row in rows:
        observed_attempts.setdefault(key, []).append(attempt)
    for key, raw_attempts in observed_attempts.items():
        attempts = sorted(
            raw_attempts
        )
        if attempts != list(range(1, len(attempts) + 1)):
            identity = dict(
                zip(("locus", "task_id", "rounds"), key, strict=True)
            )
            raise RuntimeError(
                f"W2-26 {pattern_slug(identity)} reservation sequence is not contiguous"
            )
    if unlimited:
        if any(
            row.get("reserved_cost_usd") is not None
            or row.get("cumulative_reserved_cost_usd") is not None
            for *_prefix, row in rows
        ):
            raise RuntimeError("W2-26 unlimited reservation contains a currency amount")
        return None
    total = 0.0
    for _sequence, _key, _attempt, _path, row in sorted(rows):
        total = round(total + float(row["reserved_cost_usd"]), 12)
        if row.get("cumulative_reserved_cost_usd") != total:
            raise RuntimeError("W2-26 cumulative cost reservation is inconsistent")
    if total > float(authorization["currency_ceiling_usd"]):
        raise RuntimeError("W2-26 existing reservations exceed the currency ceiling")
    return total


def _validate_triplet_report(
    report: Mapping[str, object],
    *,
    pattern: Mapping[str, object],
    manifest: Mapping[str, object],
    authorization: Mapping[str, object],
    manifest_path: Path | None = None,
    authorization_path: Path | None = None,
) -> None:
    digest = report.get("triplet_report_sha256")
    payload = {
        key: value for key, value in report.items() if key != "triplet_report_sha256"
    }
    rows = report.get("results")
    rows = rows if isinstance(rows, list) else []
    if (
        report.get("schema_version")
        != "chemworld-work-ii-resource-calibration-triplet-0.2"
        or digest != canonical_json_sha256(payload)
        or report.get("rounds") != pattern.get("rounds")
        or report.get("locus") != pattern.get("locus")
        or report.get("task_id") != pattern.get("task_id")
        or report.get("world_seed") != pattern.get("world_seed")
        or report.get("config_file_sha256")
        != pattern["campaign_config_binding"]["sha256"]
        or report.get("manifest_sha256") != canonical_json_sha256(manifest)
        or report.get("development_runtime_commit_observed")
        != authorization.get("development_runtime_commit_observed")
        or report.get("authorization_sha256")
        != authorization.get("authorization_sha256")
        or sorted(
            row.get("arm") for row in rows if isinstance(row, Mapping)
        )
        != sorted(RESOURCE_CALIBRATION_ARMS)
    ):
        raise RuntimeError(
            f"W2-26 {pattern_slug(pattern)} terminal triplet is invalid"
        )
    if manifest_path is not None and authorization_path is not None:
        reservation_bindings = []
        for row in rows:
            binding = row.get("resource_calibration_execution_binding")
            binding = binding if isinstance(binding, Mapping) else {}
            reservation = binding.get("cost_reservation")
            reservation = reservation if isinstance(reservation, Mapping) else {}
            relative = reservation.get("path")
            if not isinstance(relative, str):
                raise RuntimeError("W2-26 terminal cell lacks its cost reservation")
            reservation_path = (ROOT / relative).resolve()
            _validate_cell_execution_binding(
                row,
                arm=str(row.get("arm")),
                pattern=pattern,
                manifest_path=manifest_path,
                authorization_path=authorization_path,
                authorization=authorization,
                reservation_path=reservation_path,
            )
            reservation_bindings.append(
                (reservation.get("attempt_number"), reservation_path.as_posix())
            )
        if len(set(reservation_bindings)) != 1:
            raise RuntimeError("W2-26 terminal triplet mixes attempt reservations")


def _validate_cell_execution_binding(
    row: Mapping[str, object],
    *,
    arm: str,
    pattern: Mapping[str, object],
    manifest_path: Path,
    authorization_path: Path,
    authorization: Mapping[str, object],
    reservation_path: Path,
) -> None:
    binding = row.get("resource_calibration_execution_binding")
    binding = binding if isinstance(binding, Mapping) else {}
    manifest_binding = binding.get("manifest")
    manifest_binding = manifest_binding if isinstance(manifest_binding, Mapping) else {}
    authorization_binding = binding.get("authorization")
    authorization_binding = (
        authorization_binding if isinstance(authorization_binding, Mapping) else {}
    )
    reservation_binding = binding.get("cost_reservation")
    reservation_binding = (
        reservation_binding if isinstance(reservation_binding, Mapping) else {}
    )
    pattern_binding = binding.get("pattern")
    pattern_binding = pattern_binding if isinstance(pattern_binding, Mapping) else {}
    if (
        manifest_binding.get("path") != manifest_path.relative_to(ROOT).as_posix()
        or manifest_binding.get("file_sha256") != file_sha256(manifest_path)
        or authorization_binding.get("path")
        != authorization_path.relative_to(ROOT).as_posix()
        or authorization_binding.get("file_sha256") != file_sha256(authorization_path)
        or authorization_binding.get("authorization_sha256")
        != authorization.get("authorization_sha256")
        or reservation_binding.get("path")
        != reservation_path.relative_to(ROOT).as_posix()
        or reservation_binding.get("file_sha256") != file_sha256(reservation_path)
        or pattern_binding.get("rounds") != pattern.get("rounds")
        or pattern_binding.get("locus") != pattern.get("locus")
        or pattern_binding.get("task_id") != pattern.get("task_id")
        or pattern_binding.get("world_seed") != pattern.get("world_seed")
        or pattern_binding.get("prior_arm") != arm
        or pattern_binding.get("campaign_config_sha256")
        != pattern.get("campaign_config_binding", {}).get("sha256")
        or pattern_binding.get("campaign_config_hash_kind")
        != pattern.get("campaign_config_binding", {}).get("hash_kind")
    ):
        raise RuntimeError("W2-26 child result is detached from its execution authorization")


def _cell_has_platform_defect(row: Mapping[str, object]) -> bool:
    """Compatibility wrapper around the shared W2-26 evidence classifier."""

    return cell_has_platform_defect(row)


def _triplet_attempt_hard_cap(authorization: Mapping[str, object]) -> int:
    """Return the authorization-owned whole-triplet attempt hard cap."""

    runtime = authorization.get("runtime_enforcement")
    runtime = runtime if isinstance(runtime, Mapping) else {}
    hard_cap = runtime.get("per_triplet_infrastructure_attempt_hard_cap")
    if (
        isinstance(hard_cap, bool)
        or not isinstance(hard_cap, int)
        or hard_cap < 1
    ):
        raise RuntimeError("W2-26 authorization lacks a valid triplet-attempt hard cap")
    return hard_cap


def _platform_defect_disposition(
    *,
    provider_attempt_hard_cap: int,
    pattern: Mapping[str, object],
    attempt_number: int,
    reserved_cost_usd: float | None,
) -> dict[str, object]:
    """Apply the authorized whole-triplet infrastructure restart hard cap."""

    automatic_resume = attempt_number < provider_attempt_hard_cap
    return {
        "status": (
            "infrastructure_incomplete_full_triplet_restarting"
            if automatic_resume
            else "infrastructure_incomplete_full_triplet_resume_cap_exhausted"
        ),
        "locus": pattern["locus"],
        "task_id": pattern["task_id"],
        "rounds": pattern["rounds"],
        "attempt_number": attempt_number,
        "provider_attempt_hard_cap": provider_attempt_hard_cap,
        "automatic_full_triplet_resume": automatic_resume,
        "next_attempt_number": attempt_number + 1 if automatic_resume else None,
        "reserved_cost_usd": reserved_cost_usd,
    }


def execute_calibration(
    *,
    manifest_path: Path,
    authorization_path: Path,
    output_root: Path,
    resume: bool,
    cell_runner: Path = CELL_RUNNER,
) -> dict[str, object]:
    """Execute or infrastructure-resume frozen triplets without replacing cells."""

    manifest_path = _inside_root(manifest_path, label="W2-26 manifest")
    authorization_path = _inside_root(
        authorization_path, label="W2-26 execution authorization"
    )
    output_root = _inside_root(output_root, label="W2-26 output root")
    manifest = _load(manifest_path)
    authorization = _load(authorization_path)
    authorization_errors = validate_resource_calibration_authorization(
        ROOT, authorization, manifest_path
    )
    if authorization_errors:
        raise RuntimeError(
            "W2-26 execution authorization failed: " + "; ".join(authorization_errors)
        )
    if output_root.exists() and not resume:
        raise FileExistsError(f"refusing to overwrite W2-26 output: {output_root}")
    if not output_root.exists() and resume:
        raise FileNotFoundError("W2-26 resume requires an existing output root")
    output_root.mkdir(parents=True, exist_ok=resume)
    authorization_copy = output_root / "execution_authorization.json"
    if authorization_copy.exists():
        if _load(authorization_copy) != authorization:
            raise RuntimeError("W2-26 authorization changed across resume")
    else:
        _write_once(authorization_copy, authorization)
    summary_path = output_root / "summary.json"
    if summary_path.is_file():
        summary = _load(summary_path)
        summary_errors = validate_resource_calibration_summary(
            summary,
            manifest=manifest,
        )
        if summary_errors:
            raise RuntimeError(
                "existing W2-26 summary failed: " + "; ".join(summary_errors)
            )
        return {
            "status": summary["status"],
            "summary_sha256": summary["summary_sha256"],
            "idempotent_existing_summary": True,
        }
    progress_path = output_root / "progress.jsonl"
    execution_started = time.monotonic()
    accepted_reports: list[dict[str, object]] = []
    currency_by_cell: dict[str, float] = {}
    unlimited = authorization.get("unlimited_spend_authorized") is True
    hard_cost = (
        None
        if unlimited
        else float(authorization["all_infrastructure_resumes"]["cost_cap_usd"])
    )
    reserved_cost = _load_and_validate_reservations(output_root, authorization)
    pattern_contracts = {
        pattern_key(row): row for row in authorization["pattern_attempt_contracts"]
    }
    provider_attempt_hard_cap = _triplet_attempt_hard_cap(authorization)
    total_triplets = len(manifest["patterns"])
    for triplet_index, pattern in enumerate(manifest["patterns"], start=1):
        rounds = int(pattern["rounds"])
        slug = pattern_slug(pattern)
        terminal_path = output_root / "terminal_triplets" / f"{slug}.json"
        if terminal_path.is_file():
            terminal_report = _load(terminal_path)
            _validate_triplet_report(
                terminal_report,
                pattern=pattern,
                manifest=manifest,
                authorization=authorization,
                manifest_path=manifest_path,
                authorization_path=authorization_copy,
            )
            accepted_reports.append(terminal_report)
            continue
        attempts_root = output_root / "triplet_attempts" / slug
        existing = sorted(attempts_root.glob("attempt-*")) if attempts_root.is_dir() else []
        if len(existing) >= provider_attempt_hard_cap:
            raise RuntimeError(f"W2-26 {slug} triplet exhausted its resume cap")
        attempt_number = len(existing) + 1
        attempt_root = attempts_root / f"attempt-{attempt_number}-{uuid4().hex}"
        attempt_root.mkdir(parents=True, exist_ok=False)
        contract = pattern_contracts[pattern_key(pattern)]
        triplet_reservation = (
            None if unlimited else float(contract["initial_triplet_cost_cap_usd"])
        )
        if (
            not unlimited
            and float(reserved_cost) + float(triplet_reservation) > float(hard_cost)
        ):
            raise RuntimeError("W2-26 currency ceiling would be exceeded before launch")
        if not unlimited:
            reserved_cost = round(
                float(reserved_cost) + float(triplet_reservation), 12
            )
        _write_once(
            attempt_root / "cost_reservation.json",
            {
                "locus": pattern["locus"],
                "task_id": pattern["task_id"],
                "rounds": rounds,
                "attempt_number": attempt_number,
                "reservation_sequence_number": 1
                + (
                    len(
                        list(
                            output_root.glob(
                                "triplet_attempts/*/attempt-*/cost_reservation.json"
                            )
                        )
                    )
                ),
                "authorization_sha256": authorization["authorization_sha256"],
                "reserved_cost_usd": triplet_reservation,
                "cumulative_reserved_cost_usd": reserved_cost,
                "currency_ceiling_usd": authorization["currency_ceiling_usd"],
            },
        )
        processes: list[dict[str, object]] = []
        started = time.monotonic()
        for arm in RESOURCE_CALIBRATION_ARMS:
            cell_root = attempt_root / arm
            child_progress = attempt_root / "progress" / f"{arm}.jsonl"
            log_path = attempt_root / "logs" / f"{arm}.log"
            log_path.parent.mkdir(parents=True, exist_ok=True)
            command = [
                sys.executable,
                str(cell_runner),
                "--config",
                str(ROOT / pattern["campaign_config_binding"]["path"]),
                "--output",
                str(cell_root),
                "--progress-file",
                str(child_progress),
                "--world-seed",
                str(pattern["world_seed"]),
                "--prior-arm",
                arm,
                "--resource-calibration-execution",
                "--resource-calibration-manifest",
                str(manifest_path),
                "--resource-calibration-authorization",
                str(authorization_copy),
                "--resource-calibration-cost-reservation",
                str(attempt_root / "cost_reservation.json"),
            ]
            log_handle = log_path.open("w", encoding="utf-8")
            kwargs: dict[str, object] = {}
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
                _write_once(
                    attempt_root / f"platform-defect-{arm}.json",
                    {
                        "rounds": rounds,
                        "locus": pattern["locus"],
                        "task_id": pattern["task_id"],
                        "arm": arm,
                        "class": "platform_execution_failure",
                        "failure_type": type(error).__name__,
                        "message": str(error)[:1000],
                        "full_triplet_restart_required": True,
                    },
                )
                processes.append(
                    {
                        "arm": arm,
                        "process": None,
                        "log_handle": None,
                        "cell_root": cell_root,
                    }
                )
                continue
            processes.append(
                {
                    "arm": arm,
                    "process": process,
                    "log_handle": log_handle,
                    "cell_root": cell_root,
                }
            )
        next_heartbeat = time.monotonic() + 30.0
        while any(
            item["process"] is not None and item["process"].poll() is None
            for item in processes
        ):
            now = time.monotonic()
            if now >= next_heartbeat:
                _emit(
                    progress_path,
                    {
                        "event": "resource_calibration_triplet_heartbeat",
                        "rounds": rounds,
                        "locus": pattern["locus"],
                        "task_id": pattern["task_id"],
                        "attempt_number": attempt_number,
                        "stage": "provider_task_triplet",
                        "task_triplet_index": triplet_index,
                        "completed_task_triplets": len(accepted_reports),
                        "total_task_triplets": total_triplets,
                        "completed_cells": len(accepted_reports) * len(
                            RESOURCE_CALIBRATION_ARMS
                        ),
                        "total_cells": total_triplets
                        * len(RESOURCE_CALIBRATION_ARMS),
                        "active_provider_processes": sum(
                            item["process"] is not None
                            and item["process"].poll() is None
                            for item in processes
                        ),
                        "elapsed_s": round(now - started, 3),
                        "execution_elapsed_s": round(now - execution_started, 3),
                        "terminal_triplets_per_hour": round(
                            len(accepted_reports)
                            / max(now - execution_started, 1.0)
                            * 3600.0,
                            3,
                        ),
                        "eta_s": (
                            round(
                                (total_triplets - len(accepted_reports))
                                * (now - execution_started)
                                / len(accepted_reports),
                                1,
                            )
                            if accepted_reports
                            else None
                        ),
                    },
                )
                next_heartbeat = now + 30.0
            time.sleep(min(1.0, max(0.05, next_heartbeat - now)))
        rows: list[dict[str, object]] = []
        platform_defect = False
        config = _load(ROOT / pattern["campaign_config_binding"]["path"])
        for item in processes:
            if item["process"] is None:
                platform_defect = True
                continue
            item["process"].wait()
            item["log_handle"].close()
            cell_summary_path = item["cell_root"] / "summary.json"
            if not cell_summary_path.is_file():
                platform_defect = True
                _write_once(
                    attempt_root / f"platform-defect-{item['arm']}.json",
                    {
                        "rounds": rounds,
                        "locus": pattern["locus"],
                        "task_id": pattern["task_id"],
                        "arm": item["arm"],
                        "class": "platform_execution_failure",
                        "failure_type": "missing_cell_summary",
                        "full_triplet_restart_required": True,
                    },
                )
                continue
            row = _load(cell_summary_path)
            _validate_cell_execution_binding(
                row,
                arm=str(item["arm"]),
                pattern=pattern,
                manifest_path=manifest_path,
                authorization_path=authorization_copy,
                authorization=authorization,
                reservation_path=attempt_root / "cost_reservation.json",
            )
            if _cell_has_platform_defect(row):
                platform_defect = True
            row["calibration_campaign_contract"] = {
                "process_time_policy": config["campaign"]["process_time_policy"],
                "closeout_policy": config["campaign"]["closeout_policy"],
            }
            cell_id = (
                f"{pattern['locus']}:{pattern['task_id']}:{rounds}:"
                f"{pattern['world_seed']}:{item['arm']}"
            )
            observed_currency = _observed_currency(row, authorization)
            if observed_currency is not None:
                currency_by_cell[cell_id] = observed_currency
            rows.append(row)
        triplet_report: dict[str, object] = {
            "schema_version": "chemworld-work-ii-resource-calibration-triplet-0.2",
            "rounds": rounds,
            "locus": pattern["locus"],
            "task_id": pattern["task_id"],
            "config_file_sha256": pattern["campaign_config_binding"]["sha256"],
            "world_seed": pattern["world_seed"],
            "manifest_sha256": canonical_json_sha256(manifest),
            "development_runtime_commit_observed": authorization[
                "development_runtime_commit_observed"
            ],
            "authorization_sha256": authorization["authorization_sha256"],
            "calibration_campaign_contract": {
                "process_time_policy": config["campaign"]["process_time_policy"],
                "closeout_policy": config["campaign"]["closeout_policy"],
            },
            "results": rows,
        }
        triplet_report["triplet_report_sha256"] = canonical_json_sha256(
            triplet_report
        )
        _write_once(attempt_root / "triplet_report.json", triplet_report)
        if platform_defect:
            disposition = _platform_defect_disposition(
                provider_attempt_hard_cap=provider_attempt_hard_cap,
                pattern=pattern,
                attempt_number=attempt_number,
                reserved_cost_usd=reserved_cost,
            )
            _emit(
                progress_path,
                {
                    "event": "resource_calibration_triplet_invalidated",
                    "rounds": rounds,
                    "locus": pattern["locus"],
                    "task_id": pattern["task_id"],
                    "attempt_number": attempt_number,
                    "resume_requires_full_triplet_restart": True,
                },
            )
            if disposition["automatic_full_triplet_resume"] is True:
                _emit(
                    progress_path,
                    {
                        "event": "resource_calibration_triplet_restarting",
                        "rounds": rounds,
                        "locus": pattern["locus"],
                        "task_id": pattern["task_id"],
                        "invalidated_attempt_number": attempt_number,
                        "next_attempt_number": disposition["next_attempt_number"],
                        "provider_attempt_hard_cap": disposition[
                            "provider_attempt_hard_cap"
                        ],
                        "full_triplet_restart_from_first_arm": True,
                        "prior_attempt_results_reused": False,
                    },
                )
                return execute_calibration(
                    manifest_path=manifest_path,
                    authorization_path=authorization_path,
                    output_root=output_root,
                    resume=True,
                    cell_runner=cell_runner,
                )
            return disposition
        _write_once(terminal_path, triplet_report)
        accepted_reports.append(triplet_report)
        now = time.monotonic()
        _emit(
            progress_path,
            {
                "event": "resource_calibration_triplet_completed",
                "stage": "provider_task_triplet",
                "locus": pattern["locus"],
                "task_id": pattern["task_id"],
                "rounds": rounds,
                "task_triplet_index": triplet_index,
                "completed_task_triplets": len(accepted_reports),
                "total_task_triplets": total_triplets,
                "completed_cells": len(accepted_reports)
                * len(RESOURCE_CALIBRATION_ARMS),
                "total_cells": total_triplets * len(RESOURCE_CALIBRATION_ARMS),
                "execution_elapsed_s": round(now - execution_started, 3),
                "terminal_triplets_per_hour": round(
                    len(accepted_reports)
                    / max(now - execution_started, 1.0)
                    * 3600.0,
                    3,
                ),
                "eta_s": round(
                    (total_triplets - len(accepted_reports))
                    * (now - execution_started)
                    / len(accepted_reports),
                    1,
                ),
            },
        )
    for pattern in manifest["patterns"]:
        reports = [
            report
            for report in accepted_reports
            if pattern_key(report) == pattern_key(pattern)
        ]
        if len(reports) != 1:
            continue
        for row in reports[0].get("results", []):
            if not isinstance(row, Mapping):
                continue
            cell_id = (
                f"{pattern['locus']}:{pattern['task_id']}:{pattern['rounds']}:"
                f"{pattern['world_seed']}:{row.get('arm')}"
            )
            observed_currency = _observed_currency(row, authorization)
            if observed_currency is not None:
                currency_by_cell[cell_id] = observed_currency
    summary = build_resource_calibration_summary(
        manifest,
        accepted_reports,
        source_commit=str(authorization["development_runtime_commit_observed"]),
        observed_currency_usd_by_cell=currency_by_cell,
    )
    summary_errors = validate_resource_calibration_summary(
        summary,
        manifest=manifest,
    )
    if summary_errors:
        raise RuntimeError("W2-26 summary failed: " + "; ".join(summary_errors))
    _write_once(summary_path, summary)
    return {
        "status": summary["status"],
        "summary_sha256": summary["summary_sha256"],
        "reserved_cost_usd": reserved_cost,
    }


def main() -> int:
    args = _parse_args()
    manifest_path = args.manifest.resolve()
    if args.build_execution_manifest:
        if args.output is None:
            raise RuntimeError("--output is required for --build-execution-manifest")
        output = _inside_root(args.output, label="W2-26 execution manifest")
        dynamic_root = (ROOT / "workstreams/flagship_tasks/reports").resolve()
        if not output.is_relative_to(dynamic_root):
            raise RuntimeError("W2-26 execution manifest must use the dynamic evidence root")
        protocol = _load(manifest_path)
        if args.provider_cohort == "deepseek-v4-flash":
            protocol["calibration_id"] = (
                "work-ii-w2-26-deepseek-v4-flash-full-task-resource-calibration-v0.1"
            )
            protocol["experiment_note"] = (
                "workstreams/flagship_tasks/"
                "WORK_II_RESOURCE_CALIBRATION_DEEPSEEK_V01_EXPERIMENT_NOTE.md"
            )
            protocol["provider_contract"] = dict(DEEPSEEK_PROVIDER_CONTRACT)
            payload = build_resource_calibration_execution_manifest(
                ROOT,
                protocol,
                runtime_config_root=DEEPSEEK_RUNTIME_CONFIG_ROOT,
                provider_override=DEEPSEEK_PROVIDER_RUNTIME,
                planning_resource_overrides=DEEPSEEK_PLANNING_RESOURCE_LIMITS,
            )
        else:
            payload = build_resource_calibration_execution_manifest(ROOT, protocol)
        _write_once(output, payload)
        print(
            json.dumps(
                {
                    "status": payload["status"],
                    "output": str(output),
                },
                ensure_ascii=False,
                sort_keys=True,
            ),
            flush=True,
        )
        return 0
    manifest = _load(manifest_path)

    if args.authorize:
        if args.output is None:
            raise RuntimeError("--output is required for --authorize")
        required = {
            "--approved-at": args.approved_at,
        }
        if not args.unlimited_spend_authorized:
            required.update(
                {
                    "--currency-ceiling-usd": args.currency_ceiling_usd,
                    "--pricing-source": args.pricing_source,
                    "--pricing-observed-at": args.pricing_observed_at,
                    "--cache-hit-input-usd-per-million": (
                        args.cache_hit_input_usd_per_million
                    ),
                    "--cache-miss-input-usd-per-million": (
                        args.cache_miss_input_usd_per_million
                    ),
                    "--output-usd-per-million": args.output_usd_per_million,
                }
            )
        missing = [flag for flag, value in required.items() if value is None]
        if not args.provider_contract_confirmed_by_user:
            missing.append("--provider-contract-confirmed-by-user")
        if not args.credential_rotation_confirmed_by_user:
            missing.append("--credential-rotation-confirmed-by-user")
        if missing:
            raise RuntimeError(
                "refusing W2-26 authorization without explicit user inputs: "
                + ", ".join(missing)
            )
        authorization = build_resource_calibration_authorization(
            ROOT,
            manifest_path,
            currency_ceiling_usd=(
                None
                if args.unlimited_spend_authorized
                else float(args.currency_ceiling_usd)
            ),
            approved_at=str(args.approved_at),
            pricing_source=(
                "provider_contract_has_no_attributable_per_run_usd_price"
                if args.unlimited_spend_authorized
                else str(args.pricing_source)
            ),
            pricing_observed_at=(
                str(args.approved_at)
                if args.unlimited_spend_authorized
                else str(args.pricing_observed_at)
            ),
            cache_hit_input_usd_per_million=(
                None
                if args.unlimited_spend_authorized
                else float(args.cache_hit_input_usd_per_million)
            ),
            cache_miss_input_usd_per_million=(
                None
                if args.unlimited_spend_authorized
                else float(args.cache_miss_input_usd_per_million)
            ),
            output_usd_per_million=(
                None
                if args.unlimited_spend_authorized
                else float(args.output_usd_per_million)
            ),
            unlimited_spend_authorized=bool(args.unlimited_spend_authorized),
        )
        authorization_errors = validate_resource_calibration_authorization(
            ROOT, authorization, manifest_path
        )
        if authorization_errors:
            raise RuntimeError(
                "W2-26 authorization failed: " + "; ".join(authorization_errors)
            )
        _write_once(_inside_root(args.output, label="W2-26 authorization"), authorization)
        print(
            json.dumps(
                {
                    "status": authorization["status"],
                    "authorization_sha256": authorization["authorization_sha256"],
                    "output": str(args.output.resolve()),
                },
                ensure_ascii=False,
                sort_keys=True,
            ),
            flush=True,
        )
        return 0

    if args.execute:
        if args.authorization is None or not args.allow_provider_execution:
            raise RuntimeError(
                "W2-26 execution requires a validated write-once authorization and "
                "--allow-provider-execution"
            )
        if args.output is None:
            raise RuntimeError("--output is required for --execute")
        progress = execute_calibration(
            manifest_path=manifest_path,
            authorization_path=args.authorization,
            output_root=args.output,
            resume=bool(args.resume),
        )
        print(json.dumps(progress, ensure_ascii=False, sort_keys=True), flush=True)
        return 0 if progress["status"] in {"passed", "failed"} else 1

    if (
        args.authorization is not None
        or args.allow_provider_execution
        or args.resume
        or any(
            value is not None
            for value in (
                args.currency_ceiling_usd,
                args.approved_at,
                args.pricing_source,
                args.pricing_observed_at,
                args.cache_hit_input_usd_per_million,
                args.cache_miss_input_usd_per_million,
                args.output_usd_per_million,
            )
        )
        or args.provider_contract_confirmed_by_user
        or args.credential_rotation_confirmed_by_user
        or args.unlimited_spend_authorized
    ):
        raise RuntimeError("provider authorization options require --authorize or --execute")
    if args.output is None:
        raise RuntimeError("--output is required for non-execution modes")
    output = args.output.resolve()
    manifest_errors = validate_resource_calibration_manifest(
        ROOT, manifest, allow_pending=True
    )
    if manifest_errors:
        raise RuntimeError(
            "resource calibration manifest failed: " + "; ".join(manifest_errors)
        )
    summary = empty_resource_calibration_summary(manifest)
    summary_errors = validate_resource_calibration_summary(summary, manifest=manifest)
    if summary_errors:
        raise RuntimeError(
            "resource calibration summary template failed: "
            + "; ".join(summary_errors)
        )
    _write_once(output, summary)
    print(
        json.dumps(
            {
                "status": summary["status"],
                "provider_calls_executed": summary["provider_calls_executed"],
                "output": str(output),
            },
            ensure_ascii=False,
            sort_keys=True,
        ),
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
