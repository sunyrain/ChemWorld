# C-W04-MisIndexed — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

Mechanistic account

Recommended process (unchanged)

The sealed recommendation remains batch 6: 0.040 mol reagent, 0.050 L solvent S2, and 0.005 mol catalyst C1; heat at 345 K for 3,600 s with 300 rpm stirring; add 0.050 g seed; then cool monotonically through 300, 285, 270, 250, and 250 K, holding each stage for 14,400 s, followed by filtration. Its final assay gave crystal recovery 0.4633, purity 1.000, and fines number fraction 0.4591, satisfying both constraints.

Material effects

The nominal material dossier made S2 the strongest crystallization prior: relative solubility 0.70, crystal growth 1.30, nucleation tendency 0.65, and impurity occlusion 0.65. Mechanistically, lower solubility should increase supersaturation on cooling, while relatively rapid growth and low nucleation should direct solute onto existing seeds instead of forming many new fine particles. Low impurity occlusion is consistent with the observed final purities, generally 0.98–1.00 in S2 batches.

The experimental evidence supports S2 as the preferred tested solvent, but not as an isolated causal comparison. Batch 3 used C1/S2 at 345 K and produced recovery 0.4291 with fines 0.3884; batch 4 used C2/S3 at 360 K and produced lower recovery, 0.3980, with excessive fines, 0.5574. Catalyst and temperature therefore confound the solvent comparison. S3’s nominally higher solubility, higher nucleation tendency, lower growth, and higher impurity occlusion than S2 nevertheless provide a coherent explanation for the direction of the result.

C1 was the practical reaction baseline. Under the 345 K conditions used in most later batches, conversion was usually approximately 0.99–1.00, while reaction selectivity and reaction yield remained near 0.50–0.53. Thus the chemistry appeared selectivity-limited rather than conversion-limited. Batch 1, which used a hotter controlled history near 360 K, had byproduct signal 0.3844, degradation warning 0.1938, selectivity 0.4724, and reaction yield 0.4702. Later C1/S2 batches at 345 K commonly showed lower byproduct/degradation signals and reaction yields near 0.51. This is consistent with avoiding unnecessary thermal severity, although changes in crystallization history and batch variability prevent attribution to temperature alone.

Only one C2 batch was completed, and C0 and C3 were not tested. Consequently, the data do not establish an intrinsic catalyst ranking. The poor C2/S3 result in batch 4 could reflect catalyst, solvent, temperature, or their interaction.

Reaction–crystallization coupling

A useful upstream approximation is

Y_rxn ≈ X × S_rxn,

where X is conversion and S_rxn is selectivity. Conversion was already nearly complete, so additional severity had little potential benefit and could increase degradation or byproduct formation. The reaction determines both the amount of target entering crystallization and the impurity environment in which nucleation and growth occur.

The reported crystal recovery is instead

R_cryst = n_target,recovered crystals / n_target,present before separation.

It excludes seed mass and is not an overall yield from charged reactant. A rough charged-reactant recovery is therefore Y_rxn × R_cryst. For batches 6, 5, 11, and 12 this product was approximately 0.235, 0.232, 0.231, and 0.234, respectively. Thus batch 6’s high crystallization recovery did not come at an obvious cost to upstream target formation, but the campaign objective and sealed selection were based on R_cryst subject to the quality constraints.

The very high crystal purity despite reaction selectivity near 0.5 implies substantial impurity rejection during crystallization/filtration. That interpretation is consistent with S2’s low nominal occlusion tendency, although the purity channel was often clipped at 1.000 and cannot establish perfect physical purity.

Supersaturation and competing particle processes

The qualitative relationships I used were

S(t) = C(t)/C*(T(t)),

J_nuc ∝ exp[-B/(ln S)^2],

G ∝ (S−1)^g,

where S is supersaturation, C* is temperature-dependent solubility, J_nuc is secondary or primary nucleation rate, and G is crystal growth rate. Lower solvent volume raises C; cooling lowers C*. Both increase S. Moderate supersaturation favors growth on seeds, while excessive or abrupt supersaturation can increase J_nuc steeply and generate fines. Recovery follows the solute balance approximately as

