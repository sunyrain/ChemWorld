import copy
import json
from collections import Counter
from types import SimpleNamespace

import pytest
from scripts import unified_matrix_c_opportunity as block
from scripts.run_paper_case_notebooks import read, write


def test_matrix_contains_matched_arms_and_three_fresh_sessions():
    rows = block.build_cases()
    assert len(rows) == len({(r["repeat"], r["id"]) for r in rows}) == 30
    assert Counter(r["opportunity"] for r in rows) == {"Research": 15, "NoResearch": 15}
    assert {r["arm"] for r in rows} == {"Opaque"}
    assert set(Counter((r["world"], r["opportunity"]) for r in rows).values()) == {3}
    assert sum(r["batches"] for r in rows) == 180
    for left, right in zip(rows[::2], rows[1::2], strict=True):
        assert left["world"] == right["world"]
        assert left["opportunity"] != right["opportunity"]


def test_design_preserves_corrected_recovery_and_query_actions():
    original = read(block.CORRECTED_DESIGN)
    design = block.prepared_design()
    assert design["queries"] == original["queries"]
    assert len(design["schedule"]) == 5
    assert all(s["arm"] == "Opaque" and s["batches"] == 12 for s in design["schedule"])
    assert "tracked initial reagent charge" in design["systems"]["12"]
    assert "tracked initial reagent charge" in design["Q"]
    assert design["resolution"] == original["resolution"]
    assert design["model"]["model"] == "gpt-5.6-sol"
    assert design["model"]["reasoning_effort"] == "medium"


def test_public_inputs_match_live_research_before_provider_and_without_truth(tmp_path, monkeypatch):
    provider_calls = []
    monkeypatch.setattr(
        block.c.pilot.ec, "_prepare_codex_home", lambda *a: provider_calls.append(a)
    )

    def stop(self, current_packet):
        raise block.InitialStateCapturedError

    monkeypatch.setattr(block.c.FormalCAgent, "_start_session", stop)
    for world_seed in range(5):
        public = block.capture_initial(tmp_path / f"capture-{world_seed}", world_seed)
        assert public["task_contract"]["study_budget"]["complete_batches"] == 12
        assert (
            "tracked initial reagent charge"
            in public["task_contract"]["prediction_metrics"]["crystal_yield"]
        )
        assert "hidden_world" not in json.dumps(public)
        assert "truth" not in public and "queries" not in public
        folder = tmp_path / f"research-{world_seed}"
        folder.mkdir()
        agent = block.ResearchAgent(
            batches=12,
            goal="optimization",
            home_root=folder / "unused-home",
            output=folder,
            workspace=folder / "laboratory",
            role_id="free_research",
        )
        block.ResearchAgent.expected_public_context = public
        try:
            with pytest.raises(block.InitialStateCapturedError):
                block.c.physics(
                    agent,
                    folder / "trajectory.jsonl",
                    world_seed=world_seed,
                    arm="Opaque",
                    batches=12,
                    observation_seed=0,
                    callback=None,
                    truths=[],
                )
        finally:
            agent.close()
            block.ResearchAgent.expected_public_context = None
        assert read(folder / "initial-public-context.json") == public
        assert (folder / "trajectory.jsonl").stat().st_size == 0
        assert not (folder / "unused-home").exists()
    assert not provider_calls


