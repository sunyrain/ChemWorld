from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

from chemworld.eval.work_ii_evidence_to_action import (
    CANDIDATE_REVEAL_GATES,
    CONDITIONS,
    DONOR_CONDITION,
    DONOR_DERIVED_CONDITIONS,
    analyze_terminal_results,
    build_design_manifest,
    build_disjoint_oracle_grid,
    build_hybrid_disjoint_oracle_grid,
    build_learned_law_artifact,
    build_oracle_law_artifact,
    build_yoked_evidence_packet,
    evaluate_candidate_packet,
    evaluate_law_action_agreement,
    evaluate_oracle_law_candidate_order,
    fit_candidate_calibrated_oracle_law_from_disjoint_grid,
    fit_candidate_domain_distilled_oracle_law_from_disjoint_grid,
    fit_extra_trees_candidate_domain_distilled_oracle_law_from_disjoint_grid,
    fit_oracle_law_from_disjoint_grid,
    predict_candidate_ranking_from_law,
    score_terminal_ranking,
    split_registered_query_pool,
    split_registered_query_pool_maximin,
    validate_protocol,
)

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "configs/benchmark/work_ii_evidence_to_action_causal_decomposition_v0.1.json"
PROTOCOL_V2 = ROOT / "configs/benchmark/work_ii_evidence_to_action_causal_decomposition_v0.2.json"
PROTOCOL_V3 = ROOT / "configs/benchmark/work_ii_evidence_to_action_causal_decomposition_v0.3.json"
PROTOCOL_V4 = ROOT / "configs/benchmark/work_ii_evidence_to_action_causal_decomposition_v0.4.json"


def _protocol() -> dict:
    return json.loads(PROTOCOL.read_text(encoding="utf-8"))


def test_protocol_is_provider_unauthorized_and_self_consistent() -> None:
    protocol = _protocol()
    assert validate_protocol(protocol) == []
    assert protocol["execution"]["provider_execution_authorized"] is False
    assert set(protocol["qualification_world_seeds"]).isdisjoint(protocol["formal_world_seeds"])


def test_oracle_v2_protocol_is_fresh_provider_unauthorized_and_self_consistent() -> None:
    protocol = json.loads(PROTOCOL_V2.read_text(encoding="utf-8"))
    assert validate_protocol(protocol) == []
    assert protocol["execution"]["provider_execution_authorized"] is False
    assert set(protocol["qualification_world_seeds"]).isdisjoint(protocol["formal_world_seeds"])
    assert set(protocol["qualification_world_seeds"]).isdisjoint(
        _protocol()["qualification_world_seeds"] + _protocol()["formal_world_seeds"]
    )


def test_oracle_v3_protocol_is_fresh_provider_unauthorized_and_self_consistent() -> None:
    protocol = json.loads(PROTOCOL_V3.read_text(encoding="utf-8"))
    v2 = json.loads(PROTOCOL_V2.read_text(encoding="utf-8"))
    assert validate_protocol(protocol) == []
    assert protocol["execution"]["provider_execution_authorized"] is False
    assert set(protocol["qualification_world_seeds"]).isdisjoint(protocol["formal_world_seeds"])
    assert set(protocol["qualification_world_seeds"] + protocol["formal_world_seeds"]).isdisjoint(
        v2["qualification_world_seeds"] + v2["formal_world_seeds"]
    )


def test_oracle_v4_protocol_is_fresh_provider_unauthorized_and_self_consistent() -> None:
    protocol = json.loads(PROTOCOL_V4.read_text(encoding="utf-8"))
    v3 = json.loads(PROTOCOL_V3.read_text(encoding="utf-8"))
    assert validate_protocol(protocol) == []
    assert protocol["execution"]["provider_execution_authorized"] is False
    assert set(protocol["qualification_world_seeds"]).isdisjoint(protocol["formal_world_seeds"])
    assert set(protocol["qualification_world_seeds"] + protocol["formal_world_seeds"]).isdisjoint(
        v3["qualification_world_seeds"] + v3["formal_world_seeds"]
    )


def test_design_compiles_exact_five_condition_denominator() -> None:
    manifest = build_design_manifest(_protocol())
    assert manifest["task_world_cluster_count"] == 15
    assert manifest["task_world_prior_stratum_count"] == 45
    assert manifest["scheduled_session_count"] == 225
    assert manifest["autonomous_session_count"] == 45
    assert manifest["donor_dependent_session_count"] == 90
    assert manifest["participant_physical_experiment_count"] == 540
    assert tuple(manifest["conditions"]) == CONDITIONS
    assert manifest["analysis"]["independent_inference_cluster"] == "task_world"
    assert manifest["analysis"]["independent_cluster_count"] == 15


