"""Reporting arithmetic, missingness and privacy checks; no scientific experiments."""

import csv
import json

import pytest
from scripts import report_unified_matrices as report


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data), encoding="utf-8")


def design(tmp_path):
    units = []
    for repeat in range(1, 4):
        for world in range(1, 6):
            for system in ("EC", "RX", "PA", "P", "C"):
                goals = ("discovery", "optimization") if system in {"EC", "RX"} else ("discovery",)
                arms = ("Opaque", "Aligned", "MisIndexed") if system != "C" else ("Opaque",)
                opportunities = ("Research", "NoResearch") if system == "C" else ("Research",)
                for goal in goals:
                    for arm in arms:
                        for opportunity in opportunities:
                            units.append(
                                {
                                    "repeat": f"repeat-{repeat:02d}",
                                    "world": f"{system}-W{world:02d}",
                                    "system": system,
                                    "goal": goal,
                                    "arm": arm,
                                    "opportunity": opportunity,
                                    "matrix": "A"
                                    if system in {"EC", "RX"}
                                    else "C"
                                    if system == "C"
                                    else "B",
                                    "batches": 0 if opportunity == "NoResearch" else 12,
                                    "id": f"{system}-W{world:02d}-{goal}-{arm}-{opportunity}",
                                }
                            )
    write(tmp_path / "design.json", {"schedule": units, "planned_sessions": 300})
    return units


def result(tmp_path, unit, *, mae=0.2, status="completed", missing_stage=None):
    level = 90 if unit["system"] == "PA" else 80
    metrics = {}
    for metric in report.METRICS[unit["system"]]:
        row = {"n": 12, "mae": mae, f"coverage{level}": 0.5, f"mean_width{level}": 0.3}
        if unit["system"] == "P":
            row["width80"] = row.pop("mean_width80")
        if unit["system"] == "C":
            row["interval_width"] = row.pop("mean_width80")
        if unit["system"] == "RX":
            row = {
                "query_count": 12,
                "reference_observation_count": 60,
                "mae_to_five_repeat_mean": mae,
                "empirical_coverage80": 0.5,
                "mean_width80": 0.3,
                "mean_interval_score_alpha_0_2": 0.4,
            }
        metrics[metric] = row
    native = {
        **unit,
        "status": status,
        "source": {"batches": [{}] * unit["batches"], "exact_replay": {"verified": True}},
        "posttests": {
            s: {"payload": {"report": "PRIVATE_PROVIDER_PAYLOAD"}} for s in report.STAGES
        },
        "prediction_evaluation": {"valid": True, "metrics": metrics},
    }
    if missing_stage:
        native["posttests"].pop(missing_stage)
    folder = tmp_path / unit["repeat"] / unit["id"]
    write(folder / "result.json", native)
    write(folder / "status.json", {"status": status})
    return folder, native


def test_partial_report_retains_all_300_and_missing_metrics(tmp_path):
    units = design(tmp_path)
    result(tmp_path, units[0])
    summary, rows, _ = report.build_report(tmp_path)
    assert summary["phase"] == "partial"
    assert summary["counts"]["planned_sessions"] == 300
    assert summary["counts"]["terminal_sessions"] == 1
    assert summary["counts"]["missing_forecasts"] == 299
    assert summary["counts"]["planned_source_batches"] == 3420
    assert len(rows) == 1380
    absent = next(r for r in rows if r["id"] != units[0]["id"])
    assert absent["mae"] is None
    assert absent["metric_available"] is False


def test_retained_units_read_original_outputs_without_replacement(tmp_path):
    current = tmp_path / "current"
    original = tmp_path / "original"
    units = design(current)
    base, _ = result(original, units[0])
    path = current / "design.json"
    metadata = json.loads(path.read_text())
    metadata["retained_units"] = {f"{units[0]['repeat']}/{units[0]['id']}": str(base)}
    write(path, metadata)
    summary, rows, _ = report.build_report(current)
    assert summary["counts"]["terminal_sessions"] == 1
    retained_row = next(r for r in rows if r["id"] == units[0]["id"])
    assert retained_row["result_path"] == str(base / "result.json")
    assert not (current / units[0]["repeat"]).exists()


def test_service_retry_attempts_are_separate_from_planned_units(tmp_path):
    design(tmp_path)
    write(
        tmp_path / "service-retries.json",
        {
            "status": "running",
            "final": {"service_retry_attempts": 7, "retried_units": 5},
            "rounds": [{"failure": "PRIVATE_PROVIDER_PAYLOAD"}],
        },
    )
    summary, _, _ = report.build_report(tmp_path)
    assert summary["counts"]["planned_sessions"] == 300
    assert summary["service_retries"]["service_retry_attempts"] == 7
    assert summary["service_retries"]["retried_units"] == 5
    assert not summary["execution_complete"]
    assert "PRIVATE_PROVIDER_PAYLOAD" not in json.dumps(summary)
    assert "additional technical attempts: 7" in report.markdown(summary)


def test_terminal_primary_is_not_complete_while_service_retries_are_pending(tmp_path):
    units = design(tmp_path)
    for unit in units:
        base = tmp_path / unit["repeat"] / unit["id"]
        write(base / "status.json", {"status": "incomplete"})
        write(base / "result.json", {"status": "failed", "source": {}})
    write(tmp_path / "service-retries.json", {"status": "running", "final": {}})
    summary, _, _ = report.build_report(tmp_path)
    assert summary["primary_units_terminal"]
    assert summary["phase"] == "service_retries"
    assert not summary["execution_complete"]


