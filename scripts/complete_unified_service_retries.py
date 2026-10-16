"""Finish user-authorized service-only reruns AFTER the fixed 300-session queue.

CLI: uv run --no-sync python -u -m scripts.complete_unified_service_retries
     --root D:/CW267/a2
Use --inspect for a read-only classification. No participant is called by import,
inspection or tests. Each service round uses the existing isolated runner, <=24
workers, a new short sibling root s01/s02/... and an unchanged scientific design.
Original results are immutable. The primary retained_units map is only a view over
terminal attempts, including unfavorable replacement outcomes. An unresolved or
ambiguous failure yields needs_review; there is no generic retry-on-failure path.
"""

from __future__ import annotations

import argparse
import copy
import json
import os
import re
import shutil
import threading
import time
from collections import Counter
from contextlib import contextmanager
from pathlib import Path

import psutil
from scripts import run_unified_matrices as runner

SCHEMA = "unified-service-retries-v1"
INPUT_DIRS = ("inputs", "references", "matrix-c-opportunity-inputs")
STAGES = ("K1", "Q", "K2")
ACCESS_HOLD = re.compile(
    r"quota|insufficient[ _](?:balance|credit)|billing|payment|authentication|unauthoriz|"
    r"invalid.api.key|(?:http|status)[ _:]*(?:401|403)",
    re.IGNORECASE,
)
EXCLUDED = re.compile(
    r"forbidden.tool|"
    r"context[ _]length|max_output_tokens|maximum.context|tool_budget|resource.budget|"
    r"operation.limit|operation_attempt_limit|session_wall_time|wall_time_limit|"
    r"max_recovered_mcp|max_consecutive_mcp|missing.*recommendation|"
    r"invalid.(?:prediction|forecast|query)|schema.validation|replay.failed|"
    r"publicinputmismatch|public.inputs.differ|required mcp|mcp server|"
    r"failed to initialize|winerror|no such file",
    re.IGNORECASE,
)
SERVICE = (
    ("rate_limit", re.compile(r"rate[ _-]?limit|too many requests|(?:http|status)[ :_]*429", re.I)),
    (
        "provider_5xx",
        re.compile(
            r"(?:http|status|status code)[ :_]*(?:5\d\d)|bad gateway|"
            r"service unavailable|gateway timeout|server overloaded",
            re.I,
        ),
    ),
    (
        "transport",
        re.compile(
            r"stream disconnected|connection (?:reset|closed|aborted)|"
            r"connectionreseterror|broken pipe|error sending request|"
            r"network (?:error|unreachable)|remoteprotocolerror|"
            r"server disconnected|tls handshake|dns resolution",
            re.I,
        ),
    ),
    (
        "provider_timeout",
        re.compile(
            r"(?:connect|read|request|network|socket|api)[ _-]?"
            r"(?:timeout|timed out)|timeouterror|"
            r"request.*timed out",
            re.I,
        ),
    ),
)
PROVIDER_BOUNDARY = re.compile(
    r"provider.failure|provider_startup_failure|max_provider_error_events|"
    r"request_wait_timeout|turn_timeout|missing_payload|"
    r"codex failed before|interrupted_before_next_action|network|transport|"
    r"stream disconnected|connection|timeout|timed out|rate.limit|http|status [45]",
    re.I,
)
MISSING_RESOURCE_MESSAGE = (
    "online model resource accounting must be complete unless provider call/token usage "
    "is explicitly complete and only uncapped monetary accounting is incomplete, or "
    "exactly one bounded experiment session has explicitly deferred usage"
)


class RetryHoldError(RuntimeError):
    """An explicit review/coordination boundary; never retry through it."""


def text(value):
    return value if isinstance(value, str) else json.dumps(value, ensure_ascii=True)


def service_category(message):
    if EXCLUDED.search(message) or ACCESS_HOLD.search(message):
        return None
    return next((name for name, pattern in SERVICE if pattern.search(message)), None)


