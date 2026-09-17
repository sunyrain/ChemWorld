from __future__ import annotations

import json
from pathlib import Path

from chemworld.eval.experiment_1_ec_qualification import (
    EXPECTED_COMMON_GATES,
    analyze_entity_world,
    entity_prior_audit,
    load_contract,
    private_world_audit,
)

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "configs/benchmark/experiment_1_ec_qualification_v1.0.1.json"


def _contract() -> dict:
    return load_contract(ROOT, CONTRACT_PATH)


def _receipt(anchor: int, category: int, replicate: int, value: float) -> dict:
    return {
        "status": "completed",
        "nuisance_anchor": anchor,
        "target_category": category,
        "replicate": replicate,
        "recipe_id": f"recipe-{anchor}-{category}",
        "allowed_metrics": {
            "transport_efficiency": value,
            "ohmic_efficiency": value,
        },
        "exact_replay": {"verified": True},
    }


def test_frozen_contract_binds_sources_and_keeps_participant_disabled() -> None:
    contract = _contract()

    assert contract["common_gates"] == list(EXPECTED_COMMON_GATES)
    assert contract["execution"]["participant_execution_authorized"] is False
    assert contract["execution"]["formal_benchmark_execution_authorized"] is False
    assert [row["world_seed"] for row in contract["worlds"]["qualification"]] == list(range(5))


def test_entity_public_priors_are_symmetric_and_leakage_free() -> None:
    audit = entity_prior_audit(_contract())

    assert audit["passed"] is True
    assert audit["aligned_sha256"] != audit["misspecified_sha256"]
    assert audit["leakage_tokens"] == []


def test_private_world_digests_are_distinct_and_mapping_is_not_reversed() -> None:
    audits = [private_world_audit(_contract(), world_seed=seed) for seed in range(5)]

    assert len({row["truth_sha256"] for row in audits}) == 5
    assert all(row["aligned_mapping_not_reversed"] for row in audits)


def test_entity_analysis_requires_all_eight_gates() -> None:
    receipts = []
    for anchor in range(2):
        for category in range(4):
            base = 0.20 if category == 0 else 0.80 if category == 2 else 0.50
            for replicate, offset in enumerate((-0.002, 0.0, 0.002)):
                receipts.append(_receipt(anchor, category, replicate, base + offset))

    report = analyze_entity_world(
        _contract(),
        world_id="EC-W01",
        world_seed=0,
        receipts=receipts,
    )

    assert report["status"] == "qualified"
    assert report["failures"] == []
    assert all(report["gates"].values())
    assert report["denominators"] == {
        "planned": 24,
        "attempted": 24,
        "completed": 24,
        "exact_replay": 24,
        "failures": 0,
    }


def test_contract_is_valid_json() -> None:
    assert isinstance(json.loads(CONTRACT_PATH.read_text(encoding="utf-8")), dict)
