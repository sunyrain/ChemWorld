from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from analyze_work_ii_w262_c2_cross_model import (  # noqa: E402
    _paired_summary,
)


def _metrics(value: float, *, completed: bool = True) -> dict:
    return {
        "terminal_completed": completed,
        "prediction_improvement": value,
        "effective_final_error": value,
        "law_mae": value,
        "law_compression_loss": value,
        "blind_gain": value,
        "blind_launched": True,
    }


def test_paired_summary_uses_codex_minus_deepseek_orientation() -> None:
    left = {
        ("A_E", "task", 1, "opaque"): _metrics(0.4),
        ("A_E", "task", 2, "opaque"): _metrics(0.2, completed=False),
    }
    right = {
        ("A_E", "task", 1, "opaque"): _metrics(0.1),
        ("A_E", "task", 2, "opaque"): _metrics(0.3),
    }
    summary = _paired_summary(left, right, bootstrap=False)
    assert summary["orientation"] == "codex_minus_deepseek"
    assert summary["paired_scheduled_cell_count"] == 2
    assert summary["terminal_completion_rate_difference"] == 0.5
    assert summary["prediction_improvement"]["mean_difference"] == pytest.approx(-0.1)