def test_shared_posttests_disable_laboratory_notebook_and_keep_thread(tmp_path, monkeypatch):
    calls = []

    def launch(command, prompt, workspace, environment, output, *args, **kwargs):
        calls.append((command, prompt, kwargs))
        output.mkdir(parents=True)
        return {"payload": {"report": "No observations."}, "thread_id": "same", "failure": None}

    monkeypatch.setattr(block.c.pilot, "launch", launch)
    agent = SimpleNamespace(
        home_root=tmp_path / "home",
        followup_environment={},
        initial_public_context={"public": "same-background"},
        last_thread_id=None,
    )
    design = block.prepared_design()
    block.posttest(agent, tmp_path / "baseline", "K1", None, {}, design)
    block.posttest(agent, tmp_path / "baseline", "K2", agent.last_thread_id, {}, design)
    block.posttest(agent, tmp_path / "research", "K1", "same", {}, design)
    assert calls[0][1].endswith(calls[2][1])
    assert "no laboratory observations" in calls[0][1]
    assert calls[1][1] == design["K2"]
    for command, _, kwargs in calls:
        for server in ("chemworld_lab", "research_notebook"):
            assert f"mcp_servers.{server}.enabled=false" in command
            assert any(x.startswith(f"mcp_servers.{server}.command=") for x in command)
        assert 'mcp_servers.public_numerics.env.TOKIO_WORKER_THREADS="2"' in command
        assert kwargs["numerics_budget"] == block.FOLLOWUP_NUMERICS
    assert agent.last_thread_id == "same"


