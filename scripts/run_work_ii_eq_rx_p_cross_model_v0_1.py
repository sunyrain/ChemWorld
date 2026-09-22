#!/usr/bin/env python3
"""Run the frozen EQ-P/RX-P cross-model block with an isolated global worker pool."""
# ruff: noqa: E501

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import subprocess
import sys
import threading
import time
from collections.abc import Mapping, Sequence
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

CONFIG = ROOT / "configs/benchmark/work_ii_eq_rx_p_cross_model_v0.1.json"
PROXY_KEYS = ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "http_proxy", "https_proxy", "all_proxy")


def read(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def digest(payload: Any) -> str:
    body = json.dumps(payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def file_sha256(path: Path) -> str:
    checksum = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            checksum.update(block)
    return checksum.hexdigest()


def provider(condition: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "id": "chemworld_openai_https",
        "name": "OpenAI",
        "model": str(condition["model"]),
        "reasoning_effort": str(condition["reasoning_effort"]),
        "auth_mode": "chatgpt_subscription_cached_login",
        "wire_api": "responses",
    }


def configure_proxy(config: Mapping[str, Any]) -> None:
    value = str(config["execution"]["proxy"])
    for key in PROXY_KEYS:
        os.environ[key] = value
    for key in ("NO_PROXY", "no_proxy"):
        os.environ[key] = "127.0.0.1,localhost"


def validate_bindings(config: Mapping[str, Any]) -> None:
    for relative, expected in config["bindings"].items():
        path = (ROOT / relative).resolve()
        if ROOT.resolve() not in path.parents or not path.is_file():
            raise RuntimeError(f"missing immutable source binding: {relative}")
        if file_sha256(path) != expected:
            raise RuntimeError(f"immutable source binding changed: {relative}")


def load_schedules() -> tuple[dict[str, Any], dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    import scripts.run_work_ii_eq_bounded_equilibrium_v2 as eq
    import scripts.run_work_ii_rx_ps_five_world_dual_goal as rx

    eq_config = eq.load_config()
    eq_schedule = [copy.deepcopy(row) for row in eq.validate_design(eq_config)["schedule"]]
    rx_config = read(rx.CONFIG)
    rx_validated = rx.validate_design(rx_config)
    rx_schedule = [copy.deepcopy(row) for row in rx_validated["schedule"] if row["locus"] == "P"]
    if len(eq_schedule) != 15 or len(rx_schedule) != 30:
        raise RuntimeError("cross-model source denominator changed")
    return eq_config, rx_config, eq_schedule, rx_schedule


def build_jobs(
    conditions: Sequence[Mapping[str, Any]],
    eq_schedule: Sequence[Mapping[str, Any]],
    rx_schedule: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    jobs: list[dict[str, Any]] = []
    for world_index in range(1, 6):
        world_suffix = f"W{world_index:02d}"
        rows = [
            *({"task": "eq-p", "cell": cell} for cell in eq_schedule if cell["world_id"].endswith(world_suffix)),
            *({"task": "rx-p", "cell": cell} for cell in rx_schedule if cell["world_id"].endswith(world_suffix)),
        ]
        for row in rows:
            for condition in conditions:
                jobs.append(
                    {
                        "condition_id": condition["condition_id"],
                        "model": condition["model"],
                        "reasoning_effort": condition["reasoning_effort"],
                        "task": row["task"],
                        "cell_id": row["cell"]["cell_id"],
                        "world_id": row["cell"]["world_id"],
                    }
                )
    if len(jobs) != 225 or len({(row["condition_id"], row["task"], row["cell_id"]) for row in jobs}) != 225:
        raise RuntimeError("cross-model schedule is not 225 unique sessions")
    return jobs


def result_path(root: Path, job: Mapping[str, Any]) -> Path:
    name = "RESULT.json" if job["task"] == "eq-p" else "result.json"
    return root / "conditions" / str(job["condition_id"]) / str(job["task"]) / "sources" / str(job["cell_id"]) / name


def result_is_complete(root: Path, job: Mapping[str, Any]) -> bool:
    path = result_path(root, job)
    if not path.is_file():
        return False
    row = read(path)
    expected = ("K1", "Q", "K2", "EQS") if job["task"] == "eq-p" else ("K1", "Q", "K2")
    return bool(
        row.get("status") == "completed"
        and row.get("source_status") == "completed"
        and len(row.get("batches", [])) == 12
        and row.get("exact_replay", {}).get("verified") is True
        and row.get("posttest_chain_sealed") is True
        and all(row.get("posttest_validation", {}).get(stage, {}).get("valid") is True for stage in expected)
    )


def _override_agent_reasoning(original: type[Any], effort: str) -> type[Any]:
    class CrossModelAgent(original):  # type: ignore[misc, valid-type]
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            super().__init__(*args, **kwargs)
            self.reasoning_effort = effort

    CrossModelAgent.__name__ = f"CrossModel{original.__name__}"
    return CrossModelAgent


def run_eq_cell(root: Path, condition: Mapping[str, Any], cell_id: str) -> dict[str, Any]:
    import scripts.run_work_ii_eq_bounded_equilibrium_v2 as eq

    configured = provider(condition)
    eq.PROVIDER = configured
    eq.v1.PROVIDER = configured
    eq.shared.PROVIDER = configured
    eq.provider_shared.PROVIDER = configured
    eq.EqFreeResearchAgent = _override_agent_reasoning(eq.EqFreeResearchAgent, str(condition["reasoning_effort"]))
    config = eq.load_config()
    validated = eq.validate_design(config)
    eq.configure_provider_helpers(config)
    cell = next((row for row in validated["schedule"] if row["cell_id"] == cell_id), None)
    if cell is None:
        raise ValueError(f"unknown EQ-P cell: {cell_id}")
    progress: dict[str, Any] = {}
    return eq.run_cell(root, config, cell, progress, threading.Lock())


def run_rx_cell(root: Path, condition: Mapping[str, Any], cell_id: str) -> dict[str, Any]:
    import scripts.run_work_ii_rx_ps_five_world_dual_goal as rx

    configured = provider(condition)
    rx.PROVIDER = configured
    rx.shared.PROVIDER = configured
    rx.rx_canary.PROVIDER = configured
    rx.rx_canary.RxFreeResearchAgent = _override_agent_reasoning(
        rx.rx_canary.RxFreeResearchAgent, str(condition["reasoning_effort"])
    )
    rx.configure_shared_helpers()
    config = read(rx.CONFIG)
    validated = rx.validate_design(config)
    cell = next(
        (row for row in validated["schedule"] if row["cell_id"] == cell_id and row["locus"] == "P"),
        None,
    )
    if cell is None:
        raise ValueError(f"unknown RX-P cell: {cell_id}")
    return rx.run_cell(
        root,
        cell,
        p_package=validated["p_package"],
        s_contract=validated["s_contract"],
        config=config,
        progress={},
    )


def run_one_cell(args: argparse.Namespace) -> None:
    config = read(CONFIG)
    validate_bindings(config)
    configure_proxy(config)
    condition = next(
        (row for row in config["conditions"] if row["condition_id"] == args.condition), None
    )
    if condition is None:
        raise ValueError(f"unknown provider condition: {args.condition}")
    root = args.output.resolve() / "conditions" / args.condition / args.task
    if args.task == "eq-p":
        result = run_eq_cell(root, condition, args.cell)
    else:
        result = run_rx_cell(root, condition, args.cell)
    print(
        json.dumps(
            {
                "stage": "cell_exit",
                "condition": args.condition,
                "task": args.task,
                "cell_id": args.cell,
                "status": result.get("status"),
                "batches": len(result.get("batches", [])),
            }
        ),
        flush=True,
    )


def write_design(
    root: Path,
    config: Mapping[str, Any],
    jobs: Sequence[Mapping[str, Any]],
    eq_config: Mapping[str, Any],
    rx_config: Mapping[str, Any],
) -> None:
    design = {
        "schema_version": "work-ii-eq-rx-p-cross-model-run-design-0.1",
        "study_config": copy.deepcopy(config),
        "study_config_sha256": file_sha256(CONFIG),
        "source_commit": os.environ.get("CHEMWORLD_SOURCE_COMMIT", "unavailable"),
        "provider_availability_resolved_before_chemworld": True,
        "schedule": list(jobs),
        "schedule_sha256": digest(jobs),
        "eq_resolved_config_sha256": digest(eq_config),
        "rx_config_sha256": digest(rx_config),
        "truth_embargo": "Shared reference truth is generated only after 225 complete sealed chains.",
    }
    path = root / "design.json"
    if path.exists() and read(path) != design:
        raise RuntimeError("existing run design differs from the frozen design")
    write(path, design)
    for condition in config["conditions"]:
        condition_root = root / "conditions" / condition["condition_id"]
        write(
            condition_root / "provider.json",
            {
                "condition_id": condition["condition_id"],
                "provider": provider(condition),
                "eq_p_sessions": 15,
                "rx_p_sessions": 30,
            },
        )


def run_job(root: Path, job: Mapping[str, Any], active: dict[str, Any], lock: threading.Lock) -> dict[str, Any]:
    key = f"{job['condition_id']}::{job['task']}::{job['cell_id']}"
    if result_is_complete(root, job):
        return {**dict(job), "returncode": 0, "already_complete": True}
    path = result_path(root, job)
    if path.parent.exists():
        return {**dict(job), "returncode": 99, "failure": "incomplete_write_once_cell_exists"}
    log_path = root / "logs" / str(job["condition_id"]) / str(job["task"]) / f"{job['cell_id']}.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    command = [
        sys.executable,
        str(Path(__file__).resolve()),
        "--mode",
        "cell",
        "--output",
        str(root),
        "--condition",
        str(job["condition_id"]),
        "--task",
        str(job["task"]),
        "--cell",
        str(job["cell_id"]),
    ]
    started = time.monotonic()
    with lock:
        active[key] = {"started": time.time(), "pid": None}
    with log_path.open("a", encoding="utf-8") as log:
        process = subprocess.Popen(
            command,
            cwd=ROOT,
            stdout=log,
            stderr=subprocess.STDOUT,
            env=os.environ.copy(),
            text=True,
        )
        with lock:
            active[key]["pid"] = process.pid
        returncode = process.wait()
    with lock:
        active.pop(key, None)
    return {
        **dict(job),
        "returncode": returncode,
        "elapsed_s": time.monotonic() - started,
        "complete": result_is_complete(root, job),
        "log": str(log_path),
    }


def matrix_summary(root: Path, jobs: Sequence[Mapping[str, Any]], phase: str) -> dict[str, Any]:
    rows = []
    for job in jobs:
        path = result_path(root, job)
        status = None
        batches = 0
        if path.is_file():
            result = read(path)
            status = result.get("status")
            batches = len(result.get("batches", []))
        rows.append({**dict(job), "result_exists": path.is_file(), "complete": result_is_complete(root, job), "status": status, "batches": batches})
    summary = {
        "schema_version": "work-ii-eq-rx-p-cross-model-summary-0.1",
        "phase": phase,
        "planned_sessions": 225,
        "complete_sessions": sum(row["complete"] for row in rows),
        "attempted_sessions": sum(row["result_exists"] for row in rows),
        "completed_source_batches": sum(row["batches"] for row in rows),
        "by_condition": {
            condition: {
                "complete": sum(row["complete"] for row in rows if row["condition_id"] == condition),
                "attempted": sum(row["result_exists"] for row in rows if row["condition_id"] == condition),
                "batches": sum(row["batches"] for row in rows if row["condition_id"] == condition),
            }
            for condition in sorted({str(row["condition_id"]) for row in rows})
        },
        "nonconforming": [row for row in rows if row["result_exists"] and not row["complete"]],
    }
    write(root / "summary.json", summary)
    return summary


def execute(root: Path, all_jobs: Sequence[Mapping[str, Any]], selected: Sequence[Mapping[str, Any]], workers: int, phase: str) -> None:
    if not 1 <= workers <= 8:
        raise ValueError("workers must remain within the qualified global range 1..8")
    active: dict[str, Any] = {}
    lock = threading.Lock()
    stop = threading.Event()
    started = time.monotonic()

    def heartbeat() -> None:
        while not stop.wait(30):
            summary = matrix_summary(root, all_jobs, phase)
            with lock:
                snapshot = copy.deepcopy(active)
            done = sum(result_is_complete(root, job) for job in selected)
            elapsed = time.monotonic() - started
            print(
                json.dumps(
                    {
                        "stage": phase,
                        "selected_complete": done,
                        "selected_total": len(selected),
                        "matrix_complete": summary["complete_sessions"],
                        "workers": workers,
                        "elapsed_s": round(elapsed),
                        "eta_s": round(elapsed / done * (len(selected) - done)) if done else None,
                        "active": snapshot,
                    }
                ),
                flush=True,
            )

    thread = threading.Thread(target=heartbeat, daemon=True)
    thread.start()
    failures: list[dict[str, Any]] = []
    try:
        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = {executor.submit(run_job, root, job, active, lock): job for job in selected}
            for future in as_completed(futures):
                outcome = future.result()
                if outcome.get("returncode") != 0 or not outcome.get("complete", outcome.get("already_complete", False)):
                    failures.append(outcome)
                summary = matrix_summary(root, all_jobs, phase)
                print(
                    json.dumps(
                        {
                            "stage": "cell_complete",
                            "condition": outcome["condition_id"],
                            "task": outcome["task"],
                            "cell_id": outcome["cell_id"],
                            "returncode": outcome["returncode"],
                            "complete": outcome.get("complete", outcome.get("already_complete", False)),
                            "matrix_complete": summary["complete_sessions"],
                        }
                    ),
                    flush=True,
                )
    finally:
        stop.set()
        thread.join(timeout=2)
    if failures:
        write(root / f"{phase}-failures.json", failures)
        raise RuntimeError(f"{phase} retained {len(failures)} nonconforming cell(s)")


def rx_p_truth(root: Path, config: Mapping[str, Any]) -> dict[str, Any]:
    import scripts.run_work_ii_rx_ps_five_world_dual_goal as rx

    rx.configure_shared_helpers()
    truth: dict[str, Any] = {}
    for world_id, world_seed in rx.WORLDS:
        truth[world_id] = {}
        for query in rx.queries(config, "P"):
            repeats = []
            for replicate in range(1, 6):
                seed = rx.deterministic_seed("rx-ps-q-v1", world_id, "P", query["query_id"], f"r{replicate:02d}")
                report = rx._reference_run(
                    root / world_id / query["query_id"] / f"replicate-{replicate:02d}",
                    query["actions"],
                    world_seed=world_seed,
                    observation_seed=seed,
                    observation_namespace=f"work-ii-rx-ps-truth-{world_id.lower()}-p-{query['query_id'].lower()}-r{replicate:02d}",
                )
                if report["failure"] or len(report["batches"]) != 1 or report["rollbacks"] or report["exact_replay"].get("verified") is not True:
                    raise RuntimeError(f"RX-P reference truth failed: {world_id}/{query['query_id']}/r{replicate}")
                repeats.append({metric: float(report["batches"][0]["metrics"][metric]) for metric in rx.METRICS})
            truth[world_id][query["query_id"]] = repeats
    write(root / "truth.json", truth)
    return truth


def finalize(root: Path, config: Mapping[str, Any], jobs: Sequence[Mapping[str, Any]], eq_config: Mapping[str, Any], rx_config: Mapping[str, Any]) -> None:
    if not all(result_is_complete(root, job) for job in jobs):
        raise RuntimeError("reference truth remains embargoed until all 225 chains complete")
    import scripts.run_work_ii_eq_bounded_equilibrium_v2 as eq
    import scripts.run_work_ii_rx_ps_five_world_dual_goal as rx

    eq_truth_root = root / "shared-reference-truth" / "eq-p"
    eq_truth = read(eq_truth_root / "truth.json") if (eq_truth_root / "truth.json").is_file() else eq.generate_truth(eq_truth_root, eq_config)
    rx_truth_root = root / "shared-reference-truth" / "rx-p"
    rx_truth = read(rx_truth_root / "truth.json") if (rx_truth_root / "truth.json").is_file() else rx_p_truth(rx_truth_root, rx_config)
    for condition in config["conditions"]:
        condition_id = condition["condition_id"]
        eq_root = root / "conditions" / condition_id / "eq-p"
        rx_root = root / "conditions" / condition_id / "rx-p"
        for path in sorted((eq_root / "sources").glob("*/RESULT.json")):
            result = read(path)
            evaluation = eq.evaluate_predictions(result["posttests"]["Q"].get("payload"), eq.queries(eq_config), eq_truth[result["world_id"]])
            evaluation["eqs"] = eq.evaluate_eqs(
                result["posttests"]["EQS"].get("payload"),
                float(eq.world_by_id(eq_config, result["world_id"])["private_authoring"]["effective_pka"]),
            )
            write(eq_root / "evaluations" / f"{result['cell_id']}.json", evaluation)
        for path in sorted((rx_root / "sources").glob("*/result.json")):
            result = read(path)
            evaluation = rx.evaluate_predictions(result["posttests"]["Q"].get("payload"), rx.queries(rx_config, "P"), rx_truth[result["world_id"]])
            write(rx_root / "evaluations" / f"{result['cell_id']}.json", evaluation)

    final = matrix_summary(root, jobs, "complete")
    write(
        root / "completion.json",
        {
            "schema_version": "work-ii-eq-rx-p-cross-model-completion-0.1",
            "completed_epoch": time.time(),
            "source_sessions": final["complete_sessions"],
            "source_batches": final["completed_source_batches"],
            "shared_reference_executions": 600,
            "summary_sha256": digest(final),
        },
    )


def coordinate(args: argparse.Namespace) -> None:
    config = read(CONFIG)
    validate_bindings(config)
    configure_proxy(config)
    eq_config, rx_config, eq_schedule, rx_schedule = load_schedules()
    jobs = build_jobs(config["conditions"], eq_schedule, rx_schedule)
    root = args.output.resolve()
    root.mkdir(parents=True, exist_ok=True)
    write_design(root, config, jobs, eq_config, rx_config)
    canary = [job for job in jobs if job["world_id"].endswith("W01")]
    remaining = [job for job in jobs if not job["world_id"].endswith("W01")]
    if len(canary) != 45 or len(remaining) != 180:
        raise RuntimeError("canary/remaining split changed")
    if args.scope in {"canary", "auto"}:
        execute(root, jobs, canary, args.workers, "w01_canary")
        if not all(result_is_complete(root, job) for job in canary):
            raise RuntimeError("remaining matrix sealed because W01 canary did not pass")
    if args.scope in {"remaining", "auto"}:
        if not all(result_is_complete(root, job) for job in canary):
            raise RuntimeError("remaining matrix sealed until all 45 W01 canary chains pass")
        execute(root, jobs, remaining, args.workers, "w02_w05")
    if args.scope in {"finalize", "auto"}:
        finalize(root, config, jobs, eq_config, rx_config)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("coordinate", "cell"), default="coordinate")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--scope", choices=("canary", "remaining", "finalize", "auto"), default="auto")
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--condition")
    parser.add_argument("--task", choices=("eq-p", "rx-p"))
    parser.add_argument("--cell")
    args = parser.parse_args()
    if args.mode == "cell":
        if not args.condition or not args.task or not args.cell:
            parser.error("cell mode requires --condition, --task, and --cell")
        run_one_cell(args)
    else:
        coordinate(args)


if __name__ == "__main__":
    main()
