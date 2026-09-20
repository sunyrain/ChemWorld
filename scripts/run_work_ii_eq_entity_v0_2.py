#!/usr/bin/env python3
"""Run the approved five-world EQ-E v0.2 characterization block."""
# ruff: noqa: E402, E501

from __future__ import annotations

import argparse
import copy
import json
import math
import subprocess
import sys
import time
from collections.abc import Mapping, Sequence
from pathlib import Path
from statistics import fmean
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import scripts.run_work_ii_eq_bounded_equilibrium as eq_runtime
import scripts.run_work_ii_eq_bounded_equilibrium_v2 as canonical
import scripts.run_work_ii_eq_entity_design_gate_v0_2 as design_gate

CONFIG = ROOT / "configs/benchmark/work_ii_eq_entity_v0.2.execution.json"
FREEZE = ROOT / "configs/benchmark/work_ii_eq_entity_freeze_v0.2.json"
TASK = "equilibrium-characterization"
ARMS = design_gate.ARMS
METRICS = design_gate.METRICS
POSTTEST_STAGES = ("K1", "Q", "K2")

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
        "Characterize how each of three selectable anonymous aqueous-medium identities changes "
        "the coupled weak-acid/direct-precipitation response. Determine which entity-conditioned "
        "relationships transfer across concentration and scale, test any supplied qualitative "
        "mapping against observations, and state evidence boundaries and competing explanations. "
        "This is mechanism characterization and entity mapping, not medium ranking or optimization."
    )
}

SYSTEM = """You are an autonomous scientist in a simulated bounded aqueous-equilibrium laboratory.
Use only the supplied chemworld_lab tools and public_numerics calculator. No filesystem, network,
repository inspection, external retrieval, or hidden-simulator access is allowed. Complete exactly
12 independent experimental batches; repetition is allowed. Three anonymous selectable aqueous media
are available as solvent codes 0, 1, and 2. Use exactly one medium identity in each batch; repeated
additions of that same medium are allowed, but different media cannot be mixed inside one batch.

All media share the public reaction background HA(aq) <=> H+(aq) + A-(aq) and
M+(aq) + A-(aq) <=> MA(s). Medium identity may change a joint bundle of effective ionization,
solid-formation, cation-availability, and activity properties. Characterize the local entity-response
map and its transfer across loading and scale. This is not a request to choose the best medium, rank a
process score, or infer a different reaction-network family. A supplied qualitative entity dossier may
be incomplete or inaccurate; public observations are authoritative.

You have at most 12 non-final instrument uses plus 12 final assays. Choose legal medium, volume,
reagent amount, replication, and measurements autonomously. pH_normalized is pH/14;
acid_dissociation_fraction is the bounded free-conjugate-base fraction; precipitation_signal is a
bounded solid proxy. Numerical residual and equilibrium_confidence are environment diagnostics, not
your uncertainty or a task score. Do not optimize them. For every batch explicitly terminate and then
measure final_assay. Continue with next_state until campaign_ended is true. After the twelfth batch,
commit the completed batch that is the most useful evidentiary anchor with a short English rationale;
this is not an optimum claim. Then return the required concise English status JSON. A separate
same-thread sequence will request K1, twelve blind quantitative predictions, and K2. Do not answer
those early. No particular conclusion is required.
"""

K1 = canonical.K1
Q_PROMPT = canonical.Q_PROMPT
K2 = canonical.K2

read = eq_runtime.read
write = eq_runtime.write
digest = eq_runtime.digest
file_sha256 = eq_runtime.file_sha256
deterministic_seed = eq_runtime.deterministic_seed


def _bound_file(binding: Mapping[str, Any], label: str) -> Path:
    path = ROOT / str(binding["path"])
    if not path.is_file() or file_sha256(path) != binding["sha256"]:
        raise RuntimeError(f"EQ-E v0.2 binding changed: {label}")
    return path


def _entity_intervention(world: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "kind": "equilibrium_entity_panel",
        "version": "eq-e-v0.2",
        "base_pka": float(world["base_pka_nuisance"]),
        "profiles": copy.deepcopy(list(world["profiles"])),
    }


