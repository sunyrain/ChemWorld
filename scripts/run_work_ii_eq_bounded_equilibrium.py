#!/usr/bin/env python3
"""Run the EQ five-world, three-arm bounded-equilibrium Work II block."""
# ruff: noqa: E402, E501, C420, RUF007

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import sys
import threading
import time
from collections.abc import Mapping, Sequence
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from statistics import fmean, pstdev
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import scripts.run_work_ii_ec_dual_goal_trial as shared
import scripts.run_work_ii_rx_p_opaque_dual_goal_canary as provider_shared

from chemworld.agents.diagnostic_numerics import FOLLOWUP_NUMERICS
from chemworld.campaign_resources import CampaignResourceCard
from chemworld.data.logging import load_jsonl
from chemworld.eval.runner import run_agent
from chemworld.eval.verify import verify_records
from chemworld.eval.work_ii_truth import _FrozenTruthReplayAgent
from chemworld.research_brief import VERSION as RESEARCH_BRIEF_VERSION
from chemworld.tasks import get_task

CONFIG = ROOT / "configs/benchmark/work_ii_eq_bounded_equilibrium_v1.1.json"
FREEZE = ROOT / "configs/benchmark/work_ii_eq_bounded_equilibrium_freeze_v1.5.json"
TASK = "equilibrium-characterization"
ARMS = ("Opaque", "Aligned", "MisIndexed")
METRICS = ("pH_normalized", "acid_dissociation_fraction", "precipitation_signal")
PROVIDER = {
    "id": "chemworld_openai_https",
    "name": "OpenAI",
    "model": "gpt-5.6-sol",
    "reasoning_effort": "medium",
    "auth_mode": "chatgpt_subscription_cached_login",
    "wire_api": "responses",
}
GOALS = {
    "characterization": (
        "Characterize this bounded aqueous-equilibrium world. Identify effective relationships "
        "among total loading, liquid volume or dilution, pH, acid dissociation, and the public "
        "precipitation proxy. Test the supplied local relationship if one exists, revise or reject "
        "it when observations warrant, distinguish equivalent explanations, and state uncertainty "
        "and scope. This is not a yield-optimization or product-process task."
    )
}
SYSTEM = """You are an autonomous scientist in a simulated bounded aqueous-equilibrium laboratory.
Use only the supplied chemworld_lab tools and public_numerics calculator. No filesystem, network,
repository inspection, external retrieval, or hidden-simulator access is allowed. The task's
research_goal is authoritative. Complete exactly 12 independent batches; repetition is allowed.
You have at most 12 non-final instrument uses across the campaign plus 12 final assays. Use legal
solvent-volume and reagent-amount changes, including staged additions when scientifically useful,
and choose measurements autonomously. This is a bounded weak-acid/precipitation slice, not general
aqueous chemistry. pH_normalized is pH/14; acid_dissociation_fraction and precipitation_signal are
bounded public response channels. equilibrium_residual and equilibrium_confidence are environment
diagnostics: equilibrium_confidence is not your uncertainty and is not a task score. Do not optimize
it. There are no mandatory equations, belief snapshots, or batch-group plans. For every batch,
explicitly terminate and then measure final_assay. A batch ending is not the campaign ending:
continue with next_state until campaign_ended is true. After the twelfth batch, use
commit_final_recommendation to select the completed batch that is the most useful evidentiary anchor,
with a short English rationale; this is not an optimization claim. Then return the required concise
English status/summary JSON. A separate same-thread sequence will request a full K1 report, fixed
blind predictions, and K2 retrospective questions. Do not answer those early. Supplied prior
information may be incomplete or inaccurate; public observations are authoritative. No particular
scientific result is required.
"""
K1 = """The experimental campaign has ended and the evidentiary anchor is sealed. Submit a complete,
self-contained scientific report in English. Explain how you think this bounded aqueous-equilibrium
world works: effective relationships among loading, volume or dilution, pH, acid dissociation, and
precipitation; important couplings or possible equations; which experiments and numerical results
formed or changed the account; its applicable range; what is not identifiable; and plausible
equivalent or competing explanations. State how any supplied prior was supported, revised, rejected,
or left untested, and state explicitly if no instance prior was supplied. Cite actual batch numbers
and values. Distinguish observation, interpolation, extrapolation, and conjecture. Do not perform new
experiments or invent unmeasured information. Develop the account fully rather than compressing it
into a short abstract. Return the JSON report field. The fixed prediction questions are revealed only
after this report is sealed.
"""
Q_PROMPT = """Using only your completed research and sealed K1 account, predict the final outcomes of
the following 12 independent new batches. Every batch starts independently from the same frozen
world. For every query and every requested metric, return a point estimate and an 80% prediction
interval, plus a substantive English per-query rationale and an English shared rationale. Account
for both model and observation uncertainty. Do not run experiments and do not modify K1. The public
environment field equilibrium_confidence is not requested, is not your uncertainty, and must not be
used as a replacement score. Return the complete predictions JSON.
"""
K2 = """Your K1 report and Q predictions are sealed, and no prediction truth or score has been shown.
Answer all seven items in English. Cite actual batch numbers and specific K1 judgments without
repeating the full experiment table or rewriting K1/Q. Do not run an experiment and do not present
hindsight as a belief recorded during the campaign.

1. Which supplied effective-acidity or dilution claims were supported, contradicted, or untested?
If no instance claim was supplied, say so. Distinguish no observed contradiction from observed
contradiction that was not acted on.
2. Which experiments actually formed or changed your account? Which choices depended mainly on the
prior, accumulated observations, or an untested assumption?
3. What competing or equivalent explanations remain? What can and cannot be distinguished by the
available evidence?
4. If exactly one additional legal complete experiment were allowed, what condition and measurement
would be most informative, and how would different possible results change your account? Do not
execute it.
5. How did the characterization objective shape experimental choice, including trade-offs among
broad coverage, replication, local identification, and precipitation-sensitive conditions?
6. What acquired evidence was underused? Which blind predictions are least reliable, which 80%
intervals may be too narrow, and where are they inconsistent with K1 scope or uncertainty?
7. What are the limitations of the sealed evidentiary anchor and of generalization across
concentration, volume, staged additions, precipitation regime, and worlds?

Return the JSON report field.
"""


