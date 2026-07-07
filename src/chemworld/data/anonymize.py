"""Utilities for preparing human pilot trajectories for release."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

EMAIL_RE = re.compile(r"[\w.\-+]+@[\w.\-]+\.[A-Za-z]{2,}")
STUDENT_ID_RE = re.compile(r"\b\d{6,14}\b")


def anonymize_text(text: str) -> str:
    text = EMAIL_RE.sub("[REDACTED_EMAIL]", text)
    text = STUDENT_ID_RE.sub("[REDACTED_ID]", text)
    return text


def participant_hash(identifier: str, salt: str) -> str:
    digest = hashlib.sha256(f"{salt}:{identifier}".encode()).hexdigest()
    return digest[:16]


def anonymize_record(record: dict[str, Any], *, salt: str) -> dict[str, Any]:
    cleaned = json.loads(json.dumps(record))
    for key in ("name", "student_name", "student_id", "email"):
        cleaned.pop(key, None)
    if "participant_id" in cleaned:
        cleaned["participant_id"] = participant_hash(str(cleaned["participant_id"]), salt)
    if "explanation" in cleaned:
        cleaned["explanation"] = json.loads(anonymize_text(json.dumps(cleaned["explanation"])))
    return cleaned


def anonymize_jsonl(input_path: str | Path, output_path: str | Path, *, salt: str) -> None:
    input_file = Path(input_path)
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with input_file.open("r", encoding="utf-8") as src, output_file.open(
        "w",
        encoding="utf-8",
    ) as dst:
        for line in src:
            if not line.strip():
                continue
            record = anonymize_record(json.loads(line), salt=salt)
            dst.write(json.dumps(record, sort_keys=True) + "\n")
