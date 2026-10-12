import json
from pathlib import Path

from chemworld.agents.campaign_notebook import CampaignNotebookServer, with_notebook


def payload(result):
    assert not result.get("isError"), result
    return json.loads(result["content"][0]["text"])


def test_notes_bind_only_published_complete_events_and_preserve_versions(tmp_path):
    public = tmp_path / "public"
    public.mkdir()
    history = public / "operation_history.jsonl"
    server = CampaignNotebookServer(public, tmp_path / "notes")
    first = payload(server._call_tool("notebook_write", {"text": "# H1\nExpect a change."}))
    assert first["current_public_cursor"]["event_count"] == 0
    history.write_bytes(
        b'{"event_id":"runner-operation-0001","observation":{"yield":0.2}}\n{"event_id":'
    )
    second = payload(
        server._call_tool(
            "notebook_write",
            {"text": "# H1\nStill unresolved.", "reviewed_through": "runner-operation-0001"},
        )
    )
    assert second["current_public_cursor"] == {
        "event_count": 1,
        "last_event_id": "runner-operation-0001",
    }
    assert server._call_tool(
        "notebook_write", {"text": "future", "reviewed_through": "runner-operation-0002"}
    )["isError"]
    assert payload(server._call_tool("notebook_log", {}))["total"] == 2
    assert "Expect a change" in payload(server._call_tool("notebook_read", {"revision": 1}))["text"]
    restored = payload(server._call_tool("notebook_restore", {"revision": 1}))
    assert restored["current_public_cursor"]["event_count"] == 1
    assert payload(server._call_tool("notebook_log", {}))["total"] == 3
    assert history.read_bytes().endswith(b'{"event_id":')


def test_tool_boundary_does_not_expose_lab_or_private_data(tmp_path):
    public = tmp_path / "public"
    public.mkdir()
    (tmp_path / "secret.json").write_text('{"truth":123}')
    server = CampaignNotebookServer(public, tmp_path / "notes")
    assert server._call_tool("step", {"operation": "heat"})["isError"]
    assert server._call_tool("notebook_read", {"path": "../secret.json"})["isError"]
    reply = server._dispatch(
        {"id": 1, "method": "initialize", "params": {"protocolVersion": "2025-06-18"}}
    )
    assert reply["result"]["serverInfo"]["name"] == "research_notebook"
    assert "123" not in json.dumps(server._dispatch({"id": 2, "method": "tools/list"}))


def test_mixin_preserves_original_command_and_instructions(tmp_path):
    class Original:
        def _command(self, *, instructions_path, schema_path):
            instructions_path.write_text("ORIGINAL SOURCE BUDGET", encoding="utf-8")
            return ["codex", "exec", "-m", "original-model", "-c", "original=1"]

    agent = with_notebook(Original)()
    agent.output = tmp_path
    agent.workspace = type("Workspace", (), {"root": tmp_path / "lab"})()
    instructions = tmp_path / "instructions.txt"
    command = agent._command(instructions_path=instructions, schema_path=Path("schema.json"))
    assert command[:6] == ["codex", "exec", "-m", "original-model", "-c", "original=1"]
    assert instructions.read_text(encoding="utf-8").startswith("ORIGINAL SOURCE BUDGET")
    config = {
        arg.split("=", 1)[0]: json.loads(arg.split("=", 1)[1])
        for arg in command[6:]
        if arg.startswith("mcp_servers.")
    }
    assert len(config["mcp_servers.research_notebook.enabled_tools"]) == 5
    assert str(tmp_path / "lab/public") in config["mcp_servers.research_notebook.args"]


def test_selected_case_denominators_and_original_budgets():
    from scripts.run_paper_case_notebooks import CASES

    assert len(CASES) == 6
    assert sum(c["batches"] for c in CASES) == 84
    assert [c["cell"] for c in CASES if c["system"] == "C"] == [
        "C-W05-B12-E-Aligned",
        "C-W05-B24-E-Aligned",
    ]
    assert [c["model"] for c in CASES if c["system"] == "EQ"] == ["gpt-5.6-sol", "gpt-6-astra"]
