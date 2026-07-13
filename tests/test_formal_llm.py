from __future__ import annotations

import copy
import json
from pathlib import Path
from types import SimpleNamespace
from typing import Any

from chemworld.agents.interaction import AgentDecisionContext
from chemworld.eval.formal_llm import (
    audit_live_llm_method_freeze,
    build_formal_live_llm_registry,
    formal_live_llm_method_bindings,
    load_live_llm_method_freeze,
)
from chemworld.eval.formal_protocol_v0_4 import load_formal_protocol
from chemworld.eval.formal_runner import (
    FormalCellSpec,
    PrivateCellRuntime,
    canonical_sha256,
    file_sha256,
    issue_run_manifest,
    load_issued_cell,
    private_seed_commitment,
    private_world_commitment,
    run_formal_cell,
)
from chemworld.eval.method_protocol import METHOD_RESOURCE_LEDGER_VERSION
from chemworld.providers.deepseek import DeepSeekClient
from chemworld.tasks import get_task


def _runtime() -> PrivateCellRuntime:
    return PrivateCellRuntime(
        method_seed=91_001,
        world_seed=81_001,
        seed_nonce="private-method-seed",
        world_nonce="private-world-seed",
        world_interventions=(),
    )


def _spec(method_id: str = "live_llm_a", condition: str = "assigned") -> FormalCellSpec:
    runtime = _runtime()
    protocol = load_formal_protocol()
    run_id = "7" * 64
    pair_id = "llm-dev-pair-opaque"
    task_id = "flow-reaction-optimization"
    return FormalCellSpec(
        run_id=run_id,
        task_id=task_id,
        pair_id=pair_id,
        spectrum_condition=condition,  # type: ignore[arg-type]
        private_seed_commitment=private_seed_commitment(
            run_id=run_id,
            pair_id=pair_id,
            method_seed=runtime.method_seed,
            nonce=runtime.seed_nonce,
        ),
        world_commitment=private_world_commitment(
            run_id=run_id,
            task_id=task_id,
            pair_id=pair_id,
            world_seed=runtime.world_seed,
            nonce=runtime.world_nonce,
            interventions=runtime.world_interventions,
        ),
        protocol_sha256=canonical_sha256(protocol),
        backend_semantic_sha256="1" * 64,
        evaluator_sha256="2" * 64,
        interaction_protocol_sha256="3" * 64,
        statistics_protocol_sha256="4" * 64,
        reference_manifest_sha256="5" * 64,
        source_commit="6" * 40,
        complete_experiments=1,
        operation_limit=1,
        method=formal_live_llm_method_bindings()[method_id],
    )


class _Client:
    def __init__(self, model: str) -> None:
        self.model = model
        self.thinking = model == "deepseek-v4-pro"
        self.reasoning_effort = "max"
        self._pricing_client = DeepSeekClient(api_key="test-only", model=model)

    def complete_json(self, **kwargs: Any) -> Any:
        del kwargs
        usage = {
            "prompt_tokens": 100,
            "completion_tokens": 20,
            "total_tokens": 120,
            "prompt_cache_hit_tokens": 40,
            "prompt_cache_miss_tokens": 60,
        }
        return SimpleNamespace(
            payload={
                "action": {"operation": "terminate"},
                "evidence": ["No prior experiment outcome is available."],
                "spectrum_interpretation": "No spectrum is currently available.",
                "hypothesis": "Closing this smoke experiment tests the formal boundary.",
                "uncertainty": 0.9,
                "rationale": "Use one explicit operation without harness repair.",
            },
            model=self.model,
            attempts=1,
            usage=usage,
            request_id="provider-request-1",
            system_fingerprint="fp-test",
            finish_reason="stop",
            reasoning_content_present=self.thinking,
            reasoning_character_count=10 if self.thinking else 0,
            attempt_records=(
                {
                    "attempt_index": 1,
                    "status": "succeeded",
                    "request_id": "provider-request-1",
                    "model_id": self.model,
                    "usage": usage,
                    "usage_complete": True,
                    "billable": True,
                    "usage_source": "provider_response",
                },
            ),
        )

    def pricing_snapshot(self) -> dict[str, Any]:
        return self._pricing_client.pricing_snapshot()

    def estimate_cost_usd(self, usage: dict[str, Any]) -> float:
        return self._pricing_client.estimate_cost_usd(usage)