def coordinator_live(root):
    path = Path(root) / "coordinator.json"
    if not path.exists():
        return False
    state = runner.read(path)
    try:
        process = psutil.Process(int(state["pid"]))
        expected = state.get("process_created_epoch")
        return expected is None or process.create_time() == expected
    except psutil.NoSuchProcess:
        return False
    except (psutil.AccessDenied, KeyError, TypeError, ValueError):
        raise RetryHoldError(f"Cannot establish coordinator liveness: {path}") from None


@contextmanager
def controller_lock(root):
    """PID creation time prevents parallel retry controllers and PID reuse errors."""
    path = root / "service-retries.lock.json"
    if path.exists():
        previous = runner.read(path)
        try:
            process = psutil.Process(int(previous["pid"]))
            if process.create_time() == previous["process_created_epoch"]:
                raise RetryHoldError("Another service-retry controller is alive")
        except psutil.NoSuchProcess:
            pass
        path.unlink()
    fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(
                {"pid": os.getpid(), "process_created_epoch": psutil.Process().create_time()},
                handle,
            )
        yield
    finally:
        path.unlink(missing_ok=True)


def stage_evidence(path, stage):
    """Read error events only in the failed stage; later turn completion cancels them."""
    paths = []
    if stage == "source":
        paths = list(path.rglob("source-stdout.jsonl"))
    else:
        paths = [p for p in path.rglob("stdout.jsonl") if p.parent.name.upper() == stage]
    matches = []
    recovered_event_seen = False
    for event_path in paths:
        last_error = None
        completed_after_error = False
        with event_path.open(encoding="utf-8", errors="replace") as handle:
            for line in handle:
                try:
                    event = json.loads(line)
                except ValueError:
                    continue
                if not isinstance(event, dict):
                    continue
                kind = event.get("type")
                if kind in {"error", "turn.failed"}:
                    error = event.get("error")
                    message = event.get("message") or (
                        error.get("message", "") if isinstance(error, dict) else error or ""
                    )
                    last_error = str(message)
                    completed_after_error = False
                elif kind == "turn.completed":
                    completed_after_error = True
        if last_error and not completed_after_error:
            category = service_category(last_error)
            if category:
                matches.append(
                    {"category": category, "path": str(event_path), "kind": "terminal_error_event"}
                )
            elif ACCESS_HOLD.search(last_error):
                return [], "technical_access_block"
            elif EXCLUDED.search(last_error):
                return [], "terminal_error_is_nonservice"
        elif last_error and completed_after_error:
            recovered_event_seen = True
    # A retained terminal receipt can establish the same failure if the raw stream
    # is absent; aggregated earlier/recovered event counts never establish this.
    receipt_paths = (
        list(path.rglob("source-receipts.json"))
        if stage == "source"
        else [p for p in path.rglob("receipt.json") if p.parent.name.upper() == stage]
    )
    for receipt_path in receipt_paths:
        value = runner.read(receipt_path)
        receipt = value[-1] if isinstance(value, list) and value else value
        if not isinstance(receipt, dict):
            continue
        failure = receipt.get("failure") or receipt.get("failure_type")
        terminal = receipt.get("status")
        if not failure or terminal in {"completed", "accepted", "terminal_accepted"}:
            continue
        if ACCESS_HOLD.search(text(failure)):
            return [], "technical_access_block"
        # provider_errors is cumulative. A direct terminal service error is
        # required before its categories can support a missing-stream fallback.
        if recovered_event_seen or not service_category(text(failure)):
            continue
        for error in receipt.get("provider_errors", []):
            if not isinstance(error, dict):
                continue
            category = error.get("category")
            if category in {"quota_or_balance", "authentication", "permission"}:
                return [], "technical_access_block"
            if category == "context_limit":
                return [], "terminal_receipt_is_nonservice"
            if category in {"rate_limit", "provider_server", "network", "capacity"}:
                matches.append(
                    {
                        "category": category,
                        "path": str(receipt_path),
                        "kind": "failed_stage_receipt",
                    }
                )
    return matches, None


