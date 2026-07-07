from __future__ import annotations

from chemworld.agents.bo import (
    GaussianProcessBOAgent,
    RandomForestEIAgent,
    SafetyConstrainedBOAgent,
)
from chemworld.data.logging import load_jsonl
from chemworld.eval.runner import run_agent


def test_surrogate_baselines_smoke(tmp_path) -> None:
    agents = [
        GaussianProcessBOAgent(n_initial=2, n_candidates=16),
        RandomForestEIAgent(n_initial=2, n_candidates=16, n_estimators=8),
        SafetyConstrainedBOAgent(n_initial=2, n_candidates=16),
    ]
    for index, agent in enumerate(agents):
        history = run_agent(
            env_id="ChemWorld",
            agent=agent,
            world_split="public-dev",
            budget=12,
            objective="balanced",
            seed=index,
            output_path=tmp_path / f"{agent.name}.jsonl",
        )
        assert 1 <= len(history) <= 12
        assert history[-1].action == {"operation": "measure", "instrument": "final_assay"}
        assert max(record.reward for record in history) >= 0.0


def test_bo_campaign_runs_multiple_recipes(tmp_path) -> None:
    path = tmp_path / "campaign_bo.jsonl"
    history = run_agent(
        env_id="ChemWorld",
        agent=GaussianProcessBOAgent(n_initial=2, n_candidates=16),
        world_split="public-test",
        budget=72,
        objective="balanced",
        seed=3,
        task_id="reaction-optimization-standard",
        output_path=path,
    )
    records = load_jsonl(path)
    final_assays = [
        record
        for record in records
        if record.get("operation_type") == "measure"
        and record.get("instrument") == "final_assay"
    ]
    assert len(history) > 6
    assert len(final_assays) >= 2
    assert records[0]["episode_mode"] == "campaign"
    assert records[0]["benchmark_task_id"] == "reaction-optimization-standard"

