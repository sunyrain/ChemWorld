"""Bounded network recovery at intact EC/PA source or posttest boundaries."""

from __future__ import annotations

import json
import re
import shutil
import tempfile
import time
from copy import deepcopy
from types import SimpleNamespace

from scripts import run_work_ii_ec_dual_goal_trial as ec
from scripts import run_work_ii_pa_single_trial as pa
from scripts.run_work_ii_astra_single_trial import read, write
from scripts.run_work_ii_study_b import _prepare_codex_home

STAGES = ("K1", "Q", "K2")
NETWORK = re.compile(
    r"network error|error sending request|error decoding response body|"
    r"connection (?:reset|closed|refused)|dns error|connection timed out",
    re.I,
)
EXCLUDED = re.compile(r"unauthorized|quota|rate.limit|\b(?:401|403|429)\b", re.I)


def source_folder(unit, folder):
    return folder if unit["system"] == "EC" else folder / "source"


def network_failure(path):
    """Classify only provider error events, never participant scientific text."""
    if not path.is_file():
        return False
    errors = []
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") in ("error", "turn.failed"):
            errors.append(json.dumps(event))
    return (
        bool(errors)
        and any(NETWORK.search(e) for e in errors)
        and not any(EXCLUDED.search(e) for e in errors)
    )


def recovery_kind(unit, result, folder):
    if result.get("status") != "failed":
        return None
    source = result if unit["system"] == "EC" else result.get("source", {})
    physical = source_folder(unit, folder)
    if source.get("operations") == 0 and network_failure(physical / "source-stdout.jsonl"):
        return "fresh_source"
    status = result.get("source_status") if unit["system"] == "EC" else source.get("status")
    if status != "completed" or not source.get("exact_replay", {}).get("verified"):
        return None
    for stage in STAGES:
        turn = result.get("posttests", {}).get(stage, {})
        if turn.get("payload") and not turn.get("failure"):
            continue
        # Missing stages after a failed turn are included only in that recovery.
        if turn.get("failure") and network_failure(physical / stage / "stdout.jsonl"):
            if any(result.get("posttests", {}).get(s) for s in STAGES[STAGES.index(stage) + 1 :]):
                return None
            return "posttests"
        return None
    return None


def usage_delta(before, after):
    if not before.get("valid") or not after.get("valid"):
        return {"known": False, "tokens": None}
    keys = ("input", "cached_input", "output", "uncached_input", "input_plus_output")
    delta = {k: after["total"][k] - before["total"][k] for k in keys}
    return {"known": all(v >= 0 for v in delta.values()), "tokens": delta}


def recover_posttests(unit, original, folder, output, design, truth, progress):
    """Keep original operations and retest; continue the retained provider thread."""
    module = ec if unit["system"] == "EC" else pa
    physical = source_folder(unit, folder)
    receipts = read(physical / "source-receipts.json")
    thread = receipts[-1]["thread_id"]
    result = deepcopy(original)
    result["failure"] = None
    result.pop("posttest_failure", None)
    result["recovery_original_thread"] = thread
    result["status"] = "recovering"
    started = time.monotonic()
    write(output / "result.json", result)
    with tempfile.TemporaryDirectory(prefix="chemworld-network-followup-") as temporary:
        from pathlib import Path

        home = Path(temporary)
        environment = _prepare_codex_home(home, ec.PROVIDER)
        shutil.copytree(physical / "provider-rollouts", home / "codex-home" / "sessions")
        agent = SimpleNamespace(home_root=home, followup_environment=environment)
        try:
            for stage in STAGES:
                previous = original.get("posttests", {}).get(stage, {})
                if previous.get("payload") and not previous.get("failure"):
                    continue
                progress.pop("provider_liveness", None)
                progress.update(stage="network_recovery", phase=stage, unit=unit["unit_id"])
                print(json.dumps({"recovery": unit["unit_id"], "stage": stage}), flush=True)
                turn = module.posttest(agent, output, stage, thread, progress, design=design)
                if turn.get("thread_id") != thread:
                    turn["failure"] = turn.get("failure") or "posttest_thread_changed"
                result["posttests"][stage] = turn
                write(output / "result.json", result)
                if turn.get("failure"):
                    result["failure"] = {"stage": stage, "message": turn["failure"]}
                    break
        finally:
            shutil.copytree(home / "codex-home" / "sessions", output / "provider-rollouts")
    result["prediction_evaluation"] = (
        ec.evaluate_predictions(
            result["posttests"].get("Q", {}).get("payload"), truth, query_set=design["queries"]
        )
        if unit["system"] == "EC"
        else pa.evaluate(result["posttests"].get("Q", {}).get("payload"), truth)
    )
    complete = all(
        result["posttests"].get(s, {}).get("payload") and not result["posttests"][s].get("failure")
        for s in STAGES
    )
    result["posttest_status"] = "completed" if complete else "failed"
    result["status"] = (
        "completed"
        if complete and not result["failure"] and result["prediction_evaluation"].get("valid")
        else "failed"
    )
    result["recovery_elapsed_s"] = time.monotonic() - started
    result["elapsed_s"] = original.get("elapsed_s", 0) + result["recovery_elapsed_s"]
    write(output / "result.json", result)
    return result


