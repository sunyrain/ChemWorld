# C-W03-Opaque — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

## Mechanistic account

### 1. Observed process map

The best qualifying result was batch 11: C1/S2, 430 K for 900 s, 0.001 g seed, then two 14,400 s cooling stages to 325 and 290 K. Its final assay gave reaction yield 0.772, selectivity 0.792, seed-excluded crystal yield 0.694, purity 1.000, and fines fraction 0.138.

The campaign suggests a coupled sequence:

1. Catalyst, solvent, temperature, and residence time establish target concentration and impurity composition.
2. That composition and the preceding thermal history determine supersaturation during cooling.
3. Seed survival, nucleation, and growth determine both isolated recovery and particle-number distribution.

A useful bookkeeping relationship is

Y_crystal = n(target in recovered solid, excluding seed) / n(initial reagent)
          ≈ Y_reaction × f_isolation,

where f_isolation includes crystallization and filtration recovery. For batches 4 and 8–11, f_isolation was approximately 0.88–0.90. Thus, over this operating region, improvements in reaction yield generally translated efficiently into crystal recovery. Batch 12 was a sharp exception.

### 2. Material effects

#### Catalyst

Under the common S2, 370 K/3600 s, low-seed staged-cooling protocol:

- Batch 4, C1: reaction yield 0.578, selectivity 0.592, crystal yield 0.507, fines 0.304.
- Batch 6, C2: reaction yield 0.518, selectivity 0.516, crystal yield 0.453, fines 0.327.
- Batch 7, C3: reaction yield 0.534, selectivity 0.508, crystal yield 0.469, fines 0.265.

Observation: C1 gave the highest target and crystal yields; C3 gave somewhat fewer fines but lower recovery. Interpretation: C1 favors target-forming chemistry, while C3 may generate a solution composition more favorable to a coarse particle population. Because each condition was run once, these are provisional material rankings rather than replicated effects.

C0 appeared inferior in batch 1, which gave selectivity 0.477 and crystal yield 0.405, but that batch used different charge, seed, and cooling conditions. A clean C0 comparison was not performed.

#### Solvent

With C1 at 370 K/3600 s and the same 0.001 g seed and staged cooling:

- Batch 3, S1: reaction yield 0.580, crystal yield 0.483, purity 0.997, fines 0.440.
- Batch 4, S2: reaction yield 0.578, crystal yield 0.507, purity 1.000, fines 0.304.
- Batch 5, S3: reaction yield 0.502, crystal yield 0.385, purity 0.980, fines 0.355.

S1 and S2 had nearly identical reaction yields, but S2 produced higher crystal recovery and fewer fines. This supports a crystallization-specific solvent effect—likely through target solubility, supersaturation development, or impurity adsorption—rather than only a reaction-rate effect. S3 was worse in both reaction and recovery. S0 was not tested under the identical low-seed protocol.

### 3. Temperature–time history and reaction selectivity

For C1/S2 with a common downstream sequence, moving to shorter, hotter reaction treatments produced a strong improvement:

- Batch 8, 350 K/7200 s: reaction yield 0.440, selectivity 0.449, crystal yield 0.387, fines 0.602.
- Batch 9, 390 K/1800 s: reaction yield 0.699, selectivity 0.686, crystal yield 0.627, fines 0.220.
- Batch 10, 410 K/1200 s: reaction yield 0.756, selectivity 0.748, crystal yield 0.677, fines 0.146.
- Batch 11, 430 K/900 s: reaction yield 0.772, selectivity 0.792, crystal yield 0.694, fines 0.138.

A qualitative kinetic representation is

X = 1 − exp[−∫k_target(T)dt],

with competing byproduct/degradation exposure governed by analogous integrals. The results imply that rapid high-temperature target formation followed by prompt cooling was preferable to prolonged exposure at lower temperature. This is only a mechanistic interpretation: no activation energies or fitted rate constants were established.

The trend was not safely extrapolatable. Batch 12, treated at 450 K for 600 s, had reaction yield 0.808 and selectivity 0.803 but crystal yield only 0.003. Thus, reaction assay performance alone did not guarantee recoverable product.

### 4. Crystallization mechanism and seeding

The initial batch used 0.05 g seed and direct cooling to 280 K over 7200 s. It produced fines 0.751 and a size index of 0.062. Batch 2 used 0.005 g seed and staged, longer cooling; fines fell to 0.521 and the size index increased to 0.104. Batches 3–11 generally used only 0.001 g seed and two long cooling stages, often giving fines below 0.50.

