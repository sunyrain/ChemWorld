"""Machine audit for the vNext operation-level agent interaction contract."""

from __future__ import annotations

import json
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

from chemworld.agents.base import BaseAgent
from chemworld.agents.interaction import (
    INTERACTION_CONTRACT_VERSION,
    AgentDecisionContext,
    InteractionCapabilities,
)
from chemworld.agents.random import RandomAgent
from chemworld.data.logging import load_jsonl
from chemworld.eval.runner import run_agent
from chemworld.physchem.mechanism_library import configuration_root
from chemworld.tasks import get_task

INTERACTION_AUDIT_VERSION = "chemworld-agent-interaction-control-audit-0.1"
INTERACTION_PROTOCOL_VERSION = "chemworld-agent-interaction-protocol-0.1"
DEFAULT_INTERACTION_PROTOCOL_PATH = (
    configuration_root() / "benchmark" / "agent_interaction_vnext.json"
)


class _SpectralContextProbeAgent(BaseAgent):
    name = "spectral_context_probe"

    def reset(self, task_info: dict[str, Any], seed: int) -> None:
        super().reset(task_info, seed)
        self._stage = 0
        self._last_audit: dict[str, Any] | None = None
        self.spectrum_used = False

    def interaction_capabilities(self) -> InteractionCapabilities:
        return InteractionCapabilities(
            decision_scope="operation",
            consumes_intermediate_observations=True,
            consumes_spectra=True,
            adapts_within_experiment=True,
            adapts_across_experiments=False,
            emits_structured_decision_audit=True,
        )

    def act(self, history: list[Any]) -> dict[str, Any]:
        del history
        raise AssertionError("runner must prefer act_with_context")

    def act_with_context(self, context: AgentDecisionContext) -> dict[str, Any]:
        sequence: list[dict[str, Any]] = [
            {"operation": "add_solvent", "volume_L": 0.028, "solvent": 2},
            {"operation": "add_reagent", "amount_mol": 0.010},
            {
                "operation": "add_catalyst",
                "catalyst_amount_mol": 0.00025,
                "catalyst": 1,
            },
            {
                "operation": "heat",
                "target_temperature_K": 378.0,
                "duration_s": 1200.0,
                "stirring_speed_rpm": 720.0,
            },
            {"operation": "measure", "instrument": "hplc"},
        ]
        action: dict[str, Any]
        evidence: tuple[str, ...]
        if self._stage < len(sequence):
            action = sequence[self._stage]
            source = "none"
            evidence = (f"public_stage={context.decision_stage}",)
        elif self._stage == len(sequence):
            self.spectrum_used = bool(context.latest_spectra.get("has_spectral_packet"))
            action = {"operation": "quench"}
            source = "spectrum"
            dominant = context.latest_spectra.get("dominant_peak", {})
            evidence = (
                "public_hplc_packet_available",
                f"dominant_group={dominant.get('group')}",
            )
        elif self._stage == len(sequence) + 1:
            action = {"operation": "terminate"}
            source = "measurement"
            evidence = ("reaction_quenched_after_public_measurement",)
        else:
            action = {"operation": "measure", "instrument": "final_assay"}
            source = "measurement"
            evidence = ("terminated_state_is_publicly_assay_eligible",)
        self._stage += 1
        self._last_audit = {
            "action": action,
            "evidence": list(evidence),
            "hypothesis": "The selected operation should preserve an auditable experiment.",
            "uncertainty": 0.35 if source == "spectrum" else 0.5,
            "rationale": "Choose one valid operation from the current public evidence.",
            "adaptation_source": source,
        }
        return action

    def decision_audit(self) -> dict[str, Any] | None:
        return self._last_audit


def load_interaction_protocol(
    path: str | Path = DEFAULT_INTERACTION_PROTOCOL_PATH,
) -> dict[str, Any]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("agent-interaction protocol must be a JSON object")
    return payload


