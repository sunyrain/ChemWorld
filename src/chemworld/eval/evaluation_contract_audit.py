"""Control audit for layered vNext evaluation and current identifiability blockers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from chemworld.eval.layered_evaluation import (
    LAYERED_EVALUATION_VERSION,
    TaskEvaluationContract,
)
from chemworld.eval.risk_cost_signal_audit import RiskCostTaskPolicy
from chemworld.physchem.mechanism_library import configuration_root
from chemworld.task_design import SERIOUS_TASK_DESIGNS
from chemworld.tasks import SERIOUS_TASK_IDS

EVALUATION_AUDIT_VERSION = "chemworld-evaluation-identifiability-audit-0.2"
EVALUATION_PROTOCOL_VERSION = "chemworld-evaluation-protocol-0.2"
DEFAULT_EVALUATION_PROTOCOL_PATH = configuration_root() / "benchmark" / "evaluation_vnext.json"
DEFAULT_PUBLICATION_SUMMARY_PATH = (
    Path(__file__).resolve().parents[3]
    / "workstreams"
    / "benchmark_v1"
    / "reports"
    / "publication-classic20-full-summary.json"
)
DEFAULT_RISK_COST_REPORT_PATH = (
    Path(__file__).resolve().parents[3]
    / "workstreams"
    / "benchmark_v1"
    / "reports"
    / "risk-cost-signal-controls.json"
)


def load_evaluation_protocol(
    path: str | Path = DEFAULT_EVALUATION_PROTOCOL_PATH,
) -> dict[str, Any]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("evaluation protocol must be a JSON object")
    return payload


def audit_evaluation_identifiability(
    protocol: dict[str, Any],
    *,
    publication_summary_path: str | Path = DEFAULT_PUBLICATION_SUMMARY_PATH,
    risk_cost_report_path: str | Path = DEFAULT_RISK_COST_REPORT_PATH,
) -> dict[str, Any]:
    risk_cost_report = json.loads(Path(risk_cost_report_path).read_text(encoding="utf-8"))
    risk_cost_controls_ready = bool(risk_cost_report.get("controls_ready", False))
    formal_methods_rerun = bool(risk_cost_report.get("formal_method_comparison_ready", False))
    risk_protocol = json.loads(
        (configuration_root() / "benchmark" / "risk_cost_vnext.json").read_text(encoding="utf-8")
    )
    contracts = {
        task_id: TaskEvaluationContract.for_task(
            task_id,
            risk_limit=RiskCostTaskPolicy.from_protocol(
                task_id,
                risk_protocol,
            ).risk_limit,
        )
        for task_id in SERIOUS_TASK_IDS
    }
    configured_tasks = protocol.get("tasks", {})
    formal_summary = json.loads(Path(publication_summary_path).read_text(encoding="utf-8"))
    formal_gates = formal_summary.get("gates", {})
    safety_constraint_active = bool(formal_gates.get("safety_constraint_active", False))
    checks = {
        "schema": protocol.get("schema_version") == EVALUATION_PROTOCOL_VERSION,
        "contract_version": protocol.get("evaluation_contract_version")
        == LAYERED_EVALUATION_VERSION,
        "candidate_is_non_claiming": protocol.get("benchmark_claim_allowed") is False,
        "task_scope": tuple(configured_tasks) == tuple(SERIOUS_TASK_IDS),
        "primary_metrics_match_task_design": all(
            configured_tasks.get(task_id) == SERIOUS_TASK_DESIGNS[task_id].primary_metric
            for task_id in SERIOUS_TASK_IDS
        ),
        "layers_are_disjoint": protocol.get("layers")
        == [
            "objective",
            "task_primary",
            "online_shaping",
            "constraints",
            "resources",
            "validity",
        ],
        "online_reward_excluded_from_primary": protocol.get("policies", {}).get(
            "online_reward_is_primary"
        )
        is False,
        "missing_primary_fails_closed": protocol.get("policies", {}).get("missing_primary")
        == "fail",
        "risk_cost_controls_ready": risk_cost_controls_ready,
        "formal_safety_constraint_active": safety_constraint_active,
        "formal_methods_rerun_with_vnext_policy": formal_methods_rerun,
    }
    controls_ready = all(
        checks[key]
        for key in checks
        if key
        not in {
            "formal_safety_constraint_active",
            "formal_methods_rerun_with_vnext_policy",
        }
    )
    evaluation_identifiable = controls_ready and formal_methods_rerun
    return {
        "schema_version": EVALUATION_AUDIT_VERSION,
        "protocol_id": protocol.get("protocol_id"),
        "status": (
            "controls_ready_method_rerun_blocked"
            if controls_ready and not evaluation_identifiable
            else "identifiable"
            if evaluation_identifiable
            else "controls_failed"
        ),
        "controls_ready": controls_ready,
        "evaluation_identifiable": evaluation_identifiable,
        "benchmark_claim_allowed": False,
        "publication_ready": False,
        "checks": checks,
        "contracts": {task_id: contract.to_dict() for task_id, contract in contracts.items()},
        "known_blockers": (
            []
            if formal_methods_rerun
            else [
                "The vNext operational-risk and process-cost controls are calibrated, "
                "but retained methods received the legacy 0.65 limit. Safe-method "
                "effects remain unidentified until every method is rerun."
            ]
        ),
        "remaining_release_gates": list(protocol.get("remaining_release_gates", ())),
    }


__all__ = [
    "DEFAULT_EVALUATION_PROTOCOL_PATH",
    "DEFAULT_RISK_COST_REPORT_PATH",
    "EVALUATION_AUDIT_VERSION",
    "audit_evaluation_identifiability",
    "load_evaluation_protocol",
]
