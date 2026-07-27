from __future__ import annotations

import json
from pathlib import Path

import pytest

from chemworld.agents.static_optimization import (
    StaticOptimizationContextBuilder,
    StaticOptimizationValidator,
)
from chemworld.eval.static_optimization_postrun import audit_world_understanding_receipts
from chemworld.eval.world_understanding import (
    ReferenceWorldClaim,
    parse_world_understanding_claims,
    score_world_understanding,
)
from chemworld.physchem.electrochemical_task_contract import (
    ELECTROCHEMICAL_WORKFLOW_ADAPTIVE_TWO_STAGE,
)
from chemworld.tasks import get_task


def test_current_electrochemical_default_uses_single_stage_controls() -> None:
    task = get_task("electrochemical-conversion").to_dict()
    interface = StaticOptimizationContextBuilder(task).build([])[
        "experiment_interface"
    ]

    assert "potential_V" in interface["recipe_parameter_schema"]
    assert "probe_potential_V" not in interface["recipe_parameter_schema"]


def test_legacy_two_stage_controls_require_explicit_workflow() -> None:
    task = get_task("electrochemical-conversion").to_dict()
    context = StaticOptimizationContextBuilder(
        task,
        electrochemical_workflow_mode=ELECTROCHEMICAL_WORKFLOW_ADAPTIVE_TWO_STAGE,
    ).build([])
    interface = context["experiment_interface"]

    assert interface["parameterization"] == "named_physical_controls"
    assert interface["internal_unit_vector_visible_to_agent"] is False
    assert "search_vector_dimension" not in interface
    assert "probe_potential_V" in interface["recipe_parameter_schema"]

    plan = StaticOptimizationValidator(
        task,
        electrochemical_workflow_mode=ELECTROCHEMICAL_WORKFLOW_ADAPTIVE_TWO_STAGE,
    ).validate(
        {
            "experiment_intent": "compare two controlled electrolysis regimes",
            "recipe_parameters": {
                "electrolyte_profile": 1,
                "solvent": 0,
                "reagent_amount_mol": 0.010,
                "probe_potential_V": 0.85,
                "probe_current_mA": 45.0,
                "probe_duration_s": 420.0,
                "controlled_potential_V": 1.10,
                "controlled_current_mA": 65.0,
                "controlled_duration_s": 1500.0,
            },
            "requested_measurement_slots": ["diagnostic-02-uvvis"],
            "measurement_objective": "measure conversion and energy response",
            "expected_effect": "the potential change should reveal a response regime",
            "uncertainty": 0.6,
        }
    )
    assert plan.recipe_parameters is not None
    assert plan.recipe_parameters["controlled_potential_V"] == pytest.approx(1.10)
    assert len(plan.search_vector) == 9


def test_world_understanding_scores_observable_equivalence_classes() -> None:
    predicted = parse_world_understanding_claims(
        [
            {
                "claim_id": "p1",
                "cause_variables": ["controlled_potential_V"],
                "effect_variable": "yield",
                "relation": "nonmonotonic",
                "mechanism_tags": ["nernst_equilibrium", "butler_volmer_kinetics"],
                "scope": "declared operating range",
                "evidence_ids": ["e1"],
                "confidence": 0.8,
            }
        ],
        evidence_catalog=["e1"],
        allowed_cause_variables=["controlled_potential_V"],
        allowed_effect_variables=["yield"],
        allowed_mechanism_tags=["nernst_equilibrium", "butler_volmer_kinetics"],
    )
    reference = (
        ReferenceWorldClaim(
            claim_id="potential-yield",
            cause_variables=("controlled_potential_V",),
            effect_variable="yield",
            accepted_relations=("nonmonotonic", "conditional"),
            mechanism_tags=("nernst_equilibrium", "butler_volmer_kinetics"),
        ),
    )
    score = score_world_understanding(predicted, reference)

    assert score.structural_edge_f1 == pytest.approx(1.0)
    assert score.directional_accuracy == pytest.approx(1.0)
    assert score.mechanism_tag_f1 == pytest.approx(1.0)
    assert score.unsupported_claim_rate == pytest.approx(0.0)
    assert score.confidence_brier_score == pytest.approx(0.04)


def test_world_understanding_reference_scores_receipt_claims() -> None:
    protocol = {
        "world_understanding": {
            "enabled": True,
            "reference_path": "configs/benchmark/world_understanding_s0_v0.1_dev.json",
            "predictive_score_enabled": False,
        }
    }
    receipt = {
        "cell": {"cell_id": "cell-1", "task_id": "electrochemical-conversion"},
        "method_id": "mock",
        "experiments": [
            {
                "result": {
                    "measurement_evidence": [{"evidence_id": "e1"}],
                }
            }
        ],
        "final_synthesis": {
            "recommendation": {
                "working_explanation": {
                    "structured_claims": [
                        {
                            "claim_id": "p1",
                            "cause_variables": ["controlled_potential_V"],
                            "effect_variable": "yield",
                            "relation": "nonmonotonic",
                            "mechanism_tags": [
                                "nernst_equilibrium",
                                "butler_volmer_kinetics",
                            ],
                            "scope": "S0 range",
                            "evidence_ids": ["e1"],
                            "confidence": 0.8,
                        }
                    ]
                }
            }
        },
    }

    audit = audit_world_understanding_receipts([receipt], protocol)

    assert audit["enabled"] is True
    assert audit["scored_cell_count"] == 1
    assert audit["cells"][0]["status"] == "scored"
    assert audit["cells"][0]["score"]["structural_edge_precision"] == pytest.approx(1.0)


def test_v03_protocol_is_explicitly_blocked_before_paid_execution() -> None:
    root = Path(__file__).resolve().parents[1]
    protocol = json.loads(
        (
            root
            / "configs/benchmark/"
            "scientific_optimization_s0_v0.3_named_electrochem_world_understanding_dev.json"
        ).read_text(encoding="utf-8")
    )

    assert protocol["status"] == "development_pending_owner_confirmation"
    assert protocol["tasks"] == ["electrochemical-conversion"]
    assert protocol["experiment_interface"]["model_facing_parameterization"] == (
        "named_physical_controls"
    )
    assert protocol["world_understanding"]["predictive_score_enabled"] is True
    predictive = protocol["world_understanding"]["predictive_validation"]
    assert predictive["query_count"] == 3
    assert predictive["paired_replicates_per_query"] == 2
    assert predictive["total_physical_experiments_per_seed"] == 12
    assert predictive["additional_model_calls"] == 0
    assert predictive["feedback_returned_to_agent"] is False
