"""Conditional hybrid action and policy semantics for RL adapters.

The benchmark action is categorical at the operation level and exposes only
the parameters required by the selected operation.  Stable-Baselines3 does not
provide a native categorical-plus-continuous policy distribution, so PPO/SAC
use an explicitly labelled Box latent adapter.  Irrelevant latent coordinates
never enter the executed action or trajectory digest.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any

import gymnasium as gym
import numpy as np

from chemworld.data.logging import to_builtin
from chemworld.world.operations import OPERATION_TYPES, operation_contracts

ACTION_SCHEMA_VERSION = "chemworld-conditional-hybrid-action-0.1"
LATENT_ADAPTER_VERSION = "chemworld-sb3-box-latent-adapter-0.1"
POLICY_DISTRIBUTION_SCHEMA_VERSION = "chemworld-masked-conditional-ppo-0.1"


def _sha256_json(payload: dict[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _space_contract(space: gym.Space[Any]) -> dict[str, Any]:
    if isinstance(space, gym.spaces.Discrete):
        return {"kind": "categorical", "cardinality": int(space.n)}
    if isinstance(space, gym.spaces.Box):
        return {
            "kind": "continuous",
            "shape": list(space.shape or ()),
            "low": to_builtin(np.asarray(space.low)),
            "high": to_builtin(np.asarray(space.high)),
            "dtype": str(space.dtype),
        }
    raise TypeError(f"unsupported event action component: {type(space).__name__}")


def conditional_hybrid_action_contract(
    event_action_space: gym.spaces.Dict,
) -> dict[str, Any]:
    """Return the canonical semantic contract and its deterministic digest."""

    parameter_keys = tuple(key for key in event_action_space.spaces if key != "operation")
    contracts = operation_contracts()
    conditional_parameters = {
        operation: [
            {
                "field": field,
                **_space_contract(event_action_space[field]),
            }
            for field in contracts[operation].required_fields
        ]
        for operation in OPERATION_TYPES
    }
    payload: dict[str, Any] = {
        "schema_version": ACTION_SCHEMA_VERSION,
        "semantic_action": {
            "operation": {
                "kind": "categorical",
                "categories": list(OPERATION_TYPES),
                "selection_policy": "public-affordance-masked categorical selection",
            },
            "parameters": {
                "kind": "operation_conditional",
                "by_operation": conditional_parameters,
                "irrelevant_parameter_policy": "excluded_from_execution_and_trajectory",
            },
        },
        "training_adapter": {
            "schema_version": LATENT_ADAPTER_VERSION,
            "framework_scope": ["stable-baselines3:PPO", "stable-baselines3:SAC"],
            "kind": "bounded_box_latent",
            "shape": [len(OPERATION_TYPES) + len(parameter_keys)],
            "bounds": [-1.0, 1.0],
            "operation_coordinate_count": len(OPERATION_TYPES),
            "parameter_coordinate_keys": list(parameter_keys),
            "operation_decode": "masked_argmax",
            "native_hybrid_distribution": False,
        },
        "empty_operation_mask_policy": (
            "retain global argmax so the environment records the invalid transition"
        ),
        "numeric_policy": "normalize decoded numpy values before execution",
    }
    payload["contract_hash"] = _sha256_json(payload)
    return payload


def policy_distribution_contract(parameter_keys: tuple[str, ...]) -> dict[str, Any]:
    """Return the dependency-free PPO probability-law contract.

    Preflight and checkpoint audits can verify this payload without importing
    Torch or Stable-Baselines3.  The executable distribution in
    :mod:`chemworld.rl.hybrid_policy` consumes the same contract.
    """

    if not parameter_keys or len(set(parameter_keys)) != len(parameter_keys):
        raise ValueError("policy parameter keys must be non-empty and unique")
    contracts = operation_contracts()
    payload: dict[str, Any] = {
        "schema_version": POLICY_DISTRIBUTION_SCHEMA_VERSION,
        "operation_distribution": "public-affordance-masked categorical",
        "parameter_distribution": "operation-conditional diagonal Gaussian",
        "parameter_keys": list(parameter_keys),
        "active_parameters": {
            operation: list(contracts[operation].required_fields)
            for operation in OPERATION_TYPES
        },
        "irrelevant_parameter_log_prob": False,
        "irrelevant_parameter_entropy": False,
        "box_carrier_is_semantic_distribution": False,
    }
    payload["contract_hash"] = _sha256_json(payload)
    return payload


def decode_conditional_hybrid_action(
    action: Any,
    *,
    event_action_space: gym.spaces.Dict,
    operation_mask: list[bool] | np.ndarray,
) -> dict[str, Any]:
    """Decode one SB3 latent vector into a categorical, conditional action."""

    parameter_keys = tuple(key for key in event_action_space.spaces if key != "operation")
    expected_shape = (len(OPERATION_TYPES) + len(parameter_keys),)
    vector = np.asarray(action, dtype=np.float32).reshape(-1)
    if vector.shape != expected_shape or not np.all(np.isfinite(vector)):
        raise ValueError(
            f"hybrid action latent must be a finite vector with shape {expected_shape}"
        )

    public_mask = np.asarray(operation_mask, dtype=bool)
    if public_mask.shape != (len(OPERATION_TYPES),):
        raise ValueError("public operation mask does not match the operation registry")
    logits = vector[: len(OPERATION_TYPES)]
    operation_index = int(
        np.argmax(np.where(public_mask, logits, -np.inf))
        if np.any(public_mask)
        else np.argmax(logits)
    )
    operation = OPERATION_TYPES[operation_index]
    required = set(operation_contracts()[operation].required_fields)
    unit = np.clip((vector[len(OPERATION_TYPES) :] + 1.0) / 2.0, 0.0, 1.0)
    payload: dict[str, Any] = {"operation": operation_index}
    for index, key in enumerate(parameter_keys):
        if key not in required:
            continue
        space = event_action_space[key]
        coordinate = float(unit[index])
        if isinstance(space, gym.spaces.Discrete):
            payload[key] = min(int(coordinate * space.n), space.n - 1)
        elif isinstance(space, gym.spaces.Box):
            value = space.low + coordinate * (space.high - space.low)
            payload[key] = to_builtin(np.asarray(value, dtype=space.dtype))
        else:
            raise TypeError(f"unsupported event action component: {key}={type(space).__name__}")
    return payload


__all__ = [
    "ACTION_SCHEMA_VERSION",
    "LATENT_ADAPTER_VERSION",
    "POLICY_DISTRIBUTION_SCHEMA_VERSION",
    "conditional_hybrid_action_contract",
    "decode_conditional_hybrid_action",
    "policy_distribution_contract",
]
