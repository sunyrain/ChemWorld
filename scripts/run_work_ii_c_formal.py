"""Crystallization calibration and a separately frozen five-world research block."""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib
import itertools
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path

import gymnasium as gym
import psutil
from scripts import run_work_ii_c_pilot as pilot
from scripts.run_work_ii_final_diagnostic import read, write

from chemworld.agent_interface import full_process_operational_state
from chemworld.agents.diagnostic_numerics import FOLLOWUP_NUMERICS
from chemworld.agents.experiment_codex_mcp import ChemWorldMCPServer
from chemworld.data.logging import load_jsonl
from chemworld.eval.runner import run_agent
from chemworld.eval.work_ii_truth import _FrozenTruthReplayAgent
from chemworld.runtime.full_process_contract import FULL_PROCESS_FREE_RESEARCH_CONTRACT
from chemworld.tasks import get_task

ROOT = Path(__file__).resolve().parents[1]
METRICS = pilot.METRICS
RESOLUTION = dict(zip(METRICS, (0.02, 0.01, 0.005, 0.10), strict=True))
NAMESPACE = "work-ii-c-formal-v1"
FACTORS = (
    "solvent",
    "seed",
    "cooling_history",
    "thermal_history",
    "continue_growth",
    "upstream_loading",
)
EXPORT_LOCK = threading.Lock()


def source_system(batches):
    return (
        pilot.SYSTEM.replace("Complete 12", f"Complete {batches}")
        .replace("with 12 extra", f"with {batches} extra")
        .replace("plus 12 final assays and 720", f"plus {batches} final assays and {60 * batches}")
    )


class FormalCAgent(pilot.CAgent):
    def __init__(self, *, batches, instructions=None, **kwargs):
        self.batches = batches
        self.instructions = instructions or source_system(batches)
        super().__init__(batches=batches, **kwargs)

    def reset(self, task_info, seed):
        super().reset(task_info, seed)
        self._task_contract["study_budget"] = {
            "complete_batches": self.batches,
            "extra_measurements": self.batches,
            "final_assays": self.batches,
            "operation_attempts": 60 * self.batches,
        }
        self._task_contract_manifest = self.workspace.publish_task_contract(self._task_contract)

    def _command(self, *, instructions_path, schema_path):
        command = super()._command(instructions_path=instructions_path, schema_path=schema_path)
        instructions_path.write_text(self.instructions, encoding="utf-8")
        (self.output / "source-instructions.txt").write_text(self.instructions, encoding="utf-8")
        return command


def process(*, solvent=3, seed=0.05, path=None, reagent=0.01, catalyst=1, volume=0.028):
    actions = pilot.recipe(solvent=solvent, seed=seed, path=path, reagent=reagent)
    actions = [a for a in actions if a.get("instrument") != "particle_size"]
    actions[0]["volume_L"] = volume
    actions[2]["catalyst"] = catalyst
    return actions


def gentle(*, end=278.15, segments=12, duration=14400):
    return [pilot.cool(300 + (end - 300) * i / segments, duration) for i in range(1, segments + 1)]


def reheat(temperature, duration):
    return {
        "operation": "heat",
        "target_temperature_K": temperature,
        "duration_s": duration,
        "stirring_speed_rpm": 600.0,
    }


def calibration_candidates():
    pairs = [
        ("solvent", "long", [process(solvent=s, path=gentle()) for s in (1, 3)]),
        (
            "solvent",
            "short",
            [
                process(solvent=s, seed=0.025, path=gentle(segments=4, duration=1800))
                for s in (1, 3)
            ],
        ),
        (
            "seed",
            "transient",
            [
                process(seed=s, path=[pilot.cool(294, 600), pilot.cool(288, 600)])
                for s in (0.001, 0.05)
            ],
        ),
        (
            "seed",
            "gentle",
            [
                process(seed=s, path=gentle(end=284, segments=8, duration=7200))
                for s in (0.003, 0.05)
            ],
        ),
        (
            "cooling_history",
            "transient",
            [
                process(seed=0.03, path=[pilot.cool(278.15, 3600)]),
                process(seed=0.03, path=[pilot.cool(278.15, 120), pilot.cool(278.15, 3480)]),
            ],
        ),
        (
            "cooling_history",
            "gentle",
            [
                process(path=gentle(segments=12, duration=7200)),
                process(path=[pilot.cool(278.15, 120), *[pilot.cool(278.15, 14380)] * 6]),
            ],
        ),
        (
            "thermal_history",
            "partial_dissolution",
            [
                process(seed=0.04, path=[pilot.cool(280, 1800), pilot.cool(280, 1800)]),
                process(
                    seed=0.04, path=[pilot.cool(280, 1800), reheat(315, 900), pilot.cool(280, 900)]
                ),
            ],
        ),
        (
            "thermal_history",
            "long_memory",
            [
                process(
                    path=[*gentle(end=285, segments=6, duration=14400), pilot.cool(285, 14400)]
                ),
                process(
                    path=[
                        *gentle(end=285, segments=6, duration=14400),
                        reheat(325, 7200),
                        pilot.cool(285, 7200),
                    ]
                ),
            ],
        ),
        (
            "continue_growth",
            "early",
            [
                process(seed=0.025, path=[pilot.cool(292, 60)]),
                process(seed=0.025, path=[pilot.cool(292, 60), pilot.cool(292, 7200)]),
            ],
        ),
        (
            "continue_growth",
            "late",
            [
                process(seed=0.045, path=gentle(end=287, segments=4, duration=3600)),
                process(
                    seed=0.045,
                    path=[*gentle(end=287, segments=4, duration=3600), pilot.cool(287, 14400)],
                ),
            ],
        ),
        (
            "upstream_loading",
            "gentle",
            [
                process(reagent=r, path=gentle(end=282, segments=8, duration=14400))
                for r in (0.004, 0.02)
            ],
        ),
        (
            "upstream_loading",
            "transient",
            [process(reagent=r, seed=0.02, path=[pilot.cool(286, 1200)]) for r in (0.005, 0.015)],
        ),
    ]
    return [
        {"id": f"D{i:02d}", "factor": factor, "variant": variant, "side": side, "actions": actions}
        for i, (factor, variant, side, actions) in enumerate(
            ((f, v, side, a) for f, v, pair in pairs for side, a in enumerate(pair)), 1
        )
    ]


