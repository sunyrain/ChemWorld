"""One development trial of intervention acquisition and component transfer.

No formal-evidence gates, provider retries, seed replacement, or automatic reruns.
See WORK_II_ASTRA_SINGLE_TRIAL_NOTE.md for the fixed scope and denominators.
"""

# ruff: noqa: RUF001

from __future__ import annotations

import argparse
import itertools
import json
import math
import secrets
import tempfile
import threading
import time
from copy import deepcopy
from dataclasses import asdict
from pathlib import Path

import numpy as np
from scripts.run_work_ii_final_diagnostic import build_command, launch, write
from scripts.run_work_ii_static_topology_q0 import _direct_measurement, _terminal_metrics
from scripts.run_work_ii_study_b import _prepare_codex_home

from chemworld.data.logging import load_jsonl
from chemworld.eval.runner import run_agent
from chemworld.eval.verify import verify_records
from chemworld.eval.work_ii_static_topology_q0 import topology_intervention
from chemworld.eval.work_ii_truth import _FrozenTruthReplayAgent
from chemworld.tasks import get_task
from chemworld.world.instruments import instrument_contracts
from chemworld.world.scoring import OBJECTIVES, TaskScoringContract

ROOT = Path(__file__).resolve().parents[1]
TASK = "reaction-to-crystallization"
WORLDS = ("R1C1", "R2C2", "R1C2", "R2C1")
TRAIN = WORLDS[:2]
SOURCES = ("standard", "diagnostic")
BOUNDS = {
    "reaction_temperature_K": (350.0, 405.0),
    "reaction_duration_s": (1200.0, 5400.0),
    "cooling_temperature_K": (275.0, 310.0),
    "cooling_duration_s": (1200.0, 7200.0),
}
METRICS = ("reaction_yield", "crystal_yield", "crystal_purity")
PROVIDER = {
    "id": "chemworld_openai_https",
    "name": "OpenAI",
    "model": "gpt-6-astra",
    "reasoning_effort": "medium",
    "auth_mode": "chatgpt_subscription_cached_login",
    "wire_api": "responses",
}


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def object_schema(properties: dict) -> dict:
    return {
        "type": "object",
        "properties": properties,
        "required": list(properties),
        "additionalProperties": False,
    }


def plan_schema() -> dict:
    return object_schema(
        {
            **{
                k: {"type": "number", "minimum": lo, "maximum": hi}
                for k, (lo, hi) in BOUNDS.items()
            },
            "intermediate_hplc": {"type": "boolean"},
        }
    )


def plan(values, *, assay=True) -> dict:
    return {**dict(zip(BOUNDS, map(float, values), strict=True)), "intermediate_hplc": assay}


def validate_plan(value: dict) -> None:
    if set(value) != {*BOUNDS, "intermediate_hplc"}:
        raise ValueError("plan fields differ from the public contract")
    for key, (low, high) in BOUNDS.items():
        number = value[key]
        if type(number) not in (float, int) or not low <= number <= high:
            raise ValueError(f"invalid control: {key}")
    if type(value["intermediate_hplc"]) is not bool:
        raise ValueError("intermediate_hplc must be boolean")


def actions(value: dict) -> list[dict]:
    validate_plan(value)
    steps = [
        {"operation": "add_solvent", "volume_L": 0.025, "solvent": 0},
        {"operation": "add_reagent", "amount_mol": 0.015},
        {"operation": "add_catalyst", "catalyst_amount_mol": 0.000315, "catalyst": 0},
        {
            "operation": "heat",
            "target_temperature_K": value["reaction_temperature_K"],
            "duration_s": value["reaction_duration_s"],
            "stirring_speed_rpm": 675.0,
        },
        {"operation": "quench"},
    ]
    if value["intermediate_hplc"]:
        steps.append({"operation": "measure", "instrument": "hplc"})
    steps.extend(
        [
            {"operation": "seed_crystals", "seed_mass_g": 0.008},
            {
                "operation": "cool_crystallize",
                "target_temperature_K": value["cooling_temperature_K"],
                "duration_s": value["cooling_duration_s"],
            },
            {"operation": "measure", "instrument": "hplc"},
            {"operation": "filter_crystals"},
            {"operation": "terminate"},
            {"operation": "measure", "instrument": "final_assay"},
        ]
    )
    return steps


def interventions(world: str) -> list[dict]:
    if world not in WORLDS:
        raise ValueError("unknown component pair")
    return ([topology_intervention()] if world.startswith("R2") else []) + [
        {
            "axis_id": "crystallization.solubility-cooling-profile",
            "mode": "extrapolation",
            "severity": -1.0 if world.endswith("C1") else 1.0,
        }
    ]


