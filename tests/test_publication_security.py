from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

from chemworld.eval.publication_security import (
    audit_exploit_resistance,
    audit_generalization_controls,
    load_generalization_security_protocol,
)
from chemworld.tasks import SERIOUS_TASK_IDS

SUMMARY_PATH = (
    Path(__file__).resolve().parents[1]
    / "workstreams"
    / "benchmark_v1"
    / "reports"
    / "publication-generalization-security-summary.json"
)


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


def test_generalization_security_summary_preserves_historical_blockers() -> None:
    report = json.loads(SUMMARY_PATH.read_text(encoding="utf-8"))

    assert report["status"] == "blocked"
    assert report["publication_ready"] is False
    assert report["gates"]["exploit_resistance_passed"] is True
    assert report["gates"]["public_seed_ood_passed"] is False
    assert report["gates"]["salted_private_eval_passed"] is False
    assert report["gates"]["distribution_shift_protocol_bindings_valid"] is False
    assert report["distribution_shifts"]["public_seed_ood"]["ready_task_count"] == 6
    assert report["distribution_shifts"]["salted_private_eval"]["ready_task_count"] == 4
    private_manifest = report["formal_run_manifests"]["salted_private_eval"]
    assert len(private_manifest["private_salt_sha256"]) == 64
    assert private_manifest["raw_private_salt_published"] is False