R_cryst = 1 − n_target,mother liquor/n_target,pre-separation,

so colder final temperature and higher concentration favor recovery, but not necessarily acceptable particle quality.

Process-history dependence

Batch 1 demonstrated that reaching a low temperature is insufficient by itself. It used only 0.020 g seed, cooled to 275 K for 7,200 s, then underwent an ambient-temperature wait before recooling. It gave recovery 0.3890 and fines 0.5100. The warm interruption probably reduced retained supersaturation or partly redissolved material, while the lower seed surface left more supersaturation available for uncontrolled nucleation. This is an interpretation, not an isolated seed-dose test.

With 0.050 g seed and uninterrupted cooling, batch 2 improved to recovery 0.4193 and fines 0.3960. Extending the final cooling in batch 3 gave recovery 0.4291 and fines 0.3884. A gentler four-stage 300→285→270→250 K schedule in batch 5 increased recovery further to 0.4448 while retaining low fines, 0.3779. Collectively, batches 1–5 motivated the revision from a simple “cool colder and longer” model to one emphasizing seeded, monotone, staged depletion of supersaturation.

Concentration then exposed a narrow quality–recovery window. Reducing S2 from 0.080 L in batch 5 to 0.050 L in batch 6 raised recovery to 0.4633, with fines still acceptable at 0.4591. An exact process repeat, batch 11, gave recovery 0.4572 and fines 0.4336. Batch 12 omitted the repeated final 250 K stage and gave recovery 0.4602 with fines 0.4419. These three results indicate that the 0.050 L region is reproducibly feasible, but they do not prove that the additional final hold has a beneficial effect.

More aggressive histories raised recovery but lost particle quality. Batch 8, with 0.060 L S2 and six cooling stages, achieved the campaign’s highest recovery, 0.4721, but failed the fines constraint at 0.5961. Batch 9 used 0.045 L and four stages; recovery was 0.4663 but the reported fines fraction was 1.000. Batch 10 used 0.055 L and four stages; recovery was 0.4652 with fines 0.5436. These results suggest threshold-like secondary nucleation rather than a smooth monotonic dependence on solvent volume.

Batch 7 tested a proposed dissolution/ripening maneuver at 0.040 L: cool, reheat to 295 K, then recool. It yielded recovery 0.4653 but fines 0.9866. I therefore rejected the initial hypothesis that this reheating would selectively dissolve fines and improve the size distribution under these conditions. However, batch 7 confounded reheating with the highest concentration tested, so it does not show that every temperature cycle is intrinsically harmful.

Revisions to the working mechanism

The initial model favored S2, moderate seeding, slow cooling, and a cold growth hold. Early batches supported S2 and continuous seeded cooling. The model was then revised in two ways:

1. Thermal history is nonmonotonic: more cold residence or reheating is not automatically beneficial. Excess processing can allow further secondary nucleation or cycling-induced nucleation.
2. Concentration creates a recovery–fines tradeoff with an apparent narrow feasible window. Less solvent often raised recovery, but conditions adjacent to 0.050 L did not reliably satisfy the fines limit.

The final mechanistic picture is therefore controlled supersaturation consumption: generate target at moderate reaction severity, provide sufficient seed surface, and lower solubility gradually enough that growth consumes supersaturation before the nucleation rate becomes dominant.

Uncertainty and unresolved tradeoffs

The final-assay noise scales were approximately 0.010 for crystal recovery, 0.010 for purity, and 0.018 for fines fraction, in addition to process variability. Batch 6 exceeded batch 12 in recovery by only about 0.0031, much less than one recovery noise standard deviation. Its selection as the sealed recommendation reflects the highest observed feasible recovery, not proof that its exact extra hold is superior.

