from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from chemworld.agents.rl import FrozenSB3Agent
from chemworld.eval.formal_rl import (
    FORMAL_RL_CHECKPOINT_INDEX_VERSION,
    FormalRLAdapter,
    FormalRLAdapterFactory,
    FormalRLContractError,
    RLCheckpointBinding,
    audit_formal_rl_contract,
    file_sha256,
    load_checkpoint_index,
    load_formal_rl_config,
    task_contract_bundle,
)
from chemworld.eval.formal_runner import (
    FormalAdapterRegistry,
    FormalCellSpec,
    FormalMethodBinding,
    PrivateCellRuntime,
    private_seed_commitment,
    private_world_commitment,
)
from chemworld.eval.method_protocol import (
    METHOD_RESOURCE_LEDGER_VERSION,
    METHOD_RESOURCE_USAGE_VERSION,
)
from chemworld.eval.resource_accounting_v0_4 import (
    RL_TRAINING_RESOURCE_VERSION,
    audit_cell_resource_accounting,
)
from chemworld.rl.hybrid_actions import policy_distribution_contract

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "configs/methods/rl_v0.4/rl_methods.json"
SHA = "a" * 64
RUN_ID = "b" * 64
COMMIT = "c" * 40


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _binding(payload: dict[str, Any], root: Path) -> RLCheckpointBinding:
    formal = json.loads(
        (ROOT / "configs/benchmark/formal_protocol_v0.4.json").read_text(encoding="utf-8")
    )
    return RLCheckpointBinding.from_payload(payload, root=root, formal_protocol=formal)


def _checkpoint_payload(
    root: Path,
    *,
    method_id: str = "ppo",
    task_id: str = "partition-discovery",
) -> dict[str, Any]:
    checkpoint = root / f"runs/{method_id}-{task_id}.zip"
    checkpoint.parent.mkdir(parents=True, exist_ok=True)
    checkpoint.write_bytes(f"checkpoint:{method_id}:{task_id}".encode())
    checkpoint_sha = file_sha256(checkpoint)
    contracts = task_contract_bundle(task_id)
    manifest: dict[str, Any] = {
        "schema_version": "chemworld-rl-checkpoint-0.2",
        "algorithm": method_id,
        "task_id": task_id,
        "checkpoint_sha256": checkpoint_sha,
        "allocation": {
            "name": "train",
            "namespace_id": "chemworld-v0.5-train-0.4",
        },
        "bench_finetuning_used": False,
        "action_contract_hash": contracts["action_contract_sha256"],
        "training_reward_contract_hash": contracts[
            "training_reward_contract_sha256"
        ],
        "versions": {"stable_baselines3": "2.9.0", "torch": "2.13.0"},
    }
    if method_id == "ppo":
        manifest["policy_distribution_contract_hash"] = contracts[
            "ppo_policy_distribution_contract_sha256"
        ]
    manifest_path = root / f"runs/{method_id}-{task_id}.manifest.json"
    _write_json(manifest_path, manifest)
    resources = {
        "schema_version": RL_TRAINING_RESOURCE_VERSION,
        "accounting_complete": True,
        "training_run_id": f"train-{method_id}-{task_id}-seed0",
        "checkpoint_sha256": checkpoint_sha,
        "source_manifest_sha256": file_sha256(manifest_path),
        "requested_training_environment_step_count": 100,
        "training_environment_step_count": 100,
        "cpu_time_s": 2.0,
        "gpu_time_s": 0.0,
        "wall_time_s": 2.5,
    }
    resource_path = root / f"runs/{method_id}-{task_id}.resources.json"
    _write_json(resource_path, resources)
    return {
        "method_id": method_id,
        "task_id": task_id,
        "checkpoint_path": checkpoint.relative_to(root).as_posix(),
        "checkpoint_manifest_path": manifest_path.relative_to(root).as_posix(),
        "training_resource_path": resource_path.relative_to(root).as_posix(),
        "checkpoint_sha256": checkpoint_sha,
    }


def _runtime() -> PrivateCellRuntime:
    return PrivateCellRuntime(
        method_seed=17,
        world_seed=10_001,
        seed_nonce="private-method-nonce",
        world_nonce="private-world-nonce",
        world_interventions=(),
    )


def _spec(binding: RLCheckpointBinding) -> FormalCellSpec:
    runtime = _runtime()
    pair_id = "pair-opaque-rl-000"
    return FormalCellSpec(
        run_id=RUN_ID,
        task_id=binding.task_id,
        pair_id=pair_id,
        spectrum_condition="masked",
        private_seed_commitment=private_seed_commitment(
            run_id=RUN_ID,
            pair_id=pair_id,
            method_seed=runtime.method_seed,
            nonce=runtime.seed_nonce,
        ),
        world_commitment=private_world_commitment(
            run_id=RUN_ID,
            task_id=binding.task_id,
            pair_id=pair_id,
            world_seed=runtime.world_seed,
            nonce=runtime.world_nonce,
            interventions=runtime.world_interventions,
        ),
        protocol_sha256=SHA,
        backend_semantic_sha256=SHA,
        evaluator_sha256=SHA,
        interaction_protocol_sha256=SHA,
        statistics_protocol_sha256=SHA,
        reference_manifest_sha256=SHA,
        source_commit=COMMIT,
        complete_experiments=1,
        operation_limit=1,
        method=FormalMethodBinding(
            method_id=binding.method_id,
            kind="rl",
            artifact_sha256=SHA,
            resource_profile="rl_evaluation",
            checkpoint_sha256=binding.checkpoint_sha256,
        ),
    )


