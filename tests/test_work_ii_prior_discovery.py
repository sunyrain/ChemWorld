from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from chemworld.eval.work_ii_prior_discovery import (
    WORK_II_HELD_OUT_QUERY_SCHEMA_VERSION,
    WORK_II_LAW_SUMMARY_SCHEMA_VERSION,
    WORK_II_SNAPSHOT_SCHEMA_VERSION,
    WORK_II_SNAPSHOT_STAGES,
    parse_work_ii_belief_snapshot,
    parse_work_ii_discovery_schedule,
    parse_work_ii_held_out_query,
    parse_work_ii_law_summary,
    score_work_ii_snapshot_predictions,
    validate_work_ii_snapshot_sequence,
)

FEATURES = ("temperature_K", "catalyst")
METRICS = ("yield", "selectivity")
QUERY_CONTRACT = {
    "held-out-low": METRICS,
    "held-out-high": METRICS,
}
ROOT = Path(__file__).resolve().parents[1]
PLAN_PATH = ROOT / "configs/benchmark/work_ii_prior_discovery_pilot.json"


def _law_summary(*, summary_id: str = "law-pre", evidence_ids: list[str] | None = None) -> dict:
    return {
        "schema_version": WORK_II_LAW_SUMMARY_SCHEMA_VERSION,
        "summary_id": summary_id,
        "feature_ids": list(FEATURES),
        "metric_laws": [
            {
                "metric_id": "yield",
                "intercept": -2.0,
                "link": "logistic",
                "lower_bound": 0.0,
                "upper_bound": 1.0,
                "terms": [
                    {
                        "term_id": "yield-temperature",
                        "basis": "linear",
                        "input_ids": ["temperature_K"],
                        "coefficient": 0.01,
                    },
                    {
                        "term_id": "yield-catalyst-2",
                        "basis": "categorical_level",
                        "input_ids": ["catalyst"],
                        "coefficient": 0.8,
                        "category_value": 2,
                    },
                ],
            },
            {
                "metric_id": "selectivity",
                "intercept": 0.2,
                "link": "identity",
                "lower_bound": 0.0,
                "upper_bound": 1.0,
                "terms": [
                    {
                        "term_id": "selectivity-temperature-square",
                        "basis": "quadratic",
                        "input_ids": ["temperature_K"],
                        "coefficient": 0.000001,
                    },
                    {
                        "term_id": "selectivity-interaction",
                        "basis": "interaction",
                        "input_ids": ["temperature_K", "catalyst"],
                        "coefficient": 0.0001,
                    },
                ],
            },
        ],
        "evidence_ids": evidence_ids or [],
        "applicability": "tested temperature range and the four anonymous catalysts",
        "limitations": ["sparse interaction coverage"],
        "confidence": 0.55,
    }


def _snapshot(
    stage: str,
    *,
    snapshot_id: str | None = None,
    evidence_ids: list[str] | None = None,
    nominal_information_available: bool = True,
) -> dict:
    evidence = evidence_ids or []
    return {
        "schema_version": WORK_II_SNAPSHOT_SCHEMA_VERSION,
        "snapshot_id": snapshot_id or f"snapshot-{stage}",
        "stage": stage,
        "prior_assessment": {
            "nominal_information_available": nominal_information_available,
            "reliability_probability": 0.7 if nominal_information_available else None,
            "suspected_misindexed_fields": [],
            "rationale": "Current evidence is limited, so the nominal mapping remains uncertain.",
        },
        "predictions": [
            {
                "query_id": query_id,
                "metrics": [
                    {
                        "metric_id": metric_id,
                        "mean": 0.5,
                        "interval_lower": 0.2,
                        "interval_upper": 0.8,
                        "confidence": 0.6,
                    }
                    for metric_id in metric_ids
                ],
            }
            for query_id, metric_ids in QUERY_CONTRACT.items()
        ],
        "law_summary": _law_summary(summary_id=f"law-{stage}", evidence_ids=evidence),
        "evidence_ids": evidence,
        "next_experiment_intent": "Run the next frozen diagnostic or autonomous experiment.",
        "overall_confidence": 0.55,
    }


def _parse_snapshot(payload: dict, *, evidence_catalog: tuple[str, ...] = ()):
    return parse_work_ii_belief_snapshot(
        payload,
        expected_stage=payload["stage"],
        query_metric_contract=QUERY_CONTRACT,
        allowed_feature_ids=FEATURES,
        allowed_metric_ids=METRICS,
        allowed_prior_fields=("catalyst",),
        evidence_catalog=evidence_catalog,
        nominal_information_available=payload["prior_assessment"][
            "nominal_information_available"
        ],
    )


def test_executable_law_summary_predicts_all_held_out_metrics() -> None:
    summary = parse_work_ii_law_summary(
        _law_summary(),
        allowed_feature_ids=FEATURES,
        allowed_metric_ids=METRICS,
        evidence_catalog=(),
        required_metric_ids=METRICS,
    )

    prediction = summary.predict({"temperature_K": 350.0, "catalyst": 2})

    assert set(prediction) == set(METRICS)
    assert 0.0 < prediction["yield"] < 1.0
    assert prediction["selectivity"] == pytest.approx(0.3925)
    assert summary.to_dict() == _law_summary()


def test_law_summary_rejects_unknown_evidence_and_unexecutable_terms() -> None:
    unknown_evidence = _law_summary(evidence_ids=["missing"])
    with pytest.raises(ValueError, match="unknown evidence"):
        parse_work_ii_law_summary(
            unknown_evidence,
            allowed_feature_ids=FEATURES,
            allowed_metric_ids=METRICS,
            evidence_catalog=("e1",),
        )

    bad_interaction = _law_summary()
    bad_interaction["metric_laws"][1]["terms"][1]["input_ids"] = ["temperature_K"]
    with pytest.raises(ValueError, match="require 2 input IDs"):
        parse_work_ii_law_summary(
            bad_interaction,
            allowed_feature_ids=FEATURES,
            allowed_metric_ids=METRICS,
            evidence_catalog=(),
        )


