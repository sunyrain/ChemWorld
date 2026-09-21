# Current programme: analysis and closure

This document consolidates the current cohorts. The generated [inventory](REPORT.md)
and [summary](summary.json) supply the timestamp and exact denominators. P is included
only to the extent shown there; no anticipated P outcome is treated as observed.
Remote EQ evidence is bound to `6a5ff6fc`. Its code and public exports were merged into main; retained results were not regenerated under the merged runtime.

Final scope, 21 September: 240 sources across six system families, 238 protocol-conforming
complete chains, 3,597/3,600 final-assayed source batches and all 720 K1/Q/K2 stages, plus
fifteen EQ-specific supplements. The two nonconforming sources are C's eleven-of-twelve
source and P W05/Opaque's ten final assays after two discarded vessels. P still used all
180 batch starts; its two discards are charged and preserved. All current workers have exited.

## Evidence to retain in the main analysis

EC E and PA E provide complete five-world, three-arm, 12/24-batch comparisons. RX provides
complete five-world P/S-prior and dual-goal comparisons at 12 batches. Bounded EQ/P and
canonical EQ-S v0.3 each contribute fifteen complete 12-batch sources. EQ-E adds fifteen
complete entity-characterization sources. They are three studies
within one system family. C supplies all thirty posttest chains and all thirty recommendation
retests; its single 11/12-batch source remains explicitly nonconforming. P closes the selected
scope with one goal, three E arms and twelve batches per source.

The nine-system platform scope remains distinct from the six contemporary system families
covered here. D, FL and BC do not have equivalent current autonomous cohorts. Do not expand
their matrix simply to fill a nine-system headline during this closure.

EC P/S single-world supplements, the superseded closed-set EQ-S pilot, early P pilots,
qualification runs, fixed references, interrupted attempts and exact replays remain separate.
Their evidence is retained; their counts do not enlarge the independent source denominator.

## Conclusions already supported by completed evidence

1. Additional experimental resources improve prediction in the observed EC/PA comparisons.
   Score MAE falls from 0.17378 to 0.11222 for EC discovery and 0.17811 to 0.10818 for EC
   optimization; PA organic-product-fraction MAE falls from 0.08291 to 0.02379. The larger
   resource envelope also changes computation and experimental allocation, so these are not
   fixed-token estimates of the marginal value of an observation.
2. Operational quality and predictive accuracy have different orderings. EC optimization
   improves the independent recommendation in 26/30 matched conditions but prediction in
   14/30; 13/30 improve the former while worsening the latter. RX does not reproduce a
   universal optimization advantage: corresponding counts are 9/30 and 6/30. Goals must
   be interpreted within each system rather than pooled into a universal ranking.
3. Prior effects are heterogeneous. In the newly completed EQ-S free-report cohort,
   Opaque/Aligned/MisIndexed mean prediction MAE is 0.01408/0.01590/0.01345, with 80%
   coverage 91.4%/82.6%/84.2%. World-level orderings vary. Neither a universal aligned
   advantage nor universal harm from misindexed information is supported.
4. Some endpoints remain difficult even with additional experiments. C fines-fraction
   MAE is 0.30999 at 12 batches and 0.27000 at 24, with 80% interval coverage only 35.6%
   and 43.9%. Its particle-quality prediction needs separate attention from purity,
   recovery and the execution validity of a recommended recipe.
5. P demonstrates why task constraints and response variables must remain separate. Aligned
   achieves retest purity >=0.80 in 3/5 worlds, versus 0/5 for either other arm; its average
   recovery is 0.04455, versus 0.12373 for Opaque and 0.32105 for MisIndexed. The latter's
   higher recovery is not superior delivery under the purity constraint. One Opaque retest
   is close to the cutoff (0.7992), so report continuous endpoints and the single-retest
   noise limitation alongside these counts. Aligned has lower mean purity-prediction MAE
   (0.18830 versus 0.22396/0.25078 for Opaque/MisIndexed), while Opaque has the lowest
   recovery MAE (0.06677 versus 0.06865/0.07271). Both-conforming paired sensitivity
   retains the directions of these average contrasts. Nominal 80% interval coverage is
   only 50.0–56.7% across arms and metrics. See the [P analysis](../work-ii-p-five-world-20260921-v4/ANALYSIS.md).

These are descriptive comparisons with five world clusters per condition and one model
realization per cell. Query values, metrics, arms and repeated goals are not additional
independent worlds. Report all planned arms, including unfavorable and null results.

## What is still an analysis task

The numerical results do not by themselves establish systematic information loss during
mechanism reporting. The retained trajectories and K1/Q/K2 artifacts can distinguish:

- Evidence not acquired: relevant interventions or measurements were not made.
- Evidence acquired but omitted or contradicted: a public observation conflicts with a K1 claim.
- Uncertainty appropriately retained: competing explanations remain unresolved.
- Report-to-prediction inconsistency: a sealed prediction conflicts with an explicit K1 relation.
- Operational success with limited explanatory scope: a useful recommendation coexists with
  poor out-of-domain prediction.

