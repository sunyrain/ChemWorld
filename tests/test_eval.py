from __future__ import annotations

from chemworld.data.logging import load_jsonl
from chemworld.eval.metrics import evaluate_records
from chemworld.eval.runner import make_agent, run_agent


def test_evaluation_from_jsonl(tmp_path) -> None:
    output = tmp_path / "run.jsonl"
    run_agent(
        env_id="ChemWorld",
        agent=make_agent("lhs"),
        world_split="public-dev",
        budget=5,
        objective="balanced",
        seed=11,
        output_path=output,
    )
    records = load_jsonl(output)
    result = evaluate_records(records)
    assert result.steps == 5
    assert 0.0 <= result.total_score <= 1.0
    assert result.agent_name in {"latin_hypercube", "LatinHypercubeAgent"}


def test_evaluation_uses_final_assay_leaderboard_score() -> None:
    base_record = {
        "agent_metadata": {"agent_name": "probe"},
        "env_id": "ChemWorld",
        "world_split": "public-test",
        "seed": 0,
        "constraint_flags": {"unsafe": False, "high_cost": False},
    }
    records = [
        {
            **base_record,
            "reward": 0.95,
            "leaderboard_score": None,
            "observation": {
                "yield": 0.95,
                "selectivity": 0.95,
                "conversion": None,
                "cost": 0.1,
                "safety_risk": 0.1,
                "score": 0.95,
            },
        },
        {
            **base_record,
            "reward": 0.20,
            "leaderboard_score": 0.20,
            "observation": {
                "yield": 0.20,
                "selectivity": 0.80,
                "conversion": 0.30,
                "cost": 0.1,
                "safety_risk": 0.1,
                "score": 0.20,
            },
        },
    ]

    result = evaluate_records(records)

    assert result.final_best_score == 0.20
    assert result.best_valid_score == 0.20

