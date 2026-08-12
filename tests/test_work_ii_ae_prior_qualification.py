from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace

import pytest

import chemworld.eval.work_ii_ae_prior_qualification as qualification_module
from chemworld.eval.provenance import (
    canonical_json_sha256,
    git_source_commit,
)
from chemworld.eval.work_ii_ae_prior_qualification import (
    build_qualification_plan,
    build_qualification_report,
    validate_qualification_plan,
    validate_qualification_report,
)
from chemworld.eval.work_ii_execution_mode import ExecutionMode

ROOT = Path(__file__).resolve().parents[1]
DESIGN_PATH = ROOT / "configs/benchmark/work_ii_formal_design_v0.1.json"


def _design() -> dict[str, object]:
    return json.loads(DESIGN_PATH.read_text(encoding="utf-8"))


def _rehash(payload: dict[str, object], field: str) -> None:
    payload.pop(field, None)
    payload[field] = canonical_json_sha256(payload)


def _plan() -> dict[str, object]:
    return build_qualification_plan(
        ROOT,
        DESIGN_PATH,
        execution_context=_release_execution_envelope(),
    )


def _development_execution_envelope() -> dict[str, object]:
    return {
        "execution_mode": "development",
        "evidence_status": "development_only",
        "release_eligible": False,
        "c2_admission_authorized": False,
        "tested_commit": None,
        "freeze_id": None,
        "release_manifest_sha256": None,
        "execution_surface_sha256": None,
    }


def _release_execution_envelope() -> dict[str, object]:
    return {
        "execution_mode": "release",
        "evidence_status": "release_candidate",
        "release_eligible": True,
        "c2_admission_authorized": True,
        "tested_commit": git_source_commit(ROOT),
        "freeze_id": "3" * 64,
        "release_manifest_sha256": "1" * 64,
        "execution_surface_sha256": "2" * 64,
    }


def _mock_execution_context(
    monkeypatch: pytest.MonkeyPatch, envelope: dict[str, object]
) -> None:
    mode = ExecutionMode(str(envelope["execution_mode"]))
    monkeypatch.setattr(
        qualification_module,
        "prepare_execution_context",
        lambda *args, **kwargs: SimpleNamespace(mode=mode),
    )
    monkeypatch.setattr(
        qualification_module,
        "build_execution_envelope",
        lambda context: deepcopy(envelope),
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
    assert plan["execution_context"]["tested_commit"]
    assert plan["execution_context"]["c2_admission_authorized"] is True
    assert "source_binding" not in plan
    assert "c2_source_binding" not in plan


def test_development_plan_preserves_science_but_cannot_be_admitted() -> None:
    design = _design()
    plan = build_qualification_plan(
        ROOT,
        DESIGN_PATH,
        execution_context=_development_execution_envelope(),
    )

    assert validate_qualification_plan(ROOT, plan, design) == []
    assert plan["development_only"] is True
    assert plan["denominators"]["evaluator_executions"] == 300
    assert "source_binding" not in plan
    assert "c2_source_binding" not in plan
    assert plan["execution_context"]["c2_admission_authorized"] is False


def test_development_plan_rejects_release_eligibility_tampering() -> None:
    plan = build_qualification_plan(
        ROOT,
        DESIGN_PATH,
        execution_context=_development_execution_envelope(),
    )
    plan["execution_context"]["release_eligible"] = True
    _rehash(plan, "plan_sha256")

    assert any(
        "development envelope has release bindings or admission" in error
        for error in validate_qualification_plan(ROOT, plan, _design())
    )


def test_release_plan_rejects_legacy_source_bindings() -> None:
    plan = _plan()
    plan["source_binding"] = {"tested_commit": "a" * 40}
    _rehash(plan, "plan_sha256")

    assert "A-E qualification plan contains legacy source bindings" in (
        validate_qualification_plan(ROOT, plan, _design())
    )


def test_trajectory_commit_must_match_bound_runtime() -> None:
    binding = {"tested_commit": "a" * 40}
    assert qualification_module._validate_trajectory_commit(
        [{"agent_metadata": {"git_commit": "a" * 40}}], binding
    ) == []
    assert qualification_module._validate_trajectory_commit(
        [{"agent_metadata": {"git_commit": "b" * 40}}], binding
    ) == ["trajectory commit does not match the A-E release execution commit"]


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
    development = _development_execution_envelope()
    _mock_execution_context(monkeypatch, development)
    plan = {
        "executions": [],
        "plan_sha256": "a" * 64,
        "execution_context": development,
        "development_only": True,
    }
    report = {
        "status": "failed",
        "execution_context": development,
        "development_only": True,
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
    output_root = tmp_path / "qualification"
    result = qualification_module.execute_qualification(
        ROOT,
        DESIGN_PATH,
        output_root,
    )

    assert result["status"] == "failed"
    assert observed["report_path"] == output_root / "report.json"
    assert (output_root / "summary.md").is_file()


def test_execute_qualification_rejects_invalid_release_context_without_output(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        qualification_module,
        "prepare_execution_context",
        lambda *args, **kwargs: (_ for _ in ()).throw(
            ValueError("release mode requires a clean worktree")
        ),
    )
    output_root = tmp_path / "qualification"

    with pytest.raises(
        qualification_module.AEPriorQualificationError,
        match="requires a clean worktree",
    ):
        qualification_module.execute_qualification(
            ROOT,
            DESIGN_PATH,
            output_root,
            execution_mode=ExecutionMode.RELEASE,
            release_manifest=tmp_path / "release.json",
        )

    assert not output_root.exists()


def test_execute_qualification_validates_plan_before_creating_output(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _mock_execution_context(monkeypatch, _development_execution_envelope())

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
    development = _development_execution_envelope()
    _mock_execution_context(monkeypatch, development)
    plan = {
        "executions": [{"task_id": "task", "world_seed": 7}],
        "plan_sha256": "b" * 64,
        "execution_context": development,
        "development_only": True,
    }
    report = {
        "status": "failed",
        "execution_context": development,
        "development_only": True,
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
