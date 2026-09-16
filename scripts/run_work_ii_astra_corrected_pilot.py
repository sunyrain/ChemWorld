"""Development pilot; see WORK_II_ASTRA_STATE_RESOLVED_PILOT_NOTE.md.

This is a new block. The closed single-trial runner and its evidence are historical.
"""

# ruff: noqa: RUF001
from __future__ import annotations

import argparse
import itertools
import json
import math
import secrets
import threading
import time
from collections import Counter
from copy import deepcopy
from pathlib import Path

import numpy as np
from scipy.optimize import linprog
from scripts.run_work_ii_astra_single_trial import (
    PROVIDER,
    ROOT,
    TASK,
    TRAIN,
    WORLDS,
    interventions,
    invoke,
    object_schema,
    read,
    write,
)
from scripts.run_work_ii_static_topology_q0 import _direct_measurement, _terminal_metrics

from chemworld.agents.base import BaseAgent
from chemworld.data.logging import load_jsonl
from chemworld.eval.runner import run_agent
from chemworld.eval.verify import verify_records
from chemworld.tasks import get_task
from chemworld.world.instruments import instrument_contracts

BOUNDS = {
    "reaction_temperature_K": (350.0, 405.0),
    "reaction_duration_s": (1200.0, 5400.0),
    "cooling_fraction": (0.0, 1.0),
    "cooling_duration_s": (1200.0, 7200.0),
}
METRICS = ("reaction_yield", "crystal_yield", "crystal_purity")
SOURCES = ("standard", "diagnostic")
TOTAL_PHYSICAL = 164
REPORT = (
    ROOT / "workstreams/flagship_tasks/reports/work-ii-astra-state-resolved-pilot-20260914.json"
)
NOTE = "workstreams/flagship_tasks/WORK_II_ASTRA_STATE_RESOLVED_PILOT_NOTE.md"


class ContractError(RuntimeError):
    """A runtime, replay or contract defect ends this development block."""


def plan(values):
    return dict(zip(BOUNDS, map(float, values), strict=True))


def validate_plan(value, *, bounds=None):
    bounds = BOUNDS if bounds is None else bounds
    if not isinstance(value, dict) or set(value) != set(bounds):
        raise ValueError("four numeric controls required; both HPLC measurements are mandatory")
    for key, (lo, hi) in bounds.items():
        v = value[key]
        if type(v) not in (float, int) or not math.isfinite(v) or not lo <= v <= hi:
            raise ValueError(f"control outside public domain: {key}")


def plan_schema():
    return object_schema(
        {k: {"type": "number", "minimum": lo, "maximum": hi} for k, (lo, hi) in BOUNDS.items()}
    )


def cooling_temperature(p, current_temperature_K):
    if not math.isfinite(current_temperature_K) or current_temperature_K < 275:
        raise ContractError("public current temperature outside the declared cooling domain")
    return 275.0 + p["cooling_fraction"] * (min(310.0, current_temperature_K) - 275.0)


def actions(p, *, current_temperature_K=298.15, bounds=None):
    """Template only; the controller resolves step eight from its public current schema."""
    validate_plan(p, bounds=bounds)
    return [
        {"operation": "add_solvent", "volume_L": 0.025, "solvent": 0},
        {"operation": "add_reagent", "amount_mol": 0.015},
        {"operation": "add_catalyst", "catalyst_amount_mol": 0.000315, "catalyst": 0},
        {
            "operation": "heat",
            "target_temperature_K": p["reaction_temperature_K"],
            "duration_s": p["reaction_duration_s"],
            "stirring_speed_rpm": 675.0,
        },
        {"operation": "quench"},
        {"operation": "measure", "instrument": "hplc"},
        {"operation": "seed_crystals", "seed_mass_g": 0.008},
        {
            "operation": "cool_crystallize",
            "target_temperature_K": cooling_temperature(p, current_temperature_K),
            "duration_s": p["cooling_duration_s"],
        },
        {"operation": "measure", "instrument": "hplc"},
        {"operation": "filter_crystals"},
        {"operation": "terminate"},
        {"operation": "measure", "instrument": "final_assay"},
    ]


def current_temperature(public_view):
    affordance = next(
        a
        for a in public_view["tool_json"]["available_actions"]
        if a["operation"] == "cool_crystallize"
    )
    constraint = next(
        c
        for c in affordance["schema"]["constraints"]
        if c["id"] == "payload_coupling:maximum_cooling_rate_K_s"
    )
    return float(constraint["parameters"]["current_temperature_K"])


class StateResolvedRecipeAgent(BaseAgent):
    name = "public_state_resolved_recipe"

    def __init__(self, p, *, bounds=None):
        self.plan = deepcopy(p)
        self.steps = actions(p, bounds=bounds)

    def reset(self, task_info, seed):
        super().reset(task_info, seed)
        self.index = 0

    def act(self, history):
        if self.index >= len(self.steps):
            raise ContractError("recipe exhausted its declared 12 operations")
        action = deepcopy(self.steps[self.index])
        if self.index == 7:
            temperature = current_temperature(history[-1].public_view)
            action["target_temperature_K"] = cooling_temperature(self.plan, temperature)
        self.index += 1
        return action


