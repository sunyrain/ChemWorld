#!/usr/bin/env python3
"""Run the EQ-S five-world mechanism-structure block."""
# ruff: noqa: E402, E501

from __future__ import annotations

import argparse
import copy
import json
import math
import sys
import time
from collections.abc import Mapping, Sequence
from itertools import pairwise
from pathlib import Path
from statistics import fmean
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import scripts.run_work_ii_eq_bounded_equilibrium as eq_v1
import scripts.run_work_ii_eq_bounded_equilibrium_v2 as eq_v2
from scipy.optimize import differential_evolution

from chemworld.physchem.equilibrium_mechanism import (
    solve_coupled_weak_acid_precipitation,
)

CONFIG = ROOT / "configs/benchmark/work_ii_eq_structural_v0.2.repair.design.json"
FREEZE = ROOT / "configs/benchmark/work_ii_eq_structural_freeze_v0.2.1.json"
FAILED_FREEZE = ROOT / "configs/benchmark/work_ii_eq_structural_freeze_v0.2.json"
TASK = eq_v1.TASK
ARMS = eq_v1.ARMS
METRICS = eq_v1.METRICS
PROVIDER = eq_v1.PROVIDER
POSTTEST_STAGES = ("K1", "Q", "K2", "EQS")

GOALS = {
    "characterization": (
        "Characterize this bounded aqueous-equilibrium world and infer a defensible reaction "
        "network. Determine how loading and dilution jointly affect normalized pH, the free "
        "acid-dissociation fraction, and the public precipitation proxy. Test any supplied "
        "structural dossier against observations, distinguish equation topology from parameter "
        "refitting, state competing explanations and scope, and do not optimize a process score."
    )
}

SYSTEM = """You are an autonomous scientist in a simulated bounded aqueous-equilibrium laboratory.
Use only the supplied chemworld_lab tools and public_numerics calculator. No filesystem, network,
repository inspection, external retrieval, or hidden-simulator access is allowed. Complete exactly
12 independent experimental batches; repetition is allowed. You have at most 12 non-final instrument
uses plus 12 final assays. Choose legal solvent volumes, reagent amounts, and measurements
autonomously. This is a bounded weak-acid/precipitation characterization task, not general aqueous
chemistry and not optimization. pH_normalized is pH/14; acid_dissociation_fraction is the bounded
free-conjugate-base fraction; precipitation_signal is a bounded solid proxy. Numerical residual and
equilibrium_confidence are environment diagnostics, not your uncertainty or a task score. Do not
optimize them. No particular model form or conclusion is required. For every batch explicitly
terminate and then measure final_assay. Continue with next_state until campaign_ended is true. After
the twelfth batch, commit the completed batch that is the most useful evidentiary anchor, with a short
English rationale; this is not an optimum claim. Then return the required concise English status JSON.
A separate same-thread sequence will request K1, twelve blind quantitative predictions, K2, and a
structured mechanism supplement. Do not answer those early. Supplied prior information may be
incomplete or inaccurate; public observations are authoritative.
"""

K1 = """The experimental phase has ended and the evidentiary anchor is sealed. Submit a complete,
self-contained mechanistic report in English. Explain how this world operates: key variables,
relationships, couplings, a plausible reaction network, mass balances, and equations or processes;
which actual experiments caused you to form or revise the account; its supported range; unidentifiable
factors; and reasonable competing explanations. Address whether the three public response channels
can be explained by one equilibrium network and distinguish a topology claim from refitting constants
inside one topology. State how any supplied dossier was supported, contradicted, revised, or left
untested, and explicitly state if no instance prior was supplied. Cite real batch numbers and values.
Separate observation, interpolation, extrapolation, and conjecture. Do not run experiments or invent
unmeasured information. Develop the report fully rather than compressing it. Return the JSON report
field in English. The fixed prediction questions are revealed only after this report is sealed.
"""

Q_PROMPT = """Using only your completed research and sealed K1 account, predict the final outcomes of
the following 12 independent new batches. Each starts independently from the same frozen world. For
every query and requested metric, return a point estimate and an 80% prediction interval, a substantive
English per-query rationale, and an English shared rationale. Account for model and observation
uncertainty. Do not run experiments or modify K1. The questions test quantitative mechanism
generalization, not optimization; predict every query and do not select a preferred condition.
equilibrium_confidence is not requested and is not your uncertainty. Return complete predictions JSON.
"""

K2 = """K1 and Q are sealed, and no prediction truth or score has been shown. Answer all seven items
in English, citing real batches and specific K1 judgments. Do not run an experiment, revise sealed
outputs, repeat the full experiment table, or present hindsight as a contemporaneous belief.

1. Which supplied structural claims were supported, contradicted, or untested? If no instance dossier
was supplied, say so. Distinguish no observed contradiction from contradiction that was not acted on.
2. Which experiments formed or changed the mechanism account? Which choices relied on the dossier,
accumulated observations, or an untested assumption?
3. What is the strongest competing reaction network or parameter-only explanation? What can and cannot
be distinguished by the evidence?
4. If exactly one additional legal complete experiment were allowed, what would you run and measure,
and how would alternative outcomes change the mechanism account? Do not execute it.
5. How did the characterization objective shape trade-offs among coverage, replication, local
identification, and any temptation to improve an operational score?
6. What acquired evidence was underused? Which blind predictions and 80% intervals are least reliable
or inconsistent with K1 scope?
7. What are the limits of the sealed evidentiary anchor, repeatability, local robustness, and
generalization across concentration, volume, materials, or worlds? Do not call it proven optimal.

Return the JSON report field in English.
"""