def test_each_stratum_has_one_donor_and_two_bound_descendants() -> None:
    manifest = build_design_manifest(_protocol())
    cells = {row["cell_id"]: row for row in manifest["cells"]}
    for stratum in manifest["strata"]:
        donor_id = stratum["donor_cell_id"]
        donor = cells[donor_id]
        assert donor["condition"] == DONOR_CONDITION
        assert donor["physical_experiment_count"] == 12
        for cell_id in stratum["cell_ids"]:
            cell = cells[cell_id]
            if cell["condition"] in DONOR_DERIVED_CONDITIONS:
                assert cell["dependency_cell_ids"] == [donor_id]
                assert cell["missing_dependency_status"] == ("not_started_due_to_missing_donor")
            else:
                assert cell["dependency_cell_ids"] == []


def test_candidate_disclosure_is_terminal_only_in_every_condition() -> None:
    manifest = build_design_manifest(_protocol())
    for cell in manifest["cells"]:
        assert cell["candidate_reveal_gate"] == CANDIDATE_REVEAL_GATES[cell["condition"]]
        assert cell["candidate_outcomes_hidden"] is True
        assert cell["checkpoint_stages"][-1] == "terminal_ranking"
        if cell["condition"] == "no_evidence":
            assert cell["checkpoint_stages"] == ["terminal_ranking"]


def test_tampered_donor_dependency_is_rejected() -> None:
    protocol = deepcopy(_protocol())
    protocol["conditions"]["learned_law_only"]["donor_dependency"] = False
    assert any(
        "learned_law_only: donor dependency is invalid" in error
        for error in validate_protocol(protocol)
    )


def test_tampered_oracle_grid_contract_is_rejected() -> None:
    protocol = deepcopy(_protocol())
    protocol["oracle_grid_contract"]["selection_reads_truth"] = True
    assert "oracle grid construction may not read truth" in validate_protocol(protocol)


def test_candidate_packet_qualification_uses_spread_not_top1_gap() -> None:
    truth = {
        f"q{index}": {"score": score}
        for index, score in enumerate((0.80, 0.7999, 0.70, 0.60, 0.50, 0.40, 0.30, 0.20))
    }
    result = evaluate_candidate_packet(truth, _protocol()["candidate_contract"])
    assert result["status"] == "passed"
    assert result["top1_gap"] < 0.001
    assert result["top1_gap_qualified"] is False


def test_flat_candidate_packet_is_rejected_before_provider() -> None:
    truth = {f"q{index}": {"score": 0.50 + index * 0.001} for index in range(8)}
    result = evaluate_candidate_packet(truth, _protocol()["candidate_contract"])
    assert result["status"] == "failed"
    assert any("raw score range" in error for error in result["errors"])


