# C-W02-Aligned — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

## Mechanistic account

### 1. Reaction–crystallization coupling
The process contains two distinct yield stages. A useful bookkeeping approximation is

**target formed ≈ n(reagent) × conversion × selectivity**,  
**isolated target ≈ target formed × crystal recovery**.

Here, crystal recovery is specifically the seed-excluded recovered target divided by target present before separation. It is therefore not the overall yield from charged reagent. This distinction matters: batch 11 had the best crystal recovery (0.679), reaction yield (0.891), and selectivity (0.911), but used only 0.01 mol reagent. Its approximate isolated target fraction of charge was 0.891×0.679≈0.605, yet its absolute output could still be lower than that of a 0.04 mol batch. The selected objective favored fractional recovery rather than throughput.

High crystal purity despite only moderate reaction selectivity shows strong impurity rejection during crystallization. For example, batch 1 had reaction selectivity 0.592 but crystal purity 0.992, and batch 6 had selectivity 0.506 but purity reported as 1.000. Thus reaction impurities largely remained in the mother liquor, although their presence may still have influenced nucleation, growth, and recovery.

### 2. Material effects
The nominal dossier suggested S2 should be favorable because of low solubility, low nucleation tendency, high growth, and low impurity occlusion. S2 did indeed support substantial recovery and excellent purity: batches 1–4 gave recoveries of 0.503–0.549 with purities of 0.989–1.000. However, the empirical campaign revised the solvent ranking. Under the tested 0.04 mol conditions, S1 gave 0.590 recovery in batch 5, compared with 0.549 for the analogous unseeded S2 batch 4 and 0.460 for S3 batch 6. These are numerical comparisons rather than isolated solvent effects because reaction histories and stochastic assay errors remain potential confounds.

At low reagent loading, both S1 and S2 performed well. Batch 11 (S1, 0.01 mol reagent) reached 0.679 recovery, 0.999 purity, and 0.911 reaction selectivity. Batch 12 (S2, 0.01 mol) reached 0.662 recovery, 1.000 purity, and 0.845 selectivity. This supports a loading-dependent improvement, plausibly because lower impurity concentration and lower supersaturation reduced occlusion and target loss. It does not establish S1 as intrinsically superior in every regime.

Catalyst C1 was used throughout after the initial prior-based choice. Consequently, the campaign provides no experimental catalyst ranking; effects of C0, C2, and C3 remain untested alternatives. Likewise, the apparent improvement from batch 1 at 370 K for 3600 s to later 350 K/2400 s reactions is consistent with less degradation, but it is confounded with crystallization history and cannot be assigned solely to temperature or time.

### 3. Process-history dependence
The initial hypothesis was that seeding, slow cooling, and growth holding would suppress fines. The experiments rejected that hypothesis over the tested range:

- Batch 1 used 0.05 g seed, cooling to 260 K, and a 14,400 s hold; its fines fraction was 0.997.
- Batch 2 used slower/deeper cooling to 250 K and a hold; fines were 1.000.
- Batch 4 omitted seed but still gave fines of 1.000, so the fine population was not simply imported seed.
- Batch 3 used crystallization at 280 K, partial reheating to 300 K, and recooling to 250 K. Recovery remained 0.534, but the final size index fell to 0.038 and fines remained 0.995. Partial dissolution/Ostwald-ripening behavior therefore did not dominate under that cycle.
- Batch 7 filtered, resuspended in fresh S1, reheated to 290 K, and recrystallized. Recovery remained good at 0.580, but fines were still 0.987. A simple solvent wash/recrystallization was insufficient.
- Batch 8 stopped at the much warmer endpoint of 300 K and still had 0.512 recovery and 0.987 fines. Deep cooling alone was therefore not the sole source of fines.
- In batch 9, 1 microgram of seed did not create an effective population and the first crystallization attempt failed its population precondition. Raising the cumulative seed to 0.005 g enabled crystallization, demonstrating a practical seed-population threshold, but final fines were still 1.000.
- Batch 10 used 0.05 g seed followed by six long holds at 280 K; its recovery was 0.560 and fines were 1.000. Batch 12 used eight long holds at 250 K and attained the largest final-assay size index, 0.084, but fines were again 1.000.

