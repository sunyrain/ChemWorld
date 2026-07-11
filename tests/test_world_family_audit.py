from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

from chemworld.eval.world_family_audit import (
    audit_world_family_controls,
    load_world_family_protocol,
)

FROZEN_REPORT = (
    Path(__file__).resolve().parents[1]
    / "workstreams"
    / "benchmark_v1"
    / "reports"
    / "world-family-axis-controls.json"
)


def test_protocol_registry_controls_pass_without_overclaiming() -> None:
    report = audit_world_family_controls(
        load_world_family_protocol(),
        run_response_probes=False,
    )
    assert report["controls_ready"] is False
    assert report["checks"]["single_axis_probe_changes_task_response"] is None
    assert report["benchmark_claim_allowed"] is False
    assert report["publication_ready"] is False


def test_protocol_axis_drift_fails_closed() -> None:
    protocol = deepcopy(load_world_family_protocol())
    protocol["tasks"]["partition-discovery"]["axes"][0] = "wrong.axis"
    report = audit_world_family_controls(protocol, run_response_probes=False)
    assert report["checks"]["configured_axes_match_registry"] is False
    assert report["controls_ready"] is False


def test_frozen_control_report_is_ready_but_non_claiming() -> None:
    report = json.loads(FROZEN_REPORT.read_text(encoding="utf-8"))
    assert report["controls_ready"] is True
    assert report["checks"]["single_axis_probe_changes_task_response"] is True
    assert report["checks"]["agent_facing_axis_identity_hidden"] is True
    assert report["benchmark_claim_allowed"] is False
    assert report["publication_ready"] is False