def _fake_run_agent(**kwargs: Any) -> None:
    output = Path(kwargs["output_path"])
    record = {
        "step": 1,
        "action": {"operation": "measure", "instrument": "final_assay"},
        "observation": {"signal": 0.5},
        "reward": 0.0,
        "method_resources": {
            "schema_version": METHOD_RESOURCE_LEDGER_VERSION,
            "accounting_complete": True,
            "operation_count": 1,
            "complete_experiment_count": 1,
            "decision_wall_time_s": 0.01,
            "update_wall_time_s": 0.0,
            "run_wall_time_s": 0.01,
            "reached_checkpoints": [1],
            "limits": {
                "operation_limit": 1,
                "complete_experiment_limit": 1,
                "checkpoint_complete_experiments": [1],
            },
            "agent_usage": {
                "schema_version": METHOD_RESOURCE_USAGE_VERSION,
                "accounting_complete": True,
                "usage_source": "frozen_rl_checkpoint_inference",
                "model_call_count": 0,
                "input_token_count": 0,
                "output_token_count": 0,
                "monetary_cost_usd": 0.0,
                "training_environment_step_count": 0,
                "cpu_time_s": 0.001,
                "gpu_time_s": 0.0,
                "model_provenance": {},
            },
        },
    }
    output.write_text(json.dumps(record) + "\n", encoding="utf-8")


def test_v04_contract_audit_is_ready_but_does_not_claim_training() -> None:
    report = audit_formal_rl_contract(load_formal_rl_config(CONFIG), root=ROOT)
    assert report["controls_ready"] is True
    assert report["status"] == "contract_ready_training_pending"
    assert report["benchmark_claim_allowed"] is False
    assert report["parent_task_complete"] is False
    assert report["task_count"] == 4
    assert report["method_count"] == 2
    assert report["required_training_run_count"] == 40
    assert report["required_checkpoint_count"] == 8
    assert report["formal_ready_checkpoint_count"] == 0
    assert all(report["checks"].values())


def test_contract_audit_fails_closed_on_bench_access_or_sac_claim() -> None:
    config = load_formal_rl_config(CONFIG)
    config["split_bindings"]["bench_access"] = "allowed"
    config["methods"]["sac"]["native_hybrid_distribution"] = True
    report = audit_formal_rl_contract(config, root=ROOT)
    assert report["controls_ready"] is False
    assert report["status"] == "contract_failed"
    assert report["checks"]["bench_and_reference_feedback_forbidden"] is False
    assert report["checks"]["sac_latent_comparability_disclosed"] is False


@pytest.mark.parametrize("method_id", ["ppo", "sac"])
def test_checkpoint_binding_verifies_contracts_and_separate_training_ledger(
    tmp_path: Path, method_id: str
) -> None:
    payload = _checkpoint_payload(tmp_path, method_id=method_id)
    binding = _binding(payload, tmp_path)
    assert binding.method_id == method_id
    assert binding.public_summary()["training_resources_separate_from_evaluation"] is True
    assert binding.public_summary()["training_environment_step_count"] == 100


def test_checkpoint_binding_rejects_train_namespace_and_resource_drift(tmp_path: Path) -> None:
    payload = _checkpoint_payload(tmp_path)
    manifest_path = tmp_path / payload["checkpoint_manifest_path"]
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["allocation"]["namespace_id"] = "chemworld-v0.5-bench-private-0.4"
    _write_json(manifest_path, manifest)
    resource_path = tmp_path / payload["training_resource_path"]
    resources = json.loads(resource_path.read_text(encoding="utf-8"))
    resources["source_manifest_sha256"] = file_sha256(manifest_path)
    _write_json(resource_path, resources)
    with pytest.raises(FormalRLContractError, match="Train namespace"):
        _binding(payload, tmp_path)

    payload = _checkpoint_payload(tmp_path)
    resources = json.loads(resource_path.read_text(encoding="utf-8"))
    resources["training_environment_step_count"] = 99
    _write_json(resource_path, resources)
    with pytest.raises(FormalRLContractError, match="training-resource ledger"):
        _binding(payload, tmp_path)


