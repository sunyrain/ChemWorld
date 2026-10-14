# C-W01-Aligned — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

The materials are anonymous benchmark identities, so the following is a process-level mechanism rather than a claim about real chemical structures.

Reaction mechanism and catalyst effects

A useful minimal network is R → P for target formation, R → B for competing byproduct formation, and P → D for thermal degradation. Accordingly, target formation can be summarized approximately as target yield ≈ conversion × selectivity, while isolated crystal yield additionally depends on crystallization and filtration recovery. Conversion was usually near unity, so selectivity—not disappearance of reagent—was the main upstream limitation.

The initial dossier-based choice was catalyst C1. Batch 1 (C1/S2, 350 K for 3600 s) gave liquid yield about 0.568 and final crystal yield 0.466. Batch 2, using C1 at 330 K for 7200 s, fell to liquid yield 0.416 and crystal yield 0.345. Temperature and residence time changed together, so this does not independently prove a temperature effect, but it revised the initial assumption that a longer, cooler reaction would be gentler and equally productive.

At the common 350 K/3600 s condition, C0 was best among the tested catalyst packages: batch 3 produced crystal yield 0.486, compared with 0.410 for C2 in batch 4 and 0.477 for C3 in batch 5. Their final purities all remained high. Halving C0 from 0.005 to 0.0025 mol in batch 8 lowered crystal yield to 0.403 and final reaction yield to 0.443. Thus C0 appears to promote productive throughput at the full tested loading; simply reducing catalyst did not suppress side chemistry enough to compensate for lost target formation. The small C0–C3 difference was not replicated and should not be treated as a precise intrinsic ranking.

Solvent effects

S2 was consistently the best solvent for the joint objective. Its public dossier described relatively low solubility, low nucleation tendency, high growth tendency, and low impurity occlusion. The observations are consistent with that prior: S2 batches commonly achieved crystal purity around 0.98–1.00 and could satisfy the fines constraint while retaining high recovery.

Changing only the solvent within the C0 reaction package degraded downstream particle quality. Batch 6 with S1 gave crystal yield 0.445 and purity 0.996, but fines were 0.553, above the 0.50 limit. Batch 7 with S3 gave yield 0.419, purity 0.971, and fines 0.590. These results suggest that solvent control of supersaturation, nucleation, and growth was at least as important as its effect on reaction activity. S0 was not experimentally tested, so its poorer expected performance remains a dossier-based alternative rather than an observation.

Reaction–crystallization coupling

A useful bookkeeping relationship is

crystal yield ≈ reaction target yield × isolation fraction,

where the isolation fraction combines precipitation and filtration. This is approximate because the synthetic measurements are noisy and channel-specific. For recommended batch 9, the corresponding values were about 0.520/0.565 ≈ 0.92. Thus further recovery gains could arise either from higher reaction selectivity or from capturing a larger fraction of already formed target; conversion alone offers little room because it was already approximately complete.

Solvent volume exposed the strongest coupling. With 0.04 mol reagent and S2 decreased from 0.08 to 0.06 L, batch 9 increased crystal yield to 0.520 while retaining purity 0.982 and fines 0.456. At 0.04 L S2, batch 10 reached a numerically higher yield of 0.530, but fines increased to 0.539 and made the batch noncompliant. Batch 11 used the same high concentration with less seed and a reheat/recool cycle; it still failed on fines at 0.523 and recovered only 0.517. At the intermediate 0.05 L volume, batch 12 recovered 0.520 with purity 0.997 and fines 0.485, narrowly passing.

The mechanistic interpretation is that reduced solvent volume lowers the amount of product left dissolved and increases supersaturation, thereby raising recovery. The same supersaturation also accelerates primary or secondary nucleation, increasing the number fraction of particles below 20 µm. Generic crystallization relationships such as growth G = k_g(S−1)^g and nucleation J increasing much more steeply with supersaturation S are useful qualitatively, but no exponents or rate constants were identified here. The observed quality/recovery frontier is therefore real within this campaign: approximately 0.04 L maximized measured recovery but violated the fines specification, while 0.05–0.06 L provided compliant compromises.

