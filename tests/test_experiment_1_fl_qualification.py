from __future__ import annotations

from pathlib import Path

from chemworld.eval.experiment_1_fl_qualification import (
    entity_prior_audit,
    load_contract,
    parametric_prior_arms,
    structural_prior_arms,
    world_truth_audit,
)

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "configs/benchmark/experiment_1_fl_qualification_v1.0.1.json"


def test_fl_contract_freezes_five_distinct_executable_worlds() -> None:
    contract = load_contract(ROOT, CONTRACT_PATH)
    truths = [world_truth_audit(contract, world) for world in contract["worlds"]["qualification"]]

    assert [row["world_id"] for row in truths] == [f"FL-W0{i}" for i in range(1, 6)]
    assert all(row["deterministic"] for row in truths)
    assert len({row["truth_sha256"] for row in truths}) == 5
    assert (
        len(
            {
                (
                    row["flow_rate_multiplier"],
                    row["flow_residence_multiplier"],
                    row["flow_boundary_ua_multiplier"],
                )
                for row in truths
            }
        )
        == 5
    )


def test_fl_entity_prior_is_blind_schema_matched_catalyst_swap() -> None:
    contract = load_contract(ROOT, CONTRACT_PATH)
    audit = entity_prior_audit(contract)

    assert audit["passed"] is True
    assert audit["checks"]["schema_matched"] is True
    assert audit["checks"]["text_template_matched"] is True
    assert audit["checks"]["catalyst_only_transposition"] is True
    assert audit["leakage_tokens"] == []


def test_fl_parametric_prior_arms_are_schema_matched_and_blind() -> None:
    contract = load_contract(ROOT, CONTRACT_PATH)
    audit = parametric_prior_arms(contract)

    assert audit["passed"] is True
    assert audit["checks"]["schema_matched"] is True
    assert audit["leakage_tokens"] == []


def test_fl_structural_prior_arms_are_schema_matched_and_blind() -> None:
    contract = load_contract(ROOT, CONTRACT_PATH)
    audit = structural_prior_arms(contract)

    assert audit["passed"] is True
    assert audit["checks"]["schema_matched"] is True
    assert audit["leakage_tokens"] == []
