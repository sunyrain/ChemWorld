from __future__ import annotations

import json
import math
from copy import deepcopy
from pathlib import Path

import jsonschema
import numpy as np
import pytest

from chemworld.eval.provenance import canonical_json_sha256, file_sha256
from chemworld.eval.work_ii_ae_prior_qualification_v03 import (
    HYPOTHESES,
    AEPriorQualificationV03Error,
    _build_plan,
    _project_classifier_metrics,
    _require_phase_evidence,
    _require_report,
    _require_upstream_chain,
    _summarize_loci,
    build_phase_plan,
    classify_blind,
    dossier_variant,
    extract_registered_measurement,
    hypothesis_permutation,
    load_resume_prefix,
    score_all_hypotheses,
    select_descriptor_pair,
    select_screen_loci,
    validate_contract,
    validate_next_receipt,
    validate_plan,
)

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = (
    ROOT / "configs/benchmark/work_ii_ae_prior_distinguishability_v0.3_candidate.json"
)
SCHEMA_PATH = (
    ROOT / "src/chemworld/schemas/work_ii_ae_prior_qualification_v03_schema.json"
)


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_contract_schema_and_semantics() -> None:
    contract = _load(CONTRACT_PATH)
    jsonschema.Draft202012Validator(_load(SCHEMA_PATH)).validate(contract)
    assert validate_contract(ROOT, contract) == []


@pytest.mark.parametrize(
    ("key", "value"),
    [
        ("measurement_stage_id", "final-assay"),
        ("gate_endpoint_id", "yield"),
        ("target_field", "solvent"),
        ("classifier_secondary_endpoint_ids", ["yield"]),
        ("descriptor_whitelist", ["reference_panel_activity_floor"]),
    ],
)
def test_contract_rejects_locus_semantic_mutation(key: str, value: object) -> None:
    contract = _load(CONTRACT_PATH)
    contract["tasks"][2]["loci"][0][key] = value  # type: ignore[index]
    assert any("exact task/locus" in error for error in validate_contract(ROOT, contract))


def test_contract_rejects_neutral_id_pair_leak() -> None:
    contract = _load(CONTRACT_PATH)
    contract["tasks"][0]["loci"][0]["locus_id"] = "ae-locus-swap-0-3"  # type: ignore[index]
    errors = validate_contract(ROOT, contract)
    assert any("neutral" in error or "exact task/locus" in error for error in errors)


def test_four_phase_plans_have_exact_denominators_and_seed_intervals() -> None:
    contract = _load(CONTRACT_PATH)
    selected = {
        task["task_id"]: task["loci"][0]["locus_id"] for task in contract["tasks"]
    }
    plans = {
        phase: _build_plan(
            ROOT,
            CONTRACT_PATH,
            contract,
            phase,
            selected=selected if phase == "confirmation" else None,
        )
        for phase in (
            "classifier_fit",
            "classifier_validation",
            "prospective_screen",
            "confirmation",
        )
    }
    assert all(validate_plan(plan) == [] for plan in plans.values())
    assert {phase: len(plan["executions"]) for phase, plan in plans.items()} == {
        "classifier_fit": 14_400,
        "classifier_validation": 14_400,
        "prospective_screen": 1_200,
        "confirmation": 600,
    }
    assert all(
        len({row["observation_seed"] for row in plan["executions"]})
        == len(plan["executions"])
        for plan in plans.values()
    )
    fit = plans["classifier_fit"]
    assert all(
        1_000_000_000 <= row["world_seed"] <= 1_199_999_999
        for row in fit["executions"]
    )
    worlds = {(row["locus_id"], row["world_seed"]) for row in fit["executions"]}
    assert len(worlds) == 600
    seeds = {world[1] for world in worlds}
    assert len(seeds) == 600


def _self_hash(value: dict[str, object], key: str) -> dict[str, object]:
    value[key] = canonical_json_sha256(
        {item_key: item_value for item_key, item_value in value.items() if item_key != key}
    )
    return value


