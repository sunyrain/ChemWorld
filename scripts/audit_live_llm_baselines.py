"""Audit live-LLM interaction and resource controls without making model claims."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from chemworld.agents.live_llm import LiveLLMAgent  # noqa: E402
from chemworld.eval.formal_llm import (  # noqa: E402
    audit_live_llm_method_freeze,
    formal_live_llm_method_bindings,
)
from chemworld.providers.deepseek import DeepSeekClient  # noqa: E402

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
    adapter_manifests = {
        role_id: LiveLLMAgent(client, role_id=role_id).manifest()
        for role_id, client in clients.items()
    }
    formal_freeze_audit = audit_live_llm_method_freeze()
    formal_bindings = formal_live_llm_method_bindings()
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
        "schema": protocol.get("schema_version") == "chemworld-live-llm-protocol-0.4",
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
                "reads_current_public_spectra",
                "adapts_within_experiment",
                "adapts_across_experiments",
            )
        ),
        "structured_public_audit_required": set(interaction["structured_decision_fields"])
        == {"evidence", "spectrum_interpretation", "hypothesis", "uncertainty", "rationale"},
        "private_reasoning_excluded": interaction["private_chain_of_thought_requested"] is False
        and interaction["private_reasoning_retained"] is False,
        "resource_accounting_complete_by_contract": all(resources.values()),
        "official_adapter_is_operation_level": all(
            manifest["interaction_capabilities"]["decision_scope"] == "operation"
            and manifest["interaction_capabilities"]["consumes_intermediate_observations"]
            and manifest["interaction_capabilities"]["adapts_within_experiment"]
            and manifest["interaction_capabilities"]["adapts_across_experiments"]
            and manifest["interaction_capabilities"]["emits_structured_decision_audit"]
            for manifest in adapter_manifests.values()
        ),
        "official_adapter_forbids_harness_assistance": (
            protocol["official_adapter_contract"]["automatic_action_repair"] is False
            and protocol["official_adapter_contract"]["automatic_terminate_or_final_assay"]
            is False
            and protocol["official_adapter_contract"]["provider_or_output_failure_policy"]
            == "retain_as_invalid_model_failure_operation"
            and protocol["official_adapter_contract"]["task_lab_is_formal_launcher"]
            is False
        ),
        "paired_spectral_ablation_is_frozen": (
            protocol["spectral_ablation"]["required"] is True
            and protocol["spectral_ablation"]["paired_on_task_world_and_model_seed"] is True
            and set(protocol["spectral_ablation"]["conditions"])
            == {"assigned", "unassigned", "masked"}
            and protocol["spectral_ablation"][
                "non_spectral_public_observations_held_constant"
            ]
            is True
        ),
        "spectral_ablation_preserves_non_spectral_evidence": (
            all(
                condition["non_spectral_public_fields"] is True
                for condition in protocol["spectral_ablation"]["conditions"].values()
            )
            and protocol["spectral_ablation"]["conditions"]["unassigned"][
                "public_spectral_raw_signal"
            ]
            is True
            and protocol["spectral_ablation"]["conditions"]["unassigned"][
                "public_assignments"
            ]
            is False
        ),
        "historical_spectra_are_request_only": interaction["historical_spectrum_access"]
        == "catalog_metadata_then_one_packet_after_explicit_id_request_on_next_decision",
        "formal_freeze_ready": formal_freeze_audit["controls_ready"] is True,
        "formal_bindings_complete": set(formal_bindings) == set(roles)
        and all(binding.prompt_sha256 for binding in formal_bindings.values())
        and all(binding.model_config_sha256 for binding in formal_bindings.values()),
        "provider_capabilities_verified": protocol["provider_verification"][
            "json_probe_succeeded"
        ]
        is True
        and protocol["provider_verification"]["thinking_probe_succeeded"] is True
        and protocol["provider_verification"]["returned_model_identity_matched"] is True
        and protocol["provider_verification"]["reasoning_content_retained"] is False,
        "cost_examples_positive": all(
            card["estimated_cost_usd"] > 0.0 for card in resource_examples.values()
        ),
    }
    controls_ready = all(checks.values())
    return {
        "schema_version": "chemworld-live-llm-audit-0.4",
        "protocol_id": protocol["protocol_id"],
        "status": "controls_ready_formal_runs_missing" if controls_ready else "controls_failed",
        "controls_ready": controls_ready,
        "formal_run_matrix_complete": False,
        "benchmark_claim_allowed": False,
        "publication_ready": False,
        "checks": checks,
        "roles": roles,
        "official_adapter_manifests": adapter_manifests,
        "formal_method_bindings": {
            method_id: binding.__dict__ for method_id, binding in formal_bindings.items()
        },
        "formal_freeze_audit": formal_freeze_audit,
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
