# C-W04-Opaque — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

## Mechanistic account

### Observed material effects
The catalyst and solvent labels are anonymous benchmark identities, so the evidence supports only empirical effects, not claims about real chemical structures.

Catalyst-C0/solvent-S0 at 370 K for 1 h produced essentially complete conversion, with HPLC selectivity and reaction yield near 0.63 in batch 1. By contrast, batch 3, which changed both catalyst and solvent to C1/S1 and reacted at 350 K for 2 h, gave final selectivity about 0.45 and a higher byproduct signal of 0.406. This indicates a substantial formulation effect, but catalyst, solvent, temperature, and time were confounded; their individual contributions remain unresolved. C0/S2 in batch 7 also had lower final selectivity, about 0.49, than the initial C0/S0 regime.

The clearest crystallization material effect involved solvent-S3. Under C0 catalysis, 0.001 g seed, and staged cooling through 300 K to 280 K, batch 8 gave a final fines fraction of 0.718, versus approximately 0.99–1.00 for the tested S0, S1, and S2 processes. Batch 12 repeated the batch-8 recipe and gave 0.733 fines. This repeat supports a genuine S3-region morphology benefit, although neither result met the required limit of 0.50.

### Reaction–crystallization coupling
A useful approximate sequence is

n_target,pre ≈ n_reagent,0 · X · S,

n_target,crystal = Y_c · n_target,pre,

where X is reaction conversion, S is selectivity to target, and Y_c is the reported seed-excluded crystallization recovery. The overall isolated target relative to initial reagent would therefore scale approximately as X·S·Y_c. The official crystal-yield metric, however, is Y_c alone: recovered seed-excluded target divided by target present before separation. Consequently, a poor reaction can still show respectable crystallization recovery while delivering less absolute target product.

Reaction composition also changes crystallization indirectly. Target concentration controls supersaturation, while byproducts and degradation products can alter solubility, nucleation, growth, agglomeration, and impurity incorporation. For example, batch 3 had poorer reaction selectivity and recovered only 0.343 of its pre-separation target, whereas the C0/S0 batches reached about 0.32–0.47. This comparison is suggestive rather than causal because several operating variables differed.

Crystallization was consistently effective as a purification step: every completed batch discussed here had crystal purity above 0.96, comfortably exceeding the 0.80 requirement. Thus impurity rejection was not the limiting mechanism. Particle-number control was.

### Crystallization mechanism and process history
A qualitative population-balance description is

∂N(L,t)/∂t + ∂[G(S,t)N(L,t)]/∂L = B(S,t)δ(L−L₀) − loss terms,

with supersaturation σ = (C−C*)/C*, growth G ≈ k_gσ^g, and nucleation B ≈ k_bσ^b. If nucleation is more supersaturation-sensitive than growth, as is common, deep or rapid supersaturation can create many small crystals faster than existing crystals can grow. The characteristic size then scales roughly as

L̄ ∝ [M_crystallized/(ρN_particles)]^(1/3).

This framework explains the principal tradeoff observed: cooling generated useful recovery and high purity, but also an excessive number of sub-20 μm particles.

History mattered in several specific ways:

* In batch 2, 0.000001 g seed was accepted operationally but did not establish an effective seed population; crystallization cooling failed until another 0.001 g was added. This demonstrates a threshold-like seeding requirement.
* Batch 1 used 0.02 g seed and direct cooling to 278 K, giving recovery 0.469 and purity 0.979, but fines 0.997. Reducing seed to 0.001 g and using long staged cooling in batch 2 retained similar recovery, 0.461, but did not resolve fines.
* Long residence time alone was ineffective. Batch 6 held near 310 K for roughly 40 h after minimal effective seeding yet gave recovery 0.332 and final fines at the upper bound.
* Thermal cycling in batch 4 did not improve the distribution: recovery was 0.380 and fines remained 1.00.
* Very fine temperature staging was also ineffective. Batch 11 traversed 315–285 K in repeated small steps and gave recovery 0.382 with fines 0.994.
* Seed loading in S3 was non-monotonic. The 0.001 g recipes in batches 8 and 12 gave fines near 0.72–0.73, whereas 0.0001 g in batch 9 and 0.01 g in batch 10 both gave fines near 1.00. This is consistent with too little seed permitting uncontrolled nucleation and too much seed producing an excessive initial particle population, but those alternatives were tested only once each.

