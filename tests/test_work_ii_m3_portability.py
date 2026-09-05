"""Information isolation, real transport projection, retained failures and nested inference."""

import json
from copy import deepcopy

import pytest
from scripts import run_work_ii_factorial as transport
from scripts import run_work_ii_m3_portability as runner
from scripts.run_work_ii_factorial import execute_plan, seal

from chemworld.eval.work_ii_factorial import TASKS, compile_design, score_slots
from chemworld.eval.work_ii_factorial_replication import replication_protocol, source_schedule
from chemworld.eval.work_ii_m3_portability import (
    CONDITIONS,
    portability_protocol,
    recipient_input,
    recipient_prompt,
    recipient_schedule,
    summarize_portability,
)


def protocol_fixture():
    return portability_protocol(
        replication_protocol(),
        {"report": "fixture", "report_sha256": "fixture", "protocol": "fixture"},
    )


def packet_fixture(protocol, task=TASKS[0]):
    packet = compile_design(protocol, task)
    for row in packet["evidence"]:
        row["score"] = 0.2 + 0.1 * row["xy"][0]
    return packet


def test_outcome_blind_new_candidates_and_within_world_order_balance():
    protocol = protocol_fixture()
    original = replication_protocol()
    assert protocol["worlds"] == original["worlds"]
    assert protocol["tasks"] == original["tasks"]
    assert protocol["evidence_xy"] == original["evidence_xy"]
    assert not {tuple(xy) for xy in protocol["candidate_xy"]} & {
        tuple(xy) for key in ("evidence_xy", "candidate_xy") for xy in original[key]
    }
    for axis in (0, 1):
        assert sorted(int(xy[axis] * 8) for xy in protocol["candidate_xy"]) == list(range(8))
    schedule = recipient_schedule(protocol)
    assert len(schedule) == len({row["call_id"] for row in schedule}) == 160
    assert len(protocol["worlds"]) * len(protocol["candidate_xy"]) == 80
    for world in protocol["worlds"]:
        for arm in CONDITIONS:
            rows = [
                row
                for row in schedule
                if row["cluster_id"] == world["cluster_id"] and row["condition"] == arm
            ]
            assert sorted(row["serial_position"] for row in rows) == [1, 2, 3, 4]


@pytest.mark.parametrize("condition", CONDITIONS)
def test_actual_outgoing_transport_respects_information_arm(tmp_path, monkeypatch, condition):
    packet = packet_fixture(protocol_fixture())
    packet["private_world"] = "FORBIDDEN_PRIVATE_WORLD"
    for row in packet["candidates"]:
        row["score"] = "FORBIDDEN_CANDIDATE_SCORE"
    law = [0.2, 0.1, 0, 0, 0, 0]
    prompt = recipient_prompt(packet, condition, law)
    received = []
    monkeypatch.setattr(transport, "_prepare_codex_home", lambda *a: {})
    monkeypatch.setattr(
        transport, "_initial_command", lambda *a: ["fixture", "--sandbox", "read-only"]
    )

    def launch(command, outgoing, **kwargs):
        received.append(outgoing)
        assert command[1:3] == ["--disable", "shell_tool"]
        assert not list(kwargs["cwd"].iterdir())
        return {
            "status": "completed",
            "thread_id": "fresh",
            "usage": {},
            "final_payload": {"candidate_id": "c01"},
            "tool_event_count": 0,
        }

    monkeypatch.setattr(transport, "_launch_turn", launch)
    result = transport.provider_call(
        tmp_path,
        condition,
        "gpt",
        "decision",
        packet,
        law,
        None,
        0,
        total=160,
        provider_override={"fixture": True},
        prompt_override=prompt,
    )
    assert result["status"] == "completed"
    assert received == [prompt]
    public = json.loads(received[0].split("\nINPUT:\n")[1])
    assert ("evidence" in public) == (condition == "raw")
    assert ("artifact" in public) == (condition in ("L", "F"))
    assert "FORBIDDEN" not in received[0]
    assert "world" not in public and "condition" not in public


def test_no_provenance_label_and_no_accidental_raw_dependence():
    packet, law = packet_fixture(protocol_fixture()), [0.2, 0.1, 0, 0, 0, 0]
    assert recipient_prompt(packet, "L", law) == recipient_prompt(packet, "F", law)
    before = {arm: recipient_input(packet, arm, law) for arm in ("none", "L", "F")}
    packet["evidence"] = [{"secret": "should never be read"}]
    for arm, expected in before.items():
        assert recipient_input(packet, arm, law) == expected
    with pytest.raises(ValueError):
        recipient_input(packet, "L", None)


def setup_run(tmp_path, monkeypatch, physical_failure=False):
    protocol = protocol_fixture()
    monkeypatch.setattr(runner, "check_frozen", lambda root: protocol)
    seal(tmp_path / "protocol.json", protocol)
    seal(tmp_path / "release.json", {"tested_commit": "fixture", "execution_surface": {}})
    seal(
        tmp_path / "physical.json",
        {
            "status": "failed" if physical_failure else "completed",
            "stop_reason": "physical_or_replay_failure" if physical_failure else None,
            "completed": 0 if physical_failure else 80,
            "receipts": [],
        },
    )
    seal(
        tmp_path / "source.json",
        {
            "artifacts": {
                state["state_id"]: {"L": [0.2, 0.1, 0, 0, 0, 0], "F": [0.2, 0.1, 0, 0, 0, 0]}
                for state in source_schedule(protocol)
            },
            "reused_source_costs": {},
        },
    )
    if not physical_failure:
        for world in protocol["worlds"]:
            seal(
                tmp_path / "public" / f"{world['cluster_id']}.json",
                packet_fixture(protocol, world["task"]),
            )
    return protocol


