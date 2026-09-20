#!/usr/bin/env python3
"""Run the canonical K1/Q/K2 EQ-S v0.3 relaunch."""
# ruff: noqa: E402, E501

from __future__ import annotations

import argparse
import copy
import json
import sys
import time
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import scripts.run_work_ii_eq_bounded_equilibrium as eq_v1
import scripts.run_work_ii_eq_bounded_equilibrium_v2 as eq_v2
import scripts.run_work_ii_eq_structural_v0_2 as eq_s_v02

V02_VALIDATE_DESIGN = eq_s_v02.validate_design

CONFIG = ROOT / "configs/benchmark/work_ii_eq_structural_v0.3.json"
FREEZE = ROOT / "configs/benchmark/work_ii_eq_structural_freeze_v0.3.json"
NOTE = ROOT / "workstreams/flagship_tasks/WORK_II_EQ_S_V0_3_CANONICAL_RELAUNCH.md"
TASK = eq_s_v02.TASK
ARMS = eq_s_v02.ARMS
METRICS = eq_s_v02.METRICS
PROVIDER = eq_s_v02.PROVIDER
POSTTEST_STAGES = ("K1", "Q", "K2")
GOALS = copy.deepcopy(eq_s_v02.GOALS)

SYSTEM = eq_s_v02.SYSTEM.replace(
    "A separate same-thread sequence will request K1, twelve blind quantitative predictions, K2, and a\n"
    "structured mechanism supplement. Do not answer those early.",
    "A separate same-thread sequence will request K1, twelve blind quantitative predictions, and K2.\n"
    "Do not answer those early.",
)
K1 = eq_v2.K1
Q_PROMPT = eq_v2.Q_PROMPT
K2 = eq_v2.K2

read = eq_v1.read
write = eq_v1.write
digest = eq_v1.digest
file_sha256 = eq_v1.file_sha256
queries = eq_s_v02.queries
world_by_id = eq_s_v02.world_by_id
public_prior = eq_s_v02.public_prior


def overlay() -> dict[str, Any]:
    payload = read(CONFIG)
    for binding_key in ("base_scientific_design", "canonical_posttest_protocol"):
        binding = payload[binding_key]
        path = ROOT / binding["path"]
        if not path.is_file() or file_sha256(path) != binding["sha256"]:
            raise RuntimeError(f"EQ-S v0.3 binding changed: {binding_key}")
    return payload


def load_config() -> dict[str, Any]:
    relaunch = overlay()
    config = eq_s_v02.load_config()
    config.update(
        {
            "schema_version": relaunch["schema_version"],
            "status": relaunch["status"],
            "execution_authorized": True,
            "provider_execution_authorized": True,
            "protocol": relaunch["canonical_posttest_protocol"]["path"],
            "posttest_stages": list(POSTTEST_STAGES),
            "counts": copy.deepcopy(relaunch["counts"]),
            "truth_embargo": relaunch["execution_policy"]["truth_embargo"],
            "canonical_relaunch": copy.deepcopy(relaunch),
        }
    )
    return config


def validate_design(config: Mapping[str, Any]) -> dict[str, Any]:
    expected = {
        "worlds": 5,
        "independent_source_sessions": 15,
        "source_batches_per_session": 12,
        "source_batches": 180,
        "posttest_stages": ["K1", "Q", "K2"],
        "posttests": 45,
        "reference_repeats_per_query": 5,
        "reference_executions": 300,
    }
    if config.get("counts") != expected:
        raise ValueError("EQ-S v0.3 denominators changed")
    if tuple(config.get("posttest_stages", ())) != POSTTEST_STAGES:
        raise ValueError("EQ-S v0.3 participant posttest chain changed")
    if "EQS" in json.dumps(config["canonical_relaunch"]["participant_posttest_stages"]):
        raise ValueError("closed-set EQS leaked into the participant chain")
    if tuple(config.get("arms", ())) != ARMS or tuple(config.get("prediction_metrics", ())) != METRICS:
        raise ValueError("EQ-S v0.3 arms or metrics changed")

    legacy = copy.deepcopy(dict(config))
    legacy["counts"] = {
        "worlds": 5,
        "independent_source_sessions": 15,
        "source_batches_per_session": 12,
        "source_batches": 180,
        "posttest_stages": ["K1", "Q", "K2", "EQS"],
        "posttests": 60,
        "reference_repeats_per_query": 5,
        "reference_executions": 300,
    }
    legacy["posttest_stages"] = ["K1", "Q", "K2", "EQS"]
    validated = V02_VALIDATE_DESIGN(legacy)
    if "network_family" in K1 or "aqueous_ion_pair_intermediate" in K1:
        raise ValueError("canonical K1 contains a candidate mechanism menu")
    if "network_family" in K2 or "aqueous_ion_pair_intermediate" in K2:
        raise ValueError("canonical K2 contains a candidate mechanism menu")
    return validated


