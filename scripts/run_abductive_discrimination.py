"""Thirty fresh autonomous investigations in matched mechanistic worlds (W2-263).

The new block uses the existing physical runtime and exact replay. It does not
replace a previous cohort or retry an unfavourable/incomplete participant.
"""

from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import json
import subprocess
import sys
import threading
import time
from collections import Counter
from pathlib import Path

import gymnasium as gym
from scripts import run_inquiry_completion as inquiry
from scripts import run_research_formation as pool
from scripts import run_work_ii_eq_bounded_equilibrium_v2 as eq
from scripts.run_paper_case_notebooks import ROOT, case_folder, emit, live, read, write

NOTE = "workstreams/flagship_tasks/WORK_II_ABDUCTIVE_COMPLETION_20261016.md"
MODE = "abductive-discrimination-matched-worlds-30"
STAGES = ("K1", "Q", "K2")
REFERENCE_REPEATS = 5
K1 = inquiry.K1
Q = inquiry.Q
K2 = inquiry.K2
MEASUREMENT_DEFINITIONS = {
    "pH_normalized": "pH divided by 14",
    "acid_dissociation_fraction": ("free deprotonated acid fraction relative to total acid feed"),
    "precipitation_signal": "precipitated acid fraction relative to total acid feed",
}
BASE_SYSTEM = eq.v1.SYSTEM
BASE_PUBLIC_CONTEXT = inquiry.public_context
INITIAL_REFERENCE_OBSERVATIONS = None


def public_context(agent, current_packet):
    context = BASE_PUBLIC_CONTEXT(agent, current_packet)
    context["measurement_definitions"] = copy.deepcopy(MEASUREMENT_DEFINITIONS)
    if INITIAL_REFERENCE_OBSERVATIONS is not None:
        context["supplied_reference_observations"] = copy.deepcopy(INITIAL_REFERENCE_OBSERVATIONS)
    return context


def build_config():
    from chemworld.physchem.abductive_worlds import build_config as build

    config = build(eq.load_config())
    config["posttest_stages"] = list(STAGES)
    return config


def schedule(config):
    """Rotate pair order and alternate mechanism order before seeing outcomes."""
    worlds = config["worlds"]
    if len(worlds) != 10:
        raise ValueError("The fixed block needs exactly ten worlds")
    rows = []
    for repeat_index, repeat in enumerate(pool.REPEATS):
        pairs = list(range(5))
        offset = repeat_index * 2
        pairs = pairs[offset:] + pairs[:offset]
        for pair in pairs:
            members = worlds[2 * pair : 2 * pair + 2]
            if (repeat_index + pair) % 2:
                members = members[::-1]
            for world in members:
                wid = world["world_id"]
                rows.append(
                    {
                        "repeat": repeat,
                        "id": f"{wid}-Opaque",
                        "system": "EQ",
                        "world": wid,
                        "pair": f"P{pair + 1:02d}",
                        "mechanism": "A" if worlds.index(world) % 2 == 0 else "B",
                        "arm": "Opaque",
                        "cell": f"{wid}--Opaque",
                        "model": eq.PROVIDER["model"],
                        "batches": 12,
                    }
                )
    if len({(u["repeat"], u["id"]) for u in rows}) != 30:
        raise ValueError("Duplicate participant units")
    return rows


def configure(config, initial_reference_observations=None):
    """Process-local adapters; no core code or historical protocol is changed."""
    global INITIAL_REFERENCE_OBSERVATIONS
    INITIAL_REFERENCE_OBSERVATIONS = initial_reference_observations
    inquiry.public_context = public_context
    definition_text = "\nMeasurement definitions: " + json.dumps(MEASUREMENT_DEFINITIONS)
    inquiry.K1, inquiry.Q, inquiry.K2 = K1 + definition_text, Q + definition_text, K2
    eq.POSTTEST_STAGES = STAGES
    eq.SYSTEM = BASE_SYSTEM + definition_text
    eq.configure_provider_helpers(config)
    eq.EqFreeResearchAgent = inquiry.ResearchAgent
    eq.run_posttest = posttest


