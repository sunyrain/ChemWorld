from __future__ import annotations

import gymnasium as gym
import numpy as np
import pytest

from chemworld.agent_interface import action_schema, validate_action
from chemworld.rl.hybrid_actions import decode_conditional_hybrid_action
from chemworld.world.operations import OPERATION_TYPES, operation_contracts
from chemworld.wrappers import ConditionalHybridActionWrapper, action_mask


def _latent(wrapper: ConditionalHybridActionWrapper, operation: str) -> np.ndarray:
    vector = np.zeros(wrapper.action_space.shape, dtype=np.float32)
    vector[wrapper.operation_types.index(operation)] = 1.0
    return vector


def test_wrapper_projects_locked_public_recipe_choices() -> None:
    env = ConditionalHybridActionWrapper(
        gym.make("ChemWorld", task_id="partition-discovery", budget_override=8)
    )
    try:
        env.reset(seed=0)
        first = _latent(env, "add_solvent")
        solvent_coordinate = len(env.operation_types) + env.parameter_keys.index("solvent")
        first[solvent_coordinate] = -1.0
        first_action = env.action(first)
        assert validate_action(env, first_action)["valid"] is True
        env.step(first)

        schema = action_schema(env, "add_solvent")
        solvent_field = next(field for field in schema["fields"] if field["field"] == "solvent")
        assert solvent_field["locked_for_current_experiment"] is True
        assert solvent_field["choices"] == [first_action["solvent"]]

        second = first.copy()
        second[solvent_coordinate] = 1.0
        second_action = env.action(second)
        assert second_action["solvent"] == first_action["solvent"]
        assert validate_action(env, second_action)["valid"] is True
    finally:
        env.close()


def test_wrapper_filters_final_assay_until_termination() -> None:
    env = ConditionalHybridActionWrapper(
        gym.make("ChemWorld", task_id="partition-discovery", budget_override=8)
    )
    try:
        env.reset(seed=0)
        env.step(_latent(env, "add_reagent"))
        env.step(_latent(env, "add_solvent"))
        measure = _latent(env, "measure")
        instrument_coordinate = len(env.operation_types) + env.parameter_keys.index("instrument")
        measure[instrument_coordinate] = -1.0

        raw_schema = action_schema(env, "measure")
        assert raw_schema["fields"][0]["choices"][0] == "final_assay"
        projected = env.action(measure)

        assert projected["instrument"] != "final_assay"
        assert validate_action(env, projected)["valid"] is True
    finally:
        env.close()


def test_decoder_uses_dynamic_public_bounds_and_cooling_constraint() -> None:
    base = gym.make("ChemWorld", task_id="reaction-to-crystallization")
    try:
        assert isinstance(base.action_space, gym.spaces.Dict)
        vector = np.zeros(49, dtype=np.float32)
        vector[OPERATION_TYPES.index("cool_crystallize")] = 1.0
        required = list(operation_contracts()["cool_crystallize"].required_fields)
        schema = {
            "operation": "cool_crystallize",
            "valid_operation_type": True,
            "required_fields": required,
            "fields": [
                {
                    "field": "target_temperature_K",
                    "bounds": {"low": 280.0, "high": 300.0},
                    "lower_bound_inclusive": True,
                    "upper_bound_inclusive": True,
                },
                {
                    "field": "duration_s",
                    "bounds": {"low": 1.0, "high": 14400.0},
                    "lower_bound_inclusive": False,
                    "upper_bound_inclusive": True,
                },
            ],
            "constraints": [
                {
                    "id": "payload_coupling:maximum_cooling_rate_K_s",
                    "kind": "cross_field_upper_bound",
                    "parameters": {
                        "current_temperature_K": 400.0,
                        "maximum_cooling_rate_K_s": 0.25,
                    },
                }
            ],
        }
        duration_coordinate = len(OPERATION_TYPES) + tuple(
            key for key in base.action_space.spaces if key != "operation"
        ).index("duration_s")
        vector[duration_coordinate] = -1.0

        decoded = decode_conditional_hybrid_action(
            vector,
            event_action_space=base.action_space,
            operation_mask=[True] * len(OPERATION_TYPES),
            operation_schema=schema,
        )

        target = float(np.asarray(decoded["target_temperature_K"]).reshape(-1)[0])
        duration = float(np.asarray(decoded["duration_s"]).reshape(-1)[0])
        assert 280.0 <= target <= 300.0
        assert duration >= (400.0 - target) / 0.25
    finally:
        base.close()


def test_adapter_uses_only_public_schema_mask_and_validation() -> None:
    env = ConditionalHybridActionWrapper(
        gym.make("ChemWorld", task_id="reaction-to-distillation", budget_override=8)
    )
    try:
        env.reset(seed=0)
        vector = _latent(env, "distill")
        selected = OPERATION_TYPES[int(env.action(vector)["operation"])]
        assert selected != "distill"
        assert action_mask(env)[OPERATION_TYPES.index(selected)] is True
    finally:
        env.close()


@pytest.mark.parametrize(
    "task_id",
    [
        "partition-discovery",
        "reaction-to-crystallization",
        "reaction-to-distillation",
        "flow-reaction-optimization",
    ],
)
@pytest.mark.parametrize("parameter_endpoint", [-1.0, 1.0])
def test_public_schema_adapter_projects_exact_latent_endpoints(
    task_id: str, parameter_endpoint: float
) -> None:
    env = ConditionalHybridActionWrapper(
        gym.make("ChemWorld", task_id=task_id, budget_override=64)
    )
    try:
        env.reset(seed=0)
        available = action_mask(env)
        for operation_index, is_available in enumerate(available):
            if not is_available:
                continue
            latent = np.full(env.action_space.shape, parameter_endpoint, dtype=np.float32)
            latent[: len(env.operation_types)] = -1.0
            latent[operation_index] = 1.0

            decoded = env.action(latent)
            validation = validate_action(env, decoded)

            assert validation["valid"] is True, (
                task_id,
                env.operation_types[operation_index],
                parameter_endpoint,
                decoded,
                validation["invalid_reasons"],
            )
    finally:
        env.close()


@pytest.mark.parametrize(
    "task_id",
    [
        "partition-discovery",
        "reaction-to-crystallization",
        "reaction-to-distillation",
        "flow-reaction-optimization",
    ],
)
def test_public_schema_adapter_keeps_seeded_walks_dispatchable(task_id: str) -> None:
    env = ConditionalHybridActionWrapper(
        gym.make("ChemWorld", task_id=task_id, budget_override=64)
    )
    rng = np.random.default_rng(3107)
    try:
        env.reset(seed=3107)
        for step in range(64):
            latent = rng.uniform(-1.0, 1.0, size=env.action_space.shape).astype(np.float32)
            decoded = env.action(latent)
            validation = validate_action(env, decoded)
            assert validation["valid"] is True, (
                task_id,
                step,
                decoded,
                validation["invalid_reasons"],
            )
            _, _, terminated, truncated, _ = env.step(latent)
            if terminated or truncated:
                env.reset(seed=3108 + step)
    finally:
        env.close()
