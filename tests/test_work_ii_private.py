from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

import pytest

import chemworld.eval.work_ii_private as private_module
from chemworld.eval.provenance import canonical_json_sha256
from chemworld.eval.work_ii_confirmatory import build_confirmatory_analysis
from chemworld.eval.work_ii_formal import (
    FORMAL_ARMS,
    build_formal_preflight,
)
from chemworld.eval.work_ii_private import (
    PRIVATE_BLOCKING_REQUIREMENTS,
    WORK_II_PRIVATE_SEAL_VERSION,
    WorkIIPrivateConfirmationError,
    build_private_confirmation_preflight,
    validate_private_confirmation_preflight,
    validate_private_seal,
    write_private_preflight_once,
)

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "configs/benchmark/work_ii_formal_design_v0.1.json"
ANALYSIS = ROOT / "configs/benchmark/work_ii_analysis_plan_v0.1.json"


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def _formal_dataset(
    task_ids: list[str],
    *,
    formal_preflight_sha256: str,
) -> dict[str, object]:
    cluster_rows: list[dict[str, object]] = []
    cell_rows: list[dict[str, object]] = []
    for task_index, task_id in enumerate(task_ids):
        for world_index in range(5):
            cluster_id = f"{task_id}-formal-{world_index}"
            aligned = 0.04 + 0.002 * world_index
            misindexed = aligned + 0.20
            cluster_rows.append(
                {
                    "world_cluster_id": cluster_id,
                    "task_id": task_id,
                    "complete_case": True,
                    "H1_prior_utility": 0.12 + 0.005 * task_index,
                    "H2_prior_vulnerability": 0.10 + 0.004 * task_index,
                    "H3_misindexed_improvement": misindexed,
                    "H3_aligned_improvement": aligned,
                    "H3_primary_contrast": misindexed - aligned,
                }
            )
            improvements = {
                "opaque": 0.03,
                "aligned_nominal": aligned,
                "misindexed_nominal": misindexed,
            }
            for arm_index, arm in enumerate(FORMAL_ARMS):
                improvement = improvements[arm]
                cell_rows.append(
                    {
                        "cell_id": f"{cluster_id}-{arm}",
                        "world_cluster_id": cluster_id,
                        "task_id": task_id,
                        "prior_arm": arm,
                        "terminal_state": "completed",
                        "checkpoint_error": {
                            "primary_improvement": improvement,
                            "missing_failure_rule": "observed_final",
                        },
                        "blind_outcome": {
                            "status": "completed",
                            "completed_execution_count": 6,
                            "recommendation_gain_over_incumbent": (
                                0.5 * improvement + 0.002 * arm_index
                            ),
                        },
                        "final_law_summary": {
                            "present": True,
                            "schema_version_matches": True,
                            "evaluator_executability_status": (
                                "passed_registered_query_execution"
                            ),
                            "continuous_prediction_validity_status": (
                                "evaluated_descriptive_no_public_binary_threshold"
                            ),
                            "normalized_mae": 0.10 + 0.002 * arm_index,
                        },
                    }
                )
    dataset: dict[str, object] = {
        "schema_version": "chemworld-work-ii-formal-analysis-dataset-0.1",
        "formal_result": True,
        "status": "passed",
        "formal_preflight_sha256": formal_preflight_sha256,
        "retained_cell_count": 75,
        "cluster_contrast_count": 25,
        "state_counts": {"completed": 75, "right_censored": 0, "failed": 0},
        "cell_rows": cell_rows,
        "cluster_rows": cluster_rows,
        "errors": [],
    }
    dataset["dataset_sha256"] = canonical_json_sha256(dataset)
    return dataset


@pytest.fixture(scope="module")
def private_fixture() -> dict[str, object]:
    design = _load(DESIGN)
    task_ids = [str(row["task_id"]) for row in design["tasks"]]
    private_start = int(design["world_cohort"]["private_confirmation"]["namespace_start"])
    seal = {
        "schema_version": WORK_II_PRIVATE_SEAL_VERSION,
        "design_id": design["design_id"],
        "seal_nonce": "7" * 64,
        "task_world_seeds": {
            task_id: [private_start + task_index * 100 + index for index in range(5)]
            for task_index, task_id in enumerate(task_ids)
        },
    }
    design["world_cohort"]["private_confirmation"][
        "sealed_identity_commitment_sha256"
    ] = canonical_json_sha256(seal)
    actual_manifest = build_formal_preflight(ROOT, DESIGN, ANALYSIS)
    authorized_manifest = deepcopy(actual_manifest)
    authorized_manifest["status"] = "passed_execution_authorized"
    authorized_manifest["formal_execution_allowed"] = True
    authorized_manifest["blocking_requirements"] = []
    authorized_manifest["design_binding"] = {
        **authorized_manifest["design_binding"],
        "sha256": canonical_json_sha256(design),
    }
    authorized_manifest["preflight_sha256"] = canonical_json_sha256(
        {key: value for key, value in authorized_manifest.items() if key != "preflight_sha256"}
    )
    blocked_manifest = deepcopy(authorized_manifest)
    blocked_manifest["status"] = "passed_execution_blocked"
    blocked_manifest["formal_execution_allowed"] = False
    blocked_manifest["blocking_requirements"] = ["test authorization blocker"]
    public_analysis = build_confirmatory_analysis(
        _formal_dataset(
            task_ids,
            formal_preflight_sha256=authorized_manifest["preflight_sha256"],
        ),
        _load(ANALYSIS),
    )
    monkeypatch = pytest.MonkeyPatch()
    monkeypatch.setattr(private_module, "validate_formal_preflight", lambda _report: [])
    try:
        report = build_private_confirmation_preflight(
            public_manifest=authorized_manifest,
            public_analysis=public_analysis,
            design=design,
            seal=seal,
        )
        yield {
            "actual_manifest": actual_manifest,
            "design": design,
            "seal": seal,
            "blocked_manifest": blocked_manifest,
            "authorized_manifest": authorized_manifest,
            "public_analysis": public_analysis,
            "report": report,
        }
    finally:
        monkeypatch.undo()


