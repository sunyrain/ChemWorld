from __future__ import annotations

from typing import Any

import scripts.export_work_ii_eq_bounded_equilibrium_reports_v2_1 as export


def _cell_payload() -> dict[str, Any]:
    return {
        "cell": {
            "cell_id": "EQ-W01--Opaque",
            "world_id": "EQ-W01",
            "arm": "Opaque",
            "status": "completed",
            "operations": 4,
        },
        "effective_origin": "original",
        "source": {"batches": [], "exact_replay": {"verified": True}},
        "posttests": {
            "K1": {"payload": {"report": "K1"}},
            "Q": {"payload": {"predictions": [], "rationale": "Q"}},
            "K2": {"payload": {"report": "K2"}},
            "EQS": {
                "payload": {
                    "effective_pka": {
                        "identifiable": True,
                        "estimate": 4.2,
                        "lower80": 4.0,
                        "upper80": 4.4,
                        "rationale": "bounded estimate",
                    },
                    "path_dependence": {
                        "assessment": "not_identifiable",
                        "rationale": "insufficient contrasts",
                    },
                    "dissociation_precipitation": {
                        "assessment": "mixed",
                        "supported_range": "tested range",
                        "competing_explanation": "shared concentration dependence",
                    },
                }
            },
        },
        "prediction_evaluation": {"metrics": {}},
    }


def test_render_cell_uses_stable_legacy_reference(monkeypatch: Any) -> None:
    monkeypatch.setattr(export.legacy, "render_cell", export.render_cell)

    rendered = export.render_cell(_cell_payload())

    assert "EQ-specific supplement" in rendered
    assert "every EQS response was sealed" in rendered