def test_held_out_query_binds_exact_public_features_and_metrics() -> None:
    query = parse_work_ii_held_out_query(
        {
            "schema_version": WORK_II_HELD_OUT_QUERY_SCHEMA_VERSION,
            "query_id": "held-out-low",
            "task_id": "reaction-safety-constrained",
            "feature_values": {"temperature_K": 350.0, "catalyst": 2},
            "metric_ids": list(METRICS),
            "replicate_count": 2,
        },
        expected_task_id="reaction-safety-constrained",
        allowed_feature_ids=FEATURES,
        allowed_metric_ids=METRICS,
    )

    assert query.replicate_count == 2
    assert query.feature_values["catalyst"] == 2


def test_belief_snapshot_separates_prior_reliability_prediction_and_law() -> None:
    snapshot = _parse_snapshot(_snapshot("pre_evidence"))

    assert snapshot.stage == "pre_evidence"
    assert snapshot.prior_assessment.reliability_probability == pytest.approx(0.7)
    assert len(snapshot.predictions) == 2
    assert {law.metric_id for law in snapshot.law_summary.metric_laws} == set(METRICS)

    opaque = _parse_snapshot(
        _snapshot("pre_evidence", nominal_information_available=False)
    )
    assert opaque.prior_assessment.reliability_probability is None


def test_snapshot_rejects_query_drift_and_pre_evidence_citations() -> None:
    query_drift = _snapshot("post_neutral", evidence_ids=["e1"])
    query_drift["predictions"][0]["metrics"].pop()
    with pytest.raises(ValueError, match="metrics do not match"):
        _parse_snapshot(query_drift, evidence_catalog=("e1",))

    leaked_evidence = _snapshot("pre_evidence", evidence_ids=["e1"])
    with pytest.raises(ValueError, match="cannot cite experimental evidence"):
        _parse_snapshot(leaked_evidence, evidence_catalog=("e1",))


def test_four_stage_sequence_and_prediction_scoring_are_explicit() -> None:
    snapshots = []
    evidence_catalog: list[str] = []
    for index, stage in enumerate(WORK_II_SNAPSHOT_STAGES):
        if index:
            evidence_catalog.append(f"e{index}")
        snapshots.append(
            _parse_snapshot(
                _snapshot(stage, evidence_ids=list(evidence_catalog)),
                evidence_catalog=tuple(evidence_catalog),
            )
        )
    validate_work_ii_snapshot_sequence(snapshots)

    observed = {
        query_id: {"yield": 0.6, "selectivity": 0.4}
        for query_id in QUERY_CONTRACT
    }
    score = score_work_ii_snapshot_predictions(snapshots[-1], observed)

    assert score["prediction_count"] == 4
    assert score["mean_absolute_error"] == pytest.approx(0.1)
    assert score["interval_coverage"] == pytest.approx(1.0)

    wrong_order = copy.copy(snapshots)
    wrong_order[1], wrong_order[2] = wrong_order[2], wrong_order[1]
    with pytest.raises(ValueError, match="four-stage order"):
        validate_work_ii_snapshot_sequence(wrong_order)


def test_discovery_schedule_exposes_exact_call_attempt_and_physical_denominators() -> None:
    schedule = parse_work_ii_discovery_schedule(
        {
            "snapshot_stages": list(WORK_II_SNAPSHOT_STAGES),
            "neutral_prefix_experiments": 2,
            "discriminating_prefix_experiments": 4,
            "autonomous_suffix_experiments": 4,
            "held_out_query_count": 4,
            "held_out_replicates_per_query": 2,
            "blind_recommendation_replicates": 3,
            "max_provider_attempts_per_decision": 2,
            "executor_guard_margin_operations": 1,
        }
    )

    assert schedule.exploration_experiments == 10
    assert schedule.provider_decisions_per_cell == 8
    assert schedule.provider_attempt_cap_per_cell == 16
    assert schedule.physical_experiments_per_cell == 21
    assert [schedule.phase_for_experiment(index) for index in (1, 2, 3, 6, 7, 10)] == [
        "neutral_prefix",
        "neutral_prefix",
        "discriminating_prefix",
        "discriminating_prefix",
        "autonomous_suffix",
        "autonomous_suffix",
    ]


def test_repository_discovery_plan_keeps_five_tasks_and_a_bounded_small_pilot() -> None:
    plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
    schedule = parse_work_ii_discovery_schedule(plan["discovery_schedule"])

    assert len(plan["task_ids"]) == 5
    assert plan["prior_arms"] == ["opaque", "aligned_nominal", "misindexed_nominal"]
    assert plan["world_seed_policy"]["completion_world_seeds"] == [0, 1, 2, 3, 4]
    assert schedule.exploration_experiments == 5
    assert schedule.provider_decisions_per_cell == 6
    assert schedule.provider_attempt_cap_per_cell == 12
    assert schedule.physical_experiments_per_cell == 16
    assert plan["stages"]["mock-discovery-preflight"]["expected_cells"] == 15
    assert plan["stages"]["real-discovery-probe"]["expected_cells"] == 3
    assert plan["stages"]["one-seed-breadth"]["expected_cells"] == 15
    assert plan["participant"]["mcp_enabled"] is False
    assert "no universal process-time cap" in plan["execution_bounds"]["repeat_rule"]
