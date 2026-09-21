"""Accelerated, provider-free purification entry/coverage gate; development evidence."""

from __future__ import annotations

import argparse
import copy
import json
import math
import tempfile
import threading
import time
from contextlib import nullcontext
from pathlib import Path

import gymnasium as gym
from scripts import run_work_ii_ec_dual_goal_trial as ec
from scripts.benchmark_runtime_views import verify_resources
from scripts.run_work_ii_final_diagnostic import read, write
from scripts.work_ii_p_inventory import inventory_v2, inventory_v3
from scripts.work_ii_p_public import presentation, product_ids

from chemworld.agents.experiment_codex_mcp import ChemWorldMCPServer
from chemworld.agents.interactive_codex_experiment import InteractiveCodexExperimentAgent
from chemworld.campaign_resources import CampaignResourceCard
from chemworld.data.logging import load_jsonl
from chemworld.eval.experiment_1_p_assets import build_extractant_dossier, frozen_world_truths
from chemworld.eval.runner import run_agent
from chemworld.eval.work_ii_truth import _FrozenTruthReplayAgent
from chemworld.foundation.state import selected_phase_id
from chemworld.runtime.full_process_contract import (
    FULL_PROCESS_FREE_RESEARCH_CONTRACT,
    sample_domain,
)
from chemworld.tasks import get_task
from chemworld.world.phase_kernel import partition_split

ROOT = Path(__file__).resolve().parents[1]
TASK = "reaction-to-purification"
ARMS = ("Opaque", "Aligned", "MisIndexed")
GOAL = (
    "Find and recommend a complete reaction/extraction/purification process maximizing "
    "recovery of target product relative to original reactant charge, subject to final purity "
    ">=0.80. Native score is diagnostic only. Choose operations, measurements, repetitions and "
    "stopping freely. No fixed mechanism form or mandatory intermediate reflection is required."
)
SYSTEM = """You are an autonomous scientist in a simulated purification laboratory.
Use chemworld_lab and public_numerics. Read material_information first. Complete 12 independent
batches with 12 extra measurements shared across the campaign and 12 final assays. Follow the
research_goal, actual operation schemas and public state. Separate_phase keeps the named phase
and removes the other; it is not a nondestructive sampling switch. Wash acts on the organic
phase. Recovery means target product in the final selected material divided by original
reactant charge. Purity includes the assay's specified solute impurities; neither is concentration.
Measurements consume sample from the declared object; carried readings are not new observations.
Terminate and final_assay close each batch, then use next_state until campaign_ended=true.
Choose a completed batch for final recommendation. Later provide a free mechanism report,
blind quantitative predictions and reflection, in that order. Do not answer those prematurely.
Use English. Anonymous material indices are categories and imply no numerical ordering.
"""


def resources(batches=12):
    return CampaignResourceCard(
        card_id=f"p-free-research-{batches}-v1",
        operation_attempt_limit=60 * batches,
        vessel_start_limit=batches,
        final_assay_limit=batches,
        nonfinal_instrument_use_limit=batches,
        stock_limits={
            "reagent_mol": 0.04 * batches,
            "solvent_L": 0.08 * batches,
            "catalyst_mol": 0.005 * batches,
            "phase_liquid_L": 0.08 * batches,
            "extractant_L": 0.08 * batches,
            "wash_solvent_L": 0.12 * batches,
        },
        process_time_limit_s=None,
    )


def recipe(
    *, duration=7200, extractant=2, volume=0.030, washes=(0.020,), concentrate=600, reagent=0.002
):
    return [
        {"operation": "add_solvent", "solvent": 2, "volume_L": 0.028},
        {"operation": "add_reagent", "amount_mol": reagent},
        {"operation": "add_catalyst", "catalyst": 1, "catalyst_amount_mol": 0.00025},
        {
            "operation": "heat",
            "target_temperature_K": 400.0,
            "duration_s": duration,
            "stirring_speed_rpm": 720.0,
        },
        {"operation": "quench"},
        {"operation": "add_phase", "phase": "aqueous", "volume_L": 0.012},
        {"operation": "add_extractant", "extractant": extractant, "volume_L": volume},
        {"operation": "mix", "duration_s": 240.0, "stirring_speed_rpm": 850.0},
        {"operation": "settle", "duration_s": 420.0},
        {"operation": "measure", "instrument": "hplc"},
        {"operation": "separate_phase", "target_phase": "organic"},
        *[{"operation": "wash", "wash_volume_L": v} for v in washes],
        {"operation": "dry"},
        *([{"operation": "concentrate", "duration_s": concentrate}] if concentrate else []),
        {"operation": "transfer", "transfer_fraction": 0.97},
        {"operation": "terminate"},
        {"operation": "measure", "instrument": "final_assay"},
    ]