def public_contract() -> dict:
    task = get_task(TASK)
    instruments = instrument_contracts()
    return {
        "task": "Reaction followed by crystallization, in a shared physical vessel",
        "objective": "Learn reusable component responses and maximize first-deployment score.",
        "learning_pairs": list(TRAIN),
        "heldout_pairs": list(WORLDS[2:]),
        "identity_semantics": "R1/R2 are reaction components; C1/C2 reusable crystallizers. "
        "Labels convey identity only. Laws remain the same across pairs. Unknown instance laws "
        "must be learned; any candidate reaction reversibility and solubility scale are unknown.",
        "interface": "Reaction produces target and impurities. Quench stops reaction. Amounts, "
        "composition, solvent volume and temperature pass to crystallization. A paid HPLC after "
        "quench provides upstream yield/conversion/selectivity. Seeds add target material; final "
        "crystal yield is a recovery fraction, not necessarily the upstream reaction yield. "
        "No free cloning or hidden-state inspection. Every proposed plan starts a new batch.",
        "bounds": BOUNDS,
        "fixed_workflow_example": actions(plan((377.5, 3300, 292.5, 4200))),
        "resources": {
            "source_batches_per_strategy": 12,
            "maximum_actions_per_batch": 12,
            "per_call_numerics_limit": 8,
            "deployment": "one sealed open-loop batch",
        },
        "instruments": {k: instruments[k].to_dict() for k in ("hplc", "final_assay")},
        "score_contract": TaskScoringContract.from_success_metrics(
            objective=task.objective, success_metrics=task.success_metrics
        ).to_dict(),
        "reaction_score_weights": asdict(OBJECTIVES[task.objective]),
        "score_formula": "reaction_score=clip(yield_weight*yield + selectivity_weight*selectivity "
        "+ conversion_weight*conversion - cost_penalty*cost - risk_penalty*safety_risk,0,1); "
        "terminal score=clip(sum(component_weights*terminal_component),0,1). "
        "Crystal yield excludes retained seed and divides recovered solution-grown target by "
        "pre-crystallization target amount. Crystal purity is target/(target+impurity) in solids.",
        "measurement_warning": "Intermediate observations are noisy and consume sample, time "
        "and cost. Final assay reports the terminal outcome. Do not assume unobserved yield "
        "or that crystal yield equals total material produced. Model values are not measurements.",
        "numerical_tool": "Use public_numerics.calculate for public arithmetic and lstsq; "
        "same 8-call limit for every condition; no files, network or simulator tool.",
    }


def execute_batch(root: Path, name: str, world: str, value: dict, seed: int) -> dict:
    folder = root / "physical" / name
    if folder.exists():
        return read(folder / "result.json")  # exact continuation, never a replacement run
    folder.mkdir(parents=True)
    write(folder / "attempt.json", {"world": world, "plan": value, "started": time.time()})
    result = {
        "name": name,
        "world": world,
        "plan": value,
        "status": "failed",
        "failure": None,
        "exact_replay": False,
        "public": None,
    }
    records = []
    try:
        steps = actions(value)
        run_agent(
            env_id=get_task(TASK).env_id,
            agent=_FrozenTruthReplayAgent(steps),
            world_split="public-dev",
            budget=len(steps),
            objective="balanced",
            seed=seed,
            agent_seed=0,
            observation_seed=seed + 1,
            task_id=TASK,
            output_path=folder / "trajectory.jsonl",
            budget_override=len(steps),
            episode_mode_override="single_experiment",
            observation_noise_mode="keyed",
            observation_noise_namespace="work-ii-astra-single-trial",
            world_interventions=interventions(world),
        )
        records = load_jsonl(folder / "trajectory.jsonl")
        replay = verify_records(
            records, tolerance=0.0, world_interventions=interventions(world)
        ).to_dict()
        write(folder / "replay.json", replay)
        result["exact_replay"] = replay.get("verified") is True
        noncommitted = [r for r in records if r.get("transaction_status") != "committed"]
        result["transaction_failures"] = [
            {k: r.get(k) for k in ("operation_type", "transaction_status", "rollback_reason")}
            for r in noncommitted
        ]
        if not result["exact_replay"]:
            raise ValueError("exact replay failed")
        if noncommitted:
            raise ValueError("one or more submitted operations did not commit")
        upstream = None
        if value["intermediate_hplc"]:
            upstream, observed = _direct_measurement(
                records, instrument="hplc", metrics=("yield", "conversion", "selectivity")
            )
            if not all(observed.values()):
                raise ValueError("missing intermediate measurement mask")
        terminal = _terminal_metrics(records, ("yield", "crystal_yield", "crystal_purity", "score"))
        final = next(r for r in records if r.get("instrument") == "final_assay")
        measurements = [
            {
                k: r.get(k)
                for k in (
                    "instrument",
                    "raw_signal",
                    "processed_estimate",
                    "observed_mask",
                    "measurement_cost",
                    "sample_consumed_L",
                    "uncertainty",
                )
            }
            for r in records
            if r.get("operation_type") == "measure"
        ]
        resource_keys = [
            k
            for k in final
            if any(
                s in k.lower()
                for s in ("cost", "resource", "ledger", "time", "energy", "sample_consum")
            )
        ]
        public = {
            "world": world,
            "plan": value,
            "upstream_hplc": upstream,
            "terminal": terminal,
            "measurements": measurements,
            "submitted_actions": len(records),
            "resources": {k: final[k] for k in resource_keys},
            "physical_resources": {
                "time_s": sum(
                    r.get("state_delta_summary", {}).get("delta_time_s", 0) for r in records
                ),
                "cost": sum(r.get("state_delta_summary", {}).get("delta_cost", 0) for r in records),
                "sample_consumed_L": sum(r.get("sample_consumed", 0) for r in records),
                "operations": len(records),
                "measurement_cost": sum(r.get("measurement_cost", 0) for r in records),
            },
        }
        result.update(status="completed", public=public)
    except Exception as exc:
        result["failure"] = {"type": type(exc).__name__, "message": str(exc)[:800]}
    write(folder / "result.json", result)
    print(
        json.dumps(
            {
                "stage": "physical",
                "unit": name,
                "world": world,
                "status": result["status"],
                "records": len(records),
            },
            ensure_ascii=False,
        ),
        flush=True,
    )
    return result


