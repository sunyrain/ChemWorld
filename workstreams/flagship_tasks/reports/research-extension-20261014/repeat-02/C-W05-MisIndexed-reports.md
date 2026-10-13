# C-W05-MisIndexed — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

Mechanistic account

The campaign supports a coupled reaction–crystallization picture in which solvent choice primarily controls crystal growth versus nucleation, while catalyst and reaction history determine the target/impurity composition entering crystallization.

Useful definitions are: reaction yield approximately Y_rxn = conversion × selectivity; crystallization recovery R_cryst = seed-excluded recovered target / target present before separation; and fines fraction f20 = N(d < 20 µm)/N_total. The stated objective maximizes R_cryst subject to crystal purity ≥ 0.80 and f20 ≤ 0.50. Thus R_cryst is not overall yield from charged reagent. An approximate overall isolated-target fraction would be Y_rxn × R_cryst, but that was not the optimization criterion.

Material effects

Solvent S2 was uniquely robust in the tested solvent screen. Its nominal dossier combined low relative solubility (0.70), low nucleation tendency (0.65), high crystal growth (1.30), and low impurity occlusion (0.65). This suggests that cooling produces supersaturation while favoring growth on existing particles rather than formation of many fines. In classical terms, supersaturation may be represented by σ = (C − C*)/C*, with nucleation B = k_b σ^b and growth G = k_g σ^g; the observations are consistent with S2 lowering effective solubility while maintaining a comparatively favorable G/B ratio.

Under the common 340 K reaction and 250 K crystallization recipe, S2 batches 3–4 gave purity 0.991–1.000 and fines 0.380–0.397. By contrast, S3 (batch 5), S1 (batch 6), and S0 (batch 7) produced fines of 0.769, 0.616, and 0.768, respectively, despite acceptable purity and recoveries of 0.411, 0.527, and 0.511. Observation: those alternatives failed the fines constraint. Interpretation: their higher effective nucleation-to-growth ratios generated more small particles. S3’s poor result despite moderately favorable nominal properties also shows that the dossier was only a prior; fixed-world residuals and process-specific behavior mattered.

Catalyst choice affected more than reaction rate. With S2 and otherwise common conditions, C0 in batch 8 produced recovery 0.500, purity 0.978, fines 0.412, normalized crystal size 0.108, conversion 1.000, and selectivity 0.560. C2 in batch 9 remained on-spec but recovery fell to 0.387 and selectivity to 0.431. C3 in batch 10 raised recovery to 0.525 but also raised fines to 0.534, making it off-spec. My interpretation is that catalyst-dependent target and byproduct concentrations alter supersaturation and impurity-mediated nucleation in the downstream mother liquor. C3 may create a larger crystallizable target load but cross into excessive nucleation; C0 provides a better growth/nucleation balance. Direct catalyst effects on crystal surfaces were not tested and remain an alternative explanation.

Reaction–crystallization coupling

Reaction composition determines the concentration of target, byproducts, and degradation products presented to crystallization. Batch 1 used C1/S2 at 370 K for 3600 s and showed conversion 1.000, selectivity about 0.497, byproduct signal 0.387, and degradation warning 0.218. Batch 2 used a shorter, cooler 350 K/1800 s reaction and showed selectivity 0.564, byproduct signal 0.281, and degradation warning 0.073. Its crystal recovery was also higher, 0.473 versus 0.395. These observations motivated abandoning the hotter history.

The interpretation is that prolonged high temperature drove parallel or secondary degradation rather than useful conversion. Such impurities can reduce target concentration, modify nucleation, or become occluded. However, batches 1 and 2 also differed in cooling history, so the recovery difference cannot be assigned solely to reaction temperature. The safer conclusion is that 370 K/3600 s offered no demonstrated benefit and clearly increased the degradation signal.

Process-history dependence

Cooling endpoint and residence history mattered. Batch 1 cooled only to 275 K and then warmed toward ambient during a subsequent wait; its recovery was 0.395. Batch 2 cooled directly to 250 K for 14,400 s and reached 0.473 recovery. This is consistent with deeper cooling increasing supersaturation and crystallized mass, while the warm wait may have allowed partial redissolution. Because reaction conditions were also changed, the magnitude of this effect remains confounded.

