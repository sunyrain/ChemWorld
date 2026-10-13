# C-W04-Aligned — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

## Mechanistic account

### Observed process behavior
The campaign indicates that crystallization morphology, rather than purity, was the binding constraint. Final crystal purity was generally about 0.97–1.00, while the fines fraction often lay near or above the required 0.50 limit.

The initial material-based hypothesis favored solvent S2 because its nominal dossier suggested low solubility, low nucleation, strong growth, and low impurity occlusion. This prediction was only partly borne out: S2 gave high purity and useful recovery, but not acceptable morphology. Batch 1 (S2/C1, 0.05 g seed, cooling to 278 K) gave recovery 0.315 and purity 0.987, but fines were 0.634. Longer cooling did not fully solve this: batch 2 (S2/C2, 290 K endpoint) gave recovery 0.193 and fines 0.527, while batch 3 (S2/C3, 295 K) gave recovery 0.205 and fines 0.575. Catalyst, temperature, and reaction history differed among these batches, so they do not isolate a pure solvent effect, but they clearly overturned the expectation that S2 would automatically meet the morphology constraint.

The evidence shifted the preferred system to S1/C1. With a 0.05 g seed charge, batch 4 reached recovery 0.322 and purity reported at 1.00, but final fines remained marginally high at 0.520. Reducing the seed charge was the most consequential change: batch 8 used 0.005 g seed and gave recovery 0.341, purity 0.976, and fines 0.481; batch 9 used 0.001 g seed and cooled to 278 K, giving recovery 0.352, purity 0.978, and fines 0.490. Thus, within this tested recipe family, the large seed charge apparently created or retained too many sub-20-micrometre particles. Lower seed mass reduced the number of small seed-derived particles relative to product grown onto them, improving both the fines fraction and the reported crystal-size/CSD metrics.

### Reaction–crystallization coupling
A useful conceptual decomposition is

`n_target ≈ n_limiting × conversion × selectivity`,

followed by a crystallization-stage recovery

`Y_cryst = n_target,recovered / n_target,before separation`.

Consequently, high crystallization recovery alone does not imply high overall synthetic yield. The selected S1/C1 batches had nearly complete reported conversion but only moderate reaction selectivity, generally about 0.42–0.47, with byproduct signals around 0.39–0.44. In batch 12, the post-reaction HPLC estimate was conversion 0.991, selectivity 0.415, and reaction yield 0.434; the final assay gave conversion 1.00, selectivity 0.424, and reaction yield 0.430. The agreement supports the interpretation that the reaction was essentially conversion-complete and that selectivity, rather than conversion, limited target formation.

Reaction composition also controls the crystallization driving force. In simplified form,

`supersaturation ratio = C_target / C*(T, solvent, impurities)`,

where `C*` is the equilibrium solubility. Crystal recovery should increase as the endpoint temperature lowers and `C*` falls. Classical qualitative relationships are useful:

`J_nucleation ∝ exp[-A/(ln supersaturation ratio)^2]`

and

`G_growth ∝ (supersaturation ratio − 1)^g`.

When supersaturation becomes too high, nucleation can rise faster than growth, increasing particle count and fines even as recovery improves. Reaction impurities may additionally change solubility, inhibit growth, or become occluded, although the consistently high measured purity suggests that impurity occlusion was not the dominant limitation in the tested S1/S2 processes.

### Endpoint-temperature tradeoff
The low-seed S1/C1 sequence showed the clearest quality/recovery tradeoff. Batch 9, ending at 278 K, gave recovery 0.352 and fines 0.490. Batch 10, ending at 270 K, increased recovery to 0.373 but moved fines to 0.497, almost exactly at the limit. Batch 11, ending at 260 K, increased recovery again to 0.383, but fines rose to 0.529 and failed the specification. This is consistent with deeper cooling increasing the mass crystallized while also creating a late nucleation population that remains below 20 micrometres.

The evidence therefore supports approximately 270 K as the lowest practical endpoint within the tested low-seed S1/C1 process, not as a universal thermodynamic optimum. Batch 12 used that endpoint with only 0.0001 g seed and achieved recovery 0.358, purity 0.990, and fines 0.488. It was selected because it balanced useful recovery with more observed fines margin than batch 10. Batch 8 had still more margin (fines 0.481) but lower recovery (0.341), illustrating that robustness and maximum observed recovery do not select exactly the same operating point.

### Process-history dependence
The results show that endpoint temperature alone is insufficient to describe the process. Seed population and thermal trajectory matter because the final particle distribution integrates nucleation, growth, dissolution, and possible secondary nucleation over time.