def test_registered_query_split_is_balanced_fixed_and_seed_free() -> None:
    rows = [
        {"query_id": f"q{index:02d}", "feature_values": {"group": index // 8}}
        for index in range(16)
    ]
    candidates, checkpoints = split_registered_query_pool(rows)
    assert [row["query_id"] for row in candidates] == [f"q{index:02d}" for index in range(0, 16, 2)]
    assert [row["query_id"] for row in checkpoints] == [
        f"q{index:02d}" for index in range(1, 16, 2)
    ]
    assert {row["feature_values"]["group"] for row in candidates} == {0, 1}
    assert {row["feature_values"]["group"] for row in checkpoints} == {0, 1}


def test_maximin_query_split_covers_public_feature_extremes_without_truth() -> None:
    rows = [
        {
            "query_id": f"q{index:02d}",
            "feature_values": {
                "temperature": float(index),
                "group": 0 if index < 8 else 1,
            },
        }
        for index in range(16)
    ]
    candidates, checkpoints = split_registered_query_pool_maximin(
        rows,
        allowed_feature_ids=["temperature", "group"],
    )
    candidate_ids = {row["query_id"] for row in candidates}
    assert len(candidates) == len(checkpoints) == 8
    assert {"q00", "q15"}.issubset(candidate_ids)
    assert {row["feature_values"]["group"] for row in candidates} == {0, 1}
    assert all("truth" not in row for row in candidates)


def test_yoked_packet_contains_scientific_evidence_but_not_private_state() -> None:
    rows = []
    for experiment in range(1, 13):
        rows.extend(
            [
                {
                    "action": {"operation": "heat", "temperature_K": 300 + experiment},
                    "agent_visible_observation": {
                        "observation": {"score": 0.0, "yield": None},
                        "observed_reward": 0.0,
                    },
                    "observed_keys": ["score"],
                    "transaction_status": "committed",
                    "agent_trace": "must not transfer",
                    "campaign_resource_card_sha256": "must-not-transfer",
                },
                {
                    "action": {"operation": "measure", "instrument": "final_assay"},
                    "agent_visible_observation": {
                        "observation": {"score": experiment / 12, "yield": 0.5},
                        "observed_reward": experiment / 12,
                    },
                    "observed_keys": ["score", "yield"],
                    "transaction_status": "committed",
                    "candidate_truth": "must not transfer",
                },
            ]
        )
    packet = build_yoked_evidence_packet(rows, donor_cell_id="donor-1")
    assert packet["complete_experiment_count"] == 12
    assert [row["after_complete_experiment"] for row in packet["checkpoint_rounds"]] == list(
        range(1, 13)
    )
    assert [
        row["after_complete_experiment"]
        for row in packet["checkpoint_rounds"]
        if row["belief_snapshot_due"]
    ] == [3, 6, 9, 12]
    rendered = json.dumps(packet)
    assert "agent_trace" not in rendered
    assert "candidate_truth" not in rendered
    assert "campaign_resource_card_sha256" not in rendered
    assert "must-not-transfer" not in rendered
    assert "temperature_K" in rendered


def test_learned_law_artifact_excludes_other_donor_state() -> None:
    summary = {
        "analysis": {
            "belief_snapshots": [
                {"stage": "pre_evidence", "law_summary": {"summary_id": "pre"}},
                {
                    "stage": "final",
                    "law_summary": {
                        "schema_version": "chemworld-work-ii-law-summary-0.1",
                        "summary_id": "final-law",
                        "metric_laws": [],
                    },
                    "predictions": [{"query_id": "checkpoint-q1"}],
                },
            ],
            "experiments": [{"secret": "not transferred"}],
        }
    }
    artifact = build_learned_law_artifact(summary, donor_cell_id="donor-1")
    assert artifact["law_summary"]["summary_id"] == "final-law"
    rendered = json.dumps(artifact)
    assert "checkpoint-q1" not in rendered
    assert "not transferred" not in rendered


def _linear_oracle_law() -> dict:
    return {
        "schema_version": "chemworld-work-ii-law-summary-0.1",
        "summary_id": "disjoint-grid-linear-oracle",
        "feature_ids": ["x"],
        "metric_laws": [
            {
                "metric_id": "score",
                "intercept": 0.0,
                "link": "identity",
                "lower_bound": -10.0,
                "upper_bound": 10.0,
                "terms": [
                    {
                        "term_id": "x-linear",
                        "basis": "linear",
                        "input_ids": ["x"],
                        "coefficient": 1.0,
                    }
                ],
            }
        ],
        "evidence_ids": ["fit-q1", "fit-q2"],
        "applicability": "registered candidate domain",
        "limitations": [],
        "confidence": 1.0,
    }


def test_oracle_artifact_requires_fit_candidate_disjointness() -> None:
    artifact = build_oracle_law_artifact(
        _linear_oracle_law(),
        fit_query_ids=["fit-q1", "fit-q2"],
        candidate_query_ids=["candidate-q1", "candidate-q2"],
        fitted_from_candidate_outcomes=False,
    )
    assert artifact["fit_used_candidate_outcomes"] is False
    assert artifact["candidate_information_included"] is False

    try:
        build_oracle_law_artifact(
            _linear_oracle_law(),
            fit_query_ids=["candidate-q1"],
            candidate_query_ids=["candidate-q1", "candidate-q2"],
            fitted_from_candidate_outcomes=False,
        )
    except ValueError as exc:
        assert "overlaps" in str(exc)
    else:  # pragma: no cover - defensive assertion
        raise AssertionError("overlapping oracle fit and candidate packets must be rejected")


def test_oracle_candidate_order_qualification_is_explicit() -> None:
    queries = [
        {"query_id": f"candidate-q{index}", "feature_values": {"x": float(index)}}
        for index in range(8)
    ]
    truth = {f"candidate-q{index}": {"score": float(index) * 0.1} for index in range(8)}
    artifact = build_oracle_law_artifact(
        _linear_oracle_law(),
        fit_query_ids=["fit-q1", "fit-q2"],
        candidate_query_ids=list(truth),
        fitted_from_candidate_outcomes=False,
    )
    result = evaluate_oracle_law_candidate_order(
        artifact,
        candidate_queries=queries,
        candidate_truth=truth,
        allowed_feature_ids=["x"],
        allowed_metric_ids=["score"],
        minimum_rank_correlation=0.80,
    )
    assert result["status"] == "passed"
    assert result["spearman_rank_correlation"] == 1.0
    assert result["top1_agreement"] is True


def test_oracle_fitter_uses_only_disjoint_registered_grid() -> None:
    fit_queries = [
        {"query_id": f"fit-q{index}", "feature_values": {"x": float(index)}} for index in range(8)
    ]
    fit_truth = {f"fit-q{index}": {"score": (float(index) / 10.0) ** 2} for index in range(8)}
    artifact = fit_oracle_law_from_disjoint_grid(
        fit_queries,
        fit_truth,
        candidate_query_ids=[f"candidate-q{index}" for index in range(8)],
        allowed_feature_ids=["x"],
        allowed_metric_ids=["score"],
        summary_id="quadratic-oracle",
    )
    assert artifact["fit_query_ids"] == [f"fit-q{index}" for index in range(8)]
    assert artifact["fit_used_candidate_outcomes"] is False
    assert artifact["law_summary"]["metric_laws"][0]["metric_id"] == "score"


def test_candidate_calibrated_oracle_is_typed_deterministic_and_outcome_blind() -> None:
    fit_queries = [
        {
            "query_id": f"fit-q{index:03d}",
            "feature_values": {"catalyst": index % 2, "x": (index + 0.25) / 96.0},
        }
        for index in range(96)
    ]
    fit_truth = {
        row["query_id"]: {
            "score": 0.2
            + 0.6 * row["feature_values"]["x"]
            + 0.05 * row["feature_values"]["catalyst"]
        }
        for row in fit_queries
    }
    candidates = [
        {
            "query_id": f"candidate-q{index}",
            "feature_values": {"catalyst": index % 2, "x": (index + 1) / 9.0},
        }
        for index in range(8)
    ]
    kwargs = {
        "candidate_queries": candidates,
        "allowed_feature_ids": ["catalyst", "x"],
        "allowed_metric_ids": ["score"],
        "summary_id": "candidate-calibrated-oracle",
        "neighbor_count": 4,
        "candidate_calibration_weight": 16.0,
    }
    first = fit_candidate_calibrated_oracle_law_from_disjoint_grid(fit_queries, fit_truth, **kwargs)
    second = fit_candidate_calibrated_oracle_law_from_disjoint_grid(
        fit_queries, fit_truth, **kwargs
    )
    assert first == second
    assert first["fit_used_candidate_outcomes"] is False
    assert first["candidate_outcomes_used"] is False
    assert first["candidate_feature_locations_used"] is True
    assert first["calibration_contract"]["neighbor_count"] == 4
    assert all(
        candidate["query_id"] not in json.dumps(first["law_summary"], sort_keys=True)
        for candidate in candidates
    )
    candidate_truth = {
        row["query_id"]: {
            "score": 0.2
            + 0.6 * row["feature_values"]["x"]
            + 0.05 * row["feature_values"]["catalyst"]
        }
        for row in candidates
    }
    qualification = evaluate_oracle_law_candidate_order(
        first,
        candidate_queries=candidates,
        candidate_truth=candidate_truth,
        allowed_feature_ids=["catalyst", "x"],
        allowed_metric_ids=["score"],
        minimum_rank_correlation=0.8,
    )
    assert qualification["status"] == "passed"


def test_candidate_domain_oracle_exactly_distills_outcome_blind_local_predictions() -> None:
    fit_queries = [
        {
            "query_id": f"fit-q{index:03d}",
            "feature_values": {"catalyst": index % 2, "x": (index + 0.25) / 96.0},
        }
        for index in range(96)
    ]
    fit_truth = {
        row["query_id"]: {
            "score": 0.2
            + 0.6 * row["feature_values"]["x"]
            + 0.05 * row["feature_values"]["catalyst"]
        }
        for row in fit_queries
    }
    candidates = [
        {
            "query_id": f"candidate-q{index}",
            "feature_values": {"catalyst": index % 2, "x": (index + 1) / 9.0},
        }
        for index in range(8)
    ]
    kwargs = {
        "candidate_queries": candidates,
        "allowed_feature_ids": ["catalyst", "x"],
        "allowed_metric_ids": ["score"],
        "summary_id": "candidate-domain-oracle",
        "neighbor_count": 4,
        "distillation_tolerance": 1.0e-9,
    }
    first = fit_candidate_domain_distilled_oracle_law_from_disjoint_grid(
        fit_queries, fit_truth, **kwargs
    )
    second = fit_candidate_domain_distilled_oracle_law_from_disjoint_grid(
        fit_queries, fit_truth, **kwargs
    )
    assert first == second
    assert first["fit_used_candidate_outcomes"] is False
    assert first["candidate_outcomes_used"] is False
    assert first["candidate_feature_locations_used"] is True
    assert first["calibration_contract"]["candidate_design_rank"] == 8
    assert first["calibration_contract"]["maximum_absolute_error"] <= 1.0e-9
    assert all(
        candidate["query_id"] not in json.dumps(first["law_summary"], sort_keys=True)
        for candidate in candidates
    )
    candidate_truth = {
        row["query_id"]: {
            "score": 0.2
            + 0.6 * row["feature_values"]["x"]
            + 0.05 * row["feature_values"]["catalyst"]
        }
        for row in candidates
    }
    qualification = evaluate_oracle_law_candidate_order(
        first,
        candidate_queries=candidates,
        candidate_truth=candidate_truth,
        allowed_feature_ids=["catalyst", "x"],
        allowed_metric_ids=["score"],
        minimum_rank_correlation=0.8,
    )
    assert qualification["status"] == "passed"


def test_extra_trees_candidate_domain_oracle_is_deterministic_and_outcome_blind() -> None:
    fit_queries = [
        {
            "query_id": f"fit-q{index:03d}",
            "feature_values": {"catalyst": index % 2, "x": (index + 0.25) / 320.0},
        }
        for index in range(320)
    ]
    fit_truth = {
        row["query_id"]: {
            "score": 0.2
            + 0.6 * row["feature_values"]["x"]
            + 0.05 * row["feature_values"]["catalyst"]
        }
        for row in fit_queries
    }
    candidates = [
        {
            "query_id": f"candidate-q{index}",
            "feature_values": {"catalyst": index % 2, "x": (index + 1) / 9.0},
        }
        for index in range(8)
    ]
    kwargs = {
        "candidate_queries": candidates,
        "allowed_feature_ids": ["catalyst", "x"],
        "allowed_metric_ids": ["score"],
        "summary_id": "extra-trees-candidate-domain-oracle",
        "tree_count": 64,
        "min_samples_leaf": 1,
        "random_seed": 20260824,
        "distillation_tolerance": 1.0e-9,
    }
    first = fit_extra_trees_candidate_domain_distilled_oracle_law_from_disjoint_grid(
        fit_queries, fit_truth, **kwargs
    )
    second = fit_extra_trees_candidate_domain_distilled_oracle_law_from_disjoint_grid(
        fit_queries, fit_truth, **kwargs
    )
    assert first == second
    assert first["fit_used_candidate_outcomes"] is False
    assert first["candidate_outcomes_used"] is False
    assert len(first["fit_query_ids"]) == 320
    assert len(first["law_summary"]["evidence_ids"]) == 128
    assert set(first["law_summary"]["evidence_ids"]).issubset(first["fit_query_ids"])
    assert first["calibration_contract"]["tree_count"] == 64
    assert first["calibration_contract"]["candidate_design_rank"] == 8
    assert first["calibration_contract"]["maximum_absolute_error"] <= 1.0e-9
    assert all(
        candidate["query_id"] not in json.dumps(first["law_summary"], sort_keys=True)
        for candidate in candidates
    )
    candidate_truth = {
        row["query_id"]: {
            "score": 0.2
            + 0.6 * row["feature_values"]["x"]
            + 0.05 * row["feature_values"]["catalyst"]
        }
        for row in candidates
    }
    qualification = evaluate_oracle_law_candidate_order(
        first,
        candidate_queries=candidates,
        candidate_truth=candidate_truth,
        allowed_feature_ids=["catalyst", "x"],
        allowed_metric_ids=["score"],
        minimum_rank_correlation=0.8,
    )
    assert qualification["evaluated_candidate_count"] == 8
    assert not any("invalid oracle typed law" in error for error in qualification["errors"])


def test_dense_oracle_grid_is_truth_blind_deterministic_and_feature_disjoint() -> None:
    registered = [
        {
            "query_id": f"registered-q{index:02d}",
            "feature_values": {
                "temperature": 300.0 + 10.0 * index,
                "catalyst": index % 4,
                "fixed_amount": 0.01,
            },
        }
        for index in range(16)
    ]
    kwargs = {
        "allowed_feature_ids": ["catalyst", "temperature", "fixed_amount"],
        "allowed_metric_ids": ["yield", "score"],
        "candidate_query_ids": [f"registered-q{index:02d}" for index in range(0, 16, 2)],
        "query_count": 96,
        "grid_id": "oracle-grid-test",
    }
    first = build_disjoint_oracle_grid(registered, **kwargs)
    second = build_disjoint_oracle_grid(registered, **kwargs)
    assert first == second
    assert len(first) == 96
    assert len({row["query_id"] for row in first}) == 96
    candidate_features = {
        json.dumps(registered[index]["feature_values"], sort_keys=True) for index in range(0, 16, 2)
    }
    assert not candidate_features & {
        json.dumps(row["feature_values"], sort_keys=True) for row in first
    }
    assert {row["feature_values"]["catalyst"] for row in first} == {0, 1, 2, 3}
    assert all("truth" not in row for row in first)


def test_hybrid_oracle_grid_has_fixed_global_and_candidate_neighborhood_coverage() -> None:
    registered = [
        {
            "query_id": f"registered-q{index:02d}",
            "feature_values": {
                "temperature": 300.0 + 10.0 * index,
                "catalyst": index % 4,
            },
        }
        for index in range(16)
    ]
    candidate_ids = [f"registered-q{index:02d}" for index in range(0, 16, 2)]
    grid = build_hybrid_disjoint_oracle_grid(
        registered,
        allowed_feature_ids=["catalyst", "temperature"],
        allowed_metric_ids=["score"],
        candidate_query_ids=candidate_ids,
        global_query_count=32,
        neighborhood_query_count=64,
        neighborhood_span_fraction=0.18,
        grid_id="hybrid-test",
    )
    assert len(grid) == 96
    assert sum(row["grid_component"] == "global" for row in grid) == 32
    assert sum(row["grid_component"] == "candidate_neighborhood" for row in grid) == 64
    candidate_features = {
        json.dumps(registered[index]["feature_values"], sort_keys=True) for index in range(0, 16, 2)
    }
    assert not candidate_features & {
        json.dumps(row["feature_values"], sort_keys=True) for row in grid
    }
    assert all("truth" not in row for row in grid)


def test_oracle_fitter_emits_executable_conditional_cubic_terms() -> None:
    fit_queries = [
        {
            "query_id": f"fit-q{index:03d}",
            "feature_values": {"catalyst": index % 2, "x": index / 95.0},
        }
        for index in range(96)
    ]
    fit_truth = {
        row["query_id"]: {
            "score": (
                row["feature_values"]["x"] ** 3
                + row["feature_values"]["catalyst"] * row["feature_values"]["x"] ** 2
            )
        }
        for row in fit_queries
    }
    artifact = fit_oracle_law_from_disjoint_grid(
        fit_queries,
        fit_truth,
        candidate_query_ids=[f"candidate-q{index}" for index in range(8)],
        allowed_feature_ids=["catalyst", "x"],
        allowed_metric_ids=["score"],
        summary_id="conditional-cubic-oracle",
    )
    bases = {term["basis"] for term in artifact["law_summary"]["metric_laws"][0]["terms"]}
    assert "cubic" in bases
    assert "conditional_quadratic" in bases


def test_dense_96_point_oracle_law_remains_executable() -> None:
    fit_queries = [
        {"query_id": f"fit-q{index:03d}", "feature_values": {"x": index / 95.0}}
        for index in range(96)
    ]
    fit_truth = {row["query_id"]: {"score": row["feature_values"]["x"] ** 2} for row in fit_queries}
    candidates = [
        {"query_id": f"candidate-q{index}", "feature_values": {"x": index / 7.0}}
        for index in range(8)
    ]
    candidate_truth = {
        row["query_id"]: {"score": row["feature_values"]["x"] ** 2} for row in candidates
    }
    artifact = fit_oracle_law_from_disjoint_grid(
        fit_queries,
        fit_truth,
        candidate_query_ids=list(candidate_truth),
        allowed_feature_ids=["x"],
        allowed_metric_ids=["score"],
        summary_id="dense-quadratic-oracle",
    )
    qualification = evaluate_oracle_law_candidate_order(
        artifact,
        candidate_queries=candidates,
        candidate_truth=candidate_truth,
        allowed_feature_ids=["x"],
        allowed_metric_ids=["score"],
        minimum_rank_correlation=0.8,
    )
    assert qualification["status"] == "passed"
    assert qualification["spearman_rank_correlation"] == 1.0


def test_terminal_ranking_uses_continuous_regret_and_tie_aware_agreement() -> None:
    truth = {
        f"q{index}": {"score": score}
        for index, score in enumerate((0.90, 0.895, 0.80, 0.70, 0.60, 0.50, 0.40, 0.30))
    }
    ranking = ["q1", "q0", "q2", "q3", "q4", "q5", "q6", "q7"]
    result = score_terminal_ranking(ranking, truth)
    assert result["top1"] == 0
    assert result["within_0_01_of_best"] == 1
    assert result["raw_regret"] < 0.01
    assert result["pairwise_ranking_agreement_excluding_truth_gaps_below_0_01"] == 1.0


def test_missing_terminal_ranking_receives_failure_aware_worst_case() -> None:
    truth = {f"q{index}": {"score": 1.0 - index * 0.1} for index in range(8)}
    result = score_terminal_ranking(None, truth)
    assert result["status"] == "failed_missing_terminal_ranking"
    assert result["top1"] == 0
    assert result["selected_rank"] is None
    assert result["failure_aware_normalized_regret"] == 1.0


def test_terminal_analysis_pairs_priors_and_retains_missing_sessions() -> None:
    manifest = build_design_manifest(_protocol())
    truth = {f"q{index}": {"score": 1.0 - index * 0.1} for index in range(8)}
    truth_by_cluster = {cluster["cluster_id"]: truth for cluster in manifest["clusters"]}
    results = {}
    for cell in manifest["cells"]:
        ranking = [f"q{index}" for index in range(8)]
        if cell["condition"] in {"no_evidence", "learned_law_only"}:
            ranking[0], ranking[1] = ranking[1], ranking[0]
        results[cell["cell_id"]] = {
            "status": "completed",
            "submission": {"ranking": ranking},
        }
    missing_id = manifest["cells"][0]["cell_id"]
    del results[missing_id]
    analysis = analyze_terminal_results(
        manifest,
        results,
        candidate_truth_by_cluster=truth_by_cluster,
    )
    assert analysis["scheduled_session_count"] == 225
    assert analysis["received_result_count"] == 224
    assert analysis["missing_or_unranked_session_count"] == 1
    assert len(analysis["paired_rows"]) == 45 * 6
    assert all(row["independent_cluster_count"] == 15 for row in analysis["contrast_summaries"])
    primary = next(
        row
        for row in analysis["contrast_summaries"]
        if row["contrast"] == "autonomous_exploration_minus_no_evidence"
    )
    assert primary["mean_failure_aware_normalized_regret_difference"] < 0.0


def test_law_implied_ranking_is_outcome_blind_and_action_agreement_is_separate() -> None:
    candidates = [
        {"query_id": f"q{index}", "feature_values": {"x": float(index)}} for index in range(8)
    ]
    law = _linear_oracle_law()
    implied = predict_candidate_ranking_from_law(
        law,
        candidate_queries=candidates,
        allowed_feature_ids=["x"],
        allowed_metric_ids=["score"],
        evidence_catalog=["fit-q1", "fit-q2"],
    )
    assert implied["law_implied_ranking"] == [f"q{index}" for index in reversed(range(8))]
    assert implied["candidate_outcomes_used"] is False

    submitted = list(implied["law_implied_ranking"])
    submitted[0], submitted[1] = submitted[1], submitted[0]
    agreement = evaluate_law_action_agreement(
        submitted,
        implied["law_implied_ranking"],
    )
    assert agreement["law_action_complete_ranking_agreement"] == 0
    assert agreement["law_implied_top1_followed"] == 0
    assert agreement["law_action_pairwise_agreement"] < 1.0