EQS = """K1, Q, and K2 are sealed, and no prediction truth, hidden parameter, arm label, or score has
been shown. Using only source-campaign evidence, return the structured mechanism supplement in English.
Choose network_family from direct_free_ion_precipitation, aqueous_ion_pair_intermediate, or
indeterminate. Choose aqueous_intermediate from absent, present, or indeterminate. Select the equation
IDs supported by your final account from acid_dissociation, free_ion_solid_equilibrium, and
aqueous_ion_pair_association. A direct classification must select the first two IDs and mark the
intermediate absent; an ion-pair classification must select all three and mark it present; an
indeterminate classification must mark the intermediate indeterminate and select only the two common
equations. Give an English rationale and cite one or more real source batch numbers. Do not estimate
pKa, Ksp, or an association constant, run an experiment, or revise earlier outputs.
"""


def read(path: Path) -> Any:
    return eq_v1.read(path)


def write(path: Path, payload: Any) -> None:
    eq_v1.write(path, payload)


def digest(payload: Any) -> str:
    return eq_v1.digest(payload)


def file_sha256(path: Path) -> str:
    return eq_v1.file_sha256(path)


def deterministic_seed(*parts: object) -> int:
    return eq_v1.deterministic_seed(*parts)


def load_config() -> dict[str, Any]:
    repair = read(CONFIG)
    binding = repair["base_config"]
    base_path = ROOT / binding["path"]
    if file_sha256(base_path) != binding["sha256"]:
        raise RuntimeError("EQ-S v0.2 repair does not bind the approved v0.1 design")
    base = read(base_path)
    runtime = repair["runtime_contract"]
    replacement = {row["world_id"]: row for row in repair["private_world_replacement"]}
    worlds = []
    for original in base["worlds"]:
        world_id = original["world_id"]
        private = copy.deepcopy(replacement[world_id])
        private.pop("world_id")
        worlds.append(
            {
                "world_id": world_id,
                "world_seed": int(original["world_seed"]),
                "world_interventions": copy.deepcopy(
                    runtime["world_interventions"][world_id]
                ),
                "private_authoring": private,
            }
        )
    return {
        **copy.deepcopy(base),
        "schema_version": repair["schema_version"],
        "status": repair["status"],
        "execution_authorized": repair["execution_authorized"],
        "provider_execution_authorized": repair["provider_execution_authorized"],
        "protocol": runtime["protocol"],
        "task_id": runtime["task_id"],
        "task": runtime["task"],
        "world_split": runtime["world_split"],
        "objective": runtime["objective"],
        "prior_locus": runtime["prior_locus"],
        "posttest_stages": copy.deepcopy(runtime["posttest_stages"]),
        "counts": copy.deepcopy(base["counts_after_approval"]),
        "source_resource_card": copy.deepcopy(runtime["source_resource_card"]),
        "worlds": worlds,
        "provider_free_gate": copy.deepcopy(runtime["provider_free_gate"]),
        "truth_embargo": runtime["truth_embargo"],
        "execution_order": copy.deepcopy(runtime["execution_order"]),
        "canary": copy.deepcopy(runtime["canary"]),
        "full_matrix": copy.deepcopy(runtime["full_matrix"]),
        "repair": copy.deepcopy(repair),
    }


def queries(config: Mapping[str, Any]) -> list[dict[str, Any]]:
    return eq_v1.queries(config)


def world_by_id(config: Mapping[str, Any], world_id: str) -> Mapping[str, Any]:
    return eq_v1.world_by_id(config, world_id)


def public_prior(
    config: Mapping[str, Any], world_id: str, arm: str
) -> dict[str, Any] | None:
    if arm == "Opaque":
        return None
    if arm not in {"Aligned", "MisIndexed"}:
        raise ValueError(f"unknown EQ-S arm: {arm}")
    target = world_by_id(config, world_id)
    source = target
    if arm == "MisIndexed":
        source = world_by_id(
            config,
            str(target["private_authoring"]["misindexed_world_id"]),
        )
    family = str(source["private_authoring"]["mechanism_family"])
    contract = config["prior_contract"]
    return {
        "schema_version": contract["schema_version"],
        **copy.deepcopy(contract["common_fields"]),
        **copy.deepcopy(contract["family_claims"][family]),
    }