Use the same observable coding rules across all scheduled sources, including successful
revision and justified uncertainty. Each judgment should cite a batch/measurement, an exact
K1 claim and, where applicable, a Q response. An independent calibrated review can assess
mechanistic explanation; it must not replace simulator-grounded prediction and retest scores.
Observed associations among these events do not identify a causal compression bottleneck.

## Closure boundary

The authorized P matrix and its bounded recovery have ended. Its source/retest inventory,
replay and resource checks all pass; fifteen token records are complete. The main matrix
used six-worker maximum concurrency and took 31.34 minutes, with no main-matrix retry.
Its technical pilot's single K2 503 was repaired on the original thread before that launch.
Preserve original invalid P data and corrected qualification as engineering evidence.
Do not rerun completed scientific cells to improve their outcomes. Next work is report/trajectory annotation, figures and an abstract
grounded in the final observed scope; new systems or models would be a separate study.


## Failure disposition after remote integration

This is a retained-data review, not a new data-producing block. No provider or simulator call was made. The main matrix has no unfilled K1/Q/K2 stages and no outstanding recommendation retest. A scientific shortfall is different from lost execution.

| Record | Verified cause and retained evidence | Disposition | Rerun decision |
|---|---|---|---|
| C-W02-B12-E-Opaque | Source trajectory used 0.96 L, exactly its solvent cap. Step 145 rejected another 0.02 L; step 158 legally discarded the last vessel for lack of solvent. Eleven final assays, three posttests and the retest are retained; exact replay checks all 158 steps with zero error. | Participant resource-allocation shortfall. The public-baseline parser originally failed on `campaign_resource_rejected`; this omission is now repaired by deterministic reanalysis. | No source or posttest rerun. Its baseline is now available; the original source shortfall and parser failure remain preserved. |
| C-W05-B24-E-MisIndexed baseline | Source has 24 final assays, all posttests and a passing retest. Public-baseline parser originally rejected the retained resource-rejection transaction at step 378; the corrected baseline now uses its 24 retained final assays. | Second deterministic baseline omission; source and prediction remain complete. | Deterministic baseline repair completed; no agent rerun. |
| P-W05-B12-E-Opaque | Twelve starts, two charged legal discards, ten final assays; K1/Q/K2 and retest complete; inventory/resource/replay checks pass. | Participant source nonconformance. | Retain; do not replace after observing the result. |
| EC-W01-B12-optimization-S-Aligned (historical supplement) | Effective source has 12 assays and K1, but Q reports `tool_budget_exceeded`; K2 was not executed. Old eight-call numerical allowance was insufficient for the attempted calculation sequence. | Posttest execution-design failure, outside the primary E cohort. | Optional Q/K2-only recovery on the original thread, with a prospectively declared revised numerical budget and separate reporting, if this supplement is needed. Do not mix it silently into the old matched contrast or redo the source by default. |
| Earlier EC/PA, C and EQ transport attempts | Failed attempts and costs remain; effective main-matrix assessment chains are complete. EQ-E index marks all fifteen effective cells original; its report records zero-action proxy preflight failures. | Historical execution incidents, already resolved. | No rerun. |
| Superseded P pilots and matrices | Actual inventory defects were repaired; the affected qualification block and fresh v4 matrix were rerun from the beginning. Current source/retest conservation and replay pass. | Invalid historical development evidence, excluded from scientific pool. | Preserve old failures; do not rerun the valid successor. |
| Low purity/recovery, poor fines prediction or interval coverage | Valid observed outcomes across the scheduled arms, with no missing answers. | Scientific results. | Analyze failures and successes together; no selective rerun. |

The previously reported C shortfall is now traced to resource use and a legal discard, not an unexplained stopped session. The source-facing contract is unchanged. Both baseline parser omissions are now repaired. All thirty public baselines were recomputed, the two missing results are available, and all twenty-eight previously available results reproduced exactly. No primary prediction or retest value changed. [Baseline reanalysis](../work-ii-c-formal-20260920-v3-auto/BASELINE_REANALYSIS.md).

EQ-E now supplies 15 sources, 180 final assays and 45 canonical stages, with all cell-level completion, replay and prediction-validity checks satisfied. Opaque/Aligned/MisIndexed macro MAE is 0.01483/0.01672/0.01460 and 80% coverage is 84.6%/85.3%/83.1%. This supports heterogeneous prior effects rather than a universal aligned advantage. Different E/P/S worlds and questions prevent treating the three EQ blocks as a matched causal comparison of prior loci.

**Recommended closure:** keep the 240-source primary pool, mark its two nonconforming sources, report both all-scheduled and conforming-only sensitivity analyses, and proceed to mechanism/trajectory annotation. No mandatory paid/model rerun is identified. Only the excluded EC supplement remains optional posttest follow-up; C baselines are repaired. [Detailed quantitative analysis](DETAILED_ANALYSIS.md) and [Chinese interpretation](INTERPRETATION_ZH.md) now examine response-specific biases, paired sensitivity and a traced mechanism/prediction example.
