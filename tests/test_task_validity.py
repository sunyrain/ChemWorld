from __future__ import annotations

import json
from pathlib import Path

from chemworld.eval.task_validity import load_task_validity_protocol

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "workstreams" / "benchmark_v1" / "reports" / "task-validity-vnext.json"


def test_task_validity_protocol_is_candidate_and_non_claiming() -> None:
    protocol = load_task_validity_protocol()
    assert protocol["benchmark_claim_allowed"] is False
    assert protocol["primary_comparator"] == "gp_bo__minus__random"
    assert protocol["comparator_absolute_sesoi"] == 0.05
    assert protocol["minimum_surface_normalized_effect"] == 0.05


def test_task_validity_report_recommends_provisional_core4() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    assert report["controls_ready"] is True
    assert report["benchmark_claim_allowed"] is False
    assert report["suite_recommendation"]["core4_claim_ready"] is False
    assert report["suite_recommendation"]["recommended_core_tasks"] == [
        "partition-discovery",
        "reaction-to-crystallization",
        "reaction-to-distillation",
        "flow-reaction-optimization",
    ]
    assert report["suite_recommendation"]["exploratory_tasks"] == [
        "electrochemical-conversion",
        "equilibrium-characterization",
    ]


def test_task_cards_preserve_legacy_negative_results() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    cards = report["task_cards"]
    assert cards["reaction-to-crystallization"]["release_role"] == "core_confirmed"
    assert cards["reaction-to-distillation"]["release_role"] == "core_confirmed"
    assert cards["partition-discovery"]["release_role"] == "core_confirmed"
    assert cards["partition-discovery"]["capability_validated_under_legacy_sesoi"] is False
    assert cards["flow-reaction-optimization"]["release_role"] == "core_candidate"
    assert cards["electrochemical-conversion"]["release_role"] == "exploratory"
    assert cards["equilibrium-characterization"]["release_role"] == "exploratory"
    assert (
        cards["equilibrium-characterization"]["minimum_adaptive_strategy_test"][
            "direction_supported"
        ]
        is False
    )