Batches 6 and 11, nominal process repeats, differed by 0.0061 in recovery and 0.0255 in fines. Their means were approximately 0.4603 recovery and 0.4463 fines. This repeat supports a real feasible region, but two runs are insufficient to estimate tails reliably. Batch 6’s fines margin below 0.50 was about 0.041, only modest relative to analytical and process uncertainty.

The central unresolved tradeoff is that the largest recoveries occurred near or beyond the particle-quality boundary. Batch 8 reached 0.4721 recovery but failed fines, whereas feasible batches 6, 11, and 12 clustered around 0.457–0.463 recovery. Purity was not the active limitation in this campaign; fines formation was. Untested alternatives include finer optimization around 0.050 L, different seed size distributions or addition temperatures, agitation effects, feedback-controlled supersaturation, and independent catalyst screening. None can be inferred to outperform the sealed batch without new experiments.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.43 | 0.3 | 0.57 |
| Q01 | crystal_purity | 0.92 | 0.85 | 0.97 |
| Q01 | crystal_size | 0.072 | 0.04 | 0.11 |
| Q01 | crystal_yield | 0.24 | 0.14 | 0.35 |
| Q02 | crystal_fines_fraction | 0.34 | 0.22 | 0.48 |
| Q02 | crystal_purity | 0.95 | 0.89 | 0.99 |
| Q02 | crystal_size | 0.085 | 0.05 | 0.13 |
| Q02 | crystal_yield | 0.29 | 0.18 | 0.41 |
| Q03 | crystal_fines_fraction | 0.73 | 0.55 | 0.89 |
| Q03 | crystal_purity | 0.87 | 0.77 | 0.95 |
| Q03 | crystal_size | 0.045 | 0.02 | 0.085 |
| Q03 | crystal_yield | 0.19 | 0.08 | 0.32 |
| Q04 | crystal_fines_fraction | 0.39 | 0.26 | 0.55 |
| Q04 | crystal_purity | 0.9 | 0.82 | 0.96 |
| Q04 | crystal_size | 0.073 | 0.04 | 0.115 |
| Q04 | crystal_yield | 0.21 | 0.11 | 0.33 |
| Q05 | crystal_fines_fraction | 0.35 | 0.22 | 0.5 |
| Q05 | crystal_purity | 0.91 | 0.83 | 0.97 |
| Q05 | crystal_size | 0.079 | 0.045 | 0.125 |
| Q05 | crystal_yield | 0.22 | 0.12 | 0.34 |
| Q06 | crystal_fines_fraction | 0.67 | 0.49 | 0.84 |
| Q06 | crystal_purity | 0.87 | 0.76 | 0.95 |
| Q06 | crystal_size | 0.043 | 0.018 | 0.08 |
| Q06 | crystal_yield | 0.23 | 0.13 | 0.36 |
| Q07 | crystal_fines_fraction | 0.34 | 0.21 | 0.5 |
| Q07 | crystal_purity | 0.91 | 0.82 | 0.97 |
| Q07 | crystal_size | 0.082 | 0.045 | 0.13 |
| Q07 | crystal_yield | 0.23 | 0.13 | 0.35 |
| Q08 | crystal_fines_fraction | 0.82 | 0.64 | 0.95 |
| Q08 | crystal_purity | 0.86 | 0.74 | 0.95 |
| Q08 | crystal_size | 0.041 | 0.015 | 0.08 |
| Q08 | crystal_yield | 0.19 | 0.08 | 0.32 |
| Q09 | crystal_fines_fraction | 0.62 | 0.4 | 0.82 |
| Q09 | crystal_purity | 0.93 | 0.82 | 0.99 |
| Q09 | crystal_size | 0.03 | 0.012 | 0.06 |
| Q09 | crystal_yield | 0.015 | 0 | 0.05 |
| Q10 | crystal_fines_fraction | 0.52 | 0.34 | 0.7 |
| Q10 | crystal_purity | 0.92 | 0.82 | 0.98 |
| Q10 | crystal_size | 0.046 | 0.02 | 0.08 |
| Q10 | crystal_yield | 0.065 | 0.015 | 0.14 |
| Q11 | crystal_fines_fraction | 0.37 | 0.23 | 0.53 |
| Q11 | crystal_purity | 0.91 | 0.82 | 0.97 |
| Q11 | crystal_size | 0.076 | 0.04 | 0.12 |
| Q11 | crystal_yield | 0.22 | 0.12 | 0.34 |
| Q12 | crystal_fines_fraction | 0.64 | 0.46 | 0.81 |
| Q12 | crystal_purity | 0.84 | 0.72 | 0.93 |
| Q12 | crystal_size | 0.049 | 0.02 | 0.09 |
| Q12 | crystal_yield | 0.39 | 0.25 | 0.53 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

