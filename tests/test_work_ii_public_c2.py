from __future__ import annotations

import json
from pathlib import Path

import pytest

from chemworld.eval.provenance import canonical_json_sha256, file_sha256
from chemworld.eval.work_ii_analysis import (
    WORK_II_ANALYSIS_ARMS,
    build_cluster_correction_record,
)
from chemworld.eval.work_ii_confirmatory import build_confirmatory_analysis
from chemworld.eval.work_ii_public_c2 import (
    ANALYSIS_CONTRACT,
    ANALYSIS_SOURCE_PATHS,
    LOCUS_IDS,
    PUBLIC_C2_LOCUS_REPORT_VERSION,
    PUBLIC_C2_MANIFEST_VERSION,
    PUBLIC_C2_PLAN_CONTRACT,
    WorkIIPublicC2AnalysisError,
    build_locus_cell_report,
    build_public_c2_analysis,
    validate_public_c2_analysis,
    validate_public_c2_analysis_plan,
    validate_public_c2_manifest,
    validate_public_c2_source_files,
)

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS_PLAN = ROOT / "configs/benchmark/work_ii_analysis_plan_v0.1.json"
TASKS = {
    "A_E": ["ae-task-0", "ae-task-1", "ae-task-2", "ae-task-3", "ae-task-4"],
    "A_P": ["ap-task-0", "ap-task-1"],
    "A_S": ["as-task-0", "as-task-1"],
}


def _hash(payload: object) -> str:
    return canonical_json_sha256(payload)


def _rehash(payload: dict[str, object], field: str) -> None:
    payload.pop(field, None)
    payload[field] = _hash(payload)


def _manifest() -> dict[str, object]:
    analysis_plan = json.loads(ANALYSIS_PLAN.read_text(encoding="utf-8"))
    manifest: dict[str, object] = {
        "schema_version": PUBLIC_C2_MANIFEST_VERSION,
        "program_scope": "C2",
        "status": "frozen",
        "formal_result": True,
        "runtime_commit": "a" * 40,
        "analysis_contract": ANALYSIS_CONTRACT,
        "analysis_plan_sha256": _hash(analysis_plan),
        "analysis_source_sha256": {
            path: _hash([path, "source"]) for path in ANALYSIS_SOURCE_PATHS
        },
        "blocks": {
            locus: {
                "locus_id": locus,
                "task_ids": TASKS[locus],
                "expected_task_count": len(TASKS[locus]),
                "worlds_per_task": 5,
                "expected_cluster_count": len(TASKS[locus]) * 5,
                "expected_cell_count": len(TASKS[locus]) * 5 * 3,
                "analysis_report_id": f"public-c2-{locus.lower()}-fixture",
                "execution_manifest_sha256": _hash([locus, "execution"]),
                **(
                    {"legacy_confirmatory_report_sha256": _hash(["A_E", "legacy"])}
                    if locus == "A_E"
                    else {}
                ),
            }
            for locus in LOCUS_IDS
        },
    }
    manifest["manifest_sha256"] = _hash(manifest)
    return manifest


def _bind_legacy_to_manifest(
    manifest: dict[str, object], legacy: dict[str, object]
) -> None:
    manifest["blocks"]["A_E"]["legacy_confirmatory_report_sha256"] = legacy[
        "report_sha256"
    ]
    _rehash(manifest, "manifest_sha256")


