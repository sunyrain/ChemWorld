# C-W02-MisIndexed — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

## Mechanistic account

The materials are anonymous benchmark catalysts and solvents, so the following is a process-level interpretation rather than a claim about real chemical identities.

### Reaction-stage material effects

At fixed S2 solvent and essentially the same reaction and direct-cooling history, catalyst identity had a large effect. C0 (batch 7) gave reaction yield 0.636, selectivity 0.609, and crystal recovery 0.579. C1 (batch 4) gave 0.576, 0.590, and 0.519, respectively; C3 (batch 6) gave 0.520, 0.518, and 0.468; C2 (batch 5) was poorest at 0.455, 0.461, and 0.382. These differences are much larger than the final-assay noise scales and caused me to revise the initial nominal-property expectation that C1 would be best. In this realized world, C0 was the strongest tested catalyst.

A useful approximate relation is

`reaction product yield ≈ conversion × selectivity`,

with deviations representing the benchmark’s degradation, side-product, and measurement terms. Conversion was near unity in most batches, so selectivity—not additional conversion—was the main reaction limitation. For example, C2/S2 in batch 5 reached conversion 0.996 but only selectivity 0.461, whereas C0/S1 in batch 11 reached conversion 0.999 and selectivity 0.706. Thus hotter or longer reaction merely to raise conversion would not be expected to solve the dominant loss.

### Solvent effects and crystallization mechanism

The nominal dossier suggested that S2 should support crystal growth and purity: low relative solubility, low nucleation tendency, high growth tendency, and low impurity occlusion. The experiments partly supported that prediction. S2 batches generally had high purity and acceptable fines. With C0, batch 7 produced purity 0.980, fines 0.351, and recovery 0.579.

S1 offered higher observed recovery but was more sensitive to cooling history. Under direct repeated cooling to 250 K with C1, batch 9 reached recovery 0.586 and purity 0.986, but its fines fraction was 0.483—passing the 0.50 limit only narrowly. S0 under a comparable direct-cooling schedule gave recovery 0.585 but fines 0.761 (batch 10), while S3 gave recovery 0.453 and fines 0.633 (batch 8). Both therefore failed the particle-quality constraint despite adequate purity.

The observations are consistent with supersaturation-controlled competition between nucleation and growth. Defining supersaturation as

`S = C / C*(T)`,

one may describe nucleation qualitatively by

`J ∝ exp[-B/(ln S)^2]`

and growth by

`G ∝ (S - 1)^g`.

A rapid increase in supersaturation can raise the number of new nuclei sharply, increasing the number fraction below 20 µm. A staged temperature descent limits the instantaneous supersaturation excursion and allows existing seed and crystals to consume solute by growth before the next cooling step.

The limiting recovery can be represented schematically as

`Rcryst ≈ 1 - Cmother(Tfinal) Vmother / ntarget,pre-separation`,

modified by incomplete equilibration, filtration retention, and occluded mother liquor. The reported recovery is explicitly seed-excluded, so added seed mass does not count as recovered target.

### Reaction–crystallization coupling

Although crystal recovery is normalized to target present before separation, reaction quality still matters indirectly. Catalyst and solvent determine the amount and composition of the target-bearing solution entering crystallization. Side products can change effective solubility, compete for crystal surfaces, promote heterogeneous nucleation, or remain in cake liquor. This coupling is visible in the fixed-S2 catalyst series: the poorly selective C2 batch 5 had both low reaction yield and low crystal recovery, whereas C0 batch 7 improved both substantially. However, this is correlation within the synthetic benchmark; a fully decoupled experiment using identical isolated feed solutions was not performed.

Purity was comparatively robust—approximately 0.977 to 1.000 across the main completed processes—so morphology and mother-liquor retention, rather than impurity rejection, were the binding crystallization constraints. High purity should not be interpreted as proof that reaction impurities were mechanistically irrelevant, only that the recovered solids rejected them effectively under the tested conditions.

### Process-history dependence

Batch 1 established feasibility with C1/S2: recovery 0.467, purity 0.991, and fines 0.400. It used only one 7,200 s cooling step to 280 K followed by a wait during which temperature drifted toward ambient. Its lower recovery is consistent with limited cold residence and partial redissolution or reduced driving force.

Extending C1/S2 cold treatment improved recovery: two 14,400 s stages at 250 K gave 0.504 in batch 2, while four such stages gave 0.519 in batch 4. The 0.015 difference is suggestive but modest relative to assay uncertainty and was not replicated.

