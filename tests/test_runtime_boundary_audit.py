from __future__ import annotations

from pathlib import Path

import gymnasium as gym

import chemworld  # noqa: F401
from chemworld.world.operations import OPERATION_TYPES


def test_chemworld_env_has_no_operation_specific_step_branching() -> None:
    source = Path("src/chemworld/envs/chemworld_env.py").read_text(encoding="utf-8")

    assert "runtime.apply_transaction" in source
    assert "runtime.apply_invalid_transaction" in source
    assert ".domain_services" not in source
    assert "operation_record.operation_type" not in source
    for operation in OPERATION_TYPES:
        assert f'== "{operation}"' not in source
        assert f"== '{operation}'" not in source


def test_invalid_action_path_is_runtime_owned() -> None:
    env = gym.make("ChemWorld", task_id="reaction-to-assay", seed=0)
    env.reset(seed=0)
    before = env.unwrapped._state

    _obs, _reward, _terminated, _truncated, info = env.step(
        {"operation": "heat", "target_temperature_K": 360.0, "duration_s": 60.0}
    )
    after = env.unwrapped._state

    assert info["kernel_id"] == "validation:invalid_action"
    assert info["transaction_status"] == "validation_failed"
    assert info["affected_ledgers"] == ["process"]
    assert after.phases == before.phases
    assert after.species == before.species
    assert after.ledger.cost > before.ledger.cost
    env.close()
