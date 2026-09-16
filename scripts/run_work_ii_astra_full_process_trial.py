"""One development round: native operation-level autonomy on three full processes."""

from __future__ import annotations

import argparse
import json
import threading
import time
from collections import Counter
from copy import deepcopy
from pathlib import Path

from scripts.run_work_ii_astra_single_trial import PROVIDER, read, write
from scripts.run_work_ii_study_b import _prepare_codex_home

from chemworld.agents.interactive_codex_experiment import InteractiveCodexExperimentAgent
from chemworld.campaign_resources import CampaignResourceCard
from chemworld.data.logging import load_jsonl
from chemworld.eval.runner import run_agent
from chemworld.eval.verify import verify_records
from chemworld.eval.work_ii_truth import _FrozenTruthReplayAgent
from chemworld.tasks import get_task
from chemworld.world.instruments import instrument_contracts
from chemworld.world.operations import operation_contracts

ROOT = Path(__file__).resolve().parents[1]
NOTE = "workstreams/flagship_tasks/WORK_II_ASTRA_FULL_PROCESS_TRIAL_NOTE.md"
TASKS = ("reaction-to-purification", "reaction-to-crystallization", "reaction-to-distillation")
LIMITS = dict(zip(TASKS, (90, 72, 72), strict=True))
QUALITY = {
    TASKS[0]: {"purity": [">=", 0.8], "recovery": [">=", 0.1]},
    TASKS[1]: {
        "crystal_purity": [">=", 0.8],
        "crystal_yield": [">=", 0.1],
        "crystal_fines_fraction": ["<=", 0.5],
    },
    TASKS[2]: {"distillate_purity": [">=", 0.8], "distillate_recovery": [">=", 0.1]},
}
NAMESPACE = "work-ii-astra-full-process-single-round"


def card(task):
    return CampaignResourceCard(
        card_id="astra-full-process-" + task,
        operation_attempt_limit=LIMITS[task],
        vessel_start_limit=1,
        final_assay_limit=1,
        nonfinal_instrument_use_limit=12,
        stock_limits={
            "reagent_mol": 0.04,
            "solvent_L": 0.08,
            "catalyst_mol": 0.005,
            "seed_g": 0.05,
            "extractant_L": 0.08,
            "phase_liquid_L": 0.08,
            "wash_solvent_L": 0.08,
        },
        process_time_limit_s=43200,
        implicit_operation_time_s={
            "quench": 120,
            "filter_crystals": 480,
            **({"dry": 300} if task == TASKS[0] else {}),
        },
    )


def reference_actions(task):
    steps = [
        {"operation": "add_solvent", "volume_L": 0.028, "solvent": 2},
        {"operation": "add_reagent", "amount_mol": 0.010},
        {"operation": "add_catalyst", "catalyst_amount_mol": 0.00025, "catalyst": 1},
        {
            "operation": "heat",
            "target_temperature_K": 385.0,
            "duration_s": 1500.0,
            "stirring_speed_rpm": 720.0,
        },
        {"operation": "wait", "duration_s": 900.0, "stirring_speed_rpm": 720.0},
        {"operation": "measure", "instrument": "hplc"},
        {"operation": "quench"},
        {"operation": "measure", "instrument": "hplc"},
    ]
    if task == TASKS[0]:
        steps += [
            {"operation": "add_phase", "phase": "aqueous", "volume_L": 0.012},
            {"operation": "add_extractant", "extractant": 3, "volume_L": 0.018},
            {"operation": "mix", "duration_s": 240.0, "stirring_speed_rpm": 850.0},
            {"operation": "settle", "duration_s": 420.0},
            {"operation": "measure", "instrument": "hplc"},
            {"operation": "separate_phase", "target_phase": "organic"},
            {"operation": "wash", "wash_volume_L": 0.008},
            {"operation": "dry"},
            {"operation": "concentrate", "duration_s": 600.0},
            {"operation": "transfer", "transfer_fraction": 0.97},
            {"operation": "measure", "instrument": "hplc"},
        ]
    elif task == TASKS[1]:
        steps += [
            {"operation": "seed_crystals", "seed_mass_g": 0.006},
            {"operation": "cool_crystallize", "target_temperature_K": 278.15, "duration_s": 1800.0},
            {
                "operation": "heat",
                "target_temperature_K": 300.0,
                "duration_s": 300.0,
                "stirring_speed_rpm": 600.0,
            },
            {"operation": "cool_crystallize", "target_temperature_K": 278.15, "duration_s": 1800.0},
            {"operation": "measure", "instrument": "hplc"},
            {"operation": "filter_crystals"},
        ]
    elif task == TASKS[2]:
        steps += [
            {"operation": "evaporate", "target_temperature_K": 335.0, "duration_s": 600.0},
            {
                "operation": "distill",
                "target_temperature_K": 360.0,
                "duration_s": 1500.0,
                "reflux_ratio": 2.0,
            },
            {"operation": "collect_fraction", "transfer_fraction": 0.5},
            {"operation": "measure", "instrument": "gc"},
            {
                "operation": "distill",
                "target_temperature_K": 370.0,
                "duration_s": 1200.0,
                "reflux_ratio": 3.0,
            },
            {"operation": "collect_fraction", "transfer_fraction": 0.92},
            {"operation": "measure", "instrument": "gc"},
        ]
    else:
        raise ValueError(task)
    return [
        *steps,
        {"operation": "terminate"},
        {"operation": "measure", "instrument": "final_assay"},
    ]


