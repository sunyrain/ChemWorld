# C-W01-MisIndexed — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

## Mechanistic account

### Recommended process and observed outcome

The sealed recommendation is **batch 12**: 0.040 mol reagent, 0.055 L solvent S2, and 0.005 mol catalyst C3; react at 350 K for 1,800 s, cool to 320 K over 3,600 s, add 0.050 g seed, then cool successively to 310, 290, and 260 K over 14,400 s per stage before filtration. Its final assay gave crystal recovery 0.574, purity 0.998, and number-fraction fines below 20 µm of 0.482. Reaction conversion was 1.000, selectivity 0.634, and degradation warning 0.097.

Crystal recovery here is conditional on material entering crystallization:

Y_crystal = recovered target product, excluding seed / target product present before separation.

It is therefore not the overall yield from charged reagent. Reaction yield and selectivity still matter indirectly because they determine target concentration and the impurity-rich environment in which crystallization occurs.

### Material effects

**Solvent S2 was the most robust solvent for the constrained objective.** Its dossier described relatively low solubility and nucleation tendency, high crystal-growth tendency, and low impurity occlusion. The experiments were qualitatively consistent with that combination: S2 repeatedly produced very high purity and controllable fines after seeded slow cooling. With 0.080 L S2, batches 2 and 6 produced recoveries of 0.558 and 0.568, purities of 0.987 and 1.000, and fines of 0.370 and 0.385, respectively.

The solvent comparison also showed why recovery alone was insufficient:

- **S0, batch 7:** recovery 0.582, purity 0.977, but fines 0.687. Its high nominal nucleation and low growth tendencies plausibly caused many small particles.
- **S1, batch 8:** recovery 0.516, purity 0.978, and fines 0.482. It barely satisfied the fines constraint but sacrificed recovery.
- **S3, batch 9:** recovery 0.476, purity 0.974, and fines 0.594. This was worse than its nominal properties suggested, indicating that nominal dossier trends did not capture all fixed-world solvent residuals or reaction–solvent interactions.
- **S2, batch 6:** recovery 0.568, purity 1.000, and fines 0.385, giving the clearest robust balance.

These comparisons used the same nominal reaction and crystallization platform, but each condition was run once. Accordingly, they establish strong observed differences—especially S0's fines failure—but not precise causal effect sizes.

**Catalyst identity affected reaction composition more clearly than crystal morphology.** The original prior favored C1 on nominal activity, but standardized S2 batches did not establish C1 as uniquely best:

- C0, batch 4: selectivity 0.645; crystal recovery 0.555; fines 0.394.
- C1, batch 2: selectivity 0.665; recovery 0.558; fines 0.370.
- C2, batch 5: selectivity 0.541; recovery 0.442; fines 0.347.
- C3, batch 6: selectivity 0.639; recovery 0.568; fines 0.385.

C2 was numerically disfavored, while C0, C1, and C3 were not convincingly separated given assay noise and single runs. C3 was retained pragmatically because batch 6 had the largest observed recovery in that comparison, not because a unique catalytic mechanism was proven.

### Reaction–crystallization coupling

The hot reaction establishes both target loading and the impurity environment. Those variables can change the effective solubility, metastable-zone width, nucleation rate, growth rate, and impurity occlusion during cooling. Thus, even though crystal recovery is normalized to target present before separation, upstream selectivity can still influence it.

A useful qualitative representation is

S = C_target / C*(T, solvent, impurity composition),

where S is supersaturation and C* is the composition-dependent equilibrium solubility. Classical nucleation behavior is often summarized as

J proportional to exp[-B/(ln S)^2],

while growth can be represented approximately as

G proportional to (S - 1)^g.

These equations are interpretive rather than fitted laws for this benchmark. They explain the observed tradeoff: raising concentration can increase crystallizable mass, but excessive supersaturation raises nucleation much more sharply than growth, creating many sub-20-µm particles.