The persistence of fines under seeded, unseeded, warm-endpoint, deep-cooled, thermally cycled, washed, and prolonged-hold histories suggests rapid secondary nucleation and/or agitation-induced attrition. Long residence alone did not shift enough of the number distribution into the coarse class. Because every hold used at least 100 rpm, an untested alternative is that even the minimum permitted agitation maintained or generated a large fine population.

### 4. Particle metrics and uncertainty
The operative quality measure is

**F20 = number of particles with diameter <20 µm / total particle number**,  
with compliance requiring F20≤0.50.

The reported size channel is approximately min(d50/250 µm,1). Independent noise on size and fines can make the two channels appear inconsistent. For example, batch 12’s size index of 0.084 corresponds nominally to d50≈21 µm, yet its fines estimate was 1.000. The final-assay size uncertainty alone corresponds to several micrometres, and the independently noisy channel estimates need not preserve exact distributional identities. Nevertheless, the fines failure is not marginal: final estimates were approximately 0.987–1.000 across all tested histories, and in-process particle measurements independently showed similarly high values. The conclusion that no batch met F20≤0.50 is therefore robust despite uncertainty in the exact d50.

Purity was consistently well above 0.80, so the unresolved tradeoff was not purity versus recovery. It was recovery versus acceptable number-based particle quality. Batch 11 maximized observed recovery at 0.679 and purity at 0.999 but had F20=0.993. Batch 12 delivered a somewhat lower recovery of 0.662 and a larger reported size but F20=1.000. Neither is compliant.

### 5. Revisions and remaining alternatives
The study began with S2 and a seeded slow-cooling mechanism as the leading hypothesis. Evidence revised this view in three ways: S1 was at least competitive and produced the highest recovery; ordinary seeding/slow cooling did not control fines; and low reagent loading became the strongest late-stage correlate of high selectivity and recovery. Because the low-loading comparison was introduced only in batches 11–12, its causal contribution is not fully separated from solvent, seed, and hold history.

The recommended batch remains batch 11 because it had the campaign-high observed crystal recovery, not because it satisfied all specifications. Further research should first replicate the loading effect and factorially vary loading, seed dose, and endpoint. Qualitatively different particle-control operations—classification or fines removal, deliberate agglomeration, substantially gentler mixing, staged supersaturation control, or a different solvent/antisolvent composition—remain untested. These alternatives are mechanistic proposals, not demonstrated outcomes.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.12 | 0.05 | 0.24 |
| Q01 | crystal_purity | 0.97 | 0.93 | 0.99 |
| Q01 | crystal_size | 0.28 | 0.2 | 0.36 |
| Q01 | crystal_yield | 0.7 | 0.62 | 0.78 |
| Q02 | crystal_fines_fraction | 0.3 | 0.16 | 0.47 |
| Q02 | crystal_purity | 0.93 | 0.87 | 0.97 |
| Q02 | crystal_size | 0.2 | 0.12 | 0.29 |
| Q02 | crystal_yield | 0.55 | 0.43 | 0.65 |
| Q03 | crystal_fines_fraction | 0.52 | 0.34 | 0.72 |
| Q03 | crystal_purity | 0.88 | 0.8 | 0.94 |
| Q03 | crystal_size | 0.16 | 0.08 | 0.25 |
| Q03 | crystal_yield | 0.5 | 0.38 | 0.59 |
| Q04 | crystal_fines_fraction | 0.34 | 0.19 | 0.52 |
| Q04 | crystal_purity | 0.9 | 0.82 | 0.95 |
| Q04 | crystal_size | 0.21 | 0.13 | 0.31 |
| Q04 | crystal_yield | 0.57 | 0.46 | 0.67 |
| Q05 | crystal_fines_fraction | 0.3 | 0.16 | 0.48 |
| Q05 | crystal_purity | 0.9 | 0.82 | 0.95 |
| Q05 | crystal_size | 0.22 | 0.14 | 0.32 |
| Q05 | crystal_yield | 0.58 | 0.47 | 0.68 |
| Q06 | crystal_fines_fraction | 0.55 | 0.38 | 0.72 |
| Q06 | crystal_purity | 0.88 | 0.8 | 0.94 |
| Q06 | crystal_size | 0.16 | 0.09 | 0.24 |
| Q06 | crystal_yield | 0.62 | 0.51 | 0.72 |
| Q07 | crystal_fines_fraction | 0.27 | 0.14 | 0.44 |
| Q07 | crystal_purity | 0.91 | 0.84 | 0.96 |
| Q07 | crystal_size | 0.23 | 0.15 | 0.33 |
| Q07 | crystal_yield | 0.6 | 0.49 | 0.7 |
| Q08 | crystal_fines_fraction | 0.43 | 0.24 | 0.64 |
| Q08 | crystal_purity | 0.92 | 0.84 | 0.97 |
| Q08 | crystal_size | 0.18 | 0.09 | 0.29 |
| Q08 | crystal_yield | 0.52 | 0.39 | 0.64 |
| Q09 | crystal_fines_fraction | 0.92 | 0.76 | 1 |
| Q09 | crystal_purity | 0.9 | 0.8 | 0.96 |
| Q09 | crystal_size | 0.05 | 0.01 | 0.11 |
| Q09 | crystal_yield | 0.03 | 0.005 | 0.09 |
| Q10 | crystal_fines_fraction | 0.75 | 0.54 | 0.92 |
| Q10 | crystal_purity | 0.9 | 0.81 | 0.96 |
| Q10 | crystal_size | 0.08 | 0.03 | 0.16 |
| Q10 | crystal_yield | 0.18 | 0.1 | 0.28 |
| Q11 | crystal_fines_fraction | 0.31 | 0.16 | 0.49 |
| Q11 | crystal_purity | 0.9 | 0.82 | 0.95 |
| Q11 | crystal_size | 0.22 | 0.14 | 0.32 |
| Q11 | crystal_yield | 0.56 | 0.45 | 0.67 |
| Q12 | crystal_fines_fraction | 0.58 | 0.4 | 0.75 |
| Q12 | crystal_purity | 0.86 | 0.77 | 0.93 |
| Q12 | crystal_size | 0.14 | 0.07 | 0.23 |
| Q12 | crystal_yield | 0.67 | 0.56 | 0.77 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