def _cell_rows(
    locus: str,
    *,
    task_effects: dict[str, float] | None = None,
) -> list[dict[str, object]]:
    rows = []
    for task_index, task in enumerate(TASKS[locus]):
        effect = 0.22 if task_effects is None else task_effects[task]
        for world_seed in range(5):
            cluster_id = f"{locus.lower()}-{task}-world-{world_seed}"
            jitter = (world_seed - 2) * 0.005
            aligned = 0.04 + jitter
            improvements = {
                "opaque": 0.03 + jitter,
                "aligned_nominal": aligned,
                "misindexed_nominal": aligned + effect,
            }
            for arm_index, arm in enumerate(WORK_II_ANALYSIS_ARMS):
                improvement = improvements[arm]
                cell_id = f"{cluster_id}-{arm}"
                rows.append(
                    {
                        "cell_id": cell_id,
                        "world_cluster_id": cluster_id,
                        "task_id": task,
                        "world_seed": world_seed,
                        "prior_arm": arm,
                        "terminal_state": "completed",
                        "terminal_reason_code": "completed_registered_campaign",
                        "terminal_receipt_sha256": _hash([cell_id, "receipt"]),
                        "checkpoint_error": {
                            "primary_improvement": improvement,
                            "effective_pre_error": 0.45 + 0.05 * arm_index,
                            "confirmatory_improvement_bounds": [
                                improvement,
                                improvement,
                            ],
                            "missing_failure_rule": "observed_final",
                        },
                        "blind_outcome": {
                            "status": "completed",
                            "completed_execution_count": 6,
                            "recommendation_gain_over_incumbent": (
                                0.5 * improvement
                                + 0.005 * task_index
                                + 0.002 * arm_index
                            ),
                        },
                        "final_law_summary": {
                            "present": True,
                            "schema_version_matches": True,
                            "evaluator_executability_status": (
                                "passed_registered_query_execution"
                            ),
                            "continuous_prediction_validity_status": (
                                "evaluated_descriptive_no_public_binary_threshold"
                            ),
                            "normalized_mae": 0.1,
                        },
                    }
                )
    return rows


def _legacy_ae_analysis(
    rows: list[dict[str, object]], execution_manifest_sha256: str
) -> tuple[dict[str, object], str]:
    cluster_rows = []
    cluster_ids = sorted({str(row["world_cluster_id"]) for row in rows})
    for cluster_id in cluster_ids:
        cells = [row for row in rows if row["world_cluster_id"] == cluster_id]
        by_arm = {str(row["prior_arm"]): row for row in cells}
        contrast = build_cluster_correction_record(
            {
                arm: by_arm[arm]["checkpoint_error"]
                for arm in WORK_II_ANALYSIS_ARMS
            }
        )
        cluster_rows.append(
            {
                "world_cluster_id": cluster_id,
                "task_id": cells[0]["task_id"],
                "complete_case": True,
                **contrast,
            }
        )
    dataset: dict[str, object] = {
        "schema_version": "chemworld-work-ii-formal-analysis-dataset-0.1",
        "formal_result": True,
        "status": "passed",
        "formal_preflight_sha256": execution_manifest_sha256,
        "retained_cell_count": 75,
        "cluster_contrast_count": 25,
        "state_counts": {"completed": 75, "right_censored": 0, "failed": 0},
        "cell_rows": rows,
        "cluster_rows": cluster_rows,
        "errors": [],
    }
    dataset["dataset_sha256"] = _hash(dataset)
    plan = json.loads(ANALYSIS_PLAN.read_text(encoding="utf-8"))
    return build_confirmatory_analysis(dataset, plan), str(dataset["dataset_sha256"])


def _locus_report(
    manifest: dict[str, object],
    locus: str,
    *,
    task_effects: dict[str, float] | None = None,
) -> dict[str, object]:
    block = manifest["blocks"][locus]
    rows = _cell_rows(locus, task_effects=task_effects)
    legacy = None
    dataset_sha256 = _hash([locus, "analysis-dataset"])
    if locus == "A_E":
        legacy, dataset_sha256 = _legacy_ae_analysis(
            rows, str(block["execution_manifest_sha256"])
        )
        _bind_legacy_to_manifest(manifest, legacy)
    report: dict[str, object] = {
        "schema_version": PUBLIC_C2_LOCUS_REPORT_VERSION,
        "report_id": block["analysis_report_id"],
        "locus_id": locus,
        "status": "passed",
        "formal_result": True,
        "errors": [],
        "analysis_provider_call_count": 0,
        "source_c2_manifest_sha256": manifest["manifest_sha256"],
        "execution_manifest_sha256": block["execution_manifest_sha256"],
        "source_analysis_dataset_sha256": dataset_sha256,
        "runtime_commit": manifest["runtime_commit"],
        "analysis_source_manifest_sha256": _hash(
            manifest["analysis_source_sha256"]
        ),
        "scheduled_cell_count": len(rows),
        "retained_cell_count": len(rows),
        "independent_cluster_count": len(rows) // 3,
        "cell_rows": rows,
        "legacy_A_E_confirmatory_analysis": legacy,
    }
    report["report_sha256"] = _hash(report)
    return report


