from copy import deepcopy

import gymnasium as gym
import pytest
from scripts.run_research_documents_demo import run

import chemworld  # noqa: F401
from chemworld.agent_interface import task_prompt
from chemworld.data.logging import TrajectoryLogger, load_jsonl
from chemworld.eval.verify import verify_records
from chemworld.runtime.semantics import RUNTIME_SEMANTICS_ID


def test_current_runtime_replays_and_old_or_mixed_identity_never_executes(tmp_path, monkeypatch):
    output = tmp_path / "documents"
    summary = run(output)
    assert summary["replay"]["verified"]
    records = load_jsonl(output / "trajectory.jsonl")
    assert all(r["runtime_semantics_id"] == RUNTIME_SEMANTICS_ID for r in records)
    variants = []
    missing = deepcopy(records)
    for row in missing:
        row.pop("runtime_semantics_id")
    variants.append(missing)
    outdated = deepcopy(records)
    for row in outdated:
        row["runtime_semantics_id"] = "outdated"
    variants.append(outdated)
    mixed = deepcopy(records)
    mixed[-1]["runtime_semantics_id"] = "outdated"
    variants.append(mixed)

    def no_execution(*args, **kwargs):
        pytest.fail("historical records must not enter the current execution engine")

    monkeypatch.setattr(gym, "make", no_execution)
    for variant in variants:
        result = verify_records(variant, tolerance=0.0)
        assert not result.verified and result.checked_steps == 0
        assert result.mismatches[0]["field"] == "runtime_semantics_id"
        assert "original frozen runtime and uv.lock" in result.mismatches[0]["reason"]


def rejected_actions_path(path):
    env = gym.make("ChemWorld", task_id="reaction-to-assay", seed=0)
    try:
        env.reset(seed=0)
        core = env.unwrapped
        before = core._state
        task = {**core.task_info(), **core.evaluator_provenance()}
        contract = task["risk_signal_contract"]
        assert contract["physical_hazard_probability"] is False
        assert "rejected action with no physical state change" in task_prompt(env)["text"]
        with TrajectoryLogger(path) as logger:
            for step in range(1, 14):
                action = {"operation": "measure", "instrument": "hplc"}
                observation, reward, terminated, truncated, info = env.step(action)
                logger.log(
                    task_info=task,
                    step=step,
                    action=action,
                    observation=observation,
                    reward=reward,
                    terminated=terminated,
                    truncated=truncated,
                    info=info,
                    agent_metadata={},
                )
                assert info["transaction_status"] == "rolled_back"
                assert info["sample_consumed"] == 0.0
                assert info["risk_signal_contract"] == contract
                after = core._state
                assert after.phases == before.phases
                assert after.temperature_K == before.temperature_K
                assert after.volume_L == before.volume_L
                assert after.species_amounts == before.species_amounts
        assert after.ledger.risk == 1.0
        assert not info["observed_mask"]["safety_risk"]
        assert "not a safety assessment" in contract["missing_penalty"]
        records = load_jsonl(path)
        assert all(r["risk_signal_contract"] == contract for r in records)
        assert verify_records(records, tolerance=0.0).verified
        return {
            "operations": 13,
            "rejected": 13,
            "physical_state_unchanged": True,
            "penalty": after.ledger.risk,
            "public_penalty_observed": False,
            "sample_consumed_L": 0.0,
            "exact_replay": True,
        }
    finally:
        env.close()


def test_procedural_penalties_do_not_imply_physical_hazard(tmp_path):
    rejected_actions_path(tmp_path / "rejected.jsonl")
