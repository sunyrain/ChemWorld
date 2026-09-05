#!/usr/bin/env python
"""Fixed M1 independent-world block; completed and interrupted attempts are retained."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np

from chemworld.eval.work_ii_execution_mode import build_release_manifest, validate_release_manifest
from chemworld.eval.work_ii_factorial import (
    MODELS,
    compile_design,
    design_matrix,
    fit_public_law,
    maximize,
    nearest_public_choice,
    public_packet,
    score_slots,
)
from chemworld.eval.work_ii_factorial_replication import source_schedule, summarize_factorial

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from scripts.run_work_ii_factorial import (  # noqa: E402
    Progress,
    execute_plan,
    provider_call,
    read,
    seal,
)

DEFAULT_OUTPUT = ROOT / "runs/work-ii-m1-replication-20260905"
PROTOCOL = ROOT / "configs/benchmark/work_ii_m1_replication_20260905.json"
NOTE = "workstreams/flagship_tasks/WORK_II_M1_REPLICATION_EXPERIMENT_NOTE.md"


def freeze(root: Path) -> dict:
    """One existing lightweight release manifest; no historical readiness dependencies."""
    protocol = read(PROTOCOL)
    for world in protocol["worlds"]:
        compile_design(protocol, world["task"])
    # Bind loaded execution modules, not manuscripts, tests or historical result/config trees.
    # Schema files cover the lazily imported task/trajectory validators.
    surface = {
        Path(__file__).relative_to(ROOT).as_posix(),
        PROTOCOL.relative_to(ROOT).as_posix(),
        "pyproject.toml",
        "uv.lock",
        "src/chemworld/schemas",
        "configs/providers/deepseek_v4_flash_models.json",
    }
    for module in tuple(sys.modules.values()):
        filename = getattr(module, "__file__", None)
        if filename:
            path = Path(filename).resolve()
            if path.is_relative_to(ROOT / "src/chemworld") or path.is_relative_to(ROOT / "scripts"):
                surface.add(path.relative_to(ROOT).as_posix())
    manifest = build_release_manifest(ROOT, execution_surface=sorted(surface))
    root.mkdir(parents=True, exist_ok=False)
    seal(root / "release.json", manifest)
    seal(root / "protocol.json", protocol)
    seal(root / "schedule.json", source_schedule(protocol))
    return {
        "status": "frozen",
        "source_commit": manifest["tested_commit"],
        "runtime_paths": len(surface),
    }


def check_frozen(root: Path) -> dict:
    errors = validate_release_manifest(ROOT, read(root / "release.json"))
    if errors:
        raise ValueError("; ".join(errors))
    protocol = read(root / "protocol.json")
    if protocol != read(PROTOCOL) or read(root / "schedule.json") != source_schedule(protocol):
        raise ValueError("frozen protocol/schedule changed")
    return protocol


def prepare(root: Path) -> dict:
    if (root / "physical.json").exists():
        return read(root / "physical.json")
    protocol = check_frozen(root)
    progress, receipts, private, packets = Progress(root), [], {}, {}
    stop_reason = None
    for world in protocol["worlds"]:
        cluster, task = world["cluster_id"], world["task"]
        packet = compile_design(protocol, task)
        local = {
            **protocol,
            "world_seed": world["world_seed"],
            "noise_namespace": protocol["noise_namespace"] + "/" + cluster,
        }
        private[cluster] = {}
        for index, row in enumerate(packet["evidence"] + packet["candidates"]):
            path = root / "physical" / cluster / row["id"]
            if (path / "receipt.json").exists():
                receipt = read(path / "receipt.json")
            elif path.exists():
                receipt = {
                    "task": task,
                    "id": row["id"],
                    "status": "interrupted",
                    "failure_type": "started_without_receipt_no_retry",
                }
                seal(path / "receipt.json", receipt)
            elif stop_reason:
                receipt = {
                    "task": task,
                    "id": row["id"],
                    "status": "not_attempted",
                    "failure_type": stop_reason,
                }
            else:
                receipt = execute_plan(local, task, row, path, index)
            receipts.append({**receipt, "cluster_id": cluster})
            if receipt["status"] == "completed":
                if index < len(packet["evidence"]):
                    row["score"] = receipt["score"]
                else:
                    private[cluster][row["id"]] = receipt["score"]
            else:
                stop_reason = "physical_or_replay_failure"
            progress.emit(
                "physical+replay",
                len(receipts),
                protocol["physical_execution_count"],
                cluster_id=cluster,
                unit=row["id"],
                status=receipt["status"],
            )
        packets[cluster] = packet
    completed = sum(row["status"] == "completed" for row in receipts)
    if not stop_reason:
        for cluster, packet in packets.items():
            path = root / "public" / f"{cluster}.json"
            projected = public_packet(packet, candidates=True)
            if path.exists():
                if read(path) != projected:
                    raise ValueError("public packet differs from retained physical receipts")
            else:
                seal(path, projected)
        if not (root / "private_scores.json").exists():
            seal(root / "private_scores.json", private)
    result = {
        "scheduled": protocol["physical_execution_count"],
        "completed": completed,
        "status": "completed" if not stop_reason else "failed",
        "stop_reason": stop_reason,
        "receipts": receipts,
    }
    seal(root / "physical.json", result)
    return result


def run_provider_block(root: Path) -> dict:
    if (root / "selections.json").exists():
        return read(root / "selections.json")
    protocol = check_frozen(root)
    physical = read(root / "physical.json")
    progress = Progress(root)
    calls, slots, artifacts, nearest, fitted_cache = [], [], {}, {}, {}
    threads = set()
    stop_reason = physical["stop_reason"]

    def call(
        state: dict,
        suffix: str,
        stage: str,
        packet: dict | None,
        law: list | None,
        blocked: bool = False,
    ) -> dict:
        nonlocal stop_reason
        call_id = state["state_id"] + "--" + suffix
        if stop_reason or blocked:
            receipt = {
                "call_id": call_id,
                "status": "not_attempted",
                "usage": {},
                "failure_type": stop_reason or "missing_source_artifact",
            }
        else:
            receipt = provider_call(
                root,
                call_id,
                state["model"],
                stage,
                packet,
                law,
                progress,
                len(calls),
                total=protocol["provider_call_opportunities"],
                provider_override=protocol["providers"][state["model"]],
            )
            thread = receipt.get("thread_id")
            if receipt.get("protocol_failure") or receipt.get("tool_event_count", 0):
                stop_reason = receipt.get("protocol_failure", "forbidden_tool_use")
            elif thread and thread in threads:
                stop_reason = "reused_session_identity"
            elif receipt["status"] == "completed" and not thread:
                stop_reason = "missing_session_identity"
            if stop_reason:
                receipt = {**receipt, "status": "protocol_failed", "failure_type": stop_reason}
            if thread:
                threads.add(thread)
        receipt = {
            **receipt,
            "state_id": state["state_id"],
            "cluster_id": state["cluster_id"],
            "model": state["model"],
            "stage": stage,
        }
        calls.append(receipt)
        progress.emit(
            "provider",
            len(calls),
            protocol["provider_call_opportunities"],
            call_id=call_id,
            status=receipt["status"],
        )
        return receipt

    for state in source_schedule(protocol):
        cluster = state["cluster_id"]
        packet = read(root / "public" / f"{cluster}.json") if not stop_reason else None
        if packet and cluster not in fitted_cache:
            fitted_cache[cluster] = fit_public_law(packet["evidence"], ridge=protocol["ridge"])
            nearest[cluster] = nearest_public_choice(packet)
        fitted = fitted_cache.get(cluster)
        source = call(state, "source", "source", packet, None)
        law = source["final_payload"]["coefficients"] if source["status"] == "completed" else None
        artifacts[state["state_id"]] = {"L": law, "F": fitted}
        metadata = {
            key: state[key] for key in ("state_id", "cluster_id", "task", "model", "repeat")
        }
        for kind in state["decision_order"]:
            coefficients = artifacts[state["state_id"]][kind]
            decision = call(
                state, kind + "-A", "decision", packet, coefficients, blocked=coefficients is None
            )
            slots.append(
                {
                    **metadata,
                    "condition": kind + "-A",
                    "status": decision["status"],
                    "candidate_id": decision["final_payload"]["candidate_id"]
                    if decision["status"] == "completed"
                    else None,
                    "failure_type": decision.get("failure_type"),
                }
            )
            choice, failure = (
                None,
                stop_reason or ("missing_source_artifact" if coefficients is None else None),
            )
            if not failure:
                try:
                    with np.errstate(over="ignore", invalid="ignore"):
                        choice = maximize(coefficients, packet["candidates"])
                except (ValueError, OverflowError) as error:
                    failure = str(error)
            slots.append(
                {
                    **metadata,
                    "condition": kind + "-X",
                    "status": "completed" if choice else "blocked",
                    "candidate_id": choice,
                    "failure_type": failure,
                }
            )
    result = {
        "slots": slots,
        "calls": calls,
        "artifacts": artifacts,
        "nearest_choices": nearest,
        "stop_reason": stop_reason,
    }
    seal(root / "selections.json", result)  # hidden outcomes are read only by analyze, below
    return result


def usage_sum(calls: list[dict]) -> dict:
    result = Counter()
    for call in calls:
        result.update(
            {
                key: value
                for key, value in call.get("usage", {}).items()
                if isinstance(value, int | float)
            }
        )
    return dict(result)


def analyze(root: Path) -> dict:
    if (root / "summary.json").exists():
        return read(root / "summary.json")
    selections = read(root / "selections.json")  # required before any truth access
    protocol, physical = read(root / "protocol.json"), read(root / "physical.json")
    truth = read(root / "private_scores.json") if physical["status"] == "completed" else {}
    rows, baselines, metrics = [], [], []
    for world in protocol["worlds"]:
        cluster = world["cluster_id"]
        selected = [row for row in selections["slots"] if row["cluster_id"] == cluster]
        if not truth:
            rows.extend(
                {
                    **row,
                    "raw_regret": None,
                    "failure_aware_regret": 1.0,
                    "near_optimal": False,
                    "top1": False,
                }
                for row in selected
            )
            continue
        rows.extend(score_slots(selected, truth[cluster]))
        best = max(truth[cluster].values())
        choice = selections["nearest_choices"].get(cluster)
        baselines.append(
            {
                "cluster_id": cluster,
                "task": world["task"],
                "nearest_public_regret": best - truth[cluster][choice] if choice else None,
                "uniform_random_expected_regret": best
                - float(np.mean(list(truth[cluster].values()))),
                "candidate_score_min": min(truth[cluster].values()),
                "candidate_score_max": best,
            }
        )
        packet = read(root / "public" / f"{cluster}.json")
        actual = np.array([truth[cluster][row["id"]] for row in packet["candidates"]])
        for state in source_schedule(protocol):
            if state["cluster_id"] != cluster:
                continue
            for kind, law in selections["artifacts"][state["state_id"]].items():
                error, status = None, "missing_artifact"
                if law is not None:
                    try:
                        with np.errstate(over="ignore", invalid="ignore"):
                            value = float(
                                np.mean(np.abs(design_matrix(packet["candidates"]) @ law - actual))
                            )
                        error = value if np.isfinite(value) else None
                    except (ValueError, OverflowError):
                        error = None
                    status = "completed" if error is not None else "nonfinite_prediction_error"
                metrics.append(
                    {
                        key: state[key]
                        for key in ("state_id", "cluster_id", "task", "model", "repeat")
                    }
                    | {"artifact": kind, "candidate_mae": error, "status": status}
                )
    valid = physical["status"] == "completed" and not selections["stop_reason"]
    statistics = summarize_factorial(rows, protocol) if valid else None
    calls = selections["calls"]
    resources = []
    for model in MODELS:
        for stage in ("source", "decision"):
            selected = [row for row in calls if row["model"] == model and row["stage"] == stage]
            resources.append(
                {
                    "model": model,
                    "stage": stage,
                    "scheduled": len(selected),
                    "completed": sum(row["status"] == "completed" for row in selected),
                    "wall_s": sum(row.get("elapsed_s", 0) for row in selected),
                    "usage": usage_sum(selected),
                }
            )
    failures = []
    for level, records, identity in (
        ("physical", physical["receipts"], "id"),
        ("provider", calls, "call_id"),
        ("condition", rows, "condition"),
    ):
        failures.extend(
            {
                "level": level,
                "unit": row[identity],
                "cluster_id": row["cluster_id"],
                "state_id": row.get("state_id"),
                "status": row["status"],
                "failure_type": row.get("failure_type", row["status"]),
            }
            for row in records
            if row["status"] != "completed"
        )
    agreement = []
    for model in MODELS:
        for kind in ("L", "F"):
            eligible, agree = 0, 0
            for state in source_schedule(protocol):
                if state["model"] != model:
                    continue
                pair = {
                    row["condition"]: row for row in rows if row["state_id"] == state["state_id"]
                }
                left, right = pair[kind + "-A"], pair[kind + "-X"]
                if left["status"] == right["status"] == "completed":
                    eligible += 1
                    agree += left["candidate_id"] == right["candidate_id"]
            agreement.append(
                {
                    "model": model,
                    "artifact": kind,
                    "scheduled": 20,
                    "eligible": eligible,
                    "agree": agree,
                }
            )
    release = read(root / "release.json")
    result = {
        "schema_version": "work-ii-m1-replication-summary-1",
        "experiment_note": NOTE,
        "formal_result": valid,
        "execution_valid": valid,
        "source_commit": release["tested_commit"],
        "execution_surface": release["execution_surface"],
        "protocol": PROTOCOL.relative_to(ROOT).as_posix(),
        "independent_world_clusters": len(protocol["worlds"]),
        "physical_scheduled": protocol["physical_execution_count"],
        "physical_completed": physical["completed"],
        "exact_replay_completed": sum(
            row.get("replay", {}).get("verified", False) for row in physical["receipts"]
        ),
        "provider_opportunities": len(calls),
        "provider_attempted": sum(row["status"] != "not_attempted" for row in calls),
        "provider_completed": sum(row["status"] == "completed" for row in calls),
        "condition_scheduled": len(rows),
        "condition_completed": sum(row["status"] == "completed" for row in rows),
        "provider_usage": usage_sum(calls),
        "provider_resources_by_stage": resources,
        "provider_wall_s": sum(row.get("elapsed_s", 0) for row in calls),
        "physical_costs": {
            key: sum(row.get(key, 0) for row in physical["receipts"])
            for key in (
                "operation_count",
                "measurement_cost",
                "recipe_duration_s",
                "reagent_amount_mol",
                "wall_s",
                "cpu_s",
            )
        },
        "statistics": statistics,
        "slots": rows,
        "baselines": baselines,
        "artifact_metrics": metrics,
        "agreement": agreement,
        "failures": failures,
        "stop_reason": selections["stop_reason"],
        "interpretation": "Fixed local quadratic response surfaces in two task families. "
        "Ten world clusters; repeated models/sessions are nested. Candidate outcomes are "
        "single keyed-noise measurements. Fit plus argmax is a classical baseline. "
        "No topology-transfer, experimental-savings or internal-mediation claim.",
    }
    seal(root / "summary.json", result)
    write_markdown(root / "summary.md", result)
    return result


def write_markdown(path: Path, report: dict) -> None:
    lines = [
        "# M1 independent-world replication",
        "",
        report["interpretation"],
        "",
        f"Execution valid: {report['execution_valid']}. "
        f"Physical: {report['physical_completed']}/200; "
        f"exact replay: {report['exact_replay_completed']}/200; provider: "
        f"{report['provider_completed']}/120; conditions: {report['condition_completed']}/160.",
        "",
    ]
    if report["statistics"]:
        lines += [
            "| Contrast (negative favors first condition) | Mean regret difference | Interval |",
            "| --- | ---: | --- |",
        ]
        for row in report["statistics"]["contrasts"]:
            lo, hi = row["interval"]
            lines.append(
                f"| {row['contrast']} | {row['mean_difference']:.6f} | "
                f"{row['interval_level'] * 100:g}% [{lo:.6f}, {hi:.6f}] |"
            )
        lines += [
            "",
            "Material primary benefit supported: "
            + str(report["statistics"]["primary_material_benefit_supported"])
            + ".",
            "",
            report["statistics"]["inference_limit"],
            "",
            "| Model | Condition | Completed/scheduled | Failure-aware regret | Near-optimal |",
            "| --- | --- | ---: | ---: | ---: |",
        ]
        for row in report["statistics"]["condition_summaries"]:
            lines.append(
                f"| {row['model']} | {row['condition']} | {row['completed']}/{row['scheduled']} "
                f"| {row['mean_failure_aware_regret']:.6f} | "
                f"{row['near_optimal_count']}/{row['scheduled']} |"
            )
    lines += [
        "",
        "| Model | Stage | Completed/scheduled | Wall seconds | Input | Output |",
        "| --- | --- | ---: | ---: | ---: | ---: |",
    ]
    for row in report["provider_resources_by_stage"]:
        lines.append(
            f"| {row['model']} | {row['stage']} | {row['completed']}/{row['scheduled']} "
            f"| {row['wall_s']:.1f} | {row['usage'].get('input_tokens', 0)} "
            f"| {row['usage'].get('output_tokens', 0)} |"
        )
    lines += [
        "",
        "Output includes reasoning; cached input is a subset. Physics CPU/wall includes "
        "exact replay; recipe resources count primary executions once. No currency estimate.",
        "",
        "Failures (all levels retained):",
        "",
        "```json",
        json.dumps(report["failures"], ensure_ascii=False, indent=2),
        "```",
        "",
        "The JSON companion contains all 160 slots, world contrasts, artifact errors, "
        "agreement denominators, baselines and resource totals.",
        "",
    ]
    with path.open("x", encoding="utf-8") as handle:
        handle.write("\n".join(lines))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=("freeze", "prepare", "run", "analyze"))
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    if args.report and args.stage != "analyze":
        parser.error("--report is only available for analyze")
    root = args.output.resolve()
    if args.stage == "freeze":
        result = freeze(root)
    elif args.stage == "prepare":
        full = prepare(root)
        result = {key: full[key] for key in ("status", "scheduled", "completed", "stop_reason")}
    else:
        if args.stage == "run":
            run_provider_block(root)
        report = analyze(root)
        if args.report:
            seal(args.report.resolve(), report)
            write_markdown(args.report.resolve().with_suffix(".md"), report)
        result = {
            key: report[key]
            for key in (
                "execution_valid",
                "provider_completed",
                "condition_completed",
                "provider_usage",
                "stop_reason",
            )
        }
    print(json.dumps(result, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
