"""Irreversible user-selection helper for the Work II submission route."""

from __future__ import annotations

from collections.abc import Mapping
from copy import deepcopy
from typing import Any

from chemworld.eval.work_ii_preregistration import (
    ROUTE_OPTIONS,
    route_decision_sha256,
    validate_submission_route_decision,
)


def select_submission_route_decision(
    decision: Mapping[str, Any],
    *,
    selected_option: str,
    selected_at: str,
) -> dict[str, Any]:
    """Record one irreversible, outcome-blind user route selection."""

    existing_errors = validate_submission_route_decision(decision)
    if existing_errors:
        raise ValueError(
            "cannot select a route from an invalid decision: "
            + "; ".join(existing_errors)
        )
    if decision.get("status") != "awaiting_user_selection":
        raise ValueError("submission route has already been selected")
    if selected_option not in ROUTE_OPTIONS:
        raise ValueError(f"unsupported submission route: {selected_option}")
    if not isinstance(selected_at, str) or not selected_at.strip():
        raise ValueError("submission-route selection requires a non-empty timestamp")

    selected = deepcopy(dict(decision))
    selected["status"] = "selected"
    selected["selected_option"] = selected_option
    selected["selected_by"] = "user"
    selected["selected_at"] = selected_at
    selected["decision_sha256"] = route_decision_sha256(selected)
    selected_errors = validate_submission_route_decision(selected)
    if selected_errors:
        raise ValueError(
            "built submission-route selection is invalid: "
            + "; ".join(selected_errors)
        )
    return selected


__all__ = ["select_submission_route_decision"]