def _model(locus_id: str) -> dict[str, object]:
    model: dict[str, object] = {
        "schema_version": "chemworld-work-ii-ae-calibrated-residual-model-0.3",
        "classifier_id": "signed-ridge-calibrated-weighted-residual-v0.3",
        "locus_id": locus_id,
        "task_id": "synthetic-task",
        "target_field": "solvent",
        "descriptor_whitelist": ["x1", "x2", "x3"],
        "descriptor_center": [0.0, 0.0, 0.0],
        "descriptor_scale": [0.5, 0.5, 0.5],
        "descriptor_keep": [True, True, True],
        "ridge_alpha": 0.0001,
        "anchor_coefficients": [
            [[0.04], [0.025], [0.015]],
            [[0.035], [-0.02], [0.01]],
        ],
        "predictive_covariance_diagonal": [1.0e-4] * 6,
        "classification_metric_ids": ["yield"],
        "hypotheses": list(HYPOTHESES),
        "decision_thresholds": {
            "swap_evidence_min": 0.01,
            "h0_evidence_min": 0.01,
            "pair_evidence_min": 0.01,
        },
        "fit_world_clusters": 60,
        "target_fit_parameters": [],
        "score_name": "calibrated_weighted_residual_score",
        "scope": "four-category-reference-response-fingerprint-not-transfer-physics",
    }
    return _self_hash(model, "model_sha256")


def _fit_report(marker: str) -> dict[str, object]:
    contract = _load(CONTRACT_PATH)
    models = []
    for task in contract["tasks"]:
        for locus in task["loci"]:
            model = _model(locus["locus_id"])
            model.update(
                {
                    "task_id": task["task_id"],
                    "target_field": locus["target_field"],
                    "marker": marker,
                }
            )
            _self_hash(model, "model_sha256")
            models.append(model)
    report = {
        "schema_version": "chemworld-work-ii-ae-locus-report-0.3",
        "development_only": True,
        "phase": "classifier_fit",
        "status": "completed",
        "marker": marker,
        "denominators": {
            "primary_executions": 14_400,
            "completed_primary_executions": 14_400,
            "exact_replays_verified": 14_400,
        },
        "failures": [],
        "models": models,
    }
    return _self_hash(report, "report_sha256")


def _validation_report(fit_report: dict[str, object]) -> dict[str, object]:
    contract = _load(CONTRACT_PATH)
    confusion = {
        truth: {
            prediction: int(prediction == truth) * 60
            for prediction in (*HYPOTHESES, "abstain")
        }
        for truth in HYPOTHESES
    }
    report = {
        "schema_version": "chemworld-work-ii-ae-locus-report-0.3",
        "development_only": True,
        "phase": "classifier_validation",
        "status": "passed",
        "fit_report_sha256": fit_report["report_sha256"],
        "models_sha256": canonical_json_sha256(fit_report["models"]),
        "denominators": {
            "primary_executions": 14_400,
            "completed_primary_executions": 14_400,
            "exact_replays_verified": 14_400,
        },
        "failures": [],
        "locus_results": [
            {
                "locus_id": locus["locus_id"],
                "world_clusters": 60,
                "offline_cases": 420,
                "confusion": deepcopy(confusion),
                "passed": True,
            }
            for task in contract["tasks"]
            for locus in task["loci"]
        ],
    }
    return _self_hash(report, "report_sha256")


def _screen_report(
    fit_report: dict[str, object], validation_report: dict[str, object]
) -> dict[str, object]:
    contract = _load(CONTRACT_PATH)
    report = {
        "schema_version": "chemworld-work-ii-ae-locus-report-0.3",
        "development_only": True,
        "phase": "prospective_screen",
        "status": "completed",
        "fit_report_sha256": fit_report["report_sha256"],
        "validation_report_sha256": validation_report["report_sha256"],
        "denominators": {
            "primary_executions": 1_200,
            "completed_primary_executions": 1_200,
            "exact_replays_verified": 1_200,
        },
        "failures": [],
        "locus_results": [
            {
                "task_id": task["task_id"],
                "locus_id": locus["locus_id"],
                "worlds_total": 5,
                "classification_all_seven_correct_worlds": 5,
                "physical_gate_worlds": 5,
                "passed": True,
            }
            for task in contract["tasks"]
            for locus in task["loci"]
        ],
    }
    return _self_hash(report, "report_sha256")