The clearest history effect occurred with S1. Batch 11 used C0, 0.05 g seed, and sequential 14,400 s stages at 320, 300, 280, 260, and 250 K. It achieved recovery 0.618, purity 0.991, and fines 0.218. This is much better morphology than direct-cooled S1 batch 9, whose fines were 0.483, while also improving recovery. Catalyst differed between these batches, so the exact size of the staging effect remains confounded; a matched C0/S1 direct-cooling control was not run.

Batch 12 repeated the batch-11 staged descent and added four further 14,400 s stages at 250 K. Its observed recovery was 0.621, purity 0.992, and fines 0.226. It remained the recommended batch because it had the highest observed recovery and wide margins to both quality limits.

### Seeding

In matched C1/S2 experiments, reducing seed from 0.05 g in batch 2 to 0.01 g in batch 3 left recovery essentially unchanged: 0.504 versus 0.503. The measured normalized size decreased from 0.112 to 0.072. Thus seed loading affected the observed size distribution more clearly than recovery in this comparison. This result is not sufficient to establish a general seed-size law because neither condition was replicated and the size difference is only modestly above the stated size-noise scale.

### Revisions, uncertainty, and unresolved tradeoffs

The initial model favored S2 and C1 based on nominal dossier properties. Experimental evidence caused two revisions: C0 replaced C1 as the preferred catalyst, and staged S1 crystallization replaced direct S2 cooling as the highest-recovery feasible process. The S2 prior remained useful for predicting relatively clean morphology but did not identify the maximum-recovery solvent/history combination.

Final-assay standard deviations were approximately 0.010 for crystal recovery and purity, 0.018 for fines, 0.025 for normalized size, 0.010 for selectivity, and 0.006 for reaction yield. Each recipe received only one final assay. Consequently, the recovery difference between batches 11 and 12—0.003—is not resolved and should not be claimed as a proven benefit of the four extra cold stages. Their fines difference, 0.008, is likewise unresolved. Batch 11 is therefore a credible shorter-cycle alternative, although batch 12 remains the sealed recommendation on highest observed recovery.

The principal unresolved tradeoff is cold residence versus cycle time, not purity versus recovery: batches 11 and 12 both comfortably met purity and fines specifications. Direct S1 cooling displayed a more apparent recovery/morphology tradeoff—high recovery but fines close to the limit—while staged cooling appeared to relax it. Replicated matched C0/S1 runs with and without staged cooling, followed by a residence-time series near 250 K, would be required to determine whether recovery truly plateaus near 0.62 and whether batch 12’s additional residence is justified.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.32 | 0.18 | 0.48 |
| Q01 | crystal_purity | 0.97 | 0.91 | 1 |
| Q01 | crystal_size | 0.14 | 0.07 | 0.23 |
| Q01 | crystal_yield | 0.22 | 0.09 | 0.37 |
| Q02 | crystal_fines_fraction | 0.52 | 0.35 | 0.69 |
| Q02 | crystal_purity | 0.98 | 0.92 | 1 |
| Q02 | crystal_size | 0.11 | 0.04 | 0.2 |
| Q02 | crystal_yield | 0.14 | 0.04 | 0.28 |
| Q03 | crystal_fines_fraction | 0.53 | 0.35 | 0.71 |
| Q03 | crystal_purity | 0.96 | 0.86 | 1 |
| Q03 | crystal_size | 0.055 | 0.015 | 0.12 |
| Q03 | crystal_yield | 0.07 | 0 | 0.18 |
| Q04 | crystal_fines_fraction | 0.42 | 0.26 | 0.59 |
| Q04 | crystal_purity | 0.97 | 0.88 | 1 |
| Q04 | crystal_size | 0.12 | 0.05 | 0.21 |
| Q04 | crystal_yield | 0.09 | 0 | 0.21 |
| Q05 | crystal_fines_fraction | 0.4 | 0.24 | 0.57 |
| Q05 | crystal_purity | 0.97 | 0.88 | 1 |
| Q05 | crystal_size | 0.13 | 0.06 | 0.23 |
| Q05 | crystal_yield | 0.085 | 0 | 0.2 |
| Q06 | crystal_fines_fraction | 0.68 | 0.51 | 0.83 |
| Q06 | crystal_purity | 0.95 | 0.84 | 1 |
| Q06 | crystal_size | 0.06 | 0.015 | 0.13 |
| Q06 | crystal_yield | 0.13 | 0.025 | 0.28 |
| Q07 | crystal_fines_fraction | 0.39 | 0.23 | 0.56 |
| Q07 | crystal_purity | 0.97 | 0.88 | 1 |
| Q07 | crystal_size | 0.135 | 0.06 | 0.24 |
| Q07 | crystal_yield | 0.1 | 0 | 0.23 |
| Q08 | crystal_fines_fraction | 0.28 | 0.13 | 0.47 |
| Q08 | crystal_purity | 0.985 | 0.92 | 1 |
| Q08 | crystal_size | 0.17 | 0.08 | 0.29 |
| Q08 | crystal_yield | 0.045 | 0 | 0.15 |
| Q09 | crystal_fines_fraction | 0.62 | 0.4 | 0.82 |
| Q09 | crystal_purity | 0.96 | 0.78 | 1 |
| Q09 | crystal_size | 0.018 | 0.004 | 0.05 |
| Q09 | crystal_yield | 0.005 | 0 | 0.035 |
| Q10 | crystal_fines_fraction | 0.57 | 0.35 | 0.77 |
| Q10 | crystal_purity | 0.965 | 0.82 | 1 |
| Q10 | crystal_size | 0.03 | 0.008 | 0.075 |
| Q10 | crystal_yield | 0.025 | 0 | 0.085 |
| Q11 | crystal_fines_fraction | 0.41 | 0.25 | 0.58 |
| Q11 | crystal_purity | 0.97 | 0.88 | 1 |
| Q11 | crystal_size | 0.13 | 0.055 | 0.23 |
| Q11 | crystal_yield | 0.09 | 0 | 0.21 |
| Q12 | crystal_fines_fraction | 0.48 | 0.33 | 0.64 |
| Q12 | crystal_purity | 0.94 | 0.84 | 0.99 |
| Q12 | crystal_size | 0.1 | 0.04 | 0.18 |
| Q12 | crystal_yield | 0.38 | 0.23 | 0.55 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

