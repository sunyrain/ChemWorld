from copy import deepcopy

import pytest
from scripts.run_work_ii_information_retry import select_failures


def test_selection_includes_all_failures_and_excludes_valid_wrong_answers():
    inputs = {"cells": [{"cell_id": name} for name in ("correct", "wrong", "tool", "interrupted")]}
    report = {
        "status": "terminal",
        "rows": [
            {"cell_id": "correct", "status": "completed", "joint_recovery": 1},
            {"cell_id": "wrong", "status": "completed", "joint_recovery": 0},
            {"cell_id": "tool", "status": "failed", "failure": "tool_budget_exceeded"},
            {
                "cell_id": "interrupted",
                "status": "failed",
                "failure": "interrupted_attempt_not_reissued",
            },
        ],
    }
    before = deepcopy((inputs, report))
    cells, selection = select_failures(inputs, report)
    assert [c["cell_id"] for c in cells] == ["tool", "interrupted"]
    assert [r["original_session"] for r in selection] == [3, 4]
    assert (inputs, report) == before


def test_selection_rejects_unstarted_or_duplicate_outcomes():
    inputs = {"cells": [{"cell_id": "a"}, {"cell_id": "b"}]}
    rows = [{"cell_id": "a", "status": "completed"}, {"cell_id": "b", "status": "unstarted"}]
    with pytest.raises(ValueError, match="unstarted"):
        select_failures(inputs, {"status": "terminal", "rows": rows})
    with pytest.raises(ValueError, match="duplicate"):
        select_failures(inputs, {"status": "terminal", "rows": [rows[0], rows[0]]})
