from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace

from chemworld.eval.work_ii_formal import build_checkpoint_contract
from chemworld.eval.work_ii_truth import (
    build_evaluator_truth_plan,
    compile_evaluator_truth_query,
    execute_evaluator_truth_plan,
    validate_evaluator_truth_plan,
    validate_evaluator_truth_report,
)

ROOT = Path(__file__).resolve().parents[1]
CONFIGS = (
    "work_ii_campaign_pilot.json",
    "work_ii_crystallization_campaign.json",
    "work_ii_distillation_campaign.json",
    "work_ii_partition_campaign.json",
    "work_ii_safety_campaign.json",
)


def _load_config(name: str) -> dict[str, object]:
    return json.loads((ROOT / "configs/benchmark" / name).read_text(encoding="utf-8"))


def test_all_formal_queries_compile_to_complete_frozen_experiments() -> None:
    expected_action_counts = {
        "electrochemical-conversion": 8,
        "reaction-to-crystallization": 12,
        "reaction-to-distillation": 12,
        "partition-discovery": 10,
        "reaction-safety-constrained": 8,
    }
    for name in CONFIGS:
        config = _load_config(name)
        checkpoint = build_checkpoint_contract(config, "opaque")
        compiled = [
            compile_evaluator_truth_query(config, query) for query in checkpoint["held_out_queries"]
        ]
        assert len(compiled) == 4
        assert all(
            len(item["action_plan"]) == expected_action_counts[config["task_id"]]
            for item in compiled
        )
        assert all(
            item["action_plan"][-1] == {"operation": "measure", "instrument": "final_assay"}
            for item in compiled
        )


def test_truth_plan_is_shared_across_arms_and_self_bound() -> None:
    config = _load_config("work_ii_partition_campaign.json")
    cluster = {
        "world_cluster_id": "work-ii-public-04-01",
        "task_id": "partition-discovery",
        "world_seed": 958536734,
    }
    plan = build_evaluator_truth_plan(
        cluster,
        config,
        formal_result=True,
        formal_preflight_sha256="a" * 64,
    )
    assert validate_evaluator_truth_plan(plan) == []
    assert plan["truth_query_count"] == 4
    assert plan["truth_query_metric_count"] == 12
    assert plan["evaluator_provider_call_count"] == 0
    assert plan["participant_operation_denominator_impact"] == 0
    assert plan["shared_across_prior_arms"] is True
    assert plan["law_summary_contract"] == {
        "allowed_feature_ids": [
            "solvent",
            "aqueous_phase_volume_L",
            "extractant",
            "extractant_volume_L",
            "mix_duration_s",
            "settle_duration_s",
            "stirring_speed_rpm",
        ],
        "allowed_metric_ids": [
            "phase_ratio",
            "product_in_organic",
            "product_in_aqueous",
        ],
        "required_metric_ids": [
            "phase_ratio",
            "product_in_organic",
            "product_in_aqueous",
        ],
        "evidence_catalog": [
            "experiment-1-final-assay",
            "experiment-2-final-assay",
            "experiment-3-final-assay",
            "experiment-4-final-assay",
            "experiment-5-final-assay",
            "experiment-6-final-assay",
            "experiment-7-final-assay",
            "experiment-8-final-assay",
        ],
    }

    tampered = deepcopy(plan)
    tampered["queries"][0]["feature_values"]["solvent"] = 3
    assert "evaluator truth plan self-hash mismatch" in validate_evaluator_truth_plan(tampered)


def test_truth_plan_accepts_pattern_owned_query_and_evidence_denominators() -> None:
    config = _load_config("work_ii_reaction_safety_matched_prior_d1.json")
    plan = build_evaluator_truth_plan(
        {
            "world_cluster_id": "reaction-safety-d1-seed0",
            "task_id": "reaction-safety-constrained",
            "world_seed": 0,
        },
        config,
        formal_result=False,
        formal_preflight_sha256=None,
    )

    assert validate_evaluator_truth_plan(plan) == []
    assert plan["truth_query_count"] == 16
    assert plan["law_summary_contract"]["evidence_catalog"] == [
        f"experiment-{index}-final-assay" for index in range(1, 11)
    ]
    heat = next(
        action for action in plan["queries"][0]["action_plan"] if action["operation"] == "heat"
    )
    assert heat["stirring_speed_rpm"] == 400.0


def test_electrochemical_matched_prior_truth_uses_autonomous_open_contract() -> None:
    config = _load_config("work_ii_electrochemical_matched_prior_d1_execution.json")
    plan = build_evaluator_truth_plan(
        {
            "world_cluster_id": "electrochemical-matched-prior-d1-seed0",
            "task_id": "electrochemical-conversion",
            "world_seed": 0,
        },
        config,
        formal_result=False,
        formal_preflight_sha256=None,
    )

    assert validate_evaluator_truth_plan(plan) == []
    assert plan["truth_query_count"] == 16
    assert all(query["workflow_mode"] == "autonomous_open_v1" for query in plan["queries"])
    assert all(len(query["action_plan"]) == 11 for query in plan["queries"])
    assert all(
        sum(action["operation"] == "electrolyze" for action in query["action_plan"]) == 2
        for query in plan["queries"]
    )


def test_truth_executor_retains_exact_four_query_denominator(
    tmp_path: Path,
    monkeypatch,
) -> None:
    import chemworld.eval.work_ii_truth as truth_module

    config = _load_config("work_ii_campaign_pilot.json")
    cluster = {
        "world_cluster_id": "development-electrochemical-seed0",
        "task_id": "electrochemical-conversion",
        "world_seed": 0,
    }
    plan = build_evaluator_truth_plan(
        cluster,
        config,
        formal_result=False,
        formal_preflight_sha256=None,
    )

    def fake_run_agent(**kwargs):
        actions = kwargs["agent"]._frozen_actions
        rows = []
        for action in actions:
            row = {
                "action": action,
                "transaction_status": "committed",
                "operation_type": action["operation"],
                "instrument": action.get("instrument"),
                "observation": {},
            }
            if action.get("instrument") == "final_assay":
                row["observation"] = {
                    "selective_product_yield": 0.6,
                    "energy_efficiency": 0.7,
                    "safety_risk": 0.1,
                }
                row["leaderboard_score"] = 0.5
            rows.append(row)
        output = Path(kwargs["output_path"])
        output.write_text(
            "".join(json.dumps(row, sort_keys=True) + "\n" for row in rows),
            encoding="utf-8",
        )
        return []

    monkeypatch.setattr(truth_module, "run_agent", fake_run_agent)
    monkeypatch.setattr(
        truth_module,
        "verify_records",
        lambda records, tolerance: SimpleNamespace(
            to_dict=lambda: {
                "verified": True,
                "checked_steps": len(records),
                "max_abs_error": 0.0,
                "mismatches": [],
            }
        ),
    )
    report = execute_evaluator_truth_plan(plan, config, tmp_path / "truth")
    assert validate_evaluator_truth_report(report, plan) == []
    assert report["status"] == "completed"
    assert report["completed_truth_query_count"] == 4
    assert report["completed_truth_query_metric_count"] == 12
    assert set(report["truth"]) == {"q-low", "q-electrolyte", "q-solvent", "q-high"}
    assert report["evaluator_provider_call_count"] == 0
    assert report["participant_feedback_emitted"] is False