The intervals represent uncertainty in the latent, noise-free outcomes, not final-assay sampling noise. Q01–Q02 apply the campaign observation that C1/S1 outperformed C1/S3 in recovery and fines, while allowing the very slow ramp to moderate nucleation. Q03–Q04 predict that more seed mainly improves size distribution and fines, with little seed-excluded recovery change. Q05–Q06 hold total aging roughly fixed: immediate cooling gives more time at the cold endpoint and slightly more recovery, but a much larger nucleation burst and excessive fines. Q07–Q08 treat reheating as an annealing/dissolution step: it should remove fines and enlarge survivors but leave less time to regain dissolved product, lowering recovery. Q09–Q10 remain weakly crystallized at 292 K; the extra two-hour dwell raises recovery modestly but is unlikely to repair the rapid-cooling morphology. Q11–Q12 isolate concentration: doubling reagent should substantially increase supersaturation and recovery, while reducing purity and pushing fines close to the limit. Uncertainty is widest for low-charge S0 recipes because the campaign did not directly locate their solubility threshold, and for annealing because no matched reheating experiment was run.

## K2

## 1. Status of the main claims

### Supported by direct observations

- **Catalyst identity materially affected the reaction and downstream recovery.** In the matched S2/direct-cooling series, C0 in batch 7 gave reaction yield 0.636, selectivity 0.609, and crystal recovery 0.579. Corresponding recoveries were 0.519 for C1 (batch 4), 0.468 for C3 (batch 6), and 0.382 for C2 (batch 5). These differences exceed the reported assay noise. The observation supports C0 as the best catalyst among those tested under that process; the molecular reason remains interpretive.
- **Solvent identity strongly affected morphology.** With C1 and comparable direct-cooling histories, S1 in batch 9 gave recovery 0.586 and fines 0.483, S3 in batch 8 gave 0.453 and 0.633, and S0 in batch 10 gave 0.585 and 0.761. Thus S0 and S3 directly failed the fines criterion in those histories, while S1 narrowly passed.
- **Purity was not the binding constraint in the tested campaign.** Final purities remained approximately 0.977–1.000 across the principal comparisons, including batches that failed on fines.
- **Seed loading had little resolved effect on recovery in one matched comparison.** Batches 2 and 3 differed mainly in seed charge, 0.05 versus 0.01 g, yet recovery was 0.504 versus 0.503. Their normalized sizes were 0.112 versus 0.072, suggesting a size effect, although this lacks replication and is only modestly above the size-noise scale.
- **Additional cold residence beyond the batch-11 schedule did not show a resolved recovery advantage.** Batch 11 produced recovery 0.618, purity 0.991, and fines 0.218; batch 12 produced 0.621, 0.992, and 0.226. The recovery difference of 0.003 is below the 0.010 assay-noise scale.