def qualification(root: Path) -> dict:
    if (root / "qualification_v2.json").exists():
        return read(root / "qualification_v2.json")
    seed = read(root / "private_inputs.json")["seed"]
    controls = [plan((377.5, 3300, 292.5, 4200)), plan((405, 5400, 275, 7200))]
    rows = [
        execute_batch(root, f"qualification_v2/{world}/{i}", world, p, seed)
        for world in WORLDS
        for i, p in enumerate(controls)
    ]
    completed = all(r["status"] == "completed" for r in rows)
    same_upstream = False
    differences = {}
    if completed:
        lookup = {(r["world"], r["name"].rsplit("/", 1)[1]): r["public"] for r in rows}
        same_upstream = all(
            lookup[(r + "C1", str(i))]["upstream_hplc"]
            == lookup[(r + "C2", str(i))]["upstream_hplc"]
            for r in ("R1", "R2")
            for i in range(2)
        )
        for i in range(2):
            for r in ("R1", "R2"):
                differences[f"{r}/control{i}"] = (
                    lookup[(r + "C2", str(i))]["terminal"]["crystal_yield"]
                    - lookup[(r + "C1", str(i))]["terminal"]["crystal_yield"]
                )
    result = {
        "planned": 8,
        "completed": sum(r["status"] == "completed" for r in rows),
        "runtime_pass": completed and same_upstream,
        "upstream_invariant_to_C": same_upstream,
        "C_effects": differences,
        "rows": rows,
        "identifiability_qualified": False,
        "formal_result": False,
    }
    write(root / "qualification_v2.json", result)
    return result


def invoke(
    root: Path, name: str, prompt: str, schema: dict, *, deadline: float, planned_calls: int = 20
) -> dict:
    folder = root / "model" / name
    if (folder / "result.json").exists():
        return read(folder / "result.json")
    if folder.exists():
        raise RuntimeError(f"incomplete attempted call {name}; no automatic replacement")
    folder.mkdir(parents=True)
    attempted = len(list((root / "model").glob("*/result.json")))
    result = {
        "name": name,
        "model": PROVIDER["model"],
        "reasoning_effort": "medium",
        "status": "failed",
        "failure": None,
        "payload": None,
    }
    write(folder / "attempt.json", {**result, "started": time.time()})
    if time.time() >= deadline:
        result.update(status="not_started", failure="block_deadline")
    else:
        try:
            with tempfile.TemporaryDirectory(prefix="chemworld-astra-trial-") as tmp:
                temporary = Path(tmp)
                workspace = temporary / "workspace"
                workspace.mkdir()
                environment = _prepare_codex_home(temporary, PROVIDER)
                schema_path = temporary / "schema.json"
                write(schema_path, schema)
                audit = folder.resolve() / "numerics.jsonl"
                command = build_command(
                    PROVIDER, schema_path, workspace, audit=audit, provider_retries=0
                )
                receipt = launch(
                    command,
                    prompt,
                    workspace,
                    environment,
                    folder / "turn",
                    min(600.0, deadline - time.time()),
                    True,
                    audit,
                    {"stage": name, "completed_calls": attempted, "planned_calls": planned_calls},
                )
                result["receipt"] = receipt
                result["payload"] = receipt.get("payload")
                if receipt.get("failure") or not isinstance(result["payload"], dict):
                    result["failure"] = receipt.get("failure") or "missing_json"
                else:
                    result["status"] = "completed"
        except Exception as exc:
            result["failure"] = {"type": type(exc).__name__, "message": str(exc)[:500]}
    write(folder / "result.json", result)
    print(
        json.dumps(
            {
                "stage": name,
                "status": result["status"],
                "completed_calls": attempted + 1,
                "planned_calls": planned_calls,
            }
        ),
        flush=True,
    )
    return result


