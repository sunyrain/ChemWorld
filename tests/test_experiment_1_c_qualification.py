from __future__ import annotations

from pathlib import Path

from chemworld.eval.experiment_1_c_qualification import (
    entity_prior_audit,
    load_contract,
    parametric_prior_arms,
    structural_prior_audit,
    world_truth_audit,
)

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "configs/benchmark/experiment_1_c_qualification_v1.0.1.json"


def test_c_contract_freezes_five_distinct_executable_worlds() -> None:
    contract = load_contract(ROOT, CONTRACT_PATH)
    truths = [
        world_truth_audit(contract, world)
        for world in contract["worlds"]["qualification"]
    ]

    assert [row["world_id"] for row in truths] == [f"C-W0{i}" for i in range(1, 6)]
    assert all(row["deterministic"] for row in truths)
    assert len({row["truth_sha256"] for row in truths}) == 5
    assert len(
        {
            (
                row["crystallization_nucleation_multiplier"],
                row["crystallization_solubility_multiplier"],
            )
            for row in truths
        }
    ) == 5


def test_c_entity_prior_is_blind_schema_matched_solvent_swap() -> None:
    contract = load_contract(ROOT, CONTRACT_PATH)
    audit = entity_prior_audit(contract)

    assert audit["passed"] is True
    assert audit["checks"]["schema_matched"] is True
    assert audit["checks"]["text_template_matched"] is True
    assert audit["checks"]["solvent_only_transposition"] is True
    assert audit["leakage_tokens"] == []


def test_c_parametric_threshold_generator_varies_and_is_symmetric() -> None:
    contract = load_contract(ROOT, CONTRACT_PATH)
    audits = [
        parametric_prior_arms(contract, world)
        for world in contract["worlds"]["qualification"]
    ]

    assert all(audit["passed"] for audit in audits)
    assert all(audit["checks"]["schema_matched"] for audit in audits)
    assert all(audit["leakage_tokens"] == [] for audit in audits)


def test_c_structural_prior_uses_seed_mediated_candidate() -> None:
    audit = structural_prior_audit()

    assert audit["passed"] is True
    assert audit["checks"]["same_public_keys"] is True
    assert audit["checks"]["target_is_seed_mediated"] is True
