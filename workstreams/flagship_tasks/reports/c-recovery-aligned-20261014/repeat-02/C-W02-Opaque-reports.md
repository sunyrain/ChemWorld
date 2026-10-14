# C-W02-Opaque — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

The campaign supports a coupled reaction–crystallization picture in which catalyst choice mainly controls how much target product enters the crystallization stage, while solvent and thermal history strongly control particle quality.

Reaction stage — observations: All catalyst-screen batches used solvent S0 and nominally the same 350 K, 3600 s reaction. Batch 1 (C0) gave HPLC conversion 1.000, selectivity 0.683, and reaction yield 0.677. The corresponding values were 0.985/0.629/0.600 for batch 2 (C1), 0.998/0.439/0.440 for batch 3 (C2), and 1.000/0.577/0.588 for batch 4 (C3). Thus C0 was the best observed catalyst, particularly relative to C2. Because each catalyst condition was run once, this establishes an empirical ranking for the tested recipe rather than a universal kinetic law.

Reaction-stage interpretation: Conversion was nearly complete in every case, so catalyst effects appeared principally through product-versus-byproduct partitioning rather than incomplete reagent consumption. A useful approximate accounting relation is n_target,liquid ≈ n_R,0 X S_rxn, where X is conversion and S_rxn is target selectivity. Under this interpretation, C0 provides the largest target inventory available for recovery. Untested alternatives include different catalyst rankings at shorter residence time, lower temperature, or lower catalyst loading.

Solvent effects — observations: With C0, changing solvent substantially altered the final crystal population. Batch 1 (S0) gave crystal yield 0.530, purity 0.979, and fines fraction 0.854. Under the staged-cooling solvent screen, batch 5 (S1) gave 0.568/0.974/0.753; batch 6 (S2) gave 0.538/1.000/0.607; and batch 7 (S3) gave 0.436/0.967/0.803. S1 preserved the greatest recovery, whereas S2 produced the lowest fines fraction. All four products comfortably exceeded the purity requirement.

Solvent interpretation: S2 probably changes target solubility, metastable-zone width, or the relative rates of nucleation and growth. In standard crystallization notation, supersaturation may be written σ = C/C*(T,solvent) − 1, with nucleation and growth represented schematically as J = k_J σ^m and G = k_G σ^g. Because nucleation is commonly more nonlinear in σ than growth, a solvent that lowers peak σ or broadens the metastable zone can reduce the number of new fine particles without proportionally eliminating crystal growth. The experiment did not independently measure solubility or supersaturation, so this is a mechanistic interpretation, not a directly observed material property. Solvent-dependent viscosity, aggregation, or seed wetting remain plausible alternatives.

Reaction–crystallization coupling: The seed-excluded recovery can be decomposed conceptually as

Y_crystal = (n_target,solid excluding seed)/n_R,0 ≈ X S_rxn f_cryst f_retain,

where f_cryst is the fraction of produced target transferred to crystals and f_retain represents separation losses. This explains why a productive catalyst is necessary but insufficient: C0 generated high reaction yield, yet S0 produced excessive fines; S2 sacrificed some reaction-stage yield but gave a substantially better particle distribution. High final purities of approximately 0.97–1.00 show that impurity rejection during crystallization was robust over the explored range, leaving fines rather than purity as the binding constraint.

Process-history dependence — recommended batch 8: Batch 8 used 0.040 mol reagent, 0.080 L S2, and 0.005 mol C0; reaction at 350 K for 3600 s; cooling to 320 K; 0.020 g seed; staged cooling through 300 K to 270 K; reheating to 310 K; and recooling through 290 K to 270 K before filtration. Its final assay gave crystal yield 0.537, purity 0.979, fines fraction 0.575, normalized crystal size 0.101, and CSD quality 0.662. It was recommended because it gave the best observed compromise between recovery and particle quality, not because it satisfied every specification.

