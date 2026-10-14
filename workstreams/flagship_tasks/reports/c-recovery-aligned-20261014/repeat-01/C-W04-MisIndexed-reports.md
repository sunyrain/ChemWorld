# C-W04-MisIndexed — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

## Mechanistic account

### Recommended process and observed result
The sealed recommendation is **batch 12**: 0.04 mol limiting reagent and 0.005 mol catalyst C1 in 0.08 L solvent S2; heat at 347.5 K for 3,600 s with 400 rpm agitation; add 0.05 g seed; cool to 250 K over 14,400 s; age for 7,200 s at 200 rpm; then filter. Its final assay gave seed-excluded crystal yield **0.454**, purity **0.997**, fines fraction below 20 µm **0.378**, and normalized crystal size **0.103** (approximately 25.6 µm d50). Thus it met both specifications with the highest observed qualifying recovery.

### Reaction mechanism and catalyst effects
A useful empirical decomposition is

**Y_rxn ≈ X·S_eff**

where X is conversion and S_eff is an effective target selectivity, and

**Y_cr = n(target in isolated solid, excluding seed)/n(initial reagent) ≈ Y_rxn·f_capture.**

The measurements approximately follow the first relationship, allowing for assay noise and the benchmark’s effective selectivity definition. Conversion was nearly complete in the productive runs, so target formation was governed mainly by selectivity and degradation rather than residual reagent.

At the common 350 K/3,600 s reaction and the same S2 crystallization program, the catalyst screen showed:

- **Batch 2, C0:** reaction yield 0.483; crystal yield 0.412; purity 0.982; fines 0.423.
- **Batch 3, C1:** reaction yield 0.513; crystal yield 0.437; purity 0.992; fines 0.367.
- **Batch 4, C2:** reaction yield 0.436; crystal yield 0.387; purity 1.000; fines 0.399.
- **Batch 5, C3:** reaction yield 0.502; crystal yield 0.430; purity 0.977; fines 0.384.

**Observation:** C1 gave the highest reaction and qualifying crystal yields in this comparison, with C3 close behind. **Interpretation:** C1 had the best realized balance of target-forming activity and selectivity in this world, while C2’s high conversion did not translate into comparable target production. This supports, but does not prove, a catalyst-specific branching between target and byproduct pathways. Each catalyst was tested only once under the matched program, so small C1–C3 differences remain uncertain.

### Solvent effects
The nominal dossier suggested that S2 should combine low solubility, relatively rapid crystal growth, reduced nucleation, and low impurity occlusion. The experiments broadly supported its quality advantage.

With C1 at 350 K, **batch 3 using S2** gave crystal yield 0.437, purity 0.992, and fines 0.367. Under a closely related held process, **batch 9 using S3** gave a higher numerical crystal yield of 0.455 but purity 0.976 and fines 0.551. Removing the post-cooling aging step did not solve the S3 morphology problem: **batch 10** gave yield 0.457, purity 0.972, and fines 0.561.

**Interpretation:** S3 allowed strong apparent capture but promoted an excessive number of small particles, or failed to support sufficient ripening of them. S2 more reliably separated target from byproduct and supported a coarser number distribution. The very high crystal purity despite reaction selectivity near 0.5 shows that crystallization was strongly selective: much of the reaction byproduct remained in the liquid rather than entering the cake.

A qualitative solubility/capture relationship is

**f_capture ≈ 1 − C*V/n_target,**

where C* is the terminal target solubility and V the solvent volume. This explains why deeper cooling can improve recovery. It is incomplete because nucleation, seed surface, impurity adsorption, and cake-liquid retention also affect the isolated solid.

### Reaction–crystallization coupling
Reaction and crystallization were not independent stages. More target generated upstream increased supersaturation during cooling, affecting both recovery and the competition between nucleation and growth. A conventional qualitative description is

**J ∝ exp[−A/(ln S)²]**, while **G ∝ (S−1)^g**,

where J is nucleation rate, G is growth rate, and S is supersaturation. Seed surface can consume supersaturation by growth and thereby suppress secondary nucleation, but rapid accumulation of supersaturation can still create fines.

This coupling helps explain why a condition could have attractive reaction yield but fail the particle constraint. For example, **batch 7 at 340 K** had crystal yield 0.446 but fines 0.559, and **batch 8** reached yield 0.452 but fines 0.559. Conversely, **batch 11 at 345 K** combined essentially the same recovery, 0.446, with fines 0.398. The sharp numerical change should not be interpreted as a proven threshold at 345 K: batch-to-batch process variation was much larger than the stated instantaneous instrument noise.

