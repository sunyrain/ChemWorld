#!/usr/bin/env python3
"""Run the provider-free Work II reaction-safety matched-prior qualification."""

from __future__ import annotations

import argparse
import copy
from collections.abc import Mapping
from pathlib import Path
from time import perf_counter
from typing import Any

from chemworld.eval.provenance import (
    canonical_json_sha256,
    file_sha256,
    write_json_atomic,
)
from chemworld.eval.work_ii_execution_mode import (
    ExecutionMode,
    WorkIIExecutionContext,
    build_execution_envelope,
    prepare_execution_context,
    validate_execution_envelope,
)
from chemworld.eval.work_ii_matched_prior_qualification import (
    MATCHED_PRIOR_VERSION,
    analyze_matched_prior_world,
    held_out_query_contract,
    rounded_reference_context,
    select_reference_candidate,
    surface_design,
)
from chemworld.tasks import get_task

try:
    from scripts.run_work_ii_mechanism_oracle_qualification import (
        InMemoryMechanismEvaluator,
    )
    from scripts.run_work_ii_q1_response_surface import (
        TASK_SPECS,
        _emit,
        _load,
    )
except ModuleNotFoundError:
    from run_work_ii_mechanism_oracle_qualification import (  # type: ignore[no-redef]
        InMemoryMechanismEvaluator,
    )
    from run_work_ii_q1_response_surface import (  # type: ignore[no-redef]
        TASK_SPECS,
        _emit,
        _load,
    )

ROOT = Path(__file__).resolve().parents[1]
TASK_ID = "reaction-safety-constrained"
SOURCE_SUMMARY = (
    ROOT
    / "workstreams/flagship_tasks/reports/"
    "work-ii-mechanism-oracle-reaction-safety-classified-v0.2-20260811.json"
)
DEFAULT_OUTPUT_ROOT = (
    ROOT / "runs/development/work-ii-reaction-safety-matched-prior-qualification-v0.3-20260811"
)
DEFAULT_SUMMARY = (
    ROOT
    / "workstreams/flagship_tasks/reports/"
    "work-ii-reaction-safety-matched-prior-qualification-20260811.json"
)
DEFAULT_PACKAGE = (
    ROOT
    / "workstreams/flagship_tasks/reports/"
    "work-ii-reaction-safety-matched-prior-package.json"
)
DEFAULT_D1_CONFIG = (
    ROOT
    / "workstreams/flagship_tasks/reports/"
    "work-ii-reaction-safety-matched-prior-d1.json"
)
SUMMARY_VERSION = "chemworld-work-ii-matched-prior-five-world-summary-0.3"
WORLD_REPORT_VERSION = "chemworld-work-ii-matched-prior-world-report-0.3"
PACKAGE_VERSION = "chemworld-work-ii-matched-prior-package-0.3"


class Progress:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.started = perf_counter()
        self.completed = 0
        self.total = 5 * 121
        self.last_emit = self.started

    def update(
        self,
        *,
        world_seed: int,
        stage: str,
        platform_failures: int,
        physical_failures: int,
        force: bool = False,
    ) -> None:
        self.completed += 1
        now = perf_counter()
        if not force and self.completed % 10 != 0 and now - self.last_emit < 30.0:
            return
        elapsed = now - self.started
        rate = self.completed / elapsed if elapsed else 0.0
        _emit(
            self.path,
            {
                "event": "matched_prior_progress",
                "task_id": TASK_ID,
                "world_seed": world_seed,
                "stage": stage,
                "completed": self.completed,
                "total": self.total,
                "throughput_queries_per_minute": round(rate * 60.0, 2),
                "eta_s": round((self.total - self.completed) / rate, 1) if rate else None,
                "platform_failure_count": platform_failures,
                "physical_failure_count": physical_failures,
                "elapsed_s": round(elapsed, 1),
            },
        )
        self.last_emit = now