Reaction history was non-monotonic. Batch 2 at 350 K for 1,800 s gave selectivity 0.665, degradation warning 0.082, and crystal recovery 0.558. Batch 3 at 335 K for 3,600 s unexpectedly gave lower selectivity (0.549), higher degradation warning (0.142), and lower recovery (0.463). The initial batch at 370 K for 3,600 s had still higher degradation warning (0.222) and only 0.479 crystal recovery. These observations revised the initial assumption that a cooler, longer reaction would necessarily be gentler: in this world, the tested 350 K/1,800 s window was better than either extreme. Because temperature and duration changed together, their individual kinetic contributions remain unresolved.

### Concentration and unresolved recovery–quality tradeoff

Changing S2 volume at fixed 0.040 mol reagent exposed the central tradeoff. Approximate initial reagent concentrations were 0.50 M at 0.080 L, 0.67 M at 0.060 L, 0.73 M at 0.055 L, and 1.0 M at 0.040 L.

- **Batch 10, 0.040 L:** recovery rose to 0.586, but fines rose to 0.633; purity was 0.984.
- **Batch 11, 0.060 L with an added 300 K stage:** recovery 0.569, fines 0.473, purity 0.996.
- **Batch 12, 0.055 L with 310/290/260 K stages:** recovery 0.574, fines 0.482, purity 0.998.
- **Batch 6, 0.080 L with a simpler slow cool:** recovery 0.568, fines 0.385, purity 1.000.

Thus, increasing concentration could raise recovery, but the most concentrated condition clearly failed particle quality. Added slow-growth stages allowed an intermediate concentration to retain most of the recovery gain while remaining just inside the fines limit.

The batch-12 programmed cooling segments correspond to increasingly controlled temperature changes: 320→310 K over four hours, 310→290 K over four hours, and 290→260 K over four hours. This staged history likely distributed supersaturation generation over time, allowing existing seeded crystals to consume solute before uncontrolled secondary nucleation became dominant.

### Seeding and process-history dependence

The first batch demonstrated that final quality depended on the entire trajectory, not merely the endpoint temperature. Batch 1 used only 0.020 g seed, cooled to 270 K, and then underwent a wait that allowed the vessel to warm toward ambient. It finished with recovery 0.479 and fines 0.563. Batch 2 used 0.050 g seed, slow cooling to 260 K, and no warming hold; recovery increased to 0.558 and fines fell to 0.370.

The mechanistic interpretation is that more seed surface and sustained controlled cooling directed supersaturation toward growth rather than spontaneous nucleation. The warming hold may also have redissolved product and reduced recovery. However, seed dose, endpoint temperature, cooling duration, and removal of the warming hold all changed together, so their separate effects were not identified. An untested alternative is that thermal history, rather than seed mass, caused most of the improvement.

Seed mass was excluded from the recovery numerator, so adding seed did not mechanically inflate reported recovery. It could nevertheless improve genuine target recovery by providing growth surface and reducing losses to poorly filterable fines.

### Revisions and uncertainty

The study revised several initial expectations:

1. The nominally favored C1 catalyst was not uniquely superior; C3 became the pragmatic working catalyst after direct comparison.
2. Lower reaction temperature with longer residence time was not automatically beneficial; batch 3 contradicted that expectation.
3. S2's nominal growth/occlusion advantages were supported, but S3's poorer-than-expected result showed that the dossier was incomplete.
4. Higher concentration improved numerical recovery only by approaching or crossing the fines boundary. Slow staged cooling mitigated but did not eliminate that conflict.

Final-assay noise standards were approximately 0.010 for recovery, 0.010 for purity, and 0.018 for fines. Consequently, batch 12's recovery advantage over batch 11—0.574 versus 0.569—is smaller than the resolution needed to establish a repeatable improvement. Its fines result of 0.482 is also only 0.018 below the 0.50 limit, approximately one stated noise standard deviation. Batch 11 had a slightly larger fines margin, while batch 6 was substantially more conservative at 0.385. The sealed recommendation remains batch 12 because it was the highest observed feasible recovery, but its superiority and constraint robustness are uncertain.