def _aligned() -> dict[str, object]:
    # X=C.T, a symmetric four-point geometry with exact signed response recovery.
    return {
        "choices": {
            "solvent": [
                {
                    "action_value": category,
                    "anonymous_material_id": f"s{category}",
                    "nominal_properties": {
                        "x1": value[0], "x2": value[1], "x3": value[2]
                    },
                }
                for category, value in enumerate(
                    [
                        (1 / math.sqrt(2), 1 / math.sqrt(6), 1 / math.sqrt(12)),
                        (-1 / math.sqrt(2), 1 / math.sqrt(6), 1 / math.sqrt(12)),
                        (0.0, -2 / math.sqrt(6), 1 / math.sqrt(12)),
                        (0.0, 0.0, -3 / math.sqrt(12)),
                    ]
                )
            ]
        }
    }


def _observations(offsets: tuple[float, float] = (0.4, 0.5)) -> list[dict[str, object]]:
    x = np.asarray(
        [
            (1 / math.sqrt(2), 1 / math.sqrt(6), 1 / math.sqrt(12)),
            (-1 / math.sqrt(2), 1 / math.sqrt(6), 1 / math.sqrt(12)),
            (0.0, -2 / math.sqrt(6), 1 / math.sqrt(12)),
            (0.0, 0.0, -3 / math.sqrt(12)),
        ]
    )
    response = [
        x @ np.asarray([0.08, 0.05, 0.03]) + offsets[0],
        x @ np.asarray([0.07, -0.04, 0.02]) + offsets[1],
    ]
    return [
        {
            "anchor_id": anchor,
            "target_category": category,
            "replicate": replicate,
            "anchor_recipe": [float(anchor)],
            "metrics": {"yield": float(response[anchor][category])},
        }
        for anchor in range(2)
        for category in range(4)
        for replicate in range(3)
    ]


@pytest.mark.parametrize("truth", HYPOTHESES)
def test_classifier_recovers_h0_and_every_swap(truth: str) -> None:
    model = _model("ae-locus-synthetic")
    candidate = {
        "task_id": "synthetic-task",
        "locus_id": "ae-locus-synthetic",
        "target_field": "solvent",
        "descriptor_whitelist": ["x1", "x2", "x3"],
    }
    varied = dossier_variant(_aligned(), "solvent", candidate["descriptor_whitelist"], truth)
    result = classify_blind(
        {
            "dossier": varied,
            "task_id": candidate["task_id"],
            "locus_id": candidate["locus_id"],
            "target_field": candidate["target_field"],
            "anchor_ids": [0, 1],
            "anchor_recipes": {"0": [0.0], "1": [1.0]},
            "registered_observations": [
                {k: v for k, v in row.items() if k != "anchor_recipe"}
                for row in _observations()
            ],
            "calibration_model": model,
        }
    )
    assert result["predicted_hypothesis"] == truth


def test_anchor_intercept_shift_does_not_change_all_predictions() -> None:
    candidate = {
        "task_id": "synthetic-task",
        "locus_id": "ae-locus-synthetic",
        "target_field": "solvent",
        "descriptor_whitelist": ["x1", "x2", "x3"],
    }
    first = score_all_hypotheses(
        candidate=candidate,
        aligned_dossier=_aligned(),
        observations=_observations((0.4, 0.5)),
        model=_model(candidate["locus_id"]),
    )
    second = score_all_hypotheses(
        candidate=candidate,
        aligned_dossier=_aligned(),
        observations=_observations((0.6, 0.3)),
        model=_model(candidate["locus_id"]),
    )
    assert [x["prediction"]["predicted_hypothesis"] for x in first["cases"]] == [
        x["prediction"]["predicted_hypothesis"] for x in second["cases"]
    ]