def _inputs() -> tuple[dict[str, object], dict[str, dict[str, object]]]:
    manifest = _manifest()
    reports = {locus: _locus_report(manifest, locus) for locus in LOCUS_IDS}
    for locus in ("A_P", "A_S"):
        reports[locus]["source_c2_manifest_sha256"] = manifest["manifest_sha256"]
        _rehash(reports[locus], "report_sha256")
    return manifest, reports


def test_positive_public_c2_fixture_passes_all_three_locus_gates() -> None:
    manifest, reports = _inputs()
    first = build_public_c2_analysis(manifest, reports)
    second = build_public_c2_analysis(manifest, reports)

    assert first == second
    assert validate_public_c2_manifest(manifest) == []
    analysis_plan = json.loads(ANALYSIS_PLAN.read_text(encoding="utf-8"))
    assert validate_public_c2_analysis_plan(manifest, analysis_plan) == []
    assert analysis_plan["public_C2_confirmatory_extension"] == PUBLIC_C2_PLAN_CONTRACT
    assert validate_public_c2_analysis(
        first, manifest=manifest, locus_reports=reports
    ) == []
    assert first["denominators"]["task_count"] == 9
    assert first["denominators"]["independent_cluster_count"] == 45
    assert first["denominators"]["retained_cell_count"] == 135
    assert first["denominators"]["failure_count"] == 0
    assert first["locus_results"]["A_E"]["gate"][
        "legacy_decision_reproduced_from_bound_rows"
    ] is True
    assert first["locus_results"]["A_P"]["gate"][
        "both_tasks_direction_consistent"
    ] is True
    assert first["C2_intersection_union"]["passed"] is True
    assert first["C2_intersection_union"]["naive_nine_task_pooling_performed"] is False


def test_locus_report_builder_emits_valid_manifest_bound_ap_report() -> None:
    manifest, reports = _inputs()
    existing = reports["A_P"]
    built = build_locus_cell_report(
        manifest=manifest,
        locus="A_P",
        source_analysis_dataset_sha256=existing[
            "source_analysis_dataset_sha256"
        ],
        cell_rows=existing["cell_rows"],
    )

    assert built == existing
    assert built["source_c2_manifest_sha256"] == manifest["manifest_sha256"]


def test_zero_variance_tail_rules_and_terminal_locus_residual_df_are_frozen() -> None:
    manifest, reports = _inputs()
    result = build_public_c2_analysis(manifest, reports)

    ap = result["locus_results"]["A_P"]["gate"]["inference"]
    assert ap["residual_degrees_of_freedom"] == 8
    assert ap["standard_error"] <= 1.0e-15
    assert ap["t_statistic"] == "Infinity"
    assert ap["one_sided_p_value"] == 0.0
    assert ap["one_sided_95pct_lower_bound"] == pytest.approx(ap["estimate"])

    reports["A_P"] = _locus_report(
        manifest,
        "A_P",
        task_effects={"ap-task-0": 0.0, "ap-task-1": 0.0},
    )
    equal_null = build_public_c2_analysis(manifest, reports)
    ap_equal = equal_null["locus_results"]["A_P"]["gate"]["inference"]
    assert ap_equal["standard_error"] <= 1.0e-15
    assert ap_equal["t_statistic"] == 0.0
    assert ap_equal["one_sided_p_value"] == 0.5
    assert ap_equal["passed"] is False


