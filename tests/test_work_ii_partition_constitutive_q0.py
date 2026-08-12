from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

from scripts.run_work_ii_partition_constitutive_q0 import (
    _measurement,
    compile_actions,
    constitutive_audit,
)

from chemworld.eval.provenance import canonical_json_sha256, file_sha256
from chemworld.eval.work_ii_partition_constitutive_q0 import (
    BASELINE_EXPONENT,
    DECLARED_SIGMA,
    INSTRUMENTS,
    LAW_IDS,
    METRICS,
    POWER_RESPONSE_EXPONENT,
    QUALIFICATION_VERSION,
    SUMMARY_VERSION,
    TASK_ID,
    TASK_REPORT_VERSION,
    analyze,
    constitutive_intervention,
    effect_gate,
    frozen_action_plan,
    noise_coordinate,
    registered_cells,
    summary_sha256,
    task_report_sha256,
    validate_summary,
    validate_task_report,
)


def _audit() -> dict[str, object]:
    audit = constitutive_audit()
    audit["execution_constitutive_binding_matches"] = True
    return audit


def _source_binding() -> dict[str, object]:
    return {
        "schema_version": "chemworld-work-ii-c2-source-binding-0.1",
        "tested_commit": "a" * 40,
        "material_tree": {
            "relative_roots": [],
            "excluded_relative_paths": [],
            "sha256": "b" * 64,
        },
    }


def _rows() -> list[dict[str, object]]:
    audit = constitutive_audit()
    rows = []
    for cell in registered_cells():
        load = int(cell["load_index"])
        phase = int(cell["phase_volume_index"])
        baseline_organic = 0.25 - 0.04 * load + 0.08 * phase
        law_gap = 0.04 * (load + 1) * (phase + 1)
        for law_id in LAW_IDS:
            organic = baseline_organic + (law_gap if law_id == LAW_IDS[1] else 0.0)
            measurements = {
                instrument: {
                    "product_in_organic": organic,
                    "product_in_aqueous": 0.95 - organic,
                    "phase_ratio": 0.20 - 0.02 * load + 0.10 * phase,
                }
                for instrument in INSTRUMENTS
            }
            rows.append(
                {
                    **cell,
                    "task_id": TASK_ID,
                    "world_seed": 0,
                    "law_id": law_id,
                    "status": "completed",
                    "safe": True,
                    "measurements": measurements,
                    "observed_masks": {
                        instrument: dict.fromkeys(METRICS, True)
                        for instrument in INSTRUMENTS
                    },
                    "action_plan_sha256": canonical_json_sha256(
                        frozen_action_plan(cell)
                    ),
                    "observation_coordinate_sha256": {
                        instrument: canonical_json_sha256(
                            noise_coordinate(str(cell["cell_id"]), instrument).to_audit_dict()
                        )
                        for instrument in INSTRUMENTS
                    },
                    "noise_key_sha256": {
                        instrument: noise_coordinate(
                            str(cell["cell_id"]), instrument
                        ).key_sha256
                        for instrument in INSTRUMENTS
                    },
                    "constitutive_intervention_hash": (
                        None
                        if law_id == LAW_IDS[0]
                        else audit["power_response_intervention_hash"]
                    ),
                    "task_contract_hash": audit["baseline_public_task_contract_hash"],
                    "mechanism_hash": audit["baseline_mechanism_hash"],
                    "exact_replay": True,
                    "participant_visible_leakage_matches": [],
                    "participant_visible_payload": {"measurements": measurements},
                }
            )
    return rows


def _task_report() -> dict[str, object]:
    rows = _rows()
    audit = _audit()
    report: dict[str, object] = {
        "schema_version": TASK_REPORT_VERSION,
        "qualification_schema_version": QUALIFICATION_VERSION,
        "formal_result": False,
        "provider_call_count": 0,
        "participant_session_count": 0,
        "c2_source_binding": _source_binding(),
        "task_id": TASK_ID,
        "world_seed": 0,
        "frozen_exponents": {
            LAW_IDS[0]: BASELINE_EXPONENT,
            LAW_IDS[1]: POWER_RESPONSE_EXPONENT,
        },
        "constitutive_audit": audit,
        "rows": rows,
        "analysis": analyze(rows, audit),
    }
    report["report_sha256"] = task_report_sha256(report)
    return report


def _summary(report_path: Path, report: dict[str, object], root: Path) -> dict[str, object]:
    analysis = report["analysis"]
    assert isinstance(analysis, dict)
    summary: dict[str, object] = {
        "schema_version": SUMMARY_VERSION,
        "qualification_schema_version": QUALIFICATION_VERSION,
        "formal_result": False,
        "provider_call_count": 0,
        "participant_session_count": 0,
        "c2_source_binding": _source_binding(),
        "task_id": TASK_ID,
        "world_seed": 0,
        "coverage": {
            "law_ids": list(LAW_IDS),
            "grid_axes": {
                "aqueous_load_volume_L": [0.006, 0.015, 0.024],
                "extractant_phase_volume_L": [0.008, 0.019, 0.030],
            },
            "grid_cell_count": 9,
            "planned_execution_count": 18,
            "attempted_execution_count": 18,
        },
        "denominators": analysis["denominators"],
        "analysis": analysis,
        "platform_stop_triggered": False,
        "five_world_provider_free_expansion_authorized": True,
        "participant_d1_authorized": False,
        "provider_execution_authorized": False,
        "decision": "proceed_to_unchanged_five_world_provider_free_qualification",
        "raw_binding": {
            "path": report_path.relative_to(root).as_posix(),
            "sha256": file_sha256(report_path),
            "report_sha256": report["report_sha256"],
        },
    }
    summary["summary_sha256"] = summary_sha256(summary)
    return summary