def load_config() -> dict[str, Any]:
    execution = read(CONFIG)
    design_path = _bound_file(execution["base_design"], "base_design")
    _bound_file(execution["canonical_posttest_protocol"], "canonical_posttest_protocol")
    _bound_file(execution["formal_design_note"], "formal_design_note")
    if execution.get("execution_authorized") is not True:
        raise RuntimeError("EQ-E v0.2 execution is not authorized")
    if execution.get("provider_execution_authorized") is not True:
        raise RuntimeError("EQ-E v0.2 provider execution remains sealed")
    config = read(design_path)
    if config.get("provider_execution_authorized") is not False:
        raise RuntimeError("EQ-E base design must remain provider sealed")
    runtime = execution["runtime"]
    worlds = []
    for source in config["worlds"]:
        world = copy.deepcopy(source)
        world["world_interventions"] = [_entity_intervention(source)]
        worlds.append(world)
    config.update(
        {
            "schema_version": execution["schema_version"],
            "status": execution["status"],
            "execution_authorized": True,
            "provider_execution_authorized": True,
            "provider_calls_authorized": None,
            "world_split": runtime["world_split"],
            "objective_runtime": runtime["objective"],
            "posttest_stages": list(runtime["posttest_stages"]),
            "truth_embargo": runtime["truth_embargo"],
            "worlds": worlds,
            "execution_overlay": execution,
        }
    )
    return config


def queries(config: Mapping[str, Any]) -> list[dict[str, Any]]:
    return design_gate.queries(config)


def world_by_id(config: Mapping[str, Any], world_id: str) -> Mapping[str, Any]:
    for world in config["worlds"]:
        if world["world_id"] == world_id:
            return world
    raise KeyError(world_id)


def public_prior(
    config: Mapping[str, Any], world_id: str, arm: str
) -> dict[str, Any] | None:
    return design_gate.public_prior(config, world_by_id(config, world_id), arm)


def research_brief() -> dict[str, Any]:
    return {
        "schema_version": "chemworld-research-brief-0.1",
        "card": "EQ",
        "prior_record": None,
    }


def validate_design(config: Mapping[str, Any]) -> dict[str, Any]:
    validated = design_gate.validate_design(config)
    if tuple(config.get("posttest_stages", ())) != POSTTEST_STAGES:
        raise ValueError("EQ-E participant chain must be exactly K1/Q/K2")
    if config.get("execution_authorized") is not True:
        raise ValueError("EQ-E execution authorization missing")
    schedule = []
    for row in validated["schedule"]:
        world = world_by_id(config, str(row["world_id"]))
        schedule.append(
            {
                **copy.deepcopy(row),
                "world_seed": int(world["world_seed"]),
                "world_interventions": copy.deepcopy(world["world_interventions"]),
            }
        )
    if any(token in SYSTEM for token in ("Q01", "0.005 M", "0.600 M")):
        raise ValueError("EQ-E source prompt leaks Q coordinates")
    if any(token in SYSTEM for token in ("pka_shift", "log10_ksp", "cation_fraction")):
        raise ValueError("EQ-E source prompt leaks private entity properties")
    if K1 != canonical.K1 or Q_PROMPT != canonical.Q_PROMPT or K2 != canonical.K2:
        raise ValueError("EQ-E canonical K1/Q/K2 prompt binding drifted")
    return {
        **validated,
        "schedule": schedule,
    }


def configure_runtime(config: Mapping[str, Any]) -> None:
    eq_runtime.CONFIG = CONFIG
    eq_runtime.FREEZE = FREEZE
    eq_runtime.TASK = TASK
    eq_runtime.ARMS = ARMS
    eq_runtime.METRICS = METRICS
    eq_runtime.PROVIDER = PROVIDER
    eq_runtime.GOALS = GOALS
    eq_runtime.SYSTEM = SYSTEM
    eq_runtime.K1 = K1
    eq_runtime.Q_PROMPT = Q_PROMPT
    eq_runtime.K2 = K2
    eq_runtime.load_config = load_config
    eq_runtime.queries = queries
    eq_runtime.world_by_id = world_by_id
    eq_runtime.public_prior = public_prior
    eq_runtime.research_brief = research_brief
    eq_runtime.validate_design = validate_design
    eq_runtime.write_summary = write_summary
    eq_runtime.configure_provider_helpers(config)


