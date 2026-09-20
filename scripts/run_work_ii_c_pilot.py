"""C-E development pilot: fixed references, three autonomous sources and posttests."""

from __future__ import annotations

import argparse
import copy
import json
import math
import shutil
import sys
import tempfile
import threading
import time
from pathlib import Path

import gymnasium as gym
from scripts import run_work_ii_ec_dual_goal_trial as ec
from scripts.run_work_ii_astra_full_process_trial import reference_actions
from scripts.run_work_ii_astra_single_trial import read, write
from scripts.run_work_ii_final_diagnostic import build_command, launch
from scripts.run_work_ii_pa_single_trial import token_accounting
from scripts.validate_work_ii_ec_pa_entry import anonymous

from chemworld.agents.diagnostic_numerics import FOLLOWUP_NUMERICS, NumericsBudget
from chemworld.agents.experiment_codex_mcp import ChemWorldMCPServer
from chemworld.agents.interactive_codex_experiment import InteractiveCodexExperimentAgent
from chemworld.campaign_resources import CampaignResourceCard
from chemworld.data.logging import load_jsonl
from chemworld.eval.runner import run_agent
from chemworld.eval.work_ii_truth import _FrozenTruthReplayAgent
from chemworld.foundation import equipment_settings
from chemworld.runtime.full_process_contract import FULL_PROCESS_FREE_RESEARCH_CONTRACT
from chemworld.tasks import get_task
from chemworld.world.crystallization_material_family import (
    REACTION_CRYSTALLIZATION_LATENT_MATERIAL_FAMILY,
)

ROOT = Path(__file__).resolve().parents[1]
TASK = "reaction-to-crystallization"
PROTOCOL = "c-free-research-development-v1-en"
ARMS = ("Opaque", "Aligned", "MisIndexed")
METRICS = ("crystal_yield", "crystal_purity", "crystal_size", "crystal_fines_fraction")
NAMESPACE = "work-ii-c-sol-pilot-v1"
CLOSE = [{"operation": "terminate"}, {"operation": "measure", "instrument": "final_assay"}]
PARTICLE = {"operation": "measure", "instrument": "particle_size"}
GOAL = (
    "Find and recommend a process maximizing seed-excluded crystal recovery, subject to "
    "crystal purity >= 0.80 and the number fraction of particles below 20 micrometres <= 0.50. "
    "A recovery of 0.10 is an initial feasibility target, not an optimization ceiling. "
    "Choose and revise experiments freely; the native composite score is secondary."
)
SYSTEM = """You are an autonomous scientist in a simulated reaction-to-crystallization laboratory.
Use only chemworld_lab and public_numerics. No external access or hidden simulator inspection.
Read material_information first. The task's research_goal is authoritative. Complete 12
independent batches with 12 extra instrument uses shared freely across HPLC and particle_size,
plus 12 final assays and 720 operation attempts. Measurements are optional up to their budget.
Use the current legal ranges and actual thermometer readings. Choose materials, reaction,
seeding, cooling, holding, reheating/redissolution, recooling and filtration freely.
The later prediction domain includes material changes, seed doses, cooling/thermal history,
stopping versus continuing growth, and upstream loading changes. Exact recipes are withheld.
crystal_yield is crystallization-stage recovery: seed-excluded recovered product divided
by the target product present before separation. It is not overall yield from reactant charge.
crystal_purity and crystal_fines_fraction are fractions; crystal_size is min(d50/250 um,1),
a bounded number-weighted size index, not a diameter in micrometres. Fines means below 20 um.
HPLC consumes a representative sample; particle_size is nondestructive after crystals exist.
All sampling and purchased seed consumption count. No arbitrary independent sample bottles.
Use English. No mandatory snapshots, fixed mechanism menu, equation template or batch grouping.
For each batch explicitly terminate and measure final_assay. Continue with next_state until
campaign_ended. Then commit_final_recommendation selecting one completed batch (1-based
lifecycle index), with a short rationale. If none meets quality constraints, state that clearly.
Return concise required status/summary JSON. Separate turns will request your mechanism
report, blind predictions and a three-question retrospective; do not answer them early.
The source allows 128 public calculator attempts. Invalid expressions count. At exhaustion,
continue from existing evidence. The source response deadline still applies.
Supplied material information can be incomplete or inaccurate; experimental observations
are authoritative. No particular scientific outcome is required.
"""
K1 = """Your experiments and operating recommendation are sealed. Give a self-contained
mechanistic account in English: important material effects, reaction/crystallization coupling,
process-history dependence, and relationships or equations you judge useful. Cite particular
batches for key claims; distinguish observations, interpretations and untested alternatives.
Discuss revisions and uncertainty, including any unresolved quality/recovery tradeoff. You may
use any explanation form; no prescribed mechanism or equation is required. Do not change the
recommended batch or answer future prediction questions. Return report."""
K2 = """Your mechanism report and predictions are sealed. No prediction truth has been supplied.
Answer three questions in English without changing sealed answers:
1. Which main claims are supported, contradicted or still untested? Cite relevant batches and
distinguish direct observations from interpretation.
2. With one additional experiment, what would you do, which competing explanations would it
distinguish, and what different outcomes would you expect?
3. Which observation did your account use least effectively, and which held-out prediction is
least reliable? Explain why. Return report."""


