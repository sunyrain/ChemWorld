from __future__ import annotations

import json

from chemworld.agents.llm import ReplayLLMAgent
from chemworld.eval.runner import run_agent


def test_replay_llm_agent_executes_event_sequence(tmp_path) -> None:
    replay_path = tmp_path / "llm_replay.jsonl"
    replay_path.write_text(
        json.dumps(
            {
                "temperature": 115.0,
                "time": 1.2,
                "initial_concentration": 0.7,
                "stirring_speed": 680.0,
                "catalyst": 1,
                "solvent": 2,
                "hypothesis": "moderate temperature should limit degradation",
                "rationale": "start with a balanced condition",
            }
        )
        + "\n",
        encoding="utf-8",
    )

    history = run_agent(
        env_id="ChemWorld",
        agent=ReplayLLMAgent(replay_path),
        world_split="public-dev",
        budget=6,
        objective="balanced",
        seed=21,
    )

    assert len(history) == 6
    assert history[0].action["operation"] == "add_solvent"
    assert history[-1].action == {"operation": "measure", "instrument": "final_assay"}

