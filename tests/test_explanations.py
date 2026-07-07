from __future__ import annotations

import pytest

from chemworld.eval.explanations import combined_artifact_score, score_mechanism_explanation


def test_mechanism_explanation_keyword_rubric() -> None:
    explanation = {
        "hypothesis": "Moderate temperature avoids degradation and byproduct formation.",
        "mechanism": "Catalyst and solvent interactions affect selectivity.",
        "risk": "High concentration increases safety risk.",
        "limits": "The claim is seed-limited and uncertain.",
        "next": "Next experiment should validate the local optimum.",
    }

    result = score_mechanism_explanation(explanation)

    assert result.normalized > 0.8
    assert "degradation" in result.passed_items
    assert not result.missing_items


def test_combined_artifact_score_is_bounded() -> None:
    assert combined_artifact_score(
        performance=2.0,
        mechanism_score=0.5,
        reproducibility=1.0,
    ) == pytest.approx(0.85)

