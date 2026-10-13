# C-W04-Opaque — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

## Mechanistic account

### Scope
The catalysts C0–C3 and solvents S0–S3 are anonymous benchmark materials, so the discussion concerns observed functional effects rather than real chemical identities. Crystal yield is the seed-excluded recovery of target already present before separation; it is not the overall yield from charged reagent.

### Reaction and material effects
All screened reactions reached very high conversion, but target selectivity differed substantially. This means conversion alone was not diagnostic: competing product formation controlled the target pool available for crystallization. For example, batch 6 (C0/S0, 360 K) gave reaction yield about 0.616 and selectivity 0.614, whereas batches 3–4 gave reaction yields only about 0.419–0.445 with lower selectivity. I interpret catalyst, solvent, and temperature as shifting competition between target and byproduct pathways after reagent consumption.

S1 had the clearest favorable crystallization effect. With C0 and broadly similar slow-cooling conditions, batch 5 (S1) had fines 0.436, while batch 6 (S0) had fines 0.823. The comparison is not perfectly isolated—reaction temperature also differed by 10 K—but the fines difference is much larger than the stated assay noise. Batches 2, 5, and 7–10 further showed that S1 repeatedly supported fines below 0.50. Thus I interpret S1 as favoring growth on existing crystals relative to secondary nucleation or agglomerate breakage. S0 supported good reaction performance and recovery but an unfavorable particle-number distribution.

The initial four-way screen was not factorial: C0/S0, C1/S1, C2/S2, and C3/S3 were changed together. Consequently, batches 2–4 do not separately identify catalyst and solvent effects. C0 was retained because it provided good target formation, while S1 was retained because its particle-quality behavior was reproducibly favorable.

### Reaction–crystallization coupling
A useful mass-accounting approximation is

`recovered target from charge ∝ reaction target yield × crystal yield`,

where the second factor is conditional recovery during crystallization. High crystal yield therefore cannot compensate fully for poor target formation, and high reaction conversion cannot compensate for low selectivity.

The crystallization metrics also depend on the composition inherited from reaction. Byproducts may change solubility, nucleation, growth, or impurity occlusion. Nevertheless, crystal purity remained high in every reported batch—approximately 0.974–1.000—so the principal observed coupling was through available target and particle formation rather than loss of chemical purity.

Batch 6 illustrates the tension: it combined strong reaction yield and crystal recovery (0.465), but its fines fraction of 0.823 made it unacceptable. Batch 10 had somewhat lower reaction yield (0.524) but combined 0.474 crystal recovery with measured fines of 0.478 and purity of 0.974. The selected process therefore reflects the particle constraint rather than simply maximizing reaction output.

### Cooling depth and recovery–quality tradeoff
Within the focused C0/S1 series using 0.01 g seed and a single 14,400 s cooling step, deeper cooling increased observed recovery:

- Batch 7, 280 K: recovery 0.424, fines 0.406.
- Batch 8, 270 K: recovery 0.452, fines 0.414.
- Batch 9, 260 K: recovery 0.460, fines 0.444.
- Batch 10, 250 K: recovery 0.474, fines 0.478.

This is consistent with a solubility-driven relationship such as

`crystal recovery ≈ 1 − C*(T_end)/C_initial`,

with lower endpoint temperature reducing equilibrium mother-liquor concentration `C*(T_end)`. Simultaneously, increasing supersaturation raises secondary-nucleation propensity, explaining the rise in the number fraction below 20 µm. A generic kinetic representation is

`growth rate G ∝ (C − C*)^g`,  `nucleation rate B ∝ (C − C*)^b`,

with particle quality deteriorating when nucleation accelerates more strongly than growth as supersaturation increases.

The apparent recovery trend is mechanistically plausible, but adjacent differences are small relative to the final-assay crystal-yield noise of about 0.01. It should therefore be treated as a directional trend, not a precisely estimated temperature law. Batch 10 maximized observed feasible recovery, but its fines value was only 0.022 below the specification and the fines noise is about 0.018. Batch 9 sacrifices roughly 0.014 observed recovery for a larger fines margin. This boundary-risk tradeoff remains unresolved.