def run_provider_free_gate(root: Path, config: Mapping[str, Any]) -> dict[str, Any]:
    gate_root = root / "provider-free-gate"
    report_path = gate_root / "gate.json"
    if report_path.exists():
        return read(report_path)
    direct = design_gate.run_gate(root / "provider-free-direct-design-gate")
    query_rows = queries(config)
    actions = [action for query in query_rows for action in query["actions"]]
    schedule = validate_design(config)["schedule"]
    executions: dict[str, list[dict[str, Any]]] = {}
    replay_passes = 0
    started = time.monotonic()
    for index, cell in enumerate(schedule, 1):
        world = world_by_id(config, str(cell["world_id"]))
        result = eq_runtime.reference_run(
            gate_root / "runs" / str(cell["cell_id"]),
            actions,
            config=config,
            world=world,
            batches=12,
            observation_seed=deterministic_seed(
                "eq-e-v0.2-integrated-gate", world["world_id"]
            ),
            observation_namespace=f"work-ii-eq-e-gate-{str(world['world_id']).lower()}",
        )
        if result["failure"] or result["rollbacks"] or len(result["batches"]) != 12:
            raise RuntimeError(f"EQ-E integrated gate failed: {cell['cell_id']}")
        replay_passes += result["exact_replay"].get("verified") is True
        executions[str(cell["cell_id"])] = result["batches"]
        elapsed = time.monotonic() - started
        print(
            json.dumps(
                {
                    "stage": "eq_e_integrated_provider_free_gate",
                    "completed_campaigns": index,
                    "total_campaigns": 15,
                    "completed_batches": index * 12,
                    "total_batches": 180,
                    "eta_s": round(elapsed / index * (15 - index)),
                }
            ),
            flush=True,
        )

    arm_identity = all(
        len(
            {
                digest(executions[f"{world['world_id']}--{arm}"][query_index]["metrics"])
                for arm in ARMS
            }
        )
        == 1
        for world in config["worlds"]
        for query_index in range(12)
    )
    checks = {
        "provider_calls_zero": True,
        "direct_design_gate_passed": direct.get("passed") is True,
        "fifteen_campaigns_180_batches": len(executions) == 15
        and sum(len(rows) for rows in executions.values()) == 180,
        "exact_replay": replay_passes == 15,
        "full_environment_entity_panel_reachable": all(
            all(metric in batch["metrics"] for metric in METRICS)
            for rows in executions.values()
            for batch in rows
        ),
        "arm_physics_and_noise_identity": arm_identity,
        "canonical_K1_Q_K2_only": tuple(config["posttest_stages"]) == POSTTEST_STAGES,
        "fixed_direct_topology": all(
            world["world_interventions"][0]["kind"] == "equilibrium_entity_panel"
            for world in config["worlds"]
        ),
        "numeric_stability": all(
            math.isfinite(float(batch["metrics"][metric]))
            and 0.0 <= float(batch["metrics"][metric]) <= 1.0
            for rows in executions.values()
            for batch in rows
            for metric in METRICS
        ),
    }
    report = {
        "schema_version": "work-ii-eq-e-integrated-provider-free-gate-0.2",
        "passed": all(checks.values()),
        "provider_calls": 0,
        "completed_campaigns": len(executions),
        "completed_batches": sum(len(rows) for rows in executions.values()),
        "exact_replay_campaigns": replay_passes,
        "checks": checks,
        "config_sha256": file_sha256(CONFIG),
        "resolved_config_sha256": digest(config),
        "base_design_sha256": file_sha256(design_gate.CONFIG),
        "direct_design_gate_sha256": file_sha256(
            root / "provider-free-direct-design-gate" / "gate.json"
        ),
        "query_sha256": digest(query_rows),
        "cell_metric_sha256": {
            cell_id: digest([batch["metrics"] for batch in rows])
            for cell_id, rows in executions.items()
        },
    }
    write(report_path, report)
    lines = [
        "# EQ-E v0.2 integrated provider-free gate",
        "",
        f"Status: **{'PASS' if report['passed'] else 'FAIL'}**. Provider calls: 0.",
        "",
        f"Completed {report['completed_campaigns']}/15 campaigns and {report['completed_batches']}/180 batches; exact replay {replay_passes}/15.",
        "",
        "| Check | Pass |",
        "|---|---|",
        *[f"| {name} | {'yes' if passed else 'no'} |" for name, passed in checks.items()],
        "",
        "This integrated gate qualifies the real Agent-facing entity-panel runtime; it makes no provider call.",
        "",
    ]
    (gate_root / "GATE_REPORT.md").write_text("\n".join(lines), encoding="utf-8")
    return report


