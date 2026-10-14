# C-W03-MisIndexed — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

Mechanistic account

The recommended process remains Batch 12: 0.040 mol reagent, 0.080 L solvent S2, 0.005 mol catalyst C1, reaction at 350 K for 1,800 s with 500 rpm stirring, addition of 0.020 g seed, one 14,400 s crystallization stage to 265 K, filtration, and final assay. It delivered the highest observed compliant seed-excluded crystal yield, 0.571, with purity 0.995 and fines number fraction 0.424.

Material effects

The material dossier described S2 as relatively low-solubility (0.7), low-nucleation (0.65), high-growth (1.3), and low-impurity-occlusion (0.65). These properties provide a plausible explanation for the consistently high filtered-solid purity observed with S2: final purities were generally about 0.98–1.00. However, every completed batch used S2, so this solvent mechanism is an interpretation consistent with the prior, not an experimentally demonstrated comparison against S0, S1, or S3.

Catalyst identity clearly affected the reaction. At 340 K for 1,800 s, HPLC gave approximately:
- Batch 2, C1: conversion 0.985, selectivity 0.611, liquid target yield 0.581.
- Batch 3, C0: conversion 0.998, selectivity 0.582, yield 0.582.
- Batch 4, C2: conversion 1.000, selectivity 0.480, yield 0.488.
- Batch 5, C3: conversion 0.997, selectivity 0.612, yield 0.602.

Thus C2 was inferior for target formation in this tested condition, while C1 and C3 were stronger candidates. Catalyst choice also changed the downstream particle outcome, but that effect is confounded with differences in crystallization history and reaction-mixture composition. C2 in Batch 4 gave relatively low crystal recovery (0.399) but compliant fines (0.390), illustrating a quality/recovery tradeoff rather than a universally poor result.

Reaction–crystallization coupling

A useful reaction approximation is

Y_liquid ≈ X × S,

where X is conversion and S is target selectivity. Downstream,

Y_crystal = n(target in filtered solid, excluding seed) / n(initial reagent),

and it is useful to write

Y_crystal ≈ Y_liquid × f_cryst,

where f_cryst combines crystallization recovery and separation retention. Based on final-assay target yield, the apparent f_cryst values were about 0.888 for Batch 12, 0.860 for Batch 10, 0.876 for Batch 11, and 0.852 for Batch 1. These are descriptive ratios, not independently measured equilibrium recoveries, and assay noise or reaction continuing after an earlier HPLC measurement can affect them.

The experiments showed that maximizing liquid-phase target production did not automatically produce acceptable particles. With C1 at 340 K for 900 s, Batch 6 HPLC showed conversion 0.979, selectivity 0.663, and liquid yield 0.638—better reaction selectivity than the more severe conditions. Nevertheless, its final crystal yield of 0.544 came with fines of 0.619. Related Batches 7–9 also had fines of 0.594, 0.589, and 0.602 despite changes in seed dose, reheating, or endpoint temperature.

In contrast, the intermediate C1 condition of 350 K for 1,800 s established a repeatable feasible window:
- Batch 10, cooling to 275 K: crystal yield 0.560, purity 0.979, fines 0.430.
- Batch 11, cooling to 270 K: crystal yield 0.560, purity 0.994, fines 0.414.
- Batch 12, cooling to 265 K: crystal yield 0.571, purity 0.995, fines 0.424.

My interpretation is that reaction severity changed not just target concentration but the impurity/byproduct environment that controls nucleation and growth. High target supersaturation after the mild, selective reaction may have promoted many small particles. A somewhat more severe reaction may have lowered effective supersaturation or introduced species that inhibited primary/secondary nucleation sufficiently to permit growth-dominated crystallization. This is plausible but unproven because target concentration and impurity identity were not independently manipulated.

A standard qualitative framework is

σ = C/C*(T,composition) − 1,
J ∝ kJ σ^m,
G ∝ kG σ^g,

where σ is supersaturation, J is nucleation rate, and G is crystal growth rate. Fines increase when nucleation dominates growth. Both the solubility C* and coefficients kJ and kG can depend on solvent, impurities, catalyst residues, and temperature history. The final crystal-size distribution is therefore a functional of the whole trajectory—CSD_final = F[T(t), σ(t), agitation, seed state, composition]—rather than of endpoint temperature alone.

Process-history dependence

History effects were strong and sometimes non-monotonic. Two consecutive cold stages produced excessive fines: Batch 2, with two 14,400 s stages at 260 K, gave recovery 0.530 but fines 0.654; Batch 3, with two stages at 275 K, gave recovery 0.502 and fines 0.644. These results are consistent with prolonged supersaturation causing secondary nucleation.