def audit_agent_interaction_contract(protocol: dict[str, Any]) -> dict[str, Any]:
    task = get_task("reaction-to-assay")
    probe = _SpectralContextProbeAgent()
    with TemporaryDirectory(prefix="chemworld-interaction-audit-") as temp_dir:
        trajectory_path = Path(temp_dir) / "probe.jsonl"
        history = run_agent(
            env_id=task.env_id,
            agent=probe,
            world_split=task.world_split,
            budget=task.budget,
            objective=task.objective,
            seed=0,
            task_id=task.task_id,
            output_path=trajectory_path,
        )
        retained_records = load_jsonl(trajectory_path)
    recipe_capabilities = RandomAgent().interaction_capabilities().to_dict()
    required_context = set(protocol.get("required_public_context", ()))
    required_audit = set(protocol.get("required_decision_audit", ()))
    context_keys = set(history[-1].decision_context) if history else set()
    audit_keys = set(history[-1].decision_audit) if history else set()
    checks = {
        "schema": protocol.get("schema_version") == INTERACTION_PROTOCOL_VERSION,
        "contract_version": protocol.get("interaction_contract_version")
        == INTERACTION_CONTRACT_VERSION,
        "candidate_is_non_claiming": protocol.get("benchmark_claim_allowed") is False,
        "three_level_hierarchy_declared": protocol.get("decision_hierarchy")
        == ["campaign", "experiment", "operation"],
        "required_public_context_present": required_context <= context_keys,
        "required_decision_audit_present": required_audit <= audit_keys,
        "operation_context_used": len(history) == 8
        and all(record.decision_context for record in history),
        "spectra_reaches_next_decision": probe.spectrum_used
        and any(
            record.decision_context.get("latest_spectra", {}).get("has_spectral_packet")
            for record in history
        ),
        "raw_spectrum_reaches_next_decision": any(
            bool(record.decision_context.get("latest_spectra", {}).get("raw_signal"))
            for record in history
        ),
        "experiment_boundary_surfaced": history[-1].event_type == "experiment_end",
        "structured_audit_retained": all(
            record.decision_audit.get("status") == "provided" for record in history
        ),
        "trajectory_retains_context_and_audit": len(retained_records) == len(history)
        and all(
            record.get("explanation", {}).get("interaction_contract_version")
            == INTERACTION_CONTRACT_VERSION
            and record.get("explanation", {}).get("decision_context")
            and record.get("explanation", {}).get("decision_audit", {}).get("status") == "provided"
            for record in retained_records
        ),
        "nonadaptive_recipe_agents_declare_limits": (
            recipe_capabilities["decision_scope"] == "experiment_recipe"
            and recipe_capabilities["consumes_spectra"] is False
            and recipe_capabilities["adapts_within_experiment"] is False
            and recipe_capabilities["adapts_across_experiments"] is False
        ),
        "private_chain_of_thought_not_requested": protocol.get("evidence_policy", {}).get(
            "private_chain_of_thought_requested"
        )
        is False,
    }
    controls_ready = all(checks.values())
    return {
        "schema_version": INTERACTION_AUDIT_VERSION,
        "protocol_id": protocol.get("protocol_id"),
        "status": "controls_ready_experiments_pending" if controls_ready else "controls_failed",
        "controls_ready": controls_ready,
        "benchmark_claim_allowed": False,
        "publication_ready": False,
        "checks": checks,
        "probe": {
            "task_id": task.task_id,
            "operation_count": len(history),
            "event_types": [record.event_type for record in history],
            "adaptation_sources": [
                record.decision_audit.get("adaptation_source") for record in history
            ],
            "final_leaderboard_score": history[-1].info.get("leaderboard_score"),
        },
        "recipe_agent_capabilities": recipe_capabilities,
        "remaining_release_gates": list(protocol.get("remaining_release_gates", ())),
        "limitations": [
            "The probe verifies information flow, not method quality.",
            "No retained real-LLM or reinforcement-learning comparison is attached.",
            "Model-call, token, wall-time, and monetary budgets remain outside this contract.",
        ],
    }


__all__ = [
    "DEFAULT_INTERACTION_PROTOCOL_PATH",
    "INTERACTION_AUDIT_VERSION",
    "audit_agent_interaction_contract",
    "load_interaction_protocol",
]