def _git_revision() -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip()


def create_freeze(root: Path, config: Mapping[str, Any]) -> dict[str, Any]:
    gate_path = root / "provider-free-gate" / "gate.json"
    if not gate_path.is_file() or read(gate_path).get("passed") is not True:
        raise RuntimeError("cannot freeze EQ-E before the integrated provider-free gate passes")
    bindings = [
        "configs/benchmark/work_ii_eq_entity_v0.2.design.json",
        "configs/benchmark/work_ii_eq_entity_v0.2.execution.json",
        "workstreams/flagship_tasks/WORK_II_CANONICAL_K1_Q_K2_PROTOCOL_V1_1.md",
        "workstreams/flagship_tasks/WORK_II_EQ_E_V0_2_FORMAL_DESIGN.md",
        "src/chemworld/physchem/equilibrium_entity_panel.py",
        "src/chemworld/physchem/equilibrium_mechanism.py",
        "src/chemworld/world/equilibrium_entity.py",
        "src/chemworld/world/scenario.py",
        "src/chemworld/runtime/observation_services.py",
        "src/chemworld/operation_validator.py",
        "scripts/run_work_ii_eq_entity_design_gate_v0_2.py",
        "scripts/run_work_ii_eq_entity_v0_2.py",
        "scripts/run_work_ii_eq_bounded_equilibrium.py",
        "scripts/run_work_ii_eq_bounded_equilibrium_v2.py",
        "tests/test_work_ii_eq_entity_design_gate_v0_2.py",
    ]
    freeze = {
        "schema_version": "work-ii-eq-e-freeze-0.2",
        "status": "frozen_for_formal_development_execution",
        "source_revision": _git_revision(),
        "config_path": str(CONFIG.relative_to(ROOT)),
        "config_sha256": file_sha256(CONFIG),
        "resolved_config_sha256": digest(config),
        "gate_path": str(gate_path.relative_to(ROOT)),
        "gate_sha256": file_sha256(gate_path),
        "provider_calls_before_freeze": 0,
        "participant_posttest_stages": list(POSTTEST_STAGES),
        "bindings": {relative: file_sha256(ROOT / relative) for relative in bindings},
    }
    if FREEZE.exists() and read(FREEZE) != freeze:
        raise RuntimeError("existing EQ-E freeze differs from the approved execution surface")
    write(FREEZE, freeze)
    return freeze


def validate_freeze(root: Path, config: Mapping[str, Any]) -> Mapping[str, Any]:
    if not FREEZE.is_file():
        raise RuntimeError("provider remains sealed: EQ-E freeze manifest is absent")
    freeze = read(FREEZE)
    gate_path = root / "provider-free-gate" / "gate.json"
    if not gate_path.is_file() or read(gate_path).get("passed") is not True:
        raise RuntimeError("provider remains sealed: EQ-E integrated gate is absent or failed")
    if freeze.get("config_sha256") != file_sha256(CONFIG):
        raise RuntimeError("EQ-E freeze does not bind the execution config")
    if freeze.get("resolved_config_sha256") != digest(config):
        raise RuntimeError("EQ-E freeze does not bind the resolved config")
    if freeze.get("gate_sha256") != file_sha256(gate_path):
        raise RuntimeError("EQ-E freeze does not bind this integrated gate")
    if freeze.get("provider_calls_before_freeze") != 0:
        raise RuntimeError("EQ-E freeze must precede every provider call")
    if freeze.get("participant_posttest_stages") != list(POSTTEST_STAGES):
        raise RuntimeError("EQ-E freeze participant chain changed")
    bindings = freeze.get("bindings")
    if not isinstance(bindings, Mapping) or not bindings:
        raise RuntimeError("EQ-E freeze has no immutable bindings")
    repository = ROOT.resolve()
    for relative, expected in bindings.items():
        path = (ROOT / str(relative)).resolve()
        if repository not in path.parents or not path.is_file() or file_sha256(path) != expected:
            raise RuntimeError(f"EQ-E freeze binding changed or is missing: {relative}")
    return freeze