class FullProcessAgent(InteractiveCodexExperimentAgent):
    """Reuse the native lab bridge with the already-used cached-login Astra route."""

    def __init__(self, *, task, **kwargs):
        self.trial_task = task
        super().__init__(
            model="gpt-6-astra",
            reasoning_effort="medium",
            model_provider="chemworld_astra_trial",
            model_provider_auth_mode="none",
            **kwargs,
        )

    def _prepare_provider_launch(self, *, temp_root):
        self._session_process_environment = _prepare_codex_home(temp_root, PROVIDER)
        self._use_isolated_codex_home = True

    def _model_provider_config_overrides(self):
        return [
            "-c",
            'model_providers.chemworld_astra_trial={name="OpenAI",wire_api="responses",'
            "requires_openai_auth=true,supports_websockets=false,request_max_retries=0,stream_max_retries=0}",
        ]

    def reset(self, task_info, seed):
        super().reset(task_info, seed)
        task = get_task(self.trial_task)
        instruments = instrument_contracts()
        operations = operation_contracts()
        self._task_contract.update(
            trial_quality_targets=QUALITY[self.trial_task],
            trial_goal="First meet every quality target, then increase recovered product while "
            "controlling costs. Native leaderboard score is secondary and reported separately. "
            "Choose the full process autonomously using paid observations; one vessel only.",
            instrument_contracts={k: instruments[k].to_dict() for k in task.allowed_instruments},
            operation_contracts={k: operations[k].to_dict() for k in task.allowed_operations},
            process_semantics=[
                "Use the actual public state and current legal parameter ranges, not an assumed "
                "temperature equal to the heater setpoint. "
                "Measurements can become stale after operations.",
                "Separate_phase discards nonselected phases irreversibly. Sampling measures the "
                "currently active material; it does not reveal hidden amounts in all phases.",
                "Quench stops reaction. Before filtration, thermal reheating can redissolve "
                "crystals; recooling and reseeding are legal when listed. "
                "After filtration only closeout is legal.",
                "Crystal yield excludes retained seed; high purity without solution-grown "
                "product is insufficient. Particle quality is available only through declared "
                "measurements, not hidden inspection.",
                "Repeated distillation processes remaining bottoms. Prior distillate and collected "
                "inventory persist; collected fractions accumulate together, "
                "not in independent bottles.",
                "No free new batch, no automatic closeout, "
                "no reference recipe or reference outcomes. "
                "Do not execute unnecessary stages just to create a long trajectory.",
            ],
        )
        self._task_contract_manifest = self.workspace.publish_task_contract(self._task_contract)

    def _command(self, *, instructions_path, schema_path):
        instructions = instructions_path.read_text(encoding="utf-8")
        instructions += (
            "\nFor this development trial, trial_goal and trial_quality_targets in the public task "
            "contract define the primary objective. The native weighted score is secondary. "
            "Use only chemworld_lab tools; do not inspect files or the repository. "
            "Report a concise final scientific summary with observations, changes you made, "
            "quality achieved and remaining uncertainty. Do not claim causal discoveries from "
            "one trajectory.\n"
        )
        instructions_path.write_text(instructions, encoding="utf-8")
        command = super()._command(instructions_path=instructions_path, schema_path=schema_path)
        command.insert(2, "--ignore-user-config")
        for feature in (
            "shell_tool",
            "browser_use",
            "computer_use",
            "in_app_browser",
            "goals",
            "image_generation",
            "skill_search",
            "hooks",
            "code_mode",
            "code_mode_host",
        ):
            command += ["--disable", feature]
        return command