def is_confirmed_p_usage_interruption(path, unit, result, failure):
    """One observed secondary error: P source disconnected before emitting usage.

    This exact host ValueError is not itself a retry reason. Require the same
    failed source's terminal transport event, failed receipt and absent usage.
    """
    if (
        unit["system"] != "P"
        or not isinstance(failure, dict)
        or failure.get("type") != "ValueError"
        or failure.get("message") != MISSING_RESOURCE_MESSAGE
        or result.get("posttests")
        or not (result.get("source", {}).get("exact_replay") or {}).get("verified")
    ):
        return False
    evidence, exclusion = stage_evidence(path, "source")
    if exclusion or not any(e["kind"] == "terminal_error_event" for e in evidence):
        return False
    for receipt_path in path.rglob("source-receipts.json"):
        values = runner.read(receipt_path)
        receipt = values[-1] if isinstance(values, list) and values else {}
        if (
            receipt.get("status") in {"failed", "interrupted_before_next_action"}
            and receipt.get("usage_complete") is False
            and receipt.get("usage_observed") is False
            and receipt.get("usage_unavailable_reason")
            in {
                "codex_cli_completed_without_usage_event",
                "codex_cli_emitted_no_usage_before_forced_termination",
            }
        ):
            return True
    return False


def classify_unit(root, unit, design=None):
    design = design or runner.read(root / "design.json")
    path = runner.folder(root, unit, design)
    state = runner.read(path / "status.json") if (path / "status.json").exists() else {}
    result = runner.read(path / "result.json") if (path / "result.json").exists() else {}
    decision = {
        "key": runner.unit_key(unit),
        "original_path": str(path),
        "stage": None,
        "category": None,
        "evidence_paths": [],
        "classification": "not_eligible",
    }
    status = state.get("status")
    if status == "completed":
        return {**decision, "reason": "completed_unit"}
    if status not in runner.TERMINAL or not result:
        return {**decision, "classification": "needs_review", "reason": "missing_terminal_result"}
    source = result.get("source") or {}
    stages = result.get("posttests") or {}
    validation = result.get("posttest_validation") or {}
    sealed = all(
        stages.get(s, {}).get("payload")
        and not stages[s].get("failure")
        and validation.get(s, {}).get("valid", True)
        for s in STAGES
    )
    if sealed and len(source.get("batches", [])) == unit["batches"]:
        return {**decision, "reason": "scientific_or_completion_failure_after_intact_research"}
    top = result.get("failure") or state.get("failure")
    if ACCESS_HOLD.search(text(top)):
        return {
            **decision,
            "classification": "needs_review",
            "category": "technical_access_block",
            "reason": "technical_access_block",
        }
    failures = []
    source_failure = source.get("failure")
    top_stage = top.get("stage") if isinstance(top, dict) else None
    if source_failure:
        failures.append(("source", source_failure))
    elif top_stage in {"source", "source_startup", "research"}:
        failures.append(("source", top))
    for stage in STAGES:
        failure = stages.get(stage, {}).get("failure")
        if failure:
            failures.append((stage, failure))
            break
    if not failures and top_stage in STAGES:
        failures.append((top_stage, top))
    if not failures and PROVIDER_BOUNDARY.search(text(top)) and not stages:
        failures.append(("source", top))
    if result.get("fatal_execution_error") or result.get("adapter_failure"):
        return {**decision, "classification": "needs_review", "reason": "adapter_execution_defect"}
    for stage, failure in failures:
        message = text(failure)
        if stage != "source" and (
            source_failure
            or len(source.get("batches", [])) != unit["batches"]
            or (source.get("operations") and not (source.get("exact_replay") or {}).get("verified"))
        ):
            return {
                **decision,
                "stage": stage,
                "reason": "source_incomplete_before_posttest_failure",
            }
        if ACCESS_HOLD.search(message):
            return {
                **decision,
                "stage": stage,
                "classification": "needs_review",
                "category": "technical_access_block",
                "reason": "technical_access_block",
            }
        if EXCLUDED.search(message):
            return {
                **decision,
                "stage": stage,
                "reason": "nonservice_failure",
                "classification": "needs_review" if status == "execution_error" else "not_eligible",
            }
        secondary_usage = stage == "source" and is_confirmed_p_usage_interruption(
            path, unit, result, failure
        )
        if not (PROVIDER_BOUNDARY.search(message) or service_category(message) or secondary_usage):
            if stage == "source":
                return {
                    **decision,
                    "stage": stage,
                    "classification": "needs_review",
                    "reason": "source_failure_is_not_an_identified_service_interruption",
                }
            continue
        evidence, exclusion = stage_evidence(path, stage)
        if exclusion:
            return {
                **decision,
                "stage": stage,
                "reason": exclusion,
                "classification": "needs_review"
                if exclusion == "technical_access_block" or status == "execution_error"
                else "not_eligible",
            }
        if evidence:
            return {
                **decision,
                "classification": "eligible",
                "stage": stage,
                "category": evidence[0]["category"],
                "evidence_paths": [e["path"] for e in evidence],
                "reason": "confirmed_p_transport_interruption_with_missing_usage"
                if secondary_usage
                else "terminal_provider_boundary_and_matching_stage_service_error",
            }
        return {
            **decision,
            "stage": stage,
            "classification": "needs_review",
            "reason": "provider_boundary_without_positive_service_evidence",
        }
    if status == "execution_error":
        return {**decision, "classification": "needs_review", "reason": "other_execution_defect"}
    return {**decision, "reason": "scientific_or_protocol_outcome"}


