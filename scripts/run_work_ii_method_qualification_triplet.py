#!/usr/bin/env python3
"""Execute the Work II qualification triplet with cost-reserved missing-only resume."""

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

from chemworld.eval.provenance import (
    canonical_json_sha256,
    file_sha256,
    write_json_atomic,
)
from chemworld.eval.work_ii_cost import (
    build_qualification_cost_ledger,
    validate_qualification_cost_contract,
    validate_qualification_cost_ledger,
)
from chemworld.eval.work_ii_formal import (
    FORMAL_ARMS,
    build_formal_preflight,
    validate_formal_bindings,
)
from chemworld.eval.work_ii_qualification import (
    METHOD_QUALIFICATION_REPORT_VERSION,
    build_qualification_attempt_authorization,
    method_qualification_report_sha256,
    validate_method_qualification_report,
    validate_qualification_attempt_authorization,
    validate_qualification_execution_authorization,
)

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "configs/benchmark/work_ii_formal_design_v0.1.json"
ANALYSIS = ROOT / "configs/benchmark/work_ii_analysis_plan_v0.1.json"
CELL_RUNNER = ROOT / "scripts/run_work_ii_campaign_pilot.py"
TRIPLET_PROGRESS_VERSION = "chemworld-work-ii-qualification-triplet-progress-0.1"
TERMINAL_RECEIPT_VERSION = "chemworld-work-ii-qualification-terminal-receipt-0.1"
INFRASTRUCTURE_RECEIPT_VERSION = (
    "chemworld-work-ii-qualification-infrastructure-receipt-0.1"
)


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object")
    return value


def _inside_root(path: Path, *, label: str) -> Path:
    resolved = path.resolve()
    try:
        resolved.relative_to(ROOT.resolve())
    except ValueError as error:
        raise RuntimeError(f"{label} must be inside the repository") from error
    return resolved


