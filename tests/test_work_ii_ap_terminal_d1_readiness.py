from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

from chemworld.eval.work_ii_ap_terminal_d1_readiness import (
    _q2_world,
    build_independent_ap_d1_readiness,
    discover_historical_ap_participant_exposure,
    validate_independent_ap_d1_readiness,
)

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "configs/benchmark/work_ii_ap_terminal_d1_independent_plan_v0.1.json"


def test_real_plan_selects_the_smallest_unexposed_q2_passed_seed_for_each_task() -> None:
    readiness, configs = build_independent_ap_d1_readiness(ROOT, PLAN)
    rows = {row["task_id"]: row for row in readiness["tasks"]}

    reaction = rows["reaction-safety-constrained"]
    assert reaction["historical_participant_exposed_world_seeds"] == [0, 1, 4]
    assert reaction["eligible_unexposed_q2_passed_world_seeds"] == [2, 3]
    assert reaction["selected_world_seed"] == 2
    assert reaction["selection_rule_satisfied"] is True
    assert reaction["status"] == "ready_static_config_provider_execution_blocked"
    config = configs["reaction-safety-constrained"]
    assert config["world_seed"] == 2
    assert config["pilot_id"] == "work-ii-reaction-safety-independent-terminal-d1-seed2"
    assert config["observation_noise_namespace"] == config["pilot_id"]
    assert set(config["prior_arms"]) == {
        "opaque",
        "aligned_nominal",
        "misindexed_nominal",
    }
    assert config["campaign"]["complete_experiments"] == 10
    assert config["campaign"]["checkpoint_complete_experiments"] == [0, 2, 4, 7, 10]
    assert config["qualification"]["execution_authorized"] is False
    assert config["independent_terminal_d1"]["historical_participant_results_replaced"] is False

    electrochemical = rows["electrochemical-conversion"]
    assert electrochemical["historical_participant_exposed_world_seeds"] == [0, 1]
    assert electrochemical["eligible_unexposed_q2_passed_world_seeds"] == [2, 3, 4]
    assert electrochemical["selected_world_seed"] == 2
    assert electrochemical["selection_rule_satisfied"] is True
    assert electrochemical["status"] == "ready_static_config_provider_execution_blocked"
    electro_config = configs["electrochemical-conversion"]
    assert electro_config["world_seed"] == 2
    assert electro_config["pilot_id"] == "work-ii-electrochemical-independent-terminal-d1-seed2"
    assert electro_config["observation_noise_namespace"] == electro_config["pilot_id"]
    assert readiness["provider_call_count"] == 0
    assert readiness["w2_26_prerequisite"] is False
    assert readiness["status"] == "ready"


def test_exposure_roster_is_discovered_from_machine_reports() -> None:
    discovered = discover_historical_ap_participant_exposure(
        ROOT, ["reaction-safety-constrained", "electrochemical-conversion"]
    )

    assert {row["world_seed"] for row in discovered["reaction-safety-constrained"]} == {
        0,
        1,
        4,
    }
    assert {row["world_seed"] for row in discovered["electrochemical-conversion"]} == {
        0,
        1,
    }


def test_exposure_discovery_is_schema_version_independent(tmp_path: Path) -> None:
    report_root = tmp_path / "workstreams/flagship_tasks/reports"
    report_root.mkdir(parents=True)
    (report_root / "future-schema.json").write_text(
        json.dumps(
            {
                "schema_version": "future-unrecognized-schema-99",
                "task_id": "reaction-safety-constrained",
                "world_seed": 9,
                "denominators": {"participant_provider_session_count": 1},
            }
        ),
        encoding="utf-8",
    )

    discovered = discover_historical_ap_participant_exposure(
        tmp_path, ["reaction-safety-constrained"]
    )

    assert discovered["reaction-safety-constrained"] == [
        {
            "path": "workstreams/flagship_tasks/reports/future-schema.json",
            "task_id": "reaction-safety-constrained",
            "world_seed": 9,
            "participant_provider_session_count": 1,
            "status": None,
        }
    ]


def test_readiness_validator_rebuilds_configs() -> None:
    readiness, configs = build_independent_ap_d1_readiness(ROOT, PLAN)
    assert validate_independent_ap_d1_readiness(ROOT, PLAN, readiness, configs) == []
    changed = deepcopy(configs)
    changed["reaction-safety-constrained"]["campaign"]["complete_experiments"] = 9

    assert validate_independent_ap_d1_readiness(ROOT, PLAN, readiness, changed) == [
        "independent A-P D1 configs differ from deterministic rebuild"
    ]


def test_no_unexposed_q2_passed_seed_fails_closed() -> None:
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    world, q2_passed, eligible, errors = _q2_world(
        ROOT,
        plan["candidates"][0],
        exposed_seeds=[0, 1, 2, 3, 4],
    )

    assert world is None
    assert q2_passed == [0, 1, 2, 3, 4]
    assert eligible == []
    assert "no Q2-passed world remains after historical participant exposure exclusion" in errors
