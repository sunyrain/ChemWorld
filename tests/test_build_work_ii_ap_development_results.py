from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/build_work_ii_ap_development_results.py"
SPEC = importlib.util.spec_from_file_location("build_work_ii_ap_development_results", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_build_summary_from_retained_terminal_runs() -> None:
    roots = tuple(ROOT / path for path in MODULE.DEFAULT_RUN_ROOTS)
    summary = MODULE.build_summary(roots)

    assert summary["status"] == "terminal_platform_requalification_required"
    assert summary["development_only"] is True
    assert summary["formal_result"] is False
    assert summary["aggregate"] == {
        "active_cells_with_exact_replay": 10,
        "attempted_operations": 725,
        "blocks_terminal": 4,
        "blocks_total": 4,
        "cells_reaching_10_experiments": 9,
        "cells_terminal": 12,
        "cells_total": 12,
        "cells_with_committed_operations": 10,
        "committed_operations": 723,
        "infrastructure_failure_cells": 2,
        "observed_complete_experiments": 99,
        "planned_complete_experiments": 120,
        "provider_error_events": 0,
        "qualification_completed_cells": 4,
        "right_censored_cells": 6,
        "store_invalid_receipts": 0,
        "store_missing_cells": 0,
    }

    markdown = MODULE.render_markdown(summary)
    assert "Terminal therefore does not mean passed" in markdown
    assert "not support a scientific provider/model/arm comparison" in markdown
    assert "missing-infrastructure-only retry" in markdown
