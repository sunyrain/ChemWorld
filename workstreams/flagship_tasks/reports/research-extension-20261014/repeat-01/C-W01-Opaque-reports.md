# C-W01-Opaque — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

## Mechanistic account

### 1. Observed material effects

At the standard charge of 0.04 mol reagent in 0.08 L solvent, C0/S0 was the most consistently productive tested combination. Batch 1 gave reaction conversion 1.00, selectivity 0.653, crystal recovery 0.509, and crystal purity 0.980. Batch 10 reached the highest observed crystal recovery, 0.534, with purity 0.972. However, both had essentially all particles in the fines class: final-assay fines fractions were 0.997 and 1.00, respectively.

The initial material screen was paired rather than fully factorial, so catalyst and solvent effects cannot generally be separated. The C1/S1 and C3/S3 pairs gave lower recoveries of 0.377 and 0.324 in batches 2 and 4. C2/S2 at 300 K produced no measurable seed-excluded recovery in batch 3. These results do not prove that C1–C3 are intrinsically inferior because each catalyst was initially tested with a different solvent and thermal history.

There is narrower evidence for a solvent effect from C0/S2 batches. Batch 6 gave recovery 0.495 and purity 0.996, but reaction selectivity was 0.586, below the roughly 0.62–0.66 values commonly observed with C0/S0. Batch 11 similarly gave recovery 0.449, purity 0.988, and selectivity 0.618. Thus S2 could still support crystallization but appeared less favorable for reaction selectivity under the tested conditions. This interpretation remains uncertain without replicated C0/S0 and C0/S2 experiments under identical thermal histories.

### 2. Reaction–crystallization coupling

The reaction and crystallization objectives were only partially aligned. High conversion or reaction yield did not ensure an acceptable crystal population. Batch 1 had complete conversion and useful crystallization recovery, but a fines fraction near one. Conversely, batch 12 had a reported reaction selectivity of 0.992 and reaction yield of 0.997, yet only 0.003 seed-excluded crystal recovery.

The relevant crystallization quantity was

`Y_crystal = recovered target product excluding seed / target product present before separation`.

It is therefore a crystallization-stage recovery, not overall yield from the initial reagent. A rough process-yield diagnostic is the product of reaction target yield and crystallization recovery. This is approximately 0.651 × 0.509 ≈ 0.33 for batch 1, versus 0.997 × 0.003 ≈ 0.003 for batch 12. This product is only illustrative because the reported reaction channels have their own measurement definitions and uncertainties.

Purity was not the principal limitation. Productive batches generally gave crystal purity above 0.96. The unresolved coupling was instead between recovering appreciable target mass and avoiding secondary nucleation or other production of sub-20-micrometre particles.

### 3. Supersaturation and particle mechanism

A useful qualitative description is based on supersaturation,

`S = C / C*(T, solvent)`,

where `C*` is the equilibrium solubility. Classical nucleation behavior can be represented schematically as

`J ≈ J0 exp[-A/(ln S)^2]`,

while crystal growth is often approximated by

`G ≈ kg(S − 1)^g`.

This form explains a sharp tradeoff: lowering temperature or increasing concentration raises recovery but can increase nucleation much more strongly than growth, generating many fines. Conditions close to saturation favor growth on existing seed but may recover almost no new target material.

Batch 3 illustrates the latter limit. At 300 K it showed excellent apparent CSD quality, zero fines, and relatively large particles, but zero seed-excluded recovery. The measured particles were therefore plausibly dominated by the added seed rather than recovered target. Productive batches cooled to approximately 270–295 K instead gave recoveries around 0.31–0.53 but fines around 0.99–1.00.

Loading provided the clearest mechanistic perturbation. The standard nominal concentration was about 0.50 mol/L. Reducing it to 0.125 mol/L in batch 9 lowered recovery to 0.312 but did not reduce fines. Extreme dilution to about 0.0125 mol/L in batch 12 reduced the fines fraction to 0.00196 and gave CSD quality 1.00, corroborated by the pre-filtration particle measurement with fines 0.0040 and CSD quality 0.987. However, recovery collapsed to 0.00296.