Batch 1 was an important exception. Its more severe 360 K/3,600 s reaction had full conversion, HPLC selectivity 0.584, and appreciable byproduct signal 0.324. After cooling to 275 K, an in-process particle measurement already showed fines 0.319. A subsequent warm drift and recooling still ended with recovery 0.468, purity 0.987, and fines 0.295. Thus thermal cycling is not intrinsically harmful; its effect depends on the mixture entering crystallization.

A deliberate rescue attempt in Batch 7 did not work. Fines were about 0.608 before a 300 K reheat/280 K recool and about 0.608 afterward, while normalized crystal size decreased in the intervening particle measurement. This argues against assuming that mild reheating will selectively dissolve fines under these conditions.

Seed amount alone also did not explain quality. Batch 6 used 0.050 g seed and still had fines 0.619; Batch 7 used 0.005 g and finished at 0.594. The successful Batches 10–12 used 0.020 g, but Batch 5 also used 0.020 g and had fines 0.649. Seed dose therefore interacted with upstream composition and supersaturation rather than acting as a simple monotonic control.

Revisions and uncertainty

The initial hypothesis favored C1/S2 and slow seeded cooling, which was partly supported. It was revised after catalyst screening to reject C2 as the best recovery catalyst and after Batches 2–9 to recognize that reaction selectivity, seed loading, or warmer crystallization endpoints alone did not guarantee low fines. The final revision identified the 350 K/1,800 s C1 reaction as an intermediate-severity window that repeatedly balanced recovery and particle quality.

Differences among Batches 10–12 are small. Final-assay noise is approximately 0.01 for crystal yield, 0.01 for purity, and 0.018 for fines, in addition to process variability. Consequently, the apparent 0.011 yield advantage of Batch 12 over Batches 10–11 is not strong evidence for a monotonic benefit of cooling from 275 to 265 K. Batch 12 is retained because it is the highest observed compliant batch, while Batches 10 and 11 provide evidence that the broader operating window is reproducible.

The remaining quality/recovery tradeoff is unresolved near the fines limit. Colder or longer crystallization might raise recovery but risks renewed nucleation; a warmer endpoint did not solve fines for the 340 K/900 s reaction. Untested alternatives include other solvents or solvent mixtures, staged cooling ramps rather than a single endpoint, controlled aging without ambient drift, crystallization agitation changes, seed-size or polymorph control, washing conditions, and independently varying impurity concentration. These alternatives could distinguish whether the observed coupling arises mainly from supersaturation, impurity-mediated nucleation inhibition, catalyst residues, or an unobserved solid-form effect.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.52 | 0.37 | 0.68 |
| Q01 | crystal_purity | 0.9 | 0.81 | 0.97 |
| Q01 | crystal_size | 0.09 | 0.04 | 0.16 |
| Q01 | crystal_yield | 0.52 | 0.39 | 0.64 |
| Q02 | crystal_fines_fraction | 0.39 | 0.26 | 0.53 |
| Q02 | crystal_purity | 0.95 | 0.87 | 0.99 |
| Q02 | crystal_size | 0.13 | 0.07 | 0.21 |
| Q02 | crystal_yield | 0.49 | 0.37 | 0.6 |
| Q03 | crystal_fines_fraction | 0.68 | 0.52 | 0.82 |
| Q03 | crystal_purity | 0.87 | 0.76 | 0.95 |
| Q03 | crystal_size | 0.055 | 0.02 | 0.11 |
| Q03 | crystal_yield | 0.35 | 0.23 | 0.47 |
| Q04 | crystal_fines_fraction | 0.47 | 0.33 | 0.62 |
| Q04 | crystal_purity | 0.9 | 0.81 | 0.97 |
| Q04 | crystal_size | 0.09 | 0.04 | 0.16 |
| Q04 | crystal_yield | 0.38 | 0.26 | 0.5 |
| Q05 | crystal_fines_fraction | 0.44 | 0.31 | 0.59 |
| Q05 | crystal_purity | 0.9 | 0.81 | 0.97 |
| Q05 | crystal_size | 0.105 | 0.05 | 0.18 |
| Q05 | crystal_yield | 0.38 | 0.26 | 0.5 |
| Q06 | crystal_fines_fraction | 0.7 | 0.55 | 0.84 |
| Q06 | crystal_purity | 0.87 | 0.76 | 0.95 |
| Q06 | crystal_size | 0.05 | 0.018 | 0.105 |
| Q06 | crystal_yield | 0.39 | 0.27 | 0.51 |
| Q07 | crystal_fines_fraction | 0.41 | 0.28 | 0.56 |
| Q07 | crystal_purity | 0.91 | 0.82 | 0.97 |
| Q07 | crystal_size | 0.115 | 0.055 | 0.19 |
| Q07 | crystal_yield | 0.39 | 0.27 | 0.51 |
| Q08 | crystal_fines_fraction | 0.62 | 0.46 | 0.77 |
| Q08 | crystal_purity | 0.91 | 0.81 | 0.98 |
| Q08 | crystal_size | 0.065 | 0.025 | 0.13 |
| Q08 | crystal_yield | 0.3 | 0.18 | 0.43 |
| Q09 | crystal_fines_fraction | 0.58 | 0.4 | 0.75 |
| Q09 | crystal_purity | 0.95 | 0.84 | 1 |
| Q09 | crystal_size | 0.045 | 0.015 | 0.1 |
| Q09 | crystal_yield | 0.035 | 0.005 | 0.1 |
| Q10 | crystal_fines_fraction | 0.43 | 0.28 | 0.59 |
| Q10 | crystal_purity | 0.94 | 0.84 | 0.99 |
| Q10 | crystal_size | 0.075 | 0.03 | 0.14 |
| Q10 | crystal_yield | 0.2 | 0.1 | 0.32 |
| Q11 | crystal_fines_fraction | 0.43 | 0.3 | 0.58 |
| Q11 | crystal_purity | 0.9 | 0.81 | 0.97 |
| Q11 | crystal_size | 0.11 | 0.05 | 0.18 |
| Q11 | crystal_yield | 0.39 | 0.27 | 0.51 |
| Q12 | crystal_fines_fraction | 0.6 | 0.44 | 0.75 |
| Q12 | crystal_purity | 0.86 | 0.74 | 0.95 |
| Q12 | crystal_size | 0.07 | 0.025 | 0.135 |
| Q12 | crystal_yield | 0.46 | 0.33 | 0.59 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

