from __future__ import annotations

from chemworld.eval.baseline_report import SERIOUS_BASELINE_AGENTS
from chemworld.eval.benchmark_validation import PRIMARY_METRIC_FIELDS
from chemworld.eval.generalization import compare_public_and_ood_reports
from chemworld.tasks import SERIOUS_TASK_IDS, get_task


def _report(*, shift: float = 0.0, invalid: float = 0.0) -> dict:
    rows = []
    for task_id in SERIOUS_TASK_IDS:
        for index, agent_name in enumerate(SERIOUS_BASELINE_AGENTS):
            value = 0.1 + 0.03 * index + shift
            rows.append(
                {
                    "task_id": task_id,
                    "agent_name": agent_name,
                    "mean_total_score": value,
                    "mean_invalid_action_rate": invalid,
                    "mean_final_assay_count": 3.0,
                    PRIMARY_METRIC_FIELDS[task_id]: value + 0.1,
                }
            )
    return {"summary_rows": rows}


def test_generalization_audit_reports_shift_and_ranking() -> None:
    audit = compare_public_and_ood_reports(
        _report(), _report(shift=-0.02), ood_seeds=(101, 102, 103)
    )
    assert audit["passed"] is True
    for task_id in SERIOUS_TASK_IDS:
        task = audit["tasks"][task_id]
        assert task["task_contract_hash"] == get_task(task_id).contract_hash
        assert task["score_diagnostics"]["rank_correlation"] == 1.0
        assert task["score_diagnostics"]["pairwise_ranking_agreement"] == 1.0
        assert task["score_diagnostics"]["mean_absolute_shift"] > 0.0


def test_generalization_audit_rejects_invalid_ood_actions() -> None:
    audit = compare_public_and_ood_reports(
        _report(), _report(invalid=0.1), ood_seeds=(101,)
    )
    assert audit["passed"] is False