def _fake_run_agent(**kwargs: Any) -> None:
    assert kwargs["evaluation_policy"] == "task_contract"
    assert kwargs["safety_limit_override"] == 0.3
    limits = kwargs["method_resource_limits"]
    assert limits["model_call_limit"] == 3
    assert limits["input_token_limit"] == 1_000_000
    assert limits["output_token_limit"] == 200_000
    assert limits["monetary_cost_limit_usd"] == 2.0
    assert limits["wall_time_limit_s"] == 1800.0
    assert limits["training_environment_step_limit"] == 0
    agent = kwargs["agent"]
    task = get_task(kwargs["task_id"])
    agent.reset(task.to_dict(), kwargs["agent_seed"])
    context = AgentDecisionContext(
        step=1,
        task_id=task.task_id,
        decision_stage="experiment_setup",
        campaign_state={"remaining_budget": 1},
        visible_metrics={},
        latest_spectra={},
        uncertainty={},
        constraint_flags={},
        available_operations=("terminate",),
        previous_event_type=None,
    )
    action = agent.act_with_public_view(
        context,
        {"tool_json": {"available_actions": [{"operation": "terminate"}]}},
    )
    agent.update(action, {}, 0.0, {"experiment_ended": True, "observed_keys": []})
    usage = agent.method_resource_usage()
    record = {
        "step": 1,
        "action": action,
        "observation": {},
        "reward": 0.0,
        "info": {"experiment_ended": True},
        "method_resources": {
            "schema_version": METHOD_RESOURCE_LEDGER_VERSION,
            "operation_count": 1,
            "complete_experiment_count": 1,
            "decision_wall_time_s": 0.01,
            "update_wall_time_s": 0.01,
            "run_wall_time_s": 0.03,
            "reached_checkpoints": [1],
            "limits": {
                "operation_limit": 1,
                "complete_experiment_limit": 1,
                "checkpoint_complete_experiments": [1],
            },
            "agent_usage": usage,
            "accounting_complete": True,
        },
    }
    Path(kwargs["output_path"]).write_text(
        json.dumps(record, sort_keys=True) + "\n", encoding="utf-8"
    )


def _replay(spec, runtime, records, trajectory_path):
    del spec, runtime, records
    return (
        {
            "verified": True,
            "trajectory_sha256": file_sha256(trajectory_path),
            "verification": {"verified": True},
        },
        {"verified": True, "engine": "formal-llm-test-replay"},
    )


def test_live_llm_freeze_binds_two_models_prompt_and_three_conditions() -> None:
    freeze = load_live_llm_method_freeze()
    report = audit_live_llm_method_freeze(freeze)
    bindings = formal_live_llm_method_bindings(freeze)

    assert report["controls_ready"] is True
    assert set(bindings) == {"live_llm_a", "live_llm_b"}
    assert len({item.model_config_sha256 for item in bindings.values()}) == 2
    assert len({item.prompt_sha256 for item in bindings.values()}) == 1
    registry = build_formal_live_llm_registry(freeze)
    assert registry.registered_methods() == (
        ("live_llm_a", "live_llm"),
        ("live_llm_b", "live_llm"),
    )


def test_live_llm_freeze_fails_closed_on_model_role_tamper() -> None:
    freeze = copy.deepcopy(load_live_llm_method_freeze())
    freeze["methods"]["live_llm_b"]["model_id"] = "deepseek-v4-pro"

    report = audit_live_llm_method_freeze(freeze)

    assert report["controls_ready"] is False
    assert report["checks"]["two_frozen_roles"] is False


def test_formal_live_llm_adapter_reconciles_attempt_receipt_without_reasoning(
    tmp_path: Path,
) -> None:
    spec = _spec()
    manifest = issue_run_manifest([spec], metadata={"formal": False, "split": "dev"})
    issued = load_issued_cell(manifest, cell_identity_sha256=spec.cell_identity_sha256)
    registry = build_formal_live_llm_registry(
        client_factory=lambda card: _Client(str(card["model_id"])),
        run_agent_fn=_fake_run_agent,
        risk_limit_factory=lambda _: 0.3,
    )

    outcome = run_formal_cell(
        issued_cell=issued,
        runtime=_runtime(),
        adapter=registry.create(spec),
        output_root=tmp_path,
        replay_evaluator=_replay,
    )

    resources = json.loads((outcome.cell_dir / "resources.json").read_text(encoding="utf-8"))
    trajectory_text = (outcome.cell_dir / "trajectory.jsonl").read_text(encoding="utf-8")
    assert outcome.status == "succeeded"
    assert resources["accounting_complete"] is True
    assert resources["axes"]["provider_request_count"] == 1
    assert resources["axes"]["input_token_count"] == 100
    assert "private reasoning" not in trajectory_text.lower()
    assert "reasoning_content" not in trajectory_text