def inspect_primary(root):
    if coordinator_live(root):
        raise RetryHoldError(
            "Primary coordinator is still alive; service retries run only afterward"
        )
    design = runner.read(root / "design.json")
    if len(design["schedule"]) != 300 or design.get("planned_sessions") != 300:
        raise RetryHoldError("Expected the fixed 300-session primary design")
    for unit in design["schedule"]:
        path = runner.folder(root, unit, design)
        if (
            not (path / "status.json").exists()
            or runner.read(path / "status.json").get("status") not in runner.TERMINAL
        ):
            raise RetryHoldError(
                "The primary 300-session queue has not fully reached terminal status"
            )
    return design, [classify_unit(root, unit, design) for unit in design["schedule"]]


def save_ledger(root, ledger):
    ledger["updated_at"] = runner.now()
    runner.write(root / "service-retries.json", ledger)


def publish_phase(root, ledger, progress=None):
    value = {
        "status": ledger["status"],
        "round": len(ledger["rounds"]),
        **(ledger.get("final") or {}),
        **(progress or {}),
    }
    stage = "terminal" if ledger["status"] == "completed" else "service_retries_" + ledger["status"]
    path = root / "summary.json"
    summary = runner.read(path) if path.exists() else {}
    summary.update(stage=stage, service_retries=value)
    runner.write(path, summary)
    # Both views use the effective-unit counts refreshed after each retry round.
    # Updating only the phase of the old completion file retained first-pass totals.
    runner.write(
        root / "completion-status.json", {k: v for k, v in summary.items() if k != "cases"}
    )


def update_final(root, ledger, decisions):
    design = runner.read(root / "design.json")
    attempts = [a for r in ledger["rounds"] for a in r.get("attempts", [])]
    completed = sum(
        runner.read(runner.folder(root, u, design) / "status.json")["status"] == "completed"
        for u in design["schedule"]
    )
    counts = Counter(d["classification"] for d in decisions)
    ledger["final"] = {
        "effective_units": 300,
        "service_retry_attempts": len(attempts),
        "planned_retry_attempts": sum(len(r["eligible_keys"]) for r in ledger["rounds"]),
        "retried_units": len({a["key"] for a in attempts}),
        "service_interruptions_remaining": counts["eligible"],
        "needs_review": counts["needs_review"],
        "scientific_failures_retained": sum(
            d["classification"] == "not_eligible" and d["reason"] != "completed_unit"
            for d in decisions
        ),
        "completed_units": completed,
    }


def prepare_round(root, ledger, design, decisions):
    number = len(ledger["rounds"]) + 1
    retry_root = root.parent / f"s{number:02d}"
    if retry_root.exists():
        raise RetryHoldError(f"Unowned retry root already exists: {retry_root}")
    selected = [d for d in decisions if d["classification"] == "eligible"]
    record = {
        "round": number,
        "root": str(retry_root),
        "state": "preparing",
        "created_at": runner.now(),
        "eligible_keys": [d["key"] for d in selected],
        "decisions": selected,
        "attempts": [],
    }
    ledger["rounds"].append(record)
    ledger["status"] = "running"
    save_ledger(root, ledger)  # Own the destination durably BEFORE creating/copying it.
    publish_phase(
        root,
        ledger,
        {"round_attempts": len(selected), "round_remaining": len(selected), "eta_s": None},
    )
    finish_preparation(root, ledger, record, design)
    return record