Q01–Q02: S1 is expected to outperform S3 through lower solubility, lower nucleation tendency, faster growth and less impurity occlusion. Q03–Q04: the larger seed charge should provide enough growth surface to control supersaturation; the 0.001 g case is near an uncertain effective-seed threshold and is assigned more fines. Q05–Q06: gradual staged cooling should suppress burst nucleation, whereas the rapid drop followed by isothermal growth should recover slightly more product but retain many fines. Q07–Q08: the terminal hold should preserve the coarse population; reheating to 315 K may dissolve crystals, but rapid recooling can regenerate fines, so the thermal-cycle prediction is lower and notably less certain. Q09–Q10: seeds make particles likely in both, but 60 seconds at 292 K should recover little seed-excluded product; the added hold increases recovery and growth without being long or cold enough to assure feasible fines. Q11–Q12: doubling reagent loading should raise supersaturation and fractional recovery but also secondary nucleation and impurity incorporation, producing a recovery–quality tradeoff. Intervals are deliberately broad because these recipes extrapolate far beyond the campaign in cooling duration, staging, S0 use and concentration; prior assays also showed independently noisy and occasionally inconsistent size/fines channels.

## K2

## 1. Status of the main claims

### Supported by direct observations
- **Crystallization strongly rejected reaction impurities.** Final crystal purity was about 0.98–1.00 even when reaction selectivity was only moderate. Examples include batch 1 (selectivity 0.592, purity 0.992) and batch 6 (0.506, reported purity 1.000). Interpreting this as preferential retention of impurities in the mother liquor is reasonable, although their exact fate was not measured directly.
- **The tested processes had a persistent fines problem, not a purity problem.** Seeded cooling (batches 1–2), thermal cycling (batch 3), no seeding (batch 4), solvent resuspension/recrystallization (batch 7), a warm endpoint (batch 8), reduced seed dose (batch 9), and prolonged holds (batches 10 and 12) all ended with fines estimates near 0.99–1.00. No completed batch met fines ≤0.50, whereas all met purity ≥0.80.
- **Low-loading batches were the strongest fractional performers observed.** Batch 11, using 0.01 mol reagent in S1, gave the campaign-high crystal recovery of 0.679, selectivity 0.911 and purity 0.999. Batch 12 independently gave recovery 0.662 and selectivity 0.845 at the same low charge in S2. This directly supports an association, not yet a causal loading law.
- **A minimum effective seed population existed.** In batch 9, 0.000001 g seed did not satisfy the crystallization-population precondition; increasing the cumulative dose to 0.005 g allowed crystallization.