def material(arm):
    return {
        "Opaque": {"mode": "opaque_codes"},
        "Aligned": {"mode": "anonymous_nominal_properties"},
        "MisIndexed": {
            "mode": "anonymous_misindexed_properties",
            "target_field": "solvent",
            "descriptor_permutation": [0, 3, 2, 1],
        },
    }[arm]


def resource_card(batches=12, *, envelope=12):
    return CampaignResourceCard(
        card_id="c-free-research-v1",
        operation_attempt_limit=60 * envelope,
        vessel_start_limit=batches,
        final_assay_limit=batches,
        nonfinal_instrument_use_limit=envelope,
        stock_limits={
            "reagent_mol": 0.04 * envelope,
            "solvent_L": 0.08 * envelope,
            "catalyst_mol": 0.005 * envelope,
            "seed_g": 1.0 * envelope,
        },
        process_time_limit_s=None,
    )


def cool(temperature, duration=14400):
    return {
        "operation": "cool_crystallize",
        "target_temperature_K": temperature,
        "duration_s": duration,
    }


def recipe(*, solvent=1, seed=0.006, path=None, reagent=0.010):
    prefix = [a for a in reference_actions(TASK)[:8] if a["operation"] != "measure"]
    prefix[0]["solvent"] = solvent
    prefix[1]["amount_mol"] = reagent
    return [
        *prefix,
        {"operation": "seed_crystals", "seed_mass_g": seed},
        *(path or [cool(290), cool(284), cool(278.15)]),
        copy.deepcopy(PARTICLE),
        {"operation": "filter_crystals"},
        *copy.deepcopy(CLOSE),
    ]


def queries():
    reheat = {
        "operation": "heat",
        "target_temperature_K": 300.0,
        "duration_s": 14400,
        "stirring_speed_rpm": 600.0,
    }
    plans = [
        ("solvent", recipe(solvent=1)),
        ("solvent", recipe(solvent=3)),
        ("seed", recipe(seed=0.006)),
        ("seed", recipe(seed=0.050)),
        ("cooling_history", recipe()),
        ("cooling_history", recipe(path=[cool(278.15)] * 3)),
        ("thermal_history", recipe(path=[cool(290), cool(278.15), cool(278.15)])),
        ("thermal_history", recipe(path=[cool(278.15), reheat, cool(278.15)])),
        ("continue_growth", recipe(path=[cool(290), cool(278.15)])),
        ("continue_growth", recipe(path=[cool(290), cool(278.15), cool(278.15)])),
        ("upstream_loading", recipe(reagent=0.008)),
        ("upstream_loading", recipe(reagent=0.016)),
    ]
    return [
        {"query_id": f"Q{i:02}", "pair": pair, "actions": actions}
        for i, (pair, actions) in enumerate(plans, 1)
    ]


def feasibility_plans():
    plans = []
    for solvent in range(4):
        actions = reference_actions(TASK)[:8]
        actions[0]["solvent"] = solvent
        actions += [{"operation": "seed_crystals", "seed_mass_g": 0.050}]
        # Same fixed, gently stepped pattern for all solvents; no selection from new outcomes.
        for i in range(1, 13):
            actions.append(cool(300 + (278.15 - 300) * i / 12))
            if i % 3 == 0:
                actions.append(copy.deepcopy(PARTICLE))
        actions += [
            {"operation": "measure", "instrument": "hplc"},
            {"operation": "filter_crystals"},
            *copy.deepcopy(CLOSE),
        ]
        plans.append({"id": f"F{solvent}", "actions": actions})
    return plans


def prediction_question(query_set):
    return (
        "Predict the noise-free final process outcomes before final-assay sampling for these "
        "12 independent batches, each starting from the original initial state. Each recipe "
        "specifies all actions, including any intermediate sampling. For each return "
        "query_id, particles_present, quality_feasible, and estimate/lower80/upper80 for "
        "crystal_yield, crystal_purity, crystal_size and crystal_fines_fraction. All metrics "
        "are 0-1: crystal_yield is seed-excluded crystallization-stage recovery relative to "
        "target product present before separation, not overall yield from reactant charge; "
        "crystal_size is "
        "min(number-weighted d50/250 micrometres,1). If no particles are expected, set "
        "particles_present=false and all three size interval fields to null. quality_feasible "
        "means purity>=0.80 and fines<=0.50 with particles present. Give a concise rationale "
        "covering the six paired comparisons and uncertainty. Do not run experiments, seek "
        "truth, or revise K1. Answer in English.\n" + json.dumps(query_set)
    )


