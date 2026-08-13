#!/usr/bin/env python3
"""Run provider-free partition constitutive functional-form A-S seed-0 Q0."""

from __future__ import annotations

import argparse
import json
import math
from collections.abc import Mapping, Sequence
from pathlib import Path
from time import perf_counter
from typing import Any

from chemworld.data.logging import load_jsonl
from chemworld.eval.provenance import canonical_json_sha256, file_sha256, write_json_atomic
from chemworld.eval.runner import run_agent
from chemworld.eval.verify import verify_records
from chemworld.eval.work_ii_execution_mode import (
    ExecutionMode,
    WorkIIExecutionContext,
    build_execution_envelope,
    prepare_execution_context,
)
from chemworld.eval.work_ii_partition_constitutive_q0 import (
    BASELINE_EXPONENT,
    INSTRUMENTS,
    LAW_IDS,
    METRICS,
    NOMINAL_IDENTITIES,
    NOMINAL_PAIR_AQUEOUS_VOLUME_L,
    NOMINAL_PAIR_EXTRACTANT_VOLUME_L,
    NOMINAL_PAIR_QUALIFICATION_VERSION,
    NOMINAL_PAIR_SOLVENT_VOLUME_L,
    NOMINAL_PAIR_SUMMARY_VERSION,
    NOMINAL_PAIR_TASK_REPORT_VERSION,
    POWER_RESPONSE_EXPONENT,
    QUALIFICATION_VERSION,
    SUMMARY_VERSION,
    TASK_ID,
    TASK_REPORT_VERSION,
    WORLD_SEED,
    analyze,
    analyze_nominal_pairs,
    constitutive_intervention,
    frozen_action_plan,
    frozen_nominal_pair_action_plan,
    noise_coordinate,
    nominal_pair_noise_coordinate,
    nominal_pair_observation_binding,
    observation_binding,
    registered_cells,
    registered_nominal_pair_cells,
    summary_sha256,
    task_report_sha256,
    validate_nominal_pair_summary,
    validate_nominal_pair_task_report,
    validate_summary,
    validate_task_report,
)
from chemworld.eval.work_ii_truth import _FrozenTruthReplayAgent
from chemworld.tasks import get_task
from chemworld.world.mechanism_family import MechanismFamilyIntervention
from chemworld.world.scenario import DefaultScenarioGenerator, get_scenario
from chemworld.world.scoring import PARTITION_S0_EXTRACTION_EFFICIENCY_V3

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_ROOT = (
    ROOT / "runs/development/work-ii-partition-nominal-pair-q0-seed0-20260812"
)
RELEASE_OUTPUT_ROOT = ROOT / "runs/release/work-ii-partition-nominal-pair-q0"
DEFAULT_SUMMARY = (
    ROOT
    / "workstreams/flagship_tasks/reports/"
    / "work-ii-partition-nominal-pair-q0-seed0-20260812.json"
)
RELEASE_SUMMARY = (
    ROOT
    / "workstreams/flagship_tasks/reports/"
    / "work-ii-partition-release-nominal-pair-q0.json"
)
TOTAL_EXECUTIONS = len(registered_cells()) * len(LAW_IDS)
NOMINAL_PAIR_TOTAL_EXECUTIONS = len(registered_nominal_pair_cells()) * len(LAW_IDS)


def compile_actions(cell: Mapping[str, Any]) -> list[dict[str, Any]]:
    return frozen_action_plan(cell)


def compile_nominal_pair_actions(cell: Mapping[str, Any]) -> list[dict[str, Any]]:
    return frozen_nominal_pair_action_plan(cell)