def message(instruction: str, payload: dict) -> str:
    return (
        "You are an experimental scientist. Use only the supplied public contract and records. "
        "You may call public_numerics.calculate for arithmetic or least squares; no other "
        "tools or external context. Return the requested JSON. Give short scientific "
        "conclusions, not private chain-of-thought.\n"
        + instruction
        + "\nPUBLIC INPUT:\n"
        + json.dumps({"contract": public_contract(), **payload}, ensure_ascii=False)
    )


def source_data(root: Path, source: str, seed: int, deadline: float) -> list[dict]:
    destination = root / f"source_{source}.json"
    if destination.exists():
        return read(destination)
    data = []
    properties = {f"{w}_{i}": plan_schema() for w in TRAIN for i in range(3)}
    for round_index in range(2):
        instruction = "Choose three experiments in each learning pair. You have two rounds "
        instruction += "of six batches; only round two sees round-one results. Your goal is "
        instruction += "accurate intervention predictions and high score in unseen pairings. "
        if source == "diagnostic":
            instruction += (
                "Organize experiments around component hypotheses and uncertainties. "
                "Use controlled contrasts and informative measurement to distinguish "
                "upstream production from downstream recovery, then test the relations. "
            )
        else:
            instruction += "Choose your own experimental strategy, using any valid public method. "
        call = invoke(
            root,
            f"acquire_{source}_{round_index}",
            message(instruction, {"round": round_index + 1, "records": clean_data(data)}),
            object_schema(properties),
            deadline=deadline,
        )
        if call["status"] != "completed":
            break
        for key in properties:
            value = call["payload"].get(key, {})
            world = key.split("_")[0]
            row = execute_batch(root, f"source/{source}/{round_index}/{key}", world, value, seed)
            data.append(row)
    write(destination, data)
    return data


def clean_data(rows: list[dict]) -> list[dict]:
    output = []
    for row in rows:
        if row["status"] != "completed":
            output.append({k: row.get(k) for k in ("world", "plan", "status", "failure")})
            continue
        public = row["public"]
        item = {k: deepcopy(public[k]) for k in ("world", "plan", "upstream_hplc", "terminal")}
        item["measurements"] = [
            {k: deepcopy(v) for k, v in m.items() if k != "raw_signal"}
            for m in public.get("measurements", [])
        ]
        item["resources"] = deepcopy(public.get("physical_resources", {}))
        output.append(item)
    return output


def fit_ridge(x, y):
    a, b = np.asarray(x, dtype=float), np.asarray(y, dtype=float)
    penalty = np.eye(a.shape[1]) * 0.01
    penalty[0, 0] = 0
    return np.linalg.solve(a.T @ a + penalty, a.T @ b).tolist()


def upstream_features(p):
    return [
        1.0,
        (p["reaction_temperature_K"] - 377.5) / 27.5,
        math.log(p["reaction_duration_s"] / 1200),
    ]


def downstream_features(p, y):
    return [
        1.0,
        y,
        (p["cooling_temperature_K"] - 292.5) / 17.5,
        math.log(p["cooling_duration_s"] / 1200),
    ]


def whole_features(p, world):
    return [
        *upstream_features(p),
        *downstream_features(p, 0)[2:],
        float(world.startswith("R2")),
        float(world.endswith("C2")),
    ]