def _emit(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rendered = json.dumps(dict(payload), ensure_ascii=False, sort_keys=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(rendered + "\n")
    print(rendered, flush=True)


def _write_once(path: Path, payload: Mapping[str, Any]) -> None:
    if path.exists():
        raise RuntimeError(f"refusing to replace immutable qualification artifact: {path}")
    write_json_atomic(path, dict(payload))


def _self_hash(payload: Mapping[str, Any], field: str) -> str:
    return canonical_json_sha256(
        {key: value for key, value in payload.items() if key != field}
    )


def _attempt_authorizations(output_root: Path, arm: str) -> list[Path]:
    directory = output_root / "attempt_authorizations" / arm
    return sorted(directory.glob("*.json")) if directory.is_dir() else []


def _audit_attempt_journal(
    output_root: Path,
    *,
    manifest: Mapping[str, Any],
    cost_contract: Mapping[str, Any],
    authorization: Mapping[str, Any],
) -> tuple[dict[str, int], dict[tuple[str, str], dict[str, Any]]]:
    counts = dict.fromkeys(FORMAL_ARMS, 0)
    attempts: dict[tuple[str, str], dict[str, Any]] = {}
    provider_attempt_ordinals: list[int] = []
    expected_ledger_paths: set[Path] = set()
    expected_authorization_paths: set[Path] = set()
    for arm in FORMAL_ARMS:
        observed_numbers: list[int] = []
        for path in _attempt_authorizations(output_root, arm):
            attempt = _load(path)
            errors = validate_qualification_attempt_authorization(
                attempt, authorization
            )
            if errors:
                raise RuntimeError(
                    f"qualification attempt authorization is invalid ({path}): "
                    + "; ".join(errors)
                )
            attempt_id = str(attempt["attempt_id"])
            attempt_number = int(attempt["attempt_number"])
            if (
                attempt.get("arm") != arm
                or path.name != f"{attempt_number}-{attempt_id}.json"
            ):
                raise RuntimeError(
                    f"qualification attempt authorization path is inconsistent: {path}"
                )
            observed_numbers.append(attempt_number)
            key = (arm, attempt_id)
            if key in attempts:
                raise RuntimeError(f"duplicate qualification attempt id: {arm}/{attempt_id}")
            ledger_path = (
                output_root
                / "cost_ledgers"
                / arm
                / f"{attempt_number}-{attempt_id}.json"
            )
            ledger = _load(ledger_path)
            ledger_errors = validate_qualification_cost_ledger(
                manifest, cost_contract, ledger
            )
            if ledger_errors:
                raise RuntimeError(
                    f"qualification cost ledger snapshot is invalid ({ledger_path}): "
                    + "; ".join(ledger_errors)
                )
            if attempt.get("qualification_cost_ledger_sha256") != ledger.get(
                "qualification_cost_ledger_sha256"
            ):
                raise RuntimeError(
                    f"qualification attempt does not bind its cost ledger: {path}"
                )
            ledger_counts = ledger.get("provider_attempt_counts_by_arm")
            if (
                not isinstance(ledger_counts, Mapping)
                or ledger_counts.get(arm) != attempt_number
            ):
                raise RuntimeError(
                    f"qualification attempt number differs from its ledger: {path}"
                )
            provider_attempt_ordinals.append(int(ledger["provider_attempt_count"]))
            expected_ledger_paths.add(ledger_path.resolve())
            expected_authorization_paths.add(path.resolve())
            attempts[key] = {
                "authorization": attempt,
                "authorization_path": path.resolve(),
                "ledger": ledger,
                "ledger_path": ledger_path.resolve(),
            }
        if sorted(observed_numbers) != list(range(1, len(observed_numbers) + 1)):
            raise RuntimeError(
                f"qualification attempt numbering is not contiguous for arm: {arm}"
            )
        counts[arm] = len(observed_numbers)

    ledger_root = output_root / "cost_ledgers"
    observed_ledger_paths = (
        {path.resolve() for path in ledger_root.glob("*/*.json")}
        if ledger_root.is_dir()
        else set()
    )
    if observed_ledger_paths != expected_ledger_paths:
        raise RuntimeError("qualification cost-ledger journal has orphaned or missing snapshots")
    authorization_root = output_root / "attempt_authorizations"
    observed_authorization_paths = (
        {path.resolve() for path in authorization_root.glob("*/*.json")}
        if authorization_root.is_dir()
        else set()
    )
    if observed_authorization_paths != expected_authorization_paths:
        raise RuntimeError("qualification attempt journal contains an unknown authorization")
    total = sum(counts.values())
    if sorted(provider_attempt_ordinals) != list(range(1, total + 1)):
        raise RuntimeError("qualification provider-attempt journal is not contiguous")
    current_ledger_path = output_root / "qualification_cost_ledger.json"
    if current_ledger_path.is_file():
        current_ledger = _load(current_ledger_path)
        ledger_errors = validate_qualification_cost_ledger(
            manifest, cost_contract, current_ledger
        )
        if ledger_errors:
            raise RuntimeError(
                "qualification current cost ledger is invalid: "
                + "; ".join(ledger_errors)
            )
        rebuilt = build_qualification_cost_ledger(manifest, cost_contract, counts)
        if current_ledger != rebuilt:
            raise RuntimeError("qualification current cost ledger differs from its journal")
    elif total:
        raise RuntimeError("qualification attempt journal lacks its current cost ledger")
    return counts, attempts


def _terminal_path(output_root: Path, arm: str) -> Path:
    return output_root / "terminal_receipts" / f"{arm}.json"


def _bound_output_path(
    output_root: Path, binding: Mapping[str, Any], *, label: str
) -> Path:
    relative = binding.get("path")
    if not isinstance(relative, str) or not relative:
        raise RuntimeError(f"{label} path is missing")
    path = (output_root / relative).resolve()
    try:
        path.relative_to(output_root.resolve())
    except ValueError as error:
        raise RuntimeError(f"{label} escapes the qualification output") from error
    return path


def _audit_terminal_receipts(
    output_root: Path,
    *,
    authorization: Mapping[str, Any],
    attempts: Mapping[tuple[str, str], Mapping[str, Any]],
    attempt_counts: Mapping[str, int],
) -> set[str]:
    terminal_root = output_root / "terminal_receipts"
    observed_paths = (
        set(terminal_root.glob("*.json")) if terminal_root.is_dir() else set()
    )
    expected_paths = {
        _terminal_path(output_root, arm)
        for arm in FORMAL_ARMS
        if _terminal_path(output_root, arm).is_file()
    }
    if observed_paths != expected_paths:
        raise RuntimeError("qualification terminal journal contains an unknown receipt")
    terminal_arms: set[str] = set()
    for arm in FORMAL_ARMS:
        terminal_path = _terminal_path(output_root, arm)
        if not terminal_path.is_file():
            continue
        terminal = _load(terminal_path)
        if (
            terminal.get("schema_version") != TERMINAL_RECEIPT_VERSION
            or terminal.get("terminal_receipt_sha256")
            != _self_hash(terminal, "terminal_receipt_sha256")
            or terminal.get("arm") != arm
            or terminal.get("state") not in {"completed", "right_censored"}
        ):
            raise RuntimeError(f"qualification terminal receipt is invalid: {arm}")
        allowed_reasons = {
            "completed": {"method_qualification_cell_completed"},
            "right_censored": {
                "method_qualification_cell_right_censored",
                "method_right_censored_unfinalized_child_after_trajectory_evidence",
            },
        }
        if terminal.get("reason_code") not in allowed_reasons[str(terminal["state"])]:
            raise RuntimeError(
                f"qualification terminal receipt has an invalid reason: {arm}"
            )
        attempt_id = str(terminal.get("attempt_id", ""))
        attempt_record = attempts.get((arm, attempt_id))
        if attempt_record is None:
            raise RuntimeError(
                f"qualification terminal receipt lacks an authorized attempt: {arm}"
            )
        attempt = attempt_record["authorization"]
        if attempt.get("attempt_number") != attempt_counts.get(arm):
            raise RuntimeError(
                f"qualification terminal receipt does not bind the latest attempt: {arm}"
            )
        attempt_binding = terminal.get("attempt_authorization_binding")
        if not isinstance(attempt_binding, Mapping):
            raise RuntimeError(
                f"qualification terminal receipt lacks its attempt binding: {arm}"
            )
        attempt_path = _bound_output_path(
            output_root, attempt_binding, label="qualification terminal attempt"
        )
        if (
            attempt_path != attempt_record["authorization_path"]
            or attempt_binding.get("sha256") != file_sha256(attempt_path)
            or attempt_binding.get("attempt_authorization_sha256")
            != attempt.get("attempt_authorization_sha256")
        ):
            raise RuntimeError(
                f"qualification terminal attempt binding is stale: {arm}"
            )
        attempt_errors = validate_qualification_attempt_authorization(
            attempt, authorization
        )
        if attempt_errors:
            raise RuntimeError(
                f"qualification terminal attempt is invalid ({arm}): "
                + "; ".join(attempt_errors)
            )
        row_binding = terminal.get("row_binding")
        if not isinstance(row_binding, Mapping):
            raise RuntimeError(f"qualification terminal row binding is missing: {arm}")
        row_path = _bound_output_path(
            output_root, row_binding, label="qualification terminal row"
        )
        if not row_path.is_file() or row_binding.get("sha256") != file_sha256(row_path):
            raise RuntimeError(f"qualification terminal row binding is stale: {arm}")
        row = _load(row_path)
        child_binding = row.get("qualification_attempt_authorization_binding")
        expected_child_binding = {
            "path": attempt_record["authorization_path"]
            .relative_to(ROOT.resolve())
            .as_posix(),
            "sha256": file_sha256(attempt_record["authorization_path"]),
            "attempt_authorization_sha256": attempt.get(
                "attempt_authorization_sha256"
            ),
            "qualification_cost_ledger_path": attempt_record["ledger_path"]
            .relative_to(ROOT.resolve())
            .as_posix(),
            "qualification_cost_ledger_sha256": attempt_record["ledger"].get(
                "qualification_cost_ledger_sha256"
            ),
        }
        if (
            row.get("arm") != arm
            or child_binding != expected_child_binding
            or (terminal.get("state") == "completed") != (row.get("completed") is True)
        ):
            raise RuntimeError(
                f"qualification terminal row differs from its authorized process: {arm}"
            )
        terminal_arms.add(arm)
    return terminal_arms


def _row_binding(output_root: Path, row_path: Path) -> dict[str, Any]:
    return {
        "path": row_path.resolve().relative_to(output_root).as_posix(),
        "sha256": file_sha256(row_path),
    }


def _write_terminal(
    output_root: Path,
    *,
    arm: str,
    state: str,
    reason_code: str,
    attempt_id: str,
    row_path: Path,
    attempt_authorization_path: Path,
) -> None:
    receipt: dict[str, Any] = {
        "schema_version": TERMINAL_RECEIPT_VERSION,
        "arm": arm,
        "state": state,
        "reason_code": reason_code,
        "attempt_id": attempt_id,
        "row_binding": _row_binding(output_root, row_path),
        "attempt_authorization_binding": {
            "path": attempt_authorization_path.resolve()
            .relative_to(output_root)
            .as_posix(),
            "sha256": file_sha256(attempt_authorization_path),
            "attempt_authorization_sha256": _load(attempt_authorization_path).get(
                "attempt_authorization_sha256"
            ),
        },
    }
    receipt["terminal_receipt_sha256"] = _self_hash(
        receipt, "terminal_receipt_sha256"
    )
    _write_once(_terminal_path(output_root, arm), receipt)


def _write_infrastructure_failure(
    output_root: Path,
    *,
    arm: str,
    attempt_id: str,
    error: BaseException,
    log_path: Path,
) -> None:
    receipt: dict[str, Any] = {
        "schema_version": INFRASTRUCTURE_RECEIPT_VERSION,
        "arm": arm,
        "attempt_id": attempt_id,
        "error_type": type(error).__name__,
        "error_message": str(error)[:1000],
        "log_path": log_path.resolve().relative_to(output_root).as_posix(),
        "log_sha256": file_sha256(log_path),
    }
    receipt["infrastructure_receipt_sha256"] = _self_hash(
        receipt, "infrastructure_receipt_sha256"
    )
    path = output_root / "infrastructure_failures" / arm / f"{attempt_id}.json"
    _write_once(path, receipt)


def _unfinalized_trajectory(path: Path) -> dict[str, Any] | None:
    if not path.is_file() or path.stat().st_size <= 0:
        return None
    nonempty = 0
    valid = 0
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.strip():
            continue
        nonempty += 1
        try:
            json.loads(line)
        except json.JSONDecodeError:
            continue
        valid += 1
    return {
        "trajectory_byte_count": path.stat().st_size,
        "nonempty_line_count": nonempty,
        "valid_json_line_count": valid,
        "malformed_or_partial_line_count": nonempty - valid,
    }


def _terminalize_process(
    output_root: Path,
    state: Mapping[str, Any],
) -> bool:
    arm = str(state["arm"])
    attempt_root = Path(state["attempt_root"])
    summary_path = attempt_root / "summary.json"
    try:
        row = _load(summary_path)
        if row.get("arm") != arm:
            raise ValueError("qualification child summary has the wrong arm")
        attempt_binding = row.get("qualification_attempt_authorization_binding")
        if not isinstance(attempt_binding, Mapping) or attempt_binding.get(
            "attempt_authorization_sha256"
        ) != _load(Path(state["attempt_authorization_path"])).get(
            "attempt_authorization_sha256"
        ):
            raise ValueError("qualification child lacks its exact attempt binding")
        if row.get("completed") is True:
            terminal_state = "completed"
            reason = "method_qualification_cell_completed"
        elif _unfinalized_trajectory(attempt_root / "trajectory.jsonl") is not None:
            terminal_state = "right_censored"
            reason = "method_qualification_cell_right_censored"
        else:
            failure = row.get("failure")
            failure = failure if isinstance(failure, Mapping) else {}
            error = RuntimeError(
                "qualification child failed before producing trajectory evidence: "
                + str(failure.get("type", "unknown"))
            )
            _write_infrastructure_failure(
                output_root,
                arm=arm,
                attempt_id=str(state["attempt_id"]),
                error=error,
                log_path=Path(state["log_path"]),
            )
            return False
        _write_terminal(
            output_root,
            arm=arm,
            state=terminal_state,
            reason_code=reason,
            attempt_id=str(state["attempt_id"]),
            row_path=summary_path,
            attempt_authorization_path=Path(state["attempt_authorization_path"]),
        )
        return True
    except (OSError, ValueError, json.JSONDecodeError) as error:
        evidence = _unfinalized_trajectory(attempt_root / "trajectory.jsonl")
        if evidence is None:
            _write_infrastructure_failure(
                output_root,
                arm=arm,
                attempt_id=str(state["attempt_id"]),
                error=error,
                log_path=Path(state["log_path"]),
            )
            return False
        recovered_row = {
            "arm": arm,
            "completed": False,
            "failure": {
                "type": type(error).__name__,
                "message": "unfinalized child retained without scientific replacement",
            },
            "analysis": {"unfinalized_trajectory_evidence": evidence},
            "method_resources": {},
            "provider_receipts": [],
            "exact_replay": {"verified": False, "mismatches": []},
            "qualification": {
                "passed": False,
                "checks": {},
                "failed_checks": ["unfinalized_child"],
            },
            "qualification_attempt_authorization_binding": {
                "path": Path(state["attempt_authorization_path"])
                .resolve()
                .relative_to(ROOT.resolve())
                .as_posix(),
                "sha256": file_sha256(Path(state["attempt_authorization_path"])),
                "attempt_authorization_sha256": _load(
                    Path(state["attempt_authorization_path"])
                ).get("attempt_authorization_sha256"),
                "qualification_cost_ledger_path": Path(state["ledger_snapshot_path"])
                .resolve()
                .relative_to(ROOT.resolve())
                .as_posix(),
                "qualification_cost_ledger_sha256": _load(
                    Path(state["ledger_snapshot_path"])
                ).get("qualification_cost_ledger_sha256"),
            },
        }
        recovered_path = attempt_root / "recovered_terminal_row.json"
        _write_once(recovered_path, recovered_row)
        _write_terminal(
            output_root,
            arm=arm,
            state="right_censored",
            reason_code="method_right_censored_unfinalized_child_after_trajectory_evidence",
            attempt_id=str(state["attempt_id"]),
            row_path=recovered_path,
            attempt_authorization_path=Path(state["attempt_authorization_path"]),
        )
        return True


def _build_report(
    output_root: Path,
    *,
    authorization_copy: Path,
    config_path: Path,
    world_seed: int,
    elapsed_s: float,
    manifest: Mapping[str, Any],
) -> tuple[dict[str, Any], list[str]]:
    rows: list[dict[str, Any]] = []
    terminal_states: dict[str, str] = {}
    for arm in FORMAL_ARMS:
        terminal = _load(_terminal_path(output_root, arm))
        row_path = output_root / str(terminal["row_binding"]["path"])
        if file_sha256(row_path) != terminal["row_binding"]["sha256"]:
            raise RuntimeError(f"qualification terminal row binding is stale: {arm}")
        rows.append(_load(row_path))
        terminal_states[arm] = str(terminal["state"])
    config = _load(config_path)
    authorization = _load(authorization_copy)
    report: dict[str, Any] = {
        "schema_version": METHOD_QUALIFICATION_REPORT_VERSION,
        "pilot_id": config["pilot_id"],
        "cell_id": f"{config['pilot_id']}--seed{world_seed}",
        "formal_cell_key_sha256": None,
        "formal_result": False,
        "qualification_execution_authorized": True,
        "qualification_execution_authorization_binding": {
            "path": authorization_copy.relative_to(ROOT).as_posix(),
            "sha256": file_sha256(authorization_copy),
            "authorization_sha256": authorization["authorization_sha256"],
        },
        "config_sha256": canonical_json_sha256(config),
        "config_file_sha256": file_sha256(config_path),
        "world_seed": world_seed,
        "cell_count": len(rows),
        "completed_cell_count": sum(row.get("completed") is True for row in rows),
        "elapsed_s": round(elapsed_s, 3),
        "terminal_states_by_arm": terminal_states,
        "results": rows,
    }
    report["report_sha256"] = method_qualification_report_sha256(report)
    return report, validate_method_qualification_report(ROOT, report, manifest)


def _validate_report_terminal_bindings(
    output_root: Path, report: Mapping[str, Any]
) -> list[str]:
    rows: list[dict[str, Any]] = []
    states: dict[str, str] = {}
    for arm in FORMAL_ARMS:
        terminal = _load(_terminal_path(output_root, arm))
        row_binding = terminal.get("row_binding")
        if not isinstance(row_binding, Mapping):
            return [f"{arm}: qualification report terminal row binding is missing"]
        row_path = _bound_output_path(
            output_root, row_binding, label="qualification report terminal row"
        )
        rows.append(_load(row_path))
        states[arm] = str(terminal.get("state"))
    errors: list[str] = []
    if report.get("results") != rows:
        errors.append("qualification report results differ from terminal receipts")
    if report.get("terminal_states_by_arm") != states:
        errors.append("qualification report states differ from terminal receipts")
    return errors


def execute_triplet(
    *,
    authorization_path: Path,
    output_root: Path,
    progress_path: Path,
    resume: bool,
    cell_runner: Path = CELL_RUNNER,
) -> dict[str, Any]:
    """Run or missing-only resume the exact qualification arm triplet."""

    manifest = build_formal_preflight(ROOT, DESIGN, ANALYSIS)
    binding_errors = validate_formal_bindings(ROOT, manifest)
    if binding_errors:
        raise RuntimeError("formal binding validation failed: " + "; ".join(binding_errors))
    authorization_path = _inside_root(
        authorization_path, label="qualification execution authorization"
    )
    authorization = _load(authorization_path)
    authorization_errors = validate_qualification_execution_authorization(
        ROOT, authorization, manifest
    )
    if authorization_errors:
        raise RuntimeError(
            "qualification execution authorization failed: "
            + "; ".join(authorization_errors)
        )
    output_root = _inside_root(output_root, label="qualification output root")
    progress_path = _inside_root(progress_path, label="qualification progress path")
    if output_root.exists() and not resume:
        raise FileExistsError(f"refusing to overwrite qualification output: {output_root}")
    if not output_root.exists() and resume:
        raise FileNotFoundError("qualification resume requires an existing output root")
    output_root.mkdir(parents=True, exist_ok=resume)
    authorization_copy = output_root / "execution_authorization.json"
    if authorization_copy.exists():
        if _load(authorization_copy) != authorization:
            raise RuntimeError("qualification execution authorization changed across resume")
    else:
        write_json_atomic(authorization_copy, authorization)
    cost_contract = authorization.get("qualification_currency_budget")
    if not isinstance(cost_contract, Mapping):
        raise RuntimeError("qualification authorization lacks its cost contract")
    cost_errors = validate_qualification_cost_contract(ROOT, manifest, cost_contract)
    if cost_errors:
        raise RuntimeError("qualification cost contract failed: " + "; ".join(cost_errors))
    cost_contract_path = output_root / "qualification_cost_contract.json"
    if cost_contract_path.exists():
        if _load(cost_contract_path) != dict(cost_contract):
            raise RuntimeError("qualification cost contract changed across resume")
    else:
        write_json_atomic(cost_contract_path, dict(cost_contract))
    schedule = authorization["qualification_schedule"]
    config_path = (ROOT / str(schedule["campaign_config_path"])).resolve()
    world_seed = int(schedule["world_seed"])
    attempt_counts, attempts = _audit_attempt_journal(
        output_root,
        manifest=manifest,
        cost_contract=cost_contract,
        authorization=authorization,
    )
    terminal_arms = _audit_terminal_receipts(
        output_root,
        authorization=authorization,
        attempts=attempts,
        attempt_counts=attempt_counts,
    )
    pending = [arm for arm in FORMAL_ARMS if arm not in terminal_arms]
    started = time.monotonic()
    processes: list[dict[str, Any]] = []
    infrastructure_failures = 0
    ledger_path = output_root / "qualification_cost_ledger.json"
    _emit(
        progress_path,
        {
            "event": "qualification_triplet_resumed" if resume else "qualification_triplet_started",
            "pending_arms": pending,
            "terminal_arms_before_start": len(FORMAL_ARMS) - len(pending),
        },
    )
    for arm in pending:
        counts = dict(attempt_counts)
        counts[arm] += 1
        proposed_ledger = build_qualification_cost_ledger(
            manifest, cost_contract, counts
        )
        if proposed_ledger["within_ceiling"] is not True:
            raise RuntimeError(
                "qualification currency ceiling would be exceeded before provider launch"
        )
        attempt_id = uuid4().hex
        attempt_number = counts[arm]
        write_json_atomic(ledger_path, proposed_ledger)
        ledger_snapshot_path = (
            output_root / "cost_ledgers" / arm / f"{attempt_number}-{attempt_id}.json"
        )
        _write_once(ledger_snapshot_path, proposed_ledger)
        attempt_authorization = build_qualification_attempt_authorization(
            authorization,
            arm=arm,
            attempt_number=attempt_number,
            attempt_id=attempt_id,
            qualification_cost_ledger_sha256=str(
                proposed_ledger["qualification_cost_ledger_sha256"]
            ),
        )
        attempt_authorization_path = (
            output_root / "attempt_authorizations" / arm / f"{attempt_number}-{attempt_id}.json"
        )
        _write_once(attempt_authorization_path, attempt_authorization)
        attempt_counts[arm] = attempt_number
        attempt_root = output_root / "attempts" / arm / attempt_id
        log_path = output_root / "logs" / arm / f"{attempt_id}.log"
        log_path.parent.mkdir(parents=True, exist_ok=True)
        child_progress = output_root / "progress" / arm / f"{attempt_id}.jsonl"
        command = [
            sys.executable,
            str(cell_runner),
            "--config",
            str(config_path),
            "--output",
            str(attempt_root),
            "--progress-file",
            str(child_progress),
            "--world-seed",
            str(world_seed),
            "--prior-arm",
            arm,
            "--qualification-execution",
            "--qualification-authorization",
            str(authorization_copy),
            "--qualification-attempt-authorization",
            str(attempt_authorization_path),
            "--qualification-cost-ledger",
            str(ledger_snapshot_path),
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
            _write_infrastructure_failure(
                output_root,
                arm=arm,
                attempt_id=attempt_id,
                error=error,
                log_path=log_path,
            )
            continue
        processes.append(
            {
                "arm": arm,
                "attempt_id": attempt_id,
                "attempt_root": attempt_root,
                "attempt_authorization_path": attempt_authorization_path,
                "ledger_snapshot_path": ledger_snapshot_path,
                "log_path": log_path,
                "log_handle": log_handle,
                "process": process,
            }
        )
        _emit(
            progress_path,
            {
                "event": "qualification_provider_cost_reserved",
                "arm": arm,
                "attempt_number": attempt_number,
                "reserved_cost_usd": proposed_ledger["reserved_cost_usd"],
                "currency_ceiling_usd": proposed_ledger[
                    "qualification_currency_ceiling_usd"
                ],
            },
        )
    next_heartbeat = time.monotonic() + 30.0
    while any(state["process"].poll() is None for state in processes):
        now = time.monotonic()
        if now >= next_heartbeat:
            active = sum(state["process"].poll() is None for state in processes)
            _emit(
                progress_path,
                {
                    "event": "qualification_triplet_heartbeat",
                    "active_provider_processes": active,
                    "elapsed_s": round(now - started, 3),
                },
            )
            next_heartbeat = now + 30.0
        time.sleep(min(1.0, max(0.05, next_heartbeat - now)))
    for state in processes:
        state["process"].wait()
        state["log_handle"].close()
        if not _terminalize_process(output_root, state):
            infrastructure_failures += 1
    attempt_counts, attempts = _audit_attempt_journal(
        output_root,
        manifest=manifest,
        cost_contract=cost_contract,
        authorization=authorization,
    )
    terminal_arms = _audit_terminal_receipts(
        output_root,
        authorization=authorization,
        attempts=attempts,
        attempt_counts=attempt_counts,
    )
    pending_after = [arm for arm in FORMAL_ARMS if arm not in terminal_arms]
    final_ledger = build_qualification_cost_ledger(
        manifest, cost_contract, attempt_counts
    )
    write_json_atomic(ledger_path, final_ledger)
    report_errors: list[str] = []
    report: dict[str, Any] | None = None
    if not pending_after:
        report_path = output_root / "report.json"
        if report_path.is_file():
            report = _load(report_path)
            report_errors = validate_method_qualification_report(
                ROOT, report, manifest
            )
            report_errors.extend(
                _validate_report_terminal_bindings(output_root, report)
            )
        else:
            report, report_errors = _build_report(
                output_root,
                authorization_copy=authorization_copy,
                config_path=config_path,
                world_seed=world_seed,
                elapsed_s=time.monotonic() - started,
                manifest=manifest,
            )
            _write_once(report_path, report)
    status = (
        "infrastructure_incomplete_missing_only_resume_required"
        if pending_after
        else "passed"
        if not report_errors
        else "qualification_failed"
    )
    progress: dict[str, Any] = {
        "schema_version": TRIPLET_PROGRESS_VERSION,
        "formal_result": False,
        "status": status,
        "terminal_arm_count": len(FORMAL_ARMS) - len(pending_after),
        "pending_arms": pending_after,
        "provider_attempt_count": final_ledger["provider_attempt_count"],
        "provider_attempt_counts_by_arm": final_ledger[
            "provider_attempt_counts_by_arm"
        ],
        "reserved_cost_usd": final_ledger["reserved_cost_usd"],
        "qualification_cost_ledger_sha256": final_ledger[
            "qualification_cost_ledger_sha256"
        ],
        "infrastructure_failure_count_this_attempt": infrastructure_failures,
        "qualification_validation_errors": report_errors,
        "report_sha256": report.get("report_sha256") if report is not None else None,
    }
    write_json_atomic(output_root / "execution_progress.json", progress)
    _emit(progress_path, {"event": "qualification_triplet_attempt_finished", **progress})
    return progress


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--execute", action="store_true", required=True)
    parser.add_argument("--authorization", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--progress-file", type=Path, required=True)
    parser.add_argument("--allow-provider-execution", action="store_true")
    parser.add_argument("--resume", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    if not args.allow_provider_execution:
        raise RuntimeError("qualification execution requires --allow-provider-execution")
    progress = execute_triplet(
        authorization_path=args.authorization,
        output_root=args.output_root,
        progress_path=args.progress_file,
        resume=bool(args.resume),
    )
    return 0 if progress["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
