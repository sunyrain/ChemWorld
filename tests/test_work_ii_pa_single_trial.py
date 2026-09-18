"""PA prediction scoring and measurement-stage regression checks."""

import json
from types import SimpleNamespace

import gymnasium as gym
import pytest
from scripts.run_work_ii_pa_single_trial import (
    ARMS,
    METRICS,
    SYSTEM,
    arm_material_information,
    evaluate,
    observations,
    queries,
    resource_card,
    source_system,
    token_accounting,
)

from chemworld.agents.interactive_codex_experiment import _initial_prompt


def test_partition_measurement_before_removal_is_not_replaced_by_terminal_zero():
    records = [
        {
            "experiment_index": 0,
            "transaction_status": "committed",
            "instrument": "hplc",
            "processed_estimate": {"product_in_aqueous": 0.6},
        },
        {
            "experiment_index": 0,
            "transaction_status": "committed",
            "action": {"operation": "separate_phase"},
        },
        {
            "experiment_index": 0,
            "transaction_status": "committed",
            "instrument": "final_assay",
            "processed_estimate": {"product_in_aqueous": 0.0},
        },
        {
            "experiment_index": 1,
            "transaction_status": "committed",
            "instrument": "hplc",
            "processed_estimate": {"product_in_aqueous": 0.4},
        },
    ]
    rows = observations(records)
    assert [r["before_phase_removal"] for r in rows] == [True, False, True]
    assert rows[0]["values"]["product_in_aqueous"] == 0.6


def test_prediction_scoring_preserves_errors_and_rejects_duplicate_queries():
    truth = {q["query_id"]: dict.fromkeys(METRICS, 0.5) for q in queries()}
    payload = {
        "predictions": [
            {
                "query_id": q,
                **{k: {"estimate": 0.6, "lower90": 0.55, "upper90": 0.65} for k in METRICS},
            }
            for q in truth
        ],
        "D1_phase": "uncertain",
        "D2_query": "uncertain",
    }
    result = evaluate(payload, truth)
    assert result["valid"]
    assert result["metrics"][METRICS[0]]["coverage90"] == 0
    assert result["metrics"][METRICS[0]]["interval_score90"] > 1
    payload["predictions"][-1] = payload["predictions"][0]
    assert not evaluate(payload, truth)["valid"]


def test_twenty_four_budget_scales_measurement_and_operation_envelopes():
    card = resource_card(24)
    assert card.vessel_start_limit == card.final_assay_limit == 24
    assert card.nonfinal_instrument_use_limit == 24
    assert card.operation_attempt_limit == 720
    assert card.process_time_limit_s is None
    assert source_system(12) == SYSTEM
    assert "Conduct 24 independent batches" in source_system(24)
    assert "24 additional instrument uses" in source_system(24)
    assert len(queries()) == 12  # Prediction denominator is independent of research budget.


def test_free_research_prompt_does_not_override_twenty_four_with_twelve():
    prompt = json.loads(
        _initial_prompt(
            task_contract={
                "free_research_campaign": True,
                "final_recommendation_required": False,
                "study_budget": {"complete_batches": 24},
            },
            task_contract_manifest={},
            current_packet={},
            material_manifest={},
            session_scope="campaign",
        )
    )
    assert prompt["task"]["study_budget"]["complete_batches"] == 24
    assert "12" not in prompt["instruction"]
    assert "no operating recommendation is required" in prompt["instruction"]
    assert prompt["belief_checkpoint_contract"] is None


def test_token_totals_do_not_sum_cumulative_followup_snapshots():
    result = {
        "source": {
            "usage": {
                "provider_token_accounting_complete": True,
                "input_token_count": 100,
                "cached_input_token_count": 80,
                "output_token_count": 10,
            }
        },
        "posttests": {
            stage: {
                "usage": {
                    "input_tokens": value,
                    "cached_input_tokens": cache,
                    "output_tokens": output,
                }
            }
            for stage, value, cache, output in (
                ("K1", 150, 100, 20),
                ("Q", 300, 200, 50),
                ("K2", 400, 270, 60),
            )
        },
    }
    usage = token_accounting(result)
    assert usage["complete"]
    assert usage["total"] == {
        "input": 400,
        "cached_input": 270,
        "output": 60,
        "uncached_input": 130,
        "input_plus_output": 460,
    }
    assert [r["input"] for r in usage["stages"]] == [100, 50, 150, 100]
    result["posttests"]["Q"]["usage"]["input_tokens"] = 50
    assert not token_accounting(result)["valid"]


