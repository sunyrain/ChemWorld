"""Historical W2-47 tests retained with the superseded producer-consumer island."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest

from chemworld.agents.interactive_codex_experiment import _campaign_system_prompt
from chemworld.eval.work_ii_longitudinal_decision import (
    build_candidate_pool,
    build_decision_design,
    candidate_packet_coverage,
    load_decision_protocol,
    select_outcome_blind_packet,
)

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "configs/benchmark/work_ii_as_longitudinal_decision_v0.1.json"


def test_protocol_freezes_five_world_ranking_only_matrix() -> None:
    _, protocol = load_decision_protocol(PROTOCOL, repository_root=ROOT)
    assert protocol["campaign_complete_experiments"] == 12
    assert protocol["checkpoint_complete_experiments"] == [0, 3, 6, 9, 12]
    assert protocol["prediction_mode"] == "ranking_only"
    assert protocol["execution"]["cluster_count"] == 5
    assert protocol["execution"]["participant_session_count"] == 15
    assert protocol["execution"]["participant_physical_experiment_count"] == 180
    assert protocol["execution"]["provider_execution_authorized"] is False


def test_outcome_blind_packets_are_balanced_and_ignore_truth_fields() -> None:
    _, protocol = load_decision_protocol(PROTOCOL, repository_root=ROOT)
    pool = build_candidate_pool(protocol)
    assert len(pool) == 128
    selected = select_outcome_blind_packet(
        pool,
        packet_seed=400,
        namespace=str(protocol["candidate_packet_namespace"]),
    )
    decorated = deepcopy(pool)
    for index, row in enumerate(decorated):
        row["truth"] = {"score": 1.0 - index / len(decorated)}
        row["hidden_rank"] = index + 1
    selected_with_truth = select_outcome_blind_packet(
        decorated,
        packet_seed=400,
        namespace=str(protocol["candidate_packet_namespace"]),
    )
    assert [row["query_id"] for row in selected] == [
        row["query_id"] for row in selected_with_truth
    ]
    assert candidate_packet_coverage(selected) == {
        "candidate_count": 8,
        "distinct_pair_count": 8,
        "volume_index_counts": {0: 2, 1: 2, 2: 2, 3: 2},
        "mixing_index_counts": {0: 4, 1: 4},
    }


def test_design_materializes_matched_packets_without_provider_or_truth_selection() -> None:
    design = build_decision_design(PROTOCOL, repository_root=ROOT)
    assert design["cluster_count"] == 5
    assert design["cell_count"] == 15
    assert design["participant_physical_experiment_count"] == 180
    assert design["candidate_truth_execution_count"] == 40
    assert design["checkpoint_truth_execution_count"] == 80
    assert design["provider_free_truth_execution_count"] == 120
    assert design["provider_free_exact_replay_count"] == 120
    assert design["provider_execution_authorized"] is False
    assert design["candidate_selection_uses_hidden_truth"] is False
    assert design["candidate_selection_uses_hidden_rank"] is False
    assert len(
        {
            cluster["terminal_action_readout"]["contract_sha256"]
            for cluster in design["clusters"]
        }
    ) == 5
    for cluster in design["clusters"]:
        contract = cluster["terminal_action_readout"]
        assert contract["prediction_mode"] == "ranking_only"
        assert contract["candidate_outcomes_included"] is False
        assert contract["hidden_ranks_included"] is False
        assert cluster["candidate_packet_coverage"]["distinct_pair_count"] == 8
        members = [
            cell for cell in design["cells"] if cell["cluster_id"] == cluster["cluster_id"]
        ]
        assert len(members) == 3
        assert len({cell["terminal_action_readout"]["contract_sha256"] for cell in members}) == 1


def test_protocol_rejects_full_prediction_terminal_mode() -> None:
    protocol = PROTOCOL.read_text(encoding="utf-8").replace(
        '"prediction_mode": "ranking_only"',
        '"prediction_mode": "full_metrics"',
    )
    target = ROOT / "tests" / ".tmp-longitudinal-decision-invalid.json"
    try:
        target.write_text(protocol, encoding="utf-8")
        with pytest.raises(ValueError, match="ranking-only"):
            load_decision_protocol(target, repository_root=ROOT)
    finally:
        target.unlink(missing_ok=True)


def test_campaign_prompt_keeps_mechanism_and_decision_readouts_separate() -> None:
    prompt = _campaign_system_prompt(
        terminal_action_readout=True,
        terminal_prediction_mode="ranking_only",
    )
    assert "final checkpoint" in prompt
    assert "Do not submit per-candidate numeric outcome predictions" in prompt
    assert "rank all" in prompt.lower()
