from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest

import chemworld.agents.experiment_codex_ipc as experiment_ipc
import chemworld.agents.experiment_codex_mcp as experiment_mcp
from chemworld.agents.interaction import AgentDecisionContext
from chemworld.agents.interactive_codex_experiment import (
    InteractiveCodexExperimentAgent,
    InteractiveCodexExperimentError,
    _classify_mcp_tool_failure,
    _final_recommendation_from_payload,
    _material_information_payload,
    _mcp_tool_failure_audit,
    _parse_final_payload,
    _participant_visible_campaign,
    _public_task_contract,
    validated_mcp_tool_failure_budget,
)


@pytest.mark.parametrize(
    ("call", "expected"),
    (
        ({"status": "completed"}, None),
        (
            {
                "status": "failed",
                "error_type": "PermissionError",
                "error_code": "atomic_replace_permission_error",
            },
            "transport_ipc_os",
        ),
        (
            {
                "status": "failed",
                "error_type": "RuntimeError",
                "error_code": "tool_execution_error",
                "error_detail": "checkpoint is not due at this stage",
            },
            "agent_invalid",
        ),
        (
            {
                "status": "failed",
                "error_type": "APIConnectionError",
                "error_code": "provider_connection_error",
            },
            "provider_network",
        ),
        ({"status": "failed", "error_type": "MysteryError"}, "unclassified"),
    ),
)
def test_mcp_tool_failure_taxonomy(call: dict[str, Any], expected: str | None) -> None:
    assert _classify_mcp_tool_failure(call) == expected


def test_mcp_tool_failure_audit_preserves_legacy_totals_but_types_streaks() -> None:
    transport = {
        "status": "failed",
        "error_type": "PermissionError",
        "error_code": "atomic_replace_permission_error",
    }
    agent_invalid = {
        "status": "failed",
        "error_type": "RuntimeError",
        "error_detail": "checkpoint is not due",
    }

    audit = _mcp_tool_failure_audit([transport] * 4 + [agent_invalid, transport, agent_invalid])

    assert audit["recovered_mcp_tool_failure_count"] == 7
    assert audit["maximum_consecutive_mcp_tool_failure_count"] == 7
    assert audit["counts_by_category"] == {
        "provider_network": 0,
        "transport_ipc_os": 5,
        "agent_invalid": 2,
        "unclassified": 0,
    }
    assert audit["maximum_consecutive_counts_by_category"]["transport_ipc_os"] == 5
    assert audit["maximum_consecutive_counts_by_category"]["agent_invalid"] == 2


def test_mcp_tool_failure_audit_groups_one_queued_duplicate_burst_as_one_episode() -> None:
    burst = [
        {
            "status": "failed",
            "tool": "step",
            "started_at": f"2026-08-13T07:41:32.{millisecond:03d}+00:00",
            "error_type": "ValueError",
            "error_code": "invalid_checkpoint_timing",
            "error_field_path": "checkpoint.stage",
            "error_detail_sha256": "same-detail",
            "result_sha256": "same-result",
        }
        for millisecond in range(306, 354)
    ]

    audit = _mcp_tool_failure_audit(burst)
    episodes = audit["recovery_episode_taxonomy"]

    assert audit["counts_by_category"]["agent_invalid"] == 48
    assert episodes["counts_by_category"]["agent_invalid"] == 1
    assert episodes["maximum_consecutive_counts_by_category"]["agent_invalid"] == 1


def test_mcp_tool_failure_audit_keeps_feedback_separated_failures_as_distinct_episodes() -> None:
    failures = [
        {
            "status": "failed",
            "tool": "commit_belief_snapshot",
            "started_at": f"2026-08-13T07:40:{second:02d}+00:00",
            "error_type": "ValueError",
            "error_code": "invalid_checkpoint_payload",
            "error_detail_sha256": "same-detail",
            "result_sha256": "same-result",
        }
        for second in (1, 15, 31)
    ]

    episodes = _mcp_tool_failure_audit(failures)["recovery_episode_taxonomy"]

    assert episodes["counts_by_category"]["agent_invalid"] == 3
    assert episodes["maximum_consecutive_counts_by_category"]["agent_invalid"] == 3