def posttest(agent, folder, private, stage, thread_id, progress, query_rows):
    if stage not in STAGES:
        raise ValueError(f"Unexpected assessment stage: {stage}")
    result = inquiry.posttest(agent, folder, private, stage, thread_id, progress, query_rows)
    receipt = read(private / stage / "receipt.json")
    result["usage"] = receipt.get("usage")
    result["method_resources"] = receipt.get("method_resources") or {
        "provider_usage": receipt.get("usage"),
        "numerics_budget": receipt.get("numerics_budget"),
        "numerics_attempts": receipt.get("numerics_attempts"),
        "elapsed_s": receipt.get("elapsed_s"),
    }
    write(folder / "sealed" / f"{stage}.json", result)
    return result


def transport_probe(root):
    """Two non-scientific turns through the production transport, outside the cohort."""
    root.mkdir(parents=True, exist_ok=False)
    home, workspace = root / "home", root / "workspace"
    home.mkdir()
    workspace.mkdir()
    environment = inquiry._prepare_codex_home(home, eq.PROVIDER)
    schema = workspace / "schema.json"
    write(schema, eq.posttest_schema("K1"))
    instructions = workspace / "instructions.md"
    instructions.write_text(
        "This is a transport check. Return the requested brief JSON report. "
        "Do not use laboratory, network, filesystem or other tools.",
        encoding="utf-8",
    )
    thread_id, results = None, []
    for stage in ("initial", "continued"):
        audit = root / f"{stage}-numerics.jsonl"
        command = eq.provider_shared.build_command(
            eq.PROVIDER,
            schema,
            workspace,
            audit=audit,
            thread_id=thread_id,
            provider_retries=0,
        )
        command += [
            "-c",
            "mcp_servers.chemworld_lab.enabled=false",
            "-c",
            f"mcp_servers.chemworld_lab.command={json.dumps(sys.executable)}",
            "-c",
            "mcp_servers.research_notebook.enabled=false",
            "-c",
            f"mcp_servers.research_notebook.command={json.dumps(sys.executable)}",
            "-c",
            f"model_instructions_file={json.dumps(instructions.as_posix())}",
        ]
        result = eq.shared.launch(
            command,
            f'Return JSON with report equal to "transport {stage} ok".',
            workspace,
            environment,
            root / stage,
            180,
            True,
            audit,
            {"stage": "transport-only", "turn": stage},
            numerics_budget=inquiry.FOLLOWUP_NUMERICS,
        )
        write(root / stage / "receipt.json", result)
        valid = (
            not result.get("failure")
            and isinstance(result.get("payload"), dict)
            and result["payload"].get("report") == f"transport {stage} ok"
            and bool(result.get("thread_id"))
            and (thread_id is None or thread_id == result["thread_id"])
        )
        results.append(
            {
                "stage": stage,
                "valid": valid,
                "failure": result.get("failure"),
                "elapsed_s": result.get("elapsed_s"),
                "resources": result.get("method_resources") or result.get("usage"),
            }
        )
        thread_id = result.get("thread_id")
        if not valid:
            break
    summary = {
        "provider": eq.PROVIDER,
        "turns": results,
        "passed": len(results) == 2 and all(r["valid"] for r in results),
        "scientific_data": False,
        "participant_sessions": 0,
    }
    write(root / "result.json", summary)
    emit(summary)
    return 0 if summary["passed"] else 1


def prepare(root, starter_root=None):
    config = build_config()
    rows = schedule(config)
    queries = eq.queries(config)
    # Record the already imported execution surface; do not hash prose or demand
    # repository cleanliness. The coordinator commits this surface once before launch.
    files = {Path(__file__).resolve(), ROOT / "uv.lock", ROOT / "pyproject.toml"}
    for module in list(sys.modules.values()):
        name = getattr(module, "__file__", None)
        if not name:
            continue
        path = Path(name).resolve()
        if path.suffix == ".py" and (
            path.is_relative_to(ROOT / "src") or path.is_relative_to(ROOT / "scripts")
        ):
            files.add(path)
    surface = {
        p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(files)
    }
    root.mkdir(parents=True, exist_ok=False)
    if starter_root is not None:
        for world in config["worlds"]:
            wid = world["world_id"]
            write(root / "starter-observations" / f"{wid}.json", read(starter_root / f"{wid}.json"))
    write(
        root / "design.json",
        {
            "mode": MODE,
            "experiment_note": NOTE,
            "schedule": rows,
            "eq_config": config,
            "worker_module": "scripts.run_abductive_discrimination",
            "concurrency": 4,
            "planned_sources": 30,
            "planned_source_batches": 360,
            "posttest_stages": list(STAGES),
            "planned_posttests": 90,
            "reference_repeats": REFERENCE_REPEATS,
            "planned_reference_batches": len(config["worlds"]) * len(queries) * REFERENCE_REPEATS,
            "planned_reference_trajectories": len(config["worlds"]) * REFERENCE_REPEATS,
            "source_retries": 0,
            "provider": eq.PROVIDER,
            "model_rng_seed": None,
            "runtime_surface": surface,
            "source_commit": subprocess.check_output(
                ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
            ).strip(),
            "source_system_prompt": BASE_SYSTEM
            + "\nMeasurement definitions: "
            + json.dumps(MEASUREMENT_DEFINITIONS),
            "evaluation_prompts": {
                "K1": K1 + "\nMeasurement definitions: " + json.dumps(MEASUREMENT_DEFINITIONS),
                "Q": Q + "\nMeasurement definitions: " + json.dumps(MEASUREMENT_DEFINITIONS),
                "K2": K2,
            },
            "measurement_definitions": MEASUREMENT_DEFINITIONS,
            "initial_reference_assays_per_session": 2,
            "initial_reference_source": str(starter_root) if starter_root else None,
            "truth_embargo": (
                "All heldout actions and reference truth hidden until source and K1 seal"
            ),
        },
    )
    for repeat in pool.REPEATS:
        write(root / repeat / "design.json", {"eq_config": config, "mode": MODE})