def recover(root, report, unit, original, folder, design, truth, progress):
    """One separately recorded recovery per logical source; idempotent after completion."""
    from scripts import run_work_ii_ec_pa_matrix as matrix

    output = root / "recoveries" / unit["unit_id"] / "attempt-1"
    if (output / "recovery.json").is_file():
        return read(output / "recovery.json")
    kind = recovery_kind(unit, original, folder)
    if kind is None:
        return None
    progress.pop("provider_liveness", None)
    progress.update(
        stage="network_recovery",
        phase="source" if kind == "fresh_source" else "posttests",
        unit=unit["unit_id"],
        operations=0,
        batches=0,
        planned_batches=unit["budget"],
    )
    output.mkdir(parents=True, exist_ok=False)
    write(output / "design.json", design)
    write(
        output / "attempt.json",
        {
            "kind": kind,
            "original_result": str(folder / "result.json"),
            "started_epoch": time.time(),
            "max_recovery_attempts_per_source": 1,
            "authorization": "2026-09-19 user requested network-failure retries",
        },
    )
    started = time.monotonic()
    if kind == "posttests":
        result = recover_posttests(unit, original, folder, output, design, truth, progress)
        actual = folder  # Export the preserved source trajectory, with recovered answers.
    elif unit["system"] == "EC":
        result = ec.run_cell(output, unit["goal"], unit["locus"], unit["arm"], truth, progress)
        actual = output / f"{unit['goal']}-{unit['locus']}-{unit['arm']}"
    else:
        actual = output / "run"
        pa.execute(
            actual,
            progress,
            arm=unit["arm"],
            batches=unit["budget"],
            world=unit["world"],
            reference_run=root / "references" / unit["world"]["world_id"],
        )
        result = read(actual / "result.json")
    public = report / unit["unit_id"] / "network-recovery"
    row = matrix.export_source(unit, result, actual, public, design)
    before = matrix.source_row(unit, original)
    additional = (
        usage_delta(before["token_accounting"], row["token_accounting"])
        if kind == "posttests"
        else {
            "known": row["token_accounting"].get("valid", False),
            "tokens": row["token_accounting"].get("total"),
        }
    )
    record = {
        "kind": kind,
        "attempt": 1,
        "row": row,
        "result_path": str((output if kind == "posttests" else actual) / "result.json"),
        "report_path": f"{unit['unit_id']}/network-recovery/REPORT.md",
        "new_source_attempts": int(kind == "fresh_source"),
        "new_source_batches": row["completed_batches"] if kind == "fresh_source" else 0,
        "new_source_operations": row["operations"] if kind == "fresh_source" else 0,
        "new_posttest_attempts": sum(
            bool(result.get("posttests", {}).get(s))
            and (
                kind == "fresh_source"
                or not original.get("posttests", {}).get(s, {}).get("payload")
                or bool(original["posttests"][s].get("failure"))
            )
            for s in STAGES
        ),
        "additional_reported_usage": additional,
        "failed_attempt_usage_complete": False,
        "usage_caveat": "Failed transport usage may be missing. Same-thread delta includes any "
        "reported failed-turn usage; it is not billed cost. Unknown is not zero.",
        "elapsed_s": time.monotonic() - started,
        "original_status": original["status"],
    }
    write(output / "recovery.json", record)
    write(public / "recovery.json", record)
    with (public / "REPORT.md").open("a", encoding="utf-8") as handle:
        handle.write(
            "\n## Network recovery\n\nOriginal failed attempt is retained separately. "
            f"Mode: {kind}; new source batches: {record['new_source_batches']}. "
            "See [recovery accounting](recovery.json).\n"
        )
    return record


def effective_row(row):
    return row.get("network_recovery", {}).get("row", row)
