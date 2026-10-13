# C-W04-Aligned — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

## Mechanistic account

### Scope and material effects
The catalyst and solvent labels are anonymous benchmark materials, so the following conclusions apply only to this campaign. The nominal dossier described S2 as having relatively low solubility and nucleation tendency, high crystal-growth tendency, and low impurity occlusion. The experiments broadly supported that prior: S2 usually produced very pure crystals and, in an appropriate concentration/seed regime, acceptable fines. S1 also gave high purity and sometimes greater recovery, but consistently poorer particle-size distributions.

The strongest solvent comparison is between batches 2 and 4, although catalyst identity also changed. Batch 2 used S2 and gave crystal recovery 0.423, purity 0.988, and fines 0.390. Batch 4 used S1 and gave slightly higher recovery, 0.439, and purity 1.000, but fines rose to 0.675. In batch 5, S1 plus a thermal cycle raised recovery to 0.479, but fines reached 1.000. Thus S1 may permit more recovered mass, but none of its tested histories met the fines constraint. S2 supplied the best observed quality/recovery compromise.

Catalyst effects cannot be ranked cleanly because catalyst, temperature, solvent volume, and crystallization history were not varied independently. C1, C3, C0, and C2 all reached approximately complete conversion in their initial tests, while final selectivity remained only about 0.44–0.53. For example, batch 1 (C1, 370 K) had conversion 1.000 and selectivity 0.512; batch 2 (C3, 350 K) had conversion 1.000 and selectivity 0.476; batch 3 (C0, 340 K) had conversion 0.998 and selectivity 0.436; and batch 4 (C2, 350 K) had conversion 0.989 and selectivity 0.479. These are observations, not an isolated catalyst ranking. C3 was retained in the recommended process because it gave complete conversion and worked reproducibly in the best crystallization region, not because the campaign proved it intrinsically superior.

### Reaction–crystallization coupling
A useful bookkeeping relationship is

n_target,before separation ≈ n_reagent × conversion × selectivity,

while the reported crystallization recovery is

Y_cryst = n_recovered target excluding seed / n_target,before separation.

Consequently, crystal recovery is a stage-specific quantity and should not be confused with overall isolated yield from reagent. A rough overall target recovery would scale as reaction yield × crystal recovery. For batch 10 this is approximately 0.474 × 0.451 ≈ 0.21 of the reagent charge, despite its crystallization-stage recovery being 0.451.

The reaction mixtures contained substantial byproduct signal, generally about 0.34–0.39, yet S2 crystals were typically 0.98–1.00 pure. I interpret this as selective partitioning during crystallization: much of the byproduct remained in the mother liquor rather than being incorporated into the solid. This interpretation is consistent with S2's nominal low occlusion tendency, but direct mother-liquor/cake mass balances were not independently measured.

A simple equilibrium/filtration picture is

Y_cryst ≈ η_filter[1 − C*(S,T_end)V/n_target],

where C* is effective target solubility at the final temperature, V is solvent volume, and η_filter represents solid capture. The data show that this equilibrium expression alone is insufficient: particle nucleation and process history strongly changed the recoverable solid. In particular, decreasing solvent volume did not monotonically increase acceptable recovery.

### Concentration, seed, and particle formation
The results indicate a narrow kinetic operating region rather than a simple dilution trend:

- Batch 3 used 0.02 L S2 and 0.010 g seed. It gave recovery 0.393 and purity 0.998, but fines were 0.995.
- Batch 2 used 0.04 L S2 and 0.010 g seed. It gave recovery 0.423, purity 0.988, and fines 0.390.
- Batch 9 used 0.05 L S2 and 0.010 g seed. Recovery was 0.446 and purity 0.988, but fines were 1.000.
- Batches 7 and 8 used 0.06 L S2 with 0.001 and 0.003 g seed. Recoveries increased to 0.449 and 0.454, but fines were 0.501 and 0.500, just above the formal limit.
- Batch 1 used 0.08 L S2, 0.030 g seed, and a warmer 275 K endpoint. Recovery was 0.423 and fines were 0.500.

I interpret the very high fines at 0.02 and 0.05 L as entry into high-supersaturation or secondary-nucleation regimes. A useful qualitative formulation is

N_new ∝ ∫J(S_supersaturation,T,agitation)dt,

L_growth ∝ ∫G(S_supersaturation,T)dt,

where excessive nucleation rate J creates many small particles, whereas sustained growth rate G on a limited population produces larger crystals. Seed loading changes both the available growth surface and the supersaturation trajectory, so its effect need not be monotonic.

