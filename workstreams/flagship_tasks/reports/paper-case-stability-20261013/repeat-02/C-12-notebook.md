# C-12 — model-authored source notebook

Development replication. Each version is the model's scientific account, not verified environment truth. Posttest answers are separate in the JSON record.

## Revision 1

Recorded: 2026-10-13T05:41:49.607909+00:00; public operations available: 0; reviewed through: not specified.

# Pre-experiment hypotheses

H1 [tentative] Solvent S2 should favor larger, purer crystals because its nominal growth is high and occlusion/nucleation are low, but its lower solubility may require a sufficiently hot reaction stage. Prediction: a seeded, slow cool in S2 will meet purity/fines constraints more readily than S0.

H2 [tentative] Catalyst C1 is the safest initial reaction choice from its high nominal activity and moderate variability; C3/S3 may improve conversion but could trade against crystallization quality. Prediction: high-temperature reaction with near-full reagent/catalyst loading, then controlled seeded cooling and a cold hold, will exceed 0.10 crystal recovery.

Decision plan: begin with C1/S2, moderate seed, slow cooling and cold hold; vary solvent/catalyst, seed dose, cooling rate/hold, and upstream loading across later independent batches. Analytical observations will override dossier priors.

---

## Revision 2

Recorded: 2026-10-13T05:44:23.549040+00:00; public operations available: 109; reviewed through: runner-operation-0109.

# Working hypotheses after batches 1–6

H1 [supported only qualitatively] S2 is the best tested solvent for particle quality. The S2 process with 0.05 g seed and slow cooling/aging gave final fines about 0.59 (runner-operation-0030), versus about 1.0 in S1 under a related long-aging process (runner-operation-0089). This is a large numerical contrast, but protocols are not identical and there is no replicate uncertainty estimate.

H2 [revised] Seed dose has a nonmonotone effect. Relative to 0.05 g seed (runner-operation-0030), 0.005 g (runner-operation-0049) and 0.20 g (runner-operation-0070) both produced very high fines; low dose likely fails to suppress secondary nucleation while excessive seed adds too many small particles. I will search near 0.03–0.06 g rather than increase dose broadly.

H3 [unresolved] A partial-dissolution/recrystallization cycle may selectively remove fines. One 305 K reheat/recool in S2 remained just above the fines constraint (runner-operation-0109), so the tested cycle is insufficient but does not exclude a stronger or repeated cycle.

Reaction note: C1/S1 gave higher reaction selectivity and crystallization recovery than C1/S2, but its fines failed badly. Since purity has comfortably exceeded 0.80 in all completed trials, the immediate decision criterion is crossing fines <=0.50; afterward optimize recovery. Next test: S2, seed near 0.05 g, stronger/repeated warm ripening before final slow recooling.

---

## Revision 3

Recorded: 2026-10-13T05:47:22.534810+00:00; public operations available: 256; reviewed through: runner-operation-0256.

# Final source-stage conclusions

H1 [supported in tested scope] S2 was the most promising tested crystallization solvent for suppressing fines, but no completed batch met the required fines fraction <=0.50. All final crystal purities exceeded 0.80, so the binding failure was particle-size distribution rather than purity.

H2 [supported qualitatively, optimum unresolved] Moderate seeding was necessary: both very low and excessive seed doses gave much worse fines than doses near 0.03–0.05 g. The best region remained around 0.03–0.05 g, but the tested changes did not cross specification.

H3 [rejected for tested implementations] Reheat/recool and post-filtration resuspension did not provide a clear fines advantage (runner-operation-0143). Strong final warming without recooling was especially adverse, giving fines 1.0 and lower recovery (runner-operation-0256). This does not exclude a narrower selective-dissolution window, but it should not be claimed from these data.

Selection decision: no batch is specification-feasible. Batches 7 and 11 had numerically similar best fines outcomes (~0.575 and ~0.587; runner-operation-0143 and runner-operation-0232); their difference is smaller than the scale suggested by the declared per-assay fines noise, so I do not treat it as evidence that batch 7 is superior. Batch 11 is the preferred fallback because it combines high purity (~0.995) and higher recovery (~0.448) with one of the lowest observed fines values, using the simpler S2/C1, 0.03 g seed, deep-cool/long-age process. The recommendation must clearly state that its fines result remains out of specification.

---