def test_frozen_constitutive_contract_and_grid() -> None:
    intervention = constitutive_intervention()
    change = intervention["constitutive_law_change"]
    assert isinstance(change, dict)
    assert BASELINE_EXPONENT == 1.0
    assert POWER_RESPONSE_EXPONENT == 1.75
    assert change == {
        "transform_id": "partition_power_response_stress_v1",
        "partition_coefficient_exponent_at_full_severity": 1.75,
    }
    cells = registered_cells()
    assert len(cells) == 9
    assert {cell["aqueous_volume_L"] for cell in cells} == {0.006, 0.015, 0.024}
    assert {cell["extractant_volume_L"] for cell in cells} == {0.008, 0.019, 0.030}
    assert all(
        effect_gate(instrument, metric)
        == max(0.03, 6.0 * DECLARED_SIGMA[instrument][metric])
        for instrument in INSTRUMENTS
        for metric in METRICS
    )


def test_compiled_action_plan_matches_the_frozen_protocol() -> None:
    actions = compile_actions(registered_cells()[0])
    assert actions == [
        {"operation": "add_solvent", "volume_L": 0.020, "solvent": 0},
        {"operation": "add_phase", "phase": "aqueous", "volume_L": 0.006},
        {"operation": "add_extractant", "extractant": 1, "volume_L": 0.008},
        {"operation": "mix", "duration_s": 420.0, "stirring_speed_rpm": 800.0},
        {"operation": "settle", "duration_s": 900.0},
        {"operation": "measure", "instrument": "hplc"},
        {"operation": "separate_phase", "target_phase": "organic"},
        {"operation": "measure", "instrument": "hplc"},
        {"operation": "terminate"},
        {"operation": "measure", "instrument": "final_assay"},
    ]


def test_measurement_uses_post_separation_hplc() -> None:
    records = []
    for value in (0.1, 0.7):
        records.append(
            {
                "transaction_status": "committed",
                "operation_type": "measure",
                "instrument": "hplc",
                "processed_estimate": dict.fromkeys(METRICS, value),
                "observed_mask": dict.fromkeys(METRICS, True),
            }
        )
    values, mask = _measurement(records, "hplc")
    assert values == dict.fromkeys(METRICS, 0.7)
    assert all(mask.values())


def test_analysis_accepts_two_axis_nonlinear_paired_signature() -> None:
    result = analyze(_rows(), _audit())
    assert result["passed"] is True
    assert result["checks"]["load_axis_observable"] is True
    assert result["checks"]["phase_volume_axis_observable"] is True
    assert result["checks"]["functional_form_signature_resolved"] is True
    assert len(result["supporting_cells"]) >= 2
    assert result["denominators"] == {
        "planned": 18,
        "attempted": 18,
        "completed": 18,
        "exact_replay": 18,
        "physical_failures": 0,
        "platform_failures": 0,
        "unsafe_completed": 0,
    }


def test_analysis_rejects_weak_or_unpaired_evidence() -> None:
    weak = _rows()
    for row in weak:
        if row["law_id"] == LAW_IDS[1]:
            paired = next(
                candidate
                for candidate in weak
                if candidate["cell_id"] == row["cell_id"]
                and candidate["law_id"] == LAW_IDS[0]
            )
            row["measurements"] = deepcopy(paired["measurements"])
    weak_result = analyze(weak, _audit())
    assert weak_result["passed"] is False
    assert "functional_form_signature_resolved" in weak_result["failures"]
    assert "at_least_two_supporting_cells" in weak_result["failures"]

    unpaired = _rows()
    unpaired[0]["noise_key_sha256"]["hplc"] = "not-paired"
    unpaired_result = analyze(unpaired, _audit())
    assert unpaired_result["passed"] is False
    assert "paired_hplc_noise" in unpaired_result["failures"]
    assert unpaired_result["channel_reports"] is None


def test_analysis_rejects_exponent_drift_and_incomplete_execution() -> None:
    drifted = _audit()
    drifted["power_response_exponent"] = 1.74
    assert "power_response_exponent_is_frozen" in analyze(_rows(), drifted)["failures"]

    incomplete = _rows()
    incomplete[0]["status"] = "physical_failure"
    result = analyze(incomplete, _audit())
    assert result["passed"] is False
    assert "all_executions_completed" in result["failures"]


def test_task_report_and_summary_validators_bind_raw_evidence(
    tmp_path: Path, monkeypatch: Any
) -> None:
    monkeypatch.setattr(
        "chemworld.eval.work_ii_partition_constitutive_q0.validate_c2_source_binding",
        lambda _root, binding: [] if binding == _source_binding() else ["wrong binding"],
    )
    report = _task_report()
    report_path = tmp_path / "raw" / "task-report.json"
    report_path.parent.mkdir()
    report_path.write_text(json.dumps(report, sort_keys=True), encoding="utf-8")
    summary = _summary(report_path, report, tmp_path)
    assert validate_task_report(report) == []
    assert validate_summary(summary, root=tmp_path) == []

    tampered = deepcopy(summary)
    tampered["decision"] = "retain_q0_scientific_rejection_and_do_not_expand"
    tampered["summary_sha256"] = summary_sha256(tampered)
    assert "partition constitutive Q0 decision mismatch" in validate_summary(tampered)

    report["rows"][0]["exact_replay"] = False
    report_path.write_text(json.dumps(report, sort_keys=True), encoding="utf-8")
    errors = validate_summary(summary, root=tmp_path)
    assert "partition constitutive Q0 raw file hash mismatch" in errors
    assert "partition constitutive Q0 task-report self-hash mismatch" in errors