A conventional qualitative model is useful:

S = C/C*(T),
J ∝ (S−1)^b,
G ∝ (S−1)^g,

where S is supersaturation, J is nucleation rate, and G is crystal growth rate. Rapid generation of high supersaturation creates many nuclei and fines; staged cooling and a small seed population can allocate solute to growth instead. The batch results are consistent with that mechanism, but seed dose and cooling profile were changed together early in the campaign, so their independent contributions remain unresolved.

Upstream history also changed the downstream particle distribution even when the nominal cooling recipe was unchanged. For example, batch 8 had fines 0.602, whereas batches 9–11 had 0.220, 0.146, and 0.138. Higher target concentration, different impurity ratios, or different seed survival at the starting temperature could all change nucleation and growth.

### 5. Interpreting the batch-12 discontinuity

Batch 12 combined almost complete reaction performance with negligible crystal recovery, extremely low fines (0.002), and a much larger size index (0.417). A plausible interpretation is that seeding at the hotter starting condition dissolved or deactivated most seeds. Only a very small number of crystals then formed and grew large, leaving almost all target in solution. This explains the simultaneous low particle count/fines, large observed particles, and very poor mass recovery.

Untested alternatives include formation of an unrecognized solid form, oiling, a thermal-history-dependent solubility change, or an impurity effect not captured by the reported selectivity. The final endpoint was colder than in batch 11, so simple insufficient cooling is not an adequate explanation by itself.

### 6. Purity, recovery, and unresolved tradeoffs

Purity was not the limiting attribute in the best region: batches 3–11 generally gave approximately 0.98–1.00 crystal purity despite moderate reaction selectivity. This suggests strong rejection of soluble byproducts during crystallization or filtration. The dominant constraints were recovery and fines.

There was no unavoidable recovery–fines conflict between batches 8 and 11: hotter/shorter reaction histories improved both. However, batch 12 exposed a different tradeoff—very coarse, nearly fines-free particles accompanied by essentially zero recovery. Consequently, minimizing fines alone would select a physically poor process. A practical optimization should maximize recovery subject to both purity and fines constraints, rather than maximize particle size or CSD quality independently.

### 7. Revisions and uncertainty

The initial view was that catalyst/solvent screening would dominate and that slower seeded cooling would reduce fines. The first point was supported, particularly for C1/S2. The second was directionally supported but remains confounded because seed mass, cooling stages, catalyst, and charge changed between early batches.

After batches 8–11, a monotonic hotter/shorter improvement appeared plausible. Batch 12 decisively revised that view: the useful region ends before 450 K under this seeding protocol, and the response is discontinuous at the process level even though reaction yield remains high.

