from __future__ import annotations

import json

from scripts import run_work_ii_rx_p_opaque_dual_goal_canary as canary


def test_fixed_rx_p_opaque_design() -> None:
    rows = canary.queries()
    assert len(rows) == 12
    assert len({row["query_id"] for row in rows}) == 12
    assert all([action["operation"] for action in row["actions"]][-3:] == [
        "quench",
        "terminate",
        "measure",
    ] for row in rows)
    material, model = canary.priors("P", "Opaque")
    assert material == {"mode": "opaque_codes"}
    assert model is not None
    assert model["locus"] == "parametric"
    assert model["model"] is None


def test_rx_source_resource_envelope() -> None:
    card = canary.resource_card()
    assert card.operation_attempt_limit == 360
    assert card.vessel_start_limit == 12
    assert card.final_assay_limit == 12
    assert card.nonfinal_instrument_use_limit == 12
    assert card.stock_limits == {
        "reagent_mol": 0.48,
        "solvent_L": 0.96,
        "catalyst_mol": 0.06,
    }
    assert card.process_time_limit_s == 144000
    assert card.implicit_operation_time_s == {"quench": 120.0}


def test_current_codex_routes_mcp_through_code_mode_host() -> None:
    command = [
        "codex",
        "exec",
        "--disable",
        "shell_tool",
        "--disable",
        "code_mode",
        "--disable",
        "code_mode_host",
    ]
    adapted = canary.enable_code_mode_tool_router(command)
    assert adapted[2:4] == ["--disable", "shell_tool"]
    assert ["--disable", "code_mode"] not in [
        adapted[index : index + 2] for index in range(len(adapted) - 1)
    ]
    assert ["--disable", "code_mode_host"] not in [
        adapted[index : index + 2] for index in range(len(adapted) - 1)
    ]
    assert adapted.count("code_mode") == 1
    assert adapted.count("code_mode_host") == 1


def test_posttest_expands_public_numerics_budget(tmp_path, monkeypatch) -> None:
    prefix = "mcp_servers.public_numerics.args="

    def fake_build_command(*args, **kwargs):
        del args, kwargs
        return [
            "codex",
            "exec",
            "--disable",
            "code_mode",
            "-c",
            prefix + json.dumps(["server.py", "--limit", "8"]),
        ]

    monkeypatch.setattr(canary, "_SHARED_BUILD_COMMAND", fake_build_command)
    command = canary.build_command({}, tmp_path / "schema.json", tmp_path)
    args_value = next(item.removeprefix(prefix) for item in command if item.startswith(prefix))
    assert json.loads(args_value)[-2:] == ["--limit", "128"]
    assert ["--enable", "code_mode"] in [
        command[index : index + 2] for index in range(len(command) - 1)
    ]