The locally successful regime was 0.04 L S2 with only 0.003–0.005 g seed, slow cooling to 250 K over 14,400 s, followed by a 14,400 s cold hold at low agitation. Batch 10, with 0.005 g seed, gave recovery 0.451, purity 0.983, fines 0.398, and CSD quality 0.709. Batch 11, with 0.003 g seed, gave recovery 0.442, purity 0.998, fines 0.380, and CSD quality 0.728. Thus reducing seed from 0.005 to 0.003 g improved the observed particle-quality metrics but did not improve recovery. The differences are modest relative to assay uncertainty and should not be treated as a precisely resolved seed optimum.

### Process-history dependence
Thermal history had a large and reproducible effect. Batch 5 was first cooled to 250 K, reheated to 285 K, and recooled; batch 6 used a milder 250→260→250 K cycle. Both finished with a fines fraction of 1.000, even though their recoveries were 0.479 and 0.444 and purities remained high. My interpretation is that reheating partially dissolved the existing population and recooling triggered a new nucleation burst rather than clean Ostwald ripening. This is supported by the common fines outcome across S1 and S2, but the campaign did not directly measure dissolution or nucleation during the cycles.

In contrast, a single slow cooling followed by an uninterrupted cold hold produced acceptable fines in batches 2, 10, 11, and 12. The process therefore has memory: final temperature alone does not determine the CSD. The route through supersaturation space, seed population, reheating, and residence time all matter.

### Recommended batch and reproducibility
Batch 10 remains the recommendation because it had the highest observed crystal recovery among batches satisfying both formal constraints: recovery 0.451, purity 0.983, and fines 0.398. Its recipe was 0.040 mol reagent, 0.005 mol C3, 0.040 L S2, reaction at 350 K for 3,600 s, 0.005 g seed, slow cooling to 250 K for 14,400 s, a 14,400 s cold hold at 100 rpm, then filtration.

Batch 12 repeated that recipe without the intermediate particle-size measurement and also qualified: recovery 0.444, purity 0.999, fines 0.388, and CSD quality 0.741. The recovery difference between batches 10 and 12 is about 0.006, smaller than the stated final-assay recovery noise of 0.010. Therefore, batch 10 has the highest observed qualifying value, but the evidence does not establish that its true recovery is greater than batch 12's. Together, the two batches support a practical recovery near 0.44–0.45 for this operating region.

### Revisions and remaining uncertainty
The initial expectation was that simply reducing S2 volume and cooling deeply would increase recovery. Batch 3 rejected that simple hypothesis: the most concentrated mixture produced lower recovery and almost entirely fine particles. The model was revised to include concentration-dependent nucleation and filtration behavior.

A second expectation was that reheating might dissolve fines and allow regrowth. Batches 5 and 6 contradicted it under the tested conditions; both cycles produced all-fines outcomes. Thermal cycling was therefore removed from the recommendation.

The unresolved tradeoff is that the highest recoveries occurred in failing or borderline particle-quality regimes. Batch 5 reached recovery 0.479 but fines 1.000. Batch 8 reached recovery 0.454 but fines 0.50037, only slightly above the limit and well within the stated fines noise of 0.018. Nevertheless, the formal observed constraint was not met, so those batches were not selected. Batch 10 sacrifices a small amount of apparent recovery to provide a substantial fines margin.

