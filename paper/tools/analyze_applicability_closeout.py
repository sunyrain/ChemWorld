"""Two fixed retained-data diagnostics; no provider, simulator or fitted predictor."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from statistics import fmean, median

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
REPORTS = ROOT / "workstreams/flagship_tasks/reports"
CLOSEOUT = REPORTS / "work-ii-evidence-closeout-20260921"
OUT = ROOT / "output/figures/applicability-closeout"
CROOT = ROOT / "runs/formal/work-ii-c-five-world-20260920-v3-auto"
ARMS = ("Opaque", "Aligned", "MisIndexed")
GROUPS = ("other_nine", "three_most_dilute")
METRICS = ("pH_normalized", "acid_dissociation_fraction", "precipitation_signal")
LABELS = {
    "pH_normalized": "pH / 14",
    "acid_dissociation_fraction": "Dissociation fraction",
    "precipitation_signal": "Precipitation signal",
}


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_csv(name, rows):
    with (OUT / name).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def equilibrium():
    study = read(CLOSEOUT / "STORY_WORLD_ANALYSIS.json")["eq_p_query_regimes"]
    process = read(CLOSEOUT / "EQ_AUTONOMOUS_PROCESS.json")
    public = REPORTS / "work-ii-eq-bounded-equilibrium-20260920/v2-public"
    index = read(public / "INDEX.json")["cells"]
    assert {r["id"] for r in study["cells"]} == {r["cell_id"] for r in index}
    assert len(index) == len(study["cells"]) == len(process["rows"]) == 15
    points, cells = [], []
    for cell in study["cells"]:
        original = read(ROOT / cell["source"])
        predictions = {
            r["query_id"]: r for r in original["posttests"]["Q"]["payload"]["predictions"]
        }
        for group in GROUPS:
            for metric in METRICS:
                selected = [p for p in cell["groups"][group]["points"] if p["metric"] == metric]
                assert len(selected) == (3 if group == "three_most_dilute" else 9)
                for point in selected:
                    pred = predictions[point["query"]]["metrics"][metric]
                    target = fmean(t[metric] for t in original["reference_truth"][point["query"]])
                    assert abs(target - point["truth_mean"]) < 1e-12
                    assert pred["estimate"] == point["estimate"]
                    assert abs(abs(pred["estimate"] - target) - point["mae"]) < 1e-12
                    points.append(
                        {
                            "id": cell["id"],
                            "world": cell["world"],
                            "arm": cell["arm"],
                            "group": group,
                            **point,
                        }
                    )
                cells.append(
                    {
                        "id": cell["id"],
                        "world": cell["world"],
                        "arm": cell["arm"],
                        "group": group,
                        "metric": metric,
                        "queries": len(selected),
                        "mae": fmean(p["mae"] for p in selected),
                        "coverage": fmean(p["coverage"] for p in selected),
                    }
                )
    assert len(points) == 540 and len(cells) == 90
    aggregates = []
    for group in GROUPS:
        for metric in METRICS:
            for arm in ARMS:
                subset = [
                    r for r in cells if (r["group"], r["metric"], r["arm"]) == (group, metric, arm)
                ]
                assert len(subset) == 5
                aggregates.append(
                    {
                        "group": group,
                        "metric": metric,
                        "arm": arm,
                        "worlds": 5,
                        "mae": fmean(r["mae"] for r in subset),
                        "coverage": fmean(r["coverage"] for r in subset),
                    }
                )
    for original in study["aggregate"]:
        subset = [
            r for r in aggregates if (r["group"], r["arm"]) == (original["group"], original["arm"])
        ]
        for field in ("mae", "coverage"):
            assert abs(fmean(r[field] for r in subset) - original[field]) < 1e-12
    effects = []
    for group in GROUPS:
        for metric in METRICS:
            subset = {
                r["arm"]: r for r in aggregates if (r["group"], r["metric"]) == (group, metric)
            }
            pairs = []
            for world in sorted({r["world"] for r in cells}):
                pair = {
                    r["arm"]: r
                    for r in cells
                    if (r["world"], r["group"], r["metric"]) == (world, group, metric)
                }
                pairs.append(pair["Aligned"]["mae"] - pair["Opaque"]["mae"])
            effects.append(
                {
                    "group": group,
                    "metric": metric,
                    "aligned_minus_opaque": subset["Aligned"]["mae"] - subset["Opaque"]["mae"],
                    "aligned_lower_worlds": sum(v < 0 for v in pairs),
                    "aligned_higher_worlds": sum(v > 0 for v in pairs),
                    "macro_difference_contribution": (
                        subset["Aligned"]["mae"] - subset["Opaque"]["mae"]
                    )
                    / 3,
                }
            )
    write_csv("eq-query-responses.csv", points)
    write_csv("eq-campaign-response-groups.csv", cells)
    write_csv("eq-response-groups.csv", aggregates)
    return {
        "campaigns": 15,
        "point_forecasts": 540,
        "aggregates": aggregates,
        "effects": effects,
        "macro": study["aggregate"],
        "source_batches": 180,
        "failures": [],
    }


def crystal():
    baseline = read(REPORTS / "work-ii-c-formal-20260920-v3-auto/BASELINE_REANALYSIS.json")
    original = read(ROOT / baseline["source_report"])["results"]
    selected = {r["id"]: r for r in baseline["rows"]}
    assert len(original) == len(selected) == 30
    queries = read(CROOT / "design.json")["queries"]
    assert len(queries) == 12
    references = {}
    for world in sorted({r["world"] for r in selected.values()}):
        reference = read(CROOT / "qualification" / world / "queries/result.json")
        references[world] = dict(
            zip((q["query_id"] for q in queries), reference["truth"], strict=True)
        )
    rows, points = [], []
    for cell in original:
        meta = selected[cell["id"]]
        forecasts = {q["query_id"]: q for q in cell["posttests"]["Q"]["payload"]["predictions"]}
        target = np.array(
            [references[meta["world"]][q["query_id"]]["crystal_purity"] for q in queries]
        )
        predicted = np.array(
            [forecasts[q["query_id"]]["crystal_purity"]["estimate"] for q in queries]
        )
        error = predicted - target
        bias = float(error.mean())
        residual = (predicted - predicted.mean()) - (target - target.mean())
        mse = float(np.mean(error**2))
        cmse = float(np.mean(residual**2))
        assert abs(mse - bias**2 - cmse) < 1e-14
        assert abs(float(np.abs(error).mean()) - meta["agent_mae"]["crystal_purity"]) < 1e-12
        assert abs(bias - meta["response_diagnostics"]["crystal_purity"]["signed_bias"]) < 1e-12
        reference_sd = float(target.std())
        row = {
            "id": cell["id"],
            "world": meta["world"],
            "arm": meta["arm"],
            "budget": meta["budget"],
            "conforming": meta["conforming"],
            "queries": 12,
            "bias_pp": bias * 100,
            "mae_pp": float(np.abs(error).mean()) * 100,
            "mse_pp2": mse * 10000,
            "squared_bias_pp2": bias**2 * 10000,
            "centred_mse_pp2": cmse * 10000,
            "centred_rmse_pp": cmse**0.5 * 100,
            "reference_sd_pp": reference_sd * 100,
            "prediction_sd_pp": float(predicted.std()) * 100,
            "bias_fraction_of_mse": bias**2 / mse,
            "underestimated_queries": int(sum(error < 0)),
        }
        rows.append(row)
        for i, query in enumerate(queries):
            points.append(
                {
                    "id": cell["id"],
                    "world": meta["world"],
                    "arm": meta["arm"],
                    "budget": meta["budget"],
                    "query": query["query_id"],
                    "reference": float(target[i]),
                    "prediction": float(predicted[i]),
                    "error": float(error[i]),
                    "centred_error": float(residual[i]),
                }
            )
    assert len(points) == 360 and sum(r["underestimated_queries"] for r in rows) == 335
    groups = []
    for budget, arm in [(None, None), *((b, a) for b in (12, 24) for a in ARMS)]:
        rr = [
            r
            for r in rows
            if (budget is None or r["budget"] == budget) and (arm is None or r["arm"] == arm)
        ]
        groups.append(
            {
                "budget": budget,
                "arm": arm or "All",
                "campaigns": len(rr),
                "mean_bias_pp": fmean(r["bias_pp"] for r in rr),
                "mean_centred_rmse_pp": fmean(r["centred_rmse_pp"] for r in rr),
                "mean_reference_sd_pp": fmean(r["reference_sd_pp"] for r in rr),
                "mean_prediction_sd_pp": fmean(r["prediction_sd_pp"] for r in rr),
                "mean_mae_pp": fmean(r["mae_pp"] for r in rr),
                "pooled_squared_bias_fraction": sum(r["squared_bias_pp2"] for r in rr)
                / sum(r["mse_pp2"] for r in rr),
                "median_campaign_bias_fraction": median(r["bias_fraction_of_mse"] for r in rr),
                "negative_bias_campaigns": sum(r["bias_pp"] < 0 for r in rr),
                "centred_error_exceeds_reference_variation": sum(
                    r["centred_rmse_pp"] > r["reference_sd_pp"] for r in rr
                ),
            }
        )
    write_csv("crystal-purity-queries.csv", points)
    write_csv("crystal-purity-campaigns.csv", rows)
    write_csv("crystal-purity-groups.csv", groups)
    return {
        "campaigns": 30,
        "point_forecasts": 360,
        "source_shortfalls": [r["id"] for r in rows if not r["conforming"]],
        "groups": groups,
        "rows": rows,
        "failures": [],
    }


def appendix(eq, crystal_data):
    lines = [
        "# Appendix G. Response contributions and purity-error diagnosis",
        "",
        "## G.1 Equilibrium reversal by response",
        "",
        "This exploratory decomposition retains all fifteen parameter-prior campaigns "
        "and all 540 response predictions. It uses the existing three-lowest-concentration "
        "grouping. MAE first averages queries within a campaign and response, "
        "then the five worlds. Averaging the three response MAEs exactly recovers Table 1. "
        "The same worlds recur across arms; queries and responses are not independent replicates.",
        "",
        "**Table G1. Original prediction MAE by response and concentration group.**",
        "",
        "| Response | Group | Opaque | Aligned | MisIndexed | Lower / higher |",
        "| :--- | :--- | ---: | ---: | ---: | :--- |",
    ]
    for metric in METRICS:
        for group in GROUPS:
            rr = {
                r["arm"]: r
                for r in eq["aggregates"]
                if (r["metric"], r["group"]) == (metric, group)
            }
            effect = next(r for r in eq["effects"] if (r["metric"], r["group"]) == (metric, group))
            name = "Dilute three" if group == "three_most_dilute" else "Other nine"
            lines.append(
                f"| {LABELS[metric]} | {name} | {rr['Opaque']['mae']:.5f} | "
                f"{rr['Aligned']['mae']:.5f} | {rr['MisIndexed']['mae']:.5f} | "
                f"{effect['aligned_lower_worlds']} / {effect['aligned_higher_worlds']} of 5 |"
            )
    lines.extend(
        [
            "",
            "The final column counts worlds with lower/higher Aligned MAE than Opaque. "
            "Signed response differences divided by three sum to the macro-error difference. "
            "They quantify the contribution on the declared normalized scales; they do not "
            "establish a shared failure mechanism or physical comparability of targets.",
            "",
            "\\clearpage",
            "",
            "## G.2 Separating purity offset from variation error",
            "",
            "For each of thirty campaigns, let $p_i$ and $y_i$ be its original prediction "
            "and retained noiseless reference for the twelve queries. Define "
            "$b=\\overline{p-y}$ and $c_i=(p_i-\\bar p)-(y_i-\\bar y)$. Then",
            "",
            "$$\\operatorname{MSE}=b^2+\\frac{1}{12}\\sum_{i=1}^{12}c_i^2.$$",
            "",
            "The first term measures the common offset; the second measures mismatched "
            "variation across conditions. Centred RMSE is the square root of the second term. "
            "Reference and prediction standard deviations use denominator twelve. "
            "All calculations retain the source-assay shortfall. Demeaning uses withheld "
            "references only for diagnosis; it is not an available predictor or a corrected "
            "performance result. MAE has no analogous additive decomposition.",
            "",
            "**Table G2. Purity offset and variation diagnostics.**",
            "",
            "| Batches | Arm | N | Bias | cRMSE | Ref. SD | Pred. SD | Offset share |",
            "| ---: | :--- | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for r in crystal_data["groups"]:
        budget = "Both" if r["budget"] is None else str(r["budget"])
        lines.append(
            f"| {budget} | {r['arm']} | {r['campaigns']} | {r['mean_bias_pp']:.3f} | "
            f"{r['mean_centred_rmse_pp']:.3f} | {r['mean_reference_sd_pp']:.3f} | "
            f"{r['mean_prediction_sd_pp']:.3f} | "
            f"{100 * r['pooled_squared_bias_fraction']:.1f}% |"
        )
    overall = crystal_data["groups"][0]
    lines.extend(
        [
            "",
            "N is the campaign count; cRMSE denotes centred RMSE. Bias, cRMSE and both "
            "standard deviations are campaign means in percentage points. "
            "Offset share is the ratio of summed squared campaign biases to summed campaign MSEs, "
            "with equal query counts; it is not the mean campaign fraction. "
            "The median campaign fraction is "
            f"{100 * overall['median_campaign_bias_fraction']:.1f}%. "
            f"Mean bias is negative in {overall['negative_bias_campaigns']} of 30 campaigns. "
            "Centred RMSE exceeds reference SD in "
            f"{overall['centred_error_exceeds_reference_variation']} of 30. "
            "These comparisons describe forecast outputs and do not identify "
            "an internal revision process. "
            "No new agent or simulator calls were made.",
            "",
        ]
    )
    (ROOT / "paper/venues/ncs/applicability_diagnostics.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    eq = equilibrium()
    print("stage=equilibrium completed=540/540", flush=True)
    c = crystal()
    print("stage=purity completed=360/360", flush=True)
    result = {
        "scope": "Fixed post hoc diagnostics of retained predictions; no new experiments",
        "provider_calls": 0,
        "simulator_calls": 0,
        "equilibrium": eq,
        "crystallization": c,
        "failures": [],
        "inputs": {
            "equilibrium": str((CLOSEOUT / "STORY_WORLD_ANALYSIS.json").relative_to(ROOT)),
            "crystallization": str(
                (
                    REPORTS / "work-ii-c-formal-20260920-v3-auto/BASELINE_REANALYSIS.json"
                ).relative_to(ROOT)
            ),
            "crystallization_execution": str(CROOT.relative_to(ROOT)),
        },
    }
    (OUT / "diagnostics.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    appendix(eq, c)
    print(
        json.dumps({"eq_effects": eq["effects"], "purity_summary": c["groups"][0]}, indent=2),
        flush=True,
    )


if __name__ == "__main__":
    main()
