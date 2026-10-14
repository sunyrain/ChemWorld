# C-W03-Aligned — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

## Mechanistic account

### 1. Observed process landscape
All batches used catalyst C1, so this campaign provides no experimental comparison among catalysts. The catalyst dossier suggested activity differences, but any catalyst-specific mechanism remains untested. C1 nevertheless gave essentially complete reagent conversion in most tested conditions; product selectivity, crystallization, and particle quality—not conversion—were the main limitations.

At full loading (0.04 mol reagent in about 0.075 L solvent), S2 and S1 produced high-purity crystals with recoveries around 0.44–0.47, but almost every particle population was dominated by sub-20 µm fines. Examples are batch 3 (S2: crystal yield 0.441, purity 0.988, fines 0.995), batch 4 (S2: 0.456, 1.000, 1.000), and batch 6 (S1: 0.465, 1.000, 1.000). Thus, purity was not the binding constraint in this region; particle-number distribution was.

S3 moderated the tradeoff but did not solve it. Batch 8 at 295 K gave lower recovery, 0.313, and fines 0.846. Batches 9–11 gave recoveries of approximately 0.280–0.305 and fines of 0.853–1.000. These observations are consistent with the dossier’s characterization of S3 as more soluble and less favorable for growth than S2, although solvent, endpoint, and history were not fully factorially separated.

The recommended batch 12 used S2 at reduced loading: 0.02 mol reagent in 0.08 L solvent, C1, a 370 K reaction, quench, 0.05 g seed, slow cooling to 280 K, and six extended cold holds. Its final assay gave crystal yield 0.4712, purity 0.9961, fines 0.4366, size index 0.0973, and CSD-quality index 0.6936. The size index corresponds to a number-weighted d50 of about 24 µm under the published scaling. It was the only batch satisfying both purity ≥0.80 and fines ≤0.50.

### 2. Reaction–crystallization coupling
A useful approximate decomposition is

Y_crystal = n_target,solid / n_reagent,0 ≈ X · S_rxn · F_cryst,

where X is conversion, S_rxn is chemical selectivity to target, and F_cryst is the fraction of formed target recovered as seed-excluded solid. This is conceptual rather than an independently calibrated kinetic model.

For batch 12, the assay liquid-product yield was about 0.676 and crystal yield was 0.471, suggesting an apparent solid recovery of roughly 0.70 of the formed target. By comparison, batch 1 had liquid-product yield about 0.572 and crystal yield about 0.472, implying greater precipitation of its available product but an unacceptable fines fraction of 0.997. Hence maximizing precipitation alone was not sufficient: the mode of precipitation determined whether the recovered material met specification.

Loading also appeared to affect the reaction. Batch 12 showed selectivity about 0.671 and liquid-product yield about 0.676, whereas full-loading S2 batches at 370 K commonly gave yields around 0.57–0.58 and selectivity around 0.57–0.60. This may indicate concentration-dependent side-product formation, but batch 12 was not replicated, so a fixed batch residual or history effect remains an alternative.

The lower-temperature reaction in batch 2 (340 K for 7200 s) produced liquid-product yield about 0.422, versus roughly 0.57 in several 370 K S2 batches. Temperature and residence time were changed together, so this does not identify an activation law; it only supports using the tested 370 K history within this campaign.

### 3. Crystallization mechanism and material effects
The results are consistent with competition between growth on existing crystals and secondary or homogeneous nucleation. A conventional representation is

σ = C/C*(T,solvent) − 1,

J ≈ J0 exp[−B/(ln(1+σ))²],

G ≈ kg(C − C*)^g,

where C* is solubility, J is nucleation rate, and G is crystal-growth rate. These equations were not fitted; they organize the observations.

At full loading, cooling apparently crossed into a high-nucleation regime. In batch 2, S2 held at 300 K gave large, essentially fines-free seed crystals but zero seed-excluded recovery. Cooling otherwise similar S2 material to 290 K in batch 3 suddenly gave 0.441 recovery but fines 0.995. This sharp change is consistent with a supersaturation threshold: above it, little new product crystallized; below it, rapid nucleation generated many small particles.

S2’s nominal low solubility, high growth tendency, and low impurity occlusion explain its excellent purity and recovery potential. However, low solubility at full loading also made deep cooling prone to excessive supersaturation. S1 behaved similarly in batches 6 and 7. S3’s greater nominal solubility plausibly reduced the driving force and lowered fines somewhat, but it also left more product in solution and reduced recovery.