class CAgent(ec.FreeResearchAgent):
    def reset(self, task_info, seed):
        InteractiveCodexExperimentAgent.reset(self, task_info, seed)
        self._task_contract.update(
            free_research_campaign=True,
            research_goal=GOAL,
            description=GOAL,
            instrument_contracts={
                k: task_info["instruments"][k] for k in task_info["allowed_instruments"]
            },
            study_budget={
                "complete_batches": 12,
                "extra_measurements": 12,
                "final_assays": 12,
                "operation_attempts": 720,
            },
            prediction_metrics={
                "crystal_yield": (
                    "seed-excluded recovered product / target product present before separation; "
                    "crystallization-stage recovery, not overall yield from reactant charge"
                ),
                "crystal_purity": "fraction",
                "crystal_size": "min(number-weighted d50/250 micrometres,1)",
                "crystal_fines_fraction": "number fraction below 20 micrometres",
            },
        )
        self._task_contract_manifest = self.workspace.publish_task_contract(self._task_contract)

    def _command(self, *, instructions_path, schema_path):
        command = super()._command(instructions_path=instructions_path, schema_path=schema_path)
        instructions_path.write_text(SYSTEM, encoding="utf-8")
        (self.output / "source-instructions.txt").write_text(SYSTEM, encoding="utf-8")
        for i, arg in enumerate(command):
            if arg.startswith("mcp_servers.public_numerics.args="):
                args = json.loads(arg.split("=", 1)[1])
                command[i] = "mcp_servers.public_numerics.args=" + json.dumps(
                    [*args, "--budget-feedback"]
                )
        return command


class TruthCapture(gym.Wrapper):
    def __init__(self, env, truths, diagnostics=None):
        super().__init__(env)
        self.truths = truths
        self.diagnostics = diagnostics

    def step(self, action):
        before = None
        if action.get("instrument") == "final_assay":
            base = self.unwrapped
            values = base.observation_kernel._truth_values(base._state)
            settings = equipment_settings(base._state.equipment, "crystallizer")
            before = {k: float(values[k]) for k in METRICS}
            before["particles_present"] = settings.get("csd_total_particle_count", 0) > 0
        result = self.env.step(action)
        if before is not None and result[4].get("transaction_status") == "committed":
            self.truths.append(before)
        if (
            self.diagnostics is not None
            and action.get("operation") == "cool_crystallize"
            and result[4].get("transaction_status") == "committed"
        ):
            settings = equipment_settings(self.unwrapped._state.equipment, "crystallizer")
            self.diagnostics.append(
                {
                    key: settings[key]
                    for key in (
                        "feed_concentration_mol_L",
                        "reference_solubility_mol_L",
                        "temperature_history_K",
                        "maximum_supersaturation_ratio",
                        "final_supersaturation_ratio",
                        "csd_total_particle_count",
                    )
                }
            )
        return result


def physics(
    agent, output, *, arm="Opaque", batches=12, observation_seed=0, callback=None, truths=None
):
    return run_agent(
        env_id=get_task(TASK).env_id,
        agent=agent,
        task_id=TASK,
        world_split="public-test",
        objective="balanced",
        seed=0,
        agent_seed=0,
        observation_seed=observation_seed,
        budget=720,
        budget_override=720,
        episode_mode_override="campaign" if batches > 1 else "single_experiment",
        campaign_resource_card=resource_card(batches),
        material_information=material(arm),
        crystallization_material_family_id=REACTION_CRYSTALLIZATION_LATENT_MATERIAL_FAMILY,
        full_process_contract_id=FULL_PROCESS_FREE_RESEARCH_CONTRACT,
        observation_noise_mode="keyed",
        observation_noise_namespace=NAMESPACE,
        output_path=output,
        step_callback=callback,
        env_wrapper=(lambda env: TruthCapture(env, truths)) if truths is not None else None,
        method_resource_limits={
            "operation_limit": 720,
            "complete_experiment_limit": 12,
            "wall_time_limit_s": 3600,
            "model_call_limit": 1,
            "input_token_limit": 16000000,
            "uncached_input_token_limit": 4000000,
            "output_token_limit": 192000,
            "training_environment_step_limit": 0,
        }
        if isinstance(agent, CAgent)
        else None,
    )


def quality(values):
    return (
        values.get("particles_present", True)
        and values.get("crystal_purity", 0) >= 0.80
        and values.get("crystal_fines_fraction", 1) <= 0.50
    )


def committed_recipe(records, lifecycle_index):
    """Extract a completed physical recipe; retain rejected attempts as provenance."""
    if type(lifecycle_index) is not int or lifecycle_index < 1:
        raise ValueError("Recommendation must identify a completed, 1-based batch")
    selected = [
        (step, r)
        for step, r in enumerate(records, 1)
        if r.get("experiment_index") == lifecycle_index - 1
    ]
    committed, rejected = [], []
    for step, record in selected:
        status = record.get("transaction_status")
        if status == "committed":
            committed.append(record)
        elif status in {"validation_failed", "rolled_back"}:
            rejected.append({"step": step, "action": record["action"], "status": status})
        else:
            raise ValueError(f"Unknown transaction status at step {step}: {status}")
    finals = [r for r in committed if r.get("instrument") == "final_assay"]
    if len(finals) != 1 or committed[-1] is not finals[0]:
        raise ValueError("Recommendation recipe must end with one committed final assay")
    return {
        "lifecycle_index": lifecycle_index,
        "actions": [copy.deepcopy(r["action"]) for r in committed],
        "source_attempts": len(selected),
        "excluded_rejected_attempts": rejected,
    }