def validate_design(config: Mapping[str, Any]) -> dict[str, Any]:
    expected_counts = {
        "worlds": 5,
        "independent_source_sessions": 15,
        "source_batches_per_session": 12,
        "source_batches": 180,
        "posttest_stages": ["K1", "Q", "K2", "EQS"],
        "posttests": 60,
        "reference_repeats_per_query": 5,
        "reference_executions": 300,
    }
    if config.get("counts") != expected_counts:
        raise ValueError("EQ-S denominators changed")
    if tuple(config.get("arms", ())) != ARMS:
        raise ValueError("EQ-S arms changed")
    if tuple(config.get("prediction_metrics", ())) != METRICS:
        raise ValueError("EQ-S metrics changed")
    if tuple(config.get("posttest_stages", ())) != POSTTEST_STAGES:
        raise ValueError("EQ-S posttest order changed")
    query_rows = queries(config)
    if len(config["worlds"]) != 5:
        raise ValueError("EQ-S requires five worlds")
    families = {
        world["world_id"]: world["private_authoring"]["mechanism_family"]
        for world in config["worlds"]
    }
    schedule = []
    for world in config["worlds"]:
        world_id = world["world_id"]
        donor = str(world["private_authoring"]["misindexed_world_id"])
        if families[donor] == families[world_id]:
            raise ValueError(f"EQ-S MisIndexed donor is not opposite-family: {world_id}")
        if public_prior(config, world_id, "Opaque") is not None:
            raise ValueError("EQ-S Opaque must be null")
        aligned = public_prior(config, world_id, "Aligned")
        wrong = public_prior(config, world_id, "MisIndexed")
        assert aligned is not None and wrong is not None
        if aligned.keys() != wrong.keys() or aligned == wrong:
            raise ValueError(f"EQ-S A/M matching failed: {world_id}")
        for forbidden in config["prior_contract"]["forbidden_public_fields"]:
            if forbidden.lower() in json.dumps(aligned, sort_keys=True).lower():
                raise ValueError(f"EQ-S public prior leaked forbidden field: {forbidden}")
        for arm in ARMS:
            schedule.append(
                {
                    "cell_id": f"{world_id}--{arm}",
                    "world_id": world_id,
                    "world_seed": int(world["world_seed"]),
                    "world_interventions": copy.deepcopy(world["world_interventions"]),
                    "arm": arm,
                    "goal": "characterization",
                }
            )
    if "Q01" in SYSTEM or json.dumps(query_rows, sort_keys=True) in SYSTEM:
        raise ValueError("EQ-S source prompt leaks Q")
    return {
        "schedule": schedule,
        "query_sha256": digest(query_rows),
        "prior_sha256": {
            row["cell_id"]: digest(public_prior(config, row["world_id"], row["arm"]))
            for row in schedule
        },
    }


def configure_provider_helpers(config: Mapping[str, Any]) -> None:
    eq_v1.CONFIG = CONFIG
    eq_v1.SYSTEM = SYSTEM
    eq_v1.K1 = K1
    eq_v1.Q_PROMPT = Q_PROMPT
    eq_v1.K2 = K2
    eq_v1.GOALS = GOALS
    eq_v1.configure_provider_helpers(config)
    eq_v2.CONFIG = CONFIG
    eq_v2.FREEZE = FREEZE
    eq_v2.SYSTEM = SYSTEM
    eq_v2.K1 = K1
    eq_v2.Q_PROMPT = Q_PROMPT
    eq_v2.K2 = K2
    eq_v2.EQS = EQS
    eq_v2.GOALS = GOALS
    eq_v2.load_config = load_config
    eq_v2.validate_design = validate_design
    eq_v2.public_prior = public_prior
    eq_v2.queries = queries
    eq_v2.world_by_id = world_by_id
    eq_v2.posttest_schema = posttest_schema
    eq_v2.validate_posttest = validate_posttest


def _mean_grid(
    results: Mapping[str, Mapping[str, Sequence[Mapping[str, float]]]],
) -> dict[str, dict[str, dict[str, float]]]:
    return {
        world_id: {
            query_id: {
                metric: fmean(float(row[metric]) for row in repeats)
                for metric in METRICS
            }
            for query_id, repeats in rows.items()
        }
        for world_id, rows in results.items()
    }