def check_public_contexts(root, config):
    """Capture before any provider or action, then require exact paired inputs."""
    contexts = {}
    for world in config["worlds"]:
        wid = world["world_id"]
        starter = root / "starter-observations" / f"{wid}.json"
        configure(config, read(starter) if starter.exists() else None)
        cell = {"cell_id": f"{wid}--Opaque", "world_id": wid, "goal": "characterization"}
        contexts[wid] = inquiry.capture_initial(config, cell, root / "public-contexts" / wid)
    matches = []
    for index in range(5):
        a, b = config["worlds"][index * 2 : index * 2 + 2]
        left, right = copy.deepcopy(contexts[a["world_id"]]), copy.deepcopy(contexts[b["world_id"]])
        starter_a = left.pop("supplied_reference_observations", None)
        starter_b = right.pop("supplied_reference_observations", None)
        # Independently created campaigns have fresh opaque instance IDs. They
        # carry no scientific information and remain in the raw public records.
        for context in (left, right):
            context.get("initial_public_state", {}).get("campaign_state", {}).pop(
                "campaign_id", None
            )
        same = left == right
        matches.append(
            {
                "pair": f"P{index + 1:02d}",
                "identical": same,
                "starter_observations_identical": starter_a == starter_b,
                "starter_observations_supplied": (starter_a is not None and starter_b is not None),
            }
        )
    report = {
        "pairs": matches,
        "all_identical": all(r["identical"] for r in matches),
        "excluded_from_scientific_matching": ["initial_public_state.campaign_state.campaign_id"],
    }
    write(root / "public-contexts/result.json", report)
    if not report["all_identical"]:
        raise RuntimeError("Mechanism identities change initial public scientific inputs")
    return report


def references(root, progress):
    design = read(root / "design.json")
    config = design["eq_config"]
    if not all(
        (root / "starter-observations" / f"{w['world_id']}.json").exists() for w in config["worlds"]
    ):
        raise RuntimeError("Two qualified actual reference assays per world are required")
    check_public_contexts(root, config)
    query_rows = eq.queries(config)
    actions = [a for q in query_rows for a in q["actions"]]
    truth, completed, operations, trajectories = {}, 0, 0, 0
    for world in config["worlds"]:
        wid = world["world_id"]
        truth[wid] = {q["query_id"]: [] for q in query_rows}
        for repeat in range(1, design["reference_repeats"] + 1):
            result = eq.reference_run(
                root / "references" / wid / f"repeat-{repeat}",
                actions,
                config=config,
                world=world,
                batches=12,
                observation_seed=eq.deterministic_seed("abductive-reference", repeat),
                observation_namespace=f"abductive-reference-r{repeat:02d}",
            )
            if (
                result["failure"]
                or result["rollbacks"]
                or len(result["batches"]) != 12
                or not result["exact_replay"]["verified"]
            ):
                raise RuntimeError(f"Reference execution/replay defect: {wid}/{repeat}")
            for q, batch in zip(query_rows, result["batches"], strict=True):
                truth[wid][q["query_id"]].append({m: batch["metrics"][m] for m in eq.METRICS})
            completed += 12
            operations += result["operation_attempts"]
            trajectories += 1
            progress.update(
                unit=f"{wid}/{repeat}", reference_batches=completed, reference_operations=operations
            )
            write(root / "references/progress.json", progress)
            emit(progress)
    write(root / "references/truth.json", {"EQ": truth})
    write(
        root / "references/complete.json",
        {
            "completed_batches": completed,
            "operations": operations,
            "trajectories": trajectories,
            "replay_verified": True,
            "public_inputs_matched": True,
        },
    )