def repair_retest(root, arm):
    """One authorized provider-free repair; original source/result files are untouched."""
    folder = root / arm
    original = read(folder / "result.json")
    if original.get("recommendation_retest", {}).get("passed"):
        raise ValueError("An intact recommendation retest must not be repeated")
    if not original["source"]["exact_replay"].get("verified"):
        raise ValueError("Source replay must be valid before retest repair")
    recipe = committed_recipe(
        load_jsonl(folder / "trajectory.jsonl"),
        original["recommendation"]["selected_experiment_index"],
    )
    result = fixed_run(
        folder / "recommendation-retest-repair",
        recipe["actions"],
        {},
        arm=arm,
        observation_seed=303,
    )
    repair = {
        "original_status": original["status"],
        "original_retest_failure": original["recommendation_retest"].get("failure"),
        "recipe": recipe,
        "recommendation_retest": result,
        "new_provider_calls": 0,
        "passed": result["passed"],
    }
    write(folder / "retest-repair.json", repair)
    return repair


def fixed_run(folder, actions, progress, *, batches=1, arm="Opaque", observation_seed=101):
    folder.mkdir(parents=True, exist_ok=False)
    write(folder / "actions.json", actions)
    truths, failure = [], None
    progress.update(stage=folder.name, phase="reference", operations=0, batches=0)

    def callback(record, trace):
        del trace
        progress["operations"] += 1
        if (
            record.info.get("instrument") == "final_assay"
            and record.info.get("transaction_status") == "committed"
        ):
            progress["batches"] += 1
        if record.info.get("transaction_status") != "committed":
            raise RuntimeError(f"reference action rejected: {record.action}")

    try:
        physics(
            _FrozenTruthReplayAgent(actions),
            folder / "trajectory.jsonl",
            arm=arm,
            batches=batches,
            callback=callback,
            truths=truths,
            observation_seed=observation_seed,
        )
    except Exception as exc:
        failure = {"type": type(exc).__name__, "message": str(exc)[:1600]}
    records = (
        load_jsonl(folder / "trajectory.jsonl") if (folder / "trajectory.jsonl").exists() else []
    )
    result = {
        "failure": failure,
        "truth": truths,
        "batches": ec.summaries(records),
        "operations": len(records),
        "exact_replay": ec.replay_with_progress(records, folder.name),
    }
    result["passed"] = (
        not failure
        and len(result["batches"]) == batches
        and result["exact_replay"].get("verified") is True
    )
    result["feasible"] = (
        bool(truths) and quality(truths[-1]) and truths[-1]["crystal_yield"] >= 0.10
    )
    write(folder / "result.json", result)
    return result


def check_public(arm):
    env = gym.make(
        "ChemWorld",
        task_id=TASK,
        seed=0,
        material_information=material(arm),
        crystallization_material_family_id=REACTION_CRYSTALLIZATION_LATENT_MATERIAL_FAMILY,
        full_process_contract_id=FULL_PROCESS_FREE_RESEARCH_CONTRACT,
        campaign_resource_card=resource_card(),
        budget_override=720,
    )
    with tempfile.TemporaryDirectory(prefix="chemworld-research-") as temporary:
        home = Path(temporary)
        agent = CAgent(
            goal="optimization",
            home_root=home,
            output=home,
            workspace=home / "laboratory",
            role_id="free_research",
        )
        try:
            env.reset(seed=0)
            agent.reset(env.unwrapped.task_info(), 0)
            agent.workspace.start_session(
                session_id="reference-check", response_timeout_s=10, session_scope="campaign"
            )
            reply = ChemWorldMCPServer(agent.workspace.root)._call_tool("material_information", {})
            if reply.get("isError"):
                raise ValueError("public material tool failed")
            payload = json.loads(reply["content"][0]["text"])
            return {
                "payload": payload,
                "contract": agent._task_contract,
                "anonymous": anonymous(payload),
                "particle_available": "particle_size"
                in agent._task_contract["instrument_contracts"],
            }
        finally:
            agent.close()
            env.close()