def _direct_null_fit(
    config: Mapping[str, Any],
    world_id: str,
    grid: Mapping[str, Mapping[str, float]],
) -> dict[str, Any]:
    gate = config["provider_free_gate"]
    query_rows = {row["query_id"]: row for row in queries(config)}
    fit_ids = list(gate["direct_null_fit_query_ids"])
    holdout_ids = list(gate["direct_null_holdout_query_ids"])
    bounds = gate["direct_null_bounds"]

    def prediction(query_id: str, values: Sequence[float]) -> dict[str, float]:
        row = query_rows[query_id]
        final = row["final_state"]
        result = solve_coupled_weak_acid_precipitation(
            acid_total_mol=float(final["reagent_mol"]),
            volume_L=float(final["solvent_L"]),
            pka=float(values[0]),
            log10_ksp=float(values[1]),
            mechanism_family="direct_free_ion_precipitation",
            cation_fraction=float(values[2]),
            activity_coefficient_ratio=float(values[3]),
        )
        return {
            "pH_normalized": result.pH / 14.0,
            "acid_dissociation_fraction": result.acid_dissociation_fraction,
            "precipitation_signal": result.precipitation_signal,
        }

    def objective(values: Sequence[float]) -> float:
        errors = []
        for query_id in fit_ids:
            predicted = prediction(query_id, values)
            for metric in METRICS:
                errors.append((predicted[metric] - grid[query_id][metric]) / 0.006)
        return fmean(error * error for error in errors)

    result = differential_evolution(
        objective,
        [
            tuple(bounds["effective_pka"]),
            tuple(bounds["log10_ksp"]),
            tuple(bounds["precipitating_cation_fraction"]),
            tuple(bounds["activity_coefficient_ratio"]),
        ],
        seed=int(gate["direct_null_optimizer_seed"]),
        popsize=10,
        maxiter=60,
        polish=True,
        workers=1,
    )
    threshold = float(gate["noncollapse_absolute_error_threshold"])
    rows = []
    for query_id in holdout_ids:
        predicted = prediction(query_id, result.x)
        errors = {
            metric: abs(predicted[metric] - grid[query_id][metric])
            for metric in METRICS
        }
        rows.append(
            {
                "query_id": query_id,
                "absolute_errors": errors,
                "metrics_above_threshold": sum(value > threshold for value in errors.values()),
            }
        )
    passing = sum(
        row["metrics_above_threshold"] >= int(gate["noncollapse_minimum_metrics"])
        for row in rows
    )
    return {
        "world_id": world_id,
        "fitted_parameters": {
            "effective_pka": float(result.x[0]),
            "log10_ksp": float(result.x[1]),
            "precipitating_cation_fraction": float(result.x[2]),
            "activity_coefficient_ratio": float(result.x[3]),
        },
        "fit_objective_noise_scaled_mse": float(result.fun),
        "holdouts": rows,
        "passing_holdout_conditions": passing,
    }


