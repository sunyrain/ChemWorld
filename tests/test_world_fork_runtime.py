from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

import pytest
from scripts.run_work_i_world_fork import build_report

from chemworld.eval.world_fork_audit import audit_runtime_world_fork
from chemworld.foundation.world_fork_divergence import DivergenceOracleSpec
from chemworld.foundation.world_fork_manifest import load_world_component_inventory
from chemworld.foundation.world_fork_runtime import (
    load_world_fork_qualification_config,
    run_runtime_world_fork,
)

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "configs/benchmark/work_i_world_fork_qualification_v0.1.json"
INVENTORY = ROOT / "configs/benchmark/work_i_world_fork_component_inventory_v0.1.json"
PREFLIGHT = (
    ROOT
    / "workstreams/arxiv_v1/reports/work-i-world-fork-runtime-preflight-v0.1.json"
)


def _case(case_id: str) -> dict:
    config = load_world_fork_qualification_config(CONFIG)
    return next(item for item in config["cases"] if item["case_id"] == case_id)


@pytest.mark.parametrize(
    "case_id",
    [
        "partition-constitutive-law-family",
        "electrochemical-material-law-counterfactual",
    ],
)
def test_real_world_fork_changes_only_declared_private_component(case_id: str) -> None:
    inventory = load_world_component_inventory(INVENTORY)
    case = _case(case_id)
    runtime = run_runtime_world_fork(
        inventory=inventory,
        task_id=case["task_id"],
        seed=0,
        intervention_class=case["intervention_class"],
        target_component_id=case["target_component_id"],
        intervention_payload=case["intervention_payload"],
    )
    spec = runtime["fork_spec"]
    assert spec["component_diff"]["changed_component_ids"] == [case["target_component_id"]]
    assert runtime["execution"]["passed"] is True
    assert runtime["exact_replay"]["passed"] is True
    assert runtime["provider_call_count"] == 0

    oracle = DivergenceOracleSpec.from_dict(case["oracle"], inventory=inventory)
    audit = audit_runtime_world_fork(runtime, inventory=inventory, oracle=oracle)
    assert audit["passed"] is True
    assert all(audit["gates"].values())
    certificate = audit["public_contract_certificate"]
    assert certificate["public_component_count"] == 9
    assert certificate["invariant_component_count"] == 9
    assert certificate["identity_leakage_finding_count"] == 0


def test_runtime_audit_detects_trace_tampering() -> None:
    inventory = load_world_component_inventory(INVENTORY)
    case = _case("partition-constitutive-law-family")
    runtime = run_runtime_world_fork(
        inventory=inventory,
        task_id=case["task_id"],
        seed=0,
        intervention_class=case["intervention_class"],
        target_component_id=case["target_component_id"],
        intervention_payload=case["intervention_payload"],
    )
    tampered = deepcopy(runtime)
    tampered["replays"]["child"]["steps"][0]["reward"] = 1.0
    oracle = DivergenceOracleSpec.from_dict(case["oracle"], inventory=inventory)
    audit = audit_runtime_world_fork(tampered, inventory=inventory, oracle=oracle)
    assert audit["passed"] is False
    assert audit["gates"]["exact_replay"] is False
    assert audit["exact_replay_audit"]["replay_hash_bound"]["child"] is False


def test_committed_preflight_is_deterministically_rebuilt() -> None:
    config = load_world_fork_qualification_config(CONFIG)
    rebuilt = build_report(config, selected_seeds=(0,))
    committed = json.loads(PREFLIGHT.read_text(encoding="utf-8"))
    assert committed == rebuilt
    assert committed["pair_count"] == 2
    assert committed["trace_count"] == 8
    assert committed["passed"] is True
