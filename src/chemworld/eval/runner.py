"""Official runner for benchmark agents."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import Any

import gymnasium as gym

import chemworld  # noqa: F401
from chemworld.agent_interface import agent_view_bundle
from chemworld.agents import (
    CodexSubagentOnlineAgent,
    CodexSubagentReplayAgent,
    GaussianProcessBOAgent,
    GaussianProcessPIAgent,
    GaussianProcessUCBAgent,
    GreedyLocalAgent,
    LatinHypercubeAgent,
    LLMReplayAgent,
    RandomAgent,
    RandomForestEIAgent,
    RandomRecipeAgent,
    SafetyConstrainedBOAgent,
    ScriptedChemistryAgent,
    ToolUsingLLMStubAgent,
)
from chemworld.agents.base import Agent, HistoryRecord
from chemworld.data.logging import TrajectoryLogger, observation_to_json
from chemworld.data.submission import git_commit

AGENT_REGISTRY: dict[str, Callable[[], Agent]] = {
    "random": RandomAgent,
    "lhs": LatinHypercubeAgent,
    "latin_hypercube": LatinHypercubeAgent,
    "greedy": GreedyLocalAgent,
    "greedy_local": GreedyLocalAgent,
    "gp_bo": GaussianProcessBOAgent,
    "gp_pi": GaussianProcessPIAgent,
    "gp_ucb": GaussianProcessUCBAgent,
    "rf_ei": RandomForestEIAgent,
    "safe_gp_bo": SafetyConstrainedBOAgent,
    "random_recipe": RandomRecipeAgent,
    "scripted_chemistry": ScriptedChemistryAgent,
    "scripted_reaction_to_purification": ScriptedChemistryAgent,
    "partition_discovery_heuristic": ScriptedChemistryAgent,
    "heuristic": ScriptedChemistryAgent,
    "tool_using_llm_stub": ToolUsingLLMStubAgent,
    "llm_replay": LLMReplayAgent,
    "codex_subagent_replay": CodexSubagentReplayAgent,
    "codex_subagent_online": CodexSubagentOnlineAgent,
}


def make_agent(name: str) -> Agent:
    if name not in AGENT_REGISTRY:
        allowed = ", ".join(sorted(AGENT_REGISTRY))
        raise ValueError(f"Unknown agent={name!r}. Allowed: {allowed}")
    return AGENT_REGISTRY[name]()


def run_agent(
    *,
    env_id: str,
    agent: Agent,
    world_split: str,
    budget: int,
    objective: str,
    seed: int,
    task_id: str | None = None,
    output_path: str | Path | None = None,
    budget_override: int | None = None,
    episode_mode_override: str | None = None,
    step_callback: Callable[[HistoryRecord, list[dict[str, Any]]], None] | None = None,
) -> list[HistoryRecord]:
    """Run one benchmark episode and optionally write a JSONL trajectory."""

    env_kwargs: dict[str, Any] = {
        "world_split": world_split,
        "budget": budget,
        "objective": objective,
        "seed": seed,
    }
    if task_id is not None:
        env_kwargs["task_id"] = task_id
    if budget_override is not None:
        env_kwargs["budget_override"] = budget_override
    if episode_mode_override is not None:
        env_kwargs["episode_mode_override"] = episode_mode_override
    env = gym.make(
        env_id,
        **env_kwargs,
    )
    initial_obs, task_info = env.reset(seed=seed)
    del initial_obs
    if not hasattr(env.unwrapped, "task_info"):
        raise RuntimeError(f"{env_id} does not expose task_info()")
    task_info = env.unwrapped.task_info()

    agent.reset(task_info, seed)
    agent_metadata = agent.manifest()
    agent_metadata["git_commit"] = git_commit()

    history: list[HistoryRecord] = []
    logger_context = TrajectoryLogger(output_path) if output_path is not None else None
    try:
        logger = logger_context.__enter__() if logger_context is not None else None
        for step in range(1, budget + 1):
            action = agent.act(history)
            observation, reward, terminated, truncated, info = env.step(action)
            obs_json = observation_to_json(observation)
            agent.update(action, obs_json, float(reward), info)
            record = HistoryRecord(
                step=step,
                action=dict(action),
                observation=obs_json,
                reward=float(reward),
                info=info,
            )
            history.append(record)
            agent_trace_factory = getattr(agent, "agent_trace", None)
            agent_trace = agent_trace_factory() if callable(agent_trace_factory) else []
            if logger is not None:
                logger.log(
                    task_info=task_info,
                    step=step,
                    action=action,
                    observation=obs_json,
                    reward=float(reward),
                    terminated=terminated,
                    truncated=truncated,
                    info=info,
                    agent_metadata=agent_metadata,
                    agent_view=agent_view_bundle(env, observation, info),
                    agent_trace=agent_trace,
                )
            if step_callback is not None:
                step_callback(record, agent_trace)
            if terminated or truncated:
                break
    finally:
        if logger_context is not None:
            logger_context.__exit__(None, None, None)
        env.close()
    return history
