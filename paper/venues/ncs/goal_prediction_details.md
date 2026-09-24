\clearpage

## E.4 Complete research-objective comparison

Figure 3 uses 120 campaigns and sixty original goal pairs. Each pair fixes world, information arm, budget and prior locus. EC has five worlds, three arms and two budgets at the entity locus; RX has five worlds, three arms and two loci at twelve batches. The independent recommendation retest and twelve-query score MAE are separate endpoints. EC references are single seeded observations; RX point references are five-observation means. No new campaigns or predictions were produced for this analysis.

**Table E3. All joint goal outcomes.**

| Higher retest | Lower score MAE | EC pairs | RX pairs |
| --- | --- | --- | --- |
| Optimization | Optimization | 13 | 4 |
| Optimization | Discovery | 13 | 5 |
| Discovery | Optimization | 1 | 4 |
| Discovery | Discovery | 3 | 17 |

Both endpoints favour the same campaign in 16/30 EC and 21/30 RX pairs, and opposite campaigns in 14/30 and 9/30. Strict signs define these descriptive counts; near-zero differences are not thereby significant. Each system reuses five worlds. RX score MAE favours optimization in 8/30 pairs; its separate six-response macro MAE does so in 6/30.

![World-level summaries of the same goal comparison. a,b, Electrochemical recommendation retests and score-prediction MAE. c,d, Reaction-processing endpoints. Each bar averages six campaigns per goal within a world. World labels are system-specific; bar means do not replace the individual paired differences in Figure 3. Scales differ across panels.](../../figures/venue-results/figureS6-goal-world-means.pdf){width=100%}

\clearpage

## E.5 Strata and recovery sensitivity

**Table E4. Endpoint orderings within design strata.**

| System | Factor | Level | Pairs | Same | Opposite |
| --- | --- | --- | --- | --- | --- |
| EC | World | W01 | 6 | 3 | 3 |
| EC | World | W02 | 6 | 4 | 2 |
| EC | World | W03 | 6 | 3 | 3 |
| EC | World | W04 | 6 | 5 | 1 |
| EC | World | W05 | 6 | 1 | 5 |
| EC | Budget | 12 | 15 | 7 | 8 |
| EC | Budget | 24 | 15 | 9 | 6 |
| EC | Arm | Aligned | 10 | 6 | 4 |
| EC | Arm | MisIndexed | 10 | 5 | 5 |
| EC | Arm | Opaque | 10 | 5 | 5 |
| EC | Locus | E | 30 | 16 | 14 |
| RX | World | W01 | 6 | 4 | 2 |
| RX | World | W02 | 6 | 4 | 2 |
| RX | World | W03 | 6 | 3 | 3 |
| RX | World | W04 | 6 | 4 | 2 |
| RX | World | W05 | 6 | 6 | 0 |
| RX | Budget | 12 | 30 | 21 | 9 |
| RX | Arm | Aligned | 10 | 6 | 4 |
| RX | Arm | MisIndexed | 10 | 9 | 1 |
| RX | Arm | Opaque | 10 | 6 | 4 |
| RX | Locus | P | 15 | 12 | 3 |
| RX | Locus | S | 15 | 9 | 6 |

Same means that the higher-retest campaign also has lower MAE; opposite means it has higher MAE. These overlapping strata do not add independent tests. Budget rows compare goals at a fixed budget, not a twelve-to-twenty-four-batch contrast. E denotes entity priors, P parameter priors and S structural priors.

The EC subset with neither campaign having a recorded recovery contains seventeen pairs: ten have the same ordering and seven the opposite ordering. Optimization has higher retests in fifteen and lower MAE in eight. This subset excludes assessment-only recovery as well as source recovery; it has uneven coverage and does not replace the full cohort.

\clearpage

## E.6 All batches of the selected electrochemical pair

The illustration uses one retrospectively selected twelve-batch Opaque pair in the first electrochemical world. It is not an additional replication or a random sample. Both original agents retain their research context for the later assessments. Every batch uses 0.020 mol in 0.040 L; current denotes the configured cap.

**Table E5. Discovery source batches.**

| Batch | Pair | V | mA | Electrolysis / s | Score |
| --- | --- | --- | --- | --- | --- |
| 1 | S0/E0 | -1.5 | 100 | 1200 | 0.000000 |
| 2 | S1/E0 | -1.5 | 100 | 1200 | 0.167530 |
| 3 | S2/E0 | -1.5 | 100 | 1200 | 0.000000 |
| 4 | S3/E0 | -1.5 | 100 | 1200 | 0.050903 |
| 5 | S0/E0 | 0.5 | 100 | 1200 | 0.509008 |
| 6 | S0/E0 | 1.5 | 100 | 1200 | 0.044293 |
| 7 | S0/E0 | 2.5 | 100 | 1200 | 0.030644 |
| 8 | S0/E1 | 0.5 | 100 | 1200 | 0.000000 |
| 9 | S0/E2 | 0.5 | 100 | 1200 | 0.482517 |
| 10 | S0/E3 | 0.5 | 100 | 1200 | 0.360679 |
| 11 | S0/E2 | 0.5 | 100 | 1200+13200 | 0.606942 |
| 12 | S0/E2 | 0.5 | 500 | 1200+13200 | 0.710658 |

**Table E6. Optimization source batches.**