def queries(design="v3"):
    pairs = [
        ("upstream_time", [recipe(duration=t) for t in (1800, 7200)]),
        ("extractant", [recipe(extractant=x, washes=(0.018,)) for x in (1, 2)]),
        ("phase_ratio", [recipe(volume=v, washes=(0.016,)) for v in (0.012, 0.040)]),
        ("washing", [recipe(duration=6000, washes=w) for w in ((), (0.024,))]),
        ("wash_staging", [recipe(volume=0.025, washes=w) for w in ((0.020,), (0.010, 0.010))]),
        (
            "concentration",
            [recipe(duration=5400, washes=(0.022,), concentrate=t) for t in (0, 600)],
        ),
    ]
    result = [
        {"query_id": f"Q{i + 1:02d}", "factor": f, "actions": a}
        for i, (f, a) in enumerate((f, a) for f, plans in pairs for a in plans)
    ]
    if design in {"v2", "v3"}:
        # Development redesign fixed after the separate loading-domain diagnostic.
        for query in result[:6]:
            query["actions"][1]["amount_mol"] = 0.040
        result[2]["actions"][6]["extractant"] = 0
    return result


def domain_queries():
    return [
        {
            "query_id": f"D{i + 1:02d}",
            "factor": "loading_extractant",
            "actions": recipe(reagent=charge, extractant=x),
        }
        for i, (charge, x) in enumerate((q, x) for q in (0.002, 0.010, 0.040) for x in range(4))
    ]


def public_dossier(asset, world, arm):
    if arm == "Opaque":
        return None
    rows = build_extractant_dossier(asset, world_truth=world)
    # Explicit allowlist: never publish the private truth binding, permutation or arm.
    return {
        "scope": {
            "contact_conditions": asset["contact_context"],
            "feed_anchors": asset["entity"]["feed_anchors"],
        },
        "interpretation": "Scoped reference properties, not a complete process model. "
        "Test their applicability; no optimum process is supplied.",
        "extractants": rows["aligned" if arm == "Aligned" else "misspecified"],
    }


class PAgent(ec.FreeResearchAgent):
    def __init__(self, *, dossier, **kwargs):
        self.dossier = dossier
        super().__init__(goal="optimization", batches=12, **kwargs)

    def reset(self, task_info, seed):
        public = copy.deepcopy(task_info)
        public["material_information"] = {"dossier": self.dossier}
        InteractiveCodexExperimentAgent.reset(self, public, seed)
        self._task_contract.update(
            free_research_campaign=True,
            research_goal=GOAL,
            description=GOAL,
            task_goal=GOAL,
            episode_mode="campaign",
            constraints=[
                "Resources persist across all 12 batches.",
                "Each final assay closes one batch, not the entire campaign.",
            ],
            study_budget={
                "complete_batches": 12,
                "extra_measurements": 12,
                "final_assays": 12,
                "operation_attempts": 720,
            },
            prediction_metrics={
                "purity": "selected target / selected solute amounts",
                "recovery": "selected target / original reactant charge",
            },
            instrument_contracts={
                k: task_info["instruments"][k] for k in task_info["allowed_instruments"]
            },
        )
        self._task_contract["experiment_lifecycle"]["planned_complete_experiments"] = 12
        self._task_contract_manifest = self.workspace.publish_task_contract(self._task_contract)

    def _command(self, *, instructions_path, schema_path):
        command = super()._command(instructions_path=instructions_path, schema_path=schema_path)
        instructions_path.write_text(SYSTEM, encoding="utf-8")
        (self.output / "source-instructions.txt").write_text(SYSTEM, encoding="utf-8")
        return command


def check_public(task_info, dossier):
    with tempfile.TemporaryDirectory(prefix="chemworld-p-gate-") as directory:
        home = Path(directory)
        agent = PAgent(
            dossier=dossier,
            home_root=home,
            output=home,
            workspace=home / "laboratory",
            role_id="free_research",
        )
        try:
            agent.reset(task_info, 0)
            agent.workspace.start_session(
                session_id="p-gate", response_timeout_s=10, session_scope="campaign"
            )
            response = ChemWorldMCPServer(agent.workspace.root)._call_tool(
                "material_information", {}
            )
            if response.get("isError"):
                raise ValueError("material_information failed")
            payload = json.loads(response["content"][0]["text"])
            serialized = json.dumps(payload).lower()
            forbidden = (
                "ethanol",
                "acetonitrile",
                "toluene",
                "cas_number",
                '"formula"',
                '"world_seed"',
                '"private_truth_binding"',
                '"permutation"',
                '"arm"',
                '"misspecified"',
            )
            return {
                "payload": payload,
                "contract": agent._task_contract,
                "anonymous": not any(v in serialized for v in forbidden),
                "dossier_delivered": payload["material_information"]["dossier"] == dossier,
                "campaign_contract": agent._task_contract["episode_mode"] == "campaign"
                and agent._task_contract["study_budget"]["complete_batches"] == 12
                and agent._task_contract["experiment_lifecycle"]["planned_complete_experiments"]
                == 12,
            }
        finally:
            agent.close()