This supports a strong supersaturation/loading effect, but it does not establish that batch 12 generated a commercially useful coarse product. With only 0.001 mol reagent and 0.05 g seed, seed surface and seed particle count were very large relative to the amount of recovered target. The excellent particle statistics could therefore describe a seed-dominated solid population. Moreover, the recovery estimate is smaller than the final assay’s nominal crystal-yield noise scale of about 0.01, so it may not be statistically distinguishable from zero.

### 4. Process-history dependence and revisions

The initial hypothesis was that slow cooling, seeding, and a cold growth hold would suppress fines. The experiments revised that view:

- Batch 5 used staged cooling through 300 K to 285 K and gave recovery 0.469 but fines 1.00.
- Batch 7 deliberately crystallized cold, reheated near 305 K to dissolve small crystals, and slowly regrew at 288 K. It still gave recovery 0.476 and fines 0.987.
- Batch 8 used 295 K and approximately 12 hours of cold holding. Recovery remained 0.448 and fines 0.987.
- Batch 10 used the maximum legal per-batch seed addition and slow cooling to 270 K. It achieved the best recovery, 0.534, but fines remained 1.00.

Thus, within the tested standard-loading regime, longer holds, staged cooling, thermal cycling, and the allowed seed dose did not resolve the fines problem. The original slow-cooling explanation was rejected, followed by rejection of a simple dissolve/regrow remedy. The hypothesis was then narrowed to supersaturation control. Moderate dilution failed, while extreme dilution strongly improved apparent particle quality at the expense of essentially all recovery.

Some recovery differences among batches are comparable to process variation and assay noise, and the histories were not exact replicates. In contrast, the difference between fines near one in productive batches and near zero in batch 12 is too large to attribute plausibly to the stated fines noise of about 0.018.

### 5. Remaining tradeoff and untested alternatives

The experiments reveal an unresolved quality–recovery boundary. Batch 10 supplied the greatest recovery but grossly violated the fines constraint. Batch 12 clearly met the purity and fines limits but was far below the 0.10 feasibility target. Batch 12 therefore remains the sealed recommendation only as the best observed quality-feasible batch, not as a satisfactory recovery optimum.

The most important untested possibility is a sharp transition at an intermediate loading between 0.001 and 0.01 mol. A denser loading series in that interval could locate the maximum recovery that still keeps fines at or below 0.50. Catalyst amount should be scaled or independently varied because conversion fell to 0.508 in batch 12, making loading and reaction extent partially confounded.

