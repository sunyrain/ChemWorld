from __future__ import annotations

import copy
import json
from pathlib import Path

from chemworld.agents.base import HistoryRecord
from chemworld.agents.greedy import GreedyLocalAgent
from chemworld.agents.task_recipes import (
    task_recipe_event_count,
    task_recipe_from_unit_vector,
    task_recipe_to_vector,
)
from chemworld.eval.formal_classic import (
    DEFAULT_CLASSIC_FREEZE_PATH,
    audit_classic_method_freeze,
    build_formal_classic_registry,
    formal_classic_method_bindings,
    load_classic_method_freeze,
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
        method_seed=210_001,
        world_seed=11_001,
        seed_nonce="method-seed-private",
        world_nonce="world-seed-private",
        world_interventions=(),
    )


def _spec(method_id: str, *, experiments: int = 5) -> FormalCellSpec:
    runtime = _runtime()
    task_id = "partition-discovery"
    run_id = "b" * 64
    pair_id = "dev-pair-opaque"
    protocol = load_formal_protocol()
    operation_limit = task_recipe_event_count(get_task(task_id).to_dict()) * experiments
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
        method=formal_classic_method_bindings()[method_id],
    )


def test_classic_freeze_is_source_bound_unique_and_bench_unseen() -> None:
    freeze = load_classic_method_freeze()
    report = audit_classic_method_freeze(freeze)
    assert report["controls_ready"] is True
    assert report["bench_results_used"] is False
    assert report["method_count"] == report["unique_artifact_count"] == 8
    registry = build_formal_classic_registry(freeze)
    assert registry.registered_methods() == tuple(
        (method_id, "classic") for method_id in sorted(freeze["methods"])
    )


def test_classic_freeze_fails_closed_on_source_or_encoding_tamper() -> None:
    freeze = load_classic_method_freeze()
    tampered = copy.deepcopy(freeze)
    tampered["methods"]["structured_gp_ei"]["recipe_encoding"] = "ordinal_ids"
    report = audit_classic_method_freeze(tampered)
    assert report["controls_ready"] is False
    assert any("typed_material_encoding_missing" in item for item in report["reasons"])


def test_greedy_local_does_not_apply_numeric_distance_to_material_ids() -> None:
    task_info = get_task("partition-discovery").to_dict()
    vector = [0.38, 0.5, 0.5, 0.63, 0.5, 0.5, 0.5, 0.5]
    recipe = task_recipe_from_unit_vector(task_info, vector)
    agent = GreedyLocalAgent(warmup=0, perturbation_scale=0.25)
    agent.exploration_probability = 0.0
    agent.reset(task_info, seed=7)
    agent._recipe_history = [
        HistoryRecord(step=1, action=recipe, observation={}, reward=1.0, info={})
    ]
    agent.act([])
    selected = task_recipe_to_vector(agent._active_recipe or {})
    assert selected[0] == vector[0]
    assert selected[3] == vector[3]
    assert agent.manifest()["material_distance_assumption"] == "none"


def test_formal_gp_adapter_replays_with_bound_risk_and_complete_resources(tmp_path) -> None:
    spec = _spec("structured_gp_ei")
    manifest = issue_run_manifest([spec], metadata={"formal": False, "split": "dev"})
    issued = load_issued_cell(manifest, cell_identity_sha256=spec.cell_identity_sha256)
    adapter = build_formal_classic_registry().create(spec)

    outcome = run_formal_cell(
        issued_cell=issued,
        runtime=_runtime(),
        adapter=adapter,
        output_root=tmp_path,
    )

    assert outcome.status == "succeeded"
    resources = json.loads((outcome.cell_dir / "resources.json").read_text(encoding="utf-8"))
    result = json.loads((outcome.cell_dir / "result.json").read_text(encoding="utf-8"))
    records = [
        json.loads(line)
        for line in (outcome.cell_dir / "trajectory.jsonl")
        .read_text(encoding="utf-8")
        .splitlines()
    ]
    assert resources["accounting_complete"] is True
    assert resources["axes"]["complete_experiment_count"] == 5
    assert resources["axes"]["fit_count"] == 1
    assert resources["axes"]["acquisition_optimization_count"] == 1
    contract = result["score_replay"]["task_evaluation_contract"]
    assert result["score_replay"]["risk_limit_source"] == "bound_override"
    assert contract["safety_limit"] == 0.2270542597781983
    assert records[0]["agent_metadata"]["agent_seed_disclosure"] == "private_committed"
    assert "seed" not in records[0]["agent_metadata"]


def test_safe_gp_activates_bound_constraint_in_dev_campaign(tmp_path) -> None:
    spec = _spec("structured_safe_gp_ei")
    adapter = build_formal_classic_registry().create(spec)
    trajectory = tmp_path / "safe-gp.jsonl"
    adapter.execute(spec=spec, runtime=_runtime(), trajectory_path=trajectory)
    records = [json.loads(line) for line in trajectory.read_text(encoding="utf-8").splitlines()]
    traces = records[-1]["agent_trace"]
    acquisitions = [item for item in traces if item["phase"] == "acquisition"]
    assert acquisitions
    diagnostics = acquisitions[-1]["decision_diagnostics"]
    assert diagnostics["risk_threshold"] == 0.2270542597781983
    assert diagnostics["safe_candidate_count"] <= diagnostics["candidate_count"]


HISTORICAL_FREEZE = (
    Path(__file__).resolve().parents[1]
    / "configs"
    / "methods"
    / "classic_v0.4"
    / "classic_methods.json"
)


def test_v041_freeze_namespace_preserves_v04_history() -> None:
    assert DEFAULT_CLASSIC_FREEZE_PATH.name == "classic_methods.json"
    assert DEFAULT_CLASSIC_FREEZE_PATH.parent.name == "classic_v0.4.1"
    assert HISTORICAL_FREEZE.is_file()
    assert DEFAULT_CLASSIC_FREEZE_PATH != HISTORICAL_FREEZE
