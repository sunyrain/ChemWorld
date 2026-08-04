from __future__ import annotations

import json

from chemworld.eval.composition_qualification_design import (
    EXPECTED_GENERATED_CASE_COUNT,
    EXPECTED_PATTERN_CASE_COUNTS,
    UNSEEN_PATTERN_ID,
    build_generated_suites,
)


def test_frozen_generated_suite_denominators_and_coverage() -> None:
    suites = build_generated_suites()
    counts = {
        str(suite.cases[0].compiled.compatibility.pattern): len(suite.cases)
        for suite in suites
    }

    assert counts == EXPECTED_PATTERN_CASE_COUNTS
    assert sum(counts.values()) == EXPECTED_GENERATED_CASE_COUNT == 52
    assert counts[UNSEEN_PATTERN_ID] == 8
    assert all(suite.report["denominators"] == suite.report["covered"] for suite in suites)
    assert all(suite.report["failure_count"] == 0 for suite in suites)
    json.dumps([suite.to_dict() for suite in suites], allow_nan=False)


def test_generated_composition_ids_do_not_reuse_reference_task_ids() -> None:
    from chemworld.tasks import list_tasks

    registered = {task.task_id for task in list_tasks()}
    generated = {
        case.request["composition_id"]
        for suite in build_generated_suites()
        for case in suite.cases
    }

    assert len(generated) == EXPECTED_GENERATED_CASE_COUNT
    assert generated.isdisjoint(registered)