Other untested alternatives include controlled reagent or antisolvent feeding, solvent mixtures, seed-size optimization rather than seed mass alone, independent catalyst-by-solvent factorial experiments, selective removal or classification of fines, and replicated experiments around the apparent transition. These mechanisms cannot be claimed from the present evidence.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.24 | 0.07 | 0.49 |
| Q01 | crystal_purity | 0.97 | 0.91 | 0.995 |
| Q01 | crystal_size | 0.23 | 0.12 | 0.36 |
| Q01 | crystal_yield | 0.31 | 0.2 | 0.43 |
| Q02 | crystal_fines_fraction | 0.16 | 0.03 | 0.39 |
| Q02 | crystal_purity | 0.98 | 0.93 | 1 |
| Q02 | crystal_size | 0.27 | 0.14 | 0.42 |
| Q02 | crystal_yield | 0.26 | 0.15 | 0.38 |
| Q03 | crystal_fines_fraction | 0.91 | 0.68 | 1 |
| Q03 | crystal_purity | 0.97 | 0.91 | 0.995 |
| Q03 | crystal_size | 0.055 | 0.02 | 0.12 |
| Q03 | crystal_yield | 0.39 | 0.27 | 0.51 |
| Q04 | crystal_fines_fraction | 0.14 | 0.03 | 0.36 |
| Q04 | crystal_purity | 0.98 | 0.93 | 1 |
| Q04 | crystal_size | 0.27 | 0.15 | 0.41 |
| Q04 | crystal_yield | 0.39 | 0.27 | 0.51 |
| Q05 | crystal_fines_fraction | 0.11 | 0.02 | 0.3 |
| Q05 | crystal_purity | 0.98 | 0.93 | 1 |
| Q05 | crystal_size | 0.29 | 0.17 | 0.44 |
| Q05 | crystal_yield | 0.39 | 0.28 | 0.51 |
| Q06 | crystal_fines_fraction | 0.72 | 0.46 | 0.94 |
| Q06 | crystal_purity | 0.94 | 0.86 | 0.99 |
| Q06 | crystal_size | 0.11 | 0.04 | 0.22 |
| Q06 | crystal_yield | 0.42 | 0.3 | 0.54 |
| Q07 | crystal_fines_fraction | 0.1 | 0.02 | 0.29 |
| Q07 | crystal_purity | 0.98 | 0.93 | 1 |
| Q07 | crystal_size | 0.3 | 0.18 | 0.45 |
| Q07 | crystal_yield | 0.4 | 0.29 | 0.52 |
| Q08 | crystal_fines_fraction | 0.84 | 0.61 | 0.99 |
| Q08 | crystal_purity | 0.93 | 0.83 | 0.99 |
| Q08 | crystal_size | 0.08 | 0.03 | 0.17 |
| Q08 | crystal_yield | 0.3 | 0.17 | 0.43 |
| Q09 | crystal_fines_fraction | 0.015 | 0 | 0.08 |
| Q09 | crystal_purity | 0.995 | 0.96 | 1 |
| Q09 | crystal_size | 0.36 | 0.24 | 0.48 |
| Q09 | crystal_yield | 0.01 | 0 | 0.05 |
| Q10 | crystal_fines_fraction | 0.1 | 0.01 | 0.29 |
| Q10 | crystal_purity | 0.99 | 0.95 | 1 |
| Q10 | crystal_size | 0.28 | 0.16 | 0.41 |
| Q10 | crystal_yield | 0.12 | 0.04 | 0.24 |
| Q11 | crystal_fines_fraction | 0.09 | 0.01 | 0.27 |
| Q11 | crystal_purity | 0.98 | 0.93 | 1 |
| Q11 | crystal_size | 0.3 | 0.18 | 0.45 |
| Q11 | crystal_yield | 0.39 | 0.28 | 0.51 |
| Q12 | crystal_fines_fraction | 0.64 | 0.37 | 0.88 |
| Q12 | crystal_purity | 0.95 | 0.87 | 0.995 |
| Q12 | crystal_size | 0.14 | 0.06 | 0.27 |
| Q12 | crystal_yield | 0.49 | 0.38 | 0.6 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

All recipes contain seed, so particles are expected even where little new target crystallizes. Q01–Q02 compare solvents: I expect S1 to recover more product but generate somewhat more fines than S3. Q03–Q04 isolate seed loading; 0.001 g provides too little growth surface and should give many fines, while 0.045 g should favor growth on seed with little change in equilibrium recovery. Q05–Q06 compare a very slow ramp with an immediate crash followed by equal aging: slow supersaturation generation should produce larger crystals and fewer fines, whereas prolonged aging is not expected to fully erase crash nucleation. Q07–Q08 compare continued cold growth with reheating and rapid recooling; the latter should partially dissolve the established population and then renucleate fines. Q09–Q10 compare stopping immediately at 292 K with two hours of growth: the immediate endpoint should be seed-dominated with negligible recovery, while continued growth raises recovery but retains acceptable quality. Q11–Q12 compare reagent loading; doubling loading should raise recovery but also supersaturation and fines enough to lose feasibility. Intervals are deliberately broad because the campaign did not independently calibrate C1/S0, these cooling ramps are much longer than those tested, and seed-dominated size measurements can look favorable even when seed-excluded recovery is very small.

