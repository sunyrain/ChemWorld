# Applicability closeout: retained-data analysis

Question: which responses contribute to the equilibrium regime reversal, and how much of crystallization purity error is a campaign-wide offset versus erroneous variation among withheld conditions?

Fixed coverage: all 15 EQ parameter-prior campaigns (five worlds, three arms, 12 queries and three responses: 540 point forecasts), and all 30 C campaigns (five worlds, three arms, two independent budgets, 12 purity queries: 360 point forecasts). Keep all source-assay shortfalls. The existing three-lowest-concentration grouping is exploratory and remains fixed. No new participant, simulator, experiment, fitted predictor or outcome-based exclusions.

Inputs: `configs/current.json` is checked first; it does not register these later EQ/C closeout exports. Use the current manuscript's retained source indexes and original producer bindings: `STORY_WORLD_ANALYSIS.json`, `EQ_AUTONOMOUS_PROCESS.json`, the EQ public `INDEX.json` and per-source `RESULT.json`; C `BASELINE_REANALYSIS.json` points to its original `summary.json`, with the original query design/reference files in `runs/formal/work-ii-c-five-world-20260920-v3-auto`. These are the already-consumed current article sources, not files chosen by version-looking names. Do not rewrite them.

Measurements: EQ campaign/group/response MAE and original interval coverage; across-world means and matched-world directions; signed response contributions to the Aligned-minus-Opaque macro-error difference. C signed mean error, raw MSE, squared mean error, and centred MSE. Verify MSE = squared bias + centred MSE for every campaign. Compare centred error with the variation of the retained references as a diagnostic, never as a corrected predictive score. Report both equally weighted campaign summaries and pooled squared-error components; do not call a ratio of summed squares a typical-campaign proportion.

Completion rules: exactly 540 EQ and 360 C query records; reproduce published aggregate MAEs and C per-campaign purity MAEs to numerical precision; retain 335 underestimates and the source shortfall; report all processing failures. No significance inference from reused queries/worlds. A failed consistency check stops publication of the derived panels until the discrepancy is resolved; it does not trigger new experiments.

Outputs: reproducible analysis/figure script, JSON summary with coverage/failures and input paths, full campaign/query CSVs, reader-facing supplementary tables, and vector Figure 5. A compact model/source note records the actual execution models and information excerpts. The main manuscript keeps chemical details brief; equations and numerical diagnostics belong in the supplement.

## Completed outputs

- `diagnostics.json` and the six EQ/C diagnostic CSVs retain all 540 equilibrium and 360 purity forecasts; processing failures are empty and the source-assay shortfall is retained. Original MAEs and the 335 underestimates are reproduced.
- EQ: Aligned worsens all three responses in all five worlds under dilution. Its other-nine benefit is mainly the precipitation response; dissociation and pH have mixed paired directions.
- C: mean signed bias is -4.289 percentage points. Squared campaign biases account for 87.647% of pooled squared error. Mean centred RMSE is 1.889 pp versus reference SD 0.598 pp; the former is greater in 29/30 campaigns. This is a diagnosis, not a corrected predictor.
- Figure 5 exports PDF/SVG/PNG under `paper/figures/venue-results/figure05-eq-coverage-reversal.*`. Three additional plotting CSVs retain all source points, withheld reference means and the most-dilute forecasts. No continuous response curve was invented.
- Reader-facing definitions and tables are in `paper/venues/ncs/applicability_diagnostics.md` and `process_model_details.md`. Execution-source notes are in `model_sources.md` here.
- Rebuild the diagnostics with `uv run --no-sync python paper/tools/analyze_applicability_closeout.py` and the figure with `uv run --no-sync python paper/tools/render_eq_closeout.py`.

Integration checked against the current English full PDF (50 pages; 150-word abstract; 3,068 main words excluding captions) and Chinese main-only PDF (11 pages). Both retain four Results sections, six main figures and one main table. Decimal values and figure bindings agree; every page was rendered and visually inspected. The remaining main figures were not redrawn for this block.
