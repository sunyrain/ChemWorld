# C-W02-Opaque — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

The materials were anonymous benchmark identities, so the evidence supports comparative process effects rather than claims about real chemical identities.

Reaction/material effects: Under otherwise similar full-loading conditions (0.040 mol reagent, 0.005 mol catalyst, 0.080 L solvent, approximately 360 K for 1 h), catalyst-C0 performed best with solvent-S0. Batch 1 gave HPLC conversion 1.00, selectivity 0.699 and reaction yield 0.693. Across the C0 solvent screen, reaction performance declined from S0 to S1, S2 and S3: batches 3–5 gave approximate HPLC yields of 0.646, 0.616 and 0.528, while byproduct signal increased from 0.249 to 0.273 and 0.329. This is strong evidence that solvent identity affects the reaction, although it may also affect analytical response and product stability. Catalyst-C1/S1 in batch 2 was poorer than C0/S1 in batch 3, but catalyst identity cannot be isolated because batch 2 also used 340 rather than 360 K and a different crystallization history.

Reaction–crystallization coupling: Crystal recovery was defined as seed-excluded target recovered from the target present immediately before separation, not as yield from the original reagent charge. A useful approximate decomposition is Y_overall = Y_reaction × R_crystallization. For batch 12, this gives about 0.701 × 0.574 ≈ 0.40 of the initial reagent as recovered crystalline target, before any additional purity convention. Crystal purity was P = target mass in solids/total solid mass. The large increase from reaction selectivity near 0.70 to crystal purity near 0.99 in batches 1 and 12 indicates effective impurity rejection during crystallization. Thus upstream selectivity controls the available target and impurity burden, while solvent-dependent solubility and thermal history control what fraction of that target is recovered.

The solvent screen shows this coupling clearly. Batch 3 (C0/S1) retained high crystal purity, 0.986, and recovery 0.559 despite lower reaction performance than S0. Batch 4 (C0/S2) gave recovery 0.531 and purity at the assay ceiling, whereas batch 5 (C0/S3), which had the poorest reaction yield/selectivity and highest byproduct signal, gave only 0.421 recovery and 0.964 purity. Because solvent simultaneously changes reaction behavior and crystallization thermodynamics, these results do not uniquely assign the recovery differences to either mechanism.

Process-history effects: The observations are consistent with the usual competition between supersaturation-driven nucleation and growth. If S=C/C* is supersaturation, nucleation can be represented qualitatively as J proportional to exp[-B/(ln S)^2], while growth may scale as G=k_g(S-1)^g. Deep cooling increases recovery by lowering C* but can raise J much faster than G, creating many fines. In the full-loading C0/S0 experiments, deeper cooling to 270–275 K gave the best recoveries: 0.555 in batch 1, 0.562 in batch 6 and 0.574 in batch 12. Shallower cooling to 300 K in batches 7–9 and 11 gave only about 0.449–0.466 recovery. This supports a solubility/recovery benefit from deeper cooling.

However, every tested history remained dominated by particles below 20 micrometres. Final fines fractions ranged from about 0.987 to 1.000. Batch 1 used 0.05 g seed, slow cooling to 270 K and a hold; its recovery was 0.555 but fines were 0.997. Batch 6 added four 305 K anneal/recooling cycles; recovery remained 0.562 and fines were 1.000. Batch 9 used a slow staircase through 310, 305 and 300 K; recovery was 0.457 and fines were 1.000. Seed dose also failed to solve the problem: batches 7, 8 and 11 used approximately 0.05, 0.005 and 1.0 g seed, respectively, yet final fines remained 0.987, 0.987 and 0.994. These observations reject my initial expectation that ordinary slow seeded cooling, longer holds or mild annealing would adequately suppress fines within the tested scope. They do not prove that seeding is intrinsically ineffective; seed size distribution, addition temperature and mixing were not independently characterized.

A reduced-loading alternative was also tested. Batch 10 used 0.010 mol reagent and 0.00125 mol catalyst in 0.080 L S0. Conversion fell to 0.930, crystal recovery fell to 0.230, and fines remained 1.000. This contradicted the tentative idea that lower concentration might reduce secondary nucleation enough to improve particle quality. Within this single test, dilution mainly sacrificed reaction and crystallization productivity.

The selected batch 12 used full loading with C0/S0, reaction near 360 K for 1 h, quench, 0.05 g seed, slow cooling to 270 K, a low-agitation hold, filtration and final assay. It produced conversion 1.00, reaction yield 0.701, crystal recovery 0.574, purity 0.989, size index 0.081 and fines fraction 1.000. It therefore maximized observed recovery while maintaining the purity requirement, but it did not meet the fines constraint. Batch 1 is a useful near-replicate: recovery 0.555, purity 0.981 and fines 0.997. The recovery advantage of batch 12 over batch 1 is only 0.019, close enough to the stated assay noise and unquantified process variability that it should be viewed as a modest observed advantage rather than a precisely established effect.

