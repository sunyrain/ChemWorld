# C-12 — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

## Mechanistic account

### System and useful relationships
The anonymous reaction is consistent with a competing network in which limiting reagent R forms target P and byproduct/degradation products D:

R → P; R or P → D.

A useful reaction description is:
- conversion = fraction of R consumed;
- selectivity = target formation relative to competing products;
- reaction yield ≈ conversion × selectivity, subject to the benchmark’s calibration;
- crystallization recovery = seed-excluded target recovered as crystals / target present immediately before separation.

Crystallization recovery is therefore not overall yield from reagent charge. As a rough process comparison, reaction yield × crystallization recovery was approximately 0.299, 0.292 and 0.304 for batches 9, 11 and 12, respectively.

For crystallization, the useful qualitative variable is supersaturation, S = C/C*(T, solvent). Nucleation generally rises more steeply with supersaturation than crystal growth. A large, sudden temperature drop can therefore generate many sub-20 µm particles, whereas gradual cooling can keep supersaturation in a growth-dominated regime. Impurity incorporation can be viewed qualitatively as increasing with rapid nucleation, occlusion and trapped mother liquor.

### Material effects
All catalyst and solvent identifiers are anonymous benchmark labels, not real chemical identities.

**Solvent S2:** The dossier suggested relatively low solubility, low nucleation tendency, high growth and low impurity occlusion. Experimentally, every completed batch used S2, so the campaign strongly establishes that S2 can deliver high purity but does not experimentally establish superiority over S0, S1 or S3. Principal optimized batches gave crystal purity of about 0.98–1.00. Alternative explanations include inherently strong lattice discrimination or selective rejection during filtration; these were not separately tested.

**Catalysts:** Under the common 340 K, 1,800 s reaction and single 14,400 s cool to 250 K:
- C0, batch 4: recovery 0.483, purity 1.000, fines 0.441;
- C1, batch 2: recovery 0.439, purity 0.984, fines 0.384;
- C2, batch 5: recovery 0.374, purity 0.976, fines 0.389;
- C3, batch 6: recovery 0.524, purity 1.000, but fines 0.540.

Thus C3 produced the highest recovery in this comparison, but its feed or crystallization behavior also promoted excessive fines under a one-step cooling history. This may reflect different target concentration, impurity composition or nucleation kinetics rather than a direct catalytic action on crystals. Those alternatives were not isolated.

### Reaction–crystallization coupling
Reaction severity affected the material entering crystallization. Batch 1 used C1 at 360 K for 3,600 s and showed degradation warning 0.194, selectivity 0.470 and crystallization recovery 0.392. Batch 2 used C1 at 340 K for 1,800 s and showed degradation warning 0.058, selectivity 0.514 and recovery 0.439. Cooling and seed history also differed, so this is not a clean reaction-temperature estimate, but it motivated avoiding the hotter, longer exposure.

The C3 staged-cooling recipe was sensitive to reaction temperature. Batch 9 used 340 K for 1,800 s and achieved recovery 0.526 with fines 0.315. Batch 10 changed the reaction temperature to 330 K while retaining the staged cooling; conversion fell to 0.974, recovery to 0.493, and fines rose to 0.596. This disconfirmed the simple hypothesis that a milder reaction would necessarily improve downstream quality. A possible interpretation is that the 330 K feed contained a different residual-reactant/impurity balance that changed supersaturation or nucleation. A batch-specific process fluctuation remains possible because this temperature comparison was not replicated.

### Process-history dependence
The strongest result was that the temperature trajectory mattered more than the final temperature alone.

Batch 6 used C3, 0.01 g seed and one 14,400 s cooling step to 250 K. It had high recovery (0.524) but failed the fines constraint (0.540). Two attempted remedies were insufficient:
- batch 7: 290 K then 250 K, recovery 0.530 and fines 0.526;
- batch 8: cool to 250 K, reheat to 310 K, then recool, recovery 0.520 and fines 0.515.

Full staging was effective. Batch 9 cooled through 320, 300, 280, 260 and 250 K, holding each programmed cooling segment for 14,400 s. It delivered recovery 0.526, purity 0.983, fines 0.315 and CSD-quality index 0.780. The direct repeat, batch 11, gave recovery 0.518, purity 0.994, fines 0.307 and CSD quality 0.764. The repeated reduction in fines supports a growth-dominated staged-cooling interpretation rather than a chance single observation.

Mechanistically, small temperature increments likely limited peak supersaturation and allowed existing crystals to consume solute before the next increment, reducing primary and secondary nucleation. The failed reheat/recool test suggests that removing fines after their formation was less effective than preventing their formation.