def constitutive_audit() -> dict[str, Any]:
    intervention = MechanismFamilyIntervention.from_dict(constitutive_intervention())
    generator = DefaultScenarioGenerator()
    scenario = get_scenario(TASK_ID)
    baseline = generator.generate(scenario, WORLD_SEED)
    power = generator.generate(scenario, WORLD_SEED, (intervention.to_dict(),))
    repeated = generator.generate(scenario, WORLD_SEED, (intervention.to_dict(),))
    baseline_domain = dict(baseline.parameters.domain_parameters)
    power_domain = dict(power.parameters.domain_parameters)
    changed_keys = sorted(
        key
        for key in set(baseline_domain) | set(power_domain)
        if baseline_domain.get(key) != power_domain.get(key)
    )
    task_contract_hash = get_task(TASK_ID).contract_hash
    return {
        "baseline_mechanism_hash": baseline.compiled_mechanism.mechanism_hash,
        "power_response_mechanism_hash": power.compiled_mechanism.mechanism_hash,
        "reaction_network_unchanged": (
            baseline.compiled_mechanism.to_dict() == power.compiled_mechanism.to_dict()
        ),
        "baseline_public_task_contract_hash": task_contract_hash,
        "power_response_public_task_contract_hash": task_contract_hash,
        "public_contract_unchanged": (
            get_task(TASK_ID).contract_hash == task_contract_hash
        ),
        "baseline_exponent": baseline.parameters.domain_parameter(
            "partition_coefficient_exponent"
        ),
        "power_response_exponent": power.parameters.domain_parameter(
            "partition_coefficient_exponent"
        ),
        "changed_domain_parameter_keys": changed_keys,
        "only_registered_constitutive_parameter_changed": (
            changed_keys == ["partition_coefficient_exponent"]
        ),
        "power_response_intervention_hash": power.initial_state.metadata.get(
            "mechanism_family_intervention_hash"
        ),
        "intervention_binding_deterministic": (
            power.initial_state.metadata.get("mechanism_family_intervention_hash")
            == repeated.initial_state.metadata.get("mechanism_family_intervention_hash")
        ),
        "execution_constitutive_binding_matches": False,
    }


def _measurement(
    records: Sequence[Mapping[str, Any]], instrument: str
) -> tuple[dict[str, float], dict[str, bool]]:
    candidates = [
        row
        for row in records
        if row.get("transaction_status") == "committed"
        and row.get("operation_type") == "measure"
        and row.get("instrument") == instrument
    ]
    if (instrument == "hplc" and len(candidates) != 2) or (
        instrument == "final_assay" and len(candidates) != 1
    ):
        raise ValueError(f"trajectory has the wrong {instrument} denominator")
    selected = candidates[-1]
    estimate = selected.get("processed_estimate")
    observed = selected.get("observed_mask")
    if not isinstance(estimate, Mapping) or not isinstance(observed, Mapping):
        raise ValueError(f"{instrument} lacks processed estimates or observed mask")
    values: dict[str, float] = {}
    mask: dict[str, bool] = {}
    for metric in METRICS:
        value = estimate.get(metric)
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise ValueError(f"{instrument} lacks finite {metric}")
        number = float(value)
        if not math.isfinite(number):
            raise ValueError(f"{instrument} {metric} is not finite")
        values[metric] = number
        mask[metric] = observed.get(metric) is True
    return values, mask


def _visible_leakage_matches(records: Sequence[Mapping[str, Any]]) -> list[str]:
    tokens = (
        "mechanism_family",
        "world_intervention",
        "private_seed",
        "hidden_state",
        "evaluator_truth",
    )
    matches = set()
    for row in records:
        public = {
            key: row.get(key)
            for key in (
                "observation",
                "observed_mask",
                "processed_estimate",
                "raw_signal",
                "agent_visible_observation",
                "agent_view",
            )
        }
        rendered = json.dumps(public, ensure_ascii=False, sort_keys=True)
        matches.update(token for token in tokens if token in rendered)
    return sorted(matches)


