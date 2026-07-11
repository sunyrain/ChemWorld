"""Evidence-backed task-validity cards and provisional suite recommendation."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from chemworld.physchem.mechanism_library import configuration_root
from chemworld.tasks import SERIOUS_TASK_IDS

TASK_VALIDITY_PROTOCOL_VERSION = "chemworld-task-validity-protocol-0.1"
TASK_VALIDITY_AUDIT_VERSION = "chemworld-task-validity-audit-0.1"
ROOT = Path(__file__).resolve().parents[3]
DEFAULT_TASK_VALIDITY_PROTOCOL_PATH = (
    configuration_root() / "benchmark" / "task_validity_vnext.json"
)
DEFAULT_FORMAL_SUMMARY_PATH = (
    ROOT / "workstreams" / "benchmark_v1" / "reports" / "publication-classic20-full-summary.json"
)
DEFAULT_RESPONSE_SURFACE_PATH = (
    ROOT / "benchmark" / "releases" / "chemworld-serious-v1" / "response_surface_audit.json"
)
DEFAULT_RISK_COST_REPORT_PATH = (
    ROOT / "workstreams" / "benchmark_v1" / "reports" / "risk-cost-signal-controls.json"
)


def load_task_validity_protocol(
    path: str | Path = DEFAULT_TASK_VALIDITY_PROTOCOL_PATH,
) -> dict[str, Any]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("task-validity protocol must be a JSON object")
    return payload


def audit_task_validity(
    protocol: dict[str, Any],
    *,
    formal_summary_path: str | Path = DEFAULT_FORMAL_SUMMARY_PATH,
    response_surface_path: str | Path = DEFAULT_RESPONSE_SURFACE_PATH,
    risk_cost_report_path: str | Path = DEFAULT_RISK_COST_REPORT_PATH,
) -> dict[str, Any]:
    formal_path = Path(formal_summary_path)
    surface_path = Path(response_surface_path)
    risk_path = Path(risk_cost_report_path)
    formal = _load_object(formal_path)
    surfaces = _load_object(surface_path)
    risk = _load_object(risk_path)
    comparator = str(protocol.get("primary_comparator", ""))
    alpha = float(protocol.get("direction_alpha", 0.05))
    absolute_sesoi = float(protocol.get("comparator_absolute_sesoi", 0.05))
    normalized_sesoi = float(protocol.get("minimum_surface_normalized_effect", 0.05))
    minimum_spread = float(protocol.get("minimum_primary_surface_spread", 0.05))

    cards: dict[str, Any] = {}
    for task_id in SERIOUS_TASK_IDS:
        formal_task = formal["tasks"][task_id]
        surface_task = surfaces["tasks"][task_id]
        risk_task = risk["tasks"][task_id]
        comparison = formal_task["primary_metric_comparisons"][comparator]
        effect = float(comparison["mean_paired_effect"])
        ci_low, ci_high = (float(item) for item in comparison["paired_bootstrap_ci"])
        adjusted_p = float(comparison["holm_adjusted_p_value"])
        spread = float(surface_task["primary_metric_distribution"]["spread"])
        normalized_effect = effect / spread if spread > 0.0 else 0.0
        direction_supported = effect > 0.0 and ci_low > 0.0 and adjusted_p < alpha
        absolute_sesoi_reached = effect >= absolute_sesoi
        normalized_sesoi_reached = normalized_effect >= normalized_sesoi
        surface_sensitive = spread >= minimum_spread
        if direction_supported and absolute_sesoi_reached:
            role = "core_confirmed"
        elif direction_supported and normalized_sesoi_reached:
            role = "core_candidate"
        else:
            role = "exploratory"
        cards[task_id] = {
            "task_id": task_id,
            "declared_primary_metric": surface_task["primary_metric"],
            "formal_primary_result_field": formal_task["primary_result_field"],
            "response_surface": {
                "minimum": surface_task["primary_metric_distribution"]["minimum"],
                "maximum": surface_task["primary_metric_distribution"]["maximum"],
                "spread": spread,
                "standard_deviation": surface_task["primary_metric_distribution"]["std"],
                "sensitive": surface_sensitive,
            },
            "minimum_adaptive_strategy_test": {
                "comparison": comparator,
                "mean_paired_effect": effect,
                "paired_bootstrap_ci": [ci_low, ci_high],
                "holm_adjusted_p_value": adjusted_p,
                "direction_supported": direction_supported,
                "comparator_absolute_sesoi": absolute_sesoi,
                "comparator_absolute_sesoi_reached": absolute_sesoi_reached,
                "surface_normalized_effect": normalized_effect,
                "minimum_surface_normalized_effect": normalized_sesoi,
                "surface_normalized_effect_reached": normalized_sesoi_reached,
            },
            "risk_context": {
                "operational_risk_tradeoff_task": risk_task["risk_tradeoff_task"],
                "score_risk_spearman": risk_task["holdout_score_risk_spearman"],
                "risk_limit_semantics": risk_task["policy"]["risk_semantics"],
            },
            "release_role": role,
            "capability_validated_under_legacy_sesoi": bool(
                formal_task["claim_gate"]["task_capability_validated"]
            ),
            "failure_cases": _failure_cases(
                task_id=task_id,
                role=role,
                direction_supported=direction_supported,
                absolute_sesoi_reached=absolute_sesoi_reached,
                risk_tradeoff=bool(risk_task["risk_tradeoff_task"]),
            ),
        }

    core_confirmed = [
        task_id for task_id, card in cards.items() if card["release_role"] == "core_confirmed"
    ]
    core_candidates = [
        task_id for task_id, card in cards.items() if card["release_role"] == "core_candidate"
    ]
    exploratory = [
        task_id for task_id, card in cards.items() if card["release_role"] == "exploratory"
    ]
    recommended_core = [
        task_id for task_id in SERIOUS_TASK_IDS if task_id in {*core_confirmed, *core_candidates}
    ]
    checks = {
        "schema": protocol.get("schema_version") == TASK_VALIDITY_PROTOCOL_VERSION,
        "candidate_is_non_claiming": protocol.get("benchmark_claim_allowed") is False,
        "formal_matrix_complete": bool(formal.get("gates", {}).get("formal_matrix_complete")),
        "formal_result_count": formal.get("matrix", {}).get("result_count") == 600,
        "task_scope": tuple(formal.get("matrix", {}).get("tasks", ())) == tuple(SERIOUS_TASK_IDS),
        "response_surface_scope": tuple(surfaces.get("task_ids", ())) == tuple(SERIOUS_TASK_IDS),
        "response_surfaces_pass": surfaces.get("passed") is True,
        "risk_cost_controls_ready": risk.get("controls_ready") is True,
        "primary_fields_align": all(
            card["formal_primary_result_field"] == f"mean_{card['declared_primary_metric']}"
            for card in cards.values()
        ),
        "all_primary_surfaces_sensitive": all(
            card["response_surface"]["sensitive"] for card in cards.values()
        ),
        "recommendation_is_core4": len(recommended_core) == 4,
        "exploratory_scope_is_electrochemistry_and_equilibrium": exploratory
        == ["electrochemical-conversion", "equilibrium-characterization"],
    }
    controls_ready = all(checks.values())
    return {
        "schema_version": TASK_VALIDITY_AUDIT_VERSION,
        "protocol_id": protocol.get("protocol_id"),
        "status": (
            "provisional_core4_confirmatory_rerun_required" if controls_ready else "controls_failed"
        ),
        "controls_ready": controls_ready,
        "benchmark_claim_allowed": False,
        "publication_ready": False,
        "suite_recommendation": {
            "decision": "provisional_core4",
            "core_confirmed": core_confirmed,
            "core_candidates": core_candidates,
            "recommended_core_tasks": recommended_core,
            "exploratory_tasks": exploratory,
            "core4_claim_ready": False,
            "reason": (
                "Four tasks support a positive declared-primary direction. Under the "
                "task-validity protocol's GP-vs-random comparator, three also pass the "
                "absolute SESOI and flow passes only the scale-normalized threshold. "
                "Freeze task-specific SESOI and repeat the vNext confirmatory run "
                "before release; this does not overwrite the older publication "
                "gate's 2/6 result."
            ),
        },
        "checks": checks,
        "task_cards": cards,
        "evidence": {
            "formal_summary_sha256": _sha256(formal_path),
            "response_surface_sha256": _sha256(surface_path),
            "risk_cost_report_sha256": _sha256(risk_path),
        },
        "limitations": [
            "The suite recommendation is retrospective and must be frozen before confirmation.",
            "A response surface proves task sensitivity, not that the declared agent "
            "capability is measured.",
            "Electrochemical and equilibrium total-score gains do not validate their "
            "declared primary metrics.",
            "Operational-risk budgets are benchmark controls, not real-world safety thresholds.",
        ],
        "remaining_release_gates": list(protocol.get("remaining_release_gates", ())),
    }


def _failure_cases(
    *,
    task_id: str,
    role: str,
    direction_supported: bool,
    absolute_sesoi_reached: bool,
    risk_tradeoff: bool,
) -> list[str]:
    cases: list[str] = []
    if not direction_supported:
        cases.append(
            "Adaptive optimization improves aggregate score but not the declared primary metric."
        )
        cases.append("Current objective/capability alignment is insufficient for a core claim.")
    elif not absolute_sesoi_reached:
        cases.append(
            "Primary direction is supported, but the universal absolute SESOI is not reached."
        )
        cases.append("Task-specific SESOI must be frozen before confirmatory evaluation.")
    if risk_tradeoff:
        cases.append("Performance and operational risk rise together on the holdout slice.")
    if role == "core_confirmed":
        cases.append("Confirmation still requires the frozen vNext world and evaluation policies.")
    if task_id == "equilibrium-characterization":
        cases.append("Confidence is largely solver-derived and may not measure information gain.")
    return cases


def _load_object(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"evidence must be a JSON object: {path}")
    return payload


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


__all__ = [
    "DEFAULT_FORMAL_SUMMARY_PATH",
    "DEFAULT_RESPONSE_SURFACE_PATH",
    "DEFAULT_RISK_COST_REPORT_PATH",
    "DEFAULT_TASK_VALIDITY_PROTOCOL_PATH",
    "TASK_VALIDITY_AUDIT_VERSION",
    "TASK_VALIDITY_PROTOCOL_VERSION",
    "audit_task_validity",
    "load_task_validity_protocol",
]