Final-assay nominal standard uncertainties were about 0.01 for crystal yield, 0.01 for purity, and 0.018 for fines. Many principal contrasts—especially batches 8 versus 11 and 11 versus 12—were far larger than those values. Nevertheless, there were no replicate batches, so run-to-run process variability and interaction effects are not quantified. The mechanistic equations above are explanatory relationships, not validated fitted laws.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | crystal_fines_fraction | 0.3 | 0.16 | 0.47 |
| Q01 | crystal_purity | 0.985 | 0.95 | 1 |
| Q01 | crystal_size | 0.14 | 0.08 | 0.23 |
| Q01 | crystal_yield | 0.5 | 0.36 | 0.63 |
| Q02 | crystal_fines_fraction | 0.26 | 0.13 | 0.43 |
| Q02 | crystal_purity | 0.965 | 0.91 | 0.995 |
| Q02 | crystal_size | 0.13 | 0.07 | 0.22 |
| Q02 | crystal_yield | 0.42 | 0.29 | 0.56 |
| Q03 | crystal_fines_fraction | 0.11 | 0.04 | 0.24 |
| Q03 | crystal_purity | 0.99 | 0.96 | 1 |
| Q03 | crystal_size | 0.26 | 0.15 | 0.4 |
| Q03 | crystal_yield | 0.5 | 0.35 | 0.64 |
| Q04 | crystal_fines_fraction | 0.32 | 0.18 | 0.5 |
| Q04 | crystal_purity | 0.985 | 0.95 | 1 |
| Q04 | crystal_size | 0.13 | 0.07 | 0.22 |
| Q04 | crystal_yield | 0.51 | 0.37 | 0.65 |
| Q05 | crystal_fines_fraction | 0.28 | 0.15 | 0.45 |
| Q05 | crystal_purity | 0.985 | 0.95 | 1 |
| Q05 | crystal_size | 0.15 | 0.08 | 0.24 |
| Q05 | crystal_yield | 0.51 | 0.37 | 0.65 |
| Q06 | crystal_fines_fraction | 0.58 | 0.39 | 0.75 |
| Q06 | crystal_purity | 0.93 | 0.84 | 0.98 |
| Q06 | crystal_size | 0.075 | 0.035 | 0.14 |
| Q06 | crystal_yield | 0.52 | 0.37 | 0.66 |
| Q07 | crystal_fines_fraction | 0.24 | 0.12 | 0.4 |
| Q07 | crystal_purity | 0.987 | 0.95 | 1 |
| Q07 | crystal_size | 0.16 | 0.09 | 0.26 |
| Q07 | crystal_yield | 0.51 | 0.37 | 0.65 |
| Q08 | crystal_fines_fraction | 0.13 | 0.05 | 0.27 |
| Q08 | crystal_purity | 0.992 | 0.96 | 1 |
| Q08 | crystal_size | 0.22 | 0.12 | 0.36 |
| Q08 | crystal_yield | 0.46 | 0.3 | 0.61 |
| Q09 | crystal_fines_fraction | 0.7 | 0.51 | 0.85 |
| Q09 | crystal_purity | 0.99 | 0.95 | 1 |
| Q09 | crystal_size | 0.045 | 0.015 | 0.1 |
| Q09 | crystal_yield | 0.035 | 0.005 | 0.12 |
| Q10 | crystal_fines_fraction | 0.46 | 0.28 | 0.65 |
| Q10 | crystal_purity | 0.98 | 0.92 | 1 |
| Q10 | crystal_size | 0.085 | 0.04 | 0.16 |
| Q10 | crystal_yield | 0.25 | 0.13 | 0.4 |
| Q11 | crystal_fines_fraction | 0.3 | 0.16 | 0.47 |
| Q11 | crystal_purity | 0.985 | 0.95 | 1 |
| Q11 | crystal_size | 0.14 | 0.08 | 0.23 |
| Q11 | crystal_yield | 0.51 | 0.37 | 0.65 |
| Q12 | crystal_fines_fraction | 0.45 | 0.27 | 0.64 |
| Q12 | crystal_purity | 0.95 | 0.87 | 0.99 |
| Q12 | crystal_size | 0.13 | 0.07 | 0.22 |
| Q12 | crystal_yield | 0.39 | 0.24 | 0.55 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

All recipes explicitly add crystalline seed, so particles are expected even when little new target crystallizes. For the solvent pair, S1 is predicted to retain the higher recovery and purity seen in the campaign, while S3 gives lower reaction-derived recovery but slightly fewer fines. The low-seed member Q03 should distribute solute over fewer nuclei than Q04, producing larger particles and fewer fines, with similar equilibrium recovery after the very long cooling schedule. Gradual cooling in Q05 should suppress secondary nucleation relative to the initial temperature crash in Q06; the long cold holds make their recoveries similar, but are not assumed to erase the early CSD difference. The reheat–recool cycle in Q08 is expected to dissolve fines and promote ripening relative to Q07, at the cost of incomplete recovery during the short final recooling. The additional 292 K hold in Q10 should materially increase growth and recovery relative to Q09, although its fines estimate remains near the feasibility boundary. Doubling upstream loading in Q12 at fixed catalyst increases supersaturation and lowers catalyst-to-reagent ratio, so I predict more fines, lower purity, and lower fractional overall recovery than Q11. Intervals are deliberately broad because these recipes extrapolate to much lower catalyst/loading and much longer crystallization histories than the sealed campaign, with no direct replicates; borderline feasibility assignments, especially Q10 and Q12, are correspondingly uncertain.

## K2

## 1. Status of the main claims

### Supported within the tested scope

- **C1/S2 was the best tested material combination for qualifying recovery.** Direct common-protocol comparisons support this. With S2 at 370 K/3600 s, batch 4 using C1 gave crystal yield 0.507, versus 0.453 for C2 in batch 6 and 0.469 for C3 in batch 7. With C1, batch 4 using S2 exceeded S1 in batch 3 and S3 in batch 5 in crystal yield and fines performance. Interpretation that these differences arise from catalyst selectivity and solvent-dependent solubility is plausible, but those microscopic causes were not directly measured.

