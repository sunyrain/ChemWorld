# C-W04-MisIndexed — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

Mechanistic account

The successful process appears to combine adequate target formation with controlled supersaturation during crystallization. The measured crystal recovery is conditional on target already present before separation, not an overall reaction yield. A useful conceptual relation is therefore

isolated target fraction ≈ reaction target yield × crystallization recovery,

while the reported campaign objective uses only the second factor. Reaction selectivity still matters indirectly because byproducts and degradation products change solution composition, supersaturation, crystal purity, and impurity occlusion.

Material effects

The initial material-based expectation was that solvent S2 would be best because its dossier indicated low relative solubility, high crystal growth, and low impurity occlusion. Experiments revised that view. S2 did give high purity and substantial recovery, but direct cooling produced almost entirely fine particles: batch 1 had recovery 0.416, purity 0.989, and fines 0.997; batch 2 had recovery 0.451, purity 0.986, and fines reported as 1.000. Increasing seed from 0.05 g in batch 1 to 1.0 g in batch 2 did not solve this problem.

Solvent S3 was more robust. Its nominally lower nucleation tendency plausibly allowed existing particles to grow while suppressing secondary nuclei. With staged cooling, batches 7, 8, 9, and 12 all met both constraints, giving recoveries of approximately 0.496, 0.501, 0.492, and 0.487, purities of 0.970–0.985, and fines fractions of 0.123–0.145. This repeated behavior supports an S3 process region rather than merely one favorable noisy assay.

A conventional supersaturation description is useful:

S = C/C*(T, solvent),
G ≈ k_g(S−1)^g,
J ≈ J0 exp[−B/(ln S)^2],

where S is supersaturation, G is crystal-growth rate, and J is nucleation rate. These equations are interpretive rather than fitted laws. They explain why a solvent with low solubility can increase recovery yet still perform poorly if it creates a large supersaturation jump: nucleation can rise much more sharply than growth, producing many sub-20 µm particles. S3 apparently provided a better balance between recovery and nucleation control in this fixed benchmark world.

Catalyst effects were not isolated cleanly. C1 was used in early batches, while the best deep-cooling series used C3. Batch 1 with C1 at 360 K for 3600 s showed complete conversion but only about 0.523 selectivity, byproduct signal 0.354, and degradation warning 0.193. The shorter 340 K/1800 s reactions generally showed degradation warnings around 0.05–0.08 and selectivities around 0.53–0.60. This is consistent with reduced thermal damage, but catalyst, solvent, temperature, and batch variation were confounded. Thus C3 is demonstrated to be compatible with the recommended process, not proven intrinsically superior.

Reaction–crystallization coupling

The hot reaction establishes the amount and composition of material available for crystallization. High conversion alone was insufficient: several batches approached complete conversion while retaining moderate selectivity and appreciable byproduct signals. Those impurities could lower effective target supersaturation, alter nucleation, or be incorporated into crystals. Nevertheless, final crystal purity remained high in most S2 and S3 processes, suggesting strong rejection of the measured impurities during crystallization. For example, batch 8 had conversion 1.000, selectivity about 0.570, byproduct signal 0.267, but crystal purity 0.970.

The recommended sequence therefore does not rely on exceptionally clean reaction liquor. Instead, it uses crystallization as a selective separation while controlling particle formation. This interpretation is limited to the tested world; no species-level mechanism or real chemical identity was disclosed.

Process-history dependence

Thermal history was the dominant observed quality lever. Direct cooling of S2 to 275 K failed the fines requirement in batches 1 and 2. In contrast, batch 5 used S3 and successive 14,400 s stages at 325, 310, 295, and 280 K; it achieved recovery 0.435, purity 0.971, and fines 0.238. Extending this schedule to 265 K in batch 6 increased recovery to 0.464 while retaining fines 0.177. Extending it to 250 K in batch 7 raised recovery to 0.496 with fines 0.123.

This progression is consistent with maintaining moderate supersaturation at each stage: solute is consumed by growth before the next temperature decrease, limiting accumulation of the supersaturation that drives secondary nucleation. The observation also revised an earlier concern that deeper cooling would necessarily create more fines. Under staged S3 cooling, deeper final temperatures instead increased recovery while preserving or improving the fines fraction.