def test_private_preflight_freezes_exact_denominators(
    private_fixture: dict[str, object],
) -> None:
    actual_manifest = private_fixture["actual_manifest"]
    assert "private_confirmation_contract" in actual_manifest
    assert all(
        "private_confirmation_contract_sha256" in cell
        for cell in actual_manifest["cells"]
    )
    report = private_fixture["report"]
    assert report["status"] == "passed_private_execution_blocked"
    assert report["private_execution_allowed"] is False
    assert report["blocking_requirements"] == list(PRIVATE_BLOCKING_REQUIREMENTS)
    assert report["provider_calls_executed"] == 0
    assert report["expected_counts"] == {
        "tasks": 5,
        "independent_task_world_clusters": 25,
        "participant_cells": 75,
        "complete_experiments": 300,
        "belief_checkpoints": 300,
        "provider_sessions": 75,
        "provider_attempts_initial_planned": 75,
        "provider_attempts_hard_cap": 150,
        "evaluator_truth_executions": 100,
        "blind_validation_executions": 450,
    }
    assert len(report["cells"]) == 75
    assert len({cell["world_cluster_id"] for cell in report["cells"]}) == 25
    assert len({cell["cell_key_sha256"] for cell in report["cells"]}) == 75


def test_private_preflight_is_deterministic_and_hides_seal_nonce(
    private_fixture: dict[str, object],
) -> None:
    first = private_fixture["report"]
    second = build_private_confirmation_preflight(
        public_manifest=private_fixture["authorized_manifest"],
        public_analysis=private_fixture["public_analysis"],
        design=private_fixture["design"],
        seal=private_fixture["seal"],
    )
    assert first == second
    assert validate_private_confirmation_preflight(
        first,
        public_manifest=private_fixture["authorized_manifest"],
        public_analysis=private_fixture["public_analysis"],
        design=private_fixture["design"],
        seal=private_fixture["seal"],
    ) == []
    serialized = json.dumps(first, sort_keys=True)
    assert str(private_fixture["seal"]["seal_nonce"]) not in serialized
    assert "seal_nonce" not in first


def test_private_preflight_rejects_blocked_public_manifest_and_tampering(
    private_fixture: dict[str, object],
) -> None:
    with pytest.raises(WorkIIPrivateConfirmationError, match="authorized public manifest"):
        build_private_confirmation_preflight(
            public_manifest=private_fixture["blocked_manifest"],
            public_analysis=private_fixture["public_analysis"],
            design=private_fixture["design"],
            seal=private_fixture["seal"],
        )
    tampered = deepcopy(private_fixture["public_analysis"])
    tampered["primary_H3"]["passed"] = False
    with pytest.raises(WorkIIPrivateConfirmationError, match="public confirmatory analysis"):
        build_private_confirmation_preflight(
            public_manifest=private_fixture["authorized_manifest"],
            public_analysis=tampered,
            design=private_fixture["design"],
            seal=private_fixture["seal"],
        )


def test_private_preflight_writer_is_private_and_write_once(
    private_fixture: dict[str, object],
    tmp_path: Path,
) -> None:
    output = tmp_path / "runs" / "private" / "preflight.json"
    write_private_preflight_once(tmp_path, output, private_fixture["report"])
    assert json.loads(output.read_text(encoding="utf-8")) == private_fixture["report"]
    with pytest.raises(FileExistsError):
        write_private_preflight_once(tmp_path, output, private_fixture["report"])
    with pytest.raises(WorkIIPrivateConfirmationError, match="runs/private"):
        write_private_preflight_once(
            tmp_path,
            tmp_path / "public-preflight.json",
            private_fixture["report"],
        )


def test_private_seal_rejects_duplicate_and_public_worlds(
    private_fixture: dict[str, object],
) -> None:
    duplicate = deepcopy(private_fixture["seal"])
    task_ids = list(duplicate["task_world_seeds"])
    duplicate["task_world_seeds"][task_ids[1]][0] = duplicate["task_world_seeds"][
        task_ids[0]
    ][0]
    assert "private seal identities are not unique and split-disjoint" in validate_private_seal(
        private_fixture["design"], duplicate
    )

    public_overlap = deepcopy(private_fixture["seal"])
    public_seed = next(
        iter(
            private_fixture["design"]["world_cohort"]["public_formal"][
                "task_world_seeds"
            ].values()
        )
    )[0]
    public_overlap["task_world_seeds"][task_ids[0]][0] = public_seed
    assert "private seal identities are not unique and split-disjoint" in validate_private_seal(
        private_fixture["design"], public_overlap
    )