def fit_reference(data: list[dict]) -> dict:
    valid = [r["public"] for r in data if r["status"] == "completed"]
    models = {"upstream": {}, "downstream": {}, "whole": None}
    for label in ("R1", "R2"):
        rows = [r for r in valid if r["world"].startswith(label) and r["upstream_hplc"]]
        if len(rows) >= 3:
            models["upstream"][label] = fit_ridge(
                [upstream_features(r["plan"]) for r in rows],
                [r["upstream_hplc"]["yield"] for r in rows],
            )
    for label in ("C1", "C2"):
        rows = [r for r in valid if r["world"].endswith(label) and r["upstream_hplc"]]
        if len(rows) >= 4:
            models["downstream"][label] = fit_ridge(
                [downstream_features(r["plan"], r["upstream_hplc"]["yield"]) for r in rows],
                [
                    [r["terminal"][k] for k in ("crystal_yield", "crystal_purity", "score")]
                    for r in rows
                ],
            )
    full = [r for r in valid if r["upstream_hplc"]]
    if len(full) >= 7:
        models["whole"] = fit_ridge(
            [whole_features(r["plan"], r["world"]) for r in full],
            [
                [
                    r["upstream_hplc"]["yield"],
                    *[r["terminal"][k] for k in ("crystal_yield", "crystal_purity", "score")],
                ]
                for r in full
            ],
        )
    return models


def predict_reference(model: dict, world: str, p: dict, kind="component"):
    if kind == "whole":
        if model["whole"] is None:
            return None
        result = np.clip(np.asarray(whole_features(p, world)) @ model["whole"], 0, 1)
    else:
        if world[:2] not in model["upstream"] or world[2:] not in model["downstream"]:
            return None
        y = float(np.clip(np.asarray(upstream_features(p)) @ model["upstream"][world[:2]], 0, 1))
        d = np.clip(np.asarray(downstream_features(p, y)) @ model["downstream"][world[2:]], 0, 1)
        result = np.r_[y, d]
    return dict(zip((*METRICS, "score"), map(float, result), strict=True))


def encode(root: Path, source: str, representation: str, data: list[dict], deadline: float):
    props = (
        {"summary": {"type": "string", "maxLength": 3600}}
        if representation == "whole"
        else {
            k: {"type": "string", "maxLength": 720} for k in ("R1", "R2", "C1", "C2", "interface")
        }
    )
    instruction = (
        "Create a reusable knowledge package from these public experimental records only. "
        "The recipient will have the public contract but no records. Retain numerical relations, "
        "uncertainty, applicability and failures needed for intervention predictions and "
        "unseen-pair deployment. No target query coordinates or feedback are available. "
    )
    instruction += (
        "Use a whole-process predictive summary, maximum 3600 characters. "
        "You may express component relationships when useful."
        if representation == "whole"
        else "Use separate R1/R2/C1/C2 relationships and an interface section, each at most "
        "720 characters; 3600 total. Preserve how upstream state affects downstream."
    )
    result = invoke(
        root,
        f"encode_{source}_{representation}",
        message(instruction, {"records": clean_data(data)}),
        object_schema(props),
        deadline=deadline,
    )
    if result["status"] != "completed":
        return None
    payload = result["payload"]
    if set(payload) != set(props) or any(
        not isinstance(payload[k], str) or len(payload[k]) > props[k]["maxLength"] for k in props
    ):
        result.update(status="failed", failure="invalid_knowledge_package")
        write(root / "model" / f"encode_{source}_{representation}" / "result.json", result)
        return None
    return payload


def repaired_package(package: dict, model: dict, kind: str):
    fixed = deepcopy(package)
    mapping = model["upstream" if kind == "R" else "downstream"]
    if len(mapping) != 2:
        return None
    for label, coefficients in mapping.items():
        c = np.round(np.asarray(coefficients), 6).tolist()
        if kind == "R":
            text = (
                "Public-data ridge estimate (not a true law): reaction yield = clip(dot("
                f"[1,(T_R-377.5)/27.5,log(t_R/1200)],{c}),0,1). "
                "T in K, time in s; valid only in the observed operating domain. "
                "Fitted only to this source's measured upstream HPLC; no target feedback."
            )
        else:
            text = (
                "Public-data ridge estimate, not a true law: "
                "[crystal_yield,crystal_purity,score] = clip("
                f"[1,upstream_yield,(T_C-292.5)/17.5,log(t_C/1200)] @ {c},0,1). "
                "Measured source HPLC yields and terminal outcomes only; no target feedback. "
                "K, seconds; empirical local validity and uncertainty apply."
            )
        if len(text) > 720:
            raise ValueError("public-data repair exceeds predeclared slot budget")
        fixed[label] = text
    return fixed


def query_coordinates():
    controls = [plan((350, 5400, 310, 7200)), plan((405, 1200, 275, 1200))]
    return {f"{w}_q{i}": {"world": w, "plan": p} for w in WORLDS for i, p in enumerate(controls)}


