from __future__ import annotations

from pathlib import Path

import pytest

from chemworld.eval.experiment_1_pa_qualification import (
    entity_prior_audit,
    fit_effective_k,
    load_contract,
    structural_prior_arms,
    true_parametric_k_star,
    world_truth_audit,
)

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "configs/benchmark/experiment_1_pa_qualification_v1.0.1.json"


def test_pa_contract_freezes_five_distinct_executable_worlds() -> None:
    contract = load_contract(ROOT, CONTRACT_PATH)
    truths = [
        world_truth_audit(contract, world)
        for world in contract["worlds"]["qualification"]
    ]

    assert [row["world_id"] for row in truths] == [f"PA-W0{i}" for i in range(1, 6)]
    assert all(row["deterministic"] for row in truths)
    assert len({row["truth_sha256"] for row in truths}) == 5
    assert all(row["partition_coefficient_exponent"] == 1.0 for row in truths)


def test_pa_entity_priors_are_blind_schema_matched_single_swap() -> None:
    contract = load_contract(ROOT, CONTRACT_PATH)
    audit = entity_prior_audit(contract)

    assert audit["passed"] is True
    assert audit["checks"]["same_descriptor_multiset"] is True
    assert audit["checks"]["solvent_dossier_unchanged"] is True
    assert audit["checks"]["pair_table_withheld"] is True
    assert audit["leakage_tokens"] == []


def test_pa_private_k_star_is_derived_and_varies_across_worlds() -> None:
    contract = load_contract(ROOT, CONTRACT_PATH)
    targets = [
        true_parametric_k_star(contract, world)["k_star"]
        for world in contract["worlds"]["qualification"]
    ]

    assert all(value > 0.0 for value in targets)
    assert len({round(value, 6) for value in targets}) == 5


def test_effective_k_fit_recovers_ideal_allocation() -> None:
    expected = 3.4
    observations = []
    for organic, aqueous in ((0.008, 0.045), (0.019, 0.035), (0.030, 0.026)):
        fraction = expected * organic / (expected * organic + aqueous)
        observations.append(
            {
                "organic_fraction": fraction,
                "aqueous_fraction": 1.0 - fraction,
                "organic_volume_L": organic,
                "aqueous_volume_L": aqueous,
            }
        )

    result = fit_effective_k(observations)

    assert result["k_star"] == pytest.approx(expected, rel=0.002)
    assert result["rmse"] < 0.001


def test_pa_structural_prior_arms_are_symmetric_and_blind() -> None:
    arms = structural_prior_arms()

    assert arms["schema_matched"] is True
    assert arms["text_template_matched"] is True
    assert arms["leakage_tokens"] == []