Important untested alternatives include replicate runs of batches 11 and 12, intermediate solvent volumes, independent variation of seed dose, isolation of individual cooling stages, catalyst–solvent interaction studies, and direct mother-liquor measurements. Those tests would be needed to distinguish a true optimum from measurement noise and fixed-run variability.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.44 | 0.3 | 0.58 |
| Q01 | crystal_purity | 0.965 | 0.91 | 1 |
| Q01 | crystal_size | 0.14 | 0.07 | 0.23 |
| Q01 | crystal_yield | 0.4 | 0.24 | 0.55 |
| Q02 | crystal_fines_fraction | 0.54 | 0.38 | 0.7 |
| Q02 | crystal_purity | 0.96 | 0.89 | 1 |
| Q02 | crystal_size | 0.115 | 0.05 | 0.21 |
| Q02 | crystal_yield | 0.35 | 0.18 | 0.51 |
| Q03 | crystal_fines_fraction | 0.69 | 0.53 | 0.83 |
| Q03 | crystal_purity | 0.925 | 0.84 | 0.99 |
| Q03 | crystal_size | 0.055 | 0.02 | 0.13 |
| Q03 | crystal_yield | 0.28 | 0.13 | 0.44 |
| Q04 | crystal_fines_fraction | 0.43 | 0.29 | 0.57 |
| Q04 | crystal_purity | 0.956 | 0.89 | 1 |
| Q04 | crystal_size | 0.135 | 0.065 | 0.23 |
| Q04 | crystal_yield | 0.36 | 0.21 | 0.51 |
| Q05 | crystal_fines_fraction | 0.44 | 0.3 | 0.58 |
| Q05 | crystal_purity | 0.957 | 0.89 | 1 |
| Q05 | crystal_size | 0.13 | 0.06 | 0.22 |
| Q05 | crystal_yield | 0.36 | 0.21 | 0.51 |
| Q06 | crystal_fines_fraction | 0.63 | 0.47 | 0.78 |
| Q06 | crystal_purity | 0.925 | 0.83 | 0.99 |
| Q06 | crystal_size | 0.065 | 0.025 | 0.14 |
| Q06 | crystal_yield | 0.4 | 0.24 | 0.56 |
| Q07 | crystal_fines_fraction | 0.46 | 0.31 | 0.61 |
| Q07 | crystal_purity | 0.952 | 0.88 | 1 |
| Q07 | crystal_size | 0.125 | 0.055 | 0.22 |
| Q07 | crystal_yield | 0.37 | 0.22 | 0.52 |
| Q08 | crystal_fines_fraction | 0.33 | 0.2 | 0.48 |
| Q08 | crystal_purity | 0.976 | 0.92 | 1 |
| Q08 | crystal_size | 0.18 | 0.09 | 0.29 |
| Q08 | crystal_yield | 0.31 | 0.16 | 0.47 |
| Q09 | crystal_fines_fraction | 0.77 | 0.59 | 0.9 |
| Q09 | crystal_purity | 0.885 | 0.76 | 0.97 |
| Q09 | crystal_size | 0.04 | 0.01 | 0.105 |
| Q09 | crystal_yield | 0.025 | 0 | 0.1 |
| Q10 | crystal_fines_fraction | 0.68 | 0.5 | 0.83 |
| Q10 | crystal_purity | 0.91 | 0.8 | 0.98 |
| Q10 | crystal_size | 0.06 | 0.02 | 0.135 |
| Q10 | crystal_yield | 0.09 | 0.02 | 0.2 |
| Q11 | crystal_fines_fraction | 0.42 | 0.28 | 0.57 |
| Q11 | crystal_purity | 0.958 | 0.89 | 1 |
| Q11 | crystal_size | 0.14 | 0.065 | 0.235 |
| Q11 | crystal_yield | 0.38 | 0.22 | 0.53 |
| Q12 | crystal_fines_fraction | 0.56 | 0.4 | 0.71 |
| Q12 | crystal_purity | 0.935 | 0.85 | 0.99 |
| Q12 | crystal_size | 0.09 | 0.035 | 0.175 |
| Q12 | crystal_yield | 0.52 | 0.36 | 0.67 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