Batch 8 added three further 14,400 s periods at 250 K. Its final recovery was 0.501, purity 0.970, fines 0.123, CSD quality 0.866, and normalized size 0.123, corresponding to a reported d50 of roughly 31 µm under the stated normalization. This was the highest observed eligible recovery and was therefore recommended. Batch 12 replicated the same operating region and returned recovery 0.487, purity 0.985, fines 0.138, and a d50 of roughly 29 µm. The replication supports robustness, although it does not establish that the extra cold residence itself causes higher recovery.

Quality–recovery tradeoff

Increasing concentration by reducing S3 volume from 0.08 L to 0.06 L in batch 10 retained recovery near 0.500 and purity 0.972, but fines rose to 0.426 and CSD quality fell to 0.696. It remained technically feasible but had much less margin to the 0.50 fines limit. This is consistent with greater supersaturation increasing nucleation.

Deep-staged S2 cooling in batch 11 also became feasible: recovery 0.482, purity 0.992, and fines 0.420. Thus sufficiently gradual cooling can partly compensate for S2’s fines tendency, but S3 at 0.08 L gave both higher observed recovery and a substantially safer fines margin.

Seed-dose conclusions were revised as well. The 1.0 g seed charge in batch 2 did not rescue direct cooling. Under the successful staged process, lowering seed from 0.05 g to 0.005 g in batch 9 produced recovery 0.492 and fines 0.145, close to the standard-seed results. Seed dose therefore was not the dominant lever in the tested range. The 0.05 g dose was retained because it had more successful corroborating batches, not because a precise optimum was established.

Uncertainty and unresolved alternatives

Final-assay noise standards were approximately 0.01 for crystal recovery and purity, 0.018 for fines, and 0.025 for normalized crystal size. Consequently, the recovery differences among batches 7, 8, 9, 10, and 12 are not individually decisive. Batch 8’s numerical lead over batch 10 is especially small, while batch 10’s much higher fines provide the stronger reason to reject the concentrated alternative. The evidence supports a robust operating region near 0.49–0.50 recovery rather than a precisely known optimum of 0.501.

The solvent and thermal-history effects were not explored in a complete factorial design, so their contributions remain partly confounded. C1 versus C3, alternative reaction temperatures, seeding temperatures, intermediate stage spacing, agitation, and deliberate Ostwald-ripening cycles remain untested or incompletely tested. A reheating cycle with S2 in batch 4 gave recovery 0.433 and fines 0.671, but that single result does not exclude a better-designed annealing cycle. Likewise, the apparent benefit of additional 250 K residence is unresolved because batch-to-batch differences are comparable to assay noise.

