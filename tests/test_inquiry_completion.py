import json
from collections import Counter
from types import SimpleNamespace

from scripts import run_inquiry_completion as s


def test_fixed_opportunity_coverage():
    rows = s.schedule()
    assert len(rows) == 30
    assert len({(u["repeat"], u["id"]) for u in rows}) == 30
    assert Counter(u["opportunity"] for u in rows) == {"Research": 15, "NoResearch": 15}
    assert set(Counter((u["world"], u["opportunity"]) for u in rows).values()) == {3}
    assert sum(u["batches"] for u in rows) == 180
    assert {u["arm"] for u in rows} == {"Opaque"}
    for a, b in zip(rows[::2], rows[1::2], strict=True):
        assert a["world"] == b["world"] and a["opportunity"] != b["opportunity"]


def test_capture_stops_before_any_action_or_provider(tmp_path, monkeypatch):
    config = s.eq.load_config()
    s.eq.configure_provider_helpers(config)
    called = []
    monkeypatch.setattr(s.eq.shared, "_prepare_codex_home", lambda *a: called.append(a))
    cells = [c for c in s.eq.validate_design(config)["schedule"] if c["arm"] == "Opaque"]
    for cell in cells:
        folder = tmp_path / cell["world_id"]
        public = s.capture_initial(config, cell, folder)
        text = json.dumps(public)
        assert "world_interventions" not in text and "private_authoring" not in text
        assert "queries" not in public
        assert public["task_contract"]["research_goal"] == s.eq.GOALS["characterization"]
        assert public["task_contract"]["study_budget"]["complete_batches"] == 12
        assert (folder / "empty-trajectory.jsonl").stat().st_size == 0
        assert not (folder / "unused-home").exists()
    assert not called


def test_common_posttests_disable_laboratory_and_preserve_thread(tmp_path, monkeypatch):
    calls = []

    def launch(command, prompt, workspace, environment, output, *a, **kw):
        calls.append((command, prompt, kw))
        output.mkdir(parents=True)
        return {
            "payload": {"report": "No experimental observations were available."},
            "thread_id": "same-thread",
            "failure": None,
        }

    monkeypatch.setattr(s.eq.shared, "launch", launch)
    agent = SimpleNamespace(
        home_root=tmp_path / "home",
        followup_environment={},
        initial_public_context={"public": "contract"},
        last_thread_id=None,
    )
    folder, private = tmp_path / "case", tmp_path / "private"
    s.posttest(agent, folder, private, "K1", None, {}, [])
    s.posttest(agent, folder, private, "K2", agent.last_thread_id, {}, [])
    for command, _, kw in calls:
        assert "mcp_servers.chemworld_lab.enabled=false" in command
        assert "mcp_servers.research_notebook.enabled=false" in command
        assert any(x.startswith("mcp_servers.research_notebook.command=") for x in command)
        assert kw["numerics_budget"] == s.FOLLOWUP_NUMERICS
    assert "no laboratory observations" in calls[0][1]
    assert calls[1][1] == s.K2
    assert agent.last_thread_id == "same-thread"


def test_missing_prediction_is_missing_not_zero():
    result = s.eq.evaluate_predictions(None, s.eq.queries(s.eq.load_config()), {})
    assert result["valid"] is False
    assert "metrics" not in result


def test_startup_exit_retains_receipt_and_stderr(tmp_path):
    import os
    import sys

    from scripts.run_work_ii_final_diagnostic import launch

    result = launch(
        [sys.executable, "-c", "import sys; sys.stderr.write('invalid transport'); sys.exit(1)"],
        "x" * 1_000_000,
        tmp_path,
        dict(os.environ),
        tmp_path / "receipt",
        10,
        False,
        tmp_path / "audit.jsonl",
        {},
    )
    assert result["failure"] == "provider_startup_failure"
    assert result["exit_code"] == 1
    assert (tmp_path / "receipt/receipt.json").exists()
    assert (tmp_path / "receipt/stderr.txt").read_text() == "invalid transport"


def test_prepare_binds_only_prospective_comparison(tmp_path):
    s.prepare(tmp_path / "run")
    design = s.read(tmp_path / "run/design.json")
    assert design["planned_posttests"] == 120
    assert design["planned_reference_batches"] == 300
    assert design["runtime_surface"]["scripts/run_inquiry_completion.py"]
    assert design["source_retries"] == 0
    assert not (tmp_path / "run/references").exists()