def truth_captured_reference(folder, actions, *, config, world, observation_seed, namespace):
    """Replay fixed actions and capture evaluator-only premeasurement physical means."""
    means = []
    original_run_agent = eq.v1.run_agent

    class CaptureMeans(gym.Wrapper):
        def __init__(self, env):
            super().__init__(env)
            self.attempts = 0

        def step(self, action):
            self.attempts += 1
            base = self.unwrapped
            is_final = (
                action.get("operation") == "measure" and action.get("instrument") == "final_assay"
            )
            premeasurement_state = copy.deepcopy(base._state) if is_final else None
            output = self.env.step(action)
            info = output[-1]
            if is_final and info.get("transaction_status") == "committed":
                mean = base.observation_kernel._equilibrium_truth_values(premeasurement_state)
                means.append({"step": self.attempts, "metrics": {m: mean[m] for m in eq.METRICS}})
            return output

    def run_with_capture(*args, **kwargs):
        return original_run_agent(*args, **kwargs, env_wrapper=CaptureMeans)

    eq.v1.run_agent = run_with_capture
    try:
        result = eq.reference_run(
            folder,
            actions,
            config=config,
            world=world,
            batches=12,
            observation_seed=observation_seed,
            observation_namespace=namespace,
        )
    finally:
        eq.v1.run_agent = original_run_agent
    result["physical_means"] = means
    write(folder / "result.json", result)
    return result


def counterfactual(root, unit, config, source):
    from chemworld.physchem.abductive_worlds import ASSAY_STD

    trajectory = case_folder(root / unit["repeat"], unit) / "trajectory.jsonl"
    records = eq.load_jsonl(trajectory) if trajectory.exists() else []
    if not records:
        return {
            "status": "no_source_actions",
            "source_actions": 0,
            "participant_feedback": False,
            "matched_batches": [],
        }
    own_world = eq.world_by_id(config, unit["world"])
    partner_id = unit["world"].rsplit("-", 1)[0] + ("-B" if unit["mechanism"] == "A" else "-A")
    partner_world = eq.world_by_id(config, partner_id)
    actions = [r["action"] for r in records]
    output = {
        "source_actions": len(actions),
        "participant_feedback": False,
        "interpretation": "Fixed selected action sequence, not alternative policy behavior",
        "worlds": {},
        "matched_batches": [],
    }
    for label, world in (("own", own_world), ("partner", partner_world)):
        result = truth_captured_reference(
            root / "counterfactual" / unit["repeat"] / unit["id"] / label,
            actions,
            config=config,
            world=world,
            observation_seed=records[0]["observation_seed"],
            namespace=records[0]["observation_noise_namespace"],
        )
        result["all_source_actions_replayed"] = result["operation_attempts"] == len(actions)
        failure = result.get("failure") or {}
        result["expected_incomplete_prefix_end"] = (
            result["all_source_actions_replayed"]
            and source.get("source_status") != "completed"
            and failure.get("message") == "truth replay exhausted its frozen action plan"
        )
        output["worlds"][label] = result
    own, partner = output["worlds"]["own"], output["worlds"]["partner"]
    own_means = {r["step"]: r["metrics"] for r in own["physical_means"]}
    partner_means = {r["step"]: r["metrics"] for r in partner["physical_means"]}
    own_batches = {r["end_step"]: r for r in own["batches"]}
    partner_batches = {r["end_step"]: r for r in partner["batches"]}
    for step in sorted(own_means.keys() & partner_means.keys()):
        a, b = own_means[step], partner_means[step]
        output["matched_batches"].append(
            {
                "source_step": step,
                "source_ordinal": own_batches[step]["ordinal"],
                "own_mean": a,
                "partner_mean": b,
                "absolute_mean_gap": {m: abs(a[m] - b[m]) for m in eq.METRICS},
                "gap_in_assay_standard_deviations": {
                    m: abs(a[m] - b[m]) / ASSAY_STD[m] for m in eq.METRICS
                },
                "same_keyed_observed_difference": {
                    m: own_batches[step]["metrics"][m] - partner_batches[step]["metrics"][m]
                    for m in eq.METRICS
                },
            }
        )
    output["own_source_observations_identical"] = [b["metrics"] for b in own["batches"]] == [
        b["metrics"] for b in source.get("batches", [])
    ]
    own_records = eq.load_jsonl(
        root / "counterfactual" / unit["repeat"] / unit["id"] / "own/trajectory.jsonl"
    )
    compared_fields = ("action", "transaction_status", "rollback_reason", "observation")
    output["own_operation_outcomes_identical"] = [
        {k: r.get(k) for k in compared_fields} for r in records
    ] == [{k: r.get(k) for k in compared_fields} for r in own_records]
    output["status"] = (
        "completed"
        if all(
            r["all_source_actions_replayed"]
            and r["exact_replay"]["verified"]
            and (not r.get("failure") or r["expected_incomplete_prefix_end"])
            for r in (own, partner)
        )
        and output["own_source_observations_identical"]
        and output["own_operation_outcomes_identical"]
        else "retained_counterfactual_failure"
    )
    write(root / "counterfactual" / unit["repeat"] / unit["id"] / "summary.json", output)
    return output


