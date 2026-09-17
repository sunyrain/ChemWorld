from __future__ import annotations

from pathlib import Path

from chemworld.eval import work_ii_structural_candidate_qualification as structural
from chemworld.eval.experiment_1_ec_qualification_repair import (
    EXPECTED_ENTITY_PERMUTATIONS,
    _structural_model_qualification_repair,
    analyze_entity_repair_world,
    entity_prior_audit_repair,
    load_repair_contract,
    private_world_audit_repair,
    structural_repair_queries,
)

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "configs/benchmark/experiment_1_ec_qualification_repair_v1.0.2.json"


def _contract() -> dict:
    return load_repair_contract(ROOT, CONTRACT_PATH)


def _receipt(anchor: int, category: int, replicate: int) -> dict:
    value = (0.1, 0.35, 0.6, 0.9)[category] + (-0.002, 0.0, 0.002)[replicate]
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


def test_repair_contract_is_frozen_and_participant_disabled() -> None:
    contract = _contract()

    assert contract["repair_scope"]["world_truth_change"] is False
    assert contract["repair_scope"]["gate_change"] is False
    assert contract["participant_execution_authorized"] is False
    assert contract["execution"]["participant_execution_authorized"] is False


def test_entity_transpositions_are_world_specific_unique_and_symmetric() -> None:
    contract = _contract()
    actual = {
        world_id: tuple(values)
        for world_id, values in contract["loci"]["entity"][
            "descriptor_permutation_by_world"
        ].items()
    }

    assert actual == EXPECTED_ENTITY_PERMUTATIONS
    assert len(set(actual.values())) == 5
    for world_id in actual:
        audit = entity_prior_audit_repair(contract, world_id=world_id)
        assert audit["passed"] is True
        assert audit["aligned_sha256"] != audit["misspecified_sha256"]
        assert audit["leakage_tokens"] == []


def test_private_mapping_remains_closer_for_all_repair_pairs() -> None:
    contract = _contract()
    for index, world_id in enumerate(EXPECTED_ENTITY_PERMUTATIONS):
        audit = private_world_audit_repair(contract, world_id=world_id, world_seed=index)
        assert audit["aligned_mapping_not_reversed"] is True
        assert len(audit["mapping_rows"]) == 2


def test_entity_analysis_uses_each_worlds_frozen_pair() -> None:
    contract = _contract()
    receipts = [
        _receipt(anchor, category, replicate)
        for anchor in range(2)
        for category in range(4)
        for replicate in range(3)
    ]

    report_w01 = analyze_entity_repair_world(
        contract,
        world_id="EC-W01",
        world_seed=0,
        receipts=receipts,
    )
    report_w04 = analyze_entity_repair_world(
        contract,
        world_id="EC-W04",
        world_seed=3,
        receipts=receipts,
    )

    assert report_w01["descriptor_permutation"] == [3, 1, 2, 0]
    assert {
        (row["left_category"], row["right_category"]) for row in report_w01["anchor_results"]
    } == {(0, 3)}
    assert report_w04["descriptor_permutation"] == [0, 1, 3, 2]
    assert {
        (row["left_category"], row["right_category"]) for row in report_w04["anchor_results"]
    } == {(2, 3)}
    assert report_w01["status"] == report_w04["status"] == "qualified"


def test_structural_repair_uses_low_potential_for_all_noisy_validation() -> None:
    queries = structural_repair_queries(_contract())
    main = [row for row in queries if row["phase"] == "main_grid"]
    validation = [row for row in queries if row["phase"] == "noisy_validation"]

    assert len(main) == 9
    assert len(validation) == 9
    assert {row["axis_a_index"] for row in validation} == {0}
    assert {row["axis_b_index"] for row in validation} == {0, 1, 2}
    assert {row["feature_values"]["controlled_potential_V"] for row in validation} == {0.75}
    assert {row["feature_values"]["controlled_current_mA"] for row in validation} == {
        15.0,
        91.0,
        190.0,
    }


def test_structural_repair_baseline_check_does_not_require_validation_center() -> None:
    metrics = (
        "selective_product_yield",
        "faradaic_efficiency",
        "transport_efficiency",
    )

    def values(axis_a: int, axis_b: int) -> dict[str, float]:
        potential = float(axis_a - 1)
        current = float(axis_b - 1)
        return {
            "selective_product_yield": 0.65 + 0.04 * potential - 0.12 * current**2,
            "faradaic_efficiency": 0.70 + 0.03 * potential - 0.10 * current**2,
            "transport_efficiency": 0.68 + 0.02 * potential - 0.09 * current**2,
        }

    main = [
        {"axis_a_index": axis_a, "axis_b_index": axis_b, "metrics": values(axis_a, axis_b)}
        for axis_a in range(3)
        for axis_b in range(3)
    ]
    groups = ((0, 0), (0, 1), (0, 2))
    validation = []
    for group_index, (axis_a, axis_b) in enumerate(groups):
        for replicate, offset in enumerate((-0.001, 0.0, 0.001), start=1):
            validation.append(
                {
                    "validation_group": group_index,
                    "replicate": replicate,
                    "metrics": {
                        metric: value + offset for metric, value in values(axis_a, axis_b).items()
                    },
                }
            )

    result = _structural_model_qualification_repair(
        main,
        validation,
        sigma=dict.fromkeys(metrics, 0.001),
        metrics=metrics,
        aligned_features=structural._electrochemical_aligned_features,
        misspecified_features=structural._electrochemical_misspecified_features,
        validation_groups=groups,
        target_axis="b",
        candidate_id="electrochemical_transport",
        effect_floor=0.03,
        noise_multiplier=6.0,
        minimum_disagreement_fraction=0.4,
    )

    assert result["checks"]["baseline_error_matched"] is True
    assert result["baseline_error_evaluation"] == "direct_prediction_match_at_frozen_center"
    assert result["baseline_error_gap"] == 0.0
    assert result["checks"]["low_counterexample_region"] is True
    assert result["checks"]["high_counterexample_region"] is True
