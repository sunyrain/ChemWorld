from collections import Counter
from pathlib import Path
from types import SimpleNamespace

import pytest
from scripts import run_abductive_discrimination as s


@pytest.fixture(autouse=True)
def restore_process_local_adapters(monkeypatch):
    for module, keys in (
        (s, ("INITIAL_REFERENCE_OBSERVATIONS",)),
        (s.eq, ("POSTTEST_STAGES", "SYSTEM", "EqFreeResearchAgent", "run_posttest")),
        (s.eq.v1, ("SYSTEM", "K1", "Q_PROMPT", "K2")),
        (s.inquiry, ("public_context", "K1", "Q", "K2")),
        (s.eq.provider_shared, ("build_command",)),
        (
            s.eq.shared,
            (
                "TASK",
                "PROVIDER",
                "METRICS",
                "GOALS",
                "SYSTEM",
                "K1",
                "K2",
                "resource_card",
                "build_command",
            ),
        ),
    ):
        for key in keys:
            monkeypatch.setattr(module, key, getattr(module, key))


def config_fixture():
    config = s.eq.load_config()
    config["worlds"] = [
        {"world_id": f"EQ-P{pair:02d}-{mechanism}"}
        for pair in range(1, 6)
        for mechanism in ("A", "B")
    ]
    return config


def test_matched_schedule_is_fixed_and_balanced():
    rows = s.schedule(config_fixture())
    assert len(rows) == 30
    assert len({(r["repeat"], r["id"]) for r in rows}) == 30
    assert set(Counter((r["pair"], r["mechanism"]) for r in rows).values()) == {3}
    assert Counter(r["mechanism"] for r in rows) == {"A": 15, "B": 15}
    assert sum(r["batches"] for r in rows) == 360
    for left, right in zip(rows[::2], rows[1::2], strict=True):
        assert left["pair"] == right["pair"]
        assert left["mechanism"] != right["mechanism"]


def test_thread_limits_cover_all_real_mcp_servers_without_duplicate_settings():
    import json
    import os

    command = s.with_thread_limits(["codex", "exec"])
    assert command == s.with_thread_limits(command)
    for server in ("chemworld_lab", "research_notebook", "public_numerics"):
        for key, value in s.WORKER_ENV.items():
            assert f"mcp_servers.{server}.env.{key}={json.dumps(value)}" in command
            assert os.environ[key] == value


def test_prepare_has_three_sealed_stages_and_no_simulator_or_provider(tmp_path, monkeypatch):
    monkeypatch.setattr(s, "build_config", config_fixture)
    monkeypatch.setattr(s.eq, "physics", lambda *a, **kw: pytest.fail("Unexpected simulator"))
    monkeypatch.setattr(s.eq.shared, "launch", lambda *a, **kw: pytest.fail("Unexpected provider"))
    root = tmp_path / "block"
    s.prepare(root)
    design = s.read(root / "design.json")
    assert design["planned_sources"] == 30
    assert design["planned_source_batches"] == 360
    assert design["planned_posttests"] == 90
    assert design["planned_reference_batches"] == 600
    assert design["posttest_stages"] == ["K1", "Q", "K2"]
    assert design["source_retries"] == 0
    assert design["model_rng_seed"] is None
    assert not (root / "references").exists()
    with pytest.raises(FileExistsError):
        s.prepare(root)


def test_posttest_embargo_and_thread_preservation(tmp_path, monkeypatch):
    calls = []

    def launch(command, prompt, workspace, environment, output, *args, **kwargs):
        calls.append((command, prompt))
        output.mkdir(parents=True)
        return {
            "payload": {"report": "A scoped scientific account."},
            "thread_id": "research-thread",
            "failure": None,
            "usage": {"input_tokens": 20, "output_tokens": 4},
        }

    monkeypatch.setattr(s.eq.shared, "launch", launch)
    agent = SimpleNamespace(home_root=tmp_path / "home", followup_environment={})
    for stage in s.STAGES:
        s.posttest(
            agent,
            tmp_path / "case",
            tmp_path / "private",
            stage,
            "research-thread",
            {},
            [{"query_id": "HIDDEN_HELDOUT"}],
        )
    assert "HIDDEN_HELDOUT" not in calls[0][1]
    assert "HIDDEN_HELDOUT" in calls[1][1]
    assert "HIDDEN_HELDOUT" not in calls[2][1]
    sealed = s.read(tmp_path / "case/sealed/K2.json")
    assert sealed["usage"] == {"input_tokens": 20, "output_tokens": 4}
    assert sealed["method_resources"]["provider_usage"] == sealed["usage"]
    for command, _ in calls:
        assert "mcp_servers.chemworld_lab.enabled=false" in command
        assert "mcp_servers.research_notebook.enabled=false" in command
    with pytest.raises(ValueError):
        s.posttest(agent, tmp_path, tmp_path, "EQS", "research-thread", {}, [])


