from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

from chemworld.eval.work_i_data_contract import (
    CONTRACT_ID,
    build_work_i_data_contract,
    data_contract_sha256,
    validate_work_i_data_contract,
)

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "configs/benchmark/work_i_incremental_data_contract_v0.1.json"


def _committed_contract() -> dict[str, object]:
    payload = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def test_committed_contract_is_the_exact_self_hashed_rebuild() -> None:
    contract = _committed_contract()
    assert contract["contract_id"] == CONTRACT_ID
    assert contract["contract_sha256"] == data_contract_sha256(contract)
    assert contract == build_work_i_data_contract(ROOT)
    assert validate_work_i_data_contract(contract, root=ROOT) == []


def test_contract_freezes_track_populations_and_analysis_roles() -> None:
    tracks = _committed_contract()["track_contracts"]
    assert tracks["F"]["formal_population"] == {
        "case_count": 2,
        "world_seed_count_per_case": 3,
        "parent_child_pair_count": 6,
        "world_variants_per_pair": 2,
        "executions_per_variant": 2,
        "trace_count": 24,
        "provider_call_count": 0,
    }
    assert tracks["V"]["formal_population"]["primary_campaign_count"] == 30
    assert tracks["V"]["formal_population"]["primary_closed_lifecycle_count"] == 180
    assert tracks["V"]["formal_population"]["deterministic_retest_campaign_count"] == 30
    assert tracks["L"]["formal_population"]["discarded_lifecycle_count"] == 36
    assert tracks["L"]["formal_population"]["closed_lifecycle_count"] == 60
    assert tracks["L"]["formal_population"]["discard_opportunity_cell_count"] == 9
    assert tracks["L"]["formal_population"]["no_discard_opportunity_cell_ids"] == ["cell-02"]
    assert tracks["F"]["record_schemas"]["world_fork_trace"]["analysis_role"] == ("audit_only")
    assert tracks["V"]["record_schemas"]["policy_retest_campaign"]["analysis_role"] == "reliability"


def test_contract_freezes_units_counting_and_missingness() -> None:
    contract = _committed_contract()
    units = contract["unit_registry"]
    assert units["mole"]["canonical_unit"] == "mol"
    assert units["dimensionless_fraction"]["maximum"] == 1.0
    assert units["normalized_score_difference"] == {
        "canonical_unit": "1",
        "json_type": "number",
        "minimum": -1.0,
        "maximum": 1.0,
    }
    counting = contract["cross_track_counting_rules"]
    assert counting["primary_units"] == {
        "F": "parent_child_pair",
        "V": "original_campaign_profile",
        "L": "discarded_lifecycle",
    }
    assert counting["never_pool_distinct_primary_units"] is True
    assert counting["exact_replays_are_verification_not_additional_primary_units"] is True
    assert counting["deterministic_retests_are_reliability_not_additional_primary_units"] is True
    assert counting["evaluator_shadow_is_not_an_original_agent_decision_or_experiment"] is True
    missingness = contract["nullability_and_failure"]
    assert missingness["only_json_null_represents_missing_numeric_values"] is True
    assert missingness["complete_case_substitution_for_registered_primary"] is False


def test_contract_binds_all_sources_and_preserves_d03_boundary() -> None:
    contract = _committed_contract()
    bindings = contract["source_bindings"]
    assert len(bindings) == 7
    assert {binding["artifact_id"] for binding in bindings} == {
        "world_fork_qualification",
        "world_fork_certificate",
        "known_policy_validity_report",
        "known_policy_delivery_manifest",
        "latent_terminal_estimand_contract",
        "latent_terminal_reconstructability",
        "latent_terminal_replay_qualification",
    }
    assert all(len(binding["embedded_sha256"]) == 64 for binding in bindings)
    assert all(len(binding["file_sha256"]) == 64 for binding in bindings)
    assert all(contract["source_validation_gates"].values())
    derived = contract["derived_layer_requirements"]
    assert derived["consumer_task"] == "W1-D03"
    assert derived["required_contract_binding"] == "contract_sha256"
    assert derived["immutable_manifest_required"] is True
    assert derived["global_artifact_mutation_authorized_by_d01"] is False


def test_validator_rejects_rehashed_count_unit_and_boundary_tampering() -> None:
    original = _committed_contract()

    bad_count = deepcopy(original)
    bad_count["track_contracts"]["V"]["formal_population"]["primary_campaign_count"] = 31
    bad_count["contract_sha256"] = data_contract_sha256(bad_count)
    assert "contract differs from deterministic frozen rebuild" in (
        validate_work_i_data_contract(bad_count, root=ROOT)
    )

    bad_unit = deepcopy(original)
    bad_unit["unit_registry"]["mole"]["canonical_unit"] = "mmol"
    bad_unit["contract_sha256"] = data_contract_sha256(bad_unit)
    assert "unit registry differs from the frozen registry" in (
        validate_work_i_data_contract(bad_unit)
    )

    bad_boundary = deepcopy(original)
    bad_boundary["derived_layer_requirements"]["global_artifact_mutation_authorized_by_d01"] = True
    bad_boundary["contract_sha256"] = data_contract_sha256(bad_boundary)
    assert "derived-layer boundary changed" in validate_work_i_data_contract(bad_boundary)
