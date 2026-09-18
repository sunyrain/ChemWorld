"""Prevent scope expansion and success-conditioned interviews in the EC trial."""

import json
from pathlib import Path
from types import SimpleNamespace

import pytest
from scripts.run_work_ii_ec_dual_goal_trial import (
    LEGACY_QUERY_VERSION,
    METRICS,
    evaluate_predictions,
    physics,
    planned_units,
    posttest_context_available,
    prediction_question,
    queries,
    recipe,
    resource_card,
    summaries,
)

from chemworld.data.logging import load_jsonl
from chemworld.eval.work_ii_truth import _FrozenTruthReplayAgent


def test_discarded_batch_does_not_enter_next_completed_recipe():
    rows = [
        {"experiment_index": 0, "action": {"operation": "add_reagent"}},
        {"experiment_index": 0, "action": {"operation": "discard_batch"}},
        {"experiment_index": 1, "action": {"operation": "add_solvent"}},
        {"experiment_index": 1, "action": {"operation": "terminate"}},
        {
            "experiment_index": 1,
            "action": {"operation": "measure", "instrument": "final_assay"},
            "instrument": "final_assay",
            "transaction_status": "committed",
            "observation": {},
        },
    ]
    completed = summaries(rows)
    assert len(completed) == 1
    assert completed[0]["lifecycle_index"] == 2
    assert [a["operation"] for a in completed[0]["actions"]] == [
        "add_solvent",
        "terminate",
        "measure",
    ]


def test_retest_accepts_long_batch_and_multiple_measurements(tmp_path: Path):
    # Both were legal in the twelve-batch source but rejected by the old single-batch card.
    actions = recipe(1, 1, -0.8, 500, 14400)
    actions[-2:-2] = [
        {"operation": "measure", "instrument": "uvvis"},
        {"operation": "measure", "instrument": "ph_meter"},
    ]
    output = tmp_path / "trajectory.jsonl"
    physics(_FrozenTruthReplayAgent(actions), output, batches=1, source_envelope=True)
    records = load_jsonl(output)
    assert len(records) == len(actions)
    assert all(r["transaction_status"] == "committed" for r in records)
    assert len(summaries(records)) == 1
    assert records[-1]["instrument"] == "final_assay"


def test_explicit_six_cell_scope_never_adds_other_prior_layers():
    selected = [
        f"{goal}-E-{arm}"
        for goal in ("discovery", "optimization")
        for arm in ("Opaque", "Aligned", "MisIndexed")
    ]
    assert ["-".join(unit) for unit in planned_units(selected)] == selected
    for invalid in ([], selected + selected[:1], ["discovery-Z-Opaque"]):
        with pytest.raises(ValueError):
            planned_units(invalid)


def test_failed_source_can_be_interviewed_only_with_intact_terminal_context():
    receipt = {
        "thread_id": "retained",
        "final_payload_valid": True,
        "provider_error_event_count": 0,
        "source_status": "failed",
    }
    assert posttest_context_available(receipt)
    for change in (
        {"thread_id": None},
        {"final_payload_valid": False},
        {"provider_error_event_count": 1},
    ):
        assert not posttest_context_available({**receipt, **change})


def test_ec_twelve_batch_card_has_no_unintended_process_time_limit():
    card = resource_card()
    assert card.vessel_start_limit == card.final_assay_limit == 12
    assert card.nonfinal_instrument_use_limit == 12
    assert card.process_time_limit_s is None
    # Existing legal per-operation maxima; stock cannot preempt the operation envelope.
    assert card.stock_limits["reagent_mol"] >= 0.04 * card.operation_attempt_limit
    assert card.stock_limits["solvent_L"] >= 0.08 * card.operation_attempt_limit


def test_ec_prediction_pairs_change_only_potential_and_preserve_legacy_version():
    rows = queries()
    assert len(rows) == 12
    assert len({json.dumps(r["actions"], sort_keys=True) for r in rows}) == 12
    assert sum(r["potential_domain"] == "negative" for r in rows) == 6
    for left, right in zip(rows[::2], rows[1::2], strict=True):
        a, b = json.loads(json.dumps(left["actions"])), json.loads(json.dumps(right["actions"]))
        assert a[2].pop("potential_V") == -0.8
        assert b[2].pop("potential_V") == 0.8
        assert a == b
    old = queries(LEGACY_QUERY_VERSION)
    assert all(r["actions"][2]["potential_V"] > 0 for r in old)
    assert max(r["actions"][3]["duration_s"] for r in old) == 2400
    assert "7200" not in prediction_question(old)


def test_ec_scoring_reports_domains_without_relabelling_historical_questions():
    query_set = queries()
    truth = {q["query_id"]: dict.fromkeys(METRICS, 0.5) for q in query_set}
    payload = {
        "predictions": [
            {
                "query_id": q["query_id"],
                **{
                    m: {
                        "estimate": 0.5 if q["potential_domain"] == "negative" else 0.7,
                        "lower80": 0.4,
                        "upper80": 0.8,
                    }
                    for m in METRICS
                },
            }
            for q in query_set
        ]
    }
    evaluation = evaluate_predictions(payload, truth, query_set=query_set)
    assert evaluation["metrics"][METRICS[0]]["n"] == 12
    assert evaluation["groups"]["potential_domain:negative"][METRICS[0]]["mae"] == 0
    assert evaluation["groups"]["potential_domain:positive"][METRICS[0]]["n"] == 6
    old = evaluate_predictions(payload, truth, query_set=queries(LEGACY_QUERY_VERSION))
    assert old["groups"] == {}
    assert not evaluate_predictions(payload, {}, query_set=query_set)["valid"]


def test_ec_posttest_uses_saved_design_instead_of_current_questions(tmp_path, monkeypatch):
    from scripts import run_work_ii_ec_dual_goal_trial as runner

    captured = []
    monkeypatch.setattr(runner, "build_command", lambda *args, **kwargs: [])

    def launch(command, message, *args):
        captured.append(message)
        return {"payload": {"report": "retained"}, "thread_id": "thread"}

    monkeypatch.setattr(runner, "launch", launch)
    agent = SimpleNamespace(home_root=tmp_path, followup_environment={})
    design = {
        "K1": "saved K1",
        "K2": "saved seven questions",
        "queries": queries(LEGACY_QUERY_VERSION),
    }
    for stage in ("K1", "Q", "K2"):
        runner.posttest(agent, tmp_path, stage, "thread", {}, design=design)
    assert captured[0] == design["K1"] and captured[2] == design["K2"]
    assert json.dumps(design["queries"]) in captured[1]
    assert "7200" not in captured[1]
