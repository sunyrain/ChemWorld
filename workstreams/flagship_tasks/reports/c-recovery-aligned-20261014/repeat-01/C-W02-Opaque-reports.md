# C-W02-Opaque — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

## Mechanistic account

The materials are anonymous benchmark identities, so the mechanism can only be phenomenological; no real molecular identities or solvent properties were supplied.

### Recommended process and observations

Batch 12 used 0.040 mol reagent, 0.080 L solvent S1, and 0.005 mol catalyst C0. It was heated at 370 K for 3,600 s with 500 rpm stirring, seeded with 0.010 g, cooled to 280 K over 14,400 s, filtered, and assayed without a subsequent cold hold. Its final assay showed complete measured conversion, reaction yield 0.686, byproduct signal 0.224, seed-excluded crystal recovery 0.584, crystal purity 0.991, fines number fraction 0.416, and normalized crystal size 0.101—equivalent to an estimated number-weighted d50 of about 25.3 µm. It therefore met both constraints with useful margins.

### Material effects

**Catalyst effect.** In S1 under the initial 380 K reaction and common 300 K crystallization history, C0 gave the best feasible recovery: batch 2 reached 0.512. C1 gave 0.493 with fines 0.492 (batch 6), C2 gave 0.388 with fines 0.564 (batch 7), and C3 gave 0.448 with fines 0.477 (batch 8). Their reaction yields were respectively 0.673, 0.625, 0.518, and 0.558. I interpret C0 as providing the best balance of target formation and byproduct suppression in this tested region. Because each combination was run once, this is an empirical ranking rather than a universal catalytic law.

**Solvent effect.** Solvent identity strongly affected particle formation, not merely chemical conversion. With C0 and a similar seeded slow-cooling/hold history, S1 produced fines 0.424 and recovery 0.512 (batch 2), while S2 produced very low fines, 0.285, but recovery 0.494 (batch 4). S0 and S3 gave excessive fines: 0.790 in batch 3 and 0.752 in batch 5. S0 could still deliver substantial recovery—0.551 in batch 1 after deeper cooling—but its fines were 0.750. Thus S1 was the best observed recovery/quality compromise, whereas S2 favored morphology and remains a plausible unoptimized alternative.

A likely interpretation is that solvent-dependent solubility and nucleation kinetics controlled whether supersaturation fed growth on existing particles or generated many new nuclei. The data do not identify which physical solvent property caused this behavior.

### Reaction–crystallization coupling

The measured overall recovery is

Y_crystal = n(target in recovered solid, excluding seed) / n(initial reagent).

A useful phenomenological decomposition is

Y_crystal ≈ Y_reaction × f_capture,

where Y_reaction is the assay target yield and f_capture represents crystallization and separation capture. This is not a fitted kinetic law, but it clarifies the two limitations. The empirical ratios Y_crystal/Y_reaction increased from about 0.760 in batch 2 to 0.779, 0.814, 0.835, and 0.851 in batches 9–12. This is consistent with progressively deeper cooling increasing capture of the target already produced by the reaction.

Chemical selectivity and crystallization selectivity were distinct. Reaction selectivity was only about 0.68–0.72 in several C0 batches, yet recovered-crystal purity was generally 0.98–0.99. I interpret this as preferential incorporation of target into the solid and rejection of reaction impurities into the mother liquor. Conversely, byproducts can still affect supersaturation, nucleation, and morphology even when the isolated solid remains chemically pure.

### Process-history dependence

The original expectation was that seeding plus slow cooling would generally suppress fines. The solvent screen revised that view: the same broad strategy worked for S1 and S2 but failed for S0 and S3, demonstrating that thermal history cannot be interpreted independently of solvent.

The initial feasible S1 process used 0.050 g seed, slow cooling to 300 K, and a 14,400 s hold. Batch 2 gave recovery 0.512 and fines 0.424. Removing the long hold and cooling farther improved observed recovery: batch 9, with 0.050 g seed and a 295 K endpoint, gave 0.553 recovery and 0.453 fines. With 0.010 g seed, batch 10 at 290 K gave 0.570 recovery and 0.448 fines, while batch 11 at 285 K gave 0.575 and 0.428. Batch 12 at 280 K gave 0.584 and 0.416.

This sequence supports deeper, slow cooling without an extended hold, but it does not isolate every causal variable: endpoint, seed dose, and—in batch 12—reaction temperature changed across the sequence. The long hold may have allowed additional degradation or byproduct formation, but the higher recovery of later batches could also be explained simply by their lower endpoints.

Changing the reaction temperature from 380 K in batch 11 to 370 K in batch 12 maintained complete measured conversion and nearly unchanged reaction yield (0.689 versus 0.686), while the byproduct signal decreased from 0.245 to 0.224. However, batch 12 also cooled 5 K farther, so its higher crystal recovery cannot be attributed uniquely to the milder reaction.

### Revisions, uncertainty, and unresolved tradeoffs

The study progressed from a generic seeding hypothesis, to recognition of strong solvent-dependent nucleation, to catalyst selection, and finally to joint reaction/cooling optimization. Batch 12 remains the recommended empirical recipe because it had the highest observed recovery satisfying both constraints.

There were no true replicates. Final-assay noise scales were approximately 0.010 for crystal recovery and purity and 0.018 for fines, with additional process uncertainty. Consequently, the small recovery differences among batches 10–12 should be viewed as a high-performing plateau rather than proof of a precisely monotonic temperature effect. Batch 12 nevertheless had comfortable constraint margins: purity was about 0.191 above its minimum and fines about 0.084 below its maximum.

