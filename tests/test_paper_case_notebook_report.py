import json

from scripts.report_paper_case_notebooks import (
    equilibrium_diagnostics,
    notebook_record,
    posttest_record,
    token_accounting,
)
from scripts.run_paper_case_notebooks import write

from chemworld.agents.campaign_notebook import CampaignNotebookServer


def test_export_flags_future_citation_without_rewriting_model_text(tmp_path):
    public = tmp_path / "public"
    public.mkdir()
    server = CampaignNotebookServer(public, tmp_path / "notebook")
    server._call_tool("notebook_write", {"text": "I measured runner-operation-0009."})
    report = notebook_record(tmp_path)
    assert report["versions"][0]["text"] == "I measured runner-operation-0009."
    assert report["validation"][0]["cursor_valid"] is True
    assert report["validation"][0]["unavailable_event_citations"] == ["runner-operation-0009"]


def test_only_usage_is_recovered_from_private_posttest_receipt(tmp_path):
    usage = {"input_tokens": 100, "cached_input_tokens": 20, "output_tokens": 10}
    write(
        tmp_path / "private-provider/Q/receipt.json",
        {
            "usage": usage,
            "thread_id": "private-session",
            "provider_payload": "private-body",
        },
    )
    record = posttest_record(tmp_path, "Q", {"payload": {"predictions": []}})
    assert record["usage"] == usage
    assert "private-session" not in str(record) and "private-body" not in str(record)
    assert posttest_record(tmp_path, "K1", {"failure": "interrupted"})["usage"] is None


def test_same_thread_usage_is_differenced_not_double_counted():
    source = {
        "provider_token_accounting_complete": True,
        "input_token_count": 100,
        "cached_input_token_count": 50,
        "output_token_count": 10,
    }
    turns = {
        stage: {
            "usage": {
                "input_tokens": 100 + 20 * i,
                "cached_input_tokens": 50 + 10 * i,
                "output_tokens": 10 + 5 * i,
            }
        }
        for i, stage in enumerate(("K1", "Q", "K2", "EQS"), 1)
    }
    accounting = token_accounting(source, turns, equilibrium=True)
    assert accounting["complete"] and accounting["valid"]
    assert accounting["total"]["input_plus_output"] == 210
    assert accounting["stage_deltas"][1]["input_tokens"] == 20
    assert token_accounting(source, {}, equilibrium=True)["complete"] is False


def test_concentration_uses_committed_additions_and_completed_batches(tmp_path):
    rows = [
        {
            "experiment_index": 0,
            "transaction_status": "committed",
            "action": {"operation": "add_reagent", "amount_mol": 0.01},
        },
        {
            "experiment_index": 0,
            "transaction_status": "rolled_back",
            "action": {"operation": "add_reagent", "amount_mol": 100},
        },
        {
            "experiment_index": 0,
            "transaction_status": "committed",
            "action": {"operation": "add_solvent", "volume_L": 0.1},
        },
        {
            "experiment_index": 0,
            "transaction_status": "committed",
            "instrument": "final_assay",
            "action": {"operation": "measure", "instrument": "final_assay"},
        },
        {
            "experiment_index": 1,
            "transaction_status": "committed",
            "action": {"operation": "add_solvent", "volume_L": 0.1},
        },
    ]
    (tmp_path / "trajectory.jsonl").write_text(
        "\n".join(json.dumps(r) for r in rows), encoding="utf-8"
    )
    result = equilibrium_diagnostics(tmp_path, tmp_path, {"system": "EQ"}, {})
    assert len(result["batch_concentrations"]) == 1
    assert abs(result["batch_concentrations"][0]["nominal_concentration_M"] - 0.1) < 1e-12
    assert result["prediction_groups"] is None
    rows += [
        {
            "experiment_index": 1,
            "transaction_status": "committed",
            "action": {"operation": "add_component", "component": 0, "amount_mol": 0.01},
        },
        {
            "experiment_index": 1,
            "transaction_status": "committed",
            "instrument": "final_assay",
            "action": {"operation": "measure", "instrument": "final_assay"},
        },
    ]
    (tmp_path / "trajectory.jsonl").write_text(
        "\n".join(json.dumps(r) for r in rows), encoding="utf-8"
    )
    component = equilibrium_diagnostics(tmp_path, tmp_path, {"system": "EQ"}, {})
    assert component["batch_concentrations"][1]["nominal_concentration_M"] is None
    assert component["batch_concentrations"][1]["component_feeds"][0]["amount_mol"] == 0.01