### Seed effects
Reducing seed from 0.05 g in batch 5 to 0.01 g in batch 7 coincided with recovery increasing from 0.406 to 0.424 and fines decreasing from 0.436 to 0.406, but those batches also differ through uncontrolled process variation. At 250 K, batch 10 used 0.01 g seed and gave recovery/fines of 0.474/0.478; batch 12 used 0.005 g and gave 0.468/0.468. Both differences are within or near instrument noise. Thus no reliable seed-dose law was established. A plausible but untested alternative is that fewer seeds allow greater growth per seed, while too few seeds permit spontaneous nucleation.

### Process-history dependence
The path to the endpoint mattered, not just final temperature. Batch 10 used one uninterrupted 14,400 s cooling step to 250 K and met the fines limit. Batch 11 first cooled to 250 K for 7,200 s, reheated to 290 K for 1,800 s, and then recooled to 250 K for 14,400 s. It produced similar recovery (0.461) and high purity (0.989), but fines rose to 0.630. The tested thermal cycle therefore failed to provide the hoped-for ripening benefit.

I interpret the batch-11 result as partial dissolution followed by renewed nucleation during recooling, or fragmentation/agglomerate restructuring during the extra thermal and stirring history. Which mechanism dominates was not measured. Slower reheating, a higher-temperature dissolution hold, gentler agitation, or a narrowly controlled Ostwald-ripening cycle remain untested alternatives; the result rejects only the particular cycle used.

Batch 1 provides another history warning. It was cooled for only 7,200 s to 275 K and then held under conditions that allowed the temperature to rebound to about 292 K before filtration. Although its recovery was 0.460 and purity 0.979, fines were 0.948. Because S0, shorter cooling, and the temperature rebound all changed together, this batch cannot isolate the cause, but it shows that nominal endpoint temperature alone is insufficient to specify a reproducible process.

### Revisions and remaining uncertainty
The initial hypothesis was that slow seeded cooling would reduce fines while deeper cooling would increase recovery. The campaign supported both ideas only within the S1 single-cool regime. The early expectation that a reheating/recooling cycle might enlarge particles was revised and rejected for the tested batch-11 history. The working view also shifted from emphasizing catalyst screening to recognizing solvent and thermal history as the dominant observed controls on particle quality.

