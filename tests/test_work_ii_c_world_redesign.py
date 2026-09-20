from __future__ import annotations

import pytest
from scripts import run_work_ii_c_world_redesign as redesign


def test_candidate_pairs_preserve_intervention_and_public_budget():
    rows = redesign.candidates()
    assert len(rows) == 36
    assert max(len(r["actions"]) for r in rows) <= 60
    for row in rows:
        actions = row["actions"]
        seed_index = next(i for i, a in enumerate(actions) if a["operation"] == "seed_crystals")
        assert actions[seed_index - 2]["operation"] == "quench"
        assert actions[seed_index - 1] == redesign.c.reheat(300, 300)
    for factor in ("cooling_history", "thermal_history"):
        for variant in ("transient", "gentle", "partial_dissolution", "long_memory", "mature"):
            pair = [r for r in rows if r["factor"] == factor and r["variant"] == variant]
            if not pair:
                continue
            assert len(pair) == 2
            duration = [sum(a.get("duration_s", 0) for a in r["actions"]) for r in pair]
            assert duration[0] == duration[1]


@pytest.mark.parametrize("seed", [2, 3])
def test_preconditioned_reference_executes_in_previously_invalid_world(seed, tmp_path):
    row = redesign.candidates()[0]
    result = redesign.c.fixed(tmp_path / "reference", row["actions"], world_seed=seed)
    assert result["passed"] and result["exact_replay"]["verified"]
    records = redesign.c.load_jsonl(tmp_path / "reference/trajectory.jsonl")
    for index in (6, 7):
        state = records[index]["agent_view"]["tool_json"]["operational_state"]
        assert state["temperature_K"] == 300
        assert "target product present before separation" in state["sampling_contract"]
    assert records[8]["action"]["target_temperature_K"] < 300


def test_metric_contract_reaches_all_public_surfaces():
    result = redesign.c.check_public("Opaque", 0, 12)
    assert result["metric_contract_consistent"]
    text = result["operational_state"]["sampling_contract"]
    assert "denominators are original reactant charge" not in text


def test_host_supersaturation_diagnostic_preserves_public_execution(tmp_path):
    from scripts.benchmark_runtime_views import semantic, verify_resources
    from scripts.run_work_ii_c_domain_diagnostic import initial_supersaturation

    actions = redesign.precondition(
        redesign.c.process(path=redesign.c.gentle(segments=2, duration=600))
    )
    plain = redesign.c.fixed(tmp_path / "plain", actions, world_seed=3)
    captured = redesign.c.fixed(
        tmp_path / "captured", actions, world_seed=3, capture_diagnostics=True
    )
    assert plain["passed"] and captured["passed"]
    assert plain["truth"] == captured["truth"]
    assert plain["batches"] == captured["batches"]
    assert len(captured["host_diagnostics"]) == 2
    assert initial_supersaturation(captured) > 0
    assert "host_diagnostics" not in plain
    records = [
        redesign.c.load_jsonl(tmp_path / name / "trajectory.jsonl")
        for name in ("plain", "captured")
    ]
    for run in records:
        assert verify_resources(run)["verified"]
    for before, after in zip(*records, strict=True):
        for key in ("agent_visible_observation", "observation", "transaction_status", "reward"):
            assert semantic(before[key]) == semantic(after[key])
        # Diagnostics are returned to the host result only, never through the lab tool.
        assert "host_diagnostics" not in after["agent_view"]["tool_json"]