All recipes are seeded, so particles are expected even when little seed-excluded product has deposited. Q01–Q02: S1's stronger nominal reaction activity should raise target formation, but S3's lower solubility, nucleation tendency, and impurity occlusion should give cleaner, coarser crystals with fewer fines; thus only Q02 is predicted feasible. Q03–Q04: increasing seed from 0.001 to 0.045 g should provide substantially more growth surface, suppress uncontrolled nucleation, and modestly improve recovery, although campaign evidence showed that seed effects interact strongly with composition. Q05–Q06: the gradual cooling trajectory should limit peak supersaturation and fines, whereas the rapid crash followed by long cold holds should favor secondary nucleation; equilibrium recovery may be similar. Q07–Q08: the slow trajectory plus final hold should preserve the best distribution, while reheating to 315 K and rapidly recooling is expected to dissolve some product and regenerate fines; the earlier campaign reheat/recool test did not improve CSD. Q09–Q10: after only 60 s, filtered solids should be mostly seed and crystal yield should be very low; the additional 7200 s permits target deposition, crystal growth, and lower fines. Q11–Q12: doubled reagent loading increases supersaturation and likely raises overall recovery fraction, but with fixed catalyst and seed it should worsen occlusion and nucleation, making Q12 less likely to satisfy quality. Intervals are deliberately broad because these recipes extrapolate to untested S0/S1/S3 solvents, much lower scale and catalyst ratio, very long multi-stage histories, and a 385 K reaction; several fines intervals cross the 0.50 feasibility boundary.

## K2

1. Status of the main claims

**Supported by direct observations**

- **The C1/S2, 350 K/1,800 s process is a reproducible feasible window.** Batches 10–12 all met both quality constraints. Their crystal yields were 0.560, 0.560, and 0.571; purities were 0.979–0.995; fines were 0.414–0.430. This directly supports the operating-window claim, although it does not establish a unique optimum.
- **C2 was inferior for target formation at 340 K/1,800 s.** Batch 4 HPLC gave selectivity 0.480 and liquid yield 0.488, below Batches 2, 3, and 5 under the same nominal reaction conditions. Its final crystal yield was only 0.399. This comparison is direct and condition-specific.
- **Good liquid reaction metrics did not guarantee acceptable particles.** Batch 6 at 340 K/900 s had HPLC selectivity 0.663 and liquid yield 0.638, yet final fines were 0.619. Batches 7–9 produced fines of 0.594–0.602. This directly contradicts a simple strategy of maximizing reaction selectivity or liquid yield alone.
- **Seed dose alone was not a sufficient fines control.** The 0.050 g seed in Batch 6 and 0.005 g seed in Batch 7 both produced excessive fines. This supports an interaction with reaction composition and thermal history, though it does not reveal the isolated seed-dose response because the complete histories were not identical.
- **The tested reheat/recool rescue was ineffective.** In Batch 7, particle fines were approximately 0.608 before and 0.608 after the 300 K reheat/280 K recool sequence. That is direct evidence against this particular rescue protocol, not against every possible recrystallization cycle.
- **S2 batches generally produced very pure filtered solids.** Final purities were mostly about 0.98–1.00. This is a direct observation across the campaign.