def test_available_world_means_do_not_weight_world_by_completion_count(tmp_path):
    units = design(tmp_path)
    selected = [u for u in units if u["system"] == "PA" and u["arm"] == "Opaque"]
    for u in selected:
        if u["world"].endswith("01"):
            result(tmp_path, u, mae=0.1)
        elif u["world"].endswith("02") and u["repeat"] == "repeat-01":
            result(tmp_path, u, mae=0.9)
    summary, _, _ = report.build_report(tmp_path)
    row = next(r for r in summary["metrics"] if r["system"] == "PA" and r["arm"] == "Opaque")
    assert row["mae_world_equal_available"] == pytest.approx(0.5)
    assert row["mae_world_equal_available"] != pytest.approx(0.3)
    assert row["available_sessions"] == 4
    assert row["planned_sessions"] == 15
    assert row["observed_worlds"] == 2
    assert row["planned_worlds"] == 5
    assert row["mae_world_equal_complete"] is None
    assert row["interval_level"] == 0.9


@pytest.mark.parametrize("system", ["EC", "RX", "PA", "P", "C"])
def test_native_field_mappings_keep_reference_denominators(tmp_path, system):
    units = design(tmp_path)
    unit = next(u for u in units if u["system"] == system)
    result(tmp_path, unit)
    _, rows, _ = report.build_report(tmp_path)
    row = next(r for r in rows if r["id"] == unit["id"] and r["repeat"] == unit["repeat"])
    assert row["mae"] == 0.2
    assert row["coverage"] == 0.5
    assert row["interval_width"] == 0.3
    assert row["interval_level"] == (0.9 if system == "PA" else 0.8)
    assert row["coverage_reference_count"] == (60 if system == "RX" else 12)


def test_invalid_c_partial_metric_is_not_imputed_or_included(tmp_path):
    units = design(tmp_path)
    unit = next(u for u in units if u["system"] == "C")
    folder, native = result(tmp_path, unit)
    native["prediction_evaluation"]["valid"] = False
    native["prediction_evaluation"]["metrics"]["crystal_yield"]["n"] = 11
    write(folder / "result.json", native)
    summary, rows, failures = report.build_report(tmp_path)
    assert summary["counts"]["usable_forecasts"] == 0
    assert all(r["mae"] is None for r in rows)
    assert any(r["category"] == "forecast_unavailable_or_invalid" for r in failures)


def test_valid_q_from_incomplete_session_retained_but_missing_q_excluded(tmp_path):
    units = design(tmp_path)
    result(tmp_path, units[0], status="incomplete", missing_stage="K2")
    result(tmp_path, units[1], status="incomplete", missing_stage="Q")
    summary, rows, failures = report.build_report(tmp_path)
    assert summary["counts"]["terminal_sessions"] == 2
    assert summary["counts"]["usable_forecasts"] == 1
    assert summary["counts"]["completed_sessions"] == 0
    assert any(r["status"] == "incomplete" and r["metric_available"] for r in rows)
    assert any(r["category"] == "missing_or_invalid_stage" and r["stage"] == "K2" for r in failures)


def test_outputs_exclude_raw_payload_and_private_error_text(tmp_path):
    units = design(tmp_path)
    folder, native = result(tmp_path, units[0], status="failed")
    native["failure"] = {"type": "provider_failure", "stage": "Q", "message": "SECRET_API_TOKEN"}
    write(folder / "result.json", native)
    summary, rows, failures = report.build_report(tmp_path)
    output = tmp_path / "analysis"
    report.write_outputs(output, summary, rows, failures)
    for p in output.iterdir():
        text = p.read_text(encoding="utf-8")
        assert "SECRET_API_TOKEN" not in text
        assert "PRIVATE_PROVIDER_PAYLOAD" not in text
    with (output / "session_metrics.csv").open(encoding="utf-8", newline="") as stream:
        exported = list(csv.DictReader(stream))
    assert len(exported) == len(rows)
    assert "result_path" in exported[0]
    assert any(r["mae"] == "" for r in exported)


def test_complete_execution_can_include_failure_and_recompute_without_replacement(tmp_path):
    units = design(tmp_path)
    for unit in units:
        write(tmp_path / unit["repeat"] / unit["id"] / "status.json", {"status": "failed"})
    summary, _, failures = report.build_report(tmp_path)
    assert summary["execution_complete"] is True
    assert summary["all_sessions_completed"] is False
    assert summary["counts"]["terminal_sessions"] == 300
    assert summary["counts"]["usable_forecasts"] == 0
    assert sum(r["category"] == "missing_terminal_result" for r in failures) == 300


def test_duplicate_or_reduced_design_rejected(tmp_path):
    units = design(tmp_path)
    write(tmp_path / "design.json", {"schedule": units[:-1]})
    with pytest.raises(ValueError, match="300"):
        report.build_report(tmp_path)


def test_identity_mismatch_excludes_numeric_result(tmp_path):
    units = design(tmp_path)
    folder, native = result(tmp_path, units[0])
    native["world"] = "EC-W99"
    write(folder / "result.json", native)
    summary, _, failures = report.build_report(tmp_path)
    assert summary["counts"]["usable_forecasts"] == 0
    assert any(r["category"] == "result_identity_mismatch" for r in failures)