def execute(
    *,
    cell: Mapping[str, Any],
    law_id: str,
    output_root: Path,
    nominal_pair: bool = False,
) -> dict[str, Any]:
    actions = (
        compile_nominal_pair_actions(cell) if nominal_pair else compile_actions(cell)
    )
    action_hash = canonical_json_sha256(actions)
    observation_seed, namespace = (
        nominal_pair_observation_binding(str(cell["cell_id"]))
        if nominal_pair
        else observation_binding(str(cell["cell_id"]))
    )
    noise_coordinates = {
        instrument: (
            nominal_pair_noise_coordinate(str(cell["cell_id"]), instrument)
            if nominal_pair
            else noise_coordinate(str(cell["cell_id"]), instrument)
        )
        for instrument in INSTRUMENTS
    }
    interventions = [] if law_id == LAW_IDS[0] else [constitutive_intervention()]
    law_root = output_root / str(cell["cell_id"]) / law_id
    law_root.mkdir(parents=True, exist_ok=False)
    trajectory = law_root / "trajectory.jsonl"
    started = perf_counter()
    records: list[dict[str, Any]] = []
    replay: dict[str, Any] | None = None
    failure: dict[str, str] | None = None
    physical_failure: dict[str, Any] | None = None
    measurements: dict[str, dict[str, float]] | None = None
    masks: dict[str, dict[str, bool]] | None = None
    noise_keys: dict[str, str] | None = None
    safe: bool | None = None
    leakage: list[str] = []
    try:
        run_agent(
            env_id=get_task(TASK_ID).env_id,
            agent=_FrozenTruthReplayAgent(actions),
            world_split=str(get_task(TASK_ID).world_split),
            budget=len(actions),
            objective="balanced",
            seed=WORLD_SEED,
            agent_seed=0,
            observation_seed=observation_seed,
            task_id=TASK_ID,
            output_path=trajectory,
            budget_override=len(actions),
            episode_mode_override="single_experiment",
            observation_noise_mode="keyed",
            observation_noise_namespace=namespace,
            scoring_contract_id=PARTITION_S0_EXTRACTION_EFFICIENCY_V3,
            world_interventions=interventions,
        )
        records = load_jsonl(trajectory)
        noncommitted = [row for row in records if row.get("transaction_status") != "committed"]
        if noncommitted:
            if all(row.get("rollback_reason") == "constitution_failed" for row in noncommitted):
                physical_failure = {
                    "rollback_count": len(noncommitted),
                    "attribution": "protocol_owned_physical_boundary",
                }
            else:
                first = noncommitted[0]
                raise ValueError(
                    "query contains a non-constitution failure: "
                    f"operation={first.get('operation_type')}, "
                    f"status={first.get('transaction_status')}, "
                    f"reason={first.get('rollback_reason')}"
                )
        replay = verify_records(records, tolerance=0.0, world_interventions=interventions).to_dict()
        if replay.get("verified") is not True:
            raise ValueError("trajectory failed exact replay")
        leakage = _visible_leakage_matches(records)
        if physical_failure is None:
            measurements = {}
            masks = {}
            noise_keys = {}
            for instrument in INSTRUMENTS:
                values, observed = _measurement(records, instrument)
                measurements[instrument] = values
                masks[instrument] = observed
                noise_keys[instrument] = noise_coordinates[instrument].key_sha256
            final_assay = next(
                row
                for row in records
                if row.get("transaction_status") == "committed"
                and row.get("instrument") == "final_assay"
            )
            safety_risk = final_assay.get("observation", {}).get("safety_risk")
            if isinstance(safety_risk, bool) or not isinstance(safety_risk, int | float):
                raise ValueError("final assay lacks finite safety_risk")
            safe = float(safety_risk) < float(get_task(TASK_ID).safety_limit)
    except Exception as error:
        failure = {"type": type(error).__name__, "message": str(error)[:1000]}
        if trajectory.is_file() and not records:
            records = load_jsonl(trajectory)
        if records:
            leakage = _visible_leakage_matches(records)
    status = (
        "platform_failure"
        if failure is not None
        else "physical_failure"
        if physical_failure is not None
        else "completed"
    )
    intervention_hashes = {
        str(row["mechanism_family_intervention_hash"])
        for row in records
        if isinstance(row.get("mechanism_family_intervention_hash"), str)
    }
    task_contract_hashes = {
        str(record["task_contract_hash"])
        for record in records
        if isinstance(record.get("task_contract_hash"), str)
    }
    mechanism_hashes = {
        str(record["mechanism_hash"])
        for record in records
        if isinstance(record.get("mechanism_hash"), str)
    }
    row = {
        **dict(cell),
        "task_id": TASK_ID,
        "world_seed": WORLD_SEED,
        "law_id": law_id,
        "status": status,
        "attribution": (
            "platform_defect_candidate"
            if status == "platform_failure"
            else "protocol_owned_physical_boundary"
            if status == "physical_failure"
            else "protocol_owned_completed_outcome"
        ),
        "safe": safe,
        "measurements": measurements,
        "observed_masks": masks,
        "action_plan_sha256": action_hash,
        "observation_coordinate_sha256": {
            instrument: canonical_json_sha256(coordinate.to_audit_dict())
            for instrument, coordinate in noise_coordinates.items()
        },
        "noise_key_sha256": noise_keys,
        "constitutive_intervention_hash": (
            next(iter(intervention_hashes)) if len(intervention_hashes) == 1 else None
        ),
        "task_contract_hash": (
            next(iter(task_contract_hashes)) if len(task_contract_hashes) == 1 else None
        ),
        "mechanism_hash": (
            next(iter(mechanism_hashes)) if len(mechanism_hashes) == 1 else None
        ),
        "exact_replay": replay is not None and replay.get("verified") is True,
        "replay": replay,
        "physical_failure": physical_failure,
        "platform_failure": failure,
        "participant_visible_leakage_matches": leakage,
        "participant_visible_payload": {
            "measurements": measurements,
            "observed_masks": masks,
        },
        "trajectory": (
            {"path": trajectory.relative_to(ROOT).as_posix(), "sha256": file_sha256(trajectory)}
            if trajectory.is_file()
            else None
        ),
        "elapsed_s": round(perf_counter() - started, 6),
    }
    write_json_atomic(law_root / "receipt.json", row)
    return row


