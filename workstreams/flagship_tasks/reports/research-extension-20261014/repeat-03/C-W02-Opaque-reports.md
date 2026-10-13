# C-W02-Opaque — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

## Mechanistic account

### 1. Material effects

The catalyst and solvent labels are anonymous benchmark identities, so the evidence supports process-specific comparisons, not real-substance assignments.

The initial paired screen showed large material effects. At the common reaction condition of 370 K for 3600 s, C0/S0 gave the strongest reaction result in batch 1 (reaction yield 0.702, selectivity 0.704), followed by C1/S1 in batch 2 (0.619 and 0.631). C2/S2 and C3/S3 were weaker in batches 3 and 4. However, catalyst and solvent were changed together, so their individual effects remain unresolved.

A more informative comparison is batches 2 and 5, which used essentially the same 0.005 g seed, slow cooling to 300 K, and growth hold but different material pairs. C1/S1 in batch 2 produced recovery 0.472, purity 0.986, and fines 0.418. C0/S0 in batch 5 gave similar recovery, 0.468, and purity 0.969, but fines rose to 0.750. Thus, the material pair strongly affected nucleation, aggregation, or crystal growth independently of bulk recovery. This result caused the main revision in the campaign: C0/S0 was initially favored because of its reaction performance, but C1/S1 became the preferred crystallization medium because it controlled fines.

Possible explanations include solvent-dependent target solubility, interfacial energy, seed wetting, growth-face kinetics, or agglomeration. A catalyst-derived impurity could also alter nucleation. These alternatives were not separated because C1 was not crossed systematically with every solvent, nor S1 with every catalyst.

### 2. Reaction–crystallization coupling

A useful approximate reaction description is

X = 1 - n_R/n_R,0,

S_rxn = n_T/(n_T+n_B),

Y_rxn ≈ X S_rxn,

where R, T, and B denote reactant, target, and byproduct. The amount of target entering crystallization is then approximately n_T,pre = n_R,0 Y_rxn.

The reported crystal recovery has a different denominator:

R_c = n_T,recovered,seed-excluded / n_T,pre.

Consequently, high crystallization recovery does not imply high overall yield from reagent. An approximate overall recovered-target fraction is Y_rxn R_c. It was about 0.386 in noncompliant batch 1, 0.293 in batch 2, 0.357 in batch 11, and 0.376 in recommended batch 12. Batch 12 was selected because the stated objective maximized R_c subject to crystal-quality constraints, not because it necessarily maximized total recovered target from the initial reagent.

Reaction composition can nevertheless affect crystallization through target concentration, impurity adsorption, and supersaturation. For example, batch 1 combined strong reaction yield with high fines, while C1/S1 batches had slightly lower reaction yield but much better particle control. In the repeated C1/S1 series, measured reaction yield varied roughly from 0.608 to 0.633 despite nominally common reaction conditions. Because cooling occurs after reaction and assay noise is present, those modest differences should not be attributed mechanistically to final cooling temperature.

### 3. Crystallization mechanism and process history

A useful driving-force variable is relative supersaturation,

σ = C/C*(T) - 1,

where C*(T) is equilibrium solubility. Primary or secondary nucleation commonly rises much more sharply with σ than growth does; schematically,

J ∝ exp[-A/{T³ ln²(1+σ)}],  and  G = k_g σ^g.

These are interpretive relationships, not fitted laws for this benchmark. They explain why a slow ramp and existing seed can direct solute toward growth rather than a burst of new fine particles. A subsequent low-agitation hold can provide additional growth or ripening time while limiting attrition.

Batch 1 illustrates adverse history: 0.020 g seed followed by relatively rapid, deep cooling to 278 K over 7200 s gave recovery 0.550 and purity 0.981, but fines 0.877 and an inferred d50 of only about 14 µm. The higher seed charge, faster cooling, deeper endpoint, shorter total aging history, and different material pair were all confounded, so the high fines cannot be assigned to one factor alone.

Batch 2 used only 0.005 g seed, cooling to 300 K over 14400 s, and a 7200 s hold. It met both constraints, with fines 0.418 and purity 0.986. This supported the original hypothesis that slow seeded cooling would suppress fines.

Within the more controlled C1/S1 sequence, batches 6–10 used 0.005 g seed, a 14400 s cooling step, and a 14400 s low-agitation hold. Lowering the endpoint produced the following observed recovery/fines pairs:

