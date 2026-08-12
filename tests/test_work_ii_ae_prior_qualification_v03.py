from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

import jsonschema
import pytest

from chemworld.eval.work_ii_ae_prior_qualification_v03 import (
    SELECTION_VERSION,
    AEPriorQualificationV03Error,
    blind_classify_transposition,
    build_confirmation_plan,
    build_screen_plan,
    moved_pair,
    score_blind_world,
    select_screen_candidates,
    validate_contract,
    validate_phase_progress,
    validate_plan,
    validate_receipt_denominator,
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


def _synthetic_dossier(permutation: tuple[int, int, int, int]) -> dict[str, object]:
    descriptor_a = (0.0, 0.3, 1.1, 2.9)
    descriptor_b = (-0.2, 0.7, 1.2, 4.0)
    return {
        "choices": {
            "solvent": [
                {
                    "action_value": category,
                    "nominal_properties": {
                        "descriptor_a": descriptor_a[source],
                        "descriptor_b": descriptor_b[source],
                    },
                }
                for category, source in enumerate(permutation)
            ]
        }
    }


def _synthetic_observations() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    offsets = (-0.006, 0.0, 0.006)
    response = (0.10, 0.18, 0.45, 0.80)
    for anchor in range(2):
        for category in range(4):
            for replicate, offset in enumerate(offsets):
                rows.append(
                    {
                        "anchor_id": anchor,
                        "target_category": category,
                        "replicate": replicate,
                        "metrics": {
                            "yield": response[category] + 0.02 * anchor + offset
                        },
                    }
                )
    return rows


def _synthetic_sigma() -> dict[str, dict[str, dict[str, float]]]:
    return {
        str(anchor): {str(category): {"yield": 0.006} for category in range(4)}
        for anchor in range(2)
    }


def test_contract_matches_schema_and_semantics() -> None:
    contract = _load(CONTRACT_PATH)
    jsonschema.Draft202012Validator(_load(SCHEMA_PATH)).validate(contract)
    assert validate_contract(ROOT, contract) == []


def test_contract_rejects_seed_collision_with_v02() -> None:
    contract = _load(CONTRACT_PATH)
    contract["cohorts"]["candidate_screen"]["task_world_seeds"][  # type: ignore[index]
        "electrochemical-conversion"
    ][0] = 934334899
    errors = validate_contract(ROOT, contract)
    assert any("not the frozen five" in error or "collides" in error for error in errors)


def test_contract_rejects_unsupported_locus_before_execution() -> None:
    contract = _load(CONTRACT_PATH)
    contract["tasks"][0]["candidates"][0]["target_field"] = "temperature"  # type: ignore[index]
    errors = validate_contract(ROOT, contract)
    assert any("unsupported candidate locus" in error for error in errors)


def test_screen_plan_has_exact_denominator_and_unique_seed_phases() -> None:
    plan = build_screen_plan(ROOT, CONTRACT_PATH)
    assert validate_plan(plan) == []
    assert len(plan["executions"]) == 1200
    coordinates = {
        (
            row["task_id"],
            row["candidate_id"],
            row["world_seed"],
            row["anchor_id"],
            row["target_category"],
            row["replicate"],
        )
        for row in plan["executions"]
    }
    assert len(coordinates) == 1200
    assert {row["phase"] for row in plan["executions"]} == {"candidate_screen"}


def test_confirmation_requires_all_five_frozen_selections() -> None:
    incomplete = {
        "schema_version": SELECTION_VERSION,
        "selected_candidate_ids": {"electrochemical-conversion": "solvent-swap-0-3"},
    }
    with pytest.raises(AEPriorQualificationV03Error, match="registered screen rule"):
        contract = _load(CONTRACT_PATH)
        results = _all_passing_screen_results(contract)
        report = {
            "schema_version": "chemworld-work-ii-ae-prior-candidate-report-0.3",
            "phase": "candidate_screen",
            "development_only": True,
            "world_results": results,
        }
        build_confirmation_plan(ROOT, CONTRACT_PATH, incomplete, report)


def test_confirmation_plan_is_600_and_seed_disjoint() -> None:
    contract = _load(CONTRACT_PATH)
    results = _all_passing_screen_results(contract)
    selection = select_screen_candidates(contract, results)
    report = {
        "schema_version": "chemworld-work-ii-ae-prior-candidate-report-0.3",
        "phase": "candidate_screen",
        "development_only": True,
        "world_results": results,
    }
    screen = build_screen_plan(ROOT, CONTRACT_PATH)
    confirmation = build_confirmation_plan(ROOT, CONTRACT_PATH, selection, report)
    assert validate_plan(confirmation) == []
    assert len(confirmation["executions"]) == 600
    assert {row["world_seed"] for row in screen["executions"]}.isdisjoint(
        {row["world_seed"] for row in confirmation["executions"]}
    )


def test_blind_classifier_identifies_swap_without_truth_input() -> None:
    result = blind_classify_transposition(
        dossier=_synthetic_dossier((3, 1, 2, 0)),
        task_id="synthetic-task",
        target_field="solvent",
        anchor_ids=[0, 1],
        support_observations=_synthetic_observations(),
        observation_sigma=_synthetic_sigma(),
    )
    assert result["decision"] == "pair"
    assert result["predicted_pair"] == [0, 3]
    assert result["nll_margin"] >= 2.0
    assert len(result["hypothesis_nll"]) == 7


def test_blind_classifier_rejects_forbidden_nested_input() -> None:
    dossier = _synthetic_dossier((3, 1, 2, 0))
    dossier["world_parameters"] = {"secret": 1}
    with pytest.raises(AEPriorQualificationV03Error, match="forbidden"):
        blind_classify_transposition(
            dossier=dossier,
            task_id="synthetic-task",
            target_field="solvent",
            anchor_ids=[0, 1],
            support_observations=_synthetic_observations(),
            observation_sigma=_synthetic_sigma(),
        )


def test_blind_classifier_abstains_when_margin_is_insufficient() -> None:
    rows = _synthetic_observations()
    for row in rows:
        row["metrics"] = {"yield": 0.5}
    result = blind_classify_transposition(
        dossier=_synthetic_dossier((3, 1, 2, 0)),
        task_id="synthetic-task",
        target_field="solvent",
        anchor_ids=[0, 1],
        support_observations=rows,
        observation_sigma=_synthetic_sigma(),
    )
    assert result["decision"] == "abstain"
    assert result["predicted_pair"] is None


def test_truth_is_used_only_by_scoring_wrapper() -> None:
    result = score_blind_world(
        dossier=_synthetic_dossier((3, 1, 2, 0)),
        task_id="synthetic-task",
        target_field="solvent",
        primary_endpoint_ids=["yield"],
        observations=_synthetic_observations(),
        true_pair=[0, 3],
        thresholds={
            "minimum_classifier_nll_margin": 2.0,
            "minimum_absolute_primary_endpoint_separation": 0.05,
            "minimum_primary_endpoint_signal_to_noise_ratio": 2.0,
        },
        sigma_floor=1.0e-6,
    )
    assert result["classifier_correct"] is True
    assert result["passed"] is True
    assert "true_pair" not in result["classification"]


def test_selection_uses_priority_not_effect_size() -> None:
    contract = _load(CONTRACT_PATH)
    results = _all_passing_screen_results(contract)
    selection = select_screen_candidates(contract, results)
    assert selection["all_tasks_selected"] is True
    for task in contract["tasks"]:
        expected = min(
            task["candidates"],
            key=lambda item: (item["scientific_priority"], item["candidate_id"]),
        )["candidate_id"]
        assert selection["selected_candidate_ids"][task["task_id"]] == expected


def _all_passing_screen_results(
    contract: dict[str, object],
) -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    for task in contract["tasks"]:
        for candidate in task["candidates"]:
            for world_seed in contract["cohorts"]["candidate_screen"][  # type: ignore[index]
                "task_world_seeds"
            ][task["task_id"]]:
                results.append(
                    {
                        "task_id": task["task_id"],
                        "candidate_id": candidate["candidate_id"],
                        "world_seed": world_seed,
                        "passed": True,
                        "effect_size": 999.0
                        if candidate["scientific_priority"] == 2
                        else 0.05,
                    }
                )
    return results


def test_selection_rejects_task_when_no_candidate_passes_five_of_five() -> None:
    contract = _load(CONTRACT_PATH)
    task = contract["tasks"][0]
    results: list[dict[str, object]] = []
    for candidate in task["candidates"]:
        for index, world_seed in enumerate(
            contract["cohorts"]["candidate_screen"]["task_world_seeds"][  # type: ignore[index]
                task["task_id"]
            ]
        ):
            results.append(
                {
                    "task_id": task["task_id"],
                    "candidate_id": candidate["candidate_id"],
                    "world_seed": world_seed,
                    "passed": index != 0,
                }
            )
    selection = select_screen_candidates(contract, results)
    assert task["task_id"] not in selection["selected_candidate_ids"]
    assert selection["all_tasks_selected"] is False


def test_receipt_validator_requires_exact_denominator_and_failures() -> None:
    plan = build_screen_plan(ROOT, CONTRACT_PATH)
    synthetic = [
        {
            "execution_id": row["execution_id"],
            "status": "completed",
            "failure": None,
        }
        for row in plan["executions"]
    ]
    assert validate_receipt_denominator(plan, synthetic) == []
    missing = deepcopy(synthetic[:-1])
    errors = validate_receipt_denominator(plan, missing)
    assert any("count" in error or "cover" in error for error in errors)


def test_progress_validator_accepts_only_immutable_prefix() -> None:
    plan = build_screen_plan(ROOT, CONTRACT_PATH)
    prefix = [
        {
            "execution_id": row["execution_id"],
            "status": "completed",
            "failure": None,
        }
        for row in plan["executions"][:2]
    ]
    assert validate_phase_progress(plan, prefix) == []
    prefix.reverse()
    assert any("prefix" in error for error in validate_phase_progress(plan, prefix))


def test_moved_pair_rejects_non_transposition() -> None:
    with pytest.raises(AEPriorQualificationV03Error, match="transposition"):
        moved_pair([1, 2, 3, 0])