def test_classifier_rejects_truth_and_target_sigma_injection() -> None:
    base = {
        "dossier": _aligned(),
        "task_id": "synthetic-task",
        "locus_id": "ae-locus-synthetic",
        "target_field": "solvent",
        "anchor_ids": [0, 1],
        "anchor_recipes": {"0": [0.0], "1": [1.0]},
        "registered_observations": [
            {k: v for k, v in row.items() if k != "anchor_recipe"}
            for row in _observations()
        ],
        "calibration_model": _model("ae-locus-synthetic"),
    }
    for key in ("truth_hypothesis", "observation_sigma"):
        attacked = deepcopy(base)
        attacked[key] = "secret"
        with pytest.raises(AEPriorQualificationV03Error, match=r"fields|forbidden"):
            classify_blind(attacked)


@pytest.mark.parametrize(
    ("key", "value"),
    [
        ("anchor_coefficients", [[[0.1]], [[0.1]]]),
        ("predictive_covariance_diagonal", [0.0] * 6),
        ("descriptor_scale", [0.0, 0.5, 0.5]),
        (
            "decision_thresholds",
            {"swap_evidence_min": -1.0, "h0_evidence_min": 0.0, "pair_evidence_min": 0.0},
        ),
    ],
)
def test_classifier_rejects_self_hashed_malformed_models(key: str, value: object) -> None:
    model = _model("ae-locus-synthetic")
    model[key] = value
    _self_hash(model, "model_sha256")
    classifier_input = {
        "dossier": _aligned(),
        "task_id": "synthetic-task",
        "locus_id": "ae-locus-synthetic",
        "target_field": "solvent",
        "anchor_ids": [0, 1],
        "anchor_recipes": {"0": [0.0], "1": [1.0]},
        "registered_observations": [
            {k: v for k, v in row.items() if k != "anchor_recipe"}
            for row in _observations()
        ],
        "calibration_model": model,
    }
    with pytest.raises(AEPriorQualificationV03Error, match="calibration"):
        classify_blind(classifier_input)


def test_non_gating_metrics_are_preserved_but_not_sent_to_classifier() -> None:
    observations = _observations()
    for row in observations:
        row["metrics"]["safety_risk"] = 0.9  # type: ignore[index]
    projected = _project_classifier_metrics(observations, ["yield"])
    assert all(set(row["metrics"]) == {"yield"} for row in projected)
    assert all("safety_risk" in row["metrics"] for row in observations)


def test_descriptor_pair_is_outcome_free_and_lexicographic_on_tie() -> None:
    assert select_descriptor_pair(_aligned(), "solvent", ["x1", "x2", "x3"]) == (0, 1)


def _record(operation: str, instrument: str | None = None, value: float = 0.4) -> dict[str, object]:
    observation = {"conversion": value, "product_in_organic": value}
    mask = {"conversion": True, "product_in_organic": True}
    return {
        "action": {"operation": operation, **({"instrument": instrument} if instrument else {})},
        "operation_type": operation,
        "instrument": instrument,
        "transaction_status": "committed",
        "step": 7,
        "operation_id": "op-7",
        "agent_visible_observation": {
            "views": {"tool_json": {"observation": observation, "observed_mask": mask}}
        },
    }


