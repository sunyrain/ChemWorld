from __future__ import annotations

from copy import deepcopy

import pytest

from chemworld.eval.work_ii_b2_identifiability import (
    audit_b2_participant_visible_identifiability,
)


def _fixture() -> tuple[dict, list[dict], dict]:
    cells = []
    results = []
    for world_seed in range(5):
        evidence = [
            {
                "query_id": f"e{index}",
                "feature_values": {"solvent": 0, "extractant": 1},
                "observations": {
                    "product_in_organic": 0.80 + index * 0.001,
                    "product_in_aqueous": 0.01,
                    "phase_ratio": 0.99,
                },
            }
            for index in range(8)
        ]
        scoring_queries = [
            {
                "query_id": f"s{index}",
                "feature_values": {"solvent": 0, "extractant": 1},
                "metric_ids": [
                    "product_in_organic",
                    "product_in_aqueous",
                    "phase_ratio",
                ],
            }
            for index in range(8)
        ]
        scoring_truth = {
            f"s{index}": {
                "product_in_organic": 0.81,
                "product_in_aqueous": 0.01,
                "phase_ratio": 0.99,
            }
            for index in range(8)
        }
        for arm in ("opaque", "aligned_nominal", "misindexed_nominal"):
            cell_id = f"world-{world_seed}--{arm}"
            cells.append(
                {
                    "cell_id": cell_id,
                    "cluster_id": f"world-{world_seed}",
                    "world_seed": world_seed,
                    "arm": arm,
                    "public_packet": {
                        "evidence": deepcopy(evidence),
                        "scoring_queries": deepcopy(scoring_queries),
                    },
                    "scoring_truth": deepcopy(scoring_truth),
                }
            )
            results.append(
                {
                    "cell_id": cell_id,
                    "status": "completed",
                    "scores": {"post": {"mean_normalized_absolute_error": 0.01}},
                }
            )
    analysis = {
        "public_summary_audit": {
            "by_arm": {
                "aligned_nominal": {
                    "world_count": 5,
                    "exact_1_75_power_law_recovery_count": 1,
                    "power_compatible_language_count": 3,
                }
            }
        }
    }
    return {"study_id": "fixture", "cells": cells}, results, analysis


def test_b2_identifiability_detects_exact_fixed_pair_alias() -> None:
    manifest, results, analysis = _fixture()
    audit = audit_b2_participant_visible_identifiability(manifest, results, analysis)
    assert audit["exact_alias"]["present"] is True
    assert audit["participant_visible_design"]["nominal_pair_count"] == 1
    assert audit["decision"]["structural_family_identification_supported"] is False
    assert audit["positive_control"]["readout_positive_control_passed"] is False
    assert audit["empirical_alternative"]["mean_scoring_error"] < 0.01


def test_b2_identifiability_rejects_unexpected_pair_variation() -> None:
    manifest, results, analysis = _fixture()
    manifest["cells"][0]["public_packet"]["evidence"][0]["feature_values"][
        "extractant"
    ] = 2
    with pytest.raises(ValueError, match="unexpectedly varies"):
        audit_b2_participant_visible_identifiability(manifest, results, analysis)

