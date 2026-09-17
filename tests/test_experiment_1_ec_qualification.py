from __future__ import annotations

import json
from pathlib import Path

from chemworld.eval.experiment_1_ec_qualification import (
    EXPECTED_COMMON_GATES,
    analyze_entity_world,
    analyze_parametric_world,
    analyze_structural_world,
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


def test_parametric_adapter_requires_replay_and_maps_all_common_gates() -> None:
    rows = [
        {
            "status": "completed",
            "exact_replay": {"verified": True},
        }
        for _ in range(121)
    ]
    analysis = {
        "checks": {
            "safe_fit_count": True,
            "safe_held_out_count": True,
            "aligned_score_normalized_mae": True,
            "qualified_reflection_exists": True,
        },
        "platform_failure_count": 0,
        "physical_failure_count": 0,
        "prior_matching": {"passed": True},
        "leakage_audit": {"passed": True},
        "blind_identification": {"identified_aligned_law": True},
        "selected_reflection": {
            "blind_error_margin": 0.10,
            "disagreement_fraction": 0.50,
            "checks": {
                "held_out_disagreement": True,
                "blind_identification_margin": True,
                "low_side_falsification_region": True,
                "high_side_falsification_region": True,
                "representatives_separated": True,
            },
        },
    }

    report = analyze_parametric_world(
        _contract(),
        world_id="EC-W01",
        world_seed=0,
        rows=rows,
        analysis=analysis,
        source_truth_sha256="truth",
    )

    assert report["status"] == "qualified"
    assert all(report["gates"].values())
    assert report["denominators"]["exact_replay"] == 121


def test_structural_adapter_maps_thresholded_topology_and_noise_gates() -> None:
    rows = [
        {"status": "completed", "exact_replay": True}
        for _ in range(18)
    ]
    analysis = {
        "checks": {
            "zero_platform_failures": True,
            "main_grid_count": True,
            "complete_main_surface": True,
            "complete_validation_surface": True,
            "axis_b_effect": True,
        },
        "model_qualification": {
            "checks": {
                "prior_schema_matched": True,
                "prior_word_count_matched": True,
                "held_out_disagreement": True,
                "blind_identification": True,
                "low_counterexample_region": True,
                "high_counterexample_region": True,
            }
        },
        "effects": {
            "topology_signature": {
                "passed": True,
                "value": 0.10,
                "sigma_observed": 0.01,
            }
        },
        "prior_arms": {
            "aligned_nominal": {"claim": "Current limitation is measurable."},
            "misindexed_nominal": {"claim": "Current limitation stays approximately stable."},
        },
    }

    report = analyze_structural_world(
        _contract(),
        world_id="EC-W01",
        world_seed=0,
        rows=rows,
        analysis=analysis,
        truth_sha256="truth",
    )

    assert report["status"] == "qualified"
    assert all(report["gates"].values())
    assert report["denominators"]["exact_replay"] == 18