@pytest.mark.parametrize(
    ("task", "stage", "records", "metric", "expected"),
    [
        (
            "electrochemical-conversion",
            "final-assay",
            [_record("terminate"), _record("measure", "final_assay")],
            "conversion",
            1,
        ),
        (
            "reaction-to-crystallization",
            "reaction-post-quench-hplc",
            [_record("quench"), _record("measure", "hplc"), _record("seed_crystals")],
            "conversion",
            1,
        ),
        (
            "reaction-to-distillation",
            "reaction-post-quench-hplc",
            [_record("quench"), _record("measure", "hplc"), _record("evaporate")],
            "conversion",
            1,
        ),
        (
            "reaction-safety-constrained",
            "reaction-post-quench-hplc",
            [_record("quench"), _record("measure", "hplc"), _record("terminate")],
            "conversion",
            1,
        ),
        (
            "partition-discovery",
            "partition-post-settle-pre-separation-hplc",
            [_record("settle"), _record("measure", "hplc"), _record("separate_phase")],
            "product_in_organic",
            1,
        ),
    ],
)
def test_measurement_event_windows(
    task: str,
    stage: str,
    records: list[dict[str, object]],
    metric: str,
    expected: int,
) -> None:
    result = extract_registered_measurement(records, task, stage, [metric])
    assert result["matched_step_index"] == expected
    assert result["operation_id"] == "op-7"


@pytest.mark.parametrize(
    "attack", ["missing_boundary", "duplicate", "wrong_instrument", "mask_false", "nan"]
)
def test_measurement_event_windows_fail_closed(attack: str) -> None:
    records = [_record("quench"), _record("measure", "hplc"), _record("evaporate")]
    if attack == "missing_boundary":
        records.pop()
    elif attack == "duplicate":
        records.insert(2, _record("measure", "hplc"))
    elif attack == "wrong_instrument":
        records[1]["instrument"] = "gc"
    elif attack == "mask_false":
        tool_json = records[1]["agent_visible_observation"]["views"]["tool_json"]  # type: ignore[index]
        tool_json["observed_mask"]["conversion"] = False
    else:
        tool_json = records[1]["agent_visible_observation"]["views"]["tool_json"]  # type: ignore[index]
        tool_json["observation"]["conversion"] = math.nan
    with pytest.raises(AEPriorQualificationV03Error):
        extract_registered_measurement(
            records, "reaction-to-distillation", "reaction-post-quench-hplc", ["conversion"]
        )


def test_selection_has_variable_zero_to_five_task_denominator() -> None:
    contract = _load(CONTRACT_PATH)
    assert select_screen_loci(contract, [])["selected_task_count"] == 0
    results = [
        {"locus_id": task["loci"][0]["locus_id"], "passed": True}
        for task in contract["tasks"][:3]
    ]
    selection = select_screen_loci(contract, results)
    assert selection["selected_task_count"] == 3


def _validation_world(locus_id: str, wrong: bool = False) -> dict[str, object]:
    return {
        "locus_id": locus_id,
        "classification": {
            "any_definite_wrong": wrong,
            "all_seven_correct": not wrong,
            "cases": [
                {
                    "truth_hypothesis": truth,
                    "prediction": {
                        "predicted_hypothesis": (
                            "swap-0-1" if wrong and truth == "H0" else truth
                        )
                    },
                    "correct": not (wrong and truth == "H0"),
                }
                for truth in HYPOTHESES
            ],
        },
    }


def test_validation_cp_boundary_rejects_one_wrong_world_and_is_finite_at_all_wrong() -> None:
    contract = _load(CONTRACT_PATH)
    locus_id = contract["tasks"][0]["loci"][0]["locus_id"]
    clean = _summarize_loci(
        contract, "classifier_validation", [_validation_world(locus_id) for _ in range(60)]
    )[0]
    assert clean["passed"] is True
    one_wrong = _summarize_loci(
        contract,
        "classifier_validation",
        [_validation_world(locus_id, index == 0) for index in range(60)],
    )[0]
    assert one_wrong["passed"] is False
    all_wrong = _summarize_loci(
        contract,
        "classifier_validation",
        [_validation_world(locus_id, True) for _ in range(60)],
    )[0]
    assert all_wrong["any_definite_wrong_cp95_upper"] == 1.0