The modest improvement in batch 8 is consistent with partial dissolution during the 310 K excursion preferentially removing small, high-curvature crystallites, followed by regrowth on surviving particles during recooling. Particle size therefore depends on the entire temperature–supersaturation trajectory, not only the final temperature. A schematic population balance is ∂n(L,t)/∂t + ∂[G(t)n(L,t)]/∂L = B(t,L) − D(t,L), where B includes primary and secondary nucleation and D includes dissolution or loss. Thermal cycling changes the signs and magnitudes of G, B, and D over time.

However, stronger or repeated cycling did not monotonically improve quality. Batch 9 used two reheating/recooling cycles and ended at yield 0.500, fines 0.652, purity 0.982, and degradation warning 0.165, all worse than batch 8 except purity. Batch 12 crystallized deeply and then heated to 325–330 K before warm filtration; it gave only 0.345 recovery and fines 0.863. These results argue against a simple rule that more reheating always removes fines. Reheating can dissolve useful large crystals, extended processing can permit degradation or secondary nucleation, and recooling can recreate the fine population.

Other process revisions were also unsuccessful. Halving reagent and catalyst charge in batch 10 did not suppress fines: recovery was 0.483 and fines 0.677. Ending the crystallization at 300 K in batch 11 likewise gave only 0.476 recovery with fines 0.629. Seed-dose comparisons were confounded by catalyst, solvent, and thermal-history changes: batch 2 used 0.001 g seed and had fines 0.945, while batch 3 used 0.050 g and had fines 0.868, so the campaign does not isolate a seed-mass effect.

Revision of the working mechanism: The initial expectation was that moderate reaction conditions, seeding, and slow cooling would jointly provide acceptable recovery and fines. Batches 1–7 rejected that broad expectation because every final fines fraction exceeded 0.50. The evidence shifted emphasis from catalyst selection alone to solvent-mediated nucleation control, with C0/S2 emerging as the most promising pairing. Batch 8 then suggested a limited benefit from one mild dissolution/regrowth cycle. Batches 9 and 12 rejected the stronger hypothesis that increasingly aggressive thermal cycling would continue improving the distribution.