Batch 12 likely succeeded because dilution lowered absolute supersaturation during the trajectory, while cooling to 280 K restored enough thermodynamic driving force for useful recovery. Slow cooling, pre-existing seed surface, and long holds then allowed more material to be incorporated by growth rather than appearing as a large population of new fines. This explanation is plausible but not uniquely established because loading, solvent volume, cold endpoint, and total hold time changed together.

### 4. Process-history dependence and revised hypotheses
The initial hypothesis was that S2, slow cooling, and modest seeding would jointly produce high recovery and coarse crystals. The material choice was supported for purity and recovery, but slow cooling and ordinary seeding were insufficient at full loading.

Several attempted revisions were rejected in their tested ranges:

- Increasing S2 seed from 0.005 g in batch 3 to 0.05 g in batch 4 did not prevent near-total fines.
- Staging batch 4 through 300 K before 290 K likewise did not control nucleation.
- Partial reheating and recooling in batch 5 left fines at 1.000, so that thermal cycle did not produce effective Ostwald ripening.
- Raising the S3 seed dose from 0.05 g in batch 8 to a cumulative 1.0 g in batch 10 left fines near 0.85–0.87 and recovery near 0.30.
- Ten extended S3 holds in batch 11 did not materially improve particle quality relative to batches 8 and 10.

These failures indicate that once the full-loading slurry entered the fine-particle regime, additional seed mass or elapsed time alone could not reverse the resulting number distribution. The successful revision was therefore upstream: reduce concentration before controlling the cold-growth history.

Endpoint temperature was not independently causal. For example, S3 batch 9 at 300 K was worse in fines than batch 8 at 295 K. That nonmonotonic result could reflect stochastic nucleation, process variability, or interactions with the precise history. It cautions against treating final temperature as the sole control variable.

### 5. Uncertainty and unresolved tradeoff
Final-assay noise scales were approximately 0.01 for crystal yield, 0.01 for purity, and 0.018 for fines, with additional process uncertainty not quantified. Consequently, the recovery difference between batch 12 (0.4712) and nonqualifying batch 1 (0.4717) is not evidence of a real difference. The decisive distinction is specification compliance, not their nominal recovery ordering. Batch 12’s purity has a very large margin, whereas its fines margin is only about 0.063 below the limit; analytical noise alone is smaller than that margin, but unmeasured batch-to-batch nucleation variability could be important.

A quality/recovery tradeoff remains mechanistically unresolved. Warm S2 conditions preserved large particles but yielded essentially no new solid in batch 2. Deep cooling at full loading recovered substantial product but created almost all fines. Dilution plus colder, prolonged growth in batch 12 escaped that tradeoff once, but it has not been replicated. Untested alternatives include intermediate loadings, a temperature ramp optimized around the nucleation boundary, controlled antisolvent addition, lower-shear histories, and catalyst changes that improve upstream selectivity.