def _write_outputs(
    *,
    rows: list[dict[str, Any]],
    audit: dict[str, Any],
    output_root: Path,
    summary_path: Path,
    started: float,
    execution_context: WorkIIExecutionContext,
) -> dict[str, Any]:
    baseline_hashes = {
        row["constitutive_intervention_hash"]
        for row in rows
        if row["law_id"] == LAW_IDS[0]
    }
    power_hashes = {
        row["constitutive_intervention_hash"]
        for row in rows
        if row["law_id"] == LAW_IDS[1]
    }
    audit["execution_constitutive_binding_matches"] = (
        len(rows) == TOTAL_EXECUTIONS
        and baseline_hashes == {None}
        and power_hashes == {audit["power_response_intervention_hash"]}
    )
    analysis = analyze(rows, audit)
    platform_stopped = any(row["status"] == "platform_failure" for row in rows)
    decision = (
        "platform_defect_stop_and_rerun_whole_block_after_fix"
        if platform_stopped
        else "proceed_to_unchanged_five_world_provider_free_qualification"
        if analysis["passed"]
        else "retain_q0_scientific_rejection_and_do_not_expand"
    )
    task_report: dict[str, Any] = {
        "schema_version": TASK_REPORT_VERSION,
        "qualification_schema_version": QUALIFICATION_VERSION,
        "formal_result": False,
        "provider_call_count": 0,
        "participant_session_count": 0,
        "execution_context": build_execution_envelope(execution_context),
        "task_id": TASK_ID,
        "world_seed": WORLD_SEED,
        "frozen_exponents": {
            "linear_response": BASELINE_EXPONENT,
            "power_response": POWER_RESPONSE_EXPONENT,
        },
        "constitutive_audit": audit,
        "rows": rows,
        "analysis": analysis,
    }
    task_report["report_sha256"] = task_report_sha256(task_report)
    report_path = output_root / "task-report.json"
    write_json_atomic(report_path, task_report)
    report_errors = validate_task_report(
        task_report,
        root=ROOT,
        expected_execution_context=execution_context,
    )
    if report_errors:
        raise RuntimeError(
            "invalid partition constitutive Q0 task report: "
            + "; ".join(report_errors)
        )
    summary: dict[str, Any] = {
        "schema_version": SUMMARY_VERSION,
        "qualification_schema_version": QUALIFICATION_VERSION,
        "formal_result": False,
        "provider_call_count": 0,
        "participant_session_count": 0,
        "execution_context": build_execution_envelope(execution_context),
        "task_id": TASK_ID,
        "world_seed": WORLD_SEED,
        "coverage": {
            "law_ids": list(LAW_IDS),
            "grid_axes": {
                "aqueous_load_volume_L": [0.006, 0.015, 0.024],
                "extractant_phase_volume_L": [0.008, 0.019, 0.030],
            },
            "grid_cell_count": len(registered_cells()),
            "planned_execution_count": TOTAL_EXECUTIONS,
            "attempted_execution_count": len(rows),
        },
        "denominators": analysis["denominators"],
        "analysis": analysis,
        "platform_stop_triggered": platform_stopped,
        "five_world_provider_free_expansion_authorized": analysis["passed"],
        "participant_d1_authorized": False,
        "provider_execution_authorized": False,
        "decision": decision,
        "raw_binding": {
            "path": report_path.relative_to(ROOT).as_posix(),
            "sha256": file_sha256(report_path),
            "report_sha256": task_report["report_sha256"],
        },
        "elapsed_s": round(perf_counter() - started, 3),
    }
    summary["summary_sha256"] = summary_sha256(summary)
    write_json_atomic(summary_path, summary)
    summary_errors = validate_summary(
        summary, root=ROOT, expected_execution_context=execution_context
    )
    if summary_errors:
        raise RuntimeError(
            "invalid partition constitutive Q0 summary: " + "; ".join(summary_errors)
        )
    return summary