def test_iut_p_value_is_maximum_of_effective_locus_gate_p_values() -> None:
    manifest, reports = _inputs()
    reports["A_S"] = _locus_report(
        manifest,
        "A_S",
        task_effects={"as-task-0": 0.45, "as-task-1": -0.05},
    )
    result = build_public_c2_analysis(manifest, reports)

    p_values = result["C2_intersection_union"]["locus_p_values"]
    assert p_values["A_S"] == 1.0
    assert result["C2_intersection_union"]["intersection_union_p_value"] == max(
        p_values.values()
    )
    assert result["C2_intersection_union"]["passed"] is False


def test_one_negative_ap_task_blocks_c2_even_when_grand_mean_is_positive() -> None:
    manifest, reports = _inputs()
    reports["A_P"] = _locus_report(
        manifest,
        "A_P",
        task_effects={"ap-task-0": 0.45, "ap-task-1": -0.05},
    )
    result = build_public_c2_analysis(manifest, reports)

    gate = result["locus_results"]["A_P"]["gate"]
    assert gate["inference"]["estimate"] > 0.0
    assert gate["both_tasks_direction_consistent"] is False
    assert gate["effective_intersection_union_p_value"] == 1.0
    assert gate["passed"] is False
    assert result["C2_intersection_union"]["passed"] is False


def test_failed_arm_is_retained_with_symmetric_adverse_bound_and_blocks_c2() -> None:
    manifest, reports = _inputs()
    failed = reports["A_S"]["cell_rows"][2]
    failed["terminal_state"] = "failed"
    failed["terminal_reason_code"] = "participant_method_failure"
    failed["checkpoint_error"]["primary_improvement"] = 0.0
    failed["checkpoint_error"]["confirmatory_improvement_bounds"] = [-1.0, 1.0]
    failed["checkpoint_error"]["missing_failure_rule"] = (
        "missing_final_with_valid_pre_sets_zero_improvement"
    )
    _rehash(reports["A_S"], "report_sha256")

    result = build_public_c2_analysis(manifest, reports)
    assert result["denominators"]["retained_cell_count"] == 135
    assert result["denominators"]["failure_count"] == 1
    assert result["denominators"]["by_locus"]["A_S"][
        "non_complete_case_cluster_count"
    ] == 1
    assert result["all_retained_failures"][0]["confirmatory_improvement_bounds"] == [
        -1.0,
        1.0,
    ]
    assert result["locus_results"]["A_S"]["gate"]["passed"] is False
    assert result["C2_intersection_union"]["passed"] is False


def test_noncompleted_arm_with_point_bound_is_rejected_fail_closed() -> None:
    manifest, reports = _inputs()
    failed = reports["A_P"]["cell_rows"][2]
    failed["terminal_state"] = "failed"
    failed["terminal_reason_code"] = "participant_method_failure"
    _rehash(reports["A_P"], "report_sha256")

    with pytest.raises(
        WorkIIPublicC2AnalysisError,
        match="failed outcome lacks symmetric adverse bounds",
    ):
        build_public_c2_analysis(manifest, reports)


def test_manifest_dataset_receipt_and_ae_legacy_tampering_are_rejected() -> None:
    manifest, reports = _inputs()
    reports["A_S"]["source_analysis_dataset_sha256"] = "bad"
    _rehash(reports["A_S"], "report_sha256")
    with pytest.raises(WorkIIPublicC2AnalysisError, match="dataset binding is invalid"):
        build_public_c2_analysis(manifest, reports)


def test_analysis_plan_hash_or_c2_extension_drift_is_rejected() -> None:
    manifest = _manifest()
    analysis_plan = json.loads(ANALYSIS_PLAN.read_text(encoding="utf-8"))
    analysis_plan["public_C2_confirmatory_extension"]["global_intersection_union"][
        "overall_p_value"
    ] = "minimum"

    errors = validate_public_c2_analysis_plan(manifest, analysis_plan)
    assert "public C2 analysis-plan hash binding mismatch" in errors
    assert "public C2 analysis-plan extension drifted" in errors