def effective_result(
    root: Path, cell: Mapping[str, Any]
) -> tuple[dict[str, Any] | None, Path]:
    original = root / "sources" / str(cell["cell_id"]) / "RESULT.json"
    candidates = [original]
    recovery_root = root / "recoveries" / str(cell["cell_id"])
    if recovery_root.is_dir():
        candidates.extend(sorted(recovery_root.glob("attempt-*/RESULT.json"), reverse=True))
    fallback: tuple[dict[str, Any] | None, Path] = (None, original)
    for path in candidates:
        if not path.is_file():
            continue
        payload = read(path)
        if fallback[0] is None:
            fallback = (payload, path)
        if payload.get("status") == "completed" and payload.get("posttest_chain_sealed") is True:
            return payload, path
    return fallback


def write_summary(
    root: Path,
    schedule: Sequence[Mapping[str, Any]],
    phase: str,
) -> dict[str, Any]:
    resolved = [effective_result(root, cell) for cell in schedule]
    rows = [(result, path) for result, path in resolved if result is not None]
    payload = {
        "schema_version": "work-ii-eq-e-summary-0.2",
        "phase": phase,
        "planned_sources": 15,
        "planned_source_batches": 180,
        "planned_posttests": 45,
        "attempted_sources": len(rows),
        "completed_sources": sum(result.get("status") == "completed" for result, _ in rows),
        "completed_source_batches": sum(len(result.get("batches", [])) for result, _ in rows),
        "sealed_posttests": sum(len(result.get("posttests", {})) for result, _ in rows),
        "sealed_posttest_chains": sum(
            result.get("posttest_chain_sealed") is True for result, _ in rows
        ),
        "failures": [
            {
                "cell_id": result["cell_id"],
                "status": result.get("status"),
                "source_status": result.get("source_status"),
                "failure": result.get("failure"),
                "effective_result": str(path.relative_to(root)),
            }
            for result, path in rows
            if result.get("status") != "completed"
        ],
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
                "posttest_chain_sealed": result.get("posttest_chain_sealed"),
                "effective_result": str(path.relative_to(root)),
            }
            for result, path in rows
        ],
    }
    write(root / "summary.json", payload)
    return payload


def write_design(
    root: Path,
    config: Mapping[str, Any],
    validated: Mapping[str, Any],
    freeze: Mapping[str, Any],
) -> None:
    payload = {
        "schema_version": "work-ii-eq-e-run-design-0.2",
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
        "participant_posttest_stages": list(POSTTEST_STAGES),
        "truth_embargo": config["truth_embargo"],
    }
    path = root / "design.json"
    if path.exists() and read(path) != payload:
        raise RuntimeError("existing EQ-E run design differs from the freeze")
    write(path, payload)


def evaluate_entity_predictions(
    payload: Any,
    config: Mapping[str, Any],
    truth: Mapping[str, Sequence[Mapping[str, float]]],
) -> dict[str, Any]:
    validation = eq_runtime.validate_posttest("Q", payload, queries(config))
    if not validation["valid"]:
        return validation
    prediction = {
        row["query_id"]: row["metrics"] for row in payload["predictions"]
    }
    truth_mean = {
        query_id: {
            metric: fmean(float(row[metric]) for row in repeats)
            for metric in METRICS
        }
        for query_id, repeats in truth.items()
    }
    by_id = {row["query_id"]: row for row in queries(config)}
    primary = [row for row in queries(config) if float(row["volume_L"]) == 0.024]
    contrast_errors = []
    for concentration in (0.005, 0.08, 0.6):
        ids = [
            row["query_id"]
            for row in primary
            if math.isclose(float(row["concentration_M"]), concentration)
        ]
        metric_errors = []
        for metric in METRICS:
            predicted = [float(prediction[item][metric]["estimate"]) for item in ids]
            observed = [float(truth_mean[item][metric]) for item in ids]
            predicted_spans = [predicted[right] - predicted[left] for left in range(3) for right in range(left + 1, 3)]
            observed_spans = [observed[right] - observed[left] for left in range(3) for right in range(left + 1, 3)]
            metric_errors.extend(
                abs(a - b) for a, b in zip(predicted_spans, observed_spans, strict=True)
            )
        contrast_errors.append(
            {"concentration_M": concentration, "pairwise_contrast_mae": fmean(metric_errors)}
        )
    scale_errors = []
    for selector in range(3):
        small = next(
            row["query_id"]
            for row in queries(config)
            if row["selector"] == selector
            and math.isclose(float(row["volume_L"]), 0.024)
            and math.isclose(float(row["concentration_M"]), 0.08)
        )
        large = next(
            row["query_id"]
            for row in queries(config)
            if row["selector"] == selector and math.isclose(float(row["volume_L"]), 0.048)
        )
        errors = []
        for metric in METRICS:
            predicted_gap = float(prediction[large][metric]["estimate"]) - float(
                prediction[small][metric]["estimate"]
            )
            truth_gap = float(truth_mean[large][metric]) - float(truth_mean[small][metric])
            errors.append(abs(predicted_gap - truth_gap))
        scale_errors.append({"selector": selector, "scale_gap_mae": fmean(errors)})
    return {
        "valid": True,
        "entity_contrast": contrast_errors,
        "same_concentration_scale_transfer": scale_errors,
        "query_coordinates_sha256": digest(by_id),
    }


