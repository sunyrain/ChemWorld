"""Fixed six-case notebook replication; see WORK_II_CASE_NOTEBOOK_RERUN_20261013.md."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import threading
import time
from pathlib import Path

from chemworld.agents.campaign_notebook import with_notebook

ROOT = Path(__file__).resolve().parents[1]
CASES = [
    {
        "id": "EC-discovery",
        "system": "EC",
        "cell": "EC-W01-B12-discovery-E-Opaque",
        "goal": "discovery",
        "model": "gpt-5.6-sol",
        "batches": 12,
    },
    {
        "id": "EC-optimization",
        "system": "EC",
        "cell": "EC-W01-B12-optimization-E-Opaque",
        "goal": "optimization",
        "model": "gpt-5.6-sol",
        "batches": 12,
    },
    {
        "id": "EQ-Sol",
        "system": "EQ",
        "cell": "EQ-W01--Opaque",
        "model": "gpt-5.6-sol",
        "batches": 12,
    },
    {
        "id": "EQ-Astra",
        "system": "EQ",
        "cell": "EQ-W03--MisIndexed",
        "model": "gpt-6-astra",
        "batches": 12,
    },
    {
        "id": "C-12",
        "system": "C",
        "cell": "C-W05-B12-E-Aligned",
        "model": "gpt-5.6-sol",
        "batches": 12,
    },
    {
        "id": "C-24",
        "system": "C",
        "cell": "C-W05-B24-E-Aligned",
        "model": "gpt-5.6-sol",
        "batches": 24,
    },
]


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write(path, data):
    from chemworld.agents.experiment_documents import _atomic_write_text

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    _atomic_write_text(path, json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def emit(data):
    print(json.dumps(data, ensure_ascii=True), flush=True)


def prepare(root):
    from scripts import run_work_ii_eq_bounded_equilibrium_v2 as eq

    binding = read(ROOT / "configs/current.json")["work_ii"]["w2_132_ec_pa_english_matrix"]
    originals = {
        case["id"]: ROOT / binding["run_root"] / "sources" / case["cell"] / "design.json"
        for case in CASES
        if case["system"] == "EC"
    }
    originals["C"] = ROOT / "runs/formal/work-ii-c-five-world-20260920-v3-auto/design.json"
    designs = {key: read(path) for key, path in originals.items()}
    assert designs["C"]["protocol"] == "c-quality-recovery-formal-v3-en"
    config = eq.load_config()
    valid = eq.validate_design(config)
    assert {c["cell"] for c in CASES if c["system"] == "EQ"} <= {
        c["cell_id"] for c in valid["schedule"]
    }
    for case in CASES[:2]:
        d = designs[case["id"]]
        assert d["batches_per_source"] == 12 and d["world_config"]["world_id"] == "EC-W01"
    root.mkdir(parents=True, exist_ok=False)
    write(
        root / "design.json",
        {
            "cases": CASES,
            "source_batches": 84,
            "reference_batches": 144,
            "reasoning_effort": "medium",
            "mode": "development-replication",
            "source_commit": subprocess.check_output(
                ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
            ).strip(),
            "originals": {
                k: {"path": str(p), "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
                for k, p in originals.items()
            },
            "eq_config": config,
            "notebook": "current versioned hypothesis role; source stage only",
            "retries": 0,
        },
    )
    for key, value in designs.items():
        write(root / "inputs" / f"{key}.json", value)
    for case in CASES:
        if case["system"] == "EC":
            write(root / case["id"] / "design.json", designs[case["id"]])
    c_design = designs["C"]
    c_design["schedule"] = [
        r
        for r in c_design["schedule"]
        if r["id"] in {c["cell"] for c in CASES if c["system"] == "C"}
    ]
    c_design.update(
        planned_sources=2,
        planned_batches=36,
        planned_posttests=6,
        planned_retests=2,
        mode="development-notebook-replication",
        automatic_retries=0,
    )
    write(root / "C" / "design.json", c_design)


def references(root, progress):
    from scripts import run_work_ii_c_formal as c
    from scripts import run_work_ii_ec_pa_matrix as ec_matrix
    from scripts import run_work_ii_eq_bounded_equilibrium_v2 as eq

    ec_design = read(root / "inputs/EC-discovery.json")
    assert ec_design["queries"] == ec_matrix.ec.queries()
    ec_ref = ec_matrix.prepare_reference(
        "EC", ec_design["world_config"], root / "references/EC", progress
    )
    progress.update(reference_batches=12)
    c_design = read(root / "C/design.json")
    c_ref = c.fixed(
        root / "C/qualification/W05/queries",
        [a for q in c_design["queries"] for a in q["actions"]],
        world_seed=4,
        batches=12,
    )
    if not c_ref["passed"]:
        raise RuntimeError("C reference execution/replay failed")
    progress.update(reference_batches=24)
    config = read(root / "design.json")["eq_config"]
    truth = {}
    query_rows = eq.queries(config)
    actions = [a for q in query_rows for a in q["actions"]]
    for world_id in ("EQ-W01", "EQ-W03"):
        truth[world_id] = {q["query_id"]: [] for q in query_rows}
        for repeat in range(1, 6):
            progress.update(stage="reference", unit=f"{world_id}/repeat-{repeat}")
            result = eq.reference_run(
                root / "references" / world_id / f"repeat-{repeat}",
                actions,
                config=config,
                world=eq.world_by_id(config, world_id),
                batches=12,
                observation_seed=eq.deterministic_seed("eq-reference-truth-v1", world_id, repeat),
                observation_namespace=f"work-ii-eq-truth-{world_id.lower()}-r{repeat:02d}",
            )
            if (
                result["failure"]
                or result["rollbacks"]
                or len(result["batches"]) != 12
                or not result["exact_replay"]["verified"]
            ):
                raise RuntimeError(f"EQ reference failed: {world_id}/{repeat}")
            for query, batch in zip(query_rows, result["batches"], strict=True):
                truth[world_id][query["query_id"]].append(
                    {m: batch["metrics"][m] for m in eq.METRICS}
                )
            progress["reference_batches"] += 12
            emit(progress)
    write(root / "references/truth.json", {"EC": ec_ref["truth"], "EQ": truth})
    write(root / "references/complete.json", {"completed_batches": 144, "replay_verified": True})


def execute_case(root, case, progress):
    if case["system"] == "EC":
        from scripts import run_work_ii_ec_dual_goal_trial as ec

        ec.FreeResearchAgent = with_notebook(ec.FreeResearchAgent)
        return ec.run_cell(
            root / case["id"],
            case["goal"],
            "E",
            "Opaque",
            read(root / "references/truth.json")["EC"],
            progress,
        )
    if case["system"] == "C":
        from scripts import run_work_ii_c_formal as c

        c.FormalCAgent = with_notebook(c.FormalCAgent)
        cell = next(
            row for row in read(root / "C/design.json")["schedule"] if row["id"] == case["cell"]
        )
        return c.source(root / "C", cell, progress)
    from scripts import run_work_ii_eq_bounded_equilibrium_v2 as eq
    from scripts.run_work_ii_eq_rx_p_cross_model_v0_1 import provider

    condition = {"model": case["model"], "reasoning_effort": "medium"}
    configured = provider(condition)
    eq.PROVIDER = eq.v1.PROVIDER = eq.shared.PROVIDER = eq.provider_shared.PROVIDER = configured
    eq.EqFreeResearchAgent = with_notebook(eq.EqFreeResearchAgent)
    config = read(root / "design.json")["eq_config"]
    cell = next(
        row for row in eq.validate_design(config)["schedule"] if row["cell_id"] == case["cell"]
    )
    eq.configure_provider_helpers(config)
    result = eq.run_cell(root / case["id"], config, cell, progress, threading.Lock())
    truth = read(root / "references/truth.json")["EQ"][cell["world_id"]]
    result["prediction_evaluation"] = eq.evaluate_predictions(
        result["posttests"].get("Q", {}).get("payload"), eq.queries(config), truth
    )
    return result


def case_folder(root, case):
    if case["system"] == "EC":
        return root / case["id"] / f"{case['goal']}-E-Opaque"
    if case["system"] == "C":
        return root / "C/sources" / case["cell"]
    return root / case["id"] / "sources" / case["cell"]


def live(root, case):
    folder = case_folder(root, case)
    path = folder / "trajectory.jsonl"
    rows = []
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                break
    return {
        "operations": len(rows),
        "batches": sum(
            r.get("instrument") == "final_assay" and r.get("transaction_status") == "committed"
            for r in rows
        ),
    }


def summarize(root):
    rows = []
    for case in CASES:
        path = root / "results" / f"{case['id']}.json"
        result = read(path) if path.exists() else {}
        source = result.get("source", result)
        folder = case_folder(root, case)
        note_dir = folder / ("private/source/notebook" if case["system"] == "EQ" else "notebook")
        # EQ's original engine keeps its private data in .private/ (resolved below).
        matches = (
            list(folder.glob("**/notebook/experiment_documents/model_owned_notebook.md"))
            if folder.exists()
            else []
        )
        if matches:
            note_dir = matches[0].parent.parent
        calls = []
        audit = note_dir / "notebook-calls.jsonl"
        if audit.exists():
            calls = [
                json.loads(line) for line in audit.read_text(encoding="utf-8").splitlines() if line
            ]
        usage = result.get("source_usage", source.get("usage", {}))
        rows.append(
            {
                **case,
                "status": result.get("status", "not_started"),
                "failure": result.get("failure"),
                "completed_batches": len(source.get("batches", [])),
                "operations": source.get("operations", 0),
                "exact_replay": source.get("exact_replay"),
                "rollbacks": source.get("rollbacks", []),
                "sealed_posttests": sum(
                    bool(v.get("payload")) and not v.get("failure")
                    for v in result.get("posttests", {}).values()
                ),
                "notebook_writes": sum(
                    r["tool"] in {"notebook_write", "notebook_restore"} and not r["error"]
                    for r in calls
                ),
                "notebook_reads": sum(
                    r["tool"] == "notebook_read" and not r["error"] for r in calls
                ),
                "notebook_tool_errors": sum(r["error"] for r in calls),
                "notebook_directory": str(note_dir.relative_to(root)) if matches else None,
                "source_usage": usage,
                "elapsed_s": result.get("elapsed_s"),
                "prediction_evaluation": result.get("prediction_evaluation"),
                "recommendation": result.get("recommendation", result.get("evidentiary_anchor")),
                "recommendation_retest": result.get("recommendation_retest"),
                "posttest_usage": {
                    k: v.get("usage", v.get("method_resources"))
                    for k, v in result.get("posttests", {}).items()
                },
            }
        )
    summary = {
        "mode": "development-replication",
        "planned_sources": 6,
        "planned_source_batches": 84,
        "planned_posttests": 20,
        "planned_reference_batches": 144,
        "terminal_sources": sum(r["status"] not in {"not_started", "running"} for r in rows),
        "completed_sources": sum(r["status"] == "completed" for r in rows),
        "completed_batches": sum(r["completed_batches"] for r in rows),
        "cases": rows,
    }
    write(root / "summary.json", summary)
    return summary


def coordinate(root):
    prepare(root)
    started = time.monotonic()
    for unit in ["references", *(c["id"] for c in CASES)]:
        log = root / "logs" / f"{unit}.log"
        log.parent.mkdir(exist_ok=True)
        with log.open("w", encoding="utf-8") as stream:
            options = {"creationflags": subprocess.CREATE_NO_WINDOW} if os.name == "nt" else {}
            process = subprocess.Popen(
                [
                    sys.executable,
                    "-m",
                    "scripts.run_paper_case_notebooks",
                    "--root",
                    str(root),
                    "--unit",
                    unit,
                ],
                cwd=ROOT,
                stdout=stream,
                stderr=subprocess.STDOUT,
                **options,
            )
            while process.poll() is None:
                summary = summarize(root)
                current = next((c for c in CASES if c["id"] == unit), None)
                counts = live(root, current) if current else {}
                completed = summary["completed_batches"] + counts.get("batches", 0)
                elapsed = time.monotonic() - started
                emit(
                    {
                        "stage": unit,
                        "terminal_sources": summary["terminal_sources"],
                        "total_sources": 6,
                        "completed_batches": completed,
                        "total_batches": 84,
                        "elapsed_s": round(elapsed),
                        "batches_per_minute": 60 * completed / elapsed,
                        "eta_s": elapsed / completed * (84 - completed) if completed else None,
                        "active": counts,
                        "log_bytes": log.stat().st_size,
                    }
                )
                time.sleep(30)
        if process.returncode:
            write(
                root / "block-stop.json",
                {
                    "unit": unit,
                    "exit_code": process.returncode,
                    "reason": "execution or reference/replay defect; no retry",
                },
            )
            break
    emit(summarize(root))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--unit", choices=["references", *(c["id"] for c in CASES)])
    parser.add_argument("--summarize", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    if args.summarize:
        emit(summarize(root))
    elif args.unit:
        progress = {"stage": args.unit, "reference_batches": 0}
        stop = threading.Event()

        def heartbeat():
            while not stop.wait(30):
                emit(progress)

        thread = threading.Thread(target=heartbeat, daemon=True)
        thread.start()
        try:
            if args.unit == "references":
                references(root, progress)
            else:
                case = next(c for c in CASES if c["id"] == args.unit)
                result = execute_case(root, case, progress)
                write(root / "results" / f"{case['id']}.json", result)
                source = result.get("source", result)
                if (
                    source.get("operations", 0)
                    and source.get("exact_replay", {}).get("verified") is not True
                ):
                    raise RuntimeError("source replay defect; stop block")
        finally:
            stop.set()
    else:
        coordinate(root)


if __name__ == "__main__":
    main()