### Revisions to the working interpretation
The initial hypothesis was that slow seeded cooling would simultaneously raise recovery and suppress fines. Batches 1 and 2 contradicted the fines portion of that hypothesis. The next interpretation attributed fines mainly to deep cooling and secondary nucleation, motivating mild-temperature holds and thermal cycling; batches 4–6 did not support those remedies. The evidence then shifted attention to solvent-dependent nucleation and growth. Batches 8 and 12 supported S3 as a better morphology region, but further adjustment of seed loading or cooling granularity did not reach specification.

### Quality–recovery tradeoff and uncertainty
No completed batch met both purity ≥0.80 and fines ≤0.50. Recovery ranged from about 0.32 to 0.47 while purity remained high, but lower recovery did not reliably produce fewer fines. The closest observed region was batch 8: crystal recovery 0.415, purity 0.968, and fines 0.718. Its batch-12 replicate gave 0.401, 0.982, and 0.733, respectively. The operating recommendation remains the sealed selection of batch 8, but it must be described as noncompliant with the fines constraint.

Instrument noise was approximately 0.01 for final crystal yield and purity and 0.018 for final fines. The small batch-8/batch-12 differences are therefore not persuasive evidence of a real difference, whereas their roughly 0.27–0.28 excess above the fines limit is much larger than measurement noise. Most other recipes were single trials, and some comparisons confounded formulation with thermal history. Particle-size readings before filtration and final-assay estimates also differed modestly, so exact rankings should not be overinterpreted.

Untested alternatives include fines classification, controlled dissolution or washing after filtration, growth-promoting additives, different solvent mixtures, lower-shear crystallization, continuous seed preparation with a characterized size distribution, and feedback control based directly on particle measurements. These are mechanistically plausible routes to reduce particle number or selectively remove fines, but the campaign provides no experimental evidence for them.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.99 | 0.93 | 1 |
| Q01 | crystal_purity | 0.97 | 0.91 | 0.995 |
| Q01 | crystal_size | 0.032 | 0.015 | 0.06 |
| Q01 | crystal_yield | 0.13 | 0.03 | 0.28 |
| Q02 | crystal_fines_fraction | 0.91 | 0.7 | 1 |
| Q02 | crystal_purity | 0.97 | 0.9 | 0.995 |
| Q02 | crystal_size | 0.05 | 0.02 | 0.1 |
| Q02 | crystal_yield | 0.18 | 0.05 | 0.35 |
| Q03 | crystal_fines_fraction | 0.84 | 0.6 | 0.99 |
| Q03 | crystal_purity | 0.98 | 0.93 | 1 |
| Q03 | crystal_size | 0.085 | 0.035 | 0.15 |
| Q03 | crystal_yield | 0.17 | 0.04 | 0.34 |
| Q04 | crystal_fines_fraction | 0.99 | 0.94 | 1 |
| Q04 | crystal_purity | 0.98 | 0.93 | 1 |
| Q04 | crystal_size | 0.032 | 0.015 | 0.065 |
| Q04 | crystal_yield | 0.16 | 0.03 | 0.33 |
| Q05 | crystal_fines_fraction | 0.97 | 0.86 | 1 |
| Q05 | crystal_purity | 0.98 | 0.93 | 1 |
| Q05 | crystal_size | 0.04 | 0.018 | 0.08 |
| Q05 | crystal_yield | 0.18 | 0.05 | 0.35 |
| Q06 | crystal_fines_fraction | 0.995 | 0.95 | 1 |
| Q06 | crystal_purity | 0.97 | 0.91 | 0.995 |
| Q06 | crystal_size | 0.025 | 0.01 | 0.055 |
| Q06 | crystal_yield | 0.2 | 0.06 | 0.38 |
| Q07 | crystal_fines_fraction | 0.96 | 0.83 | 1 |
| Q07 | crystal_purity | 0.98 | 0.93 | 1 |
| Q07 | crystal_size | 0.043 | 0.019 | 0.085 |
| Q07 | crystal_yield | 0.19 | 0.05 | 0.36 |
| Q08 | crystal_fines_fraction | 0.94 | 0.77 | 1 |
| Q08 | crystal_purity | 0.985 | 0.94 | 1 |
| Q08 | crystal_size | 0.05 | 0.02 | 0.1 |
| Q08 | crystal_yield | 0.15 | 0.03 | 0.33 |
| Q09 | crystal_fines_fraction | 0.998 | 0.96 | 1 |
| Q09 | crystal_purity | 0.97 | 0.89 | 1 |
| Q09 | crystal_size | 0.025 | 0.008 | 0.055 |
| Q09 | crystal_yield | 0.045 | 0 | 0.14 |
| Q10 | crystal_fines_fraction | 0.985 | 0.9 | 1 |
| Q10 | crystal_purity | 0.975 | 0.91 | 1 |
| Q10 | crystal_size | 0.033 | 0.012 | 0.07 |
| Q10 | crystal_yield | 0.12 | 0.02 | 0.28 |
| Q11 | crystal_fines_fraction | 0.98 | 0.89 | 1 |
| Q11 | crystal_purity | 0.98 | 0.93 | 1 |
| Q11 | crystal_size | 0.038 | 0.017 | 0.075 |
| Q11 | crystal_yield | 0.18 | 0.05 | 0.35 |
| Q12 | crystal_fines_fraction | 0.91 | 0.7 | 0.99 |
| Q12 | crystal_purity | 0.965 | 0.89 | 0.995 |
| Q12 | crystal_size | 0.062 | 0.027 | 0.12 |
| Q12 | crystal_yield | 0.44 | 0.27 | 0.62 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

