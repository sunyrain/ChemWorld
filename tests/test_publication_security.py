from __future__ import annotations

from copy import deepcopy

from chemworld.eval.publication_security import (
    audit_exploit_resistance,
    audit_generalization_controls,
    load_generalization_security_protocol,
)
from chemworld.tasks import SERIOUS_TASK_IDS


def test_generalization_protocol_fails_closed_on_missing_axis_controls() -> None:
    report = audit_generalization_controls(load_generalization_security_protocol())

    assert report["protocol_valid"] is True
    assert report["axis_generalization_ready"] is False
    assert report["invariance_ready"] is False
    assert report["generalization_ready"] is False
    assert set(report["tasks"]) == set(SERIOUS_TASK_IDS)
    assert all(
        axis["missing_modes"]
        for task in report["tasks"].values()
        for axis in task["axes"].values()
    )


def test_generalization_protocol_detects_task_axis_drift() -> None:
    protocol = deepcopy(load_generalization_security_protocol())
    protocol["axis_control_status"]["partition-discovery"] = {
        "wrong axis": ["interpolation"]
    }

    report = audit_generalization_controls(protocol)

    assert report["protocol_valid"] is False
    assert report["tasks"]["partition-discovery"]["configured_axes_match"] is False


def test_exploit_matrix_rejects_score_shortcuts_and_is_key_order_invariant() -> None:
    report = audit_exploit_resistance()

    assert report["passed"] is True
    assert report["task_count"] == len(SERIOUS_TASK_IDS)
    for task in report["tasks"].values():
        assert task["passed"] is True
        assert all(task["probes"].values())