Process-history dependence

Thermal and seeding history affected the final particle population, not merely the endpoint temperature. Batch 1 used 0.05 g seed, a shorter cooling program, and an intervening ambient-temperature wait; its final fines were 0.479. Batch 2 used 0.01 g seed and a longer direct cooling hold at 260 K; fines improved to 0.414, although reaction conditions also changed, so the difference cannot be assigned uniquely to seed amount or cooling rate. Under the common reaction and crystallization schedule, batch 3 achieved fines of 0.329, showing that the slow-cooling package can provide a wide compliance margin at lower concentration.

Staged cooling in batches 10 and 12 was intended to keep supersaturation lower while allowing seeded growth. It was sufficient at 0.05 L in batch 12 but not at 0.04 L in batch 10. Reheating batch 11 to 310 K and recooling was intended to dissolve fines preferentially, yet fines remained above the limit. Possible explanations include insufficient dissolution, renewed nucleation during the second cooling step, or particle attrition; these alternatives were not distinguished experimentally.

Revisions and uncertainty

The campaign revised three initial views. First, the dossier-led C1 choice was replaced by C0 after the catalyst screen. Second, longer/cooler reaction conditions did not preserve recovery in batch 2. Third, concentration was recognized as the dominant recovery lever only after batch 9, but batches 10–11 showed that maximizing supersaturation was incompatible with the fines constraint.

Most comparisons are single batches, and several changed more than one factor. Final-assay noise is material: the approximately 0.0006 yield difference between batch 9 (0.5204) and batch 12 (0.5198) is not evidence of a genuine recovery difference. Batch 9 nevertheless has the stronger fines margin, whereas batch 12 has higher measured purity and particle-size index. Catalyst ranking, the separate effects of seed mass and cooling rate, and the cause of reheat-cycle failure remain unresolved without replication or orthogonal experiments.

The sealed recommendation therefore remains batch 9: 0.04 mol reagent, 0.06 L S2, and 0.005 mol C0; react at 350 K for 3600 s at 500 rpm, cool to 320 K for 3600 s, add 0.01 g seed, cool to 260 K for 14400 s, and filter. Its observed final crystal yield was 0.5204, purity 0.9823, and fines fraction 0.4560.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.24 | 0.14 | 0.36 |
| Q01 | crystal_purity | 0.96 | 0.9 | 0.99 |
| Q01 | crystal_size | 0.18 | 0.11 | 0.27 |
| Q01 | crystal_yield | 0.28 | 0.19 | 0.38 |
| Q02 | crystal_fines_fraction | 0.38 | 0.25 | 0.52 |
| Q02 | crystal_purity | 0.91 | 0.82 | 0.97 |
| Q02 | crystal_size | 0.13 | 0.07 | 0.21 |
| Q02 | crystal_yield | 0.22 | 0.14 | 0.32 |
| Q03 | crystal_fines_fraction | 0.58 | 0.43 | 0.72 |
| Q03 | crystal_purity | 0.86 | 0.75 | 0.94 |
| Q03 | crystal_size | 0.07 | 0.03 | 0.13 |
| Q03 | crystal_yield | 0.11 | 0.05 | 0.19 |
| Q04 | crystal_fines_fraction | 0.43 | 0.29 | 0.57 |
| Q04 | crystal_purity | 0.89 | 0.79 | 0.96 |
| Q04 | crystal_size | 0.1 | 0.05 | 0.17 |
| Q04 | crystal_yield | 0.13 | 0.07 | 0.21 |
| Q05 | crystal_fines_fraction | 0.4 | 0.27 | 0.54 |
| Q05 | crystal_purity | 0.89 | 0.79 | 0.96 |
| Q05 | crystal_size | 0.12 | 0.06 | 0.2 |
| Q05 | crystal_yield | 0.13 | 0.07 | 0.21 |
| Q06 | crystal_fines_fraction | 0.56 | 0.41 | 0.7 |
| Q06 | crystal_purity | 0.87 | 0.76 | 0.95 |
| Q06 | crystal_size | 0.08 | 0.03 | 0.14 |
| Q06 | crystal_yield | 0.13 | 0.07 | 0.22 |
| Q07 | crystal_fines_fraction | 0.37 | 0.24 | 0.51 |
| Q07 | crystal_purity | 0.9 | 0.8 | 0.96 |
| Q07 | crystal_size | 0.13 | 0.07 | 0.21 |
| Q07 | crystal_yield | 0.14 | 0.08 | 0.22 |
| Q08 | crystal_fines_fraction | 0.34 | 0.21 | 0.5 |
| Q08 | crystal_purity | 0.91 | 0.81 | 0.97 |
| Q08 | crystal_size | 0.14 | 0.07 | 0.23 |
| Q08 | crystal_yield | 0.11 | 0.05 | 0.19 |
| Q09 | crystal_fines_fraction | 0.72 | 0.56 | 0.84 |
| Q09 | crystal_purity | 0.91 | 0.79 | 0.97 |
| Q09 | crystal_size | 0.035 | 0.01 | 0.08 |
| Q09 | crystal_yield | 0.008 | 0.001 | 0.025 |
| Q10 | crystal_fines_fraction | 0.57 | 0.41 | 0.71 |
| Q10 | crystal_purity | 0.9 | 0.78 | 0.97 |
| Q10 | crystal_size | 0.065 | 0.025 | 0.12 |
| Q10 | crystal_yield | 0.035 | 0.012 | 0.075 |
| Q11 | crystal_fines_fraction | 0.39 | 0.26 | 0.53 |
| Q11 | crystal_purity | 0.89 | 0.79 | 0.96 |
| Q11 | crystal_size | 0.12 | 0.06 | 0.2 |
| Q11 | crystal_yield | 0.13 | 0.07 | 0.21 |
| Q12 | crystal_fines_fraction | 0.48 | 0.34 | 0.63 |
| Q12 | crystal_purity | 0.85 | 0.73 | 0.94 |
| Q12 | crystal_size | 0.09 | 0.04 | 0.16 |
| Q12 | crystal_yield | 0.21 | 0.12 | 0.32 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