A single warm reheat/recool experiment did not produce the hoped-for ripening benefit. Batch 5 reheated a crystallized S1/C1 slurry to 305 K and recooled it to 285 K; it ended with recovery 0.301 and fines 0.559, worse than the simpler batch 4 trajectory. A plausible interpretation is that partial dissolution followed by renewed cooling generated another nucleation population rather than selectively enlarging existing crystals. However, this was one implementation, confounded by assay noise and batch variability, so it does not rule out a properly optimized temperature-cycling or Ostwald-ripening strategy.

Likewise, applying a second cooling/holding command at 285 K in batch 6 did not clearly improve the result: recovery was 0.330 and fines 0.523. The operation may have added little growth driving force once the first cooling stage had depleted supersaturation. Batch 1 is additionally difficult to interpret because its post-cooling wait allowed the slurry to warm toward ambient before filtration; redissolution or restructuring during that interval may have altered both recovery and particle distribution.

### Material effects and interpretation limits
S1 ultimately performed better than the nominal dossier implied for constraint-feasible crystallization. Its moderate solubility, reduced nominal occlusion, and balanced nucleation/growth tendencies may have allowed a broader growth window than S2 under the realized hidden material residuals. C1 was retained because it gave reproducibly high conversion and adequate target formation in the successful S1 batches. The C2 and C3 trials did not outperform it, but those comparisons were confounded with solvent, temperature, and crystallization conditions; the campaign does not establish a catalyst-specific elementary reaction mechanism.

The anonymous materials also preclude claims about molecular identities, transition states, polymorphs, or specific intermolecular interactions. A compatible but untested alternative is that S1 stabilizes the growing crystal face or weakens homogeneous nucleation relative to S2 under this particular hidden world. Another is that differences attributed to solvent actually arise from solvent-dependent reaction impurity profiles. No experiment independently exchanged crystallization solvent after completing the same reaction, so those explanations remain unresolved.

### Revisions and uncertainty
The principal revision was from a dossier-led S2 hypothesis to an evidence-led S1/C1, low-seed process. A second revision was recognizing that colder endpoints do not monotonically improve the constrained objective: recovery continued to increase down to 260 K, but fines became unacceptable.

The final-assay standard deviations were approximately 0.010 for crystal recovery, 0.010 for purity, and 0.018 for fines. Batch 10's fines margin was only about 0.003, much smaller than one assay standard deviation. Batch 12's margin was about 0.012 and therefore better but still smaller than one standard deviation. The recovery difference between batches 10 and 12 was about 0.015, also only around the scale of combined measurement uncertainty. Accordingly, their numerical ranking is not strong evidence of a reproducible effect; batch 12 is a risk-aware operating choice rather than proof of a unique optimum. Replication would be needed to quantify process variability and establish the probability of satisfying the fines limit.

