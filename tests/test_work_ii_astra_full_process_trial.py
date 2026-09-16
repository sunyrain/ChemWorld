from pathlib import Path

import gymnasium as gym
import pytest
from scripts.run_work_ii_astra_full_process_trial import (
    LIMITS,
    QUALITY,
    TASKS,
    FullProcessAgent,
    card,
    quality_checks,
    summarize,
)


@pytest.mark.parametrize("task", TASKS)
def test_single_vessel_trial_enforces_stock_and_exposes_complete_contract(tmp_path, task):
    env = gym.make(
        "ChemWorld",
        task_id=task,
        seed=0,
        episode_mode_override="single_experiment",
        budget_override=LIMITS[task],
        campaign_resource_card=card(task),
    )
    agent = FullProcessAgent(task=task, workspace=tmp_path / "lab", role_id="test")
    try:
        _, info = env.reset(seed=0)
        agent.reset(info, 0)
        contract = agent._task_contract
        assert contract["trial_quality_targets"] == QUALITY[task]
        assert "final_assay" in contract["instrument_contracts"]
        assert set(contract["operation_contracts"]) >= {"heat", "measure", "terminate"}
        assert agent.model == "gpt-6-astra"
        assert agent.reasoning_effort == "medium"
        env.step({"operation": "add_solvent", "volume_L": 0.04, "solvent": 0})
        env.step({"operation": "add_reagent", "amount_mol": 0.04})
        _, _, _, _, rejected = env.step({"operation": "add_reagent", "amount_mol": 0.001})
        assert rejected["transaction_status"] == "campaign_resource_rejected"
    finally:
        agent.close()
        env.close()


def test_quality_does_not_reward_empty_or_seed_only_product():
    assert not all(
        quality_checks(
            TASKS[1],
            {
                "crystal_purity": 1,
                "crystal_yield": 0,
                "crystal_fines_fraction": 0,
            },
        ).values()
    )
    assert not summarize(TASKS[0], [])["quality_passed"]
    assert not all(quality_checks(TASKS[0], {"purity": 1}).values())


def test_trial_launch_preserves_requested_model_disables_retries_and_nonlab_tools(tmp_path):
    agent = FullProcessAgent(task=TASKS[0], workspace=tmp_path / "lab", role_id="test")
    instructions = tmp_path / "instructions.md"
    instructions.write_text("Scientific experiment.", encoding="utf-8")
    command = agent._command(instructions_path=instructions, schema_path=Path("schema.json"))
    assert command[command.index("-m") + 1] == "gpt-6-astra"
    assert "request_max_retries=0,stream_max_retries=0" in " ".join(command)
    assert "requires_openai_auth=true" in " ".join(command)
    assert "--ignore-user-config" in command
    assert "shell_tool" in command
    assert "trial_quality_targets" in instructions.read_text(encoding="utf-8")