Uncertainty and unresolved tradeoff: No completed batch met both purity ≥0.80 and fines ≤0.50. Batch 8 remained about 0.075 above the fines boundary. Final-assay noise scales were approximately 0.010 for crystal yield and purity and 0.018 for fines, with additional process uncertainty, so batch 8 cannot be represented as compliant. Moreover, most conditions were unreplicated and several comparisons changed more than one factor. The observed campaign therefore leaves an unresolved quality–recovery tradeoff: deep cooling supports recovery but promotes nucleation; warm dissolution can reduce recoverable solid and may not selectively remove fines; long histories increase degradation risk. A future study would need replicated C0/S2 experiments that independently vary seed dose, cooling rate, endpoint temperature, and a single controlled annealing excursion, ideally supported by solubility or supersaturation measurements.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.38 | 0.23 | 0.55 |
| Q01 | crystal_purity | 0.97 | 0.93 | 0.995 |
| Q01 | crystal_size | 0.14 | 0.08 | 0.22 |
| Q01 | crystal_yield | 0.45 | 0.33 | 0.56 |
| Q02 | crystal_fines_fraction | 0.52 | 0.35 | 0.7 |
| Q02 | crystal_purity | 0.96 | 0.91 | 0.995 |
| Q02 | crystal_size | 0.13 | 0.06 | 0.22 |
| Q02 | crystal_yield | 0.34 | 0.23 | 0.46 |
| Q03 | crystal_fines_fraction | 0.72 | 0.56 | 0.86 |
| Q03 | crystal_purity | 0.97 | 0.92 | 0.995 |
| Q03 | crystal_size | 0.07 | 0.03 | 0.13 |
| Q03 | crystal_yield | 0.43 | 0.31 | 0.54 |
| Q04 | crystal_fines_fraction | 0.34 | 0.2 | 0.51 |
| Q04 | crystal_purity | 0.97 | 0.93 | 0.995 |
| Q04 | crystal_size | 0.15 | 0.08 | 0.23 |
| Q04 | crystal_yield | 0.42 | 0.3 | 0.54 |
| Q05 | crystal_fines_fraction | 0.29 | 0.16 | 0.45 |
| Q05 | crystal_purity | 0.97 | 0.93 | 0.995 |
| Q05 | crystal_size | 0.16 | 0.09 | 0.24 |
| Q05 | crystal_yield | 0.43 | 0.31 | 0.55 |
| Q06 | crystal_fines_fraction | 0.67 | 0.5 | 0.82 |
| Q06 | crystal_purity | 0.97 | 0.92 | 0.995 |
| Q06 | crystal_size | 0.075 | 0.03 | 0.14 |
| Q06 | crystal_yield | 0.44 | 0.32 | 0.56 |
| Q07 | crystal_fines_fraction | 0.27 | 0.14 | 0.43 |
| Q07 | crystal_purity | 0.97 | 0.93 | 0.995 |
| Q07 | crystal_size | 0.17 | 0.1 | 0.26 |
| Q07 | crystal_yield | 0.43 | 0.31 | 0.55 |
| Q08 | crystal_fines_fraction | 0.59 | 0.41 | 0.75 |
| Q08 | crystal_purity | 0.965 | 0.91 | 0.995 |
| Q08 | crystal_size | 0.095 | 0.04 | 0.17 |
| Q08 | crystal_yield | 0.38 | 0.26 | 0.5 |
| Q09 | crystal_fines_fraction | 0.48 | 0.28 | 0.68 |
| Q09 | crystal_purity | 0.96 | 0.86 | 0.995 |
| Q09 | crystal_size | 0.08 | 0.04 | 0.14 |
| Q09 | crystal_yield | 0.025 | 0.005 | 0.08 |
| Q10 | crystal_fines_fraction | 0.4 | 0.23 | 0.59 |
| Q10 | crystal_purity | 0.97 | 0.91 | 0.995 |
| Q10 | crystal_size | 0.105 | 0.05 | 0.18 |
| Q10 | crystal_yield | 0.2 | 0.09 | 0.32 |
| Q11 | crystal_fines_fraction | 0.32 | 0.18 | 0.49 |
| Q11 | crystal_purity | 0.97 | 0.93 | 0.995 |
| Q11 | crystal_size | 0.15 | 0.08 | 0.23 |
| Q11 | crystal_yield | 0.43 | 0.31 | 0.55 |
| Q12 | crystal_fines_fraction | 0.56 | 0.39 | 0.72 |
| Q12 | crystal_purity | 0.94 | 0.87 | 0.985 |
| Q12 | crystal_size | 0.1 | 0.05 | 0.17 |
| Q12 | crystal_yield | 0.5 | 0.37 | 0.62 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

All recipes contain seed and a crystallization step, so particles are expected throughout. For the solvent pair, S1 is predicted to preserve more target recovery and generate fewer fines than S3, consistent with the campaign solvent ranking, although both intervals are broad because the present C1/385 K regime is extrapolative. Increasing seed from 0.001 to 0.045 g should suppress uncontrolled nucleation and shift the population toward larger particles without materially changing seed-excluded recovery. Slow stepped cooling should give similar equilibrium recovery but markedly fewer fines than a rapid drop followed by a low-temperature hold. The 315 K reheat/rapid recool is expected to lose some recovered solid and regenerate fines, based on the adverse aggressive-cycle results. Extending growth at 292 K should substantially increase seed-excluded yield and modestly enlarge particles relative to immediate filtration, though the short-history predictions are especially uncertain. Doubling upstream reagent loading should raise overall crystal recovery through greater supersaturation but also increase secondary nucleation, impurity incorporation, and fines. Purity is generally predicted above 0.80 because crystallization rejected impurities robustly in the campaign; feasibility classifications use the point estimates, while intervals show substantial uncertainty from unreplicated material effects, reaction-condition extrapolation, and history-dependent nucleation.

## K2

1. Supported, contradicted, and untested claims