- **The 350–430 K series favored progressively hotter, shorter reaction histories.** Batches 8–11 directly showed crystal yield increasing from 0.387 to 0.627, 0.677, and 0.694, while fines decreased from 0.602 to 0.220, 0.146, and 0.138. This supports the empirical process relationship, not a fitted Arrhenius mechanism.

- **Reaction yield generally translated efficiently into crystal yield over batches 4 and 8–11.** The implied isolation fraction was about 0.88–0.90. This directly supports the bookkeeping factorization `crystal yield ≈ reaction yield × isolation fraction` locally.

- **Purity was not the limiting constraint in the productive region.** Batches 3–11 generally produced crystal purity near 0.98–1.00. The observation is direct; the proposed explanation that crystallization rejected soluble impurities remains interpretive because mother-liquor composition was not separately quantified.

- **Batch 12 demonstrated a real recovery/CSD discontinuity.** Despite reaction yield 0.808 and selectivity 0.803, it gave crystal yield 0.003, size index 0.417, and fines 0.002. Thus, excellent reaction metrics did not guarantee overall recovery, and extremely coarse, fines-free material could coexist with negligible recovered target.

### Contradicted or revised

- **A monotonic “hotter and shorter is always better” claim was contradicted.** Batches 8–11 suggested that trend, but batch 12 at 450 K/600 s sharply broke it. The defensible claim is restricted to the observed 350–430 K region under the tested downstream history.

- **A simple inverse relation between median particle size and fines is inadequate.** For example, batch 2 had a larger size index than batch 3 but also more fines. Size and number fraction below 20 µm describe different parts of the distribution and need not move monotonically together.

### Still untested or only weakly supported

- **The independent effects of seed dose and cooling rate remain untested.** Batch 1 versus batch 2 changed catalyst, loading, seed dose, and cooling history together. Later low-seed batches generally performed well, but there was no controlled seed-only comparison in the campaign.

- **The proposed seed-dissolution explanation for batch 12 is untested.** Its large particles, nearly zero fines, and negligible recovery are consistent with loss of effective seeds at 450 K, but an altered solid form, oiling, persistent supersaturation, or an unobserved chemical change could produce similar observations.

- **C0’s ranking is unresolved.** Batch 1 used C0 but differed from the controlled C1/C2/C3 comparisons in several other variables.

- **Repeatability is untested.** Material and temperature comparisons were single batches. Most major differences exceed nominal assay noise, but run-to-run process variability was not measured.

## 2. One additional experiment

I would repeat the batch-12 C1/S2 reaction—450 K for 600 s—but delay addition of the same seed dose until the mixture has cooled to 325 K. I would then use the same subsequent cooling and filtration history as batch 12.

This experiment distinguishes two principal explanations:

1. **High-temperature seed dissolution or deactivation.** If this dominated batch 12, adding seed only after cooling should restore nucleation and substantial crystal recovery, plausibly toward the batch-11 scale, while increasing particle count and fines relative to batch 12.
2. **An irreversible upstream change caused by the 450 K exposure.** If the product became uncrystallizable, formed another phase, or underwent an assay-invisible transformation, delayed seeding would not rescue recovery; crystal yield would remain near zero despite viable low-temperature seed.

An intermediate recovery would indicate mixed control: partial upstream damage combined with loss of effective seeds. This single experiment is more diagnostic than merely repeating batch 12 because it changes the causal feature implicated by the observed sparse, coarse particles.

## 3. Least effectively used observation and least reliable prediction

### Least effectively used observation

The account used the joint **crystal-size and fines observations** least effectively, particularly the contrast between batches 2 and 3. Batch 2 had size index 0.104 with fines 0.521, whereas batch 3 had a smaller size index of 0.071 but fewer fines, 0.440. My explanation leaned heavily on a simple “fewer seeds/slower cooling gives larger particles and fewer fines” narrative. The data show that the number-weighted median and the sub-20-µm fraction can respond differently to distribution breadth or multiple particle populations. Without full particle-size distributions, attributing both metrics to one nucleation–growth axis was oversimplified.

### Least reliable held-out prediction

**Q09 is the least reliable prediction.** It filters only 60 seconds after cooling to 292 K, whereas every campaign batch allowed crystallization for thousands of seconds. Its particle population may therefore be dominated by the added seed, while crystal yield explicitly excludes seed mass. The campaign provides little evidence for the onset kinetics of target deposition over the first minute or for how seed particles alone affect the reported size and fines metrics. Consequently, the predicted very low yield and high fines are directionally motivated but substantially more extrapolative than predictions involving long cooling histories.