def test_screen_report_rejects_inconsistent_locus_counts() -> None:
    contract = _load(CONTRACT_PATH)
    loci = [
        {
            "task_id": task["task_id"],
            "locus_id": locus["locus_id"],
            "worlds_total": 5,
            "classification_all_seven_correct_worlds": 5,
            "physical_gate_worlds": 5,
            "passed": True,
        }
        for task in contract["tasks"]
        for locus in task["loci"]
    ]
    report = {
        "schema_version": "chemworld-work-ii-ae-locus-report-0.3",
        "development_only": True,
        "phase": "prospective_screen",
        "status": "completed",
        "denominators": {
            "primary_executions": 1200,
            "completed_primary_executions": 1200,
            "exact_replays_verified": 1200,
        },
        "failures": [],
        "locus_results": loci,
    }
    _self_hash(report, "report_sha256")
    _require_report(report, "prospective_screen")
    report["locus_results"][0]["worlds_total"] = 4
    _self_hash(report, "report_sha256")
    with pytest.raises(AEPriorQualificationV03Error, match="five-world"):
        _require_report(report, "prospective_screen")


def test_forged_passed_validation_without_raw_evidence_cannot_open_screen() -> None:
    fit_report = _fit_report("fit-a")
    validation_report = _validation_report(fit_report)
    with pytest.raises(AEPriorQualificationV03Error, match="raw evidence bundle"):
        build_phase_plan(
            ROOT,
            CONTRACT_PATH,
            "prospective_screen",
            fit_report=fit_report,
            validation_report=validation_report,
        )


def test_validation_rejects_substituted_fit_report() -> None:
    fit_a = _fit_report("fit-a")
    fit_b = _fit_report("fit-b")
    validation_a = _validation_report(fit_a)
    with pytest.raises(AEPriorQualificationV03Error, match="not bound"):
        _require_upstream_chain(fit_report=fit_b, validation_report=validation_a)


def test_validation_plan_binding_rejects_fit_substitution() -> None:
    contract = _load(CONTRACT_PATH)
    fit_a = _fit_report("fit-a")
    fit_b = _fit_report("fit-b")
    validation_plan_a = _build_plan(
        ROOT,
        CONTRACT_PATH,
        contract,
        "classifier_validation",
        upstream={"fit_report_sha256": fit_a["report_sha256"]},
    )
    with pytest.raises(AEPriorQualificationV03Error, match="deterministic reconstruction"):
        _require_phase_evidence(
            root=ROOT,
            contract_path=CONTRACT_PATH,
            contract=contract,
            phase="classifier_validation",
            plan=validation_plan_a,
            receipts=[],
            report=_validation_report(fit_b),
            fit_report=fit_b,
        )


def test_confirmation_chain_rejects_screen_from_other_validation() -> None:
    fit_report = _fit_report("fit-a")
    validation_a = _validation_report(fit_report)
    validation_b = deepcopy(validation_a)
    validation_b["marker"] = "validation-b"
    _self_hash(validation_b, "report_sha256")
    screen_a = _screen_report(fit_report, validation_a)
    with pytest.raises(AEPriorQualificationV03Error, match="upstream chain"):
        _require_upstream_chain(
            fit_report=fit_report,
            validation_report=validation_b,
            screen_report=screen_a,
        )


def test_permutation_convention_is_self_inverse() -> None:
    for hypothesis in HYPOTHESES:
        permutation = hypothesis_permutation(hypothesis)
        assert tuple(permutation[index] for index in permutation) == (0, 1, 2, 3)