### Contradicted or substantially weakened
- **The initial claim that ordinary seeding, slow cooling and holding would suppress fines was contradicted in the tested range.** Batches 1, 2, 10 and 12 retained essentially all-number fines despite these measures.
- **Simple thermal ripening was not effective.** Batch 3’s reheat/recool cycle did not improve fines and produced a smaller final size estimate than the nearby baselines. Batch 7’s post-filtration resuspension, heating and recrystallization also left fines at 0.987. These results contradict a strong version of the hypothesis that modest reheating alone selectively removes fines.
- **The nominal expectation that S2 would clearly dominate was weakened.** S2 produced good purity and recovery, but S1 gave higher observed recovery in the comparable high-loading region (batch 5 versus batch 4) and the campaign maximum in batch 11. Because these were not perfectly matched solvent experiments, this does not prove universal S1 superiority.

### Still untested or unresolved
- A causal **reagent-loading effect** remains unresolved because batches 11–12 also differed from earlier batches in seed and hold history.
- **Catalyst identity** was not screened; all completed batches used C1.
- Secondary nucleation and agitation-induced attrition are interpretations of the fines persistence, not directly observed mechanisms. Substantially gentler mixing, controlled antisolvent addition, agglomeration, and particle classification were not tested.
- The effect of staged, very slow cooling using repeated `cool_crystallize` operations was not tested during the campaign; long `wait` operations are not necessarily mechanistically equivalent.
- Absolute throughput was not optimized. A high fractional recovery at 0.01 mol charge can still yield less isolated mass than a lower-recovery 0.04 mol process.

## 2. One additional experiment

I would run an exact high-loading counterpart to batch 11: S1 at the same solvent volume, C1 charge, reaction temperature/time, 0.05 g seed, cooling endpoint and no-hold isolation history, changing only reagent from 0.01 to 0.04 mol. I would include an in-process particle-size measurement immediately before filtration and the final assay.

This single matched experiment would distinguish two explanations:

1. **True loading mechanism:** lower loading reduces impurity burden and secondary nucleation, improving reaction selectivity, fractional crystal recovery and particle quality.
2. **Confounding/noise explanation:** batch 11 appeared superior mainly because its seed, hold history or assay realization differed from earlier high-loading batches.

If the loading mechanism is correct, the 0.04 mol experiment should show lower selectivity and fractional recovery than batch 11, more fines, and possibly lower purity, while still producing more absolute isolated target. If loading was not causal, its recovery and selectivity should remain near batch 11 within uncertainty, and particle outcomes should not deteriorate systematically. A large recovery change without a corresponding pre-filtration particle change would instead implicate solubility or separation rather than nucleation.

## 3. Least effectively used observation and least reliable prediction

The account used **batch 7’s unusually low final byproduct and degradation signals** least effectively. After filtration, resuspension and recrystallization, its byproduct signal was about 0.024 and degradation warning about 0.006, far below many other batches, yet selectivity was only 0.576 and fines remained 0.987. I focused on its failure to improve particles but did not fully explore whether the wash selectively removed particular impurities or whether reaction-channel estimates after phase processing were not directly comparable with earlier liquid-phase measurements. That ambiguity limits mechanistic interpretation.

The least reliable held-out prediction is **Q03**. It combines untested solvent S0 with a 0.001 g seed dose close to the only observed seed-population discontinuity. If that dose is below the effective threshold, particles might not form as predicted and every conditional size estimate would change qualitatively. If it is effective, the exceptionally long staged cooling could give much coarser particles than inferred from the campaign’s single-step cooling histories. Thus both `particles_present` and the fines/size intervals rest on extrapolation across a threshold, making Q03 less reliable than predictions based on clearly effective seed charges.
