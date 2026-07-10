from __future__ import annotations

import numpy as np
import pytest

from chemworld.physchem.solver_backend import ODESolverPolicy, solve_ode


def test_solver_policy_hash_is_stable_and_sensitive_to_tolerances() -> None:
    baseline = ODESolverPolicy(solver_id="test-policy", method="RK45")
    equivalent = ODESolverPolicy(solver_id="test-policy", method="RK45")
    changed = ODESolverPolicy(solver_id="test-policy", method="RK45", rtol=1.0e-7)

    assert baseline.policy_hash == equivalent.policy_hash
    assert baseline.policy_hash != changed.policy_hash
    assert baseline.to_dict()["policy_hash"] == baseline.policy_hash


@pytest.mark.parametrize(
    ("field", "value"),
    (
        ("rtol", float("nan")),
        ("atol", float("inf")),
        ("max_step_s", float("nan")),
        ("first_step_s", float("inf")),
    ),
)
def test_solver_policy_rejects_nonfinite_numeric_controls(field: str, value: float) -> None:
    with pytest.raises(ValueError, match="finite"):
        ODESolverPolicy(solver_id="invalid-policy", **{field: value})


def test_solver_backend_emits_replay_diagnostics() -> None:
    policy = ODESolverPolicy(
        solver_id="exponential-decay-rk45-v1",
        method="RK45",
        rtol=1.0e-10,
        atol=1.0e-12,
    )
    report = solve_ode(
        lambda _time, state: -state,
        [1.0],
        time_span_s=(0.0, 1.0),
        evaluation_times_s=(0.0, 0.5, 1.0),
        policy=policy,
    )

    assert report.success
    assert report.t.tolist() == [0.0, 0.5, 1.0]
    assert report.y[0, -1] == pytest.approx(np.exp(-1.0), rel=1.0e-8)
    assert report.diagnostic.evaluation_count == 3
    assert report.diagnostic.final_time_s == pytest.approx(1.0)
    assert report.diagnostic.nfev > 0
    assert report.diagnostic.to_dict()["policy"]["policy_hash"] == policy.policy_hash


def test_solver_events_require_named_policy_contract() -> None:
    def crossing(_time: float, state: np.ndarray) -> float:
        return float(state[0] - 0.5)

    unnamed_policy = ODESolverPolicy(solver_id="unnamed-event-policy", method="RK45")
    with pytest.raises(ValueError, match=r"policy\.event_names"):
        solve_ode(
            lambda _time, _state: np.asarray([-1.0]),
            [1.0],
            time_span_s=(0.0, 1.0),
            policy=unnamed_policy,
            events=(crossing,),
        )

    named_policy = ODESolverPolicy(
        solver_id="named-event-policy",
        method="RK45",
        event_names=("half_concentration",),
    )
    report = solve_ode(
        lambda _time, _state: np.asarray([-1.0]),
        [1.0],
        time_span_s=(0.0, 1.0),
        policy=named_policy,
        events=(crossing,),
    )

    assert report.success
    assert report.diagnostic.event_count == 1


def test_solver_backend_validates_state_span_and_evaluation_grid() -> None:
    def rhs(_time: float, state: np.ndarray) -> np.ndarray:
        return -state

    with pytest.raises(ValueError, match="one-dimensional"):
        solve_ode(rhs, [[1.0]], time_span_s=(0.0, 1.0))
    with pytest.raises(ValueError, match="earlier"):
        solve_ode(rhs, [1.0], time_span_s=(1.0, 0.0))
    with pytest.raises(ValueError, match="within"):
        solve_ode(
            rhs,
            [1.0],
            time_span_s=(0.0, 1.0),
            evaluation_times_s=(0.0, 1.1),
        )
    with pytest.raises(ValueError, match="sorted"):
        solve_ode(
            rhs,
            [1.0],
            time_span_s=(0.0, 1.0),
            evaluation_times_s=(0.8, 0.2),
        )