def _write_nominal_pair_outputs(
    *,
    rows: list[dict[str, Any]],
    audit: dict[str, Any],
    output_root: Path,
    summary_path: Path,
    started: float,
    execution_context: WorkIIExecutionContext,
) -> dict[str, Any]:
    baseline_hashes = {
        row["constitutive_intervention_hash"]
        for row in rows
        if row["law_id"] == LAW_IDS[0]
    }
    power_hashes = {
        row["constitutive_intervention_hash"]
        for row in rows
        if row["law_id"] == LAW_IDS[1]
    }
    audit["execution_constitutive_binding_matches"] = (
        len(rows) == NOMINAL_PAIR_TOTAL_EXECUTIONS
        and baseline_hashes == {None}
        and power_hashes == {audit["power_response_intervention_hash"]}
    )
    analysis = analyze_nominal_pairs(rows, audit)
    platform_stopped = any(row["status"] == "platform_failure" for row in rows)
    decision = (
        "platform_defect_stop_and_rerun_whole_block_after_fix"
        if platform_stopped
        else "proceed_to_unchanged_five_world_provider_free_qualification"
        if analysis["passed"]
        else "retain_q0_scientific_rejection_and_do_not_expand"
    )
    task_report: dict[str, Any] = {
        "schema_version": NOMINAL_PAIR_TASK_REPORT_VERSION,
        "qualification_schema_version": NOMINAL_PAIR_QUALIFICATION_VERSION,
        "formal_result": False,
        "provider_call_count": 0,
        "participant_session_count": 0,
        "execution_context": build_execution_envelope(execution_context),
        "task_id": TASK_ID,
        "world_seed": WORLD_SEED,
        "frozen_exponents": {
            LAW_IDS[0]: BASELINE_EXPONENT,
            LAW_IDS[1]: POWER_RESPONSE_EXPONENT,
        },
        "constitutive_audit": audit,
        "rows": rows,
        "analysis": analysis,
    }
    task_report["report_sha256"] = task_report_sha256(task_report)
    report_path = output_root / "task-report.json"
    write_json_atomic(report_path, task_report)
    report_errors = validate_nominal_pair_task_report(
        task_report,
        root=ROOT,
        expected_execution_context=execution_context,
    )
    if report_errors:
        raise RuntimeError(
            "invalid partition nominal-pair Q0 task report: "
            + "; ".join(report_errors)
        )
    summary: dict[str, Any] = {
        "schema_version": NOMINAL_PAIR_SUMMARY_VERSION,
        "qualification_schema_version": NOMINAL_PAIR_QUALIFICATION_VERSION,
        "formal_result": False,
        "provider_call_count": 0,
        "participant_session_count": 0,
        "execution_context": build_execution_envelope(execution_context),
        "task_id": TASK_ID,
        "world_seed": WORLD_SEED,
        "coverage": {
            "law_ids": list(LAW_IDS),
            "grid_axes": {
                "solvent": list(NOMINAL_IDENTITIES),
                "extractant": list(NOMINAL_IDENTITIES),
            },
            "fixed_coordinates": {
                "aqueous_volume_L": NOMINAL_PAIR_AQUEOUS_VOLUME_L,
                "extractant_volume_L": NOMINAL_PAIR_EXTRACTANT_VOLUME_L,
                "solvent_volume_L": NOMINAL_PAIR_SOLVENT_VOLUME_L,
            },
            "grid_cell_count": len(registered_nominal_pair_cells()),
            "planned_execution_count": NOMINAL_PAIR_TOTAL_EXECUTIONS,
            "attempted_execution_count": len(rows),
        },
        "denominators": analysis["denominators"],
        "analysis": analysis,
        "platform_stop_triggered": platform_stopped,
        "five_world_provider_free_expansion_authorized": analysis["passed"],
        "participant_d1_authorized": False,
        "provider_execution_authorized": False,
        "decision": decision,
        "raw_binding": {
            "path": report_path.relative_to(ROOT).as_posix(),
            "sha256": file_sha256(report_path),
            "report_sha256": task_report["report_sha256"],
        },
        "elapsed_s": round(perf_counter() - started, 3),
    }
    summary["summary_sha256"] = summary_sha256(summary)
    write_json_atomic(summary_path, summary)
    summary_errors = validate_nominal_pair_summary(
        summary,
        root=ROOT,
        expected_execution_context=execution_context,
    )
    if summary_errors:
        raise RuntimeError(
            "invalid partition nominal-pair Q0 summary: "
            + "; ".join(summary_errors)
        )
    return summary