def product_utility(yield_estimate, recovery, purity, process_time_s):
    for value in (yield_estimate, recovery, purity):
        if not math.isfinite(value) or not 0 <= value <= 1:
            raise ValueError("public product component outside [0,1]")
    if not math.isfinite(process_time_s) or process_time_s <= 0:
        raise ValueError("positive recorded process time required")
    estimate = yield_estimate * (1 - 0.00020 / 0.025) * recovery * purity
    return {
        "quality_adjusted_recovery_estimate": estimate,
        "utility_per_hour": 3600 * estimate / process_time_s,
    }


def public_contract():
    instruments = instrument_contracts()
    return {
        "task": "Reaction followed by crystallization in a shared vessel",
        "learning_pairs": list(TRAIN),
        "heldout_pairs": list(WORLDS[2:]),
        "identity_semantics": "R1/R2 identify reusable reaction components, C1/C2 crystallizers. "
        "Labels give identity only, not kinetic or solubility properties. Same component laws "
        "persist across pairs. Unknown reversibility and solubility must be learned from data.",
        "objective": "Predict intervention responses and maximize utility_per_hour in new pairs.",
        "bounds": BOUNDS,
        "cooling_coordinate": "Heating temperature is a SETPOINT, not necessarily achieved. "
        "Immediately before cooling the shared recipe executor reads current_temperature_K "
        "from the public action schema and applies "
        "cooling_T=275+cooling_fraction*(min(310,current_temperature_K)-275), all K. "
        "The fraction is sealed in advance. No HPLC-dependent change or new model decision "
        "is allowed. All conditions use this same public state-resolved control mapping.",
        "mandatory_operations": [
            a["operation"] + (":" + a["instrument"] if "instrument" in a else "")
            for a in actions(plan((377.5, 3300, 0.5, 4200)))
        ],
        "fixed_materials": {
            "solvent_L": 0.025,
            "solvent_id": 0,
            "reactant_mol": 0.015,
            "catalyst_mol": 0.000315,
            "catalyst_id": 0,
            "seed_g": 0.008,
            "stirring_rpm": 675,
        },
        "interface": "Quench stops chemistry. Target, residual reactant, impurities, solvent "
        "volume and temperature pass downstream. HPLC immediately after quench AND immediately "
        "before filtration is mandatory, charged and cannot be omitted. HPLC samples remove "
        "0.00020 L each; initial solvent is 0.025 L. Seeds add target, but crystal_yield excludes "
        "retained seed and divides recovered solution-grown target by pre-seeding target. "
        "Crystal purity describes all filtered solids including seeds. No hidden-state access.",
        "utility": "quality_adjusted_recovery_estimate = upstream_HPLC_yield * "
        "(1-0.00020/0.025) * final_crystal_yield * final_crystal_purity; "
        "utility_per_hour = 3600 * quality_adjusted_recovery_estimate / actual_process_time_s. "
        "This is a noisy public-observation product estimate, not exact molar isolated yield. "
        "Use actual process time (reaction, quench, cooling, filtration). Legacy score is "
        "diagnostic only and is NOT the objective. Zero crystal recovery gives zero utility.",
        "resources": {
            "batches_per_source": 16,
            "source_rounds": 2,
            "actions_per_batch": 12,
            "per_call_numerics_limit": 8,
            "deployment": "one sealed recipe; cooling uses publicly observed current temperature",
        },
        "instruments": {k: instruments[k].to_dict() for k in ("hplc", "final_assay")},
        "measurement_warning": "Processed estimates are noisy; no unobserved value is a "
        "measurement. Final assay and two HPLCs consume samples/cost. All methods have the "
        "same tools, control domains and physical budget. No target feedback during readout.",
    }


def message(instruction, payload):
    return (
        "You are an experimental scientist. Use only the supplied public contract and records. "
        "You may use public_numerics.calculate up to eight times for arithmetic or least "
        "squares, no other tools or external context. Return requested JSON and concise "
        "scientific conclusions, not private chain-of-thought.\n"
        + instruction
        + "\nPUBLIC INPUT:\n"
        + json.dumps({"contract": public_contract(), **payload})
    )


