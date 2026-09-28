"""Bounded six-session EQ-P comparison; reuse the existing scientific protocol."""

# ruff: noqa: RUF001

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from statistics import fmean

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

MODELS = ("gpt-5.6-luna", "gpt-5.6-terra", "gpt-5.5")
ARMS = ("Opaque", "Aligned")
WORLD = "EQ-W01"
DILUTE = ("Q03", "Q08", "Q09")
REPORT = ROOT / "workstreams/flagship_tasks/reports/eq-six-model-comparison-20260927"


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def emit(value):
    print(json.dumps(value, ensure_ascii=False), flush=True)


def jobs():
    return [{"model": m, "arm": a, "cell_id": f"{WORLD}--{a}"} for m in MODELS for a in ARMS]


def folder(root, job):
    return root / "conditions" / job["model"] / "sources" / job["cell_id"]


def probe(model, root):
    from chemworld.providers.codex_subscription import CodexSubscriptionClient

    started = time.monotonic()
    client = CodexSubscriptionClient(
        model=model, reasoning_effort="medium", timeout_s=120, max_attempts=1
    )
    answer = client.complete_json(
        system_prompt="Return the requested JSON. Do not use tools.",
        user_prompt='Return {"ok":true}.',
        max_tokens=128,
        output_schema={
            "type": "object",
            "properties": {"ok": {"type": "boolean"}},
            "required": ["ok"],
            "additionalProperties": False,
        },
    )
    result = {
        "model": model,
        "valid": answer.payload == {"ok": True},
        "elapsed_s": time.monotonic() - started,
    }
    write(root / "compatibility" / f"{model}.json", result)
    emit(result)
    if not result["valid"]:
        raise RuntimeError("Provider compatibility probe returned an invalid payload")


def cell(root, model, arm):
    from scripts.run_work_ii_eq_rx_p_cross_model_v0_1 import run_eq_cell

    result = run_eq_cell(
        root / "conditions" / model,
        {"model": model, "reasoning_effort": "medium"},
        f"{WORLD}--{arm}",
    )
    emit(
        {"model": model, "arm": arm, "status": result["status"], "batches": len(result["batches"])}
    )


def progress(root, processes, started, phase):
    rows = []
    for job, process, _ in processes:
        target = folder(root, job) if phase == "research" else None
        row = {**job, "process_returncode": process.poll()}
        if target is not None:
            trajectory = target / "trajectory.jsonl"
            operations = batches = 0
            if trajectory.exists():
                for line in trajectory.read_text(encoding="utf-8").splitlines():
                    try:
                        record = json.loads(line)
                    except ValueError:
                        continue
                    operations += 1
                    if (
                        record.get("instrument") == "final_assay"
                        and record.get("transaction_status") == "committed"
                    ):
                        batches += 1
            sealed = [p.stem for p in (target / "sealed").glob("*.json")]
            row.update(operations=operations, batches=batches, sealed=sealed)
            if (target / "RESULT.json").exists():
                result = read(target / "RESULT.json")
                row.update(status=result["status"], batches=len(result.get("batches", [])))
        rows.append(row)
    elapsed = time.monotonic() - started
    completed = sum(r["process_returncode"] is not None for r in rows)
    batches = sum(r.get("batches", 0) for r in rows)
    payload = {
        "phase": phase,
        "elapsed_s": round(elapsed),
        "terminal_sessions": completed,
        "total_sessions": len(rows),
        "completed_batches": batches,
        "total_batches": 72 if phase == "research" else 0,
        "batches_per_min": round(60 * batches / elapsed, 2) if elapsed else 0,
        "eta_s": round(elapsed * (72 - batches) / batches)
        if phase == "research" and 0 < batches < 72
        else None,
        "cells": rows,
    }
    write(root / "progress.json", payload)
    emit(payload)