def run(args: argparse.Namespace) -> dict[str, Any]:
    execution_context = prepare_execution_context(
        ROOT,
        mode=args.execution_mode,
        release_manifest=args.release_manifest,
    )
    if args.output_root.exists() or args.summary.exists():
        raise FileExistsError("refusing to overwrite partition constitutive Q0 outputs")
    args.output_root.mkdir(parents=True)
    started = perf_counter()
    audit = constitutive_audit()
    rows: list[dict[str, Any]] = []
    for cell in registered_nominal_pair_cells():
        for law_id in LAW_IDS:
            row = execute(
                cell=cell,
                law_id=law_id,
                output_root=args.output_root,
                nominal_pair=True,
            )
            rows.append(row)
            elapsed = perf_counter() - started
            rate = len(rows) / elapsed if elapsed else 0.0
            print(
                json.dumps(
                    {
                        "stage": "paired_execution",
                        "completed": len(rows),
                        "total": NOMINAL_PAIR_TOTAL_EXECUTIONS,
                        "throughput_executions_per_minute": round(rate * 60.0, 2),
                        "eta_s": round(
                            (NOMINAL_PAIR_TOTAL_EXECUTIONS - len(rows)) / rate, 1
                        )
                        if rate
                        else None,
                        "failure_count": sum(item["status"] != "completed" for item in rows),
                        "current_cell": cell["cell_id"],
                        "law_id": law_id,
                        "status": row["status"],
                    },
                    sort_keys=True,
                ),
                flush=True,
            )
            if row["status"] == "platform_failure":
                return _write_nominal_pair_outputs(
                    rows=rows,
                    audit=audit,
                    output_root=args.output_root,
                    summary_path=args.summary,
                    started=started,
                    execution_context=execution_context,
                )
    return _write_nominal_pair_outputs(
        rows=rows,
        audit=audit,
        output_root=args.output_root,
        summary_path=args.summary,
        started=started,
        execution_context=execution_context,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--summary", type=Path)
    parser.add_argument(
        "--execution-mode",
        choices=[mode.value for mode in ExecutionMode],
        default=ExecutionMode.DEVELOPMENT.value,
    )
    parser.add_argument("--release-manifest", type=Path)
    args = parser.parse_args()
    if (
        args.execution_mode == ExecutionMode.RELEASE.value
        and args.output_root.resolve() == DEFAULT_OUTPUT_ROOT.resolve()
    ):
        args.output_root = RELEASE_OUTPUT_ROOT
    args.output_root = args.output_root.resolve()
    args.summary = (
        args.summary.resolve()
        if args.summary is not None
        else (
            RELEASE_SUMMARY
            if args.execution_mode == ExecutionMode.RELEASE.value
            else args.output_root / "summary.json"
        ).resolve()
    )
    if args.release_manifest is not None:
        args.release_manifest = args.release_manifest.resolve()
    summary = run(args)
    print(
        json.dumps(
            {
                "attempted": summary["denominators"]["attempted"],
                "planned": summary["denominators"]["planned"],
                "decision": summary["decision"],
                "elapsed_s": summary["elapsed_s"],
            },
            sort_keys=True,
        ),
        flush=True,
    )
    return 0 if summary["analysis"]["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