def test_public_inputs_require_exact_pair_match(tmp_path, monkeypatch):
    config = config_fixture()
    monkeypatch.setattr(s, "configure", lambda *args: None)
    monkeypatch.setattr(s.inquiry, "capture_initial", lambda *a: {"public": "same"})
    assert s.check_public_contexts(tmp_path / "ok", config)["all_identical"]
    monkeypatch.setattr(
        s.inquiry, "capture_initial", lambda config, cell, folder: {"leak": cell["world_id"]}
    )
    with pytest.raises(RuntimeError, match="initial public"):
        s.check_public_contexts(tmp_path / "bad", config)
    assert s.read(tmp_path / "bad/public-contexts/result.json")["all_identical"] is False


def test_real_initial_contexts_hide_world_identity_without_actions(tmp_path, monkeypatch):
    calls = []
    monkeypatch.setattr(s.eq.shared, "_prepare_codex_home", lambda *a: calls.append(a))
    config = s.build_config()
    report = s.check_public_contexts(tmp_path, config)
    assert report["all_identical"] and len(report["pairs"]) == 5
    assert not calls
    for trajectory in tmp_path.glob("public-contexts/*/empty-trajectory.jsonl"):
        assert trajectory.stat().st_size == 0
    assert len(list(tmp_path.glob("public-contexts/*/empty-trajectory.jsonl"))) == 10


def test_counterfactual_uses_actual_state_and_retains_incomplete_prefix(tmp_path, monkeypatch):
    from chemworld.physchem.abductive_worlds import solve_query
    from chemworld.runtime.observation_services import ChemWorldObservationKernel

    original = ChemWorldObservationKernel._equilibrium_truth_values

    def reject_empty_truth_access(self, state):
        assert state.volume_L > 0, "A rejected empty final assay must not ask for physical truth"
        return original(self, state)

    monkeypatch.setattr(
        ChemWorldObservationKernel, "_equilibrium_truth_values", reject_empty_truth_access
    )

    config = s.build_config()
    s.configure(config)
    unit = s.schedule(config)[0]
    world = s.eq.world_by_id(config, unit["world"])
    queries = s.eq.queries(config)[:2]
    actions = [{"operation": "measure", "instrument": "final_assay"}]
    actions += [a for q in queries for a in q["actions"]]
    source = s.truth_captured_reference(
        tmp_path / "source",
        actions,
        config=config,
        world=world,
        observation_seed=42,
        namespace="test-fixed-actions",
    )
    assert source["operation_attempts"] == len(actions)
    assert source["exact_replay"]["verified"]
    assert source["rollbacks"] == [1]
    assert source["failure"]["message"] == "truth replay exhausted its frozen action plan"
    for query, captured in zip(queries, source["physical_means"], strict=True):
        assert captured["metrics"] == pytest.approx(solve_query(world, query)["metrics"])
    trajectory = s.case_folder(tmp_path / unit["repeat"], unit) / "trajectory.jsonl"
    trajectory.parent.mkdir(parents=True)
    trajectory.write_bytes(Path(tmp_path / "source/trajectory.jsonl").read_bytes())
    source["source_status"] = "partial"
    result = s.counterfactual(tmp_path, unit, config, source)
    assert result["status"] == "completed"
    assert result["own_source_observations_identical"]
    assert len(result["matched_batches"]) == 2
    assert result["worlds"]["own"]["expected_incomplete_prefix_end"]
    assert result["worlds"]["partner"]["expected_incomplete_prefix_end"]
    assert result["participant_feedback"] is False


def test_missing_and_failed_sessions_keep_planned_denominators(tmp_path, monkeypatch):
    monkeypatch.setattr(s, "build_config", config_fixture)
    s.prepare(tmp_path / "block")
    root = tmp_path / "block"
    unit = s.read(root / "design.json")["schedule"][0]
    s.write(
        s.pool.result_path(root, unit),
        {
            "status": "retained_nonconforming",
            "failure": "retained provider failure",
            "batches": [{}, {}],
            "operations": 12,
            "posttests": {},
        },
    )
    summary = s.snapshot(root)
    assert summary["planned_sources"] == 30
    assert summary["planned_posttests"] == 90
    assert summary["terminal_sources"] == 1
    assert summary["completed_sources"] == 0
    assert summary["completed_batches"] == 2
    assert summary["sealed_posttests"] == 0
    assert summary["cases"][0]["failure"] == "retained provider failure"
    assert len(summary["cases"]) == 30
