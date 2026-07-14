from __future__ import annotations

import ast
from pathlib import Path

import pytest

from chemworld.reference.builders.v0_4 import (
    SOURCE_PROFILES,
    ReferenceObservation,
    propose_normalized_candidates,
)

SOURCE = Path(__file__).resolve().parents[1] / "src/chemworld/reference/builders/v0_4.py"


def test_reference_builder_profiles_are_deterministic_distinct_and_normalized() -> None:
    observations = (
        ReferenceObservation((0.1, 0.2, 0.3), 0.2, True),
        ReferenceObservation((0.7, 0.5, 0.4), 0.8, False),
        ReferenceObservation((0.4, 0.9, 0.6), 0.6, True),
    )
    outputs = {}
    for profile in SOURCE_PROFILES:
        kwargs = {
            "profile": profile,
            "namespace": "chemworld-v0.5-reference-search-0.4",
            "task_id": "partition-discovery",
            "pair_index": 7,
            "dimension_count": 3,
            "count": 12,
            "observations": observations,
        }
        first = propose_normalized_candidates(**kwargs)
        assert first == propose_normalized_candidates(**kwargs)
        assert len(first) == len(set(first)) == 12
        assert all(len(row) == 3 and all(0.0 <= value <= 1.0 for value in row) for row in first)
        outputs[profile] = first
    assert len(set(outputs.values())) == 4


def test_reference_builder_rng_is_separated_by_task_pair_and_profile() -> None:
    def build(task: str, pair: int, profile: str):
        return propose_normalized_candidates(
            profile,  # type: ignore[arg-type]
            namespace="chemworld-v0.5-reference-search-0.4",
            task_id=task,
            pair_index=pair,
            dimension_count=2,
            count=8,
        )

    assert build("a", 1, "global_space_filling") != build("a", 2, "global_space_filling")
    assert build("a", 1, "global_space_filling") != build("b", 1, "global_space_filling")
    assert build("a", 1, "global_space_filling") != build("a", 1, "ensemble_surrogate")


def test_reference_builder_source_imports_no_evaluated_agent_namespace() -> None:
    tree = ast.parse(SOURCE.read_text(encoding="utf-8"))
    imports = {
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    } | {
        node.module or "" for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)
    }
    assert not any(name.startswith("chemworld.agents") for name in imports)
    assert not any(name.startswith("chemworld.rl") for name in imports)
    assert not any(name.startswith("chemworld.providers") for name in imports)


def test_reference_builder_rejects_invalid_public_observations() -> None:
    with pytest.raises(ValueError, match="normalized"):
        propose_normalized_candidates(
            "ensemble_surrogate",
            namespace="n",
            task_id="t",
            pair_index=0,
            dimension_count=2,
            count=1,
            observations=(ReferenceObservation((2.0, 0.0), 1.0, True),),
        )
