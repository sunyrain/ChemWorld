from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

import pytest

import chemworld.eval.work_ii_ae_prior_qualification as qualification_module
from chemworld.eval.provenance import (
    canonical_json_sha256,
    git_source_commit,
)
from chemworld.eval.work_ii_ae_prior_qualification import (
    AE_MATERIAL_SOURCE_EXCLUSIONS,
    AE_MATERIAL_SOURCE_ROOTS,
    AE_SOURCE_BINDING_VERSION,
    build_qualification_plan,
    build_qualification_report,
    validate_qualification_plan,
    validate_qualification_report,
)
from chemworld.eval.work_ii_source_binding import work_ii_material_tree_sha256

ROOT = Path(__file__).resolve().parents[1]
DESIGN_PATH = ROOT / "configs/benchmark/work_ii_formal_design_v0.1.json"


def _design() -> dict[str, object]:
    return json.loads(DESIGN_PATH.read_text(encoding="utf-8"))


def _rehash(payload: dict[str, object], field: str) -> None:
    payload.pop(field, None)
    payload[field] = canonical_json_sha256(payload)


def _clean_source_binding() -> dict[str, object]:
    return {
        "schema_version": AE_SOURCE_BINDING_VERSION,
        "tested_commit": git_source_commit(ROOT),
        "worktree_clean_before_execution": True,
        "material_tree": {
            "relative_roots": list(AE_MATERIAL_SOURCE_ROOTS),
            "excluded_relative_paths": list(AE_MATERIAL_SOURCE_EXCLUSIONS),
            "sha256": work_ii_material_tree_sha256(
                ROOT,
                relative_roots=AE_MATERIAL_SOURCE_ROOTS,
                excluded_relative_paths=AE_MATERIAL_SOURCE_EXCLUSIONS,
            ),
        },
    }


def _plan() -> dict[str, object]:
    return build_qualification_plan(
        ROOT,
        DESIGN_PATH,
        source_binding=_clean_source_binding(),
    )


def _synthetic_receipts(
    plan: dict[str, object], *, separated: bool = True
) -> list[dict[str, object]]:
    receipts: list[dict[str, object]] = []
    for row in plan["executions"]:
        metric_value = 0.30 if separated and row["side"] == "right" else 0.10
        metrics = dict.fromkeys(row["registered_metric_ids"], metric_value)
        receipt = {
            key: deepcopy(row[key])
            for key in (
                "execution_index",
                "execution_id",
                "pair_id",
                "task_id",
                "world_seed",
                "region_id",
                "background_coordinate",
                "replicate_index",
                "side",
                "target_field",
                "target_coordinate",
                "target_category",
                "registered_metric_ids",
                "observation_seed",
                "observation_noise_namespace",
                "recipe_sha256",
            )
        }
        receipt.update(
            {
                "provider_call_count": 0,
                "status": "completed",
                "registered_metrics": metrics,
                "exact_replay": {"verified": True},
                "trajectory": {
                    "path": f"executions/{row['execution_index']}/trajectory.jsonl",
                    "sha256": "a" * 64,
                },
                "failure": None,
            }
        )
        _rehash(receipt, "receipt_sha256")
        receipts.append(receipt)
    return receipts


def test_plan_freezes_exact_five_task_cartesian_qualification() -> None:
    design = _design()
    plan = _plan()

    assert validate_qualification_plan(ROOT, plan, design) == []
    assert plan["denominators"] == {
        "tasks": 5,
        "task_worlds": 25,
        "regions": 50,
        "paired_noise_replicates": 150,
        "evaluator_executions": 300,
        "registered_metric_values": 1020,
        "paired_metric_differences": 510,
    }
    assert plan["participant_provider_calls"] == 0
    assert plan["participant_outcomes_read"] is False
    assert plan["source_binding"]["tested_commit"]
    assert plan["source_binding"]["worktree_clean_before_execution"] is True
    assert len(plan["source_binding"]["material_tree"]["sha256"]) == 64


def test_evidence_registration_files_are_excluded_from_ae_material_tree() -> None:
    assert "configs/current.json" in AE_MATERIAL_SOURCE_EXCLUSIONS
    assert (
        "configs/benchmark/work_ii_c2_admission_manifest_v0.1.json"
        in AE_MATERIAL_SOURCE_EXCLUSIONS
    )


