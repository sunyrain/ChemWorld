from __future__ import annotations

import copy
from types import SimpleNamespace

import gymnasium as gym
import pytest
from scripts import run_work_ii_c_pilot as c
from scripts.run_work_ii_astra_full_process_trial import reference_actions

from chemworld.agents.diagnostic_numerics import FOLLOWUP_NUMERICS
from chemworld.materials import material_choice_labels
from chemworld.runtime.full_process_contract import (
    FULL_PROCESS_FREE_RESEARCH_CONTRACT,
    FULL_PROCESS_SEED_CONTRACT,
)


@pytest.mark.parametrize("arm", c.ARMS)
def test_c_actual_material_tool_and_dynamic_particle_contract(arm):
    reply = c.check_public(arm)
    assert reply["anonymous"] and reply["particle_available"]
    assert (reply["payload"]["material_information"]["dossier"] is None) == (arm == "Opaque")
    assert material_choice_labels("solvent", task_id=c.TASK)["3"] == "solvent-S3"
    assert material_choice_labels("catalyst", task_id=c.TASK)["1"] == "catalyst-C1"


@pytest.mark.parametrize(
    "contract,open_measurements",
    [
        (FULL_PROCESS_SEED_CONTRACT, False),
        (FULL_PROCESS_FREE_RESEARCH_CONTRACT, True),
    ],
)
def test_new_contract_frees_measurement_order_preserving_physical_preconditions(
    contract,
    open_measurements,
):
    env = gym.make(
        "ChemWorld", task_id=c.TASK, seed=0, budget_override=100, full_process_contract_id=contract
    )
    try:
        env.reset(seed=0)
        _, _, _, _, invalid = env.step({"operation": "filter_crystals"})
        assert invalid["transaction_status"] == "rolled_back"
        for action in [a for a in reference_actions(c.TASK)[:8] if a["operation"] != "measure"]:
            assert env.step(action)[4]["transaction_status"] == "committed"
        seed = {"operation": "seed_crystals", "seed_mass_g": 0.006}
        info = env.step(seed)[4]
        assert (info["transaction_status"] == "committed") == open_measurements
        if not open_measurements:
            assert not info["preconditions"]["seed_crystals_requires_current_reaction_assay"]
            env.step({"operation": "measure", "instrument": "hplc"})
            assert env.step(seed)[4]["transaction_status"] == "committed"
        assert env.step(c.cool(278.15))[4]["transaction_status"] == "committed"
        filtered = env.step({"operation": "filter_crystals"})[4]
        assert (filtered["transaction_status"] == "committed") == open_measurements
    finally:
        env.close()


def test_v5_preserves_v4_thermal_and_seed_accounting_for_identical_legal_actions():
    truths = []
    for contract in (FULL_PROCESS_SEED_CONTRACT, FULL_PROCESS_FREE_RESEARCH_CONTRACT):
        env = gym.make(
            "ChemWorld",
            task_id=c.TASK,
            seed=0,
            budget_override=100,
            full_process_contract_id=contract,
        )
        try:
            env.reset(seed=0)
            for action in reference_actions(c.TASK)[:-2]:
                assert env.step(action)[4]["transaction_status"] == "committed"
            base = env.unwrapped
            truths.append(base.observation_kernel._truth_values(base._state))
        finally:
            env.close()
    assert truths[0] == truths[1]


def test_c_posttest_uses_actual_saved_budget_and_thread(tmp_path, monkeypatch):
    captured = {}

    def capture(command, message, *args, **kwargs):
        captured.update(command=command, message=message, kwargs=kwargs)
        return {"payload": {"report": "answer"}, "thread_id": "original"}

    monkeypatch.setattr(c, "launch", capture)
    agent = SimpleNamespace(home_root=tmp_path, followup_environment={})
    c.posttest(
        agent,
        tmp_path,
        "K1",
        "original",
        {},
        {"posttest_numerics": FOLLOWUP_NUMERICS.to_dict(), "K1": "saved question"},
    )
    assert captured["message"] == "saved question"
    assert captured["kwargs"]["numerics_budget"] == FOLLOWUP_NUMERICS
    assert "original" in captured["command"]
    assert "128" in (tmp_path / "followup/instructions.md").read_text()


def test_prediction_error_does_not_become_execution_failure():
    truth = {
        q["query_id"]: {**dict.fromkeys(c.METRICS, 0.2), "particles_present": True}
        for q in c.queries()
    }
    payload = {
        "predictions": [
            {
                "query_id": k,
                "particles_present": True,
                "quality_feasible": False,
                **{m: {"estimate": 0.8, "lower80": 0.7, "upper80": 0.9} for m in c.METRICS},
            }
            for k in truth
        ]
    }
    result = c.evaluate(payload, truth, c.queries())
    assert result["valid"]
    assert result["metrics"]["crystal_yield"]["mae"] == pytest.approx(0.6)
    bad = copy.deepcopy(payload)
    bad["predictions"][0]["crystal_yield"]["lower80"] = 0.95
    assert not c.evaluate(bad, truth, c.queries())["valid"]