class Capture(gym.Wrapper):
    def __init__(self, env, diagnostics, audits, parameters):
        super().__init__(env)
        self.rows = diagnostics
        self.audits = audits
        self.parameters = parameters

    def step(self, action):
        base = self.unwrapped
        state = base._state
        view = base.observation_kernel.species_view
        self.parameters.update(
            {
                k: base.world.domain_parameter(k)
                for k in ("partition_coefficient_multiplier", "partition_phase_volume_multiplier")
            }
        )
        before = None
        if action.get("operation") == "measure":
            truth = base.observation_kernel._truth_values(state)
            view = (
                base.runtime.species_view
                if hasattr(base.runtime, "species_view")
                else base.observation_kernel.species_view
            )
            phases = {} if state.phases is None else state.phases.phases
            chosen = selected_phase_id(state.phases) or "organic"
            phase = phases.get(chosen)
            target_ids = product_ids(view)
            impurity_ids = view.impurity_species_for_state(state)
            amount = (
                sum(phase.species_amounts_mol.get(k, 0.0) for k in target_ids)
                if phase
                else view.target_amount(state)
            )
            impurity = (
                sum(phase.species_amounts_mol.get(k, 0.0) for k in impurity_ids)
                if phase
                else view.impurity_amount(state)
            )
            charge = view.initial_reactant_amount(state)
            before = {
                "instrument": action["instrument"],
                "selected_phase": chosen,
                "truth": {
                    k: float(truth[k]) for k in ("purity", "recovery", "process_mass_balance_error")
                },
                "selected_target_mol": amount,
                "original_charge_mol": charge,
                "purity_arithmetic_error": abs(
                    truth["purity"] - amount / max(amount + impurity, 1e-12)
                ),
                "recovery_arithmetic_error": abs(truth["recovery"] - amount / max(charge, 1e-12)),
                "phase_product_mol": {
                    k: sum(p.species_amounts_mol.get(s, 0.0) for s in target_ids)
                    for k, p in phases.items()
                },
                "removed_product_mol": 0.0
                if state.process is None
                else state.process.metrics.get("removed_phase_product_mol", 0.0),
            }
        # Capture the committed state before final_assay creates the next vessel.
        runtime = base.runtime
        original = runtime.apply_transaction
        committed = []

        def capture_transaction(current, submitted):
            outcome = original(current, submitted)
            committed.append(outcome.state)
            return outcome

        runtime.apply_transaction = capture_transaction
        try:
            result = self.env.step(action)
        finally:
            runtime.apply_transaction = original
        downstream = {
            "add_phase",
            "add_extractant",
            "mix",
            "settle",
            "separate_phase",
            "wash",
            "dry",
            "concentrate",
            "transfer",
            "terminate",
            "measure",
        }
        if (
            committed
            and result[4].get("transaction_status") == "committed"
            and action.get("operation") in downstream
        ):
            self.audits.append(inventory_audit(state, committed[-1], action, view, result[4]))
        if before is not None and result[4].get("transaction_status") == "committed":
            self.rows.append(before)
        return result


