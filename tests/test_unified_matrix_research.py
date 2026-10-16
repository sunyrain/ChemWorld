"""Scientific-design and failure-preservation tests; no provider launches."""

from collections import Counter
from pathlib import Path

import pytest
from scripts import unified_matrix_research as m


def unit(system="EC"):
    return {"repeat": "repeat-01", **next(c for c in m.build_cases() if c["system"] == system)}


def complete_native():
    return {
        "batches": [{"lifecycle_index": i} for i in range(1, 13)],
        "operations": 120,
        "exact_replay": {"verified": True},
        "posttests": {s: {"payload": {"report": "sealed"}} for s in ("K1", "Q", "K2")},
        "prediction_evaluation": {"valid": True},
        "recommendation_retest": {"batches": [{}], "exact_replay": {"verified": True}},
    }


def test_full_factorial_conditions_do_not_smuggle_repeats_or_new_arms():
    rows = m.build_cases()
    assert len(rows) == len({r["id"] for r in rows}) == 90
    assert Counter(r["system"] for r in rows) == {"EC": 30, "RX": 30, "PA": 15, "P": 15}
    for system, per_world in (("EC", 6), ("RX", 6), ("PA", 3), ("P", 3)):
        cells = [r for r in rows if r["system"] == system]
        assert set(Counter(r["world"] for r in cells).values()) == {per_world}
        assert {r["model"] for r in cells} == {"gpt-5.6-sol"}
        assert {r["batches"] for r in cells} == {12}
        assert all("repeat" not in r for r in cells)
    assert {r["locus"] for r in rows if r["system"] == "RX"} == {"P"}
    for row in rows:
        if row["system"] == "RX":
            native_goal = {
                "discovery": "mechanism_discovery",
                "optimization": "safety_constrained_optimization",
            }[row["goal"]]
            assert row["cell"] == f"{row['world']}--P--{native_goal}--{row['arm']}"


def test_pa_has_no_mandatory_operating_recommendation():
    native = complete_native()
    native.pop("recommendation_retest")
    assert m.normalize_result(native, unit("PA"), Path("source"), 1)["status"] == "completed"
    assert m.normalize_result(native, unit("EC"), Path("source"), 1)["status"] == "failed"


def test_missing_forecast_stays_missing_and_in_denominator():
    native = complete_native()
    native["posttests"].pop("Q")
    native["prediction_evaluation"] = {"valid": False, "failure": "missing"}
    result = m.normalize_result(native, unit(), Path("source"), 1)
    assert result["status"] == "failed"
    assert len(result["source"]["batches"]) == 12
    assert "Q" not in result["posttests"]
    assert "prediction" in result["failure"]["failed_checks"]


def test_result_is_write_once_and_terminal_failure_never_replaced(tmp_path, monkeypatch):
    calls = []

    def fake(root, folder, case, progress):
        calls.append(case["id"])
        return complete_native(), folder / "participant"

    monkeypatch.setattr(m, "_execute", fake)
    case = unit()
    result = m.execute_unit(tmp_path, case)
    assert result["status"] == "completed"
    assert m.execute_unit(tmp_path, case) == result
    assert len(calls) == 1
    other = unit("RX")
    m.write(tmp_path / other["repeat"] / other["id"] / "status.json", {"status": "failed"})
    with pytest.raises(RuntimeError, match="Terminal status"):
        m.execute_unit(tmp_path, other)
    assert len(calls) == 1


def test_postprocessing_exception_preserves_native_source_and_sealed_stages(tmp_path, monkeypatch):
    case = unit()

    def fail(root, folder, row, progress):
        path, _ = m._native_locations(folder, row)
        m.write(path, complete_native())
        raise RuntimeError("reference unavailable")

    monkeypatch.setattr(m, "_execute", fail)
    result = m.execute_unit(tmp_path, case)
    assert result["status"] == "failed"
    assert len(result["source"]["batches"]) == 12
    assert set(result["posttests"]) == {"K1", "Q", "K2"}
    assert result["failure"]["message"] == "reference unavailable"
    assert result["fatal_execution_error"] is True