def execute(root, unit, progress):
    config = read(root / "design.json")["eq_config"]
    configure(config, read(root / "starter-observations" / f"{unit['world']}.json"))
    if case_folder(root / unit["repeat"], unit).exists() or pool.result_path(root, unit).exists():
        raise FileExistsError("Participant already started; no retry or overwrite")
    cell = {
        "cell_id": unit["cell"],
        "world_id": unit["world"],
        "arm": "Opaque",
        "goal": "characterization",
    }
    result = eq.run_cell(
        root / unit["repeat"] / unit["id"], config, cell, progress, threading.Lock()
    )
    truth = read(root / "references/truth.json")["EQ"][unit["world"]]
    result["prediction_evaluation"] = eq.evaluate_predictions(
        result["posttests"].get("Q", {}).get("payload"), eq.queries(config), truth
    )
    result["posttest_chain_sealed"] = all(
        result.get("posttest_validation", {}).get(s, {}).get("valid") is True
        and not result.get("posttests", {}).get(s, {}).get("failure")
        for s in STAGES
    )
    result["status"] = (
        "completed"
        if result["source_status"] == "completed"
        and result["posttest_chain_sealed"]
        and not result.get("failure")
        else "retained_nonconforming"
    )
    result.update(pair=unit["pair"], mechanism=unit["mechanism"], repeat=unit["repeat"])
    progress.update(phase="sealed-action-sequence-counterfactual")
    result["counterfactual"] = counterfactual(root, unit, config, result)
    write(pool.result_path(root, unit), result)
    pool.validate_result(result)


def snapshot(root, active=(), *, started=None):
    design = read(root / "design.json")
    rows = []
    for unit in design["schedule"]:
        path = pool.result_path(root, unit)
        result = read(path) if path.exists() else {}
        key = (unit["repeat"], unit["id"])
        counts = live(root / unit["repeat"], unit) if key in active and not result else {}
        tests = result.get("posttests", {})
        sealed = [
            s
            for s in STAGES
            if tests.get(s, {}).get("payload")
            and not tests[s].get("failure")
            and result.get("posttest_validation", {}).get(s, {}).get("valid") is True
        ]
        rows.append(
            {
                **unit,
                "status": result.get("status", "running" if key in active else "not_started"),
                "completed_batches": len(result.get("batches", [])) + counts.get("batches", 0),
                "operations": result.get("operations", 0) + counts.get("operations", 0),
                "failure": result.get("failure"),
                "sealed_posttests": len(sealed),
                "missing_posttests": [s for s in STAGES if s not in sealed],
                "posttest_failures": {
                    s: t["failure"] for s, t in tests.items() if t.get("failure")
                },
                "exact_replay": result.get("exact_replay"),
                "rollbacks": result.get("rollbacks", []),
                "source_usage": result.get("source_usage"),
                "posttest_usage": {s: t.get("method_resources") for s, t in tests.items()},
                "prediction_evaluation": result.get("prediction_evaluation"),
                "counterfactual": result.get("counterfactual"),
                "elapsed_s": result.get("elapsed_s"),
            }
        )
    output = {
        "mode": MODE,
        "planned_sources": len(rows),
        "planned_source_batches": sum(u["batches"] for u in rows),
        "planned_posttests": len(rows) * len(STAGES),
        "planned_reference_batches": design["planned_reference_batches"],
        "terminal_sources": sum(r["status"] not in {"not_started", "running"} for r in rows),
        "completed_sources": sum(r["status"] == "completed" for r in rows),
        "completed_batches": sum(r["completed_batches"] for r in rows),
        "sealed_posttests": sum(r["sealed_posttests"] for r in rows),
        "active_units": [
            {k: r[k] for k in ("repeat", "id", "operations", "completed_batches")}
            for r in rows
            if (r["repeat"], r["id"]) in active
        ],
        "reference": read(root / "references/complete.json")
        if (root / "references/complete.json").exists()
        else None,
        "block_stop": read(root / "block-stop.json")
        if (root / "block-stop.json").exists()
        else None,
        "cases": rows,
    }
    if started is not None:
        elapsed = max(time.monotonic() - started, 1e-6)
        completed = output["completed_batches"]
        output.update(
            elapsed_s=round(elapsed),
            batches_per_minute=60 * completed / elapsed,
            batch_eta_s=elapsed / completed * (360 - completed) if completed else None,
        )
    write(root / "summary.json", output)
    return output