def inventory_audit(before, after, action, view, info):
    """Reconcile retained + itemized discarded + independently calculated sampled solute."""
    groups = {"product": product_ids(view), "impurity": view.impurity_species}
    errors = {}
    phases = {} if before.phases is None else before.phases.phases
    domain = sample_domain(before)
    sample = float(info.get("sample_consumed", 0.0))
    operation = action["operation"]
    histories = [
        (
            before.metadata.get("removed_phase_inventory_history", []),
            after.metadata.get("removed_phase_inventory_history", []),
        )
    ]
    equipment_id = {
        "dry": "sorbent_dryer",
        "concentrate": "vacuum_concentrator",
        "transfer": "transfer_line",
    }.get(operation)
    if equipment_id and after.equipment is not None:
        previous_equipment = (
            None if before.equipment is None else before.equipment.equipment.get(equipment_id)
        )
        histories.append(
            (
                previous_equipment.settings.get("removed_phase_inventory_history", [])
                if previous_equipment
                else [],
                after.equipment.equipment[equipment_id].settings.get(
                    "removed_phase_inventory_history", []
                ),
            )
        )
    # Metadata and equipment can retain different cumulative prefixes. Read the
    # current operation's own receipt once, not their concatenated histories.
    removed = next(
        (
            h[-1]["inventories"]
            for previous, h in reversed(histories)
            if h and h != previous and h[-1]["operation"] == operation
        ),
        {},
    )
    for group, species in groups.items():
        retained_before = sum(before.species_amounts.get(s, 0.0) for s in species)
        retained_after = sum(after.species_amounts.get(s, 0.0) for s in species)
        discarded = sum(
            sum(item["species_amounts_mol"].get(s, 0.0) for s in species)
            if item.get("species_amounts_mol")
            else item[f"{group}_mol"]
            for item in removed.values()
        )

        sample_phases = [phases[k] for k in domain]
        sample_volume = sum(p.volume_L for p in sample_phases)
        sampled = (
            (
                sample
                * sum(p.species_amounts_mol.get(s, 0.0) for p in sample_phases for s in species)
                / sample_volume
            )
            if sample and sample_volume
            else 0.0
        )
        errors[group] = abs(retained_before - retained_after - discarded - sampled)
    untouched = True
    if sample:
        untouched = all(
            phase == after.phases.phases.get(key)
            for key, phase in phases.items()
            if key not in domain
        )
    charge_error = abs(view.initial_reactant_amount(before) - view.initial_reactant_amount(after))
    return {
        "operation": action["operation"],
        "instrument": action.get("instrument"),
        "inventory_errors_mol": errors,
        "sample_volume_L": sample,
        "unselected_phases_unchanged": untouched,
        "original_charge_error_mol": charge_error,
        "passed": max(errors.values()) < 1e-9 and charge_error < 1e-9 and untouched,
    }


class GateAgent(_FrozenTruthReplayAgent):
    def __init__(self, actions, dossier):
        super().__init__(actions)
        self.dossier = dossier
        self.public = None

    def reset(self, task_info, seed):
        super().reset(task_info, seed)
        self.public = check_public(task_info, self.dossier)


def execute(folder, world, arm, asset, plan, progress):
    with presentation(public_dossier(asset, world, arm), GOAL, 12):
        return _execute(folder, world, arm, asset, plan, progress)


def _execute(folder, world, arm, asset, plan, progress):
    folder.mkdir(parents=True, exist_ok=False)
    actions = [copy.deepcopy(a) for q in plan for a in q["actions"]]
    write(folder / "actions.json", actions)
    agent = GateAgent(actions, public_dossier(asset, world, arm))
    diagnostics, audits, parameters, failure = [], [], {}, None
    started = time.monotonic()

    def callback(record, trace):
        del trace
        progress["operations"] += 1
        if record.info.get("transaction_status") != "committed":
            raise ValueError(f"Illegal fixed action: {record.action}")
        if record.info.get("instrument") == "final_assay":
            progress["batches"] += 1

    try:
        run_agent(
            env_id=get_task(TASK).env_id,
            agent=agent,
            task_id=TASK,
            world_split="public-test",
            objective="balanced",
            seed=world["world_seed"],
            world_interventions=world["world_interventions"],
            agent_seed=0,
            observation_seed=101,
            budget=720,
            budget_override=720,
            episode_mode_override="campaign",
            campaign_resource_card=resources(),
            material_information={"mode": "opaque_codes"},
            full_process_contract_id=FULL_PROCESS_FREE_RESEARCH_CONTRACT,
            observation_noise_mode="keyed",
            observation_noise_namespace="p-gate-v1",
            output_path=folder / "trajectory.jsonl",
            step_callback=callback,
            env_wrapper=lambda env: Capture(env, diagnostics, audits, parameters),
        )
    except Exception as exc:
        failure = {"type": type(exc).__name__, "message": str(exc)}
    records = (
        load_jsonl(folder / "trajectory.jsonl") if (folder / "trajectory.jsonl").exists() else []
    )
    progress["phase"] = "exact_replay"
    replay = ec.replay_with_progress(
        records, folder.name, world_interventions=world["world_interventions"]
    )
    ledger = None
    try:
        ledger = verify_resources(records) if records else None
    except Exception as exc:
        failure = failure or {"type": type(exc).__name__, "message": str(exc), "stage": "ledger"}
    batches = ec.summaries(records)
    final = [r for r in diagnostics if r["instrument"] == "final_assay"]
    checks = {
        "legal_complete_execution": failure is None
        and len(batches) == 12
        and len(records) == len(actions),
        "exact_replay": replay.get("verified") is True,
        "resource_ledger": ledger is not None,
        "public_delivery": bool(agent.public)
        and all(agent.public[k] for k in ("anonymous", "dossier_delivered", "campaign_contract")),
        "metric_arithmetic": len(final) == 12
        and all(
            r["purity_arithmetic_error"] < 1e-9 and r["recovery_arithmetic_error"] < 1e-9
            for r in final
        ),
        "finite_metrics": len(final) == 12
        and all(math.isfinite(v) for r in final for v in r["truth"].values()),
        "mass_balance": len(final) == 12
        and all(r["truth"]["process_mass_balance_error"] <= 1e-8 for r in final),
        "inventory_and_sampling": len(audits)
        == sum(
            a["operation"] not in {"add_solvent", "add_reagent", "add_catalyst", "heat", "quench"}
            for a in actions
        )
        and all(a["passed"] for a in audits),
        "world_parameters": parameters == {k: world[k] for k in parameters}
        and len(parameters) == 2,
        "dynamic_public_contract": all(
            not any(
                token in json.dumps(r.get("agent_view", {})).lower()
                for token in (
                    "ethanol",
                    "acetonitrile",
                    "toluene",
                    "cas_number",
                    "single-experiment task",
                )
            )
            for r in records
        ),
    }
    result = {
        "world_id": world["world_id"],
        "arm": arm,
        "passed": all(checks.values()),
        "checks": checks,
        "failure": failure,
        "completed_batches": len(batches),
        "operations": len(records),
        "exact_replay": replay,
        "resources": ledger,
        "public": agent.public,
        "diagnostics": diagnostics,
        "inventory_audits": audits,
        "executed_parameters": parameters,
        "truth": [r["truth"] for r in final],
        "observations": [b["metrics"] for b in batches],
        "elapsed_s": time.monotonic() - started,
    }
    write(folder / "result.json", result)
    return result


