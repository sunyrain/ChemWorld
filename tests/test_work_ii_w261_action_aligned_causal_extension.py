from __future__ import annotations

import json
import shutil
import sys
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from run_work_ii_evidence_to_action_formal import (  # noqa: E402
    CodexRecipientSessionClient,
)
from run_work_ii_study_b import (  # noqa: E402
    _initial_command,
    _prepare_codex_home,
    _provider_compatible_output_schema,
)
from run_work_ii_w250_action_aligned_causal_extension import (  # noqa: E402
    DISPLAY_CONDITIONS,
    build_inputs,
    provider_free_canary,
)
from run_work_ii_w250_yoked_schema_repair import (  # noqa: E402
    W250YokedRepairClient,
)
from run_work_ii_w261_codex_open_action_donors import (  # noqa: E402
    materialize as materialize_codex_donors,
)
from run_work_ii_w261_yoked_condition_recovery import (  # noqa: E402
    build_recovery_inputs,
    recovery_provider_free_canary,
)

from chemworld.eval.work_ii_evidence_to_action_runtime import (  # noqa: E402
    terminal_output_schema,
    validate_terminal_submission,
    validate_yoked_snapshot_submission,
)


def test_deepseek_extension_preserves_all_slots_and_runs_no_evidence_for_failures() -> None:
    inputs = build_inputs(participant="deepseek")

    assert inputs["scheduled_stratum_count"] == 45
    assert inputs["admitted_stratum_count"] == 42
    assert inputs["retained_donor_failure_count"] == 3
    assert inputs["scheduled_condition_slot_count"] == 180
    assert inputs["new_recipient_session_count"] == 129
    assert inputs["condition_order_for_display"] == list(DISPLAY_CONDITIONS)
    assert "oracle_law" not in inputs["condition_order_for_display"]
    failed = [row for row in inputs["strata"] if not row["admitted"]]
    assert len(failed) == 3
    assert all(row["recipient_conditions"] == ["no_evidence"] for row in failed)
    assert all("candidate_truth" in row["inputs"] for row in failed)


def test_deepseek_provider_free_canary_covers_every_public_baseline() -> None:
    canary = provider_free_canary(build_inputs(participant="deepseek"))

    assert canary["status"] == "passed"
    assert canary["checked_no_evidence_strata"] == 45
    assert canary["checked_admitted_strata"] == 42
    assert canary["checked_yoked_snapshot_schemas"] == 210
    assert canary["candidate_preterminal_reveal_count"] == 0
    assert canary["provider_calls"] == 0


def test_codex_donor_successor_matches_deepseek_science_surface() -> None:
    manifest = materialize_codex_donors()

    assert manifest["scheduled_cell_count"] == 45
    assert manifest["scheduled_participant_physical_experiments"] == 540
    assert manifest["new_provider_free_truth_executions"] == 0
    assert manifest["matched_deepseek_science_surface"] is True
    assert manifest["model"] == "gpt-5.6-sol"
    assert manifest["reasoning_effort"] == "medium"