def fake_provider(root, call_id, model, stage, packet, law, progress, completed, **kwargs):
    return {
        "call_id": call_id,
        "thread_id": call_id,
        "status": "completed",
        "final_payload": {"candidate_id": "c01"},
        "usage": {"input_tokens": 10, "output_tokens": 1},
        "raw_events": "NEVER_EXPORT_RAW",
        "elapsed_s": 1,
    }


def test_no_truth_dependency_until_all_choices_sealed_and_sanitized_export(tmp_path, monkeypatch):
    protocol = setup_run(tmp_path, monkeypatch)
    monkeypatch.setattr(runner, "provider_call", fake_provider)
    with pytest.raises(FileNotFoundError):
        runner.analyze(tmp_path)
    selections = runner.run_provider_block(tmp_path)  # No private_scores.json exists.
    assert len(selections["slots"]) == len(selections["calls"]) == 160
    assert len(selections["controls"]) == 90
    monkeypatch.setattr(runner, "provider_call", lambda *a, **k: pytest.fail("paid retry"))
    assert runner.run_provider_block(tmp_path) == selections
    seal(
        tmp_path / "private_scores.json",
        {
            world["cluster_id"]: {f"c{i + 1:02d}": 0.2 + i * 0.05 for i in range(8)}
            for world in protocol["worlds"]
        },
    )
    report = runner.analyze(tmp_path)
    assert report["execution_valid"] and report["provider_completed"] == 160
    assert report["provider_usage"]["input_tokens"] == 1600
    assert report["additional_independent_worlds"] == 0
    assert len(report["statistics"]["world_contrasts"]) == 60
    assert "NEVER_EXPORT_RAW" not in json.dumps(report)
    destination = tmp_path / "export.json"
    assert runner.export_report(tmp_path, destination) == report
    assert runner.export_report(tmp_path, destination) == report
    destination.write_text('{"different":"result"}', encoding="utf-8")
    with pytest.raises(ValueError, match="replace"):
        runner.export_report(tmp_path, destination)


@pytest.mark.parametrize("violation", ["reused", "tool", "identity", "schema"])
def test_protocol_stop_and_participant_failure_keep_all_opportunities(
    tmp_path, monkeypatch, violation
):
    setup_run(tmp_path, monkeypatch)
    attempted = []

    def provider(*args, **kwargs):
        attempted.append(args[1])
        receipt = fake_provider(*args, **kwargs)
        receipt["thread_id"] = (
            None if violation == "identity" else "same" if violation == "reused" else args[1]
        )
        receipt["tool_event_count"] = int(violation == "tool")
        if violation == "schema":
            receipt.update(status="schema_failed", failure_type="invalid candidate")
        return receipt

    monkeypatch.setattr(runner, "provider_call", provider)
    result = runner.run_provider_block(tmp_path)
    assert len(result["slots"]) == len(result["calls"]) == 160
    assert len(attempted) == (160 if violation == "schema" else 2 if violation == "reused" else 1)
    assert bool(result["stop_reason"]) == (violation != "schema")


def test_failed_physics_keeps_unstarted_denominator(tmp_path, monkeypatch):
    setup_run(tmp_path, monkeypatch, physical_failure=True)
    monkeypatch.setattr(runner, "provider_call", lambda *a, **k: pytest.fail("provider launched"))
    runner.run_provider_block(tmp_path)
    result = runner.analyze(tmp_path)
    assert not result["execution_valid"] and result["statistics"] is None
    assert result["provider_attempted"] == 0 and result["condition_scheduled"] == 160
    assert len(result["failures"]) == 320


def scored_fixture(protocol):
    rows = []
    for state in source_schedule(protocol):
        benefit = 0.1 if state["task"] == TASKS[0] else 0.3
        for arm in CONDITIONS:
            row = {
                **{
                    key: state[key] for key in ("state_id", "cluster_id", "task", "model", "repeat")
                },
                "condition": arm,
                "status": "completed",
                "candidate_id": "good" if arm == "L" else "bad",
            }
            rows.extend(score_slots([row], {"good": 0.8, "bad": 0.8 - benefit}))
    return rows


def test_primary_direction_world_inference_and_nested_repeat_invariance():
    protocol = protocol_fixture()
    rows = scored_fixture(protocol)
    result = summarize_portability(rows, protocol)
    assert result["contrasts"][0]["mean_difference"] == pytest.approx(-0.2)
    assert result["contrasts"][0]["interval"] == pytest.approx([-0.2, -0.2])
    assert result["primary_material_benefit_supported"]
    assert all(row["interval_level"] == 0.99 for row in result["contrasts"][1:])
    repeated = deepcopy(protocol)
    repeated["model_repeats"] = 4
    assert (
        summarize_portability(scored_fixture(repeated), repeated)["contrasts"]
        == result["contrasts"]
    )
    with pytest.raises(ValueError, match="denominator"):
        summarize_portability(rows[:-1], protocol)
    rows[0].update(
        status="schema_failed",
        raw_regret=None,
        failure_aware_regret=1.0,
        near_optimal=False,
        top1=False,
    )
    failed = summarize_portability(rows, protocol)
    assert any(row["completed_pair_count"] == 3 for row in failed["world_contrasts"])


@pytest.mark.parametrize("task", TASKS)
def test_shared_physical_constructor_and_exact_replay_on_development_fixture(tmp_path, task):
    protocol = protocol_fixture()
    protocol.update(
        world_seed=0, formal_result=False, noise_namespace="m3-development-qualification"
    )
    row = compile_design(protocol, task)["candidates"][0]
    receipt = execute_plan(protocol, task, row, tmp_path / "candidate", 0)
    assert receipt["status"] == "completed"
    assert receipt["action_plan_equal"] and receipt["replay"]["verified"]
    assert 0 <= receipt["score"] <= 1