def test_source_file_validator_binds_materialized_analysis_code(tmp_path: Path) -> None:
    manifest = _manifest()
    for relative in ANALYSIS_SOURCE_PATHS:
        path = tmp_path / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(relative, encoding="utf-8")
        manifest["analysis_source_sha256"][relative] = file_sha256(path)
    _rehash(manifest, "manifest_sha256")
    assert validate_public_c2_source_files(manifest, root=tmp_path) == []

    changed = tmp_path / ANALYSIS_SOURCE_PATHS[0]
    changed.write_text("changed", encoding="utf-8")
    assert any(
        "analysis source hash mismatch" in error
        for error in validate_public_c2_source_files(manifest, root=tmp_path)
    )


def test_receipt_and_ae_legacy_tampering_are_rejected() -> None:
    manifest, reports = _inputs()
    reports["A_P"]["cell_rows"][0]["terminal_receipt_sha256"] = "f" * 63
    _rehash(reports["A_P"], "report_sha256")
    with pytest.raises(WorkIIPublicC2AnalysisError, match="terminal_receipt_sha256"):
        build_public_c2_analysis(manifest, reports)

    manifest, reports = _inputs()
    reports["A_E"]["legacy_A_E_confirmatory_analysis"]["primary_H3"]["passed"] = False
    _rehash(
        reports["A_E"]["legacy_A_E_confirmatory_analysis"], "report_sha256"
    )
    _rehash(reports["A_E"], "report_sha256")
    with pytest.raises(
        WorkIIPublicC2AnalysisError,
        match="legacy report differs from its C2 manifest binding",
    ):
        build_public_c2_analysis(manifest, reports)


def test_rehashed_ae_legacy_iut_or_claim_tampering_is_rejected() -> None:
    manifest, reports = _inputs()
    legacy = reports["A_E"]["legacy_A_E_confirmatory_analysis"]
    legacy["primary_H3"]["intersection_union_p_value"] = 0.5
    legacy["claim_decisions"][
        "selective_evidence_driven_wrong_prior_correction"
    ] = False
    _rehash(legacy, "report_sha256")
    _bind_legacy_to_manifest(manifest, legacy)
    for locus in LOCUS_IDS:
        reports[locus]["source_c2_manifest_sha256"] = manifest["manifest_sha256"]
        _rehash(reports[locus], "report_sha256")

    with pytest.raises(
        WorkIIPublicC2AnalysisError,
        match="report structure or claim decision is inconsistent",
    ):
        build_public_c2_analysis(manifest, reports)


def test_output_validator_detects_rehashed_claim_and_iut_tampering() -> None:
    manifest, reports = _inputs()
    result = build_public_c2_analysis(manifest, reports)
    result["C2_intersection_union"]["passed"] = False
    result["claim_decision"]["cross_locus_initial_world_model_effects_supported"] = False
    result["claim_decision"]["highest_public_claim_scope"] = "below_C2"
    _rehash(result, "report_sha256")

    errors = validate_public_c2_analysis(result)
    assert "public C2 intersection-union decision mismatch" in errors
    assert "public C2 claim decision mismatch" in errors
    assert "public C2 report differs from its bound raw inputs" in validate_public_c2_analysis(
        result,
        manifest=manifest,
        locus_reports=reports,
    )


def test_output_validator_detects_rehashed_embedded_gate_and_scope_tampering() -> None:
    manifest, reports = _inputs()
    result = build_public_c2_analysis(manifest, reports)
    result["locus_results"]["A_P"]["gate"]["passed"] = False
    result["claim_decision"]["highest_public_claim_scope"] = "below_C2"
    _rehash(result, "report_sha256")

    errors = validate_public_c2_analysis(result)
    assert "public C2 A_P embedded gate decision mismatch" in errors
    assert "public C2 highest public claim scope mismatch" in errors


def test_duplicate_cell_or_receipt_identity_across_loci_is_rejected() -> None:
    manifest, reports = _inputs()
    reports["A_S"]["cell_rows"][0]["cell_id"] = reports["A_P"]["cell_rows"][0][
        "cell_id"
    ]
    _rehash(reports["A_S"], "report_sha256")

    with pytest.raises(WorkIIPublicC2AnalysisError, match="globally unique"):
        build_public_c2_analysis(manifest, reports)
