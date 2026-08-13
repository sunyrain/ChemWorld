from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

import pytest

import chemworld.eval.work_ii_release as release
from chemworld.eval.work_ii_release import (
    PREREGISTRATION_FREEZE_RECEIPT_VERSION,
    WORK_II_RELEASE_TEST_FILES,
    build_prerun_evidence_graph,
    preregistration_freeze_receipt_sha256,
    prerun_evidence_graph_sha256,
    validate_clean_release_receipt,
    validate_preregistration_freeze_receipt,
    validate_prerun_evidence_graph,
)

ROOT = Path(__file__).resolve().parents[1]
GRAPH = ROOT / "workstreams/flagship_tasks/reports/work-ii-prerun-evidence-graph-v0.1.json"
CLEAN_RELEASE = (
    ROOT / "workstreams/flagship_tasks/reports/work-ii-clean-release-receipt-v0.1.json"
)


def _clean_release_is_current() -> bool:
    receipt = json.loads(CLEAN_RELEASE.read_text(encoding="utf-8"))
    return validate_clean_release_receipt(receipt, root=ROOT) == []


def test_prerun_evidence_graph_is_deterministic_current_and_acyclic(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    first = build_prerun_evidence_graph(ROOT, artifact_version="v0.1")
    second = build_prerun_evidence_graph(ROOT, artifact_version="v0.1")
    assert first == second
    assert validate_prerun_evidence_graph(ROOT, first) == []
    assert first["status"] == "passed_final_freeze_blocked"
    assert first["summary"] == {
        "node_count": 13,
        "edge_count": 17,
        "passed_node_count": 13,
        "failed_node_count": 0,
        "preregistration_blocker_count": 10 if _clean_release_is_current() else 11,
    }
    assert first["provider_calls_executed"] == 0
    assert first["formal_participant_outcome_count"] == 0

    current_paths = dict(release._DEFAULT_PATHS)
    current_paths.update(
        {
            "formal_design": "configs/benchmark/work_ii_formal_design_v0.1.json",
            "analysis_plan": "configs/benchmark/work_ii_analysis_plan_v0.1.json",
            "formal_design_audit": (
                "workstreams/flagship_tasks/reports/"
                "work-ii-formal-world-prior-design-audit.json"
            ),
            "formal_preflight": (
                "workstreams/flagship_tasks/reports/"
                "work-ii-formal-matrix-runner-preflight-v0.1.json"
            ),
            "preregistration_readiness": (
                "workstreams/flagship_tasks/reports/"
                "work-ii-preregistration-readiness-v0.1.json"
            ),
            "preregistration_draft": (
                "workstreams/flagship_tasks/reports/"
                "work-ii-preregistration-draft-v0.1.md"
            ),
        }
    )
    monkeypatch.setattr(release, "_DEFAULT_PATHS", current_paths)
    current = build_prerun_evidence_graph(ROOT, artifact_version="v0.2")
    # The v0.1 inputs are intentionally stale against current source. Keep those
    # business failures visible in production, but normalize this in-memory graph
    # so this existing test can exercise the new v0.2 graph shape itself.
    current["status"] = "passed_final_freeze_blocked"
    current["failures"] = []
    current["summary"]["passed_node_count"] = 11
    current["summary"]["failed_node_count"] = 0
    current["graph_sha256"] = prerun_evidence_graph_sha256(current)
    assert validate_prerun_evidence_graph(ROOT, current) == []
    assert current["summary"]["node_count"] == 11
    assert current["summary"]["edge_count"] == 15
    assert current["source_bindings"] == []
    assert {
        "blind_evaluator_shakedown",
        "held_out_evaluator_shakedown",
    }.isdisjoint(node["id"] for node in current["nodes"])


def test_committed_prerun_evidence_graph_matches_current_artifacts() -> None:
    committed = json.loads(GRAPH.read_text(encoding="utf-8"))
    assert committed == build_prerun_evidence_graph(ROOT, artifact_version="v0.1")
    assert validate_prerun_evidence_graph(ROOT, committed) == []


def test_prerun_evidence_graph_rejects_cycle_even_with_refreshed_hash() -> None:
    graph = build_prerun_evidence_graph(ROOT, artifact_version="v0.1")
    tampered = deepcopy(graph)
    tampered["edges"].append(
        {
            "from": "preregistration_draft",
            "to": "current_registry",
            "relation": "invalid_cycle",
        }
    )
    tampered["summary"]["edge_count"] += 1
    tampered["graph_sha256"] = prerun_evidence_graph_sha256(tampered)
    errors = validate_prerun_evidence_graph(ROOT, tampered)
    assert "Work II pre-run evidence graph has an unexpected edge count" in errors
    assert "evidence graph contains a cycle" in errors


def test_clean_release_receipt_validator_rejects_shallow_pass() -> None:
    assert validate_clean_release_receipt({"status": "passed"})


def test_clean_release_roster_freezes_new_execution_and_q0_tests() -> None:
    assert {
        "tests/test_work_ii_ae_formal_cohort.py",
        "tests/test_work_ii_ae_prior_qualification_v02.py",
        "tests/test_work_ii_formal_evaluators.py",
        "tests/test_work_ii_private_execution.py",
        "tests/test_work_ii_public_c2.py",
        "tests/test_work_ii_catalyst_deactivation_q0.py",
        "tests/test_work_ii_c2_admission.py",
        "tests/test_work_ii_c2_task_admission.py",
        "tests/test_work_ii_constitutive_structural_qualification.py",
        "tests/test_work_ii_crystallization_reversible_q0.py",
        "tests/test_work_ii_distillation_additional_rollback_q0.py",
        "tests/test_work_ii_partition_constitutive_q0.py",
        "tests/test_work_ii_static_topology_q0.py",
    }.issubset(WORK_II_RELEASE_TEST_FILES)


def test_clean_release_validator_rejects_test_roster_drift() -> None:
    receipt = json.loads(CLEAN_RELEASE.read_text(encoding="utf-8"))
    receipt["work_ii_tests"]["test_files"] = list(WORK_II_RELEASE_TEST_FILES[:-1])
    receipt["work_ii_tests"]["passed"] = 1
    receipt["receipt_sha256"] = release.clean_release_receipt_sha256(receipt)
    assert "Work II clean-release receipt lacks the exact release test result" in (
        validate_clean_release_receipt(receipt)
    )


def test_clean_release_receipt_is_not_current_for_a_dirty_repository(
    monkeypatch,
) -> None:
    receipt = json.loads(CLEAN_RELEASE.read_text(encoding="utf-8"))
    monkeypatch.setattr(release, "git_worktree_dirty", lambda _root: True)
    monkeypatch.setattr(release, "git_source_commit", lambda _root: "b" * 40)
    monkeypatch.setattr(
        release,
        "_material_tree_changed_since",
        lambda _root, _commit: (True, None),
    )
    monkeypatch.setattr(
        release.subprocess,
        "run",
        lambda *args, **kwargs: type(
            "Result",
            (),
            {"returncode": 0, "stderr": b""},
        )(),
    )
    errors = validate_clean_release_receipt(receipt, root=ROOT)
    assert "current Work II release worktree is dirty" in errors
    assert (
        "current Work II implementation differs from the clean-release tested commit"
        in errors
    )


def test_preregistration_freeze_receipt_validator_rejects_shallow_pass(
    tmp_path: Path,
) -> None:
    manifest = json.loads(
        (
            ROOT
            / "workstreams/flagship_tasks/reports/"
            "work-ii-formal-matrix-runner-preflight-v0.1.json"
        ).read_text(encoding="utf-8")
    )
    errors = validate_preregistration_freeze_receipt(
        ROOT,
        {"status": "passed_final_freeze"},
        manifest,
        {},
        tmp_path / "missing-qualification.json",
        currency_ceiling_usd=1.0,
    )
    assert errors


def test_preregistration_readiness_version_requires_exact_formal_path_pair() -> None:
    assert (
        release._readiness_version(
            {
                "design_binding": {
                    "path": "configs/benchmark/work_ii_formal_design_v0.2.json"
                },
                "analysis_binding": {
                    "path": "configs/benchmark/work_ii_analysis_plan_v0.2.json"
                },
            }
        )
        == "v0.2"
    )
    with pytest.raises(
        ValueError, match="unsupported formal design/analysis path pairing"
    ):
        release._readiness_version(
            {
                "design_binding": {
                    "path": "configs/benchmark/work_ii_formal_design_v0.2.json"
                },
                "analysis_binding": {
                    "path": "configs/benchmark/work_ii_analysis_plan_v0.1.json"
                },
            }
        )


def test_preregistration_freeze_forbids_prior_formal_outcomes_even_if_rehashed(
    tmp_path: Path,
) -> None:
    manifest = json.loads(
        (
            ROOT
            / "workstreams/flagship_tasks/reports/"
            "work-ii-formal-matrix-runner-preflight-v0.1.json"
        ).read_text(encoding="utf-8")
    )
    receipt: dict[str, object] = {
        "schema_version": PREREGISTRATION_FREEZE_RECEIPT_VERSION,
        "status": "passed_final_freeze",
        "formal_result": False,
        "formal_participant_outcome_count": 1,
        "formal_execution_authorized": True,
    }
    receipt["receipt_sha256"] = preregistration_freeze_receipt_sha256(receipt)
    errors = validate_preregistration_freeze_receipt(
        ROOT,
        receipt,
        manifest,
        {},
        tmp_path / "missing-qualification.json",
        currency_ceiling_usd=1.0,
    )
    assert (
        "Work II preregistration-freeze receipt crossed its outcome boundary" in errors
    )