Unresolved alternatives include catalyst–solvent interactions, agitation effects, independent reaction-temperature effects, seed-dose effects, and whether the fines increase at deep cooling is caused by secondary nucleation or mechanical breakage. No factorial replication separated these mechanisms. Purity appears robustly above 0.80, but recovery differences among batches 9, 10, and 12 are not sharply resolved, and compliance of the deepest-cooling process with the 0.50 fines limit has a narrow uncertainty margin.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.2 | 0.09 | 0.35 |
| Q01 | crystal_purity | 0.97 | 0.92 | 0.995 |
| Q01 | crystal_size | 0.17 | 0.09 | 0.28 |
| Q01 | crystal_yield | 0.15 | 0.03 | 0.3 |
| Q02 | crystal_fines_fraction | 0.43 | 0.26 | 0.62 |
| Q02 | crystal_purity | 0.96 | 0.89 | 0.995 |
| Q02 | crystal_size | 0.1 | 0.045 | 0.2 |
| Q02 | crystal_yield | 0.11 | 0.015 | 0.26 |
| Q03 | crystal_fines_fraction | 0.48 | 0.28 | 0.69 |
| Q03 | crystal_purity | 0.97 | 0.9 | 0.998 |
| Q03 | crystal_size | 0.1 | 0.04 | 0.22 |
| Q03 | crystal_yield | 0.1 | 0.01 | 0.25 |
| Q04 | crystal_fines_fraction | 0.35 | 0.2 | 0.54 |
| Q04 | crystal_purity | 0.97 | 0.91 | 0.998 |
| Q04 | crystal_size | 0.13 | 0.065 | 0.24 |
| Q04 | crystal_yield | 0.12 | 0.02 | 0.27 |
| Q05 | crystal_fines_fraction | 0.33 | 0.18 | 0.51 |
| Q05 | crystal_purity | 0.97 | 0.91 | 0.998 |
| Q05 | crystal_size | 0.14 | 0.07 | 0.25 |
| Q05 | crystal_yield | 0.12 | 0.02 | 0.28 |
| Q06 | crystal_fines_fraction | 0.68 | 0.5 | 0.83 |
| Q06 | crystal_purity | 0.96 | 0.88 | 0.995 |
| Q06 | crystal_size | 0.055 | 0.02 | 0.12 |
| Q06 | crystal_yield | 0.13 | 0.02 | 0.29 |
| Q07 | crystal_fines_fraction | 0.31 | 0.16 | 0.49 |
| Q07 | crystal_purity | 0.97 | 0.91 | 0.998 |
| Q07 | crystal_size | 0.15 | 0.075 | 0.27 |
| Q07 | crystal_yield | 0.13 | 0.025 | 0.29 |
| Q08 | crystal_fines_fraction | 0.63 | 0.43 | 0.8 |
| Q08 | crystal_purity | 0.96 | 0.88 | 0.995 |
| Q08 | crystal_size | 0.065 | 0.025 | 0.14 |
| Q08 | crystal_yield | 0.08 | 0.005 | 0.23 |
| Q09 | crystal_fines_fraction | 0.82 | 0.65 | 0.94 |
| Q09 | crystal_purity | 0.97 | 0.88 | 1 |
| Q09 | crystal_size | 0.025 | 0.008 | 0.065 |
| Q09 | crystal_yield | 0.004 | 0 | 0.04 |
| Q10 | crystal_fines_fraction | 0.7 | 0.5 | 0.86 |
| Q10 | crystal_purity | 0.97 | 0.89 | 1 |
| Q10 | crystal_size | 0.045 | 0.015 | 0.1 |
| Q10 | crystal_yield | 0.025 | 0 | 0.1 |
| Q11 | crystal_fines_fraction | 0.34 | 0.19 | 0.52 |
| Q11 | crystal_purity | 0.97 | 0.91 | 0.998 |
| Q11 | crystal_size | 0.14 | 0.07 | 0.25 |
| Q11 | crystal_yield | 0.12 | 0.02 | 0.28 |
| Q12 | crystal_fines_fraction | 0.46 | 0.29 | 0.65 |
| Q12 | crystal_purity | 0.93 | 0.83 | 0.985 |
| Q12 | crystal_size | 0.105 | 0.05 | 0.2 |
| Q12 | crystal_yield | 0.42 | 0.24 | 0.58 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

All recipes are seeded, so particles are expected even where little seed-excluded product grows. Q01–Q02 assigns S1 lower fines and larger crystals than S3, following the observed solvent dependence, although the extrapolation to this long staged ramp is uncertain. Q03–Q04 treats 0.001 g seed as insufficient surface area relative to 0.045 g, increasing secondary-nucleation risk; this seed effect was unresolved experimentally, so the intervals overlap. Q05–Q06 predicts similar endpoint recovery but much poorer size quality after the rapid initial crash, because the gradual ramp limits peak supersaturation. Q07–Q08 applies the observed adverse history dependence of reheating and rapid recooling: partial dissolution followed by renucleation should lower retained recovery and raise fines. Q09–Q10 predicts very little seed-excluded recovery at 292 K; the extra hold permits some growth but does not erase the fines-rich rapid-cooling history. Q11–Q12 predicts that doubling reagent concentration greatly raises fractional recovery by increasing target concentration relative to solubility, while also increasing supersaturation, impurity-occlusion risk and fines. Uncertainty is broad because the campaign used larger charges, mostly C0/S1, far shorter cooling histories, and did not independently identify C1/S0 solubility, seed-dose effects, or long-time ripening.