Overall, the supported mechanistic picture is a nearly conversion-complete but moderately selective reaction feeding a supersaturation-controlled crystallization. Lower S1 seed loading reduces the small-particle population, while deeper cooling raises recovery until nucleation-driven fines become limiting. High purity is comparatively robust, leaving the unresolved recovery-versus-fines tradeoff as the main optimization problem.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.39 | 0.29 | 0.49 |
| Q01 | crystal_purity | 0.97 | 0.92 | 1 |
| Q01 | crystal_size | 0.14 | 0.08 | 0.21 |
| Q01 | crystal_yield | 0.36 | 0.24 | 0.48 |
| Q02 | crystal_fines_fraction | 0.48 | 0.37 | 0.59 |
| Q02 | crystal_purity | 0.94 | 0.87 | 0.99 |
| Q02 | crystal_size | 0.105 | 0.055 | 0.17 |
| Q02 | crystal_yield | 0.27 | 0.16 | 0.4 |
| Q03 | crystal_fines_fraction | 0.39 | 0.27 | 0.51 |
| Q03 | crystal_purity | 0.95 | 0.88 | 0.99 |
| Q03 | crystal_size | 0.18 | 0.1 | 0.27 |
| Q03 | crystal_yield | 0.16 | 0.06 | 0.29 |
| Q04 | crystal_fines_fraction | 0.55 | 0.44 | 0.66 |
| Q04 | crystal_purity | 0.95 | 0.88 | 0.99 |
| Q04 | crystal_size | 0.095 | 0.045 | 0.16 |
| Q04 | crystal_yield | 0.17 | 0.07 | 0.3 |
| Q05 | crystal_fines_fraction | 0.53 | 0.42 | 0.64 |
| Q05 | crystal_purity | 0.95 | 0.88 | 0.99 |
| Q05 | crystal_size | 0.105 | 0.05 | 0.17 |
| Q05 | crystal_yield | 0.17 | 0.07 | 0.3 |
| Q06 | crystal_fines_fraction | 0.65 | 0.54 | 0.76 |
| Q06 | crystal_purity | 0.93 | 0.85 | 0.98 |
| Q06 | crystal_size | 0.07 | 0.025 | 0.13 |
| Q06 | crystal_yield | 0.18 | 0.07 | 0.31 |
| Q07 | crystal_fines_fraction | 0.51 | 0.4 | 0.62 |
| Q07 | crystal_purity | 0.95 | 0.88 | 0.99 |
| Q07 | crystal_size | 0.115 | 0.055 | 0.18 |
| Q07 | crystal_yield | 0.18 | 0.08 | 0.31 |
| Q08 | crystal_fines_fraction | 0.6 | 0.48 | 0.72 |
| Q08 | crystal_purity | 0.93 | 0.85 | 0.98 |
| Q08 | crystal_size | 0.08 | 0.03 | 0.145 |
| Q08 | crystal_yield | 0.12 | 0.035 | 0.24 |
| Q09 | crystal_fines_fraction | 0.86 | 0.73 | 0.96 |
| Q09 | crystal_purity | 0.95 | 0.85 | 1 |
| Q09 | crystal_size | 0.03 | 0.008 | 0.07 |
| Q09 | crystal_yield | 0.01 | 0 | 0.055 |
| Q10 | crystal_fines_fraction | 0.74 | 0.61 | 0.86 |
| Q10 | crystal_purity | 0.95 | 0.86 | 1 |
| Q10 | crystal_size | 0.045 | 0.015 | 0.095 |
| Q10 | crystal_yield | 0.055 | 0.005 | 0.15 |
| Q11 | crystal_fines_fraction | 0.55 | 0.44 | 0.66 |
| Q11 | crystal_purity | 0.95 | 0.88 | 0.99 |
| Q11 | crystal_size | 0.095 | 0.045 | 0.16 |
| Q11 | crystal_yield | 0.17 | 0.07 | 0.3 |
| Q12 | crystal_fines_fraction | 0.59 | 0.47 | 0.71 |
| Q12 | crystal_purity | 0.91 | 0.82 | 0.97 |
| Q12 | crystal_size | 0.085 | 0.035 | 0.15 |
| Q12 | crystal_yield | 0.49 | 0.36 | 0.62 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

All recipes are seeded, so particles are expected even where little seed-excluded product crystallizes. Q01–Q02: S1 is predicted to outperform S3 through lower solubility, lower nucleation and lower occlusion, giving greater recovery and fewer fines. Q03–Q04: reducing seed from 0.045 to 0.001 g should produce fewer competing particles, larger crystals and fewer fines; the very long schedule makes their recoveries similar. Q05–Q06: gradual cooling should suppress the initial nucleation burst relative to a 120 s crash, while the long common residence time keeps recovery broadly similar. Q07–Q08: the 315 K reheat followed by rapid recooling is expected to dissolve some product and regenerate fines, consistent with the campaign’s unsuccessful reheat/recool test. Q09–Q10: a 292 K hold permits limited growth beyond the 60 s endpoint, but high solubility and the warm endpoint keep seed-excluded recovery low and fines high. Q11–Q12: doubling concentration substantially increases fractional recovery by reducing the relative dissolved-product loss, but also raises supersaturation, impurity burden and secondary nucleation. Intervals are deliberately broad because S0/S3 and these multi-day trajectories were not directly tested; uncertainty includes hidden material residuals, reaction-derived impurity differences and extrapolation of seed/cooling-history effects. Borderline feasibility classifications, especially Q02 and Q07, are correspondingly uncertain.

## K2

## 1. Status of the main claims

### Supported within the tested operating window

- **Lower seed loading improved morphology in S1/C1.** This is the cleanest comparison. Batch 4 used 0.05 g seed and gave fines 0.520, recovery 0.322 and purity 1.00; otherwise similar batch 8 used 0.005 g seed and gave fines 0.481, recovery 0.341 and purity 0.976. These are direct observations. Interpreting them as fewer small seed-derived particles and less competition for growth is plausible, but particle-number evolution was not measured directly.

- **Deeper cooling increased recovery until fines became limiting.** Under low-seed S1/C1 conditions, batch 9 at 278 K gave recovery 0.352 and fines 0.490; batch 10 at 270 K gave 0.373 and 0.497; batch 11 at 260 K gave 0.383 and 0.529. The numerical trend is directly observed. The explanation that deeper cooling raises supersaturation and secondary nucleation is an interpretation, not a direct measurement of nucleation rate.