Particle-size conclusions are less certain than the fines conclusion. Final-assay size has a stated noise scale of 0.025, and batch 8 illustrates the issue: its in-process particle measurement gave size index 0.043, whereas the final assay gave 0.086, while both indicated essentially all particles were fines. Independent noisy estimates of size and fines can therefore appear internally awkward near the 20-micrometre threshold. In contrast, the fines result was consistently near unity across all 12 batches, so the failure of the fines specification is robust.

The unresolved tradeoff is therefore not simply high recovery versus slightly poorer particle quality: deeper cooling clearly increased recovery, but none of the shallower, slower, seeded or annealed histories approached the required fines fraction of 0.50. Untested alternatives include post-filtration resuspension or size classification, a true dissolution/recrystallization wash, solvent mixtures or antisolvent staging, independently characterized larger seeds, different mixing during the nucleation window, and a higher-temperature anneal that dissolves fines without destroying the desired crystals. No evidence from this campaign establishes that any of these would succeed. The sealed recommendation remains batch 12, explicitly as the highest-recovery, high-purity but fines-noncompliant process.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.28 | 0.12 | 0.52 |
| Q01 | crystal_purity | 0.97 | 0.92 | 1 |
| Q01 | crystal_size | 0.15 | 0.09 | 0.22 |
| Q01 | crystal_yield | 0.29 | 0.18 | 0.41 |
| Q02 | crystal_fines_fraction | 0.57 | 0.32 | 0.79 |
| Q02 | crystal_purity | 0.93 | 0.84 | 0.99 |
| Q02 | crystal_size | 0.11 | 0.06 | 0.18 |
| Q02 | crystal_yield | 0.18 | 0.08 | 0.3 |
| Q03 | crystal_fines_fraction | 0.62 | 0.36 | 0.84 |
| Q03 | crystal_purity | 0.97 | 0.91 | 1 |
| Q03 | crystal_size | 0.09 | 0.04 | 0.16 |
| Q03 | crystal_yield | 0.31 | 0.19 | 0.44 |
| Q04 | crystal_fines_fraction | 0.25 | 0.1 | 0.49 |
| Q04 | crystal_purity | 0.97 | 0.92 | 1 |
| Q04 | crystal_size | 0.17 | 0.1 | 0.24 |
| Q04 | crystal_yield | 0.32 | 0.2 | 0.45 |
| Q05 | crystal_fines_fraction | 0.23 | 0.08 | 0.46 |
| Q05 | crystal_purity | 0.97 | 0.92 | 1 |
| Q05 | crystal_size | 0.18 | 0.11 | 0.25 |
| Q05 | crystal_yield | 0.34 | 0.22 | 0.47 |
| Q06 | crystal_fines_fraction | 0.87 | 0.68 | 0.98 |
| Q06 | crystal_purity | 0.96 | 0.9 | 1 |
| Q06 | crystal_size | 0.055 | 0.025 | 0.105 |
| Q06 | crystal_yield | 0.35 | 0.23 | 0.48 |
| Q07 | crystal_fines_fraction | 0.2 | 0.06 | 0.43 |
| Q07 | crystal_purity | 0.97 | 0.92 | 1 |
| Q07 | crystal_size | 0.19 | 0.12 | 0.27 |
| Q07 | crystal_yield | 0.35 | 0.23 | 0.48 |
| Q08 | crystal_fines_fraction | 0.59 | 0.31 | 0.82 |
| Q08 | crystal_purity | 0.96 | 0.89 | 1 |
| Q08 | crystal_size | 0.105 | 0.05 | 0.18 |
| Q08 | crystal_yield | 0.31 | 0.17 | 0.45 |
| Q09 | crystal_fines_fraction | 0.98 | 0.88 | 1 |
| Q09 | crystal_purity | 0.96 | 0.85 | 1 |
| Q09 | crystal_size | 0.04 | 0.015 | 0.08 |
| Q09 | crystal_yield | 0.015 | 0 | 0.055 |
| Q10 | crystal_fines_fraction | 0.88 | 0.68 | 0.98 |
| Q10 | crystal_purity | 0.97 | 0.89 | 1 |
| Q10 | crystal_size | 0.06 | 0.025 | 0.115 |
| Q10 | crystal_yield | 0.075 | 0.025 | 0.15 |
| Q11 | crystal_fines_fraction | 0.24 | 0.08 | 0.48 |
| Q11 | crystal_purity | 0.97 | 0.92 | 1 |
| Q11 | crystal_size | 0.18 | 0.11 | 0.26 |
| Q11 | crystal_yield | 0.35 | 0.23 | 0.48 |
| Q12 | crystal_fines_fraction | 0.42 | 0.2 | 0.67 |
| Q12 | crystal_purity | 0.96 | 0.9 | 1 |
| Q12 | crystal_size | 0.16 | 0.09 | 0.24 |
| Q12 | crystal_yield | 0.52 | 0.39 | 0.65 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