def _prepare_execution(
    args: argparse.Namespace,
) -> tuple[WorkIIExecutionContext, dict[str, object]]:
    context = prepare_execution_context(
        ROOT,
        mode=getattr(args, "execution_mode", ExecutionMode.DEVELOPMENT.value),
        release_manifest=getattr(args, "release_manifest", None),
    )
    return context, build_execution_envelope(context)


def _resolve_output_paths(
    args: argparse.Namespace, context: WorkIIExecutionContext
) -> tuple[Path, Path, Path, Path]:
    output_root = args.output_root.resolve()
    summary_path = (
        args.summary.resolve()
        if args.summary is not None
        else (
            DEFAULT_SUMMARY
            if context.mode is ExecutionMode.RELEASE
            else output_root / "summary.json"
        )
    )
    package_path = (
        args.package.resolve()
        if args.package is not None
        else (
            DEFAULT_PACKAGE
            if context.mode is ExecutionMode.RELEASE
            else output_root / "package.json"
        )
    )
    d1_config_path = (
        args.d1_config.resolve()
        if args.d1_config is not None
        else (
            DEFAULT_D1_CONFIG
            if context.mode is ExecutionMode.RELEASE
            else output_root / "d1.json"
        )
    )
    return output_root, summary_path, package_path, d1_config_path


def _validate_source_execution_context(
    source_summary: Mapping[str, Any],
    execution_context: WorkIIExecutionContext,
) -> tuple[Mapping[str, Any] | None, bool]:
    source_context = source_summary.get("execution_context")
    if not isinstance(source_context, Mapping):
        if execution_context.mode is ExecutionMode.RELEASE:
            raise ValueError("release Q2 source lacks its execution context")
        return None, True
    if execution_context.mode is ExecutionMode.RELEASE:
        context_errors = validate_execution_envelope(ROOT, source_context, execution_context)
        if context_errors:
            raise ValueError(
                "release Q2 source must use the same release freeze: "
                + "; ".join(context_errors)
            )
    elif source_context.get("execution_mode") not in {
        ExecutionMode.DEVELOPMENT.value,
        ExecutionMode.RELEASE.value,
    }:
        raise ValueError("development Q2 source has an unsupported execution mode")
    return source_context, False


def _source_reports(
    source_summary: Mapping[str, Any],
    *,
    source_summary_path: Path,
    execution_context: WorkIIExecutionContext,
) -> tuple[list[dict[str, Any]], bool]:
    if source_summary.get("q2_authorized") is not True:
        raise ValueError("mechanism-oracle source does not authorize Q2")
    if source_summary.get("decision") != "proceed_to_q2_matched_prior_construction":
        raise ValueError("mechanism-oracle source decision drifted")
    if source_summary.get("summary_sha256") != canonical_json_sha256(
        {
            key: value
            for key, value in source_summary.items()
            if key != "summary_sha256"
        }
    ):
        raise ValueError("mechanism-oracle source summary self-hash mismatch")
    bindings = source_summary.get("raw_bindings")
    if not isinstance(bindings, list) or len(bindings) != 5:
        raise ValueError("mechanism-oracle source must bind five raw reports")
    source_execution_context, legacy_source_evidence = _validate_source_execution_context(
        source_summary, execution_context
    )
    reports = []
    for binding in sorted(bindings, key=lambda item: int(item["world_seed"])):
        path = (ROOT / str(binding["path"])).resolve()
        if not path.is_relative_to(ROOT) or not path.is_file():
            raise FileNotFoundError(path)
        if file_sha256(path) != str(binding["sha256"]):
            raise ValueError(f"mechanism-oracle raw binding hash mismatch: {path}")
        report = _load(path)
        if report.get("report_sha256") != canonical_json_sha256(
            {key: value for key, value in report.items() if key != "report_sha256"}
        ):
            raise ValueError("mechanism-oracle raw source self-hash mismatch")
        if int(report["world_seed"]) != int(binding["world_seed"]):
            raise ValueError("mechanism-oracle raw binding world mismatch")
        if report.get("analysis", {}).get("passed") is not True:
            raise ValueError("mechanism-oracle raw source contains a failed world")
        if (
            not legacy_source_evidence
            and report.get("execution_context") != source_execution_context
        ):
            raise ValueError("mechanism-oracle raw source execution context drifted")
        reports.append(report)
    return reports, legacy_source_evidence