All recipes contain added seed, so particles are expected even when little new target crystallizes. Q01–Q02 extrapolate the observed S1/S3 comparison: S1 is predicted to retain the better fines–recovery balance despite nominal properties favoring S3 in some respects. Q03–Q04 assign the larger seed lower fines and larger crystals; seed is excluded from recovery, so its benefit is kinetic rather than arithmetic. Q05–Q06 contrast slow cooling with a temperature crash: the crash should give slightly faster recovery but substantially more nucleation and fines despite the long cold hold. Q07–Q08 treat the 315 K cycle as an anneal that dissolves fines and enlarges survivors, with some recovery loss because the final recooling is short. Q09–Q10 predict little seed-excluded recovery after the 60-second cool; the two-hour hold permits additional growth but does not erase the poor particle-size distribution. Q11–Q12 apply the observed concentration tradeoff: doubled reagent loading raises recovery but also supersaturation and fines. Intervals are deliberately broad because these recipes use much smaller charges, a hotter quenched reaction, and far longer cooling histories than the campaign; several feasibility calls, especially Q01, Q04–Q05, Q07, Q11, and Q12, remain close enough to the 0.50 fines boundary that modest model error could reverse them.

## K2

## 1. Status of the main claims

### Supported by direct observations

- **S2 gave the most robust constrained performance among the tested solvents.** Under comparable 0.080 L seeded cooling, S2 batch 6 achieved recovery 0.568, purity 1.000, and fines 0.385. S0 batch 7 had slightly higher recovery, 0.582, but failed on fines at 0.687; S1 batch 8 was feasible but had lower recovery, 0.516; S3 batch 9 had lower recovery, 0.476, and failed on fines at 0.594. The observation is the ranking of measured outcomes. The interpretation—that S2’s low nominal nucleation/occlusion and high growth tendencies caused this balance—is plausible but not directly measured.

- **Increasing concentration created a recovery–particle-quality tradeoff.** Batch 10, using 0.040 L S2, reached recovery 0.586 but fines 0.633. Batch 11 at 0.060 L with slower staging gave recovery 0.569 and fines 0.473; batch 12 at 0.055 L with additional stages gave recovery 0.574 and fines 0.482. The observed association is supported. Attribution specifically to supersaturation-driven nucleation is an interpretation because solvent volume and thermal schedule were not independently varied.

- **Process history mattered.** Batch 1, with 0.020 g seed, cooling to 270 K, and a subsequent warming wait, gave recovery 0.479 and fines 0.563. Batch 2, with 0.050 g seed, controlled cooling to 260 K, and no warming hold, gave recovery 0.558 and fines 0.370. This directly shows that the combined histories differed substantially in outcome. It does not identify which changed operation was responsible.

- **The tested 350 K/1,800 s reaction window outperformed the tested hotter and cooler/longer histories.** Batch 2 gave selectivity 0.665 and degradation warning 0.082. Batch 1 at 370 K/3,600 s had selectivity 0.572 and degradation warning 0.222; batch 3 at 335 K/3,600 s had selectivity 0.549 and degradation warning 0.142. This supports a local empirical preference, not a general kinetic optimum.

### Contradicted or revised

- **The initial expectation that C1 would be uniquely best was contradicted.** At the standardized S2 process, C0, C1, and C3 gave similar recoveries: 0.555 in batch 4, 0.558 in batch 2, and 0.568 in batch 6. C2 was lower at 0.442 in batch 5. The evidence disfavors a unique C1 advantage, although it does not securely rank C0, C1, and C3.