## K2

1. **Status of the main claims**

- **Supported observationally, but not fully isolated:** S1 was associated with better particle quality than S0. Batch 5 (C0/S1, 350 K reaction, 280 K cooling endpoint) had fines 0.436, whereas batch 6 (C0/S0, 360 K reaction, otherwise similar crystallization) had fines 0.823. The direct observation is the large difference; attributing it specifically to solvent is an interpretation because reaction temperature and resulting composition also differed.
- **Supported as a within-series trend:** In batches 7–10, all using C0/S1, 0.01 g seed, and 14,400 s cooling, lowering the endpoint from 280 to 250 K increased observed crystal yield from 0.424 to 0.474 while fines rose from 0.406 to 0.478. This supports a recovery–quality tradeoff consistent with increasing supersaturation. Adjacent yield differences are comparable to assay noise, so only the overall direction is reasonably supported.
- **Supported directly:** Purity was robust throughout the campaign, approximately 0.974–1.000. Within the tested space, fines—not purity—were the binding quality constraint.
- **Contradicted for the tested procedure:** The expectation that reheating and recooling would improve crystal size distribution was contradicted. Batch 11’s 290 K reheat/recool history produced fines of 0.630, versus 0.478 for the single-cool batch 10, without improving recovery. This rejects that specific cycle, not thermal ripening in general.
- **Unresolved:** The seed-dose effect remains unresolved. At 250 K, batches 10 and 12 used 0.01 and 0.005 g seed and gave recovery/fines of 0.474/0.478 and 0.468/0.468. Those differences are too small relative to measurement uncertainty to establish a law.
- **Still untested:** Independent catalyst effects, catalyst–solvent interactions, agitation effects, a true cooling-rate series at fixed total time, and the distinction between secondary nucleation and mechanical fragmentation were not isolated. The initial C0/S0, C1/S1, C2/S2, and C3/S3 screen changed catalyst and solvent together.

2. **One additional experiment**

I would run an exact solvent-control counterpart to batch 5: C0/S0, reaction at 350 K for 3,600 s, 0.05 g seed, one 14,400 s cooling step to 280 K, followed by particle-size measurement, filtration, and final assay. Every setting would match batch 5 except S0 replacing S1.

This would distinguish two leading explanations for the batch 5–6 fines difference:

- **Solvent-controlled crystallization:** If the new S0 batch again produced much higher fines and smaller crystals than batch 5, while reaction composition remained reasonably similar, it would support the interpretation that S0 promotes secondary nucleation or poor growth habit.
- **Reaction-temperature/upstream-composition or stochastic effect:** If the new batch resembled batch 5 rather than batch 6, the earlier S0 result would be better explained by the 360 K reaction history, its impurity profile, or batch variability rather than solvent alone.

An intermediate HPLC measurement before seeding would strengthen the discrimination: similar reaction yield/selectivity but different particle outcomes would favor a direct solvent effect; large compositional differences would support reaction–crystallization coupling.

3. **Least effectively used evidence and least reliable prediction**

The account used the paired in-situ particle-size and final-assay readings least effectively. Batches 5–12 generally had particle measurements before filtration as well as final measurements, but the report emphasized final-assay values. Comparing those readings could have better quantified measurement scatter, checked whether filtration altered the representative particle population, and highlighted how uncertain boundary compliance was in batches 10 and 12.

The least reliable held-out prediction is Q12. It doubled reagent concentration relative to Q11 while also using C1/S0 and an extremely long staged cooling history—conditions not directly represented in the campaign. Its predicted recovery relied heavily on an assumed solubility/concentration relationship inferred from fixed-charge experiments. No campaign batch varied concentration independently, and reaction yield determines the actual target concentration entering crystallization. Consequently, both the magnitude of the predicted recovery increase and the associated purity/fines tradeoff are substantially more extrapolative than the predictions based mainly on cooling-history comparisons.