All recipes contain seed, so particles are expected even where seed-excluded product recovery is very small. Q01/Q02 assigns solvent-S1 higher recovery, purity and growth quality than S3, following the observed solvent ranking. Q03/Q04 predicts that 0.045 g seed suppresses uncontrolled nucleation better than 0.001 g during the exceptionally slow ramp. Q05/Q06 gives similar endpoint recovery but sharply worse size and fines after crash cooling, because the rapid supersaturation excursion should create many nuclei before the long hold. Q07/Q08 treats the 315 K reheat followed by rapid recooling as partially dissolving the established population and then regenerating fines; this direction is uncertain because the campaign tested only milder annealing. Q09/Q10 predicts very little seed-excluded recovery after 60 seconds at 292 K, with a two-hour hold adding some growth but not enough to remove the fines problem. Q11/Q12 predicts higher loading substantially raises recovery, while added supersaturation modestly worsens fines despite larger crystals. Intervals are deliberately broad because these schedules extrapolate far beyond the tested continuous-cooling durations; size and fines carry the greatest uncertainty, and several feasibility calls lie near the fines threshold.

## K2

1. Claim status

Supported by direct observation:
- Material/solvent effects were important. With C0 under otherwise similar full-loading conditions, HPLC reaction yield declined from about 0.69 in S0 (batch 1) to 0.65, 0.62 and 0.53 in S1, S2 and S3 (batches 3–5), while byproduct signal generally increased. Interpreting this as a solvent effect is reasonable, although the data do not identify a molecular cause.
- Crystallization strongly purified the target. Batches 1–12 all reported crystal purity above 0.96 despite reaction selectivities commonly near 0.55–0.72. Impurity rejection is directly observed; selective incorporation or differential solubility is the mechanistic interpretation.
- Deep cooling favored recovery in the tested C0/S0 processes. Batches 1, 6 and 12, ending near 270–275 K, recovered about 0.56–0.57, whereas the shallower 300 K processes in batches 7–9 and 11 recovered about 0.45–0.47. This comparison is suggestive rather than perfectly controlled because seed dose, holds and cycling differed.
- Lower loading did not solve the problem. Batch 10 recovered only 0.23 and still had fines of 1.00, compared with roughly 0.56 recovery at full loading in batches 1, 6 and 12.
- The fines failure was robust: every final assay gave a fines fraction near 0.99–1.00.

Contradicted within the tested scope:
- My initial expectation that ordinary slow seeded cooling, long holds or mild annealing would suppress fines was contradicted. Batch 6 used repeated 305 K anneal/recooling cycles, batch 9 used staircase cooling, and batches 7, 8 and 11 varied seed dose and hold time; none approached the 0.50 fines limit.
- The hypothesis that dilution would reduce secondary nucleation enough to improve quality was contradicted by batch 10.

Still untested or unresolved:
- A catalyst effect was not isolated. Batch 2 used C1, but it also differed in solvent, reaction temperature and crystallization history.
- The nucleation-versus-growth equation in the account was an interpretation, not a directly fitted kinetic law.
- Truly continuous very slow cooling all the way to approximately 278 K was not tested in the campaign. Batch 9 cooled slowly only to 300 K, while batch 6 combined deep cooling with reheating cycles.
- Post-filtration resuspension/classification, solvent mixtures, characterized larger seeds, and a stronger selective-dissolution anneal were not tested.

2. One additional experiment

I would repeat the batch-12 upstream process exactly—C0/S0, full loading, approximately 360 K reaction, quench and 0.05 g seed—but replace its four-hour descent to 270 K with a continuous staircase from 300 to 278 K over roughly 72–76 hours. I would make particle-size measurements at an intermediate temperature and immediately before filtration, then perform the same filtration and final assay.

This would distinguish three explanations. If batch 12 produced fines primarily because rapid supersaturation caused a primary-nucleation burst, the slow ramp should produce a substantially larger number-weighted size and fines below 0.50, while retaining moderately high recovery and purity. If fines instead arise from persistent secondary nucleation, seed fragmentation, attrition or an intrinsically fine stable population, fines should remain near 0.9–1.0 despite the slow ramp, although recovery may remain around 0.5. If in-situ particle measurements show low fines but the final assay again shows high fines, filtration, sampling or measurement representation—not crystallizer kinetics—would become the leading explanation. A large loss of recovery with few new crystals would instead indicate that growth was solubility- or kinetics-limited during the slow ramp.

3. Least-used observation and least-reliable prediction

The observation used least effectively was the disagreement between pre-filtration particle measurements and final-assay size, especially in batch 8: the particle instrument reported size index about 0.043 and fines 0.999, while the final assay reported size about 0.086 and fines 0.987. I mentioned this as uncertainty but did not fully incorporate it when discussing apparent size improvements. It argues that isolated size estimates should receive little mechanistic weight unless supported by fines and repeated measurements. The consistently high fines values were much more reliable than the apparent size differences.

Q08 is the least reliable held-out prediction. It requires extrapolating from the ineffective 305 K annealing in batch 6 to a stronger 315 K reheat followed by rapid recooling. That step could selectively dissolve fines and improve the distribution, dissolve most product and lower recovery, or erase the mature population and cause renewed nucleation during recooling. The campaign did not constrain which nonlinear outcome dominates, so the predicted direction for both fines and recovery has particularly wide mechanistic uncertainty.