For the final two S2/C1 batches, the inferred capture fractions were about 0.90: batch 11 had 0.446 crystal yield from 0.498 reaction yield, and batch 12 had 0.454 from 0.506. Batch 3 captured about 0.85. Thus both target formation and downstream capture contributed to the final improvement.

### Process-history dependence
The initial feasibility experiment, **batch 1**, used a hotter reaction near 371 K, only 0.02 g seed, cooling to 278 K over 7,200 s, and no extended aging. It gave substantial crystal yield (0.378) and excellent purity (0.987), but fines were 0.545 and therefore failed specification.

The revised program used 0.05 g seed, cooling to 250 K over 14,400 s, followed by agitated aging. **Batch 2** was the first clear qualifying result: yield 0.412 and fines 0.423. This supports the combined effect of more seed surface, deeper/slower cooling, and additional growth or ripening time. These variables were changed together, however, so their individual causal contributions were not isolated.

The 7,200 s `wait` after cooling also allowed the system to relax back toward ambient temperature rather than enforcing a strictly isothermal 250 K hold. Therefore the likely history includes cold precipitation followed by partial warming, dissolution–reprecipitation, and/or Ostwald ripening. An explicitly controlled cold hold is an untested alternative and might produce a different recovery–size balance.

### Revisions during the campaign
1. **Initial hypothesis:** C1/S2 would be favorable from the material dossier. Batch 1 confirmed recovery and purity feasibility but revealed fines as the binding constraint.
2. **First revision:** increase seed dose and use deeper, slower cooling plus aging. Batch 2 then met the fines limit.
3. **Catalyst revision:** matched batches 2–5 established C1 as the strongest observed catalyst rather than relying only on nominal activity.
4. **Temperature revision:** 330–340 K trials produced acceptable purity and recovery but unexpectedly high fines (batches 6–8). Results at 345 K and 347.5 K gave a better joint outcome (batches 11–12).
5. **Solvent alternative:** S3 was tested because it offered high numerical recovery, but batches 9 and 10 repeatedly failed the fines specification. S2 was retained.

### Remaining uncertainty and tradeoff
Purity was not the limiting quality attribute: qualifying S2 batches were generally near 0.98–1.00 purity. The unresolved tradeoff is between maximum recovery and particle-number quality. Some of the largest raw crystal yields—batches 9 and 10 at about 0.455–0.457—failed because fines exceeded 0.55. Batch 12 achieved nearly the same recovery while providing a sizeable observed fines margin.

