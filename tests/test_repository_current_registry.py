from __future__ import annotations

import json
import tomllib
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "configs" / "current.json"


def _registry() -> dict[str, Any]:
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def _declared_paths(value: Any):
    if isinstance(value, dict):
        for key, item in value.items():
            if key in {
                "backend",
                "backend_report",
                "protocol",
                "interaction_strata",
                "statistical_analysis",
                "method_freeze_report",
                "preflight_report",
                "protocol_report",
                "classic_methods",
                "classic_report",
                "operation_methods",
                "operation_report",
                "live_llm_report",
            }:
                yield item
            else:
                yield from _declared_paths(item)
    elif isinstance(value, list):
        for item in value:
            yield from _declared_paths(item)


def test_current_registry_paths_exist() -> None:
    registry = _registry()
    declared = list(_declared_paths(registry))

    assert declared
    assert all(isinstance(path, str) for path in declared)
    missing = [path for path in declared if not (ROOT / path).is_file()]
    assert missing == []


def test_current_registry_matches_package_and_claim_boundaries() -> None:
    registry = _registry()
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))

    assert registry["project"]["version"] == pyproject["project"]["version"]
    assert registry["project"]["role"] == "agent_capability_evaluation_and_training_environment"
    assert registry["project"]["environment_updates_agent_weights"] is False
    assert registry["formal_evaluation"]["formal_results_present"] is False
    assert registry["formal_evaluation"]["benchmark_claim_allowed"] is False
    assert registry["mechanism_adaptation"]["publication_ready"] is False


def test_current_mechanism_agent_and_legacy_agent_remain_replayable() -> None:
    from chemworld.agents import MechanismDiagnosticLiveLLMAgent
    from chemworld.agents.mechanism_adaptation_live_llm import (
        MechanismAdaptationLiveLLMAgent,
        MechanismCandidateSpec,
    )

    assert MechanismAdaptationLiveLLMAgent.__name__ == "MechanismAdaptationLiveLLMAgent"
    assert MechanismCandidateSpec.__name__ == "MechanismCandidateSpec"
    assert MechanismDiagnosticLiveLLMAgent.__name__ == "MechanismDiagnosticLiveLLMAgent"
