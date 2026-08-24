from __future__ import annotations

import importlib
import json
import os
import sys
from pathlib import Path

import jsonschema

from chemworld.eval.work_ii_evidence_to_action_runtime import (
    yoked_snapshot_output_schema,
)

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
formal_runner = importlib.import_module("run_work_ii_evidence_to_action_formal")
Progress = importlib.import_module("work_ii_longitudinal_runtime").Progress


def _provider() -> dict:
    return {
        "id": "deepseek",
        "name": "DeepSeek",
        "model": "deepseek-v4-flash",
        "reasoning_effort": "high",
        "request_timeout_s": 30.0,
    }


def _client(tmp_path: Path, monkeypatch) -> formal_runner.CodexRecipientSessionClient:
    monkeypatch.setattr(
        formal_runner.codex_harness,
        "_prepare_codex_home",
        lambda *_: dict(os.environ),
    )
    monkeypatch.setattr(
        formal_runner.codex_harness,
        "_initial_command",
        lambda _provider, schema, workspace: [
            "codex",
            "exec",
            "--output-schema",
            str(schema),
            "--sandbox",
            "read-only",
            "-C",
            str(workspace),
        ],
    )
    initial_threads = iter(("thread-no", "thread-yoked", "thread-oracle"))
    active_yoked: list[str] = []

    def launch(command, _prompt, **_kwargs):
        if "resume" in command:
            thread_id = active_yoked[0]
        else:
            thread_id = next(initial_threads)
            if thread_id == "thread-yoked":
                active_yoked.append(thread_id)
        return {
            "status": "completed",
            "return_code": 0,
            "elapsed_s": 0.1,
            "thread_id": thread_id,
            "usage": {"input_tokens": 10, "output_tokens": 2},
            "event_counts": {"thread.started": 1, "turn.completed": 1},
            "provider_errors": [],
            "tool_event_count": 0,
            "stderr_byte_count": 0,
            "stderr_sha256": "0" * 64,
            "final_payload": {"ok": True},
        }

    monkeypatch.setattr(formal_runner.codex_harness, "_launch_turn", launch)
    return formal_runner.CodexRecipientSessionClient(
        provider=_provider(),
        stratum_id="stratum-1",
        output_root=tmp_path / "turns",
        progress=Progress(tmp_path / "progress.jsonl"),
        query_metric_contract={"checkpoint-q": ["score"]},
        allowed_feature_ids=["temperature"],
        allowed_metric_ids=["score"],
        allowed_prior_fields=[],
        nominal_information_available=False,
    )


def test_yoked_snapshot_provider_schema_is_valid_json_schema() -> None:
    schema = yoked_snapshot_output_schema(
        stage="pre_evidence",
        query_metric_contract={"checkpoint-q": ["score"]},
        allowed_feature_ids=["temperature"],
        allowed_metric_ids=["score"],
        allowed_prior_fields=[],
        evidence_catalog=[],
        nominal_information_available=False,
    )
    jsonschema.Draft202012Validator.check_schema(schema)
    assert schema["properties"]["stage"]["const"] == "pre_evidence"
    assert schema["properties"]["predictions"]["minItems"] == 1


def test_recipient_client_uses_fresh_condition_threads_and_resumes_yoked(
    tmp_path: Path,
    monkeypatch,
) -> None:
    with _client(tmp_path, monkeypatch) as client:
        client.complete_json(
            system_prompt="system",
            user_prompt='{"condition":"no_evidence","stage":"terminal_ranking"}',
            output_schema={"type": "object"},
        )
        client.complete_json(
            system_prompt="system",
            user_prompt=(
                '{"condition":"yoked_evidence","stage":"pre_evidence",'
                '"visible_yoked_evidence_rounds":[]}'
            ),
        )
        client.complete_json(
            system_prompt="system",
            user_prompt=(
                '{"condition":"yoked_evidence","stage":"after_experiment_3",'
                '"visible_yoked_evidence_rounds":[]}'
            ),
        )
        client.complete_json(
            system_prompt="system",
            user_prompt='{"condition":"oracle_law","stage":"terminal_ranking"}',
            output_schema={"type": "object"},
        )
        audit = client.session_audit(
            autonomous_thread_id="thread-autonomous",
            autonomous_provider_call_count=1,
        )
    assert client.total_provider_call_count == 4
    assert audit["recipient_condition_thread_count"] == 3
    assert audit["recipient_condition_threads_unique"] is True
    assert audit["yoked_turn_count"] == 2
    assert audit["yoked_same_thread"] is True
    assert audit["passed"] is True