def _run_world(
    *,
    source_report: Mapping[str, Any],
    config: Mapping[str, Any],
    spec: Mapping[str, Any],
    output_root: Path,
    progress: Progress,
    execution_context: Mapping[str, object],
    legacy_source_evidence: bool,
) -> dict[str, Any]:
    world_seed = int(source_report["world_seed"])
    selected = select_reference_candidate(source_report)
    context = rounded_reference_context(selected["vector"])
    design = surface_design(context)
    evaluator = InMemoryMechanismEvaluator(
        task_id=TASK_ID,
        config=config,
        spec=spec,
        world_seed=world_seed,
    )
    rows: list[dict[str, Any]] = []
    started = perf_counter()
    try:
        for design_row in design:
            result = evaluator.evaluate(
                design_row["vector"],
                phase="matched_prior_surface",
                extra={key: value for key, value in design_row.items() if key != "vector"},
            )
            rows.append(result)
            progress.update(
                world_seed=world_seed,
                stage="surface",
                platform_failures=evaluator.failure_count,
                physical_failures=evaluator.physical_failure_count,
                force=len(rows) == len(design),
            )
    finally:
        evaluator.close()
    sigma = float(source_report["analysis"]["validation_noise"]["sigma"] or 0.0)
    analysis = analyze_matched_prior_world(
        rows,
        validation_sigma=sigma,
        reference_context=context,
        world_token=f"{TASK_ID}:{world_seed}",
    )
    selected_rows_by_id = {str(row["query_id"]): row for row in rows}
    held_out_rows = [
        selected_rows_by_id[str(row["query_id"])] for row in analysis.get("held_out_queries", [])
    ]
    held_out_queries = held_out_query_contract(held_out_rows, reference_context=context)
    public = analysis.get("public_priors", {})
    prior_arms = {
        "opaque": {
            "material_information": {"mode": "opaque_codes"},
            "initial_world_model": public.get("opaque"),
        },
        "aligned_nominal": {
            "material_information": {"mode": "opaque_codes"},
            "initial_world_model": public.get("supplied_a"),
        },
        "misindexed_nominal": {
            "material_information": {"mode": "opaque_codes"},
            "initial_world_model": public.get("supplied_b"),
        },
    }
    report: dict[str, Any] = {
        "schema_version": WORLD_REPORT_VERSION,
        "qualification_schema_version": MATCHED_PRIOR_VERSION,
        "formal_result": False,
        "execution_context": dict(execution_context),
        "legacy_source_evidence": legacy_source_evidence,
        "task_id": TASK_ID,
        "world_seed": world_seed,
        "source_mechanism_oracle_report_sha256": str(source_report["report_sha256"]),
        "reference_selection": selected,
        "reference_context": context,
        "surface_rows": rows,
        "analysis": analysis,
        "prior_arms": prior_arms,
        "held_out_queries": held_out_queries,
        "elapsed_s": round(perf_counter() - started, 3),
    }
    report["report_sha256"] = canonical_json_sha256(report)
    world_root = output_root / f"world-{world_seed}"
    world_root.mkdir(parents=True, exist_ok=False)
    write_json_atomic(world_root / "world-report.json", report)
    return report


