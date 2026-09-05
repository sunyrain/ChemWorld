#!/usr/bin/env python
"""Execute the fixed M3 context-portability block, retaining every attempted unit."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

import numpy as np

from chemworld.eval.work_ii_execution_mode import build_release_manifest, validate_release_manifest
from chemworld.eval.work_ii_factorial import (
    MODELS,
    compile_design,
    maximize,
    nearest_public_choice,
    public_packet,
    score_slots,
)
from chemworld.eval.work_ii_factorial_replication import source_schedule
from chemworld.eval.work_ii_m3_portability import (
    CONDITIONS,
    portability_protocol,
    recipient_prompt,
    recipient_schedule,
    summarize_portability,
)

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
from scripts.run_work_ii_factorial_replication import usage_sum  # noqa: E402

PROTOCOL = ROOT / "configs/benchmark/work_ii_m3_portability_20260905.json"
NOTE = "workstreams/flagship_tasks/WORK_II_M3_PORTABILITY_EXPERIMENT_NOTE.md"
DEFAULT_OUTPUT = ROOT / "runs/work-ii-m3-portability-20260905"
COST_KEYS = (
    "operation_count",
    "measurement_cost",
    "recipe_duration_s",
    "reagent_amount_mol",
    "wall_s",
    "cpu_s",
)


def load_source(protocol: dict) -> dict:
    binding = protocol["source_binding"]
    path = ROOT / binding["report"]
    if hashlib.sha256(path.read_bytes()).hexdigest() != binding["report_sha256"]:
        raise ValueError("bound M1 source report changed")
    report = read(path)
    if not report["execution_valid"] or not report["formal_result"]:
        raise ValueError("M3 requires the completed sealed M1 source block")
    scientific = report["scientific_source_data"]
    # Explicit projection drops old terminal candidates, scores and provider payloads.
    return {
        "artifacts": scientific["source_artifacts"],
        "public_packets": {
            key: public_packet(value, candidates=False)
            for key, value in scientific["public_packets"].items()
        },
        "reused_source_costs": {
            "public_physical": [
                row
                for row in report["physical_resources_by_role"]
                if row["role"] == "public_evidence"
            ],
            "source_generation": [
                row for row in report["provider_resources_by_stage"] if row["stage"] == "source"
            ],
            "scope": "Historical shared M1 acquisition/generation costs; not newly incurred. "
            "F was reused, not recomputed; its original fitting CPU was not separately measured.",
        },
    }


def freeze(root: Path) -> dict:
    protocol = read(PROTOCOL)
    binding = read(ROOT / "configs/current.json")["work_ii"]["w2_72_m1_replication"]
    if protocol != portability_protocol(read(ROOT / binding["protocol"]), binding):
        raise ValueError("protocol differs from declared outcome-blind design/current M1 binding")
    source = load_source(protocol)
    expected = {state["state_id"] for state in source_schedule(protocol)}
    if set(source["artifacts"]) != expected:
        raise ValueError("sealed M1 source-state denominator differs")
    for world in protocol["worlds"]:
        packet = compile_design(protocol, world["task"])
        original = source["public_packets"][world["cluster_id"]]
        for row, old in zip(packet["evidence"], original["evidence"], strict=True):
            if any(row[key] != old[key] for key in ("id", "xy", "controls", "action_plan")):
                raise ValueError("source and target physical controls no longer match")
    surface = {
        Path(__file__).relative_to(ROOT).as_posix(),
        PROTOCOL.relative_to(ROOT).as_posix(),
        binding["protocol"],
        binding["report"],
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
    seal(root / "schedule.json", recipient_schedule(protocol))
    seal(root / "source.json", source)
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
    if protocol != read(PROTOCOL) or read(root / "schedule.json") != recipient_schedule(protocol):
        raise ValueError("frozen protocol/schedule changed")
    if read(root / "source.json") != load_source(protocol):
        raise ValueError("retained M1 source projection changed")
    return protocol


def prepare(root: Path) -> dict:
    if (root / "physical.json").exists():
        return read(root / "physical.json")
    protocol = check_frozen(root)
    source, progress = read(root / "source.json"), Progress(root)
    receipts, private, packets, stop_reason = [], {}, {}, None
    for world in protocol["worlds"]:
        cluster, task = world["cluster_id"], world["task"]
        packet = compile_design(protocol, task)
        packet["evidence"] = source["public_packets"][cluster]["evidence"]
        local = {
            **protocol,
            "world_seed": world["world_seed"],
            "noise_namespace": protocol["noise_namespace"] + "/" + cluster,
        }
        private[cluster] = {}
        for index, row in enumerate(packet["candidates"]):
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
        packets[cluster] = public_packet(packet, candidates=True)
    if not stop_reason:
        for cluster, packet in packets.items():
            path = root / "public" / f"{cluster}.json"
            if path.exists():
                if read(path) != packet:
                    raise ValueError("packet changed on resume")
            else:
                seal(path, packet)
        if not (root / "private_scores.json").exists():
            seal(root / "private_scores.json", private)
    result = {
        "scheduled": protocol["physical_execution_count"],
        "completed": sum(row["status"] == "completed" for row in receipts),
        "status": "failed" if stop_reason else "completed",
        "stop_reason": stop_reason,
        "receipts": receipts,
    }
    seal(root / "physical.json", result)
    return result


def run_provider_block(root: Path) -> dict:
    if (root / "selections.json").exists():
        return read(root / "selections.json")
    protocol = check_frozen(root)
    source, physical = read(root / "source.json"), read(root / "physical.json")
    calls, slots, threads, controls = [], [], set(), []
    stop_reason, progress = physical["stop_reason"], Progress(root)
    for state in recipient_schedule(protocol):
        cluster, condition = state["cluster_id"], state["condition"]
        law = source["artifacts"][state["state_id"]].get(condition)
        blocked = condition in ("L", "F") and law is None
        prompt_bytes = None
        if stop_reason or blocked:
            receipt = {
                "call_id": state["call_id"],
                "status": "not_attempted",
                "usage": {},
                "failure_type": stop_reason or "missing_source_artifact",
            }
        else:
            packet = read(root / "public" / f"{cluster}.json")
            prompt = recipient_prompt(packet, condition, law)
            prompt_bytes = len(prompt.encode("utf-8"))
            receipt = provider_call(
                root,
                state["call_id"],
                state["model"],
                "decision",
                packet,
                law,
                progress,
                len(calls),
                total=protocol["provider_call_opportunities"],
                provider_override=protocol["providers"][state["model"]],
                prompt_override=prompt,
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
        calls.append({**receipt, **state, "prompt_bytes": prompt_bytes})
        slots.append(
            {
                **state,
                "status": receipt["status"],
                "candidate_id": receipt["final_payload"]["candidate_id"]
                if receipt["status"] == "completed"
                else None,
                "failure_type": receipt.get("failure_type"),
            }
        )
        progress.emit(
            "recipient",
            len(calls),
            protocol["provider_call_opportunities"],
            call_id=state["call_id"],
            status=receipt["status"],
        )
    if physical["status"] == "completed":
        for state in source_schedule(protocol):
            packet = read(root / "public" / f"{state['cluster_id']}.json")
            for kind in ("L", "F"):
                law = source["artifacts"][state["state_id"]][kind]
                choice, failure = None, "missing_source_artifact"
                if law is not None:
                    try:
                        choice, failure = maximize(law, packet["candidates"]), None
                    except (ValueError, OverflowError):
                        failure = "nonfinite_prediction"
                controls.append(
                    {
                        **{
                            key: state[key]
                            for key in ("state_id", "cluster_id", "task", "model", "repeat")
                        },
                        "condition": kind + "-X",
                        "candidate_id": choice,
                        "status": "completed" if choice else "blocked",
                        "failure_type": failure,
                    }
                )
        for world in protocol["worlds"]:
            packet = read(root / "public" / f"{world['cluster_id']}.json")
            controls.append(
                {
                    "cluster_id": world["cluster_id"],
                    "task": world["task"],
                    "condition": "nearest",
                    "status": "completed",
                    "candidate_id": nearest_public_choice(packet),
                }
            )
    result = {"calls": calls, "slots": slots, "controls": controls, "stop_reason": stop_reason}
    seal(root / "selections.json", result)  # No new candidate scores have been loaded.
    return result


def analyze(root: Path) -> dict:
    if (root / "summary.json").exists():
        return read(root / "summary.json")
    selections = read(root / "selections.json")
    protocol, physical, source = (
        read(root / name) for name in ("protocol.json", "physical.json", "source.json")
    )
    truth = read(root / "private_scores.json") if physical["status"] == "completed" else {}
    rows, controls, baselines = [], [], []
    for world in protocol["worlds"]:
        cluster = world["cluster_id"]
        selected = [row for row in selections["slots"] if row["cluster_id"] == cluster]
        if truth:
            rows.extend(score_slots(selected, truth[cluster]))
            controls.extend(
                score_slots(
                    [row for row in selections["controls"] if row["cluster_id"] == cluster],
                    truth[cluster],
                )
            )
            baselines.append(
                {
                    "cluster_id": cluster,
                    "task": world["task"],
                    "uniform_random_expected_regret": max(truth[cluster].values())
                    - float(np.mean(list(truth[cluster].values()))),
                }
            )
        else:
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
    valid = physical["status"] == "completed" and not selections["stop_reason"]
    calls = selections["calls"]
    resources = []
    for model in MODELS:
        for condition in CONDITIONS:
            selected = [
                row for row in calls if row["model"] == model and row["condition"] == condition
            ]
            resources.append(
                {
                    "model": model,
                    "condition": condition,
                    "scheduled": len(selected),
                    "completed": sum(row["status"] == "completed" for row in selected),
                    "wall_s": sum(row.get("elapsed_s", 0) for row in selected),
                    "usage": usage_sum(selected),
                    "prompt_bytes": sum(row.get("prompt_bytes") or 0 for row in selected),
                    "prompt_available": sum(
                        row.get("prompt_bytes") is not None for row in selected
                    ),
                }
            )
    failures = []
    for level, records, identity in (
        ("physical", physical["receipts"], "id"),
        ("provider", calls, "call_id"),
        ("condition", rows, "call_id"),
        ("deterministic_control", controls, "condition"),
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
            for row in rows:
                if (
                    row["model"] != model
                    or row["condition"] != kind
                    or row["status"] != "completed"
                ):
                    continue
                match = next(
                    (
                        control
                        for control in controls
                        if control.get("state_id") == row["state_id"]
                        and control["condition"] == kind + "-X"
                        and control["status"] == "completed"
                    ),
                    None,
                )
                if match:
                    eligible += 1
                    agree += row["candidate_id"] == match["candidate_id"]
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
    attempted = [row for row in calls if row["status"] != "not_attempted"]
    report = {
        "schema_version": "work-ii-m3-portability-summary-1",
        "experiment_note": NOTE,
        "formal_result": valid,
        "execution_valid": valid,
        "source_commit": release["tested_commit"],
        "execution_surface": release["execution_surface"],
        "source_binding": protocol["source_binding"],
        "independent_world_clusters": len(protocol["worlds"]),
        "additional_independent_worlds": 0,
        "reused_source_states": len(source["artifacts"]),
        "recipient_measurements": 0,
        "physical_scheduled": protocol["physical_execution_count"],
        "physical_completed": physical["completed"],
        "exact_replay_completed": sum(
            row.get("replay", {}).get("verified", False) for row in physical["receipts"]
        ),
        "provider_opportunities": len(calls),
        "provider_attempted": len(attempted),
        "provider_completed": sum(row["status"] == "completed" for row in calls),
        "condition_scheduled": len(rows),
        "condition_completed": sum(row["status"] == "completed" for row in rows),
        "provider_usage": usage_sum(calls),
        "provider_resources": resources,
        "provider_usage_coverage": {
            "attempted": len(attempted),
            "with_input_and_output_usage": sum(
                all(key in row.get("usage", {}) for key in ("input_tokens", "output_tokens"))
                for row in attempted
            ),
        },
        "provider_wall_s": sum(row.get("elapsed_s", 0) for row in calls),
        "physical_costs": {
            key: sum(row.get(key, 0) for row in physical["receipts"]) for key in COST_KEYS
        },
        "reused_source_costs": source["reused_source_costs"],
        "statistics": summarize_portability(rows, protocol) if valid else None,
        "slots": rows,
        "deterministic_controls": controls,
        "random_baselines": baselines,
        "agreement": agreement,
        "failures": failures,
        "stop_reason": selections["stop_reason"],
        "scientific_source_data": {
            "protocol": {key: value for key, value in protocol.items() if key != "providers"},
            "source_artifacts": source["artifacts"],
            "public_packets": {
                world["cluster_id"]: read(root / "public" / f"{world['cluster_id']}.json")
                for world in protocol["worlds"]
                if (root / "public" / f"{world['cluster_id']}.json").exists()
            },
            "candidate_scores_after_selections_sealed": truth,
            "provider_calls": [
                {
                    key: row[key]
                    for key in (
                        "call_id",
                        "state_id",
                        "cluster_id",
                        "model",
                        "repeat",
                        "condition",
                        "serial_position",
                        "status",
                        "usage",
                        "elapsed_s",
                        "prompt_bytes",
                        "failure_type",
                    )
                    if key in row
                }
                for row in calls
            ],
        },
        "interpretation": (
            "Same-world context portability on new candidate plans. None, raw evidence, "
            "model law and fitted law are separated in fresh tool-free recipients. Ten reused "
            "M1 worlds, not ten additional replication worlds. Quadratic is a representation "
            "family, not simulator truth. No mechanism-transfer, equivalence, "
            "experimental-savings or internal-mediation claim."
        ),
    }
    seal(root / "summary.json", report)
    (root / "summary.md").write_text(markdown_report(report), encoding="utf-8", newline="\n")
    return report


def markdown_report(report: dict) -> str:
    lines = [
        "# M3 information separation and context portability",
        "",
        report["interpretation"],
        "",
        f"Execution valid: {report['execution_valid']}. Physical: {report['physical_completed']}/"
        f"{report['physical_scheduled']}; exact replay: {report['exact_replay_completed']}/"
        f"{report['physical_scheduled']}; provider: {report['provider_completed']}/"
        f"{report['provider_opportunities']}; conditions: {report['condition_completed']}/"
        f"{report['condition_scheduled']}.",
        "",
    ]
    statistics = report["statistics"]
    if statistics:
        lines += ["| Prespecified regret contrast | Mean | Interval |", "| --- | ---: | --- |"]
        for row in statistics["contrasts"]:
            lo, hi = row["interval"]
            lines.append(
                f"| {row['contrast']} | {row['mean_difference']:.6f} | "
                f"{row['interval_level'] * 100:g}% [{lo:.6f}, {hi:.6f}] |"
            )
        lines += [
            "",
            "Negative differences favor the first arm. Primary material benefit supported: "
            + str(statistics["primary_material_benefit_supported"])
            + ".",
            "",
            statistics["inference_limit"],
            "",
            "| Model | Condition | Completed/scheduled | Mean regret | Near-optimal |",
            "| --- | --- | ---: | ---: | ---: |",
        ]
        for row in statistics["condition_summaries"]:
            lines.append(
                f"| {row['model']} | {row['condition']} | {row['completed']}/{row['scheduled']} "
                f"| {row['mean_failure_aware_regret']:.6f} | "
                f"{row['near_optimal_count']}/{row['scheduled']} |"
            )
        lines += ["", "| World | Primary L minus none | Completed pairs |", "| --- | ---: | ---: |"]
        for row in statistics["world_contrasts"]:
            if row["contrast"] == "L_minus_none":
                lines.append(
                    f"| {row['cluster_id']} | {row['mean_difference']:.6f} | "
                    f"{row['completed_pair_count']}/{row['nested_state_count']} |"
                )
    lines += [
        "",
        "| Model | Information | Calls | Wall seconds | Input | Output | Prompt bytes |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in report["provider_resources"]:
        lines.append(
            f"| {row['model']} | {row['condition']} | {row['completed']}/{row['scheduled']} | "
            f"{row['wall_s']:.1f} | {row['usage'].get('input_tokens', 'unknown')} | "
            f"{row['usage'].get('output_tokens', 'unknown')} | {row['prompt_bytes']} |"
        )
    lines += [
        "",
        "Provider output includes reasoning; cache is a subset of input. Missing usage is "
        "unknown. Physical CPU/wall includes replay; recipe resources count primary execution "
        "once. Reused M1 public experiments and source generation are historical shared costs, "
        "not new execution. The JSON records them separately. No currency estimate.",
        "",
        "All failures (empty means none):",
        "",
        "```json",
        json.dumps(report["failures"], ensure_ascii=False, indent=2),
        "```",
        "",
        "The JSON includes every slot, all six world contrasts, deterministic controls, "
        "agreement denominators, original artifacts, inputs and post-seal candidate scores. "
        "Raw provider events, session identities and credentials are excluded.",
        "",
    ]
    return "\n".join(lines)


def export_report(root: Path, destination: Path) -> dict:
    report = read(root / "summary.json")
    if destination.exists() and read(destination) != report:
        raise ValueError("refusing to replace a different scientific result")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    destination.with_suffix(".md").write_text(
        markdown_report(report), encoding="utf-8", newline="\n"
    )
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=("freeze", "prepare", "run", "analyze", "export"))
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    root = args.output.resolve()
    if args.stage == "freeze":
        result = freeze(root)
    elif args.stage == "prepare":
        full = prepare(root)
        result = {key: full[key] for key in ("status", "scheduled", "completed", "stop_reason")}
    else:
        if args.stage == "run":
            run_provider_block(root)
        if args.stage == "export":
            if not args.report:
                parser.error("export requires --report")
            report = export_report(root, args.report.resolve())
        else:
            report = analyze(root)
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
