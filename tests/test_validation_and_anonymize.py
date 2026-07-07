from __future__ import annotations

import json

import pytest

from chemworld.data.anonymize import anonymize_jsonl, anonymize_text
from chemworld.data.logging import load_jsonl
from chemworld.data.validation import validate_records
from chemworld.eval.runner import make_agent, run_agent


def test_validate_records_rejects_missing_schema(tmp_path) -> None:
    path = tmp_path / "run.jsonl"
    run_agent(
        env_id="ChemWorld",
        agent=make_agent("random"),
        world_split="public-dev",
        budget=2,
        objective="balanced",
        seed=1,
        output_path=path,
    )
    records = load_jsonl(path)
    validate_records(records)
    records[0].pop("schema_version")
    with pytest.raises(ValueError, match="missing keys"):
        validate_records(records)


def test_trajectory_records_include_instrument_signal_layers(tmp_path) -> None:
    path = tmp_path / "run.jsonl"
    run_agent(
        env_id="ChemWorld",
        agent=make_agent("random"),
        world_split="public-dev",
        budget=8,
        objective="balanced",
        seed=2,
        output_path=path,
    )
    records = load_jsonl(path)
    validate_records(records)
    measured = [record for record in records if record["instrument"] is not None]
    assert measured
    assert "raw_signal" in measured[-1]
    assert "processed_estimate" in measured[-1]
    assert "uncertainty" in measured[-1]


def test_anonymize_helpers_redact_personal_identifiers(tmp_path) -> None:
    assert anonymize_text("student 12345678 <a.b@example.edu>") == (
        "student [REDACTED_ID] <[REDACTED_EMAIL]>"
    )

    source = tmp_path / "raw.jsonl"
    target = tmp_path / "anon.jsonl"
    source.write_text(
        json.dumps(
            {
                "participant_id": "alice",
                "student_id": "12345678",
                "email": "a.b@example.edu",
                "explanation": {"note": "email a.b@example.edu"},
            }
        )
        + "\n",
        encoding="utf-8",
    )
    anonymize_jsonl(source, target, salt="study")
    payload = json.loads(target.read_text(encoding="utf-8"))
    assert "student_id" not in payload
    assert "email" not in payload
    assert payload["participant_id"] != "alice"
    assert "[REDACTED_EMAIL]" in payload["explanation"]["note"]