def _d1_config(
    base: Mapping[str, Any],
    world_package: Mapping[str, Any],
    *,
    execution_context: Mapping[str, object] | None = None,
    legacy_source_evidence: bool = False,
) -> dict[str, Any]:
    config = copy.deepcopy(dict(base))
    config.update(
        {
            "schema_version": "chemworld-work-ii-campaign-pilot-0.4",
            "pilot_id": "work-ii-reaction-safety-matched-prior-d1",
            "formal_result": False,
            "execution_context": dict(
                execution_context
                or build_execution_envelope(
                    prepare_execution_context(ROOT, mode=ExecutionMode.DEVELOPMENT)
                )
            ),
            "legacy_source_evidence": legacy_source_evidence,
            "world_seed": int(world_package["world_seed"]),
            "observation_noise_namespace": "work-ii-reaction-safety-matched-prior-d1",
            "prior_arms": copy.deepcopy(world_package["prior_arms"]),
            "snapshot_stages": [
                "pre_evidence",
                "after_experiment_2",
                "after_experiment_4",
                "after_experiment_7",
                "final",
            ],
        }
    )
    config["intervention"] = {
        "locus": "parametric",
        "target": "reaction_temperature_duration_local_law",
        "target_controls": ["reaction_temperature_K", "reaction_duration_s"],
        "fixed_reference_context": copy.deepcopy(world_package["reference_context"]),
        "material_information_matched_opaque": True,
        "world_and_resource_contract_matched": True,
        "q2_binding_sha256": str(world_package["world_package_sha256"]),
    }
    config["belief_checkpoint"] = {
        "allowed_feature_ids": [
            "catalyst",
            "solvent",
            "reagent_amount_mol",
            "catalyst_amount_mol",
            "stirring_speed_rpm",
            "solvent_volume_L",
            "reaction_temperature_K",
            "reaction_duration_s",
        ],
        "allowed_metric_ids": ["yield", "selectivity", "safety_risk", "score"],
        "allowed_prior_fields": ["reaction_temperature_K", "reaction_duration_s"],
        "held_out_queries": copy.deepcopy(world_package["held_out_queries"]),
    }
    config["campaign"] = {
        "card_id": "work-ii-reaction-safety-a-p-k10-two-repeat",
        "checkpoint_complete_experiments": [0, 2, 4, 7, 10],
        "complete_experiments": 10,
        "final_assay_limit": 10,
        "nonfinal_instrument_use_limit": 10,
        "operation_attempt_limit": 100,
        "operation_repeat_limits": {"heat": 12, "quench": 10},
        "implicit_operation_time_s": {"quench": 120.0},
        "process_time_limit_s": 145200.0,
        "process_time_policy": {
            "pattern_id": "reaction-safety-a-p-k10-two-repeat",
            "formula": "8 unique heat maxima + 2 exact-repeat heat maxima + 10 quench reserves",
            "required_stage_max_s": 115200.0,
            "repeat_allowance_s": 28800.0,
            "implicit_stage_reserve_s": 1200.0,
        },
        "stock_limits": {
            "catalyst_mol": 0.006325,
            "reagent_mol": 0.345,
            "solvent_L": 0.575,
        },
        "vessel_start_limit": 10,
        "closeout_policy": {
            "policy": "participant_controlled_advisory_no_hidden_allocation",
            "automatic_action_repair": False,
            "automatic_closeout": False,
            "planned_batches": 10,
            "discard_path_operations_per_batch": 1,
            "discard_path_total_operation_reserve": 10,
            "final_assay_path_operations_per_batch": 2,
            "final_assay_path_total_operation_reserve": 20,
        },
    }
    config["method_resources"].update(
        {
            "checkpoint_complete_experiments": [2, 4, 7, 10],
            "complete_experiment_limit": 10,
            "operation_limit": 100,
            "resource_status": "development_d1_envelope_pending_pattern_calibration",
        }
    )
    config["qualification"] = {
        "required_operation_counts": {},
        "q2_passed": True,
        "execution_authorized": False,
        "formal_r5_authorized": False,
    }
    return config


