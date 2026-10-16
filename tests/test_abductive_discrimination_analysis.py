import pytest
from scripts import analyze_abductive_discrimination as s


def test_missing_q_is_not_zero_error():
    assert s.prediction_rows({"prediction_evaluation": {"valid": False}}, {}) == []


def test_query_error_and_coverage_use_repeated_observations():
    session = {
        "repeat": "repeat-01",
        "id": "test",
        "pair": "P01",
        "mechanism": "A",
        "prediction_evaluation": {"valid": True},
        "posttests": {
            "Q": {
                "payload": {
                    "predictions": [
                        {
                            "query_id": "Q01",
                            "rationale": "test",
                            "metrics": {
                                "pH_normalized": {"estimate": 0.4, "lower80": 0.35, "upper80": 0.45}
                            },
                        }
                    ]
                }
            }
        },
    }
    rows = s.prediction_rows(
        session, {"Q01": [{"pH_normalized": 0.3}, {"pH_normalized": 0.4}, {"pH_normalized": 0.5}]}
    )
    assert rows[0]["absolute_error"] == pytest.approx(0)
    assert rows[0]["empirical_coverage80"] == pytest.approx(1 / 3)
    assert rows[0]["reference_repeats"] == 3


def test_worker_exit_keeps_all_planned_sessions_and_failure(tmp_path):
    root, report = tmp_path / "raw", tmp_path / "report"
    schedule = s.run.schedule(s.run.build_config())
    s.write(root / "design.json", {"source_commit": "test", "schedule": schedule})
    failed = schedule[0]
    s.write(
        root / "block-stop.json",
        {"unit": [failed["repeat"], failed["id"]], "reason": "retained worker process exit1"},
    )
    summary = s.analyze(root, report)
    assert summary["planned_sessions"] == 30
    assert summary["terminal_sessions"] == 1
    assert summary["session_statuses"] == {"worker_startup_failure": 1, "not_started": 29}
    assert summary["completed_source_assays"] == 0
    assert summary["semantic_review_summary"] == "reading-summary.json"
    assert summary["resource_summary"] == "resource-summary.json"
    assert summary["automatic_semantic_classification"] is False
    assert "semantically_reviewed_sessions" not in summary
    case = s.read(report / "sessions" / failed["repeat"] / f"{failed['id']}.json")
    assert case["result_origin"] == "retained_worker_exit_marker"
    assert case["failure"] == "retained worker process exit1"
    assert case["semantic_review_file"] == "semantic_repeat01.json"
    assert case["automatic_semantic_classification"] is False
    assert "semantic_coding" not in case
