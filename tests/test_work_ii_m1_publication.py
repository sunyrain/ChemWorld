"""The publication export preserves results while excluding raw provider identities/events."""

import json

import pytest
from scripts.export_work_ii_m1_report import export_report
from scripts.run_work_ii_factorial import seal


def test_scientific_export_preserves_scores_and_excludes_raw_provider_content(tmp_path):
    root, out = tmp_path / "retained", tmp_path / "report.json"
    report = {
        "execution_valid": True,
        "interpretation": "Fixture only.",
        "physical_completed": 200,
        "exact_replay_completed": 200,
        "provider_completed": 120,
        "condition_completed": 160,
        "condition_scheduled": 160,
        "statistics": None,
        "provider_resources_by_stage": [],
        "failures": [],
        "slots": [{"failure_aware_regret": 0.0123}],
    }
    seal(root / "summary.json", report)
    seal(root / "protocol.json", {"worlds": [{"cluster_id": "world"}]})
    seal(
        root / "physical.json",
        {
            "receipts": [
                {"task": "fixture", "id": "e01", "status": "completed", "wall_s": 2},
                {"task": "fixture", "id": "c01", "status": "completed", "wall_s": 3},
            ]
        },
    )
    seal(root / "private_scores.json", {"world": {"c01": 0.123}})
    seal(root / "public/world.json", {"evidence": [{"score": 0.234}]})
    seal(
        root / "selections.json",
        {
            "artifacts": {"state": {"L": [0.1] * 6}},
            "calls": [
                {
                    "call_id": "call",
                    "status": "completed",
                    "usage": {"input_tokens": 45},
                    "thread_id": "SECRET_CANARY",
                    "raw_events": ["SECRET_CANARY"],
                    "environment": {"api_key": "SECRET_CANARY"},
                }
            ],
        },
    )
    exported = export_report(root, out)
    assert {key: exported[key] for key in report} == report
    assert exported["scientific_source_data"]["candidate_scores_after_selections_sealed"] == {
        "world": {"c01": 0.123}
    }
    assert exported["scientific_source_data"]["provider_calls"][0]["usage"]["input_tokens"] == 45
    assert "SECRET_CANARY" not in json.dumps(exported)
    assert [row["wall_s"] for row in exported["physical_resources_by_role"]] == [2, 3]
    assert json.loads((root / "summary.json").read_text(encoding="utf-8")) == report
    assert export_report(root, out) == exported
    changed = dict(exported, slots=[{"failure_aware_regret": 0.5}])
    out.write_text(json.dumps(changed), encoding="utf-8")
    with pytest.raises(ValueError, match="different sealed result"):
        export_report(root, out)
    assert json.loads(out.read_text(encoding="utf-8")) == changed
