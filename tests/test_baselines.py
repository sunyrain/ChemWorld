from __future__ import annotations

from chemworld.eval.runner import make_agent, run_agent


def test_baseline_runner_smoke(tmp_path) -> None:
    output = tmp_path / "random.jsonl"
    history = run_agent(
        env_id="ChemWorld",
        agent=make_agent("random"),
        world_split="public-dev",
        budget=4,
        objective="balanced",
        seed=3,
        output_path=output,
    )
    assert len(history) == 4
    assert output.exists()
    assert output.read_text(encoding="utf-8").count("\n") == 4


def test_greedy_runner_smoke(tmp_path) -> None:
    output = tmp_path / "greedy.jsonl"
    history = run_agent(
        env_id="ChemWorld",
        agent=make_agent("greedy"),
        world_split="public-dev",
        budget=4,
        objective="balanced",
        seed=4,
        output_path=output,
    )
    assert len(history) == 4


