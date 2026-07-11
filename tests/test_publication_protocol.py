from __future__ import annotations

from copy import deepcopy

import pytest

from chemworld.eval.publication_protocol import (
    assert_valid_publication_protocol,
    canonical_protocol_sha256,
    load_publication_protocol,
    publication_protocol_manifest,
)
from chemworld.tasks import SERIOUS_TASK_IDS


def test_frozen_publication_protocol_is_valid_and_task_level() -> None:
    protocol = load_publication_protocol()
    manifest = publication_protocol_manifest(protocol)

    assert manifest["valid"] is True
    assert len(manifest["protocol_sha256"]) == 64
    assert [item["task_id"] for item in protocol["tasks"]] == list(SERIOUS_TASK_IDS)
    assert protocol["experimental_design"]["seeds"] == list(range(20))
    assert protocol["experimental_design"]["complete_experiments_per_task_seed"] == 40
    assert protocol["reporting"]["cross_task_aggregate_score"] is None
    assert "tool_using_llm_stub" not in {
        item["method_id"] for item in protocol["methods"]
    }


def test_publication_protocol_digest_is_order_independent() -> None:
    protocol = load_publication_protocol()
    reversed_protocol = dict(reversed(list(protocol.items())))

    assert canonical_protocol_sha256(protocol) == canonical_protocol_sha256(
        reversed_protocol
    )


def test_publication_protocol_fails_closed_on_seed_or_claim_drift() -> None:
    protocol = load_publication_protocol()
    drifted = deepcopy(protocol)
    drifted["experimental_design"]["seeds"] = list(range(5))
    drifted["tasks"][0]["capability_claim"] = "changed after seeing results"

    with pytest.raises(ValueError, match=r"paired_seed_depth.*task_contracts|task_contracts"):
        assert_valid_publication_protocol(drifted)
