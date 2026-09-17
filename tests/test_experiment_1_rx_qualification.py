from __future__ import annotations

from pathlib import Path

from chemworld.eval.experiment_1_rx_qualification import (
    EXPECTED_ENTITY_PERMUTATION,
    entity_prior_audit,
    load_contract,
    structural_prior_arms,
    world_truth_audit,
)

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "configs/benchmark/experiment_1_rx_qualification_v1.0.1.json"


def _contract() -> dict:
    return load_contract(ROOT, CONTRACT_PATH)


def test_rx_contract_is_frozen_provider_free_and_participant_disabled() -> None:
    contract = _contract()

    assert contract["participant_provider_calls"] == 0
    assert contract["participant_execution_authorized"] is False
    assert contract["formal_benchmark_execution_authorized"] is False
    assert contract["execution"]["post_failure_redesign_in_same_campaign_forbidden"] is True
    assert tuple(contract["loci"]["entity"]["descriptor_permutation"]) == (
        EXPECTED_ENTITY_PERMUTATION
    )


def test_rx_truth_hash_is_deterministic_and_world_specific() -> None:
    contract = _contract()
    first = world_truth_audit(contract, world_seed=0)
    repeated = world_truth_audit(contract, world_seed=0)
    second = world_truth_audit(contract, world_seed=1)

    assert first == repeated
    assert first["truth_sha256"] != second["truth_sha256"]
    assert first["truth_family"] == "deactivating_baseline"
    assert len(first["mapping_rows"]) == 2


def test_rx_entity_and_structural_priors_are_symmetric_and_distinct() -> None:
    entity = entity_prior_audit(_contract())
    structural = structural_prior_arms()

    assert entity["passed"] is True
    assert entity["aligned_sha256"] != entity["misspecified_sha256"]
    assert set(structural["aligned"]) == set(structural["misspecified"])
    assert structural["aligned"]["claim"] != structural["misspecified"]["claim"]
