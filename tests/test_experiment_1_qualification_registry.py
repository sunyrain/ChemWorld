from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/build_experiment_1_qualification_registry.py"
EC_REGISTRY = (
    ROOT / "workstreams/flagship_tasks/experiment_1/results/EC/v1.0.2/composite-registry.json"
)


def _module():
    spec = importlib.util.spec_from_file_location("experiment_1_campaign_registry", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_campaign_registry_has_105_units_and_preserves_pending_status() -> None:
    registry = _module().build_registry({"EC": EC_REGISTRY})

    assert registry["denominator"] == 105
    assert len(registry["rows"]) == 105
    assert registry["status_counts"] == {
        "qualified": 15,
        "failed": 0,
        "pending": 90,
        "N/A": 0,
    }
    assert registry["systems"]["EC"]["participant_ready_candidate"] is True
    assert registry["systems"]["RX"]["participant_ready_candidate"] is False
    assert registry["participant_execution_authorized"] is False
    assert all(row["participant_execution_authorized"] is False for row in registry["rows"])