def with_eq_mcp_startup_timeout(command: Sequence[str]) -> list[str]:
    """Allow the Materials NFS-backed MCP import to finish without changing tool budgets."""
    old = "mcp_servers.chemworld_lab.startup_timeout_sec=30"
    new = "mcp_servers.chemworld_lab.startup_timeout_sec=180"
    adjusted = [new if argument == old else argument for argument in command]
    if adjusted.count(new) != 1:
        raise RuntimeError("EQ runner could not bind the laboratory MCP startup timeout")
    return adjusted


class EqFreeResearchAgent(provider_shared.RxFreeResearchAgent):
    def _command(self, *, instructions_path: Path, schema_path: Path) -> list[str]:
        return with_eq_mcp_startup_timeout(
            super()._command(
                instructions_path=instructions_path,
                schema_path=schema_path,
            )
        )


def read(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_config() -> dict[str, Any]:
    """Resolve the versioned repair overlay without altering its failed predecessor."""
    overlay = read(CONFIG)
    binding = overlay.get("base_config")
    if not isinstance(binding, Mapping):
        return overlay
    base_path = ROOT / str(binding["path"])
    if file_sha256(base_path) != binding["sha256"]:
        raise RuntimeError("EQ repair overlay does not bind the current base config")
    resolved = read(base_path)
    resolved["schema_version"] = overlay["schema_version"]
    resolved["status"] = overlay["status"]
    resolved["protocol"] = overlay["protocol"]
    resolved["queries"] = copy.deepcopy(overlay["query_replacement"])
    resolved["repair"] = {
        key: copy.deepcopy(value)
        for key, value in overlay.items()
        if key not in {"query_replacement"}
    }
    return resolved


def write(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def digest(payload: Any) -> str:
    body = json.dumps(payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def deterministic_seed(*parts: object) -> int:
    text = "|".join(str(part) for part in parts)
    return int.from_bytes(hashlib.sha256(text.encode()).digest()[:8], "big") % 2_147_483_647


def resource_card(config: Mapping[str, Any], batches: int = 12) -> CampaignResourceCard:
    frozen = config["source_resource_card"]
    scale = batches / 12
    return CampaignResourceCard(
        card_id=f"eq-bounded-equilibrium-v1-{batches}",
        operation_attempt_limit=int(frozen["operation_attempt_limit"] * scale),
        vessel_start_limit=batches,
        final_assay_limit=batches,
        nonfinal_instrument_use_limit=batches,
        stock_limits={
            "reagent_mol": float(frozen["reagent_mol"]) * scale,
            "solvent_L": float(frozen["solvent_L"]) * scale,
        },
        process_time_limit_s=None,
    )


def queries(config: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = copy.deepcopy(list(config["queries"]))
    expected = [f"Q{index:02d}" for index in range(1, 13)]
    if len(rows) != 12 or [row.get("query_id") for row in rows] != expected:
        raise ValueError("EQ query contract must be ordered Q01--Q12")
    return rows


def world_by_id(config: Mapping[str, Any], world_id: str) -> Mapping[str, Any]:
    world = next((row for row in config["worlds"] if row["world_id"] == world_id), None)
    if world is None:
        raise KeyError(world_id)
    return world


def public_prior(config: Mapping[str, Any], world_id: str, arm: str) -> dict[str, Any] | None:
    if arm == "Opaque":
        return None
    world = world_by_id(config, world_id)
    source = world
    if arm == "MisIndexed":
        source = world_by_id(config, world["private_authoring"]["misindexed_world_id"])
    claim = source["private_authoring"]["aligned_prior"]
    contract = config["prior_contract"]
    return {
        "schema_version": contract["schema_version"],
        "scope": contract["scope"],
        "claim": {
            "effective_pka_interval80": list(claim["effective_pka_interval80"]),
            "dilution_response": {
                "anchor": copy.deepcopy(contract["anchor"]),
                "delta_pH_normalized": claim["dilution_delta_pH_normalized"],
                "delta_acid_dissociation_fraction": claim[
                    "dilution_delta_acid_dissociation_fraction"
                ],
            },
        },
        "confidence": copy.deepcopy(contract["confidence"]),
    }


def research_brief() -> dict[str, Any]:
    return {
        "schema_version": RESEARCH_BRIEF_VERSION,
        "card": "EQ",
        "prior_record": None,
    }


def validate_design(config: Mapping[str, Any]) -> dict[str, Any]:
    counts = config["counts"]
    if counts != {
        "worlds": 5,
        "independent_source_sessions": 15,
        "source_batches_per_session": 12,
        "source_batches": 180,
        "posttests_per_session": 3,
        "posttests": 45,
        "reference_repeats_per_query": 5,
        "reference_executions": 300,
    }:
        raise ValueError("EQ frozen denominators changed")
    if tuple(config["arms"]) != ARMS or tuple(config["prediction_metrics"]) != METRICS:
        raise ValueError("EQ frozen arms or metric set changed")
    query_rows = queries(config)
    worlds = list(config["worlds"])
    if len(worlds) != 5 or len({row["world_id"] for row in worlds}) != 5:
        raise ValueError("EQ requires five unique worlds")
    for world in worlds:
        opaque = public_prior(config, world["world_id"], "Opaque")
        aligned = public_prior(config, world["world_id"], "Aligned")
        wrong = public_prior(config, world["world_id"], "MisIndexed")
        if opaque is not None or aligned is None or wrong is None:
            raise ValueError("EQ prior arms are incomplete")
        comparable_a = copy.deepcopy(aligned)
        comparable_m = copy.deepcopy(wrong)
        claim_a = comparable_a.pop("claim")
        claim_m = comparable_m.pop("claim")
        if comparable_a != comparable_m or set(claim_a) != set(claim_m) or claim_a == claim_m:
            raise ValueError(f"EQ A/M mismatch outside the registered claim: {world['world_id']}")
        if set(claim_a["dilution_response"]) != set(claim_m["dilution_response"]):
            raise ValueError("EQ A/M dilution schema differs")
        if claim_a["dilution_response"]["anchor"] != claim_m["dilution_response"]["anchor"]:
            raise ValueError("EQ A/M public anchors differ")
    required_coverage = {
        "near_domain",
        "concentration_volume_decoupling",
        "two_stage_dosing",
        "dissociation_precipitation_competition",
        "boundary_extrapolation",
        "equivalent_explanation",
        "interval_calibration",
    }
    observed_coverage = {tag for row in query_rows for tag in row["coverage"]}
    if not required_coverage <= observed_coverage:
        raise ValueError("EQ Q coverage contract is incomplete")
    schedule = [
        {
            "cell_id": f"{world['world_id']}--{arm}",
            "world_id": world["world_id"],
            "world_seed": int(world["world_seed"]),
            "world_interventions": copy.deepcopy(world["world_interventions"]),
            "arm": arm,
            "goal": "characterization",
        }
        for world in worlds
        for arm in ARMS
    ]
    return {
        "schedule": schedule,
        "query_sha256": digest(query_rows),
        "prior_sha256": {
            row["cell_id"]: digest(public_prior(config, row["world_id"], row["arm"]))
            for row in schedule
        },
    }


def configure_provider_helpers(config: Mapping[str, Any]) -> None:
    shared.TASK = TASK
    shared.PROVIDER = PROVIDER
    shared.METRICS = list(METRICS)
    shared.GOALS = GOALS
    shared.SYSTEM = SYSTEM
    shared.K1 = K1
    shared.K2 = K2
    shared.resource_card = lambda batches=12: resource_card(config, batches)
    shared.build_command = provider_shared.build_command


def physics(
    agent: Any,
    output: Path,
    *,
    config: Mapping[str, Any],
    world: Mapping[str, Any],
    batches: int = 12,
    observation_seed: int,
    observation_namespace: str,
    callback: Any = None,
) -> Any:
    operations = int(config["source_resource_card"]["operation_attempt_limit"] * batches / 12)
    return run_agent(
        env_id=get_task(TASK).env_id,
        agent=agent,
        task_id=TASK,
        world_split=config["world_split"],
        objective=config["objective"],
        seed=int(world["world_seed"]),
        world_interventions=copy.deepcopy(world["world_interventions"]),
        agent_seed=deterministic_seed("eq-agent", world["world_id"]),
        observation_seed=observation_seed,
        budget=operations,
        budget_override=operations,
        episode_mode_override="campaign" if batches > 1 else "single_experiment",
        campaign_resource_card=resource_card(config, batches),
        material_information={"mode": "opaque_codes"},
        research_brief=research_brief(),
        observation_noise_mode="keyed",
        observation_noise_namespace=observation_namespace,
        output_path=output,
        step_callback=callback,
        method_resource_limits=(
            {
                "operation_limit": operations,
                "complete_experiment_limit": batches,
                "wall_time_limit_s": 5700,
                "model_call_limit": 1,
                "input_token_limit": 8_000_000,
                "uncached_input_token_limit": 2_000_000,
                "output_token_limit": 128_000,
                "training_environment_step_limit": 0,
            }
            if isinstance(agent, provider_shared.RxFreeResearchAgent)
            else None
        ),
    )


def reference_run(
    folder: Path,
    actions: Sequence[Mapping[str, Any]],
    *,
    config: Mapping[str, Any],
    world: Mapping[str, Any],
    batches: int,
    observation_seed: int,
    observation_namespace: str,
) -> dict[str, Any]:
    result_path = folder / "result.json"
    if result_path.exists():
        return read(result_path)
    if folder.exists():
        raise RuntimeError(f"incomplete write-once reference directory: {folder}")
    folder.mkdir(parents=True)
    failure = None
    try:
        physics(
            _FrozenTruthReplayAgent(list(actions)),
            folder / "trajectory.jsonl",
            config=config,
            world=world,
            batches=batches,
            observation_seed=observation_seed,
            observation_namespace=observation_namespace,
        )
    except Exception as exc:
        failure = {"type": type(exc).__name__, "message": str(exc)[:1600]}
    records = load_jsonl(folder / "trajectory.jsonl") if (folder / "trajectory.jsonl").exists() else []
    replay = (
        verify_records(
            records,
            tolerance=0,
            world_interventions=copy.deepcopy(world["world_interventions"]),
        ).to_dict()
        if records
        else {"verified": False}
    )
    result = {
        "failure": failure,
        "batches": shared.summaries(records),
        "operation_attempts": len(records),
        "rollbacks": [
            index + 1
            for index, row in enumerate(records)
            if row.get("transaction_status") != "committed"
        ],
        "exact_replay": replay,
    }
    write(result_path, result)
    return result


def _metric_means(repeats: Sequence[Mapping[str, Any]]) -> dict[str, float]:
    return {metric: fmean(float(row[metric]) for row in repeats) for metric in METRICS}


def run_provider_free_gate(root: Path, config: Mapping[str, Any]) -> dict[str, Any]:
    gate_root = root / "provider-free-gate"
    report_path = gate_root / "gate.json"
    if report_path.exists():
        return read(report_path)
    query_rows = queries(config)
    gate = config["provider_free_gate"]
    repeats = int(gate["noise_repeats"])
    actions = [action for query in query_rows for action in query["actions"]]
    all_results: dict[str, dict[str, list[dict[str, float]]]] = {}
    replay_passes = 0
    planned_runs = len(config["worlds"]) * repeats
    completed_runs = 0
    started = time.monotonic()
    for world in config["worlds"]:
        world_results = {query["query_id"]: [] for query in query_rows}
        for repeat in range(1, repeats + 1):
            result = reference_run(
                gate_root / "runs" / world["world_id"] / f"repeat-{repeat:02d}",
                actions,
                config=config,
                world=world,
                batches=12,
                observation_seed=deterministic_seed(
                    "eq-provider-free-gate-v1", world["world_id"], repeat
                ),
                observation_namespace=(
                    f"work-ii-eq-gate-{world['world_id'].lower()}-r{repeat:02d}"
                ),
            )
            if result["failure"] or result["rollbacks"] or len(result["batches"]) != 12:
                raise RuntimeError(
                    f"EQ provider-free gate execution failed: {world['world_id']}/r{repeat:02d}"
                )
            replay_passes += result["exact_replay"].get("verified") is True
            for query, batch in zip(query_rows, result["batches"], strict=True):
                world_results[query["query_id"]].append(
                    {metric: float(batch["metrics"][metric]) for metric in METRICS}
                )
            completed_runs += 1
            elapsed = time.monotonic() - started
            print(
                json.dumps(
                    {
                        "stage": "provider_free_gate",
                        "completed_campaigns": completed_runs,
                        "total_campaigns": planned_runs,
                        "completed_batches": completed_runs * 12,
                        "total_batches": planned_runs * 12,
                        "throughput_batches_per_min": round(completed_runs * 12 / elapsed * 60, 2),
                        "eta_s": round(elapsed / completed_runs * (planned_runs - completed_runs)),
                    }
                ),
                flush=True,
            )
        all_results[world["world_id"]] = world_results

    mean_grid = {
        world_id: {query_id: _metric_means(values) for query_id, values in rows.items()}
        for world_id, rows in all_results.items()
    }
    pka_centers = {
        world["world_id"]: float(world["private_authoring"]["effective_pka"])
        for world in config["worlds"]
    }
    ordered_ids = [world["world_id"] for world in config["worlds"]]
    per_query_separation = {}
    for query in query_rows:
        query_id = query["query_id"]
        adjacent = []
        for left, right in zip(ordered_ids, ordered_ids[1:], strict=False):
            left_values = [14 * row["pH_normalized"] for row in all_results[left][query_id]]
            right_values = [14 * row["pH_normalized"] for row in all_results[right][query_id]]
            gap = abs(fmean(right_values) - fmean(left_values))
            noise = math.sqrt(pstdev(left_values) ** 2 + pstdev(right_values) ** 2)
            adjacent.append(
                {"pair": [left, right], "gap_pH": gap, "separation_sigma": gap / max(noise, 0.02)}
            )
        per_query_separation[query_id] = adjacent
    best_probe = max(
        per_query_separation,
        key=lambda query_id: min(
            row["separation_sigma"] for row in per_query_separation[query_id]
        ),
    )
    best_probe_min_sigma = min(
        row["separation_sigma"] for row in per_query_separation[best_probe]
    )
    best_probe_min_gap = min(row["gap_pH"] for row in per_query_separation[best_probe])

    response_spans = {}
    for world_id in ordered_ids:
        response_spans[world_id] = {
            "pH": 14
            * (
                max(row["pH_normalized"] for row in mean_grid[world_id].values())
                - min(row["pH_normalized"] for row in mean_grid[world_id].values())
            ),
            "acid_dissociation_fraction": max(
                row["acid_dissociation_fraction"] for row in mean_grid[world_id].values()
            )
            - min(row["acid_dissociation_fraction"] for row in mean_grid[world_id].values()),
            "precipitation_signal": max(
                row["precipitation_signal"] for row in mean_grid[world_id].values()
            )
            - min(row["precipitation_signal"] for row in mean_grid[world_id].values()),
        }
    default_mae = fmean(
        abs(row["pH_normalized"] - 0.5)
        for world_rows in mean_grid.values()
        for row in world_rows.values()
    )
    one_shot_maes = {}
    for world_id in ordered_ids:
        anchor = mean_grid[world_id]["Q12"]["pH_normalized"]
        one_shot_maes[world_id] = fmean(
            abs(row["pH_normalized"] - anchor) for row in mean_grid[world_id].values()
        )
    equivalent_gaps = {}
    for world_id in ordered_ids:
        equivalent = [mean_grid[world_id][query_id] for query_id in ("Q05", "Q06", "Q07")]
        equivalent_gaps[world_id] = max(
            max(row[metric] for row in equivalent) - min(row[metric] for row in equivalent)
            for metric in METRICS
        )
    aligned_passes = {}
    misindexed_gaps = {}
    for world in config["worlds"]:
        world_id = world["world_id"]
        actual = pka_centers[world_id]
        aligned = public_prior(config, world_id, "Aligned")
        wrong = public_prior(config, world_id, "MisIndexed")
        assert aligned is not None and wrong is not None
        low, high = aligned["claim"]["effective_pka_interval80"]
        wrong_low, wrong_high = wrong["claim"]["effective_pka_interval80"]
        aligned_passes[world_id] = low <= actual <= high
        misindexed_gaps[world_id] = min(abs(actual - wrong_low), abs(actual - wrong_high))

    checks = {
        "exact_replay": replay_passes / planned_runs >= gate["require_exact_replay_fraction"],
        "five_worlds_complete": len(all_results) == 5
        and all(len(rows) == 12 for rows in all_results.values()),
        "strict_opaque_no_instance_prior": all(
            public_prior(config, world_id, "Opaque") is None for world_id in ordered_ids
        ),
        "aligned_compatible": all(aligned_passes.values()),
        "misindexed_publicly_refutable": min(misindexed_gaps.values())
        >= gate["minimum_misindexed_pka_center_gap"],
        "adjacent_world_separation": best_probe_min_gap
        >= gate["minimum_adjacent_world_pH_gap"],
        "response_signal": all(
            span["pH"] >= gate["minimum_within_world_pH_span"]
            and span["acid_dissociation_fraction"]
            >= gate["minimum_within_world_dissociation_span"]
            and span["precipitation_signal"]
            >= gate["minimum_within_world_precipitation_span"]
            for span in response_spans.values()
        ),
        "active_information_gain": best_probe_min_sigma
        >= gate["minimum_best_probe_adjacent_separation_sigma"],
        "default_nontrivial": default_mae
        >= gate["minimum_default_constant_mae_pH_normalized"],
        "one_shot_nontrivial": min(one_shot_maes.values())
        >= gate["minimum_one_shot_constant_mae_pH_normalized"],
        "equivalent_paths_stable": max(equivalent_gaps.values())
        <= gate["maximum_equivalent_path_mean_gap"],
        "q_numeric_stability": all(
            math.isfinite(value) and 0 <= value <= 1
            for world_rows in mean_grid.values()
            for row in world_rows.values()
            for value in row.values()
        ),
        "budget_window": completed_runs == planned_runs,
    }
    report = {
        "schema_version": "work-ii-eq-provider-free-gate-1.0",
        "config_sha256": file_sha256(CONFIG),
        "provider_calls": 0,
        "planned_campaigns": planned_runs,
        "completed_campaigns": completed_runs,
        "planned_batches": planned_runs * 12,
        "completed_batches": completed_runs * 12,
        "replay_passes": replay_passes,
        "checks": checks,
        "passed": all(checks.values()),
        "best_probe": best_probe,
        "best_probe_min_adjacent_gap_pH": best_probe_min_gap,
        "best_probe_min_adjacent_separation_sigma": best_probe_min_sigma,
        "response_spans": response_spans,
        "default_constant_mae_pH_normalized": default_mae,
        "one_shot_constant_mae_pH_normalized": one_shot_maes,
        "equivalent_path_max_mean_gap": equivalent_gaps,
        "misindexed_pka_interval_edge_gaps": misindexed_gaps,
        "mean_grid": mean_grid,
        "thresholds": copy.deepcopy(gate),
        "elapsed_s": time.monotonic() - started,
    }
    write(report_path, report)
    markdown = [
        "# EQ provider-free gate",
        "",
        f"Status: **{'PASS' if report['passed'] else 'FAIL'}**. Provider calls: 0.",
        "",
        f"Completed {completed_runs}/{planned_runs} campaigns and {completed_runs * 12}/{planned_runs * 12} batches; exact replay {replay_passes}/{planned_runs}.",
        f"Best pre-registered query probe: {best_probe}; minimum adjacent gap {best_probe_min_gap:.4f} pH and separation {best_probe_min_sigma:.2f} sigma.",
        "",
        "| Check | Pass |",
        "| --- | --- |",
        *[f"| {name} | {'yes' if value else 'no'} |" for name, value in checks.items()],
        "",
        "Thresholds were frozen in the machine config before this gate. A failure is retained and requires a versioned repair; no threshold is relaxed here.",
        "",
    ]
    (gate_root / "GATE_REPORT.md").write_text("\n".join(markdown), encoding="utf-8")
    return report


def posttest_schema(stage: str) -> dict[str, Any]:
    if stage != "Q":
        return {
            "type": "object",
            "additionalProperties": False,
            "properties": {"report": {"type": "string"}},
            "required": ["report"],
        }
    interval = {
        "type": "object",
        "additionalProperties": False,
        "properties": {key: {"type": "number"} for key in ("estimate", "lower80", "upper80")},
        "required": ["estimate", "lower80", "upper80"],
    }
    metric_map = {
        "type": "object",
        "additionalProperties": False,
        "properties": {metric: interval for metric in METRICS},
        "required": list(METRICS),
    }
    row = {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "query_id": {"type": "string"},
            "metrics": metric_map,
            "rationale": {"type": "string"},
        },
        "required": ["query_id", "metrics", "rationale"],
    }
    return {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "predictions": {"type": "array", "items": row, "minItems": 12, "maxItems": 12},
            "rationale": {"type": "string"},
        },
        "required": ["predictions", "rationale"],
    }


def _contains_cjk(text: str) -> bool:
    return any("\u3400" <= char <= "\u9fff" for char in text)


def validate_posttest(stage: str, payload: Any, query_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    if not isinstance(payload, Mapping):
        return {"valid": False, "failure": "missing_payload"}
    if stage != "Q":
        report = payload.get("report")
        valid = isinstance(report, str) and bool(report.strip()) and not _contains_cjk(report)
        return {"valid": valid, "failure": None if valid else "report_missing_or_not_English"}
    rows = payload.get("predictions")
    if not isinstance(rows, list) or len(rows) != 12:
        return {"valid": False, "failure": "predictions_missing_or_wrong_count"}
    expected = [row["query_id"] for row in query_rows]
    ids = [row.get("query_id") for row in rows if isinstance(row, Mapping)]
    if sorted(ids) != sorted(expected):
        return {"valid": False, "failure": "query_ids_missing_or_duplicated"}
    try:
        for row in rows:
            if not isinstance(row.get("rationale"), str) or _contains_cjk(row["rationale"]):
                raise ValueError("row_rationale_missing_or_not_English")
            if set(row["metrics"]) != set(METRICS):
                raise ValueError("metric_set_mismatch")
            for metric in METRICS:
                estimate, lower, upper = (
                    float(row["metrics"][metric][key])
                    for key in ("estimate", "lower80", "upper80")
                )
                if not all(math.isfinite(value) for value in (estimate, lower, upper)):
                    raise ValueError("non_finite_prediction")
                if not 0 <= lower <= estimate <= upper <= 1:
                    raise ValueError("invalid_prediction_interval")
        rationale = payload.get("rationale")
        if not isinstance(rationale, str) or _contains_cjk(rationale):
            raise ValueError("overall_rationale_missing_or_not_English")
    except (KeyError, TypeError, ValueError) as exc:
        return {"valid": False, "failure": str(exc)}
    return {"valid": True, "failure": None}


def run_posttest(
    agent: Any,
    folder: Path,
    private_folder: Path,
    stage: str,
    thread_id: str,
    progress: dict[str, Any],
    query_rows: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    workspace = agent.home_root / "followup"
    workspace.mkdir(exist_ok=True)
    schema_path = workspace / f"{stage}-schema.json"
    write(schema_path, posttest_schema(stage))
    instructions = workspace / "instructions.md"
    instructions.write_text(
        "Continue your own completed research using your existing public observations. "
        "No new laboratory experiments, network, filesystem, repository, or hidden-truth access. "
        "Only public_numerics.calculate is available. Answer the current question fully in English; "
        "do not rewrite earlier sealed outputs. equilibrium_confidence is an environment diagnostic, "
        "not your uncertainty and not a task score.",
        encoding="utf-8",
    )
    message = K1 if stage == "K1" else K2
    if stage == "Q":
        message = Q_PROMPT + "\n" + json.dumps(list(query_rows), ensure_ascii=False)
    audit = private_folder / f"{stage}-numerics.jsonl"
    command = provider_shared.build_command(
        PROVIDER,
        schema_path,
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
        f"model_instructions_file={json.dumps(instructions.as_posix())}",
    ]
    raw = shared.launch(
        command,
        message,
        workspace,
        agent.followup_environment,
        private_folder / stage,
        1200,
        True,
        audit,
        {**progress, "phase": stage},
        numerics_budget=FOLLOWUP_NUMERICS,
    )
    write(private_folder / stage / "receipt.json", raw)
    public = {
        "payload": raw.get("payload"),
        "failure": raw.get("failure") or (None if raw.get("payload") else "missing_payload"),
        "elapsed_s": raw.get("elapsed_s"),
        "method_resources": raw.get("method_resources"),
    }
    write(folder / "sealed" / f"{stage}.json", public)
    return public


def run_cell(
    root: Path,
    config: Mapping[str, Any],
    cell: Mapping[str, Any],
    progress: dict[str, Any],
    progress_lock: threading.Lock,
) -> dict[str, Any]:
    folder = root / "sources" / cell["cell_id"]
    result_path = folder / "RESULT.json"
    if result_path.exists():
        return read(result_path)
    if folder.exists():
        raise RuntimeError(f"incomplete write-once cell requires recovery: {cell['cell_id']}")
    private_folder = create_cell_folders(folder)
    prior = public_prior(config, cell["world_id"], cell["arm"])
    write(
        folder / "public-input-binding.json",
        {
            "cell_id": cell["cell_id"],
            "research_brief": research_brief(),
            "initial_world_model": prior,
            "world_public_id": cell["world_id"],
            "arm": cell["arm"],
            "source_batches": 12,
        },
    )
    write(private_folder / "attempt.json", {**dict(cell), "started_epoch": time.time()})
    world = world_by_id(config, cell["world_id"])
    started = time.monotonic()
    result: dict[str, Any] = {
        "schema_version": "work-ii-eq-cell-result-1.0",
        "cell_id": cell["cell_id"],
        "world_id": cell["world_id"],
        "arm": cell["arm"],
        "goal": cell["goal"],
        "status": "failed",
        "failure": None,
        "posttests": {},
        "posttest_validation": {},
    }
    agent = EqFreeResearchAgent(
        goal=cell["goal"],
        home_root=private_folder / "home",
        output=private_folder / "source",
        workspace=private_folder / "laboratory",
        initial_world_model=prior,
        request_timeout_s=1200,
        finalization_timeout_s=300,
        session_wall_time_limit_s=5400,
        max_recovered_mcp_tool_failures=12,
        max_consecutive_mcp_tool_failures=6,
        max_provider_error_events=0,
        pre_action_restart_limit=0,
        accepted_turn_continuation_limit=0,
        provider_process_attempt_limit=1,
        max_initial_prompt_bytes=262144,
        max_tool_output_bytes=131072,
        history_event_limit=360,
        history_byte_limit=524288,
        session_progress_callback=lambda payload: progress.update(
            {cell["cell_id"]: {"phase": "source", "provider": payload}}
        ),
    )
    cell_progress = {"stage": cell["cell_id"], "phase": "source", "operations": 0, "batches": 0}

    def callback(record: Any, trace: Any) -> None:
        del trace
        cell_progress["operations"] += 1
        if (
            record.info.get("instrument") == "final_assay"
            and record.info.get("transaction_status") == "committed"
        ):
            cell_progress["batches"] += 1
        with progress_lock:
            progress[cell["cell_id"]] = dict(cell_progress)

    try:
        physics(
            agent,
            folder / "trajectory.jsonl",
            config=config,
            world=world,
            observation_seed=deterministic_seed("eq-source-v1", cell["cell_id"]),
            observation_namespace=f"work-ii-eq-source-{cell['cell_id'].lower()}",
            callback=callback,
        )
    except Exception as exc:
        result["failure"] = {"type": type(exc).__name__, "message": str(exc)[:1600]}
    finally:
        agent.close()
    records = load_jsonl(folder / "trajectory.jsonl") if (folder / "trajectory.jsonl").exists() else []
    result["batches"] = shared.summaries(records)
    result["operations"] = len(records)
    result["rollbacks"] = [
        {"step": index + 1, "action": row.get("action"), "reason": row.get("rollback_reason")}
        for index, row in enumerate(records)
        if row.get("transaction_status") != "committed"
    ]
    result["exact_replay"] = (
        verify_records(
            records,
            tolerance=0,
            world_interventions=copy.deepcopy(world["world_interventions"]),
        ).to_dict()
        if records
        else {"verified": False}
    )
    receipts = agent.provider_receipts()
    write(private_folder / "source-receipts.json", receipts)
    result["source_usage"] = agent.method_resource_usage()
    last = receipts[-1] if receipts else {}
    thread_id = last.get("thread_id")
    result["thread_id_sha256"] = (
        hashlib.sha256(str(thread_id).encode()).hexdigest() if thread_id else None
    )
    result["evidentiary_anchor"] = last.get("final_recommendation")
    result["source_status"] = (
        "completed"
        if len(result["batches"]) == 12 and result["exact_replay"].get("verified") is True
        else "partial"
        if result["batches"]
        else "failed"
    )
    query_rows = queries(config)
    if thread_id and result["source_status"] == "completed":
        for stage in ("K1", "Q", "K2"):
            cell_progress["phase"] = stage
            turn = run_posttest(
                agent,
                folder,
                private_folder,
                stage,
                str(thread_id),
                cell_progress,
                query_rows,
            )
            result["posttests"][stage] = turn
            result["posttest_validation"][stage] = validate_posttest(
                stage, turn.get("payload"), query_rows
            )
            if not result["posttest_validation"][stage]["valid"]:
                break
    result["posttest_chain_sealed"] = all(
        result["posttest_validation"].get(stage, {}).get("valid") is True
        for stage in ("K1", "Q", "K2")
    )
    result["status"] = (
        "completed"
        if result["source_status"] == "completed"
        and result["posttest_chain_sealed"]
        and not result["failure"]
        else "retained_nonconforming"
    )
    result["elapsed_s"] = time.monotonic() - started
    write(result_path, result)
    return result


def create_cell_folders(folder: Path) -> Path:
    """Create every write-once parent required before the provider process can launch."""
    folder.mkdir(parents=True)
    private_folder = folder / "private-provider"
    private_folder.mkdir()
    (private_folder / "source").mkdir()
    return private_folder


def evaluate_predictions(
    payload: Any,
    query_rows: Sequence[Mapping[str, Any]],
    truth: Mapping[str, Sequence[Mapping[str, float]]],
) -> dict[str, Any]:
    validation = validate_posttest("Q", payload, query_rows)
    if not validation["valid"]:
        return validation
    predictions = {row["query_id"]: row for row in payload["predictions"]}
    output = {}
    for metric in METRICS:
        errors: list[float] = []
        coverage: list[bool] = []
        widths: list[float] = []
        interval_scores: list[float] = []
        for query in query_rows:
            query_id = query["query_id"]
            interval = predictions[query_id]["metrics"][metric]
            estimate, lower, upper = (
                float(interval[key]) for key in ("estimate", "lower80", "upper80")
            )
            outcomes = [float(row[metric]) for row in truth[query_id]]
            errors.append(abs(estimate - fmean(outcomes)))
            for outcome in outcomes:
                coverage.append(lower <= outcome <= upper)
                widths.append(upper - lower)
                penalty = 0.0
                if outcome < lower:
                    penalty = 10 * (lower - outcome)
                elif outcome > upper:
                    penalty = 10 * (outcome - upper)
                interval_scores.append((upper - lower) + penalty)
        output[metric] = {
            "query_count": 12,
            "reference_observation_count": 60,
            "mae_to_five_repeat_mean": fmean(errors),
            "empirical_coverage80": fmean(coverage),
            "mean_width80": fmean(widths),
            "mean_interval_score_alpha_0_2": fmean(interval_scores),
        }
    return {
        "valid": True,
        "metrics": output,
        "equilibrium_confidence_used_as_agent_uncertainty_or_score": False,
    }


def generate_truth(root: Path, config: Mapping[str, Any]) -> dict[str, Any]:
    truth_path = root / "reference-truth" / "truth.json"
    if truth_path.exists():
        return read(truth_path)
    query_rows = queries(config)
    actions = [action for query in query_rows for action in query["actions"]]
    truth: dict[str, dict[str, list[dict[str, float]]]] = {}
    completed = 0
    total = 25
    started = time.monotonic()
    for world in config["worlds"]:
        truth[world["world_id"]] = {query["query_id"]: [] for query in query_rows}
        for repeat in range(1, 6):
            result = reference_run(
                root / "reference-truth" / "runs" / world["world_id"] / f"repeat-{repeat:02d}",
                actions,
                config=config,
                world=world,
                batches=12,
                observation_seed=deterministic_seed(
                    "eq-reference-truth-v1", world["world_id"], repeat
                ),
                observation_namespace=(
                    f"work-ii-eq-truth-{world['world_id'].lower()}-r{repeat:02d}"
                ),
            )
            if result["failure"] or result["rollbacks"] or len(result["batches"]) != 12:
                raise RuntimeError(
                    f"EQ reference truth failed: {world['world_id']}/r{repeat:02d}"
                )
            for query, batch in zip(query_rows, result["batches"], strict=True):
                truth[world["world_id"]][query["query_id"]].append(
                    {metric: float(batch["metrics"][metric]) for metric in METRICS}
                )
            completed += 1
            elapsed = time.monotonic() - started
            print(
                json.dumps(
                    {
                        "stage": "reference_truth",
                        "completed_campaigns": completed,
                        "total_campaigns": total,
                        "completed_executions": completed * 12,
                        "total_executions": 300,
                        "eta_s": round(elapsed / completed * (total - completed)),
                    }
                ),
                flush=True,
            )
    write(truth_path, truth)
    return truth


def write_summary(root: Path, schedule: Sequence[Mapping[str, Any]], phase: str) -> dict[str, Any]:
    results = []
    for cell in schedule:
        path = root / "sources" / cell["cell_id"] / "RESULT.json"
        if path.exists():
            results.append(read(path))
    payload = {
        "schema_version": "work-ii-eq-matrix-summary-1.0",
        "phase": phase,
        "planned_sources": 15,
        "planned_source_batches": 180,
        "planned_posttests": 45,
        "attempted_sources": len(results),
        "completed_sources": sum(row.get("status") == "completed" for row in results),
        "completed_source_batches": sum(len(row.get("batches", [])) for row in results),
        "sealed_posttests": sum(len(row.get("posttests", {})) for row in results),
        "sealed_posttest_chains": sum(row.get("posttest_chain_sealed") is True for row in results),
        "failures": [
            {
                "cell_id": row["cell_id"],
                "status": row.get("status"),
                "source_status": row.get("source_status"),
                "failure": row.get("failure"),
            }
            for row in results
            if row.get("status") != "completed"
        ],
        "cells": [
            {
                "cell_id": row["cell_id"],
                "world_id": row["world_id"],
                "arm": row["arm"],
                "status": row.get("status"),
                "source_batches": len(row.get("batches", [])),
                "posttests": len(row.get("posttests", {})),
                "posttest_chain_sealed": row.get("posttest_chain_sealed"),
            }
            for row in results
        ],
    }
    write(root / "summary.json", payload)
    return payload


def validate_execution_repair_evidence(
    provider_calls: Any, repair: Any
) -> None:
    if not isinstance(provider_calls, int) or provider_calls < 1 or not isinstance(repair, Mapping):
        raise RuntimeError("invalid EQ freeze manifest provider-call count")
    if repair.get("provider_api_turn_attempts") != provider_calls:
        raise RuntimeError("invalid EQ execution-repair provider count")
    phase = repair.get("repair_phase")
    if phase == "pre_scientific":
        valid = (
            repair.get("accepted_model_calls") == 0
            and repair.get("scientific_actions") == 0
            and repair.get("source_batches") == 0
            and repair.get("scientific_output_retained") is False
        )
    elif phase == "post_source_pre_truth":
        valid = (
            repair.get("affected_cells") == ["EQ-W01--Opaque"]
            and repair.get("accepted_source_model_calls") == 1
            and repair.get("scientific_actions") == 60
            and repair.get("source_batches") == 12
            and repair.get("source_exact_replay") is True
            and repair.get("completed_posttest_payloads") == 0
            and repair.get("truth_generated") is False
            and repair.get("scientific_contract_changed") is False
            and repair.get("source_rerun_required") is False
        )
    else:
        valid = False
    if not valid:
        raise RuntimeError("invalid EQ execution-repair evidence")


def validate_freeze(root: Path, config: Mapping[str, Any]) -> Mapping[str, Any]:
    if not FREEZE.exists():
        raise RuntimeError("provider remains sealed: EQ freeze manifest is absent")
    freeze = read(FREEZE)
    gate_path = root / "provider-free-gate" / "gate.json"
    if not gate_path.exists():
        raise RuntimeError("provider remains sealed: provider-free gate result is absent")
    gate = read(gate_path)
    if gate.get("passed") is not True:
        raise RuntimeError("provider remains sealed: provider-free gate did not pass")
    if freeze.get("config_sha256") != file_sha256(CONFIG):
        raise RuntimeError("EQ freeze manifest does not bind the current config")
    if gate.get("config_sha256") != file_sha256(CONFIG):
        raise RuntimeError("EQ provider-free gate does not bind the current config")
    if freeze.get("gate_sha256") != file_sha256(gate_path):
        raise RuntimeError("EQ freeze manifest does not bind this provider-free gate")
    if freeze.get("resolved_config_sha256") != digest(config):
        raise RuntimeError("EQ freeze manifest does not bind the resolved config")
    bindings = freeze.get("bindings")
    if not isinstance(bindings, Mapping) or not bindings:
        raise RuntimeError("EQ freeze manifest has no immutable file bindings")
    repository = ROOT.resolve()
    for relative, expected in bindings.items():
        path = (ROOT / str(relative)).resolve()
        if repository not in path.parents or not path.is_file():
            raise RuntimeError(f"invalid or missing EQ freeze binding: {relative}")
        if file_sha256(path) != expected:
            raise RuntimeError(f"EQ freeze binding changed: {relative}")
    provider_calls = freeze.get("provider_calls_before_freeze")
    if provider_calls != 0:
        validate_execution_repair_evidence(
            provider_calls, freeze.get("execution_repair_evidence")
        )
    if freeze.get("status") != "frozen_for_formal_development_execution":
        raise RuntimeError("EQ freeze manifest status is not executable")
    return freeze


def write_design(root: Path, config: Mapping[str, Any], validated: Mapping[str, Any], freeze: Mapping[str, Any]) -> None:
    design = {
        "schema_version": "work-ii-eq-run-design-1.0",
        "config": copy.deepcopy(config),
        "config_sha256": file_sha256(CONFIG),
        "freeze": copy.deepcopy(freeze),
        "schedule": copy.deepcopy(validated["schedule"]),
        "query_sha256": validated["query_sha256"],
        "prior_sha256": copy.deepcopy(validated["prior_sha256"]),
        "provider": copy.deepcopy(PROVIDER),
        "system_prompt": SYSTEM,
        "K1": K1,
        "Q": Q_PROMPT,
        "K2": K2,
        "truth_embargo": config["truth_embargo"],
    }
    path = root / "design.json"
    if path.exists() and read(path) != design:
        raise RuntimeError("existing EQ run design differs from the frozen design")
    write(path, design)


def execute_sources(
    root: Path,
    config: Mapping[str, Any],
    schedule: Sequence[Mapping[str, Any]],
    *,
    workers: int,
) -> list[dict[str, Any]]:
    if not 1 <= workers <= 8:
        raise ValueError("workers must be in 1..8")
    progress: dict[str, Any] = {}
    progress_lock = threading.Lock()
    stop = threading.Event()
    started = time.monotonic()

    def heartbeat() -> None:
        while not stop.wait(30):
            with progress_lock:
                snapshot = copy.deepcopy(progress)
            completed = sum(
                (root / "sources" / cell["cell_id"] / "RESULT.json").exists()
                for cell in schedule
            )
            elapsed = time.monotonic() - started
            print(
                json.dumps(
                    {
                        "stage": "provider_sources",
                        "completed": completed,
                        "total": len(schedule),
                        "workers": workers,
                        "elapsed_s": round(elapsed),
                        "eta_s": round(elapsed / completed * (len(schedule) - completed))
                        if completed
                        else None,
                        "active": snapshot,
                    },
                    default=str,
                ),
                flush=True,
            )

    heartbeat_thread = threading.Thread(target=heartbeat, daemon=True)
    heartbeat_thread.start()
    results = []
    try:
        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = {
                executor.submit(run_cell, root, config, cell, progress, progress_lock): cell
                for cell in schedule
            }
            for future in as_completed(futures):
                cell = futures[future]
                result = future.result()
                results.append(result)
                summary = write_summary(root, validate_design(config)["schedule"], "provider_sources")
                print(
                    json.dumps(
                        {
                            "stage": "cell_complete",
                            "cell_id": cell["cell_id"],
                            "status": result["status"],
                            "completed_sources": summary["completed_sources"],
                            "attempted_sources": summary["attempted_sources"],
                        }
                    ),
                    flush=True,
                )
    finally:
        stop.set()
        heartbeat_thread.join(timeout=2)
    return results


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--scope", choices=("gate", "canary", "full"), required=True)
    parser.add_argument("--workers", type=int, default=1)
    args = parser.parse_args()
    config = load_config()
    validated = validate_design(config)
    configure_provider_helpers(config)
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
    freeze = validate_freeze(root, config)
    write_design(root, config, validated, freeze)
    schedule = validated["schedule"]
    selected = (
        [cell for cell in schedule if cell["world_id"] == "EQ-W01"]
        if args.scope == "canary"
        else schedule
    )
    execute_sources(root, config, selected, workers=args.workers)
    summary = write_summary(root, schedule, "canary_complete" if args.scope == "canary" else "sources_complete")
    if args.scope == "canary":
        if summary["attempted_sources"] < 3:
            raise RuntimeError("EQ canary did not attempt all three W01 arms")
        return
    results = [
        read(root / "sources" / cell["cell_id"] / "RESULT.json")
        for cell in schedule
        if (root / "sources" / cell["cell_id"] / "RESULT.json").exists()
    ]
    if len(results) != 15 or not all(row.get("posttest_chain_sealed") is True for row in results):
        write_summary(root, schedule, "truth_embargoed_incomplete_posttest_chain")
        raise RuntimeError("not all 15 K2 responses are sealed; reference truth remains embargoed")
    truth = generate_truth(root, config)
    for result in results:
        evaluation = evaluate_predictions(
            result["posttests"]["Q"].get("payload"),
            queries(config),
            truth[result["world_id"]],
        )
        write(root / "evaluations" / f"{result['cell_id']}.json", evaluation)
    summary = write_summary(root, schedule, "complete")
    completion = {
        "schema_version": "work-ii-eq-completion-1.0",
        "completed_epoch": time.time(),
        "source_sessions": len(results),
        "source_batches": sum(len(row.get("batches", [])) for row in results),
        "posttests": sum(len(row.get("posttests", {})) for row in results),
        "reference_executions": 300,
        "equilibrium_confidence_used_as_agent_uncertainty_or_score": False,
        "summary_sha256": digest(summary),
    }
    write(root / "completion.json", completion)


if __name__ == "__main__":
    main()