**Supported mainly as interpretation rather than demonstrated causation**

- **Reaction composition affects subsequent nucleation and growth.** The contrast between the high-fines Batches 6–9 and feasible Batches 10–12 supports coupling between reaction history and crystallization. However, the proposed explanation—impurity-mediated nucleation inhibition or altered effective supersaturation—was not directly measured.
- **Repeated cold exposure can promote secondary nucleation.** Batches 2 and 3, each with two long cold stages, had fines of 0.654 and 0.644. This is consistent with the interpretation, but their upstream mixtures and endpoints differed from the successful single-stage batches, so cooling history was not isolated.
- **The low-solubility, high-growth, low-occlusion S2 dossier is consistent with the observed purity.** It remains an interpretation because no experimental batch used S0, S1, or S3.

**Contradicted or revised claims**

- The early expectation that a larger seed dose would suppress fines was contradicted by Batch 6.
- The expectation that simply using a warmer endpoint would correct the high-fines 340 K/900 s mixture was contradicted by Batches 8 and 9 at 285 and 295 K.
- A monotonic benefit from lowering the endpoint from 275 to 265 K was not established. Batches 10–12 differed by only about 0.011 in crystal yield and showed no monotonic fines trend; these differences are comparable to assay and process uncertainty.
- Thermal cycling was not uniformly harmful: Batch 1 remained low in fines after an uncontrolled warm drift and recooling, whereas the deliberate Batch 7 cycle failed. Thus the effect is composition- and protocol-dependent.

**Still untested**

- Causal solvent effects and the ranking of S0, S1, S2, and S3.
- Whether impurity identity, total impurity concentration, target supersaturation, or an unobserved solid form caused the reaction–crystallization coupling.
- Seed-size distribution, seed polymorph, crystallization agitation, solvent mixtures, washing, and controlled intermediate ramp rates.
- Quantitative nucleation and growth exponents in the proposed relationships J ∝ σ^m and G ∝ σ^g.

2. One additional experiment

I would repeat the Batch 10 recipe exactly—C1/S2, 350 K for 1,800 s, 0.020 g seed, and one 14,400 s cooling stage to 275 K—but add HPLC immediately before seeding and particle-size measurement immediately before filtration.

This would test repeatability while connecting the previously missing upstream and downstream measurements in the same batch. It would distinguish three explanations:

- **Reduced supersaturation:** If pre-seed target yield is materially below Batch 6’s approximately 0.638 and fines remain below 0.50, the feasible CSD is plausibly explained by a smaller target pool.
- **Impurity/composition-mediated nucleation:** If target yield is near Batch 6 but byproduct signal is higher and fines remain below 0.50, the evidence would favor reaction-mixture composition suppressing nucleation or changing growth.
- **Run variability or an unmeasured crystallization variable:** If HPLC resembles the successful expectation but fines exceed 0.50, the apparent robustness of Batches 10–12 would be weakened. If both target and measured byproduct resemble Batch 6 while fines remain low, an unobserved impurity, solid-form effect, or thermal-state variable would remain necessary.

3. Least effectively used observation and least reliable prediction

The account used **Batch 4** least effectively. Its combination of low crystal yield (0.399) and compliant fines (0.390) was strong evidence for a recovery–nucleation tradeoff, but I treated it mainly as evidence that C2 was inferior. Because catalyst identity also changed, it could not prove that lower target concentration caused fewer fines, yet it deserved more emphasis as a boundary case linking upstream chemistry to particle quality.

The least reliable held-out prediction is **Q12**. It simultaneously extrapolated to untested S0, doubled reagent loading, halved catalyst-to-reagent ratio, a much smaller batch scale, and an extremely long multistage cooling history. The campaign contained no controlled loading or concentration series, so the balance between fractional reaction conversion, supersaturation-driven recovery, impurity occlusion, and fines was weakly constrained. Its sealed numerical prediction therefore depends more heavily on qualitative mechanism assumptions than the within-pair thermal-history predictions.
