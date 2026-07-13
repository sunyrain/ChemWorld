from __future__ import annotations

from chemworld.agents.random import RandomAgent
from chemworld.data.logging import load_jsonl
from chemworld.eval.runner import run_agent
from chemworld.tasks import get_task


def test_runner_separates_private_agent_rng_from_world_seed(tmp_path) -> None:
    task = get_task("partition-discovery")
    paths = [tmp_path / "method-a.jsonl", tmp_path / "method-b.jsonl"]
    for method_seed, path in zip((101, 202), paths, strict=True):
        run_agent(
            env_id=task.env_id,
            agent=RandomAgent(),
            world_split=task.world_split,
            budget=task.budget,
            objective=task.objective,
            seed=11_000,
            agent_seed=method_seed,
            task_id=task.task_id,
            output_path=path,
            budget_override=10,
            safety_limit_override=0.2270542597781983,
        )

    left, right = (load_jsonl(path) for path in paths)
    assert left[0]["seed"] == right[0]["seed"] == 11_000
    assert left[0]["agent_metadata"]["agent_seed_disclosure"] == "private_committed"
    assert "seed" not in left[0]["agent_metadata"]
    assert left[0]["agent_metadata"]["safety_limit_override"] == 0.2270542597781983
    assert [item["action"] for item in left] != [item["action"] for item in right]


def test_runner_rejects_ambiguous_risk_override() -> None:
    task = get_task("partition-discovery")
    try:
        run_agent(
            env_id=task.env_id,
            agent=RandomAgent(),
            world_split=task.world_split,
            budget=task.budget,
            objective=task.objective,
            seed=11_000,
            task_id=task.task_id,
            evaluation_policy="vnext_risk_cost",
            safety_limit_override=0.2,
        )
    except ValueError as exc:
        assert "cannot be combined" in str(exc)
    else:  # pragma: no cover - fail-closed guard
        raise AssertionError("ambiguous risk policies must be rejected")