A second consecutive 14,400 s period at 250 K did not improve the C0/S2 process. Batch 12 gave recovery 0.486, purity 0.993, and fines 0.427, compared with batch 8’s 0.500, 0.978, and 0.412 after one cold period. Observation: extra cold residence added no measured benefit. Interpretation: the system was already close to its useful recovery plateau after the first period, or any small benefit was hidden by run-to-run and assay variation. This was the reason to retain the shorter batch-8 history.

Seed effects were weaker than initially expected. In matched C1/S2 batches, increasing seed from 0.005 g (batch 3) to 0.05 g (batch 4) changed recovery from 0.437 to 0.452, normalized size from 0.066 to 0.077, and fines from 0.380 to 0.397. These small, partly inconsistent changes do not establish a seed-dose effect. With C3, increasing seed tenfold from 0.05 g in batch 10 to 0.50 g in batch 11 reduced fines only from 0.534 to 0.516 and recovery from 0.525 to 0.516. The larger seed charge moved fines in the desired direction but did not establish an on-spec process.

Revisions and uncertainty

The initial catalyst choice was C1 because it had the highest nominal reference-panel activity. Experimental evidence shifted the recommendation to C0: reaction activity alone did not predict the best constrained crystallization outcome. The initial expectation that more seed would materially suppress fines was also weakened by batches 3–4 and 10–11. Finally, the prediction that a second cold period would increase recovery was not supported by batch 12.

Most comparisons are single batches rather than replicated estimates. The final-assay noise model gives standard deviations of roughly 0.01 for crystal recovery and 0.018 for fines, in addition to process variation. Therefore, the 0.014 recovery difference between batches 8 and 12 is not strong evidence of a real superiority, although the extra residence time still lacks demonstrated value. Likewise, C3’s fines values of 0.534 and 0.516 lie near the 0.50 boundary; the latter is especially uncertain, but neither observed assay met the constraint and neither provides the safety margin of batch 8.

The principal unresolved tradeoff is therefore recovery versus particle quality. S1, S0, and C3 combinations produced recoveries up to 0.527 but excessive fines. C0/S2 sacrificed a small amount of apparent maximum recovery to obtain purity 0.978 and a comfortable fines margin at 0.412. Untested alternatives include controlled partial redissolution/ripening, staged cooling, lower supersaturation generation, or feedback-controlled seeding for C3 or S1. Such strategies might preserve their recovery advantage while reducing fines, but the campaign provides no direct evidence that they would succeed.