The benefit costs substantial time: the staged program used five 14,400 s cooling segments, versus one in the direct-cooling batches. Throughput and energy were not part of the primary recovery constraint but remain important scale-up tradeoffs.

### Seed effects
At the C1 single-cool condition, increasing seed from 0.01 g in batch 2 to 0.05 g in batch 3 produced nearly unchanged recovery (0.439 versus 0.439) and compliant fines (0.384 versus 0.370). The measured size index moved from 0.105 to 0.066, contrary to a simple expectation that more seed would yield larger particles, but the difference is only about 1.2 combined instrument standard deviations and was not replicated.

Under full C3 staging, increasing seed from 0.01 g in batches 9/11 to 0.05 g in batch 12 retained good performance: batch 12 gave recovery 0.521, purity 0.996, fines 0.311, CSD quality 0.769 and size index 0.105. It did not clearly increase seed-excluded recovery. This is mechanistically reasonable because added seed supplies growth surface but is excluded from the recovery numerator.

### Revisions during the campaign
The initial hypothesis favored C1/S2, modest seed and slow cooling. Batch 1 confirmed strong impurity rejection but narrowly failed the fines criterion and showed excessive degradation. The program was revised to a shorter 340 K reaction and uninterrupted deep cooling; batch 2 then met both constraints.

Catalyst screening revised the catalyst preference to C3 because of its higher recovery, but batch 6 exposed a recovery–fines tradeoff. Two-stage cooling and reheat/recool did not reliably solve it. The mechanism was consequently revised from “reach a low final temperature slowly” to “control supersaturation throughout the entire temperature path.” Five-stage cooling in batches 9 and 11 supported that revision. Batch 10 showed that reducing reaction temperature was not beneficial in this scope.

### Uncertainty and unresolved tradeoffs
Final-assay standard deviations were approximately 0.010 for recovery, 0.010 for purity, 0.018 for fines and CSD quality, and 0.025 for size. Consequently, recovery differences among batches 9, 11 and 12—0.526, 0.518 and 0.521—are not strong evidence that one formulation is intrinsically superior. Their shared conclusion is more robust: the C3/S2, 340 K/1,800 s reaction followed by full staged cooling repeatedly met both quality constraints at about 0.52 recovery.

The remaining tradeoff is between recovery, particle quality and process duration. Direct C3 cooling gave similar or slightly greater recovery in batches 6–7 but failed the fines limit. Full staging reduced fines substantially without an obvious recovery penalty, but required much longer processing. Batch 12 offered the largest measured size among the staged runs while its recovery was slightly below batch 9; both differences are within measurement/process uncertainty. Further replicated work would be needed to decide whether seed dose truly changes size or whether a shorter staged schedule can preserve the fines benefit.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.2 | 0.09 | 0.34 |
| Q01 | crystal_purity | 0.95 | 0.88 | 0.99 |
| Q01 | crystal_size | 0.105 | 0.06 | 0.17 |
| Q01 | crystal_yield | 0.32 | 0.2 | 0.45 |
| Q02 | crystal_fines_fraction | 0.32 | 0.18 | 0.48 |
| Q02 | crystal_purity | 0.91 | 0.82 | 0.97 |
| Q02 | crystal_size | 0.085 | 0.045 | 0.145 |
| Q02 | crystal_yield | 0.24 | 0.13 | 0.37 |
| Q03 | crystal_fines_fraction | 0.58 | 0.41 | 0.73 |
| Q03 | crystal_purity | 0.88 | 0.77 | 0.95 |
| Q03 | crystal_size | 0.055 | 0.025 | 0.105 |
| Q03 | crystal_yield | 0.15 | 0.05 | 0.27 |
| Q04 | crystal_fines_fraction | 0.42 | 0.27 | 0.58 |
| Q04 | crystal_purity | 0.91 | 0.82 | 0.97 |
| Q04 | crystal_size | 0.08 | 0.04 | 0.135 |
| Q04 | crystal_yield | 0.18 | 0.08 | 0.3 |
| Q05 | crystal_fines_fraction | 0.39 | 0.24 | 0.55 |
| Q05 | crystal_purity | 0.91 | 0.82 | 0.97 |
| Q05 | crystal_size | 0.085 | 0.045 | 0.14 |
| Q05 | crystal_yield | 0.18 | 0.08 | 0.3 |
| Q06 | crystal_fines_fraction | 0.61 | 0.45 | 0.76 |
| Q06 | crystal_purity | 0.87 | 0.75 | 0.95 |
| Q06 | crystal_size | 0.055 | 0.025 | 0.1 |
| Q06 | crystal_yield | 0.19 | 0.08 | 0.31 |
| Q07 | crystal_fines_fraction | 0.36 | 0.22 | 0.52 |
| Q07 | crystal_purity | 0.91 | 0.82 | 0.97 |
| Q07 | crystal_size | 0.09 | 0.05 | 0.15 |
| Q07 | crystal_yield | 0.19 | 0.09 | 0.31 |
| Q08 | crystal_fines_fraction | 0.46 | 0.3 | 0.63 |
| Q08 | crystal_purity | 0.89 | 0.78 | 0.96 |
| Q08 | crystal_size | 0.105 | 0.055 | 0.175 |
| Q08 | crystal_yield | 0.16 | 0.06 | 0.28 |
| Q09 | crystal_fines_fraction | 0.72 | 0.56 | 0.85 |
| Q09 | crystal_purity | 0.86 | 0.72 | 0.95 |
| Q09 | crystal_size | 0.035 | 0.015 | 0.075 |
| Q09 | crystal_yield | 0.012 | 0.001 | 0.045 |
| Q10 | crystal_fines_fraction | 0.58 | 0.41 | 0.73 |
| Q10 | crystal_purity | 0.88 | 0.76 | 0.95 |
| Q10 | crystal_size | 0.052 | 0.022 | 0.1 |
| Q10 | crystal_yield | 0.05 | 0.012 | 0.12 |
| Q11 | crystal_fines_fraction | 0.4 | 0.25 | 0.56 |
| Q11 | crystal_purity | 0.91 | 0.82 | 0.97 |
| Q11 | crystal_size | 0.083 | 0.043 | 0.14 |
| Q11 | crystal_yield | 0.18 | 0.08 | 0.3 |
| Q12 | crystal_fines_fraction | 0.47 | 0.31 | 0.64 |
| Q12 | crystal_purity | 0.87 | 0.76 | 0.95 |
| Q12 | crystal_size | 0.105 | 0.055 | 0.175 |
| Q12 | crystal_yield | 0.38 | 0.24 | 0.52 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