The intervals are epistemic predictions for noise-free states, not final-assay noise bars. Q01/Q02 isolates solvent: S3 is expected to improve growth relative to nucleation and therefore reduce fines versus S1, but the very large seed charge should still prevent feasibility. Q03/Q04 isolates seed loading: 0.001 g should distribute recovered product over fewer particles, giving larger crystals and fewer fines than 0.045 g, with little direct change in seed-excluded recovery. Q05/Q06 compares gradual and abrupt cooling at similar total duration: the abrupt plunge should give slightly faster recovery but a stronger nucleation burst, smaller particles, and more fines. Q07/Q08 tests a late thermal cycle; partial redissolution may modestly coarsen particles and improve purity, but prior cycling evidence did not show a robust fines benefit and incomplete regrowth may lower recovery. Q09/Q10 isolates cold residence time: the added two hours should increase seed-excluded recovery and growth, although the initial rapid supersaturation leaves both populations fine-rich. Q11/Q12 doubles reagent concentration: higher target concentration should markedly raise crystallization recovery and product mass per seed, increasing size, while possibly lowering purity slightly through greater coprecipitation. All recipes are predicted to form particles, but none has a central fines estimate at or below 0.50. Uncertainty is broad because these recipes extrapolate to lower concentration, catalyst-C1, unusually high relative seed loading, and much longer segmented cooling than the completed campaign.

## K2

## 1. Status of the main claims

### Supported in the tested domain
- **An effective seed population was necessary.** In batch 2, 0.000001 g seed was accepted but cooling failed the effective-seed precondition; adding 0.001 g enabled crystallization. This is a direct operational observation. Interpreting it as a physical threshold in seed number or mass is plausible but not independently measured.
- **Crystallization purified effectively but did not control particle number.** All completed batches had final crystal purity above 0.96, while fines were generally about 0.99–1.00. Batch 1, for example, gave recovery 0.469 and purity 0.979 but fines 0.997. Thus impurity rejection was directly successful, whereas the fines constraint was not.
- **The S3/0.001 g-seed region improved morphology relative to the other tested recipes.** Batch 8 gave fines 0.718, purity 0.968, and recovery 0.415; its recipe replicate, batch 12, gave 0.733, 0.982, and 0.401. The repeat supports a real recipe-region effect. Attributing it specifically to solvent-dependent nucleation or growth remains an interpretation because an exactly matched S0 control was not replicated alongside it.
- **The initial C0/S0 reaction regime performed better than the combined C1/S1 alternative tested.** Batch 1 showed essentially complete conversion and approximately 0.63 selectivity/yield, whereas batch 3 had selectivity about 0.45 and more byproduct. The direct claim is only that the complete formulations differed; separate catalyst and solvent effects were not identified.