These are noise-free latent-outcome predictions conditioned on the sealed K1 account; the 80% intervals represent process/model uncertainty rather than final-assay noise. Q01–Q02: S3 is expected to outperform S1 through lower solubility, lower nucleation tendency, faster growth and less impurity occlusion. Q03–Q04: increasing seed from 0.001 to 0.045 g supplies surface area that suppresses secondary nucleation, chiefly lowering fines. Q05–Q06: slow staged cooling and crash cooling should approach similar recovery after equal total time, but the crash should create substantially more fines and smaller particles. Q07–Q08: the 315 K excursion followed by rapid recooling is expected to cause dissolution/re-nucleation and degrade size distribution, consistent with the adverse thermal-cycle observation in batch 7. Q09–Q10: an additional 7200 s at 292 K permits some seed-excluded deposition and growth, but predicted recovery remains low and fines remain borderline. Q11–Q12: doubling reagent loading raises supersaturation and recovery but increases nucleation and impurity occlusion, creating a recovery–quality tradeoff. All recipes contain seed, so particles are expected even where seed-excluded product recovery is near zero. Feasibility calls near the 0.50 fines boundary—especially Q01, Q04, Q05, Q10 and Q11—are correspondingly uncertain.

## K2

1. Status of the main claims

Supported by direct observations:

- A reproducible feasible S2 operating region exists near 0.050 L solvent, 0.050 g seed, and monotone staged cooling. Batch 6 gave recovery 0.4633, purity 1.000, and fines 0.4591; its nominal repeat, batch 11, gave 0.4572, 0.9995, and 0.4336. Batch 12, with one fewer final cold hold, gave 0.4602, 1.000, and 0.4419. Directly, all three met the constraints with similar recovery. Interpreting this as a robust local process window is reasonable, although three runs do not define its full boundaries.

- Fines, rather than purity, were the active quality limitation. All final crystal purities were approximately 0.98–1.00, including several batches that failed because of fines: batch 7 had fines 0.9866, batch 8 had 0.5961, batch 9 had 1.000, and batch 10 had 0.5436. The interpretation is that crystallization rejected impurities effectively but particle nucleation was sensitive to process history.

- Recovery and particle quality exhibited a tradeoff. Batch 8 had the highest observed recovery, 0.4721, but failed the fines constraint at 0.5961. Feasible batches 6, 11, and 12 had slightly lower recoveries of 0.4572–0.4633. This is a direct observed tradeoff in the tested recipes, not proof of a universal Pareto frontier.

- The reaction was generally conversion-saturated and selectivity-limited. Later batches commonly had conversion near 0.99–1.00 but selectivity and reaction yield near 0.50–0.53. Batch 1’s hotter history had selectivity 0.4724, reaction yield 0.4702, byproduct signal 0.3844, and degradation warning 0.1938. The observation supports avoiding unnecessary severity; attributing the entire difference to temperature remains interpretive because other history differed.

- The initial continuous-cooling strategy improved on the interrupted first process. Batch 1, with 0.020 g seed and an ambient-warming interruption, gave recovery 0.3890 and fines 0.5100. Batches 2 and 3, with 0.050 g seed and uninterrupted cooling, gave recoveries 0.4193 and 0.4291 with fines 0.3960 and 0.3884. The improvement is directly observed, but seed dose and thermal continuity were changed together.