Supported by direct observations:
- Catalyst choice affected reaction selectivity more than conversion under the screened S0 conditions. Batches 1–4 all approached complete conversion, while C0 in batch 1 gave the highest HPLC selectivity and yield (0.683 and 0.677), compared with C1 in batch 2 (0.629 and 0.600), C2 in batch 3 (0.439 and 0.440), and C3 in batch 4 (0.577 and 0.588). Interpreting this as different product/byproduct partitioning is reasonable, but the underlying catalytic pathways were not observed directly.
- Solvent affected particle quality. In the C0 solvent comparison, S2 in batch 6 had lower final fines (0.607) than S1 in batch 5 (0.753) and S3 in batch 7 (0.803), while retaining 0.538 crystal yield and essentially unit purity. This directly supports a solvent association; attributing it specifically to solubility or metastable-zone width remains interpretation.
- Crystallization robustly rejected impurities. Every completed batch had final crystal purity well above 0.80, generally about 0.97–1.00, despite sizable reaction byproduct signals.
- Thermal history mattered non-monotonically. Batch 8’s single mild cycle gave fines 0.575, whereas the more aggressive histories in batch 9 and batch 12 gave 0.652 and 0.863. This directly contradicts any monotonic “more reheating gives fewer fines” rule.

Contradicted or narrowed:
- The initial expectation that seeding plus slow staged cooling would be sufficient for specification was contradicted: none of the 12 batches reached fines ≤0.50.
- Lower loading was not an effective fines-control intervention in the tested form. Batch 10 still had fines 0.677 and yield 0.483.
- Simply filtering at a warmer endpoint did not solve the tradeoff. Batch 11, ending at 300 K, still had fines 0.629 while recovery fell to 0.476.
- Selective fines dissolution during the batch 8 cycle remains only a possible explanation, not a demonstrated mechanism. Batch 8 improved relative to batch 6, but it was not replicated and several history variables differed.

Still untested:
- Solubility curves, supersaturation, metastable-zone widths, and nucleation or growth rate laws were never measured.
- Seed dose was not isolated: batches with different seed masses also changed catalyst, solvent, or thermal history.
- Aggregation, attrition, seed wetting, and secondary nucleation remain alternatives to a purely dissolution–regrowth account.
- The C0 catalyst ranking was not tested outside the original temperature, concentration, and residence-time regime.

2. One additional experiment

I would repeat the C0/S2 batch-8 recipe but add particle-size observations at three mechanistically diagnostic points: immediately before the 310 K reheat, immediately after that reheat, and after the final recooling. Small liquid samples for HPLC before and after reheating would track target loss and byproduct growth. The batch would then be filtered and assayed normally.

This experiment would distinguish:
- Selective fines dissolution: reheating should immediately lower the fines fraction, increase number-weighted size, and reduce solid recovery; subsequent slow recooling should restore some recovery without fully recreating fines.
- Re-nucleation during recooling: the post-reheat distribution might improve, followed by a sharp fines rebound during recooling.
- Chemical degradation rather than physical dissolution: HPLC target signal should decrease and byproduct signal increase during the warm interval.
- Attrition or aggregation effects: particle metrics could change without a corresponding change in dissolved target inventory.

If batch 8’s apparent benefit was mostly noise or batch variability, the staged measurements and final result would show no coherent dissolution–regrowth sequence. This single experiment would not establish reproducibility as strongly as a replicate series, but it would provide the most direct mechanistic discrimination within one batch.

3. Least effectively used observation and least reliable held-out prediction

The observation used least effectively was the discrepancy within batch 8 between the in-process particle measurement and final assay. Before filtration, the particle instrument reported fines about 0.587 and normalized size about 0.058; the final assay reported fines about 0.575 but size about 0.101. My account emphasized the favorable final size and fines without adequately confronting the large size disagreement. It may reflect instrument modality, process-proxy uncertainty, filtration-state effects, or ordinary noise, but it weakens any strong claim that the cycle genuinely enlarged the number-weighted population.

Q09 is the least reliable held-out prediction. It filters only 60 seconds after cooling to 292 K, so the solid population may be dominated by added seed while seed-excluded target recovery is extremely small. No campaign batch probed such a short growth interval, and the relationship between seed mass, measured fines, crystal purity, and near-zero newly crystallized product was not calibrated. Its predicted fines estimate of 0.48 is also close to the 0.50 feasibility boundary, making the Boolean quality classification particularly fragile. No truth was available, so this is an uncertainty assessment rather than a revision of the sealed prediction.