def test_no_research_never_accesses_laboratory_and_retains_failed_q(tmp_path, monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("NoResearch accessed the laboratory")

    monkeypatch.setattr(block.c, "physics", forbidden)
    monkeypatch.setattr(block.c, "fixed", forbidden)
    monkeypatch.setattr(block, "_prepare_codex_home", lambda *args: {})
    calls = []

    def posttest(agent, folder, stage, thread_id, progress, design):
        calls.append(stage)
        agent.last_thread_id = "same"
        return {
            "payload": None if stage == "Q" else {"report": "No observations."},
            "failure": "provider_failure" if stage == "Q" else None,
        }

    monkeypatch.setattr(block, "posttest", posttest)
    public = {"public": "same-background"}
    original = copy.deepcopy(public)
    result = block.no_research(tmp_path / "case", block.prepared_design(), public, {}, {})
    assert calls == ["K1", "Q"]
    assert result["source"]["operations"] == 0
    assert result["source"]["batches"] == []
    assert result["status"] == "failed"
    assert result["failure"]["stage"] == "Q"
    assert result["prediction_evaluation"]["valid"] is False
    assert public == original


def test_terminal_unit_is_never_replaced(tmp_path):
    unit = block.build_cases()[0]
    path = tmp_path / unit["repeat"] / unit["id"] / "status.json"
    write(path, {"status": "failed", "failure": "retained failure"})
    before = path.read_bytes()
    with pytest.raises(FileExistsError, match="Terminal unit"):
        block.execute_unit(tmp_path, unit)
    assert path.read_bytes() == before


def test_prepared_inputs_and_research_unit_keep_truth_out_of_public_context(tmp_path, monkeypatch):
    fixed_calls = []

    def fixed(folder, actions, *, world_seed, batches):
        fixed_calls.append((world_seed, batches))
        value = {
            "passed": True,
            "truth": [{"host_reference_only": 123}] * 12,
            "batches": [{}] * 12,
            "operations": len(actions),
            "exact_replay": {"verified": True},
        }
        write(folder / "result.json", value)
        return value

    monkeypatch.setattr(block.c, "fixed", fixed)
    summary = block.prepare_inputs(tmp_path)
    assert summary["reference_batches"] == 60
    assert fixed_calls == [(w, 12) for w in range(5)]
    unit = next(u for u in block.build_cases() if u["opportunity"] == "Research")
    folder = tmp_path / unit["repeat"] / unit["id"]
    write(folder / "status.json", {"status": "running"})
    original_agent, original_posttest = block.c.FormalCAgent, block.c.pilot.posttest

    def source(root, cell, progress):
        assert block.c.FormalCAgent is block.ResearchAgent
        assert block.c.pilot.posttest is block.posttest
        context = block.ResearchAgent.expected_public_context
        assert "host_reference_only" not in json.dumps(context)
        assert read(root / "qualification/W01/queries/result.json")["truth"][0] == {
            "host_reference_only": 123
        }
        return {
            "status": "completed",
            "failure": None,
            "source": {"batches": [{}] * 12, "operations": 120, "exact_replay": {"verified": True}},
            "posttests": {
                s: {"payload": {"report": "sealed"}, "failure": None} for s in block.STAGES
            },
            "prediction_evaluation": {"valid": True},
            "recommendation_retest": {"passed": True, "exact_replay": {"verified": True}},
        }

    monkeypatch.setattr(block.c, "source", source)
    result = block.execute_unit(tmp_path, {**unit, "scheduler_index": 3})
    assert result["status"] == "completed"
    assert result["posttest_chain_sealed"]
    assert all((folder / "sealed" / f"{s}.json").exists() for s in block.STAGES)
    assert read(folder / "status.json")["status"] == "completed"
    assert block.c.FormalCAgent is original_agent
    assert block.c.pilot.posttest is original_posttest
    with pytest.raises(FileExistsError):
        block.execute_unit(tmp_path, unit)


def test_adapter_failure_retains_native_source_usage_and_replay(tmp_path, monkeypatch):
    unit = next(u for u in block.build_cases() if u["opportunity"] == "Research")
    inputs = tmp_path / block.INPUT_DIRECTORY
    write(inputs / "complete.json", {"ready": True})
    write(inputs / "design.json", block.prepared_design())
    write(inputs / "public/W01/initial-public-context.json", {"public": "same"})
    write(inputs / "references/W01/result.json", {"truth": [{}] * 12})
    native = {
        "status": "running",
        "failure": {"stage": "Q", "message": "provider_failure"},
        "source": {
            "batches": [{}] * 12,
            "operations": 123,
            "exact_replay": {"verified": True},
            "usage": {"input_token_count": 456},
        },
        "posttests": {"K1": {"payload": {"report": "sealed"}, "failure": None}},
        "posttest_validation": {"K1": {"valid": True, "preserved": True}},
    }

    def source(root, cell, progress):
        write(root / "sources" / cell["id"] / "result.json", native)
        raise KeyError("unexpected adapter integration defect")

    monkeypatch.setattr(block.c, "source", source)
    result = block.execute_unit(tmp_path, unit)
    assert result["fatal_execution_error"]
    assert result["failure"] == native["failure"]
    assert result["adapter_failure"]["type"] == "KeyError"
    assert result["source"] == native["source"]
    assert result["posttest_validation"]["K1"] == native["posttest_validation"]["K1"]
    assert result["posttests"] == native["posttests"]


def test_provider_failure_is_nonfatal_and_invalid_q_is_not_sealed(tmp_path):
    unit = next(u for u in block.build_cases() if u["opportunity"] == "NoResearch")
    native = {
        "status": "failed",
        "failure": {"stage": "Q", "message": "provider_failure"},
        "source": {"batches": [], "operations": 0},
        "posttests": {
            "K1": {"payload": {"report": "sealed"}, "failure": None},
            "Q": {"payload": {"predictions": []}, "failure": "provider_failure"},
        },
        "prediction_evaluation": {"valid": False, "failure": "missing query IDs"},
    }
    result = block.normalize_result(native, unit, tmp_path)
    assert not result.get("fatal_execution_error")
    assert result["posttest_validation"]["K1"]["valid"]
    assert not result["posttest_validation"]["Q"]["valid"]
    assert not result["posttest_chain_sealed"]
    assert result["source"]["operations"] == 0
    assert result["checks"]["source_replay"] is True


def test_baseline_token_completeness_uses_three_cumulative_snapshots(tmp_path, monkeypatch):
    monkeypatch.setattr(block, "_prepare_codex_home", lambda *args: {})
    monkeypatch.setattr(block.c, "evaluate", lambda *args: {"valid": True})

    def posttest(agent, folder, stage, thread_id, progress, design):
        n = block.STAGES.index(stage) + 1
        return {
            "payload": {"report": "sealed"},
            "failure": None,
            "usage": {
                "input_tokens": n * 100,
                "cached_input_tokens": n * 20,
                "output_tokens": n * 10,
            },
        }

    monkeypatch.setattr(block, "posttest", posttest)
    result = block.no_research(tmp_path / "baseline", block.prepared_design(), {}, {}, {})
    assert result["tokens"]["complete"]
    assert result["tokens"]["total"]["input"] == 300
    assert result["tokens"]["total"]["output"] == 30