Overall, batch 8 is mechanistically consistent with a moderate reaction history that limits degradation, followed by S2-mediated low-solubility crystallization in a growth-favoring regime. It delivered the highest observed seed-excluded recovery among batches that actually satisfied both quality constraints.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.26 | 0.14 | 0.4 |
| Q01 | crystal_purity | 0.94 | 0.87 | 0.99 |
| Q01 | crystal_size | 0.23 | 0.13 | 0.34 |
| Q01 | crystal_yield | 0.43 | 0.32 | 0.54 |
| Q02 | crystal_fines_fraction | 0.34 | 0.2 | 0.5 |
| Q02 | crystal_purity | 0.95 | 0.88 | 0.99 |
| Q02 | crystal_size | 0.2 | 0.11 | 0.31 |
| Q02 | crystal_yield | 0.36 | 0.25 | 0.48 |
| Q03 | crystal_fines_fraction | 0.61 | 0.45 | 0.77 |
| Q03 | crystal_purity | 0.92 | 0.83 | 0.98 |
| Q03 | crystal_size | 0.09 | 0.03 | 0.18 |
| Q03 | crystal_yield | 0.32 | 0.21 | 0.44 |
| Q04 | crystal_fines_fraction | 0.3 | 0.17 | 0.45 |
| Q04 | crystal_purity | 0.94 | 0.86 | 0.99 |
| Q04 | crystal_size | 0.21 | 0.11 | 0.32 |
| Q04 | crystal_yield | 0.35 | 0.24 | 0.47 |
| Q05 | crystal_fines_fraction | 0.29 | 0.16 | 0.44 |
| Q05 | crystal_purity | 0.94 | 0.85 | 0.99 |
| Q05 | crystal_size | 0.22 | 0.12 | 0.34 |
| Q05 | crystal_yield | 0.36 | 0.25 | 0.48 |
| Q06 | crystal_fines_fraction | 0.62 | 0.46 | 0.77 |
| Q06 | crystal_purity | 0.92 | 0.82 | 0.98 |
| Q06 | crystal_size | 0.1 | 0.04 | 0.2 |
| Q06 | crystal_yield | 0.38 | 0.27 | 0.5 |
| Q07 | crystal_fines_fraction | 0.27 | 0.14 | 0.42 |
| Q07 | crystal_purity | 0.95 | 0.87 | 0.99 |
| Q07 | crystal_size | 0.24 | 0.13 | 0.36 |
| Q07 | crystal_yield | 0.38 | 0.27 | 0.5 |
| Q08 | crystal_fines_fraction | 0.32 | 0.15 | 0.53 |
| Q08 | crystal_purity | 0.96 | 0.87 | 1 |
| Q08 | crystal_size | 0.27 | 0.13 | 0.42 |
| Q08 | crystal_yield | 0.27 | 0.15 | 0.4 |
| Q09 | crystal_fines_fraction | 0.58 | 0.32 | 0.8 |
| Q09 | crystal_purity | 0.98 | 0.88 | 1 |
| Q09 | crystal_size | 0.07 | 0.02 | 0.14 |
| Q09 | crystal_yield | 0.015 | 0 | 0.05 |
| Q10 | crystal_fines_fraction | 0.46 | 0.29 | 0.64 |
| Q10 | crystal_purity | 0.95 | 0.85 | 0.99 |
| Q10 | crystal_size | 0.11 | 0.04 | 0.21 |
| Q10 | crystal_yield | 0.1 | 0.04 | 0.19 |
| Q11 | crystal_fines_fraction | 0.29 | 0.16 | 0.45 |
| Q11 | crystal_purity | 0.94 | 0.85 | 0.99 |
| Q11 | crystal_size | 0.23 | 0.12 | 0.35 |
| Q11 | crystal_yield | 0.37 | 0.26 | 0.49 |
| Q12 | crystal_fines_fraction | 0.56 | 0.39 | 0.72 |
| Q12 | crystal_purity | 0.89 | 0.77 | 0.97 |
| Q12 | crystal_size | 0.13 | 0.05 | 0.24 |
| Q12 | crystal_yield | 0.55 | 0.42 | 0.67 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

Q01–Q02 compare solvents under the same highly seeded slow ramp: prior campaign evidence favors S1 over S3 for recovery and fines, although both are predicted on-spec after slow growth. Q03–Q04 isolate seed dose in S0; the larger seed population should suppress secondary nucleation and reduce fines, with only a modest recovery change. Q05–Q06 compare gradual cooling with an immediate crash followed by the same long cold residence: equilibrium recovery should be similar, but the crash is expected to create many persistent fines. Q07–Q08 compare a cold hold with reheating/redissolution; reheating should remove some small crystals and improve size distribution but sacrifice recovery, with wide uncertainty because rapid recooling could instead renucleate fines. Q09–Q10 test residence at 292 K: immediate filtration should recover almost no seed-excluded product, whereas two hours permits measurable growth and may bring the point estimate just inside the fines limit. Q11–Q12 increase reagent concentration at fixed solvent and catalyst; higher target loading should raise fractional recovery but also supersaturation, impurity burden, and fines, creating the main quality–recovery tradeoff. All recipes contain seed, so particles are expected even when seed-excluded recovery is nearly zero. Intervals are deliberately broad because the very long ramps, crash cooling, reheating, low scale, and concentration change lie outside the directly tested campaign region; several feasibility calls, especially Q02, Q08, Q10, and Q12, remain threshold-sensitive.

## K2

1. Claim status