## K2

1. Supported, contradicted, and untested claims

Supported by direct observations:
- Productive standard-load crystallization consistently produced high purity but excessive fines. Batches 1, 5, 7, 8 and 10 with C0/S0 gave roughly 0.45–0.53 crystal recovery and purity above 0.96, while fines remained about 0.99–1.00. Batches 6 and 11 showed the same recovery–fines conflict with C0/S2.
- C0/S0 was the best standard-load combination actually observed: batch 10 had the highest recovery, 0.534. This supports its empirical ranking among tested recipes, not intrinsic catalyst superiority.
- Loading strongly affected the apparent particle population. Moderate dilution in batch 9 still gave fines 1.00 and recovery 0.312, whereas extreme dilution in batch 12 gave fines 0.00196 and recovery 0.00296. The interpretation that lower supersaturation suppresses nucleation is plausible, but the batch-12 solids may have been dominated by seed.
- Purity was generally not limiting; most recovered solids assayed above 0.96 purity.

Contradicted within the tested scope:
- The initial claim that ordinary slow cooling and a cold hold would solve the fines problem was contradicted by batches 5 and 8.
- Selective dissolution and regrowth did not rescue quality under the tested cycle: batch 7 reheated to about 305 K and still finished with fines 0.987.
- Moderate dilution alone was insufficient, as shown by batch 9.
- Increasing seed to the legal per-batch maximum did not eliminate fines at standard loading; batch 10 still had fines 1.00.

Still untested or unresolved:
- Catalyst effects independent of solvent remain untested because the first material screen was paired rather than factorial. C1/S1, C2/S2 and C3/S3 cannot establish separate catalyst rankings.
- The concentration interval between 0.001 and 0.01 mol was not mapped, so a useful quality/recovery transition may exist there.
- Ultra-slow multiday ramps, controlled feeding, solvent mixtures, seed-size distributions, fines classification and genuine replication were not tested in the campaign.
- Batch 12 formally met the quality constraints, but its recovery estimate was below the assay’s approximate 0.01 noise scale. Evidence for materially positive seed-excluded recovery is therefore weak.

2. One additional experiment

I would run an interpolation experiment identical to batch 12 except for 0.004 mol reagent in 0.08 L S0 and 0.0008 mol C0 catalyst, preserving the batch-12 catalyst/reagent ratio. I would use 0.05 g seed, the same reaction conditions, slow cooling to 270 K, the same prolonged hold, a pre-filtration particle measurement, filtration and final assay.

This single-factor loading test would distinguish three explanations:
- Smooth supersaturation control: recovery should rise above batch 12 while fines increase gradually, potentially revealing a feasible intermediate regime.
- A sharp secondary-nucleation threshold: recovery should improve, but fines should jump toward the near-one values of batch 9.
- Seed-dominated apparent quality or insufficient target formation: particle quality should remain excellent while seed-excluded recovery stays near zero.

The most informative result would be appreciable recovery with fines below 0.50; it would demonstrate that the campaign simply missed a narrow operating window. High recovery with fines near one would instead support an abrupt nucleation boundary.

3. Least effectively used observation and least reliable prediction

The observation used least effectively was batch 2, the only direct C1 experiment. It showed C1/S1 conversion 1.00, selectivity about 0.529, recovery 0.377 and fines 1.00, but the mechanistic account concentrated mainly on C0/S0 and the concentration series. Because every held-out recipe uses C1, batch 2 deserved more weight. Its different solvent, concentration, temperature and cooling history nevertheless prevent clean transfer.

Q02 is the least reliable held-out prediction. It combines C1 with S3, a pairing never tested, and applies an exceptionally long cooling ramp absent from the campaign. The inferred S1-versus-S3 ranking came from batches 2 and 4, where catalyst and solvent changed together, so it confounds both material effects. Consequently, Q02’s predicted recovery, particle size, fines and feasibility rest on a larger extrapolation than the other paired comparisons.
