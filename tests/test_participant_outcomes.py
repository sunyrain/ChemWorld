from __future__ import annotations

import pytest

from chemworld.eval.participant_outcomes import (
    compact_readiness,
    participant_outcome_id,
)


def test_legacy_participant_gates_map_to_outcomes() -> None:
    assert participant_outcome_id("Gate B") == "O1"
    assert participant_outcome_id("C") == "O2"
    assert participant_outcome_id("D") == "O3"
    assert participant_outcome_id("E") == "O4"
    assert participant_outcome_id("O5") == "O5"


def test_negative_participant_result_does_not_block_release_readiness() -> None:
    readiness = compact_readiness(
        environment_ready=True,
        methods_frozen=True,
        execution_complete=True,
        release_ready=True,
        result_status="negative",
    )
    assert readiness["release_ready"] is True
    assert readiness["result_status"] == "negative"
    assert readiness["participant_performance_controls_release_readiness"] is False


def test_compact_readiness_rejects_impossible_state_ordering() -> None:
    with pytest.raises(ValueError, match="methods cannot freeze"):
        compact_readiness(
            environment_ready=False,
            methods_frozen=True,
            execution_complete=False,
            release_ready=False,
        )