Untested alternatives include finer staged cooling without reheating, changing the temperature at which seed is introduced, different seed morphology, a narrow solvent volume between 0.04 and 0.05 L, modified filtration conditions, mixed-solvent or antisolvent policies, and direct mother-liquor analysis. These might move the recovery/quality frontier, but the campaign provides no evidence that they would do so. The sharp fines changes with concentration also warrant replication before being interpreted as a smooth physical law rather than a threshold-like benchmark response.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.3 | 0.18 | 0.45 |
| Q01 | crystal_purity | 0.96 | 0.9 | 0.99 |
| Q01 | crystal_size | 0.18 | 0.11 | 0.27 |
| Q01 | crystal_yield | 0.31 | 0.2 | 0.42 |
| Q02 | crystal_fines_fraction | 0.44 | 0.29 | 0.61 |
| Q02 | crystal_purity | 0.91 | 0.82 | 0.97 |
| Q02 | crystal_size | 0.14 | 0.08 | 0.22 |
| Q02 | crystal_yield | 0.24 | 0.13 | 0.36 |
| Q03 | crystal_fines_fraction | 0.57 | 0.38 | 0.76 |
| Q03 | crystal_purity | 0.86 | 0.75 | 0.94 |
| Q03 | crystal_size | 0.17 | 0.08 | 0.29 |
| Q03 | crystal_yield | 0.18 | 0.08 | 0.3 |
| Q04 | crystal_fines_fraction | 0.43 | 0.27 | 0.61 |
| Q04 | crystal_purity | 0.87 | 0.76 | 0.95 |
| Q04 | crystal_size | 0.15 | 0.08 | 0.24 |
| Q04 | crystal_yield | 0.21 | 0.1 | 0.33 |
| Q05 | crystal_fines_fraction | 0.41 | 0.25 | 0.58 |
| Q05 | crystal_purity | 0.87 | 0.76 | 0.95 |
| Q05 | crystal_size | 0.17 | 0.09 | 0.27 |
| Q05 | crystal_yield | 0.22 | 0.11 | 0.34 |
| Q06 | crystal_fines_fraction | 0.56 | 0.38 | 0.75 |
| Q06 | crystal_purity | 0.86 | 0.74 | 0.94 |
| Q06 | crystal_size | 0.11 | 0.05 | 0.2 |
| Q06 | crystal_yield | 0.23 | 0.12 | 0.35 |
| Q07 | crystal_fines_fraction | 0.39 | 0.23 | 0.56 |
| Q07 | crystal_purity | 0.88 | 0.77 | 0.95 |
| Q07 | crystal_size | 0.19 | 0.1 | 0.3 |
| Q07 | crystal_yield | 0.23 | 0.12 | 0.35 |
| Q08 | crystal_fines_fraction | 0.85 | 0.66 | 0.97 |
| Q08 | crystal_purity | 0.91 | 0.81 | 0.97 |
| Q08 | crystal_size | 0.08 | 0.03 | 0.15 |
| Q08 | crystal_yield | 0.18 | 0.07 | 0.3 |
| Q09 | crystal_fines_fraction | 0.85 | 0.65 | 0.98 |
| Q09 | crystal_purity | 0.94 | 0.8 | 0.99 |
| Q09 | crystal_size | 0.05 | 0.025 | 0.08 |
| Q09 | crystal_yield | 0.005 | 0 | 0.03 |
| Q10 | crystal_fines_fraction | 0.68 | 0.45 | 0.88 |
| Q10 | crystal_purity | 0.91 | 0.78 | 0.98 |
| Q10 | crystal_size | 0.07 | 0.035 | 0.12 |
| Q10 | crystal_yield | 0.07 | 0.02 | 0.15 |
| Q11 | crystal_fines_fraction | 0.42 | 0.26 | 0.59 |
| Q11 | crystal_purity | 0.87 | 0.76 | 0.95 |
| Q11 | crystal_size | 0.17 | 0.09 | 0.27 |
| Q11 | crystal_yield | 0.22 | 0.11 | 0.34 |
| Q12 | crystal_fines_fraction | 0.58 | 0.39 | 0.76 |
| Q12 | crystal_purity | 0.84 | 0.71 | 0.93 |
| Q12 | crystal_size | 0.18 | 0.09 | 0.29 |
| Q12 | crystal_yield | 0.42 | 0.28 | 0.55 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

The paired predictions apply the campaign’s qualitative mechanisms beyond the tested region, so intervals are deliberately broad. Q01–Q02: S1’s lower nominal solubility, lower nucleation tendency, faster growth and lower occlusion favor greater recovery, purity and size than S3. Q03–Q04: more seed should suppress uncontrolled primary nucleation and modestly improve capture, but may limit growth per seed; the net prediction is fewer fines with 0.045 g seed. Q05–Q06: gradual cooling should keep supersaturation lower and favor growth, whereas the rapid drop creates more nuclei; the long hold makes recovery similar but does not fully erase the CSD difference. Q07–Q08: reheating to 315 K followed by rapid recooling is predicted to dissolve part of the population and generate a new nucleation burst, consistent with the severe fines observed after both thermal cycles in campaign batches 5 and 6. Q09–Q10: seeds ensure particles are present even after 60 seconds, but meaningful seed-excluded recovery is initially negligible; a 7200-second hold increases deposition and size while fines likely remain excessive at 292 K. Q11–Q12: doubling reagent raises supersaturation and fractional recovery but also promotes secondary nucleation and impurity incorporation, creating a recovery–quality tradeoff. Feasibility flags use the point estimates; several fines intervals cross 0.50, reflecting substantial uncertainty in this untested S0 regime.

## K2

1. **Status of the main claims**