def physics(
    agent,
    output,
    *,
    world_seed,
    arm,
    batches,
    observation_seed,
    callback,
    truths,
    envelope=None,
    diagnostics=None,
):
    envelope = batches if envelope is None else envelope
    return run_agent(
        env_id=get_task(pilot.TASK).env_id,
        agent=agent,
        task_id=pilot.TASK,
        world_split="public-test",
        objective="balanced",
        seed=world_seed,
        agent_seed=0,
        observation_seed=observation_seed,
        budget=60 * envelope,
        budget_override=60 * envelope,
        episode_mode_override="campaign" if batches > 1 else "single_experiment",
        campaign_resource_card=pilot.resource_card(batches, envelope=envelope),
        material_information=pilot.material(arm),
        crystallization_material_family_id=pilot.REACTION_CRYSTALLIZATION_LATENT_MATERIAL_FAMILY,
        full_process_contract_id=FULL_PROCESS_FREE_RESEARCH_CONTRACT,
        observation_noise_mode="keyed",
        observation_noise_namespace=NAMESPACE,
        output_path=output,
        step_callback=callback,
        env_wrapper=lambda env: pilot.TruthCapture(env, truths, diagnostics),
        method_resource_limits={
            "operation_limit": 60 * batches,
            "complete_experiment_limit": batches,
            "wall_time_limit_s": 300 * batches,
            "model_call_limit": 1,
            "input_token_limit": 16000000 * batches // 12,
            "uncached_input_token_limit": 4000000 * batches // 12,
            "output_token_limit": 192000 * batches // 12,
            "training_environment_step_limit": 0,
        }
        if isinstance(agent, FormalCAgent)
        else None,
    )


def fixed(
    root,
    actions,
    *,
    world_seed=17,
    arm="Opaque",
    batches=1,
    observation_seed=101,
    envelope=None,
    capture_diagnostics=False,
):
    root.mkdir(parents=True, exist_ok=False)
    write(root / "actions.json", actions)
    started = time.monotonic()
    truths, failure = [], None
    diagnostics = [] if capture_diagnostics else None
    progress = {
        "stage": root.name,
        "operations": 0,
        "completed_batches": 0,
        "planned_batches": batches,
    }
    stop = threading.Event()

    def heartbeat():
        while not stop.wait(30):
            print(
                json.dumps({**progress, "elapsed_s": round(time.monotonic() - started)}), flush=True
            )

    def callback(record, trace):
        del trace
        progress["operations"] += 1
        if record.info.get("transaction_status") != "committed":
            raise ValueError(f"illegal fixed action: {record.action}")
        progress["completed_batches"] += record.info.get("instrument") == "final_assay"

    thread = threading.Thread(target=heartbeat, daemon=True)
    thread.start()
    try:
        try:
            physics(
                _FrozenTruthReplayAgent(actions),
                root / "trajectory.jsonl",
                world_seed=world_seed,
                arm=arm,
                batches=batches,
                observation_seed=observation_seed,
                callback=callback,
                truths=truths,
                envelope=envelope,
                diagnostics=diagnostics,
            )
        except Exception as exc:
            failure = {"type": type(exc).__name__, "message": str(exc)}
        records = (
            load_jsonl(root / "trajectory.jsonl") if (root / "trajectory.jsonl").exists() else []
        )
        replay = pilot.ec.replay_with_progress(records, root.name)
        result = {
            "failure": failure,
            "truth": truths,
            "batches": pilot.ec.summaries(records),
            "operations": len(records),
            "exact_replay": replay,
            "elapsed_s": time.monotonic() - started,
            "world_instance": records[0].get("crystallization_material_instance_sha256")
            if records
            else None,
        }
        result["passed"] = (
            not failure and len(result["batches"]) == batches and replay.get("verified") is True
        )
        if diagnostics is not None:
            result["host_diagnostics"] = diagnostics
        write(root / "result.json", result)
        return result
    finally:
        stop.set()
        thread.join(timeout=2)