def test_codex_recipient_accepts_runtime_none_as_cached_openai_login(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source_home = tmp_path / "source-codex-home"
    source_home.mkdir()
    (source_home / "auth.json").write_text('{"auth":"test"}\n', encoding="utf-8")
    monkeypatch.setenv("CODEX_HOME", str(source_home))
    monkeypatch.setattr(shutil, "which", lambda _name: "codex")
    provider = {
        "id": "chemworld_openai_https",
        "name": "OpenAI",
        "wire_api": "responses",
        "auth_mode": "none",
        "model": "gpt-5.6-sol",
        "reasoning_effort": "medium",
    }
    launch_root = tmp_path / "launch"
    launch_root.mkdir()

    environment = _prepare_codex_home(launch_root, provider)
    isolated_auth = Path(environment["CODEX_HOME"]) / "auth.json"
    assert isolated_auth.read_text(encoding="utf-8") == '{"auth":"test"}\n'

    command = _initial_command(provider, tmp_path / "schema.json", tmp_path / "workspace")
    assert "--ignore-user-config" in command
    assert any(
        "model_providers.chemworld_openai_https=" in item for item in command
    )


def test_non_openai_runtime_none_auth_remains_rejected(tmp_path: Path) -> None:
    with pytest.raises(RuntimeError, match="unsupported Study B provider authentication mode"):
        _prepare_codex_home(
            tmp_path,
            {"id": "unknown", "auth_mode": "none"},
        )


def test_openai_schema_projection_removes_only_unsupported_unique_items() -> None:
    provider = {"id": "chemworld_openai_https", "auth_mode": "none"}
    source = terminal_output_schema([f"q{index}" for index in range(8)])

    projected = _provider_compatible_output_schema(provider, source)

    assert source["properties"]["ranking"]["uniqueItems"] is True
    assert "uniqueItems" not in projected["properties"]["ranking"]
    expected = dict(source["properties"]["ranking"])
    expected.pop("uniqueItems")
    assert projected["properties"]["ranking"] == expected


def test_non_openai_schema_projection_preserves_unique_items() -> None:
    provider = {"id": "deepseek", "auth_mode": "experimental_bearer_token"}
    source = terminal_output_schema([f"q{index}" for index in range(8)])

    assert _provider_compatible_output_schema(provider, source) == source


def test_local_terminal_validator_still_rejects_duplicate_ranking() -> None:
    query_ids = [f"q{index}" for index in range(8)]
    with pytest.raises(ValueError, match="permutation"):
        validate_terminal_submission(
            {
                "schema_version": (
                    "chemworld-work-ii-evidence-to-action-terminal-submission-0.1"
                ),
                "ranking": ["q0", "q0", *query_ids[2:]],
                "selected_query_id": "q0",
                "decision_rationale": "duplicate should fail local validation",
            },
            candidate_query_ids=query_ids,
        )


def test_yoked_client_leaves_nullable_terms_for_the_single_shared_validator(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    payload = {
        "law_summary": {
            "metric_laws": [
                {
                    "terms": [
                        {
                            "term_id": "term-linear-temperature",
                            "basis": "linear",
                            "input_ids": ["temperature"],
                            "coefficient": 0.25,
                            "category_value": None,
                        }
                    ]
                }
            ]
        }
    }

    def fake_complete_json(*_args: object, **_kwargs: object) -> SimpleNamespace:
        return SimpleNamespace(payload=deepcopy(payload))

    monkeypatch.setattr(CodexRecipientSessionClient, "complete_json", fake_complete_json)
    client = object.__new__(W250YokedRepairClient)
    completion = client.complete_json(
        system_prompt="test",
        user_prompt=json.dumps(
            {"condition": "yoked_evidence", "stage": "pre_evidence"}
        ),
    )

    term = completion.payload["law_summary"]["metric_laws"][0]["terms"][0]
    assert "category_value" in term
    assert term["category_value"] is None


def test_shared_yoked_validator_normalizes_nullable_term_exactly_once() -> None:
    payload = {
        "schema_version": "chemworld-work-ii-belief-snapshot-0.1",
        "snapshot_id": "snapshot-pre",
        "stage": "pre_evidence",
        "prior_assessment": {
            "nominal_information_available": False,
            "reliability_probability": None,
            "suspected_misindexed_fields": [],
            "rationale": "The target locus is opaque.",
        },
        "predictions": [
            {
                "query_id": "checkpoint-q",
                "metrics": [
                    {
                        "metric_id": "score",
                        "mean": 0.5,
                        "interval_lower": 0.2,
                        "interval_upper": 0.8,
                        "confidence": 0.7,
                    }
                ],
            }
        ],
        "law_summary": {
            "schema_version": "chemworld-work-ii-law-summary-0.1",
            "summary_id": "law-pre",
            "feature_ids": ["temperature"],
            "metric_laws": [
                {
                    "metric_id": "score",
                    "intercept": 0.5,
                    "link": "identity",
                    "lower_bound": 0.0,
                    "upper_bound": 1.0,
                    "terms": [
                        {
                            "term_id": "term-linear-temperature",
                            "basis": "linear",
                            "input_ids": ["temperature"],
                            "coefficient": 0.25,
                            "category_value": None,
                        }
                    ],
                }
            ],
            "evidence_ids": [],
            "applicability": "registered checkpoint domain",
            "limitations": [],
            "confidence": 0.7,
        },
        "evidence_ids": [],
        "next_experiment_intent": "Inspect the next yoked observation.",
        "overall_confidence": 0.7,
    }

    parsed = validate_yoked_snapshot_submission(
        payload,
        stage="pre_evidence",
        query_metric_contract={"checkpoint-q": ["score"]},
        allowed_feature_ids=["temperature"],
        allowed_metric_ids=["score"],
        allowed_prior_fields=[],
        evidence_catalog=[],
        nominal_information_available=False,
    )

    term = parsed["law_summary"]["metric_laws"][0]["terms"][0]
    assert "category_value" not in term


@pytest.mark.parametrize(
    ("participant", "admitted", "retained_key_errors"),
    (("deepseek", 42, 39), ("codex", 26, 22)),
)
def test_yoked_recovery_covers_the_full_admitted_condition(
    participant: str,
    admitted: int,
    retained_key_errors: int,
) -> None:
    inputs = build_recovery_inputs(participant=participant)

    assert inputs["new_recipient_session_count"] == admitted
    assert inputs["source_incident"]["category_value_key_error_count"] == (
        retained_key_errors
    )
    assert sum(
        row["recipient_conditions"] == ["yoked_evidence"]
        for row in inputs["strata"]
    ) == admitted
    assert all(
        row["recipient_conditions"] == []
        for row in inputs["strata"]
        if not row["admitted"]
    )

    canary = recovery_provider_free_canary(inputs)
    assert canary["status"] == "passed"
    assert canary["checked_admitted_strata"] == admitted
    assert canary["checked_yoked_snapshot_schemas"] == admitted * 5
    assert canary["provider_calls"] == 0