def _completed_receipt(
    plan: dict[str, object], index: int, output: Path, *, resumed: bool = False
) -> dict[str, object]:
    row = plan["executions"][index]  # type: ignore[index]
    relative = (
        Path("resume-executions") / "1" / str(index) / "trajectory.jsonl"
        if resumed
        else Path("executions") / str(index) / "trajectory.jsonl"
    )
    trajectory = output / relative
    trajectory.parent.mkdir(parents=True, exist_ok=True)
    trajectory.write_text('{"step": 1}\n', encoding="utf-8")
    receipt = {
        key: deepcopy(row[key])
        for key in (
            "execution_index",
            "execution_id",
            "phase",
            "task_id",
            "locus_id",
            "world_index",
            "world_seed",
            "anchor_id",
            "target_category",
            "replicate",
            "anchor_recipe",
            "measurement_stage_id",
        )
    }
    receipt.update(
        {
            "schema_version": "chemworld-work-ii-ae-locus-receipt-0.3",
            "plan_sha256": plan["plan_sha256"],
            "provider_call_count": 0,
            "status": "completed",
            "failure": None,
            "measurement": {
                "measurement_stage_id": row["measurement_stage_id"],
                "metrics": dict.fromkeys(row["measured_metric_ids"], 0.5),
            },
            "classification_metrics": dict.fromkeys(
                row["classification_metric_ids"], 0.5
            ),
            "non_gating_secondary_metrics": dict.fromkeys(
                row["non_gating_secondary_metric_ids"], 0.5
            ),
            "exact_replay": {"verified": True},
            "trajectory": {
                "path": relative.as_posix(),
                "sha256": file_sha256(trajectory),
            },
        }
    )
    return _self_hash(receipt, "receipt_sha256")


def _resume_fixture(tmp_path: Path) -> tuple[Path, dict[str, object], dict[str, object]]:
    contract = _load(CONTRACT_PATH)
    plan = _build_plan(ROOT, CONTRACT_PATH, contract, "classifier_fit")
    output = tmp_path / "run"
    (output / "receipts").mkdir(parents=True)
    (output / "plan.json").write_text(json.dumps(plan), encoding="utf-8")
    receipt = _completed_receipt(plan, 0, output)
    (output / "receipts" / "0.json").write_text(
        json.dumps(receipt), encoding="utf-8"
    )
    return output, plan, receipt


def test_resume_accepts_validated_prefix_and_one_orphan_next_execution(
    tmp_path: Path,
) -> None:
    output, plan, receipt = _resume_fixture(tmp_path)
    orphan = output / "executions" / "1" / "trajectory.jsonl"
    orphan.parent.mkdir(parents=True)
    orphan.write_text('{"partial": true}\n', encoding="utf-8")
    assert load_resume_prefix(output, plan, minimum_quiescent_seconds=0) == [receipt]
    assert validate_next_receipt(plan, 1, _completed_receipt(plan, 1, output, resumed=True)) == []


@pytest.mark.parametrize("attack", ["plan", "gap", "trajectory", "platform", "orphan"])
def test_resume_rejects_mutation_and_non_prefix_state(
    tmp_path: Path, attack: str
) -> None:
    output, plan, receipt = _resume_fixture(tmp_path)
    if attack == "plan":
        stored = json.loads((output / "plan.json").read_text(encoding="utf-8"))
        stored["participant_provider_calls"] = 1
        (output / "plan.json").write_text(json.dumps(stored), encoding="utf-8")
    elif attack == "gap":
        (output / "receipts" / "0.json").rename(output / "receipts" / "1.json")
    elif attack == "trajectory":
        (output / receipt["trajectory"]["path"]).write_text(  # type: ignore[index]
            "tampered\n", encoding="utf-8"
        )
    elif attack == "platform":
        receipt["status"] = "platform_failure"
        receipt["failure"] = {"type": "Error", "message": "boom"}
        receipt["measurement"] = None
        receipt["classification_metrics"] = None
        receipt["non_gating_secondary_metrics"] = None
        receipt["exact_replay"] = None
        _self_hash(receipt, "receipt_sha256")
        (output / "receipts" / "0.json").write_text(
            json.dumps(receipt), encoding="utf-8"
        )
    else:
        orphan = output / "executions" / "2" / "trajectory.jsonl"
        orphan.parent.mkdir(parents=True)
        orphan.write_text('{"partial": true}\n', encoding="utf-8")
    with pytest.raises(AEPriorQualificationV03Error):
        load_resume_prefix(output, plan, minimum_quiescent_seconds=0)


def test_resume_rejects_non_quiescent_active_output(tmp_path: Path) -> None:
    output, plan, _ = _resume_fixture(tmp_path)
    with pytest.raises(AEPriorQualificationV03Error, match="not quiescent"):
        load_resume_prefix(output, plan, minimum_quiescent_seconds=60)