- Batch 6, 295 K: 0.511 / 0.407
- Batch 7, 290 K: 0.532 / 0.396
- Batch 8, 285 K: 0.550 / 0.374
- Batch 9, 280 K: 0.552 / 0.415
- Batch 10, 275 K: 0.564 / 0.404

Recovery therefore increased with deeper cooling, consistent with reduced mother-liquor solubility. Fines did not increase monotonically over this range; their scatter is compatible with measurement/process variability or competing growth and secondary-nucleation effects. All five batches retained purity above 0.98.

Batches 11 and 12 reduced seed to 0.002 g while retaining the long cooling and hold history. Batch 11 at 265 K gave recovery 0.572, purity 0.998, and fines 0.399. Batch 12 at 250 K gave the highest observed compliant recovery, 0.593, with purity 0.999 and fines 0.471. Its normalized crystal-size result corresponds to an approximate d50 of 25 µm. The low seed charge plausibly reduced the number of initial growth centers, leaving more target available per particle, but this interpretation is unproven because seed dose and endpoint were changed together.

### 4. Revisions and uncertainty

The first revision was from reaction-led selection to morphology-led material selection: batch 5 showed that transferring the gentle batch-2 profile to C0/S0 did not solve its fines problem. The second revision was that deeper cooling in C1/S1 did not immediately incur the expected fines penalty; batches 6–10 showed increasing recovery with broadly stable fines. The final revision was qualified rather than categorical: batch 12 maximized observed recovery, but it approached the fines boundary.

The final-assay standard deviations were declared as 0.010 for crystal recovery, 0.010 for purity, and 0.018 for fines. Batch 12's fines margin, 0.500−0.471 = 0.029, is only about 1.6 assay standard deviations. Batch 11's margin is about 0.101, or 5.6 standard deviations. Meanwhile, the recovery difference between batches 12 and 11 is 0.021, only about 1.5 combined recovery standard deviations. Thus batch 12 is the correct observed-data choice for maximum compliant recovery, but batch 11 is the more robust quality-margin alternative. No replicate establishes that the recovery difference is reproducible.

The unresolved quality/recovery tradeoff is therefore concentrated below 265 K: deeper cooling appears to recover more target, while the 250 K observation suggests a renewed increase in fines. Replication of batches 11 and 12, fixed-temperature seed-dose experiments, crossed catalyst/solvent tests, and staged cooling or annealing would be needed to distinguish true effects from noise and to preserve batch-12 recovery with a larger fines margin.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.27 | 0.14 | 0.43 |
| Q01 | crystal_purity | 0.98 | 0.94 | 1 |
| Q01 | crystal_size | 0.22 | 0.13 | 0.33 |
| Q01 | crystal_yield | 0.52 | 0.4 | 0.63 |
| Q02 | crystal_fines_fraction | 0.72 | 0.55 | 0.87 |
| Q02 | crystal_purity | 0.985 | 0.95 | 1 |
| Q02 | crystal_size | 0.09 | 0.04 | 0.17 |
| Q02 | crystal_yield | 0.31 | 0.18 | 0.46 |
| Q03 | crystal_fines_fraction | 0.2 | 0.08 | 0.38 |
| Q03 | crystal_purity | 0.975 | 0.93 | 1 |
| Q03 | crystal_size | 0.34 | 0.2 | 0.5 |
| Q03 | crystal_yield | 0.43 | 0.28 | 0.57 |
| Q04 | crystal_fines_fraction | 0.43 | 0.27 | 0.6 |
| Q04 | crystal_purity | 0.975 | 0.93 | 1 |
| Q04 | crystal_size | 0.16 | 0.09 | 0.25 |
| Q04 | crystal_yield | 0.51 | 0.39 | 0.63 |
| Q05 | crystal_fines_fraction | 0.36 | 0.21 | 0.53 |
| Q05 | crystal_purity | 0.974 | 0.93 | 1 |
| Q05 | crystal_size | 0.18 | 0.1 | 0.29 |
| Q05 | crystal_yield | 0.51 | 0.39 | 0.63 |
| Q06 | crystal_fines_fraction | 0.62 | 0.45 | 0.78 |
| Q06 | crystal_purity | 0.969 | 0.92 | 1 |
| Q06 | crystal_size | 0.09 | 0.04 | 0.17 |
| Q06 | crystal_yield | 0.53 | 0.4 | 0.65 |
| Q07 | crystal_fines_fraction | 0.32 | 0.18 | 0.49 |
| Q07 | crystal_purity | 0.976 | 0.94 | 1 |
| Q07 | crystal_size | 0.2 | 0.11 | 0.32 |
| Q07 | crystal_yield | 0.52 | 0.4 | 0.64 |
| Q08 | crystal_fines_fraction | 0.23 | 0.1 | 0.42 |
| Q08 | crystal_purity | 0.982 | 0.94 | 1 |
| Q08 | crystal_size | 0.27 | 0.14 | 0.43 |
| Q08 | crystal_yield | 0.47 | 0.32 | 0.61 |
| Q09 | crystal_fines_fraction | 0.86 | 0.68 | 0.97 |
| Q09 | crystal_purity | 0.96 | 0.88 | 1 |
| Q09 | crystal_size | 0.045 | 0.015 | 0.09 |
| Q09 | crystal_yield | 0.015 | 0 | 0.06 |
| Q10 | crystal_fines_fraction | 0.66 | 0.47 | 0.83 |
| Q10 | crystal_purity | 0.965 | 0.9 | 1 |
| Q10 | crystal_size | 0.08 | 0.035 | 0.15 |
| Q10 | crystal_yield | 0.13 | 0.05 | 0.24 |
| Q11 | crystal_fines_fraction | 0.37 | 0.22 | 0.54 |
| Q11 | crystal_purity | 0.976 | 0.93 | 1 |
| Q11 | crystal_size | 0.17 | 0.09 | 0.28 |
| Q11 | crystal_yield | 0.52 | 0.4 | 0.64 |
| Q12 | crystal_fines_fraction | 0.61 | 0.43 | 0.78 |
| Q12 | crystal_purity | 0.95 | 0.88 | 0.99 |
| Q12 | crystal_size | 0.1 | 0.045 | 0.19 |
| Q12 | crystal_yield | 0.69 | 0.56 | 0.8 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