def scalar(value):
    while isinstance(value, list) and value:
        value = value[0]
    return float(value) if isinstance(value, (float, int)) and not isinstance(value, bool) else None


def quality_checks(task, metrics):
    return {
        key: metrics.get(key) is not None
        and (metrics[key] >= bound if operator == ">=" else metrics[key] <= bound)
        for key, (operator, bound) in QUALITY[task].items()
    }


def summarize(task, records):
    finals = [
        r
        for r in records
        if r.get("transaction_status") == "committed" and r.get("instrument") == "final_assay"
    ]
    final = finals[-1] if finals else {}
    metrics = {
        k: scalar(v)
        for k, v in final.get("observation", {}).items()
        if scalar(v) is not None and not k.endswith("_mask")
    }
    checks = quality_checks(task, metrics)
    failures = [
        {
            "step": i + 1,
            "action": r.get("action"),
            "status": r.get("transaction_status"),
            "reason": r.get("rollback_reason"),
            "failed_preconditions": {
                k: v for k, v in r.get("preconditions", {}).items() if v is False
            },
        }
        for i, r in enumerate(records)
        if r.get("transaction_status") != "committed"
    ]
    committed = [r for r in records if r.get("transaction_status") == "committed"]
    last = records[-1] if records else {}
    resources = (
        last.get("agent_view", {})
        .get("tool_json", {})
        .get("campaign_state", {})
        .get("campaign_resources", {})
    )
    measurements = []
    for i, row in enumerate(records):
        if row.get("operation_type") == "measure" and row.get("transaction_status") == "committed":
            public = row.get("agent_view", {}).get("tool_json", {})
            measurements.append(
                {
                    "step": i + 1,
                    "instrument": row.get("instrument"),
                    "public_measurement": public.get("measurement"),
                    "observation": row.get("observation"),
                }
            )
    return {
        "operation_attempts": len(records),
        "committed_operations": len(committed),
        "final_assays": len(finals),
        "final_metrics": metrics,
        "leaderboard_score": final.get("leaderboard_score"),
        "quality_checks": checks,
        "quality_passed": bool(finals) and all(checks.values()),
        "operation_counts": dict(Counter(r.get("operation_type") for r in committed)),
        "failures": failures,
        "final_campaign_resources": resources,
        "actions": [
            {"step": i + 1, "action": r.get("action"), "status": r.get("transaction_status")}
            for i, r in enumerate(records)
        ],
        "measurements": measurements,
        "total_process_time_s": resources.get("state", {})
        .get("report_only", {})
        .get("process_time_s"),
    }