def test_mcp_tool_failure_audit_classifies_rejected_begin_batch_cascade() -> None:
    def failed(
        started_at: str,
        *,
        argument_keys: list[str],
        detail: str,
        detail_hash: str,
    ) -> dict[str, Any]:
        return {
            "status": "failed",
            "tool": "commit_belief_snapshot",
            "started_at": started_at,
            "error_type": "ValueError",
            "error_code": "invalid_belief_snapshot",
            "error_detail": detail,
            "error_detail_sha256": detail_hash,
            "argument_keys": argument_keys,
        }

    calls = [
        failed(
            "2026-08-13T10:02:58.026756+00:00",
            argument_keys=["action", "snapshot_header"],
            detail="prior assessment availability does not match the public dossier",
            detail_hash="availability-1",
        ),
        failed(
            "2026-08-13T10:03:11.968812+00:00",
            argument_keys=["action", "snapshot_header"],
            detail="prior assessment availability does not match the public dossier",
            detail_hash="availability-2",
        ),
        {"status": "completed", "tool": "step"},
        failed(
            "2026-08-13T10:09:15.793923+00:00",
            argument_keys=["action", "snapshot_header"],
            detail="belief_snapshot stage does not match the requested snapshot",
            detail_hash="wrong-stage",
        ),
    ]
    calls.extend(
        failed(
            f"2026-08-13T10:09:15.{millisecond:06d}+00:00",
            argument_keys=(
                ["action"]
                if offset == 7
                else ["action", "page_id", "predictions"]
            ),
            detail="begin must be accepted before belief snapshot pages",
            detail_hash="begin-not-accepted",
        )
        for offset, millisecond in enumerate(
            (798880, 801952, 804992, 807202, 810219, 813293, 815308, 818166)
        )
    )

    audit = _mcp_tool_failure_audit(calls)
    episodes = audit["recovery_episode_taxonomy"]

    assert audit["recovered_mcp_tool_failure_count"] == 11
    assert audit["counts_by_category"]["agent_invalid"] == 11
    assert audit["maximum_consecutive_counts_by_category"]["agent_invalid"] == 9
    assert episodes["counts_by_category"]["agent_invalid"] == 3
    assert episodes["maximum_consecutive_counts_by_category"]["agent_invalid"] == 2
    assert episodes["dependent_batch_cascade_failure_count"] == 8
    assert episodes["dependent_batch_cascade_group_count"] == 1
    assert episodes["maximum_dependent_batch_cascade_size"] == 8
    assert episodes["dependent_batch_cascades"] == [
        {
            "classification": "dependent_batch_cascade",
            "upstream_call_index": 3,
            "dependent_call_indices": list(range(4, 12)),
        }
    ]


def test_mcp_tool_failure_audit_does_not_collapse_dependency_after_success() -> None:
    begin = {
        "status": "failed",
        "tool": "commit_belief_snapshot",
        "started_at": "2026-08-13T10:09:15.793923+00:00",
        "error_type": "ValueError",
        "error_code": "invalid_belief_snapshot",
        "error_detail": "belief_snapshot stage does not match the requested snapshot",
        "argument_keys": ["action", "snapshot_header"],
    }
    dependent = {
        "status": "failed",
        "tool": "commit_belief_snapshot",
        "started_at": "2026-08-13T10:09:15.798880+00:00",
        "error_type": "ValueError",
        "error_code": "invalid_belief_snapshot",
        "error_detail": "begin must be accepted before belief snapshot pages",
        "argument_keys": ["action", "page_id", "predictions"],
    }

    episodes = _mcp_tool_failure_audit(
        [begin, {"status": "completed", "tool": "status"}, dependent]
    )["recovery_episode_taxonomy"]

    assert episodes["counts_by_category"]["agent_invalid"] == 2
    assert episodes["dependent_batch_cascade_failure_count"] == 0


def test_typed_mcp_budget_requires_a_complete_consistent_taxonomy() -> None:
    taxonomy = _mcp_tool_failure_audit(
        [
            {
                "status": "failed",
                "error_type": "PermissionError",
                "error_code": "atomic_replace_permission_error",
            },
            {
                "status": "failed",
                "error_code": "invalid_checkpoint_timing",
            },
        ]
    )
    receipt = {
        "recovered_mcp_tool_failure_count": 2,
        "current_consecutive_mcp_tool_failure_count": 2,
        "maximum_consecutive_mcp_tool_failure_count": 2,
        "mcp_tool_failure_taxonomy": taxonomy,
        "scientific_compliance_mcp_tool_failure_count": 1,
        "current_consecutive_scientific_compliance_mcp_tool_failure_count": 1,
        "maximum_consecutive_scientific_compliance_mcp_tool_failure_count": 1,
        "scientific_compliance_mcp_tool_failure_episode_count": 1,
        "current_consecutive_scientific_compliance_mcp_tool_failure_episode_count": 1,
        "maximum_consecutive_scientific_compliance_mcp_tool_failure_episode_count": 1,
    }
    budget = validated_mcp_tool_failure_budget(receipt)
    assert budget["scientific_count"] == 1
    assert budget["scientific_episode_count"] == 1
    assert budget["transport_count"] == 1

    malformed = dict(receipt)
    malformed["scientific_compliance_mcp_tool_failure_count"] = -1
    with pytest.raises(ValueError, match="non-negative integer"):
        validated_mcp_tool_failure_budget(malformed)

    mismatched = dict(receipt)
    mismatched["scientific_compliance_mcp_tool_failure_count"] = 0
    with pytest.raises(ValueError, match="disagree with taxonomy"):
        validated_mcp_tool_failure_budget(mismatched)


def test_final_payload_parser_accepts_exact_json_and_one_json_fence() -> None:
    payload = {"status": "campaign_complete", "summary": "done"}
    exact, exact_encoding = _parse_final_payload(json.dumps(payload))
    fenced, fenced_encoding = _parse_final_payload("```json\n" + json.dumps(payload) + "\n```")

    assert exact == payload
    assert exact_encoding == "json"
    assert fenced == payload
    assert fenced_encoding == "markdown_json_fence"


def test_final_payload_parser_rejects_json_embedded_in_prose() -> None:
    payload, encoding = _parse_final_payload(
        'Campaign complete: {"status":"campaign_complete","summary":"done"}'
    )

    assert payload is None
    assert encoding is None


def test_campaign_recommendation_normalizes_flat_and_nested_payloads() -> None:
    flat = {
        "status": "campaign_complete",
        "summary": "done",
        "selected_experiment_index": 2,
        "selection_rationale": "best public score",
    }
    nested = {
        "status": "campaign_complete",
        "summary": "done",
        "final_recommendation": {
            "selected_experiment_index": 3,
            "selection_rationale": "best public score",
        },
    }

    assert _final_recommendation_from_payload(flat) == {
        "selected_experiment_index": 2,
        "selection_rationale": "best public score",
    }
    assert _final_recommendation_from_payload(nested) == nested["final_recommendation"]


