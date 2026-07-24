from __future__ import annotations

import copy
import json
from pathlib import Path

from chemworld.eval.flagship_semantics_audit import (
    audit_flagship_experiment_semantics,
)
from chemworld.eval.mechanism_adaptation import (
    load_mechanism_adaptation_protocol,
)

ROOT = Path(__file__).resolve().parents[1]


def _inputs() -> tuple[dict, dict, dict]:
    protocol = load_mechanism_adaptation_protocol(
        ROOT / "configs/benchmark/mechanism_adaptation_v0.3.0.json"
    )
    plan = json.loads(
        (
            ROOT
            / "configs/benchmark/mechanism_adaptation_gate_a_v0.3.0.json"
        ).read_text(encoding="utf-8")
    )
    graph = json.loads(
        (ROOT / plan["diagnostic_relation_graph"]["report"]).read_text(
            encoding="utf-8"
        )
    )
    return protocol, plan, graph


def test_current_flagship_semantics_audit_covers_every_gate_component() -> None:
    protocol, plan, graph = _inputs()
    report = audit_flagship_experiment_semantics(protocol, plan, graph)

    assert report["pass"] is True
    assert report["failure_count"] == 0
    assert report["check_count"] == 18
    assert report["formal_flagship_task_ids"] == [
        "reaction-to-crystallization",
        "electrochemical-conversion",
    ]


def test_flagship_semantics_audit_rejects_missing_no_change_truth() -> None:
    protocol, plan, graph = _inputs()
    broken = copy.deepcopy(protocol)
    broken["evaluation_tracks"]["calibrated_online_change"][
        "truth_change_time_support"
    ] = [6, 8, 10]

    report = audit_flagship_experiment_semantics(broken, plan, graph)

    assert report["pass"] is False
    failed = {item["check"] for item in report["failures"]}
    assert "protocol_schema_valid" in failed
    assert "a3_true_no_change_condition" in failed
