#!/usr/bin/env python
"""Execute the fixed M0/M1 development block; resume never retries a started unit."""

from __future__ import annotations

import argparse
import json
import sys
import tempfile
import time
from collections import Counter
from pathlib import Path
from typing import Any

import numpy as np

from chemworld.data.logging import load_jsonl
from chemworld.eval.runner import run_agent
from chemworld.eval.verify import verify_records
from chemworld.eval.work_ii_factorial import (
    CONDITIONS,
    MODELS,
    TASKS,
    compile_design,
    design_matrix,
    development_protocol,
    fit_public_law,
    maximize,
    nearest_public_choice,
    output_schema,
    participant_prompt,
    public_packet,
    score_slots,
    validate_payload,
)
from chemworld.eval.work_ii_truth import _FrozenTruthReplayAgent, _truth_metrics
from chemworld.tasks import get_task

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from scripts.run_work_ii_study_b import (  # noqa: E402
    _initial_command,
    _launch_turn,
    _prepare_codex_home,
)

DEFAULT_OUTPUT = ROOT / "runs/development/work-ii-m0-m1-20260905"
PROVIDER_CONFIGS = {
    "deepseek": ROOT / "workstreams/flagship_tasks/reports/"
    "work-ii-w2-26-deepseek-runtime-configs-v0.1/a_p--electrochemical-conversion--r10.json",
    "gpt": ROOT / "configs/benchmark/work_ii_c2_gpt56_sol_medium_runtime_v0.1/"
    "a_p--electrochemical-conversion--r10.json",
}