def readout_schema(queries):
    return object_schema(
        {
            "predictions": object_schema(
                {
                    q: object_schema(
                        {k: {"type": "number", "minimum": 0, "maximum": 1} for k in METRICS}
                    )
                    for q in queries
                }
            ),
            "deployments": object_schema({w: plan_schema() for w in WORLDS}),
        }
    )


def run_readout(root, name, packet, queries, seed, deadline):
    if packet is None:
        return {"name": name, "status": "not_started", "failure": "missing_source_or_package"}
    result = invoke(
        root,
        f"read_{name}",
        message(
            "Predict each blind query: reaction_yield means HPLC target yield immediately after "
            "quench; crystal_yield and crystal_purity are terminal final-assay values. Then choose "
            "one complete deployment plan per world to maximize the public score. No experiment or "
            "feedback is available in this turn. Plans are sealed before any execution; you cannot "
            "adapt to target readings. All predictions must be in [0,1].",
            {"knowledge_delivery": packet, "blind_queries": queries},
        ),
        readout_schema(queries),
        deadline=deadline,
    )
    if result["status"] != "completed":
        return {"name": name, "status": result["status"], "failure": result["failure"]}
    payload = result["payload"]
    try:
        if set(payload["predictions"]) != set(queries):
            raise ValueError("prediction denominator mismatch")
        for prediction in payload["predictions"].values():
            if set(prediction) != set(METRICS) or not all(
                type(v) in (int, float) and 0 <= v <= 1 for v in prediction.values()
            ):
                raise ValueError("invalid prediction")
        if set(payload["deployments"]) != set(WORLDS):
            raise ValueError("deployment denominator mismatch")
        for p in payload["deployments"].values():
            validate_plan(p)
    except (KeyError, TypeError, ValueError) as exc:
        return {"name": name, "status": "failed", "failure": f"invalid_readout: {exc}"}
    deployed = [
        execute_batch(root, f"deploy/{name}/{w}", w, payload["deployments"][w], seed)
        for w in WORLDS
    ]
    return {
        "name": name,
        "status": "completed",
        "predictions": payload["predictions"],
        "deployments": deployed,
    }


def run(root: Path):
    if not qualification(root)["runtime_pass"]:
        print("Runtime qualification failed; dependent model experiments not started.", flush=True)
        summarize(root)
        return
    inputs = read(root / "private_inputs.json")
    seed, deadline = inputs["seed"], inputs["deadline"]
    sources, packages, references = {}, {}, {}
    for source in SOURCES:
        sources[source] = source_data(root, source, seed, deadline)
        complete = len(sources[source]) == 12 and all(
            r["status"] == "completed" for r in sources[source]
        )
        references[source] = fit_reference(sources[source])
        for representation in ("whole", "component"):
            packages[f"{source}_{representation}"] = (
                encode(root, source, representation, sources[source], deadline)
                if complete
                else None
            )
    # Fixed nonadaptive Latin-hypercube-like design, unrelated to any model outcomes.
    design = [(i, (5 * i + 1) % 6, (i + 3) % 6, (5 * i + 4) % 6) for i in range(6)]
    sources["space_filling"] = [
        execute_batch(
            root,
            f"source/space_filling/{w}/{i}",
            w,
            plan(
                [
                    lo + (hi - lo) * (j + 0.5) / 6
                    for j, (lo, hi) in zip(indices, BOUNDS.values(), strict=True)
                ]
            ),
            seed,
        )
        for w in TRAIN
        for i, indices in enumerate(design)
    ]
    references["space_filling"] = fit_reference(sources["space_filling"])
    write(root / "reference_models.json", references)
    write(root / "packages.json", packages)
    queries = query_coordinates()
    truth = {
        q: execute_batch(root, f"blind/{q}", v["world"], v["plan"], seed)
        for q, v in queries.items()
    }
    write(root / "blind_truth.json", truth)
    conditions = {}
    for source in SOURCES:
        complete = len(sources[source]) == 12 and all(
            r["status"] == "completed" for r in sources[source]
        )
        conditions[f"{source}_raw"] = {"records": clean_data(sources[source])} if complete else None
        for representation in ("whole", "component"):
            conditions[f"{source}_{representation}"] = packages[f"{source}_{representation}"]
    conditions["task_only"] = {}
    base = packages["standard_component"]
    for kind in ("R", "C"):
        swapped = deepcopy(base)
        if swapped is not None:
            swapped[kind + "1"], swapped[kind + "2"] = swapped[kind + "2"], swapped[kind + "1"]
        conditions[f"standard_swap_{kind}"] = swapped
    conditions["standard_sham"] = dict(reversed(list(base.items()))) if base is not None else None
    for kind in ("R", "C"):
        conditions[f"standard_repair_{kind}"] = (
            repaired_package(base, references["standard"], kind) if base is not None else None
        )
    rows = []
    for name, packet in conditions.items():
        rows.append(run_readout(root, name, packet, queries, seed, deadline))
        write(root / "readouts.json", rows)
    reference_rows = []
    grid = [
        plan(values)
        for values in itertools.product(*[(lo, (lo + hi) / 2, hi) for lo, hi in BOUNDS.values()])
    ]
    for source in SOURCES:
        for kind in ("component", "whole", "best_history"):
            for world in WORLDS:
                candidates = (
                    [(p, predict_reference(references[source], world, p, kind)) for p in grid]
                    if kind != "best_history"
                    else []
                )
                if kind == "best_history":
                    valid = [r for r in sources[source] if r["status"] == "completed"]
                    chosen = (
                        max(valid, key=lambda r: r["public"]["terminal"]["score"])["plan"]
                        if valid
                        else None
                    )
                else:
                    valid = [(p, pred) for p, pred in candidates if pred is not None]
                    chosen = max(valid, key=lambda row: row[1]["score"])[0] if valid else None
                name = f"reference/{source}/{kind}/{world}"
                reference_rows.append(
                    execute_batch(root, name, world, chosen, seed)
                    if chosen is not None
                    else {
                        "name": name,
                        "world": world,
                        "status": "not_started",
                        "failure": "public_reference_not_fittable",
                    }
                )
    write(root / "reference_deployments.json", reference_rows)
    summarize(root)