def coverage(rows, plan):
    if len(rows) != 12:
        return {"passed": False, "reason": "incomplete_reference"}
    positive = sum(r["purity"] >= 0.8 and r["recovery"] > 0 for r in rows)
    feasible = sum(r["purity"] >= 0.8 and r["recovery"] >= 0.1 for r in rows)
    pairs = [
        {
            "factor": plan[i]["factor"],
            "deltas": {k: rows[i + 1][k] - rows[i][k] for k in ("purity", "recovery")},
        }
        for i in range(0, 12, 2)
    ]
    for p in pairs:
        p["resolved"] = max(abs(v) for v in p["deltas"].values()) >= 0.02
    resolved = sum(p["resolved"] for p in pairs)
    checks = {
        "quality_classes": 3 <= positive <= 9,
        "feasible_witness": feasible > 0,
        "four_resolved_pairs": resolved >= 4,
        "material_resolved": pairs[1]["resolved"],
        "postprocess_resolved": any(p["resolved"] for p in pairs[3:]),
    }
    return {
        "passed": all(checks.values()),
        "checks": checks,
        "quality_positive": positive,
        "quality_negative": 12 - positive,
        "feasible": feasible,
        "resolved_pairs": resolved,
        "pairs": pairs,
    }


def aqueous_probe(folder, world):
    folder.mkdir(parents=True, exist_ok=False)
    actions = [
        *recipe()[:10],
        {"operation": "separate_phase", "target_phase": "aqueous"},
        {"operation": "terminate"},
        {"operation": "measure", "instrument": "final_assay"},
    ]
    diagnostics, audits, parameters = [], [], {}
    write(folder / "actions.json", actions)
    failure = None
    with presentation(None, GOAL, 1):
        try:
            run_agent(
                env_id=get_task(TASK).env_id,
                agent=_FrozenTruthReplayAgent(actions),
                task_id=TASK,
                world_split="public-test",
                objective="balanced",
                seed=world["world_seed"],
                world_interventions=world["world_interventions"],
                agent_seed=0,
                observation_seed=101,
                budget=60,
                budget_override=60,
                episode_mode_override="campaign",
                campaign_resource_card=resources(1),
                material_information={"mode": "opaque_codes"},
                full_process_contract_id=FULL_PROCESS_FREE_RESEARCH_CONTRACT,
                observation_noise_mode="keyed",
                observation_noise_namespace="p-gate-v1",
                output_path=folder / "trajectory.jsonl",
                env_wrapper=lambda env: Capture(env, diagnostics, audits, parameters),
            )
        except Exception as exc:
            failure = {"type": type(exc).__name__, "message": str(exc)}
        records = (
            load_jsonl(folder / "trajectory.jsonl")
            if (folder / "trajectory.jsonl").exists()
            else []
        )
        replay = ec.replay_with_progress(
            records, folder.name, world_interventions=world["world_interventions"]
        )
    final = [d for d in diagnostics if d["instrument"] == "final_assay"]
    checks = {
        "complete_legal": failure is None
        and len(records) == len(actions)
        and all(r["transaction_status"] == "committed" for r in records),
        "exact_replay": replay.get("verified") is True,
        "aqueous_target_assay": len(final) == 1
        and final[0]["selected_phase"] == "aqueous"
        and final[0]["selected_target_mol"] > 0
        and final[0]["truth"]["recovery"] > 0,
        "arithmetic": len(final) == 1
        and final[0]["purity_arithmetic_error"] < 1e-9
        and final[0]["recovery_arithmetic_error"] < 1e-9,
        "inventory_and_sampling": len(audits) == 8 and all(a["passed"] for a in audits),
    }
    result = {
        "world_id": world["world_id"],
        "passed": all(checks.values()),
        "checks": checks,
        "failure": failure,
        "completed_batches": len(final),
        "operations": len(records),
        "exact_replay": replay,
        "inventory_audits": audits,
        "diagnostics": diagnostics,
    }
    write(folder / "result.json", result)
    return result