def execute(root, task, kind, progress):
    folder = root / kind / task
    if (folder / "result.json").is_file():
        return read(folder / "result.json")
    if folder.exists():
        raise RuntimeError(f"retained incomplete attempt; no relaunch: {folder}")
    folder.mkdir(parents=True)
    write(folder / "attempt.json", {"task": task, "kind": kind, "started": time.time()})
    progress.update(stage=kind + "/" + task, operations=0)
    started = time.monotonic()
    failure = None
    if kind.startswith("reference"):
        agent = _FrozenTruthReplayAgent(reference_actions(task))
    else:
        agent = FullProcessAgent(
            task=task,
            workspace=folder / "workspace",
            role_id="astra_full_process_trial",
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

    def on_step(record, trace):
        del trace
        progress["operations"] += 1
        progress["last_action"] = deepcopy(record.action)
        print(
            json.dumps(
                {
                    "stage": progress["stage"],
                    "operations": progress["operations"],
                    "action": record.action,
                    "elapsed_s": round(time.monotonic() - started, 1),
                }
            ),
            flush=True,
        )

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
            campaign_resource_card=card(task),
            observation_noise_mode="keyed",
            observation_noise_namespace=NAMESPACE,
            step_callback=on_step,
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
        failure = {"type": type(exc).__name__, "message": str(exc)[:1200]}
    finally:
        if isinstance(agent, FullProcessAgent):
            agent.close()
    records = (
        load_jsonl(folder / "trajectory.jsonl") if (folder / "trajectory.jsonl").is_file() else []
    )
    summary = summarize(task, records)
    replay = (
        verify_records(records, tolerance=0.0).to_dict()
        if records
        else {"verified": False, "checked_steps": 0}
    )
    write(folder / "replay.json", replay)
    receipts = agent.provider_receipts() if isinstance(agent, FullProcessAgent) else []
    usage = agent.method_resource_usage() if isinstance(agent, FullProcessAgent) else {}
    write(folder / "receipts.json", receipts)
    result = {
        "task": task,
        "kind": kind,
        "failure": failure,
        "status": "completed" if summary["final_assays"] == 1 and failure is None else "failed",
        "elapsed_s": time.monotonic() - started,
        "exact_replay": replay.get("verified") is True,
        "replay_checked_steps": replay.get("checked_steps"),
        "summary": summary,
        "provider_usage": usage,
        "provider_final": [r.get("final_payload") for r in receipts],
    }
    result["execution_qualified"] = (
        result["status"] == "completed" and result["exact_replay"] and not summary["failures"]
    )
    write(folder / "result.json", result)
    progress["completed"] += 1
    print(
        json.dumps(
            {
                "stage": progress["stage"],
                "status": result["status"],
                "completed": progress["completed"],
                "total": 7,
                "quality": summary["quality_passed"],
                "failure": failure,
            }
        ),
        flush=True,
    )
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--phase", choices=("reference", "repair-reference", "agent", "all"), default="all"
    )
    args = parser.parse_args()
    root = args.output.resolve()
    root.mkdir(parents=True, exist_ok=True)
    previous = len(list(root.glob("*/*/result.json")))
    progress = {"stage": "starting", "completed": previous, "total": 7, "operations": 0}
    stop = threading.Event()
    started = time.monotonic()

    def heartbeat():
        while not stop.wait(30):
            elapsed = time.monotonic() - started
            done = progress["completed"]
            newly_done = done - previous
            print(
                json.dumps(
                    {
                        **progress,
                        "elapsed_s": round(elapsed, 1),
                        "units_per_min": round(newly_done * 60 / elapsed, 3),
                        "eta_s": round(elapsed * (7 - done) / newly_done) if newly_done else None,
                    }
                ),
                flush=True,
            )

    thread = threading.Thread(target=heartbeat, daemon=True)
    thread.start()
    try:
        if args.phase == "repair-reference":
            original = read(root / "reference" / TASKS[0] / "result.json")
            if "operation=dry" not in str(original.get("failure")):
                raise RuntimeError("correction is only for the retained dry reservation failure")
            execute(root, TASKS[0], "reference-corrected", progress)
        for task in TASKS:
            if args.phase in {"reference", "all"}:
                execute(root, task, "reference", progress)
        if args.phase in {"agent", "all"}:
            for task in TASKS:
                ref_path = root / "reference" / task / "result.json"
                if (
                    task == TASKS[0]
                    and (root / "reference-corrected" / task / "result.json").is_file()
                ):
                    ref_path = root / "reference-corrected" / task / "result.json"
                if not ref_path.is_file() or not read(ref_path)["execution_qualified"]:
                    write(
                        root / "not_started" / (task + ".json"),
                        {"task": task, "reason": "reference_execution_not_qualified"},
                    )
                    continue
                execute(root, task, "agent", progress)
    finally:
        stop.set()
        thread.join(timeout=2)
        results = [
            read(path)
            for kind in ("reference", "reference-corrected", "agent")
            for task in TASKS
            if (path := root / kind / task / "result.json").is_file()
        ]
        report = {
            "schema_version": "work-ii-astra-full-process-trial-1",
            "formal_result": False,
            "experiment_note": NOTE,
            "model": "gpt-6-astra",
            "reasoning_effort": "medium",
            "scheduled_reference": 4,
            "scheduled_agent": 3,
            "results": results,
            "not_started": [read(p) for p in (root / "not_started").glob("*.json")],
        }
        write(root / "summary.json", report)
        print(
            json.dumps({"summary": str(root / "summary.json"), "results": len(results)}), flush=True
        )


if __name__ == "__main__":
    main()
