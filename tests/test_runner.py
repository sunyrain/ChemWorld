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


def test_unknown_agent_operation_is_retained_as_invalid_transaction(tmp_path) -> None:
    class UnknownOperationAgent:
        name = "unknown-operation-test"

        def reset(self, task_info, seed):
            del task_info, seed

        def act(self, history):
            del history
            return {"operation": "model_failure"}

        def update(self, action, observation, reward, info):
            del action, observation, reward, info

        def manifest(self):
            return {}

    output = tmp_path / "invalid.jsonl"
    records = run_agent(
        env_id="ChemWorld",
        agent=UnknownOperationAgent(),
        world_split="public-test",
        budget=1,
        objective="balanced",
        seed=7,
        task_id="partition-discovery",
        output_path=output,
        budget_override=1,
    )

    assert len(records) == 1
    assert records[0].action == {"operation": "model_failure"}
    assert records[0].info["transaction_status"] == "validation_failed"
    assert records[0].info["operation_type"] == "model_failure"
    assert records[0].info["preconditions"]["action_schema_valid"] is False


def test_complete_experiment_budget_stops_campaign_without_synthetic_action(
    tmp_path,
) -> None:
    class SequenceAgent:
        name = "sequence-test"

        def reset(self, task_info, seed):
            del seed
            self.task_info = task_info
            self.actions = iter(
                [
                    {"operation": "add_solvent", "volume_L": 0.02, "solvent": 1},
                    {"operation": "add_reagent", "amount_mol": 0.006},
                    {"operation": "terminate"},
                    {"operation": "measure", "instrument": "final_assay"},
                    {"operation": "add_solvent", "volume_L": 0.02, "solvent": 1},
                ]
            )

        def act(self, history):
            del history
            return next(self.actions)

        def update(self, action, observation, reward, info):
            del action, observation, reward, info

        def manifest(self):
            return {}

    agent = SequenceAgent()
    records = run_agent(
        env_id="ChemWorld",
        agent=agent,
        world_split="public-test",
        budget=8,
        objective="balanced",
        seed=1200,
        task_id="flow-reaction-optimization",
        output_path=tmp_path / "one-experiment.jsonl",
        budget_override=8,
        episode_mode_override="campaign",
        method_resource_limits={
            "operation_limit": 8,
            "complete_experiment_limit": 1,
        },
    )

    assert len(records) == 4
    assert records[-1].action == {"operation": "measure", "instrument": "final_assay"}
    assert records[-1].method_resources["complete_experiment_count"] == 1
    assert agent.task_info["method_budget_contract"] == {
        "operation_limit": 8,
        "complete_experiment_limit": 1,
    }
