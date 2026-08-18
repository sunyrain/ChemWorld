from __future__ import annotations

import json
from pathlib import Path

from chemworld.eval.work_ii_longitudinal_action_readout import (
    build_candidate_queries,
    build_terminal_contract,
    validate_terminal_contract,
)

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "configs/benchmark/work_ii_as_longitudinal_ranking_canary_v0.1.json"


def test_ranking_canary_protocol_is_true_twelve_round_three_arm_development() -> None:
    protocol = json.loads(PROTOCOL.read_text(encoding="utf-8"))
    assert protocol["campaign_complete_experiments"] == 12
    assert protocol["checkpoint_complete_experiments"] == [0, 3, 6, 9, 12]
    assert protocol["arms"] == ["opaque", "aligned_nominal", "misindexed_nominal"]
    assert protocol["participant_physical_experiment_count"] == 36
    assert protocol["prediction_mode"] == "ranking_only"
    assert protocol["provider_execution_authorized"] is True


def test_ranking_only_contract_keeps_candidates_hidden_but_removes_prediction_table() -> None:
    grid = json.loads(
        (
            ROOT / "configs/benchmark/work_ii_as_longitudinal_action_readout_v0.1.json"
        ).read_text(encoding="utf-8")
    )
    candidates = build_candidate_queries(grid)[::8][:8]
    contract = build_terminal_contract(
        study_id="ranking-canary-test",
        world_seed=1,
        candidates=candidates,
        prediction_mode="ranking_only",
    )
    validate_terminal_contract(contract)
    assert contract["prediction_mode"] == "ranking_only"
    assert contract["candidate_outcomes_included"] is False
    assert contract["hidden_ranks_included"] is False
    assert all("truth" not in item for item in contract["candidate_queries"])