def prior_check(world, asset, plan, campaign):
    """Check scoped physics, the fixed derangement and an opposed material ranking."""
    aligned = public_dossier(asset, world, "Aligned")
    wrong = public_dossier(asset, world, "MisIndexed")
    contact_checks = []
    for extractant, row in enumerate(aligned["extractants"]):
        for anchor, published in zip(asset["entity"]["feed_anchors"], row["anchors"], strict=True):
            actual = partition_split(
                product_mol=anchor["product_mol"],
                impurity_mol=anchor["impurity_mol"],
                solvent=extractant,
                coefficient_multiplier=world["partition_coefficient_multiplier"],
                phase_volume_multiplier=world["partition_phase_volume_multiplier"],
                **asset["contact_context"],
            )
            expected = {
                "K_product": actual["partition_coefficient"],
                "K_impurity": actual["impurity_partition_coefficient"],
                "product_in_organic_mol": actual["organic_product_mol"],
                "product_in_aqueous_mol": actual["aqueous_product_mol"],
                "impurity_in_organic_mol": actual["organic_impurity_mol"],
                "impurity_in_aqueous_mol": actual["aqueous_impurity_mol"],
            }
            error = max(abs(published[k] - v) for k, v in expected.items())
            contact_checks.append(
                {"extractant": extractant, "anchor": anchor["anchor_id"], "max_error": error}
            )
    pair = [
        next(a["extractant"] for a in q["actions"] if a["operation"] == "add_extractant")
        for q in plan[2:4]
    ]

    def direction(payload):
        values = [payload["extractants"][x]["anchors"][0]["product_organic_fraction"] for x in pair]
        return values[1] - values[0]

    a_delta, m_delta = direction(aligned), direction(wrong)
    truth_delta = campaign["truth"][3]["recovery"] - campaign["truth"][2]["recovery"]
    public_delta = campaign["observations"][3]["recovery"] - campaign["observations"][2]["recovery"]
    checks = {
        "scoped_A_matches_executable_kernel": all(r["max_error"] < 1e-12 for r in contact_checks),
        "matched_M_permutation": all(
            wrong["extractants"][i]["anchors"] == aligned["extractants"][j]["anchors"]
            for i, j in enumerate(asset["entity"]["misindex_permutation"])
        ),
        "opposed_material_ranking": a_delta * m_delta < 0,
        "public_material_contrast": abs(truth_delta) >= 0.02
        and abs(public_delta) >= 0.02
        and truth_delta * a_delta > 0
        and public_delta * a_delta > 0,
    }
    return {
        "passed": all(checks.values()),
        "checks": checks,
        "scoped_contacts": contact_checks,
        "material_pair": pair,
        "A_fraction_delta": a_delta,
        "M_fraction_delta": m_delta,
        "final_true_recovery_delta": truth_delta,
        "final_public_recovery_delta": public_delta,
        "limitation": "Kernel-scope consistency plus a qualitative full-process contrast; "
        "not a noise-calibrated recovery of the complete mechanism or guaranteed agent discovery.",
    }