def execute(root, selected, mode):
    processes = []
    started = time.monotonic()
    for job in selected:
        log_path = root / "logs" / f"{mode}-{job['model']}-{job.get('arm', 'probe')}.log"
        log_path.parent.mkdir(parents=True, exist_ok=True)
        log = log_path.open("w", encoding="utf-8")
        command = [
            "uv",
            "run",
            "--no-sync",
            "python",
            str(Path(__file__).resolve()),
            "--mode",
            mode,
            "--output",
            str(root),
            "--model",
            job["model"],
        ]
        if mode == "cell":
            command += ["--arm", job["arm"]]
        options = {"creationflags": subprocess.CREATE_NO_WINDOW} if os.name == "nt" else {}
        process = subprocess.Popen(
            command,
            cwd=ROOT,
            stdout=log,
            stderr=subprocess.STDOUT,
            env=os.environ.copy(),
            **options,
        )
        processes.append((job, process, log))
    phase = "research" if mode == "cell" else "compatibility"
    try:
        progress(root, processes, started, phase)
        while any(p.poll() is None for _, p, _ in processes):
            time.sleep(30)
            progress(root, processes, started, phase)
    finally:
        for _, _, log in processes:
            log.close()
    return all(p.returncode == 0 for _, p, _ in processes)


def reference_truth(root, config):
    import scripts.run_work_ii_eq_bounded_equilibrium_v2 as eq

    target = root / "shared-reference" / "truth.json"
    if target.exists():
        return read(target)
    queries = eq.queries(config)
    actions = [action for q in queries for action in q["actions"]]
    world = eq.world_by_id(config, WORLD)
    truth = {q["query_id"]: [] for q in queries}
    for repeat in range(1, 6):
        result = eq.reference_run(
            root / "shared-reference" / f"repeat-{repeat:02d}",
            actions,
            config=config,
            world=world,
            batches=12,
            observation_seed=eq.deterministic_seed("eq-reference-truth-v1", WORLD, repeat),
            observation_namespace=f"work-ii-eq-truth-{WORLD.lower()}-r{repeat:02d}",
        )
        if (
            result["failure"]
            or result["rollbacks"]
            or len(result["batches"]) != 12
            or result["exact_replay"].get("verified") is not True
        ):
            raise RuntimeError("Shared reference execution failed")
        for q, batch in zip(queries, result["batches"], strict=True):
            truth[q["query_id"]].append({m: float(batch["metrics"][m]) for m in eq.METRICS})
        emit({"phase": "reference", "completed": repeat * 12, "total": 60})
    write(target, truth)
    return truth


