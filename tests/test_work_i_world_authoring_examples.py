from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest
from scripts.validate_work_i_world_authoring_examples import (
    EXAMPLE_PATHS,
    INVENTORY_PATH,
    REPORT_PATH,
    WorldAuthoringExampleError,
    _read_json,
    receipt_sha256,
    validate_example_payload,
)

from chemworld.foundation.world_fork_manifest import load_world_component_inventory
from chemworld.foundation.world_fork_spec import WorldForkSpecError

ROOT = Path(__file__).resolve().parents[1]


def _receipt() -> dict[str, object]:
    return _read_json(ROOT / REPORT_PATH)


def test_committed_receipt_is_self_hashed_and_frozen() -> None:
    receipt = _receipt()
    assert receipt["receipt_sha256"] == receipt_sha256(receipt)
    assert receipt["status"] == "passed"


def test_examples_cover_both_frozen_intervention_classes() -> None:
    receipt = _receipt()
    examples = receipt["examples"]
    assert isinstance(examples, list)
    assert len(examples) == 2
    assert {row["intervention_class"] for row in examples} == {
        "mechanism_or_constitutive_law",
        "material_law_counterfactual",
    }
    assert {row["target_component_id"] for row in examples} == {
        "private_physics.constitutive_laws",
        "private_physics.material_laws",
    }
    assert all(
        row["public_contract_invariant"] is True
        and row["public_contract_component_count"] == 9
        and row["invariant_component_count"] == 14
        for row in examples
    )
    assert receipt["claim_boundary"] == {
        "agent_performance_claim": False,
        "divergence_claim": False,
        "execution_claim": False,
        "provider_calls_required": False,
        "qualification_certificate_replaced": False,
    }


def test_wrapper_unknown_fields_and_claim_promotion_fail_closed() -> None:
    inventory = load_world_component_inventory(ROOT / INVENTORY_PATH)
    payload = _read_json(ROOT / EXAMPLE_PATHS[0])
    payload["undeclared"] = True
    with pytest.raises(WorldAuthoringExampleError, match="fields do not match schema"):
        validate_example_payload(payload, inventory)

    payload = _read_json(ROOT / EXAMPLE_PATHS[0])
    payload["claim_boundary"]["execution_claim"] = True
    with pytest.raises(WorldAuthoringExampleError, match="cannot claim execution"):
        validate_example_payload(payload, inventory)


def test_public_target_and_receipt_tampering_fail_closed() -> None:
    inventory = load_world_component_inventory(ROOT / INVENTORY_PATH)
    payload = _read_json(ROOT / EXAMPLE_PATHS[0])
    payload["target_component_id"] = "public_contract.actions"
    with pytest.raises(WorldForkSpecError, match="not an intervention target"):
        validate_example_payload(payload, inventory)

    receipt = deepcopy(_receipt())
    receipt["claim_boundary"]["execution_claim"] = True
    assert receipt["receipt_sha256"] != receipt_sha256(receipt)