**Supported by direct observations**
- **S2 provided the most reliable quality–recovery compromise.** S2 batches 2, 10, 11 and 12 all met the purity and fines constraints. Batch 10 gave recovery 0.451, purity 0.983 and fines 0.398; its matched replicate, batch 12, gave 0.444, 0.999 and 0.388. This directly supports local robustness near the recommended recipe.
- **S1 showed a recovery–particle-quality tradeoff.** Batch 4 reached recovery 0.439 but fines 0.675; batch 5 reached 0.479 but fines 1.000. High purity was retained, so fines—not purity—were the binding problem in the tested S1 processes.
- **Reheating and recooling were harmful to the CSD under the tested conditions.** Batch 5 used a 285 K reheat and batch 6 a milder 260 K reheat; both ended at fines 1.000. The observation is direct. Partial dissolution followed by renewed nucleation is an interpretation because dissolution and nucleation were not measured directly.
- **A narrow S2 operating region existed around 0.04 L solvent and small seed charges.** Batches 10–12 produced fines of 0.38–0.40, whereas batch 3 at 0.02 L and batch 9 at 0.05 L produced fines near 1.0. That contrast is observed, although the exact causal threshold is not isolated.
- **Reaction conversion was generally not limiting.** Final assays or HPLC showed approximately complete conversion in batches 1–3 and 7–12. Moderate selectivity and substantial byproduct signal remained, yet S2 crystals were highly pure.

**Contradicted or revised claims**
- **Lower solvent volume should monotonically increase crystallization recovery:** contradicted by batch 3. Reducing S2 to 0.02 L gave lower recovery, 0.393, and fines 0.995 rather than an improvement.
- **Thermal cycling should dissolve fines and promote ripening:** contradicted under the tested histories by batches 5 and 6, which instead produced all-fines outcomes.
- **The nominally strongest catalyst should be inferable from conversion or selectivity:** not supported. Catalyst, temperature, volume and crystallization history co-varied, and all catalysts gave high conversion with only moderate selectivity.

**Still untested**
- Selective rejection of byproducts into mother liquor is a plausible interpretation of high crystal purity, but separate mother-liquor and cake compositions were not measured.
- The apparent sharp fines transition between 0.04 and 0.05 L S2 was not isolated from catalyst, seed and temperature differences.
- Seed-addition temperature, seed morphology, mixed-solvent strategies, filtration optimization and staged cooling without reheating remain untested.
- The campaign did not establish a quantitative nucleation or solubility law; the proposed equations were organizing models rather than fitted relationships.

2. **One additional experiment**

I would repeat the batch-10 process while changing only S2 volume from 0.040 to 0.050 L: 0.040 mol reagent, 0.005 mol C3, reaction at 350 K for 3600 s, 0.005 g seed, 14,400 s cooling to 250 K, 14,400 s cold hold and identical filtration. I would include non-destructive particle-size measurements at several points during cooling and at the end of the hold.

This would distinguish three explanations:
- **Concentration-driven nucleation threshold:** fines would rise abruptly at some cooling stage and finish near the batch-9 value, while recovery might remain around 0.44–0.46.
- **Smooth solubility/growth response:** recovery and particle metrics would change gradually from the batch-10/12 values rather than jumping to fines near 1.0.
- **Batch-9 confounding or stochasticity:** if the 0.050 L batch remained near fines 0.39–0.45, batch 9’s all-fines result would more likely reflect its different catalyst/temperature/seed combination or an uncontrolled realization rather than solvent volume alone.

Time-resolved particle measurements would also show whether excessive fines appear during the ramp or only during the cold hold, separating primary/secondary nucleation from later attrition or filtration-related explanations.

3. **Least effectively used observation and least reliable prediction**

The account used the intermediate particle-size result from batch 1 least effectively. Before the extra hold and filtration, particle imaging gave size about 0.056 and fines about 0.524; the final assay later gave size about 0.069 and fines about 0.500. Although the instruments and noise models differ, this was the campaign’s clearest temporal indication that continued residence could grow particles and modestly reduce fines. The report emphasized the final outcomes but did not exploit this observation enough when discussing growth during cold holds.

The least reliable held-out prediction is **Q09**. It extrapolates from multi-hour or multi-day crystallizations to only 60 seconds at 292 K. Seeds guarantee that particles may be present, but the seed-excluded product recovery should be near zero, leaving predicted purity, size and fines highly sensitive to how the initial seed population and trace deposited product are represented. No campaign batch probed this short-time, seed-dominated regime, so its intervals rely much more on qualitative assumptions than the long-ramp comparisons.
