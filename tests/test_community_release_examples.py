"""Public onboarding examples must run without a repository working directory."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def test_manual_sequence_uses_public_identity_and_completes_assay(tmp_path):
    example = Path(__file__).resolve().parents[1] / "examples/demo_manual_event_sequence.py"
    result = subprocess.run(
        [sys.executable, str(example)], cwd=tmp_path, text=True, capture_output=True, check=True
    )
    rows = [json.loads(line) for line in result.stdout.splitlines()]
    assert rows[0]["task"] == "reaction-to-assay"
    assert any(value is None for value in rows[0]["initial"].values())
    assert "NaN" not in result.stdout
    assert rows[-1] == {"final_assay_completed": True}
    assert len(rows[1:-1]) == 8
    assert all(row["transaction_status"] == "committed" for row in rows[1:-1])
    assert rows[-2]["terminated"] is True


def test_manual_sequence_reports_rejection_without_claiming_completion(monkeypatch, capsys):
    import runpy

    import gymnasium as gym

    example = Path(__file__).resolve().parents[1] / "examples/demo_manual_event_sequence.py"
    module = runpy.run_path(str(example))
    make = gym.make
    closed = []

    class RejectedFirstAction:
        def __init__(self):
            self.env = make("ChemWorld", task_id="reaction-to-assay", budget=8, seed=7)

        def reset(self, **kwargs):
            return self.env.reset(**kwargs)

        def step(self, action):
            # Exercise a real rejected transaction, rather than fabricate a receipt.
            return self.env.step({"operation": "measure", "instrument": "hplc"})

        def close(self):
            self.env.close()
            closed.append(True)

    monkeypatch.setattr(gym, "make", lambda *args, **kwargs: RejectedFirstAction())
    import pytest

    with pytest.raises(RuntimeError, match="did not reach"):
        module["main"]()
    rows = [json.loads(line) for line in capsys.readouterr().out.splitlines()]
    assert len(rows) == 3
    assert rows[-1] == {"final_assay_completed": False}
    assert rows[1]["transaction_status"] != "committed"
    assert closed == [True]