def posttest_schema(stage: str) -> dict[str, Any]:
    if stage not in POSTTEST_STAGES:
        raise ValueError(f"noncanonical participant posttest: {stage}")
    return eq_v1.posttest_schema(stage)


def validate_posttest(
    stage: str,
    payload: Any,
    query_rows: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    if stage not in POSTTEST_STAGES:
        return {"valid": False, "failure": f"noncanonical participant posttest: {stage}"}
    return eq_v1.validate_posttest(stage, payload, query_rows)


def effective_result(root: Path, cell: Mapping[str, Any]) -> tuple[dict[str, Any] | None, Path]:
    original = root / "sources" / cell["cell_id"] / "RESULT.json"
    candidates = [original]
    recovery_root = root / "recoveries" / cell["cell_id"]
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
        "schema_version": "work-ii-eq-s-canonical-summary-0.3",
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
            }
            for result, _ in rows
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


def configure_runtime(config: Mapping[str, Any]) -> None:
    eq_s_v02.CONFIG = CONFIG
    eq_s_v02.SYSTEM = SYSTEM
    eq_s_v02.K1 = K1
    eq_s_v02.Q_PROMPT = Q_PROMPT
    eq_s_v02.K2 = K2
    eq_s_v02.validate_design = validate_design
    eq_s_v02.configure_provider_helpers(config)

    eq_v2.CONFIG = CONFIG
    eq_v2.FREEZE = FREEZE
    eq_v2.SYSTEM = SYSTEM
    eq_v2.K1 = K1
    eq_v2.Q_PROMPT = Q_PROMPT
    eq_v2.K2 = K2
    eq_v2.GOALS = GOALS
    eq_v2.POSTTEST_STAGES = POSTTEST_STAGES
    eq_v2.load_config = load_config
    eq_v2.validate_design = validate_design
    eq_v2.public_prior = public_prior
    eq_v2.queries = queries
    eq_v2.world_by_id = world_by_id
    eq_v2.posttest_schema = posttest_schema
    eq_v2.validate_posttest = validate_posttest
    eq_v2.write_summary = write_summary


def run_provider_free_gate(root: Path, config: Mapping[str, Any]) -> dict[str, Any]:
    report = eq_s_v02.run_provider_free_gate(root, config)
    canonical_checks = {
        "canonical_K1_bound": K1 == eq_v2.K1,
        "canonical_Q_outer_prompt_bound": Q_PROMPT == eq_v2.Q_PROMPT,
        "canonical_K2_bound": K2 == eq_v2.K2,
        "participant_chain_exactly_K1_Q_K2": tuple(config["posttest_stages"]) == POSTTEST_STAGES,
        "closed_set_EQS_absent": "EQS" not in config["posttest_stages"],
        "external_audit_not_participant_prompt": (
            config["canonical_relaunch"]["mechanism_evaluation"]["participant_candidate_labels_exposed"]
            is False
        ),
    }
    report["schema_version"] = "work-ii-eq-s-provider-free-gate-0.3"
    report["canonical_protocol_checks"] = canonical_checks
    report["checks"].update(canonical_checks)
    report["passed"] = all(report["checks"].values())
    write(root / "provider-free-gate" / "gate.json", report)
    return report