All recipes contain seed, so particles are expected even when seed-excluded product recovery is very small. Q01–Q02: the nominal S1 profile—lower solubility, nucleation, and occlusion than S3—supports higher recovery, purity, and size with fewer fines. Q03–Q04: more seed surface should consume supersaturation through growth and suppress spontaneous fines, although the seed effect was not cleanly resolved experimentally. Q05–Q06: gradual cooling should preserve similar equilibrium recovery but avoid the nucleation burst caused by the rapid initial drop. Q07–Q08: reheating may dissolve small particles and increase size, but the short recool can regenerate fines and leave less recovered product than an uninterrupted staged history. Q09–Q10: a 292 K hold permits some growth after the rapid drop, but recovery remains low and fines likely remain excessive. Q11–Q12: doubling reagent concentration should substantially increase crystallization recovery and growth, while also increasing nucleation, occlusion, and therefore uncertainty near the fines limit. The intervals are deliberately broad because S0, S1, and S3 were not directly tested in the sealed campaign, these recipes use a different scale and thermal history, and several feasibility calls lie close to the 0.50 fines boundary.

## K2

## 1. Status of the main claims

### Supported by direct observations
- **The C3/S2 staged process repeatedly met both quality constraints at roughly 0.52 crystallization recovery.** Batch 9 gave recovery 0.526, purity 0.983 and fines 0.315; its direct repeat, batch 11, gave 0.518, 0.994 and 0.307. Batch 12, with more seed, remained consistent at 0.521, 0.996 and 0.311. The interpretation that this is a robust operating region is supported, although the small recovery ranking among those batches is not statistically resolved.
- **C3 offered high recovery but an adverse fines tendency under simple cooling.** In the matched catalyst comparison, batch 6 reached recovery 0.524 but fines 0.540. C0, C1 and C2 in batches 4, 2 and 5 gave recoveries 0.483, 0.439 and 0.374, respectively, with compliant fines. This is a direct catalyst-associated observation; whether C3 acts through target concentration, impurity composition or another feed property remains interpretive.
- **Full staged cooling was associated with much better particle quality than the simpler C3 histories.** Batch 6 used a single long cool and failed fines at 0.540; batch 7 used two stages and still failed at 0.526; batch 8 used reheat/recool and narrowly failed at 0.515. Five-stage batches 9 and 11 gave fines near 0.31. The conclusion that process history matters is well supported.
- **The tested reheat/recool remedy was insufficient.** Batch 8 increased the size index relative to batch 6 but did not reliably cross the fines criterion. This directly supports prevention of excessive nucleation over attempting to repair the distribution afterward under that particular recycle.
- **A milder C3 reaction was not automatically better.** Batch 10 at 330 K gave recovery 0.493 and fines 0.596, versus 0.526 and 0.315 in batch 9 at 340 K with the same nominal staged crystallization. This contradicts the simple monotonic claim that lowering reaction temperature improves downstream quality, although the comparison was not replicated.
- **More seed did not clearly increase seed-excluded recovery.** Batch 2 versus batch 3 gave essentially identical recovery, about 0.439, at 0.01 versus 0.05 g seed. Under full staging, batches 9/11 at 0.01 g and batch 12 at 0.05 g all lay near 0.52. That is consistent with the recovery definition excluding seed mass.

