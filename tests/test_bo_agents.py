from __future__ import annotations

from chemworld.agents.bo import (
    GaussianProcessBOAgent,
    RandomForestEIAgent,
    SafetyConstrainedBOAgent,
)
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