All recipes contain seed, so particles are expected even when seed-excluded product recovery is very small. Q01 is favored over Q02 because S1 has lower nominal solubility, nucleation, and impurity occlusion than S3; S3 may react faster, but the expected crystallization penalty dominates. Q04's larger seed charge should suppress uncontrolled nucleation relative to Q03, modestly increasing capture and reducing fines, although excessive seed can limit growth per particle. Slow staged cooling in Q05 should produce larger particles and fewer fines than the rapid crash in Q06, with similar equilibrium-limited yield. The 315 K reheat in Q08 should dissolve fines and increase mean size relative to Q07, but at the cost of incompletely recovered product after the short recooling step. Extending growth at 292 K in Q10 should raise seed-excluded yield and size and lower fines versus Q09, though both remain fines-limited. Doubling reagent loading in Q12 should increase supersaturation and recovery relative to Q11, while worsening fines and purity; the fixed catalyst charge partially offsets that gain through a lower catalyst-to-reagent ratio. Uncertainty is broad because S0 was untested, 385 K and multi-day cooling lie outside the campaign, and seed loading is very large relative to reagent. Several feasibility calls are therefore close to the fines or purity boundary.

## K2

1. Claim status

Supported by direct observations:
- S2 was the best tested solvent for the joint recovery/quality objective. Under otherwise comparable C0 conditions, batch 3 (S2) gave crystal yield 0.486, purity 0.990 and fines 0.329; batch 6 (S1) gave 0.445, 0.996 and 0.553; batch 7 (S3) gave 0.419, 0.971 and 0.590. Thus S1 and S3 failed the fines constraint while S2 passed. Interpreting this as differences in solubility, nucleation and growth is mechanistic inference, not a directly measured rate law.
- C0 outperformed C2 at the common 350 K package: batches 3 and 4 gave crystal yields 0.486 and 0.410. C0 was only slightly above C3 in batch 5 (0.477), so that ranking remains uncertain without replication. Halving C0 loading in batch 8 lowered yield to 0.403, directly opposing the idea that less catalyst would improve net target production by suppressing side chemistry.
- Concentration exposed a recovery–fines tradeoff. Moving from 0.08 L S2 in batch 3 to 0.06 L in batch 9 raised yield from 0.486 to 0.520 but increased fines from 0.329 to 0.456. At 0.04 L, batch 10 reached 0.530 yield but failed with 0.539 fines; batch 12 at 0.05 L was compliant at 0.520 yield and 0.485 fines. This supports, but does not prove, a supersaturation-driven tradeoff because seed and cooling details were not identical across every comparison.
- Near-complete conversion did not guarantee high target recovery. Final conversion was commonly near one while selectivity and target yield varied appreciably, supporting the interpretation that selectivity and isolation—not conversion alone—limited recovery.