The final-assay standard deviations were approximately 0.01 for crystal yield and purity and 0.018 for fines, but these describe measurement noise, not full process reproducibility. No exact replicate of batch 12 was performed, and the morphology variation among nominally similar S2 histories indicates meaningful process variance. Consequently, batch 12 is the highest observed qualifying process, not a proven global optimum. Untested alternatives include finer temperature spacing around 345–350 K, independently controlled cold aging, staged cooling, different seed-size distributions, and controlled antisolvent or solvent-mixture strategies.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.24 | 0.12 | 0.4 |
| Q01 | crystal_purity | 0.94 | 0.88 | 0.99 |
| Q01 | crystal_size | 0.24 | 0.14 | 0.36 |
| Q01 | crystal_yield | 0.34 | 0.24 | 0.44 |
| Q02 | crystal_fines_fraction | 0.17 | 0.07 | 0.31 |
| Q02 | crystal_purity | 0.97 | 0.92 | 1 |
| Q02 | crystal_size | 0.31 | 0.19 | 0.45 |
| Q02 | crystal_yield | 0.39 | 0.29 | 0.49 |
| Q03 | crystal_fines_fraction | 0.55 | 0.36 | 0.73 |
| Q03 | crystal_purity | 0.89 | 0.8 | 0.96 |
| Q03 | crystal_size | 0.15 | 0.07 | 0.27 |
| Q03 | crystal_yield | 0.25 | 0.15 | 0.36 |
| Q04 | crystal_fines_fraction | 0.32 | 0.17 | 0.5 |
| Q04 | crystal_purity | 0.91 | 0.83 | 0.97 |
| Q04 | crystal_size | 0.21 | 0.11 | 0.34 |
| Q04 | crystal_yield | 0.28 | 0.18 | 0.39 |
| Q05 | crystal_fines_fraction | 0.29 | 0.15 | 0.46 |
| Q05 | crystal_purity | 0.91 | 0.83 | 0.97 |
| Q05 | crystal_size | 0.23 | 0.13 | 0.36 |
| Q05 | crystal_yield | 0.27 | 0.17 | 0.38 |
| Q06 | crystal_fines_fraction | 0.53 | 0.34 | 0.71 |
| Q06 | crystal_purity | 0.87 | 0.76 | 0.95 |
| Q06 | crystal_size | 0.14 | 0.06 | 0.25 |
| Q06 | crystal_yield | 0.28 | 0.18 | 0.39 |
| Q07 | crystal_fines_fraction | 0.27 | 0.13 | 0.44 |
| Q07 | crystal_purity | 0.91 | 0.83 | 0.97 |
| Q07 | crystal_size | 0.24 | 0.14 | 0.37 |
| Q07 | crystal_yield | 0.28 | 0.18 | 0.39 |
| Q08 | crystal_fines_fraction | 0.18 | 0.07 | 0.34 |
| Q08 | crystal_purity | 0.94 | 0.87 | 0.99 |
| Q08 | crystal_size | 0.32 | 0.19 | 0.47 |
| Q08 | crystal_yield | 0.26 | 0.16 | 0.37 |
| Q09 | crystal_fines_fraction | 0.68 | 0.49 | 0.84 |
| Q09 | crystal_purity | 0.86 | 0.72 | 0.95 |
| Q09 | crystal_size | 0.035 | 0.015 | 0.075 |
| Q09 | crystal_yield | 0.035 | 0.005 | 0.1 |
| Q10 | crystal_fines_fraction | 0.47 | 0.29 | 0.65 |
| Q10 | crystal_purity | 0.9 | 0.8 | 0.97 |
| Q10 | crystal_size | 0.085 | 0.04 | 0.15 |
| Q10 | crystal_yield | 0.13 | 0.06 | 0.23 |
| Q11 | crystal_fines_fraction | 0.28 | 0.14 | 0.45 |
| Q11 | crystal_purity | 0.91 | 0.83 | 0.97 |
| Q11 | crystal_size | 0.23 | 0.13 | 0.36 |
| Q11 | crystal_yield | 0.28 | 0.18 | 0.39 |
| Q12 | crystal_fines_fraction | 0.46 | 0.28 | 0.64 |
| Q12 | crystal_purity | 0.86 | 0.77 | 0.94 |
| Q12 | crystal_size | 0.16 | 0.08 | 0.28 |
| Q12 | crystal_yield | 0.34 | 0.23 | 0.45 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

All recipes add seed, so particles are expected even where seed-excluded product recovery is small. Q01–Q02: S3 is predicted to give greater capture, purity and growth with fewer fines than S1, although S1 has the stronger nominal reaction activity. Q03–Q04: increasing seed from 0.001 to 0.045 g should provide enough growth surface to suppress secondary nucleation, modestly raise recovery and lower fines. Q05–Q06: gradual staged cooling should favor growth, whereas the rapid drop is expected to create a nucleation burst; the long cold residence narrows the yield difference but may not fully erase the fines penalty. Q07–Q08: the 315 K thermal cycle should preferentially dissolve fines and permit regrowth on recooling, improving size, purity and fines at a small recovery cost. Q09–Q10: two hours of continued growth at 292 K should substantially increase seed-excluded recovery and particle size relative to immediate filtration, though feasibility remains borderline. Q11–Q12: doubled reagent loading increases supersaturation and capture but halves the catalyst-to-reagent ratio, so fractional recovery rises only moderately while purity, size and fines worsen. Intervals are deliberately broad because these recipes use S0/S1, much lower scale and catalyst loading, very long staged histories, and thermal cycling not directly represented in the campaign; several feasibility calls lie close to the fines or purity limits.

## K2

## 1. Status of the main claims