def finish_preparation(root, ledger, record, design):
    retry_root = Path(record["root"])
    retry_root.mkdir(parents=True, exist_ok=True)
    if any(retry_root.glob("repeat-*")):
        raise RetryHoldError("Partial preparation already contains participant attempts")
    for name in INPUT_DIRS:
        if not (root / name).is_dir():
            raise RetryHoldError(f"Prepared scientific inputs missing: {name}")
        shutil.copytree(root / name, retry_root / name, dirs_exist_ok=True)
    selected = set(record["eligible_keys"])
    retry_design = copy.deepcopy(design)
    retry_design["workers"] = min(24, int(design["workers"]))
    retry_design["retained_units"] = {
        runner.unit_key(u): str(runner.folder(root, u, design))
        for u in design["schedule"]
        if runner.unit_key(u) not in selected
    }
    retry_design["service_retry"] = {
        "primary_root": str(root),
        "round": record["round"],
        "eligible_keys": record["eligible_keys"],
    }
    runner.write(retry_root / "design.json", retry_design)
    runner.write(
        retry_root / "prepared.json",
        {"at": runner.now(), "planned_sessions": 300, "service_retry_sessions": len(selected)},
    )
    record["state"] = "prepared"
    save_ledger(root, ledger)


def merge_terminal_attempts(root, ledger, record):
    """Idempotent two-file publication; raw originals and retry results never change."""
    design = runner.read(root / "design.json")
    units = {runner.unit_key(u): u for u in design["schedule"]}
    selected = {d["key"]: d for d in record["decisions"]}
    existing = {a["key"]: a for a in record["attempts"]}
    mapping = design.setdefault("retained_units", {})
    for key in record["eligible_keys"]:
        path = Path(record["root"]) / units[key]["repeat"] / units[key]["id"]
        state_path = path / "status.json"
        if not state_path.exists():
            continue
        state = runner.read(state_path)
        if state.get("status") not in runner.TERMINAL:
            continue
        current = str(runner.folder(root, units[key], design))
        if current not in {selected[key]["original_path"], str(path)}:
            raise RetryHoldError(f"Effective unit changed outside this retry round: {key}")
        if key not in existing:
            record["attempts"].append(
                {
                    "key": key,
                    "original_path": selected[key]["original_path"],
                    "retry_path": str(path),
                    "status": state["status"],
                    "failure": state.get("failure"),
                    "ended_at": state.get("ended_at", runner.now()),
                }
            )
        mapping[key] = str(path)
    record["state"] = "publishing"
    save_ledger(root, ledger)
    runner.write(root / "design.json", design)
    all_terminal = len(record["attempts"]) == len(record["eligible_keys"])
    record["state"] = "completed" if all_terminal else "needs_review"
    record["ended_at"] = runner.now()
    save_ledger(root, ledger)
    runner.snapshot(root)
    return all_terminal


