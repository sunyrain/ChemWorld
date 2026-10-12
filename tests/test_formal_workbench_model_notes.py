from __future__ import annotations

import time

import pytest
from scripts import run_formal_workbench_model_notes as study


@pytest.mark.parametrize("unit", [1, 2, 3])
def test_full_physical_path_then_model_notes_and_report(tmp_path, unit):
    host = study.Host(tmp_path, unit, time.time() + 120)
    try:
        initial = host.call("lab_status", {})
        assert "recipe" not in initial and "notebook" in initial
        host.call("notebook_write", {"text": "Before actions: prediction, not fact."})
        for action in host.run.data["recipe"]:
            result = host.call("lab_step", {"action": action})
            assert result["transaction_status"] == "committed"
        assert host.run.env is None
        assert host.run.data["status"] == "completed"
        assert host.call("lab_status", {})["physical_status"] == "completed"
        host.call("notebook_read", {})
        host.call("notebook_write", {"text": "After assay: observed evidence and limitations."})
        assert host.call("finish_batch", {"report": "Evidence summary."})["finished"]
        assert host.run.data["status"] == "completed"
    finally:
        host.close()
    result = study.summarize(
        tmp_path,
        unit,
        {
            "usage": {"input_tokens": 12, "output_tokens": 8},
            "usage_complete": True,
            "exit_code": 0,
            "stop_reason": None,
            "elapsed_s": 1,
            "transport_failures": [],
        },
    )
    assert result["engineering_passed"] and result["notebook_passed"]
    assert result["notebook_versions"] == 2 and result["replay"]["verified"]
    assert result["host"]["calls"] == sum(result["tool_counts"].values())


def test_errors_consume_tool_budget_and_notes_do_not_unlock_physics(tmp_path):
    host = study.Host(tmp_path, 1, time.time() + 120)
    try:
        assert "error" in host.call("unknown", {})
        assert host.result["calls"] == 1
        assert host.call("lab_history", {}) == {"total": 0, "events": []}
        host.result["calls"] = study.CALLS
        assert "error" in host.call("notebook_write", {"text": "over budget"})
        assert not host.run.notebook("model", "log", {})["revisions"]
    finally:
        host.close()


def test_platform_rollback_stops_physics_but_allows_report(tmp_path, monkeypatch):
    host = study.Host(tmp_path, 1, time.time() + 120)
    try:
        monkeypatch.setattr(host.run, "step", lambda action: {"transaction_status": "rolled_back"})
        assert host.call("lab_step", {"action": {}})["transaction_status"] == "rolled_back"
        assert host.result["platform_failure"]
        assert "error" in host.call("lab_step", {"action": {}})
        host.call("notebook_write", {"text": "Platform failure; no valid result."})
        assert host.call("finish_batch", {"report": "Failure retained."})["finished"]
        assert host.run.data["status"] == "failed"
    finally:
        host.close()


def test_dispatch_exposes_only_native_public_tools(tmp_path):
    host = study.Host(tmp_path, 1, time.time() + 120)
    try:
        response = study.dispatch(host, {"id": 1, "method": "tools/list"})
        assert response["result"]["tools"] == study.definitions()
        schema = host.call("lab_schema", {"operations": ["heat", "measure"]})
        assert set(schema) == {"heat", "measure"}
        assert "error" in host.call("lab_measurement", {"event_id": "../../run"})
    finally:
        host.close()
