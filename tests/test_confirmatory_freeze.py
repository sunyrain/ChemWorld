from __future__ import annotations

import copy
import json
from pathlib import Path

from chemworld.eval.confirmatory_freeze import (
    audit_confirmatory_freeze,
    canonical_json_file_sha256,
    load_confirmatory_freeze,
)

FROZEN_REPORT = (
    Path(__file__).resolve().parents[1]
    / "workstreams"
    / "benchmark_v1"
    / "reports"
    / "confirmatory-freeze-controls.json"
)


def test_confirmatory_freeze_is_pre_result_and_fail_closed() -> None:
    report = audit_confirmatory_freeze(load_confirmatory_freeze())

    assert report["controls_ready"] is True
    assert report["protocol_frozen"] is True
    assert report["confirmatory_rerun_ready"] is False
    assert report["primary_classical_rerun_ready"] is True
    assert report["primary_methods_ready"] is True
    assert report["benchmark_claim_allowed"] is False
    assert report["publication_ready"] is False
    assert report["confirmatory_seeds"] == list(range(20, 40))
    assert report["task_roles"]["core"] == [
        "partition-discovery",
        "reaction-to-crystallization",
        "reaction-to-distillation",
        "flow-reaction-optimization",
    ]
    assert report["sesoi"]["partition-discovery"]["sesoi"] == 0.0292
    assert report["sesoi"]["reaction-to-crystallization"]["sesoi"] == 0.038827
    assert report["world_family_allocation"]["core_axis_count"] == 8
    assert report["world_family_allocation"]["train_dev_extrapolation_cells"] == 0


def test_freeze_rejects_posthoc_sesoi_and_overlapping_world_cells() -> None:
    protocol = load_confirmatory_freeze()

    posthoc = copy.deepcopy(protocol)
    posthoc["sesoi"]["tasks"]["flow-reaction-optimization"]["sesoi"] = 0.001
    posthoc_report = audit_confirmatory_freeze(posthoc)
    assert posthoc_report["checks"]["sesoi_derivation_matches"] is False
    assert posthoc_report["controls_ready"] is False

    overlapping = copy.deepcopy(protocol)
    overlapping["world_family_allocation"]["dev"]["cells"]["interpolation"] = [0.5]
    overlap_report = audit_confirmatory_freeze(overlapping)
    assert overlap_report["checks"]["world_cells_pairwise_disjoint"] is False
    assert overlap_report["controls_ready"] is False


def test_frozen_confirmatory_report_preserves_blockers() -> None:
    report = json.loads(FROZEN_REPORT.read_text(encoding="utf-8"))

    assert report["controls_ready"] is True
    assert report["protocol_frozen"] is True
    assert report["confirmatory_rerun_ready"] is False
    assert report["primary_classical_rerun_ready"] is True
    assert report["publication_ready"] is False
    assert "ppo" in report["missing_required_methods"]
    assert report["exploit_matrix_complete"] is True


def test_evidence_digest_is_json_semantic_and_line_ending_neutral(tmp_path: Path) -> None:
    left = tmp_path / "left.json"
    right = tmp_path / "right.json"
    left.write_bytes(b'{"b": 2,\n"a": 1}\n')
    right.write_bytes(b'{\r\n  "a": 1,\r\n  "b": 2\r\n}\r\n')

    assert canonical_json_file_sha256(left) == canonical_json_file_sha256(right)