- **The expectation that a cooler, longer reaction would necessarily reduce degradation and improve selectivity was contradicted locally.** Batch 3 at 335 K/3,600 s was worse than batch 2 at 350 K/1,800 s. Temperature and residence time changed together, so the result does not establish a non-monotonic temperature law by itself.

- **Nominal solvent properties were not universally predictive.** S3 was expected to be relatively favorable from its dossier, yet batch 9 was worse than S1 and S2 on the constrained outcome. Hidden solvent residuals, reaction–solvent coupling, or both are plausible explanations.

### Still untested or unresolved

- The separate causal effects of seed mass, cooling rate, endpoint temperature, and the batch-1 warming hold remain unresolved.
- The small recovery difference between batches 11 and 12 is unresolved: 0.005 is below the scale needed to establish repeatable superiority, and batch 12’s fines value of 0.482 lies close to the 0.50 boundary.
- Catalyst effects among C0, C1, and C3 remain unresolved without replication and direct comparison of pre-crystallization composition.
- The proposed supersaturation, nucleation, growth, and impurity-occlusion mechanism was not directly measured. No solubility curve, mother-liquor concentration, nucleation count, or time-resolved growth data were obtained.
- Interactions among catalyst, solvent, concentration, and thermal history were sparsely sampled and remain largely untested.

## 2. One additional experiment

I would repeat the complete **batch-2 process**, changing only the seed dose from 0.050 g to 0.020 g: S2/C1 at 0.040 mol reagent and 0.080 L solvent, reaction at 350 K for 1,800 s, cooling to 320 K, 0.020 g seed, then the same slow cooling to 260 K without a warming hold. I would measure particle size before filtration and perform the same final assay.

This would distinguish two explanations for the batch-1 versus batch-2 improvement:

1. **Seed-surface explanation:** the larger seed charge suppressed spontaneous or secondary nucleation and directed supersaturation into growth.
2. **Thermal-history explanation:** avoiding the warming hold and using the batch-2 cooling trajectory caused most of the improvement, while seed dose was secondary.

If seed surface was the dominant cause, the new batch should move toward batch 1: fines would rise substantially from batch 2’s 0.370, crystal size would decline, and recovery might fall because more product would remain as poorly filterable fines. If thermal history was dominant, the new batch should remain closer to batch 2, with fines comfortably below 0.50 and recovery near 0.56 despite the smaller seed dose. An intermediate outcome would indicate that both effects contributed. This single experiment would not resolve their interaction completely, but it would remove the largest confound in the original comparison.

## 3. Least-used observation and least-reliable held-out prediction

The account used the **pre-filtration particle-size measurements** least effectively. It concentrated mainly on final assays even though batches 1–11 also had non-destructive particle readings before filtration. For example, batch 2 gave pre-filtration fines 0.353 and size 0.091, versus final fines 0.370 and size 0.111; batch 6 gave 0.346 and 0.063 before filtration versus 0.385 and 0.057 finally. These differences could have been used more explicitly to assess particle-measurement variability, filtration-associated representativeness, and the uncertainty of fines classifications. With only one reading of each type per batch, however, they cannot cleanly separate instrument noise from real sampling differences.

The least reliable held-out prediction is **Q08**, which predicted that reheating a mature S0 slurry to 315 K and recooling would reduce fines and increase size while lowering recovery. No campaign batch tested a deliberate dissolution–recrystallization cycle after prolonged crystallization. The only warming-related evidence was batch 1’s passive warming after cooling, and that comparison was confounded by seed dose, endpoint temperature, and reaction history—and it did not demonstrate beneficial annealing. In Q08, reheating might instead dissolve most product or seed, change impurity incorporation, or create a new nucleation burst during the rapid recool. Therefore, the predicted directions for size, fines, and recovery are substantially more speculative than predictions based on the directly observed solvent or concentration comparisons.