def execute_batch(root, name, world, p, seed, *, bounds=None):
    folder = root / "physical" / name
    if folder.exists():
        if not (folder / "result.json").exists():
            raise ContractError(f"retained incomplete attempt cannot be replaced: {name}")
        result = read(folder / "result.json")
        if result.get("contract_failure"):
            raise ContractError(f"retained contract failure: {name}")
        return result
    folder.mkdir(parents=True)
    write(folder / "attempt.json", {"world": world, "plan": p, "started": time.time()})
    result = {
        "name": name,
        "world": world,
        "plan": p,
        "status": "failed",
        "failure": None,
        "contract_failure": False,
        "exact_replay": False,
        "public": None,
        "resources": {},
    }
    records = []
    validated = False
    try:
        actions(p, bounds=bounds)
        validated = True
        run_agent(
            env_id=get_task(TASK).env_id,
            agent=StateResolvedRecipeAgent(p, bounds=bounds),
            world_split="public-dev",
            budget=12,
            objective="balanced",
            seed=seed,
            agent_seed=0,
            observation_seed=seed + 1,
            task_id=TASK,
            output_path=folder / "trajectory.jsonl",
            budget_override=12,
            episode_mode_override="single_experiment",
            observation_noise_mode="keyed",
            observation_noise_namespace="work-ii-astra-corrected-pilot",
            world_interventions=interventions(world),
        )
        records = load_jsonl(folder / "trajectory.jsonl")
        if len(records) != 12 or any(r["transaction_status"] != "committed" for r in records):
            raise ContractError("compiled valid plan failed its 12-operation lifecycle")
        actual_quench = current_temperature(records[6]["agent_view"])
        expected_cooling = cooling_temperature(p, actual_quench)
        actual_cooling = records[7]["action"]["target_temperature_K"]
        if not math.isclose(actual_cooling, expected_cooling, abs_tol=1e-8):
            raise ContractError("recorded cooling action differs from public state mapping")
        if actual_cooling > actual_quench + 1e-8:
            raise ContractError("compiled cooling temperature exceeds actual state")
        upstream, observed = _direct_measurement(
            records, instrument="hplc", metrics=("yield", "conversion", "selectivity")
        )
        if not all(observed.values()):
            raise ContractError("required upstream observation missing")
        terminal = _terminal_metrics(records, ("yield", "crystal_yield", "crystal_purity", "score"))
        result["public"] = {
            "world": world,
            "plan": p,
            "actual_cooling_temperature_K": actual_cooling,
            "actual_quench_temperature_K": actual_quench,
            "upstream_hplc": upstream,
            "terminal": terminal,
            "observations": [
                {
                    "instrument": r["instrument"],
                    "processed_estimate": r["processed_estimate"],
                    "observed_mask": r["observed_mask"],
                    "uncertainty": r["uncertainty"],
                }
                for r in records
                if r["operation_type"] == "measure"
            ],
        }
        result["status"] = "completed"
    except Exception as exc:
        result["failure"] = {"type": type(exc).__name__, "message": str(exc)[:600]}
        result["contract_failure"] = validated
    if (folder / "trajectory.jsonl").exists():
        records = load_jsonl(folder / "trajectory.jsonl")
    result["resources"] = {
        "process_time_s": sum(
            r.get("state_delta_summary", {}).get("delta_time_s", 0) for r in records
        ),
        "cost_units": sum(r.get("state_delta_summary", {}).get("delta_cost", 0) for r in records),
        "sample_consumed_L": sum(r.get("sample_consumed", 0) for r in records),
        "measurement_cost_units": sum(r.get("measurement_cost", 0) for r in records),
        "operation_count": len(records),
    }
    result["failed_operations"] = [
        {
            "operation": r["operation_type"],
            "status": r["transaction_status"],
            "failed_preconditions": [
                k for k, v in r.get("preconditions", {}).items() if v is False
            ],
        }
        for r in records
        if r["transaction_status"] != "committed"
    ]
    if records:
        try:
            replay = verify_records(
                records, tolerance=0.0, world_interventions=interventions(world)
            ).to_dict()
            write(folder / "replay.json", replay)
            result["exact_replay"] = replay.get("verified") is True
            if not result["exact_replay"]:
                raise ContractError("exact replay failed")
        except Exception as exc:
            result.update(
                status="failed",
                contract_failure=True,
                failure={"type": type(exc).__name__, "message": str(exc)[:600]},
            )
    if result["status"] == "completed":
        terminal = result["public"]["terminal"]
        terminal.update(
            product_utility(
                result["public"]["upstream_hplc"]["yield"],
                terminal["crystal_yield"],
                terminal["crystal_purity"],
                result["resources"]["process_time_s"],
            )
        )
        result["public"]["resources"] = result["resources"]
    write(folder / "result.json", result)
    print(
        json.dumps(
            {"stage": "physical", "unit": name, "status": result["status"], "records": len(records)}
        ),
        flush=True,
    )
    if result["contract_failure"]:
        raise ContractError(f"{name}: {result['failure']}")
    return result


def qualification_plans():
    # OA(8,4,2,2): every pair of columns contains all four binary level pairs.
    return [
        plan([BOUNDS[k][j] for k, j in zip(BOUNDS, (a, b, c, a ^ b ^ c), strict=True)])
        for a, b, c in itertools.product((0, 1), repeat=3)
    ]


def qualification(root, seed):
    rows = [
        execute_batch(root, f"qualification/{w}/{i}", w, p, seed)
        for w in WORLDS
        for i, p in enumerate(qualification_plans())
    ]
    lookup = {(r["world"], int(r["name"].split("/")[-1])): r["public"] for r in rows}
    invariant = all(
        lookup[(r + "C1", i)]["upstream_hplc"] == lookup[(r + "C2", i)]["upstream_hplc"]
        for r in ("R1", "R2")
        for i in range(8)
    )
    diagnostics = {
        "runtime_pass": invariant and all(r["status"] == "completed" for r in rows),
        "upstream_invariant_to_C": invariant,
        "max_C_recovery_effect": max(
            abs(
                lookup[(r + "C1", i)]["terminal"]["crystal_yield"]
                - lookup[(r + "C2", i)]["terminal"]["crystal_yield"]
            )
            for r in ("R1", "R2")
            for i in range(8)
        ),
        "best_of_eight_utility_by_world": {
            w: max(lookup[(w, i)]["terminal"]["utility_per_hour"] for i in range(8)) for w in WORLDS
        },
        "full_identifiability_qualified": False,
    }
    write(root / "qualification.json", diagnostics)
    if not diagnostics["runtime_pass"]:
        raise ContractError("qualification failed")
    return diagnostics


def public_data(rows):
    return [
        deepcopy(r["public"])
        if r["status"] == "completed"
        else {k: r.get(k) for k in ("world", "plan", "status", "failure")}
        for r in rows
    ]


