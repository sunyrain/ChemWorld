"""Frozen Stable-Baselines3 policies exposed through the official agent runner."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Literal

import gymnasium as gym
import numpy as np

import chemworld  # noqa: F401
from chemworld.agents.base import BaseAgent, HistoryRecord
from chemworld.agents.interaction import AgentDecisionContext, InteractionCapabilities
from chemworld.rl.hybrid_actions import (
    conditional_hybrid_action_contract,
    decode_conditional_hybrid_action,
)
from chemworld.rl.hybrid_policy import policy_distribution_contract
from chemworld.rl.rewards import reward_contract
from chemworld.tasks import get_task
from chemworld.world.operations import OPERATION_TYPES

RLAlgorithm = Literal["ppo", "sac"]


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_manifest(value: str | Path | dict[str, Any]) -> dict[str, Any]:
    if isinstance(value, dict):
        return dict(value)
    payload = json.loads(Path(value).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("RL checkpoint manifest must be a JSON object")
    return payload


def build_frozen_rl_observation(
    public_view: dict[str, Any],
    context: AgentDecisionContext,
) -> tuple[np.ndarray, list[bool]]:
    """Rebuild the training observation from the official public view only."""

    rl_view = public_view.get("rl")
    if not isinstance(rl_view, dict) or rl_view.get("schema_version") != "chemworld-rl-view-0.2":
        raise ValueError("frozen RL policy requires the public RL view 0.2 contract")
    values = rl_view.get("vector")
    observed_mask = rl_view.get("mask")
    if not isinstance(values, list) or not isinstance(observed_mask, list):
        raise ValueError("public RL view is missing vector or observation mask")
    available = set(context.available_operations)
    operation_mask = [operation in available for operation in OPERATION_TYPES]
    campaign = context.campaign_state
    budget = max(int(campaign.get("budget", 1)), 1)
    operation_count = max(int(campaign.get("operation_count", 0)), 0)
    experiment_index = max(int(campaign.get("experiment_index", 0)), 0)
    summaries = campaign.get("experiment_summaries", [])
    summary_count = len(summaries) if isinstance(summaries, list) else 0
    progress = [
        min(operation_count / budget, 1.0),
        min(max(budget - operation_count, 0) / budget, 1.0),
        min(summary_count / max(experiment_index + 1, 1), 1.0),
    ]
    observation = np.asarray(
        [*values, *observed_mask, *[float(item) for item in operation_mask], *progress],
        dtype=np.float32,
    )
    if not np.all(np.isfinite(observation)):
        raise ValueError("frozen RL public observation must be finite")
    return observation, operation_mask


class FrozenSB3Agent(BaseAgent):
    """Inference-only PPO/SAC adapter with checkpoint and compute provenance.

    The adapter receives the exact public view exported to every official
    trajectory.  It cannot access the environment object, hidden world axis, or
    shaped training reward.
    """

    def __init__(
        self,
        *,
        algorithm: RLAlgorithm,
        checkpoint: str | Path,
        checkpoint_manifest: str | Path | dict[str, Any],
        task_id: str,
        deterministic: bool = False,
        policy_seed: int | None = None,
    ) -> None:
        if algorithm not in {"ppo", "sac"}:
            raise ValueError("algorithm must be ppo or sac")
        self.algorithm = algorithm
        self.name = algorithm
        self.checkpoint = Path(checkpoint).resolve()
        self.checkpoint_manifest = _load_manifest(checkpoint_manifest)
        self.declared_task_id = task_id
        self.deterministic = bool(deterministic)
        self.policy_seed = policy_seed
        self.checkpoint_sha256 = _sha256(self.checkpoint)
        if self.checkpoint_manifest.get("schema_version") != "chemworld-rl-checkpoint-0.2":
            raise ValueError(
                "unsupported RL checkpoint manifest; legacy checkpoints must be retrained "
                "under the current action and reward contracts"
            )
        if self.checkpoint_manifest.get("algorithm") != algorithm:
            raise ValueError("RL checkpoint algorithm does not match adapter")
        if self.checkpoint_manifest.get("task_id") != task_id:
            raise ValueError("RL checkpoint task does not match adapter")
        if self.checkpoint_manifest.get("checkpoint_sha256") != self.checkpoint_sha256:
            raise ValueError("RL checkpoint digest does not match its manifest")
        schema_env = gym.make("ChemWorld", task_id=task_id)
        try:
            if not isinstance(schema_env.action_space, gym.spaces.Dict):
                raise TypeError("ChemWorld event action space must be Dict")
            self._event_action_space = schema_env.action_space
        finally:
            schema_env.close()
        self.action_contract = conditional_hybrid_action_contract(self._event_action_space)
        self.reward_contract = reward_contract(get_task(task_id).allowed_operations)
        if self.checkpoint_manifest.get("action_contract_hash") != self.action_contract[
            "contract_hash"
        ]:
            raise ValueError("RL checkpoint action contract hash is incompatible")
        if self.checkpoint_manifest.get(
            "training_reward_contract_hash"
        ) != self.reward_contract["contract_hash"]:
            raise ValueError("RL checkpoint reward contract hash is incompatible")
        parameter_keys = tuple(
            str(item)
            for item in self.action_contract["training_adapter"][
                "parameter_coordinate_keys"
            ]
        )
        self.policy_distribution_contract = policy_distribution_contract(parameter_keys)
        if algorithm == "ppo" and self.checkpoint_manifest.get(
            "policy_distribution_contract_hash"
        ) != self.policy_distribution_contract["contract_hash"]:
            raise ValueError("RL checkpoint policy distribution contract hash is incompatible")
        try:
            import stable_baselines3 as sb3
        except ImportError as exc:  # pragma: no cover - optional dependency
            raise RuntimeError(
                "install ChemWorld with the 'rl' extra to evaluate PPO or SAC"
            ) from exc
        model_class = sb3.PPO if algorithm == "ppo" else sb3.SAC
        self._model = model_class.load(self.checkpoint)
        expected_action_shape = tuple(
            self.action_contract["training_adapter"]["shape"]
        )
        if tuple(self._model.action_space.shape or ()) != expected_action_shape:
            raise ValueError("RL checkpoint latent action shape is incompatible")
        self._prediction_count = 0
        self._last_trace: list[dict[str, Any]] = []

    def reset(self, task_info: dict[str, Any], seed: int) -> None:
        super().reset(task_info, seed)
        if task_info.get("task_id") != self.declared_task_id:
            raise ValueError("frozen RL checkpoint cannot evaluate a different task")
        try:
            from stable_baselines3.common.utils import set_random_seed
        except ImportError as exc:  # pragma: no cover - guarded in __init__
            raise RuntimeError("stable-baselines3 became unavailable") from exc
        resolved_seed = seed if self.policy_seed is None else int(self.policy_seed)
        set_random_seed(resolved_seed)
        self._model.set_random_seed(resolved_seed)
        self._prediction_count = 0
        self._last_trace = []

    def act(self, history: list[HistoryRecord]) -> dict[str, Any]:
        del history
        raise RuntimeError("FrozenSB3Agent requires the official public-view runner")

    def act_with_public_view(
        self,
        context: AgentDecisionContext,
        public_view: dict[str, Any],
    ) -> dict[str, Any]:
        observation, operation_mask = build_frozen_rl_observation(public_view, context)
        expected_shape = tuple(self._model.observation_space.shape or ())
        if observation.shape != expected_shape:
            raise ValueError(
                f"checkpoint observation shape {expected_shape} does not match public view "
                f"shape {observation.shape}"
            )
        action_vector, _ = self._model.predict(
            observation,
            deterministic=self.deterministic,
        )
        action = decode_conditional_hybrid_action(
            action_vector,
            event_action_space=self._event_action_space,
            operation_mask=operation_mask,
        )
        self._prediction_count += 1
        operation_index = int(action["operation"])
        self._last_trace = [
            {
                "trace_schema_version": "chemworld-frozen-rl-decision-0.2",
                "policy_mode": (
                    "deterministic" if self.deterministic else "stochastic_frozen_seed"
                ),
                "policy_seed": self.seed if self.policy_seed is None else self.policy_seed,
                "prediction_index": self._prediction_count,
                "selected_operation": OPERATION_TYPES[operation_index],
                "public_valid_operation_count": int(sum(operation_mask)),
                "checkpoint_sha256": self.checkpoint_sha256,
                "action_contract_hash": self.action_contract["contract_hash"],
            }
        ]
        return action

    def agent_trace(self) -> list[dict[str, Any]]:
        return [dict(item) for item in self._last_trace]

    def manifest(self) -> dict[str, Any]:
        payload = super().manifest()
        payload.update(
            {
                "algorithm": self.algorithm,
                "policy": "MlpPolicy",
                "policy_mode": (
                    "deterministic" if self.deterministic else "stochastic_frozen_seed"
                ),
                "checkpoint_filename": self.checkpoint.name,
                "checkpoint_sha256": self.checkpoint_sha256,
                "checkpoint_manifest_schema": self.checkpoint_manifest["schema_version"],
                "action_contract_hash": self.action_contract["contract_hash"],
                "training_reward_contract_hash": self.reward_contract["contract_hash"],
                "policy_distribution_contract_hash": self.policy_distribution_contract[
                    "contract_hash"
                ],
                "training_allocation": self.checkpoint_manifest.get("allocation", {}),
                "uses_training_reward_at_evaluation": False,
                "public_view_only": True,
            }
        )
        return payload

    def method_resource_usage(self) -> dict[str, Any]:
        manifest = self.checkpoint_manifest
        return {
            "schema_version": "chemworld-method-resource-usage-0.1",
            "accounting_complete": True,
            "usage_source": "verified_rl_checkpoint_manifest",
            "model_call_count": 0,
            "input_token_count": 0,
            "output_token_count": 0,
            "monetary_cost_usd": 0.0,
            "training_environment_step_count": int(
                manifest.get("training_environment_step_count", 0)
            ),
            "cpu_time_s": float(manifest.get("cpu_time_s", 0.0)),
            "gpu_time_s": float(manifest.get("gpu_time_s", 0.0)),
            "model_provenance": {
                "framework": "stable_baselines3",
                "algorithm": self.algorithm,
                "checkpoint_sha256": self.checkpoint_sha256,
                "versions": manifest.get("versions", {}),
            },
        }

    def interaction_capabilities(self) -> InteractionCapabilities:
        return InteractionCapabilities(
            decision_scope="operation",
            consumes_intermediate_observations=True,
            consumes_spectra=False,
            adapts_within_experiment=True,
            adapts_across_experiments=False,
            emits_structured_decision_audit=False,
        )


__all__ = ["FrozenSB3Agent", "RLAlgorithm", "build_frozen_rl_observation"]
