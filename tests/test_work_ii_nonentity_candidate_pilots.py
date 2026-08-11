from __future__ import annotations

from copy import deepcopy

import pytest
import scripts.build_work_ii_nonentity_candidate_pilots as candidate_pilots
from scripts.build_work_ii_nonentity_candidate_pilots import (
    _crystallization_queries,
    _partition_queries,
    _safety_queries,
    _structural_summary,
)


def _structural_rows(scores: dict[tuple[str, str], float]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for module_a_level in ("mild", "strong"):
        for module_b_level in ("mild", "strong"):
            rows.append(
                {
                    "query_id": f"{module_a_level}-{module_b_level}",
                    "feature_values": {
                        "_module_a_level": module_a_level,
                        "_module_b_level": module_b_level,
                    },
                    "status": "completed",
                    "metrics": {"score": scores[(module_a_level, module_b_level)]},
                    "failure": None,
                    "trajectory_sha256": "abc",
                    "exact_replay": {"verified": True},
                }
            )
    return rows


def test_candidate_query_roster_is_frozen_and_unique() -> None:
    query_groups = (
        (_crystallization_queries(), 4),
        (_partition_queries(), 4),
        (_safety_queries(), 16),
    )

    for queries, expected_count in query_groups:
        assert len(queries) == expected_count
        assert len({query["query_id"] for query in queries}) == expected_count


def test_structural_summary_qualifies_the_more_influential_module(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(candidate_pilots, "ROOT", tmp_path)
    rows = _structural_rows(
        {
            ("mild", "mild"): 0.10,
            ("mild", "strong"): 0.15,
            ("strong", "mild"): 0.50,
            ("strong", "strong"): 0.55,
        }
    )
    base = {
        "task_id": "test-task",
        "belief_checkpoint": {"allowed_prior_fields": []},
    }

    result = _structural_summary(
        candidate_id="test",
        base=deepcopy(base),
        rows=rows,
        module_a="module_a",
        module_b="module_b",
        a_levels=("mild", "strong"),
        b_levels=("mild", "strong"),
        config_path=tmp_path / "pilot.json",
        factorial={},
    )

    assert result["qualified"] is True
    assert result["dominant_module"] == "module_a"
    assert result["module_influences"]["module_a"] == pytest.approx(0.4)
    assert result["module_influences"]["module_b"] == pytest.approx(0.05)
    assert result["influence_gap"] == pytest.approx(0.35)
    assert result["generated_config"] is not None
    assert all(
        not any(key.startswith("_module_") for key in row["feature_values"])
        for row in result["recipes"]
    )