The principal unresolved tradeoff is between deeper cooling, which can increase capture, and secondary nucleation, which can increase the number fraction of fines. S1 happened to remain feasible through 280 K in the tested history, but still produced more fines than S2. An optimized S2 process with deeper cooling might potentially combine its morphology advantage with higher recovery, but that alternative was not tested. Also untested were independent reaction-temperature bracketing, seeding at a controlled lower temperature, replicated seed-dose comparisons, staged cooling profiles, solvent mixtures, reduced solvent volume, and post-crystallization washing or resuspension.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.37 | 0.23 | 0.52 |
| Q01 | crystal_purity | 0.97 | 0.91 | 0.995 |
| Q01 | crystal_size | 0.11 | 0.06 | 0.18 |
| Q01 | crystal_yield | 0.37 | 0.27 | 0.47 |
| Q02 | crystal_fines_fraction | 0.72 | 0.57 | 0.84 |
| Q02 | crystal_purity | 0.95 | 0.87 | 0.99 |
| Q02 | crystal_size | 0.055 | 0.025 | 0.11 |
| Q02 | crystal_yield | 0.29 | 0.19 | 0.39 |
| Q03 | crystal_fines_fraction | 0.39 | 0.24 | 0.55 |
| Q03 | crystal_purity | 0.97 | 0.91 | 0.995 |
| Q03 | crystal_size | 0.16 | 0.09 | 0.25 |
| Q03 | crystal_yield | 0.35 | 0.25 | 0.45 |
| Q04 | crystal_fines_fraction | 0.58 | 0.43 | 0.72 |
| Q04 | crystal_purity | 0.97 | 0.91 | 0.995 |
| Q04 | crystal_size | 0.07 | 0.035 | 0.13 |
| Q04 | crystal_yield | 0.36 | 0.26 | 0.46 |
| Q05 | crystal_fines_fraction | 0.43 | 0.28 | 0.58 |
| Q05 | crystal_purity | 0.975 | 0.92 | 0.998 |
| Q05 | crystal_size | 0.105 | 0.055 | 0.18 |
| Q05 | crystal_yield | 0.36 | 0.26 | 0.46 |
| Q06 | crystal_fines_fraction | 0.72 | 0.57 | 0.84 |
| Q06 | crystal_purity | 0.96 | 0.89 | 0.995 |
| Q06 | crystal_size | 0.052 | 0.022 | 0.105 |
| Q06 | crystal_yield | 0.37 | 0.27 | 0.47 |
| Q07 | crystal_fines_fraction | 0.45 | 0.3 | 0.6 |
| Q07 | crystal_purity | 0.97 | 0.91 | 0.997 |
| Q07 | crystal_size | 0.1 | 0.05 | 0.17 |
| Q07 | crystal_yield | 0.36 | 0.26 | 0.46 |
| Q08 | crystal_fines_fraction | 0.28 | 0.16 | 0.43 |
| Q08 | crystal_purity | 0.985 | 0.94 | 1 |
| Q08 | crystal_size | 0.145 | 0.08 | 0.23 |
| Q08 | crystal_yield | 0.34 | 0.24 | 0.44 |
| Q09 | crystal_fines_fraction | 0.68 | 0.51 | 0.82 |
| Q09 | crystal_purity | 0.94 | 0.84 | 0.99 |
| Q09 | crystal_size | 0.04 | 0.015 | 0.09 |
| Q09 | crystal_yield | 0.035 | 0.005 | 0.1 |
| Q10 | crystal_fines_fraction | 0.49 | 0.33 | 0.65 |
| Q10 | crystal_purity | 0.96 | 0.89 | 0.995 |
| Q10 | crystal_size | 0.085 | 0.04 | 0.15 |
| Q10 | crystal_yield | 0.24 | 0.13 | 0.35 |
| Q11 | crystal_fines_fraction | 0.52 | 0.37 | 0.67 |
| Q11 | crystal_purity | 0.97 | 0.91 | 0.997 |
| Q11 | crystal_size | 0.075 | 0.035 | 0.14 |
| Q11 | crystal_yield | 0.35 | 0.25 | 0.45 |
| Q12 | crystal_fines_fraction | 0.48 | 0.32 | 0.64 |
| Q12 | crystal_purity | 0.94 | 0.85 | 0.99 |
| Q12 | crystal_size | 0.1 | 0.05 | 0.18 |
| Q12 | crystal_yield | 0.29 | 0.18 | 0.4 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

Q01–Q02: S1 is expected to retain the markedly better recovery and morphology observed relative to S3, while both remain chemically selective during crystallization. Q03–Q04: at this small reagent charge, 0.001 g seed is near the previously successful seed-to-reagent ratio; 0.045 g distributes limited product over many seed particles, lowering number-weighted size and raising fines. Q05–Q06: gradual cooling should limit primary nucleation, whereas the 120 s crash should create persistent fines despite the long cold residence; equilibrium recovery should be similar. Q07–Q08: the 315 K temperature cycle should preferentially dissolve small particles and permit regrowth on recooling, improving size, fines, and purity with a modest recovery penalty. Q09–Q10: seeds ensure particles are present in both, but 60 s permits little seed-excluded deposition; the additional 2 h at 292 K substantially increases capture and growth. Q11–Q12: doubling reagent at fixed catalyst lowers catalyst-to-reagent ratio and therefore predicted fractional recovery, although the greater product mass per seed should modestly increase size and reduce seed-dominated fines. Intervals are broad because all recipes extrapolate far beyond the tested residence times and loadings; fines classifications near 0.50, especially Q10–Q12, are correspondingly uncertain.

## K2

Retained failure: provider_failure
