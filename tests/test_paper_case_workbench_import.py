import json

import pytest
from scripts import import_paper_case_workbench as importer

from chemworld.agents.experiment_documents import ExperimentDocumentWorkspace
from chemworld.workbench.service import ResearchStore, write_json


def test_import_preserves_public_events_notes_and_reports_without_private_state(
    tmp_path, monkeypatch
):
    source = tmp_path / "source"
    documents = ExperimentDocumentWorkspace(source / "notebook", versioned_notebook=True)
    documents.initialize()
    documents.notebook_tool("write", text="Before any action")
    rows = []
    for i in range(2):
        action = {"operation": "measure", "instrument": "final_assay"}
        documents.append_operation(
            {
                "event_id": f"runner-operation-{i + 1:04d}",
                "action": action,
                "transaction_status": "committed",
                "observation": {"yield": 0.4 + i / 10},
                "observed_keys": ["yield"],
                "ok": True,
            }
        )
        rows.append(
            {
                "action": action,
                "experiment_index": i,
                "timestamp": "2026-10-13T00:00:00Z",
                "task_id": "reaction-to-assay",
                "seed": 0,
                "budget": 100,
                "agent_view": {"tool_json": {"campaign_state": {"operation_count": 2}}},
                "private_truth": "do not copy",
                "raw_signal": {"private": "not public"},
            }
        )
    documents.notebook_tool("write", text="After both batches")
    (source / "trajectory.jsonl").write_text(
        "\n".join(json.dumps(r) for r in rows), encoding="utf-8"
    )
    case = {"id": "EC-discovery", "batches": 2, "cell": "example", "model": "example"}
    reports = tmp_path / "reports"
    write_json(
        reports / "EC-discovery.json",
        {
            "status": "completed",
            "operations": 2,
            "completed_batches": 2,
            "elapsed_s": 5,
            "token_accounting": {
                "complete": True,
                "total": {"input_tokens": 100, "output_tokens": 20},
            },
            "exact_replay": {"verified": True, "checked_steps": 2, "max_abs_error": 0},
            "posttests": {"K1": {"payload": {"report": "Model report"}}},
            "notebook": {"tool_failures": 1},
            "source_usage": {"recovered_mcp_tool_failure_count": 0},
        },
    )
    monkeypatch.setattr(importer, "case_folder", lambda *_: source)
    destination = tmp_path / "store"
    record = importer.import_case(source, reports, destination, case)
    store = ResearchStore(destination)
    try:
        run = store.get(record["id"])
        snapshot = run.snapshot()
        assert snapshot["batch_count"] == 2 and snapshot["final_assay_count"] == 2
        assert [e["batch"] for e in snapshot["events"]] == [1, 2]
        assert snapshot["events"][0]["observation"] == {"yield": 0.4}
        assert "do not copy" not in json.dumps(snapshot)
        assert not (run.root / "trajectory.jsonl").exists()
        assert not (run.root / "measurements").exists()
        assert run.notebook("model", "read", {"revision": 1})["text"] == "Before any action"
        assert run.notebook("model", "read", {"revision": 2})["public_cursor"]["event_count"] == 2
        assert "Model report" in snapshot["sealed_reports"][0]["text"]
        assert snapshot["sealed_reports"][0]["payload"] == {"report": "Model report"}
        with pytest.raises(ValueError, match="Imported campaign"):
            run.replay()
        with pytest.raises(ValueError, match="not active"):
            run.step({"operation": "wait"})
        assert (
            importer.import_case(source, reports, destination, case)["status"] == "already_imported"
        )
        assert len(list(destination.glob("*/run.json"))) == 1
    finally:
        store.close()
