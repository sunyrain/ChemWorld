"""Exercise the real calculator/launcher boundary without a paid model call."""

from __future__ import annotations

import json
import os
import sys
from types import SimpleNamespace

import pytest
from scripts import run_work_ii_ec_dual_goal_trial as ec
from scripts import run_work_ii_pa_single_trial as pa
from scripts.run_work_ii_final_diagnostic import build_command, launch

from chemworld.agents.diagnostic_numerics import FOLLOWUP_NUMERICS, NumericsBudget


def calculator_command(command):
    prefix = "mcp_servers.public_numerics.args="
    return [
        sys.executable,
        *json.loads(next(s[len(prefix) :] for s in command if s.startswith(prefix))),
    ]


@pytest.mark.parametrize(
    "budget,calls,expected_failure",
    [
        (None, 12, "tool_budget_exceeded"),
        (FOLLOWUP_NUMERICS, 12, None),
        (NumericsBudget(2, "continue_answer"), 3, None),
    ],
)
def test_calculator_exhaustion_and_answer_completion(tmp_path, budget, calls, expected_failure):
    audit = tmp_path / "audit.jsonl"
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    command = build_command(
        {"id": "fixture", "model": "fixture", "reasoning_effort": "medium"},
        tmp_path / "schema.json",
        workspace,
        audit=audit,
        numerics_budget=budget,
    )
    server = calculator_command(command)
    # A deterministic provider fixture invokes the actual copied STDIO MCP server.
    # Delay the final answer so the launcher's legacy kill path really has to run.
    child = tmp_path / "provider.py"
    child.write_text(
        "import json, subprocess, sys, time\n"
        "sys.stdin.read()\n"
        "requests=[{'jsonrpc':'2.0','id':i,'method':'tools/call',"
        "'params':{'name':'calculate','arguments':{'expression':str(i)+'+1'}}} "
        "for i in range(int(sys.argv[2]))]\n"
        "result=subprocess.run(json.loads(sys.argv[1]), "
        "input='\\n'.join(json.dumps(r) for r in requests)+'\\n', "
        "text=True,capture_output=True,check=True,timeout=15)\n"
        "print(json.dumps({'type':'thread.started','thread_id':'fixture-thread'}),flush=True)\n"
        "for i,line in enumerate(result.stdout.splitlines()):\n"
        " r=json.loads(line)['result']\n"
        " print(json.dumps({'type':'item.completed','item':{'id':str(i),"
        "'type':'mcp_tool_call','server':'public_numerics','tool':'calculate',"
        "'result':r,'status':'failed' if r.get('isError') else 'completed'}}),flush=True)\n"
        "time.sleep(0.8)\n"
        "print(json.dumps({'type':'item.completed','item':{'type':'agent_message',"
        "'text':json.dumps({'report':'answer submitted'})}}),flush=True)\n"
        "print(json.dumps({'type':'turn.completed','usage':{'input_tokens':1,"
        "'cached_input_tokens':0,'output_tokens':1}}),flush=True)\n",
        encoding="utf-8",
    )
    receipt = launch(
        [sys.executable, str(child), json.dumps(server), str(calls)],
        "Twelve prediction questions",
        workspace,
        dict(os.environ),
        tmp_path / "turn",
        15,
        True,
        audit,
        {},
        numerics_budget=budget,
    )
    rows = [json.loads(line) for line in audit.read_text(encoding="utf-8").splitlines()]
    assert len(rows) == calls
    assert receipt["failure"] == expected_failure
    if expected_failure:
        assert not receipt["payload"]
        assert "--budget-feedback" not in server
    else:
        assert receipt["payload"] == {"report": "answer submitted"}
        assert receipt["numerics_budget"] == budget.to_dict()
        assert receipt["numerics_attempts"] == calls
        assert rows[0]["budget"]["remaining"] == budget.limit - 1
        if calls > budget.limit:
            assert rows[-1]["status"] == "rejected"
            assert rows[-1]["error_code"] == "calculation_budget_exhausted"
            assert rows[-1]["budget"]["remaining"] == 0
            assert "value" not in rows[-1]
        else:
            assert all(r["status"] == "completed" for r in rows)


@pytest.mark.parametrize("runner", [ec, pa], ids=["EC", "PA"])
@pytest.mark.parametrize("new_design", [False, True], ids=["saved-legacy", "new-budget"])
def test_posttest_uses_saved_budget_for_instructions_server_and_launcher(
    tmp_path,
    monkeypatch,
    runner,
    new_design,
):
    captured = {}

    def capture(command, message, *args, **kwargs):
        captured.update(command=command, message=message, kwargs=kwargs)
        return {"payload": {"predictions": []}, "thread_id": "original-thread"}

    monkeypatch.setattr(runner, "launch", capture)
    design = {"Q": "saved blind questions"}
    if new_design:
        design["posttest_numerics"] = FOLLOWUP_NUMERICS.to_dict()
    runner.posttest(
        SimpleNamespace(home_root=tmp_path, followup_environment={}),
        tmp_path,
        "Q",
        "original-thread",
        {},
        design=design,
    )
    server = calculator_command(captured["command"])
    assert captured["message"] == "saved blind questions"
    assert "original-thread" in captured["command"]
    instructions = (tmp_path / "followup/instructions.md").read_text(encoding="utf-8")
    if new_design:
        assert server[server.index("--limit") + 1] == "128"
        assert "--budget-feedback" in server
        assert captured["kwargs"]["numerics_budget"] == FOLLOWUP_NUMERICS
        assert "128" in instructions and "submit your answer" in instructions
        assert "8 calls per follow-up" not in instructions
    else:
        assert server[server.index("--limit") + 1] == "8"
        assert "--budget-feedback" not in server
        assert "numerics_budget" not in captured["kwargs"]
        assert "128" not in instructions
