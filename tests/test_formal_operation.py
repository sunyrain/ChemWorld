from __future__ import annotations

import copy
import json

from chemworld.agents.task_recipes import task_recipe_event_count
from chemworld.eval.formal_operation import (
    audit_operation_method_freeze,
    build_formal_operation_registry,
    formal_operation_method_bindings,
    load_operation_method_freeze,
)
from chemworld.eval.formal_protocol_v0_4 import load_formal_protocol
from chemworld.eval.formal_runner import (
    FormalCellSpec,
    PrivateCellRuntime,
    canonical_sha256,
    issue_run_manifest,
    load_issued_cell,
    private_seed_commitment,
    private_world_commitment,
    run_formal_cell,
)
from chemworld.tasks import get_task


def _runtime() -> PrivateCellRuntime:
    return PrivateCellRuntime(
        method_seed=230_001,
        world_seed=11_001,
        seed_nonce="operation-method-seed-private",
        world_nonce="operation-world-seed-private",
        world_interventions=(),
    )


def _spec(method_id: str, *, experiments: int = 2) -> FormalCellSpec:
    runtime = _runtime()
    task_id = "partition-discovery"
    run_id = "7" * 64
    pair_id = "operation-dev-pair-opaque"
    protocol = load_formal_protocol()
    operation_limit = 2 * task_recipe_event_count(get_task(task_id).to_dict()) * experiments
    return FormalCellSpec(
        run_id=run_id,
        task_id=task_id,
        pair_id=pair_id,
        spectrum_condition="masked",
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
        backend_semantic_sha256="a" * 64,
        evaluator_sha256="c" * 64,
        interaction_protocol_sha256="d" * 64,
        statistics_protocol_sha256="e" * 64,
        reference_manifest_sha256="f" * 64,
        source_commit="1" * 40,
        complete_experiments=experiments,
        operation_limit=operation_limit,
        method=formal_operation_method_bindings()[method_id],
    )


def test_operation_freeze_is_source_bound_unique_and_bench_unseen() -> None:
    freeze = load_operation_method_freeze()
    report = audit_operation_method_freeze(freeze)

    assert report["controls_ready"] is True
    assert report["bench_results_used"] is False
    assert report["reference_search_results_used"] is False
    assert report["method_count"] == report["unique_artifact_count"] == 3
    registry = build_formal_operation_registry(freeze)
    assert registry.registered_methods() == (
        ("observation_blind", "classic"),
        ("operation_random", "classic"),
        ("rule_based", "classic"),
    )


def test_operation_freeze_fails_closed_on_capability_or_source_tamper() -> None:
    freeze = load_operation_method_freeze()
    tampered = copy.deepcopy(freeze)
    tampered["methods"]["operation_random"]["consumes_spectra"] = True
    report = audit_operation_method_freeze(tampered)
    assert report["controls_ready"] is False
    assert "operation_random:spectrum_consumption_mismatch" in report["reasons"]
    assert "operation_random:artifact_sha256_mismatch" in report["reasons"]


def test_formal_operation_adapter_replays_with_complete_resources(tmp_path) -> None:
    spec = _spec("observation_blind")
    manifest = issue_run_manifest([spec], metadata={"formal": False, "split": "dev"})
    issued = load_issued_cell(manifest, cell_identity_sha256=spec.cell_identity_sha256)

    outcome = run_formal_cell(
        issued_cell=issued,
        runtime=_runtime(),
        adapter=build_formal_operation_registry().create(spec),
        output_root=tmp_path,
    )

    assert outcome.status == "succeeded"
    resources = json.loads((outcome.cell_dir / "resources.json").read_text(encoding="utf-8"))
    result = json.loads((outcome.cell_dir / "result.json").read_text(encoding="utf-8"))
    records = [
        json.loads(line)
        for line in (outcome.cell_dir / "trajectory.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    assert resources["resource_profile"] == "operation_baseline"
    assert resources["accounting_complete"] is True
    assert resources["axes"]["complete_experiment_count"] == 2
    assert resources["axes"]["provider_request_count"] == 0
    assert all(record["formal_method_id"] == "observation_blind" for record in records)
    assert all(
        record["explanation"]["decision_audit"]["status"] == "provided" for record in records
    )
    assert result["score_replay"]["risk_limit_source"] == "bound_override"
