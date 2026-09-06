"""Reader-facing projections of current published evidence, never raw provider records."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def evidence_summary():
    current = json.loads((ROOT / "configs/current.json").read_text(encoding="utf-8"))["work_ii"]

    def read(key):
        return json.loads((ROOT / current[key]["report"]).read_text(encoding="utf-8"))

    diagnostic = read("w2_77_final_diagnostic")
    result = {
        "source": "published_research",
        "scope": "Two agent configurations; distinct protocols",
        "diagnostic": {
            key: diagnostic[key]
            for key in ("scheduled", "worlds", "counts", "by_prior", "by_model_tool", "primary")
        },
    }
    for name, key in (("m1", "w2_72_m1_replication"), ("m3", "w2_69_m3_portability")):
        report = read(key)
        primary = next(c for c in report["statistics"]["contrasts"] if c["primary"])
        worlds = [
            r
            for r in report["statistics"]["world_contrasts"]
            if r["contrast"] == primary["contrast"]
        ]
        result[name] = {
            "worlds": report["independent_world_clusters"],
            "sessions": report["provider_opportunities"],
            "completed": report["provider_completed"],
            "failures": len(report["failures"]),
            "conditions": report["statistics"]["condition_summaries"],
            "primary": primary,
            "agreement": report["agreement"],
            "world_effects": [
                {
                    "world": f"{'E' if r['task'].startswith('electro') else 'C'}"
                    f"{r['cluster_id'].rsplit('w', 1)[-1]}",
                    "task": r["task"],
                    "difference": r["mean_difference"],
                }
                for r in worlds
            ],
        }
    if "w2_79_public_information" in current:
        info = read("w2_79_public_information")
        result["public_information"] = {
            key: info[key] for key in ("worlds", "scheduled_pairs", "summaries", "interpretation")
        }
    return result
