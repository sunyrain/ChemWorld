from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

from scripts.freeze_work_i_known_policies import build_artifact, build_markdown

from chemworld.eval.known_policy_contract import (
    FORMAL_WORLD_SEEDS,
    INFORMATION_ARMS,
    LIFECYCLES_PER_CELL,
    POLICY_IDS,
    PROBE_SCHEDULE,
    build_known_policy_contract,
    known_policy_contract_sha256,
    validate_known_policy_contract,
)
from chemworld.eval.policy_validity_contract import profile_contract_sha256

ROOT = Path(__file__).resolve().parents[1]
MACHINE = ROOT / "configs/benchmark/work_i_known_policy_contract_v0.1.json"
HUMAN = ROOT / "workstreams/arxiv_v1/reports/work-i-known-policy-contract-v0.1.md"


def test_frozen_artifacts_rebuild_exactly() -> None:
    artifact = build_artifact()
    assert json.loads(MACHINE.read_text(encoding="utf-8")) == artifact
    assert HUMAN.read_text(encoding="utf-8") == build_markdown(artifact)
    assert artifact["contract_sha256"] == known_policy_contract_sha256(
        build_known_policy_contract()
    )
    assert artifact["depends_on"]["profile_contract_sha256"] == (
        profile_contract_sha256()
    )


def test_matrix_and_policy_identity_are_frozen_before_execution() -> None:
    contract = build_known_policy_contract()
    matrix = contract["formal_matrix"]
    assert matrix["world_seeds"] == list(FORMAL_WORLD_SEEDS)
    assert matrix["information_arms"] == list(INFORMATION_ARMS)
    assert matrix["policy_ids"] == list(POLICY_IDS)
    assert matrix["lifecycles_per_cell"] == LIFECYCLES_PER_CELL
    assert matrix["campaign_count"] == 30
    assert matrix["closed_lifecycle_count"] == 180
    assert matrix["provider_call_count"] == 0


def test_shared_probe_schedule_is_safe_and_resource_bounded() -> None:
    contract = build_known_policy_contract()
    schedule = contract["probe_schedule"]
    assert len(PROBE_SCHEDULE) == LIFECYCLES_PER_CELL
    assert schedule["campaign_stock_envelope"] == {
        "solvent_L": 0.15,
        "reagent_mol_for_full_prefix": 0.09,
    }
    assert {probe.solvent for probe in PROBE_SCHEDULE} == {0, 1, 2, 3}
    assert {probe.electrolyte_profile for probe in PROBE_SCHEDULE} == {0, 1, 2, 3}
    assert all(0.65 <= probe.potential_V <= 1.25 for probe in PROBE_SCHEDULE)
    assert all(15.0 <= probe.current_mA <= 90.0 for probe in PROBE_SCHEDULE)


def test_expected_signatures_encode_decision_structure_not_endpoint_rank() -> None:
    signatures = build_known_policy_contract()["expected_profile_signatures"]
    exact = signatures["exact_by_policy"]
    assert exact["assay_all"]["assay_fraction"] == 1.0
    assert exact["start_then_discard"]["discard_fraction"] == 1.0
    assert exact["measure_then_threshold"]["measured_lifecycle_fraction"] == 1.0
    assert exact["measure_then_threshold"]["threshold_decision_concordance"] == 1.0
    assert signatures["threshold_policy_algebra"] == {
        "symbol": (
            "p = assayed threshold-policy lifecycles / closed threshold-policy lifecycles"
        ),
        "domain_after_formal_non_degeneracy_gate": "0 < p < 1",
        "assay_fraction": "p",
        "discard_fraction": "1 - p",
        "continued_after_measurement_fraction": "p",
        "post_measure_process_operations_per_closed_lifecycle": "p",
        "mean_first_measurement_operation_fraction": "2/3 - p/6",
        "attempted_operations_per_closed_lifecycle": "6 + 2p",
        "committed_operations_per_closed_lifecycle": "6 + 2p",
    }
    assert "mean_assayed_score" in signatures["explicit_non_orderings"]
    assert "best_assayed_score" in signatures["explicit_non_orderings"]


def test_threshold_value_is_firewalled_from_formal_worlds() -> None:
    threshold = build_known_policy_contract()["threshold_qualification"]
    assert threshold["status_after_v02"] == "unbound_until_W1-V03"
    assert threshold["diagnostic_signal"] == "observation.conversion"
    assert threshold["comparator"] == ">="
    assert threshold["forbidden_data"] == "formal world seeds 0, 1, 2, 3, 4"
    encoded = json.dumps(threshold, sort_keys=True)
    assert "qualified_threshold" not in encoded
    assert "threshold_value" not in encoded


def test_validator_accepts_frozen_contract_and_rejects_semantic_drift() -> None:
    contract = build_known_policy_contract()
    assert validate_known_policy_contract(contract) == []

    drifted = deepcopy(contract)
    drifted["formal_matrix"]["provider_call_count"] = 1
    drifted["probe_schedule"]["cards"][0]["potential_V"] = 2.0
    drifted["policies"][1]["reads_material_information"] = True
    drifted["threshold_qualification"]["status_after_v02"] = "bound"
    errors = validate_known_policy_contract(drifted)
    assert "known policies must make zero provider calls" in errors
    assert "probe-01.potential_V is outside bounds" in errors
    assert "start_then_discard must ignore material information" in errors
    assert "V02 must not bind a threshold value" in errors