Contradicted or revised:
- The initial dossier-led preference for C1 was revised. Batch 1 with C1 produced 0.466 crystal yield, while C0 batch 3 produced 0.486 with a better fines margin. This is suggestive rather than a clean C1–C0 comparison because their crystallization histories differed.
- The expectation that a longer, cooler reaction would retain productivity was contradicted operationally: C1 batch 2 at 330 K/7200 s gave only 0.345 crystal yield versus 0.466 for batch 1 at 350 K/3600 s. Temperature and residence time were confounded, so the individual cause remains unresolved.
- Reheating was expected to remove fines. Batch 11 remained noncompliant at 0.523 fines and recovered less than batch 10. The observed process package failed; whether reheating itself was ineffective is unresolved because seed loading also changed.

Still untested or weakly tested:
- S0 was never tested in the campaign.
- Cooling rate, seed mass and cold-aging time were not varied orthogonally. Apparent improvements between batches 1 and 2 cannot be assigned uniquely to any one of them.
- The proposed competitive-reaction and nucleation/growth equations were organizing interpretations; no kinetic constants, orders or nucleation barriers were fitted.
- Catalyst rankings and the batch 9 versus batch 12 choice lack replication. Their approximately 0.0006 yield difference is far smaller than the assay uncertainty.
- Primary nucleation, secondary nucleation, attrition and Ostwald ripening were not separately observed.

2. One additional experiment

I would run the batch-12 recipe unchanged except reduce S2 from 0.05 to 0.04 L: 0.04 mol reagent, 0.005 mol C0, 350 K for 3600 s at 500 rpm; cool to 325 K, add 0.005 g seed, cool through 300 K to 260 K using the batch-12 staged schedule, then filter and perform the final assay. This is also equivalent to repeating the batch-10 concentration with batch 12's lower seed charge.

It would distinguish two leading explanations for the batch-10/batch-12 difference. If concentration-driven spontaneous nucleation is dominant, the new 0.04 L batch should resemble batches 10–11: yield around 0.52–0.54 but fines above 0.50. If batch 10 failed mainly because its 0.01 g seed charge generated too many counted particles, reducing seed to 0.005 g should retain the high recovery while bringing fines below 0.50. A third outcome—lower yield with better fines—would suggest that seed surface controls both capture kinetics and particle count. A pre-filtration particle-size measurement plus the final assay would help determine whether filtration or assay noise changes the apparent boundary, but the final assay would remain decisive.

3. Least-used observation and least-reliable prediction

The account used the intermediate particle-size measurements least effectively. Batches 1–7 had paid in-process particle measurements, but the interpretation relied mainly on final assays. Differences between intermediate and final readings—for example fines of about 0.318 before the final assay versus 0.329 finally in batch 3—could have been used to separate actual process evolution from measurement variability and to test whether filtration systematically changed the representative slurry. Instead, those readings were treated mostly as confirmation.

Q09 is the least reliable held-out prediction. It combines untested S0, a 385 K upstream reaction outside the campaign range, a large seed charge relative to only 0.004 mol reagent, and just 60 seconds of crystallization at 292 K. No campaign batch probed such a short crystallization interval. The predicted product yield is therefore highly sensitive to unknown early-time kinetics, while particle presence and number-weighted size may be dominated by the added seed even though seed is excluded from crystal yield. That decoupling makes its yield, size and fines estimates less transferable from the completed batches than the longer-history predictions.
