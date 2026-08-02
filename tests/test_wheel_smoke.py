from __future__ import annotations

import pytest
from scripts.smoke_test_wheel import (
    _validate_current_registry_payload,
    _validate_readiness_payload,
    _wheel_build_command,
    _wheel_install_command,
)


def _payload(*, status: str, contract_ready: int, benchmark_ready: int) -> dict[str, object]:
    return {
        "serious_suite_status": status,
        "serious_task_count": 6,
        "contract_ready_count": contract_ready,
        "benchmark_ready_count": benchmark_ready,
    }


def test_candidate_wheel_requires_complete_contracts_without_empirical_claim() -> None:
    _validate_readiness_payload(
        _payload(status="candidate", contract_ready=6, benchmark_ready=0),
        require_validated_benchmark=False,
    )

    with pytest.raises(RuntimeError, match="validated benchmark evidence"):
        _validate_readiness_payload(
            _payload(status="candidate", contract_ready=6, benchmark_ready=0),
            require_validated_benchmark=True,
        )


@pytest.mark.parametrize(
    ("status", "contract_ready", "benchmark_ready"),
    [
        ("candidate", 5, 0),
        ("candidate", 6, 1),
        ("validated", 6, 5),
        ("unknown", 6, 0),
    ],
)
def test_wheel_smoke_rejects_inconsistent_readiness(
    status: str,
    contract_ready: int,
    benchmark_ready: int,
) -> None:
    with pytest.raises(RuntimeError):
        _validate_readiness_payload(
            _payload(
                status=status,
                contract_ready=contract_ready,
                benchmark_ready=benchmark_ready,
            ),
            require_validated_benchmark=False,
        )


def test_wheel_smoke_uses_current_registry_claim_boundary() -> None:
    payload: dict[str, object] = {
        "current_registry_schema": "chemworld-current-surface-registry-0.4",
        "project_role": "agent_capability_evaluation_and_training_environment",
        "environment_updates_agent_weights": False,
        "formal_results_present": True,
        "publication_ready": False,
    }
    _validate_current_registry_payload(payload)
    stale = dict(payload, current_registry_schema="chemworld-current-surface-registry-0.3")
    with pytest.raises(RuntimeError, match="claim boundaries"):
        _validate_current_registry_payload(stale)


def test_wheel_smoke_prefers_uv_without_requiring_pip(tmp_path) -> None:
    repository = tmp_path / "repository"
    wheel_dir = tmp_path / "wheel"
    install_dir = tmp_path / "install"
    wheel = wheel_dir / "chemworld_bench-0.2.0-py3-none-any.whl"

    assert _wheel_build_command(repository, wheel_dir, uv_executable="uv") == [
        "uv",
        "build",
        "--wheel",
        "--out-dir",
        str(wheel_dir),
        str(repository),
    ]
    assert _wheel_install_command(wheel, install_dir, uv_executable="uv") == [
        "uv",
        "pip",
        "install",
        "--no-deps",
        "--target",
        str(install_dir),
        str(wheel),
    ]