All recipes contain added seed, so particles are expected even when seed-excluded product recovery is very small. Q01/Q02 predicts that solvent S1 retains the favorable particle behavior observed during the campaign, whereas S3 gives lower recovery and many fines. Q03/Q04 assigns the small seed charge fewer, larger particles but slower recovery; the large seed charge accelerates capture while increasing number-weighted fines. Q05/Q06 predicts similar eventual recovery but strong history dependence: gradual cooling limits secondary nucleation, while the rapid temperature drop leaves a finer population despite the long hold. Q07/Q08 treats the 315 K cycle as partial fines dissolution and ripening, improving size and fines at the cost of some unrecovered dissolved target. Q09/Q10 predicts that the additional 292 K hold permits measurable growth and recovery but remains too short and shallow for a compliant size distribution. Q11/Q12 predicts that doubling reagent concentration raises supersaturation and recovery but also secondary nucleation and impurity inclusion, making Q12 fines-limited. Intervals are deliberately broad because these recipes extrapolate beyond the tested charge scale, seed loading, 385 K quenched reaction, and exceptionally long multistage cooling histories; several feasibility calls near the 0.50 fines boundary are therefore uncertain.

## K2

## 1. Status of the main claims

### Supported by direct observations

- **Material pair strongly affects crystallization behavior.** Batches 2 and 5 used nearly the same seed charge and 300 K cooling/hold profile. C1/S1 in batch 2 gave fines 0.418, whereas C0/S0 in batch 5 gave 0.750, at similar crystal recoveries of 0.472 and 0.468. The difference is directly observed; attributing it specifically to solubility, interfacial energy, or impurity adsorption is interpretation.
- **C1/S1 provided a reproducible feasible operating region.** Batches 6–12 all had purity above 0.98 and fines below 0.50. This directly supports selecting that pair for constrained crystallization.
- **Deeper cooling increased recovery within the tested C1/S1 sequence.** Recovery rose from 0.511 at 295 K in batch 6 to 0.564 at 275 K in batch 10 under otherwise similar seeded, slow-cooling histories. Batches 11 and 12 extended the numerical trend to 0.572 at 265 K and 0.593 at 250 K, although their smaller seed charge introduces a confound.
- **Purity was not the active constraint in the optimized region.** Batches 6–12 remained at approximately 0.982–1.000 purity. Fines, rather than purity, determined proximity to infeasibility.

### Partly supported but confounded