def summarize(root, config):
    import scripts.run_work_ii_eq_bounded_equilibrium_v2 as eq

    truth = reference_truth(root, config)
    rows = []
    for job in jobs():
        path = folder(root, job) / "RESULT.json"
        if not path.exists():
            rows.append({**job, "status": "missing_result", "prediction_metrics": None})
            continue
        result = read(path)
        row = {
            **job,
            "status": result["status"],
            "source_status": result["source_status"],
            "source_batches": len(result.get("batches", [])),
            "operations": result.get("operations"),
            "replay_verified": result.get("exact_replay", {}).get("verified"),
            "sealed_stages": {
                s: v.get("valid") for s, v in result.get("posttest_validation", {}).items()
            },
            "elapsed_s": result.get("elapsed_s"),
            "failure": result.get("failure"),
            "prediction_metrics": None,
        }
        payload = result.get("posttests", {}).get("Q", {}).get("payload")
        if eq.validate_posttest("Q", payload, eq.queries(config))["valid"]:
            predictions = {p["query_id"]: p for p in payload["predictions"]}
            groups = {}
            for name, query_ids in [
                ("other_nine", [q for q in truth if q not in DILUTE]),
                ("dilute_three", list(DILUTE)),
            ]:
                details = {}
                for metric in eq.METRICS:
                    errors, covered, widths = [], [], []
                    for qid in query_ids:
                        p = predictions[qid]["metrics"][metric]
                        actual = [r[metric] for r in truth[qid]]
                        errors.append(abs(p["estimate"] - fmean(actual)))
                        covered.extend(p["lower80"] <= y <= p["upper80"] for y in actual)
                        widths.append(p["upper80"] - p["lower80"])
                    details[metric] = {
                        "mae": fmean(errors),
                        "coverage80": fmean(covered),
                        "width80": fmean(widths),
                    }
                groups[name] = {
                    "query_count": len(query_ids),
                    "macro_mae": fmean(v["mae"] for v in details.values()),
                    "coverage80": fmean(v["coverage80"] for v in details.values()),
                    "responses": details,
                }
            row["prediction_metrics"] = groups
            row["most_dilute_dissociation"] = {
                "prediction": predictions["Q08"]["metrics"]["acid_dissociation_fraction"],
                "reference_mean": fmean(r["acid_dissociation_fraction"] for r in truth["Q08"]),
            }
        rows.append(row)
    comparisons = []
    for model in MODELS:
        arms = {r["arm"]: r for r in rows if r["model"] == model}
        if all(arms[a]["prediction_metrics"] is not None for a in ARMS):
            delta = {
                group: arms["Aligned"]["prediction_metrics"][group]["macro_mae"]
                - arms["Opaque"]["prediction_metrics"][group]["macro_mae"]
                for group in ("other_nine", "dilute_three")
            }
            comparisons.append(
                {
                    "model": model,
                    "aligned_minus_opaque": delta,
                    "reversal": delta["other_nine"] < 0 < delta["dilute_three"],
                }
            )
    summary = {
        "status": "complete"
        if all(r["status"] == "completed" for r in rows)
        else "terminal_with_failures",
        "evidence_scope": "development single-world six-session comparison",
        "planned_sessions": 6,
        "completed_sessions": sum(r["status"] == "completed" for r in rows),
        "planned_source_batches": 72,
        "completed_source_batches": sum(r.get("source_batches", 0) for r in rows),
        "reasoning_effort": "medium",
        "world": WORLD,
        "dilute_queries": DILUTE,
        "cells": rows,
        "matched_comparisons": comparisons,
    }
    write(root / "summary.json", summary)
    write(REPORT / "summary.json", summary)
    lines = [
        "# 六会话跨模型平衡对照",
        "",
        "同一世界，三个模型均使用 medium，各自完成 Opaque/Aligned 自主研究。",
        "",
        f"完成 {summary['completed_sessions']}/6 会话、"
        f"{summary['completed_source_batches']}/72 来源批次；所有失败保留。",
        "",
        "| 模型 | 信息条件 | 状态 | 其余九题 MAE | 最稀三题 MAE | 最稀三题覆盖率 |",
        "|---|---|---|---:|---:|---:|",
    ]
    for row in rows:
        metrics = row["prediction_metrics"]
        values = (
            [
                f"{metrics['other_nine']['macro_mae']:.5f}",
                f"{metrics['dilute_three']['macro_mae']:.5f}",
                f"{metrics['dilute_three']['coverage80']:.1%}",
            ]
            if metrics
            else ["缺失"] * 3
        )
        lines.append("| " + " | ".join([row["model"], row["arm"], row["status"], *values]) + " |")
    lines.extend(
        [
            "",
            "每个模型/信息条件只有一次独立研究；查询与响应不是独立重复，不据此作稳定模型排名。",
            "",
        ]
    )
    (REPORT / "REPORT_ZH.md").write_text("\n".join(lines), encoding="utf-8")
    emit(
        {
            "phase": "finished",
            "status": summary["status"],
            "completed_sessions": summary["completed_sessions"],
            "report": str(REPORT),
        }
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=("coordinate", "cell", "probe", "summarize", "check"),
        default="coordinate",
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--model", choices=MODELS)
    parser.add_argument("--arm", choices=ARMS)
    args = parser.parse_args()
    root = args.output.resolve()
    if args.mode == "probe":
        probe(args.model, root)
        return
    if args.mode == "cell":
        cell(root, args.model, args.arm)
        return
    import scripts.run_work_ii_eq_bounded_equilibrium_v2 as eq

    config = eq.load_config()
    schedule = eq.validate_design(config)["schedule"]
    assert all(any(r["cell_id"] == job["cell_id"] for r in schedule) for job in jobs())
    if args.mode == "check":
        emit(
            {
                "sessions": jobs(),
                "batches": 72,
                "posttests": list(eq.POSTTEST_STAGES),
                "dilute_queries": DILUTE,
            }
        )
        return
    if args.mode == "summarize":
        summarize(root, config)
        return
    root.mkdir(parents=True, exist_ok=False)
    write(
        root / "design.json",
        {
            "sessions": jobs(),
            "model_effort": "medium",
            "dilute_queries": DILUTE,
            "resolved_config": config,
            "source_budget": config["source_resource_card"],
            "posttest_stages": list(eq.POSTTEST_STAGES),
            "scope": "development bounded replication; no automatic expansion",
        },
    )
    if not execute(root, [{"model": m} for m in MODELS], "probe"):
        raise RuntimeError(
            "Compatibility probe failed; no scientific sessions started. "
            "Inspect retained probe logs."
        )
    execute(root, jobs(), "cell")
    summarize(root, config)


if __name__ == "__main__":
    main()