Contradicted or substantially weakened:

- The early idea that reheating could beneficially ripen away fines was contradicted under the tested condition. Batch 7’s cool–reheat–recool history produced fines 0.9866 rather than an improved distribution. However, that batch also used only 0.040 L solvent, so the observation contradicts the combined recipe, not every possible ripening cycle.

- A simple “colder or longer is always better” rule was contradicted. Batch 8 used extensive cold aging and reached recovery 0.4721, but fines deteriorated to 0.5961. Batch 12, with one fewer final hold than batches 6 and 11, remained competitive at recovery 0.4602 and fines 0.4419. The extra hold therefore had no demonstrated benefit beyond batch variability.

- A smooth monotonic solvent-volume relationship was not supported. Around the feasible 0.050 L condition, both 0.045 L in batch 9 and 0.055 L in batch 10 failed badly on fines, as did 0.060 L with a longer history in batch 8. This suggests threshold behavior or interactions, but the volume changes were confounded with cooling duration in some comparisons.

Still untested or unresolved:

- S2’s intrinsic superiority over S3 was not isolated. Batch 3, using C1/S2 at 345 K, outperformed batch 4, using C2/S3 at 360 K, but catalyst and temperature were confounded with solvent. S0 and S1 were not tested during the campaign.

- No causal catalyst ranking was established. Almost all batches used C1; only batch 4 used C2, while C0 and C3 were untested.

- The isolated effect of seed mass remains unresolved because batch 1 versus batches 2–3 also changed thermal history.

- Agitation, seed size distribution, seed-addition temperature, direct supersaturation control, and impurity-specific occlusion were not independently varied or measured.

2. One additional experiment

I would repeat batch 11 exactly—0.040 mol reagent, 0.050 L S2, 0.005 mol C1, 345 K reaction, 0.050 g seed, and the 300→285→270→250 K monotone schedule—but replace its final 14,400 s hold at 250 K with a time-matched cycle: heat from 250 to 295 K for 7,200 s and recool to 250 K for 7,200 s. All other factors would remain unchanged.

Existing batch 11 is then the closest control, with equal total post-seeding time. The experiment would distinguish two explanations for batch 7:

- Thermal-cycle mechanism: reheating dissolves some solids and rapid recooling creates a new nucleation burst. Expected result: fines rise above 0.50, normalized size and CSD quality decline, and recovery may fall or only partly recover after recooling.

- Concentration mechanism: batch 7 failed mainly because its 0.040 L solvent charge caused excessive supersaturation, not because of the thermal cycle. Expected result: the new 0.050 L batch remains near batches 6 and 11—roughly 0.46 recovery with fines around 0.43–0.46.

An intermediate result would support an interaction: cycling is harmful primarily when loading is already high. This experiment would not change the sealed recommendation; it would test the weakest causal link in the mechanism.

3. Least effectively used observation and least reliable prediction

The crystal-size observations were used least effectively. The account concentrated on recovery and the thresholded fines metric, while normalized crystal size varied substantially even among closely related batches: 0.0529 in batch 6, 0.0780 in batch 11, and 0.0997 in batch 12. Prefilter particle measurements also differed from final-assay estimates—for example, batch 6’s prefilter fines estimate was about 0.420 versus 0.459 in the final assay. I did not construct a quantitative link among size, fines, seed population, filtration, and instrument-specific uncertainty. Consequently, the proposed growth-versus-nucleation explanation is better supported for the fines constraint than for exact d50 behavior.

Q08 is the least reliable held-out prediction. Its sealed prediction assigned a severe fines outcome to a 315 K heat excursion, largely by extrapolating from batch 7. But batch 7 combined thermal cycling with the campaign’s highest concentration, used S2 rather than Q08’s S0, reheated only to 295 K, and followed a different cooling history. Thus the prediction transfers a mechanism across solvent, concentration, excursion temperature, and timing based on one confounded observation. The sealed Q08 values and feasibility call remain unchanged, but its interval may still underrepresent structural model uncertainty.