Therefore, the strongest supported account is that batch 12 combined favorable S2 purity/growth behavior with reduced supersaturation from dilution and a long seeded cold-growth history. Its performance is compelling within the completed campaign, while reproducibility and the individual causal contributions of loading, endpoint temperature, and hold duration remain open.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.12 | 0.03 | 0.3 |
| Q01 | crystal_purity | 0.982 | 0.94 | 1 |
| Q01 | crystal_size | 0.36 | 0.22 | 0.5 |
| Q01 | crystal_yield | 0.245 | 0.14 | 0.35 |
| Q02 | crystal_fines_fraction | 0.28 | 0.1 | 0.5 |
| Q02 | crystal_purity | 0.955 | 0.88 | 0.99 |
| Q02 | crystal_size | 0.27 | 0.14 | 0.41 |
| Q02 | crystal_yield | 0.135 | 0.05 | 0.24 |
| Q03 | crystal_fines_fraction | 0.72 | 0.45 | 0.93 |
| Q03 | crystal_purity | 0.9 | 0.78 | 0.98 |
| Q03 | crystal_size | 0.08 | 0.03 | 0.17 |
| Q03 | crystal_yield | 0.065 | 0 | 0.16 |
| Q04 | crystal_fines_fraction | 0.32 | 0.12 | 0.56 |
| Q04 | crystal_purity | 0.93 | 0.82 | 0.99 |
| Q04 | crystal_size | 0.23 | 0.11 | 0.38 |
| Q04 | crystal_yield | 0.08 | 0 | 0.18 |
| Q05 | crystal_fines_fraction | 0.28 | 0.1 | 0.52 |
| Q05 | crystal_purity | 0.93 | 0.82 | 0.99 |
| Q05 | crystal_size | 0.24 | 0.12 | 0.39 |
| Q05 | crystal_yield | 0.08 | 0 | 0.18 |
| Q06 | crystal_fines_fraction | 0.9 | 0.68 | 1 |
| Q06 | crystal_purity | 0.88 | 0.73 | 0.97 |
| Q06 | crystal_size | 0.055 | 0.015 | 0.13 |
| Q06 | crystal_yield | 0.085 | 0 | 0.19 |
| Q07 | crystal_fines_fraction | 0.25 | 0.08 | 0.48 |
| Q07 | crystal_purity | 0.935 | 0.83 | 0.99 |
| Q07 | crystal_size | 0.25 | 0.13 | 0.4 |
| Q07 | crystal_yield | 0.085 | 0 | 0.18 |
| Q08 | crystal_fines_fraction | 0.85 | 0.6 | 1 |
| Q08 | crystal_purity | 0.91 | 0.78 | 0.98 |
| Q08 | crystal_size | 0.065 | 0.02 | 0.15 |
| Q08 | crystal_yield | 0.07 | 0 | 0.17 |
| Q09 | crystal_fines_fraction | 0.015 | 0 | 0.08 |
| Q09 | crystal_purity | 0.995 | 0.94 | 1 |
| Q09 | crystal_size | 0.4 | 0.28 | 0.52 |
| Q09 | crystal_yield | 0 | 0 | 0.025 |
| Q10 | crystal_fines_fraction | 0.02 | 0 | 0.12 |
| Q10 | crystal_purity | 0.99 | 0.92 | 1 |
| Q10 | crystal_size | 0.42 | 0.28 | 0.57 |
| Q10 | crystal_yield | 0.01 | 0 | 0.055 |
| Q11 | crystal_fines_fraction | 0.28 | 0.09 | 0.52 |
| Q11 | crystal_purity | 0.93 | 0.81 | 0.99 |
| Q11 | crystal_size | 0.24 | 0.11 | 0.4 |
| Q11 | crystal_yield | 0.08 | 0 | 0.18 |
| Q12 | crystal_fines_fraction | 0.82 | 0.57 | 0.98 |
| Q12 | crystal_purity | 0.86 | 0.72 | 0.95 |
| Q12 | crystal_size | 0.075 | 0.03 | 0.16 |
| Q12 | crystal_yield | 0.22 | 0.11 | 0.34 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

These are extrapolations from the sealed campaign, with broad intervals because solvent S0 and the 385 K, lower-catalyst reaction were not directly tested. Q01 versus Q02 favors S1 over the more soluble S3 for recovery, growth and fines control, despite S3's potentially stronger reaction activity. Q03 versus Q04 predicts that the larger seed charge supplies enough surface to suppress secondary nucleation; equilibrium yield changes little, but size and fines improve. Q05 versus Q06 assigns similar final recovery but much poorer CSD to the rapid quench, since long holding did not repair established fines in the campaign. Q07 versus Q08 likewise predicts that reheating followed by fast recooling resets nucleation and sacrifices the slowly established coarse population. At 292 K, Q09 and Q10 are expected to contain mostly the deliberately added seed: continued holding gives only slight seed-excluded growth, while particles remain large and clean. Q11 versus Q12 expresses the unresolved loading tradeoff: doubling reagent increases seed-excluded recovery but raises supersaturation, impurity occlusion and secondary nucleation. Feasibility booleans use the point estimates; Q04, Q05, Q07 and Q11 remain especially uncertain because their fines intervals cross 0.50.

## K2

## 1. Status of the main claims

