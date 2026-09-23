"""Offline functional checks only; synthetic replies are never scientific observations."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

import pytest
import scripts.run_work_ii_eq_fixed_evidence as trial


@pytest.fixture
def prepared(tmp_path):
    source, root = tmp_path / "synthetic-source", tmp_path / "readout"
    # Retained recipe/final-assay summaries exercise the real importer; intermediate fixtures
    # are deliberately synthetic and never written into an actual experiment directory.
    for world in trial.WORLD_IDS:
        for arm in trial.SOURCE_ARMS:
            cell = f"{world}--{arm}"
            public = trial.read(trial.EXPORT / "sources" / cell / "RESULT.json")
            rows = []
            for batch in public["source"]["batches"]:
                for action in batch["actions"]:
                    final = action.get("instrument") == "final_assay"
                    observation = batch["metrics"] if final else {"pH_normalized": 0.123456}
                    rows.append(
                        {
                            "action": action,
                            "experiment_index": batch["lifecycle_index"] - 1,
                            "transaction_status": "committed",
                            "instrument": action.get("instrument"),
                            "terminated": final or action["operation"] == "terminate",
                            "truncated": False,
                            "observation": observation,
                            "agent_trace": "SECRET_DONOR_THINKING",
                            "evaluation_outcome": {"secret": "HIDDEN_TRUTH"},
                            "agent_visible_observation": {
                                "observation": observation,
                                "views": {
                                    "tool_json": {
                                        "raw_signal": {"fixture": "synthetic_intermediate"},
                                        "research_brief": {"prior_record": "SECRET_DONOR_DOSSIER"},
                                        "lab_report": {
                                            "failure_summary": {"transaction_status": "committed"}
                                        },
                                    }
                                },
                            },
                        }
                    )
            folder = source / "sources" / cell
            folder.mkdir(parents=True)
            (folder / "trajectory.jsonl").write_text(
                "\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8"
            )
            trial.write(
                folder / "workspace/reference/task_contract.json",
                {
                    "allowed_instruments": ["ph_meter", "uvvis", "final_assay"],
                    "operation_contracts": {"measure": {"required_fields": ["instrument"]}},
                    "instrument_contracts": {"ph_meter": {"unit": "pH"}},
                    "initial_world_model": "SECRET_DONOR_DOSSIER",
                    "world_id": world,
                    "arm": arm,
                },
            )
    trial.prepare(source, root)
    return source, root


def payload(value=0.25):
    return {
        "rationale": "Synthetic offline reply.",
        "predictions": [
            {
                "query_id": f"Q{i:02d}",
                "rationale": "Synthetic offline prediction.",
                "metrics": {
                    m: {
                        "estimate": value,
                        "lower80": max(0, value - 0.1),
                        "upper80": min(1, value + 0.1),
                    }
                    for m in trial.METRICS
                },
            }
            for i in range(1, 13)
        ],
    }


def offline_home(folder, provider):
    del provider
    (folder / "codex-home").mkdir()
    return {"CODEX_HOME": str(folder / "codex-home")}


def test_materialization_keeps_observations_but_excludes_source_beliefs(prepared):
    _, root = prepared
    assert trial.check(root, environment=False)["pairs"] == 15
    design = trial.read(root / "design.json")
    for cell in design["cells"]:
        packet = trial.read(root / "packets" / f"{cell['id']}.json")
        serialized = trial.encoded(packet)
        for forbidden in (
            "SECRET_DONOR",
            "HIDDEN_TRUTH",
            "EQ-W",
            "MisIndexed",
            "Aligned",
            "Opaque",
        ):
            assert forbidden not in serialized
        assert packet["records"][0]["observation"]["pH_normalized"] == 0.123456
        assert "synthetic_intermediate" in serialized
        assert len(packet["queries"]) == 12
    opaque = root / "packets/R01.json"
    changed = trial.read(opaque)
    changed["records"][0]["observation"]["pH_normalized"] = 0.4
    trial.write(opaque, changed)
    with pytest.raises(ValueError, match="paired evidence differs"):
        trial.check(root, environment=False)


def test_missing_raw_inputs_cannot_be_replaced_by_final_assays(tmp_path):
    with pytest.raises(ValueError, match="EQ-W05--MisIndexed"):
        trial.prepare(tmp_path / "absent", tmp_path / "output")
    assert not (tmp_path / "output").exists()


def test_actual_entrypoint_uses_independent_sessions_and_finishes_once(prepared, monkeypatch):
    _, root = prepared
    original_check = trial.check
    monkeypatch.setattr(trial, "check", lambda root, **kw: original_check(root, environment=False))
    monkeypatch.setattr(trial, "_prepare_codex_home", offline_home)
    monkeypatch.setattr(trial.provider.shutil, "which", lambda _: "codex")
    calls, homes = [], set()

    def launch(
        command, message, workspace, environment, output, timeout, enabled, audit, progress, **kw
    ):
        assert "resume" not in command
        assert "--ignore-user-config" in command and "shell_tool" in command
        assert "chemworld_lab" not in " ".join(command)
        assert timeout == 1200 and kw["numerics_budget"].limit == 128
        assert "model_context_window=872000" in command
        assert not (Path(environment["CODEX_HOME"]) / "sessions").exists()
        assert {p.name for p in workspace.iterdir()} == {"answer-schema.json", "instructions.md"}
        homes.add(environment["CODEX_HOME"])
        packet = json.loads(message.removeprefix("INPUT:\n"))
        assert "truth" not in packet
        calls.append(packet)
        return {
            "payload": payload(),
            "failure": None,
            "elapsed_s": 0,
            "usage": {"input_tokens": 5, "output_tokens": 10},
            "numerics_attempts": 0,
        }

    monkeypatch.setattr(trial.provider, "launch", launch)
    result = trial.run(root)
    assert len(calls) == len(homes) == 30
    assert result["terminal_sessions"] == result["valid_sessions"] == 30
    assert result["valid_pairs"] == 15 and result["complete_worlds"] == 5
    assert result["primary"]["macro"]["interaction"] == 0
    assert trial.run(root) == result
    assert len(calls) == 30  # Running an already completed block never calls again.


def test_group_scoring_has_the_right_sign_and_reference_denominators():
    truth = {f"Q{i:02d}": [dict.fromkeys(trial.METRICS, 0.2)] * 5 for i in range(1, 13)}
    opaque, aligned = payload(0.3), payload(0.2)
    for row in aligned["predictions"]:
        if row["query_id"] in trial.DILUTE:
            row["metrics"] = {
                m: {"estimate": 0.5, "lower80": 0.4, "upper80": 0.6} for m in trial.METRICS
            }
    a = trial.score(aligned, truth, trial.DILUTE)
    o = trial.score(opaque, truth, trial.DILUTE)
    assert a["queries"] == 3 and a["references_per_metric"] == 15
    assert a["metrics"]["macro"]["mae"] - o["metrics"]["macro"]["mae"] == pytest.approx(0.2)
    assert a["metrics"]["macro"]["interval_score"] == pytest.approx(2.2)
    other = [q for q in truth if q not in trial.DILUTE]
    assert trial.score(aligned, truth, other)["references_per_metric"] == 45
    assert trial.score(aligned, truth, other)["metrics"]["macro"]["mae"] == 0


def test_three_transport_failures_stop_without_retries_and_preserve_denominator(
    prepared, monkeypatch
):
    _, root = prepared
    check = trial.check
    monkeypatch.setattr(trial, "check", lambda root, **kw: check(root, environment=False))
    calls = []

    def fail(*args):
        calls.append(args[2]["id"])
        return {"failure": "provider_failure", "payload": None}

    monkeypatch.setattr(trial, "execute_cell", fail)
    report = trial.run(root)
    assert len(calls) == 3
    assert report["planned_sessions"] == 30 and report["unstarted_sessions"] == 27
    assert report["primary"] is None and len(report["failures"]) == 3
    with pytest.raises(ValueError, match="block stopped"):
        trial.run(root)
    assert len(calls) == 3


def test_schema_failure_is_retained_without_changing_world_weights(prepared, monkeypatch):
    _, root = prepared
    design = trial.read(root / "design.json")
    for i, cell in enumerate(design["cells"]):
        answer = payload() if i else {"predictions": []}
        folder = root / "sessions" / cell["id"]
        trial.write(folder / "started.json", {"design_sha256": trial.digest(design)})
        trial.write(folder / "result.json", trial.terminal_result({"payload": answer}, design))
    report = trial.analyze(root)
    assert report["valid_sessions"] == 29 and report["valid_pairs"] == 14
    assert report["complete_worlds"] == 4 and report["primary"] is None
    assert report["worlds"][0]["valid_pairs"] == 2
    assert report["worlds"][0]["contrast"] is None
    changed = copy.deepcopy(design)
    changed["evidence_class"] = "formal"
    trial.write(root / "design.json", changed)
    with pytest.raises(ValueError, match="design changed after"):
        trial.check(root, environment=False)


def test_ambiguous_started_session_is_not_retried(prepared, monkeypatch):
    _, root = prepared
    design = trial.read(root / "design.json")
    trial.write(root / "sessions/R01/started.json", {"design_sha256": trial.digest(design)})
    original = trial.check
    monkeypatch.setattr(trial, "check", lambda root, **kw: original(root, environment=False))
    monkeypatch.setattr(trial, "execute_cell", lambda *a: pytest.fail("must not call provider"))
    with pytest.raises(ValueError, match="ambiguous started cell"):
        trial.run(root)


def test_retained_public_export_preserves_intermediate_measurements_and_staged_additions():
    cell = "EQ-W03--Aligned"  # Includes one additional committed solvent addition.
    path = trial.EXPORT / "sources" / cell / "trajectory.jsonl"
    batches = trial.read(path.parent / "RESULT.json")["source"]["batches"]
    history = trial.exported_history(path, cell, batches)
    raw = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
    assert len(history["records"]) == len(raw) == 61
    for row, original in zip(history["records"], raw, strict=True):
        tool = original["environment_output"]["views"]["tool_json"]
        assert row["action"] == original["agent_output"]["action"]
        assert row["observation"] == original["environment_output"]["observation"]
        for key in trial.TOOL_KEYS:
            assert row[key] == trial.public_metadata(tool[key])
        assert row["transaction_status"] == original["transaction"]["status"]
        assert row["rollback_reason"] == original["transaction"]["rollback_reason"]
    assert sum(r["instrument"] == "ph_meter" for r in history["records"]) == 12
    assert sum(r["action"]["operation"] == "add_solvent" for r in history["records"]) == 13
    assert all(r["transaction_status"] == "committed" for r in history["records"])
    serialized = trial.encoded(history)
    for label in (
        "EQ-W",
        "decision_audit",
        "belief_update_rule",
        "prior_record",
        "reference_truth",
    ):
        assert label not in serialized
    assert history["public_contract"]["operation_schema_catalog"]


def test_public_trajectory_binding_prevents_accidental_source_substitution(tmp_path):
    cell = "EQ-W01--Opaque"
    source = trial.EXPORT / "sources" / cell
    result = trial.read(source / "RESULT.json")
    path = tmp_path / "trajectory.jsonl"
    path.write_bytes((source / "trajectory.jsonl").read_bytes() + b"\n")
    trial.write(tmp_path / "RESULT.json", result)
    assert (
        hashlib.sha256(path.read_bytes()).hexdigest()
        != result["source"]["agent_visible_trajectory"]["public_sha256"]
    )
    with pytest.raises(ValueError, match="does not match its result binding"):
        trial.exported_history(path, cell, result["source"]["batches"])


def test_pair_entrypoint_stops_after_two_calls_and_retains_the_existing_design(
    prepared, monkeypatch
):
    _, root = prepared
    before = (root / "design.json").read_bytes()
    original = trial.check
    monkeypatch.setattr(trial, "check", lambda root, **kw: original(root, environment=False))
    calls = []

    def execute(root, design, cell, progress):
        calls.append(cell["id"])
        assert progress["total"] == 2
        assert not (root / "pair-summary.json").exists()
        return {"payload": payload(), "failure": None, "elapsed_s": 1, "numerics_attempts": 0}

    monkeypatch.setattr(trial, "execute_cell", execute)
    report = trial.run(root, pair_only=True)
    assert calls == ["R01", "R02"]
    assert report["planned_sessions"] == report["valid_sessions"] == 2
    assert report["contrast"]["macro"]["interaction"] == 0
    assert (root / "design.json").read_bytes() == before
    assert not (root / "sessions/R03").exists()
    assert trial.run(root, pair_only=True) == report
    assert calls == ["R01", "R02"]