def test_source_binding_accepts_ancestor_but_rejects_stale_material_tree(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    design = _design()
    plan = _plan()
    ancestor = "a" * 40
    descendant = "b" * 40
    plan["source_binding"]["tested_commit"] = ancestor
    _rehash(plan, "plan_sha256")
    monkeypatch.setattr(qualification_module, "git_source_commit", lambda root: descendant)
    monkeypatch.setattr(
        qualification_module,
        "_commit_is_ancestor",
        lambda root, tested, current: (tested == ancestor and current == descendant, None),
    )

    assert validate_qualification_plan(ROOT, plan, design) == []

    plan["source_binding"]["material_tree"]["sha256"] = "0" * 64
    _rehash(plan, "plan_sha256")
    assert any(
        "material-source tree is stale" in error
        for error in validate_qualification_plan(ROOT, plan, design)
    )


def test_trajectory_commit_must_match_bound_runtime() -> None:
    binding = {"tested_commit": "a" * 40}
    assert qualification_module._validate_trajectory_commit(
        [{"agent_metadata": {"git_commit": "a" * 40}}], binding
    ) == []
    assert qualification_module._validate_trajectory_commit(
        [{"agent_metadata": {"git_commit": "b" * 40}}], binding
    ) == ["trajectory commit does not match the A-E qualification tested commit"]


def test_plan_validator_rejects_rehashed_config_and_recipe_tampering() -> None:
    design = _design()
    plan = _plan()

    stale_config = deepcopy(plan)
    stale_config["campaign_config_bindings"][0]["sha256"] = "0" * 64
    _rehash(stale_config, "plan_sha256")
    assert any(
        "campaign config binding is stale" in error
        for error in validate_qualification_plan(ROOT, stale_config, design)
    )

    changed_recipe = deepcopy(plan)
    changed_recipe["executions"][0]["target_category"] = 3
    _rehash(changed_recipe, "plan_sha256")
    assert any(
        "frozen cartesian recipe contract" in error
        for error in validate_qualification_plan(ROOT, changed_recipe, design)
    )


def test_report_validator_recalculates_thresholds_and_all_aggregations() -> None:
    design = _design()
    plan = _plan()
    report = build_qualification_report(plan, _synthetic_receipts(plan), design)

    assert report["status"] == "passed"
    assert validate_qualification_report(ROOT, report, design) == []
    assert len(report["region_results"]) == 50
    assert len(report["world_results"]) == 25
    assert len(report["task_results"]) == 5
    assert len(report["execution_receipt_bindings"]) == 300

    threshold_tamper = deepcopy(report)
    threshold_tamper["region_results"][0]["mean_metric_vector_separation"] = 0.0
    _rehash(threshold_tamper, "report_sha256")
    assert any(
        "region checks mismatch" in error
        for error in validate_qualification_report(ROOT, threshold_tamper, design)
    )

    aggregate_tamper = deepcopy(report)
    aggregate_tamper["world_results"][0]["passed_region_count"] = 1
    _rehash(aggregate_tamper, "report_sha256")
    assert any(
        "world aggregation mismatch" in error
        for error in validate_qualification_report(ROOT, aggregate_tamper, design)
    )


def test_scientifically_failed_but_consistent_report_is_structurally_valid() -> None:
    design = _design()
    plan = _plan()
    report = build_qualification_report(
        plan,
        _synthetic_receipts(plan, separated=False),
        design,
    )

    assert report["status"] == "failed"
    assert report["failures"]
    assert report["denominators"]["passed_regions"] == 0
    assert validate_qualification_report(ROOT, report, design) == []


def test_execute_qualification_validates_the_written_report_evidence_path(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source_binding = {"tested_commit": "a" * 40}
    plan = {
        "executions": [],
        "plan_sha256": "a" * 64,
        "source_binding": source_binding,
    }
    report = {
        "status": "failed",
        "failures": [{"check": "scientific_threshold"}],
        "denominators": {
            "tasks": 5,
            "task_worlds": 25,
            "regions": 50,
            "paired_noise_replicates": 150,
            "evaluator_executions": 300,
            "passed_tasks": 0,
            "passed_task_worlds": 0,
            "passed_regions": 0,
        },
    }
    observed: dict[str, Path] = {}
    monkeypatch.setattr(
        qualification_module,
        "build_qualification_plan",
        lambda root, design_path, **kwargs: plan,
    )
    monkeypatch.setattr(
        qualification_module,
        "build_qualification_report",
        lambda plan, receipts, design: report,
    )

    def _validate(
        root: Path,
        candidate: dict[str, object],
        design: dict[str, object],
        *,
        report_path: Path | None = None,
    ) -> list[str]:
        del root, candidate, design
        assert report_path is not None and report_path.is_file()
        observed["report_path"] = report_path
        return []

    monkeypatch.setattr(qualification_module, "validate_qualification_report", _validate)
    monkeypatch.setattr(qualification_module, "validate_qualification_plan", lambda *args: [])
    monkeypatch.setattr(qualification_module, "_require_clean_launch", lambda root: None)
    monkeypatch.setattr(
        qualification_module, "_source_binding", lambda root: source_binding
    )
    monkeypatch.setattr(
        qualification_module, "git_source_commit", lambda root: "a" * 40
    )
    monkeypatch.setattr(qualification_module, "git_worktree_dirty", lambda root: False)
    output_root = tmp_path / "qualification"
    result = qualification_module.execute_qualification(
        ROOT,
        DESIGN_PATH,
        output_root,
    )

    assert result["status"] == "failed"
    assert observed["report_path"] == output_root / "report.json"
    assert (output_root / "summary.md").is_file()


def test_execute_qualification_rejects_dirty_launch_without_creating_output(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(qualification_module, "git_worktree_dirty", lambda root: True)
    output_root = tmp_path / "qualification"

    with pytest.raises(
        qualification_module.AEPriorQualificationError,
        match="requires a clean worktree",
    ):
        qualification_module.execute_qualification(ROOT, DESIGN_PATH, output_root)

    assert not output_root.exists()


def test_execute_qualification_validates_plan_before_creating_output(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source_binding = {"tested_commit": "a" * 40}
    monkeypatch.setattr(qualification_module, "_require_clean_launch", lambda root: None)
    monkeypatch.setattr(
        qualification_module, "_source_binding", lambda root: source_binding
    )
    monkeypatch.setattr(
        qualification_module, "git_source_commit", lambda root: "a" * 40
    )

    def _fail_plan(*args: object, **kwargs: object) -> dict[str, object]:
        raise qualification_module.AEPriorQualificationError("invalid frozen plan")

    monkeypatch.setattr(qualification_module, "build_qualification_plan", _fail_plan)
    output_root = tmp_path / "qualification"

    with pytest.raises(
        qualification_module.AEPriorQualificationError,
        match="invalid frozen plan",
    ):
        qualification_module.execute_qualification(ROOT, DESIGN_PATH, output_root)

    assert not output_root.exists()


def test_execution_progress_reports_elapsed_throughput_and_eta(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    source_binding = {"tested_commit": "a" * 40}
    plan = {
        "executions": [{"task_id": "task", "world_seed": 7}],
        "plan_sha256": "b" * 64,
        "source_binding": source_binding,
    }
    report = {
        "status": "failed",
        "failures": [{"check": "scientific_threshold"}],
        "denominators": {
            "tasks": 5,
            "task_worlds": 25,
            "regions": 50,
            "paired_noise_replicates": 150,
            "evaluator_executions": 300,
            "passed_tasks": 0,
            "passed_task_worlds": 0,
            "passed_regions": 0,
        },
    }
    monkeypatch.setattr(qualification_module, "_require_clean_launch", lambda root: None)
    monkeypatch.setattr(
        qualification_module, "_source_binding", lambda root: source_binding
    )
    monkeypatch.setattr(
        qualification_module, "git_source_commit", lambda root: "a" * 40
    )
    monkeypatch.setattr(qualification_module, "git_worktree_dirty", lambda root: False)
    monkeypatch.setattr(
        qualification_module,
        "build_qualification_plan",
        lambda root, design_path, **kwargs: plan,
    )
    monkeypatch.setattr(qualification_module, "validate_qualification_plan", lambda *args: [])
    monkeypatch.setattr(
        qualification_module,
        "execute_one",
        lambda root, plan, row, output: {"status": "completed"},
    )
    monkeypatch.setattr(
        qualification_module,
        "build_qualification_report",
        lambda plan, receipts, design: report,
    )
    monkeypatch.setattr(
        qualification_module,
        "validate_qualification_report",
        lambda *args, **kwargs: [],
    )
    ticks = iter((100.0, 102.0))
    monkeypatch.setattr(qualification_module.time, "perf_counter", lambda: next(ticks))

    qualification_module.execute_qualification(
        ROOT,
        DESIGN_PATH,
        tmp_path / "qualification",
    )

    progress = json.loads(capsys.readouterr().out.strip())
    assert progress["elapsed_s"] == 2.0
    assert progress["throughput_executions_per_minute"] == 30.0
    assert progress["eta_s"] == 0.0