def finalize_after_sources(
    root: Path,
    config: Mapping[str, Any],
    schedule: Sequence[Mapping[str, Any]],
) -> None:
    resolved = [effective_result(root, cell) for cell in schedule]
    results = [result for result, _ in resolved if result is not None]
    if len(results) != 15 or not all(
        row.get("status") == "completed" and row.get("posttest_chain_sealed") is True
        for row in results
    ):
        write_summary(root, schedule, "truth_embargoed_incomplete_K2_chain")
        raise RuntimeError("not all 15 K2 responses are sealed; truth remains embargoed")
    truth = eq_runtime.generate_truth(root, config)
    for result in results:
        evaluation = eq_runtime.evaluate_predictions(
            result["posttests"]["Q"].get("payload"),
            queries(config),
            truth[result["world_id"]],
        )
        evaluation["entity_mapping"] = evaluate_entity_predictions(
            result["posttests"]["Q"].get("payload"),
            config,
            truth[result["world_id"]],
        )
        write(root / "evaluations" / f"{result['cell_id']}.json", evaluation)
    summary = write_summary(root, schedule, "complete")
    write(
        root / "completion.json",
        {
            "schema_version": "work-ii-eq-e-completion-0.2",
            "completed_epoch": time.time(),
            "source_sessions": 15,
            "source_batches": sum(len(row.get("batches", [])) for row in results),
            "posttests": sum(len(row.get("posttests", {})) for row in results),
            "reference_executions": 300,
            "participant_posttest_stages": list(POSTTEST_STAGES),
            "operation_recommendation_applicable": False,
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
    configure_runtime(config)
    root = args.output.resolve()
    root.mkdir(parents=True, exist_ok=True)
    if args.scope == "gate":
        report = run_provider_free_gate(root, config)
        print(
            json.dumps(
                {
                    "stage": "eq_e_integrated_provider_free_gate_complete",
                    "passed": report["passed"],
                    "campaigns": report["completed_campaigns"],
                    "batches": report["completed_batches"],
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
        print(json.dumps(write_summary(root, validated["schedule"], "status")), flush=True)
        return
    freeze = validate_freeze(root, config)
    write_design(root, config, validated, freeze)
    schedule = validated["schedule"]
    canary = [cell for cell in schedule if cell["world_id"] == "EQ-E-W01"]
    if args.scope == "canary":
        if not 1 <= args.workers <= 3:
            raise ValueError("EQ-E canary workers must be in 1..3")
        selected = [cell for cell in canary if effective_result(root, cell)[0] is None]
    else:
        canary_results = [effective_result(root, cell)[0] for cell in canary]
        if not all(
            result is not None
            and result.get("status") == "completed"
            and result.get("posttest_chain_sealed") is True
            for result in canary_results
        ):
            raise RuntimeError("remaining EQ-E matrix is sealed until all W01 canary chains complete")
        if not 1 <= args.workers <= 8:
            raise ValueError("EQ-E remaining workers must be in 1..8")
        selected = [
            cell
            for cell in schedule
            if cell["world_id"] != "EQ-E-W01" and effective_result(root, cell)[0] is None
        ]
    if selected:
        eq_runtime.execute_sources(root, config, selected, workers=args.workers)
    summary = write_summary(
        root,
        schedule,
        "canary_complete" if args.scope == "canary" else "sources_complete",
    )
    if args.scope == "canary":
        if summary["completed_sources"] < 3:
            raise RuntimeError("EQ-E canary did not complete all three K1/Q/K2 chains")
        return
    finalize_after_sources(root, config, schedule)


if __name__ == "__main__":
    main()
