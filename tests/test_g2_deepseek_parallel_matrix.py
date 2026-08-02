from __future__ import annotations

import json
from pathlib import Path

from scripts import run_g2_deepseek_parallel_matrix as campaign


def test_parallel_protocol_freezes_exact_matched_matrix() -> None:
    protocol = campaign._load_protocol(campaign.DEFAULT_CONFIG)
    cells = campaign.matrix._scheduled_cells(protocol)
    pairs = campaign._group_pairs(cells)

    assert protocol["agent"]["model"] == "deepseek-v4-flash"
    assert len(cells) == 10
    assert len(pairs) == 5
    assert all(len(pair) == 2 for pair in pairs)
    assert [pair[0]["world_seed"] for pair in pairs] == [0, 1, 2, 3, 4]
    assert all(
        pair[0]["within_pair_order"] == 1 and pair[1]["within_pair_order"] == 2 for pair in pairs
    )


def test_parallel_dry_run_qualifies_all_five_pairs() -> None:
    protocol = campaign._load_protocol(campaign.DEFAULT_CONFIG)
    report = campaign._dry_run(protocol, campaign._source_manifest(campaign.DEFAULT_CONFIG))

    assert report["passed"] is True
    assert report["world_pair_count"] == 5
    assert report["planned_cells"] == 10
    assert report["planned_physical_experiments"] == 60
    assert report["maximum_concurrent_pairs"] == 5
    assert len(report["pair_audits"]) == 5


def test_only_pre_action_provider_failure_can_be_retried(
    tmp_path: Path,
    monkeypatch,
) -> None:
    protocol = campaign._load_protocol(campaign.DEFAULT_CONFIG)
    cell = campaign.matrix._scheduled_cells(protocol)[0]
    card = campaign.matrix._campaign_card(protocol, qualification=False)
    limits = campaign.matrix._method_limits(protocol, qualification=False)
    calls = 0

    def run_cell_light(*, cell_root: Path, cell, **kwargs):  # type: ignore[no-untyped-def]
        nonlocal calls
        del kwargs
        calls += 1
        cell_root.mkdir(parents=True)
        if calls == 1:
            payload = {
                "run_status": "provider_infrastructure_failure",
                "cell": dict(cell),
                "accepted_operation_count": 0,
            }
            (cell_root / "run_summary.json").write_text(json.dumps(payload), encoding="utf-8")
            raise RuntimeError("redacted provider failure")
        payload = {
            "run_status": "provider_infrastructure_failure",
            "cell": dict(cell),
            "accepted_operation_count": 1,
        }
        (cell_root / "run_summary.json").write_text(json.dumps(payload), encoding="utf-8")
        raise RuntimeError("redacted provider failure after an operation")

    monkeypatch.setattr(campaign.matrix, "_run_cell_light", run_cell_light)
    result = campaign._run_cell_with_pre_action_retries(
        protocol=protocol,
        source={},
        runtime={},
        cell=cell,
        output_root=tmp_path,
        card=card,
        method_limits=limits,
    )

    assert calls == 2
    assert len(result["attempts"]) == 2
    assert result["attempts"][0]["retryable_pre_action_provider_failure"] is True
    assert result["attempts"][1]["retryable_pre_action_provider_failure"] is False
    assert result["summary"]["accepted_operation_count"] == 1
