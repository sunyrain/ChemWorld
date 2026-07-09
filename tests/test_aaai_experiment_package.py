from __future__ import annotations

import json

import gymnasium as gym
import pytest

import chemworld  # noqa: F401
from chemworld.eval.baseline_report import AAAI_BASELINE_AGENTS, generate_baseline_report
from chemworld.eval.paper_artifact import create_paper_artifact
from chemworld.eval.runner import make_agent, run_agent
from chemworld.tasks import AAAI_TASK_IDS, get_task


def test_aaai_task_set_is_frozen() -> None:
    assert AAAI_TASK_IDS == (
        "reaction-optimization-standard",
        "reaction-to-purification",
        "partition-discovery",
        "reaction-to-distillation",
        "electrochemical-conversion",
        "equilibrium-characterization",
    )
    for task_id in AAAI_TASK_IDS:
        task = get_task(task_id)
        assert task.env_id == "ChemWorld"
        assert task.world_law_id == "chemworld-physical-chemistry"
        assert task.contract_hash


@pytest.mark.parametrize("task_id", AAAI_TASK_IDS)
def test_aaai_tasks_reset_with_public_contracts(task_id: str) -> None:
    task = get_task(task_id)
    env = gym.make("ChemWorld", task_id=task.task_id, seed=task.seeds[0])
    try:
        _, info = env.reset(seed=task.seeds[0])
        assert info["task_id"] == task.task_id
        assert info["task_contract_hash"] == task.contract_hash
        assert info["mechanism_hash"]
        assert info["scoring_contract_hash"]
        assert info["observation_contract_hash"]
        assert info["physics_maturity"] == task.kernel_maturity.lowest_level.value
    finally:
        env.close()


def test_equilibrium_characterization_exposes_public_ph_meter_only() -> None:
    env = gym.make("ChemWorld", task_id="equilibrium-characterization", seed=0)
    try:
        env.reset(seed=0)
        for action in (
            {"operation": "add_solvent", "volume_L": 0.030, "solvent": 0},
            {"operation": "add_reagent", "amount_mol": 0.006},
        ):
            env.step(action)
        _, reward, terminated, truncated, info = env.step(
            {"operation": "measure", "instrument": "ph_meter"}
        )
        assert not terminated
        assert not truncated
        assert reward > 0.0
        assert "pH_normalized" in info["observed_keys"]
        assert "equilibrium_confidence" in info["processed_estimate"]
        assert info["raw_signal"]["kind"] == "ph_meter_signal"
        assert "pH" in info["raw_signal"]
        assert "pka" not in json.dumps(info["raw_signal"]).lower()
        assert "species_amounts" not in json.dumps(info["raw_signal"]).lower()
        assert 0.0 <= float(info["processed_estimate"]["pH_normalized"]) <= 1.0
    finally:
        env.close()


def test_equilibrium_final_assay_is_leaderboard_eligible() -> None:
    env = gym.make("ChemWorld", task_id="equilibrium-characterization", seed=0)
    try:
        env.reset(seed=0)
        for action in (
            {"operation": "add_solvent", "volume_L": 0.030, "solvent": 0},
            {"operation": "add_reagent", "amount_mol": 0.006},
            {"operation": "measure", "instrument": "ph_meter"},
            {"operation": "terminate"},
        ):
            env.step(action)
        _, reward, _, _, info = env.step({"operation": "measure", "instrument": "final_assay"})
        assert reward > 0.0
        assert info["leaderboard_score"] == pytest.approx(reward)
        assert "ph_meter" in info["raw_signal"]["channels"]
        assert "equilibrium_residual" in info["processed_estimate"]
    finally:
        env.close()


def test_codex_subagent_replay_agent_runs_equilibrium_trace(tmp_path) -> None:
    output = tmp_path / "codex_replay.jsonl"
    history = run_agent(
        env_id="ChemWorld",
        agent=make_agent("codex_subagent_replay"),
        world_split="public-test",
        budget=24,
        objective="balanced",
        seed=0,
        task_id="equilibrium-characterization",
        output_path=output,
    )
    assert history
    assert output.exists()
    records = [
        json.loads(line)
        for line in output.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    assert records[-1]["agent_metadata"]["agent_family"] == "codex_subagent"
    assert records[-1]["agent_metadata"]["requires_online_model"] is False


def test_aaai_baseline_report_smoke_contains_equilibrium_metrics(tmp_path) -> None:
    report = generate_baseline_report(
        task_ids=["equilibrium-characterization"],
        agents=["scripted_chemistry", "codex_subagent_replay"],
        seeds=[0],
        output_dir=tmp_path / "baseline",
    )
    assert report.result_count == 2
    assert report.solver_provenance["schema_version"] == "chemworld-solver-provenance-0.1"
    assert "codex_subagent_replay" in AAAI_BASELINE_AGENTS
    rows = report.summary_rows
    assert {row["agent_name"] for row in rows} == {
        "scripted_chemistry",
        "codex_subagent_replay",
    }
    for row in rows:
        assert "mean_equilibrium_confidence" in row
        assert "mean_equilibrium_residual" in row


def test_aaai_artifact_smoke_includes_solver_provenance(tmp_path) -> None:
    summary = create_paper_artifact(
        output_dir=tmp_path / "artifact",
        task_ids=["equilibrium-characterization"],
        agents=["scripted_chemistry"],
        seeds=[0],
    )
    provenance = tmp_path / "artifact" / "manifests" / "solver_provenance_manifest.json"
    assert summary["replay_verified"] is True
    assert provenance.exists()
    payload = json.loads(provenance.read_text(encoding="utf-8"))
    assert payload["tasks"][0]["task_id"] == "equilibrium-characterization"
    assert payload["solver_tolerances"]["acid_base_root_xtol"] == pytest.approx(1.0e-14)
