"""World, language, budget and denominator boundaries of the English matrix."""

import json
from types import SimpleNamespace

import pytest
from scripts import run_work_ii_ec_dual_goal_trial as ec
from scripts import run_work_ii_ec_pa_matrix as matrix
from scripts import run_work_ii_pa_single_trial as pa


def test_matrix_has_exact_authorized_denominators_and_ec_followups_are_last():
    rows = matrix.units()
    assert len(rows) == len({r["unit_id"] for r in rows}) == 90
    assert sum(r["budget"] for r in rows) == 1620
    assert sum(r["system"] == "EC" for r in rows) == 60
    assert sum(r["system"] == "PA" for r in rows) == 30
    extended = matrix.units(include_ps=True)
    assert extended[:90] == rows
    assert len(extended) == 102
    assert all(r["budget"] == 12 and r["world"]["world_id"] == "EC-W01" for r in extended[90:])
    assert {r["locus"] for r in extended[90:]} == {"P", "S"}
    assert len({json.dumps(w["world_interventions"]) for w in matrix.worlds("PA")}) == 5


@pytest.mark.parametrize("system", ["EC", "PA"])
@pytest.mark.parametrize("arm", pa.ARMS)
def test_world_five_twenty_four_public_entry_is_english_and_budget_matched(system, arm):
    entry = matrix.public_entry(system, matrix.worlds(system)[4], 24, arm)
    assert entry["passed"]
    assert entry["study_budget"]["complete_batches"] == 24
    assert entry["study_budget"]["final_assays"] == 24
    assert (entry["material_reply"]["material_information"]["dossier"] is None) == (arm == "Opaque")


@pytest.mark.parametrize("module", [ec, pa])
def test_new_questions_are_english_and_budget_prompt_scales(module):
    question = ec.prediction_question(ec.queries()) if module is ec else pa.question("Q")
    assert not matrix.CJK.search(json.dumps([module.K1, question, module.K2], ensure_ascii=False))
    assert "English" in module.K1 and "English" in module.K2
    assert "24" in module.source_system(24)
    assert "12" not in module.source_system(24)


@pytest.mark.parametrize("module,system", [(ec, "EC"), (pa, "PA")])
def test_physics_routes_world_and_budget_to_actual_runner(monkeypatch, tmp_path, module, system):
    captured = []
    monkeypatch.setattr(module, "run_agent", lambda **kwargs: captured.append(kwargs))
    world = matrix.worlds(system)[4]
    module.physics(object(), tmp_path / "unused.jsonl", world=world, batches=24)
    assert captured[0]["seed"] == 4
    assert captured[0]["world_interventions"] == world["world_interventions"]
    assert captured[0]["campaign_resource_card"].vessel_start_limit == 24
    assert captured[0]["budget_override"] == 720


def test_ec_entity_transpositions_follow_each_world():
    values = [
        ec.priors("E", "MisIndexed", world_id=w["world_id"], world_seed=w["world_seed"])[0][
            "descriptor_permutation"
        ]
        for w in matrix.worlds("EC")
    ]
    assert values == [[3, 1, 2, 0], [2, 1, 0, 3], [0, 3, 2, 1], [0, 1, 3, 2], [0, 2, 1, 3]]


def test_replay_passes_the_actual_world_intervention_manifest(monkeypatch):
    captured = []

    def verify(records, **kwargs):
        captured.append(kwargs)
        return SimpleNamespace(to_dict=lambda: {"verified": True})

    monkeypatch.setattr(ec, "verify_records", verify)
    manifest = matrix.worlds("PA")[1]["world_interventions"]
    assert ec.replay_with_progress([{}], "check", world_interventions=manifest)["verified"]
    assert captured == [{"tolerance": 0, "world_interventions": manifest}]


def test_new_pa_report_is_english_and_keeps_a_missing_source(tmp_path):
    root, out = tmp_path / "source", tmp_path / "report"
    root.mkdir()
    pa.write(
        root / "design.json",
        {
            "world_config": matrix.worlds("PA")[0],
            "arm": "Opaque",
            "source_batches": 24,
            "system": pa.source_system(24),
            "goal": pa.study_goal(24),
            "K1": pa.K1,
            "Q": pa.question("Q"),
            "K2": pa.K2,
        },
    )
    pa.write(
        root / "result.json",
        {
            "status": "failed",
            "protocol_version": pa.PROTOCOL_VERSION,
            "failure": {"stage": "source", "message": "retained startup failure"},
        },
    )
    pa.export(root, out)
    report = (out / "REPORT.md").read_text(encoding="utf-8")
    assert not matrix.CJK.search(report)
    assert "completed batches: 0/24" in report
    summary = pa.read(out / "summary.json")
    assert summary["english_output"] is None
    assert summary["status"] == "failed"