def save(root, report, result, started):
    result.update(
        elapsed_s=time.monotonic() - started,
        completed_batches=sum(r["completed_batches"] for r in result["campaigns"]),
        completed_campaigns=len(result["campaigns"]),
        passed_campaigns=sum(r["passed"] for r in result["campaigns"]),
        operations=sum(r["operations"] for r in result["campaigns"]),
        replay_steps=sum(r["exact_replay"].get("checked_steps", 0) for r in result["campaigns"]),
    )
    write(root / "summary.json", result)
    write(report / "summary.json", result)
    lines = [
        "# P accelerated development "
        + ("domain diagnostic" if result["design"] == "domain" else "gate"),
        "",
        "Provider-free development evidence; no participant result or formal promotion.",
        "",
        f"Status: {result['status']}. "
        f"Batches {result['completed_batches']}/{result['planned_batches']}; "
        f"campaigns {result['completed_campaigns']}/{result['planned_campaigns']}; "
        f"engineering passes {result['passed_campaigns']}/{result['planned_campaigns']}.",
        f"Operations: {result['operations']}; replay steps: {result['replay_steps']}; "
        f"wall time {result['elapsed_s']:.2f} s.",
        "",
        "| World | Quality + / - | Feasible | Resolved pairs | Science | Arm equivalence | Prior |",
        "| --- | ---: | ---: | ---: | --- | --- | --- |",
    ]
    for w, row in result["worlds"].items():
        q = row["coverage"]
        domain = result["design"] == "domain"
        pairs = "N/A" if domain else f"{q.get('resolved_pairs', '-')}/6"
        science = "N/A" if domain else q["passed"]
        arms = "N/A" if domain else row["arm_equivalent"]
        lines.append(
            f"| {w} | {q.get('quality_positive', '-')} / {q.get('quality_negative', '-')} | "
            f"{q.get('feasible', '-')} | {pairs} | "
            f"{science} | {arms} | {row.get('prior', {}).get('passed', 'N/A')} |"
        )
    lines += [
        "",
        "| Campaign | Batches | Engineering | Failed checks / exception |",
        "| --- | ---: | --- | --- |",
    ]
    for r in result["campaigns"]:
        failed = [k for k, v in r["checks"].items() if not v]
        lines.append(
            f"| {r['world_id']}/{r['arm']} | {r['completed_batches']}/12 | "
            f"{r['passed']} | {', '.join(failed)} {r['failure'] or ''} |"
        )
    lines += [
        "",
        "No retries or within-block changes. "
        "All failures and unexecuted units remain in denominators.",
        "Actual K1/Q/K2 provider completion is outside this gate. "
        "Scoped property consistency does not prove unrestricted mechanism identifiability.",
    ]
    if result["design"] == "domain":
        lines += [
            "",
            "Loading-domain diagnostic only: science-pair and three-arm qualification "
            "are not evaluated. A completed engineering pass is not a full gate pass.",
        ]
    if "world_distinction" in result:
        lines += [
            "",
            f"Distinct executed world pairs: {sum(result['world_distinction'].values())}/10.",
        ]
    if result.get("aqueous_probes"):
        probes = result["aqueous_probes"]
        lines += [
            "",
            f"Additional aqueous branch checks: {sum(p['passed'] for p in probes)}/5; "
            f"batches {sum(p['completed_batches'] for p in probes)}/5; "
            f"operations {sum(p['operations'] for p in probes)}; "
            f"replay steps {sum(p['exact_replay'].get('checked_steps', 0) for p in probes)}.",
        ]
        for p in probes:
            lines.append(
                f"- {p['world_id']}: failed checks "
                f"{[k for k, v in p['checks'].items() if not v]}; error {p['failure']}."
            )
    if result["design"] in {"v2", "v3"}:
        lines += [
            "",
            "Prior check: 8 scoped kernel contacts per world, exact fixed permutation, "
            "opposed X0/X2 rankings and a resolved public final-recovery contrast. "
            "This does not certify unrestricted transfer of the scoped dossier or "
            "mechanism identifiability under every autonomous trajectory.",
        ]
    (report / "REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(root, report, design="v3"):
    root.mkdir(parents=True, exist_ok=False)
    report.mkdir(parents=True, exist_ok=True)
    asset = read(ROOT / "configs/benchmark/experiment_1_p_asset_authoring_v1.1.0.json")
    worlds = frozen_world_truths(asset)
    plan = domain_queries() if design == "domain" else queries(design)
    arms = ("Opaque",) if design == "domain" else ARMS
    planned = len(worlds) * len(arms) * 12
    write(
        root / "design.json",
        {
            "note": "WORK_II_P_GATE_NOTE.md",
            "worlds": worlds,
            "queries": plan,
            "arms": arms,
            "resources": resources().to_dict(),
            "provider_calls": 0,
            "planned_batches": planned,
            "design": design,
        },
    )
    result = {
        "status": "running",
        "development_only": True,
        "provider_calls": 0,
        "planned_batches": planned,
        "planned_campaigns": len(worlds) * len(arms),
        "design": design,
        "campaigns": [],
        "worlds": {},
    }
    (root / "executor.py").write_bytes(Path(__file__).read_bytes())
    (root / "public_adapter.py").write_bytes((ROOT / "scripts/work_ii_p_public.py").read_bytes())
    started, stop = time.monotonic(), threading.Event()
    progress = {"stage": "starting", "phase": "execution", "batches": 0, "operations": 0}

    def heartbeat():
        while not stop.wait(30):
            elapsed = time.monotonic() - started
            n = progress["batches"]
            print(
                json.dumps(
                    {
                        **progress,
                        "planned_batches": planned,
                        "elapsed_s": elapsed,
                        "batches_per_s": n / elapsed,
                        "eta_s": elapsed / n * (planned - n) if n else None,
                    }
                ),
                flush=True,
            )

    thread = threading.Thread(target=heartbeat, daemon=True)
    thread.start()
    try:
        save(root, report, result, started)
        for world in worlds:
            rows = []
            for arm in arms:
                progress.update(stage=f"{world['world_id']}/{arm}", phase="execution")
                print(json.dumps({**progress, "planned_batches": planned}), flush=True)
                row = execute(root / world["world_id"] / arm, world, arm, asset, plan, progress)
                rows.append(row)
                result["campaigns"].append(row)
                save(root, report, result, started)
            result["worlds"][world["world_id"]] = {
                "coverage": coverage(rows[0]["truth"], plan),
                "arm_equivalent": len(rows) == 3
                and all(
                    r["truth"] == rows[0]["truth"] and r["observations"] == rows[0]["observations"]
                    for r in rows
                )
                and len(rows[0]["truth"]) == 12,
            }
            if design == "domain":
                result["worlds"][world["world_id"]] = {
                    "coverage": {
                        k: result["worlds"][world["world_id"]]["coverage"][k]
                        for k in ("quality_positive", "quality_negative", "feasible")
                    },
                    "arm_equivalent": None,
                }
            elif design in {"v2", "v3"} and len(rows[0]["truth"]) == 12:
                result["worlds"][world["world_id"]]["prior"] = prior_check(
                    world, asset, plan, rows[0]
                )
        if design in {"v2", "v3"}:
            opaque = [r for r in result["campaigns"] if r["arm"] == "Opaque"]
            result["world_distinction"] = {
                f"{a['world_id']}/{b['world_id']}": a["executed_parameters"]
                != b["executed_parameters"]
                and a["truth"] != b["truth"]
                and a["observations"] != b["observations"]
                for i, a in enumerate(opaque)
                for b in opaque[i + 1 :]
            }
        if design == "v3":
            result["aqueous_probes"] = []
            for world in worlds:
                progress.update(stage=f"{world['world_id']}/aqueous_branch", phase="branch_probe")
                print(json.dumps(progress), flush=True)
                result["aqueous_probes"].append(
                    aqueous_probe(root / "aqueous" / world["world_id"], world)
                )
                save(root, report, result, started)
        result["status"] = "completed"
        result["passed"] = all(r["passed"] for r in result["campaigns"]) and (
            design == "domain"
            or all(
                w["coverage"]["passed"] and w["arm_equivalent"] for w in result["worlds"].values()
            )
        )
        if design in {"v2", "v3"}:
            result["passed"] = (
                result["passed"]
                and all(w.get("prior", {}).get("passed", False) for w in result["worlds"].values())
                and len(result["world_distinction"]) == 10
                and all(result["world_distinction"].values())
            )
        if design == "v3":
            result["passed"] = result["passed"] and all(
                p["passed"] for p in result["aqueous_probes"]
            )
    finally:
        stop.set()
        thread.join(timeout=2)
        save(root, report, result, started)
    print(
        json.dumps(
            {
                k: result[k]
                for k in ("status", "passed", "completed_batches", "operations", "elapsed_s")
            }
        ),
        flush=True,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--design", choices=("v1", "v2", "v3", "domain"), default="v3")
    parser.add_argument("--inventory-v2", action="store_true")
    parser.add_argument("--inventory-v3", action="store_true")
    args = parser.parse_args()
    correction = (
        inventory_v3()
        if args.inventory_v3
        else inventory_v2()
        if args.inventory_v2
        else nullcontext()
    )
    with correction:
        run(args.root.resolve(), args.report.resolve(), args.design)