def test_canary_allows_scientific_donor_failure_but_not_schema_failure() -> None:
    base = {
        "stratum_id": "stratum-1",
        "fresh_session_audit": {"passed": True},
        "recipient_provider_receipts": [],
        "cell_results": {
            "donor": {
                "cell_id": "donor",
                "condition": "autonomous_exploration",
                "status": "failed_retained",
                "failure_classification": "scientific_process",
                "provider_call_count": 0,
                "provider_usage": {},
            }
        },
    }
    scientific = [{**base, "stratum_id": f"stratum-{index}"} for index in range(3)]
    assert formal_runner._canary_defects(scientific) == []

    invalid = [dict(row) for row in scientific]
    invalid[0] = {
        **invalid[0],
        "cell_results": {
            "recipient": {
                "cell_id": "recipient",
                "condition": "no_evidence",
                "status": "failed_retained",
                "failure": {"classification": "participant_schema"},
            }
        },
    }
    assert any("participant_schema" in item for item in formal_runner._canary_defects(invalid))


def test_finalize_rejected_preparation_preserves_frozen_denominator(
    tmp_path: Path,
    monkeypatch,
) -> None:
    task_id = "task"
    world_seed = 17
    cluster_id = "cluster-17"
    cluster_root = (
        tmp_path / "prepared" / "clusters" / task_id / f"seed-{world_seed}" / task_id
    )
    for name in ("candidate-truth", "checkpoint-truth", "oracle-grid-truth"):
        report_path = cluster_root / name / "report.json"
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text("{}\n", encoding="utf-8")
    candidate_ids = [f"c{index}" for index in range(8)]
    (cluster_root / "public_candidate_packet.json").write_text(
        json.dumps(
            {
                "candidate_outcomes_included": False,
                "candidates": [{"query_id": query_id} for query_id in candidate_ids],
            }
        ),
        encoding="utf-8",
    )

    protocol = {
        "study_id": "study",
        "candidate_contract": {"candidate_count": 8},
        "oracle_grid_contract": {"query_count_per_task": 96},
        "artifact_contract": {"minimum_oracle_candidate_rank_correlation": 0.8},
    }
    monkeypatch.setattr(formal_runner, "validate_protocol", lambda _protocol: [])
    monkeypatch.setattr(
        formal_runner,
        "build_design_manifest",
        lambda _protocol: {
            "clusters": [
                {
                    "cluster_id": cluster_id,
                    "task_id": task_id,
                    "world_seed": world_seed,
                }
            ]
        },
    )

    def retained_report(path: Path, *, expected_query_count: int):
        return (
            {
                "truth": {},
                "evaluator_provider_call_count": 0,
            },
            expected_query_count,
            "b" * 64,
            "c" * 40,
        )

    monkeypatch.setattr(
        formal_runner,
        "_verify_retained_truth_report",
        retained_report,
    )
    monkeypatch.setattr(
        formal_runner,
        "evaluate_candidate_packet",
        lambda *_args, **_kwargs: {"status": "passed"},
    )
    monkeypatch.setattr(
        formal_runner,
        "_retained_oracle_task_bundle",
        lambda **_kwargs: {
            "grid": [],
            "candidate_feature_queries": [
                {"query_id": query_id} for query_id in candidate_ids
            ],
            "feature_ids": [],
            "metric_ids": [],
        },
    )
    monkeypatch.setattr(
        formal_runner,
        "fit_oracle_law_from_disjoint_grid",
        lambda *_args, **_kwargs: {"artifact_type": "test"},
    )
    oracle_qualification = {
        "status": "failed",
        "spearman_rank_correlation": 0.738095,
        "top1_agreement": False,
        "fit_candidate_overlap_count": 0,
    }
    monkeypatch.setattr(
        formal_runner,
        "evaluate_oracle_law_candidate_order",
        lambda *_args, **_kwargs: oracle_qualification,
    )

    summary = formal_runner.finalize_rejected_preparation(
        protocol=protocol,
        output_root=tmp_path,
    )

    assert summary["status"] == "scientifically_rejected_before_provider"
    assert summary["attempted_cluster_count"] == 1
    assert summary["qualified_cluster_count"] == 0
    assert summary["provider_free_truth_query_count"] == 112
    assert summary["provider_free_exact_replay_count"] == 112
    assert summary["participant_provider_call_count"] == 0
    assert summary["participant_physical_experiment_count"] == 0
    assert summary["failure"]["cluster_id"] == cluster_id
    assert (tmp_path / "provider-free-preparation-summary.json").is_file()
    assert (tmp_path / "REPORT_ZH.md").is_file()
    assert (cluster_root / "rejected-oracle-artifact.json").is_file()