def prepare(root, progress):
    root.mkdir(parents=True, exist_ok=False)
    query_set = queries()
    design = {
        "protocol": PROTOCOL,
        "model": ec.PROVIDER,
        "world": "C-W01",
        "arms": list(ARMS),
        "batches_per_source": 12,
        "planned_preparation_batches": 19,
        "resources": resource_card().to_dict(),
        "posttest_numerics": FOLLOWUP_NUMERICS.to_dict(),
        "system": SYSTEM,
        "goal": GOAL,
        "queries": query_set,
        "feasibility_plans": feasibility_plans(),
        "K1": K1,
        "Q": prediction_question(query_set),
        "K2": K2,
        "contract": FULL_PROCESS_FREE_RESEARCH_CONTRACT,
        "material_family": REACTION_CRYSTALLIZATION_LATENT_MATERIAL_FAMILY,
    }
    write(root / "design.json", design)
    result = {"passed": False, "checks": {}, "references": {}, "failure": None}
    try:
        public = {arm: check_public(arm) for arm in ARMS}
        write(root / "public-inputs.json", public)
        aligned = public["Aligned"]["payload"]["material_information"]["dossier"]
        misindexed = public["MisIndexed"]["payload"]["material_information"]["dossier"]
        checks = result["checks"]
        checks["anonymous_instruments"] = all(
            p["anonymous"] and p["particle_available"] for p in public.values()
        )
        checks["opaque_has_no_dossier"] = (
            public["Opaque"]["payload"]["material_information"]["dossier"] is None
        )
        checks["solvent_swap_only"] = aligned["choices"]["catalyst"] == misindexed["choices"][
            "catalyst"
        ] and all(
            misindexed["choices"]["solvent"][i]["nominal_properties"]
            == aligned["choices"]["solvent"][j]["nominal_properties"]
            for i, j in enumerate([0, 3, 2, 1])
        )
        if not all(checks.values()):
            raise ValueError("public-input checks failed")
        plans = [("queries", [a for q in query_set for a in q["actions"]], 12, "Opaque")]
        plans += [(p["id"], p["actions"], 1, "Opaque") for p in design["feasibility_plans"]]
        # One particle reading plus one HPLC sample exercises both declared instruments.
        probe = recipe()
        probe.insert(-3, {"operation": "measure", "instrument": "hplc"})
        plans += [("mapping-" + arm, probe, 1, arm) for arm in ARMS]
        for name, actions, batches, arm in plans:
            reference = fixed_run(root / name, actions, progress, batches=batches, arm=arm)
            result["references"][name] = reference
            write(root / "preparation.json", result)
            if not reference["passed"]:
                raise ValueError(f"reference execution failed: {name}")
        checks["quality_witness"] = any(
            result["references"][p["id"]]["feasible"] for p in design["feasibility_plans"]
        )
        probes = [result["references"]["mapping-" + arm] for arm in ARMS]
        checks["same_physics"] = all(p["truth"] == probes[0]["truth"] for p in probes)
        checks["same_observations"] = all(
            p["batches"][0]["metrics"] == probes[0]["batches"][0]["metrics"] for p in probes
        )
        result["passed"] = all(checks.values())
    except Exception as exc:
        result["failure"] = {"type": type(exc).__name__, "message": str(exc)[:1600]}
    result["completed_batches"] = sum(len(r["batches"]) for r in result["references"].values())
    result["operations"] = sum(r["operations"] for r in result["references"].values())
    write(root / "preparation.json", result)
    return result


def schema(stage):
    if stage != "Q":
        return ec.schema(stage)
    interval = {
        "type": "object",
        "additionalProperties": False,
        "properties": {k: {"type": "number"} for k in ("estimate", "lower80", "upper80")},
        "required": ["estimate", "lower80", "upper80"],
    }
    size = copy.deepcopy(interval)
    size["properties"] = {k: {"type": ["number", "null"]} for k in interval["properties"]}
    row = {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "query_id": {"type": "string"},
            "particles_present": {"type": "boolean"},
            "quality_feasible": {"type": "boolean"},
            **{k: size if k == "crystal_size" else interval for k in METRICS},
        },
        "required": ["query_id", "particles_present", "quality_feasible", *METRICS],
    }
    return {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "predictions": {"type": "array", "items": row},
            "rationale": {"type": "string"},
        },
        "required": ["predictions", "rationale"],
    }


def posttest(agent, folder, stage, thread_id, progress, design):
    budget = NumericsBudget.from_record(design["posttest_numerics"])
    workspace = agent.home_root / "followup"
    workspace.mkdir(exist_ok=True)
    schema_path = workspace / f"{stage}-schema.json"
    write(schema_path, schema(stage))
    instructions = workspace / "instructions.md"
    instructions.write_text(
        "Continue your original research on the same thread. Only "
        "public_numerics.calculate is available; no laboratory, files, "
        "network or hidden access. Answer in English; earlier outputs "
        "remain sealed. " + budget.disclosure(),
        encoding="utf-8",
    )
    audit = folder / f"{stage}-numerics.jsonl"
    command = build_command(
        ec.PROVIDER,
        schema_path,
        workspace,
        audit=audit,
        thread_id=thread_id,
        provider_retries=0,
        numerics_budget=budget,
    )
    command += [
        "-c",
        "mcp_servers.chemworld_lab.enabled=false",
        "-c",
        f"mcp_servers.chemworld_lab.command={json.dumps(sys.executable)}",
        "-c",
        f"model_instructions_file={json.dumps(instructions.as_posix())}",
    ]
    result = launch(
        command,
        design[stage],
        workspace,
        agent.followup_environment,
        folder / stage,
        1200,
        True,
        audit,
        {**progress, "phase": stage},
        numerics_budget=budget,
    )
    if not result.get("payload"):
        result["failure"] = result.get("failure") or "missing_payload"
    if result.get("thread_id") != thread_id:
        result["failure"] = result.get("failure") or "posttest_thread_changed"
    write(folder / stage / "receipt.json", result)
    return result


