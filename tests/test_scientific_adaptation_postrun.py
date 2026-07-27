from __future__ import annotations

import copy

from scripts.run_scientific_adaptation_shakedown import (
    DEVELOPMENT_TEST_METHODS,
    DEVELOPMENT_TEST_PROTOCOL,
    _DeterministicMockClient,
    _run_cell,
)

from chemworld.eval.mechanism_adaptation_execution import (
    load_json_object,
    load_protocol_object,
    selected_campaign_rows,
)
from chemworld.eval.scientific_adaptation_postrun import (
    replay_scientific_adaptation_receipt,
)


def _mock_receipt():
    protocol = load_protocol_object(DEVELOPMENT_TEST_PROTOCOL)
    methods = load_json_object(DEVELOPMENT_TEST_METHODS)
    row = selected_campaign_rows(
        protocol,
        tasks=["reaction-to-crystallization"],
        limit=1,
    )[0]
    receipt = _run_cell(
        protocol=protocol,
        methods=methods,
        method_id="dev_flash_direct",
        row=row,
        provider="mock",
        pre_experiments=1,
        post_experiments=1,
        client_override=_DeterministicMockClient(model="deepseek-v4-flash"),
    )
    return receipt, row


def test_terminal_receipt_physical_replay_is_exact() -> None:
    receipt, row = _mock_receipt()

    audit = replay_scientific_adaptation_receipt(receipt, row)

    assert audit["verified"] is True
    assert audit["replayed_experiment_count"] == 2
    assert all(item["mismatch_fields"] == [] for item in audit["experiments"])


def test_terminal_receipt_physical_replay_detects_score_tampering() -> None:
    receipt, row = _mock_receipt()
    tampered = copy.deepcopy(receipt)
    tampered["experiments"][1]["result"]["terminal_summary"][
        "leaderboard_score"
    ] += 0.01

    audit = replay_scientific_adaptation_receipt(tampered, row)

    assert audit["verified"] is False
    assert audit["experiments"][0]["verified"] is True
    assert audit["experiments"][1]["mismatch_fields"] == ["terminal_summary"]