### Supported by direct observations
- **Full-loading S1/S2 processes recovered substantial, very pure product but produced excessive fines.** Batches 3–6 gave crystal yields of about 0.44–0.47 and purities of about 0.98–1.00, while fines were approximately 0.99–1.00. This is a direct empirical pattern.
- **Warm crystallization can preserve coarse seed particles at the expense of seed-excluded recovery.** Batch 2, held at 300 K, had essentially zero crystal yield and fines near zero. The observed particles were therefore principally the added seed.
- **More seed alone did not solve the fines problem.** Batch 3 used 0.005 g seed and batch 4 used 0.05 g, yet both had fines near one. More decisively, increasing the S3 seed charge from 0.05 g in batch 8 to a cumulative 1.0 g in batch 10 left fines around 0.85–0.87 and recovery around 0.30–0.31.
- **Simply extending the hold was insufficient in the tested full-loading regime.** Batch 11 used ten long S3 holds but remained at crystal yield 0.296 and fines 0.853, similar to batches 8 and 10.
- **The combined batch-12 process met both constraints.** Batch 12 directly showed crystal yield 0.4712, purity 0.9961 and fines 0.4366.

### Supported as interpretations, but not isolated causally
- **Supersaturation/loading controlled the recovery–fines tradeoff.** Batch 12 used half the reagent loading of the earlier S2 batches and was the only qualifying run. This strongly supports the interpretation, but loading was changed together with solvent volume, endpoint temperature and hold history.
- **S3 moderated nucleation but sacrificed recovery.** Batches 8–11 generally had lower fines than full-loading S1/S2 batches, but also lower recovery. Because their thermal programs differed, this is comparative evidence rather than a clean solvent effect.
- **Dilution may have improved the upstream reaction as well as crystallization.** Batch 12 had assay yield/selectivity near 0.676/0.671, higher than the roughly 0.57–0.60 values in several full-loading S2 runs. That concentration effect is plausible but rests on one batch.

### Contradicted in the tested ranges
- **The initial claim that slow cooling plus modest seeding would by itself control fines** was contradicted by batches 3–7.
- **The proposed partial-reheat/Ostwald-ripening remedy** was contradicted in its tested form by batch 5, which still had fines at 1.000.
- **The idea that enough added seed or enough elapsed time would necessarily rescue an already nucleated slurry** was contradicted by batches 10 and 11.

### Still untested
- Catalyst effects remain untested because every completed batch used C1.
- The individual effects of dilution, endpoint temperature, cooling profile and prolonged cold holding in batch 12 were not separated.
- Batch-12 repeatability is unknown.
- The proposed nucleation and growth equations were explanatory constructs, not fitted or independently validated laws.

## 2. One additional experiment

I would repeat the complete batch-12 procedure while changing only the initial reagent charge from 0.02 to 0.04 mol, keeping S2 volume at 0.08 L, catalyst charge, reaction history, seed mass, cooling to 280 K and all six cold holds unchanged.

This matched high-loading experiment would distinguish two leading explanations:

1. **Loading/supersaturation is the decisive cause.** The doubled charge should give a smaller number-weighted size and fines above 0.50—potentially approaching the near-unity fines seen in batches 3–5—while retaining high purity and substantial normalized recovery.
2. **The long batch-12 cold history is sufficient even at high loading.** The new batch should remain coarse and qualifying, with fines below 0.50 and normalized recovery near batch 12.

A third possibility is strong stochastic nucleation: an intermediate or inconsistent result would indicate that neither single-run comparison securely identifies the cause. This experiment would not fully quantify repeatability, but it is the cleanest one-batch intervention for separating loading from the batch-12 thermal history.

## 3. Weakest use of evidence and least reliable prediction

The account used the **degradation-warning and byproduct observations** least effectively. Final assays showed degradation warnings around 0.18–0.25 and appreciable byproduct signals, including batch 2’s relatively high degradation warning of about 0.253. I discussed concentration-dependent selectivity but did not build a convincing temperature–time degradation mechanism from those channels. Only one intermediate HPLC measurement was available, and reaction temperature, duration, solvent and loading were not independently varied, so stronger interpretation would have exceeded the evidence.

The least reliable held-out prediction is **Q10**. It predicted almost no seed-excluded yield, large seed-dominated particles and low fines after an additional 7200 s at 292 K in S0. No campaign batch used S0, and the result is highly sensitive to whether the target concentration lies just below or just above S0’s solubility boundary at 292 K. If undersaturated, the prediction is reasonable; if slightly supersaturated, two hours could produce appreciable growth or a burst of secondary nucleation and could reverse the predicted quality classification. Thus Q10 combines an untested solvent, an uncalibrated solubility threshold, a new scale and a duration effect not isolated by the campaign.