- **Reaction conversion was effectively complete while selectivity remained moderate.** In batch 12, post-reaction HPLC estimated conversion 0.991, selectivity 0.415 and yield 0.434; the final assay gave conversion 1.00, selectivity 0.424 and yield 0.430. This directly supports conversion completeness and a selectivity limitation for that recipe.

- **Purity was not the principal binding constraint.** Across the relevant completed batches, final purity remained approximately 0.97–1.00 while fines frequently exceeded 0.50. This is a direct campaign-wide observation.

### Contradicted or revised

- **The initial expectation that S2 would inherently give favorable morphology was contradicted operationally.** Batch 1 had fines 0.634; batches 2 and 3 had fines 0.527 and 0.575. Those results directly contradict the practical prediction of constraint-feasible S2 crystallization under the tested recipes. They do not prove an intrinsic S2 effect because catalyst, charge, temperature and thermal history were not held constant across all S2/S1 comparisons.

- **The tested reheat/recool cycle did not improve ripening.** Relative to batch 4, batch 5 added a 305 K reheat and recooling stage but changed recovery from 0.322 to 0.301 and fines from 0.520 to 0.559. Thus improvement was contradicted for that implementation. The proposed explanation—partial dissolution followed by renewed nucleation—remains interpretive.

- **An extra isothermal cooling stage did not clearly improve morphology.** Batch 6 gave recovery 0.330 and fines 0.523, essentially no convincing improvement over batch 4. This argues against a large benefit from that specific added hold, but does not exclude longer or differently controlled maturation.

### Still untested or only weakly supported

- A molecular explanation for the S1/S2 difference, including solvent effects on particular crystal faces, impurity adsorption or polymorph selection, remains untested.
- The claim that C1 is intrinsically the best catalyst is weak: C2 and C3 were tested under confounded crystallization conditions rather than in a controlled catalyst-only comparison.
- Classical nucleation-versus-growth equations are useful organizing models, but nucleation rate, growth rate, solubility curves and polymorph identity were not measured.
- The apparent superiority of batch 12 over batch 10 is not statistically established. Their recovery difference was about 0.015 and their fines difference about 0.009, both comparable to combined assay uncertainty.

## 2. One additional experiment

I would run a **within-batch staged endpoint experiment** based on batch 9: S1/C1, the same reaction charge and history, 0.001 g seed, and cooling to 278 K for 14,400 s. I would make a non-destructive particle-size measurement at 278 K, then cool the same slurry to 270 K for another 14,400 s, make a second particle-size measurement, filter, terminate and perform the final assay.

This would distinguish two leading explanations for the batch 9–11 trend:

1. **Deeper cooling creates a new fine-particle population.** Expected outcome: the 270 K measurement shows a higher fines fraction and little or negative change in number-weighted size, while the final assay shows increased recovery relative to batch 9.
2. **The apparent endpoint trend mainly reflects between-batch and assay variability.** Expected outcome: particle size and fines remain essentially unchanged after the 278→270 K stage, with the final outcome falling within ordinary batch-to-batch scatter.

A third possible result—larger particles and lower fines after the second stage—would indicate continued growth or ripening rather than secondary nucleation and would directly challenge the mechanism used in the report. The within-batch comparison would remove catalyst, charge, seed and initial reaction history as confounders, although intermediate particle measurements would still not provide an intermediate crystal-recovery measurement.

## 3. Least effectively used observation and least reliable prediction

The account used the **disagreement between in-process particle imaging and final-assay morphology** least effectively. For example, batch 4 had a pre-filtration particle estimate near 0.484 fines but a final value of 0.520; batch 6 similarly had an in-process estimate near 0.484 and a final value of 0.523. These gaps are larger than should be ignored when interpreting values close to the 0.50 limit. They could reflect different instrument biases, sampling state, filtration/history effects or ordinary noise. The report acknowledged uncertainty but treated final-assay differences more mechanistically than these discrepancies warranted.

**Q12 is the least reliable held-out prediction.** It extrapolated simultaneously to solvent S0, a reaction/crystallization protocol not directly tested in the campaign, and a twofold concentration increase. Its predicted recovery relied on an assumed nonlinear reduction in the fraction left dissolved, while its predicted fines and purity relied on an assumed supersaturation/impurity penalty. No campaign pair isolated concentration at fixed solvent, seed and thermal history, and no S0 solubility curve was measured. Therefore the direction of higher recovery is mechanistically plausible, but the sealed numerical estimates and accompanying quality classification have the weakest empirical calibration.