def run(args: argparse.Namespace) -> dict[str, Any]:
    context, execution_context = _prepare_execution(args)
    source_summary_path = args.source_summary.resolve()
    output_root, summary_path, package_path, d1_config_path = _resolve_output_paths(
        args, context
    )
    paths = [output_root, summary_path, package_path, d1_config_path]
    dynamic_root = (ROOT / "workstreams/flagship_tasks/reports").resolve()
    if context.mode is ExecutionMode.RELEASE:
        for path in (summary_path, package_path, d1_config_path):
            if not path.resolve().is_relative_to(dynamic_root):
                raise ValueError(
                    "matched-prior tracked outputs must use the dynamic evidence root"
                )
    if any(path.exists() for path in paths):
        raise FileExistsError("refusing to overwrite matched-prior qualification outputs")
    source_summary = _load(source_summary_path)
    source_reports, legacy_source_evidence = _source_reports(
        source_summary,
        source_summary_path=source_summary_path,
        execution_context=context,
    )
    spec = TASK_SPECS[TASK_ID]
    base_config = _load((ROOT / str(spec["config"])).resolve())
    output_root.mkdir(parents=True)
    progress = Progress(args.progress_file)
    started = perf_counter()
    world_reports = [
        _run_world(
            source_report=source_report,
            config=base_config,
            spec=spec,
            output_root=output_root,
            progress=progress,
            execution_context=execution_context,
            legacy_source_evidence=legacy_source_evidence,
        )
        for source_report in source_reports
    ]
    package_worlds = []
    raw_bindings = []
    for report in world_reports:
        world_seed = int(report["world_seed"])
        raw_path = output_root / f"world-{world_seed}" / "world-report.json"
        world_package: dict[str, Any] = {
            "task_id": TASK_ID,
            "world_seed": world_seed,
            "reference_context": report["reference_context"],
            "prior_arms": report["prior_arms"],
            "held_out_queries": report["held_out_queries"],
            "qualification_passed": bool(report["analysis"]["passed"]),
            "qualification_report_sha256": str(report["report_sha256"]),
        }
        world_package["world_package_sha256"] = canonical_json_sha256(world_package)
        package_worlds.append(world_package)
        raw_bindings.append(
            {
                "world_seed": world_seed,
                "path": raw_path.relative_to(ROOT).as_posix(),
                "sha256": file_sha256(raw_path),
                "passed": bool(report["analysis"]["passed"]),
            }
        )
    qualification_passed = all(row["qualification_passed"] for row in package_worlds)
    package: dict[str, Any] = {
        "schema_version": PACKAGE_VERSION,
        "qualification_schema_version": MATCHED_PRIOR_VERSION,
        "formal_result": False,
        "execution_context": execution_context,
        "legacy_source_evidence": legacy_source_evidence,
        "task_id": TASK_ID,
        "source_summary": {
            "path": source_summary_path.relative_to(ROOT).as_posix(),
            "sha256": file_sha256(source_summary_path),
        },
        "qualification_passed": qualification_passed,
        "arm_semantics": {
            "opaque": "opaque",
            "aligned_nominal": "aligned",
            "misindexed_nominal": "misspecified",
        },
        "worlds": package_worlds,
    }
    package["package_sha256"] = canonical_json_sha256(package)
    write_json_atomic(package_path, package)
    d1_config = (
        _d1_config(
            base_config,
            package_worlds[0],
            execution_context=execution_context,
            legacy_source_evidence=legacy_source_evidence,
        )
        if qualification_passed
        else None
    )
    if d1_config is not None:
        write_json_atomic(d1_config_path, d1_config)
    failures = [
        {"world_seed": report["world_seed"], "failure": failure}
        for report in world_reports
        for failure in report["analysis"].get("failures", [])
    ]
    summary: dict[str, Any] = {
        "schema_version": SUMMARY_VERSION,
        "qualification_schema_version": MATCHED_PRIOR_VERSION,
        "formal_result": False,
        "execution_context": execution_context,
        "legacy_source_evidence": legacy_source_evidence,
        "task_id": TASK_ID,
        "world_seeds": list(get_task(TASK_ID).seeds),
        "provider_call_count": 0,
        "coverage": {
            "world_count": 5,
            "surface_queries_per_world": 121,
            "planned_surface_query_count": 605,
            "held_out_queries_per_world": 16,
        },
        "denominators": {
            "world_count": 5,
            "passed_world_count": sum(report["analysis"]["passed"] for report in world_reports),
            "classified_surface_query_count": sum(
                int(report["analysis"]["classified_count"]) for report in world_reports
            ),
            "platform_failure_count": sum(
                int(report["analysis"]["platform_failure_count"]) for report in world_reports
            ),
            "physical_failure_count": sum(
                int(report["analysis"]["physical_failure_count"]) for report in world_reports
            ),
            "safe_fit_count": sum(
                int(report["analysis"]["safe_fit_count"]) for report in world_reports
            ),
            "safe_held_out_count": sum(
                int(report["analysis"]["safe_held_out_count"]) for report in world_reports
            ),
        },
        "worlds": [
            {
                "world_seed": report["world_seed"],
                "passed": report["analysis"]["passed"],
                "reference_selection": report["reference_selection"],
                "reference_context": report["reference_context"],
                "physical_failure_count": report["analysis"]["physical_failure_count"],
                "safe_fit_count": report["analysis"]["safe_fit_count"],
                "safe_held_out_count": report["analysis"]["safe_held_out_count"],
                "aligned_score_normalized_mae": report["analysis"].get(
                    "aligned_score_normalized_mae"
                ),
                "aligned_risk_normalized_mae": report["analysis"].get(
                    "aligned_risk_normalized_mae"
                ),
                "selected_reflection": report["analysis"].get("selected_reflection"),
                "prior_matching": report["analysis"].get("prior_matching"),
                "leakage_audit": report["analysis"].get("leakage_audit"),
                "elapsed_s": report["elapsed_s"],
            }
            for report in world_reports
        ],
        "raw_bindings": raw_bindings,
        "failure_count": len(failures),
        "failures": failures,
        "qualification_passed": qualification_passed,
        "d1_authorized": qualification_passed,
        "provider_execution_authorized": False,
        "decision": (
            "proceed_to_reaction_safety_d1"
            if qualification_passed
            else "reject_reaction_safety_matched_prior_before_d1"
        ),
        "generated_package": {
            "path": package_path.relative_to(ROOT).as_posix(),
            "sha256": file_sha256(package_path),
        },
        "generated_d1_config": (
            {
                "path": d1_config_path.relative_to(ROOT).as_posix(),
                "sha256": file_sha256(d1_config_path),
            }
            if d1_config is not None
            else None
        ),
        "elapsed_s": round(perf_counter() - started, 3),
        "interpretation": (
            "Provider-free Q2 qualification of matched local priors. Physical failures are "
            "retained as safety outcomes; only platform failures invalidate execution."
        ),
    }
    summary["summary_sha256"] = canonical_json_sha256(summary)
    write_json_atomic(summary_path, summary)
    _emit(
        args.progress_file,
        {
            "event": "matched_prior_completed",
            "passed_worlds": summary["denominators"]["passed_world_count"],
            "worlds": 5,
            "classified": summary["denominators"]["classified_surface_query_count"],
            "platform_failures": summary["denominators"]["platform_failure_count"],
            "physical_failures": summary["denominators"]["physical_failure_count"],
            "decision": summary["decision"],
            "elapsed_s": summary["elapsed_s"],
        },
    )
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--source-summary", type=Path, default=SOURCE_SUMMARY)
    parser.add_argument("--summary", type=Path)
    parser.add_argument("--package", type=Path)
    parser.add_argument("--d1-config", type=Path)
    parser.add_argument("--progress-file", type=Path, required=True)
    parser.add_argument(
        "--execution-mode",
        choices=[mode.value for mode in ExecutionMode],
        default=ExecutionMode.DEVELOPMENT.value,
    )
    parser.add_argument("--release-manifest", type=Path)
    args = parser.parse_args()
    summary = run(args)
    return 0 if summary["qualification_passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
