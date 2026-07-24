"""Expand the public calibrated changed/no-change campaign matrix."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from chemworld.eval.mechanism_adaptation import (
    build_paired_campaign_matrix,
    load_mechanism_adaptation_protocol,
)
from chemworld.eval.mechanism_adaptation_preflight import DEFAULT_PROTOCOL, ROOT

DEFAULT_OUTPUT = (
    ROOT / "workstreams/flagship_tasks/reports/mechanism-adaptation-v0.3.0-public-matrix.json"
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--protocol", type=Path, default=DEFAULT_PROTOCOL)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    protocol = load_mechanism_adaptation_protocol(args.protocol)
    rows = build_paired_campaign_matrix(protocol)
    pair_count = len({row["pair_id"] for row in rows})
    matrix_sha256 = hashlib.sha256(
        json.dumps(rows, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    report = {
        "schema_version": "chemworld-mechanism-adaptation-campaign-matrix-0.3.0",
        "protocol_id": protocol["protocol_id"],
        "protocol_sha256": hashlib.sha256(
            json.dumps(
                protocol,
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
        ).hexdigest(),
        "matrix_scope": "public_development_seeds_only",
        "private_matrix_policy": "expand after maintainer-controlled seed commitment",
        "paired_cell_count": pair_count,
        "campaign_arm_count": len(rows),
        "materialized_rows_in_report": False,
        "matrix_sha256": matrix_sha256,
        "generator": "scripts/plan_mechanism_adaptation_matrix.py",
        "axes": {
            "tasks": protocol["design"]["tasks"],
            "world_seeds": protocol["design"]["public_development_seeds"],
            "provider_repeats_per_paired_cell": protocol["design"][
                "provider_repeats_per_paired_cell"
            ],
            "candidate_label_modes": protocol["diagnosis_contract"]["candidate_label_modes"],
            "evaluation_track_id": "calibrated_online_change",
            "change_after_experiments": [
                item
                for item in protocol["evaluation_tracks"][
                    "calibrated_online_change"
                ]["change_after_experiments"]
                if item != "never"
            ],
            "arms": ["changed", "no_change_twin"],
        },
        "sample_rows": rows[:4],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(args.output)


if __name__ == "__main__":
    main()
