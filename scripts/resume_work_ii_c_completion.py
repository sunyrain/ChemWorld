"""Resume the user-authorized C matrix, preserving completed chains and failed attempts."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import threading
import time
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace

import psutil
from scripts import run_work_ii_c_formal as formal
from scripts.recover_work_ii_ec_pa_network import EXCLUDED, network_failure, provider_errors
from scripts.run_work_ii_final_diagnostic import read, write


def transport_failure(folder: Path) -> bool:
    return retryable_transport(folder / "source-stdout.jsonl")


def retryable_transport(path: Path) -> bool:
    errors = provider_errors(path)
    return network_failure(path) or (
        any("idle timeout waiting for sse" in e.lower() for e in errors)
        and not any(EXCLUDED.search(e) for e in errors)
    )


def retry_delay(failures: int) -> int:
    return min(900, 60 * 2 ** min(max(failures - 1, 0), 4))


def atomic_write(path: Path, value) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    write(temporary, value)
    temporary.replace(path)


def archive_source_failure(root: Path, cell: dict, result: dict) -> Path:
    """Preserve a diagnosed attempt before reusing its effective-source slot."""
    folder = root / "sources" / cell["id"]
    if (
        result["status"] != "failed"
        or result["failure"].get("stage") != "source"
        or result["posttests"]
        or not transport_failure(folder)
        or (
            result["source"]["operations"]
            and result["source"]["exact_replay"].get("verified") is not True
        )
    ):
        raise ValueError("Source is not an isolated, replay-verified transport failure")
    parent = root / "failed-sources" / cell["id"]
    parent.mkdir(parents=True, exist_ok=True)
    destination = parent / f"attempt-{len(list(parent.glob('attempt-*'))) + 1:04d}"
    # Both absolute targets must be inside this new recovery root before moving.
    for target in (folder, destination):
        if not target.resolve().is_relative_to(root.resolve()):
            raise ValueError("Source archive escaped the recovery root")
    folder.rename(destination)
    prior = read(root / "prior-attempt.json")
    prior.setdefault("automatic_failed_attempts", []).append(
        {
            "cell": cell["id"],
            "original_folder": str(folder),
            "root": str(destination),
            "operations": result["source"]["operations"],
            "final_assays": len(result["source"]["batches"]),
            "failure": result["failure"],
            "tokens": result.get("tokens"),
            "exact_replay": result["source"]["exact_replay"],
        }
    )
    prior["operations"] += result["source"]["operations"]
    prior["final_assays"] += len(result["source"]["batches"])
    prior["provider_sources"] += 1
    atomic_write(root / "prior-attempt.json", prior)
    return destination


def retry_posttest(call, agent, folder, stage, thread_id, progress, design, wait):
    """Continue only a disconnected posttest; keep its thread and calculator ledger."""
    attempts, elapsed = [], 0.0
    while True:
        turn = call(agent, folder, stage, thread_id, progress, design)
        elapsed += turn.get("elapsed_s", 0)
        if not (
            turn.get("failure") == "provider_failure"
            and not turn.get("payload")
            and turn.get("thread_id") in (None, thread_id)
            and retryable_transport(folder / stage / "stdout.jsonl")
        ):
            if attempts:
                turn["elapsed_s"] = elapsed
                turn["transport_recovery_attempts"] = attempts
                write(folder / stage / "receipt.json", turn)
            return turn
        archive = folder / "posttest-interruptions" / stage / f"attempt-{len(attempts) + 1:04d}"
        archive.parent.mkdir(parents=True, exist_ok=True)
        for target in (folder / stage, archive):
            if not target.resolve().is_relative_to(folder.resolve()):
                raise ValueError("Posttest archive escaped its source folder")
        # launch() requires a fresh output directory. Move the sealed failed turn
        # to its archive while keeping the cumulative calculator audit in place.
        (folder / stage).rename(archive)
        audit = folder / f"{stage}-numerics.jsonl"
        if audit.exists():
            shutil.copyfile(audit, archive / "numerics-through-interruption.jsonl")
        attempts.append({"root": str(archive), "receipt": turn})
        # The live numerics audit is deliberately never reset: its 128-call limit
        # applies across retries. The original thread retains partial turn context.
        wait(len(attempts), stage)


def prepare(
    original: Path,
    root: Path,
    report: Path,
    retained_completed: int,
    retry_cells: list[str],
    recovery_index: int,
    automatic: bool = False,
) -> None:
    formal.verify_frozen(original)
    if formal.controller_alive(read(original / "controller-status.json")):
        raise ValueError("Original controller remains alive")
    completed, failed = [], []
    for cell in read(original / "design.json")["schedule"]:
        folder = original / "sources" / cell["id"]
        if not folder.exists():
            continue
        result = read(folder / "result.json")
        if result["status"] == "completed":
            completed.append(cell["id"])
        elif (
            cell["id"] in retry_cells
            and result["status"] == "failed"
            and result["failure"].get("stage") == "source"
            and not result["posttests"]
            and transport_failure(folder)
            and (
                not result["source"]["operations"]
                or result["source"]["exact_replay"].get("verified") is True
            )
        ):
            failed.append(
                {
                    "cell": cell["id"],
                    "root": str(folder),
                    "failure": result["failure"],
                    "operations": result["source"]["operations"],
                    "final_assays": len(result["source"]["batches"]),
                    "tokens": result.get("tokens"),
                    "exact_replay": result["source"]["exact_replay"],
                }
            )
        else:
            raise ValueError(f"Unclassified retained source: {cell['id']}")
    if len(completed) != retained_completed or {f["cell"] for f in failed} != set(retry_cells):
        raise ValueError("Completion recovery coverage differs from the declared operator note")
    root.mkdir(parents=True, exist_ok=False)
    files = ["design.json", "release.json", "qualification/result.json"]
    files += [f"qualification/W{i:02d}/queries/result.json" for i in range(1, 6)]
    for relative in files:
        destination = root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(original / relative, destination)
        if destination.read_bytes() != (original / relative).read_bytes():
            raise ValueError(f"Copy differs: {relative}")
    for cell in completed:
        shutil.copytree(original / "sources" / cell, root / "sources" / cell)
    prior = read(original / "prior-attempt.json")
    write(
        root / "prior-attempt.json",
        {
            "root": str(original),
            "qualification_reused_from": str(original / "qualification"),
            "qualification_reexecuted": False,
            "retained_completed_cells": completed,
            "retry_cells": retry_cells,
            "transport_recovery": recovery_index,
            "failed_attempts": failed,
            "earlier_attempt": prior,
            "operations": prior["operations"] + sum(f["operations"] for f in failed),
            "final_assays": prior["final_assays"] + sum(f["final_assays"] for f in failed),
            "provider_sources": prior["provider_sources"] + len(failed),
            "retry_limit_per_declared_cell": 1,
            "automatic_transport_recovery": automatic,
        },
    )
    if automatic:
        prior = read(root / "prior-attempt.json")
        prior["retry_limit_per_declared_cell"] = None
        prior["retry_policy"] = "transport only; exponential backoff 60..900 seconds"
        write(root / "prior-attempt.json", prior)
    formal.verify_frozen(root)
    formal.export(root, report)


def run(root: Path, report: Path, proxy: str, *, automatic: bool = False) -> None:
    if (root / "controller-status.json").exists():
        raise ValueError("This completion recovery already started; inspect its durable boundary")
    for name in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY"):
        os.environ[name] = proxy
    os.environ["NO_PROXY"] = "localhost,127.0.0.1,::1"
    formal.verify_frozen(root)
    if not read(root / "qualification/result.json")["passed"]:
        raise ValueError("Qualification has not passed")
    design = read(root / "design.json")
    prior = read(root / "prior-attempt.json")
    retained_completed = len(prior["retained_completed_cells"])
    started = time.monotonic()
    state = {
        "pid": os.getpid(),
        "process_created": psutil.Process().create_time(),
        "stage": "sources",
        "started_epoch": time.time(),
        "transport_recovery": prior["transport_recovery"],
        "automatic_transport_recovery": automatic,
        "retry_events": 0,
    }
    progress = {"stage": "starting", "phase": "source", "operations": 0, "batches": 0}
    stop = threading.Event()
    emit_lock = threading.Lock()

    def _emit():
        temporary = root / "controller-status.tmp"
        write(temporary, {**state, "epoch": time.time()})
        temporary.replace(root / "controller-status.json")
        summary = formal.export(root, report)
        if automatic:
            summary["automatic_recovery"] = {
                "status": state.get("activity", "executing"),
                "retry_events": state["retry_events"],
                "retry_at_epoch": state.get("retry_at_epoch"),
                "cell": progress.get("stage"),
                "phase": progress.get("phase"),
            }
            atomic_write(report / "summary.json", summary)
            path = report / "REPORT.md"
            body = path.read_text(encoding="utf-8")
            body = body.replace("reference final assays", "interrupted source batch assays")
            body = body.replace(
                "These do not count as sealed qualification units.",
                "These are extra source attempts, excluded from effective matrix denominators.",
            )
            banner = (
                f"Automatic transport recovery: {state.get('activity', 'executing')}; "
                f"retry events: {state['retry_events']}. "
                "Single executor; 60/120/240/480/900-second backoff; "
                "completed results and scientific outcomes are not retried.\n\n"
            )
            if state.get("retry_at_epoch"):
                banner += (
                    "Next attempt at "
                    + time.strftime("%Y-%m-%d %H:%M:%S %z", time.localtime(state["retry_at_epoch"]))
                    + f"; cell {progress.get('stage')}, phase {progress.get('phase')}.\n\n"
                )
            path.write_text(body.replace("\n\n", "\n\n" + banner, 1), encoding="utf-8")
        elapsed = time.monotonic() - started
        fresh = summary["completed_chains"] - retained_completed
        current = {
            **progress,
            "completed_chains": summary["completed_chains"],
            "planned_chains": 30,
            "sealed_batches": summary["sealed_batches"],
            "elapsed_s": round(elapsed),
            "chains_per_hour": fresh * 3600 / elapsed if elapsed else 0,
            "eta_s": (
                elapsed / fresh * (30 - summary["completed_chains"])
                if fresh > 0 and state.get("activity") != "retry_wait"
                else None
            ),
            "activity": state.get("activity", "executing"),
            "retry_events": state["retry_events"],
            "retry_at_epoch": state.get("retry_at_epoch"),
        }
        write(root / "progress.json", current)
        print(json.dumps(current), flush=True)

    def emit():
        with emit_lock:
            _emit()

    def heartbeat():
        while not stop.wait(30):
            emit()

    def wait_for_retry(failures, phase):
        delay = retry_delay(failures)
        state.update(
            activity="retry_wait",
            retry_at_epoch=time.time() + delay,
            retry_events=state["retry_events"] + 1,
        )
        progress["phase"] = phase
        emit()
        deadline = time.monotonic() + delay
        while time.monotonic() < deadline:
            time.sleep(min(30, max(0, deadline - time.monotonic())))
        state.update(activity="executing", retry_at_epoch=None)
        emit()

    original_posttest = formal.pilot.posttest

    def automatic_posttest(agent, folder, stage, thread_id, progress, design):
        return retry_posttest(
            original_posttest, agent, folder, stage, thread_id, progress, design, wait_for_retry
        )

    emit()
    thread = threading.Thread(target=heartbeat, daemon=True)
    thread.start()
    if automatic:
        formal.pilot.posttest = automatic_posttest
    try:
        for cell in design["schedule"]:
            folder = root / "sources" / cell["id"]
            if folder.exists():
                if read(folder / "result.json")["status"] == "completed":
                    continue
                raise ValueError(f"Unexpected retained attempt: {cell['id']}")
            formal.verify_frozen(root)
            source_failures = 0
            while True:
                result = formal.source(root, cell, progress)
                emit()
                if not (automatic and transport_failure(folder) and result["status"] == "failed"):
                    break
                with emit_lock:
                    archive_source_failure(root, cell, result)
                source_failures += 1
                wait_for_retry(source_failures, "source")
                formal.verify_frozen(root)
            if transport_failure(folder) and result["status"] != "completed":
                state.update(
                    stage="interrupted", reason="provider_transport_failure", cell=cell["id"]
                )
                break
            if result.get("source", {}).get("exact_replay", {}).get("verified") is not True:
                state.update(
                    stage="interrupted",
                    activity="halted",
                    reason="source_replay_not_verified",
                    cell=cell["id"],
                )
                break
        else:
            summary = formal.export(root, report)
            state["stage"] = (
                "completed" if summary["completed_chains"] == 30 else "ended_with_incomplete_chains"
            )
            state["activity"] = "finished"
    except BaseException as exc:
        state.update(
            stage="interrupted",
            activity="halted",
            failure={"type": type(exc).__name__, "message": str(exc)},
        )
        raise
    finally:
        formal.pilot.posttest = original_posttest
        stop.set()
        thread.join(timeout=5)
        emit()


def repair_posttests(root, cell, progress, wait):
    """Repair a retained posttest interruption without rerunning source experiments."""
    folder = root / "sources" / cell["id"]
    original = read(folder / "result.json")
    context = Path((original.get("posttest_repair") or {}).get("root", folder))
    failed_stage = (original.get("failure") or {}).get("stage")
    error_path = context / str(failed_stage) / "stdout.jsonl"
    revoked = any("refresh token was revoked" in e.lower() for e in provider_errors(error_path))
    if (
        original["status"] != "failed"
        or failed_stage not in ("K1", "Q", "K2")
        or not (retryable_transport(error_path) or revoked)
        or original["source"]["exact_replay"].get("verified") is not True
    ):
        return False
    previous_turn = read(context / failed_stage / "receipt.json")
    if previous_turn.get("payload"):
        return False
    receipts = read(folder / "source-receipts.json")
    if not formal.pilot.ec.posttest_context_available(receipts[-1]):
        raise ValueError("Posttest repair has no intact terminal source context")
    home = Path(read(folder / "runtime-location.json")["home"])
    if not (home / "codex-home" / "sessions").exists():
        raise ValueError("Retained posttest thread storage is missing")
    if revoked:
        current_auth = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")) / "auth.json"
        isolated_auth = home / "codex-home/auth.json"
        if not current_auth.exists() or current_auth.read_bytes() == isolated_auth.read_bytes():
            raise ValueError("Revoked isolated login has no newer local credential to reuse")
        # Same authorized provider account, refreshed credential only; no token is
        # logged and the retained session/context files remain untouched.
        shutil.copyfile(current_auth, isolated_auth)
    ordinal = len(list(folder.glob("posttest-repair*"))) + 1
    repair = folder / ("posttest-repair" if ordinal == 1 else f"posttest-repair-{ordinal}")
    repair.mkdir(exist_ok=False)
    write(repair / "original-result.json", original)
    design = read(root / "design.json")
    environment = {**os.environ, "CODEX_HOME": str(home / "codex-home")}
    agent = SimpleNamespace(home_root=home, followup_environment=environment)
    result = deepcopy(original)
    result["failure"] = None
    result["posttest_repair"] = {"root": str(repair), "original_failure": original["failure"]}
    if revoked:
        result["posttest_repair"]["credential_refreshed_from_current_local_login"] = True
    started = time.monotonic()
    thread_id = receipts[-1]["thread_id"]
    for stage in ("K1", "Q", "K2"):
        sealed = result["posttests"].get(stage, {})
        if sealed.get("payload") and not sealed.get("failure"):
            continue
        audit = context / f"{stage}-numerics.jsonl"
        if audit.exists():
            shutil.copyfile(audit, repair / audit.name)
        progress.update(stage=cell["id"], phase=stage)
        turn = retry_posttest(
            formal.pilot.posttest, agent, repair, stage, thread_id, progress, design, wait
        )
        result["posttests"][stage] = turn
        write(repair / "result.json", result)
        if turn.get("failure"):
            result["failure"] = {"stage": stage, "message": turn["failure"]}
            break
    references = read(root / "qualification" / f"W{cell['world_seed'] + 1:02d}/queries/result.json")
    truths = dict(zip([q["query_id"] for q in design["queries"]], references["truth"], strict=True))
    result["prediction_evaluation"] = formal.evaluate(
        result["posttests"].get("Q", {}).get("payload"), truths, design["queries"]
    )
    records = formal.load_jsonl(folder / "trajectory.jsonl")
    if "public_baselines" not in result:
        try:
            result["public_baselines"] = formal.public_baselines(records, design["queries"], truths)
        except ValueError as exc:
            if "Unknown transaction status" not in str(exc):
                raise
            # Preserve the baseline diagnostic; it must not erase sealed answers.
            result["public_baselines"] = {"available": False, "failure": str(exc)}
    if "recommendation_retest" not in result:
        selected = (result.get("recommendation") or {}).get("selected_experiment_index")
        batch = next(
            (b for b in result["source"]["batches"] if b["lifecycle_index"] == selected), None
        )
        if batch:
            # Later failed operations cannot change an earlier selected recipe.
            prefix = [r for r in records if r["step"] <= batch["end_step"]]
            result["recommendation_recipe"] = formal.pilot.committed_recipe(prefix, selected)
            progress["phase"] = "recommendation_retest"
            result["recommendation_retest"] = formal.fixed(
                repair / "recommendation-retest",
                result["recommendation_recipe"]["actions"],
                world_seed=cell["world_seed"],
                arm=cell["arm"],
                observation_seed=303,
                envelope=cell["batches"],
            )
    if len(result["source"]["batches"]) != cell["batches"]:
        result["retained_source_nonconformance"] = {
            "completed_batches": len(result["source"]["batches"]),
            "planned_batches": cell["batches"],
        }
    complete = (
        not result["failure"]
        and len(result["source"]["batches"]) == cell["batches"]
        and all(
            result["posttests"].get(s, {}).get("payload")
            and not result["posttests"][s].get("failure")
            for s in ("K1", "Q", "K2")
        )
        and result.get("recommendation_retest", {}).get("passed")
    )
    result["status"] = "completed" if complete else "failed"
    result["elapsed_s"] += time.monotonic() - started
    result["tokens"] = formal.pilot.token_accounting(result)
    write(repair / "result.json", result)
    atomic_write(folder / "result.json", result)
    return True


def drain_posttests(root, report, proxy):
    """Wait for the current executor to exit, then fill only transport-interrupted questions."""
    status_path = root / "posttest-repair-controller.json"
    if status_path.exists() and formal.controller_alive(read(status_path)):
        raise ValueError("A posttest continuation is already alive")
    state = {
        "pid": os.getpid(),
        "process_created": psutil.Process().create_time(),
        "stage": "waiting_for_source_queue",
        "repaired_sources": 0,
    }
    progress = {}
    stop = threading.Event()
    lock = threading.Lock()
    owns_queue = False

    def emit():
        with lock:
            state["epoch"] = time.time()
            atomic_write(status_path, state)
            if owns_queue:
                atomic_write(root / "controller-status.json", state)
                summary = formal.export(root, report)
                progress.update(
                    completed_chains=summary["completed_chains"],
                    planned_chains=30,
                    completed_posttests=summary["completed_posttests"],
                    planned_posttests=90,
                )
            print(json.dumps({**state, **progress}), flush=True)

    def heartbeat():
        while not stop.wait(30):
            emit()

    def wait(failures, stage):
        state.update(activity="retry_wait", retry_at_epoch=time.time() + retry_delay(failures))
        progress["phase"] = stage
        emit()
        deadline = time.monotonic() + retry_delay(failures)
        while time.monotonic() < deadline:
            time.sleep(min(30, max(0, deadline - time.monotonic())))
        state.update(activity="repairing_posttests", retry_at_epoch=None)
        emit()

    emit()
    thread = threading.Thread(target=heartbeat, daemon=True)
    thread.start()
    try:
        while formal.controller_alive(read(root / "controller-status.json")):
            time.sleep(30)
        previous = read(root / "controller-status.json")
        if previous.get("stage") not in ("completed", "ended_with_incomplete_chains"):
            raise ValueError("Source queue exited unexpectedly; no automatic ownership takeover")
        formal.verify_frozen(root)
        for name in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY"):
            os.environ[name] = proxy
        os.environ["NO_PROXY"] = "localhost,127.0.0.1,::1"
        owns_queue = True
        state.update(stage="sources", activity="repairing_posttests")
        emit()
        for cell in read(root / "design.json")["schedule"]:
            if repair_posttests(root, cell, progress, wait):
                state["repaired_sources"] += 1
                emit()
        summary = formal.export(root, report)
        state.update(
            stage="completed"
            if summary["completed_chains"] == 30
            else "ended_with_incomplete_chains",
            activity="finished",
        )
    except BaseException as exc:
        state.update(stage="interrupted", activity="halted", failure=str(exc))
        raise
    finally:
        stop.set()
        thread.join(timeout=5)
        emit()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--original", type=Path, required=True)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--proxy", required=True)
    parser.add_argument(
        "--phase", choices=("launch", "run", "queue-repairs", "repair-wait"), required=True
    )
    parser.add_argument("--retained-completed", type=int)
    parser.add_argument("--retry-cells", nargs="+")
    parser.add_argument("--recovery-index", type=int)
    parser.add_argument("--automatic", action="store_true")
    args = parser.parse_args()
    original, root, report = args.original.resolve(), args.root.resolve(), args.report.resolve()
    if args.phase == "repair-wait":
        drain_posttests(root, report, args.proxy)
        return
    if args.phase == "queue-repairs":
        status = root / "posttest-repair-controller.json"
        if status.exists() and formal.controller_alive(read(status)):
            raise ValueError("A posttest continuation is already alive")
        command = [
            "uv",
            "run",
            "--no-sync",
            "python",
            "-m",
            "scripts.resume_work_ii_c_completion",
            "--original",
            str(original),
            "--root",
            str(root),
            "--report",
            str(report),
            "--proxy",
            args.proxy,
            "--phase",
            "repair-wait",
        ]
        process = formal.detached_process(command, root / "posttest-repair-controller.log")
        print({"queued_posttest_repair_pid": process.pid}, flush=True)
        return
    if args.phase == "run":
        run(root, report, args.proxy, automatic=args.automatic)
        return
    if any(
        value is None for value in (args.retained_completed, args.retry_cells, args.recovery_index)
    ):
        parser.error("launch requires declared retained-completed, retry-cells and recovery-index")
    prepare(
        original,
        root,
        report,
        args.retained_completed,
        args.retry_cells,
        args.recovery_index,
        args.automatic,
    )
    command = [
        "uv",
        "run",
        "--no-sync",
        "python",
        "-m",
        "scripts.resume_work_ii_c_completion",
        "--original",
        str(original),
        "--root",
        str(root),
        "--report",
        str(report),
        "--proxy",
        args.proxy,
        "--phase",
        "run",
    ]
    if args.automatic:
        command.append("--automatic")
    process = formal.detached_process(command, root / "controller.log")
    receipt = {"pid": process.pid, "command": command, "started_epoch": time.time()}
    write(root / "controller-launch.json", receipt)
    print(receipt, flush=True)


if __name__ == "__main__":
    main()