def read(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def seal(path: Path, value: Any) -> None:
    """Write once, including failures and attempt markers; no outcome replacement."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2, allow_nan=False)
        handle.write("\n")


class Progress:
    def __init__(self, root: Path):
        self.path = root / "progress.jsonl"
        self.started = time.perf_counter()

    def emit(self, stage: str, completed: int, total: int, **extra: Any) -> None:
        elapsed = time.perf_counter() - self.started
        rate = completed / elapsed if elapsed else 0
        row = {
            "stage": stage,
            "completed": completed,
            "total": total,
            "elapsed_s": round(elapsed, 1),
            "units_per_minute": round(rate * 60, 3),
            "eta_s": round((total - completed) / rate, 1) if rate else None,
            **extra,
        }
        line = json.dumps(row, ensure_ascii=False)
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(line + "\n")
        print(line, flush=True)


class FrozenPlanAgent(_FrozenTruthReplayAgent):
    name = "work_ii_shared_frozen_plan"

    def __init__(self, actions, *, formal_result=False):
        super().__init__(actions)
        self.formal_result = formal_result

    def manifest(self) -> dict[str, Any]:
        return {
            **super().manifest(),
            "execution_role": "fixed_design_replication"
            if self.formal_result
            else "fixed_design_development",
            "participant_feedback": False,
        }


def execute_plan(
    protocol: dict,
    task: str,
    row: dict,
    path: Path,
    observation_index: int,
    interventions: list | None = None,
) -> dict:
    """The same constructor, actions, score and replay serve public and private roles."""
    if path.exists():
        raise FileExistsError(f"physical execution already started: {path}")
    path.mkdir(parents=True)
    seal(path / "started.json", {"task": task, "id": row["id"]})
    started, cpu_started = time.perf_counter(), time.process_time()
    receipt: dict[str, Any] = {"task": task, "id": row["id"], "status": "failed"}
    trajectory = path / "trajectory.jsonl"
    try:
        actions = row["action_plan"]
        spec = protocol["tasks"][task]
        run_agent(
            env_id=get_task(task).env_id,
            agent=FrozenPlanAgent(actions, formal_result=protocol.get("formal_result", False)),
            world_split=protocol["world_split"],
            budget=len(actions),
            objective=protocol["objective"],
            seed=protocol["world_seed"],
            agent_seed=0,
            observation_seed=protocol["observation_seed_base"] + observation_index,
            task_id=task,
            output_path=trajectory,
            budget_override=len(actions),
            episode_mode_override="single_experiment",
            world_interventions=interventions,
            electrochemical_workflow_mode=row["workflow_mode"],
            scoring_contract_id=spec.get("scoring_contract_id"),
            observation_noise_mode=protocol["observation_noise_mode"],
            observation_noise_namespace=protocol["noise_namespace"] + "/" + task,
        )
        records = load_jsonl(trajectory)
        if [record["action"] for record in records] != actions:
            raise ValueError("executed ActionPlan differs from public compiled ActionPlan")
        if any(record.get("transaction_status") != "committed" for record in records):
            raise ValueError("non-committed operation in fixed ActionPlan")
        final = [record for record in records if record.get("instrument") == "final_assay"]
        if len(final) != 1:
            raise ValueError("expected one final assay")
        replay = verify_records(records, tolerance=0.0, world_interventions=interventions).to_dict()
        receipt["replay"] = replay
        if not replay["verified"]:
            raise ValueError("exact replay failed")
        score = _truth_metrics(final[0], ["score"])["score"]
        if not 0 <= score <= 1:
            raise ValueError("score outside the registered scale")
        receipt.update(
            {
                "status": "completed",
                "score": score,
                "action_plan_equal": True,
                "operation_count": len(records),
                "method_resources": final[0]["method_resources"],
                "measurement_cost": sum(record.get("measurement_cost", 0) for record in records),
                "recipe_duration_s": sum(
                    value for key, value in row["controls"].items() if key.endswith("duration_s")
                ),
                "reagent_amount_mol": row["controls"]["reagent_amount_mol"],
                "instrument_calls": dict(
                    Counter(record["instrument"] for record in records if record.get("instrument"))
                ),
            }
        )
    except Exception as error:
        receipt.update({"failure_type": type(error).__name__, "failure_message": str(error)[:1000]})
    receipt.update(
        {"wall_s": time.perf_counter() - started, "cpu_s": time.process_time() - cpu_started}
    )
    seal(path / "receipt.json", receipt)
    return receipt


def prepare(root: Path) -> dict:
    if root.exists():
        return read(root / "m0.json")  # incomplete physical preparation is never rerun in place
    protocol = development_protocol()
    packets = {task: compile_design(protocol, task) for task in TASKS}
    root.mkdir(parents=True)
    seal(root / "protocol.json", protocol)
    progress = Progress(root)
    receipts, private = [], {}
    for task, packet in packets.items():
        private[task] = {}
        for index, row in enumerate(packet["evidence"] + packet["candidates"]):
            receipt = execute_plan(protocol, task, row, root / "physical" / task / row["id"], index)
            receipts.append(receipt)
            if receipt["status"] == "completed":
                if row["id"].startswith("e"):
                    row["score"] = receipt["score"]
                else:
                    private[task][row["id"]] = receipt["score"]
            progress.emit("physical+replay", len(receipts), 42, status=receipt["status"])
    control = []
    for label, interventions in (("parent", None), ("child", protocol["intervention"])):
        receipt = execute_plan(
            protocol,
            TASKS[0],
            packets[TASKS[0]]["evidence"][0],
            root / "physical" / "intervention" / label,
            0,
            interventions,
        )
        control.append(receipt)
        receipts.append(receipt)
        progress.emit("intervention+replay", len(receipts), 42, status=receipt["status"])
    complete = sum(row["status"] == "completed" for row in receipts)
    report = {
        "formal_result": False,
        "scheduled": 42,
        "completed": complete,
        "status": "completed" if complete == 42 else "failed",
        "receipts": receipts,
        "intervention_score_difference": control[1]["score"] - control[0]["score"]
        if all(row["status"] == "completed" for row in control)
        else None,
    }
    if complete == 42:
        for task, packet in packets.items():
            seal(root / "public" / f"{task}.json", public_packet(packet, candidates=True))
        seal(root / "private_scores.json", private)
    seal(root / "m0.json", report)
    return report


def provider_call(
    root: Path,
    call_id: str,
    model: str,
    stage: str,
    packet: dict,
    coefficients: list | None,
    progress: Progress,
    completed: int,
    *,
    total: int = 12,
    provider_override: dict | None = None,
) -> dict:
    path = root / "provider" / call_id
    if (path / "receipt.json").exists():
        return read(path / "receipt.json")
    if (path / "started.json").exists():
        receipt = {
            "call_id": call_id,
            "status": "interrupted",
            "usage": {},
            "failure_type": "started_without_receipt_no_retry",
        }
        seal(path / "receipt.json", receipt)
        return receipt
    ids = [row["id"] for row in packet["candidates"]]
    prompt = participant_prompt(packet, coefficients=coefficients)
    seal(path / "started.json", {"call_id": call_id, "model": model, "stage": stage})
    seal(path / "prompt.json", {"prompt": prompt})
    provider = provider_override or read(PROVIDER_CONFIGS[model])["provider"]
    receipt: dict[str, Any] = {"call_id": call_id, "status": "failed", "usage": {}}
    try:
        with tempfile.TemporaryDirectory(prefix="chemworld-m1-") as temp:
            temporary = Path(temp)
            workspace = temporary / "workspace"
            workspace.mkdir()
            schema = temporary / "output-schema.json"
            seal(schema, output_schema(stage, ids))
            environment = _prepare_codex_home(temporary, provider)
            command = _initial_command(provider, schema, workspace)
            index = command.index("--sandbox")
            command[index:index] = ["--disable", "shell_tool"]
            raw = _launch_turn(
                command,
                prompt,
                cwd=workspace,
                environment=environment,
                timeout_s=600,
                liveness=lambda event: progress.emit(
                    "provider-live", completed, total, call_id=call_id, live=event
                ),
            )
            receipt.update(raw)
        if receipt["status"] == "completed":
            if receipt.get("tool_event_count", 0):
                receipt["protocol_failure"] = "forbidden_tool_use"
                raise RuntimeError("forbidden_tool_use")
            if not receipt.get("thread_id"):
                receipt["protocol_failure"] = "missing_session_identity"
                raise RuntimeError("missing_session_identity")
            validate_payload(receipt.get("final_payload"), stage, ids)
    except ValueError as error:
        receipt.update({"status": "schema_failed", "failure_type": str(error)})
    except Exception as error:
        receipt.update({"status": "failed", "failure_type": type(error).__name__})
    seal(path / "receipt.json", receipt)
    return receipt


def run_provider_block(root: Path) -> dict:
    if (root / "selections.json").exists():
        return read(root / "selections.json")
    if read(root / "m0.json")["status"] != "completed":
        raise RuntimeError("physical/replay block failed; provider block is stopped")
    progress = Progress(root)
    calls, all_slots, artifacts, baseline_choices = [], [], {}, {}
    threads, stop_reason = set(), None

    def call(
        call_id: str, model: str, stage: str, packet: dict, law: list | None, blocked: bool = False
    ) -> dict:
        nonlocal stop_reason
        if stop_reason or blocked:
            receipt = {
                "call_id": call_id,
                "status": "not_attempted",
                "failure_type": stop_reason or "missing_source_artifact",
                "usage": {},
            }
        else:
            receipt = provider_call(root, call_id, model, stage, packet, law, progress, len(calls))
            thread = receipt.get("thread_id")
            if receipt.get("tool_event_count", 0) or (thread and thread in threads):
                stop_reason = "forbidden_tool_or_reused_session"
                receipt = {**receipt, "status": "protocol_failed", "failure_type": stop_reason}
            elif receipt.get("status") == "completed" and not thread:
                stop_reason = "missing_session_identity"
            if thread:
                threads.add(thread)
        calls.append(receipt)
        progress.emit("provider", len(calls), 12, call_id=call_id, status=receipt["status"])
        return receipt

    for task in TASKS:
        packet = read(root / "public" / f"{task}.json")
        fitted = fit_public_law(packet["evidence"])
        baseline_choices[task] = nearest_public_choice(packet)
        for model in MODELS:
            prefix = task + "--" + model
            source = call(prefix + "--source", model, "source", packet, None)
            law = (
                source["final_payload"]["coefficients"] if source["status"] == "completed" else None
            )
            artifacts[prefix] = {"L": law, "F": fitted}
            for kind, coefficients in (("L", law), ("F", fitted)):
                decision = call(
                    prefix + "--" + kind + "-A",
                    model,
                    "decision",
                    packet,
                    coefficients,
                    blocked=coefficients is None,
                )
                all_slots.append(
                    {
                        "task": task,
                        "model": model,
                        "condition": kind + "-A",
                        "status": decision["status"],
                        "candidate_id": decision["final_payload"]["candidate_id"]
                        if decision["status"] == "completed"
                        else None,
                    }
                )
                try:
                    choice = maximize(coefficients, packet["candidates"]) if coefficients else None
                except ValueError:
                    choice = None
                all_slots.append(
                    {
                        "task": task,
                        "model": model,
                        "condition": kind + "-X",
                        "status": "completed" if choice and not stop_reason else "blocked",
                        "candidate_id": choice if not stop_reason else None,
                    }
                )
    report = {
        "slots": all_slots,
        "calls": calls,
        "artifacts": artifacts,
        "nearest_choices": baseline_choices,
        "stop_reason": stop_reason,
    }
    seal(root / "selections.json", report)  # no candidate outcome read before this write
    return report


def analyze(root: Path) -> dict:
    if (root / "summary.json").exists():
        return read(root / "summary.json")
    selections = read(root / "selections.json")
    truth, m0 = read(root / "private_scores.json"), read(root / "m0.json")
    rows, baselines, law_metrics = [], [], []
    for task in TASKS:
        rows.extend(
            score_slots([row for row in selections["slots"] if row["task"] == task], truth[task])
        )
        best = max(truth[task].values())
        baselines.append(
            {
                "task": task,
                "nearest_public_regret": best - truth[task][selections["nearest_choices"][task]],
                "uniform_random_expected_regret": best - np.mean(list(truth[task].values())),
                "candidate_score_min": min(truth[task].values()),
                "candidate_score_max": best,
            }
        )
        packet = read(root / "public" / f"{task}.json")
        actual = np.array([truth[task][row["id"]] for row in packet["candidates"]])
        for model in MODELS:
            for kind, law in selections["artifacts"][task + "--" + model].items():
                law_metrics.append(
                    {
                        "task": task,
                        "model": model,
                        "artifact": kind,
                        "candidate_mae": float(
                            np.mean(np.abs(design_matrix(packet["candidates"]) @ law - actual))
                        )
                        if law
                        else None,
                    }
                )
    contrasts = []
    for task in TASKS:
        for model in MODELS:
            selected = {
                row["condition"]: row["failure_aware_regret"]
                for row in rows
                if row["task"] == task and row["model"] == model
            }
            contrasts.append(
                {
                    "task": task,
                    "model": model,
                    "F-X_minus_L-X": selected["F-X"] - selected["L-X"],
                    "L-X_minus_L-A": selected["L-X"] - selected["L-A"],
                    "F-X_minus_F-A": selected["F-X"] - selected["F-A"],
                }
            )
    calls = selections["calls"]
    usage = Counter()
    for row in calls:
        usage.update(
            {
                key: value
                for key, value in row.get("usage", {}).items()
                if isinstance(value, int | float)
            }
        )
    report = {
        "formal_result": False,
        "independent_world_clusters": 2,
        "physical_scheduled": 42,
        "physical_completed": m0["completed"],
        "exact_replay_completed": sum(
            row.get("replay", {}).get("verified", False) for row in m0["receipts"]
        ),
        "intervention_score_difference": m0["intervention_score_difference"],
        "provider_opportunities": 12,
        "provider_attempted": sum(row["status"] != "not_attempted" for row in calls),
        "provider_completed": sum(row["status"] == "completed" for row in calls),
        "condition_scheduled": 16,
        "condition_completed": sum(row["status"] == "completed" for row in rows),
        "provider_usage": dict(usage),
        "provider_wall_s": sum(row.get("elapsed_s", 0) for row in calls),
        "physical_costs": {
            key: sum(row.get(key, 0) for row in m0["receipts"])
            for key in (
                "operation_count",
                "measurement_cost",
                "recipe_duration_s",
                "reagent_amount_mol",
                "wall_s",
                "cpu_s",
            )
        },
        "failures": [
            {
                "call_id": row["call_id"],
                "status": row["status"],
                "failure_type": row.get("failure_type", row["status"]),
            }
            for row in calls
            if row["status"] != "completed"
        ],
        "slots": rows,
        "baselines": baselines,
        "artifact_metrics": law_metrics,
        "paired_contrasts": contrasts,
        "stop_reason": selections["stop_reason"],
        "interpretation": "Two development worlds; no confidence interval, significance test, "
        "formal qualification, or generalization claim. Costs are simulator units and provider "
        "tokens/wall time; currency and billing overhead are not estimated.",
    }
    seal(root / "summary.json", report)
    lines = [
        "# M0/M1 development result",
        "",
        report["interpretation"],
        "",
        f"Physical/replay: {report['physical_completed']}/42; provider: "
        f"{report['provider_completed']}/12; condition availability: "
        f"{report['condition_completed']}/16.",
        "",
        "| Task | Model | Condition | Status | Regret (failure-aware) |",
        "| --- | --- | --- | --- | ---: |",
    ]
    for row in sorted(
        rows, key=lambda row: (row["task"], row["model"], CONDITIONS.index(row["condition"]))
    ):
        lines.append(
            f"| {row['task']} | {row['model']} | {row['condition']} | {row['status']} "
            f"| {row['failure_aware_regret']:.6f} |"
        )
    lines.extend(
        [
            "",
            "Provider usage: " + json.dumps(report["provider_usage"]),
            "",
            "Failures: " + json.dumps(report["failures"]),
            "",
        ]
    )
    with (root / "summary.md").open("x", encoding="utf-8") as handle:
        handle.write("\n".join(lines))
    return report


def export_summary(root: Path, destination: Path) -> dict:
    """Export a sanitized, reproducible summary; retain the original run outputs."""
    report = dict(analyze(root))
    resource_rows = []
    calls = read(root / "selections.json")["calls"]
    for model in MODELS:
        for stage in ("source", "decision"):
            selected = [
                row
                for row in calls
                if f"--{model}--" in row["call_id"]
                and (row["call_id"].endswith("--source") == (stage == "source"))
            ]
            usage = Counter()
            for row in selected:
                usage.update(
                    {
                        key: value
                        for key, value in row.get("usage", {}).items()
                        if isinstance(value, int | float)
                    }
                )
            resource_rows.append(
                {
                    "model": model,
                    "stage": stage,
                    "scheduled": len(selected),
                    "completed": sum(row["status"] == "completed" for row in selected),
                    "wall_s": sum(row.get("elapsed_s", 0) for row in selected),
                    "usage": dict(usage),
                }
            )
    report["provider_resources_by_stage"] = resource_rows
    report["schema_version"] = "work-ii-m0-m1-development-summary-1"
    report["experiment_note"] = (
        "workstreams/flagship_tasks/WORK_II_M0_M1_DEVELOPMENT_EXPERIMENT_NOTE.md"
    )
    seal(destination, report)
    lines = [
        "# M0/M1 development summary",
        "",
        report["interpretation"],
        "",
        "L = model-generated quadratic; F = public-only ridge fit; "
        "A = fresh model decision; X = shared deterministic maximizer.",
        "",
        "| Task | Model | L-A | L-X | F-A | F-X |",
        "| --- | --- | ---: | ---: | ---: | ---: |",
    ]
    for task in TASKS:
        for model in MODELS:
            regrets = {
                row["condition"]: row["failure_aware_regret"]
                for row in report["slots"]
                if row["task"] == task and row["model"] == model
            }
            values = " | ".join(f"{regrets[key]:.6f}" for key in CONDITIONS)
            lines.append(f"| {task} | {model} | {values} |")
    lines += [
        "",
        "Regret uses fixed utility scale 1; near-optimality threshold 0.01.",
        "",
        "| Task | Nearest public evidence | Uniform random (exact expectation) |",
        "| --- | ---: | ---: |",
    ]
    for row in report["baselines"]:
        lines.append(
            f"| {row['task']} | {row['nearest_public_regret']:.6f} | "
            f"{row['uniform_random_expected_regret']:.6f} |"
        )
    lines += [
        "",
        f"Physical execution and exact replay: {report['physical_completed']}/42 each. "
        f"Provider completion: {report['provider_completed']}/12. "
        f"Condition availability: {report['condition_completed']}/16.",
        "",
        "| Model | Stage | Complete/scheduled | Wall seconds | Input | Output |",
        "| --- | --- | ---: | ---: | ---: | ---: |",
    ]
    for row in resource_rows:
        lines.append(
            f"| {row['model']} | {row['stage']} | {row['completed']}/{row['scheduled']} "
            f"| {row['wall_s']:.1f} | {row['usage'].get('input_tokens', 0)} "
            f"| {row['usage'].get('output_tokens', 0)} |"
        )
    lines += [
        "",
        "Output usage includes reasoning tokens; cached input is a subset of input. "
        "Recipe duration and measurement costs are simulator units. Physical CPU/wall "
        "includes replay; recipe resource sums count main executions once.",
        "",
        "Failures: " + json.dumps(report["failures"]),
        "",
        "See the JSON companion for all slots, artifact errors, paired contrasts and costs.",
        "",
    ]
    with destination.with_suffix(".md").open("x", encoding="utf-8") as handle:
        handle.write("\n".join(lines))
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=("prepare", "run", "analyze"))
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--report", type=Path, help="analyze only: write a sanitized JSON/Markdown pair"
    )
    args = parser.parse_args()
    if args.report and args.stage != "analyze":
        parser.error("--report belongs to the provider-free analyze stage")
    root = args.output.resolve()
    if args.stage == "prepare":
        result = prepare(root)
        print(
            json.dumps({key: result[key] for key in ("status", "scheduled", "completed")}),
            flush=True,
        )
    else:
        if args.stage == "run":
            run_provider_block(root)
        result = analyze(root)
        if args.report:
            export_summary(root, args.report.resolve())
        print(
            json.dumps(
                {
                    key: result[key]
                    for key in (
                        "provider_completed",
                        "condition_completed",
                        "provider_usage",
                        "failures",
                    )
                }
            ),
            flush=True,
        )


if __name__ == "__main__":
    main()