def test_codex_campaign_view_uses_one_based_experiment_indices() -> None:
    visible = _participant_visible_campaign(
        {
            "experiment_index": 1,
            "done": False,
            "experiment_summaries": [{"experiment_index": 0, "leaderboard_score": 0.4}],
            "completed_batches": [{"experiment_index": 0, "leaderboard_score": 0.4}],
            "discarded_batches": [],
            "last_terminal_summary": {
                "experiment_index": 0,
                "leaderboard_score": 0.4,
            },
            "campaign_resources": {
                "campaign_terminal": False,
                "current_experiment": {
                    "experiment_index": 1,
                    "vessel_started": False,
                },
            },
        }
    )

    assert visible["experiment_index_base"] == 1
    assert visible["completed_experiment_count"] == 1
    assert visible["experiment_index"] == 2
    assert visible["experiment_summaries"][0]["experiment_index"] == 1
    assert visible["completed_batches"][0]["experiment_index"] == 1
    assert visible["last_terminal_summary"]["experiment_index"] == 1
    assert visible["campaign_resources"]["current_experiment"] == {
        "experiment_index": 2,
        "vessel_started": False,
        "experiment_index_base": 1,
    }


@pytest.mark.parametrize(
    ("module", "write"),
    (
        (
            experiment_ipc,
            lambda path: experiment_ipc._atomic_write_bytes(path, b'{"ok":true}\n'),
        ),
        (
            experiment_mcp,
            lambda path: experiment_mcp._atomic_json(path, {"ok": True}),
        ),
    ),
)
def test_atomic_ipc_writes_retry_transient_permission_errors(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    module: Any,
    write: Any,
) -> None:
    target = tmp_path / "active_session.json"
    real_replace = module.os.replace
    attempts = 0

    def flaky_replace(source: Any, destination: Any) -> None:
        nonlocal attempts
        attempts += 1
        if attempts <= 2:
            raise PermissionError(5, "transient sharing violation", str(destination))
        real_replace(source, destination)

    monkeypatch.setattr(module.os, "replace", flaky_replace)
    monkeypatch.setattr(module.time, "sleep", lambda _seconds: None)

    write(target)

    assert attempts == 3
    assert json.loads(target.read_text(encoding="utf-8")) == {"ok": True}


def test_material_payload_blinds_aligned_vs_misindexed_mode_labels() -> None:
    dossier = {"presentation": "anonymous", "choices": {"solvent": []}}
    aligned = _material_information_payload(
        {
            "material_information": {
                "mode": "anonymous_nominal_properties",
                "dossier": dossier,
            },
            "material_catalog": {},
        }
    )
    misindexed = _material_information_payload(
        {
            "material_information": {
                "mode": "anonymous_misindexed_properties",
                "dossier": dossier,
            },
            "material_catalog": {},
        }
    )
    assert aligned == misindexed
    assert "anonymous_misindexed_properties" not in json.dumps(misindexed).lower()


def test_material_payload_marks_opaque_without_internal_mode_name() -> None:
    payload = _material_information_payload(
        {
            "material_information": {"mode": "opaque_codes"},
            "material_catalog": {},
        }
    )
    serialized = json.dumps(payload).lower()
    assert payload["material_information"]["availability"] == "opaque_identifiers_only"
    assert "opaque_codes" not in serialized


def test_material_payload_can_carry_a_blinded_initial_world_model() -> None:
    initial_model = {
        "schema_version": "chemworld-work-ii-initial-world-model-0.1",
        "locus": "parametric",
        "availability": "supplied_incomplete_model",
        "model": {
            "reference_context": {"electrolyte_profile": 0, "solvent": 0},
            "potential_window_V": [0.82, 0.96],
            "current_window_mA": [45.0, 65.0],
        },
        "interpretation": "Experimental evidence is authoritative.",
    }
    payload = _material_information_payload(
        {
            "material_information": {"mode": "opaque_codes"},
            "material_catalog": {},
        },
        initial_world_model=initial_model,
    )

    assert payload["material_information"]["availability"] == "opaque_identifiers_only"
    assert payload["initial_world_model"] == initial_model


def test_initial_world_model_rejects_participant_visible_arm_identity() -> None:
    with pytest.raises(ValueError, match="identity fields"):
        _material_information_payload(
            {"material_information": {"mode": "opaque_codes"}},
            initial_world_model={"locus": "parametric", "prior_arm": "aligned"},
        )


def test_initial_world_model_rejects_nested_participant_identity() -> None:
    with pytest.raises(ValueError, match=r"model\.condition_id"):
        _material_information_payload(
            {"material_information": {"mode": "opaque_codes"}},
            initial_world_model={
                "locus": "parametric",
                "model": {"condition_id": "hidden-arm-label"},
            },
        )


def test_public_task_contract_exposes_composition_and_explicit_closeout() -> None:
    composition = {
        "composition_id": "generated-world",
        "world": {"components": [{"kind": "reaction"}]},
        "task": {"resources": {"operation_budget": 16, "final_assays": 1}},
    }
    contract = _public_task_contract(
        {
            "task_id": "generated-world",
            "task_contract_hash": "a" * 64,
            "composition": composition,
            "allowed_operations": ["terminate", "measure"],
            "allowed_instruments": ["final_assay"],
            "method_budget_contract": {"complete_experiment_limit": 1},
        }
    )
    assert contract["composition"] == composition
    assert contract["experiment_lifecycle"] == {
        "schema_version": "chemworld-public-experiment-lifecycle-0.1",
        "planned_complete_experiments": 1,
        "explicit_terminate_required": True,
        "final_assay_required": True,
        "final_assay_after_terminate": True,
        "automatic_closeout": False,
    }