@pytest.mark.parametrize("arm", ARMS)
def test_pa_material_selection_reaches_actual_agent_workspace_and_mcp_reply(arm):
    from scripts.validate_work_ii_ec_pa_entry import anonymous, material_reply

    env = gym.make(
        "ChemWorld",
        task_id="partition-discovery",
        seed=0,
        material_information=arm_material_information(arm),
    )
    try:
        env.reset(seed=0)
        reply = material_reply(env.unwrapped.task_info(), arm)
    finally:
        env.close()
    assert anonymous(reply)
    dossier = reply["material_information"]["dossier"]
    assert (dossier is None) == (arm == "Opaque")
    if dossier is not None:
        from chemworld.materials import static_material_information_dossier

        assert dossier == static_material_information_dossier(
            arm_material_information(arm), task_id="partition-discovery"
        )


@pytest.mark.parametrize("export_failure", [False, True])
def test_pa_block_keeps_failed_source_and_reuses_reference_without_expanding_scope(
    tmp_path, monkeypatch, export_failure
):
    from scripts import run_work_ii_pa_single_trial as runner

    calls = []

    def execute(root, progress, *, arm, batches, reference_run):
        calls.append((arm, reference_run))
        root.mkdir()
        result = {
            "status": "failed" if arm == "Aligned" else "completed",
            "reference": {"passed": True, "completed_batches": 12},
            "reference_reused_from": str(reference_run) if reference_run else None,
            "source": {"completed_batches": 12, "operations": 120},
            "posttests": {s: {"payload": {"report": "ok"}} for s in ("K1", "Q", "K2")},
        }
        runner.write(root / "result.json", result)

    monkeypatch.setattr(runner, "execute", execute)

    def export(*args):
        if export_failure:
            raise RuntimeError("report error")

    monkeypatch.setattr(runner, "export", export)
    root = tmp_path / "block"
    if export_failure:
        with pytest.raises(RuntimeError, match="report error"):
            runner.execute_block(root, tmp_path / "report", list(ARMS), {}, batches=12)
        summary = runner.read(root / "summary.json")
        assert summary["source_batches"] == summary["new_reference_batches"] == 12
        assert summary["posttests_completed"] == 3
        assert [r["status"] for r in summary["results"]] == ["failed", "not_started", "not_started"]
        return
    runner.execute_block(root, tmp_path / "report", list(ARMS), {}, batches=12)
    summary = runner.read(root / "summary.json")
    assert calls == [
        ("Opaque", None),
        ("Aligned", root / "Opaque"),
        ("MisIndexed", root / "Opaque"),
    ]
    assert summary["planned_sources"] == 3 and summary["completed_sources"] == 2
    assert summary["source_batches"] == 36 and summary["new_reference_batches"] == 12
    assert summary["posttests_completed"] == 9


def test_pa_invalid_arm_does_not_create_an_output_or_start_a_run(tmp_path):
    from scripts import run_work_ii_pa_single_trial as runner

    root = tmp_path / "bad"
    with pytest.raises(ValueError, match="unknown PA"):
        runner.execute(root, {}, arm="MisSpelled")
    assert not root.exists()


def test_pa_followup_uses_saved_question_and_rejects_a_different_thread(tmp_path, monkeypatch):
    from scripts import run_work_ii_pa_single_trial as runner

    messages = []
    monkeypatch.setattr(runner, "build_command", lambda *args, **kwargs: [])

    def launch(command, message, *args):
        messages.append(message)
        return {"payload": {"report": "answer"}, "thread_id": "wrong-thread"}

    monkeypatch.setattr(runner, "launch", launch)
    agent = SimpleNamespace(home_root=tmp_path, followup_environment={})
    result = runner.posttest(
        agent, tmp_path, "K2", "source-thread", {}, design={"K2": "saved question"}
    )
    assert messages == ["saved question"]
    assert result["failure"] == "posttest_thread_changed"