def source_data(root, source, seed, deadline):
    rows = []
    properties = {f"{w}_{i}": plan_schema() for w in TRAIN for i in range(4)}
    for round_index in range(2):
        instruction = (
            "Choose four batches per learning pair this round. There are two rounds and "
            "sixteen total batches; round two sees only your own first-round results. Learn "
            "responses for accurate blind predictions and high utility_per_hour in new pairs. "
        )
        instruction += (
            "Organize controlled contrasts around component hypotheses and uncertainties; "
            "distinguish reaction production from downstream recovery and test interface "
            "dependence. All valid public methods are allowed."
            if source == "diagnostic"
            else "Choose your own strategy using any valid public experimental or numerical method."
        )
        call = invoke(
            root,
            f"acquire_{source}_{round_index}",
            message(instruction, {"round": round_index + 1, "records": public_data(rows)}),
            object_schema(properties),
            deadline=deadline,
        )
        if call["status"] != "completed":
            break
        for key in properties:
            rows.append(
                execute_batch(
                    root,
                    f"source/{source}/{round_index}/{key}",
                    key.split("_")[0],
                    call["payload"].get(key, {}),
                    seed,
                )
            )
        write(root / f"source_{source}.json", rows)
    return rows


def encode(root, source, representation, data, deadline):
    props = (
        {"summary": {"type": "string", "maxLength": 4500}}
        if representation == "whole"
        else {
            k: {"type": "string", "maxLength": 900} for k in ("R1", "R2", "C1", "C2", "interface")
        }
    )
    instruction = (
        "Create reusable knowledge from these public records. Recipient has the same contract "
        "but no source records. Preserve numeric relations, uncertainty, limitations and "
        "failures useful for predicting interventions and maximizing product utility in unseen "
        "pairings. Target query coordinates and results are unavailable. "
    ) + (
        "Write one whole-process summary, at most 4500 characters; component reasoning is allowed."
        if representation == "whole"
        else "Write R1/R2/C1/C2/interface sections, at most 900 characters each, 4500 total."
    )
    call = invoke(
        root,
        f"encode_{source}_{representation}",
        message(instruction, {"records": public_data(data)}),
        object_schema(props),
        deadline=deadline,
    )
    payload = call.get("payload")
    valid = (
        call["status"] == "completed"
        and isinstance(payload, dict)
        and set(payload) == set(props)
        and all(
            isinstance(payload[k], str) and len(payload[k]) <= props[k]["maxLength"] for k in props
        )
    )
    write(
        root / "packages" / f"{source}_{representation}.json",
        {
            "valid": valid,
            "payload": payload if valid else None,
            "failure": None if valid else "missing_or_invalid_knowledge_package",
        },
    )
    return payload if valid else None


def upstream_features(p):
    t = (p["reaction_temperature_K"] - 377.5) / 27.5
    d = math.log(p["reaction_duration_s"] / 1200)
    return [1.0, t, d, t * d]


def downstream_features(p, y, conversion, temperature):
    return [
        1.0,
        y,
        conversion,
        (temperature - 332.5) / 27.5,
        (cooling_temperature(p, temperature) - 292.5) / 17.5,
        math.log(p["cooling_duration_s"] / 1200),
    ]


def whole_features(p, w):
    return [
        *upstream_features(p),
        2 * p["cooling_fraction"] - 1,
        math.log(p["cooling_duration_s"] / 1200),
        float(w.startswith("R2")),
        float(w.endswith("C2")),
    ]


def ridge(x, y):
    a, b = np.asarray(x), np.asarray(y)
    penalty = np.eye(a.shape[1]) * 0.01
    penalty[0, 0] = 0
    return np.linalg.solve(a.T @ a + penalty, a.T @ b).tolist()


def fit_reference(rows):
    valid = [r["public"] for r in rows if r["status"] == "completed"]
    model = {"R": {}, "C": {}, "whole": None, "overhead_s": 500.0}
    if valid:
        model["overhead_s"] = float(
            np.mean(
                [
                    r["resources"]["process_time_s"]
                    - r["plan"]["reaction_duration_s"]
                    - r["plan"]["cooling_duration_s"]
                    for r in valid
                ]
            )
        )
    for label in ("R1", "R2", "C1", "C2"):
        group = [r for r in valid if label in r["world"]]
        if len(group) < 6:
            continue
        if label.startswith("R"):
            model["R"][label] = ridge(
                [upstream_features(r["plan"]) for r in group],
                [
                    [
                        r["upstream_hplc"]["yield"],
                        r["upstream_hplc"]["conversion"],
                        (r["actual_quench_temperature_K"] - 298.15) / 70,
                    ]
                    for r in group
                ],
            )
        else:
            model["C"][label] = ridge(
                [
                    downstream_features(
                        r["plan"],
                        r["upstream_hplc"]["yield"],
                        r["upstream_hplc"]["conversion"],
                        r["actual_quench_temperature_K"],
                    )
                    for r in group
                ],
                [[r["terminal"][k] for k in METRICS[1:]] for r in group],
            )
    if len(valid) >= 10:
        model["whole"] = ridge(
            [whole_features(r["plan"], r["world"]) for r in valid],
            [
                [r["upstream_hplc"]["yield"], *[r["terminal"][k] for k in METRICS[1:]]]
                for r in valid
            ],
        )
    return model