Supported by direct observations:
- S2 was the most robust screened solvent for the stated quality constraints. Under the common 340 K/250 K recipe, S2 batches 3–4 had purity 0.991–1.000 and fines 0.380–0.397. S3, S1 and S0 in batches 5–7 had fines 0.769, 0.616 and 0.768. The interpretation that S2 has a favorable growth-to-nucleation balance is plausible from its nominal properties, but nucleation and growth rates were not measured directly.
- Batch 8 was the highest-recovery observed feasible batch: C0/S2 gave crystal yield 0.500, purity 0.978 and fines 0.412. C2 was feasible but lower-yielding in batch 9 (0.387), while C3 had higher recovery in batch 10 (0.525) but failed on fines (0.534).
- The severe reaction history was unfavorable. Batch 1 at 370 K for 3600 s had degradation warning 0.218 and selectivity about 0.497, versus 0.073 and 0.564 in batch 2 at 350 K for 1800 s. Interpreting this as thermally promoted degradation is reasonable, although the downstream recovery comparison is confounded by different cooling histories.
- Increasing C3 seed from 0.05 g in batch 10 to 0.50 g in batch 11 moved fines only from 0.534 to 0.516 and did not produce an observed feasible batch. Likewise, the matched C1 seed comparison in batches 3–4 showed only small changes. Thus a strong seed-dose benefit was not supported.
- Extending the C0/S2 cold history did not improve the observed result: batch 12 gave yield 0.486 and fines 0.427 versus 0.500 and 0.412 in batch 8. The difference is small relative to noise and process variability, so this supports only the operational conclusion that extra time had no demonstrated benefit—not a strong claim that it lowers recovery.

Contradicted or revised:
- The initial prior that nominally most-active C1 would be the best catalyst was contradicted by the constrained process results; C0 produced the best observed feasible recovery.
- The expectation that substantially more seed would reliably suppress fines was weakened by batches 3–4 and contradicted operationally by batches 10–11, where even tenfold more seed left C3 off-spec.
- The pre-batch-12 prediction that a second cold period would improve recovery was not borne out.

Still untested:
- The proposed causal law that catalyst-dependent liquor composition changes supersaturation and nucleation was not directly measured. A direct catalyst–crystal-surface effect remains possible.
- No nucleation rate, growth rate, solubility curve or supersaturation trajectory was observed, so the growth/nucleation equations were explanatory models rather than fitted laws.
- Controlled slow ramps, deliberate ripening after crystallization, concentration effects and rapid-crash histories were not tested in the campaign. The corresponding held-out predictions remain extrapolations.

2. One additional experiment

I would repeat the batch-10 C3/S2 composition and reaction exactly, including 0.05 g seed and the same 250 K endpoint, but replace its single 4-hour cooling operation with a long, staged temperature ramp from the post-reaction temperature to 250 K. I would take non-destructive particle-size readings at an intermediate temperature and immediately before filtration, followed by the normal final assay.

This uses batch 10 as the matched historical control and distinguishes two main explanations:
- Kinetic supersaturation explanation: C3’s high fines arose because target accumulated faster than the original cooling history could accommodate by seeded growth. A slower ramp should increase size/CSD quality, reduce fines below 0.50, and retain recovery near 0.50 or higher.
- Composition or surface-specific explanation: C3-generated impurities, or a catalyst-dependent surface interaction, intrinsically promote secondary nucleation or inhibit growth. Fines would remain above 0.50 despite slow supersaturation generation, perhaps with little size improvement.

An intermediate reading showing fines rise abruptly only late in the ramp would support a supersaturation threshold. Persistently high fines from early in the ramp would favor impurity-mediated nucleation or ineffective seeds. A third possible outcome—low fines but substantially reduced recovery—would expose a genuine recovery/ripening tradeoff rather than either simple explanation.

3. Least-used observation and least-reliable prediction

The account used crystal CSD-quality observations least effectively. For example, batch 8 had CSD quality 0.727, versus 0.627 for C3 batch 10 and 0.543 for S3 batch 5. Those measurements broadly reinforce the proposed growth-versus-secondary-nucleation interpretation, but the report concentrated on the hard fines constraint and barely integrated CSD quality or its pre-filtration measurements. A stronger analysis would compare how CSD quality, normalized size and fines moved together and whether filtration changed them.

Q08 is the least reliable held-out prediction. It adds a 315 K reheating/redissolution step after a very long slow crystallization, followed by only one hour of recooling. No campaign batch reheated an established crystal population, so neither the dissolution fraction nor the balance between selective fines dissolution, survivor growth and renewed nucleation was calibrated. I predicted lower recovery with improved size distribution, but rapid recooling could instead generate fresh fines, while extensive dissolution could leave much less recovered product. Its broad interval reflected this unresolved sign and magnitude. Q10 is also threshold-sensitive, but Q08 requires a qualitatively new mechanism and is therefore the larger extrapolation.
