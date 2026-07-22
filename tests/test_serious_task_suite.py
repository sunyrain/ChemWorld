from __future__ import annotations

import json

import gymnasium as gym
import pytest

import chemworld  # noqa: F401
from chemworld.agents import CodexSubagentOnlineAgent
from chemworld.eval.baseline_report import SERIOUS_BASELINE_AGENTS, generate_baseline_report
from chemworld.eval.paper_artifact import create_paper_artifact
from chemworld.eval.runner import AGENT_REGISTRY, make_agent, run_agent
from chemworld.tasks import SERIOUS_TASK_IDS, get_task
from chemworld.world.parameters import WORLD_FAMILY_VERSION


def test_serious_benchmark_v1_set_is_frozen() -> None:
    assert SERIOUS_TASK_IDS == (
        "partition-discovery",
        "reaction-to-crystallization",
        "reaction-to-distillation",
        "flow-reaction-optimization",
        "electrochemical-conversion",
        "equilibrium-characterization",
    )
    for task_id in SERIOUS_TASK_IDS:
        task = get_task(task_id)
        assert task.env_id == "ChemWorld"
        assert task.world_law_id == WORLD_FAMILY_VERSION
        assert task.contract_hash
        assert task.kernel_maturity.proxy_allowed is False
        assert task.to_card()["release_status"] == "serious-benchmark-v1"
        assert "serious" in task.to_card()["suite_memberships"]


@pytest.mark.parametrize("task_id", SERIOUS_TASK_IDS)
def test_serious_tasks_reset_with_public_contracts(task_id: str) -> None:
    task = get_task(task_id)
    env = gym.make("ChemWorld", task_id=task.task_id, seed=task.seeds[0])
    try:
        _, info = env.reset(seed=task.seeds[0])
        provenance = env.unwrapped.evaluator_provenance()
        assert info["task_id"] == task.task_id
        assert info["task_contract_hash"] == task.contract_hash
        assert provenance["mechanism_hash"]
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
        observation, reward, terminated, truncated, info = env.step(
            {"operation": "measure", "instrument": "ph_meter"}
        )
        assert not terminated
        assert not truncated
        assert reward > 0.0
        assert "pH_normalized" in info["observed_keys"]
        assert "pH_normalized" in observation
        assert "pH_normalized" in env.observation_space.spaces
        assert float(observation["pH_normalized"][0]) == pytest.approx(
            float(info["processed_estimate"]["pH_normalized"])
        )
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
        assert info["leaderboard_score"] > 0.0
        assert info["environment_reward"]["fresh_measurement"] is True
        assert reward == pytest.approx(info["environment_reward"]["score_delta"])
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
        json.loads(line) for line in output.read_text(encoding="utf-8").splitlines() if line.strip()
    ]
    assert records[-1]["agent_metadata"]["agent_family"] == "codex_subagent"
    assert records[-1]["agent_metadata"]["requires_online_model"] is False


def test_codex_online_protocol_is_external_only_not_inprocess_agent() -> None:
    assert "codex_subagent_online" not in AGENT_REGISTRY
    with pytest.raises(ValueError, match="Unknown agent"):
        make_agent("codex_subagent_online")
    manifest = CodexSubagentOnlineAgent().manifest()
    assert manifest["execution_policy"] == "external_codex_subagent_orchestrator"
    assert manifest["replay_agent"] == "codex_subagent_replay"


def test_serious_baseline_report_smoke_contains_equilibrium_metrics(tmp_path) -> None:
    report = generate_baseline_report(
        task_ids=["equilibrium-characterization"],
        agents=["scripted_chemistry", "codex_subagent_replay"],
        seeds=[0],
        output_dir=tmp_path / "baseline",
    )
    assert report.result_count == 2
    assert report.solver_provenance["schema_version"] == "chemworld-solver-provenance-0.2"
    # Replay traces remain available as diagnostics, but are not an official
    # cross-task baseline because their fixed action plan is task-specific.
    assert "codex_subagent_replay" not in SERIOUS_BASELINE_AGENTS
    rows = report.summary_rows
    assert {row["agent_name"] for row in rows} == {
        "scripted_chemistry",
        "codex_subagent_replay",
    }
    for row in rows:
        assert "mean_equilibrium_confidence" in row
        assert "mean_equilibrium_residual" in row
        assert float(row["mean_equilibrium_confidence"]) > 0.0


def test_serious_artifact_smoke_includes_solver_provenance(tmp_path) -> None:
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