def _context(step: int, remaining: int) -> AgentDecisionContext:
    return AgentDecisionContext(
        step=step,
        task_id="reaction-to-assay",
        decision_stage="experiment_setup" if step == 1 else "experiment_control",
        campaign_state={
            "remaining_budget": remaining,
            "budget": 10,
            "experiment_index": 0,
            "campaign_resources": {
                "remaining": {
                    "vessel_starts": 6,
                    "material_amount_mol": {"material-M1": 0.2},
                },
                "hard_limits": {"instrument_uses": {"hplc": 4}},
            },
        },
        visible_metrics={"cost": 0.1 * (step - 1), "score": 0.0},
        latest_spectra={"has_spectral_packet": False},
        uncertainty={},
        constraint_flags={},
        available_operations=("add_reagent", "terminate"),
        previous_event_type=None if step == 1 else "operation_result",
    )


def _action(operation: str, fields: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "operation": operation,
        "valid": True,
        "schema": {
            "fields": fields,
            "required_fields": [field["field"] for field in fields],
        },
    }


def _view(*, with_raw: bool = False) -> dict[str, Any]:
    raw = (
        {
            "kind": "hplc_chromatogram",
            "axis": [0.0, 1.0, 2.0],
            "intensity": [0.1, 0.8, 0.2],
        }
        if with_raw
        else {}
    )
    return {
        "tool_json": {
            "available_actions": [
                _action(
                    "add_reagent",
                    [
                        {
                            "field": "amount_mol",
                            "bounds": {"low": 0.0, "high": 0.04},
                        }
                    ],
                ),
                _action("terminate", []),
                _action(
                    "add_solvent",
                    [
                        {
                            "field": "solvent",
                            "choices": [0, 1],
                            "choice_labels": {
                                "0": "solvent-S1",
                                "1": "solvent-S2",
                            },
                        },
                        {
                            "field": "volume_L",
                            "bounds": {"low": 0.0, "high": 0.05},
                        },
                    ],
                ),
            ],
            "raw_signal": raw,
            "processed_estimate": {"yield": 0.4} if with_raw else {},
        }
    }


_FAKE_CODEX = r"""
import json
import subprocess
import sys
from pathlib import Path

agent = Path(sys.argv[1])

def emit(value):
    print(json.dumps(value, separators=(",", ":")), flush=True)

emit({"type": "thread.started", "thread_id": "fake-thread"})
actions = [
    {"operation": "add_reagent", "amount_mol": 0.01},
    {"operation": "terminate"},
]
for index, action in enumerate(actions, start=1):
    result = subprocess.run(
        [
            sys.executable,
            str(agent / "lab_tool.py"),
            "step",
            "--expected-step",
            str(index),
            "--action-json",
            json.dumps(action, separators=(",", ":")),
        ],
        cwd=agent,
        capture_output=True,
        text=True,
        check=False,
    )
    emit({
        "type": "item.completed",
        "item": {
            "id": f"command-{index}",
            "type": "command_execution",
            "command": "python lab_tool.py step --expected-step N --action-json JSON",
            "aggregated_output": result.stdout,
            "exit_code": result.returncode,
            "status": "completed" if result.returncode == 0 else "failed",
        },
    })
    response = json.loads(result.stdout)
    if response.get("experiment_ended") or response.get("budget_exhausted"):
        break
emit({
    "type": "item.completed",
    "item": {
        "id": "final",
        "type": "agent_message",
        "text": json.dumps({
            "status": "experiment_complete",
            "summary": "The experiment was closed after the declared operations."
        }),
    },
})
emit({
    "type": "turn.completed",
    "usage": {
        "input_tokens": 1234,
        "cached_input_tokens": 234,
        "cache_write_input_tokens": 100,
        "output_tokens": 321,
        "reasoning_output_tokens": 200,
    },
})
"""

_FAKE_FINAL_ASSAY = r"""
import json
import subprocess
import sys
from pathlib import Path

agent = Path(sys.argv[1])

def emit(value):
    print(json.dumps(value, separators=(",", ":")), flush=True)

emit({"type": "thread.started", "thread_id": "fake-final-thread"})
action = {"operation": "measure", "instrument": "final_assay"}
result = subprocess.run(
    [
        sys.executable,
        str(agent / "lab_tool.py"),
        "step",
        "--expected-step",
        "1",
        "--action-json",
        json.dumps(action, separators=(",", ":")),
    ],
    cwd=agent,
    capture_output=True,
    text=True,
    check=False,
)
emit({
    "type": "item.completed",
    "item": {
        "id": "command-final",
        "type": "command_execution",
        "command": "python lab_tool.py step --expected-step 1 --action-json JSON",
        "aggregated_output": result.stdout,
        "exit_code": result.returncode,
        "status": "completed" if result.returncode == 0 else "failed",
    },
})
emit({
    "type": "item.completed",
    "item": {
        "id": "final",
        "type": "agent_message",
        "text": json.dumps({
            "status": "experiment_complete",
            "summary": "A successful final assay completed the experiment.",
        }),
    },
})
emit({
    "type": "turn.completed",
    "usage": {
        "input_tokens": 800,
        "cached_input_tokens": 100,
        "output_tokens": 200,
    },
})
"""

