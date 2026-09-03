from __future__ import annotations

import inspect

from chemworld.eval.work_ii_current_composite import (
    build_current_composite_inputs,
    execute_current_composite_evaluator,
)


def test_current_composite_accepts_an_explicit_cross_model_cohort_id() -> None:
    build_signature = inspect.signature(build_current_composite_inputs)
    execute_signature = inspect.signature(execute_current_composite_evaluator)
    assert build_signature.parameters["cohort_id"].default == (
        "work-ii-deepseek-c2-current-composite-v0.1"
    )
    assert execute_signature.parameters["cohort_id"].default == (
        "work-ii-deepseek-c2-current-composite-v0.1"
    )
