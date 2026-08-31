from __future__ import annotations

import json
import sys
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import run_work_ii_reviewer_followups as runner  # noqa: E402

from chemworld.eval.work_ii_reviewer_followup import (  # noqa: E402
    B3_METRIC_IDS,
    build_b3_candidate_queries,
)


class _CaptureProgress:
    def __init__(self) -> None:
        self.events: list[dict] = []

    def emit(self, event: dict) -> None:
        self.events.append(event)


def test_b3_provider_free_contract_ignores_participant_interface_only() -> None:
    source = runner.json.loads(
        (ROOT / "configs/benchmark/work_ii_as_study_b3_shared_index_deepseek_v0.1.json")
        .read_text(encoding="utf-8")
    )
    target = runner.json.loads(
        (
            ROOT
            / "configs/benchmark/work_ii_as_study_b3_shared_index_gpt56_sol_medium_v0.1.json"
        ).read_text(encoding="utf-8")
    )
    assert runner._b3_provider_free_contract(source) == runner._b3_provider_free_contract(
        target
    )

    interface_variant = deepcopy(target)
    interface_variant["stage_status_encoding"] = "runner_derived"
    assert runner._b3_provider_free_contract(
        source
    ) == runner._b3_provider_free_contract(interface_variant)

    drifted = deepcopy(target)
    drifted["qualification"]["minimum_action_gain"] = 0.01
    assert runner._b3_provider_free_contract(
        source
    ) != runner._b3_provider_free_contract(drifted)


def test_b3_phase_authorization_blocks_formal_after_canary_authorization() -> None:
    manifest = {
        "protocol_status": "participant_execution_authorized_canary_only",
        "execution": {
            "canary_execution_authorized": True,
            "formal_execution_authorized": False,
        },
    }
    assert runner._b3_execution_authorized(manifest, phase="canary") is True
    assert runner._b3_execution_authorized(manifest, phase="formal") is False

    legacy = {"protocol_status": "provider_execution_authorized", "execution": {}}
    assert runner._b3_execution_authorized(legacy, phase="formal") is True
    blocked = {"protocol_status": "participant_execution_blocked", "execution": {}}
    assert runner._b3_execution_authorized(blocked, phase="canary") is False


def _submission(queries: list[dict], *, stage: str, action_index: int | None = None) -> dict:
    payload = {
        "status": f"{stage}_submission_complete",
        "mechanism_family": "FAMILY_B_POWER",
        "estimated_reference_exponent": 1.75,
        "confidence": 0.8,
        "typed_law": {
            "law_type": "reference_coefficient_power",
            "mechanism_family": "FAMILY_B_POWER",
            "reference_exponent": 1.75,
        },
        "predictions": [
            {
                "query_id": query["query_id"],
                "metrics": dict.fromkeys(B3_METRIC_IDS, 0.5),
            }
            for query in queries
        ],
        "model_summary": "Power response.",
    }
    if stage == "post":
        payload["selected_action_index"] = action_index
        payload["evidence_assessment"] = "Evidence supports the power response."
    return payload


def test_b3_runner_retains_invalid_shared_index_payload_without_retry(
    monkeypatch,
) -> None:
    protocol = runner.json.loads(
        (ROOT / "configs/benchmark/work_ii_as_study_b3_identifiable_law_action_v0.1.json")
        .read_text(encoding="utf-8")
    )
    queries = build_b3_candidate_queries(protocol)[:8]
    for index, query in enumerate(queries):
        query["action_index"] = index
    pre_payload = _submission(queries, stage="pre")
    invalid_post_payload = _submission(queries, stage="post", action_index=8)
    turns = iter(
        [
            {"status": "completed", "thread_id": "thread-1", "final_payload": pre_payload},
            {
                "status": "completed",
                "thread_id": "thread-1",
                "final_payload": invalid_post_payload,
            },
        ]
    )
    monkeypatch.setattr(runner, "_prepare_b3_environment", lambda *_args: {})
    monkeypatch.setattr(runner, "_b3_initial_command", lambda *_args: ["codex"])
    monkeypatch.setattr(runner, "_resume_command", lambda *_args, **_kwargs: ["codex"])
    monkeypatch.setattr(runner, "_launch_turn", lambda *_args, **_kwargs: next(turns))

    scoring_truth = {
        query["query_id"]: dict.fromkeys(B3_METRIC_IDS, 0.5) for query in queries
    }
    result = runner._run_b3_cell_attempt(
        {
            "study_id": "shared-index-fixture",
            "cell_id": "cell-1",
            "cluster_id": "cluster-1",
            "replicate_index": 1,
            "locus": "A_S_B3",
            "task_id": "partition-discovery",
            "world_seed": 1,
            "arm": "opaque",
            "action_selection_encoding": "zero_based_index",
            "initial_world_model": {},
            "public_packet_sha256": "0" * 64,
            "public_packet": {
                "candidate_mechanism_families": [],
                "metric_range": [0.0, 1.0],
                "evidence": [],
                "scoring_action_queries": queries,
            },
            "scoring_truth": scoring_truth,
        },
        provider={"request_timeout_s": 30.0},
        progress=_CaptureProgress(),
        phase="canary",
    )

    assert result["status"] == "failed"
    assert result["failure"]["classification"] == "participant_schema"
    assert result["failure"]["message"] == "post selected action index is invalid"
    assert result["post_submission"] == invalid_post_payload
    assert len(result["provider_receipts"]) == 2