def summarize(root: Path):
    physical = [read(p) for p in sorted((root / "physical").rglob("result.json"))]
    calls = [read(p) for p in sorted((root / "model").glob("*/result.json"))]
    rows = read(root / "readouts.json") if (root / "readouts.json").exists() else []
    truth = read(root / "blind_truth.json") if (root / "blind_truth.json").exists() else {}
    conditions = []
    for row in rows:
        report = {"condition": row["name"], "status": row["status"], "failure": row.get("failure")}
        if row["status"] == "completed":
            report["mae"] = {}
            for split, worlds in (("learning", TRAIN), ("heldout", WORLDS[2:])):
                metric_errors = {k: [] for k in METRICS}
                for q, t in truth.items():
                    if t["world"] not in worlds or t["status"] != "completed":
                        continue
                    target = {
                        "reaction_yield": t["public"]["upstream_hplc"]["yield"],
                        **{k: t["public"]["terminal"][k] for k in METRICS[1:]},
                    }
                    for k in METRICS:
                        metric_errors[k].append(abs(row["predictions"][q][k] - target[k]))
                report["mae"][split] = {
                    k: float(np.mean(v)) if v else None for k, v in metric_errors.items()
                }
            report["deployment"] = {
                r["world"]: {
                    "status": r["status"],
                    "score": r["public"]["terminal"]["score"]
                    if r["status"] == "completed"
                    else 0.0,
                    "plan": r["plan"],
                    "failure": r.get("failure"),
                }
                for r in row["deployments"]
            }
        conditions.append(report)
    token_usage = {}
    for c in calls:
        for k, v in c.get("receipt", {}).get("usage", {}).items():
            if type(v) in (int, float):
                token_usage[k] = token_usage.get(k, 0) + v
    summary = {
        "schema_version": "work-ii-astra-single-trial-1",
        "formal_result": False,
        "model": PROVIDER["model"],
        "reasoning_effort": "medium",
        "independent_groups": 1,
        "planned_model_calls": 20,
        "attempted_model_calls": len(calls),
        "completed_model_calls": sum(c["status"] == "completed" for c in calls),
        "failed_model_calls": sum(c["status"] == "failed" for c in calls),
        "not_started_model_calls": 20 - sum(c["status"] != "not_started" for c in calls),
        "planned_original_physical_runs": 132,
        "attempted_original_physical_runs": len(physical),
        "completed_original_physical_runs": sum(r["status"] == "completed" for r in physical),
        "failed_original_physical_runs": sum(r["status"] == "failed" for r in physical),
        "not_started_original_physical_runs": 132 - len(physical),
        "exact_replay_verified": sum(r["exact_replay"] for r in physical),
        "reported_token_usage": token_usage,
        "provider_wall_seconds": sum(c.get("receipt", {}).get("elapsed_s", 0) for c in calls),
        "subscription_usd_cost": None,
        "qualification": read(root / "qualification_v2.json"),
        "initial_engineering_failures": 8,
        "initial_qualification": read(root / "qualification.json"),
        "conditions": conditions,
        "all_failures": [
            {"unit": r.get("name"), "failure": r.get("failure")}
            for r in [*calls, *physical]
            if r["status"] != "completed"
        ],
        "physical_rows": physical,
        "limits": [
            "one constructed group; no uncertainty intervals or generalization claims",
            "fixed workflow; sealed open-loop deployment; no within-batch adaptation",
            "public ridge references have not established mechanism identifiability",
            "Raw is a normalized public scientific record, not private state or reasoning",
            "shared fixed observation noise coordinate; no independent noise repeats",
            "no exact endpoint-matching or support-overlap qualification yet",
        ],
    }
    write(root / "summary.json", summary)
    report_dir = ROOT / "workstreams/flagship_tasks/reports"
    write(report_dir / "work-ii-astra-single-trial-20260914.json", summary)
    text = [
        "# Astra 单次开发试跑",
        "",
        "仅 GPT-6 Astra / medium；一组反应—结晶四格世界。",
        "此为开发试跑，不能据此推断系统性失效或总体效果。",
        "",
        f"模型完成 {summary['completed_model_calls']}/20；失败 {summary['failed_model_calls']}；"
        f"未启动 {summary['not_started_model_calls']}。",
        f"物理完成 {summary['completed_original_physical_runs']}/132（含原8次工程失败）；"
        f"失败 {summary['failed_original_physical_runs']}；"
        f"精确重放通过 {summary['exact_replay_verified']}。",
        "",
        "| 条件 | 状态 | 留出反应产率 MAE | 留出晶体产率 MAE | R1C2 score | R2C1 score |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for r in conditions:
        if r["status"] == "completed":
            e, d = r["mae"]["heldout"], r["deployment"]
            text.append(
                f"| {r['condition']} | {r['status']} | {e['reaction_yield']:.4f} | "
                f"{e['crystal_yield']:.4f} | {d['R1C2']['score']:.4f} | "
                f"{d['R2C1']['score']:.4f} |"
            )
        else:
            text.append(f"| {r['condition']} | {r['status']} | — | — | — | — |")
    text += [
        "",
        "## 失败与边界",
        "",
        *[f"- {f['unit']}: {f['failure']}" for f in summary["all_failures"]],
        "",
        *[f"- {s}" for s in summary["limits"]],
        "",
    ]
    (report_dir / "work-ii-astra-single-trial-20260914.md").write_text(
        "\n".join(text), encoding="utf-8"
    )
    print(
        json.dumps(
            {
                k: v
                for k, v in summary.items()
                if k
                not in ("physical_rows", "qualification", "initial_qualification", "conditions")
            },
            ensure_ascii=False,
        ),
        flush=True,
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("prepare", "qualify", "run", "summarize"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = args.output.resolve()
    if (root / "closed.json").exists():
        if args.mode == "summarize":
            from scripts.closeout_work_ii_astra_single_trial import build_report

            build_report(root)
            return
        raise SystemExit(
            "This trial is closed after public-contract defects. Its attempted conditions "
            "must not be resumed or replaced. See the retained closeout report."
        )
    stop = threading.Event()
    started = time.monotonic()

    def heartbeat():
        while not stop.wait(30):
            finished = len(list((root / "physical").rglob("result.json")))
            calls = len(list((root / "model").glob("*/result.json")))
            elapsed = time.monotonic() - started
            denominator = 16 if args.mode in ("prepare", "qualify") else 132
            rate = finished * 60 / elapsed
            print(
                json.dumps(
                    {
                        "stage": args.mode,
                        "completed_physical": finished,
                        "planned_physical": denominator,
                        "completed_calls": calls,
                        "planned_calls": 20,
                        "physical_per_minute": round(rate, 2),
                        "eta_minutes": round((denominator - finished) / rate, 1) if rate else None,
                        "elapsed_s": round(elapsed),
                    }
                ),
                flush=True,
            )

    worker = threading.Thread(target=heartbeat, daemon=True)
    worker.start()
    try:
        if args.mode == "prepare":
            root.mkdir(parents=True, exist_ok=False)
            write(
                root / "private_inputs.json",
                {"seed": secrets.randbelow(1_000_000) + 10_000, "deadline": time.time() + 14_400},
            )
            write(root / "public_contract.json", public_contract())
            qualification(root)
        elif args.mode == "run":
            run(root)
        elif args.mode == "qualify":
            qualification(root)
        else:
            summarize(root)
    finally:
        stop.set()
        worker.join(timeout=2)


if __name__ == "__main__":
    main()