def coverage(truths):
    positive = sum(pilot.quality(t) for t in truths)
    contrasts = []
    for i in range(0, len(truths), 2):
        deltas = {m: truths[i + 1][m] - truths[i][m] for m in METRICS}
        contrasts.append(
            {
                "factor": FACTORS[i // 2],
                "deltas": deltas,
                "resolved": any(abs(deltas[m]) > RESOLUTION[m] for m in METRICS),
            }
        )
    return {
        "quality_positive": positive,
        "quality_negative": len(truths) - positive,
        "feasible": sum(pilot.quality(t) and t["crystal_yield"] >= 0.10 for t in truths),
        "resolved_pairs": sum(p["resolved"] for p in contrasts),
        "contrasts": contrasts,
    }


def select_pairs(candidates, results):
    options = []
    for factor in FACTORS:
        options.append(
            [
                [r for r in candidates if r["factor"] == factor and r["variant"] == v]
                for v in dict.fromkeys(r["variant"] for r in candidates if r["factor"] == factor)
            ]
        )
    ranked = []
    for pairs in itertools.product(*options):
        rows = [r for pair in pairs for r in pair]
        if not all(results[r["id"]]["passed"] for r in rows):
            continue
        if len({json.dumps(r["actions"], sort_keys=True) for r in rows}) != 12:
            continue
        truths = [results[r["id"]]["truth"][0] for r in rows]
        cov = coverage(truths)
        acceptable = (
            cov["quality_positive"] >= 3
            and cov["quality_negative"] >= 3
            and cov["resolved_pairs"] >= 4
            and cov["feasible"] > 0
        )
        strength = sum(
            min(abs(p["deltas"][m]) / RESOLUTION[m], 5) for p in cov["contrasts"] for m in METRICS
        )
        ranked.append(
            (
                (
                    acceptable,
                    cov["resolved_pairs"],
                    min(cov["quality_positive"], cov["quality_negative"]),
                    strength,
                ),
                rows,
                cov,
            )
        )
    if not ranked:
        return {"acceptable": False, "reason": "no complete unique candidate combination"}
    rank, rows, cov = max(ranked, key=lambda r: r[0])
    return {
        "acceptable": rank[0],
        "coverage": cov,
        "queries": [
            {
                "query_id": f"Q{i:02d}",
                "pair": r["factor"],
                "calibration_id": r["id"],
                "actions": r["actions"],
            }
            for i, r in enumerate(rows, 1)
        ],
    }


def calibrate(root, report):
    root.mkdir(parents=True, exist_ok=False)
    candidates = calibration_candidates()
    planned = len(candidates)
    write(
        root / "design.json",
        {
            "phase": "development",
            "world_seed": 17,
            "candidates": candidates,
            "resolution": RESOLUTION,
            "planned_new_batches": planned,
            "retained_batches": 0,
        },
    )
    results, started = {}, time.monotonic()
    for n, row in enumerate(candidates, 1):
        results[row["id"]] = fixed(root / row["id"], row["actions"])
        elapsed = time.monotonic() - started
        write(root / "results.json", results)
        print(
            json.dumps(
                {
                    "stage": "calibration",
                    "completed": n,
                    "total": planned,
                    "elapsed_s": round(elapsed),
                    "batches_per_hour": n * 3600 / elapsed,
                    "eta_s": round(elapsed / n * (planned - n)),
                }
            ),
            flush=True,
        )
    selected = select_pairs(candidates, results)
    write(root / "selection.json", selected)
    report.mkdir(parents=True, exist_ok=True)
    write(
        report / "calibration.json",
        {
            "development_only": True,
            "new_batches": planned,
            "retained_batches": 0,
            "candidates": candidates,
            "results": results,
            "selection": selected,
            "elapsed_s": time.monotonic() - started,
        },
    )
    lines = [
        "# Crystallization development calibration",
        "",
        f"All {len(candidates)} candidates retained: {planned} newly executed, "
        "Development world is excluded from formal worlds.",
        "",
        "| Candidate | Factor | Variant | Executed | Recovery | Purity | "
        "Size index | Fines | Quality |",
        "| --- | --- | --- | --- | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in candidates:
        r = results[row["id"]]
        t = r["truth"][0] if r["truth"] else {}
        lines.append(
            f"| {row['id']} | {row['factor']} | {row['variant']} | {r['passed']} | "
            + " | ".join(f"{t[m]:.6f}" if m in t else "missing" for m in METRICS)
            + f" | {pilot.quality(t)} |"
        )
    lines += ["", "## Development selection", "", "```json", json.dumps(selected, indent=2), "```"]
    (report / "CALIBRATION.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def evaluate(payload, truths, query_set):
    """Schema failures, predictive errors, ties and missing answers remain separate."""
    rows = payload.get("predictions", []) if isinstance(payload, dict) else []
    expected = [q["query_id"] for q in query_set]
    ids = [r.get("query_id") for r in rows if isinstance(r, dict)]
    if len(rows) != len(expected) or len(ids) != len(rows) or set(ids) != set(expected):
        return {"valid": False, "failure": "missing/duplicate/unknown query IDs"}
    by_id = {r["query_id"]: r for r in rows}
    failures, metrics, intervals = [], {}, {}
    for metric in METRICS:
        errors, scores, widths, covered = [], [], [], []
        for qid in expected:
            interval = by_id[qid].get(metric)
            if not isinstance(interval, dict):
                failures.append([qid, metric, "missing interval"])
                continue
            vals = [interval.get(k) for k in ("estimate", "lower80", "upper80")]
            if not all(type(v) in (int, float) and math.isfinite(v) for v in vals):
                failures.append([qid, metric, "nonfinite or missing number"])
                continue
            estimate, lo, hi = vals
            if not 0 <= lo <= estimate <= hi <= 1:
                failures.append([qid, metric, "invalid interval"])
                continue
            target = truths[qid][metric]
            intervals[qid, metric] = vals
            errors.append(abs(estimate - target))
            widths.append(hi - lo)
            covered.append(lo <= target <= hi)
            scores.append(hi - lo + 10 * max(lo - target, 0) + 10 * max(target - hi, 0))
        metrics[metric] = {
            "n": len(errors),
            "planned": len(expected),
            "mae": sum(errors) / len(errors) if errors else None,
            "coverage80": sum(covered) / len(covered) if covered else None,
            "interval_width": sum(widths) / len(widths) if widths else None,
            "interval_score80": sum(scores) / len(scores) if scores else None,
        }
    confusion = dict.fromkeys(
        ("true_positive", "false_positive", "true_negative", "false_negative"), 0
    )
    for qid in expected:
        predicted = by_id[qid].get("quality_feasible")
        if type(predicted) is not bool:
            failures.append([qid, "quality_feasible", "not boolean"])
            continue
        actual = pilot.quality(truths[qid])
        confusion[
            ("true_" if predicted == actual else "false_")
            + ("positive" if predicted else "negative")
        ] += 1
    positive = confusion["true_positive"] + confusion["false_negative"]
    negative = confusion["true_negative"] + confusion["false_positive"]
    balanced = (
        (confusion["true_positive"] / positive + confusion["true_negative"] / negative) / 2
        if positive and negative
        else None
    )
    contrasts = []
    for i in range(0, len(expected), 2):
        a, b = expected[i : i + 2]
        for metric in METRICS:
            if (a, metric) not in intervals or (b, metric) not in intervals:
                continue
            actual = truths[b][metric] - truths[a][metric]
            predicted = intervals[b, metric][0] - intervals[a, metric][0]
            resolution = RESOLUTION[metric]

            def sign(x, threshold=resolution):
                return 0 if abs(x) <= threshold else (1 if x > 0 else -1)

            contrasts.append(
                {
                    "factor": query_set[i]["pair"],
                    "metric": metric,
                    "true_delta": actual,
                    "predicted_delta": predicted,
                    "absolute_delta_error": abs(actual - predicted),
                    "resolved": abs(actual) > resolution,
                    "direction_correct": sign(actual) == sign(predicted),
                }
            )
    return {
        "valid": not failures,
        "failures": failures,
        "metrics": metrics,
        "quality": {**confusion, "balanced_accuracy": balanced},
        "contrasts": contrasts,
        "resolved_direction_n": sum(c["resolved"] for c in contrasts),
        "resolved_direction_correct": sum(
            c["resolved"] and c["direction_correct"] for c in contrasts
        ),
        "tie_n": sum(not c["resolved"] for c in contrasts),
        "tie_correct": sum(not c["resolved"] and c["direction_correct"] for c in contrasts),
    }


def recipe_features(actions):
    values = dict.fromkeys(
        ("reagent", "volume", "seed", "heat_time", "cool_time", "min_temp", "max_temp", "segments"),
        0.0,
    )
    solvent = catalyst = 0
    temperatures = []
    for a in actions:
        op = a.get("operation")
        if op == "add_solvent":
            values["volume"] += a.get("volume_L", 0) / 0.08
            solvent = int(a.get("solvent", 0))
        elif op == "add_catalyst":
            catalyst = int(a.get("catalyst", 0))
        elif op == "add_reagent":
            values["reagent"] += a.get("amount_mol", 0) / 0.04
        elif op == "seed_crystals":
            values["seed"] += a.get("seed_mass_g", 0) / 0.05
        elif op in {"heat", "cool_crystallize"}:
            values["heat_time" if op == "heat" else "cool_time"] += a.get("duration_s", 0) / 172800
            values["segments"] += 1 / 12
            temperatures.append(a.get("target_temperature_K", 300))
    if temperatures:
        values["min_temp"] = (min(temperatures) - 250) / 180
        values["max_temp"] = (max(temperatures) - 250) / 180
    return [
        *values.values(),
        *[float(solvent == i) for i in range(4)],
        *[float(catalyst == i) for i in range(4)],
    ]


def public_baselines(records, queries, truths):
    """Fit exclusively to a source's public final observations, never reference outcomes."""
    batches = pilot.ec.summaries(records)
    eligible = [
        b for b in batches if all(type(b["metrics"].get(m)) in (int, float) for m in METRICS)
    ]
    if not eligible:
        return {"training_batches": 0, "available": False}
    mean = {m: sum(b["metrics"][m] for b in eligible) / len(eligible) for m in METRICS}
    errors = {name: {m: [] for m in METRICS} for name in ("public_mean", "public_nearest_neighbor")}
    features = [
        recipe_features(pilot.committed_recipe(records, b["lifecycle_index"])["actions"])
        for b in eligible
    ]
    for q in queries:
        feature = recipe_features(q["actions"])
        index = min(
            range(len(features)),
            key=lambda i: sum((a - b) ** 2 for a, b in zip(feature, features[i], strict=True)),
        )
        for name, prediction in (
            ("public_mean", mean),
            ("public_nearest_neighbor", eligible[index]["metrics"]),
        ):
            for metric in METRICS:
                errors[name][metric].append(abs(prediction[metric] - truths[q["query_id"]][metric]))
    return {
        "training_batches": len(eligible),
        "available": True,
        "mae": {n: {m: sum(v) / len(v) for m, v in rows.items()} for n, rows in errors.items()},
    }


def configure(root, calibration, budgets):
    selection = read(calibration / "selection.json")
    if not selection.get("acceptable"):
        raise ValueError(
            "Development coverage is insufficient; retain and redesign before formal launch"
        )
    root.mkdir(parents=True, exist_ok=False)
    rows = []
    for seed in range(5):
        for budget in budgets if seed % 2 == 0 else budgets[::-1]:
            arms = list(pilot.ARMS)
            arms = arms[seed % 3 :] + arms[: seed % 3]
            for arm in arms:
                rows.append(
                    {
                        "id": f"C-W{seed + 1:02d}-B{budget}-E-{arm}",
                        "world_seed": seed,
                        "batches": budget,
                        "arm": arm,
                    }
                )
    design = {
        "protocol": "c-quality-recovery-formal-v1-en",
        "mode": "pre-freeze",
        "model": pilot.ec.PROVIDER,
        "budgets": budgets,
        "schedule": rows,
        "queries": selection["queries"],
        "calibration_root": str(calibration),
        "K1": pilot.K1,
        "Q": pilot.prediction_question(
            [{"query_id": q["query_id"], "actions": q["actions"]} for q in selection["queries"]]
        ),
        "K2": pilot.K2,
        "systems": {str(b): source_system(b) for b in budgets},
        "posttest_numerics": FOLLOWUP_NUMERICS.to_dict(),
        "resolution": RESOLUTION,
        "planned_sources": len(rows),
        "planned_batches": sum(r["batches"] for r in rows),
        "planned_posttests": 3 * len(rows),
        "planned_retests": len(rows),
        "formal_validation_batches": 75,
        "automatic_retries": 0,
    }
    write(root / "design.json", design)


def check_public(arm, seed, batches):
    env = gym.make(
        "ChemWorld",
        task_id=pilot.TASK,
        seed=seed,
        material_information=pilot.material(arm),
        crystallization_material_family_id=pilot.REACTION_CRYSTALLIZATION_LATENT_MATERIAL_FAMILY,
        full_process_contract_id=FULL_PROCESS_FREE_RESEARCH_CONTRACT,
        campaign_resource_card=pilot.resource_card(batches, envelope=batches),
        budget_override=60 * batches,
    )
    with tempfile.TemporaryDirectory(prefix="chemworld-research-") as directory:
        home = Path(directory)
        agent = FormalCAgent(
            batches=batches,
            goal="optimization",
            home_root=home,
            output=home,
            workspace=home / "laboratory",
            role_id="free_research",
        )
        try:
            env.reset(seed=seed)
            agent.reset(env.unwrapped.task_info(), 0)
            agent.workspace.start_session(
                session_id="reference-check", response_timeout_s=10, session_scope="campaign"
            )
            reply = ChemWorldMCPServer(agent.workspace.root)._call_tool("material_information", {})
            if reply.get("isError"):
                raise ValueError("material tool failed")
            payload = json.loads(reply["content"][0]["text"])
            operational = full_process_operational_state(env.unwrapped, {})
            metric_texts = (
                source_system(batches),
                pilot.prediction_question([]),
                agent._task_contract["prediction_metrics"]["crystal_yield"],
                operational["sampling_contract"],
            )
            return {
                "payload": payload,
                "contract": agent._task_contract,
                "anonymous": pilot.anonymous(payload),
                "particle_available": "particle_size"
                in agent._task_contract["instrument_contracts"],
                "metric_contract_consistent": all(
                    "target product present before separation" in text for text in metric_texts
                ),
                "operational_state": operational,
            }
        finally:
            agent.close()
            env.close()


def qualify(root, report):
    design = read(root / "design.json")
    output = root / "qualification"
    output.mkdir(parents=True, exist_ok=False)
    write(output / "result.json", {"worlds": {}, "status": "running", "passed": False})
    results, started = {}, time.monotonic()
    query_actions = [a for q in design["queries"] for a in q["actions"]]
    probe = process(path=[pilot.cool(285, 300)])
    probe.insert(-3, copy.deepcopy(pilot.PARTICLE))
    # One nondestructive particle reading tests the new C instrument boundary.
    # Sampling and arbitrary source measurement allocation have separate real-path tests.
    for seed in range(5):
        world = output / f"W{seed + 1:02d}"
        public = {
            f"{b}-{a}": check_public(a, seed, b) for b in design["budgets"] for a in pilot.ARMS
        }
        write(world / "public.json", public)
        references = fixed(world / "queries", query_actions, world_seed=seed, batches=12)
        mappings = {
            a: fixed(world / f"mapping-{a}", probe, world_seed=seed, arm=a) for a in pilot.ARMS
        }
        cov = coverage(references["truth"]) if len(references["truth"]) == 12 else {}
        checks = {
            "metric_contract_consistent": all(
                p["metric_contract_consistent"] for p in public.values()
            ),
            "public_anonymous": all(
                p["anonymous"] and p["particle_available"] for p in public.values()
            ),
            "opaque_no_dossier": all(
                public[f"{b}-Opaque"]["payload"]["material_information"]["dossier"] is None
                for b in design["budgets"]
            ),
            "budget_delivery": all(
                p["contract"]["study_budget"]["complete_batches"] == int(key.split("-")[0])
                for key, p in public.items()
            ),
            "exact_execution": references["passed"] and all(r["passed"] for r in mappings.values()),
            "same_physics": all(
                r["truth"] == mappings["Opaque"]["truth"] for r in mappings.values()
            ),
            "same_observations": all(
                r["batches"]
                and r["batches"][0]["metrics"] == mappings["Opaque"]["batches"][0]["metrics"]
                for r in mappings.values()
            ),
            "feasible_witness": cov.get("feasible", 0) > 0,
            "quality_coverage": cov.get("quality_positive", 0) >= 3
            and cov.get("quality_negative", 0) >= 3,
            "factor_coverage": cov.get("resolved_pairs", 0) >= 4,
        }
        results[str(seed)] = {
            "checks": checks,
            "coverage": cov,
            "reference": references,
            "mapping": mappings,
            "passed": all(checks.values()),
        }
        write(output / "result.json", {"worlds": results, "status": "running", "passed": False})
        elapsed = time.monotonic() - started
        print(
            json.dumps(
                {
                    "stage": "qualification",
                    "completed_worlds": len(results),
                    "total_worlds": 5,
                    "elapsed_s": round(elapsed),
                    "eta_s": round(elapsed / len(results) * (5 - len(results))),
                }
            ),
            flush=True,
        )
    distinct = len({r["reference"]["world_instance"] for r in results.values()}) == 5
    result = {
        "worlds": results,
        "status": "completed",
        "distinct_material_worlds": distinct,
        "passed": distinct and all(r["passed"] for r in results.values()),
        "elapsed_s": time.monotonic() - started,
    }
    write(output / "result.json", result)
    report.mkdir(parents=True, exist_ok=True)
    # Keep individual held-out outcomes in the private execution root until sources seal.
    write(
        report / "qualification.json",
        {
            "status": result["status"],
            "passed": result["passed"],
            "distinct_material_worlds": distinct,
            "worlds": {
                f"C-W{int(k) + 1:02d}": {"checks": r["checks"], "passed": r["passed"]}
                for k, r in results.items()
            },
            "elapsed_s": result["elapsed_s"],
        },
    )


def source(root, cell, progress):
    design = read(root / "design.json")
    folder = root / "sources" / cell["id"]
    folder.mkdir(parents=True, exist_ok=False)
    write(folder / "attempt.json", {"started_epoch": time.time(), "attempt": 1})
    started = time.monotonic()
    budget, arm = cell["batches"], cell["arm"]
    home = Path(tempfile.mkdtemp(prefix="chemworld-research-"))
    write(folder / "runtime-location.json", {"home": str(home)})
    result = {
        "id": cell["id"],
        "arm": arm,
        "batches_budget": budget,
        "status": "running",
        "failure": None,
        "posttests": {},
    }
    write(folder / "result.json", result)
    progress.update(
        stage=cell["id"], phase="source", operations=0, batches=0, planned_batches=budget
    )
    agent = FormalCAgent(
        batches=budget,
        instructions=design["systems"][str(budget)],
        goal="optimization",
        home_root=home,
        output=folder,
        workspace=home / "laboratory",
        role_id="free_research",
        request_timeout_s=1200,
        finalization_timeout_s=300,
        session_wall_time_limit_s=300 * budget,
        max_recovered_mcp_tool_failures=12,
        max_consecutive_mcp_tool_failures=6,
        max_provider_error_events=0,
        pre_action_restart_limit=0,
        accepted_turn_continuation_limit=0,
        provider_process_attempt_limit=1,
        max_initial_prompt_bytes=262144,
        max_tool_output_bytes=131072,
        history_event_limit=60 * budget,
        history_byte_limit=2097152 * budget // 12,
    )
    truths = []

    def callback(record, trace):
        del trace
        progress["operations"] += 1
        if (
            record.info.get("transaction_status") == "committed"
            and record.info.get("instrument") == "final_assay"
        ):
            progress["batches"] += 1

    try:
        physics(
            agent,
            folder / "trajectory.jsonl",
            world_seed=cell["world_seed"],
            arm=arm,
            batches=budget,
            observation_seed=0,
            callback=callback,
            truths=truths,
        )
    except Exception as exc:
        result["failure"] = {"stage": "source", "type": type(exc).__name__, "message": str(exc)}
    finally:
        agent.close()
    records = (
        load_jsonl(folder / "trajectory.jsonl") if (folder / "trajectory.jsonl").exists() else []
    )
    shutil.copytree(agent.workspace.root, folder / "workspace")
    receipts = agent.provider_receipts()
    write(folder / "source-receipts.json", receipts)
    last = receipts[-1] if receipts else {}
    result["source"] = {
        "batches": pilot.ec.summaries(records),
        "truth": truths,
        "operations": len(records),
        "elapsed_s": time.monotonic() - started,
        "usage": agent.method_resource_usage(),
        "exact_replay": pilot.ec.replay_with_progress(records, cell["id"]),
        "rollbacks": [
            {"step": r["step"], "action": r["action"], "reason": r.get("rollback_reason")}
            for r in records
            if r.get("transaction_status") != "committed"
        ],
    }
    result["recommendation"] = last.get("final_recommendation")
    write(folder / "result.json", result)
    try:
        if pilot.ec.posttest_context_available(last):
            for stage in ("K1", "Q", "K2"):
                progress["phase"] = stage
                turn = pilot.posttest(agent, folder, stage, last["thread_id"], progress, design)
                result["posttests"][stage] = turn
                write(folder / "result.json", result)
                if turn.get("failure"):
                    result["failure"] = result["failure"] or {
                        "stage": stage,
                        "message": turn["failure"],
                    }
                    break
        else:
            result["failure"] = result["failure"] or {
                "stage": "handoff",
                "message": "no intact terminal source context",
            }
        references = read(
            root / "qualification" / f"W{cell['world_seed'] + 1:02d}" / "queries" / "result.json"
        )
        truth = dict(
            zip([q["query_id"] for q in design["queries"]], references["truth"], strict=True)
        )
        result["prediction_evaluation"] = evaluate(
            result["posttests"].get("Q", {}).get("payload"), truth, design["queries"]
        )
        result["public_baselines"] = public_baselines(records, design["queries"], truth)
        selected = (result["recommendation"] or {}).get("selected_experiment_index")
        batch = next(
            (b for b in result["source"]["batches"] if b["lifecycle_index"] == selected), None
        )
        if batch:
            progress["phase"] = "recommendation_retest"
            result["recommendation_recipe"] = pilot.committed_recipe(records, selected)
            result["recommendation_retest"] = fixed(
                folder / "recommendation-retest",
                result["recommendation_recipe"]["actions"],
                world_seed=cell["world_seed"],
                arm=arm,
                observation_seed=303,
                envelope=budget,
            )
        result["status"] = (
            "completed"
            if (
                len(result["source"]["batches"]) == budget
                and not result["failure"]
                and result["source"]["exact_replay"].get("verified") is True
                and len(result["posttests"]) == 3
                and result.get("recommendation_retest", {}).get("passed")
            )
            else "failed"
        )
    except Exception as exc:
        result["failure"] = result["failure"] or {
            "stage": progress["phase"],
            "type": type(exc).__name__,
            "message": str(exc),
        }
        result["status"] = "failed"
    result["elapsed_s"] = time.monotonic() - started
    result["tokens"] = pilot.token_accounting(result)
    write(folder / "result.json", result)
    return result


def read_live_records(path):
    if not path.exists():
        return []
    records = []
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError:
            # Only the trailing in-flight append may be incomplete; sealed replay is stricter.
            break
    return records


def export(root, report):
    with EXPORT_LOCK:
        return _export(root, report)


def _export(root, report):
    design = read(root / "design.json")
    qualification_path = root / "qualification" / "result.json"
    qualification = read(qualification_path) if qualification_path.exists() else {}
    controller_path = root / "controller-status.json"
    controller = read(controller_path) if controller_path.exists() else {}
    phase = (
        controller["stage"]
        if controller.get("stage") in {"completed", "ended_with_incomplete_chains"}
        else "interrupted"
        if controller.get("stage") == "interrupted"
        or (
            controller.get("stage") in {"qualification", "sources"}
            and not controller_alive(controller)
        )
        else "sources"
        if qualification.get("passed")
        else "qualification_failed"
        if qualification.get("status") == "completed"
        else "qualification_running"
        if qualification.get("status") == "running"
        else "qualification_pending"
        if (root / "release.json").exists()
        else "awaiting_freeze"
    )
    rows = []
    for cell in design["schedule"]:
        folder = root / "sources" / cell["id"]
        result = (
            read(folder / "result.json")
            if (folder / "result.json").exists()
            else {
                "id": cell["id"],
                "arm": cell["arm"],
                "batches_budget": cell["batches"],
                "status": "not_started",
                "posttests": {},
            }
        )
        if result["status"] == "running":
            records = read_live_records(folder / "trajectory.jsonl")
            result["live_batches"] = len(pilot.ec.summaries(records))
            result["live_operations"] = len(records)
        result["posttests"] = {
            stage: {
                k: t.get(k)
                for k in (
                    "payload",
                    "failure",
                    "elapsed_s",
                    "usage",
                    "numerics_budget",
                    "numerics_attempts",
                )
            }
            for stage, t in result["posttests"].items()
        }
        rows.append(result)
    summary = {
        "phase": phase,
        "controller": controller,
        "retained_prior_attempt": read(root / "prior-attempt.json")
        if (root / "prior-attempt.json").exists()
        else None,
        "qualification_completed_worlds": len(qualification.get("worlds", {})),
        "qualification_world_checks": {
            f"C-W{int(key) + 1:02d}": {
                "passed": world["passed"],
                "failed_checks": [name for name, passed in world["checks"].items() if not passed],
                "execution_failure": world["reference"].get("failure"),
            }
            for key, world in qualification.get("worlds", {}).items()
        },
        "protocol": design["protocol"],
        "planned_sources": len(rows),
        "started_sources": sum(r["status"] != "not_started" for r in rows),
        "completed_chains": sum(r["status"] == "completed" for r in rows),
        "failed_sources": sum(r["status"] == "failed" for r in rows),
        "planned_batches": design["planned_batches"],
        "sealed_batches": sum(len(r.get("source", {}).get("batches", [])) for r in rows),
        "live_unsealed_batches": sum(r.get("live_batches", 0) for r in rows if "source" not in r),
        "planned_posttests": design["planned_posttests"],
        "completed_posttests": sum(
            bool(t.get("payload")) and not t.get("failure")
            for r in rows
            for t in r["posttests"].values()
        ),
        "results": rows,
    }
    report.mkdir(parents=True, exist_ok=True)
    write(report / "summary.json", summary)
    lines = [
        "# Crystallization formal experiment",
        "",
        f"Phase: {phase}.",
        "",
        f"Started: {summary['started_sources']}/{len(rows)}; "
        f"complete chains: {summary['completed_chains']}/{len(rows)}; "
        f"failures: {summary['failed_sources']}.",
        f"Sealed batches: {summary['sealed_batches']}/{summary['planned_batches']}; "
        f"additional live unsealed batches: {summary['live_unsealed_batches']}. "
        f"Posttests: {summary['completed_posttests']}/{summary['planned_posttests']}.",
        "",
        "| Cell | Status | Batches | K1/Q/K2 |",
        "| --- | --- | ---: | ---: |",
    ]
    if summary["retained_prior_attempt"]:
        prior = summary["retained_prior_attempt"]
        lines[7:7] = [
            f"Additional interrupted-attempt consumption: {prior['final_assays']} reference "
            f"final assays, {prior['operations']} operations, "
            f"{prior['provider_sources']} model sources. "
            "These do not count as sealed qualification units.",
            "",
        ]
    details = [
        f"Qualification world results sealed: {summary['qualification_completed_worlds']}/5. "
        "A sealed failure is not a qualified world.",
        "",
    ]
    if controller.get("stage") == "interrupted" and "operations" in controller:
        details.extend(
            [
                f"This interrupted attempt retains {controller['operations']} reference operations "
                f"and {controller['final_assays']} final assays. "
                f"Reason: {controller.get('reason', '')}",
                "",
            ]
        )
    for world, result in summary["qualification_world_checks"].items():
        failed = ", ".join(result["failed_checks"]) or "none"
        details.append(f"- {world}: passed={result['passed']}; failed checks: {failed}.")
    if summary["qualification_world_checks"]:
        details.append("")
    lines[7:7] = details
    for row in rows:
        batches = row.get("live_batches", len(row.get("source", {}).get("batches", [])))
        n = sum(bool(t.get("payload")) and not t.get("failure") for t in row["posttests"].values())
        lines.append(
            f"| [{row['id']}]({row['id']}.md) | {row['status']} | "
            f"{batches}/{row['batches_budget']} | {n}/3 |"
        )
        details = [f"# {row['id']}", "", f"Status: {row['status']}", ""]
        for batch in row.get("source", {}).get("batches", []):
            details += [
                f"## Batch {batch['ordinal']}",
                "",
                "```json",
                json.dumps(batch, indent=2),
                "```",
                "",
            ]
        for stage in ("K1", "Q", "K2"):
            details += [
                f"## {stage}",
                "",
                "```json",
                json.dumps(row["posttests"].get(stage), indent=2),
                "```",
                "",
            ]
        details += [
            "## Evaluation and accounting",
            "",
            "```json",
            json.dumps(
                {
                    k: row.get(k)
                    for k in (
                        "failure",
                        "recommendation",
                        "recommendation_recipe",
                        "prediction_evaluation",
                        "public_baselines",
                        "tokens",
                        "elapsed_s",
                    )
                },
                indent=2,
            ),
            "```",
        ]
        (report / f"{row['id']}.md").write_text("\n".join(details) + "\n", encoding="utf-8")
    lines += [
        "",
        "Scientific infeasibility is retained separately from execution failure. "
        "Query truth is never returned to model sessions.",
    ]
    (report / "REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return summary


def controller_alive(state):
    """Check process identity, not a persisted 'running' string or a recycled PID."""
    try:
        process = psutil.Process(state["pid"])
        return process.is_running() and process.create_time() == state["process_created"]
    except (KeyError, psutil.NoSuchProcess, psutil.AccessDenied):
        return False


def detached_process(command, log):
    if sys.platform == "win32":
        # Launch through the OS service: child-tree cleanup can defeat job breakaway.
        helper = Path(tempfile.mkdtemp(prefix="chemworld-detached-")) / "redirect.py"
        helper.write_text(
            "import subprocess,sys\n"
            "with open(sys.argv[1], 'ab', buffering=0) as log:\n"
            " result=subprocess.run(sys.argv[2:],stdin=subprocess.DEVNULL,"
            "stdout=log,stderr=subprocess.STDOUT)\n"
            "raise SystemExit(result.returncode)\n",
            encoding="utf-8",
        )
        uv = shutil.which("uv")
        if not uv:
            raise RuntimeError("Locked-environment launcher uv is unavailable")
        uv = str(Path(uv).resolve())
        command = [shutil.which(command[0]) or command[0], *command[1:]]
        specification = {
            "command": subprocess.list2cmdline(
                [uv, "run", "--no-sync", "python", str(helper), str(log.resolve()), *command]
            ),
            "cwd": str(ROOT),
        }
        powershell = (
            "$ErrorActionPreference='Stop'; "
            "$spec=$env:CHEMWORLD_DETACHED_LAUNCH | ConvertFrom-Json; "
            "$startup=New-CimInstance -ClassName Win32_ProcessStartup -ClientOnly "
            "-Property @{ShowWindow=[uint16]0}; "
            "Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments "
            "@{CommandLine=$spec.command;CurrentDirectory=$spec.cwd;"
            "ProcessStartupInformation=$startup} | "
            "Select-Object ProcessId,ReturnValue | ConvertTo-Json -Compress"
        )
        reply = subprocess.run(
            ["powershell", "-NoProfile", "-NonInteractive", "-Command", powershell],
            env={**os.environ, "CHEMWORLD_DETACHED_LAUNCH": json.dumps(specification)},
            capture_output=True,
            text=True,
            check=True,
            timeout=30,
        )
        receipt = json.loads(reply.stdout)
        if receipt["ReturnValue"] != 0:
            raise RuntimeError(f"OS process service rejected launch: {receipt}")
        return psutil.Process(receipt["ProcessId"])
    options = {
        "cwd": ROOT,
        "stdin": subprocess.DEVNULL,
        "close_fds": True,
        "start_new_session": True,
    }
    with log.open("ab") as output:
        return subprocess.Popen(command, stdout=output, stderr=output, **options)


def launch_pipeline(root, report):
    verify_frozen(root)
    if (root / "controller-launch.json").exists() or (root / "qualification").exists():
        raise ValueError("This attempt already started; diagnose retained data before recovery")
    command = [
        "uv",
        "run",
        "--no-sync",
        "python",
        "-m",
        "scripts.run_work_ii_c_formal",
        "--root",
        str(root),
        "--report",
        str(report),
        "--phase",
        "pipeline",
    ]
    process = detached_process(command, root / "controller.log")
    receipt = {
        "pid": process.pid,
        "process_created": psutil.Process(process.pid).create_time(),
        "command": command,
        "launch_method": "windows_process_service" if sys.platform == "win32" else "new_session",
    }
    write(root / "controller-launch.json", receipt)
    print(json.dumps(receipt), flush=True)


def pipeline(root, report):
    verify_frozen(root)
    state = {
        "pid": os.getpid(),
        "process_created": psutil.Process().create_time(),
        "stage": "qualification",
        "started_epoch": time.time(),
    }
    stop = threading.Event()

    def emit():
        payload = {**state, "epoch": time.time()}
        temporary = root / "controller-status.tmp"
        write(temporary, payload)
        temporary.replace(root / "controller-status.json")
        export(root, report)
        print(json.dumps(payload), flush=True)

    def heartbeat():
        while not stop.wait(30):
            emit()

    emit()
    thread = threading.Thread(target=heartbeat, daemon=True)
    thread.start()
    try:
        qualify(root, report)
        if not read(root / "qualification/result.json")["passed"]:
            state["stage"] = "held_after_qualification"
            return
        state["stage"] = "sources"
        run(root, report)
        summary = export(root, report)
        state["stage"] = (
            "completed"
            if summary["completed_chains"] == summary["planned_sources"]
            else "ended_with_incomplete_chains"
        )
    except BaseException as exc:
        state.update(stage="interrupted", failure={"type": type(exc).__name__, "message": str(exc)})
        raise
    finally:
        stop.set()
        thread.join(timeout=10)
        emit()


def runtime_surface():
    files = {Path(__file__).resolve(), ROOT / "uv.lock", ROOT / "pyproject.toml"}
    for module in list(sys.modules.values()):
        filename = getattr(module, "__file__", None)
        if not filename:
            continue
        path = Path(filename).resolve()
        if path.suffix == ".py" and (
            path.is_relative_to(ROOT / "src") or path.is_relative_to(ROOT / "scripts")
        ):
            files.add(path)
    return {
        p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(files)
    }


def freeze(root):
    # Resolve task/runtime inputs before binding; reports never enter this surface.
    design = read(root / "design.json")
    check_public("Opaque", 0, max(design["budgets"]))
    importlib.import_module("chemworld.physchem.crystallization_adapter_manifest")
    surface = runtime_surface()
    changed = subprocess.check_output(
        ["git", "diff", "HEAD", "--name-only", "--", *surface], cwd=ROOT, text=True
    ).strip()
    untracked = subprocess.check_output(
        ["git", "ls-files", "--others", "--exclude-standard", "--", *surface], cwd=ROOT, text=True
    ).strip()
    if changed or untracked:
        raise ValueError("Commit the execution-relevant source once before formal freeze")
    path = root / "release.json"
    if path.exists():
        raise FileExistsError("This block already has its one release binding")
    write(
        path,
        {
            "source_commit": subprocess.check_output(
                ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
            ).strip(),
            "surface": surface,
            "design_sha256": hashlib.sha256((root / "design.json").read_bytes()).hexdigest(),
        },
    )


def verify_frozen(root):
    binding = read(root / "release.json")
    if hashlib.sha256((root / "design.json").read_bytes()).hexdigest() != binding["design_sha256"]:
        raise ValueError("Frozen design changed")
    mismatches = [
        p
        for p, h in binding["surface"].items()
        if hashlib.sha256((ROOT / p).read_bytes()).hexdigest() != h
    ]
    if mismatches:
        raise ValueError(f"Frozen execution surface changed: {mismatches}")


def run(root, report):
    verify_frozen(root)
    if not read(root / "qualification" / "result.json")["passed"]:
        raise ValueError("Formal qualification failed; no provider calls")
    design = read(root / "design.json")
    progress = {"stage": "starting", "completed_cells": 0, "planned_cells": len(design["schedule"])}
    stop, started = threading.Event(), time.monotonic()

    def heartbeat():
        while not stop.wait(30):
            elapsed = time.monotonic() - started
            state = {**progress, "elapsed_s": round(elapsed)}
            write(root / "progress.json", state)
            export(root, report)
            print(json.dumps(state), flush=True)

    thread = threading.Thread(target=heartbeat, daemon=True)
    thread.start()
    try:
        for cell in design["schedule"]:
            result_path = root / "sources" / cell["id"] / "result.json"
            if result_path.exists():
                previous = read(result_path)
                if previous["status"] in {"completed", "failed"}:
                    progress["completed_cells"] += 1
                    continue
                raise ValueError(
                    "Retained nonterminal source requires explicit infrastructure diagnosis"
                )
            verify_frozen(root)
            result = source(root, cell, progress)
            progress["completed_cells"] += 1
            export(root, report)
            if result.get("source", {}).get("exact_replay", {}).get("verified") is not True:
                break
    finally:
        stop.set()
        thread.join(timeout=5)
        export(root, report)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument(
        "--phase",
        choices=[
            "calibrate",
            "configure",
            "freeze",
            "qualify",
            "run",
            "report",
            "launch",
            "pipeline",
        ],
        required=True,
    )
    parser.add_argument("--calibration", type=Path)
    parser.add_argument("--budgets", type=int, nargs="+", default=[12, 24])
    args = parser.parse_args()
    root, report = args.root.resolve(), args.report.resolve()
    if args.phase == "calibrate":
        calibrate(root, report)
    elif args.phase == "configure":
        if not args.calibration or args.budgets not in ([12], [12, 24]):
            raise ValueError("Provide calibration and a supported budget scope")
        configure(root, args.calibration.resolve(), args.budgets)
        export(root, report)
    elif args.phase == "freeze":
        freeze(root)
    elif args.phase == "qualify":
        verify_frozen(root)
        qualify(root, report)
    elif args.phase == "run":
        run(root, report)
    elif args.phase == "launch":
        launch_pipeline(root, report)
    elif args.phase == "pipeline":
        pipeline(root, report)
    else:
        export(root, report)


if __name__ == "__main__":
    main()