def test_b3_post_prompt_explicitly_requires_fields_added_after_pre() -> None:
    packet = {
        "candidate_mechanism_families": [],
        "evidence": [],
        "scoring_action_queries": [],
    }
    for encoding, selection_field in (
        ("query_id", "selected_action_query_id"),
        ("zero_based_index", "selected_action_index"),
    ):
        prompt = runner._b3_evidence_prompt(
            {
                "task_id": "partition-discovery",
                "action_selection_encoding": encoding,
                "public_packet": packet,
            }
        )
        assert "first-turn JSON shape is not sufficient" in prompt
        assert selection_field in prompt
        assert "evidence_assessment" in prompt


def test_b3_openai_command_has_one_cached_login_and_provider_override(
    tmp_path: Path,
) -> None:
    provider = json.loads(
        (
            ROOT
            / "configs/benchmark/"
            "work_ii_as_study_b3_main_evidence_successor_gpt56_sol_medium_v0.1.json"
        ).read_text(encoding="utf-8")
    )["provider"]
    schema = tmp_path / "schema.json"
    schema.write_text("{}\n", encoding="utf-8")
    workspace = tmp_path / "workspace"
    workspace.mkdir()

    command = runner._b3_initial_command(provider, schema, workspace)
    rendered = " ".join(command)

    assert command.count("--ignore-user-config") == 1
    assert rendered.count("model_providers.chemworld_openai_https=") == 1
    assert "--disable shell_tool" in rendered


def test_b3_openai_environment_reuses_isolated_cached_login_setup(
    monkeypatch,
    tmp_path: Path,
) -> None:
    expected = {"CODEX_HOME": "isolated"}
    observed: list[tuple[Path, dict]] = []

    def prepare(temp_root: Path, provider: dict) -> dict[str, str]:
        observed.append((temp_root, provider))
        return expected

    monkeypatch.setattr(runner, "_prepare_codex_home", prepare)
    provider = {"auth_mode": "chatgpt_subscription_cached_login"}

    assert runner._prepare_b3_environment(tmp_path, provider) == expected
    assert observed == [(tmp_path, provider)]


def test_b3_runner_derived_status_removes_status_schema_and_ignores_status_text(
    monkeypatch,
) -> None:
    protocol = runner.json.loads(
        (ROOT / "configs/benchmark/work_ii_as_study_b3_identifiable_law_action_v0.1.json")
        .read_text(encoding="utf-8")
    )
    queries = build_b3_candidate_queries(protocol)[:8]
    for index, query in enumerate(queries):
        query["action_index"] = index
    pre_payload = _submission(queries, stage="pre")
    post_payload = _submission(queries, stage="post", action_index=3)
    post_payload["status"] = "pre_submission_complete"
    turns = iter(
        [
            {"status": "completed", "thread_id": "thread-1", "final_payload": pre_payload},
            {
                "status": "completed",
                "thread_id": "thread-1",
                "final_payload": post_payload,
            },
        ]
    )
    schemas: list[dict] = []

    def initial_command(_provider: dict, schema_path: Path, _workspace: Path) -> list[str]:
        schemas.append(json.loads(schema_path.read_text(encoding="utf-8")))
        return ["codex"]

    def resume_command(
        _initial: list[str], *, thread_id: str, schema_path: Path
    ) -> list[str]:
        assert thread_id == "thread-1"
        schemas.append(json.loads(schema_path.read_text(encoding="utf-8")))
        return ["codex"]

    monkeypatch.setattr(runner, "_prepare_b3_environment", lambda *_args: {})
    monkeypatch.setattr(runner, "_b3_initial_command", initial_command)
    monkeypatch.setattr(runner, "_resume_command", resume_command)
    monkeypatch.setattr(runner, "_launch_turn", lambda *_args, **_kwargs: next(turns))

    scoring_truth = {
        query["query_id"]: {
            **dict.fromkeys(B3_METRIC_IDS, 0.5),
            "score": 1.0 - 0.05 * index,
        }
        for index, query in enumerate(queries)
    }
    result = runner._run_b3_cell_attempt(
        {
            "study_id": "runner-derived-fixture",
            "cell_id": "cell-1",
            "cluster_id": "cluster-1",
            "replicate_index": 1,
            "locus": "A_S_B3",
            "task_id": "partition-discovery",
            "world_seed": 1,
            "arm": "opaque",
            "action_selection_encoding": "zero_based_index",
            "stage_status_encoding": "runner_derived",
            "initial_world_model": {},
            "public_packet_sha256": "0" * 64,
            "public_packet": {
                "candidate_mechanism_families": [],
                "metric_range": [0.0, 1.0],
                "evidence": [],
                "scoring_action_queries": queries,
            },
            "scoring_truth": scoring_truth,
            "evidence_incumbent_score": 0.4,
            "action_opportunity_threshold": 0.02,
            "action_opportunity_eligible": True,
        },
        provider={"request_timeout_s": 30.0},
        progress=_CaptureProgress(),
        phase="canary",
    )

    assert result["status"] == "completed"
    assert result["same_thread"] is True
    assert result["post_submission"]["status"] == "pre_submission_complete"
    assert result["selected_action"]["query_id"] == queries[3]["query_id"]
    assert len(schemas) == 2
    assert all("status" not in schema["properties"] for schema in schemas)