def predict_reference(model, w, p, kind="component"):
    if kind == "whole":
        if model["whole"] is None:
            return None
        values = np.clip(np.asarray(whole_features(p, w)) @ model["whole"], 0, 1)
    else:
        if w[:2] not in model["R"] or w[2:] not in model["C"]:
            return None
        y, conversion, scaled_temperature = np.clip(
            np.asarray(upstream_features(p)) @ model["R"][w[:2]], 0, 1
        )
        temperature = 298.15 + 70 * scaled_temperature
        downstream = np.clip(
            np.asarray(downstream_features(p, y, conversion, temperature)) @ model["C"][w[2:]], 0, 1
        )
        values = np.r_[y, downstream]
    result = dict(zip(METRICS, map(float, values), strict=True))
    result.update(
        product_utility(
            *values, p["reaction_duration_s"] + p["cooling_duration_s"] + model["overhead_s"]
        )
    )
    return result


def repaired_package(base, rows, kind):
    fixed = deepcopy(base)
    for label in (kind + "1", kind + "2"):
        data = [r["public"] for r in rows if r["status"] == "completed" and label in r["world"]]
        table = []
        for r in data:
            p, h, t = r["plan"], r["upstream_hplc"], r["terminal"]
            values = (
                [
                    p["reaction_temperature_K"],
                    p["reaction_duration_s"] / 1000,
                    h["yield"],
                    h["conversion"],
                    h["selectivity"],
                ]
                if kind == "R"
                else [
                    h["yield"],
                    h["conversion"],
                    r["actual_quench_temperature_K"],
                    r["actual_cooling_temperature_K"],
                    p["cooling_duration_s"] / 1000,
                    t["crystal_yield"],
                    t["crystal_purity"],
                ]
            )
            table.append([round(v, 3) for v in values])
        header = (
            "Measured source rows [TR_K,tR_1000s,yield,conversion,selectivity]:"
            if kind == "R"
            else "Measured source rows "
            "[inlet_yield,conversion,Tquench_K,TC_K,tC_1000s,recovery,purity]:"
        )
        text = (
            header
            + json.dumps(table, separators=(",", ":"))
            + "; noisy local data, not a true law; no target feedback."
        )
        if len(text) > 900:
            raise ValueError("public numeric repair exceeds fixed slot")
        fixed[label] = text
    return fixed


def swapped_package(base, kind):
    if base is None:
        return None

    def rename(text):
        return (
            text.replace(kind + "1", "__COMPONENT_SWAP__")
            .replace(kind + "2", kind + "1")
            .replace("__COMPONENT_SWAP__", kind + "2")
        )

    return {rename(key): rename(value) for key, value in base.items()}


def queries():
    controls = [(355, 2100, 0.2, 2400), (382, 3900, 0.55, 4800), (400, 1500, 0.85, 6600)]
    return {
        f"{w}_q{i}": {
            "world": w,
            "plan": plan(p),
        }
        for w in WORLDS
        for i, p in enumerate(controls)
    }


def readout(root, name, packet, seed, deadline):
    if packet is None:
        return {"name": name, "status": "not_started", "failure": "missing_source_or_package"}
    schema = object_schema(
        {
            "predictions": object_schema(
                {
                    q: object_schema(
                        {k: {"type": "number", "minimum": 0, "maximum": 1} for k in METRICS}
                    )
                    for q in queries()
                }
            ),
            "deployments": object_schema({w: plan_schema() for w in WORLDS}),
        }
    )
    call = invoke(
        root,
        f"read_{name}",
        message(
            "Predict all blind queries: reaction_yield is upstream HPLC yield; crystal_yield and "
            "crystal_purity are final assay outcomes. Then choose one full deployment per world "
            "to maximize utility_per_hour, using mandatory assays and the cooling coordinate. "
            "No target feedback or extra physical experiment is available. All four plans are "
            "sealed together. Predictions must lie in [0,1].",
            {"knowledge_delivery": packet, "blind_queries": queries()},
        ),
        schema,
        deadline=deadline,
    )
    result = {
        "name": name,
        "status": call["status"],
        "failure": call.get("failure"),
        "deployments": [],
    }
    if call["status"] == "completed":
        try:
            payload = call["payload"]
            if set(payload["predictions"]) != set(queries()) or set(payload["deployments"]) != set(
                WORLDS
            ):
                raise ValueError("readout denominator mismatch")
            for pred in payload["predictions"].values():
                if set(pred) != set(METRICS) or any(
                    type(v) not in (int, float) or not 0 <= v <= 1 for v in pred.values()
                ):
                    raise ValueError("invalid prediction")
            result["predictions"] = payload["predictions"]
            # Each invalid plan is retained independently; no output correction or retry.
            for w in WORLDS:
                result["deployments"].append(
                    execute_batch(root, f"deploy/{name}/{w}", w, payload["deployments"][w], seed)
                )
        except (ValueError, KeyError, TypeError) as exc:
            result.update(status="failed", failure=f"invalid_readout: {exc}")
    return result


def support_vector(public):
    p, h = public["plan"], public["upstream_hplc"]
    return [
        h["yield"],
        h["conversion"],
        (public["actual_quench_temperature_K"] - 305) / 55,
        (public["actual_cooling_temperature_K"] - 275) / 35,
        math.log(p["cooling_duration_s"] / 1200) / math.log(6),
    ]