| Batch | Pair | V | mA | Electrolysis / s | Score |
| --- | --- | --- | --- | --- | --- |
| 1 | S0/E0 | 1 | 100 | 3600 | 0.535704 |
| 2 | S1/E1 | -1.5 | 300 | 7200 | 0.282124 |
| 3 | S2/E2 | 1.5 | 300 | 7200 | 0.674932 |
| 4 | S3/E3 | 1.5 | 300 | 7200 | 0.313717 |
| 5 | S2/E0 | 1.5 | 300 | 7200 | 0.033808 |
| 6 | S0/E2 | 1.5 | 300 | 7200 | 0.042443 |
| 7 | S2/E2 | 1 | 300 | 7200 | 0.570485 |
| 8 | S2/E2 | 2 | 300 | 7200 | 0.000000 |
| 9 | S2/E2 | 1.5 | 500 | 7200 | 0.722737 |
| 10 | S2/E2 | 1.5 | 500 | 10000 | 0.731956 |
| 11 | S2/E2 | 1.4 | 500 | 9000 | 0.714786 |
| 12 | S2/E2 | 1.5 | 400 | 12000 | 0.749194 |

Both campaigns select batch 12. Independent retests are 0.717587 for discovery and 0.756122 for optimization; twelve-query score MAEs are 0.088394 and 0.229397.

\clearpage

## E.7 Operation sequence and subsequent public accounts

All batches add reagent, add solvent, set potential/electrolyte/current, electrolyze, measure UV-visible response, terminate and obtain a final assay, in that order. Discovery batches 11 and 12 insert a second 13,200-s electrolysis after the first 1,200-s electrolysis and its UV-visible measurement. Their 14,400-s totals therefore do not describe one uninterrupted operation. The records contain 86 discovery and 84 optimization operations. The phase labels in Figure 3 summarize recorded choices, not contemporaneous internal thoughts.

The following original public rationales accompany the sealed Q forecasts, after research and K1. They were issued without reference feedback. They are public accounts, not validated mechanisms or evidence that the acquired observations were sufficient.

**Discovery Q rationale (verbatim).**

> Predictions use the campaign’s empirical potential-window and charge-delivery trends at nearly the same concentration: +0.8 V is treated as closer to the productive +0.5 V regime than −0.8 V, duration raises conversion and yield, and 500 mA raises yield while penalizing faradaic, transport, and energy efficiencies. Electrolyte and solvent adjustments follow the matched short-run screens. Intervals are deliberately broad because both test potentials are unmeasured, long-time data exist only at +0.5 V/E2, and low-yield assay noise strongly affects short runs and the score’s yield gate.

**Optimization Q rationale (verbatim).**

> Predictions use the observed S0/E0 batch as the main local anchor, scale product formation with electrolysis duration and configured current, and impose the campaign’s strong positive-potential window. The S0/E1, S0/E3, and S2/E0 combinations are assigned low activity because cross-pair controls showed severe nonadditive solvent–electrolyte incompatibility. Higher current raises expected yield but lowers transport and charge efficiency. Intervals include final-assay noise plus substantial extrapolation uncertainty, especially for negative polarity and untested material pairs.

\clearpage

## E.8 Complete optimization forecasts

All twelve forecasts use 0.012 mol in 0.025 L. Predictions and nominal 80% intervals were sealed before reference feedback. References below are the original seeded observations. The four bold query identifiers share +0.8 V, 100 mA and 7,200 s, while changing the material pair.

**Table E7. Query settings, sealed forecasts and reference scores.**

| Q | Pair | V | mA | s | Forecast | 80% interval | Reference |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 01 | S0/E0 | -0.8 | 100 | 600 | 0.050 | 0.000-0.180 | 0.032659 |
| 02 | S0/E0 | 0.8 | 100 | 600 | 0.230 | 0.040-0.480 | 0.349491 |
| 03 | S0/E0 | -0.8 | 100 | 7200 | 0.250 | 0.080-0.440 | 0.358985 |
| **04** | S0/E0 | 0.8 | 100 | 7200 | 0.570 | 0.430-0.680 | 0.572012 |
| 05 | S0/E1 | -0.8 | 100 | 7200 | 0.080 | 0.000-0.250 | 0.362359 |
| **06** | S0/E1 | 0.8 | 100 | 7200 | 0.100 | 0.000-0.290 | 0.627599 |
| 07 | S0/E3 | -0.8 | 100 | 7200 | 0.070 | 0.000-0.230 | 0.347853 |
| **08** | S0/E3 | 0.8 | 100 | 7200 | 0.090 | 0.000-0.280 | 0.542955 |
| 09 | S2/E0 | -0.8 | 100 | 7200 | 0.060 | 0.000-0.210 | 0.288226 |
| **10** | S2/E0 | 0.8 | 100 | 7200 | 0.070 | 0.000-0.240 | 0.494376 |
| 11 | S0/E0 | -0.8 | 500 | 7200 | 0.170 | 0.040-0.360 | 0.276451 |
| 12 | S0/E0 | 0.8 | 500 | 7200 | 0.550 | 0.390-0.680 | 0.344881 |

Score MAE is 0.229397; interval coverage is 5/12. The accurate Q04 prediction is retained alongside the large underestimates at Q06, Q08 and Q10. Source-to-query changes involve amount, volume and electrical settings, so these contrasts do not isolate one changed variable. Twelve query outcomes do not establish population calibration. No intermediate sealed prediction checkpoints were collected, so final prediction errors cannot be plotted as a within-session learning curve.