The mechanistically defensible conclusion is therefore that gradual S3 cooling controls secondary nucleation and provides a broad quality margin, while deep final cooling supplies recovery. The recommended batch 8 represents the best observed eligible member of that region, but the exact cold-hold duration, catalyst advantage, and maximum achievable recovery remain uncertain.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.47 | 0.31 | 0.64 |
| Q01 | crystal_purity | 0.88 | 0.81 | 0.94 |
| Q01 | crystal_size | 0.083 | 0.05 | 0.12 |
| Q01 | crystal_yield | 0.31 | 0.22 | 0.4 |
| Q02 | crystal_fines_fraction | 0.28 | 0.15 | 0.43 |
| Q02 | crystal_purity | 0.94 | 0.89 | 0.98 |
| Q02 | crystal_size | 0.108 | 0.07 | 0.15 |
| Q02 | crystal_yield | 0.4 | 0.31 | 0.49 |
| Q03 | crystal_fines_fraction | 0.68 | 0.49 | 0.85 |
| Q03 | crystal_purity | 0.83 | 0.74 | 0.91 |
| Q03 | crystal_size | 0.06 | 0.03 | 0.1 |
| Q03 | crystal_yield | 0.25 | 0.15 | 0.35 |
| Q04 | crystal_fines_fraction | 0.49 | 0.33 | 0.66 |
| Q04 | crystal_purity | 0.85 | 0.77 | 0.92 |
| Q04 | crystal_size | 0.08 | 0.045 | 0.12 |
| Q04 | crystal_yield | 0.27 | 0.18 | 0.37 |
| Q05 | crystal_fines_fraction | 0.45 | 0.29 | 0.62 |
| Q05 | crystal_purity | 0.86 | 0.78 | 0.93 |
| Q05 | crystal_size | 0.086 | 0.05 | 0.13 |
| Q05 | crystal_yield | 0.28 | 0.19 | 0.38 |
| Q06 | crystal_fines_fraction | 0.79 | 0.63 | 0.92 |
| Q06 | crystal_purity | 0.81 | 0.71 | 0.9 |
| Q06 | crystal_size | 0.05 | 0.025 | 0.085 |
| Q06 | crystal_yield | 0.31 | 0.21 | 0.41 |
| Q07 | crystal_fines_fraction | 0.42 | 0.27 | 0.59 |
| Q07 | crystal_purity | 0.86 | 0.78 | 0.93 |
| Q07 | crystal_size | 0.092 | 0.055 | 0.135 |
| Q07 | crystal_yield | 0.29 | 0.2 | 0.39 |
| Q08 | crystal_fines_fraction | 0.58 | 0.39 | 0.76 |
| Q08 | crystal_purity | 0.88 | 0.8 | 0.95 |
| Q08 | crystal_size | 0.082 | 0.045 | 0.13 |
| Q08 | crystal_yield | 0.23 | 0.13 | 0.34 |
| Q09 | crystal_fines_fraction | 0.88 | 0.7 | 0.99 |
| Q09 | crystal_purity | 0.9 | 0.78 | 0.98 |
| Q09 | crystal_size | 0.04 | 0.015 | 0.08 |
| Q09 | crystal_yield | 0.012 | 0 | 0.045 |
| Q10 | crystal_fines_fraction | 0.72 | 0.52 | 0.89 |
| Q10 | crystal_purity | 0.87 | 0.76 | 0.95 |
| Q10 | crystal_size | 0.057 | 0.025 | 0.1 |
| Q10 | crystal_yield | 0.08 | 0.025 | 0.16 |
| Q11 | crystal_fines_fraction | 0.43 | 0.28 | 0.6 |
| Q11 | crystal_purity | 0.86 | 0.78 | 0.93 |
| Q11 | crystal_size | 0.09 | 0.052 | 0.135 |
| Q11 | crystal_yield | 0.28 | 0.19 | 0.38 |
| Q12 | crystal_fines_fraction | 0.7 | 0.51 | 0.86 |
| Q12 | crystal_purity | 0.82 | 0.72 | 0.9 |
| Q12 | crystal_size | 0.062 | 0.03 | 0.105 |
| Q12 | crystal_yield | 0.4 | 0.29 | 0.51 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

Q01–Q02: S3 is expected to outperform S1 through lower solubility, lower nucleation tendency and lower impurity occlusion, increasing recovery, size and purity while reducing fines. Q03–Q04: additional seed surface should suppress uncontrolled S0 nucleation, but Q04 remains borderline because S0 intrinsically favors nucleation and occlusion. Q05–Q06: gradual cooling should direct supersaturation into growth; the rapid initial plunge in Q06 should create persistent fines despite similar total cold residence and slightly higher recovery. Q07–Q08: the long staged schedule is favorable, whereas reheating to 315 K followed by rapid recooling is expected to dissolve product and then regenerate fines before filtration; a better-controlled annealing cycle remains an alternative. Q09–Q10: particles are present because both are seeded, but 60 seconds gives almost no seed-excluded recovery; the 2-hour hold adds growth without fully repairing the abrupt-cooling CSD. Q11–Q12: doubling loading should raise supersaturation and recovery but worsen occlusion and secondary nucleation, producing a recovery–quality tradeoff. Intervals are relatively broad because these recipes extrapolate to S0/S1, much lower charge, 385 K reaction history and unusually long fine temperature steps; several feasibility classifications, especially Q01, Q04, Q05, Q07 and Q11, are therefore close to the fines or purity boundaries.

## K2

1. Status of the main claims

Supported by direct observations:

- A staged S3 process defines a reproducibly feasible region. Batches 5–9 and 12 all used staged S3 cooling and met the purity and fines limits. In particular, batches 7, 8, 9 and 12 gave recovery around 0.49–0.50, purity around 0.97–0.98, and fines around 0.12–0.15. The observation is reproducibility; the interpretation is that S3 and the staged trajectory jointly suppress secondary nucleation.
- Extending staged S3 cooling to lower final temperatures was associated with higher recovery without loss of particle quality: batch 5 at 280 K gave recovery 0.435 and fines 0.238, batch 6 at 265 K gave 0.464 and 0.177, and batch 7 at 250 K gave 0.496 and 0.123. The numerical trend is observed, but attributing it specifically to equilibrium solubility is mechanistic interpretation because concentration and supersaturation were not measured.
- Direct S2 cooling was unsuitable for particle quality. Batches 1 and 2 had fines of approximately 1 despite high purity and recoveries of 0.416 and 0.451. Batch 11 showed that S2 was not intrinsically infeasible: deep staged cooling produced recovery 0.482, purity 0.992 and fines 0.420. Thus history can partly compensate for the solvent effect.
- Higher loading exposed a quality–recovery tradeoff. Batch 10, using 0.06 L S3 rather than 0.08 L, retained recovery near 0.500 but increased fines to 0.426 and reduced CSD quality. This is direct evidence of association; attributing it to higher supersaturation is interpretation.