def hull_distance(points, target):
    a, t = np.asarray(points, dtype=float), np.asarray(target, dtype=float)
    if not len(a):
        return None
    n, d = a.shape
    solution = linprog(
        np.r_[np.zeros(n), 1],
        A_ub=np.vstack([np.c_[a.T, -np.ones(d)], np.c_[-a.T, -np.ones(d)]]),
        b_ub=np.r_[t, -t],
        A_eq=[np.r_[np.ones(n), 0]],
        b_eq=[1],
        bounds=[(0, None)] * (n + 1),
        method="highs",
    )
    if not solution.success:
        raise ValueError("support distance optimization failed")
    return max(0.0, float(solution.fun))


def support_report(sources, truth):
    output = []
    for source, rows in sources.items():
        valid = [r["public"] for r in rows if r["status"] == "completed"]
        for q, actual in truth.items():
            if actual["status"] != "completed":
                continue
            candidates = [r for r in valid if r["world"][2:] == actual["world"][2:]]
            distance = hull_distance(
                [support_vector(r) for r in candidates], support_vector(actual["public"])
            )
            output.append(
                {
                    "source": source,
                    "query": q,
                    "world": actual["world"],
                    "distance": distance,
                    "near_support": distance is not None and distance <= 0.05,
                    "learning_feed_yield_range": [
                        min(r["upstream_hplc"]["yield"] for r in candidates),
                        max(r["upstream_hplc"]["yield"] for r in candidates),
                    ]
                    if candidates
                    else None,
                    "test_feed_yield": actual["public"]["upstream_hplc"]["yield"],
                }
            )
    return output


def run(root):
    inputs = read(root / "private_inputs.json")
    seed, deadline = inputs["seed"], inputs["deadline"]
    qualification(root, seed)
    sources, packages, references = {}, {}, {}
    # Reference coverage is fixed before any Agent outcomes are available.
    indices = [(i, (3 * i + 1) % 8, (5 * i + 2) % 8, (7 * i + 3) % 8) for i in range(8)]
    sources["space_filling"] = [
        execute_batch(
            root,
            f"source/space_filling/{w}/{i}",
            w,
            plan([lo + (hi - lo) * j / 7 for j, (lo, hi) in zip(ix, BOUNDS.values(), strict=True)]),
            seed,
        )
        for w in TRAIN
        for i, ix in enumerate(indices)
    ]
    write(root / "source_space_filling.json", sources["space_filling"])
    for source in SOURCES:
        sources[source] = source_data(root, source, seed, deadline)
        complete = len(sources[source]) == 16 and all(
            r["status"] == "completed" for r in sources[source]
        )
        for representation in ("whole", "component"):
            packages[f"{source}_{representation}"] = (
                encode(root, source, representation, sources[source], deadline)
                if complete
                else None
            )
    write(root / "packages.json", packages)
    references = {s: fit_reference(rows) for s, rows in sources.items()}
    write(root / "reference_models.json", references)
    truth = {}
    for q, value in queries().items():
        truth[q] = execute_batch(root, f"blind/{q}", value["world"], value["plan"], seed)
        write(root / "blind_truth.json", truth)
    write(root / "support.json", support_report(sources, truth))
    conditions = {}
    for source in SOURCES:
        complete = len(sources[source]) == 16 and all(
            r["status"] == "completed" for r in sources[source]
        )
        conditions[f"{source}_raw"] = (
            {"records": public_data(sources[source])} if complete else None
        )
        for representation in ("whole", "component"):
            conditions[f"{source}_{representation}"] = packages[f"{source}_{representation}"]
    conditions["task_only"] = {}
    base = packages["standard_component"]
    for kind in ("R", "C"):
        conditions[f"standard_swap_{kind}"] = swapped_package(base, kind)
    conditions["standard_sham"] = dict(reversed(list(base.items()))) if base is not None else None
    for kind in ("R", "C"):
        conditions[f"standard_repair_{kind}"] = (
            repaired_package(base, sources["standard"], kind) if base is not None else None
        )
    write(root / "deliveries.json", conditions)
    readouts = []
    for name, packet in conditions.items():
        if time.time() >= deadline:
            raise ContractError("block deadline; remaining conditions not started")
        readouts.append(readout(root, name, packet, seed, deadline))
        write(root / "readouts.json", readouts)
    grid = [
        plan(v) for v in itertools.product(*[(lo, (lo + hi) / 2, hi) for lo, hi in BOUNDS.values()])
    ]
    reference_rows = []
    for source in SOURCES:
        for kind in ("component", "whole", "best_history"):
            for w in WORLDS:
                valid = [r for r in sources[source] if r["status"] == "completed"]
                if kind == "best_history":
                    # Seen pair: its own history; unseen pair: all source records, fixed rule.
                    eligible = [r for r in valid if r["world"] == w] if w in TRAIN else valid
                    chosen = (
                        max(eligible, key=lambda r: r["public"]["terminal"]["utility_per_hour"])[
                            "plan"
                        ]
                        if eligible
                        else None
                    )
                else:
                    candidates = [
                        (p, predict_reference(references[source], w, p, kind)) for p in grid
                    ]
                    valid_predictions = [(p, pred) for p, pred in candidates if pred is not None]
                    chosen = (
                        max(valid_predictions, key=lambda item: item[1]["utility_per_hour"])[0]
                        if valid_predictions
                        else None
                    )
                name = f"reference/{source}/{kind}/{w}"
                reference_rows.append(
                    execute_batch(root, name, w, chosen, seed)
                    if chosen
                    else {
                        "name": name,
                        "status": "not_started",
                        "failure": "reference_not_fittable",
                    }
                )
                write(root / "reference_deployments.json", reference_rows)