def run_round(root, ledger, record, run_function):
    retry_root = Path(record["root"])
    if coordinator_live(retry_root):
        raise RetryHoldError(f"Retry round already has a live coordinator: {retry_root}")
    retry_design = runner.read(retry_root / "design.json")
    selected = set(record["eligible_keys"])
    units = [u for u in retry_design["schedule"] if runner.unit_key(u) in selected]
    for unit in units:
        path = retry_root / unit["repeat"] / unit["id"]
        if path.exists() and (
            not (path / "status.json").exists()
            or runner.read(path / "status.json").get("status") not in runner.TERMINAL
        ):
            raise RetryHoldError(
                f"Ambiguous partial retry attempt retained without relaunch: {path}"
            )
    all_terminal = all((retry_root / u["repeat"] / u["id"] / "status.json").exists() for u in units)
    if all_terminal:
        return merge_terminal_attempts(root, ledger, record)
    record.update(state="running", started_at=record.get("started_at", runner.now()))
    ledger["status"] = "running"
    save_ledger(root, ledger)
    stop = threading.Event()

    def progress():
        while not stop.is_set():
            summary_path = retry_root / "summary.json"
            summary = runner.read(summary_path) if summary_path.exists() else {}
            terminal = sum(
                (retry_root / u["repeat"] / u["id"] / "status.json").exists()
                and runner.read(retry_root / u["repeat"] / u["id"] / "status.json").get("status")
                in runner.TERMINAL
                for u in units
            )
            value = {
                "round_attempts": len(units),
                "round_terminal": terminal,
                "round_remaining": len(units) - terminal,
                "eta_s": summary.get("eta_s"),
            }
            publish_phase(root, ledger, value)
            runner.emit({"stage": "service_retries", "round": record["round"], **value})
            stop.wait(30)

    heartbeat = threading.Thread(target=progress, daemon=True)
    heartbeat.start()
    try:
        record["exit_code"] = run_function(retry_root)
    finally:
        stop.set()
        heartbeat.join(timeout=5)
        save_ledger(root, ledger)
    return merge_terminal_attempts(root, ledger, record)


def complete(root, *, run_function=None, retry_delay_s=30):
    root = Path(root).resolve()
    run_function = run_function or runner.run
    design, decisions = inspect_primary(root)
    with controller_lock(root):
        ledger_path = root / "service-retries.json"
        ledger = (
            runner.read(ledger_path)
            if ledger_path.exists()
            else {
                "schema": SCHEMA,
                "primary_root": str(root),
                "created_at": runner.now(),
                "status": "inspecting",
                "rounds": [],
                "original_units": {
                    runner.unit_key(u): str(runner.folder(root, u, design))
                    for u in design["schedule"]
                },
            }
        )
        if ledger.get("schema") != SCHEMA or ledger.get("primary_root") != str(root):
            raise RetryHoldError("Retry ledger belongs to a different study or schema")
        try:
            while True:
                pending = (
                    ledger["rounds"][-1]
                    if ledger["rounds"] and ledger["rounds"][-1]["state"] != "completed"
                    else None
                )
                if pending:
                    if pending["state"] == "needs_review":
                        raise RetryHoldError("Previous retry round is held for explicit review")
                    if pending["state"] == "preparing":
                        finish_preparation(root, ledger, pending, design)
                    if not run_round(root, ledger, pending, run_function):
                        _, decisions = inspect_primary(root)
                        update_final(root, ledger, decisions)
                        ledger["latest_decisions"] = decisions
                        raise RetryHoldError(
                            "Retry round stopped before all selected units became terminal"
                        )
                design, decisions = inspect_primary(root)
                update_final(root, ledger, decisions)
                ledger["latest_decisions"] = decisions
                if not any(d["classification"] == "eligible" for d in decisions):
                    if any(d["classification"] == "needs_review" for d in decisions):
                        raise RetryHoldError(
                            "Remaining terminal failures require review; "
                            "no ambiguous reruns launched"
                        )
                    ledger["status"] = "completed"
                    save_ledger(root, ledger)
                    runner.snapshot(root)
                    publish_phase(root, ledger)
                    runner.emit({"stage": "service_retries_completed", **ledger["final"]})
                    return ledger
                if ledger["rounds"] and retry_delay_s:
                    runner.emit({"stage": "service_retry_backoff", "seconds": retry_delay_s})
                    time.sleep(min(60, max(0, retry_delay_s)))
                prepare_round(root, ledger, design, decisions)
        except Exception as exc:
            ledger["status"] = "needs_review"
            ledger["hold"] = {"type": type(exc).__name__, "message": str(exc), "at": runner.now()}
            save_ledger(root, ledger)
            publish_phase(root, ledger)
            raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--inspect", action="store_true")
    args = parser.parse_args()
    try:
        if args.inspect:
            _, decisions = inspect_primary(args.root.resolve())
            runner.emit(
                {
                    "counts": dict(Counter(d["classification"] for d in decisions)),
                    "decisions": decisions,
                }
            )
        else:
            complete(args.root)
    except RetryHoldError as exc:
        runner.emit({"stage": "service_retries_needs_review", "reason": str(exc)})
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