Contradicted or substantially revised:

- The initial expectation that S2 would be the best overall solvent was contradicted as a robust operating recommendation. Its nominal low solubility and high growth did not prevent severe fines under direct cooling, and even staged batch 11 had much less fines margin than the S3 series.
- The hypothesis that simply adding substantially more seed would repair fines was contradicted in the tested direct-cooling context. Raising seed from 0.05 g in batch 1 to 1.0 g in batch 2 did not materially reduce fines. This comparison is not perfectly isolated because reaction temperature and duration also changed.
- The initial concern that deeper cooling would necessarily worsen nucleation was contradicted over the tested staged-S3 sequence: batches 5–7 showed lower fines, rather than higher fines, as the final temperature decreased.

Still unresolved or untested:

- Catalyst C3 was shown to be compatible with the best process, but superiority over C1 was not established because catalyst, reaction history and crystallization conditions were not varied factorially.
- The proposed supersaturation, nucleation and growth mechanism was not directly measured. No concentration trajectory, metastable-zone width, nucleation rate or growth rate was observed.
- Impurity rejection was inferred from moderate reaction selectivity combined with high crystal purity; actual impurity incorporation or surface adsorption was not characterized.
- The benefit of the three additional 250 K periods remains unresolved. Batch 8 was numerically best, but batches 7, 9 and 12 differed by amounts comparable with assay noise.
- The seed-size distribution, mixing dependence, deliberate ripening cycles, and the exact optimum stage spacing remain untested. Overall isolated yield from reagent is also unresolved because crystal_yield was explicitly conditional on target present before separation.

2. One additional experiment

I would repeat the batch-8 S3/C3 composition and reaction exactly, including 0.04 mol reagent, 0.08 L S3, 0.005 mol C3 and 0.05 g seed, but replace the 325/310/295/280/265/250 K sequence with a rapid direct cool to 250 K. I would then keep the total time at 250 K equal to the total crystallization time of batch 8 before filtering and assaying.

This single experiment would separate thermal path from final temperature and total cold residence while retaining the solvent, reaction mixture, seed dose and total duration. It would distinguish three explanations:

- Staged-supersaturation explanation: a rapid drop should generate many secondary nuclei. Expected outcome: recovery similar to or slightly above batch 8, but fines above 0.50, smaller normalized size and lower CSD quality.
- Final-temperature/residence explanation: if only reaching 250 K and waiting matters, the result should resemble batch 8, with recovery near 0.49–0.50 and fines near 0.12–0.15.
- Solvent-dominant explanation: if S3 alone largely prevents fines, rapid cooling may cause only a modest deterioration while remaining feasible.

A result with initially poor particles but substantial improvement after the long 250 K residence would additionally support cold ripening; persistent fines would indicate that early nucleation history is effectively irreversible on this timescale.

3. Least effectively used observation and least reliable prediction

The observation used least effectively was batch 3’s temperature history. After staged S3 cooling to 280 K, its subsequent wait allowed the material to warm toward approximately 298 K, yet the final assay still showed fines about 0.222 and recovery 0.424. My account grouped this mainly with successful staged cooling, but the unintended warming could also indicate partial dissolution/ripening or could simply be an innocuous control artifact. Because there was no matched batch with the same prehistory and no warming, I could not exploit it cleanly. It weakens any overly simple claim that monotonically decreasing temperature alone generated the favorable CSD.

Q08 is the least reliable held-out prediction. It combines S0—never tested in the campaign—with a long fine-step crystallization, reheating to 315 K, and rapid recooling. Two competing mechanisms point in opposite directions: reheating could dissolve fines and improve the CSD through ripening, or it could dissolve substantial product and the rapid recool could regenerate fines. Batch 4 provides only a weak analogue because it used S2, a smaller 300 K reheat and a different schedule. Accordingly, the sealed Q08 estimate depends more on extrapolated mechanism than the other predictions and should have the widest practical model uncertainty.
