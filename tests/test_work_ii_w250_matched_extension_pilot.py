from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from run_work_ii_w250_matched_extension_pilot import (  # noqa: E402
    CONDITION_ORDER,
    DONOR_CELL_ID,
    build_pilot_inputs,
)
from run_work_ii_w250_yoked_schema_repair import (  # noqa: E402
    normalize_nullable_law_terms,
    provider_compatible_yoked_snapshot_schema,
)

from chemworld.eval.work_ii_evidence_to_action_runtime import (  # noqa: E402
    build_recipient_context,
    validate_yoked_snapshot_submission,
)


def test_pilot_reuses_the_first_complete_w250_donor_without_oracle() -> None:
    inputs = build_pilot_inputs()

    assert inputs["donor"]["cell_id"] == DONOR_CELL_ID
    assert inputs["condition_order"] == list(CONDITION_ORDER)
    assert inputs["new_session_count"] == 3
    assert inputs["new_physical_experiment_count"] == 0
    assert inputs["donor"]["existing_autonomous_score"]["top1"] == 1
    assert inputs["donor_derivatives"]["yoked_evidence_packet"]["complete_experiment_count"] == 12
    assert inputs["donor_derivatives"]["learned_law_artifact"]["artifact_type"] == (
        "participant_final_typed_law"
    )
    assert "oracle_law" not in inputs["condition_order"]


def test_yoked_candidate_reveal_occurs_only_at_terminal() -> None:
    inputs = build_pilot_inputs()
    common = {
        "task_contract": inputs["task_contract"],
        "initial_world_model": inputs["initial_world_model"],
        "candidate_packet": inputs["candidate_packet"],
        "yoked_evidence_packet": inputs["donor_derivatives"]["yoked_evidence_packet"],
    }
    pre = build_recipient_context(
        condition="yoked_evidence",
        stage="pre_evidence",
        **common,
    )
    terminal = build_recipient_context(
        condition="yoked_evidence",
        stage="terminal_ranking",
        **common,
    )

    assert pre["candidate_packet"] is None
    assert len(terminal["candidate_packet"]) == 8
    assert "candidate_queries" not in inputs["task_contract"]["terminal_decision_contract"]


def test_repair_schema_removes_provider_unsupported_union_branches() -> None:
    inputs = build_pilot_inputs()
    schema = provider_compatible_yoked_snapshot_schema(
        stage="pre_evidence",
        query_metric_contract=inputs["query_metric_contract"],
        allowed_feature_ids=inputs["allowed_feature_ids"],
        allowed_metric_ids=inputs["allowed_metric_ids"],
        allowed_prior_fields=inputs["allowed_prior_fields"],
        evidence_catalog=[],
        nominal_information_available=inputs["nominal_information_available"],
    )

    rendered = str(schema)
    assert "oneOf" not in rendered
    assert "anyOf" not in rendered
    assert (
        schema["properties"]["prior_assessment"]["properties"]
        ["suspected_misindexed_fields"]["maxItems"]
        == 0
    )
    assert schema["properties"]["evidence_ids"]["maxItems"] == 128
    assert (
        schema["properties"]["law_summary"]["properties"]["evidence_ids"]["maxItems"]
        == 128
    )
    assert schema["properties"]["predictions"]["items"]["properties"]["query_id"][
        "enum"
    ] == list(inputs["query_metric_contract"])


def test_repair_normalization_only_removes_null_unconditional_categories() -> None:
    payload = {
        "law_summary": {
            "metric_laws": [
                {
                    "terms": [
                        {"basis": "linear", "category_value": None},
                        {"basis": "conditional_linear", "category_value": 2},
                        {"basis": "linear", "category_value": "unexpected"},
                    ]
                }
            ]
        }
    }

    terms = normalize_nullable_law_terms(payload)["law_summary"]["metric_laws"][0]["terms"]
    assert "category_value" not in terms[0]
    assert terms[1]["category_value"] == 2
    assert terms[2]["category_value"] == "unexpected"


def test_snapshot_validator_accepts_w250_final_event_catalog_below_128() -> None:
    evidence_ids = [f"event-{index:03d}" for index in range(85)]
    payload = {
        "schema_version": "chemworld-work-ii-belief-snapshot-0.1",
        "snapshot_id": "snapshot-final",
        "stage": "final",
        "prior_assessment": {
            "nominal_information_available": False,
            "reliability_probability": None,
            "suspected_misindexed_fields": [],
            "rationale": "The target locus is opaque.",
        },
        "predictions": [
            {
                "query_id": "checkpoint-q",
                "metrics": [
                    {
                        "metric_id": "score",
                        "mean": 0.5,
                        "interval_lower": 0.2,
                        "interval_upper": 0.8,
                        "confidence": 0.7,
                    }
                ],
            }
        ],
        "law_summary": {
            "schema_version": "chemworld-work-ii-law-summary-0.1",
            "summary_id": "law-final",
            "feature_ids": ["temperature"],
            "metric_laws": [
                {
                    "metric_id": "score",
                    "intercept": 0.5,
                    "link": "identity",
                    "lower_bound": 0.0,
                    "upper_bound": 1.0,
                    "terms": [],
                }
            ],
            "evidence_ids": evidence_ids,
            "applicability": "registered checkpoint domain",
            "limitations": [],
            "confidence": 0.7,
        },
        "evidence_ids": evidence_ids,
        "next_experiment_intent": "Rank the terminal candidates.",
        "overall_confidence": 0.7,
    }

    parsed = validate_yoked_snapshot_submission(
        payload,
        stage="final",
        query_metric_contract={"checkpoint-q": ["score"]},
        allowed_feature_ids=["temperature"],
        allowed_metric_ids=["score"],
        allowed_prior_fields=[],
        evidence_catalog=evidence_ids,
        nominal_information_available=False,
    )
    assert len(parsed["evidence_ids"]) == 85