### Supported only as interpretation, not isolated causally
- **Staging probably reduced peak supersaturation and favored growth over nucleation.** The fines results support this mechanism, but batch 9 also had five times the cooling residence time of batch 6. The campaign did not separate the temperature-path effect from total aging time.
- **S2 enabled strong impurity rejection.** Purities were generally about 0.98–1.00, even when reaction selectivity was moderate. This directly shows good purification in S2, but selective lattice incorporation, mother-liquor displacement during filtration and solvent-specific occlusion were not independently measured.
- **The hotter, longer batch-1 reaction caused more degradation.** Batch 1 had degradation warning 0.194, compared with 0.058 in batch 2, but seed dose and crystallization history also changed. The direction is plausible, not a clean temperature/time effect.

### Contradicted or revised claims
- The initial preference for **C1 as the best practical catalyst** was revised: C3 produced greater recovery once its fines problem was controlled by staging.
- The expectation that a nominal low-temperature `wait` would act as a controlled aging hold was contradicted operationally in batch 1 because the vessel warmed toward ambient during that wait.
- A general claim that **more seed produces larger crystals** was contradicted by batch 3 relative to batch 2, although batch 12 showed the opposite direction relative to some staged runs. The seed–size relationship remains unresolved rather than simply reversed.

### Still untested
- No experimental solvent comparison was performed: S0, S1 and S3 were absent from the campaign. Their effects in the sealed predictions rely on nominal dossier properties and mechanistic extrapolation.
- Chemical identities, explicit solubility curves, supersaturation, nucleation rates and growth rates were not observed.
- The effects of scale, reagent concentration, quenching, very short crystallization times and seed-only particle distributions were not tested.
- Whether staged cooling can be shortened without losing its fines benefit remains unknown.

## 2. One additional experiment

I would repeat the batch-9 composition and reaction—S2, C3, 340 K for 1,800 s and 0.01 g seed—but replace the five descending temperature stages with a direct cool to 250 K followed by four additional 14,400 s `cool_crystallize` holds at 250 K. This would match batch 9’s total cooling residence time while imposing the large temperature drop at the start.

It would distinguish two explanations currently confounded:
1. **Temperature-path/supersaturation control:** staged temperature reductions prevent the initial nucleation burst.
2. **Total-time/ripening control:** the improvement mainly comes from spending about 72,000 s in crystallization, irrespective of the path.

Expected outcomes:
- If path control dominates, recovery should remain near the C3 level, but fines should stay closer to batch 6’s approximately 0.54 than to batch 9’s approximately 0.31; CSD quality should also remain poorer.
- If total aging and ripening dominate, fines and CSD quality should approach batches 9 and 11 despite the initial direct drop.
- An intermediate result would indicate that both early supersaturation control and subsequent aging contribute.

This experiment would be more informative than another nominal replicate because it changes only the principal remaining confound in the strongest mechanistic claim.

## 3. Least-used observation and least-reliable prediction

The account used the **intermediate batch-1 HPLC observation** least effectively. After the initial reaction it showed conversion 1.000, selectivity about 0.496 and byproduct signal about 0.359. The final assay later showed selectivity about 0.470, byproduct signal about 0.382 and degradation warning 0.194. I mainly discussed the terminal degradation result, but the directional change could indicate continued unquenched chemistry during the long crystallization history. It cannot be treated as definitive because the instruments, sampling states and uncertainties differ, yet it deserved more attention in the reaction–crystallization coupling discussion.

**Q09 is the least reliable held-out prediction.** It allows only 60 s of cooling to 292 K before filtration, whereas the campaign’s informative crystallizations lasted thousands to tens of thousands of seconds. Its recovered solid would likely be dominated by the introduced seed and transient nuclei, so particle size, fines and even apparent purity depend on how minimally grown seed and newly formed particles are represented. The campaign provided almost no evidence for that regime. Q12 is another high-uncertainty extrapolation because it doubles concentration in untested S0, but Q09 is farther outside the observed time domain.