def create_freeze(root: Path, config: Mapping[str, Any]) -> dict[str, Any]:
    gate_path = root / "provider-free-gate" / "gate.json"
    if not gate_path.is_file() or read(gate_path).get("passed") is not True:
        raise RuntimeError("cannot freeze EQ-S v0.3 before a passing provider-free gate")
    bindings = [
        "configs/benchmark/work_ii_eq_structural_v0.3.json",
        "configs/benchmark/work_ii_eq_structural_v0.2.repair.design.json",
        "configs/benchmark/work_ii_eq_structural_v0.1.design.json",
        "workstreams/flagship_tasks/WORK_II_CANONICAL_K1_Q_K2_PROTOCOL_V1_1.md",
        "workstreams/flagship_tasks/WORK_II_EQ_S_V0_3_CANONICAL_RELAUNCH.md",
        "src/chemworld/physchem/equilibrium_mechanism.py",
        "src/chemworld/runtime/observation_services.py",
        "src/chemworld/world/world_family.py",
        "scripts/run_work_ii_eq_structural_v0_2.py",
        "scripts/run_work_ii_eq_structural_v0_3.py",
        "scripts/run_work_ii_eq_bounded_equilibrium_v2.py",
        "tests/test_work_ii_eq_structural_v0_2.py",
        "tests/test_work_ii_eq_structural_v0_3.py",
        "tests/test_runtime_view_efficiency.py",
    ]
    freeze = {
        "schema_version": "work-ii-eq-s-freeze-0.3",
        "status": "frozen_for_formal_development_execution",
        "config_path": str(CONFIG.relative_to(ROOT)),
        "config_sha256": file_sha256(CONFIG),
        "resolved_config_sha256": digest(config),
        "gate_path": str(gate_path.relative_to(ROOT)),
        "gate_sha256": file_sha256(gate_path),
        "provider_calls_before_freeze": 0,
        "participant_posttest_stages": list(POSTTEST_STAGES),
        "closed_set_participant_supplement": None,
        "supersedes_without_overwriting": "EQ-S v0.2.1 closed-set pilot",
        "bindings": {relative: file_sha256(ROOT / relative) for relative in bindings},
    }
    write(FREEZE, freeze)
    return freeze


def write_design(
    root: Path,
    config: Mapping[str, Any],
    validated: Mapping[str, Any],
    freeze: Mapping[str, Any],
) -> None:
    design = {
        "schema_version": "work-ii-eq-s-run-design-0.3",
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
        "external_mechanism_audit": copy.deepcopy(
            config["canonical_relaunch"]["mechanism_evaluation"]
        ),
        "truth_embargo": config["truth_embargo"],
    }
    path = root / "design.json"
    if path.exists() and read(path) != design:
        raise RuntimeError("existing EQ-S v0.3 run design differs")
    write(path, design)


def finalize_after_sources(
    root: Path,
    config: Mapping[str, Any],
    schedule: Sequence[Mapping[str, Any]],
) -> None:
    resolved = [effective_result(root, cell) for cell in schedule]
    results = [result for result, _ in resolved if result is not None]
    if len(results) != 15 or not all(row.get("posttest_chain_sealed") is True for row in results):
        write_summary(root, schedule, "truth_embargoed_incomplete_K2_chain")
        raise RuntimeError("not all 15 K2 responses are sealed; truth remains embargoed")
    truth = eq_v1.generate_truth(root, config)
    for result in results:
        evaluation = eq_v1.evaluate_predictions(
            result["posttests"]["Q"].get("payload"),
            queries(config),
            truth[result["world_id"]],
        )
        evaluation["response_shape"] = eq_s_v02.evaluate_structure_predictions(
            result["posttests"]["Q"].get("payload"),
            config,
            truth[result["world_id"]],
        )
        evaluation["mechanism_evaluation"] = {
            "primary_artifact": "K1",
            "status": "sealed_for_external_blind_descriptive_audit",
            "closed_set_participant_classification": None,
        }
        write(root / "evaluations" / f"{result['cell_id']}.json", evaluation)
    summary = write_summary(root, schedule, "complete")
    write(
        root / "completion.json",
        {
            "schema_version": "work-ii-eq-s-completion-0.3",
            "completed_epoch": time.time(),
            "source_sessions": 15,
            "source_batches": sum(len(row.get("batches", [])) for row in results),
            "posttests": sum(len(row.get("posttests", {})) for row in results),
            "participant_posttest_stages": list(POSTTEST_STAGES),
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
    configure_runtime(config)
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
        print(json.dumps(write_summary(root, validated["schedule"], "status")), flush=True)
        return

    freeze = eq_v2.validate_freeze(root, config)
    write_design(root, config, validated, freeze)
    schedule = validated["schedule"]
    canary = [cell for cell in schedule if cell["world_id"] == "EQ-S-W01"]
    if args.scope == "canary":
        if not 1 <= args.workers <= 3:
            raise ValueError("EQ-S v0.3 canary workers must be in 1..3")
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
            raise ValueError("EQ-S v0.3 remaining workers must be in 1..8")
        selected = [
            cell
            for cell in schedule
            if cell["world_id"] != "EQ-S-W01" and effective_result(root, cell)[0] is None
        ]
    if selected:
        eq_v2.execute_sources(root, config, selected, workers=args.workers)
    summary = write_summary(
        root,
        schedule,
        "canary_complete" if args.scope == "canary" else "sources_complete",
    )
    if args.scope == "canary":
        if summary["completed_sources"] < 3:
            raise RuntimeError("EQ-S v0.3 canary did not complete all three K1/Q/K2 chains")
        return
    finalize_after_sources(root, config, schedule)


if __name__ == "__main__":
    main()
