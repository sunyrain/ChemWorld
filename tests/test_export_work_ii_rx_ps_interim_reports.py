import json
from pathlib import Path

import scripts.export_work_ii_rx_ps_interim_reports as export


def dump(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


def test_resolve_result_prefers_latest_repair(tmp_path: Path) -> None:
    cell = "RX-W01--P--mechanism_discovery--Opaque"
    dump(tmp_path / "sources" / cell / "result.json", {"status": "old"})
    dump(
        tmp_path / "sources" / cell / "posttest-repair-v10" / "effective-result.json",
        {"status": "completed"},
    )

    path, result = export.resolve_result(tmp_path, cell)

    assert path.parent.name == "posttest-repair-v10"
    assert result["status"] == "completed"


def test_readable_report_excludes_private_provider_fields() -> None:
    result = {
        "cell_id": "RX-W04--S--safety_constrained_optimization--MisIndexed",
        "world_id": "RX-W04",
        "locus": "S",
        "goal": "safety_constrained_optimization",
        "arm": "MisIndexed",
        "status": "retained_nonconforming",
        "source_status": "completed",
        "operations": 7,
        "rollbacks": [],
        "posttest_chain_sealed": False,
        "exact_replay": {"verified": True},
        "recommendation": {
            "selected_experiment_index": 1,
            "selection_rationale": "Retained source recommendation.",
        },
        "batches": [
            {
                "ordinal": 1,
                "lifecycle_index": 1,
                "end_step": 7,
                "actions": [
                    {"operation": "add_solvent", "solvent": 0, "volume_L": 0.08},
                    {"operation": "add_reagent", "amount_mol": 0.04},
                    {
                        "operation": "add_catalyst",
                        "catalyst": 0,
                        "catalyst_amount_mol": 0.005,
                    },
                    {
                        "operation": "heat",
                        "target_temperature_K": 350,
                        "duration_s": 3600,
                        "stirring_speed_rpm": 600,
                    },
                ],
                "metrics": dict.fromkeys(export.METRICS, 0.5),
            }
        ],
        "posttest_validation": {
            "K1": {"valid": False, "failure": "missing_payload"},
            "Q": {"valid": True, "failure": None},
            "K2": {"valid": True, "failure": None},
        },
        "posttests": {
            "K1": {
                "payload": None,
                "failure": "provider_failure",
                "provider_errors": ["private error"],
                "thread_id": "secret-thread",
                "exit_code": 1,
                "elapsed_s": 1.0,
            },
            "Q": {
                "payload": {"rationale": "r", "predictions": []},
                "failure": None,
                "provider_errors": [],
                "thread_id": "secret-thread",
                "exit_code": 0,
                "elapsed_s": 2.0,
            },
            "K2": {
                "payload": {"report": "retrospective"},
                "failure": None,
                "provider_errors": [],
                "thread_id": "secret-thread",
                "exit_code": 0,
                "elapsed_s": 3.0,
            },
        },
    }

    report = export.render_report(Path("result.json"), result)

    assert "No valid K1 payload was produced" in report
    assert "Retained incomplete-chain notice" in report
    assert "retrospective" in report
    assert "secret-thread" not in report
    assert "private error" not in report
