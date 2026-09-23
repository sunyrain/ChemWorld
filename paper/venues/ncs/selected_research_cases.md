# Appendix D. Selected autonomous research histories

Figure 2 and Supplementary Fig. S4 follow the same retrospectively selected Aligned crystallization pair. Each budget is an independent session. The case documents actions, observations and later public accounts; it does not estimate the cohort-wide effect of additional resources.

## D.1 Experimental paths, recommendations and retests

A retrospectively selected Aligned crystallization pair illustrates how independent sessions can follow different experimental paths (Fig. 2). The 12-batch session first obtains a quality-feasible product in batch 1 and later lowers the cooling endpoint from 260 to 250 K. The 24-batch session first becomes feasible in batch 20, after changing heating and introducing staged cooling. Its selected procedure has higher independently retested recovery and lower fines than the smaller session's selection. This example illustrates recorded actions and outcomes, not a population budget effect. Contemporaneous decision reasons were not recorded; the illustration therefore shows recorded changes without reconstructing immediate thoughts.

The 12-batch session first meets the quality constraints at batch 1, with recovery 34.7%, and reaches its best feasible observed recovery of 51.2% at batch 10. The 24-batch session first becomes feasible at batch 20 and reaches 57.0% at batch 23. Quality feasibility and subsequent optimization are distinct milestones. All 36 original batch results remain in the source data, including the infeasible trials.

Quench in this environment stops reaction chemistry while subsequent cooling and crystal growth remain possible. The two sessions differ in materials and multiple process conditions; their comparison does not isolate a quench effect. Heating and cooling values are requested targets, not measured temperature trajectories. The K1 summaries were written after the source experiments and are distinct from contemporaneous decision logs.

\clearpage

## D.2 Sealed predictions and subsequent reflection

Figure S4 follows the same sessions through sealed prediction and subsequent reflection; the proposed experiment was not executed.

![Sealed predictions and subsequent reflection in the same selected crystallization pair. a, The withheld comparison replaces a two-hour hold at 278.15 K with heating towards 315 K for one hour and recooling for one hour after a common preceding recipe. Thermal profiles are schematic. b, Both original sessions predict lower fines. The condensed public K2 answers follow sealed Q predictions without reference feedback. c, The 24-batch session proposes changing only the cooling procedure of its selected batch; possible outcomes would distinguish upstream, cooling and interaction explanations. This proposal was not executed. d, The evaluator's reference concerns the thermal intervention in a, not the proposed experiment in c, and was unavailable during Q and K2.](../../figures/final-ppt/figureS4-posttest-reflection.png){width=100%}

\clearpage

# Appendix E. Supporting outcomes and examples

## E.1 Quality constraints and response-specific references

Purification gives a related distinction between recovery and acceptable delivery. Aligned recommendations meet the purity threshold in three of five worlds, compared with none for Opaque or MisIndexed. Yet mean recovered fractions are 0.04455, 0.12373 and 0.32105 for Aligned, Opaque and MisIndexed, respectively. Recovering more material therefore does not imply satisfying the commission. A single retest near the purity threshold is also not a precise estimate of a procedure's reliability. These system-specific outcomes cannot be represented faithfully by a universal yield score (Fig. S5a).

Purification provides another response-specific example: fourteen of fifteen campaigns correctly judge a small concentration effect on purity, but only two correctly judge the small purity effect of splitting a wash. Recognizing approximate invariance is itself a predictive achievement, and depends on the intervention.

In crystallization, agent size forecasts have lower MAE than the source mean in four of thirty campaigns and fines forecasts in twenty-one (Fig. S5b,c). Together with the recovery and purity contrasts in the main text, these results retain the complete response-specific comparison.

![Additional operational and predictive outcomes. a, All fifteen purification recommendations, showing original-charge recovery and independently retested purity. The line marks the purity threshold of 0.80; eligible counts are 0/5, 3/5 and 0/5 for Opaque, Aligned and MisIndexed. b,c, Size and fines MAE for all thirty crystallization campaigns relative to each campaign's public observation mean. Points above the diagonal favour the mean; the campaign with a source-assay shortfall remains included. These panels use different response scales.](../../figures/final-ppt/figureS5-secondary-outcomes.png){width=100%}

## E.2 Additional selected examples

In a selected Aligned phase-partitioning campaign pair, the larger budget covers all sixteen material pairings and then allocates eight experiments to process variation; the smaller campaign covers ten pairings. This is a plausible route to improvement, not a cohort-wide causal explanation. Two Aligned world pairs nevertheless worsen.

Uncertainty is part of the same applicability problem. The poor dilute-equilibrium coverage shows that a wrong extrapolation can also be overconfident. In a retrospectively selected MisIndexed crystallization campaign, the mechanism report explicitly acknowledges that only one solvent was tested. Nevertheless, predicted purity averages 0.86833 against a reference mean of 0.98566, and all twelve nominal 80% intervals miss. A verbal statement of uncertainty does not by itself ensure calibrated quantitative prediction.

\clearpage

## E.3 Complete crystallization baseline and interval comparisons

Figure 6b reports how often each response is predicted more accurately than the public observation mean. Table E1 supplies the corresponding error magnitudes and the public nearest-neighbour comparison. Each baseline is fitted separately to the same campaign's public final assays; neither receives withheld outcomes or additional experiments. Nearest-neighbour prediction also uses public recipe features. These are empirical references rather than strong system-identification baselines.

\needspace{12\baselineskip}

**Table E1. Crystallization prediction errors and baseline comparisons.**

| Response | Agent MAE | Mean MAE | Nearest MAE | Wins: mean | Wins: nearest |
| :--- | ---: | ---: | ---: | ---: | ---: |
| Recovery | 0.09185 | 0.17135 | 0.17308 | 26/30 | 26/30 |
| Purity | 0.04354 | 0.00482 | 0.00905 | 0/30 | 4/30 |
| Size index | 0.06923 | 0.02345 | 0.02708 | 4/30 | 7/30 |
| Fines fraction | 0.29000 | 0.31651 | 0.32426 | 21/30 | 20/30 |

MAE is averaged equally over all thirty campaigns in each response's original scale; errors are not ranked across responses. Recovery, purity and fines are fractions, while size is the declared size index. Mean and Nearest denote the public observation-mean and nearest-neighbour predictors. Wins count strictly lower agent MAE; neither comparison has ties. The source-assay shortfall remains included, and the five world instances are reused across arms and independent budget sessions.

Table E2 accompanies the purity coverage comparison in Figure 6d. Wider intervals need not cover a biased prediction's reference, while coverage exceeding the nominal level does not by itself establish calibration or sharpness.

\needspace{12\baselineskip}

**Table E2. Purity interval coverage and width by information arm and budget.**

| Budget | Information arm | Campaigns | Coverage (%) | Mean width (pp) |
| ---: | :--- | ---: | ---: | ---: |
| 12 | Opaque | 5 | 98.3 | 6.81 |
| 12 | Aligned | 5 | 60.0 | 12.94 |
| 12 | MisIndexed | 5 | 23.3 | 15.53 |
| 24 | Opaque | 5 | 95.0 | 8.59 |
| 24 | Aligned | 5 | 73.3 | 12.37 |
| 24 | MisIndexed | 5 | 55.0 | 12.31 |

The original intervals have nominal 80% coverage and concern the pre-final-assay response target. Coverage and interval width are averaged over each campaign's twelve queries and then over its five-world arm-budget group. Each row contains sixty query targets but only five world clusters; queries are not independent world replicates. Width is expressed in percentage points of purity. All original intervals and source failures remain unchanged.
