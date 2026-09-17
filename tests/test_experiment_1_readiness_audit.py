from pathlib import Path

import pytest
from scripts.run_experiment_1_readiness_audit import (
    _smoke_gates,
    _unit_gates,
    load_contract,
)

from chemworld.eval.experiment_1_ec_qualification import EXPECTED_COMMON_GATES

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize(
    ("system", "filename", "task_id"),
    (
        ("P", "experiment_1_p_readiness_v1.0.1.json", "reaction-to-purification"),
        ("D", "experiment_1_d_readiness_v1.0.1.json", "reaction-to-distillation"),
    ),
)
def test_readiness_contracts_are_frozen_and_hash_bound(
    system: str, filename: str, task_id: str
) -> None:
    contract = load_contract(ROOT / "configs" / "benchmark" / filename)
    assert contract["system_id"] == system
    assert contract["task_id"] == task_id
    assert tuple(contract["common_gates"]) == EXPECTED_COMMON_GATES
    assert [row["world_seed"] for row in contract["worlds"]] == list(range(5))
    assert contract["execution"]["qualification_denominator_authorized"] is False


def test_smoke_gates_require_verified_hash_complete_public_execution() -> None:
    row = {
        "verify_status": "pass",
        "invalid_count": 0,
        "constitution_failure_count": 0,
        "ledger_single_source_failures": 0,
        "public_leakage_failures": 0,
        "task_contract_hash": "a",
        "mechanism_hash": "b",
        "score_contract_hash": "c",
        "profile_hash": "d",
        "observation_contract_hash": "e",
    }
    assert _smoke_gates(row) == (True, True)
    assert _smoke_gates({**row, "public_leakage_failures": 1}) == (True, False)


def test_readiness_units_fail_closed_without_private_worlds() -> None:
    p_entity = _unit_gates("P", "entity", q2=True, q3=True)
    d_entity = _unit_gates("D", "entity", q2=True, q3=True)
    assert p_entity["Q1_world_integrity"] is False
    assert p_entity["Q4_prior_symmetry"] is False
    assert d_entity["Q4_prior_symmetry"] is True
    assert all(not gates["Q5_identifiability"] for gates in (p_entity, d_entity))
