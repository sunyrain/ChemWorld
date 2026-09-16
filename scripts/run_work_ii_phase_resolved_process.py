"""W2-105: fixed feasibility block and one Astra episode per qualified task."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import threading
import time
from copy import deepcopy
from dataclasses import replace
from pathlib import Path

import gymnasium as gym
from scripts.analyze_work_ii_astra_full_process_trial import analyze_cell
from scripts.run_work_ii_astra_full_process_trial import (
    LIMITS,
    QUALITY,
    ROOT,
    TASKS,
    FullProcessAgent,
    card,
    quality_checks,
    reference_actions,
    summarize,
)
from scripts.run_work_ii_astra_single_trial import read, write

from chemworld.data.logging import load_jsonl
from chemworld.eval.runner import run_agent
from chemworld.eval.verify import verify_records
from chemworld.eval.work_ii_truth import _FrozenTruthReplayAgent
from chemworld.runtime.full_process_contract import FULL_PROCESS_CONTRACT
from chemworld.tasks import get_task

NOTE = "workstreams/flagship_tasks/WORK_II_PHASE_RESOLVED_PROCESS_NOTE.md"
NAMESPACE = "work-ii-phase-resolved-process-v1"
CLOSE = [{"operation": "terminate"}, {"operation": "measure", "instrument": "final_assay"}]
PARTICLE = {"operation": "measure", "instrument": "particle_size"}


def resource_card(task):
    original = card(task)
    return replace(
        original,
        card_id="phase-resolved-" + task,
        implicit_operation_time_s={**original.implicit_operation_time_s, "measure": 120},
    )


def plans():
    result = []

    def add(label, task, actions):
        result.append(
            {"cell": label, "task": task, "actions": deepcopy(actions), "kind": "reference"}
        )

    for i, (temperature, duration, extractant, wash) in enumerate(
        itertools.product((370, 385, 400), (3600, 7200), (2, 3), (0, 0.004)), 1
    ):
        prefix = reference_actions(TASKS[0])[:3]
        add(
            f"P{i:02}",
            TASKS[0],
            [
                *prefix,
                {
                    "operation": "heat",
                    "target_temperature_K": temperature,
                    "duration_s": duration,
                    "stirring_speed_rpm": 720,
                },
                {"operation": "measure", "instrument": "hplc"},
                {"operation": "quench"},
                {"operation": "add_phase", "phase": "aqueous", "volume_L": 0.012},
                {"operation": "add_extractant", "extractant": extractant, "volume_L": 0.018},
                {"operation": "mix", "duration_s": 240, "stirring_speed_rpm": 850},
                {"operation": "settle", "duration_s": 420},
                {"operation": "measure", "instrument": "hplc"},
                {"operation": "separate_phase", "target_phase": "organic"},
                *([{"operation": "wash", "wash_volume_L": wash}] if wash else []),
                {"operation": "dry"},
                {"operation": "concentrate", "duration_s": 600},
                {"operation": "transfer", "transfer_fraction": 0.97},
                *CLOSE,
            ],
        )
    for i, (seed, target, duration, hold) in enumerate(
        itertools.product((0.006, 0.050), (285, 278.15), (7200, 14400), (0, 14400)), 1
    ):
        add(
            f"C{i:02}",
            TASKS[1],
            [
                *reference_actions(TASKS[1])[:8],
                {"operation": "seed_crystals", "seed_mass_g": seed},
                {
                    "operation": "cool_crystallize",
                    "target_temperature_K": target,
                    "duration_s": duration,
                },
                PARTICLE,
                *(
                    [
                        {
                            "operation": "cool_crystallize",
                            "target_temperature_K": target,
                            "duration_s": hold,
                        },
                        PARTICLE,
                    ]
                    if hold
                    else []
                ),
                {"operation": "measure", "instrument": "hplc"},
                {"operation": "filter_crystals"},
                *CLOSE,
            ],
        )
    binding = read(ROOT / "configs/current.json")["work_ii"]["w2_103_astra_full_process_trial"]
    report = ROOT / binding["report"]
    if hashlib.sha256(report.read_bytes()).hexdigest() != binding["report_sha256"]:
        raise ValueError("historical prefix binding mismatch")
    d = [
        r["action"]
        for r in load_jsonl(ROOT / binding["run_root"] / "agent" / TASKS[2] / "trajectory.jsonl")
    ][:10]
    for i, (temperature, duration, reflux) in enumerate(
        itertools.product((350, 365, 385), (100, 300, 600), (3, 10)), 1
    ):
        add(
            f"D{i:02}",
            TASKS[2],
            [
                *d,
                {
                    "operation": "distill",
                    "target_temperature_K": temperature,
                    "duration_s": duration,
                    "reflux_ratio": reflux,
                },
                {"operation": "collect_fraction", "transfer_fraction": 1.0},
                {"operation": "measure", "instrument": "gc"},
                *CLOSE,
            ],
        )
    return result


class ResolvedAgent(FullProcessAgent):
    def reset(self, task_info, seed):
        super().reset(task_info, seed)
        self._task_contract.update(
            full_process_contract_id=task_info["full_process_contract_id"],
            instrument_contracts={
                k: task_info["instruments"][k] for k in task_info["allowed_instruments"]
            },
        )
        self._task_contract["process_semantics"] += [
            "For v2 and later, distill accepts optional cut_fraction in [0.005, 0.9], "
            "independent of duration; the actual cut remains duty-limited. Repeated cooling "
            "retains particle cohorts. For v3 and later, reheating after quench dissolves solid "
            "according to the existing solubility closure, with equal radial recession of "
            "the particle population. For v4, seed origin is tracked through solid/liquor "
            "transfers; reprecipitated seed never earns new-product yield. Origin tracking "
            "uses well-mixed tracer fractions within each phase, without core-shell resolution.",
            "All recovery and crystal-yield denominators are original reactant charge; "
            "crystal yield excludes retained seed. Downstream local yield is not total yield.",
            "Sampling withdraws only the selected liquid phase (organic when unselected). "
            "Crystalline solids and mother liquor use representative slurry sampling together, "
            "including after filtration. Other saved liquid receivers are not depleted.",
            "collect_fraction transfer_fraction=0 reselects an existing saved collected_fraction "
            "without adding current distillate. Positive fractions mix into that receiver.",
            "particle_size provides noisy number-weighted d50 and fines fraction below 20 um "
            "when a crystal population exists. It costs 0.04 and 120 seconds, without withdrawal. "
            "This is a bounded synthetic sensor, without raw images. HPLC gives chemical quality.",
        ]
        self._task_contract_manifest = self.workspace.publish_task_contract(self._task_contract)


class DiagnosticCapture(gym.Wrapper):
    def __init__(self, env, records):
        super().__init__(env)
        self.records = records

    def step(self, action):
        before = self.unwrapped.observation_kernel._truth_values(self.unwrapped._state)
        result = self.env.step(action)
        self.records.append({"action": deepcopy(action), "pre_action_truth": before})
        return result


def execute(root, plan, progress):
    folder = root / plan["cell"]
    if (folder / "result.json").exists():
        return read(folder / "result.json")
    folder.mkdir()  # Retained incomplete attempts may not be relaunched.
    write(folder / "plan.json", plan)
    task, kind = plan["task"], plan["kind"]
    progress.update(stage=plan["cell"], operations=0)
    started, diagnostic, failure = time.monotonic(), [], None
    agent = (
        _FrozenTruthReplayAgent(plan["actions"])
        if kind == "reference"
        else ResolvedAgent(
            task=task,
            workspace=folder / "workspace",
            role_id="phase_resolved_process",
            request_timeout_s=600,
            finalization_timeout_s=120,
            session_wall_time_limit_s=1800,
            max_recovered_mcp_tool_failures=8,
            max_consecutive_mcp_tool_failures=4,
            max_provider_error_events=0,
            pre_action_restart_limit=0,
            accepted_turn_continuation_limit=0,
            provider_process_attempt_limit=1,
            max_initial_prompt_bytes=131072,
            history_event_limit=100,
            session_progress_callback=lambda payload: progress.update(provider_liveness=payload),
        )
    )

    def on_step(record, trace):
        progress["operations"] += 1
        if kind == "agent":
            print(
                json.dumps(
                    {"stage": plan["cell"], "step": progress["operations"], "action": record.action}
                ),
                flush=True,
            )
        elif record.info.get("transaction_status") != "committed":
            raise RuntimeError(f"candidate stopped at failed transaction: {record.action}")

    try:
        run_agent(
            env_id=get_task(task).env_id,
            agent=agent,
            world_split="public-test",
            budget=LIMITS[task],
            budget_override=LIMITS[task],
            objective="balanced",
            seed=0,
            agent_seed=0,
            observation_seed=1,
            task_id=task,
            output_path=folder / "trajectory.jsonl",
            episode_mode_override="single_experiment",
            campaign_resource_card=replace(
                resource_card(task),
                process_time_limit_s=plan.get(
                    "process_time_limit_s", resource_card(task).process_time_limit_s
                ),
            ),
            observation_noise_mode="keyed",
            observation_noise_namespace=NAMESPACE,
            full_process_contract_id=plan.get("contract", FULL_PROCESS_CONTRACT),
            step_callback=on_step,
            env_wrapper=lambda env: DiagnosticCapture(env, diagnostic),
            method_resource_limits={
                "operation_limit": LIMITS[task],
                "complete_experiment_limit": 1,
                "wall_time_limit_s": 1920,
                "model_call_limit": 1,
                "input_token_limit": 4000000,
                "uncached_input_token_limit": 1000000,
                "output_token_limit": 64000,
                "training_environment_step_limit": 0,
            },
        )
    except Exception as exc:
        failure = {"type": type(exc).__name__, "message": str(exc)[:1600]}
    finally:
        if kind == "agent":
            agent.close()
    rows = load_jsonl(folder / "trajectory.jsonl") if (folder / "trajectory.jsonl").exists() else []
    summary = summarize(task, rows)
    replay = verify_records(rows, tolerance=0).to_dict() if rows else {"verified": False}
    receipts = agent.provider_receipts() if kind == "agent" else []
    truth = (
        next(
            (
                d["pre_action_truth"]
                for d in reversed(diagnostic)
                if d["action"].get("instrument") == "final_assay"
            ),
            {},
        )
        if summary["final_assays"]
        else {}
    )
    result = {
        "cell": plan["cell"],
        "task": task,
        "kind": kind,
        "failure": failure,
        "status": "completed" if summary["final_assays"] and not failure else "failed",
        "elapsed_s": time.monotonic() - started,
        "summary": summary,
        "provider_usage": agent.method_resource_usage() if kind == "agent" else {},
        "exact_replay": replay.get("verified") is True,
        "assay_truth": truth,
        "truth_quality_checks": quality_checks(task, truth),
    }
    write(folder / "evaluator_states.json", diagnostic)
    write(folder / "replay.json", replay)
    write(folder / "receipts.json", receipts)
    write(folder / "result.json", result)
    analysis = analyze_cell(folder)
    result["analysis"] = analysis
    result["witness"] = (
        result["status"] == "completed"
        and result["exact_replay"]
        and not summary["failures"]
        and summary["quality_passed"]
        and all(result["truth_quality_checks"].values())
        and all(analysis["validation"].values())
    )
    write(folder / "result.json", result)
    progress["completed"] += 1
    print(
        json.dumps(
            {
                "stage": plan["cell"],
                "completed": progress["completed"],
                "total": progress["total"],
                "witness": result["witness"],
                "truth": {k: truth.get(k) for k in QUALITY[task]},
                "failure": failure,
            }
        ),
        flush=True,
    )
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--phase", choices=("reference", "agent"), default="reference")
    args = parser.parse_args()
    root = args.output.resolve()
    root.mkdir(parents=True, exist_ok=True)
    planned = plans()
    write(root / "planned_candidates.json", planned)
    selected = (
        planned
        if args.phase == "reference"
        else [
            {"cell": "A" + str(i + 1), "task": task, "kind": "agent"}
            for i, task in enumerate(TASKS)
            if any(
                read(root / p["cell"] / "result.json").get("witness")
                for p in planned
                if p["task"] == task and (root / p["cell"] / "result.json").exists()
            )
        ]
    )
    progress = {"stage": "starting", "completed": 0, "total": len(selected), "operations": 0}
    stop = threading.Event()
    started = time.monotonic()

    def heartbeat():
        while not stop.wait(30):
            elapsed = time.monotonic() - started
            rate = progress["completed"] / elapsed
            print(
                json.dumps(
                    {
                        **progress,
                        "elapsed_s": round(elapsed),
                        "units_per_min": 60 * rate,
                        "eta_s": (len(selected) - progress["completed"]) / rate if rate else None,
                    }
                ),
                flush=True,
            )

    worker = threading.Thread(target=heartbeat, daemon=True)
    worker.start()
    try:
        for plan in selected:
            execute(root, plan, progress)
    finally:
        stop.set()
        worker.join()


if __name__ == "__main__":
    main()