def run_provider_free_gate(root: Path, config: Mapping[str, Any]) -> dict[str, Any]:
    gate_root = root / "provider-free-gate"
    report_path = gate_root / "gate.json"
    if report_path.exists():
        return read(report_path)
    gate = config["provider_free_gate"]
    query_rows = queries(config)
    actions = [action for query in query_rows for action in query["actions"]]
    repeats = int(gate["noise_repeats"])
    planned = len(config["worlds"]) * repeats
    all_results: dict[str, dict[str, list[dict[str, float]]]] = {}
    replay_passes = 0
    completed = 0
    started = time.monotonic()
    for world in config["worlds"]:
        world_rows = {query["query_id"]: [] for query in query_rows}
        for repeat in range(1, repeats + 1):
            result = eq_v1.reference_run(
                gate_root / "runs" / world["world_id"] / f"repeat-{repeat:02d}",
                actions,
                config=config,
                world=world,
                batches=12,
                observation_seed=deterministic_seed(
                    "eq-s-provider-free-gate-v0.2", world["world_id"], repeat
                ),
                observation_namespace=(
                    f"work-ii-eq-s-gate-{world['world_id'].lower()}-r{repeat:02d}"
                ),
            )
            if result["failure"] or result["rollbacks"] or len(result["batches"]) != 12:
                raise RuntimeError(
                    f"EQ-S gate execution failed: {world['world_id']}/r{repeat:02d}"
                )
            replay_passes += result["exact_replay"].get("verified") is True
            for query, batch in zip(query_rows, result["batches"], strict=True):
                world_rows[query["query_id"]].append(
                    {metric: float(batch["metrics"][metric]) for metric in METRICS}
                )
            completed += 1
            elapsed = time.monotonic() - started
            print(
                json.dumps(
                    {
                        "stage": "eq_s_provider_free_gate",
                        "completed_campaigns": completed,
                        "total_campaigns": planned,
                        "completed_batches": completed * 12,
                        "total_batches": planned * 12,
                        "eta_s": round(elapsed / completed * (planned - completed)),
                    }
                ),
                flush=True,
            )
        all_results[world["world_id"]] = world_rows
    means = _mean_grid(all_results)
    response_spans = {
        world_id: {
            metric: max(row[metric] for row in grid.values())
            - min(row[metric] for row in grid.values())
            for metric in METRICS
        }
        for world_id, grid in means.items()
    }
    scale_groups = config["structural_scorer"]["scale_controls"]
    scale_gaps = {}
    for world_id, grid in means.items():
        scale_gaps[world_id] = []
        for group in scale_groups:
            rows = [grid[query_id] for query_id in group["query_ids"]]
            scale_gaps[world_id].append(
                max(
                    max(row[metric] for row in rows) - min(row[metric] for row in rows)
                    for metric in METRICS
                )
            )
    null_fits = {
        world["world_id"]: _direct_null_fit(config, world["world_id"], means[world["world_id"]])
        for world in config["worlds"]
    }
    minimum_holdouts = int(gate["noncollapse_minimum_holdout_conditions"])
    family_checks = {}
    for world in config["worlds"]:
        world_id = world["world_id"]
        family = world["private_authoring"]["mechanism_family"]
        passing = null_fits[world_id]["passing_holdout_conditions"]
        family_checks[world_id] = (
            passing < minimum_holdouts
            if family == "direct_free_ion_precipitation"
            else passing >= minimum_holdouts
        )
    forbidden = tuple(
        str(item).lower() for item in config["prior_contract"]["forbidden_public_fields"]
    )
    priors = [
        public_prior(config, world["world_id"], arm)
        for world in config["worlds"]
        for arm in ARMS
        if arm != "Opaque"
    ]
    prior_text = json.dumps(priors, sort_keys=True).lower()
    checks = {
        "provider_calls_zero": True,
        "fifteen_campaigns_180_batches": completed == 15,
        "exact_replay": replay_passes == planned,
        "strict_opaque": all(
            public_prior(config, world["world_id"], "Opaque") is None
            for world in config["worlds"]
        ),
        "matched_opposite_A_M": all(
            public_prior(config, world["world_id"], "Aligned")
            != public_prior(config, world["world_id"], "MisIndexed")
            for world in config["worlds"]
        ),
        "no_numeric_or_query_prior_leakage": not any(item in prior_text for item in forbidden),
        "source_prompt_hides_Q": "Q01" not in SYSTEM,
        "response_signal": all(
            spans["pH_normalized"] >= float(gate["minimum_pH_normalized_span"])
            and spans["acid_dissociation_fraction"] >= float(gate["minimum_dissociation_span"])
            and spans["precipitation_signal"] >= float(gate["minimum_precipitation_span"])
            for spans in response_spans.values()
        ),
        "scale_controls": max(max(values) for values in scale_gaps.values())
        <= float(gate["maximum_scale_control_mean_gap"]),
        "parameter_only_noncollapse": all(family_checks.values()),
        "q_numeric_stability": all(
            math.isfinite(value) and 0.0 <= value <= 1.0
            for grid in means.values()
            for row in grid.values()
            for value in row.values()
        ),
        "fixed_query_and_score_contract": digest(query_rows)
        == validate_design(config)["query_sha256"],
    }
    report = {
        "schema_version": "work-ii-eq-s-provider-free-gate-0.2",
        "config_sha256": file_sha256(CONFIG),
        "resolved_config_sha256": digest(config),
        "provider_calls": 0,
        "planned_campaigns": planned,
        "completed_campaigns": completed,
        "planned_batches": planned * 12,
        "completed_batches": completed * 12,
        "replay_passes": replay_passes,
        "checks": checks,
        "passed": all(checks.values()),
        "response_spans": response_spans,
        "scale_control_max_mean_gaps": scale_gaps,
        "direct_null_fits": null_fits,
        "family_noncollapse_checks": family_checks,
        "mean_grid": means,
        "thresholds": copy.deepcopy(gate),
        "elapsed_s": time.monotonic() - started,
    }
    write(report_path, report)
    lines = [
        "# EQ-S provider-free gate v0.2",
        "",
        f"Status: **{'PASS' if report['passed'] else 'FAIL'}**. Provider calls: 0.",
        "",
        f"Completed {completed}/{planned} campaigns and {completed * 12}/{planned * 12} batches; exact replay {replay_passes}/{planned}.",
        "",
        "| Check | Pass |",
        "|---|---|",
        *[f"| {name} | {'yes' if passed else 'no'} |" for name, passed in checks.items()],
        "",
        "A failure is retained and repaired by version; no threshold is relaxed in place.",
        "",
    ]
    (gate_root / "GATE_REPORT.md").write_text("\n".join(lines), encoding="utf-8")
    return report


def posttest_schema(stage: str) -> dict[str, Any]:
    if stage != "EQS":
        return eq_v1.posttest_schema(stage)
    return {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "network_family": {
                "enum": [
                    "direct_free_ion_precipitation",
                    "aqueous_ion_pair_intermediate",
                    "indeterminate",
                ]
            },
            "aqueous_intermediate": {"enum": ["absent", "present", "indeterminate"]},
            "selected_equation_ids": {
                "type": "array",
                "minItems": 2,
                "maxItems": 3,
                "items": {
                    "enum": [
                        "acid_dissociation",
                        "free_ion_solid_equilibrium",
                        "aqueous_ion_pair_association",
                    ]
                },
            },
            "rationale": {"type": "string"},
            "cited_source_batches": {
                "type": "array",
                "minItems": 1,
                "items": {"type": "integer", "minimum": 1, "maximum": 12},
            },
        },
        "required": [
            "network_family",
            "aqueous_intermediate",
            "selected_equation_ids",
            "rationale",
            "cited_source_batches",
        ],
    }