### Supported by direct observations
- **C1 was the best observed catalyst in the matched screen.** At 350 K with S2 and the common crystallization history, batch 3 (C1) gave reaction yield 0.513 and qualifying crystal yield 0.437, versus 0.412 for C0 (batch 2), 0.387 for C2 (batch 4), and 0.430 for C3 (batch 5). Interpreting this as superior target-pathway activity is reasonable, but each catalyst had only one matched run.
- **Crystallization strongly rejected reaction impurities.** Reaction selectivity was only about 0.45–0.52 in batches 2–5 and 11–12, whereas isolated-crystal purity was approximately 0.98–1.00. The purity contrast is observed directly; preferential exclusion of byproduct into mother liquor is the interpretation.
- **S3 carried a fines penalty under the tested histories.** S3 batches 9 and 10 had high crystal yields, 0.455–0.457, but fines of 0.551–0.561. The related S2 batch 3 had yield 0.437 and fines 0.367. Thus S3’s failure was reproducible across held and unheld variants, although a fully matched replicated solvent comparison was not performed.
- **The 345–347.5 K region gave the best observed joint outcome for C1/S2.** Batch 11 at 345 K gave yield 0.446, purity 0.996 and fines 0.398; batch 12 at 347.5 K gave 0.454, 0.997 and 0.378. By comparison, batches 6 and 7 at 330 and 340 K had fines of 0.641 and 0.559. These are direct observations, but calling the region a mechanistic optimum remains an interpretation because exact replicates were absent.

### Contradicted or narrowed
- **A simple universal claim that more seed plus slower/deeper cooling necessarily suppresses fines is contradicted.** The revised package worked in batches 2–5 and 11–12, but nominally similar downstream treatment still produced excessive fines in batches 6–8. The defensible claim is therefore conditional: seeding and slow cooling can help, but morphology also depends on upstream state and uncontrolled batch variation.
- **A simple recovery–quality tradeoff is incomplete.** S3 batches 9–10 supported the expected tradeoff—high recovery with excessive fines—but batch 12 achieved nearly the same recovery with much better fines. Material identity and process history can shift the frontier rather than merely move along one fixed tradeoff.

### Still untested
- The isolated causal effect of seed dose: batch 1 versus later batches changed seed, endpoint temperature, cooling duration and aging together.
- Whether the post-cooling benefit arose from time, warming toward ambient, Ostwald ripening, agglomeration or another mechanism.
- Exact reproducibility of batch 12 and the continuous temperature response around 345–350 K.
- Explicit isothermal holding at 250 K, seed-size distribution, staged seeding, solvent mixtures, antisolvent addition and concentration/loading effects.
- The proposed nucleation and growth equations were qualitative organizing models, not fitted laws.

## 2. One additional experiment

I would repeat the complete batch-12 process but add non-destructive particle-size measurements **immediately after reaching 250 K and again after the 7,200 s post-cooling wait**, followed by the same filtration and final assay. The underlying operating recipe would otherwise remain unchanged.

This would distinguish three explanations:

1. **Post-cooling dissolution–reprecipitation or ripening:** d50 should increase and fines should decrease during the wait, possibly with a small loss or redistribution of recovered product as the system warms.
2. **Morphology fixed mainly during slow cooling:** the two particle measurements should be similar; final morphology would then be attributed chiefly to the cooling trajectory and upstream supersaturation.
3. **Secondary nucleation or attrition during aging:** fines should increase, or d50 should decrease, during the wait despite acceptable morphology at 250 K.

The experiment would also test whether batch 12’s favorable morphology is reproducible. A repeat near yield 0.45, purity near 1.0 and fines near 0.38 would strengthen the process claim; a large deviation would indicate that process variance, rather than the 347.5 K condition alone, explains much of the apparent optimum.

## 3. Underused observation and least reliable prediction

The account used the **intermediate particle-size measurements** least effectively. For example, batch 2 measured fines of about 0.405 and normalized size 0.088 before filtration, while its final assay gave 0.423 and 0.108. That pairing could have been used more explicitly to show that morphology was largely established before filtration and to separate process evolution from instrument/filter differences. Similar intermediate measurements in later batches could have supported a more rigorous measurement-to-final comparison.

The least reliable held-out prediction is **Q09**. It filters only 60 s after cooling to 292 K, uses a large seed mass relative to the 0.004 mol reagent charge, and lies far outside the campaign’s long crystallization histories. Seed particles are certainly present, but the requested yield excludes seed while size and fines can be dominated by the seed population. Consequently, particles_present is easier to predict than seed-excluded recovery, purity or fines. The sealed Q09 numerical prediction therefore carries substantial structural uncertainty beyond its stated interval. Q08’s untested thermal cycle is also highly extrapolative, but Q09 is more problematic because it approaches the seed-dominated, near-zero-product regime.