_FAKE_TAMPER_BEFORE_ACTION = r"""
import json
import time
import sys
from pathlib import Path

agent = Path(sys.argv[1])
root = agent.parent
active = json.loads((root / ".ipc" / "active_session.json").read_text(encoding="utf-8"))
session_id = active["session_id"]
request = {
    "schema_version": active["schema_version"],
    "session_id": session_id,
    "request_id": "tampered-request",
    "expected_step": 1,
    "action": {"operation": "terminate"},
}
request_path = agent / ".transport" / session_id / "requests" / "tampered-request.json"
request_path.write_text(json.dumps(request), encoding="utf-8")
(agent / "lab_tool.py").write_text("# tampered", encoding="utf-8")
time.sleep(10)
"""

_FAKE_TAMPER_AFTER_TERMINAL_RESPONSE = r"""
import json
import subprocess
import sys
from pathlib import Path

agent = Path(sys.argv[1])

def emit(value):
    print(json.dumps(value, separators=(",", ":")), flush=True)

emit({"type": "thread.started", "thread_id": "fake-tamper-thread"})
result = subprocess.run(
    [
        sys.executable,
        str(agent / "lab_tool.py"),
        "step",
        "--expected-step",
        "1",
        "--action-json",
        '{"operation":"terminate"}',
    ],
    cwd=agent,
    capture_output=True,
    text=True,
    check=False,
)
(agent / "lab_tool.py").write_text("# tampered after response", encoding="utf-8")
emit({
    "type": "item.completed",
    "item": {
        "id": "command-terminal",
        "type": "command_execution",
        "command": "python lab_tool.py step --expected-step 1 --action-json JSON",
        "aggregated_output": result.stdout,
        "exit_code": result.returncode,
        "status": "completed" if result.returncode == 0 else "failed",
    },
})
emit({
    "type": "item.completed",
    "item": {
        "id": "final",
        "type": "agent_message",
        "text": json.dumps({
            "status": "experiment_complete",
            "summary": "Terminal response received.",
        }),
    },
})
emit({
    "type": "turn.completed",
    "usage": {"input_tokens": 100, "output_tokens": 20},
})
"""

_FAKE_NO_REQUEST = r"""
import json
import time

print(json.dumps({"type": "thread.started", "thread_id": "fake-stalled-thread"}), flush=True)
time.sleep(10)
"""


