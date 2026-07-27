from __future__ import annotations

import copy
import json
from pathlib import Path

from chemworld.eval.confirmatory_task_semantics_audit import (
    audit_confirmatory_task_semantics,
)
from chemworld.eval.mechanism_adaptation import (
    load_mechanism_adaptation_protocol,
)
from chemworld.eval.mechanism_adaptation_execution import load_json_object

ROOT = Path(__file__).resolve().parents[1]


def _inputs() -> tuple[dict, dict, dict]:
    protocol = load_mechanism_adaptation_protocol(
        ROOT / "configs/benchmark/mechanism_adaptation_v0.3.0_rc28.json"
    )
    plan = load_json_object(
        ROOT / "configs/benchmark/mechanism_adaptation_gate_a_v0.3.0_rc28.json"
    )
    graph = json.loads(
        (ROOT / plan["diagnostic_relation_graph"]["report"]).read_text(
            encoding="utf-8"
        )
    )
    return protocol, plan, graph


def test_current_semantics_audit_reports_frozen_relation_graph_drift() -> None:
    protocol, plan, graph = _inputs()
    report = audit_confirmatory_task_semantics(protocol, plan, graph)

    assert report["pass"] is False
    assert report["failure_count"] == 1
    assert report["check_count"] == 25
    assert report["failures"][0]["check"] == (
        "diagnostic_relation_graph_frozen_and_bound"
    )
    assert report["confirmatory_benchmark_task_ids"] == [
        "reaction-to-crystallization",
        "electrochemical-conversion",
    ]


def test_confirmatory_task_semantics_audit_rejects_missing_no_change_truth() -> None:
    protocol, plan, graph = _inputs()
    broken = copy.deepcopy(protocol)
    broken["evaluation_tracks"]["calibrated_online_change"][
        "truth_change_time_support"
    ] = [6, 8, 10]

    report = audit_confirmatory_task_semantics(broken, plan, graph)

    assert report["pass"] is False
    failed = {item["check"] for item in report["failures"]}
    assert "protocol_schema_valid" in failed
    assert "a3_true_no_change_condition" in failed