def export_report(root, report):
    summary = snapshot(root)
    report.mkdir(parents=True, exist_ok=True)
    write(report / "summary.json", summary)
    fields = [
        "repeat",
        "id",
        "pair",
        "mechanism",
        "status",
        "completed_batches",
        "operations",
        "sealed_posttests",
        "missing_posttests",
        "failure",
        "elapsed_s",
    ]
    with (report / "sessions.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        for row in summary["cases"]:
            writer.writerow(
                {
                    k: json.dumps(row[k]) if isinstance(row[k], (dict, list)) else row[k]
                    for k in fields
                }
            )
    statuses = dict(Counter(r["status"] for r in summary["cases"]))
    text = (
        "# Matched mechanistic worlds: execution summary\n\n"
        "This is a separate prospective cohort. Prediction scores do not by themselves establish "
        "explanation formation or mechanism discovery. Source notes and actual operations require "
        "proposition-level interpretation. All started sessions and failures are retained.\n\n"
        f"- Terminal sessions: {summary['terminal_sources']}/30.\n"
        f"- Complete source/assessment chains: {summary['completed_sources']}/30.\n"
        f"- Completed source assays: {summary['completed_batches']}/360.\n"
        f"- Valid sealed assessments: {summary['sealed_posttests']}/90.\n"
        f"- Status counts: {json.dumps(statuses)}.\n\n"
        "See `sessions.csv` for exact session denominators and failures, and `summary.json` "
        "for replay, source/posttest resources and prediction results. Mechanism A/B labels "
        "are evaluator metadata, never participant inputs. No controlled model sampling seed "
        "was available; repetitions are fresh sessions.\n"
    )
    (report / "REPORT.md").write_text(text, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--unit")
    parser.add_argument("--repeat")
    parser.add_argument("--prepare-only", action="store_true")
    parser.add_argument("--run-prepared", action="store_true")
    parser.add_argument("--summarize", action="store_true")
    parser.add_argument("--report", type=Path)
    parser.add_argument("--transport-probe", action="store_true")
    parser.add_argument("--starter-root", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    if args.transport_probe:
        return transport_probe(root)
    if args.summarize or args.report:
        if args.report:
            export_report(root, args.report)
        emit({k: v for k, v in snapshot(root).items() if k != "cases"})
        return 0
    if not args.unit:
        if not args.run_prepared:
            prepare(root, args.starter_root)
        if args.prepare_only:
            return 0
        pool.snapshot = snapshot
        return pool.coordinate_prepared(root)
    progress = {"stage": args.unit, "reference_batches": 0}
    stop = threading.Event()

    def heartbeat():
        while not stop.wait(30):
            emit(progress)

    threading.Thread(target=heartbeat, daemon=True).start()
    try:
        if args.unit == "references":
            references(root, progress)
        else:
            unit = next(
                u
                for u in read(root / "design.json")["schedule"]
                if u["id"] == args.unit and u["repeat"] == args.repeat
            )
            execute(root, unit, progress)
    finally:
        stop.set()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
