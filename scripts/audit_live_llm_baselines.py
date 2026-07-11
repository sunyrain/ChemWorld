"""Audit live-LLM interaction and resource controls without making model claims."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from apps.task_lab.deepseek_client import DeepSeekClient  # noqa: E402

PROTOCOL = ROOT / "configs/benchmark/live_llm_vnext.json"
OUTPUT = ROOT / "workstreams/benchmark_v1/reports/live-llm-controls.json"


def build_report() -> dict[str, Any]:
    protocol = json.loads(PROTOCOL.read_text(encoding="utf-8"))
    roles = protocol["agent_roles"]
    clients = {
        role_id: DeepSeekClient(
            api_key="audit-only-not-sent",
            model=card["model_id"],
            thinking=bool(card["thinking"]),
            reasoning_effort=card["reasoning_effort"] or "high",
        )
        for role_id, card in roles.items()
    }
    pricing = {role_id: client.pricing_snapshot() for role_id, client in clients.items()}
    resource_examples = {
        role_id: {
            "usage": {
                "prompt_tokens": 1000,
                "prompt_cache_hit_tokens": 400,
                "prompt_cache_miss_tokens": 600,
                "completion_tokens": 200,
                "total_tokens": 1200,
            },
            "estimated_cost_usd": client.estimate_cost_usd(
                {
                    "prompt_tokens": 1000,
                    "prompt_cache_hit_tokens": 400,
                    "prompt_cache_miss_tokens": 600,
                    "completion_tokens": 200,
                }
            ),
        }
        for role_id, client in clients.items()
    }
    interaction = protocol["interaction_requirements"]
    resources = protocol["resource_requirements"]
    checks = {
        "schema": protocol.get("schema_version") == "chemworld-live-llm-protocol-0.1",
        "candidate_is_non_claiming": protocol.get("benchmark_claim_allowed") is False,
        "two_independent_model_ids": len({card["model_id"] for card in roles.values()}) == 2,
        "no_deprecated_model_alias": all(not item["legacy_alias"] for item in pricing.values()),
        "pricing_matches_frozen_protocol": all(
            item["input_cache_hit_per_million_usd"]
            == protocol["pricing_usd_per_million_tokens"][item["model_id"]]["input_cache_hit"]
            and item["input_cache_miss_per_million_usd"]
            == protocol["pricing_usd_per_million_tokens"][item["model_id"]]["input_cache_miss"]
            and item["output_per_million_usd"]
            == protocol["pricing_usd_per_million_tokens"][item["model_id"]]["output"]
            for item in pricing.values()
        ),
        "adaptive_spectra_and_memory_required": all(
            interaction[name]
            for name in (
                "one_live_call_per_model_decision",
                "reads_public_spectra",
                "adapts_within_experiment",
                "adapts_across_experiments",
            )
        ),
        "structured_public_audit_required": set(interaction["structured_decision_fields"])
        == {"evidence", "spectrum_interpretation", "hypothesis", "uncertainty", "rationale"},
        "private_reasoning_excluded": interaction["private_chain_of_thought_requested"] is False
        and interaction["private_reasoning_retained"] is False,
        "resource_accounting_complete_by_contract": all(resources.values()),
        "cost_examples_positive": all(
            card["estimated_cost_usd"] > 0.0 for card in resource_examples.values()
        ),
    }
    controls_ready = all(checks.values())
    return {
        "schema_version": "chemworld-live-llm-audit-0.1",
        "protocol_id": protocol["protocol_id"],
        "status": "controls_ready_formal_runs_missing" if controls_ready else "controls_failed",
        "controls_ready": controls_ready,
        "formal_run_matrix_complete": False,
        "benchmark_claim_allowed": False,
        "publication_ready": False,
        "checks": checks,
        "roles": roles,
        "pricing_snapshots": pricing,
        "resource_examples": resource_examples,
        "remaining_release_gates": protocol["formal_readiness_requirements"],
    }


def main() -> None:
    report = build_report()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    if not report["controls_ready"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