def validate_posttest(
    stage: str,
    payload: Any,
    query_rows: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    if stage != "EQS":
        return eq_v1.validate_posttest(stage, payload, query_rows)
    if not isinstance(payload, Mapping):
        return {"valid": False, "failure": "missing_payload"}
    common = {"acid_dissociation", "free_ion_solid_equilibrium"}
    try:
        family = payload["network_family"]
        intermediate = payload["aqueous_intermediate"]
        equation_rows = payload["selected_equation_ids"]
        if (
            not isinstance(equation_rows, list)
            or len(equation_rows) != len(set(equation_rows))
        ):
            raise ValueError("duplicate_or_invalid_equation_ids")
        equations = set(equation_rows)
        rationale = payload["rationale"]
        cited = payload["cited_source_batches"]
        if not isinstance(rationale, str) or not rationale.strip() or eq_v1._contains_cjk(rationale):
            raise ValueError("rationale_missing_or_not_English")
        if not isinstance(cited, list) or not cited or len(set(cited)) != len(cited):
            raise ValueError("invalid_cited_source_batches")
        if any(not isinstance(item, int) or not 1 <= item <= 12 for item in cited):
            raise ValueError("invalid_cited_source_batch")
        if family == "direct_free_ion_precipitation":
            valid = intermediate == "absent" and equations == common
        elif family == "aqueous_ion_pair_intermediate":
            valid = intermediate == "present" and equations == {
                *common,
                "aqueous_ion_pair_association",
            }
        elif family == "indeterminate":
            valid = intermediate == "indeterminate" and equations == common
        else:
            valid = False
        if not valid:
            raise ValueError("contradictory_mechanism_topology")
    except (KeyError, TypeError, ValueError) as exc:
        return {"valid": False, "failure": str(exc)}
    return {"valid": True, "failure": None}


def evaluate_eqs(payload: Any, truth_family: str) -> dict[str, Any]:
    validation = validate_posttest("EQS", payload, ())
    if not validation["valid"]:
        return validation
    predicted = str(payload["network_family"])
    truth_set = set(
        {
            "direct_free_ion_precipitation": [
                "acid_dissociation",
                "free_ion_solid_equilibrium",
            ],
            "aqueous_ion_pair_intermediate": [
                "acid_dissociation",
                "free_ion_solid_equilibrium",
                "aqueous_ion_pair_association",
            ],
        }[truth_family]
    )
    predicted_set = set(payload["selected_equation_ids"])
    return {
        "valid": True,
        "truth_family": truth_family,
        "predicted_family": predicted,
        "abstained": predicted == "indeterminate",
        "network_family_correct": predicted == truth_family,
        "aqueous_intermediate_correct": payload["aqueous_intermediate"]
        == ("present" if truth_family == "aqueous_ion_pair_intermediate" else "absent"),
        "exact_equation_set_correct": predicted_set == truth_set,
        "equation_set_jaccard": len(predicted_set & truth_set) / len(predicted_set | truth_set),
    }


def _shape_vector(values: Sequence[float], x: Sequence[float]) -> tuple[list[float], list[float]]:
    slopes = [
        (float(right_y) - float(left_y)) / (float(right_x) - float(left_x))
        for left_y, right_y, left_x, right_x in zip(
            values[:-1],
            values[1:],
            x[:-1],
            x[1:],
            strict=True,
        )
    ]
    curvature = [right - left for left, right in pairwise(slopes)]
    return slopes, curvature


def evaluate_structure_predictions(
    payload: Any,
    config: Mapping[str, Any],
    truth: Mapping[str, Sequence[Mapping[str, float]]],
) -> dict[str, Any]:
    validation = validate_posttest("Q", payload, queries(config))
    if not validation["valid"]:
        return validation
    prediction = {row["query_id"]: row["metrics"] for row in payload["predictions"]}
    truth_mean = {
        query_id: {
            metric: fmean(float(row[metric]) for row in repeats)
            for metric in METRICS
        }
        for query_id, repeats in truth.items()
    }
    fixed_volume = config["structural_scorer"]["response_shape"]["fixed_volume_query_ids"]
    dilution = config["structural_scorer"]["response_shape"][
        "fixed_amount_dilution_query_ids_in_increasing_inverse_volume"
    ]
    by_id = {row["query_id"]: row for row in queries(config)}

    def block_error(ids: Sequence[str]) -> dict[str, float]:
        x = [math.log10(float(by_id[item]["final_state"]["analytical_concentration_M"])) for item in ids]
        slope_errors = []
        curvature_errors = []
        for metric in METRICS:
            predicted_values = [float(prediction[item][metric]["estimate"]) for item in ids]
            truth_values = [float(truth_mean[item][metric]) for item in ids]
            predicted_slopes, predicted_curvature = _shape_vector(predicted_values, x)
            truth_slopes, truth_curvature = _shape_vector(truth_values, x)
            slope_errors.extend(abs(a - b) for a, b in zip(predicted_slopes, truth_slopes, strict=True))
            curvature_errors.extend(
                abs(a - b)
                for a, b in zip(predicted_curvature, truth_curvature, strict=True)
            )
        return {
            "slope_mae": fmean(slope_errors),
            "curvature_mae": fmean(curvature_errors),
        }

    scale = []
    for group in config["structural_scorer"]["scale_controls"]:
        ids = group["query_ids"]
        predicted_gap = max(
            max(float(prediction[item][metric]["estimate"]) for item in ids)
            - min(float(prediction[item][metric]["estimate"]) for item in ids)
            for metric in METRICS
        )
        truth_gap = max(
            max(float(truth_mean[item][metric]) for item in ids)
            - min(float(truth_mean[item][metric]) for item in ids)
            for metric in METRICS
        )
        scale.append(
            {
                "query_ids": list(ids),
                "predicted_max_gap": predicted_gap,
                "truth_max_gap": truth_gap,
                "absolute_gap_error": abs(predicted_gap - truth_gap),
            }
        )
    return {
        "valid": True,
        "concentration_response": block_error(fixed_volume),
        "dilution_response": block_error(dilution),
        "scale_controls": scale,
    }


def create_freeze(root: Path, config: Mapping[str, Any]) -> dict[str, Any]:
    gate_path = root / "provider-free-gate" / "gate.json"
    if not gate_path.is_file() or read(gate_path).get("passed") is not True:
        raise RuntimeError("cannot freeze EQ-S before a passing provider-free gate")
    bindings = [
        "configs/benchmark/work_ii_eq_structural_v0.1.design.json",
        "configs/benchmark/work_ii_eq_structural_v0.2.repair.design.json",
        "workstreams/flagship_tasks/WORK_II_EQ_S_STRUCTURAL_DESIGN_V0_1.md",
        "workstreams/flagship_tasks/WORK_II_EQ_S_V0_1_NONCOLLAPSE_PREFLIGHT.md",
        "src/chemworld/physchem/equilibrium_mechanism.py",
        "src/chemworld/runtime/observation_services.py",
        "src/chemworld/world/world_family.py",
        "scripts/run_work_ii_eq_structural_v0_2.py",
        "scripts/recover_work_ii_eq_structural_v0_2.py",
        "tests/test_work_ii_eq_structural_v0_2.py",
        "configs/benchmark/work_ii_eq_structural_freeze_v0.2.json",
        "workstreams/flagship_tasks/WORK_II_EQ_S_V0_2_1_SCHEMA_RECOVERY.md",
    ]
    freeze = {
        "schema_version": "work-ii-eq-s-freeze-0.2.1",
        "status": "frozen_for_formal_development_execution",
        "config_path": str(CONFIG.relative_to(ROOT)),
        "config_sha256": file_sha256(CONFIG),
        "resolved_config_sha256": digest(config),
        "gate_path": str(gate_path.relative_to(ROOT)),
        "gate_sha256": file_sha256(gate_path),
        "provider_calls_before_freeze": 0,
        "supersedes_freeze": str(FAILED_FREEZE.relative_to(ROOT)),
        "repair_scope": "provider JSON-schema compatibility only; scientific contract unchanged",
        "bindings": {relative: file_sha256(ROOT / relative) for relative in bindings},
    }
    write(FREEZE, freeze)
    return freeze


def bind_v2_runtime(config: Mapping[str, Any]) -> None:
    configure_provider_helpers(config)


def effective_result(root: Path, cell: Mapping[str, Any]) -> tuple[dict[str, Any] | None, Path]:
    original = root / "sources" / cell["cell_id"] / "RESULT.json"
    if original.is_file():
        payload = read(original)
        if payload.get("status") == "completed" and payload.get("posttest_chain_sealed") is True:
            return payload, original
    recovery_root = root / "recoveries" / cell["cell_id"]
    if recovery_root.is_dir():
        for candidate in sorted(recovery_root.glob("attempt-*/RESULT.json"), reverse=True):
            payload = read(candidate)
            if payload.get("status") == "completed" and payload.get("posttest_chain_sealed") is True:
                return payload, candidate
    return (read(original), original) if original.is_file() else (None, original)


def write_effective_summary(
    root: Path,
    schedule: Sequence[Mapping[str, Any]],
    phase: str,
) -> dict[str, Any]:
    resolved = [effective_result(root, cell) for cell in schedule]
    rows = [(result, path) for result, path in resolved if result is not None]
    payload = {
        "schema_version": "work-ii-eq-s-effective-summary-0.2.1",
        "phase": phase,
        "planned_sources": 15,
        "planned_source_batches": 180,
        "planned_posttests": 60,
        "attempted_sources": len(rows),
        "completed_sources": sum(result.get("status") == "completed" for result, _ in rows),
        "completed_source_batches": sum(len(result.get("batches", [])) for result, _ in rows),
        "sealed_posttests": sum(len(result.get("posttests", {})) for result, _ in rows),
        "sealed_posttest_chains": sum(
            result.get("posttest_chain_sealed") is True for result, _ in rows
        ),
        "cells": [
            {
                "cell_id": result["cell_id"],
                "world_id": result["world_id"],
                "arm": result["arm"],
                "status": result.get("status"),
                "source_batches": len(result.get("batches", [])),
                "posttests": {
                    stage: result.get("posttest_validation", {}).get(stage, {}).get("valid")
                    for stage in POSTTEST_STAGES
                },
                "effective_result": str(path.relative_to(root)),
            }
            for result, path in rows
        ],
    }
    write(root / "effective-summary.json", payload)
    return payload


def write_design_revision(
    root: Path,
    config: Mapping[str, Any],
    validated: Mapping[str, Any],
    freeze: Mapping[str, Any],
) -> None:
    design = {
        "schema_version": "work-ii-eq-s-run-design-0.2.1",
        "config_sha256": file_sha256(CONFIG),
        "resolved_config_sha256": digest(config),
        "freeze": copy.deepcopy(freeze),
        "schedule": copy.deepcopy(validated["schedule"]),
        "query_sha256": validated["query_sha256"],
        "prior_sha256": copy.deepcopy(validated["prior_sha256"]),
        "provider": copy.deepcopy(PROVIDER),
        "system_prompt": SYSTEM,
        "K1": K1,
        "Q": Q_PROMPT,
        "K2": K2,
        "EQS": EQS,
        "truth_embargo": config["truth_embargo"],
        "scientific_contract_changed_from_v0.2": False,
        "repair": "Removed unsupported JSON-schema uniqueItems keywords; uniqueness remains locally validated.",
    }
    path = root / "design-revisions" / "v0.2.1.json"
    if path.exists() and read(path) != design:
        raise RuntimeError("existing EQ-S v0.2.1 design revision differs")
    write(path, design)


def finalize_after_sources(root: Path, config: Mapping[str, Any], schedule: Sequence[Mapping[str, Any]]) -> None:
    resolved = [effective_result(root, cell) for cell in schedule]
    results = [result for result, _ in resolved if result is not None]
    if len(results) != 15 or not all(row.get("posttest_chain_sealed") is True for row in results):
        write_effective_summary(root, schedule, "truth_embargoed_incomplete_EQS_chain")
        raise RuntimeError("not all 15 EQS responses are sealed; truth remains embargoed")
    truth = eq_v1.generate_truth(root, config)
    for result in results:
        numeric = eq_v1.evaluate_predictions(
            result["posttests"]["Q"].get("payload"),
            queries(config),
            truth[result["world_id"]],
        )
        numeric["eqs"] = evaluate_eqs(
            result["posttests"]["EQS"].get("payload"),
            str(
                world_by_id(config, result["world_id"])["private_authoring"][
                    "mechanism_family"
                ]
            ),
        )
        numeric["response_shape"] = evaluate_structure_predictions(
            result["posttests"]["Q"].get("payload"),
            config,
            truth[result["world_id"]],
        )
        write(root / "evaluations" / f"{result['cell_id']}.json", numeric)
    summary = write_effective_summary(root, schedule, "complete")
    write(
        root / "completion.json",
        {
            "schema_version": "work-ii-eq-s-completion-0.2.1",
            "completed_epoch": time.time(),
            "source_sessions": 15,
            "source_batches": sum(len(row.get("batches", [])) for row in results),
            "posttests": sum(len(row.get("posttests", {})) for row in results),
            "reference_executions": 300,
            "summary_sha256": digest(summary),
        },
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--scope",
        choices=("gate", "freeze", "canary", "remaining", "status"),
        required=True,
    )
    parser.add_argument("--workers", type=int, default=1)
    args = parser.parse_args()
    config = load_config()
    validated = validate_design(config)
    bind_v2_runtime(config)
    root = args.output.resolve()
    root.mkdir(parents=True, exist_ok=True)
    if args.scope == "gate":
        report = run_provider_free_gate(root, config)
        print(
            json.dumps(
                {
                    "stage": "provider_free_gate_complete",
                    "passed": report["passed"],
                    "completed_batches": report["completed_batches"],
                    "provider_calls": 0,
                }
            ),
            flush=True,
        )
        if not report["passed"]:
            raise SystemExit(2)
        return
    if args.scope == "freeze":
        print(json.dumps(create_freeze(root, config)), flush=True)
        return
    if args.scope == "status":
        print(json.dumps(eq_v2.write_summary(root, validated["schedule"], "status")), flush=True)
        return
    freeze = eq_v2.validate_freeze(root, config)
    write_design_revision(root, config, validated, freeze)
    schedule = validated["schedule"]
    canary = [cell for cell in schedule if cell["world_id"] == "EQ-S-W01"]
    if args.scope == "canary":
        if not 1 <= args.workers <= 3:
            raise ValueError("EQ-S canary workers must be in 1..3")
        selected = [cell for cell in canary if effective_result(root, cell)[0] is None]
    else:
        canary_results = [effective_result(root, cell)[0] for cell in canary]
        if not all(
            result is not None
            and result.get("status") == "completed"
            and result.get("posttest_chain_sealed") is True
            for result in canary_results
        ):
            raise RuntimeError("remaining matrix is sealed until all W01 canary chains complete")
        if not 1 <= args.workers <= 8:
            raise ValueError("EQ-S remaining workers must be in 1..8")
        selected = [cell for cell in schedule if cell["world_id"] != "EQ-S-W01"]
    if selected:
        eq_v2.execute_sources(root, config, selected, workers=args.workers)
    summary = write_effective_summary(
        root,
        schedule,
        "canary_complete" if args.scope == "canary" else "sources_complete",
    )
    if args.scope == "canary":
        if summary["completed_sources"] < 3:
            raise RuntimeError("EQ-S canary did not complete all three full chains")
        return
    finalize_after_sources(root, config, schedule)


if __name__ == "__main__":
    main()