def evaluate(payload, truth, query_set):
    rows = payload.get("predictions", []) if isinstance(payload, dict) else []
    ids = [r.get("query_id") for r in rows]
    expected = [q["query_id"] for q in query_set]
    if len(ids) != len(expected) or set(ids) != set(expected):
        return {"valid": False, "reason": "missing/duplicate/unknown query IDs"}
    by_id = {r["query_id"]: r for r in rows}
    metrics, failures = {}, []
    for metric in METRICS:
        errors, covered, widths = [], [], []
        for key in expected:
            r, target = by_id[key], truth[key]
            values = r.get(metric, {})
            vals = [values.get(k) for k in ("estimate", "lower80", "upper80")]
            if metric == "crystal_size" and not r.get("particles_present") and vals == [None] * 3:
                if target["particles_present"]:
                    failures.append(
                        {"query": key, "metric": metric, "reason": "missed particle presence"}
                    )
                continue
            if not all(type(v) in (float, int) and math.isfinite(v) for v in vals):
                failures.append(
                    {"query": key, "metric": metric, "reason": "invalid numeric answer"}
                )
                continue
            estimate, lo, hi = vals
            if not 0 <= lo <= estimate <= hi <= 1:
                failures.append({"query": key, "metric": metric, "reason": "invalid interval"})
                continue
            if metric == "crystal_size" and not target["particles_present"]:
                continue
            errors.append(abs(estimate - target[metric]))
            covered.append(lo <= target[metric] <= hi)
            widths.append(hi - lo)
        metrics[metric] = {
            "n": len(errors),
            "planned": 12,
            "mae": sum(errors) / len(errors) if errors else None,
            "covered": sum(covered),
            "mean_interval_width": sum(widths) / len(widths) if widths else None,
        }

    def sign(x):
        return 0 if abs(x) <= 0.03 else 1 if x > 0 else -1

    pairs = []
    for i in range(0, 12, 2):
        a, b = expected[i : i + 2]
        for metric in METRICS:
            x, y = by_id[a][metric]["estimate"], by_id[b][metric]["estimate"]
            if type(x) not in (float, int) or type(y) not in (float, int):
                continue
            pairs.append(
                {
                    "pair": query_set[i]["pair"],
                    "metric": metric,
                    "correct": sign(y - x) == sign(truth[b][metric] - truth[a][metric]),
                }
            )
    return {
        "valid": not any(f["reason"] != "missed particle presence" for f in failures),
        "failures": failures,
        "metrics": metrics,
        "pairs": pairs,
        "pair_correct": sum(p["correct"] for p in pairs),
        "pair_n": len(pairs),
        "quality_correct": sum(by_id[k]["quality_feasible"] == quality(truth[k]) for k in expected),
        "presence_correct": sum(
            by_id[k]["particles_present"] == truth[k]["particles_present"] for k in expected
        ),
    }


def run_source(root, arm, progress):
    design = read(root / "design.json")
    folder = root / arm
    folder.mkdir(parents=True, exist_ok=False)
    write(folder / "attempt.json", {"started_epoch": time.time(), "planned_attempts": 1})
    result = {"arm": arm, "status": "running", "failure": None, "posttests": {}}
    write(folder / "result.json", result)
    started = time.monotonic()
    # Neutral directory names avoid exposing the treatment in provider inputs. Retain sessions.
    home = Path(tempfile.mkdtemp(prefix="chemworld-research-"))
    write(folder / "runtime-location.json", {"home": str(home)})
    agent = CAgent(
        goal="optimization",
        home_root=home,
        output=folder,
        workspace=home / "laboratory",
        role_id="free_research",
        request_timeout_s=1200,
        finalization_timeout_s=300,
        session_wall_time_limit_s=3600,
        max_recovered_mcp_tool_failures=12,
        max_consecutive_mcp_tool_failures=6,
        max_provider_error_events=0,
        pre_action_restart_limit=0,
        accepted_turn_continuation_limit=0,
        provider_process_attempt_limit=1,
        max_initial_prompt_bytes=262144,
        max_tool_output_bytes=131072,
        history_event_limit=720,
        history_byte_limit=2097152,
        session_progress_callback=lambda p: progress.update(provider_liveness=p),
    )
    progress.update(stage=arm, phase="source", operations=0, batches=0)
    truths = []

    def callback(record, trace):
        del trace
        progress["operations"] += 1
        if (
            record.info.get("instrument") == "final_assay"
            and record.info.get("transaction_status") == "committed"
        ):
            progress["batches"] += 1
        print(
            json.dumps({k: v for k, v in progress.items() if k != "provider_liveness"}), flush=True
        )

    try:
        physics(agent, folder / "trajectory.jsonl", arm=arm, callback=callback, truths=truths)
    except Exception as exc:
        result["failure"] = {
            "stage": "source",
            "type": type(exc).__name__,
            "message": str(exc)[:1600],
        }
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
        "batches": ec.summaries(records),
        "truth": truths,
        "operations": len(records),
        "elapsed_s": time.monotonic() - started,
        "usage": agent.method_resource_usage(),
        "exact_replay": ec.replay_with_progress(records, arm),
        "rollbacks": [
            {"step": i + 1, "action": r["action"], "reason": r.get("rollback_reason")}
            for i, r in enumerate(records)
            if r.get("transaction_status") != "committed"
        ],
    }
    result["recommendation"] = last.get("final_recommendation")
    write(folder / "result.json", result)
    try:
        if ec.posttest_context_available(last):
            for stage in ("K1", "Q", "K2"):
                progress.update(phase=stage)
                progress.pop("provider_liveness", None)
                turn = posttest(agent, folder, stage, last["thread_id"], progress, design)
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
                "stage": "source_handoff",
                "message": "no intact terminal context for posttests",
            }
        reference = read(root / "queries" / "result.json")
        truth = dict(
            zip([q["query_id"] for q in design["queries"]], reference["truth"], strict=True)
        )
        result["prediction_evaluation"] = evaluate(
            result["posttests"].get("Q", {}).get("payload"), truth, design["queries"]
        )
        selected = (result["recommendation"] or {}).get("selected_experiment_index")
        batch = next(
            (b for b in result["source"]["batches"] if b["lifecycle_index"] == selected), None
        )
        if batch is not None:
            result["recommendation_recipe"] = committed_recipe(records, selected)
            result["recommendation_retest"] = fixed_run(
                folder / "recommendation-retest",
                result["recommendation_recipe"]["actions"],
                progress,
                arm=arm,
                observation_seed=303,
            )
        result["status"] = (
            "completed"
            if (
                len(result["source"]["batches"]) == 12
                and not result["failure"]
                and result["source"]["exact_replay"].get("verified") is True
                and len(result["posttests"]) == 3
                and result["prediction_evaluation"]["valid"]
                and result.get("recommendation_retest", {}).get("passed") is True
            )
            else "failed"
        )
    except Exception as exc:
        result["failure"] = result["failure"] or {
            "stage": progress["phase"],
            "type": type(exc).__name__,
            "message": str(exc)[:1600],
        }
        result["status"] = "failed"
    result["elapsed_s"] = time.monotonic() - started
    result["tokens"] = token_accounting(result)
    sessions = home / "codex-home/sessions"
    if sessions.exists():
        shutil.copytree(sessions, folder / "provider-rollouts")
    write(folder / "result.json", result)
    return result