def _fake_process_factory(
    commands: list[list[str]],
    prompts: list[str],
    *,
    script: str = _FAKE_CODEX,
):
    def factory(command: Any, prompt: str, cwd: Path):
        commands.append(list(command))
        prompts.append(prompt)
        return subprocess.Popen(
            [sys.executable, "-c", script, str(cwd)],
            cwd=cwd,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

    return factory


def test_custom_provider_command_uses_responses_and_no_secret(
    tmp_path: Path,
) -> None:
    agent = InteractiveCodexExperimentAgent(
        workspace=tmp_path / "workspace",
        role_id="test",
        model_provider="wellau",
        model_provider_name="WellAU",
        model_provider_base_url="https://api.wellau.com/v1",
        model_provider_env_key="WELLAU_API_KEY",
        process_factory=lambda command, prompt, cwd: None,
    )
    command = agent._command(
        instructions_path=tmp_path / "instructions.md",
        schema_path=tmp_path / "schema.json",
    )
    joined = " ".join(command)
    assert 'approval_policy="never"' in joined
    assert "approvals_reviewer" not in joined
    assert "mcp_servers.chemworld_lab.command" in joined
    assert "chemworld.agents.experiment_codex_mcp" in joined
    assert "mcp_servers.chemworld_lab.supports_parallel_tool_calls=false" in joined
    assert 'model_provider="wellau"' in joined
    assert 'model_providers.wellau.name="WellAU"' in joined
    assert 'model_providers.wellau.base_url="https://api.wellau.com/v1"' in joined
    assert 'model_providers.wellau.env_key="WELLAU_API_KEY"' in joined
    assert 'model_providers.wellau.wire_api="responses"' in joined
    assert "sk-live" not in joined.lower()


def test_bearer_provider_uses_isolated_codex_home_and_catalog(tmp_path: Path) -> None:
    key_path = tmp_path / "provider-key.txt"
    key_path.write_text("sk-test-provider-key", encoding="utf-8")
    catalog_path = tmp_path / "models.json"
    catalog_path.write_text('{"models": [{"slug": "deepseek-v4-flash"}]}', encoding="utf-8")
    agent = InteractiveCodexExperimentAgent(
        workspace=tmp_path / "workspace",
        role_id="test",
        model="deepseek-v4-flash",
        reasoning_effort="high",
        model_provider="deepseek",
        model_provider_name="DeepSeek",
        model_provider_base_url="https://api.deepseek.com/",
        model_provider_wire_api="responses",
        model_provider_auth_mode="experimental_bearer_token",
        model_provider_api_key_file=key_path,
        model_provider_model_catalog_json=catalog_path,
        process_factory=lambda command, prompt, cwd: None,
    )
    temp_root = tmp_path / "launch"
    temp_root.mkdir()
    agent._prepare_provider_launch(temp_root=temp_root)
    assert agent._use_isolated_codex_home is True
    config_path = temp_root / "codex-home" / "config.toml"
    config = config_path.read_text(encoding="utf-8")
    assert 'model = "deepseek-v4-flash"' in config
    assert 'wire_api = "responses"' in config
    assert "sk-test-provider-key" in config
    command = agent._command(
        instructions_path=tmp_path / "instructions.md",
        schema_path=tmp_path / "schema.json",
    )
    assert "--ignore-user-config" not in command


def test_one_codex_process_controls_two_runner_operations(
    tmp_path: Path,
) -> None:
    commands: list[list[str]] = []
    prompts: list[str] = []
    task_info = {
        "task_id": "reaction-to-assay",
        "objective": "balanced",
        "budget": 10,
        "episode_mode": "single_experiment",
        "experiment_lifecycle": {
            "terminate_effect": "only final assay becomes legal",
        },
        "scoring_contract": {"contract_id": "score-v1", "yield_weight": 0.5},
        "material_information": {"mode": "anonymous_nominal_properties"},
        "material_catalog": {
            "solvent-S1": {"secret_property_value": 12.3},
        },
    }
    agent = InteractiveCodexExperimentAgent(
        workspace=tmp_path / "workspace",
        role_id="interactive-test",
        process_factory=_fake_process_factory(commands, prompts),
        request_timeout_s=5.0,
        finalization_timeout_s=5.0,
    )
    agent.reset(task_info, seed=0)
    assert agent.workspace.snapshot_agent_files() == {}

    first = agent.act_with_public_view(_context(1, 10), _view())
    assert first == {"operation": "add_reagent", "amount_mol": 0.01}
    current = json.loads(agent.workspace.current_path.read_text(encoding="utf-8"))
    assert current["campaign_resources"]["remaining"]["vessel_starts"] == 6
    assert current["campaign_resources"]["remaining"]["material_amount_mol"]["material-M1"] == 0.2
    solvent = next(item for item in current["legal_actions"] if item["operation"] == "add_solvent")
    assert solvent["solvent"]["choice_labels"]["0"] == "solvent-S1"
    assert agent.method_resource_usage()["provider_usage_pending"] is True
    assert agent.method_resource_usage()["in_flight_model_call_count"] == 1
    agent.update(
        first,
        {"cost": 0.1, "score": 0.0},
        0.0,
        {
            "transaction_status": "committed",
            "operation_type": "add_reagent",
            "experiment_ended": False,
            "observed_keys": ["cost", "score"],
            "constraint_flags": {},
        },
    )

    second = agent.act_with_public_view(_context(2, 9), _view(with_raw=True))
    assert second == {"operation": "terminate"}
    agent.update(
        second,
        {"cost": 0.1, "score": 0.2},
        0.2,
        {
            "transaction_status": "committed",
            "operation_type": "terminate",
            "experiment_ended": True,
            "observed_keys": ["cost", "score"],
            "constraint_flags": {},
            "leaderboard_score": 0.2,
        },
    )

    assert len(commands) == 1
    assert "--ephemeral" in commands[0]
    assert "--sandbox" in commands[0]
    assert commands[0][-1] == str(agent.workspace.agent_directory)
    assert "secret_property_value" not in prompts[0]
    assert "../reference/material_information.json" in prompts[0]
    assert "chemworld_lab" in prompts[0]
    assert "host-owned STDIO MCP" in prompts[0]
    assert "python lab_tool.py" not in prompts[0]
    assert "score-v1" in prompts[0]
    usage = agent.method_resource_usage()
    assert usage["provider_usage_pending"] is False
    assert usage["input_token_count"] == 1234
    assert usage["output_token_count"] == 321
    receipt = agent.provider_receipts()[0]
    assert receipt["usage"]["reasoning_output_tokens"] == 200
    assert receipt["final_payload_encoding"] == "json"
    assert receipt["final_payload_summary"].startswith("The experiment")
    assert receipt["lab_tool_integrity_verified_after_session"] is True
    assert receipt["mcp_tool_integrity_verified_after_session"] is True
    assert receipt["experiment_tool_integrity_verified_after_session"] is True
    assert receipt["private_reasoning_retained"] is False
    assert receipt["scientific_compliance_mcp_tool_failure_count"] == 0
    assert receipt["mcp_tool_failure_taxonomy"]["counts_by_category"] == {
        "provider_network": 0,
        "transport_ipc_os": 0,
        "agent_invalid": 0,
        "unclassified": 0,
    }
    assert len(receipt["tool_events"]) == 2
    assert all(event["output_body_retained"] is False for event in receipt["tool_events"])
    assert agent.workspace.snapshot_agent_files() == {}
    assert list((tmp_path / "workspace" / "public" / "artifacts").glob("*.json")) == []
    assert list(agent.workspace.sessions_directory.iterdir()) == []
    assert list(agent.workspace.transport_directory.iterdir()) == []
    assert not (agent.workspace.agent_directory / "request.json").exists()


def test_measurement_artifact_is_immutable_across_update_and_next_state(
    tmp_path: Path,
) -> None:
    def unused_factory(command: Any, prompt: str, cwd: Path):
        del command, prompt, cwd
        raise AssertionError("no process should be launched")

    agent = InteractiveCodexExperimentAgent(
        workspace=tmp_path / "workspace",
        role_id="artifact-test",
        process_factory=unused_factory,
    )
    agent.reset({"task_id": "x", "budget": 3}, seed=0)
    action = {"operation": "measure", "instrument": "uvvis"}
    raw = _view(with_raw=True)["tool_json"]["raw_signal"]
    artifact = agent._publish_outcome_artifact(
        event_id="runner-operation-0001",
        action=action,
        info={"raw_signal": raw},
    )
    assert artifact is not None
    agent._pending_outcome = {
        "event_id": "runner-operation-0001",
        "action": action,
        "artifact": artifact,
    }

    assert agent._publish_latest_artifact(_view(with_raw=True)) == artifact
    assert len(list(agent.workspace.artifacts_directory.glob("*.json"))) == 1


def test_final_assay_or_termination_is_never_added_by_host(tmp_path: Path) -> None:
    commands: list[list[str]] = []
    prompts: list[str] = []
    agent = InteractiveCodexExperimentAgent(
        workspace=tmp_path / "workspace",
        role_id="interactive-test",
        process_factory=_fake_process_factory(commands, prompts),
        request_timeout_s=5.0,
        finalization_timeout_s=5.0,
    )
    agent.reset({"task_id": "x", "budget": 1}, seed=0)
    action = agent.act_with_public_view(_context(1, 1), _view())
    assert action["operation"] == "add_reagent"
    agent.update(
        action,
        {"score": 0.0},
        0.0,
        {
            "transaction_status": "committed",
            "operation_type": "add_reagent",
            "experiment_ended": False,
            "observed_keys": ["score"],
            "constraint_flags": {},
        },
    )
    receipt = agent.provider_receipts()[0]
    assert receipt["terminal_reason"] == "budget_exhausted"
    history = [
        json.loads(line)
        for line in agent.workspace.history_path.read_text(encoding="utf-8").splitlines()
    ]
    assert [event["action"]["operation"] for event in history] == ["add_reagent"]


def test_successful_single_experiment_final_assay_finalizes_without_info_flag(
    tmp_path: Path,
) -> None:
    commands: list[list[str]] = []
    prompts: list[str] = []
    agent = InteractiveCodexExperimentAgent(
        workspace=tmp_path / "workspace",
        role_id="interactive-test",
        process_factory=_fake_process_factory(
            commands,
            prompts,
            script=_FAKE_FINAL_ASSAY,
        ),
        request_timeout_s=5.0,
        finalization_timeout_s=5.0,
    )
    agent.reset({"task_id": "x", "budget": 10}, seed=0)
    action = agent.act_with_public_view(_context(1, 10), _view())
    assert action == {"operation": "measure", "instrument": "final_assay"}
    agent.update(
        action,
        {"score": 0.7},
        0.7,
        {
            "transaction_status": "committed",
            "operation_type": "measure",
            "instrument": "final_assay",
            "experiment_ended": False,
            "leaderboard_score": 0.7,
            "observed_keys": ["score"],
            "constraint_flags": {},
        },
    )

    receipt = agent.provider_receipts()[0]
    assert receipt["terminal_reason"] == "experiment_complete"
    assert agent.method_resource_usage()["provider_usage_pending"] is False


def test_process_exit_before_action_is_fail_closed_after_bounded_restart(
    tmp_path: Path,
) -> None:
    calls = 0

    def factory(command: Any, prompt: str, cwd: Path):
        nonlocal calls
        del command, prompt
        calls += 1
        return subprocess.Popen(
            [sys.executable, "-c", "raise SystemExit(0)"],
            cwd=cwd,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

    agent = InteractiveCodexExperimentAgent(
        workspace=tmp_path / "workspace",
        role_id="interactive-test",
        process_factory=factory,
        request_timeout_s=1.0,
        finalization_timeout_s=1.0,
        pre_action_restart_limit=1,
    )
    agent.reset({"task_id": "x", "budget": 2}, seed=0)
    with pytest.raises(InteractiveCodexExperimentError, match="no fallback"):
        agent.act_with_public_view(_context(1, 2), _view())
    assert calls == 2
    assert len(agent.provider_receipts()) == 2
    assert all(
        receipt["status"] == "interrupted_before_next_action"
        for receipt in agent.provider_receipts()
    )
    assert agent.workspace.history_path.read_text(encoding="utf-8") == ""


def test_session_wall_time_limit_stops_stalled_process_and_records_receipt(
    tmp_path: Path,
) -> None:
    commands: list[list[str]] = []
    prompts: list[str] = []
    progress: list[dict[str, Any]] = []
    agent = InteractiveCodexExperimentAgent(
        workspace=tmp_path / "workspace",
        role_id="session-wall-limit-test",
        process_factory=_fake_process_factory(
            commands,
            prompts,
            script=_FAKE_NO_REQUEST,
        ),
        request_timeout_s=5.0,
        finalization_timeout_s=1.0,
        session_wall_time_limit_s=0.1,
        session_progress_callback=progress.append,
        session_progress_interval_s=0.02,
        pre_action_restart_limit=0,
    )
    agent.reset({"task_id": "x", "budget": 1}, seed=0)

    with pytest.raises(InteractiveCodexExperimentError, match="session_wall_time_limit"):
        agent.act_with_public_view(_context(1, 1), _view())

    receipt = agent.provider_receipts()[0]
    assert receipt["status"] == "interrupted_before_next_action"
    assert receipt["failure_type"] == "session_wall_time_limit"
    assert receipt["session_elapsed_s"] >= 0.1
    assert receipt["usage_observed"] is False
    assert receipt["usage_unavailable_reason"] == (
        "codex_cli_emitted_no_usage_before_forced_termination"
    )
    assert receipt["belief_snapshots"] == []
    assert receipt["belief_snapshot_count"] == 0
    assert receipt["final_recommendation"] is None
    assert receipt["final_recommendation_source"] is None
    assert receipt["scientific_compliance_mcp_tool_failure_count"] == 0
    assert receipt["mcp_tool_failure_taxonomy"]["counts_by_category"] == {
        "provider_network": 0,
        "transport_ipc_os": 0,
        "agent_invalid": 0,
        "unclassified": 0,
    }
    usage = agent.method_resource_usage()
    assert usage["provider_usage_pending"] is False
    assert usage["token_counts_observed"] is False
    assert progress
    assert progress[0]["event"] == "provider_session_liveness"


def test_consecutive_mcp_failure_limit_is_independent_of_total_limit(
    tmp_path: Path,
) -> None:
    def unused_factory(command: Any, prompt: str, cwd: Path):
        del command, prompt, cwd
        raise AssertionError("no process should be launched")

    agent = InteractiveCodexExperimentAgent(
        workspace=tmp_path / "workspace",
        role_id="consecutive-limit-test",
        process_factory=unused_factory,
        max_recovered_mcp_tool_failures=3,
        max_consecutive_mcp_tool_failures=1,
        max_provider_error_events=1,
    )
    assert (
        agent._operational_limit_failure(
            {
                "session_elapsed_s": 1.0,
                "recovered_mcp_tool_failure_count": 2,
                "current_consecutive_mcp_tool_failure_count": 1,
                "provider_error_event_count": 0,
            }
        )
        is None
    )
    assert (
        agent._operational_limit_failure(
            {
                "session_elapsed_s": 1.0,
                "recovered_mcp_tool_failure_count": 2,
                "current_consecutive_mcp_tool_failure_count": 2,
                "provider_error_event_count": 0,
            }
        )
        == "max_consecutive_mcp_tool_failures"
    )


def test_lab_tool_tamper_is_rejected_before_action_acceptance(tmp_path: Path) -> None:
    commands: list[list[str]] = []
    prompts: list[str] = []
    agent = InteractiveCodexExperimentAgent(
        workspace=tmp_path / "workspace",
        role_id="tamper-test",
        process_factory=_fake_process_factory(
            commands,
            prompts,
            script=_FAKE_TAMPER_BEFORE_ACTION,
        ),
        request_timeout_s=5.0,
        finalization_timeout_s=2.0,
        pre_action_restart_limit=0,
    )
    agent.reset({"task_id": "x", "budget": 2}, seed=0)

    with pytest.raises(InteractiveCodexExperimentError, match="modified"):
        agent.act_with_public_view(_context(1, 2), _view())

    assert agent.workspace.history_path.read_text(encoding="utf-8") == ""
    assert agent.provider_receipts()[0]["lab_tool_integrity_verified_after_session"] is False


def test_lab_tool_tamper_after_terminal_response_fails_post_session_check(
    tmp_path: Path,
) -> None:
    commands: list[list[str]] = []
    prompts: list[str] = []
    agent = InteractiveCodexExperimentAgent(
        workspace=tmp_path / "workspace",
        role_id="tamper-test",
        process_factory=_fake_process_factory(
            commands,
            prompts,
            script=_FAKE_TAMPER_AFTER_TERMINAL_RESPONSE,
        ),
        request_timeout_s=5.0,
        finalization_timeout_s=5.0,
    )
    agent.reset({"task_id": "x", "budget": 2}, seed=0)
    action = agent.act_with_public_view(_context(1, 2), _view())
    assert action == {"operation": "terminate"}

    with pytest.raises(InteractiveCodexExperimentError, match="post-session integrity"):
        agent.update(
            action,
            {"score": 0.2},
            0.2,
            {
                "transaction_status": "committed",
                "operation_type": "terminate",
                "experiment_ended": True,
                "observed_keys": ["score"],
                "constraint_flags": {},
            },
        )

    assert agent.provider_receipts()[0]["lab_tool_integrity_verified_after_session"] is False


def test_campaign_can_start_fresh_exec_while_agent_directory_persists(
    tmp_path: Path,
) -> None:
    commands: list[list[str]] = []
    prompts: list[str] = []
    agent = InteractiveCodexExperimentAgent(
        workspace=tmp_path / "workspace",
        role_id="interactive-test",
        process_factory=_fake_process_factory(commands, prompts),
        request_timeout_s=5.0,
        finalization_timeout_s=5.0,
    )
    agent.reset({"task_id": "campaign", "budget": 10}, seed=0)
    memory = agent.workspace.agent_directory / "hypotheses.md"
    memory.write_text("persistent agent-authored hypothesis", encoding="utf-8")

    first = agent.act_with_public_view(_context(1, 10), _view())
    agent.update(
        first,
        {"score": 0.1},
        0.1,
        {
            "transaction_status": "committed",
            "operation_type": first["operation"],
            "experiment_ended": True,
            "observed_keys": ["score"],
            "constraint_flags": {},
        },
    )
    second = agent.act_with_public_view(_context(2, 9), _view())
    agent.update(
        second,
        {"score": 0.2},
        0.2,
        {
            "transaction_status": "committed",
            "operation_type": second["operation"],
            "experiment_ended": True,
            "observed_keys": ["score"],
            "constraint_flags": {},
        },
    )

    assert len(commands) == 2
    assert len(agent.provider_receipts()) == 2
    assert memory.read_text(encoding="utf-8") == "persistent agent-authored hypothesis"