def summary(root, failure=None):
    physical = [read(p) for p in sorted((root / "physical").rglob("result.json"))]
    calls = [read(p) for p in sorted((root / "model").glob("*/result.json"))]
    attempts = list((root / "physical").rglob("attempt.json"))
    readouts = read(root / "readouts.json") if (root / "readouts.json").exists() else []
    truth = read(root / "blind_truth.json") if (root / "blind_truth.json").exists() else {}
    support = read(root / "support.json") if (root / "support.json").exists() else []
    source_rows = {
        s: read(root / f"source_{s}.json")
        for s in (*SOURCES, "space_filling")
        if (root / f"source_{s}.json").exists()
    }
    support_lookup = {(r["source"], r["query"]): r["near_support"] for r in support}
    conditions = []
    for row in readouts:
        result = {
            "condition": row["name"],
            "status": row["status"],
            "failure": row.get("failure"),
            "errors": [],
        }
        if "predictions" in row:
            source = "diagnostic" if row["name"].startswith("diagnostic") else "standard"
            for q, actual in truth.items():
                if actual["status"] != "completed":
                    continue
                target = {
                    "reaction_yield": actual["public"]["upstream_hplc"]["yield"],
                    **{k: actual["public"]["terminal"][k] for k in METRICS[1:]},
                }
                pred = row["predictions"][q]
                result["errors"].append(
                    {
                        "query": q,
                        "world": actual["world"],
                        "truth": target,
                        "prediction": pred,
                        "absolute_error": {k: abs(pred[k] - target[k]) for k in METRICS},
                        "near_support": support_lookup.get((source, q))
                        if row["name"] != "task_only"
                        else None,
                    }
                )
            result["mae"] = {}
            for split, worlds in (("learning", TRAIN), ("heldout", WORLDS[2:])):
                errors = [r for r in result["errors"] if r["world"] in worlds]
                result["mae"][split] = {
                    "valid_queries": len(errors),
                    "planned_queries": 6,
                    **{
                        k: float(np.mean([r["absolute_error"][k] for r in errors]))
                        if errors
                        else None
                        for k in METRICS
                    },
                }
            result["deployment"] = {
                r["world"]: {
                    "status": r["status"],
                    "plan": r["plan"],
                    "utility_per_hour": r["public"]["terminal"]["utility_per_hour"]
                    if r["status"] == "completed"
                    else 0.0,
                    "quality_adjusted_recovery_estimate": r["public"]["terminal"][
                        "quality_adjusted_recovery_estimate"
                    ]
                    if r["status"] == "completed"
                    else 0.0,
                }
                for r in row["deployments"]
            }
        conditions.append(result)
    usage = Counter()
    for call in calls:
        usage.update(call.get("receipt", {}).get("usage", {}))
    count = Counter(r["status"] for r in physical)
    stages = {}
    for row in physical:
        stages.setdefault(row["name"].split("/")[0], Counter())[row["status"]] += 1
    resources = Counter()
    for row in physical:
        resources.update(row["resources"])
    payload = {
        "schema_version": "work-ii-astra-corrected-pilot-1",
        "formal_result": False,
        "status": "development_stopped" if failure else "development_completed",
        "stop_reason": failure,
        "model": PROVIDER["model"],
        "reasoning_effort": "medium",
        "independent_groups": 1,
        "experiment_note": NOTE,
        "model_calls": {
            "planned": 20,
            "attempted": len(calls),
            "completed": sum(c["status"] == "completed" for c in calls),
            "failed": sum(c["status"] == "failed" for c in calls),
            "not_started": 20 - len(calls),
            "retries": 0,
        },
        "physical_runs": {
            "planned": TOTAL_PHYSICAL,
            "attempted": len(attempts),
            "completed": count["completed"],
            "failed": count["failed"],
            "interrupted": len(attempts) - len(physical),
            "not_started": TOTAL_PHYSICAL - len(attempts),
            "exact_replay_verified": sum(r["exact_replay"] for r in physical),
        },
        "stages": stages,
        "conditions": conditions,
        "support": support,
        "reported_model_usage": dict(usage),
        "physical_resources": dict(resources),
        "subscription_usd_cost": None,
        "model_call_rows": [
            {
                "name": c["name"],
                "status": c["status"],
                "failure": c.get("failure"),
                "usage": c.get("receipt", {}).get("usage", {}),
                "wall_seconds": c.get("receipt", {}).get("elapsed_s"),
            }
            for c in calls
        ],
        "qualification": read(root / "qualification.json")
        if (root / "qualification.json").exists()
        else None,
        "source_counts": {
            s: {"completed": sum(r["status"] == "completed" for r in rows), "planned": 16}
            for s, rows in source_rows.items()
        },
        "physical_rows": [
            {
                k: r[k]
                for k in (
                    "name",
                    "world",
                    "plan",
                    "status",
                    "failure",
                    "contract_failure",
                    "exact_replay",
                    "resources",
                    "failed_operations",
                )
            }
            | {
                "upstream_hplc": r["public"]["upstream_hplc"] if r["public"] else None,
                "terminal": r["public"]["terminal"] if r["public"] else None,
            }
            for r in physical
        ],
        "limits": [
            "One constructed group and one call per condition; no population inference.",
            "Sealed workflow with public temperature-resolved cooling; "
            "no HPLC-adaptive decisions.",
            "Public-observation product proxy, not exact isolated product moles.",
            "Measured convex-hull support is not complete hidden-interface support.",
            "Public ridge baselines are not qualified strong identification methods.",
            "Sham/content differences include fresh-call variability; no causal population claim.",
        ],
    }
    write(root / "summary.json", payload)
    write(REPORT, payload)
    lines = [
        "# Astra medium：修正合同后的单次开发实验",
        "",
        f"状态：{payload['status']}；仅一个反应—结晶四格组，每条件一次。",
        "",
        f"模型 {payload['model_calls']['completed']}/20 完成；"
        f"物理 {count['completed']}/{TOTAL_PHYSICAL} 完成；"
        f"失败 {count['failed']}，未启动 {TOTAL_PHYSICAL - len(attempts)}；"
        f"重放通过 {payload['physical_runs']['exact_replay_verified']}。",
        "",
        "评分为基于公开测量的质量加权回收估计/过程小时，扣除晶种回收；旧score只作诊断。",
        "不是精确摩尔产率。学习/留出各6个查询；无独立复现，不作系统性失效推断。",
        "",
        "| 条件 | 留出反应MAE | 留出回收MAE | 留出纯度MAE | R1C2效用/小时 | R2C1效用/小时 |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for r in conditions:
        if "mae" not in r:
            lines.append(f"| {r['condition']} | 未完成 | — | — | — | — |")
            continue
        e, d = r["mae"]["heldout"], r["deployment"]
        lines.append(
            f"| {r['condition']} | {e['reaction_yield']:.4f} | {e['crystal_yield']:.4f} | "
            f"{e['crystal_purity']:.4f} | {d.get('R1C2', {}).get('utility_per_hour', 0):.4f} | "
            f"{d.get('R2C1', {}).get('utility_per_hour', 0):.4f} |"
        )
    lines += [
        "",
        "## 支持域与失败",
        "",
        "近支持使用事前固定的公开5维凸包距离≤0.05；不等于完整隐状态支持。",
    ]
    for s in source_rows:
        items = [r for r in support if r["source"] == s and r["world"] in WORLDS[2:]]
        lines.append(
            f"- {s}：留出查询近支持 {sum(r['near_support'] for r in items)}/{len(items)}。"
        )
    if failure:
        lines.append(f"- 停止原因：{failure}")
    for r in [*physical, *calls]:
        if r["status"] != "completed":
            lines.append(f"- {r['name']}：{r.get('failure')}")
    lines += [
        "",
        "逐批资源、预测真值/误差、部署参数及参考结果见同名JSON；原始provider及私有初始化留在ignored运行目录。",
        "",
        f"报告token用量：`{json.dumps(dict(usage))}`。美元费用未估算。",
        "",
    ]
    REPORT.with_suffix(".md").write_text("\n".join(lines), encoding="utf-8")
    print(
        json.dumps({k: payload[k] for k in ("status", "model_calls", "physical_runs")}), flush=True
    )
    return payload


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("run", "summarize"))
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--initialization-from", type=Path)
    args = parser.parse_args()
    root = args.output.resolve()
    if args.mode == "summarize":
        previous = read(root / "closed.json") if (root / "closed.json").exists() else {}
        summary(root, previous.get("failure"))
        return
    root.mkdir(parents=True, exist_ok=False)
    started = time.monotonic()
    write(
        root / "private_inputs.json",
        {
            "seed": read(args.initialization_from / "private_inputs.json")["seed"]
            if args.initialization_from
            else secrets.randbelow(1_000_000) + 10_000,
            "deadline": time.time() + 14400,
        },
    )
    write(root / "public_contract.json", public_contract())
    write(
        root / "design.json",
        {
            "qualification": qualification_plans(),
            "queries": queries(),
            "physical_planned": TOTAL_PHYSICAL,
            "models_planned": 20,
        },
    )
    stop = threading.Event()

    def heartbeat():
        while not stop.wait(30):
            count = len(list((root / "physical").rglob("result.json")))
            calls = len(list((root / "model").glob("*/result.json")))
            elapsed = time.monotonic() - started
            rate = count * 60 / elapsed
            print(
                json.dumps(
                    {
                        "stage": "pilot",
                        "completed_physical": count,
                        "planned_physical": TOTAL_PHYSICAL,
                        "completed_calls": calls,
                        "planned_calls": 20,
                        "physical_per_minute": round(rate, 2),
                        "eta_minutes": round((TOTAL_PHYSICAL - count) / rate, 1) if rate else None,
                        "elapsed_s": round(elapsed),
                    }
                ),
                flush=True,
            )

    worker = threading.Thread(target=heartbeat, daemon=True)
    worker.start()
    failure = None
    try:
        run(root)
    except (Exception, KeyboardInterrupt) as exc:
        failure = f"{type(exc).__name__}: {exc}"
    finally:
        stop.set()
        worker.join(timeout=2)
        write(root / "closed.json", {"failure": failure, "resume_planned": False})
        summary(root, failure)
    if failure:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