### Contradicted or revised

- **The initial expectation that C1 would be the preferred catalyst was contradicted.** C0 was substantially better in the controlled S2 catalyst comparison, especially batch 7 versus batch 4.
- **The initial expectation that S2 would provide the overall optimum was contradicted as an optimization claim.** S2 did provide feasible morphology, but the highest observed recoveries came from the C0/S1 staged processes in batches 11 and 12. The narrower claim that S2 is comparatively forgiving for morphology remains consistent with the observations.
- **A strong claim that four extra 250 K stages improve recovery is unsupported and weakly contradicted by resolution limits.** Batch 12 was numerically highest, but it was statistically indistinguishable from batch 11 on recovery and fines.

### Still untested or only interpretive

- **Staged cooling as the cause of the batch-11 morphology improvement remains confounded.** Batch 9 used C1/S1 with direct cooling, whereas batch 11 used C0/S1 with staged cooling. Their fines differed greatly—0.483 versus 0.218—but catalyst and reaction composition also changed.
- **Reaction–crystallization coupling is supported only by correlation.** In the fixed-S2 catalyst series, better selectivity accompanied better recovery, but no experiment crystallized identical isolated feeds containing controlled impurity levels. Impurity-mediated nucleation, solubility changes, and surface poisoning therefore remain plausible rather than demonstrated mechanisms.
- **The proposed supersaturation, nucleation, and growth equations are useful interpretations, not fitted laws.** No concentration, solubility, or nucleation-rate measurements were made.
- **The claim that reheating would anneal fines while sacrificing some recovery was wholly untested in the campaign.** It was used only as a mechanistic basis for held-out prediction Q08.

## 2. One additional experiment

I would run a **matched C0/S1 direct-cooling control for batch 11**. I would copy batch 11’s reagent, solvent, catalyst, reaction, quench, seed charge, total crystallization duration, filtration, and assay, but replace its 320→300→280→260→250 K sequence with immediate cooling to 250 K followed by the same total residence time at 250 K. A non-destructive particle-size reading shortly after the plunge and another immediately before filtration would be included if permitted within the single experiment.

This experiment would distinguish three explanations:

1. **Staged-supersaturation explanation:** Immediate cooling should cause a nucleation burst, producing substantially higher fines and smaller particles than batch 11. Recovery could be similar or somewhat higher because the material spends longer at 250 K.
2. **Material-combination explanation:** If C0/S1 alone caused the good result, the direct-cooled control should retain approximately batch-11 recovery and morphology despite the changed path.
3. **Cold-exposure/equilibrium explanation:** If final temperature and accumulated cold time dominate, direct cooling should give equal or higher recovery without a major fines penalty; this would weaken the proposed history-dependent nucleation mechanism.

The most diagnostic outcome would be similar recovery but a large early and final fines increase in the direct-cooled control. Conversely, final fines near batch 11’s 0.218 would argue that the earlier batch-9 comparison was mainly confounded by catalyst or feed composition.

## 3. Underused observation and least-reliable prediction

The **batch-1 intermediate HPLC observation** was used least effectively. Before crystallization it already showed conversion near 1.0, yield about 0.574, selectivity about 0.580, and byproduct signal about 0.311. The final assay retained very similar reaction metrics while adding crystal outcomes. Explicitly comparing those readings would have strengthened the claim that reaction chemistry was essentially complete before crystallization and that subsequent score changes arose mainly from solid formation and separation. The mechanism report instead relied mostly on final-assay cross-batch comparisons.

The **least reliable held-out prediction is Q08**. It combines two major extrapolations absent from the campaign: a low-charge S0 feed near an unknown solubility threshold and a 315 K reheating/278 K recooling cycle. Its predicted balance—lower recovery but larger particles and fewer fines—depends on how much solid dissolves at 315 K, whether seeds survive, and whether one hour of recooling is sufficient for regrowth. None of those quantities was measured. Q08 is therefore less reliable than predictions involving only cooling-rate, seed, or residence-time changes already bracketed by campaign experience.