- **Slow seeded cooling suppresses fines.** Batch 1, with a faster/deeper cooling history and 0.020 g seed, had fines 0.877; batch 2, with 0.005 g seed and slow cooling plus a hold, had fines 0.418. This is consistent with the claim but does not isolate cooling rate: material pair, seed amount, endpoint, and aging time all changed.
- **The 250 K endpoint introduces a recovery–fines tradeoff.** Batch 12 had the highest recovery, 0.593, but fines increased to 0.471 from 0.399 in batch 11. This is a direct numerical comparison, but the recovery difference is modest relative to assay uncertainty, and endpoint and seed history were not independently replicated.
- **Lower seed loading favors larger or cleaner particles.** Batch 11 used 0.002 g seed and was feasible, but it also used a different endpoint from the 0.005 g-seed batches. A seed-dose effect therefore remains an interpretation rather than an isolated result.

### Contradicted or revised

- **The initially favored reaction pair would also be the best complete process.** Batch 1 showed that C0/S0 had the strongest observed reaction result, but batch 5 showed that its poor fines behavior persisted under a gentler crystallization profile. This contradicted the initial reaction-led selection strategy and motivated prioritizing C1/S1.
- **Deeper cooling would necessarily cause a monotonic fines increase.** Batches 6–10 did not show that pattern: fines fluctuated between about 0.374 and 0.415 while recovery increased. A sharp monotonic relationship was therefore contradicted over 295–275 K, although a penalty may begin at still lower temperature.

### Still untested

- The separate causal effects of catalyst and solvent, because the initial screen changed them in pairs.
- Whether solvent effects arise from solubility, growth-face kinetics, seed wetting, agglomeration, or catalyst-derived impurities.
- Replicability of batches 11 and 12 and the true significance of their recovery difference.
- Independent seed-dose, cooling-rate, agitation, concentration, and temperature-cycle effects.
- Whether staged annealing can preserve batch-12 recovery while increasing the fines margin.

## 2. Best single additional experiment

I would run **C0/S1 under the exact batch-2/batch-5 crystallization protocol**: the same reagent and catalyst amounts used in the campaign, 370 K for 3600 s, 0.005 g seed, cooling to 300 K over 14400 s, a 7200 s hold at the same agitation, filtration, and final assay. A pre-crystallization HPLC measurement would be included if the measurement allowance permitted it.

This cross-over would distinguish three explanations for the batch-2/batch-5 morphology difference:

1. **Solvent-dominant explanation:** C0/S1 should resemble batch 2, with fines near 0.42 and feasible purity. That would implicate S1-dependent solubility or crystal-surface kinetics despite using C0.
2. **Catalyst or catalyst-derived impurity explanation:** C0/S1 should resemble batch 5, with fines near 0.75. That would indicate that C0 or its reaction mixture governs nucleation or aggregation even in S1.
3. **Catalyst–solvent interaction:** an intermediate or qualitatively different result would show that neither main effect alone explains the behavior.

Recovery is less discriminating because batches 2 and 5 both gave about 0.47; particle size and fines are the primary diagnostic outputs. One cross-over cannot fully estimate both main effects and their interaction, but it provides the greatest causal discrimination against the existing two reference batches.

## 3. Least effectively used observation and least reliable prediction

### Underused observation

**Batch 3 was used least effectively.** It had poor reaction yield and crystal recovery—about 0.426 and 0.339—but also the lowest observed fines fraction, 0.278, high CSD quality of about 0.752, and purity about 0.988. My account emphasized its weak reaction performance and did not sufficiently exploit the fact that C2/S2 may be a strong morphology-control system. That observation reinforces reaction–crystallization decoupling and suggests that a crossed or concentration-adjusted C2/S2 process might trade reaction productivity for exceptional particle quality. Because C2 and S2 were paired, the responsible material remains unknown.

The paid intermediate particle-size observations were also not used quantitatively; the account relied mainly on final-assay particle metrics. Comparing in-situ and final values could have helped separate crystallization history from filtration or assay variability.

### Least reliable held-out prediction

**Q08 is the least reliable prediction.** It predicted that reheating an established slurry to 315 K and recooling would dissolve fines, increase normalized size, and reduce fines at the cost of some recovery. No campaign batch included a dissolution–recrystallization temperature cycle. The outcome depends on unknown solubility at 315 K, the fraction of crystals that survive as seeds, dissolution selectivity by particle size, possible aggregation or polymorphic change, and whether the one-hour recooling step causes renewed nucleation. The opposite result—substantial dissolution followed by a fine-particle burst and reduced recovery—is also plausible. Its intervals therefore may still understate structural uncertainty.