def export(root, report):
    report.mkdir(parents=True, exist_ok=True)
    preparation = read(root / "preparation.json")
    preparation["status"] = (
        "completed"
        if preparation["passed"]
        else "failed"
        if preparation.get("failure") or "completed_batches" in preparation
        else "running"
    )
    preparation.setdefault(
        "completed_batches",
        sum(len(r["batches"]) for r in preparation.get("references", {}).values()),
    )
    preparation.setdefault(
        "operations", sum(r["operations"] for r in preparation.get("references", {}).values())
    )
    results = [
        read(root / arm / "result.json")
        if (root / arm / "result.json").exists()
        else {"arm": arm, "status": "not_started", "posttests": {}}
        for arm in ARMS
    ]
    original_complete = sum(r["status"] == "completed" for r in results)
    repairs = []
    for row in results:
        repair_path = root / row["arm"] / "retest-repair.json"
        if repair_path.exists():
            repair = read(repair_path)
            repairs.append({"arm": row["arm"], **repair})
            row["original_status"] = row["status"]
            row["original_recommendation_retest"] = row.get("recommendation_retest")
            row["retest_repair"] = repair
            if repair["passed"]:
                row["recommendation_retest"] = repair["recommendation_retest"]
                if (
                    not row.get("failure")
                    and len(row.get("source", {}).get("batches", [])) == 12
                    and row["source"]["exact_replay"].get("verified")
                    and row.get("prediction_evaluation", {}).get("valid")
                    and len(row["posttests"]) == 3
                    and all(
                        t.get("payload") and not t.get("failure") for t in row["posttests"].values()
                    )
                ):
                    row["status"] = "completed"
    summary = {
        "development_only": True,
        "planned_sources": 3,
        "planned_source_batches": 36,
        "planned_posttests": 9,
        "original_completed_sources": original_complete,
        "retest_repairs": repairs,
        "retest_attempts": sum(bool(r.get("recommendation_retest")) for r in results)
        + len(repairs),
        "preparation": preparation,
        "completed_sources": sum(r["status"] == "completed" for r in results),
        "completed_batches": sum(len(r.get("source", {}).get("batches", [])) for r in results),
        "completed_posttests": sum(
            sum(bool(t.get("payload")) and not t.get("failure") for t in r["posttests"].values())
            for r in results
        ),
        "results": results,
    }
    summary["prediction_design"] = {
        "slots": 12,
        "unique_recipes": 9,
        "shared_controls": [["Q01", "Q03", "Q05"], ["Q07", "Q10"]],
    }
    summary["retained_preparation_failures"] = [
        {
            "attempt": "v1",
            "stage": "resource_card_construction",
            "operations": 0,
            "completed_batches": 0,
            "provider_calls": 0,
        },
        {
            "attempt": "v2",
            "stage": "public_material_identity",
            "operations": 0,
            "completed_batches": 0,
            "provider_calls": 0,
        },
        {
            "attempt": "v3",
            "stage": "legacy_measurement_order",
            "operations": 7,
            "committed_operations": 6,
            "completed_batches": 0,
            "provider_calls": 0,
            "exact_replay_checked_operations": 7,
        },
    ]
    # Receipts and provider transport stay in runs; publish scientific outputs and accounting only.
    public = copy.deepcopy(summary)
    for row in public["results"]:
        row["posttests"] = {
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
            for stage, t in row["posttests"].items()
        }
    write(report / "summary.json", public)
    lines = [
        "# Crystallization C-E pilot",
        "",
        "Development pilot; GPT-5.6 Sol / medium. One world, three prior arms, "
        "no outcome-based retries.",
        "Twelve paired prediction slots use nine unique recipes. Shared controls are "
        "dependent comparisons, not additional independent scientific samples.",
        "Metric correction (2026-09-20): the original saved prompts incorrectly described "
        "crystal_yield as relative to reactant charge. The simulator reports seed-excluded "
        "crystallization-stage recovery relative to target product before separation. "
        "Original prompts and outcomes remain preserved; this mismatch limits interpretation "
        "of the pilot's quantitative predictions. Future prompts use the simulator's definition.",
        "",
        f"Preparation batches: {preparation['completed_batches']}/19; "
        f"status: {preparation['status']}; passed: {preparation['passed']}. "
        f"Complete chains: {summary['completed_sources']}/3; "
        f"source batches: {summary['completed_batches']}/36; "
        f"posttests: {summary['completed_posttests']}/9.",
        "",
        f"Original complete chains: {original_complete}/3; "
        f"additional retest attempts: {len(repairs)}. "
        "Original failures remain in the machine summary; "
        "repaired results never replace raw records.",
        "",
        "| Arm | Status | Batches | Posttests | Recovery | Purity | Fines | "
        "Quality passes | Recovery target met |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | --- | --- |",
    ]
    for row in results:
        batches = row.get("source", {}).get("batches", [])
        retest = row.get("recommendation_retest", {}).get("truth", [])
        v = retest[-1] if retest else {}
        n = sum(bool(t.get("payload")) and not t.get("failure") for t in row["posttests"].values())
        lines.append(
            f"| [{row['arm']}]({row['arm']}.md) | {row['status']} | {len(batches)}/12 | {n}/3 | "
            f"{v.get('crystal_yield', '')} | {v.get('crystal_purity', '')} | "
            f"{v.get('crystal_fines_fraction', '')} | {quality(v) if v else ''} | "
            f"{quality(v) and v.get('crystal_yield', 0) >= 0.10 if v else ''} |"
        )
        details = [
            f"# {row['arm']} crystallization pilot",
            "",
            f"Status: {row['status']}; failure: {row.get('failure')}",
            f"Original status: {row.get('original_status', row['status'])}; "
            f"retest repair present: {bool(row.get('retest_repair'))}.",
            "",
            "## Source batches",
            "",
            "| Batch | Recovery | Purity | Size index | Fines |",
            "| ---: | ---: | ---: | ---: | ---: |",
        ]
        for b in batches:
            details.append(
                "| "
                + " | ".join(
                    [str(b["lifecycle_index"]), *[str(b["metrics"].get(k)) for k in METRICS]]
                )
                + " |"
            )
        for stage in ("K1", "Q", "K2"):
            payload = row["posttests"].get(stage, {}).get("payload")
            details += [
                "",
                f"## {stage}",
                "",
                (payload.get("report") or json.dumps(payload, indent=2))
                if payload
                else "Not completed.",
            ]
        details += [
            "",
            "## Evaluation and resources",
            "",
            "```json",
            json.dumps(
                {
                    k: row.get(k)
                    for k in ("prediction_evaluation", "tokens", "elapsed_s", "recommendation")
                },
                indent=2,
            ),
            "```",
        ]
        (report / f"{row['arm']}.md").write_text("\n".join(details) + "\n", encoding="utf-8")
    lines += [
        "",
        "## Preparation",
        "",
        "```json",
        json.dumps({k: preparation[k] for k in ("checks", "failure", "operations")}, indent=2),
        "```",
        "",
        "All reference and source exact replays and recommendation retests are accounted "
        "separately in summary.json. A completed chain is execution completion, "
        "not scientific success.",
    ]
    (report / "REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--phase", choices=("prepare", "sources", "report"), required=True)
    args = parser.parse_args()
    root, report = args.root.resolve(), args.report.resolve()
    progress = {
        "stage": "starting",
        "completed_sources": 0,
        "planned_sources": 3,
        "operations": 0,
        "batches": 0,
    }
    stop, started = threading.Event(), time.monotonic()

    def heartbeat():
        while not stop.wait(30):
            elapsed = time.monotonic() - started
            rate = progress["completed_sources"] / elapsed
            heartbeat_payload = {
                **progress,
                "elapsed_s": round(elapsed),
                "sources_per_hour": rate * 3600,
                "eta_s": (3 - progress["completed_sources"]) / rate if rate else None,
            }
            write(root / "progress.json", heartbeat_payload)
            print(json.dumps(heartbeat_payload), flush=True)

    thread = threading.Thread(target=heartbeat, daemon=True)
    thread.start()
    try:
        if args.phase == "prepare":
            result = prepare(root, progress)
            export(root, report)
            print(
                json.dumps(
                    {
                        k: result[k]
                        for k in ("passed", "checks", "failure", "completed_batches", "operations")
                    }
                ),
                flush=True,
            )
            if not result["passed"]:
                raise SystemExit(1)
        elif args.phase == "sources":
            if not read(root / "preparation.json")["passed"]:
                raise ValueError("preparation failed; no provider launch")
            for arm in read(root / "design.json")["arms"]:
                if (root / arm).exists():
                    raise FileExistsError("source already attempted; no implicit recovery")
                result = run_source(root, arm, progress)
                progress["completed_sources"] += 1
                export(root, report)
                if result.get("source", {}).get("exact_replay", {}).get("verified") is not True:
                    break
        else:
            export(root, report)
    finally:
        stop.set()
        thread.join(timeout=2)


if __name__ == "__main__":
    main()
