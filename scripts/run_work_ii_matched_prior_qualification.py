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
    git_source_commit,
    write_json_atomic,
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
        _scoped_dirty_paths,
    )
except ModuleNotFoundError:
    from run_work_ii_mechanism_oracle_qualification import (  # type: ignore[no-redef]
        InMemoryMechanismEvaluator,
    )
    from run_work_ii_q1_response_surface import (  # type: ignore[no-redef]
        TASK_SPECS,
        _emit,
        _load,
        _scoped_dirty_paths,
    )

ROOT = Path(__file__).resolve().parents[1]
TASK_ID = "reaction-safety-constrained"
SOURCE_SUMMARY = (
    ROOT
    / "workstreams/flagship_tasks/reports/"
    "work-ii-mechanism-oracle-reaction-safety-classified-v0.2-20260811.json"
)
DEFAULT_OUTPUT_ROOT = (
    ROOT / "runs/development/work-ii-reaction-safety-matched-prior-qualification-20260811"
)
DEFAULT_SUMMARY = (
    ROOT
    / "workstreams/flagship_tasks/reports/"
    "work-ii-reaction-safety-matched-prior-qualification-20260811.json"
)
DEFAULT_PACKAGE = (
    ROOT / "configs/benchmark/work_ii_reaction_safety_matched_prior_package.json"
)
DEFAULT_D1_CONFIG = (
    ROOT / "configs/benchmark/work_ii_reaction_safety_matched_prior_d1.json"
)
SUMMARY_VERSION = "chemworld-work-ii-matched-prior-five-world-summary-0.1"
WORLD_REPORT_VERSION = "chemworld-work-ii-matched-prior-world-report-0.1"
PACKAGE_VERSION = "chemworld-work-ii-matched-prior-package-0.1"


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


def _source_reports(source_summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    if source_summary.get("q2_authorized") is not True:
        raise ValueError("mechanism-oracle source does not authorize Q2")
    if source_summary.get("decision") != "proceed_to_q2_matched_prior_construction":
        raise ValueError("mechanism-oracle source decision drifted")
    bindings = source_summary.get("raw_bindings")
    if not isinstance(bindings, list) or len(bindings) != 5:
        raise ValueError("mechanism-oracle source must bind five raw reports")
    reports = []
    for binding in sorted(bindings, key=lambda item: int(item["world_seed"])):
        path = (ROOT / str(binding["path"])).resolve()
        if not path.is_file():
            raise FileNotFoundError(path)
        if file_sha256(path) != str(binding["sha256"]):
            raise ValueError(f"mechanism-oracle raw binding hash mismatch: {path}")
        report = _load(path)
        if int(report["world_seed"]) != int(binding["world_seed"]):
            raise ValueError("mechanism-oracle raw binding world mismatch")
        if report.get("analysis", {}).get("passed") is not True:
            raise ValueError("mechanism-oracle raw source contains a failed world")
        reports.append(report)
    return reports


def _run_world(
    *,
    source_report: Mapping[str, Any],
    config: Mapping[str, Any],
    spec: Mapping[str, Any],
    output_root: Path,
    progress: Progress,
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
        "aligned": {
            "material_information": {"mode": "opaque_codes"},
            "initial_world_model": public.get("supplied_a"),
        },
        "misspecified": {
            "material_information": {"mode": "opaque_codes"},
            "initial_world_model": public.get("supplied_b"),
        },
    }
    report: dict[str, Any] = {
        "schema_version": WORLD_REPORT_VERSION,
        "qualification_schema_version": MATCHED_PRIOR_VERSION,
        "formal_result": False,
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


def _d1_config(base: Mapping[str, Any], world_package: Mapping[str, Any]) -> dict[str, Any]:
    config = copy.deepcopy(dict(base))
    config.update(
        {
            "schema_version": "chemworld-work-ii-campaign-pilot-0.4",
            "pilot_id": "work-ii-reaction-safety-matched-prior-d1",
            "formal_result": False,
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
        "execution_authorized": True,
        "formal_r5_authorized": False,
    }
    return config


def run(args: argparse.Namespace) -> dict[str, Any]:
    dirty = _scoped_dirty_paths()
    if dirty:
        raise RuntimeError(
            "matched-prior qualification requires clean scoped sources: "
            + ", ".join(dirty)
        )
    paths = [args.output_root, args.summary, args.package, args.d1_config]
    if any(path.exists() for path in paths):
        raise FileExistsError("refusing to overwrite matched-prior qualification outputs")
    source_summary = _load(SOURCE_SUMMARY)
    source_reports = _source_reports(source_summary)
    spec = TASK_SPECS[TASK_ID]
    base_config = _load((ROOT / str(spec["config"])).resolve())
    args.output_root.mkdir(parents=True)
    progress = Progress(args.progress_file)
    started = perf_counter()
    world_reports = [
        _run_world(
            source_report=source_report,
            config=base_config,
            spec=spec,
            output_root=args.output_root,
            progress=progress,
        )
        for source_report in source_reports
    ]
    package_worlds = []
    raw_bindings = []
    for report in world_reports:
        world_seed = int(report["world_seed"])
        raw_path = args.output_root / f"world-{world_seed}" / "world-report.json"
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
        "task_id": TASK_ID,
        "source_summary": {
            "path": SOURCE_SUMMARY.relative_to(ROOT).as_posix(),
            "sha256": file_sha256(SOURCE_SUMMARY),
        },
        "qualification_passed": qualification_passed,
        "worlds": package_worlds,
    }
    package["package_sha256"] = canonical_json_sha256(package)
    write_json_atomic(args.package, package)
    d1_config = _d1_config(base_config, package_worlds[0]) if qualification_passed else None
    if d1_config is not None:
        write_json_atomic(args.d1_config, d1_config)
    failures = [
        {"world_seed": report["world_seed"], "failure": failure}
        for report in world_reports
        for failure in report["analysis"].get("failures", [])
    ]
    summary: dict[str, Any] = {
        "schema_version": SUMMARY_VERSION,
        "qualification_schema_version": MATCHED_PRIOR_VERSION,
        "formal_result": False,
        "source_commit": git_source_commit(ROOT),
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
        "decision": (
            "proceed_to_reaction_safety_d1"
            if qualification_passed
            else "reject_reaction_safety_matched_prior_before_d1"
        ),
        "generated_package": {
            "path": args.package.relative_to(ROOT).as_posix(),
            "sha256": file_sha256(args.package),
        },
        "generated_d1_config": (
            {
                "path": args.d1_config.relative_to(ROOT).as_posix(),
                "sha256": file_sha256(args.d1_config),
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
    write_json_atomic(args.summary, summary)
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
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--package", type=Path, default=DEFAULT_PACKAGE)
    parser.add_argument("--d1-config", type=Path, default=DEFAULT_D1_CONFIG)
    parser.add_argument("--progress-file", type=Path, required=True)
    args = parser.parse_args()
    summary = run(args)
    return 0 if summary["qualification_passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