### Contradicted or narrowed
- **“Slow seeded cooling will suppress fines” was contradicted.** Slow or staged cooling in batches 1, 2, 7, and 11 still produced excessive fines. Batch 11 used especially fine temperature staging yet ended at 0.994 fines.
- **“More time at mild supersaturation will mainly grow existing crystals” was not supported.** Batch 6 spent roughly 40 hours near 310 K but still had final fines at 1.00 and recovery 0.332.
- **“Thermal cycling will selectively dissolve fines and coarsen the population” was not supported under the tested history.** Batch 4 remained at 1.00 fines after cycling. This does not exclude a better-designed dissolution cycle.
- **A monotonic seed-loading benefit was contradicted in S3.** Batch 8 used 0.001 g and gave the best fines result, whereas 0.0001 g in batch 9 and 0.01 g in batch 10 both gave fines near 1.00. The interpretation of an intermediate seed optimum is provisional because each alternative loading was tested once.

### Still untested
The individual catalyst effect, the individual solvent effect under otherwise identical reaction histories, direct supersaturation and solubility measurements, seed-size distribution, nucleation rate, attrition, agglomeration, post-filtration classification, solvent mixtures, additives, and concentration dependence remain untested. It is also unresolved whether the S3 benefit arose primarily during the first cooling stage, the deep-cooling stage, or filtration. No tested process resolved the recovery–fines tradeoff while maintaining fines at or below 0.50.

## 2. One additional experiment

I would repeat the batch-8 S3/C0/0.001 g-seed process as a single time-resolved experiment, taking non-destructive particle-size measurements immediately after effective seeding, after reaching 300 K, after the 300 K hold, after reaching 280 K, and after the final cold hold. Small liquid samples for HPLC at the same stages would estimate target depletion. A final measurement after filtration would complete the comparison.

This would distinguish several competing explanations:
- **Secondary nucleation during deep cooling:** fines would be relatively low at 300 K but jump during the 300→280 K stage as target leaves solution.
- **Small inherited seeds with growth limitation:** fines would already be high immediately after seeding and would decline slowly, if at all, while size rose with target depletion.
- **Shear-driven attrition:** fines would increase during isothermal stirred holds even without a major change in target concentration.
- **Filtration or measurement-context effects:** the in-situ slurry could look acceptable while the post-filtration final assay deteriorated.

A low-fines population at 300 K followed by a sharp low-temperature deterioration would support stopping or controlling the second cooling stage. Persistently high fines from the first measurement would instead direct work toward seed preparation or particle classification. Growth without a fines increase but little target depletion would indicate insufficient supersaturation rather than excessive nucleation.

## 3. Weakest use of evidence and least reliable prediction

The account used the differences between in-situ particle measurements and post-filtration final assays least effectively. For example, batch 8 had in-situ fines 0.731 and final fines 0.718, while other batches showed larger size or fines shifts between the two contexts. I mentioned these discrepancies as uncertainty but did not systematically use them to separate true process evolution, filtration effects, and instrument-context differences. The proposed time-resolved experiment addresses that weakness.

The least reliable held-out prediction is **Q02**. Its predicted S3 morphology advantage extrapolates the batch-8/batch-12 result from catalyst C0 and 0.001 g seed to catalyst C1, 0.045 g seed, lower charge concentration, and a much longer cooling history. The campaign contained no C1/S3 experiment and showed that the S3 benefit was highly seed-dependent: 0.01 g already performed poorly in batch 10. Therefore the direction of the Q01/Q02 solvent contrast was mechanistically plausible, but its magnitude—especially for crystal size and fines—was weakly constrained.