def test_partial_native_directory_is_never_automatically_restarted(tmp_path):
    case = unit()
    (tmp_path / case["repeat"] / case["id"] / "participant").mkdir(parents=True)
    with pytest.raises(RuntimeError, match="Partial participant"):
        m.execute_unit(tmp_path, case)


def test_no_seed_or_budget_substitution(tmp_path):
    for key, value in (("batches", 24), ("model", "other-model"), ("world", "EC-W99")):
        altered = {**unit(), key: value}
        with pytest.raises(ValueError):
            m.execute_unit(tmp_path, altered)


def test_p_followups_have_one_attempt_even_for_transport_error(monkeypatch):
    from scripts import run_work_ii_ec_dual_goal_trial as ec

    calls = []
    original_metrics = ec.METRICS

    def fail(*args, **kwargs):
        calls.append(ec.METRICS)
        return {"failure": "provider_failure"}

    monkeypatch.setattr(ec, "posttest", fail)
    result = m._single_p_posttest(None, None, "Q", "thread", {}, {})
    assert result["failure"] == "provider_failure"
    assert calls == [("purity", "recovery")]
    assert original_metrics == ec.METRICS


def test_pa_interval_level_and_rx_goal_difference_preserved():
    from scripts import run_work_ii_pa_single_trial as pa
    from scripts import run_work_ii_rx_ps_five_world_dual_goal as rx

    assert "90%" in pa.question("Q")
    assert "lower90" in str(pa.schema("Q"))
    assert set(rx.GOALS) == {"mechanism_discovery", "safety_constrained_optimization"}
    assert "secondary" in rx.GOALS["mechanism_discovery"]
    assert "primary" in rx.GOALS["safety_constrained_optimization"]


@pytest.mark.parametrize("system", ["EC", "PA", "RX", "P"])
def test_actual_source_command_keeps_notebook_and_all_mcp_thread_limits(
    tmp_path,
    monkeypatch,
    system,
):
    from scripts import run_work_ii_ec_dual_goal_trial as ec
    from scripts import run_work_ii_p_study as p
    from scripts import run_work_ii_pa_single_trial as pa
    from scripts import run_work_ii_rx_ps_five_world_dual_goal as rx
    from scripts.unified_matrix_runtime import WORKER_ENV, bounded_notebook

    from chemworld.agents.interactive_codex_experiment import InteractiveCodexExperimentAgent

    monkeypatch.setattr(
        InteractiveCodexExperimentAgent,
        "_command",
        lambda *a, **k: ["codex", "exec", "-m", m.MODEL],
    )
    kwargs = {
        "home_root": tmp_path,
        "output": tmp_path,
        "workspace": tmp_path / "laboratory",
        "role_id": "free_research",
    }
    if system == "EC":
        base, kwargs = ec.FreeResearchAgent, {**kwargs, "goal": "discovery"}
    elif system == "PA":
        base, kwargs = pa.PAAgent, {**kwargs, "arm": "Opaque"}
    elif system == "P":
        base, kwargs = p.StudyAgent, {**kwargs, "dossier": None}
    else:
        for name in (
            "TASK",
            "PROVIDER",
            "METRICS",
            "GOALS",
            "SYSTEM",
            "K1",
            "K2",
            "resource_card",
            "build_command",
        ):
            monkeypatch.setattr(ec, name, getattr(ec, name))
        rx.configure_shared_helpers()
        base, kwargs = rx.rx_canary.RxFreeResearchAgent, {**kwargs, "goal": "mechanism_discovery"}
    agent = bounded_notebook(base, final_recommendation_required=system != "PA")(**kwargs)
    try:
        instructions = tmp_path / "instructions.md"
        command = agent._command(
            instructions_path=instructions, schema_path=tmp_path / "schema.json"
        )
        text = instructions.read_text(encoding="utf-8")
        assert "research_notebook tools are authorized" in text
        assert "record a concise testable expectation if you have one" in text
        assert "reference-truth" not in text
        if system == "PA":
            assert "no best-batch recommendation" in text
            assert "before committing your final recommendation" not in text
        for server in ("chemworld_lab", "research_notebook", "public_numerics"):
            for key in WORKER_ENV:
                assert any(c.startswith(f"mcp_servers.{server}.env.{key}=") for c in command)
    finally:
        agent.close()