def test_checkpoint_index_rejects_duplicate_task_method(tmp_path: Path) -> None:
    payload = _checkpoint_payload(tmp_path)
    index = {
        "schema_version": FORMAL_RL_CHECKPOINT_INDEX_VERSION,
        "checkpoints": [payload, payload],
    }
    path = tmp_path / "checkpoint-index.json"
    _write_json(path, index)
    formal = json.loads(
        (ROOT / "configs/benchmark/formal_protocol_v0.4.json").read_text(encoding="utf-8")
    )
    with pytest.raises(FormalRLContractError, match="duplicate"):
        load_checkpoint_index(path, root=tmp_path, formal_protocol=formal)


def test_formal_adapter_binds_cell_and_keeps_training_resources_out_of_cell(
    tmp_path: Path,
) -> None:
    binding = _binding(_checkpoint_payload(tmp_path), tmp_path)
    spec = _spec(binding)
    output = tmp_path / "trajectory.jsonl"
    adapter = FormalRLAdapter(
        binding,
        agent_factory=lambda _binding, _seed: object(),
        run_agent_fn=_fake_run_agent,
    )
    adapter.execute(spec=spec, runtime=_runtime(), trajectory_path=output)
    records = [json.loads(line) for line in output.read_text(encoding="utf-8").splitlines()]
    final = records[-1]
    assert final["formal_cell_identity_sha256"] == spec.cell_identity_sha256
    assert final["formal_method_id"] == "ppo"
    assert final["method_resources"]["agent_usage"][
        "training_environment_step_count"
    ] == 0
    assert "training_resource" not in final["formal_resource_evidence"]
    accounting = audit_cell_resource_accounting(
        records,
        cell_identity_sha256=spec.cell_identity_sha256,
        method_id="ppo",
        method_kind="rl",
        resource_profile="rl_evaluation",
        rl_checkpoint_sha256=binding.checkpoint_sha256,
    )
    assert accounting["accounting_complete"] is True
    assert accounting["axes"]["training_environment_step_count"] == 0


def test_formal_adapter_registry_is_exact_and_rejects_unbound_task(tmp_path: Path) -> None:
    binding = _binding(_checkpoint_payload(tmp_path), tmp_path)
    registry = FormalAdapterRegistry()
    factory = FormalRLAdapterFactory(
        [binding],
        agent_factory=lambda _binding, _seed: object(),
        run_agent_fn=_fake_run_agent,
    )
    factory.register(registry)
    assert registry.registered_methods() == (("ppo", "rl"),)
    assert registry.create(_spec(binding)).method_id == "ppo"

    other_payload = _checkpoint_payload(
        tmp_path / "other",
        task_id="reaction-to-crystallization",
    )
    other = _binding(other_payload, tmp_path / "other")
    with pytest.raises(FormalRLContractError, match="no frozen RL checkpoint"):
        factory.create(_spec(other))


def test_formal_adapter_rejects_unregistered_spectrum_condition(tmp_path: Path) -> None:
    binding = _binding(_checkpoint_payload(tmp_path), tmp_path)
    spec = _spec(binding)
    assigned = FormalCellSpec(
        **{
            **spec.__dict__,
            "spectrum_condition": "assigned",
        }
    )
    adapter = FormalRLAdapter(
        binding,
        agent_factory=lambda _binding, _seed: object(),
        run_agent_fn=_fake_run_agent,
    )
    with pytest.raises(FormalRLContractError, match="masked spectra"):
        adapter.execute(spec=assigned, runtime=_runtime(), trajectory_path=tmp_path / "x.jsonl")


def test_frozen_agent_reports_inference_resources_not_checkpoint_training() -> None:
    agent = FrozenSB3Agent.__new__(FrozenSB3Agent)
    agent.algorithm = "ppo"
    agent.checkpoint_sha256 = "d" * 64
    agent.checkpoint_manifest = {
        "training_environment_step_count": 102_400,
        "cpu_time_s": 1000.0,
        "gpu_time_s": 900.0,
        "versions": {"stable_baselines3": "2.9.0", "torch": "2.13.0"},
    }
    agent._evaluation_cpu_time_s = 0.125
    agent._evaluation_gpu_time_s = 0.25
    agent.resource_reporting_scope = "formal_evaluation_only"
    usage = agent.method_resource_usage()
    assert usage["training_environment_step_count"] == 0
    assert usage["cpu_time_s"] == 0.125
    assert usage["gpu_time_s"] == 0.25
    assert usage["training_resource_policy"].endswith("not_evaluation_cell")


def test_dependency_free_policy_contract_is_stable_for_every_core_task() -> None:
    hashes = set()
    for task_id in load_formal_rl_config(CONFIG)["formal_core_tasks"]:
        bundle = task_contract_bundle(task_id)
        policy = bundle["ppo_policy_distribution_contract"]
        rebuilt = policy_distribution_contract(tuple(policy["parameter_keys"]))
        assert rebuilt == policy
        assert policy["operation_distribution"] == "public-affordance-masked categorical"
        assert policy["irrelevant_parameter_log_prob"] is False
        hashes.add(policy["contract_hash"])
    assert len(hashes) == 1
